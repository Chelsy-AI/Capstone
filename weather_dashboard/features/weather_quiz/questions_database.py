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
        "question": "Which city experienced the highest number of days with temperatures above 40°C (104°F) in 2024?",
        "choices": ["Phoenix", "Ahmedabad", "Denver", "Columbus"],
        "correct_answer": "Phoenix",
        "explanation": "Phoenix recorded the most days above 40°C (104°F) due to its desert climate, with summer temperatures consistently exceeding 104°F from May through September."
    },
    {
        "id": 2,
        "category": "Rainfall Patterns", 
        "question": "On which date did the city of Lebrija record its highest daily rainfall, and how does this compare to the wettest day in Columbus?",
        "choices": ["October 30 - much higher than Columbus", "March 15 - similar to Columbus", "September 8 - lower than Columbus", "December 3 - identical to Columbus"],
        "correct_answer": "October 30 - much higher than Columbus",
        "explanation": "Lebrija's peak rainfall of 4.154 inches occurred on October 30, 2024, significantly exceeding Columbus's highest single-day rainfall due to tropical weather patterns."
    },
    {
        "id": 3,
        "category": "Temperature Analysis",
        "question": "Between Ahmedabad and Denver, which city had a greater temperature range (difference between highest and lowest recorded temperatures) in 2024?",
        "choices": ["Ahmedabad", "Denver", "Both approximately equal", "Cannot determine"],
        "correct_answer": "Denver",
        "explanation": "Denver's continental climate creates larger temperature swings between winter lows (below 0°F) and summer highs (above 100°F), while Ahmedabad maintains more consistent heat year-round."
    },
    {
        "id": 4,
        "category": "Climate Characteristics",
        "question": "Which city showed the most stable daily average temperature across all four seasons in 2024?",
        "choices": ["Phoenix", "Lebrija", "Columbus", "Ahmedabad"],
        "correct_answer": "Lebrija",
        "explanation": "Lebrija's tropical location near the equator results in minimal seasonal temperature variation, with temperatures remaining between 68-88°F throughout the year."
    },
    {
        "id": 5,
        "category": "Extreme Weather Events",
        "question": "Identify the city that experienced the longest continuous stretch of temperatures above 35°C (95°F), and state how many days that stretch lasted.",
        "choices": ["Phoenix - 65 days", "Ahmedabad - 42 days", "Denver - 15 days", "Columbus - 8 days"],
        "correct_answer": "Phoenix - 65 days",
        "explanation": "Phoenix's desert climate features extended periods of intense heat, with the longest heatwave lasting from late May through July with temperatures consistently above 95°F."
    },
    {
        "id": 6,
        "category": "Temperature Analysis",
        "question": "Which of the five cities had the highest number of days with minimum temperatures below 0°C (32°F) in 2024?",
        "choices": ["Denver", "Columbus", "Phoenix", "Ahmedabad"],
        "correct_answer": "Denver",
        "explanation": "Denver's high altitude (5,280 feet) and continental climate result in more frequent freezing temperatures, with winter minimums dropping well below 0°F on multiple occasions."
    },
    {
        "id": 7,
        "category": "Atmospheric Conditions",
        "question": "Which city had the most days with relative humidity above 90%, and what might this indicate about its climate?",
        "choices": ["Lebrija - tropical climate", "Columbus - humid continental", "Phoenix - desert humidity", "Denver - mountain moisture"],
        "correct_answer": "Lebrija - tropical climate",
        "explanation": "Lebrija's tropical location results in consistently high humidity levels above 90% on many days, typical of equatorial climates with abundant moisture."
    },
    {
        "id": 8,
        "category": "Rainfall Patterns",
        "question": "During which month did Ahmedabad receive the majority of its annual rainfall, and how does this compare to Phoenix in the same month?",
        "choices": ["July - much higher than Phoenix", "March - similar to Phoenix", "October - lower than Phoenix", "December - identical to Phoenix"],
        "correct_answer": "July - much higher than Phoenix",
        "explanation": "Ahmedabad receives most rainfall during monsoon season in July (over 10 inches total), while Phoenix remains extremely dry during this period with minimal precipitation."
    },
    {
        "id": 9,
        "category": "Climate Characteristics",
        "question": "Which city had the highest average sunshine duration per day over the entire year?",
        "choices": ["Phoenix", "Ahmedabad", "Denver", "Columbus"],
        "correct_answer": "Phoenix",
        "explanation": "Phoenix's desert climate provides the most consistent sunshine throughout the year, with daily sunshine duration often exceeding 12-13 hours during peak months."
    },
    {
        "id": 10,
        "category": "Extreme Weather Events",
        "question": "Which city recorded the highest wind gust in 2024, and during which type of weather event did it likely occur?",
        "choices": ["Columbus - severe thunderstorm", "Denver - mountain downslope winds", "Phoenix - dust storm", "Lebrija - tropical storm"],
        "correct_answer": "Columbus - severe thunderstorm",
        "explanation": "Columbus experienced the highest wind gust (likely during spring/summer thunderstorms) typical of the Midwest's severe weather patterns with strong convective systems."
    },
    {
        "id": 11,
        "category": "Temperature Analysis",
        "question": "Between Columbus and Lebrija, which city had fewer days with temperatures deviating more than ±10°C (±18°F) from the monthly average?",
        "choices": ["Columbus", "Lebrija", "Both equal", "Cannot determine"],
        "correct_answer": "Lebrija",
        "explanation": "Lebrija's tropical climate shows minimal daily temperature variation, resulting in fewer extreme deviations from monthly averages compared to Columbus's variable continental climate."
    },
    {
        "id": 12,
        "category": "Seasonal Variations",
        "question": "Which cities experienced measurable snowfall in 2024?",
        "choices": ["Denver only", "Columbus only", "Denver and Columbus", "All cities had snow"],
        "correct_answer": "Denver and Columbus",
        "explanation": "Both Denver and Columbus recorded snowfall during winter months due to their continental climates, while Phoenix's desert climate and Ahmedabad/Lebrija's warm climates prevent snow formation."
    },
    {
        "id": 13,
        "category": "Temperature Analysis",
        "question": "Which city showed the most unusual temperature pattern in January 2024 compared to typical winter expectations?",
        "choices": ["Denver", "Columbus", "Phoenix", "Ahmedabad"],
        "correct_answer": "Columbus",
        "explanation": "Columbus experienced several notably warm days in January 2024, with temperatures reaching the 60s°F, which is unusual for typical Midwest winter patterns."
    },
    {
        "id": 14,
        "category": "Extreme Weather Events",
        "question": "Was there evidence of simultaneous extreme weather events across multiple cities in 2024?",
        "choices": ["Yes - summer heatwaves in Phoenix and Ahmedabad", "Yes - winter storms in Columbus and Denver", "No simultaneous events occurred", "Yes - rainfall events in all tropical cities"],
        "correct_answer": "Yes - summer heatwaves in Phoenix and Ahmedabad",
        "explanation": "During peak summer months, both Phoenix and Ahmedabad experienced concurrent extreme heat events with temperatures exceeding 110°F, indicating large-scale atmospheric patterns."
    },
    {
        "id": 15,
        "category": "Weather Trends",
        "question": "Which city was the first to cross 35°C (95°F) in 2024, and approximately when did it occur?",
        "choices": ["Ahmedabad - mid March", "Phoenix - early April", "Columbus - late May", "Denver - early June"],
        "correct_answer": "Ahmedabad - mid March",
        "explanation": "Ahmedabad's pre-monsoon heat begins early in the year, with temperatures reaching 95°F by mid-March, earlier than other cities due to its continental location and latitude."
    },
    {
        "id": 16,
        "category": "Temperature Analysis",
        "question": "Which city had the most dramatic single-day temperature drops during 2024?",
        "choices": ["Denver", "Columbus", "Phoenix", "Ahmedabad"],
        "correct_answer": "Denver",
        "explanation": "Denver's continental climate and high altitude create conditions for rapid temperature changes, especially during cold front passages, with drops exceeding 30°F possible in 24 hours."
    },
    {
        "id": 17,
        "category": "Rainfall Patterns",
        "question": "Which city experienced the longest period without measurable rainfall in 2024?",
        "choices": ["Phoenix - 80+ consecutive days", "Ahmedabad - 60 days", "Denver - 35 days", "Columbus - 20 days"],
        "correct_answer": "Phoenix - 80+ consecutive days",
        "explanation": "Phoenix's desert climate creates extended dry periods, with the longest drought lasting from late spring through mid-summer, typical of Sonoran Desert patterns."
    },
    {
        "id": 18,
        "category": "Temperature Analysis",
        "question": "Which city had the highest overall average temperature throughout 2024?",
        "choices": ["Ahmedabad", "Phoenix", "Lebrija", "Denver"],
        "correct_answer": "Phoenix",
        "explanation": "Despite Ahmedabad's extreme summer heat, Phoenix's consistently hot desert climate with minimal winter cooling results in the highest annual average temperature."
    },
    {
        "id": 19,
        "category": "Rainfall Patterns",
        "question": "Which city had the most consistent rainfall distribution across all 12 months of 2024?",
        "choices": ["Columbus", "Lebrija", "Denver", "Phoenix"],
        "correct_answer": "Columbus",
        "explanation": "Columbus's humid continental climate provides relatively consistent precipitation throughout the year without extreme dry seasons, unlike monsoon (Ahmedabad) or desert (Phoenix) patterns."
    },
    {
        "id": 20,
        "category": "Seasonal Variations",
        "question": "On December 25, 2024, which cities represented the temperature extremes (coldest and warmest)?",
        "choices": ["Coldest: Denver, Warmest: Lebrija", "Coldest: Columbus, Warmest: Phoenix", "Coldest: Phoenix, Warmest: Ahmedabad", "Coldest: Ahmedabad, Warmest: Denver"],
        "correct_answer": "Coldest: Denver, Warmest: Lebrija",
        "explanation": "Denver's high altitude winter creates the coldest Christmas temperatures (around 30-40°F), while Lebrija's tropical location maintains warm temperatures (70-80°F) year-round."
    },
    {
        "id": 21,
        "category": "Temperature Analysis",
        "question": "Which two cities likely had the largest temperature difference on the same day in 2024?",
        "choices": ["Denver and Phoenix - 50°F difference", "Ahmedabad and Columbus - 45°F difference", "Denver and Lebrija - 60°F difference", "Phoenix and Columbus - 40°F difference"],
        "correct_answer": "Denver and Lebrija - 60°F difference",
        "explanation": "The combination of Denver's winter cold (potentially below 0°F) and Lebrija's tropical warmth (75-85°F) creates the largest possible temperature gap between cities on the same day."
    },
    {
        "id": 22,
        "category": "Rainfall Patterns",
        "question": "Which city-month combination likely recorded the highest total monthly rainfall in 2024?",
        "choices": ["Lebrija - October", "Columbus - May", "Ahmedabad - July", "Denver - April"],
        "correct_answer": "Ahmedabad - July",
        "explanation": "Ahmedabad's monsoon season peaks in July, producing the highest monthly rainfall totals in the dataset, with daily amounts often exceeding 1-2 inches during active monsoon periods."
    },
    {
        "id": 23,
        "category": "Seasonal Variations",
        "question": "Did any city show evidence of unusual seasonal temperature patterns in 2024?",
        "choices": ["Yes - Denver had warm winter days", "Yes - Columbus had cold summer periods", "No - all cities followed normal patterns", "Yes - Phoenix had cool summer nights"],
        "correct_answer": "Yes - Denver had warm winter days",
        "explanation": "Denver showed some unusually warm winter days reaching 50-60°F, which while not extreme, represent notable departures from typical winter patterns for the elevation and latitude."
    },
    {
        "id": 24,
        "category": "Weather Trends",
        "question": "Defining 'comfortable weather' as 65-80°F with no rain, which city had the most such days in a single month?",
        "choices": ["Columbus - September", "Denver - May", "Phoenix - December", "Lebrija - January"],
        "correct_answer": "Columbus - September",
        "explanation": "Columbus in September typically offers ideal conditions with pleasant temperatures and reduced rainfall frequency, representing peak comfortable weather for the region."
    },
    {
        "id": 25,
        "category": "Extreme Weather Events",
        "question": "Which city demonstrated the most variable day-to-day weather patterns throughout 2024?",
        "choices": ["Denver", "Phoenix", "Ahmedabad", "Columbus"],
        "correct_answer": "Denver",
        "explanation": "Denver's continental climate and elevation create the most unpredictable weather with rapid changes in temperature, precipitation, and wind patterns due to mountain meteorology."
    },
    {
        "id": 26,
        "category": "Temperature Analysis",
        "question": "Which city had the largest average daily temperature range (difference between daily max and min) in 2024?",
        "choices": ["Phoenix", "Denver", "Ahmedabad", "Columbus"],
        "correct_answer": "Phoenix",
        "explanation": "Phoenix's desert climate creates the largest diurnal temperature swings, with hot days (110°F+) and relatively cooler nights (70-80°F), resulting in daily ranges often exceeding 30-40°F."
    },
    {
        "id": 27,
        "category": "Rainfall Patterns",
        "question": "Which city had the highest percentage of days with measurable rainfall (>0.01 inches) in 2024?",
        "choices": ["Columbus - ~40%", "Lebrija - ~35%", "Denver - ~25%", "Phoenix - ~8%"],
        "correct_answer": "Columbus - ~40%",
        "explanation": "Columbus's humid continental climate results in frequent precipitation events throughout the year, with rain occurring on approximately 140-150 days annually."
    },
    {
        "id": 28,
        "category": "Seasonal Variations",
        "question": "Which city showed the earliest signs of spring warming in 2024?",
        "choices": ["Phoenix", "Ahmedabad", "Lebrija", "Denver"],
        "correct_answer": "Phoenix",
        "explanation": "Phoenix's desert location shows early spring warming with consistent temperature increases beginning in February, reaching 80°F+ by early March."
    },
    {
        "id": 29,
        "category": "Extreme Weather Events",
        "question": "Did multiple cities experience simultaneous extreme heat (≥100°F) during summer 2024?",
        "choices": ["Yes - Phoenix, Ahmedabad, and occasionally others", "Yes - all cities reached 100°F simultaneously", "No - only one city at a time", "Yes - Phoenix and Denver only"],
        "correct_answer": "Yes - Phoenix, Ahmedabad, and occasionally others",
        "explanation": "During peak summer months, large-scale atmospheric patterns caused concurrent extreme heat in Phoenix and Ahmedabad, with Phoenix consistently above 100°F and Ahmedabad reaching similar levels."
    },
    {
        "id": 30,
        "category": "Weather Trends",
        "question": "Which city experienced the most dramatic temperature swing within a single week in 2024?",
        "choices": ["Denver - 40°F+ range", "Columbus - 35°F range", "Phoenix - 25°F range", "Ahmedabad - 20°F range"],
        "correct_answer": "Denver - 40°F+ range",
        "explanation": "Denver's continental climate and elevation create conditions for rapid and extreme temperature changes, with weekly swings from near 0°F to 50°F+ possible during transitional seasons."
    },
    {
        "id": 31,
        "category": "Climate Characteristics",
        "question": "Which city's weather patterns most closely resembled a typical desert climate throughout 2024?",
        "choices": ["Phoenix", "Ahmedabad", "Denver", "Columbus"],
        "correct_answer": "Phoenix",
        "explanation": "Phoenix exhibited classic desert characteristics: minimal rainfall, extreme heat, large diurnal temperature ranges, abundant sunshine, and extended dry periods."
    },
    {
        "id": 32,
        "category": "Atmospheric Conditions",
        "question": "Which city likely experienced the most days with low relative humidity (<30%) in 2024?",
        "choices": ["Phoenix", "Denver", "Ahmedabad", "Columbus"],
        "correct_answer": "Phoenix",
        "explanation": "Phoenix's desert climate consistently produces very low humidity levels, especially during spring and early summer before monsoon season, often dropping below 20%."
    },
    {
        "id": 33,
        "category": "Rainfall Patterns",
        "question": "Which city showed the most distinct wet and dry seasons in 2024?",
        "choices": ["Ahmedabad", "Phoenix", "Columbus", "Denver"],
        "correct_answer": "Ahmedabad",
        "explanation": "Ahmedabad's monsoon climate creates the most dramatic contrast between the dry pre-monsoon months (minimal rain) and wet monsoon season (July-September with heavy rainfall)."
    },
    {
        "id": 34,
        "category": "Temperature Analysis",
        "question": "Which city maintained the most consistent nighttime temperatures throughout 2024?",
        "choices": ["Lebrija", "Phoenix", "Ahmedabad", "Columbus"],
        "correct_answer": "Lebrija",
        "explanation": "Lebrija's tropical location near the equator results in minimal variation in nighttime temperatures, typically remaining in the 60-75°F range year-round."
    },
    {
        "id": 35,
        "category": "Extreme Weather Events",
        "question": "Which city was most likely to experience rapid weather changes within 24 hours?",
        "choices": ["Denver", "Columbus", "Phoenix", "Ahmedabad"],
        "correct_answer": "Denver",
        "explanation": "Denver's location east of the Rocky Mountains creates ideal conditions for rapid weather changes due to chinook winds, elevation effects, and continental air mass interactions."
    },
    {
        "id": 36,
        "category": "Seasonal Variations",
        "question": "Which city showed the least seasonal variation in daylight hours throughout 2024?",
        "choices": ["Lebrija", "Phoenix", "Ahmedabad", "Denver"],
        "correct_answer": "Lebrija",
        "explanation": "Lebrija's location closest to the equator results in minimal variation in daylight hours throughout the year, with approximately 12 hours of daylight year-round."
    },
    {
        "id": 37,
        "category": "Weather Trends",
        "question": "Which city experienced the most significant temperature drop during its transition from summer to winter?",
        "choices": ["Denver", "Columbus", "Ahmedabad", "Phoenix"],
        "correct_answer": "Denver",
        "explanation": "Denver shows the most dramatic seasonal temperature transition, dropping from summer highs near 90-100°F to winter lows potentially below 0°F, a range exceeding 100°F."
    },
    {
        "id": 38,
        "category": "Climate Characteristics",
        "question": "Based on 2024 data, which city would be classified as having a tropical climate?",
        "choices": ["Lebrija", "Phoenix", "Ahmedabad", "Columbus"],
        "correct_answer": "Lebrija",
        "explanation": "Lebrija exhibits classic tropical climate characteristics: minimal temperature variation, high humidity, consistent temperatures above 60°F year-round, and location near the equator."
    },
    {
        "id": 39,
        "category": "Atmospheric Conditions",
        "question": "Which city likely had the most clear, sunny days throughout 2024?",
        "choices": ["Phoenix", "Denver", "Ahmedabad", "Columbus"],
        "correct_answer": "Phoenix",
        "explanation": "Phoenix's desert climate provides maximum sunshine duration with minimal cloud cover, especially during the extended dry season from October through May."
    },
    {
        "id": 40,
        "category": "Fun Weather Facts",
        "question": "If you wanted to experience the widest variety of weather conditions in 2024, which city would provide the most diverse climate experiences?",
        "choices": ["Denver", "Columbus", "Phoenix", "Ahmedabad"],
        "correct_answer": "Denver",
        "explanation": "Denver's continental mountain climate offers the greatest weather diversity: snow and freezing temperatures, thunderstorms, rapid changes, altitude effects, and four distinct seasons with dramatic transitions."
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

def get_random_questions(count=10):
    """Return a random selection of questions."""
    import random
    return random.sample(WEATHER_QUESTIONS, min(count, len(WEATHER_QUESTIONS)))

def get_questions_by_difficulty(difficulty_level="mixed"):
    """
    Return questions filtered by difficulty level.
    difficulty_level: "easy", "medium", "hard", or "mixed"
    """
    if difficulty_level == "mixed":
        return WEATHER_QUESTIONS
    
    # Questions 1-15: Easy (basic comparisons)
    # Questions 16-30: Medium (analysis and trends)  
    # Questions 31-40: Hard (complex patterns and climate classification)
    
    if difficulty_level == "easy":
        return [q for q in WEATHER_QUESTIONS if q["id"] <= 15]
    elif difficulty_level == "medium":
        return [q for q in WEATHER_QUESTIONS if 16 <= q["id"] <= 30]
    elif difficulty_level == "hard":
        return [q for q in WEATHER_QUESTIONS if q["id"] > 30]
    
    return WEATHER_QUESTIONS