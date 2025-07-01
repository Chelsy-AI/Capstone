from geopy.geocoders import Nominatim

# ──────────────────────────────────────────────────────────────────────────────
# Uses geopy's Nominatim service to get latitude and longitude of a city.
# ──────────────────────────────────────────────────────────────────────────────
def get_lat_lon(city):
    """
    Geocode the city name to latitude and longitude coordinates.
    Returns (lat, lon) tuple or (None, None) if failed.
    """
    geolocator = Nominatim(user_agent="my_weather_app")
    try:
        location = geolocator.geocode(city)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print(f"[ERROR] Geocode failed for {city}: {e}")
    return None, None
