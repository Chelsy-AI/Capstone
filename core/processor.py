import requests
from PIL import Image, ImageTk
import io
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# Displays current weather info including temperature, description, update time,
# and weather icon on the GUI. Converts temperature based on selected unit (°C or °F).
# Fetches and processes icon image for display.
# ──────────────────────────────────────────────────────────────────────────────
def display_weather(data, temp_label, desc_label, update_label, icon_label, app):
    """
    Update the GUI weather display widgets with the latest weather data.
    """
    try:
        temp_c = data["main"]["temp"]
        temp_f = temp_c * 9 / 5 + 32
        temp = f"{round(temp_c)} °C" if app.unit == "C" else f"{round(temp_f)} °F"
        temp_label.configure(text=temp)

        weather = data["weather"][0]
        description = weather["description"].capitalize()
        desc_label.configure(text=description)

        update_time = datetime.utcfromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M UTC")
        update_label.configure(text=f"Updated at: {update_time}")

        # Load weather icon image from OpenWeatherMap
        icon_code = weather["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        response = requests.get(icon_url)
        image = Image.open(io.BytesIO(response.content)).convert("RGBA")

        # Store original image and create PhotoImage for Tkinter
        app.original_icon = image
        app.icon_image = ImageTk.PhotoImage(image)
        icon_label.configure(image=app.icon_image)
        icon_label.image = app.icon_image

    except Exception as e:
        temp_label.configure(text="N/A")
        desc_label.configure(text="No description")
        update_label.configure(text="Updated at: Unknown")


# ──────────────────────────────────────────────────────────────────────────────
# Extract relevant weather details (humidity, wind, pressure, visibility, UV,
# precipitation) from Open-Meteo API JSON data.
# ──────────────────────────────────────────────────────────────────────────────
def extract_weather_details(data):
    """
    Extracts humidity, wind speed, pressure, visibility, UV index, and precipitation
    from detailed weather data dictionary.
    Returns a dictionary of these values.
    """
    current = data.get("current", {})
    daily = data.get("daily", {})

    return {
        "humidity": current.get("relative_humidity_2m", "N/A"),
        "wind": current.get("wind_speed_10m", "N/A"),
        "pressure": current.get("surface_pressure", "N/A"),
        "visibility": current.get("visibility", "N/A"),
        "uv": daily.get("uv_index_max", ["N/A"])[0],
        "precipitation": daily.get("precipitation_sum", ["N/A"])[0],
    }
