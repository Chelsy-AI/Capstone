"""
UTILITY FUNCTIONS MODULE
 
This module contains helper functions used throughout the weather app.
Utility functions are small, focused functions that perform specific tasks
and can be reused in different parts of the application.
"""

import re
from typing import Union, Tuple, Optional

# TEMPERATURE UTILITIES

def toggle_unit(current_unit: str) -> str:
    """
    Switch between Celsius and Fahrenheit temperature units.
    
    This is a simple toggle function - if current unit is Celsius, 
    it returns Fahrenheit, and vice versa.
    
    Args:
        current_unit (str): Current temperature unit ("°C" or "°F")
        
    Returns:
        str: The opposite temperature unit
    """
    # Use a ternary operator to toggle between units
    return "°F" if current_unit == "°C" else "°C"


def kelvin_to_celsius(kelvin: Optional[Union[int, float]]) -> Optional[float]:
    """
    Convert temperature from Kelvin to Celsius.
        
    Formula: Celsius = Kelvin - 273.15
    
    Args:
        kelvin: Temperature in Kelvin (can be int, float, or None)
        
    Returns:
        float: Temperature in Celsius rounded to 1 decimal place, or None if invalid input
    """
    # Quick check for invalid input - return None immediately if bad data
    if kelvin is None or not isinstance(kelvin, (int, float)):
        return None
    
    try:
        # Apply the conversion formula and round to 1 decimal place
        celsius = kelvin - 273.15
        return round(celsius, 1)
    except (TypeError, ValueError):
        # Handle any unexpected conversion errors
        return None


def kelvin_to_fahrenheit(kelvin: Optional[Union[int, float]]) -> Optional[float]:
    """
    Convert temperature from Kelvin to Fahrenheit.
    
    This does the conversion in two steps:
    1. Convert Kelvin to Celsius
    2. Convert Celsius to Fahrenheit
    
    Formula: Fahrenheit = (Kelvin - 273.15) × 9/5 + 32
    
    Args:
        kelvin: Temperature in Kelvin (can be int, float, or None)
        
    Returns:
        float: Temperature in Fahrenheit rounded to 1 decimal place, or None if invalid input
    """
    # Quick check for invalid input
    if kelvin is None or not isinstance(kelvin, (int, float)):
        return None
    
    try:
        # More efficient: do conversion in one step instead of calling kelvin_to_celsius first
        fahrenheit = (kelvin - 273.15) * 9 / 5 + 32
        return round(fahrenheit, 1)
    except (TypeError, ValueError):
        # Handle any conversion errors
        return None


def celsius_to_fahrenheit(celsius: Optional[Union[int, float]]) -> Optional[float]:
    """
    Convert temperature from Celsius to Fahrenheit.
        
    Formula: Fahrenheit = (Celsius × 9/5) + 32
    
    Args:
        celsius: Temperature in Celsius (can be int, float, or None)
        
    Returns:
        float: Temperature in Fahrenheit rounded to 1 decimal place, or None if invalid input
    """
    # Check for invalid input first
    if celsius is None or not isinstance(celsius, (int, float)):
        return None
    
    try:
        # Apply Celsius to Fahrenheit conversion formula
        fahrenheit = celsius * 9 / 5 + 32
        return round(fahrenheit, 1)
    except (TypeError, ValueError):
        return None


def fahrenheit_to_celsius(fahrenheit: Optional[Union[int, float]]) -> Optional[float]:
    """
    Convert temperature from Fahrenheit to Celsius.
    
    Formula: Celsius = (Fahrenheit - 32) × 5/9
    
    Args:
        fahrenheit: Temperature in Fahrenheit (can be int, float, or None)
        
    Returns:
        float: Temperature in Celsius rounded to 1 decimal place, or None if invalid input
    """
    # Check for invalid input first
    if fahrenheit is None or not isinstance(fahrenheit, (int, float)):
        return None
    
    try:
        # Apply Fahrenheit to Celsius conversion formula
        celsius = (fahrenheit - 32) * 5 / 9
        return round(celsius, 1)
    except (TypeError, ValueError):
        return None


def format_temperature(temp: Union[float, int, str, None], unit: str) -> str:
    """
    Format temperature value with its unit for display in the GUI.
    
    This function ensures temperature is displayed consistently
    throughout the app, with proper handling of missing data.
    
    Args:
        temp: Temperature value (number, string, or None)
        unit: Temperature unit ("C", "F", "°C", "°F")
        
    Returns:
        str: Formatted temperature string like "25.5 °C" or "N/A" if invalid
    """
    # Handle missing or invalid temperature data quickly
    if temp is None:
        return "N/A"
    
    # Handle case where temp might already be a string "N/A"
    if isinstance(temp, str):
        return temp
    
    try:
        # Ensure unit has degree symbol for consistency
        if unit in ("C", "F"):
            unit = f"°{unit}"
        
        # Format the temperature with the unit
        # This ensures consistent display format throughout the app
        return f"{temp} {unit}"
    except (TypeError, ValueError):
        return "N/A"

