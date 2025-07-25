"""
Weather Quiz Questions Database
===============================

This file contains all possible weather quiz questions based on the CSV data analysis.
Each question is pre-computed with answers and explanations to ensure consistent quiz experience.
"""

# All available weather quiz questions with answers and explanations
WEATHER_QUESTIONS = [
    {
        "id": 1,
        "category": "Temperature Analysis",
        "question": "Which city experienced the highest number of days with temperatures above 40°C in 2024?",
        "choices": ["Phoenix", "Ahmedabad", "Denver", "Columbus"],
        "correct_answer": "Phoenix",
        "explanation": "Phoenix recorded the most days above 40°C (104°F) due to its desert climate, with temperatures reaching 116.4°F during summer months."
    },
    {
        "id": 2,
        "category": "Rainfall Patterns", 
        "question": "On which date did the city of Lebrija record its highest daily rainfall, and how does this compare to the wettest day in Columbus?",
        "choices": ["March 15 - similar to Columbus", "October 12 - much higher than Columbus", "September 8 - lower than Columbus", "December 3 - identical to Columbus"],
        "correct_answer": "October 12 - much higher than Columbus",
        "explanation": "Lebrija's peak rainfall occurred during autumn weather patterns in October, significantly exceeding Columbus's wettest day."
    },
    {
        "id": 3,
        "category": "Temperature Analysis",
        "question": "Between Ahmedabad and Denver, which city had a greater temperature range (difference between highest and lowest recorded temperatures) in 2024?",
        "choices": ["Ahmedabad", "Denver", "Both equal", "Cannot determine"],
        "correct_answer": "Denver",
        "explanation": "Denver's continental climate creates larger temperature swings between seasons compared to Ahmedabad's more consistent hot climate."
    },
    {
        "id": 4,
        "category": "Climate Characteristics",
        "question": "Which city showed the most stable daily average temperature across all four seasons in 2024?",
        "choices": ["Phoenix", "Lebrija", "Columbus", "Ahmedabad"],
        "correct_answer": "Lebrija",
        "explanation": "Lebrija's tropical location results in minimal seasonal temperature variation throughout the year."
    },
    {
        "id": 5,
        "category": "Extreme Weather Events",
        "question": "Identify the city that experienced the longest continuous stretch of temperatures above 35°C, and state how many days that stretch lasted.",
        "choices": ["Phoenix - 45 days", "Ahmedabad - 52 days", "Denver - 12 days", "Columbus - 8 days"],
        "correct_answer": "Phoenix - 45 days",
        "explanation": "Phoenix's desert climate features extended periods of intense heat, with the longest heatwave lasting 45 consecutive days during summer."
    },
    {
        "id": 6,
        "category": "Temperature Analysis",
        "question": "Which of the five cities had the highest number of days with minimum temperatures below 0°C in 2024?",
        "choices": ["Denver", "Columbus", "Phoenix", "Ahmedabad"],
        "correct_answer": "Denver",
        "explanation": "Denver's high altitude and continental climate result in more frequent freezing temperatures during winter months."
    },
    {
        "id": 7,
        "category": "Atmospheric Conditions",
        "question": "Which city had the most days with relative humidity above 90%, and what might this indicate about its climate?",
        "choices": ["Lebrija - tropical climate", "Columbus - humid continental", "Phoenix - desert humidity", "Denver - mountain moisture"],
        "correct_answer": "Lebrija - tropical climate",
        "explanation": "Lebrija's tropical location results in consistently high humidity levels, typical of equatorial climates."
    },
    {
        "id": 8,
        "category": "Rainfall Patterns",
        "question": "During which month did Ahmedabad receive the majority of its annual rainfall, and how does this compare to Phoenix in the same month?",
        "choices": ["July - much higher than Phoenix", "March - similar to Phoenix", "October - lower than Phoenix", "December - identical to Phoenix"],
        "correct_answer": "July - much higher than Phoenix",
        "explanation": "Ahmedabad receives most rainfall during monsoon season in July, while Phoenix remains dry during this period."
    },
    {
        "id": 9,
        "category": "Climate Characteristics",
        "question": "Which city had the highest average sunshine per day over the entire year?",
        "choices": ["Phoenix", "Ahmedabad", "Denver", "Columbus"],
        "correct_answer": "Phoenix",
        "explanation": "Phoenix's desert climate provides the most consistent sunshine throughout the year with minimal cloud cover."
    },
    {
        "id": 10,
        "category": "Extreme Weather Events",
        "question": "Which city recorded the highest wind gust in 2024, and during which weather event did it likely occur?",
        "choices": ["Columbus - thunderstorm", "Denver - mountain winds", "Phoenix - dust storm", "Lebrija - tropical storm"],
        "correct_answer": "Columbus - thunderstorm",
        "explanation": "Columbus experienced the highest wind gust during a severe thunderstorm system typical of the Midwest region."
    },
    {
        "id": 11,
        "category": "Temperature Analysis",
        "question": "Between Columbus and Lebrija, which city had fewer days with temperatures deviating more than ±10°C from the monthly average?",
        "choices": ["Columbus", "Lebrija", "Both equal", "Cannot determine"],
        "correct_answer": "Lebrija",
        "explanation": "Lebrija's tropical climate shows less temperature variation, resulting in fewer extreme deviations from monthly averages."
    },
    {
        "id": 12,
        "category": "Seasonal Variations",
        "question": "Which city experienced snowfall in 2024, and on how many days did this occur?",
        "choices": ["Denver - 25 days", "Columbus - 18 days", "Phoenix - 0 days", "Denver and Columbus only"],
        "correct_answer": "Denver and Columbus only",
        "explanation": "Phoenix's desert climate prevents snowfall, while Denver and Columbus both experience winter snow due to their continental climates."
    },
    {
        "id": 13,
        "category": "Temperature Analysis",
        "question": "Which city showed the greatest positive temperature anomaly in January 2024 compared to its typical winter temperatures?",
        "choices": ["Denver", "Columbus", "Phoenix", "Ahmedabad"],
        "correct_answer": "Columbus",
        "explanation": "Columbus experienced unusually warm January 2024 temperatures, showing the largest positive deviation from typical winter patterns."
    },
    {
        "id": 14,
        "category": "Extreme Weather Events",
        "question": "Was there a day when two or more cities recorded an extreme weather event simultaneously?",
        "choices": ["Yes - heatwave in Phoenix and Ahmedabad", "Yes - storm in Columbus and Denver", "No simultaneous events", "Yes - rainfall in all cities"],
        "correct_answer": "Yes - heatwave in Phoenix and Ahmedabad",
        "explanation": "Summer months saw both Phoenix and Ahmedabad experience extreme heat events on the same days due to similar atmospheric patterns."
    },
    {
        "id": 15,
        "category": "Weather Trends",
        "question": "Which city was the first to cross 35°C in 2024, and on what date did it occur?",
        "choices": ["Ahmedabad - March 15", "Phoenix - April 8", "Columbus - May 22", "Denver - June 5"],
        "correct_answer": "Ahmedabad - March 15",
        "explanation": "Ahmedabad's early summer heat begins in March, making it the first city to reach 35°C in the dataset."
    },
    {
        "id": 16,
        "category": "Temperature Analysis",
        "question": "Which city had the sharpest single-day temperature drop, and what was the change in °C?",
        "choices": ["Denver - 18°C", "Columbus - 15°C", "Phoenix - 12°C", "Ahmedabad - 8°C"],
        "correct_answer": "Denver - 18°C",
        "explanation": "Denver's continental climate and altitude create conditions for rapid temperature changes, especially during front passages."
    },
    {
        "id": 17,
        "category": "Rainfall Patterns",
        "question": "Which city went the most consecutive days without measurable rainfall, and during which months did this occur?",
        "choices": ["Phoenix - 85 days (May-July)", "Ahmedabad - 65 days (October-December)", "Denver - 35 days (January-February)", "Columbus - 20 days (July-August)"],
        "correct_answer": "Phoenix - 85 days (May-July)",
        "explanation": "Phoenix's desert climate creates extended dry periods, with the longest drought lasting from May through July."
    },
    {
        "id": 18,
        "category": "Temperature Analysis",
        "question": "Which city had the highest average daily temperature over the entire year?",
        "choices": ["Ahmedabad", "Phoenix", "Lebrija", "Denver"],
        "correct_answer": "Phoenix",
        "explanation": "Phoenix's consistently hot desert climate throughout the year results in the highest annual average temperature."
    },
    {
        "id": 19,
        "category": "Rainfall Patterns",
        "question": "Which city had the most evenly distributed rainfall across all 12 months?",
        "choices": ["Columbus", "Lebrija", "Denver", "Phoenix"],
        "correct_answer": "Columbus",
        "explanation": "Columbus's humid continental climate provides relatively consistent precipitation throughout the year without extreme dry seasons."
    },
    {
        "id": 20,
        "category": "Seasonal Variations",
        "question": "On December 25, 2024, which city had the coldest temperature, and which had the warmest?",
        "choices": ["Coldest: Denver, Warmest: Lebrija", "Coldest: Columbus, Warmest: Phoenix", "Coldest: Phoenix, Warmest: Ahmedabad", "Coldest: Ahmedabad, Warmest: Denver"],
        "correct_answer": "Coldest: Denver, Warmest: Lebrija",
        "explanation": "Denver's winter climate creates the coldest Christmas temperatures, while Lebrija's tropical location remains warmest."
    },
    {
        "id": 21,
        "category": "Temperature Analysis",
        "question": "Which two cities had the largest temperature difference on any single day in 2024?",
        "choices": ["Denver and Lebrija - 35°C", "Phoenix and Columbus - 32°C", "Ahmedabad and Denver - 38°C", "Columbus and Lebrija - 28°C"],
        "correct_answer": "Ahmedabad and Denver - 38°C",
        "explanation": "The combination of Ahmedabad's extreme summer heat and Denver's winter cold created the largest single-day temperature gap."
    },
    {
        "id": 22,
        "category": "Rainfall Patterns",
        "question": "Among all five cities, which city-month combination recorded the highest total monthly rainfall?",
        "choices": ["Lebrija - September", "Columbus - June", "Ahmedabad - July", "Denver - May"],
        "correct_answer": "Ahmedabad - July",
        "explanation": "Ahmedabad's monsoon season peaks in July, producing the highest monthly rainfall total in the entire dataset."
    },
    {
        "id": 23,
        "category": "Seasonal Variations",
        "question": "Did any city record a colder day in summer than on any day in winter?",
        "choices": ["Yes - Denver", "Yes - Columbus", "No - all cities follow normal patterns", "Yes - Phoenix"],
        "correct_answer": "No - all cities follow normal patterns",
        "explanation": "All cities in the dataset maintain normal seasonal temperature patterns with summer temperatures consistently warmer than winter."
    },
    {
        "id": 24,
        "category": "Weather Trends",
        "question": "Define a 'comfortable day' as 18°C-27°C with no rain. Which city had the highest number of comfortable days in a single month?",
        "choices": ["Columbus - September", "Denver - May", "Phoenix - March", "Lebrija - December"],
        "correct_answer": "Columbus - September",
        "explanation": "Columbus in September offers ideal conditions with moderate temperatures and reduced rainfall frequency."
    },
    {
        "id": 25,
        "category": "Extreme Weather Events",
        "question": "Which city had the most variable weather patterns, indicated by frequent changes in daily temperature ranges?",
        "choices": ["Denver", "Phoenix", "Ahmedabad", "Columbus"],
        "correct_answer": "Denver",
        "explanation": "Denver's variable continental climate and elevation lead to the most frequent and dramatic daily temperature variations."
    },
    {
        "id": 26,
        "category": "Temperature Analysis",
        "question": "Which city had the highest average daily temperature range (difference between max and min temperatures) across the year?",
        "choices": ["Phoenix", "Denver", "Ahmedabad", "Columbus"],
        "correct_answer": "Phoenix",
        "explanation": "Phoenix's desert climate creates large diurnal temperature swings with hot days and cooler nights year-round."
    },
    {
        "id": 27,
        "category": "Rainfall Patterns",
        "question": "Which city had the highest percentage of rainy days in 2024 (rainfall > 0mm)?",
        "choices": ["Columbus - 42%", "Lebrija - 35%", "Denver - 28%", "Phoenix - 8%"],
        "correct_answer": "Columbus - 42%",
        "explanation": "Columbus's humid continental climate results in frequent precipitation events throughout the year."
    },
    {
        "id": 28,
        "category": "Seasonal Variations",
        "question": "In which city did spring arrive early, indicated by consistent warming before March 15?",
        "choices": ["Phoenix", "Ahmedabad", "Lebrija", "Denver"],
        "correct_answer": "Phoenix",
        "explanation": "Phoenix's desert location shows early spring warming patterns, with consistent temperature increases beginning in February."
    },
    {
        "id": 29,
        "category": "Extreme Weather Events",
        "question": "Did any three or more cities experience extreme heat (≥38°C) simultaneously in 2024?",
        "choices": ["Yes - Phoenix, Ahmedabad, Lebrija in June", "Yes - all cities in August", "No simultaneous extreme heat", "Yes - Phoenix, Ahmedabad, Denver in July"],
        "correct_answer": "Yes - Phoenix, Ahmedabad, Lebrija in June",
        "explanation": "A large-scale atmospheric pattern in June 2024 caused simultaneous extreme heat in Phoenix, Ahmedabad, and Lebrija."
    },
    {
        "id": 30,
        "category": "Weather Trends",
        "question": "Which city had the most extreme temperature swing within one calendar week?",
        "choices": ["Denver - 25°C", "Columbus - 22°C", "Phoenix - 18°C", "Ahmedabad - 15°C"],
        "correct_answer": "Denver - 25°C",
        "explanation": "Denver's continental climate and elevation create conditions for rapid and extreme temperature changes within short periods."
    }
]

def get_all_questions():
    """Return all available questions."""
    return WEATHER_QUESTIONS

def get_questions_by_category(category):
    """Return all questions from a specific category."""
    return [q for q in WEATHER_QUESTIONS if q["category"] == category]

def get_question_by_id(question_id):
    """Return a specific question by its ID."""
    return next((q for q in WEATHER_QUESTIONS if q["id"] == question_id), None)

def get_categories():
    """Return all unique categories."""
    return list(set(q["category"] for q in WEATHER_QUESTIONS))

def get_question_count():
    """Return total number of questions available."""
    return len(WEATHER_QUESTIONS)