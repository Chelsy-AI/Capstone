#!/usr/bin/env python3
"""
Comprehensive Feature Test Suite
=================================

Master test runner that executes all feature tests and provides
a comprehensive overview of the weather application's functionality.

Features tested:
- City Comparison
- Weather Graphs  
- History Tracker
- Interactive Map
- Sun & Moon Phases
- Theme Switcher
- Tomorrow's Weather Prediction
- Weather Quiz
- Weather Icons

This provides a complete health check of all weather app features.
"""

import sys
import os
import unittest
import time
from io import StringIO

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all feature test modules with safer error handling
def safe_import_test_module(module_name, function_name):
    """Safely import a test module and function."""
    try:
        module = __import__(module_name, fromlist=[function_name])
        return getattr(module, function_name), True
    except (ImportError, AttributeError) as e:
        return None, False

# Import test functions
run_city_comparison_tests, CITY_COMPARISON_AVAILABLE = safe_import_test_module('test_city_comparison', 'run_city_comparison_tests')
run_graphs_tests, GRAPHS_AVAILABLE = safe_import_test_module('test_graphs', 'run_graphs_tests')
run_history_tracker_tests, HISTORY_TRACKER_AVAILABLE = safe_import_test_module('test_history_tracker', 'run_history_tracker_tests')
run_interactive_map_tests, INTERACTIVE_MAP_AVAILABLE = safe_import_test_module('test_interactive_map', 'run_interactive_map_tests')
run_sun_moon_phases_tests, SUN_MOON_PHASES_AVAILABLE = safe_import_test_module('test_sun_moon_phases', 'run_sun_moon_phases_tests')
run_theme_switcher_tests, THEME_SWITCHER_AVAILABLE = safe_import_test_module('test_theme_switcher', 'run_theme_switcher_tests')
run_tomorrows_guess_tests, TOMORROWS_GUESS_AVAILABLE = safe_import_test_module('test_tomorrows_guess', 'run_tomorrows_guess_tests')
run_weather_quiz_tests, WEATHER_QUIZ_AVAILABLE = safe_import_test_module('test_weather_quiz', 'run_weather_quiz_tests')
run_weather_icons_tests, WEATHER_ICONS_AVAILABLE = safe_import_test_module('test_weather_icons', 'run_weather_icons_tests')


def print_test_header():
    """Print test suite header."""
    print("🌤️  Weather App - Comprehensive Feature Test Suite")
    print("=" * 60)
    print("Testing all weather application features...")
    print()


def print_test_summary(results):
    """Print test results summary."""
    print()
    print("=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    total_features = len(results)
    passed_features = sum(1 for result in results.values() if result)
    failed_features = total_features - passed_features
    
    print(f"Features Tested: {total_features}")
    print(f"✅ Passed: {passed_features}")
    print(f"❌ Failed: {failed_features}")
    print()
    
    # Detailed results
    for feature_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} - {feature_name}")
    
    print()
    
    # Overall assessment
    success_rate = (passed_features / total_features) * 100 if total_features > 0 else 0
    
    if success_rate >= 90:
        print("🎉 EXCELLENT - All core features working properly!")
    elif success_rate >= 75:
        print("✅ GOOD - Most features working, minor issues detected")
    elif success_rate >= 50:
        print("⚠️  FAIR - Several features have issues, needs attention")
    else:
        print("❌ POOR - Major issues detected, significant problems")
    
    print(f"Overall Success Rate: {success_rate:.1f}%")
    return success_rate >= 75


def run_feature_test(test_function, feature_name, available):
    """Run a single feature test with error handling."""
    if not available or test_function is None:
        print(f"⚠️  {feature_name} - Test not available, skipping")
        return False
    
    try:
        start_time = time.time()
        result = test_function()
        end_time = time.time()
        
        duration = end_time - start_time
        if result:
            print(f"   ⏱️  Completed in {duration:.2f}s")
        
        return result
    except Exception as e:
        print(f"   💥 {feature_name} test crashed: {str(e)}")
        return False


def run_all_feature_tests():
    """Run all available feature tests."""
    print_test_header()
    
    # Define all tests
    feature_tests = [
        (run_city_comparison_tests, "City Comparison", CITY_COMPARISON_AVAILABLE),
        (run_graphs_tests, "Weather Graphs", GRAPHS_AVAILABLE),
        (run_history_tracker_tests, "History Tracker", HISTORY_TRACKER_AVAILABLE),
        (run_interactive_map_tests, "Interactive Map", INTERACTIVE_MAP_AVAILABLE),
        (run_sun_moon_phases_tests, "Sun & Moon Phases", SUN_MOON_PHASES_AVAILABLE),
        (run_theme_switcher_tests, "Theme Switcher", THEME_SWITCHER_AVAILABLE),
        (run_tomorrows_guess_tests, "Tomorrow's Weather Prediction", TOMORROWS_GUESS_AVAILABLE),
        (run_weather_quiz_tests, "Weather Quiz", WEATHER_QUIZ_AVAILABLE),
        (run_weather_icons_tests, "Weather Icons", WEATHER_ICONS_AVAILABLE)
    ]
    
    # Run each test
    results = {}
    total_start_time = time.time()
    
    for test_function, feature_name, available in feature_tests:
        print(f"Testing {feature_name}...")
        result = run_feature_test(test_function, feature_name, available)
        results[feature_name] = result
        print()
    
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    # Print summary
    overall_success = print_test_summary(results)
    print(f"Total Test Duration: {total_duration:.2f}s")
    
    return overall_success


