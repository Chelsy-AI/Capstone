"""
Test Runner - Run all weather app tests with detailed reporting
==============================================================

This script runs all tests and provides comprehensive reporting.
"""

import unittest
import sys
import os
import time
from io import StringIO

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


class ColoredTextTestResult(unittest.TextTestResult):
    """Test result class with colored output for better readability"""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.success_count = 0
        self.verbosity = verbosity
        
    def addSuccess(self, test):
        super().addSuccess(test)
        self.success_count += 1
        if self.verbosity > 1:
            self.stream.write("✅ ")
            self.stream.write(str(test))
            self.stream.writeln(" ... ok")
    
    def addError(self, test, err):
        super().addError(test, err)
        if self.verbosity > 1:
            self.stream.write("❌ ")
            self.stream.write(str(test))
            self.stream.writeln(" ... ERROR")
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        if self.verbosity > 1:
            self.stream.write("❌ ")
            self.stream.write(str(test))
            self.stream.writeln(" ... FAIL")
    
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        if self.verbosity > 1:
            self.stream.write("⏭️  ")
            self.stream.write(str(test))
            self.stream.writeln(f" ... skipped: {reason}")


class ColoredTextTestRunner(unittest.TextTestRunner):
    """Test runner with colored output"""
    
    def __init__(self, **kwargs):
        kwargs['resultclass'] = ColoredTextTestResult
        super().__init__(**kwargs)


def discover_and_run_tests(test_directory="tests", pattern="test_*.py", verbosity=2):
    """
    Discover and run all tests in the test directory.
    
    Args:
        test_directory (str): Directory containing test files
        pattern (str): Pattern to match test files
        verbosity (int): Level of output detail (0=quiet, 1=normal, 2=verbose)
    
    Returns:
        unittest.TestResult: Test results
    """
    # Discover all tests
    loader = unittest.TestLoader()
    
    # If test directory doesn't exist, try current directory
    if not os.path.exists(test_directory):
        test_directory = os.path.dirname(os.path.abspath(__file__))
    
    try:
        suite = loader.discover(test_directory, pattern=pattern)
    except ImportError as e:
        print(f"❌ Error discovering tests: {e}")
        print("Make sure all test dependencies are installed.")
        return None
    
    # Run the tests
    runner = ColoredTextTestRunner(verbosity=verbosity, buffer=True)
    result = runner.run(suite)
    
    return result


def run_specific_test_file(test_file, verbosity=2):
    """
    Run a specific test file.
    
    Args:
        test_file (str): Path to test file
        verbosity (int): Level of output detail
    
    Returns:
        unittest.TestResult: Test results
    """
    loader = unittest.TestLoader()
    
    try:
        # Remove .py extension if present
        if test_file.endswith('.py'):
            test_file = test_file[:-3]
        
        # Load the test module
        suite = loader.loadTestsFromName(test_file)
        
        # Run the tests
        runner = ColoredTextTestRunner(verbosity=verbosity, buffer=True)
        result = runner.run(suite)
        
        return result
        
    except ImportError as e:
        print(f"❌ Error loading test file '{test_file}': {e}")
        return None


def print_test_summary(result):
    """
    Print a detailed summary of test results.
    
    Args:
        result (unittest.TestResult): Test results to summarize
    """
    if not result:
        return
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped)
    successes = total_tests - failures - errors - skipped
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    print(f"Total Tests:     {total_tests}")
    print(f"✅ Passed:       {successes}")
    print(f"❌ Failed:       {failures}")
    print(f"❌ Errors:       {errors}")
    print(f"⏭️  Skipped:      {skipped}")
    
    # Calculate success rate
    if total_tests > 0:
        success_rate = (successes / total_tests) * 100
        print(f"Success Rate:   {success_rate:.1f}%")
    
    print("="*60)
    
    # Print failures and errors in detail
    if failures:
        print("\nFAILURES:")
        print("-" * 40)
        for test, traceback in result.failures:
            print(f"❌ {test}")
            print(f"   {traceback}")
            print()
    
    if errors:
        print("\nERRORS:")
        print("-" * 40)
        for test, traceback in result.errors:
            print(f"❌ {test}")
            print(f"   {traceback}")
            print()
    
    if skipped:
        print("\nSKIPPED:")
        print("-" * 40)
        for test, reason in result.skipped:
            print(f"⏭️  {test}")
            print(f"   Reason: {reason}")
            print()


