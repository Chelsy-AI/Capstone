from .geocode import get_lat_lon
import requests
import datetime
import time

# ────────────────────────────────────────────────────────────────────────────── 
# HISTORICAL WEATHER DATA API MODULE
# 
# This module fetches historical weather data from the Open-Meteo Archive API.
# It includes caching to avoid repeated API calls and provides temperature
# data for the last 7 days for any given city.
# 
# API Used: Open-Meteo Archive API 
# Data Retrieved: Daily max, min, and mean temperatures for past 7 days
# ────────────────────────────────────────────────────────────────────────────── 

# ────────────────────────────────────────────────────────────────────────────── 
# CACHING SYSTEM
# ────────────────────────────────────────────────────────────────────────────── 

# Global cache dictionary to store recent API responses
# Structure: {city_name: (timestamp, data)}
# This prevents making the same API call multiple times in a short period
_weather_cache = {}

# How long to keep cached data (in seconds)
# 120 seconds = 2 minutes - reasonable for historical data that doesn't change
CACHE_DURATION = 120

def _is_cache_valid(city_key):
    """
    Check if we have valid cached data for a city.
    
    """
    if city_key not in _weather_cache:
        return False, None
    
    cached_time, cached_data = _weather_cache[city_key]
    current_time = time.time()
    
    # Check if cache is still fresh
    if current_time - cached_time < CACHE_DURATION:
        return True, cached_data
    else:
        # Cache expired, remove it
        del _weather_cache[city_key]
        return False, None

def _cache_data(city_key, data):
    """
    Store data in the cache with current timestamp.
    
    """
    current_time = time.time()
    _weather_cache[city_key] = (current_time, data)

def clear_weather_cache():
    """
    Clear all cached weather data.
    Useful for debugging or if you want fresh data.
    """
    global _weather_cache
    _weather_cache.clear()

# ────────────────────────────────────────────────────────────────────────────── 
# MAIN API FUNCTION
# ────────────────────────────────────────────────────────────────────────────── 

def fetch_world_history(city):
    """
    Fetch last 7 days of daily temperature data for the specified city.
    
    This function:
    1. Validates input
    2. Checks cache for recent data
    3. Gets city coordinates using geocoding
    4. Calculates date range (last 7 days)
    5. Makes API request to Open-Meteo Archive
    6. Validates and caches the response
    
    """
    
    # ────────────────────────────────────────────────────────────────────────── 
    # INPUT VALIDATION
    # ────────────────────────────────────────────────────────────────────────── 
    
    # Check if city parameter is valid
    if not isinstance(city, str):
        return {}
    
    # Remove extra whitespace and convert to lowercase for cache key
    city = city.strip()
    if not city:
        return {}
    
    city_key = city.lower()
    
    # ────────────────────────────────────────────────────────────────────────── 
    # CHECK CACHE
    # ────────────────────────────────────────────────────────────────────────── 
    
    # Check if we have recent cached data for this city
    cache_valid, cached_data = _is_cache_valid(city_key)
    if cache_valid:
        return cached_data
    
    # ────────────────────────────────────────────────────────────────────────── 
    # GET CITY COORDINATES
    # ────────────────────────────────────────────────────────────────────────── 
    
    # Convert city name to latitude/longitude coordinates
    # This is needed because the weather API requires coordinates, not city names
    lat, lon = get_lat_lon(city)
    
    if lat is None or lon is None:
        return {}
    
    
    # ────────────────────────────────────────────────────────────────────────── 
    # CALCULATE DATE RANGE
    # ────────────────────────────────────────────────────────────────────────── 
    
    # Get last 7 days of data (excluding today since today isn't complete)
    # We want complete days only, so we end at yesterday
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    start_date = end_date - datetime.timedelta(days=6)
    
    # Convert dates to ISO format (YYYY-MM-DD) required by the API
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()
    
    
    # ────────────────────────────────────────────────────────────────────────── 
    # BUILD API REQUEST URL
    # ────────────────────────────────────────────────────────────────────────── 
    
    # Build the URL for the Open-Meteo Archive API
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"                                    # City coordinates
        f"&start_date={start_date_str}&end_date={end_date_str}"             # Date range
        f"&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean" # What data to get
        f"&timezone=auto"                                                    # Use local timezone
    )
    
    # ────────────────────────────────────────────────────────────────────────── 
    # MAKE API REQUEST
    # ────────────────────────────────────────────────────────────────────────── 
    
    try:
        
        # Make the HTTP request with timeout to prevent hanging
        response = requests.get(url, timeout=10)
        
        # Check if request was successful (status code 200)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # ────────────────────────────────────────────────────────────────────── 
        # VALIDATE RESPONSE DATA
        # ────────────────────────────────────────────────────────────────────── 
        
        # Extract the 'daily' section which contains our temperature data
        daily = data.get("daily", {})
        
        if not daily:
            return {}
        
        # Get temperature lists from the daily data
        max_temps = daily.get("temperature_2m_max")
        min_temps = daily.get("temperature_2m_min")
        mean_temps = daily.get("temperature_2m_mean")
        dates = daily.get("time")
        
        # Check if all required temperature data is present
        if not max_temps or not min_temps or not mean_temps or not dates:
            return {}
        
        # Check if temperature lists have data (not empty)
        if (len(max_temps) == 0 or len(min_temps) == 0 or 
            len(mean_temps) == 0 or len(dates) == 0):
            return {}
        
        # Check if all lists have the same length (data consistency)
        if not (len(max_temps) == len(min_temps) == len(mean_temps) == len(dates)):
            return {}
        
        # ────────────────────────────────────────────────────────────────────── 
        # CACHE AND RETURN SUCCESS
        # ────────────────────────────────────────────────────────────────────── 
        
        # Cache the successful response for future use
        _cache_data(city_key, daily)
        
        return daily

    except:
        pass 

# ────────────────────────────────────────────────────────────────────────────── 
# HELPER FUNCTIONS
# ────────────────────────────────────────────────────────────────────────────── 

def get_cache_info():
    """
    Get information about the current cache state.
    Useful for debugging and monitoring.
    
    """
    current_time = time.time()
    cache_info = {
        'total_entries': len(_weather_cache),
        'entries': []
    }
    
    for city_key, (cached_time, data) in _weather_cache.items():
        age_seconds = current_time - cached_time
        time_remaining = CACHE_DURATION - age_seconds
        
        cache_info['entries'].append({
            'city': city_key,
            'age_seconds': round(age_seconds, 1),
            'time_remaining': round(time_remaining, 1),
            'expired': time_remaining <= 0
        })
    
    return cache_info

def format_temperature_data(daily_data, unit='C'):
    """
    Format temperature data for display.
    
    """
    if not daily_data:
        return []
    
    dates = daily_data.get('time', [])
    max_temps = daily_data.get('temperature_2m_max', [])
    min_temps = daily_data.get('temperature_2m_min', [])
    
    formatted_data = []
    
    for i, date in enumerate(dates):
        if i < len(max_temps) and i < len(min_temps):
            max_temp = max_temps[i]
            min_temp = min_temps[i]
            
            # Convert to Fahrenheit if requested
            if unit == 'F':
                max_temp = max_temp * 9/5 + 32
                min_temp = min_temp * 9/5 + 32
            
            formatted_data.append(f"{date}: {max_temp:.1f}°{unit} / {min_temp:.1f}°{unit}")
    
    return formatted_data
