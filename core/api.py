"""
Weather API Integration Module
=============================

This module handles all external API calls for weather data retrieval.
It integrates with multiple weather APIs to provide comprehensive weather information:
- WeatherDB API for basic weather data
- Open-Meteo API for detailed environmental data and geocoding

Key Features:
- City name to coordinates resolution
- Current weather data fetching
- Detailed environmental data (humidity, wind, pressure, UV index, etc.)
- Error handling for API failures
- Data combination from multiple sources

"""

import requests
import os
from dotenv import load_dotenv
from .geocode import get_lat_lon

load_dotenv()

# Retrieve API credentials from environment variables
API_KEY = os.getenv("weatherdb_api_key")
BASE_URL = os.getenv("weatherdb_base_url")


def resolve_coordinates_by_city(city_name):
    """
    Convert city name to latitude and longitude coordinates
    
    This function uses the Open-Meteo geocoding API to find the geographic
    coordinates of a given city name. This is essential for APIs that require
    lat/lon coordinates instead of city names.
    
    """
    # Construct the geocoding API URL with the city name
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    
    # Make HTTP GET request to the geocoding API
    response = requests.get(url)
    
    # Parse the JSON response
    data = response.json()
    
    # Check if we got valid results
    if data.get("results"):
        # Extract latitude and longitude from the first result
        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]
        return lat, lon
    
    # Return None values if no results found
    return None, None


def get_basic_weather_from_weatherdb(city_name):
    """
    Fetch basic current weather data from WeatherDB API
    
    This function retrieves fundamental weather information like temperature,
    humidity, wind speed, and weather conditions from the WeatherDB API.
    
    """
    try:
        # Set up API request parameters
        params = {
            "q": city_name,           # City name query
            "appid": API_KEY,         # API authentication key
            "units": "metric"         # Use Celsius for temperature
        }
        
        # Make HTTP GET request to WeatherDB API
        response = requests.get(BASE_URL, params=params)
        
        # Check if request was successful (status code 200)
        if response.status_code == 200:
            return response.json(), None
        else:
            # Return error message for unsuccessful requests
            return None, f"City '{city_name}' not found."
            
    except Exception as e:
        # Handle any network or parsing errors
        return None, str(e)


def get_detailed_environmental_data(city):
    """
    Fetch detailed environmental data from Open-Meteo API
    
    This function retrieves comprehensive environmental information including
    humidity, wind speed, atmospheric pressure, visibility, UV index, and
    precipitation data using the Open-Meteo weather API.
    
    """
    # First, get the latitude and longitude for the city
    lat, lon = get_lat_lon(city)
    
    # Return None if we couldn't geocode the city
    if not lat or not lon:
        return None
    
    # Construct the Open-Meteo API URL with all required parameters
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure,visibility"
        "&daily=uv_index_max,precipitation_sum"
        "&timezone=auto"
    )
    
    # Make HTTP GET request to Open-Meteo API
    resp = requests.get(url)
    
    # Return parsed JSON if successful, None otherwise
    if resp.status_code == 200:
        return resp.json()
    return None


def get_current_weather(city):
    """
    Combine and process weather data from multiple APIs
    
    This is the main function that orchestrates data collection from multiple
    weather APIs and combines them into a single, comprehensive weather report.
    It handles errors gracefully and provides fallback values.
    
    """
    # Get basic weather data from WeatherDB API
    weather_data, err = get_basic_weather_from_weatherdb(city)
    
    # Get detailed environmental data from Open-Meteo API
    detailed_data = get_detailed_environmental_data(city)
    
    # Handle case where basic weather data is unavailable
    if not weather_data:
        return {
            "temperature": None,
            "humidity": None,
            "wind_speed": None,
            "pressure": None,
            "icon": "❓",  # Question mark emoji for unknown weather
            "error": err or "Unknown error",
            "description": "No description"
        }
    
    # Extract data from the basic weather response
    main = weather_data.get("main", {})  # Main weather data (temp, humidity, pressure)
    wind = weather_data.get("wind", {})  # Wind information
    weather_list = weather_data.get("weather", [{}])  # Weather conditions array
    
    # Get weather icon and description from the first weather condition
    icon = weather_list[0].get("icon", "01d")  # Default to clear day icon
    description = weather_list[0].get("description", "No description").capitalize()
    
    # Initialize UV index and precipitation with default values
    uv_index = None
    precipitation = None
    
    # Process detailed environmental data if available
    if detailed_data:
        # Extract UV index (maximum for today)
        uv_index_list = detailed_data.get("daily", {}).get("uv_index_max")
        if uv_index_list and isinstance(uv_index_list, list) and len(uv_index_list) > 0:
            uv_index = uv_index_list[0]
        
        # Extract precipitation data (sum for today)
        precipitation_list = detailed_data.get("daily", {}).get("precipitation_sum")
        if precipitation_list and isinstance(precipitation_list, list) and len(precipitation_list) > 0:
            precipitation = precipitation_list[0]
    
    # Return comprehensive weather data dictionary
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
