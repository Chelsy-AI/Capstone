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

        # Icon image cache to avoid repeated downloads
        self.icon_cache = {}

        # Initialize widget placeholders as None (created in build_gui)
        self.history_frame = None
        self.temp_label = None
        self.desc_label = None
        self.update_label = None
        self.icon_label = None
        self.tomorrow_guess_frame = None
        self.city_entry = None  # Will be assigned in build_gui

        build_gui(self)  # Create all widgets and assign them

        # Start weather update in background thread safely after GUI initialized
        self.after_idle(lambda: threading.Thread(target=self.update_weather, daemon=True).start())

    def toggle_theme(self):
        if self.theme == LIGHT_THEME:
            self.theme = DARK_THEME
            ctk.set_appearance_mode("dark")
        else:
            self.theme = LIGHT_THEME
            ctk.set_appearance_mode("light")

        # Rebuild entire GUI to apply new theme colors
        build_gui(self)

        # Update the weather data display to refresh texts/images after rebuild
        self.update_weather()

    def toggle_temp_unit(self, event=None):
        self.unit = "F" if self.unit == "C" else "C"
        self.update_temperature_label()
        self.update_tomorrow_prediction()
        self.update_weather_history()

    def update_temperature_label(self):
        if self.temp_label is None:
            return  # Widget not ready yet

        if self.temp_c is None:
            self.temp_label.configure(text="N/A")
        elif self.unit == "C":
            self.temp_label.configure(text=f"{self.temp_c} °C")
        else:
            self.temp_label.configure(text=f"{self.temp_f} °F")

    def update_weather(self):
        city = self.city_var.get().strip() or "New York"

        # Fetch historical data for history display
        self.history_data = fetch_world_history(city)

        # Fetch current weather
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
            return

        temp_c = data.get("temperature")
        if temp_c is not None:
            self.temp_c = round(temp_c, 1)
            self.temp_f = round((temp_c * 9 / 5) + 32, 1)
        else:
            self.temp_c = self.temp_f = None

        self.update_temperature_label()

        if self.desc_label:
            self.desc_label.configure(text=data.get("description", "No description"))

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

        # Update metric labels
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

        # Update tomorrow's prediction and weather history on main thread using after
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
            predicted_display = (
                f"{predicted_temp} °C" if self.unit == "C"
                else f"{round((predicted_temp * 9 / 5) + 32, 1)} °F"
            )

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


def run_app():
    app = WeatherApp()
    app.mainloop()
