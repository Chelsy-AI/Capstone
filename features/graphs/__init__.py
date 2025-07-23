"""
Weather Graphs Module
====================

This module provides comprehensive weather data visualization including:
- Temperature trends and analysis
- Weather metrics tracking
- Prediction accuracy graphs
- Multi-city comparisons
- Interactive charts with hover tooltips

"""

from .controller import GraphsController
from .graph_generator import WeatherGraphGenerator
from .hover_tooltip import HoverTooltip

__all__ = [
    'GraphsController',
    'WeatherGraphGenerator', 
    'HoverTooltip'
]

__version__ = "1.0.0"
__author__ = "Weather App Team"
__description__ = "Interactive weather data visualization and analysis"
