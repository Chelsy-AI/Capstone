import requests
import os
from dotenv import load_dotenv

# Load environment variables (WeatherDB API key and base URL)
load_dotenv()

API_KEY = os.getenv("weatherdb_api_key")
BASE_URL = os.getenv("weatherdb_base_url")

# Get the latitude and longitude for a given city using Open-Meteo's geocoding API
def resolve_coordinates_by_city(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    response = requests.get(url)
    data = response.json()
    if data.get("results"):
        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]
        return lat, lon
    return None, None

# Get basic weather data (temperature, humidity, etc.) from WeatherDB
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

# Get detailed environmental weather data (UV, pressure, pollen, etc.) from Open-Meteo
def get_detailed_environmental_data(city_name):
    lat, lon = resolve_coordinates_by_city(city_name)
    if not lat or not lon:
        return None

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure,visibility"
        f"&daily=uv_index_max,precipitation_sum,pollen_index"
        f"&timezone=auto"
    )

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
