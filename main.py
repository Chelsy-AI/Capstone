"""
Main Entry Point for Weather Dashboard
"""

import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_dependencies():
    """Check if all required dependencies are available"""
    required_modules = [
        'tkinter',
        'requests', 
        'PIL',
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module} found")
        except ImportError:
            missing.append(module)
            print(f"❌ {module} missing")
    
    if missing:
        print(f"\nMissing dependencies: {', '.join(missing)}")
        print("Please install them using: pip install requests pillow")
        return False
    
    print("✓ All dependencies found")
    return True


def create_data_directory():
    """Ensure data directory exists for CSV storage"""
    data_dir = os.path.join(project_root, 'data')
    try:
        os.makedirs(data_dir, exist_ok=True)
        print(f"✓ Data directory ready: {data_dir}")
        return True
    except Exception as e:
        print(f"❌ Failed to create data directory: {e}")
        return False


def run_weather_app():
    """Run the weather application with error handling"""
    try:
        print("Starting Weather Application...")
        print("=" * 40)

        # Check dependencies
        if not check_dependencies():
            print("\n❌ Cannot start app - missing dependencies")
            return False
        
        # Create data directory
        if not create_data_directory():
            print("\n⚠️ Warning: Could not create data directory")
        
        # Import and run the app
        print("\n🚀 Launching weather app...")
        from config.weather_app import run_app
        run_app()
        
        print("\n✓ Weather app closed successfully")
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 App interrupted by user")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Check if all files are in the correct location")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point with comprehensive error handling"""
    
    print("🌤️ Weather Dashboard Starting...")
    print("================================")
    
    # Run the application
    success = run_weather_app()
    
    if not success:
        print("\n❌ Application failed to start properly")
        print("Please check the error messages above")
    
    # Keep console open on Windows for debugging
    if os.name == 'nt':
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()