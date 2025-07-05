import pytest
from core import utils
import customtkinter as ctk
from core.theme import LIGHT_THEME, DARK_THEME
from unittest.mock import MagicMock

def test_toggle_unit():
    assert utils.toggle_unit("°C") == "°F"
    assert utils.toggle_unit("°F") == "°C"
    assert utils.toggle_unit("Unknown") == "°C"  # optional

def test_kelvin_to_celsius():
    assert utils.kelvin_to_celsius(273.15) == 0.0
    assert utils.kelvin_to_celsius(300) == round(300 - 273.15, 1)

def test_kelvin_to_fahrenheit():
    assert utils.kelvin_to_fahrenheit(273.15) == 32.0
    assert utils.kelvin_to_fahrenheit(300) == round((300 - 273.15) * 9 / 5 + 32, 1)

def test_format_temperature():
    assert utils.format_temperature(25, "°C") == "25 °C"
    assert utils.format_temperature(None, "°C") == "N/A"

def test_toggle_theme(monkeypatch):
    class DummyApp:
        def __init__(self):
            self.theme = LIGHT_THEME
            self.parent_frame = MagicMock()
            self.configure = MagicMock()
            self.build_metrics_labels = MagicMock()
            self.update_weather = MagicMock()
            self.show_weather_history = MagicMock()

    app = DummyApp()

    monkeypatch.setattr(ctk, "set_appearance_mode", lambda mode: None)
    monkeypatch.setattr("core.gui.build_gui", lambda app: None)

    utils.toggle_theme(app)

    assert app.theme == DARK_THEME
    app.configure.assert_called_once_with(fg_color=app.theme["bg"])
    app.parent_frame.configure.assert_called_once_with(fg_color=app.theme["bg"])
    app.build_metrics_labels.assert_called_once()
    app.update_weather.assert_called_once()
    app.show_weather_history.assert_called_once()
