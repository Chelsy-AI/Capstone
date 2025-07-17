#!/usr/bin/env python3
"""
Main entry point for the Weather Dashboard application
"""

if __name__ == "__main__":
    try:
        from core.app import run_app
        run_app()
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure all required files are in place and dependencies are installed.")
        print("Run: pip install -r requirements.txt")
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()