from geopy.geocoders import Nominatim

_geocode_cache = {}

def get_lat_lon(city):
    """
    Geocode the city name to latitude and longitude coordinates.
    Uses in-memory cache to speed up repeated lookups.
    Returns (lat, lon) tuple or (None, None) if failed.
    """
    city_key = city.lower()
    if city_key in _geocode_cache:
        return _geocode_cache[city_key]

    geolocator = Nominatim(user_agent="my_weather_app")
    try:
        location = geolocator.geocode(city, timeout=5)
        if location:
            lat_lon = (location.latitude, location.longitude)
            _geocode_cache[city_key] = lat_lon
            return lat_lon
    except Exception as e:
        print(f"[ERROR] Geocode failed for {city}: {e}")

    _geocode_cache[city_key] = (None, None)
    return None, None
