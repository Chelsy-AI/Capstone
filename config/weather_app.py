import tkinter as tk
import threading
import traceback
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from features.tomorrows_guess.predictor import get_tomorrows_prediction
from config.themes import LIGHT_THEME, DARK_THEME
from config.api import get_current_weather
from config.storage import save_weather
from config.gui import WeatherGUI

from features.interactive_map.controller import MapController


class WeatherApp(tk.Tk):
    """
    Weather Application Main Logic
    
    This class handles the core business logic and data management
    for the weather application. All GUI components are handled by 
    the modular GUI system in config.gui.
    """
    
    def __init__(self):
        super().__init__()
        
        self.title("Smart Weather App")
        self.geometry("800x600")
        self.minsize(700, 500)
        
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
        
        # Initialize modular GUI system
        self.gui = WeatherGUI(self)
        
        # Build GUI
        self.gui.build_gui()
        
        # Auto-load weather
        self.after(1000, self.fetch_and_display)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Map controller for interactive map
        self.map_controller = MapController(self.gui.main_frame, self.city_var.get)


    def fetch_and_display(self):
        """Fetch and display weather data"""
        threading.Thread(target=self._fetch_weather, daemon=True).start()

    def _fetch_weather(self):
        """Fetch weather in background thread"""
        try:
            city = self.city_var.get().strip() or "New York"
            print(f"🌍 Fetching weather for: {city}")
            
            weather_data = get_current_weather(city)
            
            if weather_data.get("error"):
                print(f"❌ Error: {weather_data['error']}")
                return
            
            # Save to CSV
            try:
                save_weather(weather_data)
                print("✅ Weather data saved to CSV")
            except Exception as e:
                print(f"⚠️ CSV save error: {e}")
            
            # Store data for preservation across rebuilds
            self.current_weather_data = weather_data
            
            # Update GUI components
            self.after(0, lambda: self.gui.update_weather_display(weather_data))
            self.after(0, lambda: self.update_tomorrow_prediction(city))
            self.after(0, lambda: self.gui.update_history_display(city))
            self.after(0, lambda: self.gui.update_background_animation(weather_data))
            self.map_controller = MapController(self, self.city_var.get)

        except Exception as e:
            print(f"❌ Weather fetch error: {e}")

    def update_tomorrow_prediction(self, city):
        """Update tomorrow's prediction metrics"""
        try:
            predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)
            
            # Store data for preservation
            self.current_prediction_data = (predicted_temp, confidence, accuracy)
            
            # Update using the GUI method
            self.gui.update_tomorrow_prediction_direct(predicted_temp, confidence, accuracy)
                
        except Exception as e:
            print(f"❌ Prediction error: {e}")

    def toggle_theme(self):
        """Toggle theme - delegate to GUI"""
        self.gui.toggle_theme()

    def toggle_unit(self):
        """Toggle temperature unit"""
        self.unit = "F" if self.unit == "C" else "C"
        print(f"🌡️ Unit changed to: {self.unit}")
        self.fetch_and_display()

    def on_close(self):
        """Clean up resources"""
        self.gui.cleanup_animation()
        self.destroy()


def run_app():
    """Main entry point"""
    try:
        print("🚀 Starting Weather App with Modular GUI...")
        app = WeatherApp()
        print("✅ App started successfully")
        app.mainloop()
    except Exception as e:
        print(f"💥 Error: {e}")
        traceback.print_exc()


# Make sure this is available for import
__all__ = ['run_app', 'WeatherApp']


if __name__ == "__main__":
    run_app()
    