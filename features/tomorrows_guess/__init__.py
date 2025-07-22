# This file makes Python treat the folder as a package and controls what gets imported

from .predictor import get_tomorrows_prediction
from .display import create_tomorrow_guess_frame, update_tomorrow_guess_display

__all__ = [
    "get_tomorrows_prediction",      # Main prediction function
    "create_tomorrow_guess_frame",   # Create the GUI frame for tomorrow's guess
    "update_tomorrow_guess_display"  # Update the display with new predictions
]