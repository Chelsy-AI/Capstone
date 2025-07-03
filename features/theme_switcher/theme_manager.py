import customtkinter as ctk
from core.theme import LIGHT_THEME, DARK_THEME
from .user_preferences import load_user_theme_preference, save_user_theme_preference

# ──────────────────────────────────────────────────────────────────────────────
# Toggles the app theme between light and dark modes, applying colors accordingly.
# Also updates user preferences.
# ──────────────────────────────────────────────────────────────────────────────
def toggle_theme(app):
    """
    Switches between LIGHT_THEME and DARK_THEME and updates the app appearance.
    Saves the user's theme preference.
    """
    if app.theme == LIGHT_THEME:
        set_night_mode(app)
    else:
        set_day_mode(app)

# ──────────────────────────────────────────────────────────────────────────────
# Applies the light theme (day mode) colors and appearance to the app.
# ──────────────────────────────────────────────────────────────────────────────
def set_day_mode(app):
    """
    Set the app theme to LIGHT_THEME and update appearance.
    """
    app.theme = LIGHT_THEME
    ctk.set_appearance_mode("light")
    app.configure(fg_color=app.theme["bg"])
    app.parent_frame.configure(fg_color=app.theme["bg"])
    save_user_theme_preference("light")

# ──────────────────────────────────────────────────────────────────────────────
# Applies the dark theme (night mode) colors and appearance to the app.
# ──────────────────────────────────────────────────────────────────────────────
def set_night_mode(app):
    """
    Set the app theme to DARK_THEME and update appearance.
    """
    app.theme = DARK_THEME
    ctk.set_appearance_mode("dark")
    app.configure(fg_color=app.theme["bg"])
    app.parent_frame.configure(fg_color=app.theme["bg"])
    save_user_theme_preference("dark")

# ──────────────────────────────────────────────────────────────────────────────
# Retrieves the user's saved theme preference from storage (if any).
# ──────────────────────────────────────────────────────────────────────────────
def get_user_preference():
    """
    Load and return saved user theme preference ('light' or 'dark').
    Returns None if no preference saved.
    """
    return load_user_theme_preference()

def apply_theme(app, theme):
    """
    Apply the selected theme to the app (light or dark) during initialization.
    """
    if theme == "dark":
        set_night_mode(app)
    else:
        set_day_mode(app)
