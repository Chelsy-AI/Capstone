"""
Main Weather Application Class
==============================

This is the heart of the weather app! It creates the main window and
coordinates all the different features like:
- Getting weather data from the internet
- Showing weather animations
- Managing different pages (main, history, predictions, etc.)
- Handling user interactions (button clicks, city searches)

Think of this as the "brain" that controls everything in the app.
"""

import tkinter as tk  # For creating the window and interface
import threading      # For doing tasks in the background
import traceback     # For showing detailed error messages
import sys
import os
from dotenv import load_dotenv  # For loading API keys from .env file

# Load environment variables (like API keys) from .env file
load_dotenv()

# Add the project root to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our custom weather app modules
from features.tomorrows_guess.predictor import get_tomorrows_prediction
from config.themes import LIGHT_THEME, DARK_THEME
from config.api import get_current_weather
from config.storage import save_weather
from config.gui import WeatherGUI


class WeatherApp(tk.Tk):
    """
    Main Weather Application Class
    
    This class creates the main window and manages all the weather app features.
    It inherits from tk.Tk, which means it IS a window that can display things.
    
    Key responsibilities:
    - Create and manage the main window
    - Store weather data and user settings
    - Coordinate between different app features
    - Handle background tasks (like downloading weather data)
    """

    def __init__(self):
        """
        Initialize the weather app.
        
        This runs when you create a new WeatherApp object.
        It sets up the window, creates variables to store data,
        and builds the user interface.
        """
        # Initialize the parent class (tk.Tk) to create a window
        super().__init__()

        # Set up the main window properties
        self.title("Smart Weather App with Sun & Moon Phases")
        self.geometry("800x700")      # Width x Height in pixels
        self.minsize(700, 600)        # Minimum size user can resize to

        # Initialize variables to store user settings and data
        self.city_var = tk.StringVar(value="New York")  # Default city to search
        self.unit = "C"               # Temperature unit (C for Celsius, F for Fahrenheit)
        self.temp_c = None           # Current temperature in Celsius
        self.temp_f = None           # Current temperature in Fahrenheit
        self.theme = LIGHT_THEME     # Current color theme
        self.text_color = "black"    # Color for text

        # Storage for weather data - preserves info when switching pages
        self.current_weather_data = {}    # Latest weather information
        self.current_prediction_data = {} # Tomorrow's weather prediction
        self.current_history_data = []    # Historical weather data
        self.current_sun_moon_data = {}   # Sun and moon information

        # Initialize the graphical user interface system
        self.gui = WeatherGUI(self)

        # Build the user interface (buttons, labels, etc.)
        self.gui.build_gui()

        # Automatically load weather data after 1 second (1000 milliseconds)
        self.after(1000, self.fetch_and_display)

        # Set up what happens when user closes the window
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_all_label_backgrounds(self, new_bg_color):
        """
        Update the background color of all text labels to match animation.
        
        When weather animations change the background color (like blue for rain,
        white for snow), we need to update all text labels so they don't look
        like ugly blue boxes on top of the new background.
        
        Args:
            new_bg_color (str): The new background color (like "#87CEEB" for sky blue)
        """
        try:
            # Make sure we have a GUI system to work with
            if hasattr(self, 'gui'):
                all_widgets = []  # List to collect all widgets we need to update
                
                # Add widgets from the main widgets list
                if hasattr(self.gui, 'widgets'):
                    all_widgets.extend(self.gui.widgets)
                
                # Add widgets from the history page
                if hasattr(self.gui, 'history_labels'):
                    all_widgets.extend(self.gui.history_labels)
                
                # Add specific weather display widgets
                weather_widgets = [
                    self.gui.humidity_value, self.gui.wind_value, self.gui.pressure_value,
                    self.gui.visibility_value, self.gui.uv_value, self.gui.precipitation_value,
                    self.gui.temp_label, self.gui.desc_label, self.gui.icon_label,
                    self.gui.temp_prediction, self.gui.accuracy_prediction, self.gui.confidence_prediction
                ]
                
                # Add non-None weather widgets to the list
                for widget in weather_widgets:
                    if widget:
                        all_widgets.append(widget)
                
                # Update the background color of all labels
                for widget in all_widgets:
                    if widget and hasattr(widget, 'configure'):
                        try:
                            widget_class = widget.winfo_class()
                            # Only update labels (not buttons or other widgets)
                            if widget_class == 'Label':
                                widget.configure(bg=new_bg_color)
                        except Exception:
                            # If updating this widget fails, just skip it
                            pass
        except Exception:
            # If the whole function fails, just skip it - not critical
            pass

    def fetch_and_display(self):
        """
        Get weather data and update the display.
        
        This starts a background task to download weather information
        so the app doesn't freeze while waiting for the internet.
        """
        # Start the actual work in a background thread
        threading.Thread(target=self._fetch_weather, daemon=True).start()

    def _fetch_weather(self):
        """
        Background task to download weather data.
        
        This runs in a separate thread so the app stays responsive.
        It downloads weather data, saves it, and then updates the display.
        
        Note: This is a "private" method (starts with _) meaning it's only
        used internally by this class.
        """
        try:
            # Get the city name from the input field (or use default)
            city = self.city_var.get().strip() or "New York"
            
            # Download current weather data from the internet
            weather_data = get_current_weather(city)

            # If there was an error getting weather data, stop here
            if weather_data.get("error"):
                return

            # Try to save the weather data to our history file
            try:
                save_weather(weather_data, city)
            except Exception:
                # If saving fails, continue anyway - not critical
                pass

            # Store the weather data so other parts of the app can use it
            self.current_weather_data = weather_data

            # Update the display (must be done on the main thread)
            # self.after() schedules these to run on the main thread
            self.after(0, lambda: self.gui.update_weather_display(weather_data))
            self.after(0, lambda: self.update_tomorrow_prediction(city))
            self.after(0, lambda: self.gui.update_history_display(city))
            self.after(0, lambda: self.gui.update_background_animation(weather_data))
            self.after(0, lambda: self.gui.update_sun_moon_display(city))

        except Exception:
            # If anything goes wrong, just skip it - the app will continue working
            pass

    def update_tomorrow_prediction(self, city):
        """
        Get and display tomorrow's weather prediction.
        
        This uses our prediction algorithm to guess what tomorrow's
        weather might be like based on recent weather patterns.
        
        Args:
            city (str): Name of the city to predict weather for
        """
        try:
            # Get prediction data (temperature, confidence level, accuracy)
            predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)
            
            # Store the prediction data
            self.current_prediction_data = (predicted_temp, confidence, accuracy)
            
            # Update the prediction display
            self.gui.update_tomorrow_prediction_direct(predicted_temp, confidence, accuracy)
        except Exception:
            # If prediction fails, use default "no data" values
            self.current_prediction_data = (None, "N/A", 0)

    def toggle_theme(self):
        """
        Switch between light and dark color themes.
        
        This changes the colors throughout the app and notifies
        other components that may need to update their appearance.
        """
        # Tell the GUI to switch themes
        self.gui.toggle_theme()
        
        # Also tell the sun/moon page about the theme change
        if hasattr(self.gui, 'sun_moon_controller'):
            self.gui.sun_moon_controller.handle_theme_change()

    def toggle_unit(self):
        """
        Switch between Celsius and Fahrenheit temperature units.
        
        This changes the temperature display and refreshes the weather
        data to show temperatures in the new unit.
        """
        # Switch between C and F
        self.unit = "F" if self.unit == "C" else "C"
        
        # Refresh the display with the new unit
        self.fetch_and_display()

    def get_current_sun_moon_data(self):
        """
        Get the current sun and moon information.
        
        This is used by other parts of the app that need to know
        about sunrise/sunset times or moon phases.
        
        Returns:
            dict: Sun and moon data, or empty dict if none available
        """
        if hasattr(self.gui, 'sun_moon_controller'):
            return self.gui.sun_moon_controller.get_current_data()
        return {}

    def is_currently_daytime(self):
        """
        Check if it's currently daytime.
        
        This can be used to automatically switch themes or change
        the behavior of animations based on time of day.
        
        Returns:
            bool: True if it's daytime, False if it's nighttime
        """
        # Try to get accurate sunrise/sunset data
        if hasattr(self.gui, 'sun_moon_controller'):
            return self.gui.sun_moon_controller.is_daytime()
        
        # Fallback: simple time-based check
        import datetime
        current_hour = datetime.datetime.now().hour
        return 6 <= current_hour < 18  # Assume daylight from 6 AM to 6 PM

    def on_close(self):
        """
        Clean up when the user closes the app.
        
        This makes sure all background tasks are stopped and
        resources are freed up properly before the app closes.
        """
        # Stop animations and clean up resources
        self.gui.cleanup_animation()
        
        # Clean up sun/moon controller
        if hasattr(self.gui, 'sun_moon_controller'):
            self.gui.sun_moon_controller.cleanup()
        
        # Actually close the window
        self.destroy()


def run_app():
    """
    Create and run the weather application.
    
    This is the main entry point that creates the app window
    and starts the main program loop. It includes error handling
    to show helpful messages if something goes wrong.
    """
    try:
        print("🌤️ Starting Weather Application...")
        
        # Create the main application window
        app = WeatherApp()
        
        # Start automatic sun/moon data updates (every 30 minutes)
        if hasattr(app.gui, 'sun_moon_controller'):
            app.gui.sun_moon_controller.start_auto_refresh(interval_minutes=30)
        
        print("✓ Weather app initialized successfully")
        
        # Start the main event loop (this keeps the app running until closed)
        app.mainloop()
        
    except Exception as e:
        # If something goes wrong, show a detailed error message
        print(f"❌ Error starting weather app: {e}")
        traceback.print_exc()


# If this file is run directly (not imported), start the app
if __name__ == "__main__":
    run_app()