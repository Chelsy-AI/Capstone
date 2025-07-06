"""
Main Weather Application Class
=============================

This module contains the core WeatherApp class that manages the entire application.
It handles the GUI setup, weather data updates, theme switching, and coordinates
all the different features of the weather application.

Key Features:
- Main application window management
- Weather data fetching and display
- Theme switching (Light/Dark mode)
- Temperature unit conversion (Celsius/Fahrenheit)
- Weather icon display with caching
- Historical weather data integration
- Tomorrow's weather prediction
- Multi-threading for smooth UI performance

"""

import customtkinter as ctk
from PIL import Image
from io import BytesIO
import requests
from datetime import datetime
import threading

from features.history_tracker.api import fetch_world_history
from features.history_tracker.display import insert_temperature_history_as_grid
from features.tomorrows_guess.display import update_tomorrow_guess_display
from features.tomorrows_guess.predictor import get_tomorrows_prediction

from core.theme import LIGHT_THEME, DARK_THEME
from core.gui import build_gui
from core.api import get_current_weather


class WeatherApp(ctk.CTk):
    """
    Main Weather Application Class
    
    This class inherits from CustomTkinter's CTk to create the main application window.
    It manages all aspects of the weather app including data fetching, display updates,
    theme management, and user interactions.
    
    Attributes:
        theme: Current theme configuration (LIGHT_THEME or DARK_THEME)
        city_var: StringVar holding the current city name
        unit: Current temperature unit ("C" for Celsius, "F" for Fahrenheit)
        temp_c: Current temperature in Celsius
        temp_f: Current temperature in Fahrenheit
        metric_value_labels: Dictionary of labels for weather metrics
        icon_cache: Cache for weather icons to avoid repeated downloads
        Various GUI widget references (frames, labels, etc.)
    """
    
    def __init__(self):
        """
        Initialize the Weather Application
        
        Sets up the main window, initializes variables, creates the GUI,
        and starts the weather data fetching in a background thread.

        """
        # Initialize the parent CTk class
        super().__init__()

        # Set up initial theme configuration
        self.theme = LIGHT_THEME
        ctk.set_appearance_mode("light")
        
        # Configure main window properties
        self.title("Weather App")
        self.geometry("800x600")
        self.configure(fg_color=self.theme["bg"])

        # Initialize application state variables
        self.city_var = ctk.StringVar(value="New York")  # Default city
        self.unit = "C"  # Default to Celsius

        # Initialize temperature storage variables
        self.temp_c = None  # Temperature in Celsius
        self.temp_f = None  # Temperature in Fahrenheit
        
        # Dictionary to store references to metric display labels
        self.metric_value_labels = {}

        # Icon image cache to avoid repeated downloads and improve performance
        self.icon_cache = {}

        # Initialize widget placeholders as None (will be created in build_gui)
        self.history_frame = None
        self.temp_label = None
        self.desc_label = None
        self.update_label = None
        self.icon_label = None
        self.tomorrow_guess_frame = None
        self.city_entry = None  

        # Create all GUI widgets and assign them to instance variables
        build_gui(self)

        # Start weather update in background thread safely after GUI is initialized
        # Using after_idle ensures GUI is fully ready before starting background tasks
        self.after_idle(lambda: threading.Thread(target=self.update_weather, daemon=True).start())

    def toggle_theme(self):
        """
        Switch between light and dark themes
        
        This method toggles the application's appearance between light and dark modes.
        It updates the theme configuration, rebuilds the GUI with new colors,
        and refreshes the weather data display.

        """
        # Toggle between light and dark themes
        if self.theme == LIGHT_THEME:
            self.theme = DARK_THEME
            ctk.set_appearance_mode("dark")
        else:
            self.theme = LIGHT_THEME
            ctk.set_appearance_mode("light")

        # Rebuild entire GUI to apply new theme colors
        # This ensures all widgets get the new theme styling
        build_gui(self)

        # Update the weather data display to refresh texts/images after rebuild
        self.update_weather()

    def toggle_temp_unit(self, event=None):
        """
        Switch between Celsius and Fahrenheit temperature units
        
        This method toggles the temperature display unit and updates all
        temperature-related displays including current weather, predictions,
        and historical data.
        
        """
        # Toggle between Celsius and Fahrenheit
        self.unit = "F" if self.unit == "C" else "C"
        
        # Update all temperature displays with the new unit
        self.update_temperature_label()
        self.update_tomorrow_prediction()
        self.update_weather_history()

    def update_temperature_label(self):
        """
        Update the main temperature display label
        
        Updates the temperature label with the current temperature in the
        selected unit (Celsius or Fahrenheit). Handles cases where temperature
        data is not available.
        """
        # Check if temperature label widget exists
        if self.temp_label is None:
            return  

        # Handle case where temperature data is not available
        if self.temp_c is None:
            self.temp_label.configure(text="N/A")
        elif self.unit == "C":
            # Display temperature in Celsius
            self.temp_label.configure(text=f"{self.temp_c} °C")
        else:
            # Display temperature in Fahrenheit
            self.temp_label.configure(text=f"{self.temp_f} °F")

    def update_weather(self):
        """
        Main weather data update method
        
        This is the core method that fetches current weather data and historical
        information, then updates all relevant GUI components. It handles API
        errors gracefully and updates the display accordingly.
        
        Runs in a background thread to prevent GUI freezing during API calls.
        """
        # Get the current city name, default to "New York" if empty
        city = self.city_var.get().strip() or "New York"

        # Fetch historical weather data for the history display feature
        self.history_data = fetch_world_history(city)

        # Fetch current weather data from API
        data = get_current_weather(city)
        
        # Handle API errors or data unavailability
        if data.get("error"):
            # Reset all temperature variables
            self.temp_c = None
            self.temp_f = None
            
            # Update GUI elements to show error state
            if self.temp_label:
                self.temp_label.configure(text="N/A")
            if self.desc_label:
                self.desc_label.configure(text=data["error"])
            
            # Set all metric labels to "N/A"
            for label in self.metric_value_labels.values():
                label.configure(text="N/A")
            
            # Clear weather icon
            if self.icon_label:
                self.icon_label.configure(image=None)
                self.icon_label.image = None
            
            # Clear update timestamp
            if self.update_label:
                self.update_label.configure(text="")
            
            # Clear tomorrow's prediction
            if self.tomorrow_guess_frame:
                update_tomorrow_guess_display(self.tomorrow_guess_frame, "N/A", "N/A", "N/A")
            return

        # Process temperature data if available
        temp_c = data.get("temperature")
        if temp_c is not None:
            # Store temperatures in both Celsius and Fahrenheit
            self.temp_c = round(temp_c, 1)
            self.temp_f = round((temp_c * 9 / 5) + 32, 1)  # Convert C to F
        else:
            self.temp_c = self.temp_f = None

        # Update the main temperature display
        self.update_temperature_label()

        # Update weather description
        if self.desc_label:
            self.desc_label.configure(text=data.get("description", "No description"))

        # Update the "last updated" timestamp
        if self.update_label:
            self.update_label.configure(text=f"Updated at {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        # Handle weather icon display with caching
        icon_code = data.get("icon")
        if icon_code and self.icon_label:
            # Check if icon is already cached
            if icon_code in self.icon_cache:
                icon_image = self.icon_cache[icon_code]
            else:
                # Download and cache the weather icon
                try:
                    url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    
                    # Convert to PIL image and create CTkImage
                    pil_img = Image.open(BytesIO(response.content)).convert("RGBA")
                    icon_image = ctk.CTkImage(light_image=pil_img, size=(64, 64))
                    
                    # Cache the icon for future use
                    self.icon_cache[icon_code] = icon_image
                except Exception:
                    # Handle icon download failures gracefully
                    icon_image = None

            # Display the icon or clear it if unavailable
            if icon_image:
                self.icon_label.configure(image=icon_image)
                self.icon_label.image = icon_image
            else:
                self.icon_label.configure(image=None)
                self.icon_label.image = None
        elif self.icon_label:
            # Clear icon if no icon code available
            self.icon_label.configure(image=None)
            self.icon_label.image = None

        # Update all weather metric labels (humidity, wind, pressure, etc.)
        metrics = {
            "humidity": f"{data.get('humidity')}%" if data.get("humidity") is not None else "N/A",
            "wind": f"{data.get('wind_speed')} m/s" if data.get("wind_speed") is not None else "N/A",
            "pressure": f"{data.get('pressure')} hPa" if data.get("pressure") is not None else "N/A",
            "visibility": f"{data.get('visibility')} m" if data.get("visibility") is not None else "N/A",
            "uv": str(data.get("uv_index")) if data.get("uv_index") is not None else "N/A",
            "precipitation": f"{data.get('precipitation')} mm" if data.get("precipitation") is not None else "N/A",
        }

        # Update each metric label with the corresponding value
        for key, val in metrics.items():
            label = self.metric_value_labels.get(key)
            if label:
                label.configure(text=val)

        # Update tomorrow's prediction and weather history on main thread using after
        # This ensures GUI updates happen on the main thread (thread-safe)
        self.after(0, lambda: self.update_tomorrow_prediction(city))
        self.after(0, self.update_weather_history)

    def update_tomorrow_prediction(self, city=None):
        """
        Update tomorrow's weather prediction display
        
        Fetches and displays the predicted weather for tomorrow, including
        temperature, confidence level, and accuracy metrics. Handles temperature
        unit conversion based on current settings.
        
        """
        # Use current city if none specified
        if city is None:
            city = self.city_var.get().strip()

        # Validate city input
        if not isinstance(city, str) or city == "":
            if self.tomorrow_guess_frame:
                update_tomorrow_guess_display(self.tomorrow_guess_frame, "N/A", "N/A", "N/A")
            return

        # Get tomorrow's weather prediction
        predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)

        # Format temperature display based on current unit setting
        if predicted_temp is None:
            predicted_display = "N/A"
        else:
            predicted_display = (
                f"{predicted_temp} °C" if self.unit == "C"
                else f"{round((predicted_temp * 9 / 5) + 32, 1)} °F"
            )

        # Update the tomorrow's prediction display
        if self.tomorrow_guess_frame:
            update_tomorrow_guess_display(
                self.tomorrow_guess_frame,
                predicted_temp=predicted_display,
                confidence=confidence,
                accuracy=accuracy
            )

    def update_weather_history(self):
        """
        Update the weather history display
        
        Clears and rebuilds the weather history section with historical temperature
        data. Handles cases where historical data is not available and displays
        appropriate messages.
        """
        # Clear existing widgets in the history frame
        if getattr(self, "history_frame", None) and self.history_frame.winfo_exists():
            for widget in self.history_frame.winfo_children():
                widget.destroy()

        # Check if we have valid historical data
        if isinstance(self.history_data, dict) and all(
            key in self.history_data for key in ["time", "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean"]
        ):
            # Display historical temperature data as a grid
            insert_temperature_history_as_grid(self.history_frame, self.city_var.get(), unit=self.unit)
        else:
            # Display "not available" message when historical data is missing
            label = ctk.CTkLabel(
                self.history_frame,
                text="Weather history not available.",
                font=("Arial", 16),
                text_color=self.theme["fg"],
            )
            label.pack(pady=10)


def run_app():
    """
    Application entry point function
    
    Creates and starts the Weather Application. This function initializes
    the WeatherApp class and starts the GUI main loop.
    
    """
    # Create an instance of the WeatherApp
    app = WeatherApp()
    
    # Start the GUI main loop (keeps the application running)
    app.mainloop()