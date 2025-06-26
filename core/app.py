import customtkinter as ctk
from features.history_tracker.display import show_weather_history
from .api import get_basic_weather_from_weatherdb
from .error_handler import handle_errors
from .theme import LIGHT_THEME, DARK_THEME
from .gui import build_gui
from datetime import datetime
import requests
from PIL import Image, ImageTk
from io import BytesIO
from .api import get_detailed_environmental_data



class WeatherApp:
    # Initializes the WeatherApp with GUI, default city, and theme.
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

    # Toggles between light and dark theme and rebuilds the UI.
    def toggle_theme(self):
        self.theme = DARK_THEME if self.theme == LIGHT_THEME else LIGHT_THEME
        build_gui(self)

    # Fetches and displays the current weather data for the selected city.
    def update_weather(self):
        city = self.city_var.get()
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

        uv_index = data.get("uv_index")  # May not be present
        pollen_count = data.get("pollen_count")
        bug_index = data.get("bug_index")
        precipitation = data.get("precipitation")

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

    # Downloads and sets the weather icon from OpenWeatherMap or uses a blank fallback.
    def set_weather_icon(self, icon_code):
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

        icon_image = ImageTk.PhotoImage(pil_img)
        self.icon_label.configure(image=icon_image, text="")
        self.icon_label.image = icon_image  # Prevent garbage collection

    # Loads and displays historical weather data for the entered city.
    def show_weather_history(self):
        city = self.city_var.get().strip()
        if city:
            show_weather_history(self.history_text, city)

    # Runs the Tkinter main loop.
    def run(self):
        self.root.mainloop()

    def update_weather_display(self):
        """
        Fetches the latest detailed weather and environmental data for the current city,
        and updates the app's GUI elements (temperature, humidity, wind, UV index, etc.)
        accordingly. Handles the case when no data is found by notifying via console output.
        """
        city = self.city_var.get()
        data = get_detailed_environmental_data(city)
        if not data:
            print("No weather data found")
            return


# Starts the WeatherApp when called from the entrypoint.
def run_app():
    app = WeatherApp()
    app.run()
