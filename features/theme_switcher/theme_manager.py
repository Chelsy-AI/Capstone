"""
Theme Manager Module

Handles all theme-related operations for the weather application including:
- Theme switching between light and dark modes
- Theme application to UI components
- Theme state management
- Integration with user preferences

This module provides a clean interface for theme management while ensuring
consistent theming across the entire application.
"""

import logging
from typing import Optional, Dict, Any, Callable
import customtkinter as ctk
from core.theme import LIGHT_THEME, DARK_THEME
from .user_preferences import load_user_theme_preference, save_user_theme_preference

# Configure logging for theme operations
logger = logging.getLogger(__name__)

# Theme constants for easy reference
THEME_LIGHT = "light"
THEME_DARK = "dark"
THEME_SYSTEM = "system"

# Valid theme options
VALID_THEMES = {THEME_LIGHT, THEME_DARK, THEME_SYSTEM}


def toggle_theme(app) -> str:
    """
    Toggle between light and dark themes.
    
    Switches the application theme from light to dark or vice versa.
    Automatically saves the new theme preference.
    
    """
    try:
        # Validate app object has required attributes
        if not hasattr(app, 'theme'):
            raise AttributeError("App object must have 'theme' attribute")
        
        # Determine current theme and switch to opposite
        if app.theme == LIGHT_THEME:
            return set_night_mode(app)
        else:
            return set_day_mode(app)
            
    except Exception as e:
        logger.error(f"Error toggling theme: {e}")
        # Fallback to light mode if error occurs
        return set_day_mode(app)


def set_day_mode(app) -> str:
    """
    Apply light theme (day mode) to the application.
    
    Sets the application to use light theme colors and appearance.
    Updates CustomTkinter appearance mode and saves user preference.
    
    """
    try:
        logger.info("Applying light theme (day mode)")
        
        # Set theme data
        app.theme = LIGHT_THEME
        
        # Apply CustomTkinter appearance mode
        ctk.set_appearance_mode("light")
        
        # Update main application colors
        _apply_theme_colors(app, LIGHT_THEME)
        
        # Save user preference
        save_user_theme_preference(THEME_LIGHT)
        
        # Trigger theme change callback if available
        _trigger_theme_callback(app, THEME_LIGHT)
        
        logger.info("Light theme applied successfully")
        return THEME_LIGHT
        
    except Exception as e:
        logger.error(f"Error applying light theme: {e}")
        raise


def set_night_mode(app) -> str:
    """
    Apply dark theme (night mode) to the application.
    
    Sets the application to use dark theme colors and appearance.
    Updates CustomTkinter appearance mode and saves user preference.
    
    """
    try:
        logger.info("Applying dark theme (night mode)")
        
        # Set theme data
        app.theme = DARK_THEME
        
        # Apply CustomTkinter appearance mode
        ctk.set_appearance_mode("dark")
        
        # Update main application colors
        _apply_theme_colors(app, DARK_THEME)
        
        # Save user preference
        save_user_theme_preference(THEME_DARK)
        
        # Trigger theme change callback if available
        _trigger_theme_callback(app, THEME_DARK)
        
        logger.info("Dark theme applied successfully")
        return THEME_DARK
        
    except Exception as e:
        logger.error(f"Error applying dark theme: {e}")
        raise


def apply_theme(app, theme: str) -> str:
    """
    Apply the specified theme to the application.
    
    A unified function to apply any theme (light, dark, or system) to the application.
    Handles theme validation and applies the appropriate theme mode.
    
    """
    # Validate theme input
    if theme not in VALID_THEMES:
        logger.warning(f"Invalid theme '{theme}', falling back to light mode")
        theme = THEME_LIGHT
    
    try:
        # Handle system theme
        if theme == THEME_SYSTEM:
            system_theme = _detect_system_theme()
            logger.info(f"System theme detected: {system_theme}")
            theme = system_theme
        
        # Apply the appropriate theme
        if theme == THEME_DARK:
            return set_night_mode(app)
        else:
            return set_day_mode(app)
            
    except Exception as e:
        logger.error(f"Error applying theme '{theme}': {e}")
        # Fallback to light theme
        return set_day_mode(app)


