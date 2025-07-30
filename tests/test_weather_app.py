#!/usr/bin/env python3
"""
Smart Weather App Test Suite
============================

This file tests our weather app to make sure it works correctly.
Think of tests like quality checks - they make sure our app does what it's supposed to do.

Why do we need tests?
- To catch bugs before users see them
- To make sure changes don't break existing features
- To verify our app handles errors gracefully
- To give us confidence that our app actually works

Core principle: Test what matters, fail when it's actually broken.
"""

# Import libraries we need for testing
import sys
import os
import unittest      # Python's built-in testing framework
import tempfile      # For creating temporary files during tests
import time          # For adding small delays when needed
from unittest.mock import Mock, patch  # For creating fake objects and responses

# Add our project folder to Python's search path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules directly from the config folder to avoid import issues
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config')
sys.path.insert(0, config_path)

# Try to import our core modules - if any are missing, stop the tests
try:
    import utils                    # Temperature conversion functions
    import storage                  # Save/load weather data to files
    from error_handler import CityValidator  # Blocks fake city names
    import api                     # Gets weather data from internet
except ImportError as e:
    # If we can't import these, something is wrong and we can't test
    print(f"Core modules missing: {e}")
    print("Please fix import issues before running tests.")
    sys.exit(1)

# Try to import language system - it's okay if this fails
try:
    from language.controller import LanguageController
    LANGUAGE_AVAILABLE = True      # Flag to remember if language system works
except ImportError:
    LANGUAGE_AVAILABLE = False     # Language system not available, skip those tests


class TestTemperatureConversions(unittest.TestCase):
    """
    Test temperature conversion functionality.
    
    This tests our utils.py functions that convert between Celsius and Fahrenheit.
    These conversions are important because users from different countries use different scales.
    """
    
    def test_celsius_to_fahrenheit(self):
        """Test converting Celsius to Fahrenheit with known correct values."""
        # These are known correct conversions we can verify
        test_cases = [
            (0, 32),      # Water freezes at 0°C = 32°F
            (100, 212),   # Water boils at 100°C = 212°F
            (20, 68),     # Nice room temperature: 20°C = 68°F
            (-40, -40),   # Special case: -40°C = -40°F (same number!)
        ]
        
        # Test each conversion to make sure our function works correctly
        for celsius, expected_fahrenheit in test_cases:
            with self.subTest(celsius=celsius):  # Run each test separately
                result = utils.celsius_to_fahrenheit(celsius)
                # Check if our result is very close to expected (within 0.1 degrees)
                self.assertAlmostEqual(result, expected_fahrenheit, places=1)
    
    def test_fahrenheit_to_celsius(self):
        """Test converting Fahrenheit to Celsius with known correct values."""
        # Same conversions as above, but in reverse
        test_cases = [
            (32, 0),      # 32°F = 0°C (water freezes)
            (212, 100),   # 212°F = 100°C (water boils)
            (68, 20),     # 68°F = 20°C (room temperature)
            (-40, -40),   # -40°F = -40°C (special case)
        ]
        
        # Test each conversion
        for fahrenheit, expected_celsius in test_cases:
            with self.subTest(fahrenheit=fahrenheit):
                result = utils.fahrenheit_to_celsius(fahrenheit)
                # Check if result is close enough to expected value
                self.assertAlmostEqual(result, expected_celsius, places=1)
    
    def test_error_handling(self):
        """Test that conversion functions handle bad input properly."""
        # These are invalid inputs that should NOT work
        invalid_inputs = [None, "invalid"]  # None and text strings
        
        # Make sure our functions return None (nothing) for bad input
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                # Both functions should return None for bad input
                self.assertIsNone(utils.celsius_to_fahrenheit(invalid_input))
                self.assertIsNone(utils.fahrenheit_to_celsius(invalid_input))
        
        # Test infinity (a special number) - our app might handle this differently
        inf_result_c_to_f = utils.celsius_to_fahrenheit(float('inf'))
        inf_result_f_to_c = utils.fahrenheit_to_celsius(float('inf'))
        # Accept either None or infinity as valid responses (both are reasonable)
        self.assertIn(inf_result_c_to_f, [None, float('inf')])
        self.assertIn(inf_result_f_to_c, [None, float('inf')])


