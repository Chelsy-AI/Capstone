"""
Sun and Moon Phases Module
=========================

This module provides sun and moon phase tracking functionality including:
- Real-time sun position and movement
- Moon phase calculations and visualization
- Sunrise/sunset times
- Dynamic celestial animations
- Multi-language support (English, Hindi, Spanish)

Key Features:
- Accurate astronomical calculations
- Visual sky display with celestial object positioning
- Golden hour timing for photography
- Automatic data caching and refresh
- Responsive design that adapts to window size
- Support for any city worldwide

Usage:
    from features.sun_moon_phases import SunMoonController, fetch_sun_moon_data
    
    # Create controller for main app
    controller = SunMoonController(app, gui_controller)
    
    # Or fetch data directly
    data = fetch_sun_moon_data("London")
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

__version__ = "1.1.0"
__author__ = "Weather App Team"
__description__ = "Sun and moon phases tracking with dynamic visualization and multi-language support"
