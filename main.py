#!/usr/bin/env python3
"""
Fixed Main Entry Point for Weather Dashboard
This version ensures all components work together properly
"""

import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_dependencies():
    """Check if all required dependencies are available"""
    required_modules = [
        'tkinter',
        'requests', 
        'PIL',
        'customtkinter'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"❌ Missing required modules: {', '.join(missing)}")
        print("Please install with: pip install -r requirements.txt")
        return False
    
    return True


def create_data_directory():
    """Ensure data directory exists for CSV storage"""
    data_dir = os.path.join(project_root, 'data')
    try:
        os.makedirs(data_dir, exist_ok=True)
        print(f"✅ Data directory ready: {data_dir}")
        return True
    except Exception as e:
        print(f"⚠️ Could not create data directory: {e}")
        return False


def run_weather_app():
    """Run the weather application with error handling"""
    try:
        print("🌤️ Starting Advanced Weather Dashboard...")
        print("=" * 50)
        
        # Check dependencies
        if not check_dependencies():
            return False
        
        # Create data directory
        create_data_directory()
        
        # Import and run the fixed app
        try:
            # Try to import the fixed app first
            exec(open('fixed_weather_app.py').read())
        except FileNotFoundError:
            # Fallback to original app structure
            from core.app import run_app
            run_app()
        
        return True
        
    except KeyboardInterrupt:
        print("\n⚡ Application interrupted by user")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all required files are in place")
        print("and dependencies are installed with: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point with comprehensive error handling"""
    print("🚀 Weather Dashboard Launcher")
    print("Python version:", sys.version)
    print("Working directory:", os.getcwd())
    print()
    
    success = run_weather_app()
    
    if success:
        print("\n✅ Application closed successfully")
    else:
        print("\n❌ Application failed to start")
        print("\nTroubleshooting tips:")
        print("1. Ensure Python 3.7+ is installed")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Check that all project files are in place")
        print("4. Verify internet connection for weather data")
    
    # Keep console open on Windows
    if os.name == 'nt':
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()