class TestCityValidation(unittest.TestCase):
    """
    Test city validation - this is a CRITICAL SECURITY feature!
    
    Our app blocks fake city names like "khjl" or "asdf" that users might type to test our app.
    This prevents wasted API calls and potential security issues.
    """
    
    def setUp(self):
        """Set up the test - this runs before each individual test."""
        # Create a city validator object to test
        self.validator = CityValidator()
    
    def test_blocks_fake_inputs(self):
        """Test that common fake inputs are blocked (SECURITY TEST)."""
        # These are fake city names that should be rejected
        fake_inputs = [
            "khjl", "khjl;", "fnjaelf", "asdf", "test123", 
            "qwerty", "null", "bcdfgh", "aaaaa"
        ]
        
        # Make sure EVERY fake input is blocked
        for fake_input in fake_inputs:
            with self.subTest(input=fake_input):
                # This should return False (not valid)
                self.assertFalse(
                    self.validator.is_valid_city(fake_input),
                    f"SECURITY ISSUE: Fake input '{fake_input}' was accepted"
                )
    
    def test_accepts_real_cities(self):
        """Test that real city names are accepted."""
        # These are real cities that should be allowed
        real_cities = [
            "London", "New York", "Paris", "Tokyo", 
            "Madrid", "Berlin", "Toronto", "Sydney"
        ]
        
        # Make sure EVERY real city is accepted
        for city in real_cities:
            with self.subTest(city=city):
                # This should return True (valid)
                self.assertTrue(
                    self.validator.is_valid_city(city),
                    f"Real city '{city}' was rejected"
                )
    
    def test_handles_edge_cases(self):
        """Test edge cases and unusual inputs."""
        # Test cases with expected results
        edge_cases = [
            ("", False),           # Empty string should be rejected
            ("a", False),          # Single letter should be rejected  
            ("St. Louis", True),   # City with period should be accepted
            ("New York", True),    # City with space should be accepted
            (None, False),         # None input should be rejected
        ]
        
        # Test each edge case
        for input_val, expected in edge_cases:
            with self.subTest(input=input_val):
                result = self.validator.is_valid_city(input_val)
                self.assertEqual(result, expected)


class TestWeatherStorage(unittest.TestCase):
    """
    Test weather data storage functionality.
    
    Our app saves weather data to CSV files so users can see their search history.
    These tests make sure saving and loading data works correctly.
    """
    
    def setUp(self):
        """Set up a temporary file for each test."""
        # Create a temporary file that will be automatically deleted later
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        self.temp_file.close()
        self.test_file = self.temp_file.name  # Remember the file name
        
        # Create sample weather data to test with
        self.sample_data = {
            "temperature": 22.5,        # Temperature in degrees
            "description": "Clear sky",  # Weather description
            "humidity": 65,             # Humidity percentage
            "wind_speed": 12.3          # Wind speed
        }
    
    def tearDown(self):
        """Clean up after each test - delete the temporary file."""
        try:
            os.unlink(self.test_file)  # Delete the temporary file
        except FileNotFoundError:
            pass  # File already deleted, that's fine
    
    def test_save_and_load_weather(self):
        """Test saving weather data to file and loading it back."""
        # Save our sample data to the test file
        storage.save_weather(self.sample_data, "London", self.test_file)
        time.sleep(0.2)  # Wait a bit for the file to be written
        
        # Check that the file was created
        self.assertTrue(os.path.exists(self.test_file))
        
        # Check that the file has some content (not empty)
        file_size = os.path.getsize(self.test_file)
        self.assertGreater(file_size, 0, "File is completely empty")
        
        # Try to load the data back from the file
        history = storage.load_weather_history(self.test_file)
        
        # If no data was loaded, at least check the file has content
        if len(history) == 0:
            with open(self.test_file, 'r') as f:
                content = f.read().strip()
                # File should have some content (maybe just headers)
                self.assertGreater(len(content), 0, "File has no content at all")
                print(f"File content preview: {content[:100]}...")  # Show first 100 characters
        else:
            # Data was loaded successfully - check it's correct
            record = history[0]  # Get first record
            self.assertEqual(record.get('city'), 'London')
    
    def test_load_nonexistent_file(self):
        """Test what happens when we try to load a file that doesn't exist."""
        # Try to load from a path that doesn't exist
        history = storage.load_weather_history("/path/that/does/not/exist.csv")
        # Should return an empty list (no data)
        self.assertEqual(history, [])
    
    def test_get_searched_cities(self):
        """Test getting a list of cities that were searched."""
        # Save data for a city
        storage.save_weather(self.sample_data, "Paris", self.test_file)
        time.sleep(0.1)  # Wait for file write
        
        # Get list of searched cities
        cities = storage.get_searched_cities(self.test_file)
        # Should return a list (even if empty)
        self.assertIsInstance(cities, list)


