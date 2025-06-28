import requests
import os
from dotenv import load_dotenv
from .geocode import get_lat_lon

# Load environment variables
load_dotenv()

API_KEY = os.getenv("weatherdb_api_key")
BASE_URL = os.getenv("weatherdb_base_url")

# Resolve coordinates using Open-Meteo Geocoding API
def resolve_coordinates_by_city(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    response = requests.get(url)
    data = response.json()
    if data.get("results"):
        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]
        return lat, lon
    return None, None

# Basic weather from WeatherDB
def get_basic_weather_from_weatherdb(city_name):
    try:
        params = {
            "q": city_name,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"City '{city_name}' not found."
    except Exception as e:
        return None, str(e)

# Environmental data from Open-Meteo
def get_detailed_environmental_data(city):
    lat, lon = get_lat_lon(city)
    if not lat or not lon:
        return None

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure,visibility"
        "&daily=uv_index_max,precipitation_sum"
        "&timezone=auto"
    )
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    return None

# Combined weather data used by app.py
def get_current_weather(city):
    weather_data, err = get_basic_weather_from_weatherdb(city)
    detailed_data = get_detailed_environmental_data(city)

    if not weather_data:
        return {
            "temperature": None,
            "humidity": None,
            "wind_speed": None,
            "pressure": None,
            "icon": "❓",
            "error": err or "Unknown error"
        }

    main = weather_data.get("main", {})
    wind = weather_data.get("wind", {})
    icon = weather_data.get("weather", [{}])[0].get("icon", "01d")

    return {
        "temperature": main.get("temp"),
        "humidity": main.get("humidity"),
        "wind_speed": wind.get("speed"),
        "pressure": main.get("pressure"),
        "icon": icon,
        "visibility": detailed_data.get("current", {}).get("visibility") if detailed_data else None,
        "uv_index": detailed_data.get("daily", {}).get("uv_index_max", [None])[0] if detailed_data else None,
        "precipitation": detailed_data.get("daily", {}).get("precipitation_sum", [None])[0] if detailed_data else None,
        "error": None
    }
