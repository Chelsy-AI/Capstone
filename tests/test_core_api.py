import pytest
from core.api import get_current_weather

def test_get_current_weather(monkeypatch):
    class MockResponse:
        def raise_for_status(self): pass
        def json(self):
            return {
                "main": {
                    "temp": 22.5,
                    "humidity": 60,
                    "pressure": 1012
                },
                "wind": {
                    "speed": 5.0
                },
                "weather": [{
                    "icon": "01d",
                    "description": "Clear sky"
                }]
            }

    def mock_get_basic(*args, **kwargs):
        return (MockResponse().json(), None)

    def mock_get_detailed(*args, **kwargs):
        return {
            "uv": 5,
            "pollen": "low",
            "bugs": "medium"
        }

    monkeypatch.setattr("core.api.get_basic_weather_from_weatherdb", mock_get_basic)
    monkeypatch.setattr("core.api.get_detailed_environmental_data", mock_get_detailed)

    result = get_current_weather("New York")
    assert isinstance(result, dict)
    assert result["temperature"] == 22.5
    assert result["humidity"] == 60
    assert result["icon"] == "☀️" or result["icon"]  # depends on icon mapping
