#!/usr/bin/env python3
"""
Quick Test - Validate core weather app functionality
==================================================

Save this file as tests/quick_test.py and run with:
python3 tests/quick_test.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_city_validation():
    """Test the most important feature - blocking fake cities"""
    print("🔍 Testing city validation...")
    
    try:
        from config.error_handler import CityValidator
        validator = CityValidator()
        
        # Test fake cities are blocked
        fake_cities = ["khjl", "khjl;", "fnjaelf", "asdf", "test123"]
        for fake in fake_cities:
            if validator.is_valid_city(fake):
                print(f"❌ FAIL: Fake city '{fake}' was accepted")
                return False
            else:
                print(f"✅ PASS: Fake city '{fake}' blocked")
        
        # Test real cities are accepted
        real_cities = ["London", "New York", "Paris", "Tokyo"]
        for real in real_cities:
            if not validator.is_valid_city(real):
                print(f"❌ FAIL: Real city '{real}' was rejected")
                return False
            else:
                print(f"✅ PASS: Real city '{real}' accepted")
        
        print("✅ City validation working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ City validation test failed: {e}")
        return False

def test_temperature_conversion():
    """Test temperature conversion functions"""
    print("\n🔍 Testing temperature conversions...")
    
    try:
        from config.utils import celsius_to_fahrenheit, fahrenheit_to_celsius
        
        # Test basic conversions
        c_to_f = celsius_to_fahrenheit(0)  # Should be 32
        if abs(c_to_f - 32.0) < 0.1:
            print("✅ PASS: 0°C → 32°F")
        else:
            print(f"❌ FAIL: 0°C → {c_to_f}°F (expected 32)")
            return False
        
        f_to_c = fahrenheit_to_celsius(212)  # Should be 100
        if abs(f_to_c - 100.0) < 0.1:
            print("✅ PASS: 212°F → 100°C")
        else:
            print(f"❌ FAIL: 212°F → {f_to_c}°C (expected 100)")
            return False
        
        print("✅ Temperature conversions working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Temperature conversion test failed: {e}")
        return False

def test_language_system():
    """Test language/translation system"""
    print("\n🔍 Testing language system...")
    
    try:
        from language.controller import LanguageController
        from unittest.mock import Mock
        
        # Create mock app and controller
        mock_app = Mock()
        mock_gui = Mock()
        controller = LanguageController(mock_app, mock_gui)
        
        # Test English
        english_text = controller.get_text("humidity")
        if english_text == "Humidity":
            print("✅ PASS: English translation working")
        else:
            print(f"❌ FAIL: English humidity = '{english_text}' (expected 'Humidity')")
            return False
        
        # Test Spanish
        controller.current_language = "Spanish"
        spanish_text = controller.get_text("humidity")
        if spanish_text == "Humedad":
            print("✅ PASS: Spanish translation working")
        else:
            print(f"❌ FAIL: Spanish humidity = '{spanish_text}' (expected 'Humedad')")
            return False
        
        # Test Hindi
        controller.current_language = "Hindi"
        hindi_text = controller.get_text("temperature")
        if hindi_text == "तापमान":
            print("✅ PASS: Hindi translation working")
        else:
            print(f"❌ FAIL: Hindi temperature = '{hindi_text}' (expected 'तापमान')")
            return False
        
        print("✅ Language system working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Language system test failed: {e}")
        return False

def test_storage_system():
    """Test weather data storage"""
    print("\n🔍 Testing storage system...")
    
    try:
        from config.storage import save_weather, load_weather_history
        import tempfile
        import os
        import time
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        temp_file.close()
        test_path = temp_file.name
        
        # Test saving weather data
        test_data = {
            "temperature": 25.5,
            "description": "Clear sky",
            "humidity": 60
        }
        
        save_weather(test_data, "London", test_path)
        time.sleep(0.1)  # Give it time to write
        
        # Test loading weather data
        history = load_weather_history(test_path)
        
        if len(history) > 0:
            print("✅ PASS: Weather data saved and loaded")
        else:
            print("❌ FAIL: No weather data found in history")
            return False
        
        # Cleanup
        try:
            os.unlink(test_path)
        except:
            pass
        
        print("✅ Storage system working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Storage system test failed: {e}")
        return False

def test_api_functions():
    """Test API functions with mocked data"""
    print("\n🔍 Testing API functions...")
    
    try:
        from config.api import get_lat_lon
        from unittest.mock import patch, Mock
        
        # Test geocoding with mocked response
        with patch('config.api.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "results": [{"latitude": 51.5074, "longitude": -0.1278}]
            }
            mock_get.return_value = mock_response
            
            lat, lon = get_lat_lon("London")
            
            if lat == 51.5074 and lon == -0.1278:
                print("✅ PASS: Geocoding API function working")
            else:
                print(f"❌ FAIL: Geocoding returned {lat}, {lon}")
                return False
        
        print("✅ API functions working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ API functions test failed: {e}")
        return False

def main():
    """Run all quick tests"""
    print("🧪 Quick Weather App Test Suite")
    print("=" * 50)
    
    all_tests = [
        test_city_validation,
        test_temperature_conversion,
        test_language_system,
        test_storage_system,
        test_api_functions
    ]
    
    passed = 0
    total = len(all_tests)
    
    for test_func in all_tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test_func.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All core functionality working!")
        return True
    else:
        print("⚠️  Some issues detected - but core features may still work")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)