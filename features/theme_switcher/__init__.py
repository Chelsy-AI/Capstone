"""
Theme Switcher Module

This module provides comprehensive theme management functionality for the weather application.
It handles switching between light and dark themes, persisting user preferences, and
applying theme changes across the entire application interface.

"""

from .theme_manager import (
    toggle_theme,
    set_day_mode,
    set_night_mode,
    get_user_preference,
    apply_theme,
    get_current_theme,
    is_dark_mode,
    reset_theme_to_default
)

from .user_preferences import (
    save_user_theme_preference,
    load_user_theme_preference,
    clear_user_preferences,
    get_preference_file_path
)

# Public API - These functions are available when importing the module
__all__ = [
    # Core theme management functions
    "toggle_theme",
    "set_day_mode", 
    "set_night_mode",
    "apply_theme",
    "get_user_preference",
    "get_current_theme",
    "is_dark_mode",
    "reset_theme_to_default",
    
    # User preference management functions
    "save_user_theme_preference",
    "load_user_theme_preference",
    "clear_user_preferences",
    "get_preference_file_path",
]

# Module version for tracking changes
__version__ = "1.0.0"

# Default theme configuration
DEFAULT_THEME = "system"  # Follow system theme by default
