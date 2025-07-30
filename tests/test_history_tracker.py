#!/usr/bin/env python3
"""
History Tracker Feature Test
=============================

Tests the weather history tracking feature including:
- API functionality
- Data fetching and caching
- Display components
- Error handling
- Data validation
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from features.history_tracker.api import (
    fetch_world_history, 
    get_lat_lon, 
    clear_weather_cache,
    get_cache_info,
    format_temperature_data,
    get_weather_summary
)


class TestHistoryTracker(unittest.TestCase):
    """Test cases for history tracker feature."""
    
    def setUp(self):
        """Set up test environment."""
        # Clear any existing cache
        clear_weather_cache()
        
    def test_coordinate_lookup(self):
        """Test city to coordinate conversion."""
        # Mock successful API response
        mock_response_data = {
            "results": [
                {
                    "latitude": 51.5074,
                    "longitude": -0.1278
                }
            ]
        }
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_get.return_value = mock_response
            
            lat, lon = get_lat_lon("London")
            
            self.assertEqual(lat, 51.5074)
            self.assertEqual(lon, -0.1278)
            
    def test_coordinate_lookup_failure(self):
        """Test coordinate lookup with invalid city."""
        # Mock failed API response
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response
            
            lat, lon = get_lat_lon("InvalidCityName")
            
            self.assertIsNone(lat)
            self.assertIsNone(lon)
            
    def test_coordinate_lookup_network_error(self):
        """Test coordinate lookup with network error."""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            lat, lon = get_lat_lon("London")
            
            self.assertIsNone(lat)
            self.assertIsNone(lon)
            
    def test_weather_history_fetch(self):
        """Test fetching weather history data."""
        # Mock coordinate lookup
        with patch('features.history_tracker.api.get_lat_lon') as mock_coords:
            mock_coords.return_value = (51.5074, -0.1278)
            
            # Mock weather API response
            mock_weather_data = {
                "daily": {
                    "time": ["2024-01-01", "2024-01-02", "2024-01-03"],
                    "temperature_2m_max": [15.0, 18.0, 20.0],
                    "temperature_2m_min": [5.0, 8.0, 10.0],
                    "temperature_2m_mean": [10.0, 13.0, 15.0]
                }
            }
            
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = mock_weather_data
                mock_response.raise_for_status = Mock()
                mock_get.return_value = mock_response
                
                data = fetch_world_history("London")
                
                self.assertIn("time", data)
                self.assertIn("temperature_2m_max", data)
                self.assertEqual(len(data["time"]), 3)
                self.assertEqual(data["temperature_2m_max"][0], 15.0)
                
    def test_weather_history_invalid_city(self):
        """Test weather history with invalid city."""
        # Mock failed coordinate lookup
        with patch('features.history_tracker.api.get_lat_lon') as mock_coords:
            mock_coords.return_value = (None, None)
            
            data = fetch_world_history("InvalidCity")
            
            self.assertEqual(data, {})
            
    def test_weather_history_network_error(self):
        """Test weather history with network error."""
        # Mock successful coordinate lookup
        with patch('features.history_tracker.api.get_lat_lon') as mock_coords:
            mock_coords.return_value = (51.5074, -0.1278)
            
            # Mock network error
            with patch('requests.get') as mock_get:
                mock_get.side_effect = Exception("Network error")
                
                data = fetch_world_history("London")
                
                self.assertEqual(data, {})
                
    def test_caching_functionality(self):
        """Test weather data caching."""
        # Mock coordinate lookup
        with patch('features.history_tracker.api.get_lat_lon') as mock_coords:
            mock_coords.return_value = (51.5074, -0.1278)
            
            # Mock weather API response
            mock_weather_data = {
                "daily": {
                    "time": ["2024-01-01"],
                    "temperature_2m_max": [15.0],
                    "temperature_2m_min": [5.0],
                    "temperature_2m_mean": [10.0]
                }
            }
            
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = mock_weather_data
                mock_response.raise_for_status = Mock()
                mock_get.return_value = mock_response
                
                # First call should hit API
                data1 = fetch_world_history("London")
                self.assertEqual(mock_get.call_count, 1)
                
                # Second call should use cache
                data2 = fetch_world_history("London")
                self.assertEqual(mock_get.call_count, 1)  # Should not increase
                
                # Data should be identical
                self.assertEqual(data1, data2)
                
    def test_cache_info(self):
        """Test cache information functionality."""
        # Initially should be empty
        cache_info = get_cache_info()
        self.assertEqual(cache_info['total_entries'], 0)
        
        # Add some cached data
        with patch('features.history_tracker.api.get_lat_lon') as mock_coords:
            mock_coords.return_value = (51.5074, -0.1278)
            
            mock_weather_data = {
                "daily": {
                    "time": ["2024-01-01"],
                    "temperature_2m_max": [15.0],
                    "temperature_2m_min": [5.0],
                    "temperature_2m_mean": [10.0]
                }
            }
            
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = mock_weather_data
                mock_response.raise_for_status = Mock()
                mock_get.return_value = mock_response
                
                fetch_world_history("London")
                
                # Cache should now have entries
                cache_info = get_cache_info()
                self.assertGreater(cache_info['total_entries'], 0)
                
    def test_temperature_data_formatting(self):
        """Test temperature data formatting."""
        # Test data with proper structure
        daily_data = {
            'time': ['2024-01-01', '2024-01-02'],
            'temperature_2m_max': [20.0, 25.0],
            'temperature_2m_min': [10.0, 15.0]
        }
        
        # Test Celsius formatting
        formatted_c = format_temperature_data(daily_data, 'C')
        self.assertEqual(len(formatted_c), 2)
        self.assertIn('20.0°C', formatted_c[0])
        self.assertIn('10.0°C', formatted_c[0])
        
        # Test Fahrenheit formatting
        formatted_f = format_temperature_data(daily_data, 'F')
        self.assertEqual(len(formatted_f), 2)
        self.assertIn('68.0°F', formatted_f[0])  # 20°C = 68°F
        self.assertIn('50.0°F', formatted_f[0])  # 10°C = 50°F
        
    def test_temperature_formatting_empty_data(self):
        """Test temperature formatting with empty data."""
        empty_data = {}
        formatted = format_temperature_data(empty_data)
        self.assertEqual(formatted, [])
        
    def test_weather_summary(self):
        """Test weather summary generation."""
        # Mock successful data fetch
        mock_data = {
            'time': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'temperature_2m_max': [20.0, 25.0, 22.0],
            'temperature_2m_min': [10.0, 15.0, 12.0],
            'temperature_2m_mean': [15.0, 20.0, 17.0]
        }
        
        with patch('features.history_tracker.api.fetch_world_history') as mock_fetch:
            mock_fetch.return_value = mock_data
            
            summary = get_weather_summary("London", days=3)
            
            self.assertEqual(summary['city'], "London")
            self.assertEqual(summary['days_analyzed'], 3)
            self.assertIn('avg_high', summary)
            self.assertIn('avg_low', summary)
            self.assertIn('hottest_day', summary)
            self.assertIn('coldest_day', summary)
            
    def test_weather_summary_no_data(self):
        """Test weather summary with no data."""
        with patch('features.history_tracker.api.fetch_world_history') as mock_fetch:
            mock_fetch.return_value = {}
            
            summary = get_weather_summary("InvalidCity")
            
            self.assertEqual(summary['days_analyzed'], 0)
            self.assertIn('error', summary)
            
    def test_input_validation(self):
        """Test input validation for API functions."""
        # Test None input
        data = fetch_world_history(None)
        self.assertEqual(data, {})
        
        # Test empty string
        data = fetch_world_history("")
        self.assertEqual(data, {})
        
        # Test non-string input
        data = fetch_world_history(123)
        self.assertEqual(data, {})
        
    def test_coordinate_validation(self):
        """Test coordinate lookup input validation."""
        # Test None input
        lat, lon = get_lat_lon(None)
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        
        # Test empty string
        lat, lon = get_lat_lon("")
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        
        # Test non-string input
        lat, lon = get_lat_lon(123)
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        
    def test_cache_clearing(self):
        """Test cache clearing functionality."""
        # Add some data to cache
        with patch('features.history_tracker.api.get_lat_lon') as mock_coords:
            mock_coords.return_value = (51.5074, -0.1278)
            
            mock_weather_data = {
                "daily": {
                    "time": ["2024-01-01"],
                    "temperature_2m_max": [15.0],
                    "temperature_2m_min": [5.0],
                    "temperature_2m_mean": [10.0]
                }
            }
            
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = mock_weather_data
                mock_response.raise_for_status = Mock()
                mock_get.return_value = mock_response
                
                fetch_world_history("London")
                
                # Verify cache has data
                cache_info = get_cache_info()
                self.assertGreater(cache_info['total_entries'], 0)
                
                # Clear cache
                clear_weather_cache()
                
                # Verify cache is empty
                cache_info = get_cache_info()
                self.assertEqual(cache_info['total_entries'], 0)
                
    def test_data_consistency(self):
        """Test data consistency in returned weather data."""
        # Mock coordinate lookup
        with patch('features.history_tracker.api.get_lat_lon') as mock_coords:
            mock_coords.return_value = (51.5074, -0.1278)
            
            # Mock weather API response with consistent data
            mock_weather_data = {
                "daily": {
                    "time": ["2024-01-01", "2024-01-02"],
                    "temperature_2m_max": [20.0, 25.0],
                    "temperature_2m_min": [10.0, 15.0],
                    "temperature_2m_mean": [15.0, 20.0]
                }
            }
            
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = mock_weather_data
                mock_response.raise_for_status = Mock()
                mock_get.return_value = mock_response
                
                data = fetch_world_history("London")
                
                # Check data consistency
                time_count = len(data["time"])
                max_temp_count = len(data["temperature_2m_max"])
                min_temp_count = len(data["temperature_2m_min"])
                mean_temp_count = len(data["temperature_2m_mean"])
                
                self.assertEqual(time_count, max_temp_count)
                self.assertEqual(time_count, min_temp_count)
                self.assertEqual(time_count, mean_temp_count)
                
    def test_weather_summary_trend_detection(self):
        """Test trend detection in weather summary."""
        # Test rising trend
        rising_data = {
            'time': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'],
            'temperature_2m_max': [15.0, 18.0, 21.0, 24.0],
            'temperature_2m_min': [5.0, 8.0, 11.0, 14.0],
            'temperature_2m_mean': [10.0, 13.0, 16.0, 19.0]
        }
        
        with patch('features.history_tracker.api.fetch_world_history') as mock_fetch:
            mock_fetch.return_value = rising_data
            
            summary = get_weather_summary("TestCity")
            
            self.assertIn('temperature_trend', summary)
            self.assertEqual(summary['temperature_trend'], 'rising')
            
        # Test falling trend
        falling_data = {
            'time': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'],
            'temperature_2m_max': [24.0, 21.0, 18.0, 15.0],
            'temperature_2m_min': [14.0, 11.0, 8.0, 5.0],
            'temperature_2m_mean': [19.0, 16.0, 13.0, 10.0]
        }
        
        with patch('features.history_tracker.api.fetch_world_history') as mock_fetch:
            mock_fetch.return_value = falling_data
            
            summary = get_weather_summary("TestCity")
            
            self.assertEqual(summary['temperature_trend'], 'falling')


def run_history_tracker_tests():
    """Run history tracker tests and return results."""
    print("📚 Testing History Tracker Feature...")
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHistoryTracker)
    
    # Run tests with suppressed output
    runner = unittest.TextTestRunner(verbosity=2, stream=open(os.devnull, 'w'))
    result = runner.run(suite)
    
    # Print results
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"   ✅ {passed}/{total_tests} tests passed")
    
    if failures > 0:
        print(f"   ❌ {failures} failures")
        for test, traceback in result.failures:
            print(f"      - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if errors > 0:
        print(f"   💥 {errors} errors")
        for test, traceback in result.errors:
            print(f"      - {test}: Error occurred")
    
    return passed == total_tests


if __name__ == "__main__":
    success = run_history_tracker_tests()
    sys.exit(0 if success else 1)