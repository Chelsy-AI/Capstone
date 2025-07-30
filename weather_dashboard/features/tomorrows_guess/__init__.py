"""
Tomorrow's Weather Prediction System
===================================

Intelligent weather forecasting module that analyzes current conditions to predict tomorrow's weather.

Features:
- Advanced weather prediction algorithms
- Interactive prediction display interface
- Real-time forecast updates
- User-friendly prediction visualization
- Integration with current weather data for enhanced accuracy

This module provides both the prediction logic and display components
for showing users what tomorrow's weather might look like.
"""

from .predictor import get_tomorrows_prediction
from .display import create_tomorrow_guess_frame, update_tomorrow_guess_display

__all__ = [
    "get_tomorrows_prediction",      # Main prediction function
    "create_tomorrow_guess_frame",   # Create the GUI frame for tomorrow's guess
    "update_tomorrow_guess_display"  # Update the display with new predictions
]