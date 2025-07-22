import tkinter as tk
import threading
import traceback
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    """

    def __init__(self):
        super().__init__()

        self.title("Smart Weather App with Sun & Moon Phases")
        self.geometry("800x700")
        self.minsize(700, 600)

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
        self.current_sun_moon_data = {}

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
            if hasattr(self, 'gui'):
                all_widgets = []
                
                if hasattr(self.gui, 'widgets'):
                    all_widgets.extend(self.gui.widgets)
                
                if hasattr(self.gui, 'history_labels'):
                    all_widgets.extend(self.gui.history_labels)
                
                weather_widgets = [
                    self.gui.humidity_value, self.gui.wind_value, self.gui.pressure_value,
                    self.gui.visibility_value, self.gui.uv_value, self.gui.precipitation_value,
                    self.gui.temp_label, self.gui.desc_label, self.gui.icon_label,
                    self.gui.temp_prediction, self.gui.accuracy_prediction, self.gui.confidence_prediction
                ]
                
                for widget in weather_widgets:
                    if widget:
                        all_widgets.append(widget)
                
                for widget in all_widgets:
                    if widget and hasattr(widget, 'configure'):
                        try:
                            widget_class = widget.winfo_class()
                            if widget_class == 'Label':
                                widget.configure(bg=new_bg_color)
                        except Exception:
                            pass
        except Exception:
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

            try:
                save_weather(weather_data, city)
            except Exception:
                pass

            self.current_weather_data = weather_data

            self.after(0, lambda: self.gui.update_weather_display(weather_data))
            self.after(0, lambda: self.update_tomorrow_prediction(city))
            self.after(0, lambda: self.gui.update_history_display(city))
            self.after(0, lambda: self.gui.update_background_animation(weather_data))
            self.after(0, lambda: self.gui.update_sun_moon_display(city))

        except Exception:
            pass

    def update_tomorrow_prediction(self, city):
        """Update tomorrow's prediction metrics"""
        try:
            predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)
            self.current_prediction_data = (predicted_temp, confidence, accuracy)
            self.gui.update_tomorrow_prediction_direct(predicted_temp, confidence, accuracy)
        except Exception:
            self.current_prediction_data = (None, "N/A", 0)

    def toggle_theme(self):
        """Toggle theme"""
        self.gui.toggle_theme()
        
        if hasattr(self.gui, 'sun_moon_controller'):
            self.gui.sun_moon_controller.handle_theme_change()

    def toggle_unit(self):
        """Toggle temperature unit"""
        self.unit = "F" if self.unit == "C" else "C"
        self.fetch_and_display()

    def get_current_sun_moon_data(self):
        """Get current sun/moon data"""
        if hasattr(self.gui, 'sun_moon_controller'):
            return self.gui.sun_moon_controller.get_current_data()
        return {}

    def is_currently_daytime(self):
        """Check if it's currently daytime"""
        if hasattr(self.gui, 'sun_moon_controller'):
            return self.gui.sun_moon_controller.is_daytime()
        
        import datetime
        current_hour = datetime.datetime.now().hour
        return 6 <= current_hour < 18

    def on_close(self):
        """Clean up resources"""
        self.gui.cleanup_animation()
        
        if hasattr(self.gui, 'sun_moon_controller'):
            self.gui.sun_moon_controller.cleanup()
        
        self.destroy()


def run_app():
    """Main entry point"""
    try:
        print("🌤️ Starting Weather Application...")
        app = WeatherApp()
        
        if hasattr(app.gui, 'sun_moon_controller'):
            app.gui.sun_moon_controller.start_auto_refresh(interval_minutes=30)
        
        print("✓ Weather app initialized successfully")
        app.mainloop()
        
    except Exception as e:
        print(f"❌ Error starting weather app: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    run_app()