import customtkinter as ctk
from PIL import Image
from io import BytesIO
import requests
from datetime import datetime

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

        self.parent_frame = None
        self.history_frame = None
        self.history_data = None
        self.temp_label = None
        self.desc_label = None
        self.update_label = None
        self.icon_label = None
        self.tomorrow_guess_frame = None

        build_gui(self)
        self.update_weather()

    def toggle_theme(self):
        self.theme = DARK_THEME if self.theme == LIGHT_THEME else LIGHT_THEME
        ctk.set_appearance_mode("dark" if self.theme == DARK_THEME else "light")
        self.configure(fg_color=self.theme["bg"])
        if self.parent_frame:
            self.parent_frame.configure(fg_color=self.theme["bg"])

        build_gui(self)
        self.update_weather()

    def toggle_temp_unit(self, event=None):
        self.unit = "F" if self.unit == "C" else "C"
        self.update_temperature_label()
        self.update_tomorrow_prediction()
        self.update_weather_history()

    def update_temperature_label(self):
        if self.temp_c is None:
            self.temp_label.configure(text="N/A")
        elif self.unit == "C":
            self.temp_label.configure(text=f"{self.temp_c} °C")
        else:
            self.temp_label.configure(text=f"{self.temp_f} °F")

    def update_weather(self):
        city = self.city_var.get().strip() or "New York"

        # Fetch historical data and store it (for display only)
        self.history_data = fetch_world_history(city)

        # Fetch current weather
        data = get_current_weather(city)
        if data.get("error"):
            self.temp_c = None
            self.temp_f = None
            self.temp_label.configure(text="N/A")
            self.desc_label.configure(text=data["error"])
            for label in self.metric_value_labels.values():
                label.configure(text="N/A")
            self.icon_label.configure(image=None)
            self.icon_label.image = None
            self.update_label.configure(text="")
            update_tomorrow_guess_display(self.tomorrow_guess_frame, "N/A", "N/A", "N/A")
            return

        temp_c = data.get("temperature")
        if temp_c is not None:
            self.temp_c = round(temp_c, 1)
            self.temp_f = round((temp_c * 9 / 5) + 32, 1)
        else:
            self.temp_c = self.temp_f = None

        self.update_temperature_label()
        self.desc_label.configure(text=data.get("description", "No description"))
        self.update_label.configure(text=f"Updated at {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        icon_code = data.get("icon")
        if icon_code:
            try:
                url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                response = requests.get(url)
                response.raise_for_status()
                pil_img = Image.open(BytesIO(response.content)).convert("RGBA")
                icon_image = ctk.CTkImage(light_image=pil_img, size=(64, 64))
                self.icon_label.configure(image=icon_image)
                self.icon_label.image = icon_image
            except Exception:
                self.icon_label.configure(image=None)
                self.icon_label.image = None
        else:
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

        # HERE: pass city string to prediction function, NOT history_data
        self.update_tomorrow_prediction(city)
        self.update_weather_history()

    def update_tomorrow_prediction(self, city=None):
        if city is None:
            city = self.city_var.get().strip()

        # Defensive: check city is string
        if not isinstance(city, str) or city == "":
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

        update_tomorrow_guess_display(
            self.tomorrow_guess_frame,
            predicted_temp=predicted_display,
            confidence=confidence,
            accuracy=accuracy
        )

    def update_weather_history(self):
        # Destroy old frame if it exists
        if getattr(self, "history_frame", None):
            try:
                if self.history_frame.winfo_exists():
                    self.history_frame.destroy()
            except Exception:
                pass

        # Create a new frame at the bottom of the app
        self.history_frame = ctk.CTkFrame(self, fg_color=self.theme["bg"])
        self.history_frame.pack(fill="x", pady=(10, 10), side="bottom")

        # Validate and display history data
        if isinstance(self.history_data, dict) and all(
            key in self.history_data for key in ["time", "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean"]
        ):
            insert_temperature_history_as_grid(self.history_frame, self.city_var.get())
        else:
            # Fallback in case data is missing or incorrect
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
