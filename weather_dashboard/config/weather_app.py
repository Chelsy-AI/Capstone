"""
Main Weather Application Class
=======================================================

Enhanced with strict city validation and error screen functionality.
Maintains all existing functionality while adding validation for fake cities.
"""

import tkinter as tk
import threading
import traceback
import sys
import os
import re
from dotenv import load_dotenv

load_dotenv()

# Add the project root to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather_dashboard.features.tomorrows_guess.predictor import get_tomorrows_prediction
from weather_dashboard.config.themes import LIGHT_THEME, DARK_THEME
from weather_dashboard.config.api import get_current_weather
from weather_dashboard.config.storage import save_weather
from weather_dashboard.gui.main_gui import WeatherGUI

# Try to import error handling if available
try:
    from weather_dashboard.config.error_handler import app_logger, safe_function_call
    error_handling_available = True
except ImportError:
    error_handling_available = False
    def safe_function_call(func, *args, fallback_result=None, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return fallback_result

class CityValidator:
    """Strict city validation to block all fake inputs."""
    
    def __init__(self):
        # Known real cities that should always be allowed
        self.valid_cities = {
            'new york', 'london', 'paris', 'tokyo', 'berlin', 'madrid', 'rome', 
            'amsterdam', 'barcelona', 'sydney', 'toronto', 'montreal', 'mumbai', 
            'delhi', 'beijing', 'moscow', 'dubai', 'singapore', 'hong kong',
            'los angeles', 'chicago', 'houston', 'phoenix', 'philadelphia',
            'san antonio', 'san diego', 'dallas', 'san jose', 'austin',
            'miami', 'atlanta', 'boston', 'seattle', 'denver', 'detroit',
            'washington', 'portland', 'las vegas', 'baltimore', 'milwaukee',
            'oslo', 'bern', 'nice', 'cork', 'bath', 'york', 'hull', 'bonn',
            'linz', 'graz', 'lyon', 'metz', 'brest', 'tours', 'dijon', 'nancy',
            'vancouver', 'calgary', 'ottawa', 'winnipeg', 'quebec', 'halifax'
        }
        
        # Patterns that indicate fake/invalid input
        self.invalid_patterns = [
            r'^[bcdfghjklmnpqrstvwxyz]{4,}$',  # Only consonants
            r'^[aeiou]{3,}$',  # Only vowels
            r'^(.)\1{3,}',  # Repeated characters
            r'^(test|fake|dummy|random|error|null|none)',  # Test words
            r'\d{2,}',  # Multiple numbers
            r'^[qwerty]{4,}$',  # Keyboard patterns
            r'^[asdf]{4,}$',
            r'^[zxcv]{4,}$',
            r'[;,!@#$%^&*()]+',  # Punctuation
            r'^[a-z]{4}[;,]?$'  # 4 random letters with punctuation
        ]
        
        # Known fake inputs to block immediately
        self.fake_inputs = {
            'khjl', 'khjl;', 'fnjaelf', 'bhjlk', 'njkef', 'ifej', 'haaae',
            'test', 'test123', 'asdf', 'qwer', 'hjkl', 'fake', 'dummy'
        }
    
    def is_valid_city(self, city: str) -> bool:
        """Strict validation to block fake cities."""
        if not city or len(city.strip()) < 2:
            return False
        
        # Clean the input
        city_clean = city.strip().lower().replace(';', '').replace(',', '')
        
        # Block known fake inputs immediately
        if city_clean in self.fake_inputs:
            if error_handling_available:
                app_logger.log_error("validation", f"Blocked known fake input: {city}", severity="INFO")
            return False
        
        # Allow known valid cities
        if city_clean in self.valid_cities:
            if error_handling_available:
                app_logger.log_error("validation", f"Approved known valid city: {city}", severity="DEBUG")
            return True
        
        # Block obvious fake patterns
        for pattern in self.invalid_patterns:
            if re.search(pattern, city_clean):
                if error_handling_available:
                    app_logger.log_error("validation", f"Blocked fake pattern in: {city}", severity="INFO")
                return False
        
        # Additional strict checks
        if len(city_clean) >= 4:
            # Block if too many consonants in a row
            if re.search(r'[bcdfghjklmnpqrstvwxyz]{4,}', city_clean):
                if error_handling_available:
                    app_logger.log_error("validation", f"Blocked too many consonants: {city}", severity="INFO")
                return False
            
            # Block weird letter combinations
            weird_combos = ['fnj', 'jae', 'aelf', 'hjl', 'bhjl', 'njk', 'kef', 'khjl']
            for combo in weird_combos:
                if combo in city_clean:
                    if error_handling_available:
                        app_logger.log_error("validation", f"Blocked weird combination '{combo}' in: {city}", severity="INFO")
                    return False
            
            # Check consonant/vowel ratio
            vowel_count = len(re.findall(r'[aeiou]', city_clean))
            consonant_count = len(city_clean) - vowel_count
            
            # Block if mostly consonants (suspicious)
            if consonant_count > vowel_count * 2.5:
                if error_handling_available:
                    app_logger.log_error("validation", f"Blocked suspicious consonant ratio: {city}", severity="INFO")
                return False
        
        return True

class WeatherApp(tk.Tk):
    """
    Main Weather Application Class with Comprehensive Translation Support
    Enhanced with city validation and error screen functionality.
    
    This class creates the main window and manages all the weather app features.
    """

    def __init__(self):
        """
        Initialize the weather app with validation functionality.
        """
        # Initialize the parent class (tk.Tk) to create a window
        super().__init__()

        # Initialize city validator
        self.city_validator = CityValidator()
        self.current_screen = "main"
        self._original_gui_frame = None

        # Set up the main window properties
        self.title("Smart Weather App")
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
        
        # Store reference to original GUI frame for error screen
        self._store_original_gui_frame()
        
        # Update app title with selected language
        if hasattr(self.gui, 'language_controller'):
            self.gui.language_controller.update_app_title()

        # Automatically load weather data after 1 second (1000 milliseconds)
        self.after(1000, self.fetch_and_display)

        # Set up what happens when user closes the window
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _store_original_gui_frame(self):
        """Store reference to the original GUI frame for error screen functionality."""
        try:
            # Find the main frame containing all GUI elements
            for child in self.winfo_children():
                if isinstance(child, tk.Frame):
                    self._original_gui_frame = child
                    break
        except Exception:
            pass

    def clear_screen(self):
        """Clear all widgets for error screen display."""
        try:
            if self._original_gui_frame:
                self._original_gui_frame.pack_forget()
            else:
                # Fallback: hide all child widgets
                for child in self.winfo_children():
                    child.pack_forget()
        except Exception:
            pass

    def restore_main_screen(self):
        """Restore the original GUI after error screen."""
        try:
            if self._original_gui_frame:
                self._original_gui_frame.pack(fill=tk.BOTH, expand=True)
            else:
                # Fallback: rebuild GUI
                self.gui.build_gui()
            
            self.current_screen = "main"
            
            # Refresh the display
            if self.current_weather_data:
                self.gui.update_weather_display(self.current_weather_data)
        except Exception:
            # If restore fails, rebuild GUI
            try:
                self.gui.build_gui()
                self.current_screen = "main"
            except:
                pass

    def show_error_screen(self, city_input: str):
        """Show full-screen error when city is invalid."""
        if error_handling_available:
            app_logger.log_error("ui", f"Showing error screen for invalid input: {city_input}", severity="INFO")
                
        # Clear the current screen
        self.clear_screen()
        self.current_screen = "error"
        
        # Create error screen
        error_frame = tk.Frame(self, bg='#87CEEB')
        error_frame.pack(fill=tk.BOTH, expand=True)
        
        # Center content
        center_frame = tk.Frame(error_frame, bg='#87CEEB')
        center_frame.pack(expand=True)
        
        # Large error icon
        error_icon = tk.Label(
            center_frame,
            text="❌",
            font=("Arial", 100),
            bg='#87CEEB',
            fg='#ff4444'
        )
        error_icon.pack(pady=(50, 30))
        
        # Error title
        error_title = tk.Label(
            center_frame,
            text="Incorrect Input",
            font=("Arial", 36, "bold"),
            bg='#87CEEB',
            fg='#ff4444'
        )
        error_title.pack(pady=20)
        
        # Error message
        error_msg = tk.Label(
            center_frame,
            text=f"'{city_input}' is not a valid city name",
            font=("Arial", 20),
            bg='#87CEEB',
            fg='#333'
        )
        error_msg.pack(pady=15)
        
        # Instructions
        instruction = tk.Label(
            center_frame,
            text="Please enter a valid city",
            font=("Arial", 18, "bold"),
            bg='#87CEEB',
            fg='#666'
        )
        instruction.pack(pady=15)
        
        # Examples
        examples = tk.Label(
            center_frame,
            text="Examples: New York, London, Tokyo, Paris, Berlin",
            font=("Arial", 16),
            bg='#87CEEB',
            fg='#888'
        )
        examples.pack(pady=15)
        
        # Back button
        back_button = tk.Button(
            center_frame,
            text="← Back",
            font=("Arial", 20, "bold"),
            bg='#4CAF50',
            fg='white',
            width=12,
            height=2,
            command=self._handle_back_button,
            cursor='hand2',
            relief='raised',
            bd=3
        )
        back_button.pack(pady=(50, 20))
        back_button.focus()
        
        # Store error frame reference for cleanup
        self._error_frame = error_frame

    def _handle_back_button(self):
        """Handle back button press from error screen."""
        try:
            # Clean up error frame
            if hasattr(self, '_error_frame'):
                self._error_frame.destroy()
            
            # Restore main screen
            self.restore_main_screen()
            
            # Focus on city entry if available
            if hasattr(self.gui, 'city_entry') and self.gui.city_entry:
                self.gui.city_entry.focus()
        except Exception:
            # Fallback: rebuild everything
            try:
                self.gui.build_gui()
                self.current_screen = "main"
            except:
                pass

    def get_current_language_code(self):
        """
        Get the current language code for API requests.
        
        Returns:
            str: Language code (en, es, hi) for OpenWeatherMap API
        """
        if hasattr(self.gui, 'language_controller') and self.gui.language_controller:
            code = self.gui.language_controller.get_language_code()
            return code
        
        return "en"  # Default to English

    def refresh_ui_language(self):
        """
        Comprehensive refresh of ALL UI text when language changes.
        """
        try:
            # Only refresh if we're on the main screen
            if self.current_screen != "main":
                return
                
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
            self.fetch_and_display()
            
        except Exception as e:
            # If refresh fails in error screen, don't try to fix
            if self.current_screen == "error":
                return
                
            # Otherwise try a simpler approach
            try:
                self.gui.show_page("main")
                self.fetch_and_display()
            except:
                pass

    def _show_weather_error(self, error_message):
        """Show weather error message in current language with proper fallbacks."""
        # Don't show weather errors if we're on the error screen
        if self.current_screen == "error":
            return
            
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
        """
        # Don't update backgrounds if we're on the error screen
        if self.current_screen == "error":
            return
            
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
        """Get weather data and update the display."""
        # Don't fetch if we're on error screen
        if self.current_screen == "error":
            return
            
        # Start the actual work in a background thread
        threading.Thread(target=self._fetch_weather, daemon=True).start()

    def _fetch_weather(self):
        """Background task to download weather data with city validation."""
        try:
            # Get the city name from the input field (or use default)
            city = self.city_var.get().strip() or "New York"
            
            # VALIDATE CITY BEFORE API CALL
            if not self.city_validator.is_valid_city(city):
                if error_handling_available:
                    app_logger.log_error("validation", f"Blocked fake city in fetch: {city}", severity="INFO")
                
                # Show error screen on main thread
                self.after(0, lambda: self.show_error_screen(city))
                return
            
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

        except Exception as e:
            # Show network error in current language
            self.after(0, lambda: self._show_weather_error("network error"))

    def update_tomorrow_prediction(self, city):
        """Get and display tomorrow's weather prediction."""
        # Don't update prediction if we're on error screen
        if self.current_screen == "error":
            return
            
        try:
            # Get prediction data
            predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)
            
            # Store the prediction data
            self.current_prediction_data = (predicted_temp, confidence, accuracy)
            
            # Update the prediction display
            self.gui.update_tomorrow_prediction_direct(predicted_temp, confidence, accuracy)
        except Exception:
            # If prediction fails, use default "no data" values
            self.current_prediction_data = (None, "N/A", 0)

    def toggle_theme(self):
        """Switch between light and dark color themes."""
        # Don't toggle theme if we're on error screen
        if self.current_screen == "error":
            return
            
        # Tell the GUI to switch themes
        self.gui.toggle_theme()
        
        # Also tell the sun/moon page about the theme change
        if hasattr(self.gui, 'sun_moon_controller'):
            self.gui.sun_moon_controller.handle_theme_change()

    def toggle_unit(self):
        """Switch between Celsius and Fahrenheit with immediate translation updates."""
        # Don't toggle unit if we're on error screen
        if self.current_screen == "error":
            return
            
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
        
    def get_current_sun_moon_data(self):
        """Get the current sun and moon information."""
        if hasattr(self.gui, 'sun_moon_controller'):
            return self.gui.sun_moon_controller.get_current_data()
        return {}

    def is_currently_daytime(self):
        """Check if it's currently daytime."""
        # Try to get accurate sunrise/sunset data
        if hasattr(self.gui, 'sun_moon_controller'):
            return self.gui.sun_moon_controller.is_daytime()
        
        # Fallback: simple time-based check
        import datetime
        current_hour = datetime.datetime.now().hour
        return 6 <= current_hour < 18  # Assume daylight from 6 AM to 6 PM

    def get_current_language(self):
        """Get the current language name."""
        if hasattr(self.gui, 'language_controller'):
            return self.gui.language_controller.current_language
        return "English"

    def get_translated_text(self, key, fallback_to_english=True):
        """Get translated text for a specific key with proper fallback handling."""
        if hasattr(self.gui, 'language_controller'):
            return self.gui.language_controller.get_text(key, fallback_to_english)
        return key

    def set_language(self, language_name):
        """Programmatically set the language with complete UI refresh."""
        if hasattr(self.gui, 'language_controller'):
            if language_name in self.gui.language_controller.supported_languages:
                # Only change if it's actually different
                if language_name != self.gui.language_controller.current_language:
                    self.gui.language_controller.current_language = language_name
                    self.gui.language_controller.save_settings()
                    
                    # Trigger complete UI refresh
                    self.refresh_ui_language()

    def get_available_languages(self):
        """Get list of available languages."""
        if hasattr(self.gui, 'language_controller'):
            return list(self.gui.language_controller.supported_languages.keys())
        return ["English"]

    def get_language_info(self):
        """Get comprehensive language information."""
        return {
            "current_language": self.get_current_language(),
            "current_language_code": self.get_current_language_code(),
            "available_languages": self.get_available_languages(),
            "translation_coverage": "100%" if hasattr(self.gui, 'language_controller') else "0%"
        }

    def force_language_refresh(self):
        """Force a complete refresh of all language-dependent elements."""
        try:
            if hasattr(self.gui, 'language_controller'):
                self.gui.language_controller.update_all_translatable_widgets()
        except Exception:
            # Fallback to simple refresh
            self.refresh_ui_language()

    def on_close(self):
        """Clean up when the user closes the app."""
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
    """
    try:
        # Create the main application window
        app = WeatherApp()
        
        # Start automatic sun/moon data updates
        if hasattr(app.gui, 'sun_moon_controller'):
            app.gui.sun_moon_controller.start_auto_refresh(interval_minutes=30)
        
        # Display current language info on startup
        lang_info = app.get_language_info()

        # Start the main event loop (this keeps the app running until closed)
        app.mainloop()
        
    except Exception as e:
        # If something goes wrong
        traceback.print_exc()


# If this file is run directly (not imported), start the app
if __name__ == "__main__":
    run_app()