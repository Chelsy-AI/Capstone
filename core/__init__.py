"""
Weather App Core Module Initialization
=====================================

This module serves as the entry point for the Weather App application.
It provides a simple interface to start the application by importing
the main WeatherApp class and run_app function.

"""

from .app import WeatherApp, run_app

# Entry point function to launch the weather app
def run_app():
    """
    Main entry point function to start the Weather App
    
    This function creates an instance of the WeatherApp class
    and starts the GUI main loop to display the application window.
        
    """
    # Create a new instance of the WeatherApp
    app = WeatherApp()
    
    # Start the GUI main loop (this keeps the window open and responsive)
    app.mainloop()
    