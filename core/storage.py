import csv
import os
from datetime import datetime

def save_weather(data, filepath="data/weather_history.csv"):
    file_exists = os.path.isfile(filepath)

    with open(filepath, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["timestamp", "city", "temperature", "description"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            data['name'],
            data['main']['temp'],
            data['weather'][0]['description']
        ])
