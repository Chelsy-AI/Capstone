"""
history_tracker module initializer

Provides clean imports for geocoding, weather fetching, and GUI display for historical weather data.
"""

from .geocode import get_lat_lon
from .api import fetch_world_history as fetch_historical_temperatures
from .display import insert_temperature_history_as_grid
