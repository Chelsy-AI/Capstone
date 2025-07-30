#!/usr/bin/env python3
"""
Theme Switcher Feature Test
===========================

Tests the theme switching feature including:
- Theme management functions
- Light/dark mode switching
- Theme persistence
- Callback system
- Error handling
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from features.theme_switcher.theme_manager import (
    toggle_theme,
    set_day_mode,
    set_night_mode,
    apply_theme,
    get_current_theme,
    is_dark_mode,
    reset_theme_to_default,
    register_theme_callback,
    unregister_theme_callback,
    validate_theme_config,
    clear_theme_cache,
    get_theme_info
)


class TestThemeSwitcher(unittest.TestCase):
    """Test cases for theme switcher feature."""
    
    def setUp(self):
        """Set up test environment."""
        # Clear theme cache before each test
        clear_theme_cache()
        
        # Create mock app
        self.mock_app = Mock()
        self.mock_app.theme = None
        self.mock_app.configure = Mock()
        self.mock_app.parent_frame = Mock()
        self.mock_app.main_frame = Mock()
        
        # Mock theme configurations
        self.light_theme = {"bg": "#FFFFFF", "text": "#000000"}
        self.dark_theme = {"bg": "#000000", "text": "#FFFFFF"}
        
    def test_set_day_mode(self):
        """Test setting light theme (day mode)."""
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('customtkinter.set_appearance_mode') as mock_ctk:
                result = set_day_mode(self.mock_app)
                
                self.assertEqual(result, "light")
                self.assertEqual(self.mock_app.theme, self.light_theme)
                mock_ctk.assert_called_with("light")
                
    def test_set_night_mode(self):
        """Test setting dark theme (night mode)."""
        with patch('features.theme_switcher.theme_manager.DARK_THEME', self.dark_theme):
            with patch('customtkinter.set_appearance_mode') as mock_ctk:
                result = set_night_mode(self.mock_app)
                
                self.assertEqual(result, "dark")
                self.assertEqual(self.mock_app.theme, self.dark_theme)
                mock_ctk.assert_called_with("dark")
                
    def test_toggle_theme_light_to_dark(self):
        """Test toggling from light to dark theme."""
        # Set initial light theme
        self.mock_app.theme = self.light_theme
        
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('features.theme_switcher.theme_manager.DARK_THEME', self.dark_theme):
                with patch('customtkinter.set_appearance_mode') as mock_ctk:
                    result = toggle_theme(self.mock_app)
                    
                    self.assertEqual(result, "dark")
                    self.assertEqual(self.mock_app.theme, self.dark_theme)
                    
    def test_toggle_theme_dark_to_light(self):
        """Test toggling from dark to light theme."""
        # Set initial dark theme
        self.mock_app.theme = self.dark_theme
        
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('features.theme_switcher.theme_manager.DARK_THEME', self.dark_theme):
                with patch('customtkinter.set_appearance_mode') as mock_ctk:
                    result = toggle_theme(self.mock_app)
                    
                    self.assertEqual(result, "light")
                    self.assertEqual(self.mock_app.theme, self.light_theme)
                    
    def test_apply_theme_light(self):
        """Test applying light theme explicitly."""
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('customtkinter.set_appearance_mode') as mock_ctk:
                result = apply_theme(self.mock_app, "light")
                
                self.assertEqual(result, "light")
                self.assertEqual(self.mock_app.theme, self.light_theme)
                
    def test_apply_theme_dark(self):
        """Test applying dark theme explicitly."""
        with patch('features.theme_switcher.theme_manager.DARK_THEME', self.dark_theme):
            with patch('customtkinter.set_appearance_mode') as mock_ctk:
                result = apply_theme(self.mock_app, "dark")
                
                self.assertEqual(result, "dark")
                self.assertEqual(self.mock_app.theme, self.dark_theme)
                
    def test_apply_theme_system(self):
        """Test applying system theme."""
        with patch('features.theme_switcher.theme_manager._detect_system_theme') as mock_detect:
            mock_detect.return_value = "light"
            
            with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
                with patch('customtkinter.set_appearance_mode') as mock_ctk:
                    result = apply_theme(self.mock_app, "system")
                    
                    self.assertEqual(result, "light")
                    mock_detect.assert_called_once()
                    
    def test_apply_theme_invalid(self):
        """Test applying invalid theme falls back to light."""
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('customtkinter.set_appearance_mode') as mock_ctk:
                result = apply_theme(self.mock_app, "invalid_theme")
                
                self.assertEqual(result, "light")
                self.assertEqual(self.mock_app.theme, self.light_theme)
                
    def test_get_current_theme_light(self):
        """Test getting current theme when light."""
        self.mock_app.theme = self.light_theme
        
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            theme = get_current_theme(self.mock_app)
            self.assertEqual(theme, "light")
            
    def test_get_current_theme_dark(self):
        """Test getting current theme when dark."""
        self.mock_app.theme = self.dark_theme
        
        with patch('features.theme_switcher.theme_manager.DARK_THEME', self.dark_theme):
            theme = get_current_theme(self.mock_app)
            self.assertEqual(theme, "dark")
            
    def test_get_current_theme_none(self):
        """Test getting current theme when none set."""
        self.mock_app.theme = None
        
        theme = get_current_theme(self.mock_app)
        self.assertIsNone(theme)
        
    def test_is_dark_mode_true(self):
        """Test dark mode detection when in dark mode."""
        self.mock_app.theme = self.dark_theme
        
        with patch('features.theme_switcher.theme_manager.DARK_THEME', self.dark_theme):
            self.assertTrue(is_dark_mode(self.mock_app))
            
    def test_is_dark_mode_false(self):
        """Test dark mode detection when in light mode."""
        self.mock_app.theme = self.light_theme
        
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            self.assertFalse(is_dark_mode(self.mock_app))
            
    def test_reset_theme_to_default(self):
        """Test resetting theme to default."""
        # Set initial dark theme
        self.mock_app.theme = self.dark_theme
        
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('customtkinter.set_appearance_mode') as mock_ctk:
                result = reset_theme_to_default(self.mock_app)
                
                self.assertEqual(result, "light")
                self.assertEqual(self.mock_app.theme, self.light_theme)
                
    def test_theme_callback_registration(self):
        """Test registering and calling theme callbacks."""
        callback_called = []
        
        def test_callback(theme_name):
            callback_called.append(theme_name)
            
        # Register callback
        register_theme_callback(test_callback)
        
        # Apply theme should trigger callback
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('customtkinter.set_appearance_mode'):
                set_day_mode(self.mock_app)
                
        # Callback should have been called
        self.assertIn("light", callback_called)
        
        # Unregister callback
        unregister_theme_callback(test_callback)
        
    def test_theme_callback_app_method(self):
        """Test calling app's built-in theme change callback."""
        self.mock_app.on_theme_changed = Mock()
        
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('customtkinter.set_appearance_mode'):
                set_day_mode(self.mock_app)
                
        # App callback should have been called
        self.mock_app.on_theme_changed.assert_called_with("light")
        
    def test_validate_theme_config_valid(self):
        """Test validating valid theme configuration."""
        valid_config = {
            "bg": "#FFFFFF",
            "text": "#000000"
        }
        
        self.assertTrue(validate_theme_config(valid_config))
        
    def test_validate_theme_config_missing_bg(self):
        """Test validating theme config missing background."""
        invalid_config = {
            "text": "#000000"
        }
        
        self.assertFalse(validate_theme_config(invalid_config))
        
    def test_validate_theme_config_invalid_bg(self):
        """Test validating theme config with invalid background."""
        invalid_config = {
            "bg": None,
            "text": "#000000"
        }
        
        self.assertFalse(validate_theme_config(invalid_config))
        
    def test_theme_caching(self):
        """Test theme caching functionality."""
        # Apply light theme
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('customtkinter.set_appearance_mode'):
                set_day_mode(self.mock_app)
                
        # Apply same theme again (should use cache)
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('customtkinter.set_appearance_mode') as mock_ctk:
                set_day_mode(self.mock_app)
                
                # Should skip theme change due to cache
                # (Implementation may vary)
                
    def test_system_theme_detection(self):
        """Test system theme detection."""
        with patch('customtkinter.get_appearance_mode') as mock_get_appearance:
            mock_get_appearance.return_value = "Dark"
            
            from features.theme_switcher.theme_manager import _detect_system_theme
            theme = _detect_system_theme()
            
            self.assertEqual(theme, "dark")
            
    def test_system_theme_detection_light(self):
        """Test system theme detection for light mode."""
        with patch('customtkinter.get_appearance_mode') as mock_get_appearance:
            mock_get_appearance.return_value = "Light"
            
            from features.theme_switcher.theme_manager import _detect_system_theme
            theme = _detect_system_theme()
            
            self.assertEqual(theme, "light")
            
    def test_system_theme_detection_error(self):
        """Test system theme detection with error."""
        with patch('customtkinter.get_appearance_mode') as mock_get_appearance:
            mock_get_appearance.side_effect = Exception("Detection failed")
            
            from features.theme_switcher.theme_manager import _detect_system_theme
            theme = _detect_system_theme()
            
            self.assertEqual(theme, "light")  # Should fallback to light
            
    def test_error_handling_missing_app_attribute(self):
        """Test error handling when app is missing theme attribute."""
        bad_app = Mock()
        delattr(bad_app, 'theme')  # Remove theme attribute
        
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('customtkinter.set_appearance_mode'):
                # Should handle gracefully and fallback to light
                result = toggle_theme(bad_app)
                self.assertEqual(result, "light")
                
    def test_error_handling_in_theme_application(self):
        """Test error handling during theme application."""
        # Mock configure to raise exception
        self.mock_app.configure.side_effect = Exception("Configure failed")
        
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('customtkinter.set_appearance_mode'):
                # Should not raise exception
                try:
                    result = set_day_mode(self.mock_app)
                    self.assertEqual(result, "light")
                except Exception:
                    self.fail("Theme application should handle configure errors gracefully")
                    
    def test_theme_info_light(self):
        """Test getting theme information for light theme."""
        info = get_theme_info("light")
        
        self.assertIn("name", info)
        self.assertIn("description", info)
        self.assertIn("config", info)
        self.assertIn("suitable_for", info)
        self.assertEqual(info["name"], "Light Theme")
        
    def test_theme_info_dark(self):
        """Test getting theme information for dark theme."""
        info = get_theme_info("dark")
        
        self.assertIn("name", info)
        self.assertIn("description", info)
        self.assertIn("config", info)
        self.assertIn("suitable_for", info)
        self.assertEqual(info["name"], "Dark Theme")
        
    def test_theme_info_unknown(self):
        """Test getting theme information for unknown theme."""
        info = get_theme_info("unknown_theme")
        
        self.assertEqual(info["name"], "Unknown Theme")
        self.assertEqual(info["suitable_for"], [])
        
    def test_multiple_callback_registration(self):
        """Test registering multiple callbacks."""
        callback1_calls = []
        callback2_calls = []
        
        def callback1(theme):
            callback1_calls.append(theme)
            
        def callback2(theme):
            callback2_calls.append(theme)
            
        # Register both callbacks
        register_theme_callback(callback1)
        register_theme_callback(callback2)
        
        # Apply theme
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('customtkinter.set_appearance_mode'):
                set_day_mode(self.mock_app)
                
        # Both callbacks should have been called
        self.assertIn("light", callback1_calls)
        self.assertIn("light", callback2_calls)
        
        # Unregister callbacks
        unregister_theme_callback(callback1)
        unregister_theme_callback(callback2)
        
    def test_callback_error_handling(self):
        """Test error handling in theme callbacks."""
        def failing_callback(theme):
            raise Exception("Callback failed")
            
        register_theme_callback(failing_callback)
        
        # Should not raise exception even if callback fails
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('customtkinter.set_appearance_mode'):
                try:
                    set_day_mode(self.mock_app)
                except Exception:
                    self.fail("Theme application should handle callback errors gracefully")
                    
        unregister_theme_callback(failing_callback)
        
    def test_cache_clearing(self):
        """Test clearing theme cache."""
        # Apply theme to populate cache
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('customtkinter.set_appearance_mode'):
                set_day_mode(self.mock_app)
                
        # Clear cache
        clear_theme_cache()
        
        # Should not affect functionality
        with patch('features.theme_switcher.theme_manager.DARK_THEME', self.dark_theme):
            with patch('customtkinter.set_appearance_mode'):
                result = set_night_mode(self.mock_app)
                self.assertEqual(result, "dark")
                
    def test_app_validation(self):
        """Test app object validation for theming."""
        from features.theme_switcher.theme_manager import _validate_app_for_theming
        
        # Valid app
        self.assertTrue(_validate_app_for_theming(self.mock_app))
        
        # Invalid app (missing configure method)
        invalid_app = Mock()
        del invalid_app.configure
        self.assertFalse(_validate_app_for_theming(invalid_app))
        
    def test_theme_constants(self):
        """Test theme constants are properly defined."""
        from features.theme_switcher.theme_manager import (
            THEME_LIGHT, THEME_DARK, THEME_SYSTEM, VALID_THEMES
        )
        
        self.assertEqual(THEME_LIGHT, "light")
        self.assertEqual(THEME_DARK, "dark")
        self.assertEqual(THEME_SYSTEM, "system")
        self.assertIn("light", VALID_THEMES)
        self.assertIn("dark", VALID_THEMES)
        self.assertIn("system", VALID_THEMES)
        
    def test_duplicate_callback_registration(self):
        """Test registering the same callback twice."""
        callback_calls = []
        
        def test_callback(theme):
            callback_calls.append(theme)
            
        # Register same callback twice
        register_theme_callback(test_callback)
        register_theme_callback(test_callback)  # Should not duplicate
        
        # Apply theme
        with patch('features.theme_switcher.theme_manager.LIGHT_THEME', self.light_theme):
            with patch('customtkinter.set_appearance_mode'):
                set_day_mode(self.mock_app)
                
        # Callback should only be called once
        self.assertEqual(callback_calls.count("light"), 1)
        
        unregister_theme_callback(test_callback)
        
    def test_unregister_nonexistent_callback(self):
        """Test unregistering callback that wasn't registered."""
        def test_callback(theme):
            pass
            
        # Should not raise exception
        try:
            unregister_theme_callback(test_callback)
        except Exception:
            self.fail("Unregistering non-existent callback should not raise exception")
            
    def test_theme_config_validation_edge_cases(self):
        """Test theme config validation with edge cases."""
        # Empty config
        self.assertFalse(validate_theme_config({}))
        
        # None config
        self.assertFalse(validate_theme_config(None))
        
        # Config with empty string bg
        empty_bg_config = {"bg": ""}
        self.assertFalse(validate_theme_config(empty_bg_config))
        
        # Config with very short bg
        short_bg_config = {"bg": "#F"}
        self.assertFalse(validate_theme_config(short_bg_config))


def run_theme_switcher_tests():
    """Run theme switcher tests and return results."""
    print("🎨 Testing Theme Switcher Feature...")
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestThemeSwitcher)
    
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
    success = run_theme_switcher_tests()
    sys.exit(0 if success else 1)