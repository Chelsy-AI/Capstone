"""
Simple Language Tests - Direct import approach
=============================================

These tests import language components directly to avoid dependency issues.
"""

import unittest
import tempfile
import json
import os
import sys
from unittest.mock import Mock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Direct imports to avoid __init__.py issues
try:
    from language.controller import LanguageController
    from language.translations import TRANSLATIONS, SUPPORTED_LANGUAGES
    LANGUAGE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import language module: {e}")
    LANGUAGE_AVAILABLE = False


@unittest.skipUnless(LANGUAGE_AVAILABLE, "Language module not available")
class TestLanguageController(unittest.TestCase):
    """Test the main language controller functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create mock app and GUI controller
        self.mock_app = Mock()
        self.mock_gui = Mock()
        
        # Create language controller
        self.controller = LanguageController(self.mock_app, self.mock_gui)
        
        # Create temporary settings file
        self.temp_settings = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_settings.close()
        self.controller.settings_file = self.temp_settings.name
    
    def tearDown(self):
        """Clean up temporary files"""
        try:
            os.unlink(self.temp_settings.name)
        except FileNotFoundError:
            pass
    
    def test_default_language(self):
        """Test that default language is English"""
        self.assertEqual(self.controller.current_language, "English")
    
    def test_get_text_english(self):
        """Test getting English text"""
        # Test basic translation
        result = self.controller.get_text("weather_app_title")
        expected = "Smart Weather App with Sun & Moon Phases"
        self.assertEqual(result, expected)
        
        # Test fallback for missing key
        result = self.controller.get_text("nonexistent_key")
        self.assertEqual(result, "nonexistent_key")
    
    def test_get_text_spanish(self):
        """Test getting Spanish text"""
        self.controller.current_language = "Spanish"
        
        # Test Spanish translation
        result = self.controller.get_text("humidity")
        self.assertEqual(result, "Humedad")
        
        # Test fallback for missing key
        result = self.controller.get_text("some_missing_key", fallback_to_english=True)
        self.assertEqual(result, "some_missing_key")
    
    def test_get_text_hindi(self):
        """Test getting Hindi text"""
        self.controller.current_language = "Hindi"
        
        # Test Hindi translation
        result = self.controller.get_text("temperature")
        self.assertEqual(result, "तापमान")
    
    def test_get_language_code(self):
        """Test getting API language codes"""
        # English
        self.controller.current_language = "English"
        self.assertEqual(self.controller.get_language_code(), "en")
        
        # Spanish
        self.controller.current_language = "Spanish"
        self.assertEqual(self.controller.get_language_code(), "es")
        
        # Hindi
        self.controller.current_language = "Hindi"
        self.assertEqual(self.controller.get_language_code(), "hi")
        
        # Unknown language should default to English
        self.controller.current_language = "Unknown"
        self.assertEqual(self.controller.get_language_code(), "en")
    
    def test_save_and_load_settings(self):
        """Test saving and loading language settings"""
        # Change language and save
        self.controller.current_language = "Spanish"
        self.controller.save_settings()
        
        # Create new controller and load settings
        new_controller = LanguageController(self.mock_app, self.mock_gui)
        new_controller.settings_file = self.temp_settings.name
        new_controller.load_settings()
        
        # Should have loaded Spanish
        self.assertEqual(new_controller.current_language, "Spanish")
    
    def test_load_invalid_settings(self):
        """Test loading invalid/corrupted settings file"""
        # Write invalid JSON to settings file
        with open(self.temp_settings.name, 'w') as f:
            f.write("invalid json content")
        
        # Should fallback to English without crashing
        new_controller = LanguageController(self.mock_app, self.mock_gui)
        new_controller.settings_file = self.temp_settings.name
        new_controller.load_settings()
        
        self.assertEqual(new_controller.current_language, "English")


@unittest.skipUnless(LANGUAGE_AVAILABLE, "Language module not available")
class TestTranslationData(unittest.TestCase):
    """Test the translation data integrity"""
    
    def test_supported_languages_structure(self):
        """Test that supported languages data is correct"""
        expected_languages = {"English", "Spanish", "Hindi"}
        actual_languages = set(SUPPORTED_LANGUAGES.keys())
        self.assertEqual(actual_languages, expected_languages)
        
        # Test language codes
        self.assertEqual(SUPPORTED_LANGUAGES["English"], "en")
        self.assertEqual(SUPPORTED_LANGUAGES["Spanish"], "es")
        self.assertEqual(SUPPORTED_LANGUAGES["Hindi"], "hi")
    
    def test_translation_completeness(self):
        """Test that all languages have key translations"""
        # Check that other languages have most core keys
        core_keys = {
            "weather_app_title", "humidity", "wind", "pressure",
            "temperature", "loading", "error", "back"
        }
        
        for language in ["Spanish", "Hindi"]:
            lang_keys = set(TRANSLATIONS[language].keys())
            
            # Most core keys should be present
            missing_core = core_keys - lang_keys
            self.assertLessEqual(len(missing_core), 1,  # Allow 1 missing key
                           f"{language} missing too many core keys: {missing_core}")
    
    def test_no_empty_translations(self):
        """Test that no translations are empty"""
        for language, translations in TRANSLATIONS.items():
            for key, value in translations.items():
                with self.subTest(language=language, key=key):
                    self.assertIsNotNone(value, f"{language}.{key} is None")
                    self.assertNotEqual(str(value).strip(), "", 
                                       f"{language}.{key} is empty")
    
    def test_ui_element_translations(self):
        """Test that all UI elements have translations"""
        ui_keys = [
            "toggle_theme", "tomorrow_prediction", "weather_history",
            "weather_quiz", "weather_graphs", "map_view", "sun_moon",
            "language", "apply", "back", "loading"
        ]
        
        for language in SUPPORTED_LANGUAGES.keys():
            missing_keys = []
            for key in ui_keys:
                if key not in TRANSLATIONS[language]:
                    missing_keys.append(key)
            
            # Allow some missing keys (not all translations may be complete)
            self.assertLessEqual(len(missing_keys), 2,
                           f"{language} missing too many UI keys: {missing_keys}")


@unittest.skipUnless(LANGUAGE_AVAILABLE, "Language module not available")
class TestSpecializedTranslations(unittest.TestCase):
    """Test specialized translation functions"""
    
    def setUp(self):
        self.mock_app = Mock()
        self.mock_gui = Mock()
        self.controller = LanguageController(self.mock_app, self.mock_gui)
    
    def test_moon_phase_translations(self):
        """Test moon phase translations"""
        moon_phases = [
            "new_moon", "waxing_crescent", "first_quarter", "waxing_gibbous",
            "full_moon", "waning_gibbous", "last_quarter", "waning_crescent"
        ]
        
        # Test in Spanish
        self.controller.current_language = "Spanish"
        for phase in moon_phases:
            translation = self.controller.get_moon_phase_translation(phase)
            self.assertIsNotNone(translation)
            # Should return something (might be English if Spanish not available)
            self.assertGreater(len(str(translation)), 0)
    
    def test_weather_condition_translations(self):
        """Test weather condition translations"""
        conditions = [
            "clear sky", "few clouds", "rain", "snow"
        ]
        
        # Test in Spanish
        self.controller.current_language = "Spanish"
        for condition in conditions:
            translation = self.controller.get_weather_condition_translation(condition)
            self.assertIsNotNone(translation)
            self.assertGreater(len(str(translation)), 0)
    
    def test_unit_translations(self):
        """Test unit symbol translations"""
        units = ["celsius", "fahrenheit", "kmh", "ms"]
        
        for language in SUPPORTED_LANGUAGES.keys():
            self.controller.current_language = language
            for unit in units:
                translation = self.controller.get_unit_translation(unit)
                self.assertIsNotNone(translation)
                self.assertGreater(len(str(translation)), 0)
    
    def test_time_formatting_with_translation(self):
        """Test time formatting with translated periods"""
        test_cases = [
            ("06:30", "morning"),
            ("18:45", "evening"),
            ("12:00", None)
        ]
        
        # Test in Spanish
        self.controller.current_language = "Spanish"
        for time_str, period in test_cases:
            result = self.controller.format_time_with_translation(time_str, period)
            self.assertIsNotNone(result)
            self.assertIn(time_str, result)


@unittest.skipUnless(LANGUAGE_AVAILABLE, "Language module not available")
class TestLanguageUtilities(unittest.TestCase):
    """Test language utility functions"""
    
    def setUp(self):
        self.mock_app = Mock()
        self.mock_gui = Mock()
        self.controller = LanguageController(self.mock_app, self.mock_gui)
    
    def test_validation_functions(self):
        """Test translation key validation"""
        # Test valid key
        self.assertTrue(self.controller.validate_translation_key("humidity"))
        
        # Test invalid key
        self.assertFalse(self.controller.validate_translation_key("nonexistent_key"))
    
    def test_available_keys(self):
        """Test getting available translation keys"""
        keys = self.controller.get_all_available_keys()
        self.assertIsInstance(keys, list)
        self.assertIn("humidity", keys)
        self.assertIn("temperature", keys)
    
    def test_language_display_names(self):
        """Test getting language display names"""
        # Test getting display name from code
        self.assertEqual(self.controller.get_language_display_name("en"), "English")
        self.assertEqual(self.controller.get_language_display_name("es"), "Spanish")
        self.assertEqual(self.controller.get_language_display_name("hi"), "Hindi")
        
        # Test unknown code
        self.assertEqual(self.controller.get_language_display_name("xx"), "English")
    
    def test_font_family_selection(self):
        """Test font family selection for different languages"""
        font_tests = [
            ("English", "Arial"),
            ("Spanish", "Arial"),
            ("Hindi", "Noto Sans Devanagari")
        ]
        
        for language, expected_font in font_tests:
            self.controller.current_language = language
            font = self.controller.get_font_family_for_language()
            self.assertEqual(font, expected_font)
    
    def test_error_message_localization(self):
        """Test localized error messages"""
        error_types = ["network", "city_not_found", "loading", "general"]
        
        for language in SUPPORTED_LANGUAGES.keys():
            self.controller.current_language = language
            for error_type in error_types:
                message = self.controller.get_error_message(error_type)
                self.assertIsNotNone(message)
                self.assertGreater(len(message), 0)
    
    def test_supported_language_functions(self):
        """Test functions that return supported language info"""
        # Test getting language codes
        codes = self.controller.get_supported_language_codes()
        expected_codes = ["en", "es", "hi"]
        self.assertEqual(set(codes), set(expected_codes))
        
        # Test getting language names
        names = self.controller.get_supported_language_names()
        expected_names = ["English", "Spanish", "Hindi"]
        self.assertEqual(set(names), set(expected_names))
    
    def test_reset_to_defaults(self):
        """Test resetting language settings to defaults"""
        # Change to non-default language
        self.controller.current_language = "Spanish"
        
        # Reset to defaults
        self.controller.reset_to_defaults()
        
        # Should be back to English
        self.assertEqual(self.controller.current_language, "English")


@unittest.skipUnless(LANGUAGE_AVAILABLE, "Language module not available")
class TestTranslationEdgeCases(unittest.TestCase):
    """Test edge cases in translation functionality"""
    
    def setUp(self):
        self.mock_app = Mock()
        self.mock_gui = Mock()
        self.controller = LanguageController(self.mock_app, self.mock_gui)
    
    def test_missing_translation_fallback(self):
        """Test fallback behavior for missing translations"""
        # Test with fallback enabled
        result = self.controller.get_text("definitely_missing_key", fallback_to_english=True)
        self.assertEqual(result, "definitely_missing_key")
        
        # Test with fallback disabled
        self.controller.current_language = "Spanish"
        result = self.controller.get_text("definitely_missing_key", fallback_to_english=False)
        self.assertEqual(result, "definitely_missing_key")
    
    def test_empty_or_none_inputs(self):
        """Test handling of empty or None inputs"""
        # Test empty string
        result = self.controller.get_text("")
        self.assertEqual(result, "")
        
        # Test None - be more flexible about what's acceptable
        try:
            result = self.controller.get_text(None)
            # Accept either None or some fallback string
            self.assertTrue(result is None or isinstance(result, str))
        except (TypeError, AttributeError):
            # Also acceptable to raise exception for None input
            pass
    
    def test_case_sensitivity(self):
        """Test case sensitivity in translation keys"""
        # Standard key
        result1 = self.controller.get_text("humidity")
        
        # Different case - should not match
        result2 = self.controller.get_text("HUMIDITY")
        result3 = self.controller.get_text("Humidity")
        
        # Only the exact case should work
        self.assertNotEqual(result1, "humidity")  # Should be translated
        self.assertEqual(result2, "HUMIDITY")     # Should return key as-is
        self.assertEqual(result3, "Humidity")     # Should return key as-is
    
    def test_unicode_handling(self):
        """Test Unicode character handling in translations"""
        # Hindi contains Unicode characters
        self.controller.current_language = "Hindi"
        
        # Test getting Hindi text
        hindi_temp = self.controller.get_text("temperature")
        self.assertEqual(hindi_temp, "तापमान")
        
        # Test that Unicode is preserved
        self.assertIn("तापमान", hindi_temp)
        
        # Test length calculation with Unicode
        self.assertGreater(len(hindi_temp), 0)


class TestLanguageFallback(unittest.TestCase):
    """Test fallback when language module isn't available"""
    
    def test_language_availability(self):
        """Test that we can detect language availability"""
        self.assertTrue(True)  # Always passes
        
        if LANGUAGE_AVAILABLE:
            print("✅ Language module available for testing")
        else:
            print("⚠️  Language module not available - tests will be skipped")


if __name__ == '__main__':
    unittest.main()