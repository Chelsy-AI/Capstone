"""
Weather History Display Module

This module provides functions to display weather history data in a GUI
using customtkinter. It includes text-based display
methods for historical weather information.
"""

from datetime import datetime, timedelta
import customtkinter as ctk
import threading
from typing import Optional, List, Dict, Any, Tuple
from .api import fetch_world_history


def insert_temperature_history_as_grid(parent, city: str, unit: str = "C"):
    """
    Fetch 7-day weather history for the city and display as a grid layout.
        
    The grid has four rows:
    - Row 0: Dates with calendar emoji (📅 2024-01-15)
    - Row 1: Maximum temperatures with up arrow (🔺 25.5°C)
    - Row 2: Minimum temperatures with down arrow (🔻 18.2°C)  
    - Row 3: Average temperatures with thermometer (🌡️ 21.8°C)
    
    Args:
        parent: The GUI container where the grid will be displayed
        city (str): Name of the city to get weather data for
        unit (str): Temperature unit - "C" for Celsius, "F" for Fahrenheit
    """
    # Input validation - ensure city is a string
    if not isinstance(city, str):
        city = "New York"  # Safe fallback default
    
    # Fetch weather data from API
    weather_data = fetch_world_history(city)
    
    # This ensures we start with a clean slate each time
    for existing_widget in parent.winfo_children():
        existing_widget.destroy()
    
    # Handle case where no data is available
    if not weather_data or "time" not in weather_data or not weather_data["time"]:
        # Create a friendly error message for the user
        error_label = ctk.CTkLabel(
            parent,
            text="No historical weather data found.",
            text_color="red",
            font=("Arial", 16, "bold")
        )
        error_label.grid(row=0, column=0, padx=10, pady=10)
        return
    
    # Configuration - how many days to show in the grid
    DAYS_TO_SHOW = 7
    
    # Extract data arrays from the API response
    # These contain lists of values, one for each day
    dates = weather_data.get("time", [])  # List of date strings
    max_temperatures = weather_data.get("temperature_2m_max", [])  # Daily highs
    min_temperatures = weather_data.get("temperature_2m_min", [])  # Daily lows
    avg_temperatures = weather_data.get("temperature_2m_mean", [])  # Daily averages
        
    def get_value_safely(data_list: List, index: int) -> Any:
        """
        Safely get a value from a list without crashing if the index doesn't exist.
        
        Args:
            data_list: List to get value from
            index: Position in the list to check
            
        Returns:
            The value at that position, or "N/A" if not available
        """
        if index < len(data_list):
            value = data_list[index]
            # Return the value if it exists and isn't None/null
            return value if value is not None else "N/A"
        else:
            # Index is beyond the list length
            return "N/A"
    
    def format_temperature_with_unit(temp, target_unit: str) -> str:
        """
        Format temperature with unit conversion and proper symbols.
        
        Args:
            temp: Temperature value (could be number or "N/A")
            target_unit: "C" for Celsius, "F" for Fahrenheit
            
        Returns:
            Formatted string like "25.5°C" or "N/A"
        """
        if temp == "N/A":
            return temp
        
        try:
            # Convert string to number for calculations
            temp_value = float(temp)
            
            # Convert Celsius to Fahrenheit if needed
            if target_unit == "F":
                temp_value = temp_value * 9 / 5 + 32
            
            # Round to 1 decimal place and add unit symbol
            return f"{round(temp_value, 1)}°{target_unit}"
        except (ValueError, TypeError):
            # If conversion fails, return "N/A" instead of crashing
            return "N/A"
        
    for day_column in range(DAYS_TO_SHOW):
        # Extract and format data for this specific day
        date_string = get_value_safely(dates, day_column)
        max_temp_formatted = format_temperature_with_unit(
            get_value_safely(max_temperatures, day_column), unit
        )
        min_temp_formatted = format_temperature_with_unit(
            get_value_safely(min_temperatures, day_column), unit
        )
        avg_temp_formatted = format_temperature_with_unit(
            get_value_safely(avg_temperatures, day_column), unit
        )
        
        # Row 0: Date headers with calendar emoji
        date_label = ctk.CTkLabel(
            parent, 
            text=f"📅 {date_string}", 
            font=("Arial", 14, "bold")
        )
        date_label.grid(row=0, column=day_column, padx=8, pady=4)
        
        # Row 1: Maximum temperatures with up arrow
        max_temp_label = ctk.CTkLabel(
            parent, 
            text=f"🔺 {max_temp_formatted}",
        )
        max_temp_label.grid(row=1, column=day_column, padx=8, pady=4)
        
        # Row 2: Minimum temperatures with down arrow
        min_temp_label = ctk.CTkLabel(
            parent, 
            text=f"🔻 {min_temp_formatted}",
        )
        min_temp_label.grid(row=2, column=day_column, padx=8, pady=4)
        
        # Row 3: Average temperatures with thermometer
        avg_temp_label = ctk.CTkLabel(
            parent, 
            text=f"🌡️ {avg_temp_formatted}",
        )
        avg_temp_label.grid(row=3, column=day_column, padx=8, pady=4)
    

