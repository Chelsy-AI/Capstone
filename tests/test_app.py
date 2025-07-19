import pytest
from config.api import get_current_weather
from config.utils import toggle_unit, kelvin_to_celsius, kelvin_to_fahrenheit, format_temperature

def test_get_current_weather(monkeypatch):
    """
    This test function checks if our get_current_weather function works correctly.
    
    We use 'monkeypatch' to replace real API calls with fake ones so we can:
    1. Test without making actual internet requests
    2. Control exactly what data our function receives
    3. Make tests run faster and more reliably
    
    """
    
    # Create a mock (fake) response that simulates what a real weather API would return
    class MockResponse:
        """
        This class pretends to be a real HTTP response from a weather API.
        We create it to simulate the structure and data that our function expects.

        """
        
        def raise_for_status(self): 
            """
            Real HTTP responses have this method to check for errors.
            Our mock version does nothing (assumes success).

            """
            pass
        
        def json(self):
            """
            This method returns fake weather data in the same format 
            that a real weather API would provide.

            """
            return {
                "main": {                    # Main weather measurements
                    "temp": 22.5,           # Temperature in Celsius
                    "humidity": 60,         # Humidity percentage
                    "pressure": 1012        # Atmospheric pressure
                },
                "wind": {                   # Wind information
                    "speed": 5.0           # Wind speed
                },
                "weather": [{              # Weather conditions (can be multiple)
                    "icon": "01d",         # Weather icon code
                    "description": "Clear sky"  # Human-readable description
                }]
            }

    def mock_get_basic(*args, **kwargs):
        """
        This function replaces the real get_basic_weather_from_weatherdb function.
        
        Instead of making a real API call, it returns our fake data.
        
        """
        return (MockResponse().json(), None)  

    def mock_get_detailed(*args, **kwargs):
        """
        This function replaces the real get_detailed_environmental_data function.
        
        Returns fake environmental data like UV index, pollen, and bug levels.
        
        """
        return {
            "uv": 5,           # UV index level
            "pollen": "low",   # Pollen count description
            "bugs": "medium"   # Bug activity level
        }

    monkeypatch.setattr("config.api.get_basic_weather_from_weatherdb", mock_get_basic)
    monkeypatch.setattr("config.api.get_detailed_environmental_data", mock_get_detailed)

    result = get_current_weather("New York")
    
    assert isinstance(result, dict), "Result should be a dictionary"
    
    assert result["temperature"] == 22.5, "Temperature should match our mock data"
    assert result["humidity"] == 60, "Humidity should match our mock data"
    
    assert result["icon"] == "01d" or result["icon"], "Icon should be present and not empty"

def test_toggle_unit():
    """
    Test the toggle_unit function which switches between Celsius and Fahrenheit.
    
    This is a simple unit test that checks if our temperature unit switching
    function works correctly in all expected scenarios.

    """
    
    # Test switching from Celsius to Fahrenheit
    assert toggle_unit("°C") == "°F", "Should switch from Celsius to Fahrenheit"
    
    # Test switching from Fahrenheit to Celsius
    assert toggle_unit("°F") == "°C", "Should switch from Fahrenheit to Celsius"
    
    # Test handling of unknown/invalid input (defaults to Celsius)
    assert toggle_unit("Unknown") == "°C", "Should default to Celsius for unknown input"

def test_kelvin_to_celsius():
    """
    Test the kelvin_to_celsius function for accurate temperature conversion.
    
    Kelvin is the scientific temperature scale where 0K = absolute zero.
    Celsius is the common temperature scale where 0°C = freezing point of water.
    
    Conversion formula: °C = K - 273.15

    """
    
    # Test the freezing point of water
    # 273.15 Kelvin should equal exactly 0 degrees Celsius
    assert kelvin_to_celsius(273.15) == 0.0, "273.15K should equal 0°C (freezing point)"
    
    # Test a warmer temperature
    # 300 Kelvin should equal 26.85 degrees Celsius
    assert kelvin_to_celsius(300) == round(300 - 273.15, 1), "300K should equal 26.9°C"

def test_kelvin_to_fahrenheit():
    """
    Test the kelvin_to_fahrenheit function for accurate temperature conversion.
    
    Fahrenheit is the temperature scale commonly used in the US.
    
    Conversion formula: °F = (K - 273.15) × 9/5 + 32

    """
    
    # Test the freezing point of water
    # 273.15 Kelvin should equal exactly 32 degrees Fahrenheit
    assert kelvin_to_fahrenheit(273.15) == 32.0, "273.15K should equal 32°F (freezing point)"
    
    # Test a warmer temperature
    # 300 Kelvin should equal 80.33 degrees Fahrenheit
    expected_fahrenheit = round((300 - 273.15) * 9 / 5 + 32, 1)
    assert kelvin_to_fahrenheit(300) == expected_fahrenheit, "300K should equal 80.3°F"

def test_format_temperature():
    """
    Test the format_temperature function which creates display-ready temperature strings.
    
    This function takes a temperature value and unit, then formats them
    into a nice string for display in the user interface.

    """
    
    # Test normal temperature formatting
    assert format_temperature(25, "°C") == "25 °C", "Should format temperature with unit"
    
    # Test handling of missing/None temperature data
    assert format_temperature(None, "°C") == "N/A", "Should show N/A for missing data"