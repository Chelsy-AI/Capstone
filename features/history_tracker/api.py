"""
Historical Weather Data API Module
==================================

This module fetches historical weather data from the internet for any city.

Key features:
- Gets weather data for the last 7 days
- Converts city names to map coordinates automatically
- Caches data to avoid repeated API calls
- Handles network errors gracefully
- Works with the Open-Meteo Archive API

How it works:
1. You give it a city name like "London"
2. It converts the city to coordinates (latitude/longitude)
3. It asks the weather API for the last 7 days of data
4. It returns temperature, precipitation, and other weather info
5. It remembers the data for 2 minutes to avoid repeated requests
"""

import requests
import datetime
import time

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CACHING SYSTEM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Global cache to store recent API responses
# This prevents making the same API call multiple times in a short period
# Structure: {city_name: (timestamp_when_saved, weather_data)}
_weather_cache = {}

# How long to keep cached data
CACHE_DURATION = 120 # 2 minutes


def get_lat_lon(city):
    """
    Convert a city name to latitude and longitude coordinates.
    
    Args:
        city (str): Name of the city
        
    Returns:
        tuple: as numbers, or (None, None) if city not found
    """
    
    # Step 1: Validate input - make sure we have a valid city name
    if not isinstance(city, str):
        return None, None
    
    # Step 2: Build the URL for the geocoding API
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    
    try:
        # Step 3: Make the HTTP request to find the city
        response = requests.get(url)
        
        # Step 4: Check if the request was successful
        if response.status_code != 200:
            # If the API returned an error status, return None
            return None, None

        # Step 5: Parse the JSON response
        data = response.json()
        
        # Step 6: Extract the search results
        results = data.get("results")
        
        # Step 7: Get coordinates from the first result
        if results and len(results) > 0:
            lat = results[0].get("latitude")
            lon = results[0].get("longitude")
            
            # Make sure both coordinates are valid numbers
            if lat is not None and lon is not None:
                return lat, lon
        
        # If we get here, no city was found
        return None, None
        
    except requests.exceptions.RequestException as e:
        # Handle network errors
        return None, None
        
    except ValueError as e:
        # Handle JSON parsing errors
        return None, None
        
    except Exception as e:
        # Handle any other unexpected errors
        return None, None


def _is_cache_valid(city_key):
    """
    Check if we have fresh cached data for a city.
    
    Args:
        city_key (str): Lowercase city name used as cache key
        
    Returns:
        tuple: (is_valid, cached_data) - True/False and the data if valid
    """
    # Check if we have any cached data for this city
    if city_key not in _weather_cache:
        return False, None
    
    # Get the cached data and when it was saved
    cached_time, cached_data = _weather_cache[city_key]
    current_time = time.time()
    
    # Check if the cache is still fresh
    if current_time - cached_time < CACHE_DURATION:
        # Cache is still good - use it
        return True, cached_data
    else:
        # Cache is too old - remove it and get fresh data
        del _weather_cache[city_key]
        return False, None


def _cache_data(city_key, data):
    """
    Store weather data in the cache with current timestamp.
    
    Args:
        city_key (str): City name used as cache key
        data (dict): Weather data to cache
    """
    current_time = time.time()
    _weather_cache[city_key] = (current_time, data)


def clear_weather_cache():
    """Clear all cached weather data."""
    global _weather_cache
    _weather_cache.clear()


