import customtkinter as ctk
from PIL import Image
from io import BytesIO
import requests
from datetime import datetime

from .theme import LIGHT_THEME, DARK_THEME
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

        # State vars
        self.city_var = ctk.StringVar(value="New York")
        self.unit = "C"  # Current temperature unit, toggled by clicking label

        # Store temps in both units after fetch
        self.temp_c = None
        self.temp_f = None

        # Main parent frame for theme changes
        self.parent_frame = ctk.CTkFrame(self, fg_color=self.theme["bg"])
        self.parent_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Hold references to metric value labels
        self.metric_value_labels = {}

        # Build GUI widgets
        build_gui(self)

        # Initial data load
        self.update_weather()
        self.show_weather_history()

    def toggle_theme(self):
        self.theme = DARK_THEME if self.theme == LIGHT_THEME else LIGHT_THEME
        ctk.set_appearance_mode("dark" if self.theme == DARK_THEME else "light")
        self.configure(fg_color=self.theme["bg"])
        self.parent_frame.configure(fg_color=self.theme["bg"])

        # Rebuild GUI for theme update
        build_gui(self)

        # Refresh displayed data
        self.update_weather()
        self.show_weather_history()

    def toggle_temp_unit(self, event=None):
        # Toggle temperature unit C <-> F on label click
        self.unit = "F" if self.unit == "C" else "C"
        self.update_temperature_label()

    def update_temperature_label(self):
        if self.temp_c is None:
            self.temp_label.configure(text="N/A")
            return

        if self.unit == "C":
            self.temp_label.configure(text=f"{self.temp_c} °C")
        else:
            self.temp_label.configure(text=f"{self.temp_f} °F")

    def update_weather(self):
        city = self.city_var.get().strip() or "New York"
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
            return

        temp_c = data.get("temperature")
        if temp_c is not None:
            self.temp_c = round(temp_c, 1)
            self.temp_f = round((temp_c * 9 / 5) + 32, 1)
        else:
            self.temp_c = None
            self.temp_f = None

        self.update_temperature_label()

        description = data.get("description", "No description")
        self.desc_label.configure(text=description)

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.update_label.configure(text=f"Updated at {now_str}")

        icon_code = data.get("icon")
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

    def show_weather_history(self):
        from features.history_tracker.display import insert_temperature_history_as_grid

        # Destroy old history frame if exists
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
