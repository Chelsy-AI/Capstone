import customtkinter as ctk

def get_weather_emoji(condition):
    if not condition:
        return "🌤️"
    condition_lower = condition.lower()
    if "clear" in condition_lower or "sunny" in condition_lower:
        return "☀️"
    elif "cloud" in condition_lower:
        if "partly" in condition_lower:
            return "⛅"
        else:
            return "☁️"
    elif "rain" in condition_lower:
        if "heavy" in condition_lower:
            return "🌧️"
        else:
            return "🌦️"
    elif "snow" in condition_lower:
        return "❄️"
    elif "thunder" in condition_lower or "storm" in condition_lower:
        return "⛈️"
    elif "mist" in condition_lower or "fog" in condition_lower:
        return "🌫️"
    elif "wind" in condition_lower:
        return "💨"
    else:
        return "🌤️"

def create_weather_notification(app, message, duration=3000):
    try:
        notification = ctk.CTkLabel(
            app,
            text=message,
            font=("Arial", 14, "bold"),
            text_color="#FFFFFF",
            fg_color="#4169E1",
            corner_radius=20,
            width=300,
            height=50
        )
        notification.place(relx=0.5, rely=0.1, anchor="center")
        app.after(duration, notification.destroy)
    except Exception as e:
        print(f"Notification creation error: {e}")

def validate_theme_colors(theme):
    try:
        required_keys = [
            "bg", "fg", "text_bg", "text_fg", "button_bg", "button_fg",
            "entry_bg", "entry_fg", "accent"
        ]
        defaults = {
            "bg": "#87CEEB",
            "fg": "#1A1A1A",
            "text_bg": "#F0F8FF",
            "text_fg": "#1A1A1A",
            "button_bg": "#4169E1",
            "button_fg": "#FFFFFF",
            "entry_bg": "#FFFFFF",
            "entry_fg": "#1A1A1A",
            "accent": "#6495ED"
        }
        for key in required_keys:
            if key not in theme or not theme[key]:
                theme[key] = defaults[key]
        return theme
    except Exception as e:
        print(f"Theme validation error: {e}")
        return theme
