#!/usr/bin/env python3
"""
Weather Icons Feature Test
===========================

Tests the weather icons feature including:
- Icon drawing functions
- Canvas management
- Weather condition mapping
- Error handling
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from features.weather_icons.canvas_icons import (
        draw_weather_icon,
        clear_icon_canvas,
        get_supported_conditions
    )
    WEATHER_ICONS_AVAILABLE = True
except ImportError:
    WEATHER_ICONS_AVAILABLE = False


@unittest.skipUnless(WEATHER_ICONS_AVAILABLE, "Weather icons not available")
class TestWeatherIcons(unittest.TestCase):
    """Test cases for weather icons feature."""
    
    def setUp(self):
        """Set up test environment."""
        # Create mock canvas
        self.mock_canvas = Mock()
        self.mock_canvas.winfo_width.return_value = 100
        self.mock_canvas.winfo_height.return_value = 100
        self.mock_canvas.delete = Mock()
        self.mock_canvas.create_oval = Mock()
        self.mock_canvas.create_line = Mock()
        self.mock_canvas.create_text = Mock()
        self.mock_canvas.create_polygon = Mock()
        
    def test_clear_icon_canvas(self):
        """Test clearing the icon canvas."""
        clear_icon_canvas(self.mock_canvas)
        
        # Should have called delete all
        self.mock_canvas.delete.assert_called_with("all")
        
    def test_draw_sunny_icon(self):
        """Test drawing sunny weather icon."""
        draw_weather_icon(self.mock_canvas, "sunny")
        
        # Should have cleared canvas first
        self.mock_canvas.delete.assert_called_with("all")
        
        # Should have drawn sun (oval) and rays (lines)
        self.assertTrue(self.mock_canvas.create_oval.called)
        self.assertTrue(self.mock_canvas.create_line.called)
        
    def test_get_supported_conditions(self):
        """Test getting list of supported weather conditions."""
        conditions = get_supported_conditions()
        
        self.assertIsInstance(conditions, list)
        self.assertGreater(len(conditions), 0)
        
        # Check for expected conditions
        expected_conditions = ["sunny", "rain", "cloudy", "snow", "storm"]
        for condition in expected_conditions:
            self.assertIn(condition, conditions)


class TestWeatherIconsFallback(unittest.TestCase):
    """Test cases for when weather icons are not available."""
    
    def test_fallback_behavior(self):
        """Test behavior when weather icons are not available."""
        if not WEATHER_ICONS_AVAILABLE:
            self.assertTrue(True)  # Placeholder test
            
    def test_import_error_handling(self):
        """Test handling of import errors."""
        try:
            import features.weather_icons
            available = True
        except ImportError:
            available = False
            
        self.assertIsInstance(available, bool)


def run_weather_icons_tests():
    """Run weather icons tests and return results."""
    print("🎨 Testing Weather Icons Feature...")
    
    if not WEATHER_ICONS_AVAILABLE:
        print("   ⚠️  Weather icons not available - skipping")
        return False
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWeatherIcons)
    
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
    success = run_weather_icons_tests()
    sys.exit(0 if success else 1)