import customtkinter as ctk
from history_tracker.display import show_weather_history
from .api import fetch_weather
from .processor import display_weather
from .storage import save_weather
from .error_handler import handle_errors
from .theme import LIGHT_THEME, DARK_THEME
from .gui import build_gui
from datetime import datetime
import requests
from PIL import Image, ImageTk
from io import BytesIO


class WeatherApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.theme = LIGHT_THEME
        self.city_var = ctk.StringVar(value="New York")
        self.unit = "C"

        self.root.title("Weather Dashboard")
        self.root.geometry("600x500")
        self.root.configure(fg_color=self.theme["bg"])

        build_gui(self)
        self.fetch_and_display()

    def toggle_theme(self):
        self.theme = DARK_THEME if self.theme == LIGHT_THEME else LIGHT_THEME
        build_gui(self)

    def fetch_and_display(self):
        city = self.city_var.get()
        data, error = fetch_weather(city)
        if error:
            handle_errors(error)
            return

        temp_c = data.get("main", {}).get("temp")
        weather_list = data.get("weather", [])
        desc = weather_list[0].get("description") if weather_list else "No description"
        update_time = data.get("dt")

        self.current_temp_c = temp_c
        self.current_desc = desc
        self.current_update_time = update_time

        if temp_c is None:
            display_temp = "N/A"
        elif self.unit == "C":
            display_temp = f"{temp_c:.1f} °C"
        else:
            temp_f = (temp_c * 9/5) + 32
            display_temp = f"{temp_f:.1f} °F"

        self.temp_label.configure(text=display_temp)
        self.desc_label.configure(text=desc.capitalize() if desc else "No description")

        if update_time:
            try:
                last_update = datetime.utcfromtimestamp(update_time).strftime("%Y-%m-%d %H:%M UTC")
            except Exception:
                last_update = "Unknown"
        else:
            last_update = "Unknown"

        self.update_label.configure(text=f"Updated at {last_update}")

        # --- Icon loading and animation ---

        icon_code = weather_list[0].get("icon") if weather_list else None

        if icon_code:
            try:
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                response = requests.get(icon_url)
                response.raise_for_status()
                img_data = response.content
                pil_img = Image.open(BytesIO(img_data)).convert("RGBA")
                self.weather_icon_img_original = pil_img
            except Exception:
                self.weather_icon_img_original = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        else:
            self.weather_icon_img_original = Image.new("RGBA", (64, 64), (0, 0, 0, 0))

        # Start rotation animation
        if hasattr(self, "animation_angle"):
            self.animation_angle = (self.animation_angle + 5) % 360
        else:
            self.animation_angle = 0

        rotated = self.weather_icon_img_original.rotate(self.animation_angle, resample=Image.BICUBIC, expand=True)
        icon_image = ImageTk.PhotoImage(rotated)

        self.icon_label.configure(image=icon_image, text="")  # no text on icon label
        self.icon_label.image = icon_image  # prevent garbage collection

        # schedule next rotation frame after 50 ms
        self.root.after(50, self.fetch_and_display)
        
        # Extract additional weather information
        humidity = data.get("main", {}).get("humidity")
        wind_speed = data.get("wind", {}).get("speed")
        pressure = data.get("main", {}).get("pressure")
        visibility = data.get("visibility")
        uv_index = data.get("uv_index")  # Assuming UV index is part of the data
        pollen_count = data.get("pollen_count")  # Assuming pollen count is part of the data
        bug_index = data.get("bug_index")  # Assuming bug index is part of the data
        precipitation = data.get("precipitation")  # Or the correct key depending on your API

        # Update labels with new data
        if humidity is not None:
            self.humidity_label.configure(text=f"Humidity: {humidity}%")
        if wind_speed is not None:
            self.wind_label.configure(text=f"Wind: {wind_speed} m/s")
        if pressure is not None:
            self.pressure_label.configure(text=f"Pressure: {pressure} hPa")
        if visibility is not None:
           self.visibility_label.configure(text=f"Visibility: {visibility} m")
        if uv_index is not None:
            self.uv_label.configure(text=f"UV Index: {uv_index}")
        if pollen_count is not None:
            self.pollen_label.configure(text=f"Pollen: {pollen_count}")
        if bug_index is not None:
            self.bug_label.configure(text=f"Bugs: {bug_index}")
        if precipitation is not None:
            self.precipitation.configure(text=f"Precipitation: {precipitation}")


    def show_weather_history(self):
        city = self.city_var.get().strip()
        if city:
            show_weather_history(self.history_text, city)

    def run(self):
        self.root.mainloop()

def run_app():
    app = WeatherApp()
    app.run()
