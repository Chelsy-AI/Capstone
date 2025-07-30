"""
Weather Graphs Module
====================================

This module provides comprehensive weather data visualization including:
- Temperature trends and analysis
- Weather metrics tracking
- Prediction accuracy graphs
- Multi-city comparisons
- Interactive charts with working hover tooltips
- Enhanced error handling and font management
"""

import warnings

# Suppress matplotlib warnings before importing components
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
warnings.filterwarnings('ignore', message='.*Glyph.*missing from font.*')
warnings.filterwarnings('ignore', message='.*Matplotlib currently does not support.*')
warnings.filterwarnings('ignore', message='.*DejaVu Sans.*')

from .controller import GraphsController
from .graph_generator import WeatherGraphGenerator

__all__ = [
    'GraphsController',
    'WeatherGraphGenerator'
]

__version__ = "1.2.0"
__author__ = "Weather App Team"
__description__ = "Interactive weather data visualization with enhanced error handling and font management"
