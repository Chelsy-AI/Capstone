import traceback
from config.animations import WeatherAnimation


class AnimationController:
    """
    Animation Controller
    
    Manages background weather animations including initialization,
    weather type mapping, and animation lifecycle management.
    """
    
    def __init__(self, app, gui_controller):
        self.app = app
        self.gui = gui_controller
        self.smart_bg = None
        
        # Weather condition mapping
        self.weather_mapping = {
            'rain_keywords': ["rain", "drizzle", "shower"],
            'snow_keywords': ["snow", "blizzard", "sleet"],
            'storm_keywords': ["thunder", "storm", "lightning"],
            'cloud_keywords': ["cloud", "overcast", "broken"],
            'clear_keywords': ["clear", "sun", "sunny"],
            'mist_keywords': ["mist", "fog", "haze"]
        }

    def setup_animation(self, canvas):
        """Initialize the animation system"""
        try:
            print("[Animation] Setting up animation system...")
            self.smart_bg = WeatherAnimation(canvas)
            
            # Start with default animation after a short delay
            self.app.after(500, lambda: self.smart_bg.start_animation("clear"))
            print("🎬 Animation system ready")
            
        except Exception as e:
            print(f"❌ Animation setup failed: {e}")
            self.smart_bg = None

    def update_background_animation(self, weather_data):
        """Update background animation based on weather data"""
        if not self.smart_bg:
            print("❌ No animation system available")
            return
            
        try:
            description = weather_data.get("description", "").lower()
            print(f"🌤️ Weather description: {description}")
            
            # Map description to animation type
            animation_type = self._map_weather_to_animation(description)
            print(f"🎬 Animation type: {animation_type}")
            
            # Update animation
            if self.smart_bg.is_animation_running():
                self.smart_bg.set_weather_type(animation_type)
            else:
                self.smart_bg.start_animation(animation_type)
                
            # Debug information
            particles = self.smart_bg.get_particle_count()
            print(f"🎬 Active particles: {particles}")
            
        except Exception as e:
            print(f"❌ Animation update error: {e}")
            traceback.print_exc()

    def _map_weather_to_animation(self, description):
        """Map weather description to animation type"""
        description_lower = description.lower()
        
        # Check each weather type
        if any(word in description_lower for word in self.weather_mapping['rain_keywords']):
            return "rain"
        elif any(word in description_lower for word in self.weather_mapping['snow_keywords']):
            return "snow"
        elif any(word in description_lower for word in self.weather_mapping['storm_keywords']):
            return "storm"
        elif any(word in description_lower for word in self.weather_mapping['cloud_keywords']):
            return "cloudy"
        elif any(word in description_lower for word in self.weather_mapping['clear_keywords']):
            return "sunny"
        elif any(word in description_lower for word in self.weather_mapping['mist_keywords']):
            return "mist"
        else:
            return "clear"  # Default fallback

    def start_animation(self, weather_type="clear"):
        """Start animation with specified weather type"""
        if self.smart_bg:
            try:
                self.smart_bg.start_animation(weather_type)
                print(f"🎬 Animation started: {weather_type}")
            except Exception as e:
                print(f"❌ Animation start error: {e}")

    def stop_animation(self):
        """Stop the animation"""
        if self.smart_bg:
            try:
                self.smart_bg.stop_animation()
                print("🎬 Animation stopped")
            except Exception as e:
                print(f"❌ Animation stop error: {e}")

    def change_weather_type(self, weather_type):
        """Change the current weather animation type"""
        if self.smart_bg:
            try:
                self.smart_bg.set_weather_type(weather_type)
                print(f"🎬 Weather type changed to: {weather_type}")
            except Exception as e:
                print(f"❌ Weather type change error: {e}")

    def is_animation_running(self):
        """Check if animation is currently running"""
        if self.smart_bg:
            try:
                return self.smart_bg.is_animation_running()
            except Exception:
                return False
        return False

    def get_animation_info(self):
        """Get information about current animation state"""
        if not self.smart_bg:
            return {
                'running': False,
                'weather_type': None,
                'particle_count': 0,
                'error': 'Animation system not initialized'
            }
        
        try:
            return {
                'running': self.smart_bg.is_animation_running(),
                'weather_type': self.smart_bg.get_current_weather(),
                'particle_count': self.smart_bg.get_particle_count(),
                'error': None
            }
        except Exception as e:
            return {
                'running': False,
                'weather_type': None,
                'particle_count': 0,
                'error': str(e)
            }

    def restart_animation(self):
        """Restart the animation system"""
        try:
            if self.smart_bg:
                current_weather = self.smart_bg.get_current_weather()
                self.stop_animation()
                self.start_animation(current_weather)
                print("🎬 Animation restarted")
        except Exception as e:
            print(f"❌ Animation restart error: {e}")

    def cleanup_animation(self):
        """Clean up animation resources"""
        if self.smart_bg:
            try:
                self.smart_bg.stop_animation()
                print("🎬 Animation cleanup completed")
            except Exception as e:
                print(f"❌ Animation cleanup error: {e}")
        self.smart_bg = None

    def update_animation_size(self, width, height):
        """Update animation canvas size"""
        if self.smart_bg:
            try:
                self.smart_bg.update_size(width, height)
                print(f"🎬 Animation size updated: {width}x{height}")
            except Exception as e:
                print(f"❌ Animation size update error: {e}")

    def set_animation_quality(self, quality_level):
        """Set animation quality level (if supported)"""
        if self.smart_bg:
            try:
                # This would need to be implemented in the WeatherAnimation class
                # For now, just log the request
                print(f"🎬 Animation quality setting requested: {quality_level}")
            except Exception as e:
                print(f"❌ Animation quality setting error: {e}")

    def get_available_weather_types(self):
        """Get list of available weather animation types"""
        return ["clear", "sunny", "rain", "snow", "storm", "cloudy", "mist"]

    def preview_weather_type(self, weather_type, duration=3000):
        """Preview a weather type for a specified duration"""
        if self.smart_bg and weather_type in self.get_available_weather_types():
            try:
                original_type = self.smart_bg.get_current_weather()
                self.smart_bg.set_weather_type(weather_type)
                print(f"🎬 Previewing weather type: {weather_type}")
                
                # Schedule return to original type
                self.app.after(duration, lambda: self.smart_bg.set_weather_type(original_type))
                
            except Exception as e:
                print(f"❌ Weather preview error: {e}")
                