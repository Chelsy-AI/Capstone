from .geocode import get_lat_lon
import requests
import datetime

def fetch_world_history(city):
    lat, lon = get_lat_lon(city)
    if lat is None or lon is None:
        return None, "Invalid city"

    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=6)

    url = (
        "https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        "&daily=temperature_2m_max,temperature_2m_min"
        "&timezone=America%2FNew_York"
    )

    try:
        response = requests.get(url)
        data = response.json()
        return data, None
    except Exception as e:
        return None, str(e)
