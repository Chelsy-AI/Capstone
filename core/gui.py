import customtkinter as ctk
from core.theme import LIGHT_THEME, DARK_THEME
from core.utils import toggle_unit, toggle_theme


def build_gui(app):
    # Clear previous widgets (for theme toggling)
    for widget in app.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode(ctk.get_appearance_mode())
    app.configure(fg_color=app.theme["bg"])

    # Create main frame
    app.parent_frame = ctk.CTkFrame(app, fg_color=app.theme["bg"])
    app.parent_frame.pack(pady=10, fill="x")

    # Theme toggle button
    theme_btn = ctk.CTkButton(
        master=app,
        text="Toggle Theme",
        command=app.toggle_theme,
        fg_color=app.theme["button_bg"],
        text_color=app.theme["button_fg"],
        width=120
    )
    theme_btn.pack(pady=10)

    # City entry
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
    app.city_entry.bind("<Return>", lambda e: app.update_weather())

    # Weather icon
    app.icon_label = ctk.CTkLabel(app, text="", image=None)
    app.icon_label.pack(pady=5)

    # Create metric labels dictionary
    app.metric_value_labels = {}

    # Feature icons and labels
    features = [
        ("humidity", "💧", "Humidity"),
        ("wind", "💨", "Wind"),
        ("pressure", "🧭", "Pressure"),
        ("visibility", "👁️", "Visibility"),
        ("uv", "🌞", "UV Index"),
        ("precipitation", "🌧️", "Precipitation"),
    ]

    for key, icon, label_text in features:
        frame = ctk.CTkFrame(app.parent_frame, width=80, height=100, fg_color=app.theme["text_bg"])
        frame.pack(side="left", padx=5)

        label_title = ctk.CTkLabel(frame, text=label_text, text_color=app.theme["text_fg"], font=("Arial", 14))
        label_title.pack(pady=(5, 0))

        label_icon = ctk.CTkLabel(frame, text=icon, font=("Arial", 24))
        label_icon.pack()

        value_label = ctk.CTkLabel(frame, text="--", text_color=app.theme["text_fg"], font=("Arial", 16))
        value_label.pack(pady=(0, 5))

        # Store the label in the dictionary
        app.metric_value_labels[key] = value_label

    # Temperature label (clickable to toggle units)
    app.temp_label = ctk.CTkLabel(
        master=app,
        text="",
        font=("Arial", 32),
        text_color=app.theme["fg"],
        cursor="hand2"
    )
    app.temp_label.pack(pady=5)
    app.temp_label.bind("<Button-1>", lambda e: toggle_unit(app))

    # Description label
    app.desc_label = ctk.CTkLabel(
        master=app,
        text="",
        font=("Arial", 20),
        text_color=app.theme["fg"]
    )
    app.desc_label.pack(pady=5)

    # Last update time label
    app.update_label = ctk.CTkLabel(
        master=app,
        text="",
        font=("Arial", 14),
        text_color=app.theme["fg"]
    )
    app.update_label.pack(pady=5)

    # History button
    app.show_history_button = ctk.CTkButton(
        master=app,
        text="Show History",
        command=app.show_weather_history,
        fg_color=app.theme["button_bg"],
        text_color=app.theme["button_fg"],
        width=120
    )
    app.show_history_button.pack(pady=(10, 10))

    # Trigger first weather fetch
    app.update_weather()