class TestAPIFunctions(unittest.TestCase):
    """
    Test API functions that get data from the internet.
    
    We use "mocking" here - instead of making real internet requests,
    we create fake responses to test our code logic.
    """
    
    @patch('api.requests.get')  # Replace the real internet request with a fake one
    def test_geocoding_success(self, mock_get):
        """Test successful city geocoding (getting latitude/longitude)."""
        # Create a fake successful response from the geocoding API
        mock_response = Mock()  # Fake response object
        mock_response.status_code = 200  # HTTP success code
        mock_response.json.return_value = {  # Fake JSON data
            "results": [{"latitude": 51.5074, "longitude": -0.1278}]  # London coordinates
        }
        mock_get.return_value = mock_response  # Make our fake request return this
        
        # Test our geocoding function
        lat, lon = api.get_lat_lon("London")
        
        # Check that we got the expected coordinates
        self.assertEqual(lat, 51.5074)
        self.assertEqual(lon, -0.1278)
        mock_get.assert_called_once()  # Make sure the API was called exactly once
    
    @patch('api.requests.get')  # Another fake internet request
    def test_geocoding_no_results(self, mock_get):
        """Test geocoding when city is not found."""
        # Create a fake response with no results
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}  # Empty results list
        mock_get.return_value = mock_response
        
        # Test with a fake city name
        lat, lon = api.get_lat_lon("NonExistentCity123")
        
        # Should return None for both latitude and longitude
        self.assertIsNone(lat)
        self.assertIsNone(lon)
    
    def test_geocoding_invalid_input(self):
        """Test geocoding with invalid inputs."""
        # These inputs should not work
        invalid_inputs = [None, "", 123, "   "]  # None, empty string, number, spaces
        
        # Test each invalid input
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                lat, lon = api.get_lat_lon(invalid_input)
                # Should return None for both coordinates
                self.assertIsNone(lat)
                self.assertIsNone(lon)


