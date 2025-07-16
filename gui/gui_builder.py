import customtkinter as ctk
import threading
from tkinter import Frame
from features.tomorrows_guess.display import create_tomorrow_guess_frame, update_tomorrow_guess_display


def build_gui(app):
    """
    Build and layout all foreground widgets above the animated background.
    """

    def get_theme_color(theme, key, fallback="#000000"):
        val = theme.get(key, fallback)
        return val if isinstance(val, str) and val.strip() else fallback

    # Destroy old widgets, but not the background canvas
    for widget in app.winfo_children():
        if widget != app.bg_canvas:
            widget.destroy()

    # === Scrollable content on top of canvas ===
    app.scroll_canvas = app.bg_canvas  # reference it explicitly

    scrollable_container = ctk.CTkFrame(app, fg_color="transparent")
    scrollable_container.place(x=0, y=0, relwidth=1, relheight=1)
    scrollable_container.lift()

    scrollbar = ctk.CTkScrollbar(scrollable_container, orientation="vertical")
    scrollbar.pack(side="right", fill="y")

    scroll_canvas = ctk.CTkCanvas(
        scrollable_container,
        bg=get_theme_color(app.theme, "bg", "#FFFFFF"),
        highlightthickness=0,
        yscrollcommand=scrollbar.set,
    )
    scroll_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.configure(command=scroll_canvas.yview)

    # Frame inside canvas for scrollable content
    scrollable_frame = ctk.CTkFrame(scroll_canvas, fg_color=get_theme_color(app.theme, "bg", "#FFFFFF"))
    window_id = scroll_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_frame_configure(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    def on_canvas_configure(event):
        scroll_canvas.itemconfig(window_id, width=event.width)

    scrollable_frame.bind("<Configure>", on_frame_configure)
    scroll_canvas.bind("<Configure>", on_canvas_configure)
    scroll_canvas.bind_all("<MouseWheel>", lambda e: scroll_canvas.yview_scroll(-1 * (e.delta // 120), "units"))

    # === Layout widgets ===
    row = 0
    app.metric_value_labels = {}

    # Weather Metrics
    features_frame = ctk.CTkFrame(scrollable_frame, fg_color=get_theme_color(app.theme, "text_bg", "#F5F5F5"))
    features_frame.grid(row=row, column=0, padx=10, pady=(20, 10), sticky="ew")
    features_frame.grid_columnconfigure(tuple(range(6)), weight=1)

    features = [
        ("humidity", "💧", "Humidity"),
        ("wind", "💨", "Wind"),
        ("pressure", "🧭", "Pressure"),
        ("visibility", "👁️", "Visibility"),
        ("uv", "🕶️", "UV Index"),
        ("precipitation", "☔️", "Precipitation"),
    ]

    for col, (key, icon, label) in enumerate(features):
        box = ctk.CTkFrame(features_frame, fg_color=get_theme_color(app.theme, "text_bg", "#EEEEEE"))
        box.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        ctk.CTkLabel(box, text=label, font=("Arial", 12)).pack(pady=(5, 0))
        ctk.CTkLabel(box, text=icon, font=("Arial", 20)).pack()
        value = ctk.CTkLabel(box, text="--", font=("Arial", 14))
        value.pack(pady=(0, 5))
        app.metric_value_labels[key] = value

    row += 1

    # Theme Button
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

    # City Entry
    app.city_entry = ctk.CTkEntry(
        scrollable_frame,
        textvariable=app.city_var,
        font=("Arial", 24),
        width=300,
        justify="center",
        fg_color=get_theme_color(app.theme, "entry_bg", "#FFFFFF"),
        text_color=get_theme_color(app.theme, "fg", "#000000"),
    )
    app.city_entry.grid(row=row, column=0, pady=10)
    app.city_entry.bind("<Return>", lambda e: threading.Thread(target=app.safe_update_weather, daemon=True).start())
    row += 1

    # Temperature Label
    app.temp_label = ctk.CTkLabel(
        scrollable_frame,
        text="-- °C",
        font=("Arial", 36, "bold"),
        text_color=get_theme_color(app.theme, "fg", "#000000"),
        cursor="hand2"
    )
    app.temp_label.grid(row=row, column=0, pady=10)
    app.temp_label.bind("<Button-1>", app.toggle_temp_unit)
    row += 1

    # Description Label
    app.desc_label = ctk.CTkLabel(scrollable_frame, text="", font=("Arial", 20), text_color=get_theme_color(app.theme, "fg", "#000000"))
    app.desc_label.grid(row=row, column=0, pady=5)
    row += 1

    # Update Time Label
    app.update_label = ctk.CTkLabel(scrollable_frame, text="", font=("Arial", 14), text_color=get_theme_color(app.theme, "fg", "#000000"))
    app.update_label.grid(row=row, column=0, pady=5)
    row += 1

    # Weather Icon
    app.icon_label = ctk.CTkLabel(scrollable_frame, text="", image=None)
    app.icon_label.grid(row=row, column=0, pady=5)
    row += 1

    # Tomorrow's Prediction
    app.tomorrow_guess_frame = create_tomorrow_guess_frame(scrollable_frame, app.theme)
    app.tomorrow_guess_frame.grid(row=row, column=0, pady=15)
    update_tomorrow_guess_display(app.tomorrow_guess_frame, "N/A", "N/A", "N/A")
    row += 1

    # History Frame
    app.history_frame = ctk.CTkFrame(scrollable_frame, fg_color=get_theme_color(app.theme, "bg", "#ffffff"))
    app.history_frame.grid(row=row, column=0, sticky="ew", pady=(10, 20), padx=10)
    row += 1

    scrollable_frame.grid_columnconfigure(0, weight=1)