def run_test_categories():
    """Run tests by category and provide category-specific reporting"""
    
    test_categories = [
        ("API Tests", "test_api_simple"),
        ("Validation Tests", "test_validation_simple"), 
        ("Utility Tests", "test_utils_simple"),
        ("Storage Tests", "test_storage_simple"),
        ("Language Tests", "test_language_simple")
    ]
    
    print("🧪 Running Weather App Test Suite")
    print("=" * 50)
    
    overall_results = {
        'total': 0,
        'passed': 0, 
        'failed': 0,
        'errors': 0,
        'skipped': 0
    }
    
    category_results = []
    
    for category_name, test_module in test_categories:
        print(f"\n🔍 Running {category_name}...")
        print("-" * 30)
        
        start_time = time.time()
        result = run_specific_test_file(test_module, verbosity=1)
        end_time = time.time()
        
        if result:
            # Calculate results for this category
            total = result.testsRun
            failures = len(result.failures)
            errors = len(result.errors)
            skipped = len(result.skipped)
            passed = total - failures - errors - skipped
            duration = end_time - start_time
            
            # Update overall results
            overall_results['total'] += total
            overall_results['passed'] += passed
            overall_results['failed'] += failures
            overall_results['errors'] += errors
            overall_results['skipped'] += skipped
            
            # Store category results
            category_results.append({
                'name': category_name,
                'total': total,
                'passed': passed,
                'failed': failures,
                'errors': errors,
                'skipped': skipped,
                'duration': duration,
                'success_rate': (passed / total * 100) if total > 0 else 0
            })
            
            # Print category summary
            status = "✅ PASSED" if (failures + errors == 0) else "❌ FAILED"
            print(f"{status} - {passed}/{total} tests passed ({duration:.2f}s)")
            
            if failures > 0:
                print(f"   ❌ {failures} failures")
            if errors > 0:
                print(f"   ❌ {errors} errors")
            if skipped > 0:
                print(f"   ⏭️  {skipped} skipped")
        else:
            print(f"❌ Could not run {category_name}")
            category_results.append({
                'name': category_name,
                'total': 0,
                'passed': 0,
                'failed': 0,
                'errors': 1,
                'skipped': 0,
                'duration': 0,
                'success_rate': 0
            })
    
    # Print overall summary
    print("\n" + "="*60)
    print("OVERALL TEST SUMMARY")
    print("="*60)
    
    for cat in category_results:
        status_icon = "✅" if (cat['failed'] + cat['errors'] == 0) else "❌"
        print(f"{status_icon} {cat['name']:<20} {cat['passed']:>3}/{cat['total']:<3} "
              f"({cat['success_rate']:>5.1f}%) {cat['duration']:>6.2f}s")
    
    print("-" * 60)
    overall_success_rate = (overall_results['passed'] / overall_results['total'] * 100) if overall_results['total'] > 0 else 0
    print(f"{'🎯 TOTAL':<20} {overall_results['passed']:>3}/{overall_results['total']:<3} "
          f"({overall_success_rate:>5.1f}%)")
    
    if overall_results['failed'] > 0:
        print(f"❌ Total Failures: {overall_results['failed']}")
    if overall_results['errors'] > 0:
        print(f"❌ Total Errors: {overall_results['errors']}")
    if overall_results['skipped'] > 0:
        print(f"⏭️  Total Skipped: {overall_results['skipped']}")
    
    print("="*60)
    
    # Return overall success status
    return overall_results['failed'] == 0 and overall_results['errors'] == 0


def check_test_dependencies():
    """Check if test dependencies are available"""
    
    print("🔍 Checking test dependencies...")
    
    required_modules = [
        'unittest',
        'tempfile', 
        'json',
        'csv',
        'datetime'
    ]
    
    optional_modules = [
        'requests',
        'PIL'
    ]
    
    missing_required = []
    missing_optional = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            missing_required.append(module)
            print(f"❌ {module} (required)")
    
    for module in optional_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            missing_optional.append(module)
            print(f"⚠️  {module} (optional)")
    
    if missing_required:
        print(f"\n❌ Missing required modules: {', '.join(missing_required)}")
        print("Please install missing modules before running tests.")
        return False
    
    if missing_optional:
        print(f"\n⚠️  Missing optional modules: {', '.join(missing_optional)}")
        print("Some tests may be skipped.")
    
    print("✅ Dependencies check passed!\n")
    return True


def main():
    """Main function to run tests based on command line arguments"""
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "check":
            # Just check dependencies
            check_test_dependencies()
            return
        
        elif command == "categories":
            # Run tests by category
            if not check_test_dependencies():
                sys.exit(1)
            
            success = run_test_categories()
            sys.exit(0 if success else 1)
        
        elif command.startswith("test_"):
            # Run specific test file
            if not check_test_dependencies():
                sys.exit(1)
            
            print(f"🧪 Running {command}...")
            result = run_specific_test_file(command, verbosity=2)
            print_test_summary(result)
            
            if result:
                success = len(result.failures) == 0 and len(result.errors) == 0
                sys.exit(0 if success else 1)
            else:
                sys.exit(1)
        
        elif command in ["help", "-h", "--help"]:
            print("Weather App Test Runner")
            print("=" * 30)
            print("Usage:")
            print("  python run_tests.py                 - Run all tests")
            print("  python run_tests.py categories      - Run tests by category") 
            print("  python run_tests.py test_api        - Run specific test file")
            print("  python run_tests.py check           - Check dependencies only")
            print("  python run_tests.py help            - Show this help")
            print()
            print("Available test files:")
            print("  test_api        - API and weather data tests")
            print("  test_validation - City validation and error handling tests")
            print("  test_utils      - Utility function tests")
            print("  test_storage    - Data storage and CSV tests")
            print("  test_language   - Language and translation tests")
            return
        
        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'python run_tests.py help' for usage information.")
            sys.exit(1)
    
    else:
        # Default: run all tests
        if not check_test_dependencies():
            sys.exit(1)
        
        print("🧪 Running All Weather App Tests...")
        print("=" * 40)
        
        start_time = time.time()
        result = discover_and_run_tests(verbosity=2)
        end_time = time.time()
        
        if result:
            print_test_summary(result)
            print(f"\nTotal test time: {end_time - start_time:.2f} seconds")
            
            # Exit with error code if tests failed
            success = len(result.failures) == 0 and len(result.errors) == 0
            if success:
                print("\n🎉 All tests passed!")
            else:
                print("\n⚠️  Some tests failed. Check the details above.")
            
            sys.exit(0 if success else 1)
        else:
            print("❌ Could not run tests")
            sys.exit(1)


if __name__ == "__main__":
    main()