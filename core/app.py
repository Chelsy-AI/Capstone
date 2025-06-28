import customtkinter as ctk
from PIL import Image
from io import BytesIO
import requests

from .theme import LIGHT_THEME, DARK_THEME
from .utils import toggle_unit, kelvin_to_celsius, kelvin_to_fahrenheit, format_temperature
from core.gui import build_gui
import core.api as weather_api


class WeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.theme = LIGHT_THEME
        ctk.set_appearance_mode("light")
        self.title("Weather App")
        self.geometry("800x600")
        self.configure(fg_color=self.theme["bg"])

        # State vars
        self.city_var = ctk.StringVar(value="New York")
        self.unit = "C"

        # Main parent frame for theme changes
        self.parent_frame = ctk.CTkFrame(self, fg_color=self.theme["bg"])
        self.parent_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Hold references to metric value labels to update later
        self.metric_value_labels = {}

        # Build GUI widgets
        build_gui(self)

        # Fetch weather and history initially
        self.update_weather()
        self.show_weather_history()

    def toggle_theme(self):
        self.theme = DARK_THEME if self.theme == LIGHT_THEME else LIGHT_THEME
        ctk.set_appearance_mode("dark" if self.theme == DARK_THEME else "light")
        self.configure(fg_color=self.theme["bg"])
        self.parent_frame.configure(fg_color=self.theme["bg"])

        # Rebuild GUI to apply theme
        build_gui(self)

        # Refresh displayed data
        self.update_weather()
        self.show_weather_history()

    def toggle_temp_unit(self, event=None):
        self.unit = toggle_unit(self.unit)
        self.update_weather()

    def update_weather(self):
        city = self.city_var.get().strip() or "New York"
        data, error = weather_api.get_basic_weather_from_weatherdb(city)

        if error or not data:
            # Show N/A or error message in labels
            self.temp_label.configure(text="N/A")
            self.desc_label.configure(text="Error fetching data")
            for label in self.metric_value_labels.values():
                label.configure(text="N/A")
            self.icon_label.configure(image=None)
            self.update_label.configure(text="")
            return

        # Temperature in Celsius from API (assume API returns Celsius)
        temp_c = data.get("main", {}).get("temp")
        weather_list = data.get("weather", [])
        desc = weather_list[0].get("description") if weather_list else ""
        update_time = data.get("dt")

        # Convert temperature based on unit
        if temp_c is None:
            display_temp = "N/A"
        else:
            if self.unit == "C":
                display_temp = f"{temp_c:.1f} °C"
            else:
                temp_f = (temp_c * 9 / 5) + 32
                display_temp = f"{temp_f:.1f} °F"

        self.temp_label.configure(text=display_temp)
        self.desc_label.configure(text=desc.capitalize() if desc else "No description")

        # Format last update time
        if update_time:
            try:
                from datetime import datetime
                last_update = datetime.utcfromtimestamp(update_time).strftime("%Y-%m-%d %H:%M UTC")
            except Exception:
                last_update = "Unknown"
        else:
            last_update = "Unknown"
        self.update_label.configure(text=f"Updated at {last_update}")

        # Load weather icon from OpenWeatherMap
        icon_code = weather_list[0].get("icon") if weather_list else None
        if icon_code:
            try:
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                response = requests.get(icon_url)
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

        main = data.get("main", {})
        wind = data.get("wind", {})
        visibility = data.get("visibility")

        # Update metric labels safely
        metrics = {
            "humidity": f"{main.get('humidity')}%" if main.get("humidity") is not None else "N/A",
            "wind": f"{wind.get('speed')} m/s" if wind.get("speed") is not None else "N/A",
            "pressure": f"{main.get('pressure')} hPa" if main.get("pressure") is not None else "N/A",
            "visibility": f"{visibility} m" if visibility is not None else "N/A",
            # You can add UV and Precipitation if available from another source
            "uv": "N/A",
            "precipitation": "N/A",
        }

        for key, val in metrics.items():
            label = self.metric_value_labels.get(key)
            if label:
                label.configure(text=val)

    def show_weather_history(self):
        # Import here to avoid circular imports
        from features.history_tracker.display import insert_temperature_history_as_grid

        # Remove existing history frame if exists
        if hasattr(self, "history_frame") and self.history_frame.winfo_exists():
            self.history_frame.destroy()

        self.history_frame = ctk.CTkFrame(
            self,
            fg_color=self.theme.get("bg", "#2b2b2b")
        )
        self.history_frame.pack(fill="x", pady=(10, 10), side="bottom")

        city = self.city_var.get().strip()
        if city:
            insert_temperature_history_as_grid(self.history_frame, city)

def run_app():
    app = WeatherApp()
    app.mainloop()
