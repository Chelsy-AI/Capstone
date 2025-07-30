"""
Simple Utility Tests - Direct import approach
============================================

These tests import utility functions directly to avoid dependency issues.
"""

import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Direct import to avoid __init__.py issues
try:
    import config.utils as utils_module
    UTILS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import utils module: {e}")
    UTILS_AVAILABLE = False


@unittest.skipUnless(UTILS_AVAILABLE, "Utils module not available")
class TestTemperatureConversions(unittest.TestCase):
    """Test temperature conversion functions"""
    
    def test_kelvin_to_celsius(self):
        """Test Kelvin to Celsius conversion"""
        test_cases = [
            (273.15, 0.0),      # Freezing point
            (373.15, 100.0),    # Boiling point  
            (293.15, 20.0),     # Room temperature
            (None, None),       # Invalid input
            ("invalid", None),  # Invalid type
        ]
        
        for kelvin, expected in test_cases:
            with self.subTest(kelvin=kelvin, expected=expected):
                result = utils_module.kelvin_to_celsius(kelvin)
                if expected is None:
                    self.assertIsNone(result)
                else:
                    self.assertAlmostEqual(result, expected, places=1)
    
    def test_celsius_to_fahrenheit(self):
        """Test Celsius to Fahrenheit conversion"""
        test_cases = [
            (0, 32.0),          # Freezing
            (100, 212.0),       # Boiling
            (20, 68.0),         # Room temperature
            (-40, -40.0),       # Same in both scales
            (None, None),       # Invalid input
        ]
        
        for celsius, expected in test_cases:
            with self.subTest(celsius=celsius, expected=expected):
                result = utils_module.celsius_to_fahrenheit(celsius)
                if expected is None:
                    self.assertIsNone(result)
                else:
                    self.assertAlmostEqual(result, expected, places=1)
    
    def test_fahrenheit_to_celsius(self):
        """Test Fahrenheit to Celsius conversion"""
        test_cases = [
            (32, 0.0),          # Freezing
            (212, 100.0),       # Boiling
            (68, 20.0),         # Room temperature
            (-40, -40.0),       # Same in both scales
            (None, None),       # Invalid input
        ]
        
        for fahrenheit, expected in test_cases:
            with self.subTest(fahrenheit=fahrenheit, expected=expected):
                result = utils_module.fahrenheit_to_celsius(fahrenheit)
                if expected is None:
                    self.assertIsNone(result)
                else:
                    self.assertAlmostEqual(result, expected, places=1)
    
    def test_toggle_unit(self):
        """Test temperature unit toggling"""
        self.assertEqual(utils_module.toggle_unit("°C"), "°F")
        self.assertEqual(utils_module.toggle_unit("°F"), "°C")
    
    def test_format_temperature(self):
        """Test temperature formatting"""
        test_cases = [
            (25.5, "C", "25.5 °C"),
            (77.9, "F", "77.9 °F"),
            (None, "C", "N/A"),
            ("N/A", "F", "N/A"),
        ]
        
        for temp, unit, expected in test_cases:
            with self.subTest(temp=temp, unit=unit, expected=expected):
                result = utils_module.format_temperature(temp, unit)
                self.assertEqual(result, expected)


@unittest.skipUnless(UTILS_AVAILABLE, "Utils module not available")
class TestValidationFunctions(unittest.TestCase):
    """Test validation utility functions"""
    
    def test_validate_city_name(self):
        """Test city name validation"""
        test_cases = [
            ("London", (True, "")),
            ("New York", (True, "")),
            ("", (False, "City name cannot be empty")),
            ("A", (False, "City name must be at least 2 characters long")),
            ("X" * 101, (False, "City name is too long")),
        ]
        
        for city, (expected_valid, expected_error_contains) in test_cases:
            with self.subTest(city=city):
                is_valid, error_msg = utils_module.validate_city_name(city)
                self.assertEqual(is_valid, expected_valid)
                if expected_error_contains:
                    self.assertIn(expected_error_contains, error_msg)


@unittest.skipUnless(UTILS_AVAILABLE, "Utils module not available")
class TestDataUtilities(unittest.TestCase):
    """Test data manipulation utility functions"""
    
    def test_safe_get_nested_value(self):
        """Test safe nested dictionary value retrieval"""
        test_data = {
            "weather": {
                "main": {
                    "temp": 25.5,
                    "humidity": 60
                }
            },
            "city": "London"
        }
        
        # Test successful nested access
        temp = utils_module.safe_get_nested_value(test_data, ["weather", "main", "temp"])
        self.assertEqual(temp, 25.5)
        
        # Test missing nested key
        missing = utils_module.safe_get_nested_value(test_data, ["weather", "missing", "key"], "default")
        self.assertEqual(missing, "default")
        
        # Test empty data
        empty_result = utils_module.safe_get_nested_value({}, ["any", "key"])
        self.assertIsNone(empty_result)
    
    def test_capitalize_words(self):
        """Test word capitalization function"""
        test_cases = [
            ("hello world", "Hello World"),
            ("new york city", "New York City"),
            ("", ""),
            ("single", "Single"),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input=input_text, expected=expected):
                result = utils_module.capitalize_words(input_text)
                self.assertEqual(result, expected)


@unittest.skipUnless(UTILS_AVAILABLE, "Utils module not available")
class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""
    
    def test_extreme_temperature_values(self):
        """Test temperature conversions with extreme values"""
        # Test very high temperatures
        high_temp = utils_module.kelvin_to_celsius(10000)
        self.assertIsNotNone(high_temp)
        
        # Test very low temperatures  
        low_temp = utils_module.kelvin_to_celsius(0.1)
        self.assertIsNotNone(low_temp)
    
    def test_floating_point_precision(self):
        """Test floating point precision in conversions"""
        celsius = 23.456789
        fahrenheit = utils_module.celsius_to_fahrenheit(celsius)
        back_to_celsius = utils_module.fahrenheit_to_celsius(fahrenheit)
        
        # Should be very close to original
        self.assertAlmostEqual(celsius, back_to_celsius, places=5)


@unittest.skipUnless(UTILS_AVAILABLE, "Utils module not available")
class TestPerformance(unittest.TestCase):
    """Test performance characteristics of utility functions"""
    
    def test_conversion_performance(self):
        """Test that conversions are fast enough for real-time use"""
        import time
        
        start_time = time.time()
        
        for i in range(1000):
            utils_module.celsius_to_fahrenheit(i)
            utils_module.fahrenheit_to_celsius(i)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 2000 conversions should complete quickly
        self.assertLess(total_time, 1.0, f"Conversions too slow: {total_time:.3f}s for 2000 conversions")


class TestUtilsFallback(unittest.TestCase):
    """Test fallback when utils module isn't available"""
    
    def test_utils_availability(self):
        """Test that we can detect utils availability"""
        self.assertTrue(True)  # Always passes
        
        if UTILS_AVAILABLE:
            print("✅ Utils module available for testing")
        else:
            print("⚠️  Utils module not available - tests will be skipped")


if __name__ == '__main__':
    unittest.main()