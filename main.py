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
        
        return True
        
    except ImportError:
        return False
    except Exception as e:
        return False

def check_dependencies():
    """
    Check if all the libraries we need are installed on this computer.
    We need certain Python libraries to make the weather app work.
    
    Returns:
        bool: True if everything is installed, False if something is missing
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
    
    missing = []  # Keep track of what's missing
    missing_optional = []  # Keep track of missing optional modules
    
    # Try to import each required library
    for module in required_modules:
        try:
            __import__(module)  # Try to load the library
        except ImportError:
            missing.append(module)  # Add to missing list
    
    # Check optional modules
    for module in optional_modules:
        try:
            __import__(module)
        except ImportError:
            missing_optional.append(module)
    
    # If core modules are missing
    if missing:
        return False
    
    # Show info about optional modules
    if missing_optional:
        return False
    
    return True


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
        return True
    except Exception as e:
        # If something goes wrong, show the error
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

        # Step 1: Make sure all required libraries are installed
        if not check_dependencies():
            return False
        
        # Step 2: Configure matplotlib to prevent font warnings
        configure_matplotlib()
        
        # Step 3: Make sure we have a place to save weather data
        if not create_data_directory():
            print("\n⚠️ Warning: Could not create data directory")
        
        # Step 4: Import and start the actual weather app
        from config.weather_app import run_app
        run_app()  # This opens the weather app window
        
        return True
        
    except KeyboardInterrupt:
        # User pressed Ctrl+C to stop the app
        return True
        
    except ImportError as e:
        # Couldn't find some of our weather app files
        return False
        
    except Exception as e:
        # Something unexpected went wrong
        import traceback
        traceback.print_exc()  # Show detailed error information
        return False


def main():
    """
    The very first function that runs when you start the program.
    
    This is the "main" entry point - when you double-click the file
    or run "python main.py", this function is what actually gets called.
    """
        
    # Try to run the application
    success = run_weather_app()
    
    # If something went wrong, show a helpful message
    if not success:
        print("\n❌ Application failed to start properly")
    
    # On Windows, keep the console window open so user can read any messages
    if os.name == 'nt':  # 'nt' means Windows
        input("\nPress Enter to exit...")


# This special line means "only run main() if this file is being run directly"
if __name__ == "__main__":
    main()