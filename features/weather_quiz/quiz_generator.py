"""
Weather Quiz Generator - Creates smart, fun questions based on real weather data
"""

import pandas as pd
import random
import os
from datetime import datetime, timedelta
from config.storage import load_weather_history


class WeatherQuizGenerator:
    """
    Generates intelligent weather quiz questions based on real data analysis
    """
    
    def __init__(self):
        self.weather_data = None
        self.ahmedabad_data = None
        self._load_data()
    
    def _load_data(self):
        """Load weather data from CSV files"""
        try:
            # Load search history data
            self.weather_data = load_weather_history()
            
            # Load Ahmedabad data if available
            ahmedabad_path = os.path.join(os.path.dirname(__file__), '../../data/Ahmedabad.csv')
            if os.path.exists(ahmedabad_path):
                self.ahmedabad_data = pd.read_csv(ahmedabad_path)
            
        except Exception as e:
            # Use fallback data if loading fails
            self.weather_data = []
            self.ahmedabad_data = None
    
    def generate_quiz(self):
        """Generate 5 smart quiz questions"""
        questions = []
        
        # Ensure we have a good mix of question types
        question_generators = [
            self._generate_temperature_comparison_question,
            self._generate_seasonal_pattern_question,
            self._generate_weather_condition_frequency_question,
            self._generate_temperature_range_question,
            self._generate_weather_trend_question
        ]
        
        # Shuffle to ensure variety
        random.shuffle(question_generators)
        
        for generator in question_generators:
            try:
                question = generator()
                if question:
                    questions.append(question)
            except Exception as e:
                # If a question fails, generate a fallback
                fallback = self._generate_fallback_question()
                if fallback:
                    questions.append(fallback)
        
        # Ensure we have exactly 5 questions
        while len(questions) < 5:
            fallback = self._generate_fallback_question()
            if fallback:
                questions.append(fallback)
        
        return questions[:5]
    
    def _generate_temperature_comparison_question(self):
        """Generate a question comparing temperatures across different periods"""
        try:
            if self.ahmedabad_data is not None and len(self.ahmedabad_data) > 50:
                # Use Ahmedabad data for temperature analysis
                data = self.ahmedabad_data
                
                # Convert temperature columns to numeric, handle errors
                data['temp_max_c'] = pd.to_numeric(data['temperature_2m_max (°F)'], errors='coerce')
                data['temp_max_c'] = (data['temp_max_c'] - 32) * 5/9  # Convert F to C
                
                # Get data for different months
                data['month'] = pd.to_datetime(data['time']).dt.month
                
                # Compare summer (May-July) vs winter (December-February)
                summer_temps = data[data['month'].isin([5, 6, 7])]['temp_max_c'].dropna()
                winter_temps = data[data['month'].isin([12, 1, 2])]['temp_max_c'].dropna()
                
                if len(summer_temps) > 5 and len(winter_temps) > 5:
                    summer_avg = round(summer_temps.mean(), 1)
                    winter_avg = round(winter_temps.mean(), 1)
                    temp_diff = round(summer_avg - winter_avg, 1)
                    
                    question = f"Based on Ahmedabad's weather data, what's the approximate difference between average summer and winter maximum temperatures?"
                    
                    correct_answer = f"{temp_diff}°C"
                    wrong_answers = [
                        f"{temp_diff + 5}°C",
                        f"{temp_diff - 3}°C", 
                        f"{temp_diff + 8}°C"
                    ]
                    
                    choices = [correct_answer] + wrong_answers
                    random.shuffle(choices)
                    
                    return {
                        "question": question,
                        "choices": choices,
                        "correct_answer": correct_answer,
                        "explanation": f"Analysis of the data shows summer temperatures average {summer_avg}°C while winter averages {winter_avg}°C, giving a difference of {temp_diff}°C."
                    }
            
            # Fallback to search history data
            if len(self.weather_data) > 10:
                temps = []
                for record in self.weather_data:
                    try:
                        temp = float(record.get('temperature', 0))
                        temps.append(temp)
                    except (ValueError, TypeError):
                        continue
                
                if len(temps) > 5:
                    avg_temp = round(sum(temps) / len(temps), 1)
                    max_temp = round(max(temps), 1)
                    
                    question = f"Based on your weather search history, what's the average temperature you've looked up?"
                    
                    correct_answer = f"{avg_temp}°C"
                    wrong_answers = [f"{avg_temp + 3}°C", f"{avg_temp - 2}°C", f"{avg_temp + 7}°C"]
                    
                    choices = [correct_answer] + wrong_answers
                    random.shuffle(choices)
                    
                    return {
                        "question": question,
                        "choices": choices,
                        "correct_answer": correct_answer,
                        "explanation": f"Your search history shows an average temperature of {avg_temp}°C across all locations you've checked."
                    }
            
            return None
            
        except Exception as e:
            return None
    
    def _generate_seasonal_pattern_question(self):
        """Generate a question about seasonal weather patterns"""
        try:
            if self.ahmedabad_data is not None and len(self.ahmedabad_data) > 100:
                data = self.ahmedabad_data
                
                # Analyze precipitation patterns
                data['month'] = pd.to_datetime(data['time']).dt.month
                monthly_rain = data.groupby('month')['rain_sum (inch)'].mean()
                
                # Find rainiest month
                rainiest_month = monthly_rain.idxmax()
                month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 
                             5: 'May', 6: 'June', 7: 'July', 8: 'August',
                             9: 'September', 10: 'October', 11: 'November', 12: 'December'}
                
                rainiest_name = month_names[rainiest_month]
                
                question = "Based on Ahmedabad's weather data, which month typically receives the most rainfall?"
                
                correct_answer = rainiest_name
                wrong_options = ['April', 'November', 'February', 'May']
                wrong_answers = [month for month in wrong_options if month != rainiest_name][:3]
                
                choices = [correct_answer] + wrong_answers
                random.shuffle(choices)
                
                return {
                    "question": question,
                    "choices": choices,
                    "correct_answer": correct_answer,
                    "explanation": f"Data analysis shows {rainiest_name} receives the highest average rainfall, which aligns with monsoon patterns in this region."
                }
            
            # Fallback question about general seasonal patterns
            question = "In most temperate climates, which season typically has the highest temperature variability (difference between day and night)?"
            
            correct_answer = "Spring"
            wrong_answers = ["Summer", "Winter", "Autumn"]
            
            choices = [correct_answer] + wrong_answers
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": "Spring often has the highest temperature variability due to transitional weather patterns and varying day lengths."
            }
            
        except Exception as e:
            return None
    
    def _generate_weather_condition_frequency_question(self):
        """Generate a question about weather condition frequencies"""
        try:
            if len(self.weather_data) > 15:
                # Analyze weather conditions from search history
                conditions = {}
                for record in self.weather_data:
                    condition = record.get('description', '').lower()
                    if condition:
                        conditions[condition] = conditions.get(condition, 0) + 1
                
                if len(conditions) > 2:
                    most_common = max(conditions.items(), key=lambda x: x[1])
                    condition_name = most_common[0].title()
                    frequency = most_common[1]
                    
                    question = f"Based on your weather search history, which condition appeared most frequently?"
                    
                    correct_answer = condition_name
                    
                    # Generate wrong answers from other conditions or common weather types
                    other_conditions = [cond for cond in conditions.keys() if cond != most_common[0]]
                    wrong_answers = [cond.title() for cond in other_conditions[:3]]
                    
                    # Fill with common weather types if needed
                    common_weather = ['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy']
                    while len(wrong_answers) < 3:
                        for weather in common_weather:
                            if weather not in wrong_answers and weather != correct_answer:
                                wrong_answers.append(weather)
                                break
                        break
                    
                    choices = [correct_answer] + wrong_answers[:3]
                    random.shuffle(choices)
                    
                    return {
                        "question": question,
                        "choices": choices,
                        "correct_answer": correct_answer,
                        "explanation": f"'{condition_name}' appeared {frequency} times in your search history, making it the most common condition you've looked up."
                    }
            
            # Fallback question about weather condition patterns
            question = "Globally, what percentage of days are typically classified as 'clear sky' or 'sunny'?"
            
            correct_answer = "About 25-30%"
            wrong_answers = ["About 50-60%", "About 10-15%", "About 70-80%"]
            
            choices = [correct_answer] + wrong_answers
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": "Most locations experience a mix of weather conditions, with truly clear days making up roughly 25-30% of the year on average."
            }
            
        except Exception as e:
            return None
    
    def _generate_temperature_range_question(self):
        """Generate a question about temperature ranges and variability"""
        try:
            if self.ahmedabad_data is not None and len(self.ahmedabad_data) > 50:
                data = self.ahmedabad_data
                
                # Calculate temperature ranges
                data['temp_max_c'] = pd.to_numeric(data['temperature_2m_max (°F)'], errors='coerce')
                data['temp_min_c'] = pd.to_numeric(data['temperature_2m_min (°F)'], errors='coerce')
                data['temp_max_c'] = (data['temp_max_c'] - 32) * 5/9  # Convert F to C
                data['temp_min_c'] = (data['temp_min_c'] - 32) * 5/9  # Convert F to C
                
                data['temp_range'] = data['temp_max_c'] - data['temp_min_c']
                avg_range = data['temp_range'].mean()
                
                if not pd.isna(avg_range):
                    avg_range = round(avg_range, 1)
                    
                    question = f"In Ahmedabad, what's the typical daily temperature range (difference between max and min)?"
                    
                    correct_answer = f"{avg_range}°C"
                    wrong_answers = [
                        f"{avg_range + 3}°C",
                        f"{avg_range - 2}°C",
                        f"{avg_range + 6}°C"
                    ]
                    
                    choices = [correct_answer] + wrong_answers
                    random.shuffle(choices)
                    
                    return {
                        "question": question,
                        "choices": choices,
                        "correct_answer": correct_answer,
                        "explanation": f"Analysis shows the average daily temperature range in Ahmedabad is {avg_range}°C, which is typical for continental climates."
                    }
            
            # Fallback question about temperature ranges
            question = "Which type of climate typically has the largest daily temperature range?"
            
            correct_answer = "Desert climate"
            wrong_answers = ["Coastal climate", "Tropical rainforest", "Arctic climate"]
            
            choices = [correct_answer] + wrong_answers
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": "Desert climates have the largest daily temperature ranges due to low humidity and clear skies, allowing rapid heating during the day and cooling at night."
            }
            
        except Exception as e:
            return None
    
    def _generate_weather_trend_question(self):
        """Generate a question about weather trends over time"""
        try:
            if self.ahmedabad_data is not None and len(self.ahmedabad_data) > 200:
                data = self.ahmedabad_data
                
                # Analyze sunshine duration trends
                data['date'] = pd.to_datetime(data['time'])
                data['month'] = data['date'].dt.month
                
                # Compare sunshine in different seasons
                summer_sunshine = data[data['month'].isin([4, 5, 6])]['sunshine_duration (s)'].mean()
                winter_sunshine = data[data['month'].isin([11, 12, 1])]['sunshine_duration (s)'].mean()
                
                if not (pd.isna(summer_sunshine) or pd.isna(winter_sunshine)):
                    if summer_sunshine > winter_sunshine:
                        longer_season = "summer"
                        shorter_season = "winter"
                    else:
                        longer_season = "winter" 
                        shorter_season = "summer"
                    
                    question = f"Based on Ahmedabad's data, which season typically has longer sunshine duration?"
                    
                    correct_answer = longer_season.title()
                    wrong_answers = ["Spring", "Autumn", shorter_season.title()]
                    
                    choices = [correct_answer] + [ans for ans in wrong_answers if ans != correct_answer][:3]
                    random.shuffle(choices)
                    
                    return {
                        "question": question,
                        "choices": choices,
                        "correct_answer": correct_answer,
                        "explanation": f"{longer_season.title()} has longer sunshine duration due to clearer skies and longer daylight hours during that period."
                    }
            
            # Fallback question about weather trends
            question = "What weather pattern is most associated with the El Niño phenomenon?"
            
            correct_answer = "Warmer ocean temperatures in the Pacific"
            wrong_answers = [
                "Increased hurricane activity in the Atlantic",
                "Colder winters in Europe", 
                "More rainfall in the Arctic"
            ]
            
            choices = [correct_answer] + wrong_answers
            random.shuffle(choices)
            
            return {
                "question": question,
                "choices": choices,
                "correct_answer": correct_answer,
                "explanation": "El Niño is characterized by unusually warm ocean temperatures in the eastern Pacific, which affects global weather patterns."
            }
            
        except Exception as e:
            return None
    
    def _generate_fallback_question(self):
        """Generate a general weather knowledge question as fallback"""
        fallback_questions = [
            {
                "question": "What is the most accurate way to measure wind speed?",
                "choices": ["Anemometer", "Barometer", "Hygrometer", "Thermometer"],
                "correct_answer": "Anemometer",
                "explanation": "An anemometer is specifically designed to measure wind speed and is the standard instrument used in weather stations."
            },
            {
                "question": "Which cloud type is most associated with thunderstorms?",
                "choices": ["Cumulonimbus", "Cirrus", "Stratus", "Altocumulus"],
                "correct_answer": "Cumulonimbus",
                "explanation": "Cumulonimbus clouds are towering clouds that can reach extreme heights and are responsible for thunderstorms, heavy rain, and severe weather."
            },
            {
                "question": "What does humidity measure in the atmosphere?",
                "choices": ["Water vapor content", "Air pressure", "Wind direction", "Temperature variation"],
                "correct_answer": "Water vapor content",
                "explanation": "Humidity measures the amount of water vapor present in the air, typically expressed as relative humidity percentage."
            },
            {
                "question": "At what temperature does water freeze at sea level?",
                "choices": ["0°C (32°F)", "-1°C (30°F)", "1°C (34°F)", "-2°C (28°F)"],
                "correct_answer": "0°C (32°F)",
                "explanation": "Water freezes at 0°C (32°F) at standard atmospheric pressure at sea level."
            },
            {
                "question": "Which weather phenomenon is measured by the Saffir-Simpson scale?",
                "choices": ["Hurricanes", "Tornadoes", "Blizzards", "Thunderstorms"],
                "correct_answer": "Hurricanes",
                "explanation": "The Saffir-Simpson scale categorizes hurricanes from Category 1 to 5 based on sustained wind speeds and potential damage."
            },
            {
                "question": "What causes the greenhouse effect in Earth's atmosphere?",
                "choices": ["Certain gases trap heat", "Solar radiation increases", "Ocean currents change", "Wind patterns shift"],
                "correct_answer": "Certain gases trap heat",
                "explanation": "Greenhouse gases like CO2, methane, and water vapor trap heat in the atmosphere by absorbing and re-emitting infrared radiation."
            },
            {
                "question": "Which direction do hurricanes rotate in the Northern Hemisphere?",
                "choices": ["Counterclockwise", "Clockwise", "Varies by location", "Straight line"],
                "correct_answer": "Counterclockwise",
                "explanation": "Due to the Coriolis effect, hurricanes rotate counterclockwise in the Northern Hemisphere and clockwise in the Southern Hemisphere."
            },
            {
                "question": "What is the primary cause of wind?",
                "choices": ["Pressure differences", "Earth's rotation", "Ocean currents", "Mountain ranges"],
                "correct_answer": "Pressure differences",
                "explanation": "Wind is primarily caused by differences in atmospheric pressure, as air moves from high-pressure areas to low-pressure areas."
            }
        ]
        
        return random.choice(fallback_questions)
    
    def _analyze_data_patterns(self):
        """Analyze patterns in the loaded data for smarter question generation"""
        try:
            patterns = {
                "temperature_trends": [],
                "weather_conditions": {},
                "seasonal_patterns": {},
                "data_quality": "low"
            }
            
            if len(self.weather_data) > 10:
                patterns["data_quality"] = "medium"
                
                # Analyze weather conditions
                for record in self.weather_data:
                    condition = record.get('description', '')
                    if condition:
                        patterns["weather_conditions"][condition] = patterns["weather_conditions"].get(condition, 0) + 1
                
                # Analyze temperatures
                temps = []
                for record in self.weather_data:
                    try:
                        temp = float(record.get('temperature', 0))
                        temps.append(temp)
                    except (ValueError, TypeError):
                        continue
                
                if len(temps) > 5:
                    patterns["temperature_trends"] = {
                        "avg": sum(temps) / len(temps),
                        "min": min(temps),
                        "max": max(temps),
                        "range": max(temps) - min(temps)
                    }
            
            if len(self.weather_data) > 20:
                patterns["data_quality"] = "high"
            
            return patterns
            
        except Exception as e:
            return {"data_quality": "low"}
    
    def get_quiz_difficulty(self):
        """Determine quiz difficulty based on available data"""
        patterns = self._analyze_data_patterns()
        
        if patterns["data_quality"] == "high":
            return "advanced"
        elif patterns["data_quality"] == "medium":
            return "intermediate"
        else:
            return "beginner"
    
    def generate_adaptive_quiz(self, user_level="intermediate"):
        """Generate quiz adapted to user level and available data"""
        difficulty = self.get_quiz_difficulty()
        
        if difficulty == "advanced" and user_level in ["intermediate", "advanced"]:
            # Use complex data analysis questions
            return self.generate_quiz()
        else:
            # Use more general knowledge questions with some data analysis
            questions = []
            
            # Mix of data-based and general questions
            data_questions = 2 if difficulty == "medium" else 1
            general_questions = 5 - data_questions
            
            # Generate data-based questions
            for _ in range(data_questions):
                question = self._generate_temperature_comparison_question()
                if question:
                    questions.append(question)
            
            # Fill with general knowledge questions
            for _ in range(general_questions):
                questions.append(self._generate_fallback_question())
            
            # Ensure we have exactly 5 questions
            while len(questions) < 5:
                questions.append(self._generate_fallback_question())
            
            return questions[:5]
    
    def get_data_summary(self):
        """Get summary of available data for quiz generation"""
        summary = {
            "search_history_entries": len(self.weather_data) if self.weather_data else 0,
            "ahmedabad_data_available": self.ahmedabad_data is not None,
            "ahmedabad_entries": len(self.ahmedabad_data) if self.ahmedabad_data is not None else 0,
            "quiz_difficulty": self.get_quiz_difficulty()
        }
        
        if self.weather_data:
            cities = set()
            conditions = set()
            for record in self.weather_data:
                city = record.get('city', '')
                condition = record.get('description', '')
                if city:
                    cities.add(city)
                if condition:
                    conditions.add(condition)
            
            summary["unique_cities"] = len(cities)
            summary["unique_conditions"] = len(conditions)
        
        return summary