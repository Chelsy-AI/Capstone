"""
Comprehensive Error Handler Module - Fixed Version
"""

import logging
import traceback
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from typing import Optional, Dict, Any, Callable
import sys

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ERROR LOGGING SETUP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class WeatherAppLogger:
    """Console-only logging system for the weather application"""
    
    def __init__(self):
        self.logger = logging.getLogger('WeatherApp')
        self.logger.setLevel(logging.INFO)
        
        # Only add handler if not already present
        if not self.logger.handlers:
            # Console handler for immediate feedback only
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            
            # Simple formatter for console output
            formatter = logging.Formatter('%(levelname)s: %(message)s')
            console_handler.setFormatter(formatter)
            
            # Add handler to logger
            self.logger.addHandler(console_handler)
    
    def get_logger(self):
        return self.logger

# Global logger instance
app_logger = WeatherAppLogger().get_logger()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SAFE ERROR HANDLING DECORATORS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def handle_api_errors(func):
    """Decorator to handle API-related errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"API Error in {func.__name__}: {str(e)}"
            app_logger.error(error_msg)
            
            # Return safe fallback data
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
    """Decorator to handle GUI-related errors"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = f"GUI Error in {func.__name__}: {str(e)}"
                app_logger.error(error_msg)
                
                if show_user_message:
                    try:
                        show_error_message(
                            "Display Error",
                            "There was an issue updating the display. The app will continue to work normally."
                        )
                    except:
                        pass  # If even error display fails, just continue
                
                # Don't crash the app, just log the error
                return None
        return wrapper
    return decorator

def handle_data_errors(func):
    """Decorator to handle data processing errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"Data Error in {func.__name__}: {str(e)}"
            app_logger.error(error_msg)
            
            # Return empty/safe data structure
            return {}
    return wrapper

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SAFE ERROR MESSAGES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def show_error_message(title: str, message: str, error_type: str = "error"):
    """Display user-friendly error messages in pop-up dialogs"""
    try:
        # Try to show message box if tkinter is available
        if error_type == "error":
            messagebox.showerror(title, message)
        elif error_type == "warning":
            messagebox.showwarning(title, message)
        elif error_type == "info":
            messagebox.showinfo(title, message)
        else:
            messagebox.showerror(title, message)
    except Exception:
        # If GUI error display fails, print to console
        app_logger.error(f"{title}: {message}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SAFE INITIALIZATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def initialize_error_handling():
    """Initialize the error handling system safely"""
    try:
        app_logger.info("Weather App Error Handling System Initialized")
        
        # Set up global exception handler for uncaught exceptions
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            app_logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
            
            try:
                show_error_message(
                    "Unexpected Error",
                    "An unexpected error occurred. The application will attempt to continue.",
                    "error"
                )
            except:
                # If we can't show GUI error, just print
                app_logger.error("Uncaught exception occurred but couldn't display error dialog")
        
        sys.excepthook = handle_exception
        
    except Exception as e:
        # If error handler setup fails, just print and continue
        print(f"Error handler initialization failed: {e}")

# Safe initialization
try:
    initialize_error_handling()
except Exception as e:
    print(f"Could not initialize error handling: {e}")

# Export commonly used functions
__all__ = [
    'handle_api_errors',
    'handle_gui_errors', 
    'handle_data_errors',
    'show_error_message',
    'app_logger'
]