from geopy.geocoders import Nominatim

def get_lat_lon(city):
    """
    Uses the Nominatim geocoder to convert a city name into latitude and longitude coordinates.

    Args:
        city (str): The name of the city to geocode.

    Returns:
        tuple: (latitude, longitude) if found, otherwise (None, None).
    """
    geolocator = Nominatim(user_agent="weather_capstone")
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    return None, None