def show_weather_history(parent_widget, city: str = "New York", unit: str = "C"):
    """
    Display weather history in a text-based tabular format.
    
    Args:
        parent_widget: The GUI container where the table will be displayed
        city (str): Name of the city to get weather data for (default: "New York")
        unit (str): Temperature unit - "C" for Celsius, "F" for Fahrenheit
    """
    # Create main container frame with proper styling
    history_frame = ctk.CTkFrame(parent_widget)
    history_frame.pack(fill="x", pady=(10, 0), padx=10)
    
    # Add title label so users know what they're looking at
    title_label = ctk.CTkLabel(
        history_frame, 
        text="7-Day Weather History", 
        font=ctk.CTkFont(size=16, weight="bold")
    )
    title_label.pack(anchor="w", padx=5, pady=(5, 0))
    
    # Create text widget for displaying the weather table
    text_display = ctk.CTkTextbox(
        history_frame, 
        width=400, 
        height=160, 
        corner_radius=8, 
        wrap="none",
        font=("Courier", 12)
    )
    text_display.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Show loading message immediately so user knows something is happening
    text_display.insert("end", "🌤️ Loading weather history...\n")
    text_display.configure(state="disabled")  # Prevent user from editing
    
    def load_weather_data_in_background():
        """
        Background thread function to load weather history data.
        
        The function fetches data, processes it, and then updates the GUI
        with the results.
        """
        try:            
            # Fetch data from the weather API
            weather_data = fetch_world_history(city)
            
            # Update the GUI with results
            text_display.configure(state="normal")  # Allow editing to update content
            text_display.delete("1.0", "end")  # Clear the loading message
            
            if not weather_data:
                # No data available - show helpful error message
                text_display.insert("end", "❌ No historical weather data found.\n")
                text_display.insert("end", "Please check your internet connection or try a different city.\n")
            else:                
                # Determine temperature unit symbol for display
                unit_symbol = "°F" if unit.upper() == "F" else "°C"
                
                # Create table header with column names
                header_line = f"{'Date':>12} | {'High':>6} | {'Low':>6} | {'Average':>8}\n"
                separator_line = "-" * 12 + "|" + "-" * 8 + "|" + "-" * 8 + "|" + "-" * 10 + "\n"
                
                text_display.insert("end", header_line)
                text_display.insert("end", separator_line)
                
                # Insert data rows - one for each day
                for daily_data in weather_data:
                    # Format temperature values with unit
                    high_temp = f"{daily_data['high']}{unit_symbol}"
                    low_temp = f"{daily_data['low']}{unit_symbol}"
                    avg_temp = f"{daily_data['average']}{unit_symbol}"
                    
                    # Create formatted row with proper spacing
                    data_row = f"{daily_data['date']:>12} | {high_temp:>6} | {low_temp:>6} | {avg_temp:>8}\n"
                    text_display.insert("end", data_row)
                
                # Add helpful note about temperature units
                text_display.insert("end", f"\n💡 Temperatures shown in {unit_symbol}")
            
        except Exception as e:
            # Handle any errors that occur during data loading
            text_display.configure(state="normal")
            text_display.delete("1.0", "end")
            text_display.insert("end", f"⚠️ Error loading weather data: {str(e)}\n")
            text_display.insert("end", "Please try again later or check your internet connection.\n")
        
        finally:
            # Always disable text widget to prevent user editing, regardless of success/failure
            text_display.configure(state="disabled")
    
    # Start the background data loading process
    # daemon=True means the thread will close when the main program closes
    loading_thread = threading.Thread(target=load_weather_data_in_background, daemon=True)
    loading_thread.start()


# ADDITIONAL UTILITY FUNCTIONS FOR ENHANCED FUNCTIONALITY

def format_date_for_display(date_string: str) -> str:
    """
    Format date string for better display in the GUI.
    
    Args:
        date_string: Date in string format (like "2024-01-15")
        
    Returns:
        Formatted date string (like "01/15" or original if formatting fails)
    """
    try:
        if isinstance(date_string, str):
            # Parse the date string and reformat it
            date_object = datetime.strptime(date_string, "%Y-%m-%d")
            return date_object.strftime("%m/%d")  # MM/DD format
        return str(date_string)
    except (ValueError, TypeError):
        # If date parsing fails, just return the original string
        return str(date_string)

