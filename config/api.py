"""
Weather API Integration Module
==============================

This module handles all communication with weather APIs on the internet.

Key functions:
- Convert city names to map coordinates
- Get current weather from multiple sources
- Combine data from different APIs for complete weather picture
- Handle errors gracefully when internet is slow or APIs are down
- Support multiple languages for weather descriptions

APIs used:
- Open-Meteo: Free weather data
- WeatherDB: Detailed current conditions
- Geocoding: Convert city names to coordinates
"""

import requests
import os
from dotenv import load_dotenv

# Load API keys and settings from .env file
load_dotenv()

# Get API credentials from environment variables
API_KEY = os.getenv("weatherdb_api_key")
BASE_URL = os.getenv("weatherdb_base_url")


def get_lat_lon(city):
    """
    Convert a city name to map coordinates.
    
    This is needed because weather APIs use coordinates, not city names.
    
    Args:
        city (str): Name of the city
        
    Returns:
        tuple: (latitude, longitude) as numbers, or (None, None) if city not found        
    """
    # Check if the input is valid
    if not isinstance(city, str):
        return None, None
    
    # Build the URL for the geocoding API
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    
    try:
        # Make the HTTP request to the geocoding service
        response = requests.get(url, timeout=10)  # Wait max 10 seconds
        
        # Check if the request was successful (HTTP 200 = OK)
        if response.status_code != 200:
            return None, None

        # Convert the response from JSON format to a Python dictionary
        data = response.json()
        
        # Get the search results from the response
        results = data.get("results")
        
        # Check if we found any matching cities
        if results and len(results) > 0:
            # Get coordinates from the first result
            lat = results[0].get("latitude")
            lon = results[0].get("longitude")
            
            # Make sure both coordinates are valid numbers
            if lat is not None and lon is not None:
                return lat, lon
        
        # If we get here, no city was found
        return None, None
        
    except Exception:
        # If anything goes wrong return None values
        return None, None


def resolve_coordinates_by_city(city_name):
    """
    Alternative function to get coordinates for a city.
    
    This does the same thing as get_lat_lon()
    
    Args:
        city_name (str): Name of the city
        
    Returns:
        tuple: (latitude, longitude) or (None, None) if not found
    """
    # Build the geocoding API URL
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    
    # Make the HTTP request
    response = requests.get(url)
    
    # Parse the JSON response
    data = response.json()
    
    # Check if we got valid results
    if data.get("results"):
        # Extract coordinates from the first result
        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]
        return lat, lon
    
    # Return None values if no results found
    return None, None


def get_basic_weather_from_weatherdb(city_name, language="en"):
    """
    Get basic weather data from WeatherDB API with language support.
    
    This API provides current weather conditions like temperature,
    humidity, wind speed, and weather descriptions.
    
    Args:
        city_name (str): Name of the city to get weather for
        language (str): Language code for weather descriptions (en, es, hi)
        
    Returns:
        tuple: (weather_data_dict, error_message)
               If successful: (data, None)
               If failed: (None, error_message)
    """
    try:
        # Set up the parameters for the API request
        params = {
            "q": city_name,           # City name to search for
            "appid": API_KEY,         # API key for authentication
            "units": "metric",        # Use Celsius for temperature
            "lang": language          # Language for weather descriptions
        }
        
        # Make the HTTP request to WeatherDB API
        response = requests.get(BASE_URL, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Success: Return the weather data and no error
            return response.json(), None
        else:
            # Failed: Return no data and an error message
            return None, f"City '{city_name}' not found."
            
    except Exception as e:
        # If anything goes wrong, return the error message
        return None, str(e)


def get_detailed_environmental_data(city):
    """
    Get detailed environmental data from Open-Meteo API.
    
    This API provides additional data like UV index, visibility,
    and precipitation.
    
    Args:
        city (str): Name of the city
        
    Returns:
        dict: Detailed weather data, or None if request failed
    """
    # First, convert city name to coordinates
    lat, lon = get_lat_lon(city)
    
    # If we couldn't find the city, return None
    if not lat or not lon:
        return None
    
    # Build the Open-Meteo API URL with all the data we want
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,surface_pressure,visibility"
        "&daily=uv_index_max,precipitation_sum"
        "&timezone=auto"  # Use the local timezone for the city
    )
    
    # Make the HTTP request
    resp = requests.get(url)
    
    # Return the data if successful, None if failed
    if resp.status_code == 200:
        return resp.json()
    return None


def get_current_weather(city, language="en"):
    """
    Get comprehensive weather data by combining multiple APIs with language support.
    
    This is the main function that other parts of the app use to get weather data.
    It combines data from multiple sources to provide the most complete picture.
    
    Args:
        city (str): Name of the city to get weather for
        language (str): Language code for weather descriptions (en, es, hi)
        
    Returns:
        dict: Complete weather data with all available information
              Always returns a dict, even if some data is missing
    """
    # Step 1: Get basic weather data from WeatherDB with language support
    weather_data, err = get_basic_weather_from_weatherdb(city, language)
    
    # Step 2: Get detailed environmental data from Open-Meteo
    detailed_data = get_detailed_environmental_data(city)
    
    # Step 3: Handle the case where basic weather data failed
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
    
    # Step 4: Extract data from the basic weather response
    main = weather_data.get("main", {})      # Temperature, humidity, pressure
    wind = weather_data.get("wind", {})      # Wind information
    weather_list = weather_data.get("weather", [{}])  # Weather conditions
    
    # Step 5: Get weather icon and description
    icon = weather_list[0].get("icon", "01d")  # Default to clear day icon
    description = weather_list[0].get("description", "No description").capitalize()
    
    # Step 6: Initialize additional data with default values
    uv_index = None
    precipitation = None
    
    # Step 7: Extract additional data from Open-Meteo if available
    if detailed_data:
        # Try to get UV index (maximum for today)
        uv_index_list = detailed_data.get("daily", {}).get("uv_index_max")
        if uv_index_list and isinstance(uv_index_list, list) and len(uv_index_list) > 0:
            uv_index = uv_index_list[0]
        
        # Try to get precipitation data (sum for today)
        precipitation_list = detailed_data.get("daily", {}).get("precipitation_sum")
        if precipitation_list and isinstance(precipitation_list, list) and len(precipitation_list) > 0:
            precipitation = precipitation_list[0]
    
    # Step 8: Return comprehensive weather data dictionary
    return {
        "temperature": main.get("temp"),         # Temperature in Celsius
        "humidity": main.get("humidity"),        # Humidity percentage
        "wind_speed": wind.get("speed"),         # Wind speed in m/s
        "pressure": main.get("pressure"),        # Atmospheric pressure in hPa
        "icon": icon,                            # Weather icon code
        "visibility": detailed_data.get("current", {}).get("visibility") if detailed_data else None,
        "uv_index": uv_index if uv_index is not None else "N/A",
        "precipitation": precipitation if precipitation is not None else "N/A",
        "error": None,                           # No error occurred
        "description": description               # Human-readable weather description
    }