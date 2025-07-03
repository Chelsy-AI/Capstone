from .geocode import get_lat_lon
import requests
import datetime
import time

_weather_cache = {}
CACHE_DURATION = 120  # Cache duration in seconds


def fetch_world_history(city):
    """
    Fetch last 7 days of daily temperature data for the specified city.
    Returns the 'daily' dict if data exists and contains valid temperature lists,
    otherwise returns an empty dict.
    Uses simple in-memory caching to reduce repeated API calls.
    """
    if not isinstance(city, str):
        print(f"[ERROR] fetch_world_history called with invalid city argument (not str): {city}")
        return {}

    city_key = city.lower()
    now = time.time()
    if city_key in _weather_cache:
        cached_time, cached_data = _weather_cache[city_key]
        if now - cached_time < CACHE_DURATION:
            return cached_data

    lat, lon = get_lat_lon(city)
    if lat is None or lon is None:
        print(f"[ERROR] Geocode failed for city '{city}'")
        return {}

    # Compute last 7 days date range (past dates only)
    end_date = datetime.date.today() - datetime.timedelta(days=1)  # yesterday
    start_date = end_date - datetime.timedelta(days=6)

    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date_str}&end_date={end_date_str}"
        f"&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean"
        f"&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        daily = data.get("daily", {})
        max_temps = daily.get("temperature_2m_max")
        min_temps = daily.get("temperature_2m_min")
        mean_temps = daily.get("temperature_2m_mean")

        if not max_temps or not min_temps or not mean_temps:
            print(f"[ERROR] Missing temperature data in API response for city '{city}'")
            return {}

        if len(max_temps) == 0 or len(min_temps) == 0 or len(mean_temps) == 0:
            print(f"[ERROR] Empty temperature lists in API response for city '{city}'")
            return {}

        # Cache the successful response
        _weather_cache[city_key] = (now, daily)
        return daily

    except Exception as e:
        print(f"[ERROR] Exception fetching weather history for city '{city}': {e}")
        return {}
