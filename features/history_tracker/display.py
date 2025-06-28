from customtkinter import CTkLabel, CTkFrame
from .api import fetch_world_history as fetch_historical_temperatures
from core.theme import LIGHT_THEME  # fallback

def insert_temperature_history_as_grid(frame, city="New York"):
    # Clear existing widgets safely
    if frame.winfo_exists():
        for widget in frame.winfo_children():
            widget.destroy()

    # Fetch data
    data, error = fetch_historical_temperatures(city)
    if error:
        print("History fetch error:", error)
        return

    days = data["daily"]["time"]
    temps_max = data["daily"]["temperature_2m_max"]
    temps_min = data["daily"]["temperature_2m_min"]

    avg_temps = []
    for tmax, tmin in zip(temps_max, temps_min):
        if tmax is not None and tmin is not None:
            avg_temps.append(round((tmax + tmin) / 2, 1))
        else:
            avg_temps.append(None)

    # Get theme from frame or fallback
    theme = getattr(frame.master, "theme", LIGHT_THEME)

    headings = ["📅 Date", "🔺 High", "🔻 Low", "🌡️ Avg"]
    data_rows = [days, temps_max, temps_min, avg_temps]

    # Create header row
    for col, heading in enumerate([""] + days):
        text_color = theme["text_fg"]
        bg_color = theme["text_bg"]

        label_text = heading if col > 0 else "🔤"
        CTkLabel(
            frame,
            text=label_text,
            font=("Arial", 12, "bold"),
            text_color=text_color,
            fg_color=bg_color
        ).grid(row=0, column=col, padx=5, pady=3, sticky="nsew")

    # Create value rows
    for row_index, (label, values) in enumerate(zip(headings[1:], data_rows[1:]), start=1):
        # First column: label (e.g. 🔺 High)
        CTkLabel(
            frame,
            text=label,
            font=("Arial", 12, "bold"),
            text_color=theme["text_fg"],
            fg_color=theme["text_bg"]
        ).grid(row=row_index, column=0, padx=5, pady=3, sticky="w")

        # Then values
        for col_index, val in enumerate(values):
            val_text = f"{val}°C" if val is not None else "N/A"
            CTkLabel(
                frame,
                text=val_text,
                font=("Arial", 12),
                text_color=theme["text_fg"],
                fg_color=theme["text_bg"]
            ).grid(row=row_index, column=col_index + 1, padx=5, pady=3)
