import customtkinter as ctk
from customtkinter import CTkImage
from features.history_tracker.display import show_weather_history
from .api import get_basic_weather_from_weatherdb, get_detailed_environmental_data
from .error_handler import handle_errors
from .theme import LIGHT_THEME, DARK_THEME
from .gui import build_gui
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO
from core.processor import extract_weather_details


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
        self.update_weather()

    def toggle_theme(self):
        self.theme = DARK_THEME if self.theme == LIGHT_THEME else LIGHT_THEME
        build_gui(self)

    def update_weather(self):
        """
        Fetches current basic weather data and updates UI labels accordingly.
        """
        city = self.city_var.get().strip()
        data, error = get_basic_weather_from_weatherdb(city)

        if error:
            handle_errors(error)
            return

        # --- Temperature & Description ---
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
            temp_f = (temp_c * 9 / 5) + 32
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

        # --- Weather Icon ---
        icon_code = weather_list[0].get("icon") if weather_list else None
        self.set_weather_icon(icon_code)

        # --- Extra Weather Info ---
        humidity = data.get("main", {}).get("humidity")
        wind_speed = data.get("wind", {}).get("speed")
        pressure = data.get("main", {}).get("pressure")
        visibility = data.get("visibility")

        uv_index = None
        precipitation = None

        self.humidity_label.configure(text=f"Humidity: {humidity}%" if humidity is not None else "Humidity: N/A")
        self.wind_label.configure(text=f"Wind: {wind_speed} m/s" if wind_speed is not None else "Wind: N/A")
        self.pressure_label.configure(text=f"Pressure: {pressure} hPa" if pressure is not None else "Pressure: N/A")
        self.visibility_label.configure(text=f"Visibility: {visibility} m" if visibility is not None else "Visibility: N/A")
        self.uv_label.configure(text=f"UV Index: {uv_index}" if uv_index is not None else "UV Index: N/A")
        self.precipitation_label.configure(text=f"Precipitation: {precipitation}" if precipitation is not None else "Precipitation: N/A")

        # After basic weather from weatherdb (temp, desc, etc.)
        env_data = get_detailed_environmental_data(city)
        env = extract_weather_details(env_data) if env_data else {}

        # Update labels using env dict
        self.humidity_label.configure(text=f"💧 Humidity: {env.get('humidity', 'N/A')}%")
        self.wind_label.configure(text=f"💨 Wind: {env.get('wind', 'N/A')} km/h")
        self.pressure_label.configure(text=f"🧭 Pressure: {env.get('pressure', 'N/A')} hPa")
        self.visibility_label.configure(text=f"👁️ Visibility: {env.get('visibility', 'N/A')} m")
        self.uv_label.configure(text=f"🌞 UV Index: {env.get('uv', 'N/A')}")
        self.precipitation_label.configure(text=f"🌧️ Precipitation: {env.get('precipitation', 'N/A')} mm")

    def set_weather_icon(self, icon_code):
        """
        Downloads and sets the weather icon from OpenWeatherMap.
        Does NOT rotate the image.
        """
        if icon_code:
            try:
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                response = requests.get(icon_url)
                response.raise_for_status()
                img_data = response.content
                pil_img = Image.open(BytesIO(img_data)).convert("RGBA")
            except Exception:
                pil_img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        else:
            pil_img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))

        icon_image = CTkImage(light_image=pil_img, size=(64, 64))
        self.icon_label.configure(image=icon_image)
        self.icon_label.image = icon_image  # Prevent garbage collection

    def show_weather_history(self):
        """
        Loads and displays historical weather data for the entered city.
        """
        city = self.city_var.get().strip()
        if city:
            show_weather_history(self.history_text, city)

    def run(self):
        self.root.mainloop()


# Entrypoint for app
def run_app():
    app = WeatherApp()
    app.run()
