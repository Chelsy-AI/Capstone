# core/gui.py

import customtkinter as ctk
from PIL import Image, ImageTk
from customtkinter import CTkImage
from core.api import get_detailed_environmental_data
from core.processor import extract_weather_details

# Builds the complete GUI layout and attaches all components to the main app window
def build_gui(app):
    # --- Clear previous widgets (for theme toggling) ---
    for widget in app.root.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app.root.configure(fg_color=app.theme["bg"])

    # --- Frame to hold horizontal weather feature boxes ---
    parent_frame = ctk.CTkFrame(app.root, fg_color=app.theme["bg"])
    parent_frame.pack(pady=10, fill="x")

    # --- Theme Toggle Button ---
    theme_btn = ctk.CTkButton(
        master=app.root,
        text="Toggle Theme",
        command=app.toggle_theme,
        fg_color=app.theme["button_bg"],
        text_color=app.theme["button_fg"],
        width=120
    )
    theme_btn.pack(pady=10)

    # --- City Input Field ---
    app.city_entry = ctk.CTkEntry(
        master=app.root,
        textvariable=app.city_var,
        font=("Arial", 24, "bold"),
        width=300,
        fg_color="transparent",
        border_width=0,
        justify="center",
        text_color=app.theme["fg"]
    )
    app.city_entry.pack(pady=(10, 20))
    app.city_entry.bind("<Return>", lambda e: app.fetch_and_display())

    # --- Weather Icon Placeholder ---
    app.icon_label = ctk.CTkLabel(app.root, text="", image=None)
    app.icon_label.configure(text="")  # Avoid any default text
    app.icon_label.pack(pady=5)

    # Initialize icon image and angle if not already defined
    if not hasattr(app, "icon_rotation_angle"):
        app.icon_rotation_angle = 0
    if not hasattr(app, "weather_icon_img_original"):
        app.weather_icon_img_original = Image.new("RGBA", (64, 64), (0, 0, 0, 0))

    # --- Create Feature Boxes for Weather Stats ---
    features = [
        ("Hum", "💧", "humidity_label"),
        ("Wind", "🌬", "wind_label"),
        ("Press", "🔵", "pressure_label"),
        ("Vis", "👁️", "visibility_label"),
        ("UV", "☀️", "uv_label"),
        ("Pollen", "🌸", "pollen_label"),
        ("Bug", "🐞", "bug_label"),
        ("Precip", "☔", "precipitation_label"),
    ]

    for fname, icon, attr_name in features:
        frame = ctk.CTkFrame(parent_frame, width=80, height=100, fg_color=app.theme["text_bg"])
        frame.pack(side="left", padx=5)

        label_name = ctk.CTkLabel(frame, text=fname, text_color=app.theme["text_fg"], font=("Arial", 14))
        label_name.pack(pady=(5,0))

        label_icon = ctk.CTkLabel(frame, text=icon, font=("Arial", 24))
        label_icon.pack()

        label_value = ctk.CTkLabel(frame, text="", text_color=app.theme["text_fg"], font=("Arial", 16))
        label_value.pack(pady=(0,5))

        setattr(app, attr_name, label_value)

    # --- Fetch current weather data and populate labels ---
        data = get_detailed_environmental_data(app.city_var.get())
    if data:
        weather = extract_weather_details(data)
        app.humidity_label.configure(text=f"Humidity: {weather['humidity']}%")
        app.wind_label.configure(text=f"Wind: {weather['wind']} km/h")
        app.pressure_label.configure(text=f"Pressure: {weather['pressure']} hPa")
        app.visibility_label.configure(text=f"Visibility: {weather['visibility']} m")
        app.uv_label.configure(text=f"UV Index: {weather['uv']}")
        app.precipitation_label.configure(text=f"Precipitation: {weather['precipitation']} mm")
        app.pollen_label.configure(text=f"Pollen: {weather['pollen']}")
    else:
        print("No weather data found")

    # --- Icon Rotation Animation ---
    def rotate_icon():
        rotated = app.weather_icon_img_original.rotate(app.icon_rotation_angle)
        app.weather_icon_img = CTkImage(light_image=rotated, size=(64, 64))
        app.icon_label.configure(image=app.weather_icon_img)
        app.icon_rotation_angle = (app.icon_rotation_angle + 10) % 360
        app.root.after(100, rotate_icon)

    rotate_icon()

    # --- Temperature Label with Unit Toggle on Click ---
    app.temp_label = ctk.CTkLabel(
        master=app.root,
        text="",
        font=("Arial", 32),
        text_color=app.theme["fg"],
        cursor="hand2"
    )
    app.temp_label.pack(pady=5)
    app.temp_label.bind("<Button-1>", lambda e: toggle_unit(app))

    # --- Weather Description Label ---
    app.desc_label = ctk.CTkLabel(
        master=app.root,
        text="",
        font=("Arial", 20),
        text_color=app.theme["fg"]
    )
    app.desc_label.pack(pady=5)

    # --- Last Updated Timestamp Label ---
    app.update_label = ctk.CTkLabel(
        master=app.root,
        text="",
        font=("Arial", 14),
        text_color=app.theme["fg"]
    )
    app.update_label.pack(pady=5)

    # --- History Text Display Box ---
    app.history_text = ctk.CTkTextbox(
        master=app.root,
        height=150,
        width=500,
        fg_color=app.theme["text_bg"],
        text_color=app.theme["text_fg"]
    )
    app.history_text.pack(pady=10)

    # --- Show History Button ---
    history_btn = ctk.CTkButton(
        master=app.root,
        text="Show History",
        command=app.show_weather_history,
        fg_color=app.theme["button_bg"],
        text_color=app.theme["button_fg"],
        width=120
    )
    history_btn.pack(pady=10)

    # --- Initial Fetch to Populate UI ---
    app.update_weather_display()

# Toggles temperature unit between Celsius and Fahrenheit and updates display
def toggle_unit(app):
    app.unit = "F" if app.unit == "C" else "C"
    app.update_weather_display()
