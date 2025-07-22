import tkinter as tk
import threading
import traceback
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("weatherdb_api_key")

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from features.tomorrows_guess.predictor import get_tomorrows_prediction
from config.themes import LIGHT_THEME, DARK_THEME
from config.api import get_current_weather
from config.storage import save_weather
from config.gui import WeatherGUI


class WeatherApp(tk.Tk):
    """
    Weather Application Main Logic with Dynamic Background Updates and Sun/Moon Integration

    This class handles the core business logic and data management
    for the weather application. All GUI components are handled by 
    the modular GUI system in config.gui.
    """

    def __init__(self):
        super().__init__()

        self.title("Smart Weather App with Sun & Moon Phases")
        self.geometry("800x700")  # Increased height for new button
        self.minsize(700, 600)    # Increased minimum height

        # Initialize variables
        self.city_var = tk.StringVar(value="New York")
        self.unit = "C"
        self.temp_c = None
        self.temp_f = None
        self.theme = LIGHT_THEME
        self.text_color = "black"

        # Data storage to preserve across rebuilds
        self.current_weather_data = {}
        self.current_prediction_data = {}
        self.current_history_data = []
        self.current_sun_moon_data = {}  # Add sun/moon data storage

        # Initialize modular GUI system
        self.gui = WeatherGUI(self)

        # Build GUI
        self.gui.build_gui()

        # Auto-load weather
        self.after(1000, self.fetch_and_display)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_all_label_backgrounds(self, new_bg_color):
        """Update all label backgrounds to match animation background"""
        try:
            # Update all widgets in GUI
            if hasattr(self, 'gui'):
                all_widgets = []
                
                # Get main widgets
                if hasattr(self.gui, 'widgets'):
                    all_widgets.extend(self.gui.widgets)
                
                # Get history labels
                if hasattr(self.gui, 'history_labels'):
                    all_widgets.extend(self.gui.history_labels)
                
                # Get specific weather widgets
                weather_widgets = [
                    self.gui.humidity_value, self.gui.wind_value, self.gui.pressure_value,
                    self.gui.visibility_value, self.gui.uv_value, self.gui.precipitation_value,
                    self.gui.temp_label, self.gui.desc_label, self.gui.icon_label,
                    self.gui.temp_prediction, self.gui.accuracy_prediction, self.gui.confidence_prediction
                ]
                
                for widget in weather_widgets:
                    if widget:
                        all_widgets.append(widget)
                
                # Update all label backgrounds
                for widget in all_widgets:
                    if widget and hasattr(widget, 'configure'):
                        try:
                            widget_class = widget.winfo_class()
                            if widget_class == 'Label':
                                widget.configure(bg=new_bg_color)
                        except Exception as e:
                            # Widget might be destroyed, skip
                            pass
                            
            
        except Exception as e:
            pass

    def fetch_and_display(self):
        """Fetch and display weather data"""
        threading.Thread(target=self._fetch_weather, daemon=True).start()

    def _fetch_weather(self):
        """Fetch weather in background thread"""
        try:
            city = self.city_var.get().strip() or "New York"

            weather_data = get_current_weather(city)

            if weather_data.get("error"):
                return

            # Save to CSV with proper city name
            try:
                # Pass the city name explicitly to ensure proper tracking
                save_weather(weather_data, city)
            except Exception as e:
                pass

            # Store data for preservation across rebuilds
            self.current_weather_data = weather_data

            # Update GUI components
            self.after(0, lambda: self.gui.update_weather_display(weather_data))
            self.after(0, lambda: self.update_tomorrow_prediction(city))
            self.after(0, lambda: self.gui.update_history_display(city))
            self.after(0, lambda: self.gui.update_background_animation(weather_data))
            
            # Update sun/moon page when city changes
            self.after(0, lambda: self.gui.update_sun_moon_display(city))

        except Exception as e:
            pass

    def update_tomorrow_prediction(self, city):
        """Update tomorrow's prediction metrics"""
        try:
            predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)

            # Store data for preservation
            self.current_prediction_data = (predicted_temp, confidence, accuracy)

            # Update using the GUI method - this will handle page-specific display
            self.gui.update_tomorrow_prediction_direct(predicted_temp, confidence, accuracy)

        except Exception as e:
            # Store empty data so we don't keep trying
            self.current_prediction_data = (None, "N/A", 0)

    def toggle_theme(self):
        """Toggle theme - delegate to GUI and update sun/moon"""
        self.gui.toggle_theme()
        
        # Update sun/moon theme if controller exists
        if hasattr(self.gui, 'sun_moon_controller'):
            self.gui.sun_moon_controller.handle_theme_change()

    def toggle_unit(self):
        """Toggle temperature unit"""
        self.unit = "F" if self.unit == "C" else "C"
        self.fetch_and_display()

    def get_current_sun_moon_data(self):
        """Get current sun/moon data for other components"""
        if hasattr(self.gui, 'sun_moon_controller'):
            return self.gui.sun_moon_controller.get_current_data()
        return {}

    def is_currently_daytime(self):
        """Check if it's currently daytime based on sun/moon data"""
        if hasattr(self.gui, 'sun_moon_controller'):
            return self.gui.sun_moon_controller.is_daytime()
        
        # Fallback to simple time check
        import datetime
        current_hour = datetime.datetime.now().hour
        return 6 <= current_hour < 18

    def get_current_moon_phase(self):
        """Get current moon phase information"""
        if hasattr(self.gui, 'sun_moon_controller'):
            return self.gui.sun_moon_controller.get_moon_phase()
        return {}

    def get_current_sun_position(self):
        """Get current sun position"""
        if hasattr(self.gui, 'sun_moon_controller'):
            return self.gui.sun_moon_controller.get_sun_position()
        return {}

    def refresh_all_data(self):
        """Refresh all data (weather, predictions, sun/moon)"""
        city = self.city_var.get().strip() or "New York"
        
        # Refresh weather data
        self.fetch_and_display()
        
        # Refresh sun/moon data if on that page
        if hasattr(self.gui, 'sun_moon_controller'):
            self.gui.sun_moon_controller.refresh_data()

    def show_sun_moon_page(self):
        """Directly show the sun/moon page"""
        if hasattr(self.gui, 'show_page'):
            self.gui.show_page("sun_moon")

    def on_close(self):
        """Clean up resources"""
        
        # Clean up GUI resources
        self.gui.cleanup_animation()
        
        # Clean up sun/moon controller
        if hasattr(self.gui, 'sun_moon_controller'):
            self.gui.sun_moon_controller.cleanup()
        
        self.destroy()


def run_app():
    """Main entry point"""
    try:
        app = WeatherApp()
        
        # Optional: Start auto-refresh for sun/moon data
        if hasattr(app.gui, 'sun_moon_controller'):
            app.gui.sun_moon_controller.start_auto_refresh(interval_minutes=30)
        
        app.mainloop()
        
    except Exception as e:
        traceback.print_exc()


# Make sure this is available for import
__all__ = ['run_app', 'WeatherApp']


if __name__ == "__main__":
    run_app()