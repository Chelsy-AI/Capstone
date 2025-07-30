#!/usr/bin/env python3
"""
Tomorrow's Weather Prediction Test
==================================

Tests the tomorrow's weather prediction feature including:
- Prediction algorithm
- Display components
- Data validation
- Error handling
- Temperature formatting
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from features.tomorrows_guess.predictor import (
    get_tomorrows_prediction,
    get_extended_prediction_info,
    validate_prediction_quality,
    _analyze_temperature_trend,
    _calculate_temperature_consistency
)
from features.tomorrows_guess.display import (
    create_tomorrow_guess_frame,
    update_tomorrow_guess_display,
    validate_prediction_data,
    format_temperature_for_display,
    format_percentage_for_display,
    get_table_dimensions
)


class TestTomorrowsPrediction(unittest.TestCase):
    """Test cases for tomorrow's weather prediction algorithm."""
    
    def test_prediction_with_valid_data(self):
        """Test prediction with good historical data."""
        # Mock valid weather history
        mock_history_data = {
            "time": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
            "temperature_2m_max": [20.0, 22.0, 21.0, 23.0, 24.0],
            "temperature_2m_min": [10.0, 12.0, 11.0, 13.0, 14.0],
            "temperature_2m_mean": [15.0, 17.0, 16.0, 18.0, 19.0]
        }
        
        with patch('features.tomorrows_guess.predictor.fetch_world_history') as mock_fetch:
            mock_fetch.return_value = mock_history_data
            
            prediction, confidence, accuracy = get_tomorrows_prediction("London")
            
            # Should return valid prediction
            self.assertIsNotNone(prediction)
            self.assertIsInstance(prediction, float)
            self.assertGreater(prediction, 0)  # Reasonable temperature
            
            # Should have confidence percentage
            self.assertIsInstance(confidence, str)
            self.assertIn("%", confidence)
            
            # Should have accuracy value
            self.assertIsInstance(accuracy, (int, float))
            self.assertGreaterEqual(accuracy, 0)
            self.assertLessEqual(accuracy, 100)
            
    def test_prediction_with_insufficient_data(self):
        """Test prediction with insufficient historical data."""
        # Mock insufficient data (only 2 days)
        mock_history_data = {
            "time": ["2024-01-01", "2024-01-02"],
            "temperature_2m_max": [20.0, 22.0],
            "temperature_2m_min": [10.0, 12.0],
            "temperature_2m_mean": [15.0, 17.0]
        }
        
        with patch('features.tomorrows_guess.predictor.fetch_world_history') as mock_fetch:
            mock_fetch.return_value = mock_history_data
            
            prediction, confidence, accuracy = get_tomorrows_prediction("London")
            
            # Should return no prediction
            self.assertIsNone(prediction)
            self.assertEqual(confidence, "0%")
            self.assertEqual(accuracy, 85)  # Default accuracy
            
    def test_prediction_with_no_data(self):
        """Test prediction with no historical data."""
        with patch('features.tomorrows_guess.predictor.fetch_world_history') as mock_fetch:
            mock_fetch.return_value = {}
            
            prediction, confidence, accuracy = get_tomorrows_prediction("InvalidCity")
            
            # Should return no prediction
            self.assertIsNone(prediction)
            self.assertEqual(confidence, "0%")
            self.assertEqual(accuracy, 85)
            
    def test_prediction_with_invalid_city(self):
        """Test prediction with invalid city input."""
        # Test None input
        prediction, confidence, accuracy = get_tomorrows_prediction(None)
        self.assertIsNone(prediction)
        self.assertEqual(confidence, "0%")
        
        # Test non-string input
        prediction, confidence, accuracy = get_tomorrows_prediction(123)
        self.assertIsNone(prediction)
        self.assertEqual(confidence, "0%")
        
    def test_confidence_calculation(self):
        """Test confidence calculation based on data quality."""
        # Test with 5 data points (should give high confidence)
        mock_history_data = {
            "time": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
            "temperature_2m_max": [20.0, 22.0, 21.0, 23.0, 24.0],
            "temperature_2m_min": [10.0, 12.0, 11.0, 13.0, 14.0],
            "temperature_2m_mean": [15.0, 17.0, 16.0, 18.0, 19.0]
        }
        
        with patch('features.tomorrows_guess.predictor.fetch_world_history') as mock_fetch:
            mock_fetch.return_value = mock_history_data
            
            prediction, confidence, accuracy = get_tomorrows_prediction("London")
            
            # Should have high confidence (30% base + 5*20% = 130%, capped at 100%)
            confidence_value = int(confidence.replace("%", ""))
            self.assertEqual(confidence_value, 100)
            
    def test_temperature_trend_analysis(self):
        """Test temperature trend analysis function."""
        # Test rising trend
        rising_temps = [15.0, 17.0, 19.0, 21.0, 23.0]
        trend = _analyze_temperature_trend(rising_temps)
        self.assertEqual(trend, "rising")
        
        # Test falling trend
        falling_temps = [23.0, 21.0, 19.0, 17.0, 15.0]
        trend = _analyze_temperature_trend(falling_temps)
        self.assertEqual(trend, "falling")
        
        # Test stable trend
        stable_temps = [20.0, 20.5, 19.5, 20.0, 20.2]
        trend = _analyze_temperature_trend(stable_temps)
        self.assertEqual(trend, "stable")
        
        # Test insufficient data
        short_temps = [20.0]
        trend = _analyze_temperature_trend(short_temps)
        self.assertEqual(trend, "stable")
        
    def test_temperature_consistency(self):
        """Test temperature consistency calculation."""
        # Test very consistent temperatures
        consistent_temps = [20.0, 20.1, 19.9, 20.0, 20.0]
        consistency = _calculate_temperature_consistency(consistent_temps)
        self.assertGreater(consistency, 0.8)  # Should be highly consistent
        
        # Test inconsistent temperatures
        inconsistent_temps = [10.0, 25.0, 5.0, 30.0, 15.0]
        consistency = _calculate_temperature_consistency(inconsistent_temps)
        self.assertLess(consistency, 0.5)  # Should be low consistency
        
        # Test single temperature
        single_temp = [20.0]
        consistency = _calculate_temperature_consistency(single_temp)
        self.assertEqual(consistency, 1.0)  # Perfect consistency with one value
        
    def test_extended_prediction_info(self):
        """Test extended prediction information."""
        mock_history_data = {
            "time": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
            "temperature_2m_max": [20.0, 22.0, 21.0, 23.0, 24.0],
            "temperature_2m_min": [10.0, 12.0, 11.0, 13.0, 14.0],
            "temperature_2m_mean": [15.0, 17.0, 16.0, 18.0, 19.0]
        }
        
        with patch('features.tomorrows_guess.predictor.fetch_world_history') as mock_fetch:
            mock_fetch.return_value = mock_history_data
            
            info = get_extended_prediction_info("London")
            
            self.assertIn("prediction", info)
            self.assertIn("confidence", info)
            self.assertIn("trend", info)
            self.assertIn("consistency", info)
            self.assertIn("data_points", info)
            self.assertIsNone(info.get("error"))
            
    def test_prediction_quality_validation(self):
        """Test prediction quality validation."""
        # Test excellent quality data
        mock_excellent_data = {
            "time": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", 
                    "2024-01-05", "2024-01-06", "2024-01-07"],
            "temperature_2m_mean": [15.0, 17.0, 16.0, 18.0, 19.0, 20.0, 21.0]
        }
        
        with patch('features.tomorrows_guess.predictor.fetch_world_history') as mock_fetch:
            mock_fetch.return_value = mock_excellent_data
            
            quality = validate_prediction_quality("London")
            
            self.assertEqual(quality["quality"], "excellent")
            self.assertEqual(quality["data_days"], 7)
            self.assertEqual(quality["missing_days"], 0)
            
    def test_prediction_with_none_values(self):
        """Test prediction handling None values in data."""
        mock_data_with_nones = {
            "time": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
            "temperature_2m_max": [20.0, None, 21.0, None, 24.0],
            "temperature_2m_min": [10.0, None, 11.0, None, 14.0],
            "temperature_2m_mean": [15.0, None, 16.0, None, 19.0]
        }
        
        with patch('features.tomorrows_guess.predictor.fetch_world_history') as mock_fetch:
            mock_fetch.return_value = mock_data_with_nones
            
            prediction, confidence, accuracy = get_tomorrows_prediction("London")
            
            # Should handle None values and still make prediction if enough valid data
            if prediction is not None:
                self.assertIsInstance(prediction, float)
            else:
                # Should return no prediction if too many None values
                self.assertEqual(confidence, "0%")


