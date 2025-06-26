from features.history_tracker.api import fetch_world_history

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

    for i in range(len(days)):
        date = days[i]
        tmax = temps_max[i]
        tmin = temps_min[i]

        if tmax is None or tmin is None:
            text_widget.insert("end", f"{date}: Temperature data unavailable.\n")
            continue

        avg = round((tmax + tmin) / 2, 2)
        total_temp += avg
        text_widget.insert("end", f"{date}: High {tmax}°C / Low {tmin}°C (Avg: {avg}°C)\n")

    valid_days = sum(1 for tmax, tmin in zip(temps_max, temps_min) if tmax is not None and tmin is not None)
    if valid_days > 0:
        weekly_avg = round(total_temp / valid_days, 2)
        text_widget.insert("end", f"\nWeekly Average Temperature: {weekly_avg}°C")
    else:
        text_widget.insert("end", "\nNo valid temperature data to calculate weekly average.")