def run_quick_smoke_test():
    """Run a quick smoke test to verify basic functionality."""
    print("🔥 Quick Smoke Test - Basic Functionality Check")
    print("-" * 50)
    
    smoke_test_results = {}
    
    # Test basic imports
    print("📦 Testing imports...")
    try:
        # Test core imports
        import features
        smoke_test_results["Core Imports"] = True
        print("   ✅ Core features imported successfully")
    except Exception as e:
        smoke_test_results["Core Imports"] = False
        print(f"   ❌ Core import failed: {e}")
    
    # Test language system
    print("🌍 Testing language system...")
    try:
        from language.controller import LanguageController
        from unittest.mock import Mock
        
        mock_app = Mock()
        mock_gui = Mock()
        lang_controller = LanguageController(mock_app, mock_gui)
        
        # Test basic translation
        text = lang_controller.get_text("humidity")
        if text == "Humidity":
            smoke_test_results["Language System"] = True
            print("   ✅ Language system working")
        else:
            smoke_test_results["Language System"] = False
            print(f"   ❌ Language system failed: got '{text}'")
    except Exception as e:
        smoke_test_results["Language System"] = False
        print(f"   ❌ Language system error: {e}")
    
    # Test config modules
    print("⚙️  Testing configuration...")
    try:
        # Test direct imports to avoid config/__init__.py issues
        sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config'))
        
        import api
        import storage
        import utils
        
        smoke_test_results["Configuration"] = True
        print("   ✅ Configuration modules loaded")
    except Exception as e:
        smoke_test_results["Configuration"] = False
        print(f"   ❌ Configuration failed: {e}")
    
    # Summary
    print()
    print("Smoke Test Results:")
    passed = sum(1 for result in smoke_test_results.values() if result)
    total = len(smoke_test_results)
    
    for test_name, result in smoke_test_results.items():
        status = "✅" if result else "❌"
        print(f"  {status} {test_name}")
    
    print(f"\nSmoke Test: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 Smoke test passed - basic functionality working!")
        return True
    else:
        print("⚠️  Smoke test issues detected - some basic functionality may be broken")
        return False


def check_test_environment():
    """Check if test environment is properly set up."""
    print("🔧 Environment Check")
    print("-" * 30)
    
    env_issues = []
    
    # Check Python version
    if sys.version_info < (3, 7):
        env_issues.append(f"Python {sys.version_info.major}.{sys.version_info.minor} too old (need 3.7+)")
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check if we're in the right directory
    expected_files = ['main.py', 'features', 'config', 'language', 'tests']
    missing_files = []
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for file_name in expected_files:
        if not os.path.exists(os.path.join(project_root, file_name)):
            missing_files.append(file_name)
    
    if missing_files:
        env_issues.append(f"Missing project files: {', '.join(missing_files)}")
    else:
        print("✅ Project structure looks correct")
    
    # Check for required test modules
    test_files = [
        'test_city_comparison.py',
        'test_graphs.py', 
        'test_history_tracker.py',
        'test_interactive_map.py',
        'test_sun_moon_phases.py',
        'test_theme_switcher.py',
        'test_tomorrows_guess.py',
        'test_weather_quiz.py',
        'test_weather_icons.py'
    ]
    
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    missing_tests = []
    for test_file in test_files:
        if not os.path.exists(os.path.join(tests_dir, test_file)):
            missing_tests.append(test_file)
    
    if missing_tests:
        env_issues.append(f"Missing test files: {', '.join(missing_tests)}")
    else:
        print("✅ All test files present")
    
    if env_issues:
        print("\n⚠️  Environment Issues:")
        for issue in env_issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ Environment check passed")
        return True


def main():
    """Main test runner."""
    print("🧪 Weather App Test Suite")
    print("========================")
    print()
    
    # Check environment first
    if not check_test_environment():
        print("\n❌ Environment issues detected. Please fix before running tests.")
        return False
    
    print()
    
    # Run smoke test first
    smoke_test_passed = run_quick_smoke_test()
    print()
    
    if not smoke_test_passed:
        print("⚠️  Smoke test failed. Continuing with feature tests but expect issues...")
        print()
    
    # Run comprehensive feature tests
    comprehensive_test_passed = run_all_feature_tests()
    
    # Final assessment
    print()
    print("🎯 FINAL ASSESSMENT")
    print("=" * 30)
    
    if smoke_test_passed and comprehensive_test_passed:
        print("🎉 ALL TESTS PASSED")
        print("Weather app is working excellently!")
        return True
    elif comprehensive_test_passed:
        print("✅ FEATURE TESTS PASSED")
        print("Weather app features working well despite minor setup issues")
        return True
    elif smoke_test_passed:
        print("⚠️  MIXED RESULTS")
        print("Basic functionality works but some features have issues")
        return False
    else:
        print("❌ MULTIPLE ISSUES DETECTED")
        print("Weather app needs significant fixes")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test suite interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Test suite crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)