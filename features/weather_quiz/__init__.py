"""
Weather Quiz Module - Static Questions Database Version
========================================================

This module provides a weather quiz feature using a pre-computed static questions database.
No CSV processing or real-time data analysis is performed.

Features:
- 40 pre-computed quiz questions from comprehensive weather data analysis
- Random selection of 5 questions per quiz for variety
- Multiple choice answers with detailed explanations
- Categorized questions covering different weather aspects
- Performance tracking and educational insights
- Instant quiz generation with no loading delays

Data Sources:
- Static database of pre-computed questions based on weather analysis
- Questions derived from temperature, rainfall, humidity, and wind patterns
- Historical weather patterns and seasonal variations
- Comparative analysis across different global climates

Question Categories:
- Temperature Analysis: City temperature comparisons and extremes
- Rainfall Patterns: Precipitation distribution and seasonal trends  
- Extreme Weather Events: Record temperatures, storms, and unusual conditions
- Climate Characteristics: Humidity, pressure, and atmospheric conditions
- Seasonal Variations: Monthly and seasonal weather patterns
- Weather Trends: Temperature stability and variability analysis
- Atmospheric Conditions: Wind, humidity, and pressure patterns
- Fun Weather Facts: Interesting meteorological trivia

Educational Value:
Each question teaches meteorological concepts through real-world data patterns,
helping users understand weather systems, climate differences, and
atmospheric science principles. All questions include detailed explanations
that provide context and learning opportunities.

Performance Benefits:
- Instant quiz generation - no data processing delays
- Consistent question quality and difficulty
- Reliable quiz experience with no external dependencies
- Pre-validated questions with accurate answers and explanations
- No CSV file requirements or data loading concerns
"""

from .controller import WeatherQuizController
from .quiz_generator import WeatherQuizGenerator
from .questions_database import (
    get_all_questions, 
    get_questions_by_category, 
    get_categories,
    get_question_count,
    get_random_questions,
    get_question_by_id
)

__all__ = [
    'WeatherQuizController', 
    'WeatherQuizGenerator',
    'get_all_questions',
    'get_questions_by_category', 
    'get_categories',
    'get_question_count',
    'get_random_questions',
    'get_question_by_id'
]

__version__ = "4.0.0"
__author__ = "Weather App Team"
__description__ = "Static weather quiz with pre-computed questions database"
__data_sources__ = "Static database of 40 pre-computed weather analysis questions"
__dependencies__ = "None - completely self-contained"
__capabilities__ = [
    "Static question database",
    "Random question selection", 
    "Instant quiz generation",
    "Educational insights",
    "Performance tracking",
    "Category-based filtering",
    "Question search functionality",
    "No external data dependencies",
    "Consistent quiz experience"
]