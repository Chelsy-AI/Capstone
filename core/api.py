import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("weatherdb_api_key")
BASE_URL = os.getenv("weatherdb_base_url")

def fetch_weather(city):
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"City '{city}' not found."
    except Exception as e:
        return None, str(e)
