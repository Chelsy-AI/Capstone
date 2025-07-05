from features.history_tracker.api import fetch_world_history

def get_tomorrows_prediction(city):
    """
    Fetch recent historical data and return predicted temp, confidence, and dummy accuracy.
    Used by GUI.
    Returns: (predicted_temp: float|None, confidence_str: str, accuracy_int: int)
    """
    if not isinstance(city, str):
        return None, "0%", 85

    raw_data = fetch_world_history(city)
    if not raw_data or 'time' not in raw_data:
        return None, "0%", 85

    times = raw_data.get("time", [])
    max_temps = raw_data.get("temperature_2m_max", [])
    min_temps = raw_data.get("temperature_2m_min", [])
    mean_temps = raw_data.get("temperature_2m_mean", [])

    days = []
    for i in range(len(times)):
        avg_temp = mean_temps[i] if i < len(mean_temps) else None
        if avg_temp is None:
            continue
        days.append({
            "date": times[i],
            "max": max_temps[i] if i < len(max_temps) else None,
            "min": min_temps[i] if i < len(min_temps) else None,
            "avg": avg_temp
        })

    if len(days) < 3:
        return None, "0%", 85

    last_three = days[-3:]
    avg_temps = [d['avg'] for d in last_three if isinstance(d['avg'], (int, float))]

    if len(avg_temps) < 3:
        return None, "0%", 85

    predicted_temp = round(sum(avg_temps) / len(avg_temps), 1)
    confidence = min(100, 30 + len(avg_temps) * 20)
    accuracy = 85

    return predicted_temp, f"{confidence}%", accuracy
