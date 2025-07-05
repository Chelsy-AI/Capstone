import os
import json

PREF_FILE = os.path.expanduser("~/.weather_app_theme_pref.json")

# ──────────────────────────────────────────────────────────────────────────────
# Saves the user's theme preference (light or dark) to a JSON file.
# ──────────────────────────────────────────────────────────────────────────────
def save_user_theme_preference(theme_name):
    """
    Save theme preference string ('light' or 'dark') to a JSON file.
    """
    try:
        with open(PREF_FILE, "w") as f:
            json.dump({"theme": theme_name}, f)
    except Exception as e:
        pass
    
# ──────────────────────────────────────────────────────────────────────────────
# Loads the user's saved theme preference from the JSON file.
# ──────────────────────────────────────────────────────────────────────────────
def load_user_theme_preference():
    """
    Load and return saved theme preference string ('light' or 'dark').
    Returns None if file doesn't exist or on error.
    """
    try:
        if os.path.isfile(PREF_FILE):
            with open(PREF_FILE, "r") as f:
                data = json.load(f)
                return data.get("theme")
    except Exception as e:
        pass
    return None
