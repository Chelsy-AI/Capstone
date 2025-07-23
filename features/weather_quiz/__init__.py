"""
Weather Quiz Module
==================

This module provides an interactive weather quiz feature that generates
smart and fun questions based on real weather data from the CSV files.

Features:
- 5 carefully crafted quiz questions
- Multiple choice answers
- Real data analysis from weather history
- Score tracking and feedback
- Educational weather insights

"""

from .controller import WeatherQuizController
from .quiz_generator import WeatherQuizGenerator

__all__ = [
    'WeatherQuizController',
    'WeatherQuizGenerator'
]

__version__ = "1.0.0"
__author__ = "Weather App Team"
__description__ = "Interactive weather quiz with smart questions based on real data"