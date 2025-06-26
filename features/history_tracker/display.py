from features.history_tracker.api import fetch_world_history

def show_weather_history(text_widget, city="New York"):
    """
    Fetches 7-day temperature history for the specified city and displays it
    in the provided text widget.

    Args:
        text_widget: A Tkinter text widget where the output will be displayed.
        city (str): Name of the city to fetch history for. Defaults to "New York".
    """
    # Clear the text widget and show initial loading message
    text_widget.delete('1.0', "end")
    text_widget.insert("end", f"Fetching 7-day history for {city}...\n")

    # Fetch history data
    data, error = fetch_world_history(city)
    if error:
        text_widget.insert("end", f"Error: {error}")
        return

    # Extract daily dates and temperatures
    days = data["daily"]["time"]
    temps_max = data["daily"]["temperature_2m_max"]
    temps_min = data["daily"]["temperature_2m_min"]

    total_temp = 0

    # Iterate over each day and display high, low, and average temperatures
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

    # Calculate and display weekly average temperature if valid data exists
    valid_days = sum(1 for tmax, tmin in zip(temps_max, temps_min) if tmax is not None and tmin is not None)
    if valid_days > 0:
        weekly_avg = round(total_temp / valid_days, 2)
        text_widget.insert("end", f"\nWeekly Average Temperature: {weekly_avg}°C")
    else:
        text_widget.insert("end", "\nNo valid temperature data to calculate weekly average.")
