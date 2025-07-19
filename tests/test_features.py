from features.history_tracker import fetch_world_history
from features.tomorrows_guess.predictor import get_tomorrows_prediction

def test_fetch_world_history_returns_data():
    """
    This test verifies that our fetch_world_history function works correctly.
    
    Unlike our previous tests, this one makes a REAL API call to get historical
    weather data. This is an "integration test" because it tests how our code
    works with an external service.
    
    What we're testing:
    1. The function can successfully retrieve historical weather data
    2. The data comes back in the expected format
    3. The data contains the fields we need
    4. The data has the right amount of information (7 days)
    """
    
    # Call our function with a real city name
    # This will make an actual HTTP request to a weather API
    data = fetch_world_history("New York")
    
    # Test 1: Check that we get back a dictionary
    # Weather APIs typically return data as JSON, which becomes a Python dict
    assert isinstance(data, dict), "Function should return a dictionary of weather data"
    
    # Test 2: Check that the dictionary contains maximum temperature data
    # "temperature_2m_max" is likely the key for daily maximum temperatures
    # The "2m" probably refers to temperature measured 2 meters above ground
    assert "temperature_2m_max" in data, "Data should include maximum temperature readings"
    
    # Test 3: Check that the dictionary contains time information
    # We need timestamps to know which temperature belongs to which day
    assert "time" in data, "Data should include time/date information"
    
    # Test 4: Check that we have exactly 7 days of temperature data
    # This suggests the function is designed to return a week's worth of history
    assert len(data["temperature_2m_max"]) == 7, "Should return exactly 7 days of temperature data"

def test_get_tomorrows_prediction():
    """
    This test verifies that our get_tomorrows_prediction function works correctly.
    
    This function appears to predict tomorrow's weather using some kind of algorithm
    or machine learning model. We're testing that it returns the right type and
    structure of data, even though we can't easily test if the prediction is accurate.
    
    What we're testing:
    1. The function returns a tuple (a container with multiple values)
    2. The tuple contains exactly 3 items in the expected order
    3. Each item is the correct data type for its purpose
    """
    
    # Call our prediction function with a real city name
    # This likely uses historical data and/or current conditions to make a prediction
    result = get_tomorrows_prediction("New York")
    
    # Test 1: Check that we get back a tuple
    # A tuple is an ordered collection of items, perfect for returning multiple related values
    assert isinstance(result, tuple), "Function should return a tuple containing prediction data"
    
    # Test 2: Check that the first item is a float (predicted temperature)
    # Temperatures are typically decimal numbers, so float is the appropriate type
    assert isinstance(result[0], (float, type(None))), "First item should be predicted temperature as a float or None"
    
    # Test 3: Check that the second item is a string (confidence description)
    # This is likely a human-readable description of how confident the prediction is
    assert isinstance(result[1], str), "Second item should be confidence description as a string"
    
    # Test 4: Check that the third item is an integer (certainty scale)
    # This is probably a numerical confidence score, like a percentage or scale rating
    assert isinstance(result[2], int), "Third item should be certainty scale as an integer"