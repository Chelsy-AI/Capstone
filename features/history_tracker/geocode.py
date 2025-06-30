from geopy.geocoders import Nominatim

def get_lat_lon(city):
    geolocator = Nominatim(user_agent="my_weather_app")
    try:
        location = geolocator.geocode(city)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print(f"[ERROR] Geocode failed for {city}: {e}")
    return None, None
