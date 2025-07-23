"""
Enhanced Weather Quiz Generator - Creates smart questions based on combined CSV data
"""

import pandas as pd
import random
import os
import numpy as np
from datetime import datetime
from pathlib import Path


class WeatherQuizGenerator:
    """
    Generates intelligent weather quiz questions based on real CSV data analysis
    """
    
    def __init__(self):
        self.weather_data = None
        self.cities = []
        self.data_loaded = False
        self._load_combined_data()
    
    def _load_combined_data(self):
        """Load weather data from the combined CSV file"""
        try:
            # Look for combined.csv in the data directory
            project_root = Path(__file__).parent.parent.parent
            csv_path = project_root / 'data' / 'combined.csv'
            
            if csv_path.exists():
                print(f"Loading weather data from {csv_path}")
                self.weather_data = pd.read_csv(csv_path)
                
                # Clean and prepare the data
                self._prepare_data()
                self.data_loaded = True
                print(f"✓ Loaded {len(self.weather_data)} weather records from {len(self.cities)} cities")
            else:
                print(f"❌ CSV file not found at {csv_path}")
                self.data_loaded = False
                
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            self.data_loaded = False
    
    def _prepare_data(self):
        """Clean and prepare the weather data for analysis"""
        if self.weather_data is None:
            return
        
        try:
            # Get unique cities
            self.cities = self.weather_data['city'].unique().tolist()
            
            # Convert date column
            self.weather_data['date'] = pd.to_datetime(self.weather_data['time'])
            self.weather_data['month'] = self.weather_data['date'].dt.month
            self.weather_data['season'] = self.weather_data['month'].apply(self._get_season)
            
            # Convert temperature columns (they're in Fahrenheit)
            temp_cols = ['temperature_2m_max (°F)', 'temperature_2m_min (°F)', 'temperature_2m_mean (°F)']
            for col in temp_cols:
                if col in self.weather_data.columns:
                    self.weather_data[col] = pd.to_numeric(self.weather_data[col], errors='coerce')
            
            # Calculate temperature range
            if 'temperature_2m_max (°F)' in self.weather_data.columns and 'temperature_2m_min (°F)' in self.weather_data.columns:
                self.weather_data['temp_range'] = (
                    self.weather_data['temperature_2m_max (°F)'] - 
                    self.weather_data['temperature_2m_min (°F)']
                )
            
            # Convert other numeric columns
            numeric_cols = [
                'rain_sum (inch)', 'snowfall_sum (inch)', 'wind_speed_10m_max (mp/h)',
                'sunshine_duration (s)', 'surface_pressure_mean (hPa)', 
                'relative_humidity_2m_mean (%)', 'cloud_cover_mean (%)'
            ]
            
            for col in numeric_cols:
                if col in self.weather_data.columns:
                    self.weather_data[col] = pd.to_numeric(self.weather_data[col], errors='coerce')
            
            print(f"Data prepared successfully. Cities: {', '.join(self.cities)}")
            
        except Exception as e:
            print(f"Error preparing data: {e}")
    
    def _get_season(self, month):
        """Convert month number to season"""
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
    
    def generate_quiz(self):
        """Generate 5 smart quiz questions based on real data"""
        if not self.data_loaded or self.weather_data is None:
            return self._generate_fallback_quiz()
        
        questions = []
        
        # Define question generators with their weights
        question_generators = [
            (self._generate_temperature_comparison_question, 1),
            (self._generate_rainfall_analysis_question, 1),
            (self._generate_seasonal_pattern_question, 1),
            (self._generate_extreme_weather_question, 1),
            (self._generate_city_climate_question, 1),
            (self._generate_humidity_wind_question, 1),
            (self._generate_weather_trend_question, 1)
        ]
        
        # Generate questions ensuring variety
        attempts = 0
        max_attempts = 20
        
        while len(questions) < 5 and attempts < max_attempts:
            generator, weight = random.choice(question_generators)
            try:
                question = generator()
                if question and not self._is_duplicate_question(question, questions):
                    questions.append(question)
            except Exception as e:
                print(f"Error generating question: {e}")
            attempts += 1
        
        # Fill remaining slots with fallback questions if needed
        while len(questions) < 5:
            fallback = self._generate_fallback_question()
            if fallback and not self._is_duplicate_question(fallback, questions):
                questions.append(fallback)
        
        return questions[:5]
    
    def _is_duplicate_question(self, new_question, existing_questions):
        """Check if question is too similar to existing ones"""
        if not existing_questions:
            return False
        
        new_q = new_question['question'].lower()
        for existing in existing_questions:
            existing_q = existing['question'].lower()
            # Simple similarity check
            common_words = set(new_q.split()) & set(existing_q.split())
            if len(common_words) > 3:  # If more than 3 words in common
                return True
        
        return False
    
    def _generate_temperature_comparison_question(self):
        """Generate questions comparing temperatures between cities"""
        try:
            # Get two random cities
            if len(self.cities) < 2:
                return None
            
            city1, city2 = random.sample(self.cities, 2)
            
            # Calculate average temperatures for each city
            city1_data = self.weather_data[self.weather_data['city'] == city1]
            city2_data = self.weather_data[self.weather_data['city'] == city2]
            
            city1_avg = city1_data['temperature_2m_mean (°F)'].mean()
            city2_avg = city2_data['temperature_2m_mean (°F)'].mean()
            
            if pd.isna(city1_avg) or pd.isna(city2_avg):
                return None
            
            # Convert to Celsius for the question
            city1_avg_c = round((city1_avg - 32) * 5/9, 1)
            city2_avg_c = round((city2_avg - 32) * 5/9, 1)
            
            if city1_avg_c > city2_avg_c:
                warmer_city = city1
                cooler_city = city2
                temp_diff = round(city1_avg_c - city2_avg_c, 1)
            else:
                warmer_city = city2
                cooler_city = city1
                temp_diff = round(city2_avg_c - city1_avg_c, 1)
            
            question = f"Based on the weather data, which city has a higher average temperature: {city1} or {city2}?"
            
            correct_answer = warmer_city
            wrong_answers = [cooler_city, "They're about the same", "Cannot be determined"]
            
            choices = [correct_answer] + wrong_answers[:3]
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"{warmer_city} has an average temperature of {city1_avg_c if warmer_city == city1 else city2_avg_c}°C, which is {temp_diff}°C warmer than {cooler_city}."
            }
            
        except Exception as e:
            return None
    
    def _generate_rainfall_analysis_question(self):
        """Generate questions about rainfall patterns"""
        try:
            # Find the city with most rainfall
            city_rainfall = self.weather_data.groupby('city')['rain_sum (inch)'].sum().sort_values(ascending=False)
            
            if len(city_rainfall) < 2:
                return None
            
            rainiest_city = city_rainfall.index[0]
            rainiest_amount = round(city_rainfall.iloc[0], 1)
            
            # Get month with most rain for that city
            city_data = self.weather_data[self.weather_data['city'] == rainiest_city]
            monthly_rain = city_data.groupby('month')['rain_sum (inch)'].sum()
            rainiest_month = monthly_rain.idxmax()
            
            month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']
            
            question = f"Which city received the most total rainfall in the dataset?"
            
            correct_answer = rainiest_city
            wrong_answers = [city for city in self.cities if city != rainiest_city][:3]
            
            choices = [correct_answer] + wrong_answers
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"{rainiest_city} received {rainiest_amount} inches of total rainfall, with the heaviest rains typically in {month_names[rainiest_month]}."
            }
            
        except Exception as e:
            return None
    
    def _generate_seasonal_pattern_question(self):
        """Generate questions about seasonal weather patterns"""
        try:
            # Pick a random city
            city = random.choice(self.cities)
            city_data = self.weather_data[self.weather_data['city'] == city]
            
            # Analyze seasonal temperatures
            seasonal_temps = city_data.groupby('season')['temperature_2m_mean (°F)'].mean()
            
            if len(seasonal_temps) < 4:
                return None
            
            # Convert to Celsius
            seasonal_temps_c = ((seasonal_temps - 32) * 5/9).round(1)
            
            hottest_season = seasonal_temps_c.idxmax()
            coldest_season = seasonal_temps_c.idxmin()
            
            question = f"In {city}, which season has the highest average temperature according to the data?"
            
            correct_answer = hottest_season
            wrong_answers = [season for season in ['Spring', 'Summer', 'Fall', 'Winter'] if season != hottest_season]
            
            choices = [correct_answer] + wrong_answers[:3]
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"In {city}, {hottest_season} has the highest average temperature at {seasonal_temps_c[hottest_season]}°C, while {coldest_season} is the coldest at {seasonal_temps_c[coldest_season]}°C."
            }
            
        except Exception as e:
            return None
    
    def _generate_extreme_weather_question(self):
        """Generate questions about extreme weather events"""
        try:
            # Find extremes across all data
            max_temp_record = self.weather_data.loc[self.weather_data['temperature_2m_max (°F)'].idxmax()]
            min_temp_record = self.weather_data.loc[self.weather_data['temperature_2m_min (°F)'].idxmin()]
            max_wind_record = self.weather_data.loc[self.weather_data['wind_speed_10m_max (mp/h)'].idxmax()]
            
            # Convert temperatures to Celsius
            max_temp_c = round((max_temp_record['temperature_2m_max (°F)'] - 32) * 5/9, 1)
            min_temp_c = round((min_temp_record['temperature_2m_min (°F)'] - 32) * 5/9, 1)
            max_wind_mph = round(max_wind_record['wind_speed_10m_max (mp/h)'], 1)
            
            # Choose which extreme to ask about
            extreme_type = random.choice(['hottest', 'coldest', 'windiest'])
            
            if extreme_type == 'hottest':
                question = f"Which city recorded the highest temperature in the dataset?"
                correct_answer = max_temp_record['city']
                explanation = f"{correct_answer} recorded the highest temperature of {max_temp_c}°C ({max_temp_record['temperature_2m_max (°F)']}°F)."
            elif extreme_type == 'coldest':
                question = f"Which city recorded the lowest temperature in the dataset?"
                correct_answer = min_temp_record['city']
                explanation = f"{correct_answer} recorded the lowest temperature of {min_temp_c}°C ({min_temp_record['temperature_2m_min (°F)']}°F)."
            else:  # windiest
                question = f"Which city recorded the highest wind speed in the dataset?"
                correct_answer = max_wind_record['city']
                explanation = f"{correct_answer} recorded the highest wind speed of {max_wind_mph} mph."
            
            wrong_answers = [city for city in self.cities if city != correct_answer][:3]
            
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
    
    def _generate_city_climate_question(self):
        """Generate questions about city climate characteristics"""
        try:
            # Analyze humidity patterns
            city_humidity = self.weather_data.groupby('city')['relative_humidity_2m_mean (%)'].mean().sort_values(ascending=False)
            
            if len(city_humidity) < 2:
                return None
            
            most_humid_city = city_humidity.index[0]
            humidity_value = round(city_humidity.iloc[0], 1)
            
            question = f"Which city has the highest average humidity according to the data?"
            
            correct_answer = most_humid_city
            wrong_answers = [city for city in self.cities if city != most_humid_city][:3]
            
            choices = [correct_answer] + wrong_answers
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"{most_humid_city} has the highest average humidity at {humidity_value}%, indicating a more moisture-rich climate."
            }
            
        except Exception as e:
            return None
    
    def _generate_humidity_wind_question(self):
        """Generate questions about humidity and wind patterns"""
        try:
            # Find city with lowest humidity or highest wind
            city_humidity = self.weather_data.groupby('city')['relative_humidity_2m_mean (%)'].mean()
            city_wind = self.weather_data.groupby('city')['wind_speed_10m_max (mp/h)'].mean()
            
            question_type = random.choice(['humidity', 'wind'])
            
            if question_type == 'humidity':
                driest_city = city_humidity.idxmin()
                humidity_value = round(city_humidity.min(), 1)
                
                question = f"Which city has the lowest average humidity, indicating a drier climate?"
                correct_answer = driest_city
                explanation = f"{driest_city} has the lowest average humidity at {humidity_value}%, making it the driest location in the dataset."
            else:
                windiest_city = city_wind.idxmax()
                wind_value = round(city_wind.max(), 1)
                
                question = f"Which city experiences the highest average wind speeds?"
                correct_answer = windiest_city
                explanation = f"{windiest_city} has the highest average wind speeds at {wind_value} mph, indicating more dynamic weather patterns."
            
            wrong_answers = [city for city in self.cities if city != correct_answer][:3]
            
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
    
    def _generate_weather_trend_question(self):
        """Generate questions about weather trends and patterns"""
        try:
            # Analyze temperature ranges
            city_temp_ranges = self.weather_data.groupby('city')['temp_range'].mean().sort_values(ascending=False)
            
            if len(city_temp_ranges) < 2:
                return None
            
            highest_range_city = city_temp_ranges.index[0]
            range_value = round(city_temp_ranges.iloc[0], 1)
            
            # Convert to Celsius
            range_value_c = round(range_value * 5/9, 1)
            
            question = f"Which city shows the greatest daily temperature variation (difference between max and min temperatures)?"
            
            correct_answer = highest_range_city
            wrong_answers = [city for city in self.cities if city != highest_range_city][:3]
            
            choices = [correct_answer] + wrong_answers
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"{highest_range_city} shows the greatest daily temperature variation with an average range of {range_value_c}°C ({range_value}°F), indicating more continental climate characteristics."
            }
            
        except Exception as e:
            return None
    
    def _generate_fallback_question(self):
        """Generate general weather knowledge questions as fallback"""
        fallback_questions = [
            {
                "question": "What weather instrument measures atmospheric pressure?",
                "choices": ["Barometer", "Anemometer", "Hygrometer", "Thermometer"],
                "correct_answer": "Barometer",
                "explanation": "A barometer measures atmospheric pressure, which helps predict weather changes."
            },
            {
                "question": "Which cloud type typically produces thunderstorms?",
                "choices": ["Cumulonimbus", "Cirrus", "Stratus", "Altostratus"],
                "correct_answer": "Cumulonimbus",
                "explanation": "Cumulonimbus clouds are towering clouds that can reach extreme heights and produce thunderstorms, heavy rain, and severe weather."
            },
            {
                "question": "What causes the Coriolis effect that influences weather patterns?",
                "choices": ["Earth's rotation", "Solar radiation", "Ocean currents", "Mountain ranges"],
                "correct_answer": "Earth's rotation",
                "explanation": "The Coriolis effect is caused by Earth's rotation and influences the direction of wind patterns and storm systems."
            },
            {
                "question": "At what relative humidity level does air become saturated?",
                "choices": ["100%", "90%", "80%", "75%"],
                "correct_answer": "100%",
                "explanation": "Air becomes saturated at 100% relative humidity, meaning it can hold no more water vapor at that temperature."
            },
            {
                "question": "What is the primary greenhouse gas in Earth's atmosphere?",
                "choices": ["Water vapor", "Carbon dioxide", "Methane", "Ozone"],
                "correct_answer": "Water vapor",
                "explanation": "Water vapor is the most abundant greenhouse gas in the atmosphere, though CO2 is the most significant human-influenced one."
            },
            {
                "question": "Which scale is used to classify tornado intensity?",
                "choices": ["Enhanced Fujita Scale", "Saffir-Simpson Scale", "Beaufort Scale", "Richter Scale"],
                "correct_answer": "Enhanced Fujita Scale",
                "explanation": "The Enhanced Fujita Scale (EF Scale) classifies tornadoes from EF0 to EF5 based on damage and estimated wind speeds."
            },
            {
                "question": "What causes a temperature inversion in the atmosphere?",
                "choices": ["Warm air above cold air", "Cold air above warm air", "Equal temperatures", "High pressure systems"],
                "correct_answer": "Warm air above cold air",
                "explanation": "A temperature inversion occurs when warm air sits above cooler air, which is opposite to the normal atmospheric temperature profile."
            },
            {
                "question": "Which type of precipitation forms when raindrops freeze before hitting the ground?",
                "choices": ["Sleet", "Snow", "Hail", "Freezing rain"],
                "correct_answer": "Sleet",
                "explanation": "Sleet forms when raindrops freeze completely before reaching the ground, creating small ice pellets."
            }
        ]
        
        return random.choice(fallback_questions)
    
    def _generate_fallback_quiz(self):
        """Generate entire quiz using fallback questions when data is unavailable"""
        questions = []
        available_questions = [
            self._generate_fallback_question() for _ in range(10)
        ]
        
        # Remove duplicates and select 5
        unique_questions = []
        used_questions = set()
        
        for q in available_questions:
            if q['question'] not in used_questions:
                unique_questions.append(q)
                used_questions.add(q['question'])
                if len(unique_questions) >= 5:
                    break
        
        return unique_questions
    
    def get_data_stats(self):
        """Get statistics about the loaded data"""
        if not self.data_loaded or self.weather_data is None:
            return {
                "data_available": False,
                "message": "No weather data available"
            }
        
        stats = {
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
            "quiz_capability": "advanced"
        }
        
        return stats
    
    def validate_data_quality(self):
        """Validate the quality of loaded data for quiz generation"""
        if not self.data_loaded:
            return {"quality": "none", "issues": ["No data loaded"]}
        
        issues = []
        quality = "good"
        
        # Check for missing values in key columns
        key_columns = ['temperature_2m_max (°F)', 'temperature_2m_min (°F)', 'rain_sum (inch)']
        for col in key_columns:
            if col in self.weather_data.columns:
                missing_pct = (self.weather_data[col].isna().sum() / len(self.weather_data)) * 100
                if missing_pct > 20:
                    issues.append(f"High missing data in {col}: {missing_pct:.1f}%")
                    quality = "fair"
        
        # Check data completeness
        if len(self.weather_data) < 100:
            issues.append(f"Limited data: only {len(self.weather_data)} records")
            quality = "fair"
        
        if len(self.cities) < 2:
            issues.append("Need at least 2 cities for comparative questions")
            quality = "poor"
        
        return {"quality": quality, "issues": issues}