def get_user_preference() -> Optional[str]:
    """
    Get the user's saved theme preference.
    
    Retrieves the theme preference from persistent storage.
    
    """
    try:
        preference = load_user_theme_preference()
        logger.info(f"Loaded user theme preference: {preference}")
        return preference
    except Exception as e:
        logger.error(f"Error loading user theme preference: {e}")
        return None


def get_current_theme(app) -> Optional[str]:
    """
    Get the currently applied theme.
    
    """
    try:
        if hasattr(app, 'theme'):
            if app.theme == LIGHT_THEME:
                return THEME_LIGHT
            elif app.theme == DARK_THEME:
                return THEME_DARK
        return None
    except Exception as e:
        logger.error(f"Error getting current theme: {e}")
        return None


def is_dark_mode(app) -> bool:
    """
    Check if the application is currently in dark mode.
    
    """
    try:
        return get_current_theme(app) == THEME_DARK
    except Exception:
        return False


def reset_theme_to_default(app) -> str:
    """
    Reset the application theme to default (light mode).
    
    Useful for error recovery or initialization scenarios.
    
    """
    try:
        logger.info("Resetting theme to default (light mode)")
        return set_day_mode(app)
    except Exception as e:
        logger.error(f"Error resetting theme: {e}")
        return THEME_LIGHT


def _apply_theme_colors(app, theme_config: Dict[str, Any]) -> None:
    """
    Apply theme colors to application components.
    
    Internal function to update the visual appearance of the application
    based on the selected theme configuration.
    
    """
    try:
        # Apply colors to main application window
        if hasattr(app, 'configure'):
            app.configure(fg_color=theme_config.get("bg", "#FFFFFF"))
        
        # Apply colors to parent frame if it exists
        if hasattr(app, 'parent_frame') and app.parent_frame:
            app.parent_frame.configure(fg_color=theme_config.get("bg", "#FFFFFF"))
        
        # Apply colors to other UI components if they exist
        if hasattr(app, 'main_frame') and app.main_frame:
            app.main_frame.configure(fg_color=theme_config.get("bg", "#FFFFFF"))
            
    except Exception as e:
        logger.error(f"Error applying theme colors: {e}")
        raise


def _trigger_theme_callback(app, theme_name: str) -> None:
    """
    Trigger theme change callback if available.
    
    Calls the theme change callback function if the app has one defined.
    This allows other parts of the application to respond to theme changes.
    
    """
    try:
        if hasattr(app, 'on_theme_changed') and callable(app.on_theme_changed):
            app.on_theme_changed(theme_name)
            logger.info(f"Theme change callback triggered for: {theme_name}")
    except Exception as e:
        logger.error(f"Error triggering theme callback: {e}")


def _detect_system_theme() -> str:
    """
    Detect the system's current theme preference.
    
    Attempts to determine if the system is using light or dark theme.
    Falls back to light theme if detection fails.
    
    """
    try:
        # For now, use CustomTkinter's detection
        # This could be enhanced with OS-specific detection
        appearance = ctk.get_appearance_mode()
        
        if appearance.lower() == "dark":
            return THEME_DARK
        else:
            return THEME_LIGHT
            
    except Exception as e:
        logger.error(f"Error detecting system theme: {e}")
        return THEME_LIGHT  # Safe fallback


def validate_theme_config(theme_config: Dict[str, Any]) -> bool:
    """
    Validate that a theme configuration is properly formatted.
    
    """
    try:
        required_keys = ["bg"]  # Add other required keys as needed
        return all(key in theme_config for key in required_keys)
    except Exception:
        return False


# Theme configuration validation
def _validate_app_for_theming(app) -> bool:
    """
    Validate that the app object is ready for theming.
    
    """
    try:
        # Check for required attributes
        required_attrs = ['configure']
        return all(hasattr(app, attr) for attr in required_attrs)
    except Exception:
        return False