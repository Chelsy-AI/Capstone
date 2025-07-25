"""
Enhanced Weather Quiz Module
============================

This module provides an intelligent weather quiz feature that uses
pre-computed questions based on real weather data analysis.

Features:
- 30+ pre-computed quiz questions from comprehensive weather data analysis
- Random selection of 5 questions per quiz for variety
- Multiple choice answers with detailed explanations
- Categorized questions covering different weather aspects
- Performance tracking and educational insights
- Consistent quiz experience without data processing delays

Data Sources:
- Pre-analyzed weather dataset with multiple cities
- Questions based on temperature, rainfall, humidity, and wind data
- Historical weather patterns and seasonal variations
- Comparative analysis across different climates

Question Categories:
- Temperature Analysis: City temperature comparisons and extremes
- Rainfall Patterns: Precipitation distribution and seasonal trends  
- Extreme Weather Events: Record temperatures, storms, and unusual conditions
- Climate Characteristics: Humidity, pressure, and atmospheric conditions
- Seasonal Variations: Monthly and seasonal weather patterns
- Weather Trends: Temperature stability and variability analysis
- Atmospheric Conditions: Wind, humidity, and pressure patterns

Educational Value:
Each question teaches meteorological concepts through real-world data,
helping users understand weather patterns, climate differences, and
atmospheric science principles. All questions include detailed explanations
that provide context and learning opportunities.

Performance Benefits:
- No CSV loading delays - instant quiz generation
- Consistent question quality and difficulty
- Reliable quiz experience regardless of data file availability
- Pre-validated questions with accurate answers and explanations
"""

from .controller import WeatherQuizController
from .quiz_generator import WeatherQuizGenerator
from .questions_database import (
    get_all_questions, 
    get_questions_by_category, 
    get_categories,
    get_question_count
)

__all__ = [
    'WeatherQuizController', 
    'WeatherQuizGenerator',
    'get_all_questions',
    'get_questions_by_category', 
    'get_categories',
    'get_question_count'
]

__version__ = "3.0.0"
__author__ = "Weather App Team"
__description__ = "Enhanced weather quiz with static question database"
__data_sources__ = "Pre-computed questions from comprehensive weather data analysis"
__capabilities__ = [
    "Static question database",
    "Random question selection", 
    "Instant quiz generation",
    "Educational insights",
    "Performance tracking",
    "Category-based filtering",
    "Question search functionality"
]