# ────────────────────────────────────────────────────────────────────────────── 
# HISTORY TRACKER MODULE INITIALIZATION
# 
# This __init__.py file makes the history_tracker folder into a Python package.
# It defines what functions are available when someone imports this package.
# 
# ────────────────────────────────────────────────────────────────────────────── 

from .api import fetch_world_history          
from .display import insert_temperature_history_as_grid             

__all__ = [
    "fetch_world_history",              
    "insert_temperature_history_as_grid"
]

# ────────────────────────────────────────────────────────────────────────────── 
# PACKAGE INFORMATION
# ────────────────────────────────────────────────────────────────────────────── 

# Package metadata 
__version__ = "1.0.0"
__author__ = "Weather App Team"
__description__ = "Historical weather data tracking and geocoding utilities"