def fetch_world_history(city):
    """
    Fetch the last 7 days of weather data for any city in the world.
    
    This is the main function that gets historical weather information.
    It handles all the complexity of coordinates, API calls, and caching.
    
    Args:
        city (str): Name of the city
        
    Returns:
        dict: Weather data for the last 7 days, or empty dict if failed
              Contains: time, temperature_2m_max, temperature_2m_min, 
                       temperature_2m_mean, and other weather measurements
    """
    
    # INPUT VALIDATION
    
    # Make sure we have a valid city name
    if not isinstance(city, str):
        return {}
    
    # Clean up the city name and make sure it's not empty
    city = city.strip()
    if not city:
        return {}
    
    # Create cache key
    city_key = city.lower()
    
    # CHECK CACHE FIRST
    
    # Check if we already have recent data for this city
    cache_valid, cached_data = _is_cache_valid(city_key)
    if cache_valid:
        # We have fresh cached data - return
        return cached_data
    
    # GET CITY COORDINATES
    
    # Convert city name to latitude/longitude coordinates
    lat, lon = get_lat_lon(city)
    
    # If we couldn't find the city, return empty data
    if lat is None or lon is None:
        return {}
    
    # CALCULATE DATE RANGE
    
    # Calculate the date range for the last 7 days
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    start_date = end_date - datetime.timedelta(days=6)  # 7 days total including end_date
    
    # Convert dates to ISO format (YYYY-MM-DD) that the API expects
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()
    
    # BUILD API REQUEST URL
    
    # Build the URL for the Open-Meteo Archive API
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"                                    # City location
        f"&start_date={start_date_str}&end_date={end_date_str}"             # Date range (last 7 days)
        f"&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean" # Temperature data we want
        f"&timezone=auto"                                                    # Use local timezone
    )
    
    # MAKE API REQUEST
    
    try:
        # Make the HTTP request with a reasonable timeout
        response = requests.get(url, timeout=10)
        
        # Check if the request was successful (HTTP 200 = OK)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # VALIDATE RESPONSE DATA
        
        # Extract the 'daily' section which contains our temperature data
        daily = data.get("daily", {})
        
        # Make sure we got the daily data section
        if not daily:
            return {}
        
        # Get all the temperature arrays from the daily data
        max_temps = daily.get("temperature_2m_max")     # Daily maximum temperatures
        min_temps = daily.get("temperature_2m_min")     # Daily minimum temperatures
        mean_temps = daily.get("temperature_2m_mean")   # Daily average temperatures
        dates = daily.get("time")                       # List of dates
        
        # Check that all required data is present
        if not max_temps or not min_temps or not mean_temps or not dates:
            return {}
        
        # Check that all arrays have data (not empty)
        if (len(max_temps) == 0 or len(min_temps) == 0 or 
            len(mean_temps) == 0 or len(dates) == 0):
            return {}
        
        # Check that all arrays have the same length (data consistency)
        expected_length = len(dates)
        if not (len(max_temps) == len(min_temps) == len(mean_temps) == expected_length):
            return {}
        
        # CACHE AND RETURN SUCCESS
        
        # Cache the successful response for future use (next 2 minutes)
        _cache_data(city_key, daily)
        
        # Return the daily weather data
        return daily

    except requests.exceptions.Timeout:
        # API request took too long
        return {}
    except requests.exceptions.RequestException:
        # Network error
        return {}
    except ValueError:
        # JSON parsing error
        return {}
    except Exception:
        # Any other unexpected error
        return {}


# HELPER FUNCTIONS

def get_cache_info():
    """
    Get information about the current cache state.
    
    This is useful for debugging and monitoring how the cache is working.
    
    Returns:
        dict: Information about cached cities and their freshness
    """
    current_time = time.time()
    cache_info = {
        'total_entries': len(_weather_cache),
        'entries': []
    }
    
    # Analyze each cached entry
    for city_key, (cached_time, data) in _weather_cache.items():
        age_seconds = current_time - cached_time
        time_remaining = CACHE_DURATION - age_seconds
        
        entry_info = {
            'city': city_key,
            'age_seconds': round(age_seconds, 1),
            'time_remaining': round(time_remaining, 1),
            'expired': time_remaining <= 0
        }
        
        cache_info['entries'].append(entry_info)
    
    return cache_info


