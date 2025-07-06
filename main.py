import os
import sys
from core import run_app

# === PATH SETUP SECTION ===
# This section ensures Python can find all our project files no matter 
# where the script is run from

project_root = os.path.dirname(os.path.abspath(__file__))

# Add our project root directory to Python's module search path
# sys.path is a list of directories where Python looks for modules to import
# insert(0, ...) adds our directory to the beginning of the list (highest priority)
# This ensures Python can find our 'core', 'features', and other custom modules
sys.path.insert(0, project_root)

# === APPLICATION ENTRY POINT ===
# This is the standard Python idiom for creating an executable script

if __name__ == "__main__":
    """
    This special condition only runs when this file is executed directly,
    not when it's imported as a module by another Python file.
    
    What this means:
    - If you run: python main.py → this code executes
    - If you run: import main → this code does NOT execute
    
    This is important because:
    1. It makes the file both importable and executable
    2. It prevents the app from starting accidentally during imports
    3. It's a Python best practice for main entry points
    """
    
    # Start our weather application
    # This calls the main function that sets up the GUI and starts the app
    run_app()

# === WHAT THIS FILE DOES ===
# This file serves as the "front door" to our weather application:
#
# 1. IMPORT MANAGEMENT: Sets up the Python path so all our modules can be found
# 2. ENTRY POINT: Provides a clean way to start the application
# 3. ORGANIZATION: Keeps the startup logic separate from the main application code
#
# When someone wants to run our weather app, they simply run:
# python main.py
#
# And this file handles all the setup and launches the application.

# === WHY WE NEED THE PATH SETUP ===
# Without the sys.path.insert() line, Python might not be able to find our
# custom modules like 'core', 'features', etc. This could happen if:
# - The script is run from a different directory
# - The project structure is nested
# - The Python environment doesn't include our project directory
#
# By explicitly adding our project root to sys.path, we ensure our imports
# work reliably regardless of where the script is executed from.

# === ALTERNATIVE APPROACHES ===
# Other ways to handle this include:
# - Using setup.py to install the package
# - Setting PYTHONPATH environment variable
# - Using relative imports throughout the project
# - Using a package manager like pip with editable installs
#
# The approach here is simple and works well for standalone applications.