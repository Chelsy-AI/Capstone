from core.gui import build_gui
import customtkinter as ctk
from core.theme import LIGHT_THEME

def test_build_gui_creates_widgets():
    """
    This test checks if our build_gui function successfully creates GUI widgets.
    
    GUI testing is tricky because we're testing visual components, but we can
    verify that the function creates the expected widgets without actually
    displaying them on screen.
    
    What this test does:
    1. Creates a mock application window with all required attributes
    2. Calls our build_gui function
    3. Verifies that widgets were actually created
    """
    
    app = ctk.CTk()
    
    # Set up all the attributes that build_gui expects to find on the app object
    # These simulate the state that would exist in a real running application
    
    # Theme configuration - controls colors, fonts, and visual styling
    app.theme = LIGHT_THEME
    
    # String variable to hold the current city name
    # StringVar is a special tkinter variable that can notify widgets when it changes
    app.city_var = ctk.StringVar(value="New York")
    
    # Dictionary to store references to metric display labels
    # This allows other parts of the app to update weather data displays
    app.metric_value_labels = {}
    
    # Mock function for switching between light and dark themes
    # lambda: None creates a function that does nothing (placeholder)
    app.toggle_theme = lambda: None
    
    # Mock function for updating the weather history display
    # In a real app, this would refresh historical weather data
    app.update_weather_history = lambda: None
    
    # Current temperature unit setting ("C" for Celsius, "F" for Fahrenheit)
    app.temp_unit = "C"
    
    # Mock function for switching between Celsius and Fahrenheit
    # event=None allows it to be called with or without an event parameter
    app.toggle_temp_unit = lambda event=None: None
    
    # Now call the function we're testing
    # This should create and arrange all the GUI widgets
    build_gui(app)
    
    # Test verification: Check that widgets were actually created
    # winfo_children() returns a list of all child widgets in the app window
    assert len(app.winfo_children()) > 0, "build_gui should create at least one widget"
    
    # What this assertion checks:
    # - If the list is empty, build_gui didn't create any widgets (test fails)
    # - If the list has items, build_gui successfully created widgets (test passes)
    
    # Why this test is important:
    # 1. Ensures build_gui doesn't crash when called
    # 2. Verifies that widgets are actually being created
    # 3. Catches basic integration issues between GUI components
    # 4. Provides a foundation for more detailed GUI testing
    
    # Limitations of this test:
    # - Doesn't verify the specific widgets created
    # - Doesn't test widget positioning or styling
    # - Doesn't test widget functionality or event handling
    # - These could be added in more advanced tests