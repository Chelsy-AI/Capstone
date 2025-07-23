"""
Enhanced Weather Quiz Module
============================

This module provides an intelligent weather quiz feature that generates
smart questions based on real weather data from the combined CSV dataset.

Features:
- 5+ carefully crafted quiz questions using real data analysis
- Multiple choice answers with detailed explanations
- Real-time data quality assessment and validation
- Advanced scoring and performance tracking
- Interactive data exploration and insights
- Comprehensive answer review with educational content

Data Sources:
- Combined weather dataset with multiple cities
- Real temperature, rainfall, humidity, and wind data
- Historical weather patterns and seasonal variations
- Comparative analysis across different climates

Question Types:
- Temperature comparisons between cities
- Rainfall and precipitation patterns
- Seasonal weather variations
- Extreme weather events analysis
- Climate characteristics identification
- Weather trend interpretation

Educational Value:
Each question teaches meteorological concepts through real-world data,
helping users understand weather patterns, climate differences, and
atmospheric science principles.

"""

from .controller import WeatherQuizController
from .quiz_generator import WeatherQuizGenerator

__all__ = [
    'WeatherQuizController', 
    'WeatherQuizGenerator'
]

__version__ = "2.0.0"
__author__ = "Weather App Team"
__description__ = "Enhanced interactive weather quiz with real data analysis"
__data_sources__ = "Combined CSV dataset with multi-city weather records"
__capabilities__ = [
    "Real data analysis",
    "Intelligent question generation", 
    "Data quality validation",
    "Educational insights",
    "Performance tracking",
    "Comparative city analysis"
]
