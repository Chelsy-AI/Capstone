"""
Comprehensive Error Handler Module
=================================

This module provides centralized error handling functionality for the Weather App.
It handles all types of errors that can occur in the application including:
- API failures and network issues
- GUI and display errors
- Data storage and file system errors
- User input validation errors
- Animation and theme errors
- Prediction and calculation errors

Key Features:
- Centralized error logging to console only
- User-friendly error messages
- Error recovery mechanisms
- Detailed error reporting for debugging
- Graceful degradation when errors occur
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
        
        # Console handler for immediate feedback only
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Simple formatter for console output
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
    
    def get_logger(self):
        return self.logger

# Global logger instance
app_logger = WeatherAppLogger().get_logger()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ERROR TYPES AND HANDLING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class WeatherAppError(Exception):
    """Base exception class for weather application errors"""
    
    def __init__(self, message: str, error_code: str = "GENERAL", details: Optional[Dict] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.now()
        super().__init__(self.message)

class APIError(WeatherAppError):
    """Errors related to API calls and external services"""
    pass

class DataError(WeatherAppError):
    """Errors related to data processing and storage"""
    pass

class GUIError(WeatherAppError):
    """Errors related to GUI components and display"""
    pass

class ValidationError(WeatherAppError):
    """Errors related to input validation"""
    pass

class AnimationError(WeatherAppError):
    """Errors related to weather animations"""
    pass

class ThemeError(WeatherAppError):
    """Errors related to theme switching and display"""
    pass

class PredictionError(WeatherAppError):
    """Errors related to weather predictions"""
    pass

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ERROR HANDLING DECORATORS
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
                    show_error_message(
                        "Display Error",
                        "There was an issue updating the display. The app will continue to work normally."
                    )
                
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
            return {} if 'dict' in str(type(func())) else []
    return wrapper

def handle_animation_errors(func):
    """Decorator to handle animation-related errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"Animation Error in {func.__name__}: {str(e)}"
            app_logger.warning(error_msg)
            
            # Animations are non-critical, just disable them silently
            return None
    return wrapper

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# USER-FRIENDLY ERROR MESSAGES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def show_error_message(title: str, message: str, error_type: str = "error"):
    """
    Display user-friendly error messages in pop-up dialogs
    
    Args:
        title: Dialog window title
        message: User-friendly error message
        error_type: Type of message (error, warning, info)
    """
    try:
        if error_type == "error":
            messagebox.showerror(title, message)
        elif error_type == "warning":
            messagebox.showwarning(title, message)
        elif error_type == "info":
            messagebox.showinfo(title, message)
        else:
            messagebox.showerror(title, message)
    except Exception:
        # Fallback to console if GUI is not available
        print(f"{title}: {message}")

def show_network_error():
    """Show network connectivity error message"""
    show_error_message(
        "Connection Error",
        "Unable to connect to weather services. Please check your internet connection and try again.",
        "error"
    )

def show_city_not_found_error(city_name: str):
    """Show city not found error message"""
    show_error_message(
        "City Not Found",
        f"Could not find weather data for '{city_name}'. Please check the spelling and try again.",
        "warning"
    )

def show_data_error():
    """Show data processing error message"""
    show_error_message(
        "Data Error",
        "There was an issue processing the weather data. Some information may not be available.",
        "warning"
    )

