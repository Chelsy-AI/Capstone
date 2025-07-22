"""
Sun and Moon Phases Controller
Manages the sun/moon page logic and coordinates between API and display
"""

import threading
import traceback
from .api import fetch_sun_moon_data
from .display import SunMoonDisplay


class SunMoonController:
    """
    Controller for the Sun and Moon Phases feature
    Manages data fetching, display updates, and animations
    """
    
    def __init__(self, app, gui_controller):
        self.app = app
        self.gui = gui_controller
        self.display = SunMoonDisplay(app, gui_controller)
        
        # Data cache
        self.current_data = {}
        self.is_fetching = False
        
    
    def build_page(self, window_width, window_height):
        """Build the sun/moon page"""
        try:
            self.display.build_sun_moon_page(window_width, window_height)
            
            # Start celestial animations
            self.display.start_celestial_animation()
            
            
        except Exception as e:
            traceback.print_exc()
    
    def update_display(self, city):
        """Update the sun/moon display for a city"""
        if self.is_fetching:
            return
        
        
        # Start background thread to fetch data
        threading.Thread(
            target=self._fetch_and_update, 
            args=(city,), 
            daemon=True
        ).start()
    
    def _fetch_and_update(self, city):
        """Fetch sun/moon data and update display (background thread)"""
        try:
            self.is_fetching = True
            
            # Fetch data from API
            sun_moon_data = fetch_sun_moon_data(city)
            
            # Store data
            self.current_data = sun_moon_data
            
            # Update display on main thread
            self.app.after(0, lambda: self._update_display_safe(sun_moon_data))
            
        except Exception as e:
            traceback.print_exc()
            
            # Show error on main thread
            error_data = {"error": str(e), "city": city}
            self.app.after(0, lambda: self._update_display_safe(error_data))
            
        finally:
            self.is_fetching = False
    
    def _update_display_safe(self, sun_moon_data):
        """Safely update display on main thread"""
        try:
            self.display.update_sun_moon_display(sun_moon_data)
            
        except Exception as e:
            traceback.print_exc()
    
    def refresh_data(self):
        """Refresh current data"""
        if self.current_data and "city" in self.current_data:
            city = self.current_data["city"]
            self.update_display(city)
        else:
            # Use current city from app
            city = self.app.city_var.get().strip() or "New York"
            self.update_display(city)
    
    def handle_theme_change(self):
        """Handle theme changes"""
        try:
            self.display.update_for_theme_change()
            
        except Exception as e:
            pass
    
    def get_current_data(self):
        """Get current sun/moon data"""
        return self.current_data.copy() if self.current_data else {}
    
    def is_data_available(self):
        """Check if data is available and valid"""
        return bool(self.current_data and not self.current_data.get("error"))
    
    def get_sun_position(self):
        """Get current sun position"""
        if self.is_data_available():
            return self.current_data.get("sun_position", {})
        return {}
    
    def get_moon_phase(self):
        """Get current moon phase information"""
        if self.is_data_available():
            return {
                "phase": self.current_data.get("moon_phase", 0),
                "name": self.current_data.get("moon_phase_name", "Unknown"),
                "illumination": self.current_data.get("moon_illumination", 0)
            }
        return {}
    
    def is_daytime(self):
        """Check if it's currently daytime"""
        if self.is_data_available():
            return self.current_data.get("is_daytime", True)
        
        # Fallback to simple time check
        import datetime
        current_hour = datetime.datetime.now().hour
        return 6 <= current_hour < 18
    
    def get_golden_hour_info(self):
        """Get golden hour timing information"""
        try:
            if self.is_data_available():
                from .api import calculate_golden_hour
                sunrise = self.current_data.get("sunrise")
                sunset = self.current_data.get("sunset")
                return calculate_golden_hour(sunrise, sunset)
            return {}
            
        except Exception as e:
            return {}
    
    def start_auto_refresh(self, interval_minutes=30):
        """Start automatic data refresh"""
        try:
            interval_ms = interval_minutes * 60 * 1000
            
            def auto_refresh():
                if hasattr(self, 'app') and self.app:
                    self.refresh_data()
                    # Schedule next refresh
                    self.app.after(interval_ms, auto_refresh)
            
            # Start auto refresh
            self.app.after(interval_ms, auto_refresh)
            
        except Exception as e:
            pass
    
    def stop_auto_refresh(self):
        """Stop automatic data refresh"""
    
    def export_data(self):
        """Export current sun/moon data for sharing"""
        try:
            if not self.is_data_available():
                return None
            
            export_data = {
                "city": self.current_data.get("city", "Unknown"),
                "date": self.current_data.get("current_time", ""),
                "sunrise": self.current_data.get("sunrise"),
                "sunset": self.current_data.get("sunset"),
                "moon_phase": self.current_data.get("moon_phase_name", "Unknown"),
                "moon_illumination": self.current_data.get("moon_illumination", 0),
                "sun_elevation": self.current_data.get("sun_position", {}).get("elevation", 0),
                "is_daytime": self.current_data.get("is_daytime", True)
            }
            
            return export_data
            
        except Exception as e:
            return None
    
    def cleanup(self):
        """Clean up resources"""
        try:
            
            # Stop animations
            if hasattr(self, 'display'):
                self.display.cleanup()
            
            # Clear data
            self.current_data.clear()
            self.is_fetching = False
            
            
        except Exception as e:
            pass


class SunMoonDataManager:
    """
    Advanced data management for sun/moon information
    Handles caching, persistence, and data validation
    """
    
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
        
    def get_cached_data(self, city):
        """Get cached data if still valid"""
        import time
        
        if city in self.cache:
            data, timestamp = self.cache[city]
            if time.time() - timestamp < self.cache_timeout:
                return data
        
        return None
    
    def cache_data(self, city, data):
        """Cache data with timestamp"""
        import time
        self.cache[city] = (data.copy(), time.time())
    
    def validate_data(self, data):
        """Validate sun/moon data structure"""
        required_fields = [
            "city", "sunrise", "sunset", "moon_phase", 
            "sun_position", "is_daytime"
        ]
        
        return all(field in data for field in required_fields)
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()


# Test function
if __name__ == "__main__":
    
    # This would normally be called by the main app
    # Just testing the data fetching part
    from .api import fetch_sun_moon_data
    
    test_cities = ["New York", "London", "Tokyo"]
    
    for city in test_cities:
        data = fetch_sun_moon_data(city)
                    