class TestTomorrowsDisplay(unittest.TestCase):
    """Test cases for tomorrow's weather display components."""
    
    def setUp(self):
        """Set up test environment."""
        # Mock parent widget
        self.mock_parent = Mock()
        
        # Mock theme
        self.mock_theme = {"bg": "#87CEEB"}
        
    def test_create_tomorrow_guess_frame(self):
        """Test creating the tomorrow's guess frame."""
        with patch('tkinter.Frame') as mock_frame_class:
            mock_frame = Mock()
            mock_frame_class.return_value = mock_frame
            
            with patch('tkinter.Label') as mock_label:
                frame = create_tomorrow_guess_frame(self.mock_parent, self.mock_theme)
                
                # Should return frame
                self.assertEqual(frame, mock_frame)
                
                # Should have created labels for the table
                self.assertTrue(mock_label.called)
                
                # Should have references to value labels
                self.assertTrue(hasattr(frame, 'temp_label'))
                self.assertTrue(hasattr(frame, 'accuracy_label'))
                self.assertTrue(hasattr(frame, 'confidence_label'))
                
    def test_update_tomorrow_guess_display(self):
        """Test updating the display with prediction data."""
        # Create mock frame with label attributes
        mock_frame = Mock()
        mock_temp_label = Mock()
        mock_accuracy_label = Mock()
        mock_confidence_label = Mock()
        
        mock_frame.temp_label = mock_temp_label
        mock_frame.accuracy_label = mock_accuracy_label
        mock_frame.confidence_label = mock_confidence_label
        
        # Test with valid data
        update_tomorrow_guess_display(mock_frame, 25.5, "85%", 90)
        
        # Should have updated labels
        mock_temp_label.configure.assert_called_with(text="25.5°F")
        mock_accuracy_label.configure.assert_called_with(text="90%")
        mock_confidence_label.configure.assert_called_with(text="85%")
        
    def test_update_display_with_none_values(self):
        """Test updating display with None values."""
        mock_frame = Mock()
        mock_temp_label = Mock()
        mock_accuracy_label = Mock()
        mock_confidence_label = Mock()
        
        mock_frame.temp_label = mock_temp_label
        mock_frame.accuracy_label = mock_accuracy_label
        mock_frame.confidence_label = mock_confidence_label
        
        # Test with None values
        update_tomorrow_guess_display(mock_frame, None, None, None)
        
        # Should show placeholders
        mock_temp_label.configure.assert_called_with(text="--")
        mock_accuracy_label.configure.assert_called_with(text="--")
        mock_confidence_label.configure.assert_called_with(text="--")
        
    def test_validate_prediction_data_valid(self):
        """Test validating valid prediction data."""
        is_valid, error = validate_prediction_data(25.5, "85%", 90)
        
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
    def test_validate_prediction_data_invalid_temp(self):
        """Test validating invalid temperature."""
        # Test extreme temperature
        is_valid, error = validate_prediction_data(200.0, "85%", 90)
        
        self.assertFalse(is_valid)
        self.assertIn("unrealistic", error)
        
    def test_validate_prediction_data_invalid_accuracy(self):
        """Test validating invalid accuracy."""
        is_valid, error = validate_prediction_data(25.5, "85%", 150)
        
        self.assertFalse(is_valid)
        self.assertIn("should be between 0-100%", error)
        
    def test_validate_prediction_data_invalid_confidence(self):
        """Test validating invalid confidence."""
        is_valid, error = validate_prediction_data(25.5, "150%", 90)
        
        self.assertFalse(is_valid)
        self.assertIn("should be between 0-100%", error)
        
    def test_format_temperature_for_display(self):
        """Test temperature formatting for display."""
        # Test valid temperature
        formatted = format_temperature_for_display(25.5, "C")
        self.assertEqual(formatted, "25.5°C")
        
        # Test whole number temperature
        formatted = format_temperature_for_display(25.0, "F")
        self.assertEqual(formatted, "25°F")
        
        # Test None temperature
        formatted = format_temperature_for_display(None)
        self.assertEqual(formatted, "--")
        
        # Test string temperature
        formatted = format_temperature_for_display("25.5°C", "C")
        self.assertEqual(formatted, "25.5°C")
        
    def test_format_percentage_for_display(self):
        """Test percentage formatting for display."""
        # Test valid percentage
        formatted = format_percentage_for_display(85.5)
        self.assertEqual(formatted, "85.5%")
        
        # Test whole number percentage
        formatted = format_percentage_for_display(85.0)
        self.assertEqual(formatted, "85%")
        
        # Test None percentage
        formatted = format_percentage_for_display(None)
        self.assertEqual(formatted, "--")
        
        # Test string percentage
        formatted = format_percentage_for_display("85%")
        self.assertEqual(formatted, "85%")
        
        # Test out of range (should be clamped)
        formatted = format_percentage_for_display(150)
        self.assertEqual(formatted, "100%")
        
        formatted = format_percentage_for_display(-10)
        self.assertEqual(formatted, "0%")
        
    def test_get_table_dimensions(self):
        """Test getting table dimensions."""
        dimensions = get_table_dimensions()
        
        self.assertIn("width", dimensions)
        self.assertIn("height", dimensions)
        self.assertIn("columns", dimensions)
        self.assertIn("rows", dimensions)
        
        # Check reasonable values
        self.assertGreater(dimensions["width"], 0)
        self.assertGreater(dimensions["height"], 0)
        self.assertEqual(dimensions["columns"], 3)
        self.assertEqual(dimensions["rows"], 3)
        
    def test_update_display_missing_attributes(self):
        """Test updating display when frame is missing attributes."""
        mock_frame = Mock()
        # Don't add label attributes
        
        # Should not raise exception
        try:
            update_tomorrow_guess_display(mock_frame, 25.5, "85%", 90)
        except Exception:
            self.fail("Should handle missing attributes gracefully")
            
    def test_format_edge_cases(self):
        """Test formatting edge cases."""
        # Test very small temperature
        formatted = format_temperature_for_display(0.1, "C")
        self.assertEqual(formatted, "0.1°C")
        
        # Test negative temperature
        formatted = format_temperature_for_display(-10.5, "F")
        self.assertEqual(formatted, "-10.5°F")
        
        # Test invalid string input
        formatted = format_temperature_for_display("invalid", "C")
        self.assertEqual(formatted, "--")
        
        # Test percentage edge cases
        formatted = format_percentage_for_display(0.1)
        self.assertEqual(formatted, "0.1%")
        
        formatted = format_percentage_for_display(99.9)
        self.assertEqual(formatted, "99.9%")


def run_tomorrows_guess_tests():
    """Run tomorrow's guess tests and return results."""
    print("🔮 Testing Tomorrow's Weather Prediction Feature...")
    
    # Create test suite
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTomorrowsPrediction))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTomorrowsDisplay))
    
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
    success = run_tomorrows_guess_tests()
    sys.exit(0 if success else 1)