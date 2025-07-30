#!/usr/bin/env python3
"""
Weather Graphs Feature Test
============================

Tests the weather graphs feature including:
- Controller initialization  
- Graph generation
- Multiple graph types
- Language support
- Error handling
- Matplotlib integration
- Caching system
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
import warnings

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Suppress matplotlib warnings for cleaner test output
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

try:
    from features.graphs.controller import GraphsController
    GRAPHS_AVAILABLE = True
except ImportError:
    GRAPHS_AVAILABLE = False


@unittest.skipUnless(GRAPHS_AVAILABLE, "Graphs feature not available")
class TestWeatherGraphs(unittest.TestCase):
    """Test cases for weather graphs feature."""
    
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
            "Weather Graphs": "Weather Graphs",
            "Select Graph Type:": "Select Graph Type:",
            "← Back": "← Back",
            "7-Day Temperature Trend": "7-Day Temperature Trend",
            "Temperature Range Chart": "Temperature Range Chart", 
            "Humidity Trends": "Humidity Trends",
            "Weather Conditions Distribution": "Weather Conditions Distribution",
            "Prediction Accuracy Chart": "Prediction Accuracy Chart",
            "Graph Information": "Graph Information"
        }.get(key, key)
        
        # Mock bg_canvas
        self.mock_gui.bg_canvas = Mock()
        self.mock_gui.bg_canvas.cget.return_value = "#87CEEB"
        self.mock_gui.widgets = []
        
        # Initialize controller
        self.controller = GraphsController(self.mock_app, self.mock_gui)
        
    def test_controller_initialization(self):
        """Test controller initializes properly."""
        self.assertIsNotNone(self.controller)
        self.assertEqual(self.controller.app, self.mock_app)
        self.assertEqual(self.controller.gui, self.mock_gui)
        self.assertIsNotNone(self.controller.graph_options)
        self.assertIn("temperature_trend", self.controller.graph_options.values())
        
    def test_language_detection(self):
        """Test language detection works correctly."""
        # Test getting current language
        current_lang = self.controller._get_current_language()
        self.assertIsInstance(current_lang, str)
        
        # Test translation
        translated = self.controller._translate_text("Weather Graphs")
        self.assertEqual(translated, "Weather Graphs")
        
    def test_build_page_without_matplotlib(self):
        """Test page building when matplotlib is not available."""
        with patch('features.graphs.controller.MATPLOTLIB_AVAILABLE', False):
            window_width, window_height = 800, 600
            
            # Should handle missing dependencies gracefully
            try:
                self.controller.build_page(window_width, window_height)
            except Exception as e:
                self.fail(f"Should handle missing matplotlib gracefully: {e}")
                
    @patch('features.graphs.controller.MATPLOTLIB_AVAILABLE', True)
    def test_build_page_with_matplotlib(self):
        """Test page building when matplotlib is available."""
        window_width, window_height = 800, 600
        
        with patch('tkinter.Button') as mock_button, \
             patch('tkinter.Label') as mock_label, \
             patch('tkinter.Frame') as mock_frame:
            
            self.controller.build_page(window_width, window_height)
            
            # Should have created GUI elements
            self.assertTrue(mock_button.called)
            self.assertTrue(mock_label.called)
            self.assertTrue(mock_frame.called)
            
    def test_graph_selection_change(self):
        """Test graph selection dropdown functionality."""
        # Set up dropdown
        self.controller.selected_graph = Mock()
        self.controller.selected_graph.get.return_value = "7-Day Temperature Trend"
        
        # Mock the load method
        with patch.object(self.controller, '_load_selected_graph') as mock_load:
            self.controller._on_graph_selection_changed()
            
            # Should have triggered graph load
            mock_load.assert_called_once()
            
    def test_graph_type_translation(self):
        """Test graph type translation between languages."""
        # Test finding English key from translated text
        english_key = self.controller._find_english_key_from_translated("7-Day Temperature Trend")
        self.assertEqual(english_key, "7-Day Temperature Trend")
        
        # Test with non-existent translation
        english_key = self.controller._find_english_key_from_translated("Non-existent Graph")
        self.assertEqual(english_key, "7-Day Temperature Trend")  # Should return default
        
    @patch('features.graphs.controller.MATPLOTLIB_AVAILABLE', True)
    def test_graph_generation(self):
        """Test graph generation process."""
        # Mock graph generator
        self.controller.graph_generator = Mock()
        self.controller.graph_generator.generate_graph.return_value = (Mock(), True, None)
        
        # Mock frame
        self.controller.graph_frame = Mock()
        self.controller.graph_frame.winfo_children.return_value = []
        
        # Test graph generation
        with patch('threading.Thread') as mock_thread:
            self.controller._load_selected_graph()
            
            # Should start background thread
            self.assertTrue(mock_thread.called)
            
    def test_caching_system(self):
        """Test graph caching functionality."""
        import time
        
        # Test cache storage
        cache_key = "test_graph_london"
        test_data = (Mock(), True, None)
        
        self.controller._cache_graph(cache_key, test_data)
        
        # Test cache retrieval
        cached_result = self.controller._get_cached_graph(cache_key)
        self.assertIsNotNone(cached_result)
        
        # Test cache expiration
        self.controller._cache_timeout = 0.001  # Very short timeout
        time.sleep(0.002)
        
        expired_result = self.controller._get_cached_graph(cache_key)
        self.assertIsNone(expired_result)
        
    def test_error_handling(self):
        """Test error handling in graph generation."""
        # Mock failing graph generator
        self.controller.graph_generator = Mock()
        self.controller.graph_generator.generate_graph.side_effect = Exception("Graph generation failed")
        
        # Mock frame
        self.controller.graph_frame = Mock()
        self.controller.graph_frame.winfo_children.return_value = []
        
        # Should handle error gracefully
        try:
            self.controller._generate_graph_background("temperature_trend", "Test Graph", "test_key")
        except Exception:
            self.fail("Error handling should prevent exceptions from propagating")
            
    def test_graph_info_display(self):
        """Test graph information display."""
        self.controller.selected_graph = Mock()
        self.controller.selected_graph.get.return_value = "7-Day Temperature Trend"
        
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.controller._show_graph_info()
            
            # Should have shown info dialog
            mock_showinfo.assert_called_once()
            
    def test_detailed_graph_info(self):
        """Test detailed graph information generation."""
        # Test various graph types
        graph_types = [
            "7-Day Temperature Trend",
            "Temperature Range Chart", 
            "Humidity Trends",
            "Weather Conditions Distribution",
            "Prediction Accuracy Chart"
        ]
        
        for graph_type in graph_types:
            info = self.controller._get_detailed_graph_info(graph_type, "London")
            self.assertIsInstance(info, str)
            self.assertIn("London", info)
            
    def test_theme_change_handling(self):
        """Test handling of theme changes."""
        # Mock graph frame
        self.controller.graph_frame = Mock()
        
        # Should handle theme change without errors
        try:
            self.controller.handle_theme_change()
        except Exception as e:
            self.fail(f"Theme change handling should not raise exceptions: {e}")
            
    def test_cleanup(self):
        """Test cleanup functionality."""
        # Set up mock frame with children
        mock_child1 = Mock()
        mock_child2 = Mock()
        self.controller.graph_frame = Mock()
        self.controller.graph_frame.winfo_children.return_value = [mock_child1, mock_child2]
        
        # Perform cleanup
        self.controller.cleanup()
        
        # Should have destroyed children
        mock_child1.destroy.assert_called_once()
        mock_child2.destroy.assert_called_once()
        
    def test_available_graph_types(self):
        """Test getting available graph types."""
        available_types = self.controller.get_available_graph_types()
        self.assertIsInstance(available_types, list)
        self.assertIn("7-Day Temperature Trend", available_types)
        
    def test_graph_availability_check(self):
        """Test checking if specific graph types are available."""
        # Test valid graph
        self.assertTrue(self.controller.is_graph_available("7-Day Temperature Trend"))
        
        # Test invalid graph
        self.assertFalse(self.controller.is_graph_available("Non-existent Graph"))
        
    def test_dependency_status(self):
        """Test dependency status information."""
        status = self.controller.get_dependency_status()
        self.assertIsInstance(status, dict)
        self.assertIn("matplotlib_available", status)
        self.assertIn("graph_generator_ready", status)
        
    def test_force_refresh(self):
        """Test force refresh functionality."""
        # Mock graph generator
        self.controller.graph_generator = Mock()
        
        # Set up selected graph
        self.controller.selected_graph = Mock()
        self.controller.selected_graph.get.return_value = "7-Day Temperature Trend"
        
        # Test force refresh
        with patch.object(self.controller, '_load_selected_graph') as mock_load:
            self.controller.force_refresh_current_graph()
            
            # Should have triggered reload
            mock_load.assert_called_once()
            
    def test_export_graph_info(self):
        """Test exporting graph information."""
        # Set up controller state
        self.controller.selected_graph = Mock()
        self.controller.selected_graph.get.return_value = "Test Graph"
        
        # Export info
        info = self.controller.export_graph_info()
        
        # Should contain expected fields
        self.assertIn("selected_graph", info)
        self.assertIn("current_city", info)
        self.assertIn("current_language", info)
        
    def test_cache_management(self):
        """Test cache management operations."""
        # Add some cache entries
        self.controller._cache_graph("key1", (Mock(), True, None))
        self.controller._cache_graph("key2", (Mock(), True, None))
        
        # Verify cache has entries
        self.assertGreater(len(self.controller._graph_cache), 0)
        
        # Clear cache
        self.controller.clear_graph_cache()
        
        # Verify cache is empty
        self.assertEqual(len(self.controller._graph_cache), 0)


def run_graphs_tests():
    """Run weather graphs tests and return results."""
    print("📊 Testing Weather Graphs Feature...")
    
    if not GRAPHS_AVAILABLE:
        print("   ⚠️  Graphs feature not available - skipping")
        return False
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWeatherGraphs)
    
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
    success = run_graphs_tests()
    sys.exit(0 if success else 1)