def format_temperature_data(daily_data, unit='C'):
    """
    Format temperature data for easy display.
    
    Args:
        daily_data (dict): Raw daily weather data from API
        unit (str): Temperature unit ('C' for Celsius, 'F' for Fahrenheit)
        
    Returns:
        list: Formatted temperature strings for each day
    """
    if not daily_data:
        return []
    
    # Extract data arrays
    dates = daily_data.get('time', [])
    max_temps = daily_data.get('temperature_2m_max', [])
    min_temps = daily_data.get('temperature_2m_min', [])
    
    formatted_data = []
    
    # Format each day's data
    for i, date in enumerate(dates):
        if i < len(max_temps) and i < len(min_temps):
            max_temp = max_temps[i]
            min_temp = min_temps[i]
            
            # Convert to Fahrenheit if requested
            if unit == 'F':
                max_temp = max_temp * 9/5 + 32
                min_temp = min_temp * 9/5 + 32
            
            # Create formatted string
            formatted_string = f"{date}: {max_temp:.1f}°{unit} / {min_temp:.1f}°{unit}"
            formatted_data.append(formatted_string)
    
    return formatted_data


def get_weather_summary(city, days=7):
    """
    Get a summary of weather conditions for a city.
    
    Args:
        city (str): Name of the city
        days (int): Number of days to analyze (default 7)
        
    Returns:
        dict: Weather summary with averages, extremes, and trends
    """
    try:
        # Get historical data
        data = fetch_world_history(city)
        
        if not data or 'time' not in data:
            return {
                "city": city,
                "days_analyzed": 0,
                "error": "No historical data available"
            }
        
        # Extract data arrays
        dates = data.get('time', [])
        max_temps = data.get('temperature_2m_max', [])
        min_temps = data.get('temperature_2m_min', [])
        mean_temps = data.get('temperature_2m_mean', [])
        
        # Filter out None values and limit to requested days
        valid_data = []
        for i in range(min(len(dates), days)):
            if (i < len(max_temps) and i < len(min_temps) and 
                max_temps[i] is not None and min_temps[i] is not None):
                valid_data.append({
                    'date': dates[i],
                    'max': max_temps[i],
                    'min': min_temps[i],
                    'mean': mean_temps[i] if i < len(mean_temps) and mean_temps[i] is not None else (max_temps[i] + min_temps[i]) / 2
                })
        
        if not valid_data:
            return {
                "city": city,
                "days_analyzed": 0,
                "error": "No valid temperature data"
            }
        
        # Calculate summary statistics
        max_temps_only = [day['max'] for day in valid_data]
        min_temps_only = [day['min'] for day in valid_data]
        mean_temps_only = [day['mean'] for day in valid_data]
        
        # Find extremes
        hottest_day = max(valid_data, key=lambda x: x['max'])
        coldest_day = min(valid_data, key=lambda x: x['min'])
        
        # Calculate trend
        if len(mean_temps_only) >= 4:
            first_half_avg = sum(mean_temps_only[:len(mean_temps_only)//2]) / (len(mean_temps_only)//2)
            second_half_avg = sum(mean_temps_only[len(mean_temps_only)//2:]) / (len(mean_temps_only) - len(mean_temps_only)//2)
            
            if second_half_avg > first_half_avg + 1:
                trend = "rising"
            elif second_half_avg < first_half_avg - 1:
                trend = "falling"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "city": city,
            "days_analyzed": len(valid_data),
            "avg_high": round(sum(max_temps_only) / len(max_temps_only), 1),
            "avg_low": round(sum(min_temps_only) / len(min_temps_only), 1),
            "avg_mean": round(sum(mean_temps_only) / len(mean_temps_only), 1),
            "hottest_day": {
                "date": hottest_day['date'],
                "temp": hottest_day['max']
            },
            "coldest_day": {
                "date": coldest_day['date'],
                "temp": coldest_day['min']
            },
            "temperature_range": round(max(max_temps_only) - min(min_temps_only), 1),
            "temperature_trend": trend,
            "data_quality": "good" if len(valid_data) >= 5 else "limited"
        }
        
    except Exception as e:
        return {
            "city": city,
            "days_analyzed": 0,
            "error": f"Analysis failed: {str(e)}"
        }
