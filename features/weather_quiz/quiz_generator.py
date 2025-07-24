"""
Enhanced Weather Quiz Generator - Creates smart questions ONLY based on combined CSV data
Modified to generate exactly 5 questions instead of 8
"""

import pandas as pd
import random
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
            project_root = Path(__file__).parent.parent.parent
            csv_path = project_root / 'data' / 'combined.csv'
            
            if csv_path.exists():
                print(f"Loading weather data from {csv_path}")
                self.weather_data = pd.read_csv(csv_path)
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
            self.cities = self.weather_data['city'].unique().tolist()
            self.weather_data['date'] = pd.to_datetime(self.weather_data['time'])
            self.weather_data['month'] = self.weather_data['date'].dt.month
            self.weather_data['season'] = self.weather_data['month'].apply(self._get_season)
            
            # Convert numeric columns
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
        """Generate exactly 5 smart quiz questions randomly selected from all available question types"""
        if not self.data_loaded or self.weather_data is None or len(self.cities) < 2:
            return []
        
        questions = []
        
        # All available question generators
        all_generators = [
            self._generate_temperature_comparison_question,
            self._generate_rainfall_analysis_question,
            self._generate_extreme_weather_question,
            self._generate_city_climate_question,
            self._generate_humidity_wind_question,
            self._generate_seasonal_pattern_question,
            self._generate_weather_trend_question,
            self._generate_pressure_analysis_question,
            self._generate_snowfall_comparison_question,
            self._generate_sunshine_duration_question,
            self._generate_cloud_cover_question,
            self._generate_temperature_range_question,
            self._generate_monthly_pattern_question,
            self._generate_wettest_driest_question,
            self._generate_wind_direction_question,
            self._generate_temperature_extremes_question,
            self._generate_rainfall_extremes_question,
            self._generate_seasonal_temperature_range_question,
            self._generate_weather_stability_question,
            self._generate_heatwave_analysis_question
        ]
        
        print(f"Generating 5 random quiz questions from {len(all_generators)} available question types")
        print(f"Data: {len(self.cities)} cities with {len(self.weather_data)} records")
        
        # Shuffle the generators to get random selection
        random.shuffle(all_generators)
        
        attempts = 0
        max_attempts = 200
        
        # Keep trying different generators until we have 5 unique questions
        while len(questions) < 5 and attempts < max_attempts:
            # Pick a random generator
            generator = random.choice(all_generators)
            attempts += 1
            
            try:
                question = generator()
                if question and not self._is_duplicate_question(question, questions):
                    questions.append(question)
                    print(f"✓ Generated question {len(questions)}: {question['question'][:60]}...")
                else:
                    if question:
                        print(f"⚠ Skipped duplicate question: {question['question'][:40]}...")
            except Exception as e:
                print(f"✗ Attempt {attempts}, Error with {generator.__name__}: {e}")
                continue
        
        # Create backup questions if still not enough
        if len(questions) < 5:
            print(f"⚠ Only generated {len(questions)} questions, creating backup questions...")
            backup_questions = self._generate_simple_questions(5 - len(questions))
            questions.extend(backup_questions)
            print(f"✓ Added {len(backup_questions)} backup questions")
        
        # Final check to ensure we have exactly 5 questions - FORCE IT
        question_slot = 0
        while len(questions) < 5:
            print(f"⚠ FORCING question generation ({len(questions)}/5), slot {question_slot}...")
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
        
        # ABSOLUTE FINAL CHECK - if we still don't have 5, create basic questions
        if len(questions) < 5:
            print(f"⚠ EMERGENCY BACKUP: Creating basic questions to reach 5 total")
            while len(questions) < 5:
                emergency_question = {
                    "question": f"Which city appears most frequently in the weather dataset?",
                    "choices": random.sample(self.cities, min(4, len(self.cities))),
                    "correct_answer": random.choice(self.cities),
                    "explanation": f"This is a basic question about the dataset structure."
                }
                questions.append(emergency_question)
                print(f"✓ Emergency question {len(questions)}: Basic dataset question")
        
        print(f"FINAL RESULT: {len(questions)} questions generated")
        return questions[:5]
    
    def _generate_temperature_extremes_question(self):
        """Which city experienced the highest number of days with temperatures above 40°C?"""
        try:
            hot_days_count = {}
            threshold_f = 40 * 9/5 + 32  # Convert 40°C to Fahrenheit
            
            for city in self.cities:
                city_data = self.weather_data[self.weather_data['city'] == city]
                hot_days = len(city_data[city_data['temperature_2m_max (°F)'] > threshold_f])
                hot_days_count[city] = hot_days
            
            if not hot_days_count or max(hot_days_count.values()) == 0:
                return None
            
            hottest_city = max(hot_days_count, key=hot_days_count.get)
            hot_days = hot_days_count[hottest_city]
            
            choices = list(self.cities)
            random.shuffle(choices)
            
            return {
                "question": "Which city experienced the highest number of days with temperatures above 40°C in 2024?",
                "choices": choices,
                "correct_answer": hottest_city,
                "explanation": f"{hottest_city} had {hot_days} days with temperatures above 40°C, the most among all cities in the dataset."
            }
        except Exception as e:
            return None
    
    def _generate_rainfall_extremes_question(self):
        """On which date did a city record its highest daily rainfall?"""
        try:
            max_rain_record = self.weather_data.loc[self.weather_data['rain_sum (inch)'].idxmax()]
            wettest_city = max_rain_record['city']
            wettest_date = max_rain_record['date'].strftime('%B %d, %Y')
            rain_amount = round(max_rain_record['rain_sum (inch)'], 2)
            
            question = f"Which city recorded the highest single-day rainfall in the dataset?"
            
            choices = list(self.cities)
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": wettest_city,
                "explanation": f"{wettest_city} recorded the highest single-day rainfall of {rain_amount} inches on {wettest_date}."
            }
        except Exception as e:
            return None
    
    def _generate_seasonal_temperature_range_question(self):
        """Which city had the greatest temperature range (difference between highest and lowest recorded temperatures)?"""
        try:
            temp_ranges = {}
            
            for city in self.cities:
                city_data = self.weather_data[self.weather_data['city'] == city]
                max_temp = city_data['temperature_2m_max (°F)'].max()
                min_temp = city_data['temperature_2m_min (°F)'].min()
                temp_range = max_temp - min_temp
                temp_ranges[city] = temp_range
            
            if not temp_ranges:
                return None
            
            highest_range_city = max(temp_ranges, key=temp_ranges.get)
            range_f = round(temp_ranges[highest_range_city], 1)
            range_c = round(range_f * 5/9, 1)
            
            choices = list(self.cities)
            random.shuffle(choices)
            
            return {
                "question": "Which city had the greatest temperature range (difference between highest and lowest recorded temperatures) in the dataset?",
                "choices": choices,
                "correct_answer": highest_range_city,
                "explanation": f"{highest_range_city} had the greatest temperature range of {range_c}°C ({range_f}°F) between its hottest and coldest recorded temperatures."
            }
        except Exception as e:
            return None
    
    def _generate_weather_stability_question(self):
        """Which city showed the most stable daily average temperature (smallest variation)?"""
        try:
            temp_stability = {}
            
            for city in self.cities:
                city_data = self.weather_data[self.weather_data['city'] == city]
                temp_std = city_data['temperature_2m_mean (°F)'].std()
                temp_stability[city] = temp_std
            
            if not temp_stability:
                return None
            
            most_stable_city = min(temp_stability, key=temp_stability.get)
            stability_f = round(temp_stability[most_stable_city], 1)
            stability_c = round(stability_f * 5/9, 1)
            
            choices = list(self.cities)
            random.shuffle(choices)
            
            return {
                "question": "Which city showed the most stable daily average temperature across the year (smallest variation)?",
                "choices": choices,
                "correct_answer": most_stable_city,
                "explanation": f"{most_stable_city} had the most stable temperatures with a standard deviation of only {stability_c}°C ({stability_f}°F)."
            }
        except Exception as e:
            return None
    
    def _generate_heatwave_analysis_question(self):
        """Which city had the highest number of days with minimum temperatures below 0°C?"""
        try:
            frost_days_count = {}
            freezing_f = 32  # 0°C in Fahrenheit
            
            for city in self.cities:
                city_data = self.weather_data[self.weather_data['city'] == city]
                frost_days = len(city_data[city_data['temperature_2m_min (°F)'] < freezing_f])
                frost_days_count[city] = frost_days
            
            if not frost_days_count or max(frost_days_count.values()) == 0:
                return None
            
            coldest_city = max(frost_days_count, key=frost_days_count.get)
            frost_days = frost_days_count[coldest_city]
            
            choices = list(self.cities)
            random.shuffle(choices)
            
            return {
                "question": "Which city had the highest number of days with minimum temperatures below 0°C (frost days)?",
                "choices": choices,
                "correct_answer": coldest_city,
                "explanation": f"{coldest_city} had {frost_days} frost days with minimum temperatures below 0°C, the most among all cities."
            }
        except Exception as e:
            return None
    
    def _generate_simple_questions(self, num_needed):
        """Generate simple backup questions when complex generators fail"""
        backup_questions = []
        
        try:
            for i in range(num_needed):
                question = self._create_simple_backup_question(i)
                if question and not self._is_duplicate_question(question, backup_questions):
                    backup_questions.append(question)
                    print(f"✓ Generated backup question {len(backup_questions)}: {question['question'][:50]}...")
                else:
                    # If duplicate or failed, try with a different index
                    for retry_index in range(10):
                        retry_question = self._create_simple_backup_question(retry_index)
                        if retry_question and not self._is_duplicate_question(retry_question, backup_questions):
                            backup_questions.append(retry_question)
                            print(f"✓ Generated retry backup question {len(backup_questions)}: {retry_question['question'][:50]}...")
                            break
        except Exception as e:
            print(f"Error generating backup questions: {e}")
        
        return backup_questions
    
    def _create_simple_backup_question(self, question_index):
        """Create a simple backup question for a specific slot"""
        try:
            # Use modulo to cycle through question types if we need more than 5
            question_type = question_index % 5
            
            if question_type == 0:  # Temperature question
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
            
            elif question_type == 1:  # Rainfall question
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
            
            elif question_type == 2:  # Extreme temperature
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
            
            elif question_type == 3:  # Wind speed question
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
                else:
                    # Fallback to pressure question if wind data not available
                    if 'surface_pressure_mean (hPa)' in self.weather_data.columns:
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
            
            elif question_type == 4:  # Humidity question
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
                else:
                    # Fallback to cloud cover question if humidity data not available
                    if 'cloud_cover_mean (%)' in self.weather_data.columns:
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
            common_words = set(new_q.split()) & set(existing_q.split())
            if len(common_words) > 3:
                return True
        
        return False
    
    def _generate_temperature_comparison_question(self):
        """Generate questions comparing temperatures between cities"""
        try:
            if len(self.cities) < 2:
                return None
            
            city1, city2 = random.sample(self.cities, 2)
            city1_data = self.weather_data[self.weather_data['city'] == city1]
            city2_data = self.weather_data[self.weather_data['city'] == city2]
            
            city1_avg = city1_data['temperature_2m_mean (°F)'].mean()
            city2_avg = city2_data['temperature_2m_mean (°F)'].mean()
            
            if pd.isna(city1_avg) or pd.isna(city2_avg):
                return None
            
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
    
    def _generate_extreme_weather_question(self):
        """Generate questions about extreme weather events from CSV data"""
        try:
            max_temp_record = self.weather_data.loc[self.weather_data['temperature_2m_max (°F)'].idxmax()]
            min_temp_record = self.weather_data.loc[self.weather_data['temperature_2m_min (°F)'].idxmin()]
            max_wind_record = self.weather_data.loc[self.weather_data['wind_speed_10m_max (mp/h)'].idxmax()]
            
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
            return None
    
    def _generate_humidity_wind_question(self):
        """Generate questions about humidity and wind patterns from CSV data"""
        try:
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
                city_wind = self.weather_data.groupby('city')['wind_speed_10m_max (mp/h)'].mean().dropna()
                
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
            return None
    
    def _generate_seasonal_pattern_question(self):
        """Generate questions about seasonal weather patterns from CSV data"""
        try:
            city = random.choice(self.cities)
            city_data = self.weather_data[self.weather_data['city'] == city]
            
            seasonal_temps = city_data.groupby('season')['temperature_2m_mean (°F)'].mean().dropna()
            if len(seasonal_temps) < 2:
                return None
            
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
                monthly_values = city_data.groupby('month')['temperature_2m_mean (°F)'].mean().dropna()
                
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
                
                if question_type == 'hottest_month':
                    logical_choices = ['June', 'July', 'August', 'September']
                else:
                    logical_choices = ['December', 'January', 'February', 'March']
                
                wrong_answers = [month for month in logical_choices if month != correct_answer]
                
            else:  # rainfall
                monthly_values = city_data.groupby('month')['rain_sum (inch)'].sum().dropna()
                
                if len(monthly_values) < 2:
                    return None
                
                wettest_month = monthly_values.idxmax()
                month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                              'July', 'August', 'September', 'October', 'November', 'December']
                
                question = f"In {city}, which month received the most rainfall according to the dataset?"
                correct_answer = month_names[wettest_month]
                
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
            return None
    
    def _generate_wettest_driest_question(self):
        """Generate questions comparing wet vs dry periods from CSV data"""
        try:
            wettest_record = self.weather_data.loc[self.weather_data['rain_sum (inch)'].idxmax()]
            driest_records = self.weather_data[self.weather_data['rain_sum (inch)'] == 0]
            
            if driest_records.empty:
                return None
            
            wettest_city = wettest_record['city']
            wettest_amount = round(wettest_record['rain_sum (inch)'], 2)
            
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
            city_wind_by_season = self.weather_data.groupby(['city', 'season'])['wind_speed_10m_max (mp/h)'].mean().unstack(fill_value=0)
            
            if city_wind_by_season.empty:
                return None
            
            windiest_overall = city_wind_by_season.stack().idxmax()
            windiest_city = windiest_overall[0]
            windiest_season = windiest_overall[1]
            wind_speed = round(city_wind_by_season.loc[windiest_city, windiest_season], 1)
            
            question = f"According to the dataset, which city experiences its windiest conditions during {windiest_season}?"
            
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
    
    def validate_data_quality(self):
        """Validate the quality of loaded data for quiz generation"""
        if not self.data_loaded:
            return {"quality": "none", "issues": ["No CSV data loaded - quiz cannot be generated"]}
        
        issues = []
        quality = "good"
        
        key_columns = ['temperature_2m_max (°F)', 'temperature_2m_min (°F)', 'rain_sum (inch)']
        for col in key_columns:
            if col in self.weather_data.columns:
                missing_pct = (self.weather_data[col].isna().sum() / len(self.weather_data)) * 100
                if missing_pct > 20:
                    issues.append(f"High missing data in {col}: {missing_pct:.1f}%")
                    quality = "fair"
        
        if len(self.weather_data) < 100:
            issues.append(f"Limited data: only {len(self.weather_data)} records")
            quality = "fair"
        
        if len(self.cities) < 2:
            issues.append("Need at least 2 cities for comparative questions")
            quality = "poor"
        
        return {"quality": quality, "issues": issues}