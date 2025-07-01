from datetime import datetime, timedelta
import customtkinter as ctk
from .api import fetch_world_history

def insert_temperature_history_as_grid(parent, city):
    """
    Fetch 7-day weather history for the city and insert into parent frame
    as a grid with four rows: Date, Max, Min, Avg temperatures.
    Show exactly 7 days, filling missing data with 'N/A'.
    If no data, display a clear "No historical weather data found." message.
    """
    if not isinstance(city, str):
        print(f"[ERROR] fetch_world_history called with invalid city argument (not str): {city}")
        city = "New York"  # fallback default

    data = fetch_world_history(city)

    # Clear any previous widgets in the parent frame
    for widget in parent.winfo_children():
        widget.destroy()

    # Check if data is missing or empty
    if not data or "time" not in data or not data["time"]:
        label = ctk.CTkLabel(
            parent,
            text="No historical weather data found.",
            text_color="red",
            font=("Arial", 16, "bold")
        )
        label.grid(row=0, column=0, padx=10, pady=10)
        return

    days_count = 7  # Number of days to show

    times = data.get("time", [])
    max_temps = data.get("temperature_2m_max", [])
    min_temps = data.get("temperature_2m_min", [])
    avg_temps = data.get("temperature_2m_mean", [])

    # Helper to get value or "N/A"
    def get_value_or_na(lst, index):
        if index < len(lst):
            val = lst[index]
            return val if val is not None else "N/A"
        else:
            return "N/A"

    for col in range(days_count):
        # Get date or N/A if missing
        date_str = get_value_or_na(times, col)
        max_temp = get_value_or_na(max_temps, col)
        min_temp = get_value_or_na(min_temps, col)
        avg_temp = get_value_or_na(avg_temps, col)

        # Row 0: Dates
        date_label = ctk.CTkLabel(parent, text=f"📅 {date_str}", font=("Arial", 14, "bold"))
        date_label.grid(row=0, column=col, padx=8, pady=4)

        # Row 1: Max temps with dot
        max_label = ctk.CTkLabel(parent, text=f"🔺  {max_temp}.")
        max_label.grid(row=1, column=col, padx=8, pady=4)

        # Row 2: Min temps with dot
        min_label = ctk.CTkLabel(parent, text=f"🔻  {min_temp}.")
        min_label.grid(row=2, column=col, padx=8, pady=4)

        # Row 3: Avg temps with dot
        avg_label = ctk.CTkLabel(parent, text=f"🌡️  {avg_temp}.")
        avg_label.grid(row=3, column=col, padx=8, pady=4)
