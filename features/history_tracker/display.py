import customtkinter as ctk
from .api import fetch_world_history

def insert_temperature_history_as_grid(parent, city):
    print(f"[DEBUG] City: {city}")
    data = fetch_world_history(city)
    print(f"[DEBUG] Raw data: {data}")

    if not data or "time" not in data:
        print(f"History fetch error (no time): {data}")
        label = ctk.CTkLabel(parent, text="No historical weather data found.", text_color="red")
        label.grid(row=0, column=0, padx=10, pady=10)
        return

    # Filter valid days only (skip if any temp is None)
    valid_days = []
    for i in range(len(data["time"])):
        max_temp = data["temperature_2m_max"][i]
        min_temp = data["temperature_2m_min"][i]
        avg_temp = data["temperature_2m_mean"][i]
        if None not in (max_temp, min_temp, avg_temp):
            valid_days.append({
                "date": data["time"][i],
                "max": max_temp,
                "min": min_temp,
                "avg": avg_temp,
            })

    if not valid_days:
        label = ctk.CTkLabel(parent, text="No valid temperature data available.", text_color="orange")
        label.grid(row=0, column=0, padx=10, pady=10)
        return

    # Row 0: Dates with calendar emoji
    for col, day in enumerate(valid_days):
        label = ctk.CTkLabel(parent, text=f"📅 {day['date']}", font=ctk.CTkFont(weight="bold"))
        label.grid(row=0, column=col, padx=8, pady=4)

    # Row 1: Max temperature with red up arrow
    for col, day in enumerate(valid_days):
        label = ctk.CTkLabel(parent, text=f"🔺 {day['max']}°C")
        label.grid(row=1, column=col, padx=8, pady=4)

    # Row 2: Min temperature with blue down arrow
    for col, day in enumerate(valid_days):
        label = ctk.CTkLabel(parent, text=f"🔻 {day['min']}°C")
        label.grid(row=2, column=col, padx=8, pady=4)

    # Row 3: Avg temperature with thermometer emoji
    for col, day in enumerate(valid_days):
        label = ctk.CTkLabel(parent, text=f"🌡️ {day['avg']}°C")
        label.grid(row=3, column=col, padx=8, pady=4)
