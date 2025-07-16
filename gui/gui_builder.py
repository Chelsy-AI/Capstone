import customtkinter as ctk
import threading
import tkinter as tk
from features.tomorrows_guess.display import create_tomorrow_guess_frame, update_tomorrow_guess_display


def build_gui(app):
    """
    Build the GUI layout for the Weather App.
    Ensures widgets are stacked above the animated background canvas.
    """

    def get_theme_color(theme, key, fallback="#000000"):
        val = theme.get(key, fallback)
        return val if isinstance(val, str) and val.strip() != "" else fallback

    for widget in app.winfo_children():
        if widget != app.bg_canvas:
            widget.destroy()

    # === Scrollable Canvas Setup ===
    canvas = app.bg_canvas
    canvas.configure(bg=get_theme_color(app.theme, "bg", "#87CEEB"))

    scrollbar = ctk.CTkScrollbar(
        app,
        orientation="vertical",
        command=canvas.yview,
        fg_color=get_theme_color(app.theme, "text_bg", "#F0F0F0"),
        button_color=get_theme_color(app.theme, "button_bg", "#4169E1"),
    )
    scrollbar.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = ctk.CTkFrame(canvas, fg_color=get_theme_color(app.theme, "bg", "#87CEEB"))
    window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_configure(event):
        canvas.itemconfig(window, width=event.width)

    def on_mouse_wheel(event):
        delta = -1 * (event.delta // 120)
        canvas.yview_scroll(delta, "units")

    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_configure)
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Linux support
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    row = 0

    # === Weather Metrics Section ===
    features_frame = ctk.CTkFrame(scrollable_frame, fg_color=get_theme_color(app.theme, "bg", "#ffffff"))
    features_frame.grid(row=row, column=0, sticky="ew", pady=10, padx=10)

    features = [
        ("humidity", "💧", "Humidity"),
        ("wind", "💨", "Wind"),
        ("pressure", "🧭", "Pressure"),
        ("visibility", "👁️", "Visibility"),
        ("uv", "🕶️", "UV Index"),
        ("precipitation", "☔️", "Precipitation"),
    ]
    features_frame.grid_columnconfigure(tuple(range(len(features))), weight=1, uniform="metrics")
    app.metric_value_labels = {}

    for col, (key, icon, label_text) in enumerate(features):
        frame = ctk.CTkFrame(features_frame, fg_color=get_theme_color(app.theme, "text_bg", "#dddddd"), corner_radius=8)
        frame.grid(row=0, column=col, padx=6, pady=5, sticky="nsew")

        ctk.CTkLabel(frame, text=label_text, text_color=get_theme_color(app.theme, "text_fg", "#111111"), font=("Arial", 14)).pack(pady=(5, 0))
        ctk.CTkLabel(frame, text=icon, font=("Arial", 24), text_color=get_theme_color(app.theme, "text_fg", "#111111")).pack()
        value_label = ctk.CTkLabel(frame, text="--", text_color=get_theme_color(app.theme, "text_fg", "#111111"), font=("Arial", 16))
        value_label.pack(pady=(0, 5))
        app.metric_value_labels[key] = value_label

    row += 1

    # === Toggle Theme Button ===
    theme_btn = ctk.CTkButton(
        scrollable_frame,
        text="Toggle Theme",
        command=app.toggle_theme,
        fg_color=get_theme_color(app.theme, "button_bg", "#4169E1"),
        text_color=get_theme_color(app.theme, "button_fg", "#ffffff"),
        width=120,
    )
    theme_btn.grid(row=row, column=0, pady=10)
    row += 1

    # === City Entry ===
    app.city_entry = ctk.CTkEntry(
        scrollable_frame,
        textvariable=app.city_var,
        font=("Arial", 24, "bold"),
        width=300,
        fg_color=get_theme_color(app.theme, "entry_bg", "#f2f2f2"),
        border_width=0,
        justify="center",
        text_color=get_theme_color(app.theme, "fg", "#000000"),
    )
    app.city_entry.grid(row=row, column=0, pady=(10, 20))
    app.city_entry.bind("<Return>", lambda e: threading.Thread(target=app.safe_update_weather, daemon=True).start())
    row += 1

    # === Temperature Label ===
    app.temp_label = ctk.CTkLabel(
        scrollable_frame,
        text="-- °C",
        font=("Arial", 32),
        text_color=get_theme_color(app.theme, "fg", "#000000"),
        cursor="hand2",
    )
    app.temp_label.grid(row=row, column=0, pady=10)
    app.temp_label.bind("<Button-1>", app.toggle_temp_unit)
    row += 1

    # === Description Label ===
    app.desc_label = ctk.CTkLabel(scrollable_frame, text="", font=("Arial", 20), text_color=get_theme_color(app.theme, "fg", "#000000"))
    app.desc_label.grid(row=row, column=0, pady=5)
    row += 1

    # === Update Time Label ===
    app.update_label = ctk.CTkLabel(scrollable_frame, text="", font=("Arial", 14), text_color=get_theme_color(app.theme, "fg", "#000000"))
    app.update_label.grid(row=row, column=0, pady=5)
    row += 1

    # === Weather Icon ===
    app.icon_label = ctk.CTkLabel(scrollable_frame, text="", image=None)
    app.icon_label.grid(row=row, column=0, pady=5)
    row += 1

    # === Tomorrow's Prediction ===
    app.tomorrow_guess_frame = create_tomorrow_guess_frame(scrollable_frame, app.theme)
    app.tomorrow_guess_frame.grid(row=row, column=0, pady=15, sticky="ew")
    update_tomorrow_guess_display(app.tomorrow_guess_frame, "N/A", "N/A", "N/A")
    row += 1

    # === History Frame ===
    app.history_frame = ctk.CTkFrame(scrollable_frame, fg_color=get_theme_color(app.theme, "bg", "#ffffff"))
    app.history_frame.grid(row=row, column=0, sticky="ew", pady=(10, 20), padx=10)
    row += 1

    scrollable_frame.grid_columnconfigure(0, weight=1)
