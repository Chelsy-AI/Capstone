"""
Animation Controller Module
===========================

This module acts as the "conductor" for weather animations. It's like having
a movie director who decides what weather effects to show based on current conditions.

Key responsibilities:
- Map weather descriptions to appropriate animations (rain → raindrops, snow → snowflakes)
- Start and stop animations smoothly
- Handle animation settings and performance
- Coordinate with the main app for background color changes
- Provide animation status information

Think of this as the "animation brain" that decides what visual effects
should be playing and manages them throughout the app's lifetime.

Weather Animation Mapping:
- Rain/Drizzle → Animated raindrops falling
- Snow/Sleet → Gentle snowflakes drifting down  
- Storms → Heavy rain + lightning effects
- Clouds → Slow-moving cloud formations
- Clear/Sunny → Minimal clouds + sunshine rays
- Mist/Fog → Low-hanging cloud effects
"""

import traceback  # For detailed error reporting when animations fail
from config.animations import WeatherAnimation


class AnimationController:
    """
    Animation Controller with Dynamic Background Support
    
    This class manages the weather animation system and acts as a bridge
    between weather data and visual effects. It translates weather conditions
    into appropriate animations and manages their lifecycle.
    """
    
    def __init__(self, app, gui_controller):
        """
        Initialize the animation controller.
        
        Args:
            app: Main weather application instance
            gui_controller: GUI controller that manages the interface
        """
        self.app = app              # Reference to main app
        self.gui = gui_controller   # Reference to GUI controller
        self.smart_bg = None        # The animation system (will be created later)
        
        # Weather condition mapping - this dictionary tells us which animations
        # to show for different weather descriptions from the API
        self.weather_mapping = {
            # Keywords that indicate rain
            'rain_keywords': ["rain", "drizzle", "shower"],
            
            # Keywords that indicate snow
            'snow_keywords': ["snow", "blizzard", "sleet"],
            
            # Keywords that indicate storms
            'storm_keywords': ["thunder", "storm", "lightning"],
            
            # Keywords that indicate clouds
            'cloud_keywords': ["cloud", "overcast", "broken"],
            
            # Keywords that indicate clear weather
            'clear_keywords': ["clear", "sun", "sunny"],
            
            # Keywords that indicate mist or fog
            'mist_keywords': ["mist", "fog", "haze"]
        }

    def setup_animation(self, canvas):
        """
        Initialize the animation system with app reference.
        
        This creates the main animation system and connects it to the canvas
        where weather effects will be displayed. It's called once during app startup.
        
        Args:
            canvas: The tkinter Canvas where animations will be drawn
        """
        try:
            # Create the main weather animation system
            self.smart_bg = WeatherAnimation(canvas)
            
            # IMPORTANT: Give the animation system access to the main app
            # This allows animations to update label backgrounds automatically
            self.smart_bg.app = self.app
            
            # Start with a default animation after a short delay
            # The delay ensures the window is fully loaded before starting animations
            self.app.after(500, lambda: self.smart_bg.start_animation("clear"))
            
        except Exception as e:
            # If animation setup fails, just continue without animations
            # The app will still work, just without pretty weather effects
            self.smart_bg = None

    def update_background_animation(self, weather_data):
        """
        Update background animation based on current weather data.
        
        This is the main function that changes animations when weather conditions
        change. It looks at the weather description and starts the appropriate
        animation (rain, snow, sunshine, etc.).
        
        Args:
            weather_data (dict): Weather information containing description and conditions
        """
        # Don't try to update if animation system isn't initialized
        if not self.smart_bg:
            return
            
        try:
            # Get the weather description from the data
            description = weather_data.get("description", "").lower()
            
            # Determine what animation type to show based on the description
            animation_type = self._map_weather_to_animation(description)
            
            # Update the animation
            if self.smart_bg.is_animation_running():
                # If animations are already running, just change the type
                self.smart_bg.set_weather_type(animation_type)
            else:
                # If animations aren't running, start them with the new type
                self.smart_bg.start_animation(animation_type)
                
            # Optional: Get debug information about particle count
            particles = self.smart_bg.get_particle_count()
            
        except Exception as e:
            # If animation update fails, print error details for debugging
            # but don't crash the app
            traceback.print_exc()

    def _map_weather_to_animation(self, description):
        """
        Map a weather description to the appropriate animation type.
        
        This is the "translation" function that looks at weather descriptions
        like "light rain" or "partly cloudy" and decides what animation to show.
        
        Args:
            description (str): Weather description from API (lowercase)
            
        Returns:
            str: Animation type ("rain", "snow", "storm", etc.)
            
        Example:
            animation = self._map_weather_to_animation("heavy rain")
            # Returns: "rain"
        """
        description_lower = description.lower()
        
        # Check each weather category to find the best match
        # We check in order of priority (storms before rain, etc.)
        
        # Check for rain conditions
        if any(word in description_lower for word in self.weather_mapping['rain_keywords']):
            return "rain"
        
        # Check for snow conditions
        elif any(word in description_lower for word in self.weather_mapping['snow_keywords']):
            return "snow"
        
        # Check for storm conditions
        elif any(word in description_lower for word in self.weather_mapping['storm_keywords']):
            return "storm"
        
        # Check for cloudy conditions
        elif any(word in description_lower for word in self.weather_mapping['cloud_keywords']):
            return "cloudy"
        
        # Check for clear/sunny conditions
        elif any(word in description_lower for word in self.weather_mapping['clear_keywords']):
            return "sunny"
        
        # Check for misty/foggy conditions
        elif any(word in description_lower for word in self.weather_mapping['mist_keywords']):
            return "mist"
        
        # Default fallback if no keywords match
        else:
            return "clear"

    def start_animation(self, weather_type="clear"):
        """
        Start animation with a specific weather type.
        
        This manually starts animations with a specified weather condition.
        Useful for testing or when you want to force a specific animation.
        
        Args:
            weather_type (str): Type of animation to start ("rain", "snow", etc.)
        """
        if self.smart_bg:
            try:
                self.smart_bg.start_animation(weather_type)
            except Exception as e:
                # If starting animation fails, just continue without it
                pass

    def stop_animation(self):
        """
        Stop all weather animations.
        
        This completely stops the animation system, useful when closing
        the app or switching to a mode where animations aren't needed.
        """
        if self.smart_bg:
            try:
                self.smart_bg.stop_animation()
            except Exception as e:
                # If stopping animation fails, just continue
                pass

    def change_weather_type(self, weather_type):
        """
        Change the current weather animation type.
        
        This switches from one animation to another without stopping
        and restarting the entire animation system.
        
        Args:
            weather_type (str): New animation type to display
        """
        if self.smart_bg:
            try:
                self.smart_bg.set_weather_type(weather_type)
            except Exception as e:
                # If changing animation fails, just continue
                pass

    def is_animation_running(self):
        """
        Check if animations are currently active.
        
        Returns:
            bool: True if animations are running, False otherwise
            
        Example:
            if controller.is_animation_running():
                print("Animations are active!")
        """
        if self.smart_bg:
            try:
                return self.smart_bg.is_animation_running()
            except Exception:
                return False
        return False

    def get_animation_info(self):
        """
        Get detailed information about the current animation state.
        
        This provides comprehensive information about what animations are
        running, how many particles are active, and any errors.
        
        Returns:
            dict: Animation status information
            
        Example:
            info = controller.get_animation_info()
            print(f"Running: {info['running']}")
            print(f"Weather: {info['weather_type']}")
            print(f"Particles: {info['particle_count']}")
        """
        # Return basic info if animation system isn't initialized
        if not self.smart_bg:
            return {
                'running': False,
                'weather_type': None,
                'particle_count': 0,
                'error': 'Animation system not initialized'
            }
        
        try:
            # Get comprehensive status from the animation system
            return {
                'running': self.smart_bg.is_animation_running(),
                'weather_type': self.smart_bg.get_current_weather(),
                'particle_count': self.smart_bg.get_particle_count(),
                'error': None
            }
        except Exception as e:
            # If getting info fails, return error state
            return {
                'running': False,
                'weather_type': None,
                'particle_count': 0,
                'error': str(e)
            }

    def restart_animation(self):
        """
        Restart the animation system.
        
        This stops and restarts animations, useful if something goes wrong
        or if you want to refresh the animation system.
        """
        try:
            if self.smart_bg:
                # Remember current weather type
                current_weather = self.smart_bg.get_current_weather()
                
                # Stop and restart with the same weather type
                self.stop_animation()
                self.start_animation(current_weather)
        except Exception as e:
            # If restart fails, just continue
            pass

    def cleanup_animation(self):
        """
        Clean up animation resources when closing the app.
        
        This properly shuts down the animation system and frees up
        memory when the app is closing.
        """
        if self.smart_bg:
            try:
                self.smart_bg.stop_animation()
            except Exception as e:
                # If cleanup fails, just continue - we're closing anyway
                pass
        self.smart_bg = None

    def update_animation_size(self, width, height):
        """
        Update animation canvas size when window is resized.
        
        This ensures animations look good when the user resizes the window
        by updating the animation boundaries.
        
        Args:
            width (int): New canvas width
            height (int): New canvas height
        """
        if self.smart_bg:
            try:
                self.smart_bg.update_size(width, height)
            except Exception as e:
                # If size update fails, just continue
                pass

    def get_available_weather_types(self):
        """
        Get a list of all available weather animation types.
        
        This is useful for testing, debugging, or creating animation
        selection interfaces.
        
        Returns:
            list: Available animation types
            
        Example:
            types = controller.get_available_weather_types()
            # Returns: ["clear", "sunny", "rain", "snow", "storm", "cloudy", "mist"]
        """
        return ["clear", "sunny", "rain", "snow", "storm", "cloudy", "mist"]

    def preview_weather_type(self, weather_type, duration=3000):
        """
        Preview a weather animation for a specified time.
        
        This temporarily changes to a different animation and then
        switches back to the original. Useful for testing or demonstrations.
        
        Args:
            weather_type (str): Animation type to preview
            duration (int): How long to show preview in milliseconds (default 3 seconds)
            
        Example:
            controller.preview_weather_type("storm", 5000)  # Show storm for 5 seconds
        """
        # Only preview if we have a valid animation system and weather type
        if self.smart_bg and weather_type in self.get_available_weather_types():
            try:
                # Remember the current animation type
                original_type = self.smart_bg.get_current_weather()
                
                # Switch to preview animation
                self.smart_bg.set_weather_type(weather_type)
                
                # Schedule return to original animation after the specified duration
                self.app.after(duration, lambda: self.smart_bg.set_weather_type(original_type))
                
            except Exception as e:
                # If preview fails, just continue
                pass

    def get_weather_mapping_info(self):
        """
        Get information about how weather descriptions map to animations.
        
        This returns the keyword mapping used to decide which animations
        to show for different weather conditions.
        
        Returns:
            dict: Weather keyword mapping information
        """
        return {
            "description": "Keyword mapping for weather animations",
            "mappings": self.weather_mapping,
            "total_keywords": sum(len(keywords) for keywords in self.weather_mapping.values()),
            "animation_types": self.get_available_weather_types()
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TESTING AND EXAMPLE USAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    """
    This section runs when you execute this file directly.
    It's useful for testing the animation controller functionality.
    """
    
    print("Testing Animation Controller")
    print("=" * 30)
    
    # Create a mock app and GUI for testing
    class MockApp:
        def after(self, delay, func):
            print(f"Scheduled function to run after {delay}ms")
    
    class MockGUI:
        pass
    
    # Test animation controller creation
    app = MockApp()
    gui = MockGUI()
    controller = AnimationController(app, gui)
    
    print("\n🎬 Testing animation controller features:")
    
    # Test available weather types
    weather_types = controller.get_available_weather_types()
    print(f"  Available weather types: {', '.join(weather_types)}")
    
    # Test weather description mapping
    test_descriptions = [
        "light rain",
        "heavy snow",
        "thunderstorm",
        "partly cloudy",
        "clear sky",
        "morning mist"
    ]
    
    print(f"\n🗺️  Testing weather description mapping:")
    for description in test_descriptions:
        animation_type = controller._map_weather_to_animation(description)
        print(f"  '{description}' → {animation_type}")
    
    # Test animation info (without actual animation system)
    print(f"\n📊 Testing animation info:")
    info = controller.get_animation_info()
    print(f"  Running: {info['running']}")
    print(f"  Error: {info['error']}")
    
    # Test weather mapping info
    print(f"\n🔗 Testing weather mapping info:")
    mapping_info = controller.get_weather_mapping_info()
    print(f"  Total keywords: {mapping_info['total_keywords']}")
    print(f"  Animation types: {len(mapping_info['animation_types'])}")
    
    print(f"\n✅ Animation controller testing completed!")
    print(f"\nNote: Full animation testing requires a tkinter Canvas.")
    print(f"This controller manages weather animations based on API descriptions.")