from datetime import datetime, timedelta
import customtkinter as ctk
from .api import fetch_world_history
from features.history_tracker.api import fetch_world_history
import threading



def insert_temperature_history_as_grid(parent, city, unit="C"):
    """
    Fetch 7-day weather history for the city and insert into parent frame
    as a grid with four rows: Date, Max, Min, Avg temperatures.
    Shows exactly 7 days, filling missing data with 'N/A'.
    Appends °C or °F to each temperature based on selected unit.
    """
    if not isinstance(city, str):
        city = "New York"  # fallback default

    data = fetch_world_history(city)

    # Clear previous widgets in the parent frame
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

    def get_value_or_na(lst, index):
        if index < len(lst):
            val = lst[index]
            return val if val is not None else "N/A"
        else:
            return "N/A"

    def format_temp(temp, unit):
        if temp == "N/A":
            return temp
        try:
            temp = float(temp)
            if unit == "F":
                temp = temp * 9 / 5 + 32
            return f"{round(temp, 1)}°{unit}"
        except Exception:
            return "N/A"

    for col in range(days_count):
        # Get date or N/A if missing
        date_str = get_value_or_na(times, col)
        max_temp = format_temp(get_value_or_na(max_temps, col), unit)
        min_temp = format_temp(get_value_or_na(min_temps, col), unit)
        avg_temp = format_temp(get_value_or_na(avg_temps, col), unit)

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

def show_weather_history(parent_widget, city="New York", unit="C"):
    history_frame = ctk.CTkFrame(parent_widget)
    history_frame.pack(fill="x", pady=(10, 0), padx=10)

    label = ctk.CTkLabel(history_frame, text="7-Day History", font=ctk.CTkFont(size=16, weight="bold"))
    label.pack(anchor="w", padx=5, pady=(5, 0))

    text_widget = ctk.CTkTextbox(history_frame, width=400, height=160, corner_radius=8, wrap="none")
    text_widget.pack(fill="both", expand=True, padx=5, pady=5)

    # Show loading message
    text_widget.insert("end", "Loading history...\n")
    text_widget.configure(state="disabled")

    def load_history():
        data = fetch_world_history(city)

        text_widget.configure(state="normal")
        text_widget.delete("1.0", "end")  # Clear loading message

        if not data:
            text_widget.insert("end", "No historical weather data found.\n")
        else:
            unit_symbol = "°F" if unit.upper() == "F" else "°C"
            text_widget.insert("end", f"Date        | High  | Low   | Average ({unit_symbol})\n")
            text_widget.insert("end", "------------|-------|-------|----------------\n")

            for entry in data:
                high = f"{entry['high']}{unit_symbol}"
                low = f"{entry['low']}{unit_symbol}"
                avg = f"{entry['average']}{unit_symbol}"

                line = f"{entry['date']} | {high:>5} | {low:>5} | {avg:>6}\n"
                text_widget.insert("end", line)

        text_widget.configure(state="disabled")

    threading.Thread(target=load_history, daemon=True).start()
