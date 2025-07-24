"""
Historical Weather Data API Module
==================================

This module fetches historical weather data from the internet for any city.
It's like having access to a weather time machine - you can see what the
weather was like in any city for the past week!

Key features:
- Gets weather data for the last 7 days
- Converts city names to map coordinates automatically
- Caches data to avoid repeated API calls (faster and more efficient)
- Handles network errors gracefully
- Works with the Open-Meteo Archive API (free, no API key needed!)

How it works:
1. You give it a city name like "London"
2. It converts the city to coordinates (latitude/longitude)
3. It asks the weather API for the last 7 days of data
4. It returns temperature, precipitation, and other weather info
5. It remembers the data for 2 minutes to avoid repeated requests

Think of this as your personal weather historian!
"""

import requests      # For making HTTP requests to weather APIs
import datetime      # For working with dates and times
import time          # For caching timestamps

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CACHING SYSTEM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Global cache to store recent API responses
# This prevents making the same API call multiple times in a short period
# Structure: {city_name: (timestamp_when_saved, weather_data)}
_weather_cache = {}

# How long to keep cached data (in seconds)
# 120 seconds = 2 minutes - reasonable for historical data that doesn't change often
CACHE_DURATION = 120


def get_lat_lon(city):
    """
    Convert a city name to latitude and longitude coordinates.
    
    Weather APIs need coordinates, not city names, so this function
    acts like a GPS system to find where a city is located on Earth.
    
    Args:
        city (str): Name of the city (like "Paris", "New York", "Tokyo")
        
    Returns:
        tuple: (latitude, longitude) as numbers, or (None, None) if city not found
        
    Example:
        lat, lon = get_lat_lon("London")
        # Returns: (51.5074, -0.1278) - London's coordinates
    """
    
    # Step 1: Validate input - make sure we have a valid city name
    if not isinstance(city, str):
        return None, None
    
    # Step 2: Build the URL for the geocoding API
    # This API is free and provided by Open-Meteo
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
        
        # Step 7: Get coordinates from the first (best) result
        if results and len(results) > 0:
            lat = results[0].get("latitude")
            lon = results[0].get("longitude")
            
            # Make sure both coordinates are valid numbers
            if lat is not None and lon is not None:
                return lat, lon
        
        # If we get here, no city was found
        return None, None
        
    except requests.exceptions.RequestException as e:
        # Handle network errors (no internet, API down, etc.)
        return None, None
        
    except ValueError as e:
        # Handle JSON parsing errors (malformed response)
        return None, None
        
    except Exception as e:
        # Handle any other unexpected errors
        return None, None