# VALIDATION UTILITIES

def validate_city_name(city_name: str) -> Tuple[bool, str]:
    """
    Validate that a city name is reasonable for API requests.
    
    This function checks if a city name meets basic requirements:
    - Not empty
    - Reasonable length (2-100 characters)
    - Contains only valid characters (letters, spaces, hyphens, apostrophes, etc.)
    
    Args:
        city_name (str): The city name to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
               If valid: (True, "")
               If invalid: (False, "Error description")
    """
    # Check if city name exists and is not empty
    if not city_name:
        return False, "City name cannot be empty"
    
    # Remove extra whitespace for better validation
    city_name = city_name.strip()
    
    # Check minimum length (need at least 2 characters)
    if len(city_name) < 2:
        return False, "City name must be at least 2 characters long"
    
    # Check maximum length (prevent extremely long inputs)
    if len(city_name) > 100:
        return False, "City name is too long"
    
    # Check for valid characters using regular expression
    # Allow: letters, spaces, hyphens, apostrophes, commas, periods
    if not re.match(r"^[a-zA-Z\s\-'.,]+$", city_name):
        return False, "City name contains invalid characters"
    
    # If all checks pass, the city name is valid
    return True, ""


def safe_get_nested_value(data: dict, keys: list, default=None):
    """
    Safely get a value from nested dictionaries without crashing.
    
    Args:
        data (dict): The dictionary to search in
        keys (list): List of keys to traverse (like ["weather", "main", "temp"])
        default: Value to return if any key is missing (default: None)
        
    Returns:
        The value if found, otherwise the default value
    """
    try:
        # Start at the top level of the data
        current = data
        
        # Walk through each key in the path
        for key in keys:
            # Check if current level is a dictionary and has the key
            if isinstance(current, dict) and key in current:
                current = current[key]  # Move deeper into the nested structure
            else:
                # Key not found at this level, return default
                return default
        
        # Successfully found the value
        return current
    except (TypeError, KeyError):
        # Handle any unexpected errors by returning default
        return default

# STRING UTILITIES

def capitalize_words(text: str) -> str:
    """
    Capitalize each word in a string properly.
    
    Args:
        text (str): The text to capitalize
        
    Returns:
        str: Text with each word capitalized, empty string if input is empty
    """
    # Handle empty or None input
    if not text:
        return ""
    
    # Split into individual words (separated by spaces)
    words = text.split()
    capitalized_words = []
    
    # Process each word individually
    for word in words:
        # Handle hyphenated words 
        if '-' in word:
            # Split on hyphens, capitalize each part, then rejoin with hyphens
            parts = word.split('-')
            capitalized_parts = [part.capitalize() for part in parts]
            capitalized_words.append('-'.join(capitalized_parts))
        else:
            # .capitalize() makes first letter uppercase, rest lowercase
            capitalized_words.append(word.capitalize())
    
    # Join all words back together with spaces
    return ' '.join(capitalized_words)


# PERFORMANCE OPTIMIZATIONS

# Cache for repeated temperature conversions to improve performance
_temp_conversion_cache = {}

def cached_temperature_conversion(temp: float, from_unit: str, to_unit: str) -> Optional[float]:
    """
    Cached temperature conversion for better performance with repeated conversions.
    
    This function caches conversion results to avoid recalculating the same
    temperature conversions multiple times, which is common in weather apps.
    
    Args:
        temp (float): Temperature value to convert
        from_unit (str): Source unit ("K", "C", "F")
        to_unit (str): Target unit ("K", "C", "F")
        
    Returns:
        float: Converted temperature, or None if conversion not supported
    """
    # Create cache key from input parameters
    cache_key = (temp, from_unit, to_unit)
    
    # Check if we've already calculated this conversion
    if cache_key in _temp_conversion_cache:
        return _temp_conversion_cache[cache_key]
    
    # Calculate conversion using existing functions
    result = None
    
    if from_unit == "K" and to_unit == "C":
        result = kelvin_to_celsius(temp)
    elif from_unit == "K" and to_unit == "F":
        result = kelvin_to_fahrenheit(temp)
    elif from_unit == "C" and to_unit == "F":
        result = celsius_to_fahrenheit(temp)
    elif from_unit == "F" and to_unit == "C":
        result = fahrenheit_to_celsius(temp)
    elif from_unit == to_unit:
        result = temp  # No conversion needed
    
    # Store result in cache for future use
    if len(_temp_conversion_cache) < 100:  # Limit cache to 100 entries
        _temp_conversion_cache[cache_key] = result
    
    return result


def clear_temperature_cache():
    """
    Clear the temperature conversion cache.
    
    Call this function if you want to free up memory or reset the cache.
    Useful for long-running applications.
    """
    global _temp_conversion_cache
    _temp_conversion_cache.clear()
    