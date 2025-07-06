"""
Weather History Display Module

This module provides functions to display weather history data in a GUI
using customtkinter. It includes both grid-based and text-based display
methods for historical weather information.

"""

from datetime import datetime, timedelta
import customtkinter as ctk
import threading
from .api import fetch_world_history
from features.history_tracker.api import fetch_world_history


def insert_temperature_history_as_grid(parent, city, unit="C"):
    """
    Fetch 7-day weather history for the city and display as a grid layout.
    
    Creates a grid with four rows displaying:
    - Row 0: Dates with calendar emoji
    - Row 1: Maximum temperatures with up arrow
    - Row 2: Minimum temperatures with down arrow  
    - Row 3: Average temperatures with thermometer
    
    """
    # Input validation - ensure city is a string
    if not isinstance(city, str):
        city = "New York"  # fallback default
    
    # Fetch weather data from API
    data = fetch_world_history(city)
    
    # Clear any existing widgets in the parent frame to avoid overlap
    for widget in parent.winfo_children():
        widget.destroy()
    
    # Handle case where no data is available
    if not data or "time" not in data or not data["time"]:
        error_label = ctk.CTkLabel(
            parent,
            text="No historical weather data found.",
            text_color="red",
            font=("Arial", 16, "bold")
        )
        error_label.grid(row=0, column=0, padx=10, pady=10)
        return
    
    # Configuration constants
    DAYS_TO_SHOW = 7
    
    # Extract data arrays from the API response
    times = data.get("time", [])
    max_temps = data.get("temperature_2m_max", [])
    min_temps = data.get("temperature_2m_min", [])
    avg_temps = data.get("temperature_2m_mean", [])
    
    def get_value_or_na(data_list, index):
        """
        Safely get a value from a list or return 'N/A' if index is out of bounds
        or the value is None.
        
        """
        if index < len(data_list):
            value = data_list[index]
            return value if value is not None else "N/A"
        else:
            return "N/A"
    
    def format_temp(temp, unit):
        """
        Format temperature with unit conversion and symbol.
        
        """
        if temp == "N/A":
            return temp
        try:
            temp = float(temp)
            # Convert Celsius to Fahrenheit if needed
            if unit == "F":
                temp = temp * 9 / 5 + 32
            return f"{round(temp, 1)}°{unit}"
        except (ValueError, TypeError):
            return "N/A"
    
    # Create grid layout for each day
    for col in range(DAYS_TO_SHOW):
        # Extract and format data for this day
        date_str = get_value_or_na(times, col)
        max_temp = format_temp(get_value_or_na(max_temps, col), unit)
        min_temp = format_temp(get_value_or_na(min_temps, col), unit)
        avg_temp = format_temp(get_value_or_na(avg_temps, col), unit)
        
        # Row 0: Date headers with calendar emoji
        date_label = ctk.CTkLabel(
            parent, 
            text=f"📅 {date_str}", 
            font=("Arial", 14, "bold")
        )
        date_label.grid(row=0, column=col, padx=8, pady=4)
        
        # Row 1: Maximum temperatures with up arrow
        max_label = ctk.CTkLabel(
            parent, 
            text=f"🔺 {max_temp}",
            text_color="#FF6B6B"  # Red color for hot temperatures
        )
        max_label.grid(row=1, column=col, padx=8, pady=4)
        
        # Row 2: Minimum temperatures with down arrow
        min_label = ctk.CTkLabel(
            parent, 
            text=f"🔻 {min_temp}",
            text_color="#4ECDC4"  # Cool blue for cold temperatures
        )
        min_label.grid(row=2, column=col, padx=8, pady=4)
        
        # Row 3: Average temperatures with thermometer
        avg_label = ctk.CTkLabel(
            parent, 
            text=f"🌡️ {avg_temp}",
            text_color="#FFD93D"  # Yellow for average
        )
        avg_label.grid(row=3, column=col, padx=8, pady=4)


