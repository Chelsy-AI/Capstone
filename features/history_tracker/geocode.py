from geopy.geocoders import Nominatim

def get_lat_lon(city):
    geolocator = Nominatim(user_agent="weather_capstone")
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    return None, None
