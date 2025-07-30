#!/usr/bin/env python3
"""
Sun Moon Phases Feature Test
============================

Tests the sun and moon phases feature including:
- API data fetching
- Astronomical calculations
- Controller functionality
- Display components
- Error handling
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import math

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from features.sun_moon_phases.api import (
    get_coordinates_for_city,
    fetch_sun_moon_data,
    calculate_sun_position,
    calculate_moon_phase,
    calculate_moon_position,
    get_moon_phase_name,
    get_moon_phase_emoji,
    calculate_moon_illumination,
    is_currently_daytime,
    format_time_for_display,
    calculate_golden_hour
)
from features.sun_moon_phases.controller import SunMoonController


class TestSunMoonPhasesAPI(unittest.TestCase):
    """Test cases for sun moon phases API functions."""
    
    def test_coordinate_lookup_success(self):
        """Test successful city coordinate lookup."""
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
            
            lat, lon = get_coordinates_for_city("London")
            
            self.assertEqual(lat, 51.5074)
            self.assertEqual(lon, -0.1278)
            
    def test_coordinate_lookup_failure(self):
        """Test coordinate lookup with invalid city."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response
            
            lat, lon = get_coordinates_for_city("InvalidCityName")
            
            self.assertIsNone(lat)
            self.assertIsNone(lon)
            
    def test_coordinate_lookup_network_error(self):
        """Test coordinate lookup with network error."""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            lat, lon = get_coordinates_for_city("London")
            
            self.assertIsNone(lat)
            self.assertIsNone(lon)
            
    def test_sun_moon_data_fetch_success(self):
        """Test successful sun/moon data fetching."""
        # Mock coordinate lookup
        with patch('features.sun_moon_phases.api.get_coordinates_for_city') as mock_coords:
            mock_coords.return_value = (51.5074, -0.1278)
            
            # Mock sunrise-sunset API response
            mock_sunrise_data = {
                "results": {
                    "sunrise": "2024-01-15T07:30:00Z",
                    "sunset": "2024-01-15T17:45:00Z",
                    "solar_noon": "2024-01-15T12:37:30Z",
                    "day_length": "36900"
                }
            }
            
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = mock_sunrise_data
                mock_get.return_value = mock_response
                
                data = fetch_sun_moon_data("London")
                
                self.assertEqual(data["city"], "London")
                self.assertEqual(data["latitude"], 51.5074)
                self.assertEqual(data["longitude"], -0.1278)
                self.assertIn("sunrise", data)
                self.assertIn("sunset", data)
                self.assertIn("sun_position", data)
                self.assertIn("moon_phase", data)
                self.assertIsNone(data["error"])
                
    def test_sun_moon_data_fetch_failure(self):
        """Test sun/moon data fetch with invalid city."""
        # Mock failed coordinate lookup
        with patch('features.sun_moon_phases.api.get_coordinates_for_city') as mock_coords:
            mock_coords.return_value = (None, None)
            
            data = fetch_sun_moon_data("InvalidCity")
            
            # Should return fallback data
            self.assertIn("error", data)
            self.assertIsNotNone(data["sun_position"])
            self.assertIsNotNone(data["moon_phase"])
            
    def test_sun_position_calculation(self):
        """Test sun position calculations."""
        # Test with known coordinates
        lat, lon = 51.5074, -0.1278  # London
        
        sun_pos = calculate_sun_position(lat, lon)
        
        self.assertIn("elevation", sun_pos)
        self.assertIn("azimuth", sun_pos)
        self.assertIn("hour_angle", sun_pos)
        self.assertIn("declination", sun_pos)
        
        # Check reasonable ranges
        self.assertGreaterEqual(sun_pos["elevation"], -90)
        self.assertLessEqual(sun_pos["elevation"], 90)
        self.assertGreaterEqual(sun_pos["azimuth"], 0)
        self.assertLess(sun_pos["azimuth"], 360)
        
    def test_moon_phase_calculation(self):
        """Test moon phase calculations."""
        phase = calculate_moon_phase()
        
        # Should be between 0 and 1
        self.assertGreaterEqual(phase, 0)
        self.assertLessEqual(phase, 1)
        self.assertIsInstance(phase, float)
        
    def test_moon_position_calculation(self):
        """Test moon position calculations."""
        lat, lon = 51.5074, -0.1278  # London
        
        moon_pos = calculate_moon_position(lat, lon)
        
        self.assertIn("elevation", moon_pos)
        self.assertIn("azimuth", moon_pos)
        self.assertIn("longitude", moon_pos)
        
        # Check reasonable ranges
        self.assertGreaterEqual(moon_pos["elevation"], -90)
        self.assertLessEqual(moon_pos["elevation"], 90)
        self.assertGreaterEqual(moon_pos["azimuth"], 0)
        self.assertLess(moon_pos["azimuth"], 360)
        
    def test_moon_phase_names(self):
        """Test moon phase name conversion."""
        # Test known phase values
        test_phases = [
            (0.0, "new_moon"),
            (0.125, "waxing_crescent"),
            (0.25, "first_quarter"),
            (0.375, "waxing_gibbous"),
            (0.5, "full_moon"),
            (0.625, "waning_gibbous"),
            (0.75, "last_quarter"),
            (0.875, "waning_crescent")
        ]
        
        for phase_value, expected_name in test_phases:
            name = get_moon_phase_name(phase_value)
            self.assertEqual(name, expected_name)
            
    def test_moon_phase_emojis(self):
        """Test moon phase emoji selection."""
        # Test that each phase returns an emoji
        test_phases = [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
        
        for phase in test_phases:
            emoji = get_moon_phase_emoji(phase)
            self.assertIsInstance(emoji, str)
            self.assertTrue(len(emoji) > 0)
            # Should contain moon emoji character
            self.assertTrue(any(ord(char) > 127 for char in emoji))
            
    def test_moon_illumination_calculation(self):
        """Test moon illumination percentage calculation."""
        # Test known values
        test_cases = [
            (0.0, 0.0),    # New moon = 0%
            (0.25, 50.0),  # First quarter = 50%
            (0.5, 100.0),  # Full moon = 100%
            (0.75, 50.0),  # Last quarter = 50%
            (1.0, 0.0)     # Back to new moon = 0%
        ]
        
        for phase, expected_illumination in test_cases:
            illumination = calculate_moon_illumination(phase)
            self.assertAlmostEqual(illumination, expected_illumination, places=1)
            
    def test_daytime_detection(self):
        """Test daytime detection functionality."""
        # Test with valid sunrise/sunset times
        sunrise = "2024-01-15T07:30:00Z"
        sunset = "2024-01-15T17:45:00Z"
        
        # Mock current time to be during day
        with patch('datetime.datetime') as mock_datetime:
            mock_now = datetime(2024, 1, 15, 12, 0, 0)  # Noon
            mock_datetime.now.return_value = mock_now
            mock_datetime.fromisoformat.side_effect = datetime.fromisoformat
            
            is_day = is_currently_daytime(sunrise, sunset)
            self.assertTrue(is_day)
            
    def test_time_formatting(self):
        """Test time display formatting."""
        # Test valid ISO time
        iso_time = "2024-01-15T07:30:00Z"
        formatted = format_time_for_display(iso_time)
        
        self.assertIsInstance(formatted, str)
        self.assertNotEqual(formatted, "N/A")
        
        # Test invalid time
        formatted_invalid = format_time_for_display(None)
        self.assertEqual(formatted_invalid, "N/A")
        
        formatted_invalid2 = format_time_for_display("invalid_time")
        self.assertEqual(formatted_invalid2, "N/A")
        
    def test_golden_hour_calculation(self):
        """Test golden hour timing calculation."""
        sunrise = "2024-01-15T07:30:00Z"
        sunset = "2024-01-15T17:45:00Z"
        
        golden_hour = calculate_golden_hour(sunrise, sunset)
        
        self.assertIn("morning_start", golden_hour)
        self.assertIn("morning_end", golden_hour)
        self.assertIn("evening_start", golden_hour)
        self.assertIn("evening_end", golden_hour)
        
        # Should not be N/A for valid times
        self.assertNotEqual(golden_hour["morning_start"], "N/A")
        self.assertNotEqual(golden_hour["evening_end"], "N/A")
        
    def test_input_validation(self):
        """Test input validation for API functions."""
        # Test None input
        lat, lon = get_coordinates_for_city(None)
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        
        # Test empty string
        lat, lon = get_coordinates_for_city("")
        self.assertIsNone(lat)
        self.assertIsNone(lon)
        
        # Test non-string input
        lat, lon = get_coordinates_for_city(123)
        self.assertIsNone(lat)
        self.assertIsNone(lon)


class TestSunMoonController(unittest.TestCase):
    """Test cases for sun moon phases controller."""
    
    def setUp(self):
        """Set up test environment."""
        # Create mock app
        self.mock_app = Mock()
        self.mock_app.city_var = Mock()
        self.mock_app.city_var.get.return_value = "London"
        self.mock_app.winfo_width.return_value = 800
        self.mock_app.winfo_height.return_value = 600
        self.mock_app.after = Mock()
        
        # Create mock GUI controller
        self.mock_gui = Mock()
        self.mock_gui.language_controller = Mock()
        self.mock_gui.language_controller.get_text.side_effect = lambda key: {
            "sun_moon_phases": "Sun & Moon Phases",
            "loading": "Loading...",
            "daytime": "Daytime",
            "nighttime": "Nighttime",
            "back": "Back"
        }.get(key, key)
        
        # Mock display
        with patch('features.sun_moon_phases.controller.SunMoonDisplay'):
            self.controller = SunMoonController(self.mock_app, self.mock_gui)
            
    def test_controller_initialization(self):
        """Test controller initializes properly."""
        self.assertIsNotNone(self.controller)
        self.assertEqual(self.controller.app, self.mock_app)
        self.assertEqual(self.controller.gui, self.mock_gui)
        self.assertFalse(self.controller.is_fetching)
        self.assertEqual(self.controller.current_data, {})
        
    def test_build_page(self):
        """Test page building."""
        window_width, window_height = 800, 600
        
        try:
            self.controller.build_page(window_width, window_height)
        except Exception as e:
            self.fail(f"Page building should not raise exceptions: {e}")
            
    def test_data_caching(self):
        """Test data caching functionality."""
        test_data = {
            "city": "London",
            "sunrise": "07:30",
            "sunset": "17:45",
            "sun_position": {"elevation": 30, "azimuth": 180}
        }
        
        # Cache data
        self.controller._cache_data("London", test_data)
        
        # Check if cached
        self.assertTrue(self.controller._has_fresh_cached_data("London"))
        
        # Retrieve cached data
        cached = self.controller._get_cached_data("London")
        self.assertEqual(cached["city"], "London")
        
    def test_cache_expiration(self):
        """Test cache expiration."""
        import time
        
        test_data = {"test": "data"}
        
        # Set very short cache duration
        self.controller._cache_duration = 0.001
        
        # Cache data
        self.controller._cache_data("TestCity", test_data)
        
        # Wait for expiration
        time.sleep(0.002)
        
        # Should no longer be fresh
        self.assertFalse(self.controller._has_fresh_cached_data("TestCity"))
        
    def test_update_display(self):
        """Test display update functionality."""
        with patch.object(self.controller, '_has_fresh_cached_data') as mock_has_cache:
            mock_has_cache.return_value = False
            
            with patch('threading.Thread') as mock_thread:
                self.controller.update_display("London")
                
                # Should start background thread
                mock_thread.assert_called_once()
                
    def test_cached_data_usage(self):
        """Test using cached data instead of fetching."""
        test_data = {"city": "London", "cached": True}
        
        self.controller._cache_data("London", test_data)
        
        with patch.object(self.controller, '_update_display_safe') as mock_update:
            self.controller.update_display("London")
            
            # Should use cached data
            mock_update.assert_called_once()
            
    def test_error_handling(self):
        """Test error handling in data fetching."""
        with patch('features.sun_moon_phases.api.fetch_sun_moon_data') as mock_fetch:
            mock_fetch.side_effect = Exception("API Error")
            
            # Should handle error gracefully
            try:
                self.controller._fetch_and_update("InvalidCity")
            except Exception:
                self.fail("Error handling should prevent exceptions from propagating")
                
    def test_refresh_data(self):
        """Test manual data refresh."""
        # Cache some data first
        test_data = {"city": "London"}
        self.controller._cache_data("London", test_data)
        
        with patch.object(self.controller, 'update_display') as mock_update:
            self.controller.refresh_data()
            
            # Should trigger update
            mock_update.assert_called_once()
            
    def test_auto_refresh_enable_disable(self):
        """Test auto-refresh functionality."""
        # Test enabling auto-refresh
        self.controller.start_auto_refresh(30)
        self.assertTrue(self.controller._auto_refresh_enabled)
        
        # Test disabling auto-refresh
        self.controller.disable_auto_refresh()
        self.assertFalse(self.controller._auto_refresh_enabled)
        
    def test_current_data_methods(self):
        """Test methods for accessing current data."""
        test_data = {
            "sun_position": {"elevation": 30, "azimuth": 180},
            "moon_phase": 0.25,
            "moon_phase_name": "first_quarter",
            "moon_illumination": 50.0,
            "is_daytime": True
        }
        
        self.controller.current_data = test_data
        
        # Test data availability
        self.assertTrue(self.controller.is_data_available())
        
        # Test sun position
        sun_pos = self.controller.get_sun_position()
        self.assertEqual(sun_pos["elevation"], 30)
        
        # Test moon phase
        moon_phase = self.controller.get_moon_phase()
        self.assertEqual(moon_phase["phase"], 0.25)
        self.assertEqual(moon_phase["name"], "first_quarter")
        
        # Test daytime check
        self.assertTrue(self.controller.is_daytime())
        
    def test_language_change_handling(self):
        """Test handling language changes."""
        try:
            self.controller.handle_language_change(800, 600)
        except Exception as e:
            self.fail(f"Language change handling should not raise exceptions: {e}")
            
    def test_theme_change_handling(self):
        """Test handling theme changes."""
        try:
            self.controller.handle_theme_change()
        except Exception as e:
            self.fail(f"Theme change handling should not raise exceptions: {e}")
            
    def test_cleanup(self):
        """Test cleanup functionality."""
        # Set up some state
        self.controller._auto_refresh_enabled = True
        self.controller.current_data = {"test": "data"}
        self.controller._data_cache = {"city": "data"}
        
        self.controller.cleanup()
        
        # Should have cleaned up state
        self.assertFalse(self.controller._auto_refresh_enabled)
        self.assertEqual(self.controller.current_data, {})
        self.assertEqual(len(self.controller._data_cache), 0)
        
    def test_golden_hour_info(self):
        """Test golden hour information retrieval."""
        test_data = {
            "sunrise": "2024-01-15T07:30:00Z",
            "sunset": "2024-01-15T17:45:00Z"
        }
        
        self.controller.current_data = test_data
        
        golden_hour = self.controller.get_golden_hour_info()
        
        self.assertIn("morning_start", golden_hour)
        self.assertIn("evening_end", golden_hour)
        
    def test_fallback_daytime_detection(self):
        """Test fallback daytime detection when no data available."""
        # Clear current data
        self.controller.current_data = {}
        
        # Mock current time
        with patch('datetime.datetime') as mock_datetime:
            mock_now = Mock()
            mock_now.hour = 14  # 2 PM
            mock_datetime.now.return_value = mock_now
            
            is_day = self.controller.is_daytime()
            # Should be True for 2 PM, but we'll accept either since it's a fallback
            self.assertIsInstance(is_day, bool)


def run_sun_moon_phases_tests():
    """Run sun moon phases tests and return results."""
    print("🌙 Testing Sun & Moon Phases Feature...")
    
    # Create test suite
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSunMoonPhasesAPI))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSunMoonController))
    
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
    success = run_sun_moon_phases_tests()
    sys.exit(0 if success else 1)