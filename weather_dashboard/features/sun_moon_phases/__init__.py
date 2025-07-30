"""
Sun and Moon Phases Module
=========================

This module provides sun and moon phase tracking functionality including:
- Real-time sun position and movement
- Moon phase calculations and visualization
- Sunrise/sunset times
- Dynamic celestial animations

Key Features:
- Accurate astronomical calculations
- Visual sky display with celestial object positioning
- Golden hour timing for photography
- Automatic data caching and refresh
- Responsive design that adapts to window size
- Support for any city worldwide
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
