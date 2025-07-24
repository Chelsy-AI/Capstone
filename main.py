"""
Main Entry Point for Weather Dashboard
======================================

This is the starting point for the weather application.
It handles:
- Checking if required libraries are installed
- Creating necessary folders
- Starting the main weather app
- Showing helpful error messages if something goes wrong

Think of this as the "power button" for your weather app!
"""

import sys
import os

# Add the main project folder to Python's search path
# This helps Python find all our weather app files
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_dependencies():
    """
    Check if all the libraries we need are installed on this computer.
    
    This is like checking if you have all the ingredients before cooking!
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
    
    missing = []  # Keep track of what's missing
    
    # Try to import each required library
    for module in required_modules:
        try:
            __import__(module)  # Try to load the library
            print(f"✓ {module} found")  # Success message
        except ImportError:
            missing.append(module)  # Add to missing list
            print(f"❌ {module} missing")  # Error message
    
    # If anything is missing, tell the user how to fix it
    if missing:
        print(f"\nMissing dependencies: {', '.join(missing)}")
        print("Please install them using: pip install requests pillow")
        return False
    
    print("✓ All dependencies found")
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
        # Create the folder (exist_ok=True means "don't error if it already exists")
        os.makedirs(data_dir, exist_ok=True)
        print(f"✓ Data directory ready: {data_dir}")
        return True
    except Exception as e:
        # If something goes wrong, show the error
        print(f"❌ Failed to create data directory: {e}")
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
        print("Starting Weather Application...")
        print("=" * 40)

        # Step 1: Make sure all required libraries are installed
        if not check_dependencies():
            print("\n❌ Cannot start app - missing dependencies")
            return False
        
        # Step 2: Make sure we have a place to save weather data
        if not create_data_directory():
            print("\n⚠️ Warning: Could not create data directory")
        
        # Step 3: Import and start the actual weather app
        print("\n🚀 Launching weather app...")
        from config.weather_app import run_app
        run_app()  # This opens the weather app window
        
        print("\n✓ Weather app closed successfully")
        return True
        
    except KeyboardInterrupt:
        # User pressed Ctrl+C to stop the app
        print("\n🛑 App interrupted by user")
        return True
        
    except ImportError as e:
        # Couldn't find some of our weather app files
        print(f"\n❌ Import error: {e}")
        print("Check if all files are in the correct location")
        return False
        
    except Exception as e:
        # Something unexpected went wrong
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()  # Show detailed error information
        return False


def main():
    """
    The very first function that runs when you start the program.
    
    This is the "main" entry point - when you double-click the file
    or run "python main.py", this function is what actually gets called.
    """
    
    print("🌤️ Weather Dashboard Starting...")
    print("================================")
    
    # Try to run the application
    success = run_weather_app()
    
    # If something went wrong, show a helpful message
    if not success:
        print("\n❌ Application failed to start properly")
        print("Please check the error messages above")
    
    # On Windows, keep the console window open so user can read any messages
    if os.name == 'nt':  # 'nt' means Windows
        input("\nPress Enter to exit...")


# This special line means "only run main() if this file is being run directly"
# (not if it's being imported by another file)
if __name__ == "__main__":
    main()