from .geocode import get_lat_lon
import requests
import datetime

def fetch_world_history(city):
    lat, lon = get_lat_lon(city)
    print(f"[DEBUG] Geocoded '{city}' to lat={lat}, lon={lon}")

    if lat is None or lon is None:
        print(f"[ERROR] City not found: {city}")
        return {}

    # Compute last 7 days
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=6)

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean"
        f"&timezone=auto"
    )

    print(f"[DEBUG] Request URL: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"[DEBUG] API response keys: {list(data.keys())}")

        if "daily" in data:
            return data["daily"]
        else:
            print(f"[ERROR] 'daily' key not in API response")
            return {}
    except Exception as e:
        print(f"[ERROR] Failed to fetch history: {e}")
        return {}
