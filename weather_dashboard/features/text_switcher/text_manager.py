"""
Theme Manager Module

This module handles all theme-related operations for the weather application.
It provides a clean interface for switching between light and dark themes,
managing user preferences, and applying consistent theming across the entire app.

The theme manager is optimized for performance and includes beginner-friendly
comments to help understand how theming systems work in GUI applications.
"""

import logging
from typing import Optional, Dict, Any, Callable, Union
import customtkinter as ctk
from config.themes import LIGHT_THEME, DARK_THEME

# Configure logging for theme operations
logger = logging.getLogger(__name__)

# THEME CONSTANTS AND CONFIGURATION

# Theme name constants for easy reference throughout the code
THEME_LIGHT = "light"
THEME_DARK = "dark"
THEME_SYSTEM = "system"  # Follow the operating system's theme preference

# Set of all valid theme options for validation
VALID_THEMES = {THEME_LIGHT, THEME_DARK, THEME_SYSTEM}

# Performance optimization: cache the last applied theme to avoid unnecessary changes
_current_theme_cache: Optional[str] = None
_theme_change_callbacks: list = []  # Functions to call when theme changes


# MAIN THEME SWITCHING FUNCTIONS

def toggle_text(app) -> str:
    """
    Toggle between light and dark themes.
    
    This is the main function users call when they want to switch themes.
    It automatically determines the current theme and switches to the opposite one.
    
    Args:
        app: The main application object that contains theme information
        
    Returns:
        str: Name of the newly applied theme ("light" or "dark")
    """
    try:
        # Validate that the app object has the required theme attribute
        if not hasattr(app, 'theme'):
            logger.error("App object missing 'theme' attribute")
            raise AttributeError("App object must have 'theme' attribute")
        
        # Determine current theme and switch to the opposite
        if app.theme == LIGHT_THEME:
            logger.info("Toggling from light to dark theme")
            return set_night_mode(app)
        else:
            logger.info("Toggling from dark to light theme")
            return set_day_mode(app)
            
    except Exception as e:
        logger.error(f"Error toggling theme: {e}")
        # Fallback to light mode if something goes wrong
        return set_day_mode(app)


def set_day_mode(app) -> str:
    """
    Apply light theme (day mode) to the application.
    
    Args:
        app: The main application object to apply theming to
        
    Returns:
        str: "light" to confirm the theme was applied
    """
    try:
        logger.info("Applying light theme (day mode)")
        
        # Check if we're already in light mode to avoid unnecessary work
        if _current_theme_cache == THEME_LIGHT:
            logger.info("Already in light mode, skipping theme change")
            return THEME_LIGHT
        
        # Set the theme data in the app object
        app.theme = LIGHT_THEME
        
        # Apply CustomTkinter appearance mode
        ctk.set_appearance_mode("light")
        
        # Update the visual appearance of app components
        _apply_theme_colors_efficiently(app, LIGHT_THEME)
        
        # Notify other parts of the app about the theme change
        _trigger_theme_callbacks(app, THEME_LIGHT)
        
        # Update cache to improve performance for future checks
        _current_theme_cache = THEME_LIGHT
        
        logger.info("Light theme applied successfully")
        return THEME_LIGHT
        
    except Exception as e:
        logger.error(f"Error applying light theme: {e}")
        raise


def set_night_mode(app) -> str:
    """
    Apply dark theme (night mode) to the application.
    
    
    Args:
        app: The main application object to apply theming to
        
    Returns:
        str: "dark" to confirm the theme was applied
    """
    try:
        logger.info("Applying dark theme (night mode)")
        
        # Performance optimization: skip if already in dark mode
        if _current_theme_cache == THEME_DARK:
            logger.info("Already in dark mode, skipping theme change")
            return THEME_DARK
        
        # Set the theme data in the app object
        app.theme = DARK_THEME
        
        # Apply CustomTkinter dark appearance mode
        ctk.set_appearance_mode("dark")
        
        # Update visual appearance with dark theme colors
        _apply_theme_colors_efficiently(app, DARK_THEME)
        
        # Notify other components about the theme change
        _trigger_theme_callbacks(app, THEME_DARK)
        
        # Update performance cache
        _current_theme_cache = THEME_DARK
        
        logger.info("Dark theme applied successfully")
        return THEME_DARK
        
    except Exception as e:
        logger.error(f"Error applying dark theme: {e}")
        raise


