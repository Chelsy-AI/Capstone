"""
Sun and Moon Phases Module
=========================

This module provides sun and moon phase tracking functionality including:
- Real-time sun position and movement
- Moon phase calculations and visualization
- Sunrise/sunset times
- Dynamic celestial animations

"""

from .api import fetch_sun_moon_data, format_time_for_display
from .display import SunMoonDisplay
from .controller import SunMoonController

__all__ = [
    'fetch_sun_moon_data',
    'format_time_for_display', 
    'SunMoonDisplay',
    'SunMoonController'
]

__version__ = "1.0.0"
__author__ = "Weather App Team"
__description__ = "Sun and moon phases tracking with dynamic visualization"