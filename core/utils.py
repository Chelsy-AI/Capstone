import customtkinter as ctk
from core.theme import LIGHT_THEME, DARK_THEME  # Import our theme dictionaries
from core.gui import build_gui

# ────────────────────────────────────────────────────────────────────────────── 
# UTILITY FUNCTIONS MODULE
# 
# This module contains helper functions used throughout the weather app.
# Utility functions are small, focused functions that perform specific tasks
# and can be reused in different parts of the application.
# ────────────────────────────────────────────────────────────────────────────── 

# ────────────────────────────────────────────────────────────────────────────── 
# TEMPERATURE UTILITIES
# ────────────────────────────────────────────────────────────────────────────── 

def toggle_unit(current_unit: str) -> str:
    """
    Switch between Celsius and Fahrenheit temperature units.
    
    This is a simple toggle function - if current unit is Celsius, 
    it returns Fahrenheit, and vice versa.
    
    """
    # Use a ternary operator (shorthand if/else) to toggle
    return "°F" if current_unit == "°C" else "°C"

def kelvin_to_celsius(kelvin):
    """
    Convert temperature from Kelvin to Celsius.
    
    Kelvin is the scientific temperature scale where 0K = absolute zero.
    Many weather APIs return temperatures in Kelvin.
    
    Formula: Celsius = Kelvin - 273.15
    
    """
    # Handle invalid input
    if kelvin is None or not isinstance(kelvin, (int, float)):
        return None
    
    try:
        # Apply the conversion formula and round to 1 decimal place
        celsius = kelvin - 273.15
        return round(celsius, 1)
    except (TypeError, ValueError):
        # Handle any conversion errors
        return None

def kelvin_to_fahrenheit(kelvin):
    """
    Convert temperature from Kelvin to Fahrenheit.
    
    This does the conversion in two steps:
    1. Convert Kelvin to Celsius
    2. Convert Celsius to Fahrenheit
    
    Formula: Fahrenheit = (Kelvin - 273.15) × 9/5 + 32
    
    """
    # Handle invalid input
    if kelvin is None or not isinstance(kelvin, (int, float)):
        return None
    
    try:
        # Convert Kelvin to Celsius, then Celsius to Fahrenheit
        celsius = kelvin - 273.15
        fahrenheit = celsius * 9 / 5 + 32
        return round(fahrenheit, 1)
    except (TypeError, ValueError):
        # Handle any conversion errors
        return None

def celsius_to_fahrenheit(celsius):
    """
    Convert temperature from Celsius to Fahrenheit.
    
    This is useful when you already have Celsius and need Fahrenheit.
    
    Formula: Fahrenheit = (Celsius × 9/5) + 32
    
    """
    if celsius is None or not isinstance(celsius, (int, float)):
        return None
    
    try:
        fahrenheit = celsius * 9 / 5 + 32
        return round(fahrenheit, 1)
    except (TypeError, ValueError):
        return None

def fahrenheit_to_celsius(fahrenheit):
    """
    Convert temperature from Fahrenheit to Celsius.
    
    Formula: Celsius = (Fahrenheit - 32) × 5/9
    
    """
    if fahrenheit is None or not isinstance(fahrenheit, (int, float)):
        return None
    
    try:
        celsius = (fahrenheit - 32) * 5 / 9
        return round(celsius, 1)
    except (TypeError, ValueError):
        return None

def format_temperature(temp, unit):
    """
    Format temperature value with its unit for display in the GUI.
    
    This function ensures temperature is displayed consistently
    throughout the app, with proper handling of missing data.
    
    """
    # Handle missing or invalid temperature data
    if temp is None:
        return "N/A"
    
    # Handle case where temp might be a string "N/A"
    if isinstance(temp, str):
        return temp
    
    try:
        # Format the temperature with the unit
        # This ensures consistent display format
        return f"{temp} {unit}"
    except (TypeError, ValueError):
        return "N/A"

# ────────────────────────────────────────────────────────────────────────────── 
# THEME UTILITIES
# ────────────────────────────────────────────────────────────────────────────── 

def toggle_theme(app):
    """
    Switch between light and dark themes for the entire application.
    
    This function:
    1. Changes the app's theme data
    2. Updates CustomTkinter's appearance mode
    3. Rebuilds the GUI with new colors
    4. Refreshes all displayed data
    
    Args:
        app: Main application object containing theme and GUI references
    """
    try:
        # --- DETERMINE NEW THEME ---
        # Switch to the opposite theme
        if app.theme == LIGHT_THEME:
            app.theme = DARK_THEME
            new_mode = "dark"
        else:
            app.theme = LIGHT_THEME
            new_mode = "light"
        
        # --- UPDATE CUSTOMTKINTER APPEARANCE ---
        # This changes the overall look of CustomTkinter widgets
        ctk.set_appearance_mode(new_mode)
        
        # --- UPDATE MAIN WINDOW COLORS ---
        # Configure the main app window with new background color
        app.configure(fg_color=app.theme["bg"])
        
        # Update parent frame if it exists
        if hasattr(app, 'parent_frame') and app.parent_frame:
            app.parent_frame.configure(fg_color=app.theme["bg"])
        
        # --- REBUILD GUI COMPONENTS ---
        # Rebuild metrics labels with new theme
        if hasattr(app, 'build_metrics_labels'):
            app.build_metrics_labels()
                
        # --- REFRESH DISPLAYED DATA ---
        # Update weather display with new theme
        if hasattr(app, 'update_weather'):
            app.update_weather()
        
        # Refresh weather history display
        if hasattr(app, 'show_weather_history'):
            app.show_weather_history()
    except Exception as e:
        print(f"Error toggling theme: {e}")

# ────────────────────────────────────────────────────────────────────────────── 
# VALIDATION UTILITIES
# ────────────────────────────────────────────────────────────────────────────── 

def validate_city_name(city_name):
    """
    Validate that a city name is reasonable for API requests.
    
    """
    if not city_name:
        return False, "City name cannot be empty"
    
    # Remove extra whitespace
    city_name = city_name.strip()
    
    if len(city_name) < 2:
        return False, "City name must be at least 2 characters long"
    
    if len(city_name) > 100:
        return False, "City name is too long"
    
    # Check for basic valid characters (letters, spaces, hyphens, apostrophes)
    import re
    if not re.match(r"^[a-zA-Z\s\-'.,]+$", city_name):
        return False, "City name contains invalid characters"
    
    return True, ""

def safe_get_nested_value(data, keys, default=None):
    """
    Safely get a value from nested dictionaries without crashing.
    
    This is like doing data["key1"]["key2"]["key3"] but won't crash
    if any of the keys don't exist.
    
    """
    try:
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    except (TypeError, KeyError):
        return default

# ────────────────────────────────────────────────────────────────────────────── 
# STRING UTILITIES
# ────────────────────────────────────────────────────────────────────────────── 

def capitalize_words(text):
    """
    Capitalize each word in a string properly.
    
    Better than .title() because it handles apostrophes correctly.
    
    """
    if not text:
        return ""
    
    # Split into words and capitalize each one
    words = text.split()
    capitalized_words = []
    
    for word in words:
        # Handle hyphenated words
        if '-' in word:
            parts = word.split('-')
            capitalized_parts = [part.capitalize() for part in parts]
            capitalized_words.append('-'.join(capitalized_parts))
        else:
            capitalized_words.append(word.capitalize())
    
    return ' '.join(capitalized_words)