def apply_theme(app, theme: str) -> str:
    """
    Apply any specified theme to the application.
    
    This is a unified function that can apply light, dark, or system theme.
    It handles theme validation and routes to the appropriate specific function.
    
    Args:
        app: The main application object
        theme: Theme name ("light", "dark", or "system")
        
    Returns:
        str: Name of the actually applied theme
    """
    # Input validation - ensure we have a valid theme name
    if theme not in VALID_THEMES:
        logger.warning(f"Invalid theme '{theme}', falling back to light mode")
        theme = THEME_LIGHT
    
    try:
        # Handle system theme detection
        if theme == THEME_SYSTEM:
            detected_theme = _detect_system_theme()
            logger.info(f"System theme detected: {detected_theme}")
            theme = detected_theme
        
        # Apply the appropriate theme using the specific functions
        if theme == THEME_DARK:
            return set_night_mode(app)
        else:
            return set_day_mode(app)
            
    except Exception as e:
        logger.error(f"Error applying theme '{theme}': {e}")
        # Always fallback to light theme if there's an error
        return set_day_mode(app)

def get_current_theme(app) -> Optional[str]:
    """
    Get the currently applied theme name.
    
    Args:
        app: The main application object
        
    Returns:
        str or None: Current theme name ("light", "dark") or None if unknown
    """
    try:
        # Check the cached value first for better performance
        if _current_theme_cache:
            return _current_theme_cache
        
        # Fallback to checking the app object directly
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
    Check if the application is currently using dark theme.
    
    Args:
        app: The main application object
        
    Returns:
        bool: True if in dark mode, False otherwise
    """
    try:
        return get_current_theme(app) == THEME_DARK
    except Exception:
        # If we can't determine the theme, assume light mode (safer default)
        return False


def reset_theme_to_default(app) -> str:
    """
    Reset the application theme to the default (light mode).
    
    Args:
        app: The main application object
        
    Returns:
        str: "light" to confirm reset to default theme
    """
    try:
        logger.info("Resetting theme to default (light mode)")
        return set_day_mode(app)
    except Exception as e:
        logger.error(f"Error resetting theme: {e}")
        return THEME_LIGHT


# INTERNAL HELPER FUNCTIONS (OPTIMIZED FOR PERFORMANCE)

def _apply_theme_colors_efficiently(app, theme_config: Dict[str, Any]) -> None:
    """
    Apply theme colors to application components efficiently.
    
    This internal function updates the visual appearance of the application
    based on the selected theme. It's optimized to only update components
    that actually exist and need updating.
    
    Args:
        app: The main application object
        theme_config: Dictionary containing theme color information
    """
    try:
        # Get the background color from theme configuration
        bg_color = theme_config.get("bg", "#FFFFFF")
        
        # List of app components that might need theme updates
        components_to_update = [
            ("configure", lambda: app.configure(fg_color=bg_color)),
            ("parent_frame", lambda: app.parent_frame.configure(fg_color=bg_color)),
            ("main_frame", lambda: app.main_frame.configure(fg_color=bg_color))
        ]
        
        # Apply theme to each component that exists
        for component_name, update_function in components_to_update:
            try:
                # Check if component exists before trying to update it
                if hasattr(app, component_name) or component_name == "configure":
                    update_function()
                    logger.debug(f"Updated {component_name} with theme colors")
            except Exception as e:
                # Don't let one component failure stop the whole theming process
                logger.debug(f"Skipped {component_name}: {e}")
                continue
            
    except Exception as e:
        logger.error(f"Error applying theme colors: {e}")
        raise


def _trigger_theme_callbacks(app, theme_name: str) -> None:
    """
    Notify other parts of the application about theme changes.
    
    Args:
        app: The main application object
        theme_name: Name of the newly applied theme
    """
    try:
        # Call the app's built-in theme change callback if it exists
        if hasattr(app, 'on_theme_changed') and callable(app.on_theme_changed):
            app.on_theme_changed(theme_name)
            logger.debug(f"Called app theme callback for: {theme_name}")
        
        # Call any registered external callbacks
        for callback_function in _theme_change_callbacks:
            try:
                callback_function(theme_name)
                logger.debug(f"Called external theme callback for: {theme_name}")
            except Exception as e:
                logger.warning(f"Theme callback failed: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Error triggering theme callbacks: {e}")


def _detect_system_theme() -> str:
    """
    Detect the operating system's current theme preference.
    
    Returns:
        str: "light" or "dark" based on system theme, defaults to "light"
    """
    try:
        # Use CustomTkinter's built-in system theme detection
        appearance = ctk.get_appearance_mode()
        
        # Convert CustomTkinter's result to our theme constants
        if appearance.lower() == "dark":
            logger.info("System theme detected: dark")
            return THEME_DARK
        else:
            logger.info("System theme detected: light")
            return THEME_LIGHT
            
    except Exception as e:
        logger.error(f"Error detecting system theme: {e}")
        # Safe fallback to light theme if detection fails
        return THEME_LIGHT


# ADVANCED THEME MANAGEMENT FEATURES

def register_theme_callback(callback_function: Callable[[str], None]) -> None:
    """
    Register a function to be called when the theme changes.
    
    This allows different parts of the application to automatically update
    their appearance when the user switches themes.
    
    Args:
        callback_function: Function that takes theme name as parameter
    """
    if callback_function not in _theme_change_callbacks:
        _theme_change_callbacks.append(callback_function)
        logger.info(f"Registered theme callback: {callback_function.__name__}")


def unregister_theme_callback(callback_function: Callable[[str], None]) -> None:
    """
    Remove a previously registered theme callback function.
    
    Args:
        callback_function: The function to remove from callbacks
    """
    if callback_function in _theme_change_callbacks:
        _theme_change_callbacks.remove(callback_function)
        logger.info(f"Unregistered theme callback: {callback_function.__name__}")


def validate_theme_config(theme_config: Dict[str, Any]) -> bool:
    """
    Validate that a theme configuration dictionary is properly formatted.
    
    Args:
        theme_config: Dictionary containing theme configuration
        
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    try:
        # Define required properties that every theme must have
        required_keys = ["bg"]  # Background color is essential
        
        # Check that all required keys are present
        has_required_keys = all(key in theme_config for key in required_keys)
        
        if not has_required_keys:
            logger.warning("Theme config missing required keys")
            return False
        
        # Validate that background color is a valid color string
        bg_color = theme_config.get("bg")
        if not isinstance(bg_color, str) or len(bg_color) < 3:
            logger.warning("Invalid background color in theme config")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating theme config: {e}")
        return False