def _is_cache_valid(city_key):
    """
    Check if we have fresh cached data for a city.
    
    This prevents making unnecessary API calls by reusing recent data.
    It's like checking if you already have fresh information before
    asking for it again.
    
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
    
    # Check if the cache is still fresh (within our time limit)
    if current_time - cached_time < CACHE_DURATION:
        # Cache is still good - use it!
        return True, cached_data
    else:
        # Cache is too old - remove it and get fresh data
        del _weather_cache[city_key]
        return False, None


def _cache_data(city_key, data):
    """
    Store weather data in the cache with current timestamp.
    
    This saves the data so we don't have to ask the API again
    for the same information in the next few minutes.
    
    Args:
        city_key (str): City name used as cache key
        data (dict): Weather data to cache
    """
    current_time = time.time()
    _weather_cache[city_key] = (current_time, data)


def clear_weather_cache():
    """
    Clear all cached weather data.
    
    This forces fresh data to be fetched on the next request.
    Useful for debugging or if you want to ensure you get the latest data.
    """
    global _weather_cache
    _weather_cache.clear()


def fetch_world_history(city):
    """
    Fetch the last 7 days of weather data for any city in the world.
    
    This is the main function that gets historical weather information.
    It handles all the complexity of coordinates, API calls, and caching
    so you just need to provide a city name.
    
    Args:
        city (str): Name of the city (like "Berlin", "Tokyo", "New York")
        
    Returns:
        dict: Weather data for the last 7 days, or empty dict if failed
              Contains: time, temperature_2m_max, temperature_2m_min, 
                       temperature_2m_mean, and other weather measurements
                       
    Example:
        data = fetch_world_history("Paris")
        # Returns: {
        #     "time": ["2024-01-10", "2024-01-11", ...],
        #     "temperature_2m_max": [15.2, 18.1, ...],
        #     "temperature_2m_min": [8.3, 12.4, ...],
        #     ...
        # }
    """
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # STEP 1: INPUT VALIDATION
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Make sure we have a valid city name
    if not isinstance(city, str):
        return {}
    
    # Clean up the city name and make sure it's not empty
    city = city.strip()
    if not city:
        return {}
    
    # Create cache key (lowercase for consistent caching)
    city_key = city.lower()
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # STEP 2: CHECK CACHE FIRST
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Check if we already have recent data for this city
    cache_valid, cached_data = _is_cache_valid(city_key)
    if cache_valid:
        # We have fresh cached data - return it immediately!
        return cached_data
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # STEP 3: GET CITY COORDINATES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Convert city name to latitude/longitude coordinates
    lat, lon = get_lat_lon(city)
    
    # If we couldn't find the city, return empty data
    if lat is None or lon is None:
        return {}
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # STEP 4: CALCULATE DATE RANGE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Calculate the date range for the last 7 days
    # We end at yesterday because today's data might not be complete yet
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    start_date = end_date - datetime.timedelta(days=6)  # 7 days total including end_date
    
    # Convert dates to ISO format (YYYY-MM-DD) that the API expects
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # STEP 5: BUILD API REQUEST URL
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    # Build the URL for the Open-Meteo Archive API
    # This API provides historical weather data for free
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"                                    # City location
        f"&start_date={start_date_str}&end_date={end_date_str}"             # Date range (last 7 days)
        f"&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean" # Temperature data we want
        f"&timezone=auto"                                                    # Use local timezone
    )
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # STEP 6: MAKE API REQUEST
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    try:
        # Make the HTTP request with a reasonable timeout
        response = requests.get(url, timeout=10)
        
        # Check if the request was successful (HTTP 200 = OK)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # STEP 7: VALIDATE RESPONSE DATA
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
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
        
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # STEP 8: CACHE AND RETURN SUCCESS
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        # Cache the successful response for future use (next 2 minutes)
        _cache_data(city_key, daily)
        
        # Return the daily weather data
        return daily

    except requests.exceptions.Timeout:
        # API request took too long
        return {}
    except requests.exceptions.RequestException:
        # Network error (no internet, API down, etc.)
        return {}
    except ValueError:
        # JSON parsing error (malformed response)
        return {}
    except Exception:
        # Any other unexpected error
        return {}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_cache_info():
    """
    Get information about the current cache state.
    
    This is useful for debugging and monitoring how the cache is working.
    
    Returns:
        dict: Information about cached cities and their freshness
        
    Example:
        info = get_cache_info()
        # Returns: {
        #     'total_entries': 3,
        #     'entries': [
        #         {'city': 'london', 'age_seconds': 45.2, 'time_remaining': 74.8},
        #         {'city': 'paris', 'age_seconds': 120.1, 'expired': True},
        #         ...
        #     ]
        # }
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
    
    This converts the raw API data into human-readable strings
    that can be shown to users.
    
    Args:
        daily_data (dict): Raw daily weather data from API
        unit (str): Temperature unit ('C' for Celsius, 'F' for Fahrenheit)
        
    Returns:
        list: Formatted temperature strings for each day
        
    Example:
        formatted = format_temperature_data(weather_data, 'F')
        # Returns: [
        #     "2024-01-10: 68.0°F / 46.4°F",
        #     "2024-01-11: 72.1°F / 53.2°F",
        #     ...
        # ]
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
    
    This provides a quick overview of recent weather patterns
    that's easy to understand and display.
    
    Args:
        city (str): Name of the city
        days (int): Number of days to analyze (default 7)
        
    Returns:
        dict: Weather summary with averages, extremes, and trends
        
    Example:
        summary = get_weather_summary("London")
        # Returns: {
        #     "city": "London",
        #     "days_analyzed": 7,
        #     "avg_high": 18.2,
        #     "avg_low": 12.1,
        #     "hottest_day": {"date": "2024-01-15", "temp": 22.3},
        #     "coldest_day": {"date": "2024-01-12", "temp": 8.7},
        #     "temperature_trend": "rising"
        # }
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
        
        # Calculate trend (simple comparison of first half vs second half)
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TESTING AND EXAMPLE USAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    """
    This section runs when you execute this file directly.
    It's useful for testing the historical weather functions.
    """
    
    print("Testing Historical Weather Data API")
    print("=" * 40)
    
    # Test cities from different continents
    test_cities = ["London", "New York", "Tokyo", "Sydney", "Cairo"]
    
    print("\n🌍 Testing weather history for multiple cities:")
    
    for city in test_cities:
        print(f"\n📍 Testing {city}:")
        
        # Test basic historical data fetch
        history = fetch_world_history(city)
        
        if history and 'time' in history:
            dates = len(history['time'])
            print(f"  ✅ Got {dates} days of historical data")
            
            # Test weather summary
            summary = get_weather_summary(city)
            if 'error' not in summary:
                print(f"  🌡️  Average high: {summary['avg_high']}°C")
                print(f"  🌡️  Average low: {summary['avg_low']}°C")
                print(f"  📈 Temperature trend: {summary['temperature_trend']}")
                print(f"  🔥 Hottest day: {summary['hottest_day']['temp']}°C on {summary['hottest_day']['date']}")
            else:
                print(f"  ❌ Summary error: {summary['error']}")
            
        else:
            print(f"  ❌ No historical data available")
    
    # Test caching system
    print(f"\n💾 Testing cache system:")
    cache_info = get_cache_info()
    print(f"  Cache entries: {cache_info['total_entries']}")
    
    if cache_info['entries']:
        for entry in cache_info['entries']:
            status = "expired" if entry['expired'] else f"{entry['time_remaining']:.1f}s remaining"
            print(f"  - {entry['city']}: {status}")
    
    # Test data formatting
    print(f"\n📊 Testing data formatting:")
    london_data = fetch_world_history("London")
    if london_data:
        formatted_c = format_temperature_data(london_data, 'C')
        formatted_f = format_temperature_data(london_data, 'F')
        
        print(f"  Celsius format: {formatted_c[0] if formatted_c else 'No data'}")
        print(f"  Fahrenheit format: {formatted_f[0] if formatted_f else 'No data'}")
    
    print(f"\n✅ Historical weather API testing completed!")
    print(f"\nNote: This API provides 7 days of historical weather data")
    print(f"for any city worldwide using the free Open-Meteo Archive API.")