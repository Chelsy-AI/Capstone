import csv
import os
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────────
# Saves weather data to a CSV file for historical tracking.
# Creates the CSV file with header row if it does not exist.
# Each record stores timestamp, city name, temperature, and description.
# ──────────────────────────────────────────────────────────────────────────────
def save_weather(data, filepath="data/weather_history.csv"):
    """
    Append weather data entry to CSV file.
    """
    file_exists = os.path.isfile(filepath)

    with open(filepath, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Write header if file is new
        if not file_exists:
            writer.writerow(["timestamp", "city", "temperature", "description"])

        # Write weather data row
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            data.get('name', 'Unknown'),
            data.get('main', {}).get('temp', 'N/A'),
            data.get('weather', [{}])[0].get('description', 'N/A')
        ])