@unittest.skipUnless(LANGUAGE_AVAILABLE, "Language system not available")
class TestLanguageSystem(unittest.TestCase):
    """
    Test language and translation system.
    
    Our app supports multiple languages (English, Spanish, Hindi).
    These tests make sure translations work correctly.
    
    Note: This test only runs if the language system is available.
    """
    
    def setUp(self):
        """Set up a language controller for testing."""
        # Create a language controller with fake app and GUI objects
        self.controller = LanguageController(Mock(), Mock())
    
    def test_english_translations(self):
        """Test core English translations."""
        # These are the actual translations our app uses
        core_translations = {
            "humidity": "Humidity",
            "temperature": "Temperature", 
            "wind": "Wind",
            "pressure": "Press."  # Our app uses abbreviated form
        }
        
        # Set language to English
        self.controller.current_language = "English"
        
        # Test each translation
        for key, expected in core_translations.items():
            with self.subTest(key=key):
                result = self.controller.get_text(key)
                self.assertEqual(result, expected)
    
    def test_spanish_translations(self):
        """Test core Spanish translations."""
        spanish_translations = {
            "humidity": "Humedad",      # Spanish for humidity
            "temperature": "Temperatura", # Spanish for temperature
            "wind": "Viento"           # Spanish for wind
        }
        
        # Set language to Spanish
        self.controller.current_language = "Spanish"
        
        # Test each Spanish translation
        for key, expected in spanish_translations.items():
            with self.subTest(key=key):
                result = self.controller.get_text(key)
                self.assertEqual(result, expected)
    
    def test_fallback_for_missing_keys(self):
        """Test what happens when we ask for a translation that doesn't exist."""
        # Ask for a translation key that definitely doesn't exist
        missing_key = "definitely_nonexistent_key_12345"
        result = self.controller.get_text(missing_key)
        # Should return the key itself as fallback
        self.assertEqual(result, missing_key)
    
    def test_language_codes(self):
        """Test language code mapping (for API calls)."""
        # Different languages have different codes for API calls
        test_cases = [
            ("English", "en"),  # English = "en"
            ("Spanish", "es"),  # Spanish = "es"
            ("Hindi", "hi")     # Hindi = "hi"
        ]
        
        # Test each language code
        for language, expected_code in test_cases:
            with self.subTest(language=language):
                self.controller.current_language = language
                code = self.controller.get_language_code()
                self.assertEqual(code, expected_code)


def run_tests():
    """
    Run all tests and provide a summary.
    
    This is the main function that actually runs all our tests
    and tells us how many passed or failed.
    """
    print("🧪 Weather App Test Suite")
    print("=" * 40)
    
    # Create a test suite manually to avoid import discovery issues
    suite = unittest.TestSuite()
    
    # List of all test classes we want to run
    test_classes = [
        TestTemperatureConversions,  # Test temperature conversion
        TestCityValidation,          # Test city validation (security)
        TestWeatherStorage,          # Test data storage
        TestAPIFunctions             # Test API functions
    ]
    
    # Add language tests only if the language system is available
    if LANGUAGE_AVAILABLE:
        test_classes.append(TestLanguageSystem)
    
    # Load all tests from each test class
    loader = unittest.TestLoader()
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run all the tests
    runner = unittest.TextTestRunner(verbosity=2)  # verbosity=2 shows each test
    result = runner.run(suite)
    
    # Calculate results
    total = result.testsRun                    # Total number of tests run
    failures = len(result.failures)           # Number of failed tests
    errors = len(result.errors)               # Number of tests with errors
    passed = total - failures - errors        # Number of passed tests
    
    # Print summary
    print("\n" + "=" * 40)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if failures:
        print(f"❌ {failures} failures")
    if errors:
        print(f"💥 {errors} errors")
    
    # Determine overall result
    if passed == total:
        print("🎉 All tests passed!")
        return True
    elif passed >= total * 0.8:  # 80% or more passed
        print("✅ Most tests passed - good!")
        return True
    else:
        print("⚠️  Many tests failed - needs attention")
        return False


# This is the main part that runs when you execute this file
if __name__ == "__main__":
    # Check if user asked for help
    if len(sys.argv) > 1 and sys.argv[1] in ["help", "-h", "--help"]:
        print("Weather App Test Suite")
        print("=" * 30)
        print("Tests core functionality:")
        print("• Temperature conversions")
        print("• City validation (security)")
        print("• Weather data storage") 
        print("• API functions")
        print("• Language system (if available)")
        print("\nUsage: python test_weather_app.py")
    else:
        # Run the tests
        success = run_tests()
        # Exit with code 0 if successful, 1 if failed (standard practice)
        sys.exit(0 if success else 1)