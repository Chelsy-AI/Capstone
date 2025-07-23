"""
Enhanced Weather Quiz Generator - Creates smart questions ONLY based on combined CSV data
"""

import pandas as pd
import random
import os
import numpy as np
from datetime import datetime
from pathlib import Path


class WeatherQuizGenerator:
    """
    Generates intelligent weather quiz questions based EXCLUSIVELY on real CSV data analysis
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
        """Generate exactly 5 smart quiz questions based ONLY on real CSV data"""
        if not self.data_loaded or self.weather_data is None or len(self.cities) < 2:
            return []  # Return empty list if no data - NO FALLBACK QUESTIONS
        
        questions = []
        
        # Priority question generators - most likely to work with any dataset
        priority_generators = [
            self._generate_temperature_comparison_question,
            self._generate_rainfall_analysis_question,
            self._generate_extreme_weather_question,
            self._generate_city_climate_question,
            self._generate_humidity_wind_question
        ]
        
        # Secondary generators - might require more specific data
        secondary_generators = [
            self._generate_seasonal_pattern_question,
            self._generate_weather_trend_question,
            self._generate_pressure_analysis_question,
            self._generate_snowfall_comparison_question,
            self._generate_sunshine_duration_question,
            self._generate_cloud_cover_question,
            self._generate_temperature_range_question,
            self._generate_monthly_pattern_question,
            self._generate_wettest_driest_question,
            self._generate_wind_direction_question
        ]
        
        # First, try priority generators
        print(f"Generating quiz from {len(self.cities)} cities with {len(self.weather_data)} records")
        
        for generator in priority_generators:
            if len(questions) >= 5:
                break
            
            for attempt in range(5):  # Try each priority generator multiple times
                try:
                    question = generator()
                    if question and not self._is_duplicate_question(question, questions):
                        questions.append(question)
                        print(f"✓ Generated question {len(questions)}: {question['question'][:50]}...")
                        break
                except Exception as e:
                    print(f"✗ Error with {generator.__name__}: {e}")
        
        # Then try secondary generators to fill remaining slots
        all_generators = priority_generators + secondary_generators
        attempts = 0
        max_attempts = 200
        
        while len(questions) < 5 and attempts < max_attempts:
            generator = random.choice(all_generators)
            attempts += 1
            
            try:
                question = generator()
                if question and not self._is_duplicate_question(question, questions):
                    questions.append(question)
                    print(f"✓ Generated question {len(questions)}: {question['question'][:50]}...")
            except Exception as e:
                print(f"✗ Attempt {attempts}, Error with {generator.__name__}: {e}")
                continue
        
        print(f"Final quiz: {len(questions)} questions generated")
        
        # If we still don't have 5, create simpler versions
        if len(questions) < 5:
            questions.extend(self._generate_simple_questions(5 - len(questions)))
        
    def _create_simple_backup_question(self, question_index):
        """Create a simple backup question for a specific slot"""
        try:
            if question_index == 0:  # Temperature question
                cities_sample = random.sample(self.cities, min(4, len(self.cities)))
                city_temps = {}
                for city in cities_sample:
                    city_data = self.weather_data[self.weather_data['city'] == city]
                    avg_temp = city_data['temperature_2m_mean (°F)'].mean()
                    if not pd.isna(avg_temp):
                        city_temps[city] = avg_temp
                
                if len(city_temps) >= 2:
                    warmest_city = max(city_temps, key=city_temps.get)
                    choices = list(city_temps.keys())
                    random.shuffle(choices)
                    
                    return {
                        "question": "Which city has the highest average temperature?",
                        "choices": choices,
                        "correct_answer": warmest_city,
                        "explanation": f"{warmest_city} has the highest average temperature among these cities."
                    }
            
            elif question_index == 1:  # Rainfall question
                cities_sample = random.sample(self.cities, min(4, len(self.cities)))
                city_rain = {}
                for city in cities_sample:
                    city_data = self.weather_data[self.weather_data['city'] == city]
                    total_rain = city_data['rain_sum (inch)'].sum()
                    if not pd.isna(total_rain):
                        city_rain[city] = total_rain
                
                if len(city_rain) >= 2:
                    rainiest_city = max(city_rain, key=city_rain.get)
                    choices = list(city_rain.keys())
                    random.shuffle(choices)
                    
                    return {
                        "question": "Which city received the most total rainfall?",
                        "choices": choices,
                        "correct_answer": rainiest_city,
                        "explanation": f"{rainiest_city} received the most total rainfall among these cities."
                    }
            
            elif question_index == 2:  # Extreme temperature
                max_temp_record = self.weather_data.loc[self.weather_data['temperature_2m_max (°F)'].idxmax()]
                hottest_city = max_temp_record['city']
                other_cities = [c for c in self.cities if c != hottest_city]
                choices = [hottest_city] + random.sample(other_cities, min(3, len(other_cities)))
                random.shuffle(choices)
                
                return {
                    "question": "Which city recorded the highest temperature?",
                    "choices": choices,
                    "correct_answer": hottest_city,
                    "explanation": f"{hottest_city} recorded the highest temperature in the dataset."
                }
            
            elif question_index == 3:  # City climate (humidity if available)
                if 'relative_humidity_2m_mean (%)' in self.weather_data.columns:
                    city_humidity = self.weather_data.groupby('city')['relative_humidity_2m_mean (%)'].mean().dropna()
                    if len(city_humidity) >= 2:
                        most_humid_city = city_humidity.idxmax()
                        available_cities = list(city_humidity.index)
                        choices = [most_humid_city] + random.sample([c for c in available_cities if c != most_humid_city], min(3, len(available_cities)-1))
                        random.shuffle(choices)
                        
                        return {
                            "question": "Which city has the highest average humidity?",
                            "choices": choices,
                            "correct_answer": most_humid_city,
                            "explanation": f"{most_humid_city} has the highest average humidity."
                        }
            
            elif question_index == 4:  # Wind question
                if 'wind_speed_10m_max (mp/h)' in self.weather_data.columns:
                    city_wind = self.weather_data.groupby('city')['wind_speed_10m_max (mp/h)'].mean().dropna()
                    if len(city_wind) >= 2:
                        windiest_city = city_wind.idxmax()
                        available_cities = list(city_wind.index)
                        choices = [windiest_city] + random.sample([c for c in available_cities if c != windiest_city], min(3, len(available_cities)-1))
                        random.shuffle(choices)
                        
                        return {
                            "question": "Which city has the highest average wind speed?",
                            "choices": choices,
                            "correct_answer": windiest_city,
                            "explanation": f"{windiest_city} has the highest average wind speed."
                        }
            
            return None
            
        except Exception as e:
            print(f"Error creating backup question {question_index}: {e}")
            return None
    
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
            wrong_answers = [cooler_city]
            # Add other cities as wrong answers
            other_cities = [c for c in self.cities if c not in [city1, city2]]
            wrong_answers.extend(random.sample(other_cities, min(2, len(other_cities))))
            
            choices = [correct_answer] + wrong_answers[:3]
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"{warmer_city} has an average temperature of {city1_avg_c if warmer_city == city1 else city2_avg_c}°C, which is {temp_diff}°C warmer than {cooler_city} according to the dataset."
            }
            
        except Exception as e:
            return None
    
    def _generate_rainfall_analysis_question(self):
        """Generate questions about rainfall patterns from CSV data"""
        try:
            city_rainfall = self.weather_data.groupby('city')['rain_sum (inch)'].sum().sort_values(ascending=False)
            
            if len(city_rainfall) < 2:
                return None
            
            rainiest_city = city_rainfall.index[0]
            rainiest_amount = round(city_rainfall.iloc[0], 1)
            driest_city = city_rainfall.index[-1]
            driest_amount = round(city_rainfall.iloc[-1], 1)
            
            question_type = random.choice(['most_rain', 'least_rain'])
            
            if question_type == 'most_rain':
                question = f"According to the dataset, which city received the most total rainfall?"
                correct_answer = rainiest_city
                explanation = f"{rainiest_city} received {rainiest_amount} inches of total rainfall in the dataset, the highest amount recorded."
            else:
                question = f"According to the dataset, which city received the least total rainfall?"
                correct_answer = driest_city
                explanation = f"{driest_city} received only {driest_amount} inches of total rainfall in the dataset, the lowest amount recorded."
            
            # Use only cities from the dataset as choices
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
    
    def _generate_seasonal_pattern_question(self):
        """Generate questions about seasonal weather patterns from CSV data"""
        try:
            city = random.choice(self.cities)
            city_data = self.weather_data[self.weather_data['city'] == city]
            
            # Analyze seasonal temperatures
            seasonal_temps = city_data.groupby('season')['temperature_2m_mean (°F)'].mean()
            
            # Remove NaN values and check if we have enough data
            seasonal_temps = seasonal_temps.dropna()
            if len(seasonal_temps) < 2:
                return None
            
            # Convert to Celsius
            seasonal_temps_c = ((seasonal_temps - 32) * 5/9).round(1)
            
            question_type = random.choice(['hottest', 'coldest'])
            
            if question_type == 'hottest':
                target_season = seasonal_temps_c.idxmax()
                question = f"In {city}, which season has the highest average temperature according to the dataset?"
                explanation = f"In {city}, {target_season} has the highest average temperature at {seasonal_temps_c[target_season]}°C according to the weather data."
            else:
                target_season = seasonal_temps_c.idxmin()
                question = f"In {city}, which season has the lowest average temperature according to the dataset?"
                explanation = f"In {city}, {target_season} has the lowest average temperature at {seasonal_temps_c[target_season]}°C according to the weather data."
            
            correct_answer = target_season
            # Use all seasons as logical choices
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
            print(f"Error in seasonal pattern question: {e}")
            return None
    
    def _generate_extreme_weather_question(self):
        """Generate questions about extreme weather events from CSV data"""
        try:
            max_temp_record = self.weather_data.loc[self.weather_data['temperature_2m_max (°F)'].idxmax()]
            min_temp_record = self.weather_data.loc[self.weather_data['temperature_2m_min (°F)'].idxmin()]
            max_wind_record = self.weather_data.loc[self.weather_data['wind_speed_10m_max (mp/h)'].idxmax()]
            
            # Convert temperatures to Celsius
            max_temp_c = round((max_temp_record['temperature_2m_max (°F)'] - 32) * 5/9, 1)
            min_temp_c = round((min_temp_record['temperature_2m_min (°F)'] - 32) * 5/9, 1)
            max_wind_mph = round(max_wind_record['wind_speed_10m_max (mp/h)'], 1)
            
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
            
            # Use only cities from the dataset as choices
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
    
    def _generate_city_climate_question(self):
        """Generate questions about city climate characteristics from CSV data"""
        try:
            # Choose metric based on what's available in the data
            available_metrics = []
            
            if 'relative_humidity_2m_mean (%)' in self.weather_data.columns:
                available_metrics.append('humidity')
            if 'surface_pressure_mean (hPa)' in self.weather_data.columns:
                available_metrics.append('pressure')
            if 'cloud_cover_mean (%)' in self.weather_data.columns:
                available_metrics.append('cloud_cover')
            
            if not available_metrics:
                return None
                
            metric = random.choice(available_metrics)
            
            if metric == 'humidity':
                city_values = self.weather_data.groupby('city')['relative_humidity_2m_mean (%)'].mean()
                question = f"According to the dataset, which city has the highest average humidity?"
                unit = "%"
            elif metric == 'pressure':
                city_values = self.weather_data.groupby('city')['surface_pressure_mean (hPa)'].mean()
                question = f"According to the dataset, which city has the highest average atmospheric pressure?"
                unit = "hPa"
            else:
                city_values = self.weather_data.groupby('city')['cloud_cover_mean (%)'].mean()
                question = f"According to the dataset, which city has the highest average cloud cover?"
                unit = "%"
            
            # Remove NaN values
            city_values = city_values.dropna()
            
            if len(city_values) < 2:
                return None
            
            city_values_sorted = city_values.sort_values(ascending=False)
            top_city = city_values_sorted.index[0]
            top_value = round(city_values_sorted.iloc[0], 1)
            
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
            print(f"Error in city climate question: {e}")
            return None
    
    def _generate_humidity_wind_question(self):
        """Generate questions about humidity and wind patterns from CSV data"""
        try:
            question_type = None
            
            # Check what data is available
            has_humidity = 'relative_humidity_2m_mean (%)' in self.weather_data.columns
            has_wind = 'wind_speed_10m_max (mp/h)' in self.weather_data.columns
            
            if has_humidity and has_wind:
                question_type = random.choice(['lowest_humidity', 'highest_wind'])
            elif has_humidity:
                question_type = 'lowest_humidity'
            elif has_wind:
                question_type = 'highest_wind'
            else:
                return None
            
            if question_type == 'lowest_humidity':
                city_humidity = self.weather_data.groupby('city')['relative_humidity_2m_mean (%)'].mean()
                city_humidity = city_humidity.dropna()
                
                if len(city_humidity) < 2:
                    return None
                    
                driest_city = city_humidity.idxmin()
                humidity_value = round(city_humidity.min(), 1)
                
                question = f"According to the dataset, which city has the lowest average humidity?"
                correct_answer = driest_city
                explanation = f"{driest_city} has the lowest average humidity at {humidity_value}% in the dataset, indicating the driest climate."
                
                available_cities = list(city_humidity.index)
                
            else:  # highest_wind
                city_wind = self.weather_data.groupby('city')['wind_speed_10m_max (mp/h)'].mean()
                city_wind = city_wind.dropna()
                
                if len(city_wind) < 2:
                    return None
                    
                windiest_city = city_wind.idxmax()
                wind_value = round(city_wind.max(), 1)
                
                question = f"According to the dataset, which city experiences the highest average wind speeds?"
                correct_answer = windiest_city
                explanation = f"{windiest_city} has the highest average wind speeds at {wind_value} mph according to the dataset."
                
                available_cities = list(city_wind.index)
            
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
            print(f"Error in humidity/wind question: {e}")
            return None
    
    def _generate_weather_trend_question(self):
        """Generate questions about weather trends from CSV data"""
        try:
            city_temp_ranges = self.weather_data.groupby('city')['temp_range'].mean().sort_values(ascending=False)
            
            if len(city_temp_ranges) < 2:
                return None
            
            question_type = random.choice(['highest_range', 'lowest_range'])
            
            if question_type == 'highest_range':
                target_city = city_temp_ranges.index[0]
                range_value = round(city_temp_ranges.iloc[0], 1)
                question = f"According to the dataset, which city shows the greatest daily temperature variation?"
            else:
                target_city = city_temp_ranges.index[-1]
                range_value = round(city_temp_ranges.iloc[-1], 1)
                question = f"According to the dataset, which city shows the smallest daily temperature variation?"
            
            range_value_c = round(range_value * 5/9, 1)
            
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
    
    def _generate_pressure_analysis_question(self):
        """Generate questions about atmospheric pressure from CSV data"""
        try:
            city_pressure = self.weather_data.groupby('city')['surface_pressure_mean (hPa)'].mean().sort_values(ascending=False)
            
            if len(city_pressure) < 2:
                return None
            
            question_type = random.choice(['highest_pressure', 'lowest_pressure'])
            
            if question_type == 'highest_pressure':
                target_city = city_pressure.index[0]
                pressure_value = round(city_pressure.iloc[0], 1)
                question = f"According to the dataset, which city has the highest average atmospheric pressure?"
            else:
                target_city = city_pressure.index[-1]
                pressure_value = round(city_pressure.iloc[-1], 1)
                question = f"According to the dataset, which city has the lowest average atmospheric pressure?"
            
            correct_answer = target_city
            wrong_answers = [city for city in self.cities if city != target_city][:3]
            
            choices = [correct_answer] + wrong_answers
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"{target_city} has an average atmospheric pressure of {pressure_value} hPa according to the dataset."
            }
            
        except Exception as e:
            return None
    
    def _generate_snowfall_comparison_question(self):
        """Generate questions about snowfall from CSV data"""
        try:
            city_snowfall = self.weather_data.groupby('city')['snowfall_sum (inch)'].sum().sort_values(ascending=False)
            
            if len(city_snowfall) < 2 or city_snowfall.iloc[0] == 0:
                return None
            
            snowiest_city = city_snowfall.index[0]
            snowfall_amount = round(city_snowfall.iloc[0], 1)
            
            question = f"According to the dataset, which city received the most total snowfall?"
            
            correct_answer = snowiest_city
            wrong_answers = [city for city in self.cities if city != snowiest_city][:3]
            
            choices = [correct_answer] + wrong_answers
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"{snowiest_city} received {snowfall_amount} inches of total snowfall according to the dataset."
            }
            
        except Exception as e:
            return None
    
    def _generate_sunshine_duration_question(self):
        """Generate questions about sunshine duration from CSV data"""
        try:
            city_sunshine = self.weather_data.groupby('city')['sunshine_duration (s)'].mean().sort_values(ascending=False)
            
            if len(city_sunshine) < 2:
                return None
            
            question_type = random.choice(['most_sunshine', 'least_sunshine'])
            
            if question_type == 'most_sunshine':
                target_city = city_sunshine.index[0]
                sunshine_hours = round(city_sunshine.iloc[0] / 3600, 1)
                question = f"According to the dataset, which city has the most average daily sunshine?"
            else:
                target_city = city_sunshine.index[-1]
                sunshine_hours = round(city_sunshine.iloc[-1] / 3600, 1)
                question = f"According to the dataset, which city has the least average daily sunshine?"
            
            correct_answer = target_city
            wrong_answers = [city for city in self.cities if city != target_city][:3]
            
            choices = [correct_answer] + wrong_answers
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"{target_city} averages {sunshine_hours} hours of sunshine per day according to the dataset."
            }
            
        except Exception as e:
            return None
    
    def _generate_cloud_cover_question(self):
        """Generate questions about cloud cover from CSV data"""
        try:
            city_clouds = self.weather_data.groupby('city')['cloud_cover_mean (%)'].mean().sort_values(ascending=False)
            
            if len(city_clouds) < 2:
                return None
            
            question_type = random.choice(['most_cloudy', 'least_cloudy'])
            
            if question_type == 'most_cloudy':
                target_city = city_clouds.index[0]
                cloud_value = round(city_clouds.iloc[0], 1)
                question = f"According to the dataset, which city has the highest average cloud cover?"
            else:
                target_city = city_clouds.index[-1]
                cloud_value = round(city_clouds.iloc[-1], 1)
                question = f"According to the dataset, which city has the lowest average cloud cover?"
            
            correct_answer = target_city
            wrong_answers = [city for city in self.cities if city != target_city][:3]
            
            choices = [correct_answer] + wrong_answers
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"{target_city} has {cloud_value}% average cloud cover according to the dataset."
            }
            
        except Exception as e:
            return None
    
    def _generate_temperature_range_question(self):
        """Generate questions about temperature extremes from CSV data"""
        try:
            # Find city with highest max temperature vs city with lowest min temperature
            max_temp_city = self.weather_data.loc[self.weather_data['temperature_2m_max (°F)'].idxmax(), 'city']
            min_temp_city = self.weather_data.loc[self.weather_data['temperature_2m_min (°F)'].idxmin(), 'city']
            max_temp_value = round((self.weather_data['temperature_2m_max (°F)'].max() - 32) * 5/9, 1)
            min_temp_value = round((self.weather_data['temperature_2m_min (°F)'].min() - 32) * 5/9, 1)
            
            question_type = random.choice(['hottest_day', 'coldest_day'])
            
            if question_type == 'hottest_day':
                question = f"According to the dataset, which city experienced the single hottest day?"
                correct_answer = max_temp_city
                explanation = f"{max_temp_city} recorded the highest single-day temperature of {max_temp_value}°C in the dataset."
            else:
                question = f"According to the dataset, which city experienced the single coldest day?"
                correct_answer = min_temp_city
                explanation = f"{min_temp_city} recorded the lowest single-day temperature of {min_temp_value}°C in the dataset."
            
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
    
    def _generate_monthly_pattern_question(self):
        """Generate questions about monthly weather patterns from CSV data"""
        try:
            city = random.choice(self.cities)
            city_data = self.weather_data[self.weather_data['city'] == city]
            
            metric = random.choice(['temperature', 'rainfall'])
            
            if metric == 'temperature':
                monthly_values = city_data.groupby('month')['temperature_2m_mean (°F)'].mean()
                monthly_values = monthly_values.dropna()  # Remove NaN values
                
                if len(monthly_values) < 2:
                    return None
                
                question_type = random.choice(['hottest_month', 'coldest_month'])
                month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                              'July', 'August', 'September', 'October', 'November', 'December']
                
                if question_type == 'hottest_month':
                    target_month = monthly_values.idxmax()
                    question = f"In {city}, which month has the highest average temperature according to the dataset?"
                else:
                    target_month = monthly_values.idxmin()
                    question = f"In {city}, which month has the lowest average temperature according to the dataset?"
                
                correct_answer = month_names[target_month]
                # Use logical months as choices - focus on seasons
                if question_type == 'hottest_month':
                    logical_choices = ['June', 'July', 'August', 'September']
                else:
                    logical_choices = ['December', 'January', 'February', 'March']
                
                wrong_answers = [month for month in logical_choices if month != correct_answer]
                
            else:  # rainfall
                monthly_values = city_data.groupby('month')['rain_sum (inch)'].sum()
                monthly_values = monthly_values.dropna()  # Remove NaN values
                
                if len(monthly_values) < 2:
                    return None
                
                wettest_month = monthly_values.idxmax()
                month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                              'July', 'August', 'September', 'October', 'November', 'December']
                
                question = f"In {city}, which month received the most rainfall according to the dataset?"
                correct_answer = month_names[wettest_month]
                
                # Use logical wet season months
                logical_choices = ['April', 'May', 'June', 'July', 'August', 'September', 'October']
                wrong_answers = [month for month in logical_choices if month != correct_answer][:3]
            
            choices = [correct_answer] + wrong_answers[:3]
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"According to the dataset, {correct_answer} shows the pattern described for {city}."
            }
            
        except Exception as e:
            print(f"Error in monthly pattern question: {e}")
            return None
    
    def _generate_wettest_driest_question(self):
        """Generate questions comparing wet vs dry periods from CSV data"""
        try:
            # Find the wettest and driest days across all data
            wettest_record = self.weather_data.loc[self.weather_data['rain_sum (inch)'].idxmax()]
            driest_records = self.weather_data[self.weather_data['rain_sum (inch)'] == 0]
            
            if driest_records.empty:
                return None
            
            wettest_city = wettest_record['city']
            wettest_amount = round(wettest_record['rain_sum (inch)'], 2)
            
            # Count dry days per city
            dry_days_per_city = driest_records.groupby('city').size().sort_values(ascending=False)
            driest_city = dry_days_per_city.index[0]
            dry_days_count = dry_days_per_city.iloc[0]
            
            question_type = random.choice(['wettest_day', 'most_dry_days'])
            
            if question_type == 'wettest_day':
                question = f"According to the dataset, which city recorded the highest single-day rainfall?"
                correct_answer = wettest_city
                explanation = f"{wettest_city} recorded the highest single-day rainfall of {wettest_amount} inches in the dataset."
            else:
                question = f"According to the dataset, which city had the most days with no rainfall?"
                correct_answer = driest_city
                explanation = f"{driest_city} had {dry_days_count} days with no rainfall according to the dataset."
            
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
    
    def _generate_wind_direction_question(self):
        """Generate questions about wind patterns from CSV data"""
        try:
            # Analyze wind speeds by city and season
            city_wind_by_season = self.weather_data.groupby(['city', 'season'])['wind_speed_10m_max (mp/h)'].mean().unstack(fill_value=0)
            
            if city_wind_by_season.empty:
                return None
            
            # Find which city has windiest season
            windiest_overall = city_wind_by_season.stack().idxmax()
            windiest_city = windiest_overall[0]
            windiest_season = windiest_overall[1]
            wind_speed = round(city_wind_by_season.loc[windiest_city, windiest_season], 1)
            
            question = f"According to the dataset, which city experiences its windiest conditions during {windiest_season}?"
            
            # Find cities that actually have data for that season
            cities_in_season = city_wind_by_season[city_wind_by_season[windiest_season] > 0].index.tolist()
            
            if len(cities_in_season) < 2:
                return None
            
            correct_answer = windiest_city
            wrong_answers = [city for city in cities_in_season if city != correct_answer][:3]
            
            choices = [correct_answer] + wrong_answers
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": f"{windiest_city} experiences its windiest conditions during {windiest_season} with average winds of {wind_speed} mph according to the dataset."
            }
            
        except Exception as e:
            return None
    
    def get_data_stats(self):
        """Get statistics about the loaded data"""
        if not self.data_loaded or self.weather_data is None:
            return {
                "data_available": False,
                "message": "No weather data available - quiz cannot be generated"
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
            "quiz_capability": "csv_data_only"
        }
        
        return stats
    
    def validate_data_quality(self):
        """Validate the quality of loaded data for quiz generation"""
        if not self.data_loaded:
            return {"quality": "none", "issues": ["No CSV data loaded - quiz cannot be generated"]}
        
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
    
    def get_all_possible_questions(self):
        """Generate and return all possible question types that can be created from the CSV data"""
        if not self.data_loaded or self.weather_data is None:
            return []
        
        all_questions = []
        question_generators = [
            ("Temperature Comparison", self._generate_temperature_comparison_question),
            ("Rainfall Analysis", self._generate_rainfall_analysis_question),
            ("Seasonal Patterns", self._generate_seasonal_pattern_question),
            ("Extreme Weather", self._generate_extreme_weather_question),
            ("City Climate", self._generate_city_climate_question),
            ("Humidity & Wind", self._generate_humidity_wind_question),
            ("Weather Trends", self._generate_weather_trend_question),
            ("Pressure Analysis", self._generate_pressure_analysis_question),
            ("Snowfall Comparison", self._generate_snowfall_comparison_question),
            ("Sunshine Duration", self._generate_sunshine_duration_question),
            ("Cloud Cover", self._generate_cloud_cover_question),
            ("Temperature Extremes", self._generate_temperature_range_question),
            ("Monthly Patterns", self._generate_monthly_pattern_question),
            ("Wet vs Dry", self._generate_wettest_driest_question),
            ("Wind Patterns", self._generate_wind_direction_question)
        ]
        
        print(f"\nGenerating all possible questions from CSV data for {len(self.cities)} cities:")
        print(f"Cities in dataset: {', '.join(self.cities)}")
        print(f"Total records: {len(self.weather_data)}")
        print("=" * 60)
        
        for category_name, generator in question_generators:
            print(f"\n{category_name} Questions:")
            print("-" * 30)
            
            # Generate multiple variations of each question type
            for attempt in range(10):  # Try to generate 10 variations per type
                try:
                    question = generator()
                    if question:
                        # Check if this exact question already exists
                        if not any(q['question'] == question['question'] for q in all_questions):
                            all_questions.append({
                                'category': category_name,
                                'question': question['question'],
                                'choices': question['choices'],
                                'correct_answer': question['correct_answer'],
                                'explanation': question['explanation']
                            })
                            print(f"✓ {question['question']}")
                        else:
                            print(f"⚠ Duplicate question skipped")
                except Exception as e:
                    print(f"✗ Error generating question: {e}")
        
        print(f"\n" + "=" * 60)
        print(f"Total unique questions generated: {len(all_questions)}")
        
        # Group by category
        by_category = {}
        for q in all_questions:
            category = q['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(q)
        
        print(f"\nQuestions by category:")
        for category, questions in by_category.items():
            print(f"  {category}: {len(questions)} questions")
        
        return all_questions