"""
Main Entry Point for Weather Dashboard
======================================

This is the starting point for the weather application.
It handles:
- Checking if required libraries are installed
- Creating necessary folders
- Starting the main weather app
- Showing helpful error messages if something goes wrong
- Configuring matplotlib to suppress font warnings
- Comprehensive error handling and recovery
"""

import sys
import os
import warnings

# Suppress matplotlib warnings BEFORE any other imports
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
warnings.filterwarnings('ignore', message='.*Glyph.*missing from font.*')
warnings.filterwarnings('ignore', message='.*Matplotlib currently does not support.*')
warnings.filterwarnings('ignore', message='.*DejaVu Sans.*')

# This helps Python find all our weather app files
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import the comprehensive error handling system
error_handling_available = False
try:
    from weather_dashboard.config.error_handler import (
        handle_file_system_errors,
        handle_library_errors,
        app_logger,
        safe_function_call,
        safe_show_error_message
    )
    error_handling_available = True
    app_logger.log_error("startup", "Comprehensive error handling system loaded successfully", severity="INFO")
except ImportError as e:
    pass
    
    # Create basic fallback functions
    def safe_function_call(func, *args, fallback_result=None, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return fallback_result
        
    # Create dummy decorators
    def handle_library_errors(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    
    def handle_file_system_errors(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

@handle_library_errors(fallback_implementation=None, version_check=False)
def configure_matplotlib():
    """
    Configure matplotlib to avoid font warnings and work better with our GUI.
    
    This function sets up matplotlib with safe font settings before the
    weather app starts, preventing those annoying font warning messages.
    """
    try:
        import matplotlib
        
        # Use non-interactive backend first
        matplotlib.use('Agg')
        
        # Configure safe font settings
        matplotlib.rcParams.update({
            'font.family': ['DejaVu Sans', 'Arial', 'Liberation Sans', 'sans-serif'],
            'font.size': 10,
            'axes.unicode_minus': False,  # Fix minus sign rendering
            'figure.autolayout': True,    # Automatic layout adjustment
            'text.usetex': False,         # Don't use LaTeX for text rendering
            'mathtext.default': 'regular', # Use regular fonts for math text
        })
        
        # Switch to GUI backend for our weather app
        matplotlib.use('TkAgg')
        
        if error_handling_available:
            app_logger.log_error("startup", "Matplotlib configured successfully", severity="INFO")
        
        return True
        
    except ImportError:
        if error_handling_available:
            app_logger.log_error("startup", "Matplotlib not available - graphs will be disabled", severity="WARNING")
        return False
    except Exception as e:
        if error_handling_available:
            app_logger.log_error("startup", f"Matplotlib configuration failed: {e}", e, severity="WARNING")
        return False


def check_dependencies():
    """
    Check if all the libraries we need are installed on this computer.
    We need certain Python libraries to make the weather app work.
    
    Returns:
        tuple: (success, missing_required, missing_optional)
    """
    # List of Python libraries our weather app needs to work
    required_modules = [
        'tkinter',   # For creating windows and buttons (comes with Python)
        'requests',  # For getting weather data from the internet
        'PIL',       # For handling weather icons and images
    ]
    
    # Optional modules for enhanced features
    optional_modules = [
        'matplotlib',  # For creating weather graphs
        'numpy',      # For numerical calculations in graphs
        'pandas',     # For data processing in graphs
    ]
    
    missing_required = []  # Keep track of what's missing
    missing_optional = []  # Keep track of missing optional modules
    
    # Try to import each required library
    for module in required_modules:
        try:
            __import__(module)  # Try to load the library
            if error_handling_available:
                app_logger.log_error("startup", f"Required module '{module}' found", severity="DEBUG")
        except ImportError:
            missing_required.append(module)  # Add to missing list
            if error_handling_available:
                app_logger.log_error("startup", f"Required module '{module}' missing", severity="ERROR")
    
    # Check optional modules
    for module in optional_modules:
        try:
            __import__(module)
            if error_handling_available:
                app_logger.log_error("startup", f"Optional module '{module}' found", severity="DEBUG")
        except ImportError:
            missing_optional.append(module)
            if error_handling_available:
                app_logger.log_error("startup", f"Optional module '{module}' missing", severity="WARNING")
    
    # Show results
    if missing_required:
        error_msg = f"Missing required modules: {', '.join(missing_required)}"
        if error_handling_available:
            app_logger.log_error("startup", error_msg, severity="ERROR")
                
        return False, missing_required, missing_optional
    
    if missing_optional:
        warning_msg = f"Missing optional modules: {', '.join(missing_optional)} (reduced functionality)"
        if error_handling_available:
            app_logger.log_error("startup", warning_msg, severity="WARNING")
    
    return True, [], missing_optional


@handle_file_system_errors(create_backup=False, auto_create_dirs=True)
def create_data_directory():
    """
    Make sure we have a 'data' folder to save weather history.
    
    The app saves weather information to CSV files so you can see
    historical weather data. This function creates the folder where
    those files will be stored.
    
    Returns:
        bool: True if folder was created successfully, False otherwise
    """
    # Path to the data folder (inside our main project folder)
    data_dir = os.path.join(project_root, 'data')
    
    try:
        # Create the folder
        os.makedirs(data_dir, exist_ok=True)
        
        if error_handling_available:
            app_logger.log_error("startup", f"Data directory ready: {data_dir}", severity="INFO")
        
        return True
    except Exception as e:
        # If something goes wrong, show the error
        error_msg = f"Could not create data directory: {e}"
        if error_handling_available:
            app_logger.log_error("startup", error_msg, e, severity="ERROR")
        return False


def run_weather_app():
    """
    Actually start the weather application.
    
    This function does all the setup checks and then launches
    the main weather app window. It's wrapped in error handling
    so if something goes wrong, we can show a helpful message.
    
    Returns:
        bool: True if app ran successfully, False if there was an error
    """
    try:        
        if error_handling_available:
            app_logger.log_error("startup", "Starting weather application", severity="INFO")

        # Step 1: Make sure all required libraries are installed
        deps_ok, missing_req, missing_opt = check_dependencies()
        
        if not deps_ok:
            error_msg = f"Cannot start: missing required dependencies: {missing_req}"
            if error_handling_available:
                app_logger.log_error("startup", error_msg, severity="CRITICAL")
            safe_show_error_message("Missing Dependencies", 
                                   f"Required modules not found: {', '.join(missing_req)}\n\n"
                                   "Please install missing dependencies and try again.")
            return False
        
        
        # Step 2: Configure matplotlib to prevent font warnings
        matplotlib_ok = safe_function_call(configure_matplotlib, fallback_result=False)
        
        # Step 3: Make sure we have a place to save weather data
        data_dir_ok = safe_function_call(create_data_directory, fallback_result=False)
        if not data_dir_ok:
            if error_handling_available:
                app_logger.log_error("startup", "Data directory creation failed", severity="WARNING")
        
        # Step 4: Try to import and start the actual weather app
        try:
            if error_handling_available:
                app_logger.log_error("startup", "Attempting to load main weather app module", severity="INFO")
            
            from weather_dashboard.config.weather_app import run_app
            
            if error_handling_available:
                app_logger.log_error("startup", "Main weather app module loaded successfully", severity="INFO")
            
            run_app()  # This opens the weather app window
            return True
            
        except ImportError as e:
            # Main weather app module not found - this shouldn't happen now
            error_msg = f"Main weather app module not found: {e}"
            if error_handling_available:
                app_logger.log_error("startup", error_msg, e, severity="ERROR")
            
            safe_show_error_message("Import Error", 
                                   f"Could not import weather app module.\n\n"
                                   f"Error: {str(e)}")
            return False
            
        except Exception as e:
            # Main weather app module found but failed to start
            error_msg = f"Main weather app failed to start: {e}"
            if error_handling_available:
                app_logger.log_error("startup", error_msg, e, severity="ERROR")
            
            import traceback
            traceback.print_exc()
            
            safe_show_error_message("Application Error", 
                                   f"Weather app failed to start.\n\n"
                                   f"Error: {str(e)}")
            return False
        
    except KeyboardInterrupt:
        # User pressed Ctrl+C to stop the app
        if error_handling_available:
            app_logger.log_error("startup", "Application stopped by user", severity="INFO")
        return True
        
    except Exception as e:
        # Something unexpected went wrong
        error_msg = f"Unexpected error during startup: {e}"
        if error_handling_available:
            app_logger.log_error("startup", error_msg, e, severity="CRITICAL")
        else:
            import traceback
            traceback.print_exc()  # Show detailed error information
        
        safe_show_error_message("Critical Error", 
                               f"A critical error occurred during startup.\n\n"
                               f"Error: {str(e)}")
        return False


def main():
    """
    The very first function that runs when you start the program.
    
    This is the "main" entry point - when you double-click the file
    or run "python main.py", this function is what actually gets called.
    """
    
    if error_handling_available:
        app_logger.log_error("main", "Weather Dashboard starting with comprehensive error handling", severity="INFO")
        
    # Try to run the application
    success = safe_function_call(run_weather_app, fallback_result=False)
    
    # Show final status
    if success:
        if error_handling_available:
            app_logger.log_error("main", "Weather Dashboard completed successfully", severity="INFO")
    else:
        if error_handling_available:
            app_logger.log_error("main", "Weather Dashboard failed to start properly", severity="ERROR")
    
    # On Windows, keep the console window open so user can read any messages
    if os.name == 'nt':  # 'nt' means Windows
        input("\nPress Enter to exit...")


# This special line means "only run main() if this file is being run directly"
if __name__ == "__main__":
    main()