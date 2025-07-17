import customtkinter as ctk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from datetime import datetime
import threading
import tkinter as tk
import traceback
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from features.history_tracker.api import fetch_world_history
from features.history_tracker.display import insert_temperature_history_as_grid
from features.tomorrows_guess.display import update_tomorrow_guess_display
from features.tomorrows_guess.predictor import get_tomorrows_prediction

from core.theme import LIGHT_THEME, DARK_THEME
from gui.gui_builder import build_gui
from core.api import get_current_weather

# Import weather animation
try:
    from gui.weather_animation import WeatherAnimation
    ANIMATION_AVAILABLE = True
    print("✅ Weather animation loaded successfully")
except ImportError:
    print("⚠️ Weather animation module not found. Using fallback.")
    ANIMATION_AVAILABLE = False
    
    class WeatherAnimation:
        def __init__(self, canvas):
            self.canvas = canvas
            self.is_running = False
        def start_animation(self, weather_type="clear"):
            self.is_running = True
            print(f"Animation placeholder: {weather_type}")
        def stop_animation(self):
            self.is_running = False
        def set_weather_type(self, weather_type):
            print(f"Animation placeholder: {weather_type}")
        def update_size(self, width, height):
            pass
        def update_theme(self, theme):
            pass


class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.theme = LIGHT_THEME
        ctk.set_appearance_mode("light")
        self.title("Weather App")
        self.geometry("800x600")

        self.city_var = ctk.StringVar(value="New York")
        self.unit = "C"

        self.temp_c = None
        self.temp_f = None
        self.metric_value_labels = {}
        self.icon_cache = {}
        self.current_weather_condition = "clear"
        self.history_data = {}

        # Validate theme
        self._validate_theme()
        self.configure(fg_color=self.theme["bg"])

        # Create animation canvas FIRST (background layer)
        self.bg_canvas = tk.Canvas(self, highlightthickness=0, bg="#87CEEB")
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Initialize weather animation
        if ANIMATION_AVAILABLE:
            self.smart_background = WeatherAnimation(self.bg_canvas)
            print("🎬 Starting initial animation...")
            self.smart_background.start_animation("rain")  # Start with visible animation for testing
        else:
            self.smart_background = None

        # Build the GUI on top of the canvas
        self.after(100, self._init_gui)

        # Handle window events
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind("<Configure>", self.on_window_resize)

    def _validate_theme(self):
        """Ensure theme has all required keys"""
        defaults = {
            "bg": "#FFFFFF",
            "fg": "#000000",
            "button_bg": "#007ACC",
            "button_fg": "#FFFFFF",
            "text_bg": "#F0F0F0",
            "text_fg": "#000000",
            "entry_bg": "#FFFFFF"
        }
        for key, default_color in defaults.items():
            if key not in self.theme or not self.theme[key]:
                self.theme[key] = default_color

    def _init_gui(self):
        """Initialize GUI after canvas is ready"""
        # Build GUI widgets
        build_gui(self)
        
        # Start weather update
        self.after(1000, lambda: threading.Thread(target=self.safe_update_weather, daemon=True).start())

    def get_text_color(self):
        """Get text color based on current theme"""
        return "white" if self.theme == DARK_THEME else "black"

    def get_value_color(self):
        """Get value text color based on current theme"""
        return "yellow" if self.theme == DARK_THEME else "blue"

    def on_window_resize(self, event):
        """Handle window resize to update canvas and animation"""
        if event.widget == self:
            # Update canvas size
            width = event.width
            height = event.height
            self.bg_canvas.configure(width=width, height=height)
            # Update animation dimensions
            if self.smart_background and ANIMATION_AVAILABLE:
                self.smart_background.update_size(width, height)

    def update_background(self, weather_condition):
        """Update the animated background based on weather condition"""
        if self.smart_background and ANIMATION_AVAILABLE:
            try:
                print(f"🎬 Updating background animation to: {weather_condition}")
                self.smart_background.set_weather_type(weather_condition)
            except Exception as e:
                print(f"❌ Animation error: {e}")
                traceback.print_exc()

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.theme = DARK_THEME if self.theme == LIGHT_THEME else LIGHT_THEME
        ctk.set_appearance_mode("dark" if self.theme == DARK_THEME else "light")
        self.configure(fg_color=self.theme["bg"])

        print(f"🎨 Theme toggled to: {'Dark' if self.theme == DARK_THEME else 'Light'}")

        # Rebuild GUI with new theme colors
        build_gui(self)

        # Update background animation
        if self.smart_background and ANIMATION_AVAILABLE:
            current_condition = self.current_weather_condition or "clear"
            self.smart_background.set_weather_type(current_condition)

    def toggle_temp_unit(self, event=None):
        """Toggle between Celsius and Fahrenheit"""
        self.unit = "F" if self.unit == "C" else "C"
        self.update_temperature_label()
        self.update_tomorrow_prediction()
        self.update_weather_history()
        print(f"🌡️ Temperature unit changed to: {self.unit}")

    def update_temperature_label(self):
        """Update the temperature display"""
        if not hasattr(self, "temp_label") or self.temp_label is None:
            return
        if self.temp_c is None:
            self.temp_label.configure(text="N/A")
        elif self.unit == "C":
            self.temp_label.configure(text=f"{self.temp_c} °C")
        else:
            self.temp_label.configure(text=f"{self.temp_f} °F")

    def safe_update_weather(self):
        """Safely update weather data in background thread"""
        try:
            self.update_weather()
        except Exception as e:
            print(f"❌ Error updating weather: {e}")
            traceback.print_exc()

    def update_weather(self):
        """Update weather data and UI"""
        city = self.city_var.get().strip() or "New York"
        print(f"🌍 Updating weather for: {city}")
        
        # Fetch weather data
        self.history_data = fetch_world_history(city)
        data = get_current_weather(city)

        if data.get("error"):
            self._handle_weather_error(data["error"])
            return

        # Update temperature data
        temp_c = data.get("temperature")
        if temp_c is not None:
            self.temp_c = round(temp_c, 1)
            self.temp_f = round((temp_c * 9 / 5) + 32, 1)
            print(f"🌡️ Temperature: {self.temp_c}°C ({self.temp_f}°F)")
        else:
            self.temp_c = self.temp_f = None

        self.update_temperature_label()
        
        # Update description
        description = data.get("description", "No description")
        print(f"☁️ Weather: {description}")
        if hasattr(self, "desc_label") and self.desc_label:
            self.desc_label.configure(text=description)
        
        # Update timestamp
        if hasattr(self, "update_label") and self.update_label:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            self.update_label.configure(text=f"Updated at {timestamp}")

        # Update weather icon
        self._update_weather_icon(data.get("icon"))

        # Update metrics
        self._update_weather_metrics(data)

        # Update background animation based on weather condition
        weather_condition = description.lower() if description else "clear"
        self.current_weather_condition = weather_condition
        
        # Map weather descriptions to animation types
        animation_type = self.map_weather_to_animation(weather_condition)
        print(f"🎬 Weather '{weather_condition}' → Animation '{animation_type}'")
        
        # Update animation immediately
        self.update_background(animation_type)
        
        # Update other components
        self.after(0, lambda: self.update_tomorrow_prediction(city))
        self.after(0, self.update_weather_history)

    def _handle_weather_error(self, error_msg):
        """Handle weather data errors"""
        print(f"❌ Weather error: {error_msg}")
        self.temp_c = None
        self.temp_f = None
        
        if hasattr(self, "temp_label") and self.temp_label:
            self.temp_label.configure(text="N/A")
        if hasattr(self, "desc_label") and self.desc_label:
            self.desc_label.configure(text=error_msg)
        
        # Clear metrics
        for label in self.metric_value_labels.values():
            if label:
                label.configure(text="N/A")
        
        # Set default animation
        self.current_weather_condition = "clear"
        self.update_background("clear")

    def _update_weather_icon(self, icon_code):
        """Update weather icon display"""
        if not icon_code or not hasattr(self, "icon_label") or not self.icon_label:
            return

        if icon_code in self.icon_cache:
            icon_image = self.icon_cache[icon_code]
        else:
            try:
                url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                pil_img = Image.open(BytesIO(response.content)).convert("RGBA")
                icon_image = ctk.CTkImage(light_image=pil_img, size=(64, 64))
                self.icon_cache[icon_code] = icon_image
            except Exception:
                icon_image = None

        if icon_image:
            self.icon_label.configure(image=icon_image)
            self.icon_label.image = icon_image
        else:
            self.icon_label.configure(image=None)
            self.icon_label.image = None

    def _update_weather_metrics(self, data):
        """Update weather metrics display"""
        metrics = {
            "humidity": f"{data.get('humidity')}%" if data.get("humidity") is not None else "N/A",
            "wind": f"{data.get('wind_speed')} m/s" if data.get("wind_speed") is not None else "N/A",
            "pressure": f"{data.get('pressure')} hPa" if data.get("pressure") is not None else "N/A",
            "visibility": f"{data.get('visibility')} m" if data.get("visibility") is not None else "N/A",
            "uv": str(data.get("uv_index")) if data.get("uv_index") is not None else "N/A",
            "precipitation": f"{data.get('precipitation')} mm" if data.get("precipitation") is not None else "N/A",
        }

        print(f"📊 Updating metrics: {metrics}")
        for key, val in metrics.items():
            label = self.metric_value_labels.get(key)
            if label:
                label.configure(text=val)

    def map_weather_to_animation(self, weather_condition):
        """Map weather description to animation type"""
        condition = weather_condition.lower()
        
        if any(word in condition for word in ["rain", "drizzle", "shower", "precipitation"]):
            return "rain"
        elif any(word in condition for word in ["snow", "blizzard", "sleet"]):
            return "snow"
        elif any(word in condition for word in ["thunder", "storm", "lightning"]):
            return "storm"
        elif any(word in condition for word in ["cloud", "overcast", "grey", "gray", "broken"]):
            return "cloudy"
        elif any(word in condition for word in ["sun", "sunny", "bright", "clear"]):
            return "sunny"
        elif any(word in condition for word in ["mist", "fog", "haze"]):
            return "mist"
        else:
            return "clear"

    def update_tomorrow_prediction(self, city=None):
        """Update tomorrow's weather prediction"""
        if city is None:
            city = self.city_var.get().strip()
        if not isinstance(city, str) or city == "":
            if hasattr(self, "tomorrow_guess_frame") and self.tomorrow_guess_frame:
                update_tomorrow_guess_display(self.tomorrow_guess_frame, "N/A", "N/A", "N/A")
            return
        
        try:
            predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)
            if predicted_temp is None:
                predicted_display = "N/A"
            else:
                predicted_display = f"{predicted_temp} °C" if self.unit == "C" else f"{round((predicted_temp * 9 / 5) + 32, 1)} °F"
            
            if hasattr(self, "tomorrow_guess_frame") and self.tomorrow_guess_frame:
                update_tomorrow_guess_display(
                    self.tomorrow_guess_frame,
                    predicted_temp=predicted_display,
                    confidence=confidence,
                    accuracy=accuracy
                )
                print(f"🔮 Prediction updated: {predicted_display}")
        except Exception as e:
            print(f"🔮 Prediction error: {e}")

    def update_weather_history(self):
        """Update weather history display"""
        if hasattr(self, "history_frame") and self.history_frame.winfo_exists():
            for widget in self.history_frame.winfo_children():
                widget.destroy()

        if isinstance(self.history_data, dict) and all(
            key in self.history_data for key in ["time", "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean"]
        ):
            insert_temperature_history_as_grid(self.history_frame, self.city_var.get(), unit=self.unit)
            print("📈 History updated")
        else:
            if hasattr(self, "history_frame") and self.history_frame:
                label = ctk.CTkLabel(
                    self.history_frame,
                    text="Weather history not available.",
                    font=("Arial", 16),
                    text_color=self.get_text_color(),
                    fg_color="transparent"
                )
                label.pack(pady=10)

    def on_close(self):
        """Handle application close"""
        print("👋 Closing Weather App...")
        try:
            if self.smart_background and ANIMATION_AVAILABLE:
                self.smart_background.stop_animation()
        except Exception:
            pass
        self.destroy()


def run_app():
    try:
        print("🚀 Starting Weather App...")
        app = WeatherApp()
        print("✅ Weather App initialized successfully")
        app.mainloop()
    except Exception as e:
        print(f"💥 Error starting application: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    run_app()