"""
GUI Module - User Interface Components
======================================

This module contains all GUI-related components for the weather application,
organized into logical submodules for better maintainability.

Components:
- main_gui: Main GUI controller and window management
- layout_manager: Responsive layout and positioning logic
- scroll_handler: Scrolling functionality and widget positioning
- weather_display: Weather data visualization components
- animation_controller: Background animation management
"""

from .main_gui import WeatherGUI
from .layout_manager import LayoutManager
from .scroll_handler import ScrollHandler
from .weather_display import WeatherDisplay
from .animation_controller import AnimationController

__all__ = [
    'WeatherGUI',
    'LayoutManager', 
    'ScrollHandler',
    'WeatherDisplay',
    'AnimationController'
]

# Module information
__version__ = "1.0.0"
__author__ = "Weather App Team"
__description__ = "Modular GUI components for weather application"