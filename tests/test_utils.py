import pytest
from core import utils
import customtkinter as ctk
from core.theme import LIGHT_THEME, DARK_THEME
from unittest.mock import MagicMock

def test_toggle_unit():
    """
    Test the toggle_unit function which switches between Celsius and Fahrenheit.
    
    This is a simple unit test that checks if our temperature unit switching
    function works correctly in all expected scenarios.

    """
    
    # Test switching from Celsius to Fahrenheit
    assert utils.toggle_unit("°C") == "°F", "Should switch from Celsius to Fahrenheit"
    
    # Test switching from Fahrenheit to Celsius
    assert utils.toggle_unit("°F") == "°C", "Should switch from Fahrenheit to Celsius"
    
    # Test handling of unknown/invalid input (defaults to Celsius)
    assert utils.toggle_unit("Unknown") == "°C", "Should default to Celsius for unknown input"
    

def test_kelvin_to_celsius():
    """
    Test the kelvin_to_celsius function for accurate temperature conversion.
    
    Kelvin is the scientific temperature scale where 0K = absolute zero.
    Celsius is the common temperature scale where 0°C = freezing point of water.
    
    Conversion formula: °C = K - 273.15

    """
    
    # Test the freezing point of water
    # 273.15 Kelvin should equal exactly 0 degrees Celsius
    assert utils.kelvin_to_celsius(273.15) == 0.0, "273.15K should equal 0°C (freezing point)"
    
    # Test a warmer temperature
    # 300 Kelvin should equal 26.85 degrees Celsius
    assert utils.kelvin_to_celsius(300) == round(300 - 273.15, 1), "300K should equal 26.9°C"
    
    # These tests verify that our conversion function uses the correct formula
    # and handles decimal precision appropriately

def test_kelvin_to_fahrenheit():
    """
    Test the kelvin_to_fahrenheit function for accurate temperature conversion.
    
    Fahrenheit is the temperature scale commonly used in the US.
    
    Conversion formula: °F = (K - 273.15) × 9/5 + 32

    """
    
    # Test the freezing point of water
    # 273.15 Kelvin should equal exactly 32 degrees Fahrenheit
    assert utils.kelvin_to_fahrenheit(273.15) == 32.0, "273.15K should equal 32°F (freezing point)"
    
    # Test a warmer temperature
    # 300 Kelvin should equal 80.33 degrees Fahrenheit
    expected_fahrenheit = round((300 - 273.15) * 9 / 5 + 32, 1)
    assert utils.kelvin_to_fahrenheit(300) == expected_fahrenheit, "300K should equal 80.3°F"
    
    # These tests ensure our Fahrenheit conversion is mathematically correct

def test_format_temperature():
    """
    Test the format_temperature function which creates display-ready temperature strings.
    
    This function takes a temperature value and unit, then formats them
    into a nice string for display in the user interface.

    """
    
    # Test normal temperature formatting
    assert utils.format_temperature(25, "°C") == "25 °C", "Should format temperature with unit"
    
    # Test handling of missing/None temperature data
    assert utils.format_temperature(None, "°C") == "N/A", "Should show N/A for missing data"
    
    # This test ensures our temperature display function:
    # 1. Properly formats valid temperatures
    # 2. Gracefully handles missing or invalid data
    # 3. Always returns a string suitable for display

def test_toggle_theme(monkeypatch):
    """
    Test the toggle_theme function which switches between light and dark themes.
    
    This is a more complex test because theme toggling affects multiple parts
    of the application. We use mocking to isolate the function and test its
    behavior without actually creating a real GUI.
        
    """
    
    # Create a fake application object for testing
    class DummyApp:
        """
        This class simulates a real application object with all the attributes
        and methods that toggle_theme expects to find.

        """
        def __init__(self):
            self.theme = LIGHT_THEME
            
            # Create mock objects for GUI components
            # MagicMock creates fake objects that remember how they were called
            self.parent_frame = MagicMock()  # Fake main container
            self.configure = MagicMock()     # Fake configuration method
            self.build_metrics_labels = MagicMock()  # Fake label builder
            self.update_weather = MagicMock()        # Fake weather updater
            self.show_weather_history = MagicMock()  # Fake history display

    # Create our fake application
    app = DummyApp()

    # Replace external functions with do-nothing versions
    # This prevents the test from trying to actually change GUI appearance
    monkeypatch.setattr(ctk, "set_appearance_mode", lambda mode: None)
    monkeypatch.setattr("core.gui.build_gui", lambda app: None)

    # Call the function we're testing
    utils.toggle_theme(app)

    # Verify that the theme was changed
    assert app.theme == DARK_THEME, "Theme should switch from light to dark"
    
    # Verify that the app's appearance was updated
    app.configure.assert_called_once_with(fg_color=app.theme["bg"]), \
        "App background should be updated with new theme color"
    
    # Verify that the main frame was updated
    app.parent_frame.configure.assert_called_once_with(fg_color=app.theme["bg"]), \
        "Parent frame should be updated with new theme color"
    
    # Verify that all the UI refresh methods were called
    app.build_metrics_labels.assert_called_once(), "Metric labels should be rebuilt"
    app.update_weather.assert_called_once(), "Weather display should be refreshed"
    app.show_weather_history.assert_called_once(), "History display should be refreshed"
    
    # What this test accomplishes:
    # 1. Verifies theme switching logic works correctly
    # 2. Ensures all UI components are properly updated
    # 3. Confirms the function calls all necessary refresh methods
    # 4. Tests the integration between theme system and GUI updates
    
    # Why we use mocking here:
    # - We don't want to create actual GUI windows during testing
    # - We want to verify that specific methods are called
    # - We want to isolate the theme logic from GUI implementation details
    # - We can run this test without a display/graphics system