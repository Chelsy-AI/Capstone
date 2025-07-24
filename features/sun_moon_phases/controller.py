"""
Sun and Moon Phases Controller
===============================

This file manages the sun and moon phases feature of our weather application.
It coordinates between getting astronomical data and displaying it on screen.

Key Responsibilities:
- Fetching sun and moon data from APIs
- Managing the visual display of celestial information  
- Handling user interactions and auto-refresh
- Caching data for performance
"""

import threading
import traceback
import time
from datetime import datetime
from .api import fetch_sun_moon_data
from .display import SunMoonDisplay


class SunMoonController:
    """
    Main controller class for the Sun and Moon Phases feature.
    
    Coordinates between API calls, display updates, and user interactions.
    """
    
    def __init__(self, app, gui_controller):
        """
        Initialize the sun/moon controller.
        
        Args:
            app: The main weather application window
            gui_controller: The GUI controller that manages different pages
        """
        self.app = app
        self.gui = gui_controller
        self.display = SunMoonDisplay(app, gui_controller)
        
        # Data management
        self.current_data = {}
        self.is_fetching = False
        
        # Data caching
        self._data_cache = {}
        self._cache_timestamps = {}
        self._cache_duration = 600  # Cache for 10 minutes
        
        # Auto-refresh settings
        self._auto_refresh_enabled = False
        self._refresh_interval = 1800  # 30 minutes
        self._last_refresh_time = 0
        
        # Error handling
        self._consecutive_errors = 0
        self._max_error_count = 3
        
    def build_page(self, window_width, window_height):
        """Build the complete sun/moon page interface."""
        try:
            self.display.build_sun_moon_page(window_width, window_height)
            self.display.start_celestial_animation()
            
        except Exception as e:
            print(f"Error building sun/moon page: {e}")
            traceback.print_exc()
    
    def update_display(self, city):
        """
        Update the sun/moon display for a specific city.
        
        Args:
            city (str): Name of the city to get sun/moon data for
        """
        if self.is_fetching:
            return
        
        # Check for cached data
        if self._has_fresh_cached_data(city):
            cached_data = self._get_cached_data(city)
            self._update_display_safe(cached_data)
            return
        
        # Fetch fresh data in background thread
        threading.Thread(
            target=self._fetch_and_update, 
            args=(city,), 
            daemon=True
        ).start()
    
    def _has_fresh_cached_data(self, city):
        """Check if we have recent cached data for a city."""
        if city not in self._data_cache:
            return False
        
        cache_time = self._cache_timestamps.get(city, 0)
        current_time = time.time()
        
        return (current_time - cache_time) < self._cache_duration
    
    def _get_cached_data(self, city):
        """Retrieve cached data for a city."""
        return self._data_cache.get(city, {}).copy()
    
    def _cache_data(self, city, data):
        """Cache sun/moon data for a city."""
        self._data_cache[city] = data.copy()
        self._cache_timestamps[city] = time.time()
        self._clean_old_cache_entries()
    
    def _clean_old_cache_entries(self):
        """Remove old cached data to keep memory usage reasonable."""
        current_time = time.time()
        cities_to_remove = []
        
        for city, cache_time in self._cache_timestamps.items():
            if (current_time - cache_time) > (self._cache_duration * 2):
                cities_to_remove.append(city)
        
        for city in cities_to_remove:
            self._data_cache.pop(city, None)
            self._cache_timestamps.pop(city, None)
    
    def _fetch_and_update(self, city):
        """Fetch sun/moon data and update display (runs in background thread)."""
        try:
            self.is_fetching = True
            self._last_refresh_time = time.time()
            
            # Fetch data from API
            sun_moon_data = fetch_sun_moon_data(city)
            sun_moon_data['city'] = city
            
            # Cache the data
            self._cache_data(city, sun_moon_data)
            self.current_data = sun_moon_data
            
            # Reset error counter
            self._consecutive_errors = 0
            
            # Update display on main thread
            self.app.after(0, lambda: self._update_display_safe(sun_moon_data))
            
        except Exception as e:
            print(f"Error fetching sun/moon data for {city}: {e}")
            traceback.print_exc()
            
            self._consecutive_errors += 1
            
            error_data = {
                "error": str(e), 
                "city": city,
                "error_count": self._consecutive_errors
            }
            
            self.app.after(0, lambda: self._update_display_safe(error_data))
            
        finally:
            self.is_fetching = False
    
    def _update_display_safe(self, sun_moon_data):
        """Safely update the display on the main GUI thread."""
        try:
            self.display.update_sun_moon_display(sun_moon_data)
        except Exception as e:
            print(f"Error updating sun/moon display: {e}")
            traceback.print_exc()
    
    def refresh_data(self):
        """Manually refresh the current sun/moon data."""
        city = self._get_current_city()
        
        # Clear cached data to force fresh fetch
        self._data_cache.pop(city, None)
        self._cache_timestamps.pop(city, None)
        
        self.update_display(city)
    
    def _get_current_city(self):
        """Get the current city name from the main application."""
        try:
            if hasattr(self.app, 'city_var') and self.app.city_var:
                city = self.app.city_var.get().strip()
                return city if city else "New York"
            return "New York"
        except Exception:
            return "New York"
    
    def start_auto_refresh(self, interval_minutes=30):
        """
        Start automatic data refresh at specified intervals.
        
        Args:
            interval_minutes (int): Refresh interval in minutes
        """
        self._refresh_interval = interval_minutes * 60  # Convert to seconds
        self._enable_auto_refresh()
    
    def _enable_auto_refresh(self):
        """Enable automatic data refresh at regular intervals."""
        if self._auto_refresh_enabled:
            return
        
        self._auto_refresh_enabled = True
        self._schedule_auto_refresh()
    
    def _schedule_auto_refresh(self):
        """Schedule the next automatic refresh."""
        if not self._auto_refresh_enabled:
            return
        
        def auto_refresh():
            if self._auto_refresh_enabled and hasattr(self, 'app') and self.app:
                current_time = time.time()
                if (current_time - self._last_refresh_time) >= self._refresh_interval:
                    city = self._get_current_city()
                    self.update_display(city)
                
                self._schedule_auto_refresh()
        
        refresh_delay = self._refresh_interval * 1000  # Convert to milliseconds
        self.app.after(refresh_delay, auto_refresh)
    
    def disable_auto_refresh(self):
        """Disable automatic data refresh."""
        self._auto_refresh_enabled = False
    
    def handle_theme_change(self):
        """Handle changes to the application theme."""
        try:
            self.display.update_for_theme_change()
        except Exception:
            pass
    
    def get_current_data(self):
        """Get a copy of the current sun/moon data."""
        return self.current_data.copy() if self.current_data else {}
    
    def is_data_available(self):
        """Check if valid sun/moon data is currently available."""
        return bool(self.current_data and not self.current_data.get("error"))
    
    def get_sun_position(self):
        """Get current sun position information."""
        if self.is_data_available():
            return self.current_data.get("sun_position", {})
        return {}
    
    def get_moon_phase(self):
        """Get current moon phase information."""
        if self.is_data_available():
            return {
                "phase": self.current_data.get("moon_phase", 0),
                "name": self.current_data.get("moon_phase_name", "Unknown"),
                "illumination": self.current_data.get("moon_illumination", 0)
            }
        return {}
    
    def is_daytime(self):
        """Check if it's currently daytime based on the latest data."""
        if self.is_data_available():
            return self.current_data.get("is_daytime", True)
        
        # Fallback: simple time-based check
        current_hour = datetime.now().hour
        return 6 <= current_hour < 18
    
    def get_golden_hour_info(self):
        """Calculate golden hour timing information."""
        try:
            if self.is_data_available():
                from .api import calculate_golden_hour
                sunrise = self.current_data.get("sunrise")
                sunset = self.current_data.get("sunset")
                return calculate_golden_hour(sunrise, sunset)
            return {}
        except Exception:
            return {}
    
    def cleanup(self):
        """Clean up resources when the controller is no longer needed."""
        try:
            self.disable_auto_refresh()
            
            if hasattr(self, 'display'):
                self.display.cleanup()
            
            self._data_cache.clear()
            self._cache_timestamps.clear()
            self.current_data.clear()
            
            self.is_fetching = False
            self._consecutive_errors = 0
            
        except Exception:
            pass


def create_sun_moon_controller(app, gui_controller):
    """Helper function to create a sun/moon controller."""
    return SunMoonController(app, gui_controller)


def get_quick_sun_moon_data(city):
    """Quick function to get sun/moon data without a full controller."""
    try:
        return fetch_sun_moon_data(city)
    except Exception as e:
        return {"error": str(e), "city": city}