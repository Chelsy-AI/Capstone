import customtkinter as ctk
from PIL import Image, ImageTk, ImageEnhance
from io import BytesIO
import requests
from datetime import datetime
import threading
import os
import tkinter as tk

from features.history_tracker.api import fetch_world_history
from features.history_tracker.display import insert_temperature_history_as_grid
from features.tomorrows_guess.display import update_tomorrow_guess_display
from features.tomorrows_guess.predictor import get_tomorrows_prediction

from core.theme import LIGHT_THEME, DARK_THEME
from gui.gui_builder import build_gui
from core.api import get_current_weather

from features.smart_background.manager import DynamicBackgroundManager


class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.theme = LIGHT_THEME
        ctk.set_appearance_mode("light")
        self.title("Weather App")
        self.geometry("800x600")
        self.configure(fg_color=self.theme["bg"])

        self.city_var = ctk.StringVar(value="New York")
        self.unit = "C"

        self.temp_c = None
        self.temp_f = None
        self.metric_value_labels = {}
        self.icon_cache = {}
        self.current_weather_condition = None
        self.background_label = None

        self.bg_canvas = tk.Canvas(self, width=800, height=600, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.after(100, lambda: self.bg_canvas.tag_lower("background_gradient"))

        self.smart_bg_manager = DynamicBackgroundManager(self.bg_canvas, width=800, height=600)
        self.smart_bg_manager.set_weather("clear")
        self.smart_bg_manager.start_animation()

        self.history_frame = None
        self.temp_label = None
        self.desc_label = None
        self.update_label = None
        self.icon_label = None
        self.tomorrow_guess_frame = None
        self.city_entry = None

        build_gui(self)
        self.setup_background()
        if self.background_label:
            self.background_label.lower()

        self.after_idle(lambda: threading.Thread(target=self.safe_update_weather, daemon=True).start())
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_background(self):
        self.background_label = ctk.CTkLabel(self, text="", fg_color="transparent")
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def get_weather_condition_category(self, description, icon_code):
        if not description and not icon_code:
            return "default"
        description = description.lower() if description else ""
        icon_code = icon_code.lower() if icon_code else ""

        if any(word in description for word in ["rain", "drizzle", "shower"]) or "rain" in icon_code:
            return "rainy"
        elif any(word in description for word in ["thunder", "storm"]) or "storm" in icon_code:
            return "stormy"
        elif any(word in description for word in ["snow", "blizzard"]) or "snow" in icon_code:
            return "snowy"
        elif any(word in description for word in ["cloud", "overcast"]) or "cloud" in icon_code:
            return "cloudy"
        elif any(word in description for word in ["clear", "sunny"]) or "clear" in icon_code or "sun" in icon_code:
            return "sunny"
        elif any(word in description for word in ["fog", "mist", "haze"]) or "fog" in icon_code:
            return "foggy"
        elif any(word in description for word in ["wind"]) or "wind" in icon_code:
            return "windy"
        else:
            return "default"

    def update_background(self, weather_condition):
        self.smart_bg_manager.set_weather(weather_condition)

    def toggle_theme(self):
        if self.smart_bg_manager:
            self.smart_bg_manager.stop_animation()

        self.theme = DARK_THEME if self.theme == LIGHT_THEME else LIGHT_THEME
        ctk.set_appearance_mode("dark" if self.theme == DARK_THEME else "light")
        self.configure(fg_color=self.theme["bg"])

        build_gui(self)
        self.smart_bg_manager = DynamicBackgroundManager(self.bg_canvas, width=800, height=600)
        self.smart_bg_manager.set_weather("clear")
        self.smart_bg_manager.start_animation()

        self.setup_background()
        self.current_weather_condition = None
        self.update_weather()

    def toggle_temp_unit(self, event=None):
        self.unit = "F" if self.unit == "C" else "C"
        self.update_temperature_label()
        self.update_tomorrow_prediction()
        self.update_weather_history()

    def update_temperature_label(self):
        if self.temp_label is None:
            return
        if self.temp_c is None:
            self.temp_label.configure(text="N/A")
        elif self.unit == "C":
            self.temp_label.configure(text=f"{self.temp_c} °C")
        else:
            self.temp_label.configure(text=f"{self.temp_f} °F")

    def safe_update_weather(self):
        try:
            self.update_weather()
        except Exception as e:
            print(f"Error updating weather: {e}")

    def update_weather(self):
        city = self.city_var.get().strip() or "New York"
        self.history_data = fetch_world_history(city)
        data = get_current_weather(city)

        if data.get("error"):
            self.temp_c = None
            self.temp_f = None
            if self.temp_label:
                self.temp_label.configure(text="N/A")
            if self.desc_label:
                self.desc_label.configure(text=data["error"])
            for label in self.metric_value_labels.values():
                label.configure(text="N/A")
            if self.icon_label:
                self.icon_label.configure(image=None)
                self.icon_label.image = None
            if self.update_label:
                self.update_label.configure(text="")
            if self.tomorrow_guess_frame:
                update_tomorrow_guess_display(self.tomorrow_guess_frame, "N/A", "N/A", "N/A")
            self.after(0, lambda: self.update_background("default"))
            return

        temp_c = data.get("temperature")
        if temp_c is not None:
            self.temp_c = round(temp_c, 1)
            self.temp_f = round((temp_c * 9 / 5) + 32, 1)
        else:
            self.temp_c = self.temp_f = None

        self.update_temperature_label()
        description = data.get("description", "No description")
        if self.desc_label:
            self.desc_label.configure(text=description)
        if self.update_label:
            self.update_label.configure(text=f"Updated at {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        icon_code = data.get("icon")
        if icon_code and self.icon_label:
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
        elif self.icon_label:
            self.icon_label.configure(image=None)
            self.icon_label.image = None

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

        weather_condition = self.get_weather_condition_category(description, icon_code)
        self.after(0, lambda: self.update_background(weather_condition))
        self.after(0, lambda: self.update_tomorrow_prediction(city))
        self.after(0, self.update_weather_history)

    def update_tomorrow_prediction(self, city=None):
        if city is None:
            city = self.city_var.get().strip()
        if not isinstance(city, str) or city == "":
            if self.tomorrow_guess_frame:
                update_tomorrow_guess_display(self.tomorrow_guess_frame, "N/A", "N/A", "N/A")
            return
        predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)
        if predicted_temp is None:
            predicted_display = "N/A"
        else:
            predicted_display = f"{predicted_temp} °C" if self.unit == "C" else f"{round((predicted_temp * 9 / 5) + 32, 1)} °F"
        if self.tomorrow_guess_frame:
            update_tomorrow_guess_display(
                self.tomorrow_guess_frame,
                predicted_temp=predicted_display,
                confidence=confidence,
                accuracy=accuracy
            )

    def update_weather_history(self):
        if getattr(self, "history_frame", None) and self.history_frame.winfo_exists():
            for widget in self.history_frame.winfo_children():
                widget.destroy()

        if isinstance(self.history_data, dict) and all(
            key in self.history_data for key in ["time", "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean"]
        ):
            insert_temperature_history_as_grid(self.history_frame, self.city_var.get(), unit=self.unit)
        else:
            label = ctk.CTkLabel(
                self.history_frame,
                text="Weather history not available.",
                font=("Arial", 16),
                text_color=self.theme["fg"],
            )
            label.pack(pady=10)

    def on_close(self):
        if self.smart_bg_manager:
            self.smart_bg_manager.stop_animation()
        self.destroy()


def run_app():
    app = WeatherApp()
    app.mainloop()


if __name__ == "__main__":
    run_app()
