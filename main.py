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
        'customtkinter'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        return False
    
    return True


def create_data_directory():
    """Ensure data directory exists for CSV storage"""
    data_dir = os.path.join(project_root, 'data')
    try:
        os.makedirs(data_dir, exist_ok=True)
        return True
    except Exception as e:
        return False


def run_weather_app():
    """Run the weather application with error handling"""
    try:

        # Check dependencies
        if not check_dependencies():
            return False
        
        # Create data directory
        create_data_directory()
        
        # Import and run the app
        from config.weather_app import run_app
        run_app()
        
        return True
        
    except KeyboardInterrupt:
        return True
        
    except ImportError as e:
        return False
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point with comprehensive error handling"""
            
    # Keep console open on Windows
    if os.name == 'nt':
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()