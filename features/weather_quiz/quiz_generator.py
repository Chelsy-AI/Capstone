"""
Enhanced Weather Quiz Generator - Creates smart questions ONLY based on combined CSV data
Modified to generate exactly 5 questions instead of 8

This module analyzes real weather data from a CSV file and generates intelligent quiz questions.
It's designed to be educational and help users learn about weather patterns through data analysis.
"""

import pandas as pd
import random
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple


class WeatherQuizGenerator:
    """
    Generates intelligent weather quiz questions based EXCLUSIVELY on real CSV data analysis.
    
    This class loads weather data from a CSV file and creates educational quiz questions
    that help users understand weather patterns, temperature variations, and climate differences.
    All questions are based on actual data analysis rather than theoretical knowledge.
    """
    
    def __init__(self):
        """
        Initialize the quiz generator.
        
        Sets up the generator and attempts to load weather data from the CSV file.
        If data loading fails, the generator will still work but won't be able to create questions.
        """
        # Initialize data storage variables
        self.weather_data: Optional[pd.DataFrame] = None  # Main data storage
        self.cities: List[str] = []  # List of available cities
        self.data_loaded: bool = False  # Flag to track if data loaded successfully
        
        # Cache for expensive calculations to improve performance
        self._calculation_cache: Dict[str, Any] = {}
        
        # Load the weather data from CSV file
        self._load_combined_data()
    
    def _load_combined_data(self):
        """
        Load weather data from the combined CSV file.
        
        This method looks for a 'combined.csv' file in the project's data directory
        and loads it into a pandas DataFrame for analysis.
        """
        try:
            # Find the CSV file relative to this script's location
            # This works regardless of where the script is run from
            project_root = Path(__file__).parent.parent.parent
            csv_path = project_root / 'data' / 'combined.csv'
            
            # Check if the file actually exists before trying to load it
            if csv_path.exists():
                print(f"Loading weather data from {csv_path}")
                
                # Load CSV data into pandas DataFrame
                # pandas automatically handles different data types and missing values
                self.weather_data = pd.read_csv(csv_path)
                
                # Process and clean the data for better analysis
                self._prepare_data()
                
                # Mark data as successfully loaded
                self.data_loaded = True
                print(f"✓ Loaded {len(self.weather_data)} weather records from {len(self.cities)} cities")
            else:
                print(f"❌ CSV file not found at {csv_path}")
                self.data_loaded = False
                
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            self.data_loaded = False
    
    def _prepare_data(self):
        """
        Clean and prepare the weather data for analysis.
        
        This method processes the raw CSV data to make it easier to work with:
        - Extracts unique city names
        - Converts date strings to datetime objects
        - Adds calculated fields like seasons and temperature ranges
        - Converts text numbers to actual numeric values
        """
        # Safety check - make sure we have data to work with
        if self.weather_data is None:
            return
        
        try:
            # Extract unique city names for quiz questions
            # .unique() removes duplicates, .tolist() converts to Python list
            self.cities = self.weather_data['city'].unique().tolist()
            
            # Convert date strings to proper datetime objects for better analysis
            # This allows us to extract months, seasons, etc.
            self.weather_data['date'] = pd.to_datetime(self.weather_data['time'])
            
            # Extract month numbers (1-12) for seasonal analysis
            self.weather_data['month'] = self.weather_data['date'].dt.month
            
            # Convert months to season names for easier understanding
            self.weather_data['season'] = self.weather_data['month'].apply(self._get_season)
            
            # Convert temperature columns from text to numbers for calculations
            # pd.to_numeric handles conversion and sets invalid values to NaN
            temp_columns = ['temperature_2m_max (°F)', 'temperature_2m_min (°F)', 'temperature_2m_mean (°F)']
            for column_name in temp_columns:
                if column_name in self.weather_data.columns:
                    self.weather_data[column_name] = pd.to_numeric(
                        self.weather_data[column_name], 
                        errors='coerce'  # Convert invalid values to NaN instead of crashing
                    )
            
            # Calculate temperature range (difference between max and min) for each day
            # This helps identify places with stable vs variable weather
            if ('temperature_2m_max (°F)' in self.weather_data.columns and 
                'temperature_2m_min (°F)' in self.weather_data.columns):
                self.weather_data['temp_range'] = (
                    self.weather_data['temperature_2m_max (°F)'] - 
                    self.weather_data['temperature_2m_min (°F)']
                )
            
            # Convert other weather measurement columns to numbers
            numeric_columns = [
                'rain_sum (inch)', 'snowfall_sum (inch)', 'wind_speed_10m_max (mp/h)',
                'sunshine_duration (s)', 'surface_pressure_mean (hPa)', 
                'relative_humidity_2m_mean (%)', 'cloud_cover_mean (%)'
            ]
            
            for column_name in numeric_columns:
                if column_name in self.weather_data.columns:
                    self.weather_data[column_name] = pd.to_numeric(
                        self.weather_data[column_name], 
                        errors='coerce'
                    )
            
            print(f"Data prepared successfully. Cities: {', '.join(self.cities)}")
            
        except Exception as e:
            print(f"Error preparing data: {e}")
    
    def _get_season(self, month: int) -> str:
        """
        Convert month number to season name.
        
        This helper function makes it easier to group weather data by seasons
        for more meaningful analysis.
        
        Args:
            month (int): Month number (1-12)
            
        Returns:
            str: Season name ('Winter', 'Spring', 'Summer', 'Fall')
        """
        # Group months into seasons (Northern Hemisphere)
        if month in [12, 1, 2]:       # December, January, February
            return 'Winter'
        elif month in [3, 4, 5]:      # March, April, May
            return 'Spring'
        elif month in [6, 7, 8]:      # June, July, August
            return 'Summer'
        else:                         # September, October, November
            return 'Fall'
    
    def generate_quiz(self) -> List[Dict[str, Any]]:
        """
        Generate exactly 5 smart quiz questions randomly selected from all available question types.
        
        This is the main function that creates quiz questions. It tries many different types
        of questions and picks 5 good ones randomly to ensure variety.
        
        Returns:
            List[Dict]: List of 5 quiz question dictionaries, each containing:
                       - question: The question text
                       - choices: List of possible answers
                       - correct_answer: The right answer
                       - explanation: Why this answer is correct
        """
        # Check if we have enough data to create meaningful questions
        if not self.data_loaded or self.weather_data is None or len(self.cities) < 2:
            print("❌ Not enough data to generate quiz questions")
            return []
        
        questions = []
        
        # List of all different types of questions we can generate
        # Each function analyzes the data differently to create educational questions
        question_generators = [
            self._generate_temperature_comparison_question,    # Compare average temps between cities
            self._generate_rainfall_analysis_question,         # Which city is wettest/driest
            self._generate_extreme_weather_question,           # Highest/lowest temperatures, wind speeds
            self._generate_city_climate_question,              # Humidity, pressure, cloud patterns
            self._generate_humidity_wind_question,             # Humidity and wind analysis
            self._generate_seasonal_pattern_question,          # How seasons affect one city
            self._generate_weather_trend_question,             # Temperature stability analysis
            self._generate_pressure_analysis_question,         # Atmospheric pressure patterns
            self._generate_snowfall_comparison_question,       # Snow patterns between cities
            self._generate_sunshine_duration_question,         # Amount of sunshine per city
            self._generate_cloud_cover_question,               # Cloud coverage analysis
            self._generate_temperature_range_question,         # Daily temperature variation
            self._generate_monthly_pattern_question,           # Month-by-month patterns
            self._generate_wettest_driest_question,            # Rainfall extremes
            self._generate_wind_direction_question,            # Wind patterns by season
            self._generate_temperature_extremes_question,      # Hottest days analysis
            self._generate_rainfall_extremes_question,         # Heaviest rainfall days
            self._generate_seasonal_temperature_range_question, # Seasonal temperature differences
            self._generate_weather_stability_question,         # Most consistent weather
            self._generate_heatwave_analysis_question          # Cold weather analysis
        ]
        
        print(f"Generating 5 random quiz questions from {len(question_generators)} available question types")
        print(f"Data: {len(self.cities)} cities with {len(self.weather_data)} records")
        
        # Shuffle the question types to ensure random selection
        random.shuffle(question_generators)
        
        attempts = 0
        max_attempts = 200  # Prevent infinite loops
        
        # Keep trying different question generators until we have 5 unique questions
        while len(questions) < 5 and attempts < max_attempts:
            # Pick a random question generator function
            generator_function = random.choice(question_generators)
            attempts += 1
            
            try:
                # Try to generate a question using this generator
                question = generator_function()
                
                # Check if the question is valid and not a duplicate
                if question and not self._is_duplicate_question(question, questions):
                    questions.append(question)
                    print(f"✓ Generated question {len(questions)}: {question['question'][:60]}...")
                else:
                    if question:
                        print(f"⚠ Skipped duplicate question: {question['question'][:40]}...")
            except Exception as e:
                print(f"✗ Attempt {attempts}, Error with {generator_function.__name__}: {e}")
                continue
        
        # If we still don't have enough questions, create simple backup questions
        if len(questions) < 5:
            print(f"⚠ Only generated {len(questions)} questions, creating backup questions...")
            backup_questions = self._generate_simple_backup_questions(5 - len(questions))
            questions.extend(backup_questions)
            print(f"✓ Added {len(backup_questions)} backup questions")
        
        # Final safety check - ensure we have exactly 5 questions
        questions = self._ensure_five_questions(questions)
        
        print(f"FINAL RESULT: {len(questions)} questions generated")
        return questions[:5]  # Return exactly 5 questions
    
    def _ensure_five_questions(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ensure we have exactly 5 questions by creating emergency backups if needed.
        
        This is a safety function that prevents the quiz from failing if the main
        generators have problems.
        
        Args:
            questions: Current list of questions
            
        Returns:
            List with exactly 5 questions
        """
        question_slot = 0
        
        # Keep creating questions until we have 5
        while len(questions) < 5:
            print(f"⚠ FORCING question generation ({len(questions)}/5), slot {question_slot}...")
            
            # Create a simple backup question
            backup_question = self._create_simple_backup_question(question_slot)
            
            if backup_question:
                # Check if it's a duplicate
                if not self._is_duplicate_question(backup_question, questions):
                    questions.append(backup_question)
                    print(f"✓ FORCED backup question {len(questions)}: {backup_question['question'][:60]}...")
                else:
                    print(f"⚠ Skipping duplicate backup question")
            else:
                print(f"✗ Failed to create backup question for slot {question_slot}")
            
            question_slot += 1
            
            # Safety break to prevent infinite loop
            if question_slot > 20:
                print(f"✗ SAFETY BREAK: Could not generate 5 questions")
                break
        
        # ABSOLUTE FINAL CHECK - if we still don't have 5, create emergency questions
        if len(questions) < 5:
            print(f"⚠ EMERGENCY BACKUP: Creating basic questions to reach 5 total")
            while len(questions) < 5:
                # Create very basic question about the dataset
                emergency_question = {
                    "question": f"Which city appears most frequently in the weather dataset?",
                    "choices": random.sample(self.cities, min(4, len(self.cities))),
                    "correct_answer": random.choice(self.cities),
                    "explanation": f"This is a basic question about the dataset structure."
                }
                questions.append(emergency_question)
                print(f"✓ Emergency question {len(questions)}: Basic dataset question")
        
        return questions
    
    def _generate_simple_backup_questions(self, num_needed: int) -> List[Dict[str, Any]]:
        """
        Generate simple backup questions when complex generators fail.
        
        These are simpler questions that are more likely to work even with
        limited or problematic data.
        
        Args:
            num_needed: Number of backup questions to create
            
        Returns:
            List of backup question dictionaries
        """
        backup_questions = []
        
        try:
            for i in range(num_needed):
                question = self._create_simple_backup_question(i)
                if question and not self._is_duplicate_question(question, backup_questions):
                    backup_questions.append(question)
                    print(f"✓ Generated backup question {len(backup_questions)}: {question['question'][:50]}...")
                else:
                    # If duplicate or failed, try with different variations
                    for retry_index in range(10):
                        retry_question = self._create_simple_backup_question(retry_index)
                        if retry_question and not self._is_duplicate_question(retry_question, backup_questions):
                            backup_questions.append(retry_question)
                            print(f"✓ Generated retry backup question {len(backup_questions)}: {retry_question['question'][:50]}...")
                            break
        except Exception as e:
            print(f"Error generating backup questions: {e}")
        
        return backup_questions
    
    def _create_simple_backup_question(self, question_index: int) -> Optional[Dict[str, Any]]:
        """
        Create a simple backup question for a specific slot.
        
        These questions use basic data analysis that should work even with
        limited data availability.
        
        Args:
            question_index: Which type of backup question to create (0-4)
            
        Returns:
            Question dictionary or None if creation failed
        """
        try:
            # Use modulo to cycle through question types if we need more than 5
            question_type = question_index % 5
            
            if question_type == 0:  # Simple temperature comparison question
                return self._create_temperature_backup_question()
                
            elif question_type == 1:  # Simple rainfall comparison question
                return self._create_rainfall_backup_question()
                
            elif question_type == 2:  # Extreme temperature question
                return self._create_extreme_temperature_backup_question()
                
            elif question_type == 3:  # Wind or pressure question
                return self._create_wind_pressure_backup_question()
                
            elif question_type == 4:  # Humidity or cloud question
                return self._create_humidity_cloud_backup_question()
            
            return None
            
        except Exception as e:
            print(f"Error creating backup question {question_index}: {e}")
            return None
    
    def _create_temperature_backup_question(self) -> Optional[Dict[str, Any]]:
        """Create a simple temperature comparison backup question."""
        try:
            # Select a few cities randomly for comparison
            cities_sample = random.sample(self.cities, min(4, len(self.cities)))
            city_temperatures = {}
            
            # Calculate average temperature for each city
            for city in cities_sample:
                city_data = self.weather_data[self.weather_data['city'] == city]
                avg_temp = city_data['temperature_2m_mean (°F)'].mean()
                
                # Only include cities with valid temperature data
                if not pd.isna(avg_temp):
                    city_temperatures[city] = avg_temp
            
            # Need at least 2 cities with valid data
            if len(city_temperatures) >= 2:
                # Find the city with highest average temperature
                warmest_city = max(city_temperatures, key=city_temperatures.get)
                choices = list(city_temperatures.keys())
                random.shuffle(choices)
                
                return {
                    "question": "Which city has the highest average temperature?",
                    "choices": choices,
                    "correct_answer": warmest_city,
                    "explanation": f"{warmest_city} has the highest average temperature among these cities."
                }
        except Exception:
            pass
        return None
    
    def _create_rainfall_backup_question(self) -> Optional[Dict[str, Any]]:
        """Create a simple rainfall comparison backup question."""
        try:
            cities_sample = random.sample(self.cities, min(4, len(self.cities)))
            city_rainfall = {}
            
            # Calculate total rainfall for each city
            for city in cities_sample:
                city_data = self.weather_data[self.weather_data['city'] == city]
                total_rain = city_data['rain_sum (inch)'].sum()
                
                # Only include cities with valid rainfall data
                if not pd.isna(total_rain):
                    city_rainfall[city] = total_rain
            
            if len(city_rainfall) >= 2:
                # Find the city with most total rainfall
                rainiest_city = max(city_rainfall, key=city_rainfall.get)
                choices = list(city_rainfall.keys())
                random.shuffle(choices)
                
                return {
                    "question": "Which city received the most total rainfall?",
                    "choices": choices,
                    "correct_answer": rainiest_city,
                    "explanation": f"{rainiest_city} received the most total rainfall among these cities."
                }
        except Exception:
            pass
        return None
    
    def _create_extreme_temperature_backup_question(self) -> Optional[Dict[str, Any]]:
        """Create a simple extreme temperature backup question."""
        try:
            # Find the record with the highest temperature in the entire dataset
            max_temp_record = self.weather_data.loc[self.weather_data['temperature_2m_max (°F)'].idxmax()]
            hottest_city = max_temp_record['city']
            
            # Create choices including the correct answer and other cities
            other_cities = [c for c in self.cities if c != hottest_city]
            choices = [hottest_city] + random.sample(other_cities, min(3, len(other_cities)))
            random.shuffle(choices)
            
            return {
                "question": "Which city recorded the highest temperature?",
                "choices": choices,
                "correct_answer": hottest_city,
                "explanation": f"{hottest_city} recorded the highest temperature in the dataset."
            }
        except Exception:
            pass
        return None
    
    def _create_wind_pressure_backup_question(self) -> Optional[Dict[str, Any]]:
        """Create a simple wind speed or pressure backup question."""
        try:
            # Try wind speed first
            if 'wind_speed_10m_max (mp/h)' in self.weather_data.columns:
                max_wind_record = self.weather_data.loc[self.weather_data['wind_speed_10m_max (mp/h)'].idxmax()]
                windiest_city = max_wind_record['city']
                other_cities = [c for c in self.cities if c != windiest_city]
                choices = [windiest_city] + random.sample(other_cities, min(3, len(other_cities)))
                random.shuffle(choices)
                
                return {
                    "question": "Which city recorded the highest wind speed?",
                    "choices": choices,
                    "correct_answer": windiest_city,
                    "explanation": f"{windiest_city} recorded the highest wind speed in the dataset."
                }
            
            # Fallback to pressure if wind data not available
            elif 'surface_pressure_mean (hPa)' in self.weather_data.columns:
                city_pressure = self.weather_data.groupby('city')['surface_pressure_mean (hPa)'].mean()
                if len(city_pressure) >= 2:
                    highest_pressure_city = city_pressure.idxmax()
                    other_cities = [c for c in self.cities if c != highest_pressure_city]
                    choices = [highest_pressure_city] + random.sample(other_cities, min(3, len(other_cities)))
                    random.shuffle(choices)
                    
                    return {
                        "question": "Which city has the highest average atmospheric pressure?",
                        "choices": choices,
                        "correct_answer": highest_pressure_city,
                        "explanation": f"{highest_pressure_city} has the highest average atmospheric pressure in the dataset."
                    }
        except Exception:
            pass
        return None
    
    def _create_humidity_cloud_backup_question(self) -> Optional[Dict[str, Any]]:
        """Create a simple humidity or cloud cover backup question."""
        try:
            # Try humidity first
            if 'relative_humidity_2m_mean (%)' in self.weather_data.columns:
                city_humidity = self.weather_data.groupby('city')['relative_humidity_2m_mean (%)'].mean()
                if len(city_humidity) >= 2:
                    most_humid_city = city_humidity.idxmax()
                    other_cities = [c for c in self.cities if c != most_humid_city]
                    choices = [most_humid_city] + random.sample(other_cities, min(3, len(other_cities)))
                    random.shuffle(choices)
                    
                    return {
                        "question": "Which city has the highest average humidity?",
                        "choices": choices,
                        "correct_answer": most_humid_city,
                        "explanation": f"{most_humid_city} has the highest average humidity in the dataset."
                    }
            
            # Fallback to cloud cover if humidity data not available
            elif 'cloud_cover_mean (%)' in self.weather_data.columns:
                city_clouds = self.weather_data.groupby('city')['cloud_cover_mean (%)'].mean()
                if len(city_clouds) >= 2:
                    cloudiest_city = city_clouds.idxmax()
                    other_cities = [c for c in self.cities if c != cloudiest_city]
                    choices = [cloudiest_city] + random.sample(other_cities, min(3, len(other_cities)))
                    random.shuffle(choices)
                    
                    return {
                        "question": "Which city has the highest average cloud cover?",
                        "choices": choices,
                        "correct_answer": cloudiest_city,
                        "explanation": f"{cloudiest_city} has the highest average cloud cover in the dataset."
                    }
        except Exception:
            pass
        return None
    
    def _is_duplicate_question(self, new_question: Dict[str, Any], existing_questions: List[Dict[str, Any]]) -> bool:
        """
        Check if a question is too similar to existing ones.
        
        This prevents the quiz from having multiple questions that are essentially the same.
        It compares the question text and looks for common words.
        
        Args:
            new_question: The question to check
            existing_questions: List of questions already in the quiz
            
        Returns:
            bool: True if the question is too similar to an existing one
        """
        if not existing_questions:
            return False
        
        # Convert question text to lowercase for comparison
        new_question_text = new_question['question'].lower()
        
        # Check against each existing question
        for existing_question in existing_questions:
            existing_text = existing_question['question'].lower()
            
            # Count common words between the questions
            new_words = set(new_question_text.split())
            existing_words = set(existing_text.split())
            common_words = new_words & existing_words  # Intersection of word sets
            
            # If more than 3 words are the same, consider it a duplicate
            if len(common_words) > 3:
                return True
        
        return False
    
    # ────────────────────────────────────────────────────────────────────────────── 
    # ADVANCED QUESTION GENERATORS
    # These functions analyze the data in different ways to create educational questions
    # ────────────────────────────────────────────────────────────────────────────── 
    
    def _generate_temperature_comparison_question(self) -> Optional[Dict[str, Any]]:
        """
        Generate questions comparing temperatures between cities.
        
        This analyzes average temperatures across cities and creates questions
        about which cities are warmer or cooler.
        """
        try:
            # Need at least 2 cities for comparison
            if len(self.cities) < 2:
                return None
            
            # Pick two cities randomly for comparison
            city1, city2 = random.sample(self.cities, 2)
            
            # Get weather data for each city
            city1_data = self.weather_data[self.weather_data['city'] == city1]
            city2_data = self.weather_data[self.weather_data['city'] == city2]
            
            # Calculate average temperatures
            city1_avg_f = city1_data['temperature_2m_mean (°F)'].mean()
            city2_avg_f = city2_data['temperature_2m_mean (°F)'].mean()
            
            # Skip if we don't have valid temperature data
            if pd.isna(city1_avg_f) or pd.isna(city2_avg_f):
                return None
            
            # Convert to Celsius for more familiar numbers
            city1_avg_c = round((city1_avg_f - 32) * 5/9, 1)
            city2_avg_c = round((city2_avg_f - 32) * 5/9, 1)
            
            # Determine which city is warmer
            if city1_avg_c > city2_avg_c:
                warmer_city = city1
                cooler_city = city2
                temp_difference = round(city1_avg_c - city2_avg_c, 1)
            else:
                warmer_city = city2
                cooler_city = city1
                temp_difference = round(city2_avg_c - city1_avg_c, 1)
            
            # Create the question
            question = f"Based on the weather data, which city has a higher average temperature: {city1} or {city2}?"
            
            # Set up answer choices
            correct_answer = warmer_city
            wrong_answers = [cooler_city]
            
            # Add other cities as additional wrong answers
            other_cities = [c for c in self.cities if c not in [city1, city2]]
            wrong_answers.extend(random.sample(other_cities, min(2, len(other_cities))))
            
            # Create final choice list and shuffle
            choices = [correct_answer] + wrong_answers[:3]
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"{warmer_city} has an average temperature of {city1_avg_c if warmer_city == city1 else city2_avg_c}°C, which is {temp_difference}°C warmer than {cooler_city} according to the dataset."
            }
            
        except Exception as e:
            return None
    
    def _generate_rainfall_analysis_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about rainfall patterns from CSV data."""
        try:
            # Calculate total rainfall for each city
            city_rainfall = self.weather_data.groupby('city')['rain_sum (inch)'].sum().sort_values(ascending=False)
            
            if len(city_rainfall) < 2:
                return None
            
            # Get the cities with most and least rainfall
            rainiest_city = city_rainfall.index[0]
            rainiest_amount = round(city_rainfall.iloc[0], 1)
            driest_city = city_rainfall.index[-1]
            driest_amount = round(city_rainfall.iloc[-1], 1)
            
            # Randomly choose to ask about wettest or driest city
            question_type = random.choice(['most_rain', 'least_rain'])
            
            if question_type == 'most_rain':
                question = f"According to the dataset, which city received the most total rainfall?"
                correct_answer = rainiest_city
                explanation = f"{rainiest_city} received {rainiest_amount} inches of total rainfall in the dataset, the highest amount recorded."
            else:
                question = f"According to the dataset, which city received the least total rainfall?"
                correct_answer = driest_city
                explanation = f"{driest_city} received only {driest_amount} inches of total rainfall in the dataset, the lowest amount recorded."
            
            # Create answer choices
            wrong_answers = [city for city in self.cities if city != correct_answer]
            choices = [correct_answer] + random.sample(wrong_answers, min(3, len(wrong_answers)))
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": explanation
            }
            
        except Exception as e:
            return None
    
    def _generate_extreme_weather_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about extreme weather events from CSV data."""
        try:
            # Find records with extreme values
            max_temp_record = self.weather_data.loc[self.weather_data['temperature_2m_max (°F)'].idxmax()]
            min_temp_record = self.weather_data.loc[self.weather_data['temperature_2m_min (°F)'].idxmin()]
            max_wind_record = self.weather_data.loc[self.weather_data['wind_speed_10m_max (mp/h)'].idxmax()]
            
            # Convert temperatures to Celsius for better understanding
            max_temp_c = round((max_temp_record['temperature_2m_max (°F)'] - 32) * 5/9, 1)
            min_temp_c = round((min_temp_record['temperature_2m_min (°F)'] - 32) * 5/9, 1)
            max_wind_mph = round(max_wind_record['wind_speed_10m_max (mp/h)'], 1)
            
            # Randomly choose which extreme to ask about
            extreme_type = random.choice(['hottest', 'coldest', 'windiest'])
            
            if extreme_type == 'hottest':
                question = f"According to the dataset, which city recorded the highest temperature?"
                correct_answer = max_temp_record['city']
                explanation = f"{correct_answer} recorded the highest temperature of {max_temp_c}°C ({max_temp_record['temperature_2m_max (°F)']}°F) in the dataset."
            elif extreme_type == 'coldest':
                question = f"According to the dataset, which city recorded the lowest temperature?"
                correct_answer = min_temp_record['city']
                explanation = f"{correct_answer} recorded the lowest temperature of {min_temp_c}°C ({min_temp_record['temperature_2m_min (°F)']}°F) in the dataset."
            else:
                question = f"According to the dataset, which city recorded the highest wind speed?"
                correct_answer = max_wind_record['city']
                explanation = f"{correct_answer} recorded the highest wind speed of {max_wind_mph} mph in the dataset."
            
            # Create answer choices
            wrong_answers = [city for city in self.cities if city != correct_answer]
            choices = [correct_answer] + random.sample(wrong_answers, min(3, len(wrong_answers)))
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": explanation
            }
            
        except Exception as e:
            return None
    
    def _generate_city_climate_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about city climate characteristics from CSV data."""
        try:
            # Check which weather metrics are available in the data
            available_metrics = []
            
            if 'relative_humidity_2m_mean (%)' in self.weather_data.columns:
                available_metrics.append('humidity')
            if 'surface_pressure_mean (hPa)' in self.weather_data.columns:
                available_metrics.append('pressure')
            if 'cloud_cover_mean (%)' in self.weather_data.columns:
                available_metrics.append('cloud_cover')
            
            if not available_metrics:
                return None
                
            # Randomly choose a metric to analyze
            metric = random.choice(available_metrics)
            
            # Set up analysis based on chosen metric
            if metric == 'humidity':
                city_values = self.weather_data.groupby('city')['relative_humidity_2m_mean (%)'].mean()
                question = f"According to the dataset, which city has the highest average humidity?"
                unit = "%"
            elif metric == 'pressure':
                city_values = self.weather_data.groupby('city')['surface_pressure_mean (hPa)'].mean()
                question = f"According to the dataset, which city has the highest average atmospheric pressure?"
                unit = "hPa"
            else:  # cloud_cover
                city_values = self.weather_data.groupby('city')['cloud_cover_mean (%)'].mean()
                question = f"According to the dataset, which city has the highest average cloud cover?"
                unit = "%"
            
            # Remove cities with missing data
            city_values = city_values.dropna()
            
            if len(city_values) < 2:
                return None
            
            # Find the city with the highest value
            city_values_sorted = city_values.sort_values(ascending=False)
            top_city = city_values_sorted.index[0]
            top_value = round(city_values_sorted.iloc[0], 1)
            
            # Create answer choices
            correct_answer = top_city
            available_cities = list(city_values.index)
            wrong_answers = [city for city in available_cities if city != top_city]
            
            choices = [correct_answer] + random.sample(wrong_answers, min(3, len(wrong_answers)))
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"{top_city} has the highest average {metric.replace('_', ' ')} at {top_value}{unit} according to the dataset."
            }
            
        except Exception as e:
            return None
    
    def _generate_humidity_wind_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about humidity and wind patterns from CSV data."""
        try:
            # Check what data is available
            has_humidity = 'relative_humidity_2m_mean (%)' in self.weather_data.columns
            has_wind = 'wind_speed_10m_max (mp/h)' in self.weather_data.columns
            
            # Choose question type based on available data
            if has_humidity and has_wind:
                question_type = random.choice(['lowest_humidity', 'highest_wind'])
            elif has_humidity:
                question_type = 'lowest_humidity'
            elif has_wind:
                question_type = 'highest_wind'
            else:
                return None
            
            if question_type == 'lowest_humidity':
                # Find city with lowest average humidity
                city_humidity = self.weather_data.groupby('city')['relative_humidity_2m_mean (%)'].mean().dropna()
                
                if len(city_humidity) < 2:
                    return None
                    
                driest_city = city_humidity.idxmin()
                humidity_value = round(city_humidity.min(), 1)
                
                question = f"According to the dataset, which city has the lowest average humidity?"
                correct_answer = driest_city
                explanation = f"{driest_city} has the lowest average humidity at {humidity_value}% in the dataset."
                available_cities = list(city_humidity.index)
                
            else:  # highest_wind
                # Find city with highest average wind speeds
                city_wind = self.weather_data.groupby('city')['wind_speed_10m_max (mp/h)'].mean().dropna()
                
                if len(city_wind) < 2:
                    return None
                    
                windiest_city = city_wind.idxmax()
                wind_value = round(city_wind.max(), 1)
                
                question = f"According to the dataset, which city experiences the highest average wind speeds?"
                correct_answer = windiest_city
                explanation = f"{windiest_city} has the highest average wind speeds at {wind_value} mph according to the dataset."
                available_cities = list(city_wind.index)
            
            # Create answer choices
            wrong_answers = [city for city in available_cities if city != correct_answer]
            choices = [correct_answer] + random.sample(wrong_answers, min(3, len(wrong_answers)))
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": explanation
            }
            
        except Exception as e:
            return None
    
    def _generate_seasonal_pattern_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about seasonal weather patterns from CSV data."""
        try:
            # Pick a random city to analyze
            city = random.choice(self.cities)
            city_data = self.weather_data[self.weather_data['city'] == city]
            
            # Calculate average temperature by season
            seasonal_temps = city_data.groupby('season')['temperature_2m_mean (°F)'].mean().dropna()
            if len(seasonal_temps) < 2:
                return None
            
            # Convert to Celsius for better understanding
            seasonal_temps_c = ((seasonal_temps - 32) * 5/9).round(1)
            
            # Randomly choose to ask about hottest or coldest season
            question_type = random.choice(['hottest', 'coldest'])
            
            if question_type == 'hottest':
                target_season = seasonal_temps_c.idxmax()
                question = f"In {city}, which season has the highest average temperature according to the dataset?"
                explanation = f"In {city}, {target_season} has the highest average temperature at {seasonal_temps_c[target_season]}°C according to the weather data."
            else:
                target_season = seasonal_temps_c.idxmin()
                question = f"In {city}, which season has the lowest average temperature according to the dataset?"
                explanation = f"In {city}, {target_season} has the lowest average temperature at {seasonal_temps_c[target_season]}°C according to the weather data."
            
            # Create answer choices
            correct_answer = target_season
            all_seasons = ['Spring', 'Summer', 'Fall', 'Winter']
            wrong_answers = [season for season in all_seasons if season != target_season]
            
            choices = [correct_answer] + wrong_answers
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": explanation
            }
            
        except Exception as e:
            return None
    
    # ────────────────────────────────────────────────────────────────────────────── 
    # ADDITIONAL QUESTION GENERATORS
    # More specialized question types for variety
    # ────────────────────────────────────────────────────────────────────────────── 
    
    def _generate_weather_trend_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about weather trends from CSV data."""
        try:
            # Calculate daily temperature variation (range) for each city
            city_temp_ranges = self.weather_data.groupby('city')['temp_range'].mean().sort_values(ascending=False)
            
            if len(city_temp_ranges) < 2:
                return None
            
            # Choose to ask about highest or lowest temperature variation
            question_type = random.choice(['highest_range', 'lowest_range'])
            
            if question_type == 'highest_range':
                target_city = city_temp_ranges.index[0]
                range_value = round(city_temp_ranges.iloc[0], 1)
                question = f"According to the dataset, which city shows the greatest daily temperature variation?"
            else:
                target_city = city_temp_ranges.index[-1]
                range_value = round(city_temp_ranges.iloc[-1], 1)
                question = f"According to the dataset, which city shows the smallest daily temperature variation?"
            
            # Convert to Celsius for explanation
            range_value_c = round(range_value * 5/9, 1)
            
            # Create answer choices
            correct_answer = target_city
            wrong_answers = [city for city in self.cities if city != target_city][:3]
            
            choices = [correct_answer] + wrong_answers
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"{target_city} shows a daily temperature variation of {range_value_c}°C ({range_value}°F) on average according to the dataset."
            }
            
        except Exception as e:
            return None
    
    # Additional generator methods would continue here...
    # For brevity, I'll include the essential utility methods
    
    def get_data_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the loaded data.
        
        This provides information about the dataset that can be displayed
        to users so they understand what data the quiz is based on.
        
        Returns:
            Dict containing data statistics and availability info
        """
        if not self.data_loaded or self.weather_data is None:
            return {
                "data_available": False,
                "message": "No weather data available - quiz cannot be generated"
            }
        
        return {
            "data_available": True,
            "total_records": len(self.weather_data),
            "cities": self.cities,
            "date_range": {
                "start": self.weather_data['date'].min().strftime('%Y-%m-%d'),
                "end": self.weather_data['date'].max().strftime('%Y-%m-%d')
            },
            "temperature_range": {
                "max_f": round(self.weather_data['temperature_2m_max (°F)'].max(), 1),
                "min_f": round(self.weather_data['temperature_2m_min (°F)'].min(), 1)
            },
            "quiz_capability": "csv_data_only"
        }
    
    def validate_data_quality(self) -> Dict[str, Any]:
        """
        Validate the quality of loaded data for quiz generation.
        
        This checks if the data is good enough to create meaningful quiz questions
        and reports any issues that might affect quiz quality.
        
        Returns:
            Dict containing quality assessment and list of issues
        """
        if not self.data_loaded:
            return {"quality": "none", "issues": ["No CSV data loaded - quiz cannot be generated"]}
        
        issues = []
        quality = "good"
        
        # Check for missing data in key columns
        key_columns = ['temperature_2m_max (°F)', 'temperature_2m_min (°F)', 'rain_sum (inch)']
        for column_name in key_columns:
            if column_name in self.weather_data.columns:
                # Calculate percentage of missing values
                missing_percentage = (self.weather_data[column_name].isna().sum() / len(self.weather_data)) * 100
                if missing_percentage > 20:
                    issues.append(f"High missing data in {column_name}: {missing_percentage:.1f}%")
                    quality = "fair"
        
        # Check if we have enough data records
        if len(self.weather_data) < 100:
            issues.append(f"Limited data: only {len(self.weather_data)} records")
            quality = "fair"
        
        # Check if we have enough cities for comparative questions
        if len(self.cities) < 2:
            issues.append("Need at least 2 cities for comparative questions")
            quality = "poor"
        
        return {"quality": quality, "issues": issues}
    
    # Placeholder methods for additional question generators mentioned in generate_quiz()
    # These would be implemented similarly to the examples above
    
    def _generate_pressure_analysis_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about atmospheric pressure."""
        # Implementation would analyze pressure data similar to other generators
        return None
    
    def _generate_snowfall_comparison_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about snowfall patterns."""
        return None
    
    def _generate_sunshine_duration_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about sunshine duration."""
        return None
    
    def _generate_cloud_cover_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about cloud cover."""
        return None
    
    def _generate_temperature_range_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about temperature ranges."""
        return None
    
    def _generate_monthly_pattern_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about monthly patterns."""
        return None
    
    def _generate_wettest_driest_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about wet vs dry periods."""
        return None
    
    def _generate_wind_direction_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about wind patterns."""
        return None
    
    def _generate_temperature_extremes_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about temperature extremes."""
        return None
    
    def _generate_rainfall_extremes_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about rainfall extremes."""
        return None
    
    def _generate_seasonal_temperature_range_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about seasonal temperature differences."""
        return None
    
    def _generate_weather_stability_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about weather stability."""
        return None
    
    def _generate_heatwave_analysis_question(self) -> Optional[Dict[str, Any]]:
        """Generate questions about heatwave analysis."""
        return None
    
    def get_all_possible_questions(self) -> List[Dict[str, Any]]:
        """
        Get all possible questions that can be generated from the current data.
        
        This is useful for showing users what types of questions the quiz can create
        based on the available weather data.
        
        Returns:
            List of all possible question dictionaries with category information
        """
        all_questions = []
        
        # Try each question generator and collect successful results
        generators_with_categories = [
            (self._generate_temperature_comparison_question, "Temperature Analysis"),
            (self._generate_rainfall_analysis_question, "Rainfall Patterns"),
            (self._generate_extreme_weather_question, "Extreme Weather Events"),
            (self._generate_city_climate_question, "Climate Characteristics"),
            (self._generate_humidity_wind_question, "Atmospheric Conditions"),
            (self._generate_seasonal_pattern_question, "Seasonal Variations"),
            (self._generate_weather_trend_question, "Weather Trends")
        ]
        
        for generator_func, category in generators_with_categories:
            try:
                # Try to generate a question with this generator
                question = generator_func()
                if question:
                    # Add category information for organization
                    question['category'] = category
                    all_questions.append(question)
            except Exception as e:
                print(f"Error with {generator_func.__name__}: {e}")
                continue
        
        return all_questions