def show_file_error():
    """Show file system error message"""
    show_error_message(
        "File Error",
        "Unable to save or load data files. Check file permissions and available disk space.",
        "warning"
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SPECIFIC ERROR HANDLERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def handle_api_timeout():
    """Handle API timeout errors"""
    app_logger.warning("API request timed out")
    show_error_message(
        "Request Timeout",
        "The weather service is taking too long to respond. Please try again in a moment.",
        "warning"
    )

def handle_invalid_city(city_name: str):
    """Handle invalid city name errors"""
    app_logger.info(f"Invalid city name provided: {city_name}")
    show_city_not_found_error(city_name)

def handle_file_permission_error(filepath: str):
    """Handle file permission errors"""
    app_logger.error(f"Permission denied accessing file: {filepath}")
    show_error_message(
        "Permission Error",
        f"Cannot access file. Please check file permissions.",
        "error"
    )

def handle_disk_space_error():
    """Handle disk space errors"""
    app_logger.error("Insufficient disk space for data storage")
    show_error_message(
        "Disk Space Error",
        "Not enough disk space to save data. Please free up some space and try again.",
        "error"
    )

def handle_animation_failure():
    """Handle animation system failures"""
    app_logger.warning("Weather animation system failed to initialize")
    # Don't show user message for animations as they're non-critical

def handle_theme_error():
    """Handle theme switching errors"""
    app_logger.warning("Theme switching encountered an error")
    show_error_message(
        "Theme Error",
        "Unable to switch themes. The current theme will be maintained.",
        "info"
    )

def handle_prediction_error():
    """Handle weather prediction errors"""
    app_logger.warning("Weather prediction system encountered an error")
    show_error_message(
        "Prediction Error",
        "Unable to generate weather prediction. Historical data may be insufficient.",
        "info"
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RECOVERY MECHANISMS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def retry_with_backoff(func: Callable, max_retries: int = 3, base_delay: float = 1.0):
    """
    Retry a function with exponential backoff
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retry attempts
        base_delay: Base delay between retries in seconds
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            delay = base_delay * (2 ** attempt)
            app_logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {str(e)}")
            import time
            time.sleep(delay)

def safe_execute(func: Callable, fallback_value=None, log_errors: bool = True):
    """
    Safely execute a function with fallback value
    
    Args:
        func: Function to execute
        fallback_value: Value to return if function fails
        log_errors: Whether to log errors
    """
    try:
        return func()
    except Exception as e:
        if log_errors:
            app_logger.warning(f"Safe execution failed for {func.__name__}: {str(e)}")
        return fallback_value

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INPUT VALIDATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def validate_city_input(city_name: str) -> tuple[bool, str]:
    """
    Validate city name input
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not city_name:
        return False, "City name cannot be empty"
    
    city_name = city_name.strip()
    
    if len(city_name) < 2:
        return False, "City name must be at least 2 characters long"
    
    if len(city_name) > 100:
        return False, "City name is too long (maximum 100 characters)"
    
    # Check for valid characters
    import re
    if not re.match(r"^[a-zA-Z\s\-'.,()]+$", city_name):
        return False, "City name contains invalid characters"
    
    return True, ""

def validate_temperature_unit(unit: str) -> bool:
    """Validate temperature unit"""
    return unit.upper() in ['C', 'F', 'CELSIUS', 'FAHRENHEIT']

def validate_api_response(response_data: Dict) -> tuple[bool, str]:
    """
    Validate API response data
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(response_data, dict):
        return False, "Invalid response format"
    
    if 'error' in response_data:
        return False, response_data['error']
    
    required_fields = ['temperature', 'description']
    missing_fields = [field for field in required_fields if field not in response_data]
    
    if missing_fields:
        return False, f"Missing required data: {', '.join(missing_fields)}"
    
    return True, ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ERROR REPORTING AND DEBUGGING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def log_system_info():
    """Log system information for debugging"""
    import platform
    import sys
    
    app_logger.info("=== SYSTEM INFORMATION ===")
    app_logger.info(f"Platform: {platform.platform()}")
    app_logger.info(f"Python Version: {sys.version}")
    app_logger.info(f"Python Executable: {sys.executable}")
    app_logger.info("==========================")

def create_error_report(error: Exception, context: Dict[str, Any] = None) -> str:
    """
    Create detailed error report for debugging
    
    Args:
        error: The exception that occurred
        context: Additional context information
    
    Returns:
        Formatted error report string
    """
    context = context or {}
    
    report = []
    report.append("=== ERROR REPORT ===")
    report.append(f"Timestamp: {datetime.now().isoformat()}")
    report.append(f"Error Type: {type(error).__name__}")
    report.append(f"Error Message: {str(error)}")
    report.append("")
    
    # Add context information
    if context:
        report.append("Context:")
        for key, value in context.items():
            report.append(f"  {key}: {value}")
        report.append("")
    
    # Add traceback
    report.append("Traceback:")
    report.append(traceback.format_exc())
    report.append("==================")
    
    return "\n".join(report)

def handle_critical_error(error: Exception, context: Dict[str, Any] = None):
    """
    Handle critical errors that might crash the application
    
    Args:
        error: The critical exception
        context: Additional context information
    """
    error_report = create_error_report(error, context)
    app_logger.critical(error_report)
    
    # Show user message
    show_error_message(
        "Critical Error",
        "A serious error occurred. The application will attempt to continue. Please restart if issues persist.",
        "error"
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GRACEFUL DEGRADATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_fallback_weather_data(city: str = "Unknown") -> Dict[str, Any]:
    """Return fallback weather data when API fails"""
    return {
        "temperature": None,
        "humidity": "N/A",
        "wind_speed": "N/A",
        "pressure": "N/A",
        "visibility": "N/A",
        "uv_index": "N/A",
        "precipitation": "N/A",
        "description": "Weather data temporarily unavailable",
        "icon": "❓",
        "error": None,
        "city": city
    }

def get_fallback_prediction_data() -> tuple:
    """Return fallback prediction data when prediction fails"""
    return None, "N/A", "N/A"

def get_fallback_history_data() -> Dict[str, Any]:
    """Return fallback history data when history API fails"""
    return {
        "time": [],
        "temperature_2m_max": [],
        "temperature_2m_min": [],
        "temperature_2m_mean": []
    }

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INITIALIZATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def initialize_error_handling():
    """Initialize the error handling system"""
    app_logger.info("Weather App Error Handling System Initialized")
    log_system_info()
    
    # Set up global exception handler for uncaught exceptions
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        app_logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        
        show_error_message(
            "Unexpected Error",
            "An unexpected error occurred. The application will attempt to continue. Please restart if issues persist.",
            "error"
        )
    
    sys.excepthook = handle_exception

# Initialize on import
initialize_error_handling()

# Export commonly used functions
__all__ = [
    'handle_api_errors',
    'handle_gui_errors', 
    'handle_data_errors',
    'handle_animation_errors',
    'show_error_message',
    'show_network_error',
    'show_city_not_found_error',
    'validate_city_input',
    'safe_execute',
    'retry_with_backoff',
    'get_fallback_weather_data',
    'get_fallback_prediction_data',
    'get_fallback_history_data',
    'handle_critical_error',
    'app_logger'
]