import requests
import os
from dotenv import load_dotenv
from .geocode import get_lat_lon

# Load environment variables
load_dotenv()

API_KEY = os.getenv("weatherdb_api_key")
BASE_URL = os.getenv("weatherdb_base_url")

def resolve_coordinates_by_city(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    response = requests.get(url)
    data = response.json()
    if data.get("results"):
        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]
        return lat, lon
    return None, None

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
            "error": err or "Unknown error",
            "description": "No description"
        }

    main = weather_data.get("main", {})
    wind = weather_data.get("wind", {})
    weather_list = weather_data.get("weather", [{}])
    icon = weather_list[0].get("icon", "01d")
    description = weather_list[0].get("description", "No description").capitalize()

    uv_index = None
    precipitation = None

    if detailed_data:
        uv_index_list = detailed_data.get("daily", {}).get("uv_index_max")
        if uv_index_list and isinstance(uv_index_list, list) and len(uv_index_list) > 0:
            uv_index = uv_index_list[0]

        precipitation_list = detailed_data.get("daily", {}).get("precipitation_sum")
        if precipitation_list and isinstance(precipitation_list, list) and len(precipitation_list) > 0:
            precipitation = precipitation_list[0]

    return {
        "temperature": main.get("temp"),
        "humidity": main.get("humidity"),
        "wind_speed": wind.get("speed"),
        "pressure": main.get("pressure"),
        "icon": icon,
        "visibility": detailed_data.get("current", {}).get("visibility") if detailed_data else None,
        "uv_index": uv_index if uv_index is not None else "N/A",
        "precipitation": precipitation if precipitation is not None else "N/A",
        "error": None,
        "description": description
    }
