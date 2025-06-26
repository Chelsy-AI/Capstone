import requests
from datetime import datetime, timedelta
from history_tracker.geocode import get_lat_lon


def fetch_world_history(city):
    lat, lon = get_lat_lon(city)
    if not lat or not lon:
        return None, "City not found."

    today = datetime.today()
    start = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    end = (today - timedelta(days=1)).strftime("%Y-%m-%d")

    url = (
        "https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start}&end_date={end}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&temperature_unit=celsius"
        f"&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.Timeout:
        return None, "Request timed out. Please check your connection."
    except requests.exceptions.ConnectionError:
        return None, "Connection error. Please check your internet."
    except requests.exceptions.HTTPError as e:
        return None, f"HTTP error: {e.response.status_code}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"
