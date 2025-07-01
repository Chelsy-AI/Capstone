import requests

def get_lat_lon(city):
    """
    Fetch the latitude and longitude of the given city using Open-Meteo geocoding API.
    Returns (latitude, longitude) tuple or (None, None) if not found.
    Defensive: logs error if input is invalid or API fails.
    """
    if not isinstance(city, str):
        print(f"[ERROR] get_lat_lon called with invalid city argument (not str): {city}")
        return None, None

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"[ERROR] Geocoding API returned status {response.status_code} for city '{city}'")
            return None, None

        data = response.json()
        results = data.get("results")
        if results and len(results) > 0:
            lat = results[0].get("latitude")
            lon = results[0].get("longitude")
            if lat is not None and lon is not None:
                return lat, lon
        print(f"[ERROR] No results found in geocoding API response for city '{city}'")
        return None, None
    except Exception as e:
        print(f"[ERROR] Exception during geocoding API request for city '{city}': {e}")
        return None, None
