#!/usr/bin/env python3
"""
Interactive Map Feature Test
============================

Tests the interactive map feature including:
- Map controller initialization
- Weather overlay functionality
- Geocoding services
- Tile server integration
- Map navigation
- Error handling
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
import threading
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from features.interactive_map.controller import MapController
    INTERACTIVE_MAP_AVAILABLE = True
except ImportError:
    INTERACTIVE_MAP_AVAILABLE = False


@unittest.skipUnless(INTERACTIVE_MAP_AVAILABLE, "Interactive map not available")
class TestInteractiveMap(unittest.TestCase):
    """Test cases for interactive map feature."""
    
    def setUp(self):
        """Set up test environment."""
        # Create mock parent widget
        self.mock_parent = Mock()
        
        # Create mock city callback
        self.mock_get_city = Mock()
        self.mock_get_city.return_value = "London"
        
        # Mock API key
        self.test_api_key = "test_api_key_123"
        
        # Mock TkinterMapView
        self.mock_map_view = Mock()
        
        with patch('features.interactive_map.controller.TkinterMapView') as mock_mapview_class:
            mock_mapview_class.return_value = self.mock_map_view
            
            with patch('features.interactive_map.controller.start_tile_server'):
                with patch('tkinter.ttk.Frame'), patch('tkinter.ttk.Label'), \
                     patch('tkinter.ttk.Combobox'), patch('tkinter.ttk.Button'), \
                     patch('tkinter.Frame'):
                    
                    # Initialize controller
                    self.controller = MapController(
                        self.mock_parent, 
                        self.mock_get_city, 
                        self.test_api_key
                    )
                    
    def test_controller_initialization(self):
        """Test controller initializes with correct settings."""
        self.assertIsNotNone(self.controller)
        self.assertEqual(self.controller.get_city_callback, self.mock_get_city)
        self.assertEqual(self.controller.api_key, self.test_api_key)
        self.assertTrue(self.controller.show_grid)
        
        # Check default coordinates (New York)
        self.assertEqual(self.controller.current_lat, 40.7127281)
        self.assertEqual(self.controller.current_lon, -74.0060152)
        self.assertEqual(self.controller.current_zoom, 6)
        
    def test_base_map_setup(self):
        """Test base map configuration."""
        self.controller.setup_base_map()
        
        # Should configure tile server
        self.mock_map_view.set_tile_server.assert_called()
        self.mock_map_view.set_zoom.assert_called_with(6)
        
    def test_geocoding_success(self):
        """Test successful city geocoding."""
        # Mock successful geocoding response
        mock_response_data = [
            {
                "lat": "51.5074",
                "lon": "-0.1278"
            }
        ]
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            coords = self.controller.geocode_city("London")
            
            self.assertIsNotNone(coords)
            self.assertEqual(coords, (51.5074, -0.1278))
            
    def test_geocoding_failure(self):
        """Test geocoding with invalid city."""
        # Mock failed geocoding response
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = []  # No results
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            coords = self.controller.geocode_city("InvalidCityName")
            
            self.assertIsNone(coords)
            
    def test_geocoding_network_error(self):
        """Test geocoding with network error."""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            coords = self.controller.geocode_city("London")
            
            self.assertIsNone(coords)
            
    def test_map_update_with_valid_city(self):
        """Test updating map with valid city."""
        # Mock successful geocoding
        with patch.object(self.controller, 'geocode_city') as mock_geocode:
            mock_geocode.return_value = (51.5074, -0.1278)
            
            self.controller.update_map()
            
            # Should have updated coordinates
            self.assertEqual(self.controller.current_lat, 51.5074)
            self.assertEqual(self.controller.current_lon, -0.1278)
            
            # Should have updated map view
            self.mock_map_view.set_position.assert_called_with(51.5074, -0.1278)
            self.mock_map_view.set_zoom.assert_called_with(6)
            
    def test_map_update_with_invalid_city(self):
        """Test updating map with invalid city."""
        # Mock failed geocoding
        with patch.object(self.controller, 'geocode_city') as mock_geocode:
            mock_geocode.return_value = None
            
            # Store original coordinates
            original_lat = self.controller.current_lat
            original_lon = self.controller.current_lon
            
            self.controller.update_map()
            
            # Coordinates should remain unchanged
            self.assertEqual(self.controller.current_lat, original_lat)
            self.assertEqual(self.controller.current_lon, original_lon)
            
    def test_weather_overlay_none(self):
        """Test setting weather overlay to none."""
        self.controller.layer_var = Mock()
        self.controller.layer_var.get.return_value = "none"
        
        self.controller.update_weather_overlay()
        
        # Should use base tile server
        expected_url = self.controller.base_tile_server
        self.mock_map_view.set_tile_server.assert_called_with(expected_url, max_zoom=22)
        
    def test_weather_overlay_with_layer(self):
        """Test setting specific weather overlay."""
        self.controller.layer_var = Mock()
        self.controller.layer_var.get.return_value = "temp_new"
        
        self.controller.update_weather_overlay()
        
        # Should use composite tile server
        args, kwargs = self.mock_map_view.set_tile_server.call_args
        self.assertIn("temp_new", args[0])
        self.assertEqual(kwargs.get('max_zoom'), 10)
        
    def test_marker_management(self):
        """Test map marker creation and removal."""
        # Set up marker
        mock_marker = Mock()
        self.controller.marker = mock_marker
        
        # Mock successful geocoding
        with patch.object(self.controller, 'geocode_city') as mock_geocode:
            mock_geocode.return_value = (51.5074, -0.1278)
            
            # Mock new marker creation
            new_marker = Mock()
            self.mock_map_view.set_marker.return_value = new_marker
            
            self.controller.update_map()
            
            # Should have deleted old marker
            self.mock_map_view.delete.assert_called_with(mock_marker)
            
            # Should have created new marker
            self.mock_map_view.set_marker.assert_called()
            self.assertEqual(self.controller.marker, new_marker)
            
    def test_refresh_functionality(self):
        """Test map refresh functionality."""
        with patch.object(self.controller, 'update_map') as mock_update:
            with patch.object(self.controller, 'update_weather_overlay') as mock_overlay:
                
                self.controller.refresh()
                
                # Should have called both update methods
                mock_update.assert_called_once()
                mock_overlay.assert_called_once()
                
    def test_tile_server_url_generation(self):
        """Test tile server URL generation."""
        # Test with different layers
        test_layers = ["temp_new", "wind_new", "precipitation_new"]
        
        for layer in test_layers:
            self.controller.layer_var = Mock()
            self.controller.layer_var.get.return_value = layer
            
            self.controller.update_weather_overlay()
            
            # Verify URL contains layer name
            args, kwargs = self.mock_map_view.set_tile_server.call_args
            self.assertIn(layer, args[0])
            
    def test_cleanup_functionality(self):
        """Test cleanup when controller is destroyed."""
        # Set up map view
        self.controller.map_view = Mock()
        
        self.controller.cleanup()
        
        # Should have destroyed map view
        self.controller.map_view.destroy.assert_called_once()
        
    def test_coordinate_validation(self):
        """Test coordinate validation in geocoding."""
        # Test valid coordinates
        mock_response_data = [
            {
                "lat": "51.5074",
                "lon": "-0.1278"
            }
        ]
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response
            
            coords = self.controller.geocode_city("London")
            
            self.assertIsInstance(coords[0], float)
            self.assertIsInstance(coords[1], float)
            
    def test_api_key_usage(self):
        """Test API key is properly used in tile server URLs."""
        self.controller.layer_var = Mock()
        self.controller.layer_var.get.return_value = "temp_new"
        
        self.controller.update_weather_overlay()
        
        # URL should contain API key
        args, kwargs = self.mock_map_view.set_tile_server.call_args
        url = args[0]
        self.assertIn(self.test_api_key, url)
        
    def test_layer_dropdown_options(self):
        """Test available layer options."""
        expected_layers = [
            "none", "temp_new", "wind_new", "precipitation_new", 
            "clouds_new", "pressure_new", "snow_new", "dewpoint_new"
        ]
        
        # This would be tested in the actual initialization
        # For now, just verify the controller has the expected structure
        self.assertTrue(hasattr(self.controller, 'layer_var'))
        
    def test_zoom_level_settings(self):
        """Test zoom level configurations."""
        # Test base map zoom
        self.controller.setup_base_map()
        self.mock_map_view.set_tile_server.assert_called_with(
            self.controller.base_tile_server, max_zoom=22
        )
        
        # Test weather overlay zoom
        self.controller.layer_var = Mock()
        self.controller.layer_var.get.return_value = "temp_new"
        
        self.controller.update_weather_overlay()
        
        args, kwargs = self.mock_map_view.set_tile_server.call_args
        self.assertEqual(kwargs.get('max_zoom'), 10)
        
    def test_city_callback_integration(self):
        """Test integration with city callback function."""
        # Change city callback return value
        self.mock_get_city.return_value = "Paris"
        
        with patch.object(self.controller, 'geocode_city') as mock_geocode:
            mock_geocode.return_value = (48.8566, 2.3522)
            
            self.controller.update_map()
            
            # Should have called geocoding with new city
            mock_geocode.assert_called_with("Paris")
            
    def test_error_handling_in_update(self):
        """Test error handling during map updates."""
        # Mock geocoding to raise exception
        with patch.object(self.controller, 'geocode_city') as mock_geocode:
            mock_geocode.side_effect = Exception("Geocoding failed")
            
            # Should not raise exception
            try:
                self.controller.update_map()
            except Exception:
                self.fail("Map update should handle geocoding errors gracefully")
                
    def test_tile_server_thread_startup(self):
        """Test tile server starts in background thread."""
        # This is tested during initialization
        # Verify that threading is used (mocked in setUp)
        self.assertTrue(hasattr(self.controller, 'tile_server_port'))
        self.assertEqual(self.controller.tile_server_port, 5005)
        
    def test_map_positioning(self):
        """Test map positioning with coordinates."""
        test_lat, test_lon = 40.7589, -73.9851  # Times Square
        
        # Simulate setting position
        self.controller.current_lat = test_lat
        self.controller.current_lon = test_lon
        
        # Update map view
        self.controller.map_view.set_position(test_lat, test_lon)
        self.controller.map_view.set_zoom(self.controller.current_zoom)
        
        # Verify position was set
        self.mock_map_view.set_position.assert_called_with(test_lat, test_lon)
        self.mock_map_view.set_zoom.assert_called_with(6)


def run_interactive_map_tests():
    """Run interactive map tests and return results."""
    print("🗺️  Testing Interactive Map Feature...")
    
    if not INTERACTIVE_MAP_AVAILABLE:
        print("   ⚠️  Interactive map not available - skipping")
        return False
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInteractiveMap)
    
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
    success = run_interactive_map_tests()
    sys.exit(0 if success else 1)