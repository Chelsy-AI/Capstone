from features.history_tracker import fetch_world_history

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
    
    # What this test tells us:
    # 1. Our function can successfully connect to the weather API
    # 2. The API is returning data in the format we expect
    # 3. We're getting a full week of historical data
    # 4. The data structure matches what the rest of our app expects
    
    # Important notes about this type of test:
    # - It depends on internet connectivity
    # - It depends on the external API being available
    # - It might be slower than other tests due to network requests
    # - It could fail if the API changes its response format
    # - It's testing real integration with external services
    
    # This is different from our previous tests because:
    # - Previous tests used "mocks" (fake data) to avoid external dependencies
    # - This test makes real API calls to verify end-to-end functionality
    # - It's more realistic but also more fragile
    
    # In a complete test suite, you might have:
    # - Unit tests with mocks (fast, reliable, test logic)
    # - Integration tests like this one (slower, test real connections)
    # - Both types serve different purposes in ensuring code quality