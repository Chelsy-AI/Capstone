import customtkinter as ctk
import tkinter as tk  # for StringVar
from core.theme import LIGHT_THEME, DARK_THEME
from features.tomorrows_guess.display import create_tomorrow_guess_frame, update_tomorrow_guess_display
from features.tomorrows_guess.predictor import get_tomorrows_prediction


def build_gui(app):
    """
    Build the complete weather app GUI using customtkinter.
    Clears all existing widgets before rebuilding (useful for theme toggling).
    """

    # --- Clear any previous widgets (e.g., for theme toggling) ---
    for widget in app.winfo_children():
        widget.destroy()

    # Set appearance mode (light/dark)
    ctk.set_appearance_mode(ctk.get_appearance_mode())

    # Set window background color
    app.configure(fg_color=app.theme["bg"])

    # --- Main container frame ---
    app.parent_frame = ctk.CTkFrame(app, fg_color=app.theme["bg"])
    app.parent_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # --- Theme toggle button ---
    theme_btn = ctk.CTkButton(
        master=app,
        text="Toggle Theme",
        command=app.toggle_theme,
        fg_color=app.theme["button_bg"],
        text_color=app.theme["button_fg"],
        width=120
    )
    theme_btn.pack(pady=10)

    # --- City input field ---
    app.city_entry = ctk.CTkEntry(
        master=app,
        textvariable=app.city_var,
        font=("Arial", 24, "bold"),
        width=300,
        fg_color="transparent",
        border_width=0,
        justify="center",
        text_color=app.theme["fg"]
    )
    app.city_entry.pack(pady=(10, 20))
    app.city_entry.bind("<Return>", lambda e: app.update_weather())  # Trigger update on Enter key

    # --- Main weather icon ---
    app.icon_label = ctk.CTkLabel(app, text="", image=None)
    app.icon_label.pack(pady=5)

    # --- Frame for all metric icons/labels ---
    features_frame = ctk.CTkFrame(app.parent_frame, fg_color=app.theme["bg"])
    features_frame.pack(pady=(10, 20), fill="x")

    # Initialize dictionary to store metric value labels
    app.metric_value_labels = {}

    # Define weather metrics to display
    features = [
        ("humidity", "💧", "Humidity"),
        ("wind", "💨", "Wind"),
        ("pressure", "🧭", "Pressure"),
        ("visibility", "👁️", "Visibility"),
        ("uv", "🌞", "UV Index"),
        ("precipitation", "🌧️", "Precipitation"),
    ]

    # Configure equal spacing across all metric columns
    features_frame.grid_columnconfigure(tuple(range(len(features))), weight=1, uniform="metrics")

    # --- Create metric cards (icon + value) ---
    for col, (key, icon, label_text) in enumerate(features):
        frame = ctk.CTkFrame(
            features_frame,
            fg_color=app.theme["text_bg"],
            corner_radius=8
        )
        frame.grid(row=0, column=col, padx=6, pady=5, sticky="nsew")  # Equal-sized cards

        # Metric label (e.g., "Humidity")
        label_title = ctk.CTkLabel(
            frame,
            text=label_text,
            text_color=app.theme["text_fg"],
            font=("Arial", 14)
        )
        label_title.pack(pady=(5, 0))

        # Emoji icon for the metric
        label_icon = ctk.CTkLabel(
            frame,
            text=icon,
            font=("Arial", 24)
        )
        label_icon.pack()

        # Metric value (e.g., "45%")
        value_label = ctk.CTkLabel(
            frame,
            text="--",
            text_color=app.theme["text_fg"],
            font=("Arial", 16)
        )
        value_label.pack(pady=(0, 5))

        # Save reference to label for live updates
        app.metric_value_labels[key] = value_label

    # --- Temperature display (clickable to toggle unit) ---
    app.temp_label = ctk.CTkLabel(
        master=app,
        text="--",
        font=("Arial", 32),
        text_color=app.theme["fg"],
        cursor="hand2"
    )
    app.temp_label.pack(pady=5)
    app.temp_label.bind("<Button-1>", lambda e: app.toggle_temp_unit())  # Toggle °C/°F on click

    # --- Weather description (e.g., "Sunny") ---
    app.desc_label = ctk.CTkLabel(
        master=app,
        text="",
        font=("Arial", 20),
        text_color=app.theme["fg"]
    )
    app.desc_label.pack(pady=5)

    # --- Last updated timestamp ---
    app.update_label = ctk.CTkLabel(
        master=app,
        text="",
        font=("Arial", 14),
        text_color=app.theme["fg"]
    )
    app.update_label.pack(pady=5)

    # --- Button to show 7-day history ---
    app.show_history_button = ctk.CTkButton(
        master=app,
        text="Show History",
        command=app.update_weather_history,
        fg_color=app.theme["button_bg"],
        text_color=app.theme["button_fg"],
        width=120
    )
    app.show_history_button.pack(pady=(10, 10))

    # --- Tomorrow's Guess Frame ---
    app.tomorrow_guess_frame = create_tomorrow_guess_frame(app.parent_frame, app.theme)

    # --- Initial weather fetch (optional on rebuild) ---
    app.update_weather()