def _validate_app_for_theming(app) -> bool:
    """
    Validate that the app object is ready for theming operations.
    
    This internal function checks if the app has the necessary attributes
    and methods for theme management to work properly.
    
    Args:
        app: The application object to validate
        
    Returns:
        bool: True if app is ready for theming, False otherwise
    """
    try:
        # Check for required attributes that theme management needs
        required_attributes = ['configure']  # At minimum, need configure method
        
        # Verify all required attributes exist
        for attribute_name in required_attributes:
            if not hasattr(app, attribute_name):
                logger.error(f"App missing required attribute: {attribute_name}")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating app for theming: {e}")
        return False


def get_theme_info(theme_name: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific theme.
    
    Args:
        theme_name: Name of the theme to get info for
        
    Returns:
        Dictionary containing theme information        
    """
    try:
        if theme_name == THEME_LIGHT:
            return {
                "name": "Light Theme",
                "description": "Bright theme suitable for daytime use",
                "config": LIGHT_THEME,
                "suitable_for": ["daytime", "bright_environments", "battery_saving"]
            }
        elif theme_name == THEME_DARK:
            return {
                "name": "Dark Theme", 
                "description": "Dark theme suitable for nighttime use",
                "config": DARK_THEME,
                "suitable_for": ["nighttime", "low_light", "reduced_eye_strain"]
            }
        else:
            return {
                "name": "Unknown Theme",
                "description": "Theme information not available",
                "config": {},
                "suitable_for": []
            }
            
    except Exception as e:
        logger.error(f"Error getting theme info for {theme_name}: {e}")
        return {"error": str(e)}


def clear_theme_cache() -> None:
    """Clear the theme performance cache."""
    global _current_theme_cache
    _current_theme_cache = None
    logger.info("Theme cache cleared")
