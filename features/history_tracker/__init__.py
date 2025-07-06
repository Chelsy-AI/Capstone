# ────────────────────────────────────────────────────────────────────────────── 
# HISTORY TRACKER MODULE INITIALIZATION
# 
# This __init__.py file makes the history_tracker folder into a Python package.
# It defines what functions are available when someone imports this package.
# 
# ────────────────────────────────────────────────────────────────────────────── 

from .api import fetch_world_history          
from .geocode import get_lat_lon             

__all__ = [
    "fetch_world_history",              
    "insert_temperature_history_as_grid", 
    "get_lat_lon",                      
]

# ────────────────────────────────────────────────────────────────────────────── 
# PACKAGE INFORMATION
# ────────────────────────────────────────────────────────────────────────────── 

# Package metadata 
__version__ = "1.0.0"
__author__ = "Weather App Team"
__description__ = "Historical weather data tracking and geocoding utilities"

# ────────────────────────────────────────────────────────────────────────────── 
# INITIALIZATION CODE 
# ────────────────────────────────────────────────────────────────────────────── 

# You can add initialization code here that runs when the package is imported
# For example, setting up logging or configuration

def _initialize_package():
    """
    Initialize the history tracker package.
    This function runs when the package is first imported.
    """
