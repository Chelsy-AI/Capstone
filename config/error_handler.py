"""
Comprehensive Error Handler Module
==================================

This module handles all errors that might occur in the weather app gracefully.
Instead of crashing when something goes wrong, the app shows helpful error messages
and continues working. It's like having a safety net for the entire application!

Key features:
- Catches API errors (when internet is down or weather service is unavailable)
- Handles GUI errors (when display updates fail)
- Manages data processing errors (when weather data is corrupted)
- Logs errors to console for debugging
- Shows user-friendly error messages
- Prevents app crashes by providing safe fallback values

Think of this as the app's "immune system" that keeps it healthy even when things go wrong!
"""

import logging      # For recording error messages
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from typing import Optional, Dict, Any, Callable
import sys


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ERROR LOGGING SETUP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class WeatherAppLogger:
    """
    Console-only logging system for the weather application.
    
    This creates a logging system that writes error messages to the console
    so developers can see what's happening when things go wrong.
    """
    
    def __init__(self):
        """Set up the logging system."""
        # Create a logger specifically for our weather app
        self.logger = logging.getLogger('WeatherApp')
        self.logger.setLevel(logging.INFO)  # Show INFO level and above
        
        # Only add a console handler if one doesn't already exist
        if not self.logger.handlers:
            # Create handler that writes to console (stdout)
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            
            # Create simple format for console output
            formatter = logging.Formatter('%(levelname)s: %(message)s')
            console_handler.setFormatter(formatter)
            
            # Add the handler to our logger
            self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """
        Get the configured logger instance.
        
        Returns:
            Logger: Configured logger for the weather app
        """
        return self.logger

# Create global logger instance that other parts of the app can use
app_logger = WeatherAppLogger().get_logger()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SAFE ERROR HANDLING DECORATORS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def handle_api_errors(func):
    """
    Decorator to handle API-related errors gracefully.
    
    This "wraps" functions that make API calls so if they fail,
    instead of crashing the app, they return safe fallback data.
    
    Args:
        func: Function that makes API calls
        
    Returns:
        Function that handles API errors safely
        
    Example:
        @handle_api_errors
        def get_weather_data(city):
            # If this fails, the decorator catches it and returns safe data
            return requests.get(f"weather-api.com/{city}").json()
    """
    def wrapper(*args, **kwargs):
        try:
            # Try to run the original function
            return func(*args, **kwargs)
        except Exception as e:
            # If it fails, log the error and return safe fallback data
            error_msg = f"API Error in {func.__name__}: {str(e)}"
            app_logger.error(error_msg)
            
            # Return safe fallback weather data so the app can continue
            return {
                "error": "Unable to fetch weather data",
                "temperature": None,
                "humidity": None,
                "wind_speed": None,
                "pressure": None,
                "description": "Service temporarily unavailable"
            }
    return wrapper


def handle_gui_errors(show_user_message=True):
    """
    Decorator to handle GUI-related errors.
    
    This protects functions that update the user interface. If updating
    the display fails, the app continues working instead of crashing.
    
    Args:
        show_user_message (bool): Whether to show error popup to user
        
    Returns:
        Decorator function
        
    Example:
        @handle_gui_errors(show_user_message=False)
        def update_temperature_display(temp):
            # If updating the display fails, just log it and continue
            temperature_label.configure(text=f"{temp}°C")
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                # Try to run the GUI update function
                return func(*args, **kwargs)
            except Exception as e:
                # If it fails, log the error
                error_msg = f"GUI Error in {func.__name__}: {str(e)}"
                app_logger.error(error_msg)
                
                # Optionally show user-friendly error message
                if show_user_message:
                    try:
                        show_error_message(
                            "Display Error",
                            "There was an issue updating the display. The app will continue to work normally."
                        )
                    except:
                        # If even the error display fails, just continue silently
                        pass
                
                # Don't crash the app, just log the error and continue
                return None
        return wrapper
    return decorator


def handle_data_errors(func):
    """
    Decorator to handle data processing errors.
    
    This protects functions that process weather data. If data processing
    fails, it returns empty data instead of crashing.
    
    Args:
        func: Function that processes data
        
    Returns:
        Function that handles data errors safely
        
    Example:
        @handle_data_errors
        def calculate_average_temperature(weather_list):
            # If calculation fails, return empty dict instead of crashing
            return sum(w['temp'] for w in weather_list) / len(weather_list)
    """
    def wrapper(*args, **kwargs):
        try:
            # Try to run the data processing function
            return func(*args, **kwargs)
        except Exception as e:
            # If it fails, log the error and return safe empty data
            error_msg = f"Data Error in {func.__name__}: {str(e)}"
            app_logger.error(error_msg)
            
            # Return empty/safe data structure
            return {}
    return wrapper


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SAFE ERROR MESSAGES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def show_error_message(title: str, message: str, error_type: str = "error"):
    """
    Display user-friendly error messages in pop-up dialogs.
    
    This shows error messages to users in a nice popup window instead
    of scary technical error messages that would confuse them.
    
    Args:
        title (str): Title for the error popup window
        message (str): User-friendly explanation of what went wrong
        error_type (str): Type of error ("error", "warning", "info")
        
    Example:
        show_error_message(
            "Internet Connection",
            "Could not connect to weather service. Please check your internet connection."
        )
    """
    try:
        # Try to show a popup message box
        if error_type == "error":
            messagebox.showerror(title, message)
        elif error_type == "warning":
            messagebox.showwarning(title, message)
        elif error_type == "info":
            messagebox.showinfo(title, message)
        else:
            # Default to error type if unknown type specified
            messagebox.showerror(title, message)
    except Exception:
        # If GUI error display fails, print to console as fallback
        app_logger.error(f"{title}: {message}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SAFE INITIALIZATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def initialize_error_handling():
    """
    Initialize the error handling system safely.
    
    This sets up the error handling system and creates a global error handler
    that catches any errors not handled elsewhere in the app.
    """
    try:
        app_logger.info("Weather App Error Handling System Initialized")
        
        # Set up global exception handler for any uncaught errors
        def handle_exception(exc_type, exc_value, exc_traceback):
            """
            Handle any uncaught exceptions in the app.
            
            This is the "last resort" error handler that catches errors
            that slip through all other error handling.
            """
            # Let KeyboardInterrupt (Ctrl+C) work normally
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            # Log the uncaught exception with full details
            app_logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
            
            # Try to show user-friendly error message
            try:
                show_error_message(
                    "Unexpected Error",
                    "An unexpected error occurred. The application will attempt to continue.",
                    "error"
                )
            except:
                # If we can't show GUI error, just print to console
                app_logger.error("Uncaught exception occurred but couldn't display error dialog")
        
        # Install our global exception handler
        sys.excepthook = handle_exception
        
    except Exception as e:
        # If error handler setup fails, just print and continue
        print(f"Error handler initialization failed: {e}")


# Initialize the error handling system when this module is imported
try:
    initialize_error_handling()
except Exception as e:
    print(f"Could not initialize error handling: {e}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXPORT COMMONLY USED FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# These are the functions that other parts of the app can import and use
__all__ = [
    'handle_api_errors',     # Decorator for API functions
    'handle_gui_errors',     # Decorator for GUI functions
    'handle_data_errors',    # Decorator for data processing functions
    'show_error_message',    # Function to show user-friendly error popups
    'app_logger'            # Logger instance for error messages
]