def create_weather_summary_text(weather_data: Dict[str, Any], city: str, unit: str = "C") -> str:
    """
    Create a text summary of weather data for easy reading.
    
    Args:
        weather_data: Dictionary containing weather information
        city: Name of the city
        unit: Temperature unit preference
        
    Returns:
        Human-readable weather summary string
    """
    try:
        if not weather_data or not weather_data.get("time"):
            return f"No weather data available for {city}."
        
        # Extract temperature data
        max_temps = weather_data.get("temperature_2m_max", [])
        min_temps = weather_data.get("temperature_2m_min", [])
        
        # Convert to target unit and calculate ranges
        if max_temps and min_temps:
            # Convert from Fahrenheit if needed
            if unit == "C":
                max_temps_converted = [(t - 32) * 5/9 for t in max_temps if t is not None]
                min_temps_converted = [(t - 32) * 5/9 for t in min_temps if t is not None]
            else:
                max_temps_converted = [t for t in max_temps if t is not None]
                min_temps_converted = [t for t in min_temps if t is not None]
            
            if max_temps_converted and min_temps_converted:
                # Calculate temperature ranges
                highest_high = round(max(max_temps_converted), 1)
                lowest_high = round(min(max_temps_converted), 1)
                highest_low = round(max(min_temps_converted), 1)
                lowest_low = round(min(min_temps_converted), 1)
                
                # Create summary text
                unit_symbol = f"°{unit}"
                summary = f"{city} weather summary: "
                summary += f"Highs {lowest_high}-{highest_high}{unit_symbol}, "
                summary += f"Lows {lowest_low}-{highest_low}{unit_symbol} "
                summary += f"over {len(max_temps_converted)} days."
                
                return summary
        
        return f"Weather data available for {city}, but temperature information is incomplete."
        
    except Exception as e:
        return f"Error creating weather summary for {city}: {str(e)}"


def validate_city_input(city_name: str) -> Tuple[bool, str]:
    """
    Validate city name input to prevent API errors.
    
    Args:
        city_name: User-provided city name
        
    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    if not city_name or not city_name.strip():
        return False, "City name cannot be empty"
    
    # Remove extra spaces
    city_name = city_name.strip()
    
    # Check reasonable length
    if len(city_name) < 2:
        return False, "City name must be at least 2 characters"
    
    if len(city_name) > 100:
        return False, "City name is too long"
    
    # Check for reasonable characters (letters, spaces, common punctuation)
    import re
    if not re.match(r"^[a-zA-Z\s\-'.,]+$", city_name):
        return False, "City name contains invalid characters"
    
    return True, ""

 
# PERFORMANCE OPTIMIZATION UTILITIES

# Cache to store recently fetched weather data to avoid repeated API calls
_weather_data_cache: Dict[str, Tuple[Dict[str, Any], float]] = {}
_cache_timeout_seconds = 300  # 5 minutes


def get_cached_weather_data(city: str) -> Optional[Dict[str, Any]]:
    """
    Get weather data from cache if available and not expired.
    
    Args:
        city: City name to check cache for
        
    Returns:
        Cached weather data or None if not available/expired
    """
    import time
    
    cache_key = city.lower().strip()
    
    if cache_key in _weather_data_cache:
        cached_data, cache_time = _weather_data_cache[cache_key]
        
        # Check if cache is still valid
        if time.time() - cache_time < _cache_timeout_seconds:
            return cached_data
        else:
            # Cache expired, remove it
            del _weather_data_cache[cache_key]
    
    return None


def cache_weather_data(city: str, data: Dict[str, Any]) -> None:
    """
    Store weather data in cache for future use.
    
    Args:
        city: City name as cache key
        data: Weather data to cache
    """
    import time
    
    cache_key = city.lower().strip()
    current_time = time.time()
    
    # Limit cache size to prevent memory issues
    if len(_weather_data_cache) >= 50:
        # Remove oldest entry
        oldest_key = min(_weather_data_cache.keys(), 
                        key=lambda k: _weather_data_cache[k][1])
        del _weather_data_cache[oldest_key]
    
    _weather_data_cache[cache_key] = (data, current_time)


def clear_weather_cache() -> None:
    """
    Clear the weather data cache.
    
    Useful for freeing memory or forcing fresh data retrieval.
    """
    global _weather_data_cache
    _weather_data_cache.clear()