def show_weather_history(parent_widget, city="New York", unit="C"):
    """
    Display weather history in a text-based tabular format.
    
    Creates a frame with a text widget that shows weather history in a 
    table format. Uses threading to prevent GUI freezing during API calls.
    
    """
    # Create main container frame
    history_frame = ctk.CTkFrame(parent_widget)
    history_frame.pack(fill="x", pady=(10, 0), padx=10)
    
    # Add title label
    title_label = ctk.CTkLabel(
        history_frame, 
        text="7-Day Weather History", 
        font=ctk.CTkFont(size=16, weight="bold")
    )
    title_label.pack(anchor="w", padx=5, pady=(5, 0))
    
    # Create text widget for displaying tabular data
    text_widget = ctk.CTkTextbox(
        history_frame, 
        width=400, 
        height=160, 
        corner_radius=8, 
        wrap="none",  # Prevent text wrapping for table formatting
        font=("Courier", 12)  # Monospace font for better table alignment
    )
    text_widget.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Show loading message immediately
    text_widget.insert("end", "🌤️ Loading weather history...\n")
    text_widget.configure(state="disabled")
    
    def load_history():
        """
        Background thread function to load weather history data.
        
        This function runs in a separate thread to prevent the GUI from
        freezing while waiting for API responses.
        """
        try:
            # Fetch data from API
            data = fetch_world_history(city)
            
            # Update GUI in main thread
            text_widget.configure(state="normal")
            text_widget.delete("1.0", "end")  # Clear loading message
            
            if not data:
                text_widget.insert("end", "❌ No historical weather data found.\n")
                text_widget.insert("end", "Please check your internet connection or try a different city.\n")
            else:
                # Determine unit symbol
                unit_symbol = "°F" if unit.upper() == "F" else "°C"
                
                # Create table header
                header = f"{'Date':>12} | {'High':>6} | {'Low':>6} | {'Average':>8}\n"
                separator = "-" * 12 + "|" + "-" * 8 + "|" + "-" * 8 + "|" + "-" * 10 + "\n"
                
                text_widget.insert("end", header)
                text_widget.insert("end", separator)
                
                # Insert data rows
                for entry in data:
                    # Format temperature values
                    high = f"{entry['high']}{unit_symbol}"
                    low = f"{entry['low']}{unit_symbol}"
                    avg = f"{entry['average']}{unit_symbol}"
                    
                    # Create formatted row
                    row = f"{entry['date']:>12} | {high:>6} | {low:>6} | {avg:>8}\n"
                    text_widget.insert("end", row)
                
                # Add helpful note
                text_widget.insert("end", f"\n💡 Temperatures shown in {unit_symbol}")
            
        except Exception as e:
            # Handle any errors that occur during data loading
            text_widget.configure(state="normal")
            text_widget.delete("1.0", "end")
            text_widget.insert("end", f"⚠️ Error loading weather data: {str(e)}\n")
            text_widget.insert("end", "Please try again later or check your internet connection.\n")
        
        finally:
            # Always disable text widget to prevent user editing
            text_widget.configure(state="disabled")
    
    # Start background thread to load data
    loading_thread = threading.Thread(target=load_history, daemon=True)
    loading_thread.start()


# Additional utility functions for enhanced functionality

def format_date_display(date_str):
    """
    Format date string for better display.
    
    """
    try:
        if isinstance(date_str, str):
            # Parse and reformat date if needed
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%m/%d")
        return str(date_str)
    except (ValueError, TypeError):
        return str(date_str)


def get_temperature_color(temp, unit="C"):
    """
    Get color code based on temperature value.
    
    """
    try:
        temp_val = float(temp)
        if unit == "F":
            # Fahrenheit color ranges
            if temp_val >= 80:
                return "#FF4757"  # Hot red
            elif temp_val >= 60:
                return "#FFA502"  # Warm orange
            elif temp_val >= 40:
                return "#2ED573"  # Cool green
            else:
                return "#5352ED"  # Cold blue
        else:
            # Celsius color ranges
            if temp_val >= 27:
                return "#FF4757"  # Hot red
            elif temp_val >= 15:
                return "#FFA502"  # Warm orange
            elif temp_val >= 5:
                return "#2ED573"  # Cool green
            else:
                return "#5352ED"  # Cold blue
    except (ValueError, TypeError):
        return "#747D8C"  # Default gray for invalid values
