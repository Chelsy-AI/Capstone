import pytest
from core.api import get_current_weather

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

    monkeypatch.setattr("core.api.get_basic_weather_from_weatherdb", mock_get_basic)
    monkeypatch.setattr("core.api.get_detailed_environmental_data", mock_get_detailed)

    result = get_current_weather("New York")
    
    assert isinstance(result, dict), "Result should be a dictionary"
    
    assert result["temperature"] == 22.5, "Temperature should match our mock data"
    assert result["humidity"] == 60, "Humidity should match our mock data"
    
    assert result["icon"] == "☀️" or result["icon"], "Icon should be present and not empty"
    
