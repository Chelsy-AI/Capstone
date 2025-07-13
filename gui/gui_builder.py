import customtkinter as ctk
from features.tomorrows_guess.display import create_tomorrow_guess_frame, update_tomorrow_guess_display
import threading
from gui.animation_gui import SmartBackground
import tkinter as tk  



def build_gui(app):
    """
    Build the complete GUI layout for the Weather App with animated smart background.
    """

    # Clear all existing widgets before rebuilding
    for widget in app.winfo_children():
        widget.destroy()

    # Create canvas to hold scrollable content FIRST
    canvas = ctk.CTkCanvas(app, bg="#87CEEB", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    app.bg_canvas = canvas

    # Initialize smart background, passing the canvas
    if not hasattr(app, 'smart_background'):
        app.smart_background = SmartBackground(app, canvas)

    # Get initial theme from smart background
    initial_theme = app.smart_background.get_adaptive_theme()
    if hasattr(app, 'theme') and isinstance(app.theme, dict):
        app.theme.update(initial_theme)
    else:
        app.theme = initial_theme

    # Update canvas background color from theme
    canvas.configure(bg=app.theme.get("bg", "#87CEEB"))

    # Add vertical scrollbar for canvas
    scrollbar = ctk.CTkScrollbar(
        app,
        orientation="vertical",
        command=canvas.yview,
        fg_color=app.theme.get("text_bg", "#F0F0F0"),
        button_color=app.theme.get("button_bg", "#4169E1"),
    )
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create scrollable frame inside the canvas
    scrollable_frame = ctk.CTkFrame(canvas, fg_color=app.theme.get("bg", "#87CEEB"))
    window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Configure scroll region whenever the scrollable_frame size changes
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Adjust the scrollable frame's width to match canvas width on resize
    def on_canvas_configure(event):
        canvas.itemconfig(window, width=event.width)
    canvas.bind("<Configure>", on_canvas_configure)

    # Enable scrolling with mouse wheel (Windows & Mac support)
    def on_mouse_wheel(event):
        delta = -1 * (event.delta // 120)  # For Windows
        canvas.yview_scroll(delta, "units")
    # MacOS uses different mouse wheel event names; bind both
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # scroll up (Linux)
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # scroll down (Linux)

    # Initialize smart background with current weather condition after a short delay
    def init_background():
        current_condition = getattr(app, 'current_weather_condition', 'clear')
        app.smart_background.start_animation(current_condition)
        app.after(200, app.smart_background.lower_background)

    app.after(200, init_background)

    row = 0

    # === WEATHER METRICS SECTION ===
    features_frame = ctk.CTkFrame(scrollable_frame, fg_color=app.theme["bg"])
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
        frame = ctk.CTkFrame(features_frame, fg_color=app.theme["text_bg"], corner_radius=8)
        frame.grid(row=0, column=col, padx=6, pady=5, sticky="nsew")

        ctk.CTkLabel(frame, text=label_text, text_color=app.theme["text_fg"], font=("Arial", 14)).pack(pady=(5, 0))
        ctk.CTkLabel(frame, text=icon, font=("Arial", 24), text_color=app.theme["text_fg"]).pack()
        value_label = ctk.CTkLabel(frame, text="--", text_color=app.theme["text_fg"], font=("Arial", 16))
        value_label.pack(pady=(0, 5))
        app.metric_value_labels[key] = value_label

    row += 1

    # === THEME TOGGLE BUTTON ===
    theme_btn = ctk.CTkButton(
        scrollable_frame,
        text="Toggle Theme",
        command=app.toggle_theme,
        fg_color=app.theme["button_bg"],
        text_color=app.theme["button_fg"],
        width=120,
    )
    theme_btn.grid(row=row, column=0, pady=10)
    row += 1

    # === CITY INPUT FIELD ===
    app.city_entry = ctk.CTkEntry(
        scrollable_frame,
        textvariable=app.city_var,
        font=("Arial", 24, "bold"),
        width=300,
        fg_color=app.theme["entry_bg"],
        border_width=0,
        justify="center",
        text_color=app.theme["fg"],
    )
    app.city_entry.grid(row=row, column=0, pady=(10, 20))
    app.city_entry.bind("<Return>", lambda e: threading.Thread(target=app.safe_update_weather, daemon=True).start())
    row += 1

    # === TEMPERATURE DISPLAY ===
    app.temp_label = ctk.CTkLabel(
        scrollable_frame,
        text="-- °C",
        font=("Arial", 32),
        text_color=app.theme["fg"],
        cursor="hand2",
    )
    app.temp_label.grid(row=row, column=0, pady=10)
    app.temp_label.bind("<Button-1>", lambda e: app.toggle_temp_unit())
    row += 1

    # === WEATHER DESCRIPTION ===
    app.desc_label = ctk.CTkLabel(scrollable_frame, text="", font=("Arial", 20), text_color=app.theme["fg"])
    app.desc_label.grid(row=row, column=0, pady=5)
    row += 1

    # === LAST UPDATED LABEL ===
    app.update_label = ctk.CTkLabel(scrollable_frame, text="", font=("Arial", 14), text_color=app.theme["fg"])
    app.update_label.grid(row=row, column=0, pady=5)
    row += 1

    # === WEATHER ICON ===
    app.icon_label = ctk.CTkLabel(scrollable_frame, text="", image=None)
    app.icon_label.grid(row=row, column=0, pady=5)
    row += 1

    # === TOMORROW'S PREDICTION FRAME ===
    app.tomorrow_guess_frame = create_tomorrow_guess_frame(scrollable_frame, app.theme)
    app.tomorrow_guess_frame.grid(row=row, column=0, pady=15, sticky="ew")
    update_tomorrow_guess_display(app.tomorrow_guess_frame, "N/A", "N/A", "N/A")
    row += 1

    # === WEATHER HISTORY FRAME ===
    app.history_frame = ctk.CTkFrame(scrollable_frame, fg_color=app.theme["bg"])
    app.history_frame.grid(row=row, column=0, sticky="ew", pady=(10, 20), padx=10)
    row += 1

    scrollable_frame.grid_columnconfigure(0, weight=1)

    # === THREAD-SAFE TOMORROW'S PREDICTION UPDATE ===
    def update_tomorrow_async(city):
        from features.tomorrows_guess.predictor import get_tomorrows_prediction
        predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)

        def update_display():
            update_tomorrow_guess_display(
                app.tomorrow_guess_frame, predicted_temp, confidence, accuracy
            )
        app.after(0, update_display)

    threading.Thread(target=update_tomorrow_async, args=(app.city_var.get(),), daemon=True).start()
