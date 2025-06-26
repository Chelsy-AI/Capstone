import requests
from datetime import datetime, timedelta
from features.history_tracker.geocode import get_lat_lon

def fetch_world_history(city):
    """
    Fetch past 7 days of daily max and min temperatures for the given city
    using Open-Meteo's archive API.

    Args:
        city (str): City name to fetch weather history for.

    Returns:
        tuple: (data_dict, error_message)
            - data_dict: Parsed JSON data if successful, else None.
            - error_message: None if successful, else string error message.
    """
    # Get latitude and longitude for the city
    lat, lon = get_lat_lon(city)
    if not lat or not lon:
        return None, "City not found."

    today = datetime.today()
    start = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    end = (today - timedelta(days=1)).strftime("%Y-%m-%d")

    # Construct API URL with required parameters
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
