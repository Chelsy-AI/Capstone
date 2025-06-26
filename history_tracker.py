import requests
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim

def get_lat_lon(city):
    geolocator = Nominatim(user_agent="weather_capstone")
    location = geolocator.geocode(city)
    print("🔍 Geocoding result for", city, "→", location)

    if location:
        return location.latitude, location.longitude
    else:
        return None, None
    
def fetch_world_history(city):
    lat, lon = get_lat_lon(city)
    if not lat or not lon:
        return None, "City not found."

    today = datetime.today()
    start = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    end = (today - timedelta(days=1)).strftime("%Y-%m-%d")

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start}&end_date={end}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone=auto"
    )

    response = requests.get(url)
    if response.status_code == 200:
        return response.json(), None
    else:
        return None, "Failed to fetch data."
    

def show_weather_history(text_widget, city="New York"):
    text_widget.delete('1.0', "end")
    text_widget.insert("end", f"Fetching 7-day history for {city}...\n")

    data, error = fetch_world_history(city)
    if error:
        text_widget.insert("end", f"Error: {error}")
        return
    
    days = data["daily"]["time"]
    temps_max = data["daily"]["temperature_2m_max"]
    temps_min = data["daily"]["temperature_2m_min"]

    total_temp = 0
    count = 0

    for i in range(len(days)):
        date = days[i]
        tmax = temps_max[i]
        tmin = temps_min[i]
        avg = round((tmax + tmin) / 2, 2)
        total_temp += avg
        count += 1
        text_widget.insert("end", f"{date}: Hight {tmax}°C / Low (tmin)°C (Avg: {avg}°C)\n")

    weekly_avg = round(total_temp / count, 2)
    text_widget.insert("end", f"\nWeekly Average Temperature: {weekly_avg}°C")