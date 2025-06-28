# core/utils.py

import customtkinter as ctk
from core.theme import LIGHT_THEME, DARK_THEME

def toggle_unit(current_unit: str) -> str:
    return "°F" if current_unit == "°C" else "°C"

def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15, 1)

def kelvin_to_fahrenheit(kelvin):
    return round((kelvin - 273.15) * 9 / 5 + 32, 1)

def format_temperature(temp, unit):
    if temp is None:
        return "N/A"
    return f"{temp} {unit}"

def toggle_theme(app):
    app.theme = DARK_THEME if app.theme == LIGHT_THEME else LIGHT_THEME
    ctk.set_appearance_mode("dark" if app.theme == DARK_THEME else "light")
    app.configure(fg_color=app.theme["bg"])
    app.parent_frame.configure(fg_color=app.theme["bg"])

    # Rebuild metrics section
    app.build_metrics_labels()

    # Rebuild entire GUI if necessary
    from core.gui import build_gui  # Avoid circular import on top
    build_gui(app)

    # Refresh content
    app.update_weather()
    app.show_weather_history()
