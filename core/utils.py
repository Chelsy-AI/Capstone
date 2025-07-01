import customtkinter as ctk
from core.theme import LIGHT_THEME, DARK_THEME

# Toggle between Celsius and Fahrenheit units
def toggle_unit(current_unit: str) -> str:
    """
    Given a temperature unit string ("°C" or "°F"), returns the toggled unit.
    """
    return "°F" if current_unit == "°C" else "°C"

# Convert Kelvin to Celsius (rounded)
def kelvin_to_celsius(kelvin):
    """
    Convert temperature from Kelvin to Celsius.
    """
    return round(kelvin - 273.15, 1)

# Convert Kelvin to Fahrenheit (rounded)
def kelvin_to_fahrenheit(kelvin):
    """
    Convert temperature from Kelvin to Fahrenheit.
    """
    return round((kelvin - 273.15) * 9 / 5 + 32, 1)

# Format temperature with unit for display
def format_temperature(temp, unit):
    """
    Format temperature value with its unit for display.
    """
    if temp is None:
        return "N/A"
    return f"{temp} {unit}"

# Toggle between light and dark themes for the app and rebuild GUI
def toggle_theme(app):
    """
    Switch between light and dark themes for the app.
    Rebuilds the GUI and refreshes weather data.
    """
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
