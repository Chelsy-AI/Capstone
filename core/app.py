import customtkinter as ctk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from datetime import datetime
import threading
import tkinter as tk
import traceback

from features.history_tracker.api import fetch_world_history
from features.history_tracker.display import insert_temperature_history_as_grid
from features.tomorrows_guess.display import update_tomorrow_guess_display
from features.tomorrows_guess.predictor import get_tomorrows_prediction

from core.theme import LIGHT_THEME, DARK_THEME
from gui.gui_builder import build_gui
from core.api import get_current_weather

from gui.animation_gui import SmartBackground


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
        self.current_weather_condition = None

        # Validate and fill missing theme keys with defaults
        def validate_theme(theme):
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
                val = theme.get(key)
                if not val or not isinstance(val, str) or val.strip() == "":
                    theme[key] = default_color

        validate_theme(self.theme)
        self.configure(fg_color=self.theme["bg"])

        # Create animation canvas that fills the entire window
        self.bg_canvas = tk.Canvas(self, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_canvas.lower("all")  # Send canvas behind all other widgets

        # Build the foreground GUI widgets on top of the canvas
        build_gui(self)

        # Initialize SmartBackground animation manager AFTER canvas is created
        self.smart_background = SmartBackground(self, self.bg_canvas)
        self.smart_background.start_animation("clear")

        # Start weather update in background thread safely
        self.after_idle(lambda: threading.Thread(target=self.safe_update_weather, daemon=True).start())

        # Handle window close to stop animation cleanly
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Bind window resize event to update canvas size
        self.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, event):
        """Handle window resize to update canvas and animation"""
        if event.widget == self:
            # Update canvas size
            self.bg_canvas.place_configure(width=event.width, height=event.height)
            # Update animation dimensions
            if hasattr(self, 'smart_background') and self.smart_background:
                self.smart_background.width = event.width
                self.smart_background.height = event.height
                self.smart_background._init_particles()

    def update_background(self, weather_condition):
        """Update the animated background based on weather condition"""
        if hasattr(self, 'smart_background') and self.smart_background:
            try:
                print(f"[DEBUG] Updating background to: {weather_condition}")
                self.smart_background.update_background(weather_condition)
            except Exception as e:
                print(f"[ERROR] Exception in update_background: {e}")
                traceback.print_exc()

    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.theme = DARK_THEME if self.theme == LIGHT_THEME else LIGHT_THEME
        ctk.set_appearance_mode("dark" if self.theme == DARK_THEME else "light")
        self.configure(fg_color=self.theme["bg"])

        # Rebuild GUI (widgets only, not canvas)
        build_gui(self)

        # Restart animation with current weather condition
        if hasattr(self, 'smart_background') and self.smart_background:
            self.smart_background.stop_animation()
            self.smart_background = SmartBackground(self, self.bg_canvas)
            current_condition = self.current_weather_condition or "clear"
            self.smart_background.start_animation(current_condition)

    def toggle_temp_unit(self, event=None):
        """Toggle between Celsius and Fahrenheit"""
        self.unit = "F" if self.unit == "C" else "C"
        self.update_temperature_label()
        self.update_tomorrow_prediction()
        self.update_weather_history()

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
            print(f"Error updating weather: {e}")
            traceback.print_exc()

    def update_weather(self):
        """Update weather data and UI"""
        city = self.city_var.get().strip() or "New York"
        self.history_data = fetch_world_history(city)
        data = get_current_weather(city)

        if data.get("error"):
            self.temp_c = None
            self.temp_f = None
            if hasattr(self, "temp_label") and self.temp_label:
                self.temp_label.configure(text="N/A")
            if hasattr(self, "desc_label") and self.desc_label:
                self.desc_label.configure(text=data["error"])
            for label in self.metric_value_labels.values():
                label.configure(text="N/A")
            if hasattr(self, "icon_label") and self.icon_label:
                self.icon_label.configure(image=None)
                self.icon_label.image = None
            if hasattr(self, "update_label") and self.update_label:
                self.update_label.configure(text="")
            if hasattr(self, "tomorrow_guess_frame") and self.tomorrow_guess_frame:
                update_tomorrow_guess_display(self.tomorrow_guess_frame, "N/A", "N/A", "N/A")
            self.current_weather_condition = "clear"
            self.after(0, lambda: self.update_background("clear"))
            return

        # Update temperature
        temp_c = data.get("temperature")
        if temp_c is not None:
            self.temp_c = round(temp_c, 1)
            self.temp_f = round((temp_c * 9 / 5) + 32, 1)
        else:
            self.temp_c = self.temp_f = None

        self.update_temperature_label()
        
        # Update description
        description = data.get("description", "No description")
        if hasattr(self, "desc_label") and self.desc_label:
            self.desc_label.configure(text=description)
        if hasattr(self, "update_label") and self.update_label:
            self.update_label.configure(text=f"Updated at {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        # Update weather icon
        icon_code = data.get("icon")
        if icon_code and hasattr(self, "icon_label") and self.icon_label:
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
        elif hasattr(self, "icon_label") and self.icon_label:
            self.icon_label.configure(image=None)
            self.icon_label.image = None

        # Update metrics
        metrics = {
            "humidity": f"{data.get('humidity')}%" if data.get("humidity") is not None else "N/A",
            "wind": f"{data.get('wind_speed')} m/s" if data.get("wind_speed") is not None else "N/A",
            "pressure": f"{data.get('pressure')} hPa" if data.get("pressure") is not None else "N/A",
            "visibility": f"{data.get('visibility')} m" if data.get("visibility") is not None else "N/A",
            "uv": str(data.get("uv_index")) if data.get("uv_index") is not None else "N/A",
            "precipitation": f"{data.get('precipitation')} mm" if data.get("precipitation") is not None else "N/A",
        }

        for key, val in metrics.items():
            label = self.metric_value_labels.get(key)
            if label:
                label.configure(text=val)

        # Update background animation based on weather condition
        weather_condition = description.lower() if description else "clear"
        self.current_weather_condition = weather_condition
        
        # Map weather descriptions to animation types
        animation_type = self.map_weather_to_animation(weather_condition)
        
        self.after(0, lambda: self.update_background(animation_type))
        self.after(0, lambda: self.update_tomorrow_prediction(city))
        self.after(0, self.update_weather_history)

    def map_weather_to_animation(self, weather_condition):
        """Map weather description to animation type"""
        condition = weather_condition.lower()
        
        if any(word in condition for word in ["rain", "drizzle", "shower", "precipitation"]):
            return "rain"
        elif any(word in condition for word in ["snow", "blizzard", "sleet"]):
            return "snow"
        elif any(word in condition for word in ["thunder", "storm", "lightning"]):
            return "storm"
        elif any(word in condition for word in ["cloud", "overcast", "grey", "gray"]):
            return "cloudy"
        elif any(word in condition for word in ["sun", "sunny", "bright"]):
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

    def update_weather_history(self):
        """Update weather history display"""
        if hasattr(self, "history_frame") and self.history_frame.winfo_exists():
            for widget in self.history_frame.winfo_children():
                widget.destroy()

        if isinstance(self.history_data, dict) and all(
            key in self.history_data for key in ["time", "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean"]
        ):
            insert_temperature_history_as_grid(self.history_frame, self.city_var.get(), unit=self.unit)
        else:
            if hasattr(self, "history_frame") and self.history_frame:
                label = ctk.CTkLabel(
                    self.history_frame,
                    text="Weather history not available.",
                    font=("Arial", 16),
                    text_color=self.theme["fg"],
                )
                label.pack(pady=10)

    def on_close(self):
        """Handle application close"""
        try:
            if hasattr(self, 'smart_background') and self.smart_background:
                self.smart_background.stop_animation()
        except Exception:
            print("[ERROR] Exception stopping animation:")
            traceback.print_exc()
        self.destroy()


def run_app():
    app = WeatherApp()
    app.mainloop()


if __name__ == "__main__":
    run_app()