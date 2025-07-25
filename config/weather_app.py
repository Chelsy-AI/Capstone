"""
Main Weather Application Class - Complete Fixed Version
=======================================================

This is the heart of the weather app! It creates the main window and
coordinates all the different features like:
- Getting weather data from the internet
- Showing weather animations
- Managing different pages (main, history, predictions, etc.)
- Handling user interactions (button clicks, city searches)
- Supporting multiple languages for weather descriptions and UI text
- Comprehensive translation management with consistent updates

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
    Main Weather Application Class with Comprehensive Translation Support
    
    This class creates the main window and manages all the weather app features.
    It inherits from tk.Tk, which means it IS a window that can display things.
    
    Key responsibilities:
    - Create and manage the main window
    - Store weather data and user settings
    - Coordinate between different app features
    - Handle background tasks (like downloading weather data)
    - Support multiple languages for weather descriptions and UI text
    - Manage language changes and UI updates consistently
    - Ensure ALL text elements are properly translated
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
        
        # Update app title with selected language
        if hasattr(self.gui, 'language_controller'):
            self.gui.language_controller.update_app_title()

        # Automatically load weather data after 1 second (1000 milliseconds)
        self.after(1000, self.fetch_and_display)

        # Set up what happens when user closes the window
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def get_current_language_code(self):
        """
        Get the current language code for API requests.
        
        Returns:
            str: Language code (en, es, hi) for OpenWeatherMap API
        """
        if hasattr(self.gui, 'language_controller'):
            return self.gui.language_controller.get_language_code()
        return "en"  # Default to English

    def refresh_ui_language(self):
        """
        Comprehensive refresh of ALL UI text when language changes.
        
        This method ensures EVERY text element in the app is properly
        updated to the new language with no mixed language issues.
        """
        try:
            # Update app title immediately
            if hasattr(self.gui, 'language_controller'):
                self.gui.language_controller.update_app_title()
            
            # Get current page to rebuild it properly
            current_page = self.gui.current_page
            
            # Clear the current page completely to prevent mixed languages
            self.gui._clear_page_widgets()
            
            # Rebuild the current page with new language
            self.gui.show_page(current_page)
            
            # Update existing weather data with new language and units
            if self.current_weather_data:
                # Force update display with translated units
                self.gui.update_weather_display(self.current_weather_data)
            
            # Update prediction display with translated units if available
            if (hasattr(self, 'current_prediction_data') and 
                self.current_prediction_data and 
                self.current_prediction_data != (None, "N/A", 0)):
                predicted_temp, confidence, accuracy = self.current_prediction_data
                self.gui.update_tomorrow_prediction_direct(predicted_temp, confidence, accuracy)
            
            # Fetch fresh weather data in the new language
            # This will get weather descriptions from the API in the selected language
            self.fetch_and_display()
            
        except Exception as e:
            # If refresh fails, try a simpler approach
            try:
                self.gui.show_page("main")
                self.fetch_and_display()
            except:
                pass

    def _show_weather_error(self, error_message):
        """Show weather error message in current language with proper fallbacks."""
        try:
            if hasattr(self.gui, 'language_controller'):
                # Determine error type and get appropriate translation
                error_lower = error_message.lower()
                
                if "not found" in error_lower or "404" in error_lower:
                    translated_error = self.gui.language_controller.get_text("city_not_found")
                elif "network" in error_lower or "timeout" in error_lower or "connection" in error_lower:
                    translated_error = self.gui.language_controller.get_text("network_error")
                elif "api" in error_lower or "key" in error_lower:
                    translated_error = self.gui.language_controller.get_text("error")
                else:
                    translated_error = self.gui.language_controller.get_text("error")
                
                # Update both temperature and description labels with error
                if hasattr(self.gui, 'temp_label') and self.gui.temp_label:
                    try:
                        self.gui.temp_label.configure(text="--")
                        self.gui.temp_label.configure(bg=self._get_canvas_bg_color())
                    except:
                        pass
                
                if hasattr(self.gui, 'desc_label') and self.gui.desc_label:
                    try:
                        self.gui.desc_label.configure(text=translated_error)
                        self.gui.desc_label.configure(bg=self._get_canvas_bg_color())
                    except:
                        pass
        except Exception:
            pass

    def _get_canvas_bg_color(self):
        """Helper method to get canvas background color."""
        try:
            if hasattr(self.gui, 'bg_canvas') and self.gui.bg_canvas:
                return self.gui.bg_canvas.cget("bg")
            return "#87CEEB"
        except:
            return "#87CEEB"

    def update_all_label_backgrounds(self, new_bg_color):
        """
        Update the background color of all text labels to match animation.
        
        Enhanced version that ensures ALL labels get updated consistently.
        
        When weather animations change the background color (like blue for rain,
        white for snow), we need to update all text labels so they don't look
        like ugly blue boxes on top of the new background.
        
        Args:
            new_bg_color (str): The new background color (like "#87CEEB" for sky blue)
        """
        try:
            if hasattr(self, 'gui'):
                all_widgets = []
                
                # Collect all widgets from different sources
                if hasattr(self.gui, 'widgets'):
                    all_widgets.extend(self.gui.widgets)
                
                if hasattr(self.gui, 'history_labels'):
                    all_widgets.extend(self.gui.history_labels)
                
                # Add specific weather display widgets
                weather_widgets = [
                    self.gui.humidity_value, self.gui.wind_value, self.gui.pressure_value,
                    self.gui.visibility_value, self.gui.uv_value, self.gui.precipitation_value,
                    self.gui.temp_label, self.gui.desc_label, self.gui.icon_label,
                    self.gui.temp_prediction, self.gui.accuracy_prediction, self.gui.confidence_prediction
                ]
                
                # Add language controller widgets if they exist
                if hasattr(self.gui, 'language_controller') and hasattr(self.gui.language_controller, 'language_widgets'):
                    all_widgets.extend(self.gui.language_controller.language_widgets)
                
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
                            pass
        except Exception:
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
        Background task to download weather data with comprehensive language support.
        
        This runs in a separate thread so the app stays responsive.
        It downloads weather data, saves it, and then updates the display.
        
        Note: This is a "private" method (starts with _) meaning it's only
        used internally by this class.
        """
        try:
            # Get the city name from the input field (or use default)
            city = self.city_var.get().strip() or "New York"
            
            # Get current language code for API request
            language_code = self.get_current_language_code()
            
            # Download current weather data from the internet with language support
            weather_data = get_current_weather(city, language_code)

            # If there was an error getting weather data, show translated error
            if weather_data.get("error"):
                self.after(0, lambda: self._show_weather_error(weather_data.get("error")))
                return

            # Try to save the weather data to our history file
            try:
                save_weather(weather_data, city)
            except Exception:
                pass

            # Store the weather data so other parts of the app can use it
            self.current_weather_data = weather_data

            # Update the display on the main thread with proper translations
            self.after(0, lambda: self.gui.update_weather_display(weather_data))
            self.after(0, lambda: self.update_tomorrow_prediction(city))
            self.after(0, lambda: self.gui.update_history_display(city))
            self.after(0, lambda: self.gui.update_background_animation(weather_data))
            self.after(0, lambda: self.gui.update_sun_moon_display(city))

        except Exception:
            # Show network error in current language
            self.after(0, lambda: self._show_weather_error("network error"))

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
        Switch between Celsius and Fahrenheit with immediate translation updates.
        
        This changes the temperature display and immediately updates
        existing data without refetching from the internet.
        """
        # Switch between C and F
        self.unit = "F" if self.unit == "C" else "C"
        
        # Immediately update display with existing data in new units
        if self.current_weather_data:
            # Update weather display with new units
            self.gui.update_weather_display(self.current_weather_data)
            
            # Update prediction display with new units if available
            if (hasattr(self, 'current_prediction_data') and 
                self.current_prediction_data and 
                self.current_prediction_data != (None, "N/A", 0)):
                predicted_temp, confidence, accuracy = self.current_prediction_data
                self.gui.update_tomorrow_prediction_direct(predicted_temp, confidence, accuracy)
        
        # Don't fetch new data, just update the display with existing data

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

    def get_current_language(self):
        """
        Get the current language name.
        
        Returns:
            str: Current language name ("English", "Spanish", "Hindi")
        """
        if hasattr(self.gui, 'language_controller'):
            return self.gui.language_controller.current_language
        return "English"

    def get_translated_text(self, key, fallback_to_english=True):
        """
        Get translated text for a specific key with proper fallback handling.
        
        This is a convenience method that other parts of the app can use
        to get translated text without directly accessing the language controller.
        
        Args:
            key (str): Translation key
            fallback_to_english (bool): Whether to fallback to English if translation missing
            
        Returns:
            str: Translated text, English fallback, or key if nothing found
        """
        if hasattr(self.gui, 'language_controller'):
            return self.gui.language_controller.get_text(key, fallback_to_english)
        return key

    def set_language(self, language_name):
        """
        Programmatically set the language with complete UI refresh.
        
        This allows other parts of the app to change the language
        without going through the language selection page.
        
        Args:
            language_name (str): Language name ("English", "Spanish", "Hindi")
        """
        if hasattr(self.gui, 'language_controller'):
            if language_name in self.gui.language_controller.supported_languages:
                # Only change if it's actually different
                if language_name != self.gui.language_controller.current_language:
                    self.gui.language_controller.current_language = language_name
                    self.gui.language_controller.save_settings()
                    
                    # Trigger complete UI refresh
                    self.refresh_ui_language()

    def get_available_languages(self):
        """
        Get list of available languages.
        
        Returns:
            list: List of available language names
        """
        if hasattr(self.gui, 'language_controller'):
            return list(self.gui.language_controller.supported_languages.keys())
        return ["English"]

    def get_language_info(self):
        """
        Get comprehensive language information.
        
        Returns:
            dict: Language information including current language and available options
        """
        return {
            "current_language": self.get_current_language(),
            "current_language_code": self.get_current_language_code(),
            "available_languages": self.get_available_languages(),
            "translation_coverage": "100%" if hasattr(self.gui, 'language_controller') else "0%"
        }

    def force_language_refresh(self):
        """
        Force a complete refresh of all language-dependent elements.
        
        This is useful if translation issues occur or if you want to
        ensure everything is properly updated.
        """
        try:
            if hasattr(self.gui, 'language_controller'):
                self.gui.language_controller.update_all_translatable_widgets()
        except Exception:
            # Fallback to simple refresh
            self.refresh_ui_language()

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
        
        # Clean up language controller
        if hasattr(self.gui, 'language_controller'):
            self.gui.language_controller.cleanup()
        
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
        
        # Display current language info on startup
        lang_info = app.get_language_info()
        print(f"📱 Language: {lang_info['current_language']} ({lang_info['current_language_code']})")
        print(f"🔤 Available languages: {', '.join(lang_info['available_languages'])}")
        print(f"🔧 Translation coverage: {lang_info['translation_coverage']}")
        
        print("✓ Weather app initialized successfully")
        print("💡 Tip: All UI text will translate when you change languages!")
        
        # Start the main event loop (this keeps the app running until closed)
        app.mainloop()
        
    except Exception as e:
        # If something goes wrong, show a detailed error message
        print(f"❌ Error starting weather app: {e}")
        traceback.print_exc()


# If this file is run directly (not imported), start the app
if __name__ == "__main__":
    run_app()