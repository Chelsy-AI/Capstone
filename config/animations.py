"""
Weather Animation System with Dynamic Background Updates
========================================================

This module creates beautiful animated weather effects that match the current weather conditions.
It's like having a live window showing the weather - when it's raining in real life,
you see animated raindrops on screen!

Features:
- Animated raindrops for rainy weather
- Falling snowflakes for snowy conditions  
- Moving clouds for cloudy skies
- Lightning effects for storms
- Sunshine rays for clear weather
- Dynamic background colors that change with weather
- Smooth 30 FPS animations for fluid motion

The animations automatically update when you search for different cities
or when weather conditions change.
"""

import tkinter as tk  # For creating the graphics canvas
import random        # For random positions and movements
import math          # For calculating sun rays and particle movements


class AnimationParticle:
    """
    Base class for all weather particles (rain, snow, clouds, etc.)
    
    This is like a template that defines common properties and behaviors
    that all weather particles share, such as position, movement, and cleanup.
    """
    
    def __init__(self, x, y, canvas_width, canvas_height):
        """
        Initialize a new weather particle.
        
        Args:
            x, y: Starting position of the particle
            canvas_width, canvas_height: Size of the animation area
        """
        self.x = x                    # Horizontal position
        self.y = y                    # Vertical position
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.id = None               # Canvas object ID for this particle
        self.active = True           # Whether this particle is still active


    def draw(self, canvas):
        """
        Draw particle on the canvas - override in subclasses.
        
        This method draws the particle on the screen.
        Each type of particle looks different when drawn.
        """
        pass

    def cleanup(self, canvas):
        """
        Clean up particle resources when it's no longer needed.
        
        This removes the particle from the canvas to free up memory.
        """
        if self.id:
            try:
                canvas.delete(self.id)  # Remove from canvas
            except:
                pass
            self.id = None

    def is_off_screen(self):
        """
        Check if particle has moved outside the visible area.
        
        Returns:
            bool: True if particle is off-screen and should be recycled
        """
        # Use a buffer zone so particles disappear smoothly
        buffer = 200
        return (self.x < -buffer or self.x > self.canvas_width + buffer or 
                self.y < -buffer or self.y > self.canvas_height + buffer)


class RainDrop(AnimationParticle):
    """
    Animated raindrop particle.
    
    Creates realistic-looking raindrops that fall from the sky with
    slight wind effects and varying speeds for natural movement.
    """
    
    def __init__(self, x, y, canvas_width, canvas_height):
        """Initialize a raindrop with random properties."""
        super().__init__(x, y, canvas_width, canvas_height)
        
        # Randomize raindrop properties for natural variation
        self.length = random.randint(15, 30)      # Length of the raindrop line
        self.speed = random.uniform(8, 20)        # How fast it falls
        self.wind = random.uniform(-3, 3)         # Horizontal wind effect
        self.color = random.choice(["#1E90FF", "#4169E1", "#0000CD"])  # Blue colors

    def update(self):
        """Move the raindrop down and sideways based on wind."""
        if not self.active:
            return
        
        # Move down and sideways
        self.y += self.speed
        self.x += self.wind
        
        # Reset position when raindrop goes off bottom of screen
        if self.y > self.canvas_height + 100:
            self.y = random.randint(-200, -50)    # Start from above screen
            self.x = random.randint(-100, self.canvas_width + 100)

    def draw(self, canvas):
        """Draw the raindrop as a slanted line."""
        if not self.active:
            return
        
        try:
            # Remove old drawing if it exists
            if self.id:
                canvas.delete(self.id)
            
            # Draw raindrop as a line with wind slant
            self.id = canvas.create_line(
                self.x, self.y,
                self.x + self.wind * 2, self.y + self.length,
                fill=self.color, width=2, tags="particle"
            )
        except:
            self.active = False  # Deactivate if drawing fails


class SnowFlake(AnimationParticle):
    """
    Animated snowflake particle.
    
    Creates gently falling snowflakes with realistic drifting motion
    and slight rotation for a natural winter effect.
    """
    
    def __init__(self, x, y, canvas_width, canvas_height):
        """Initialize a snowflake with random properties."""
        super().__init__(x, y, canvas_width, canvas_height)
        
        # Randomize snowflake properties
        self.size = random.randint(3, 10)         # Size of the snowflake
        self.speed = random.uniform(1, 5)         # Falling speed (slower than rain)
        self.drift = random.uniform(-1.5, 1.5)   # Horizontal drifting
        self.phase = random.uniform(0, 2 * math.pi)  # For swaying motion
        self.rotation = 0                         # Current rotation angle

    def update(self):
        """Move the snowflake with gentle swaying motion."""
        if not self.active:
            return
        
        # Move down slowly
        self.y += self.speed
        
        # Add swaying motion using sine wave
        self.phase += 0.02
        self.x += self.drift + math.sin(self.phase) * 1.5
        
        # Rotate slightly for realism
        self.rotation += 0.1
        
        # Reset when snowflake goes off screen
        if self.y > self.canvas_height + 50:
            self.y = random.randint(-100, -20)
            self.x = random.randint(-50, self.canvas_width + 50)

    def draw(self, canvas):
        """Draw the snowflake as a white circle."""
        if not self.active:
            return
        
        try:
            # Remove old drawing
            if self.id:
                canvas.delete(self.id)
            
            # Draw snowflake as a circle with light blue outline
            self.id = canvas.create_oval(
                self.x - self.size, self.y - self.size,
                self.x + self.size, self.y + self.size,
                fill="white", outline="lightblue", width=1, tags="particle"
            )
        except:
            self.active = False


class CloudParticle(AnimationParticle):
    """
    Animated cloud particle.
    
    Creates realistic-looking clouds that slowly drift across the sky.
    Each cloud is made of multiple overlapping circles for a natural appearance.
    """
    
    def __init__(self, x, y, canvas_width, canvas_height):
        """Initialize a cloud with random properties."""
        super().__init__(x, y, canvas_width, canvas_height)
        
        # Randomize cloud properties
        self.width = random.randint(80, 150)      # Width of the cloud
        self.height = random.randint(30, 60)      # Height of the cloud
        self.speed = random.uniform(0.2, 1.0)     # Drifting speed (very slow)
        self.parts = []                           # List of cloud parts (circles)

    def update(self):
        """Move the cloud slowly across the sky."""
        if not self.active:
            return
        
        # Move cloud horizontally
        self.x += self.speed
        
        # Reset cloud position when it goes off the right side
        if self.x > self.canvas_width + self.width + 100:
            self.x = -self.width - 100              # Start from left side
            self.y = random.randint(20, self.canvas_height // 3)  # Random height

    def draw(self, canvas):
        """Draw the cloud as multiple overlapping circles."""
        if not self.active:
            return
        
        try:
            # Clean up old cloud parts
            for part_id in self.parts:
                canvas.delete(part_id)
            self.parts.clear()
            
            # Draw cloud as several overlapping circles
            num_circles = random.randint(3, 5)
            for i in range(num_circles):
                # Calculate position for this circle
                offset_x = i * (self.width // num_circles)
                offset_y = random.randint(-self.height//4, self.height//4)
                size = self.height + random.randint(-10, 10)
                
                # Create one part of the cloud
                part_id = canvas.create_oval(
                    self.x + offset_x, self.y + offset_y,
                    self.x + offset_x + size, self.y + offset_y + size,
                    fill="#E0E0E0", outline="#D0D0D0", width=1, tags="particle"
                )
                self.parts.append(part_id)
            
            # Store the first part as the main ID
            self.id = self.parts[0] if self.parts else None
        except:
            self.active = False

    def cleanup(self, canvas):
        """Override cleanup to handle multiple cloud parts."""
        # Clean up all cloud parts
        for part_id in self.parts:
            try:
                canvas.delete(part_id)
            except:
                pass
        self.parts.clear()
        super().cleanup(canvas)


class WeatherAnimation:
    """
    Main weather animation controller.
    
    This is the "conductor" that manages all the weather particles and effects.
    It creates different types of particles based on weather conditions,
    animates them smoothly, and updates the background colors dynamically.
    """
    
    def __init__(self, canvas):
        """
        Initialize the weather animation system.
        
        Args:
            canvas: The tkinter Canvas where animations will be drawn
        """
        self.canvas = canvas
        self.width = 800           # Default canvas width
        self.height = 600          # Default canvas height
        self.particles = []        # List of all active particles
        self.is_running = False    # Whether animation is currently running
        self.animation_id = None   # ID for scheduled animation frames
        self.current_weather = "clear"  # Current weather type
        self.frame_count = 0       # Count of animation frames for timing
        self.lightning_timer = 0   # Timer for lightning effects
        self.app = None           # Reference to main app (set by controller)
        
        # Performance settings for smooth animation
        self.fps = 30                           # Frames per second
        self.frame_delay = int(1000 / self.fps) # Milliseconds between frames
        self.max_particles = 150                # Maximum number of particles
        
        # Bind to canvas resize events
        try:
            self.canvas.bind("<Configure>", self._on_canvas_resize)
        except:
            pass

    def _on_canvas_resize(self, event):
        """Handle canvas resize events by updating dimensions."""
        if event.widget == self.canvas:
            # Update canvas dimensions (with minimum sizes for safety)
            self.width = max(event.width, 100)
            self.height = max(event.height, 100)
            
            # Update all particles with new boundaries
            for particle in self.particles:
                if hasattr(particle, 'canvas_width'):
                    particle.canvas_width = self.width
                    particle.canvas_height = self.height

    def update_size(self, width, height):
        """
        Update animation size manually.
        
        Args:
            width, height: New dimensions for the animation area
        """
        self.width = max(width, 100)
        self.height = max(height, 100)
        
        # Update all existing particles
        for particle in self.particles:
            if hasattr(particle, 'canvas_width'):
                particle.canvas_width = self.width
                particle.canvas_height = self.height

    def start_animation(self, weather_type="clear"):
        """
        Start weather animation for a specific weather type.
        
        Args:
            weather_type (str): Type of weather to animate ("rain", "snow", etc.)
        """
        self.current_weather = weather_type
        
        # Initialize particles if not already running
        if not self.is_running:
            self.is_running = True
            self._initialize_particles()
            self._start_animation_loop()
        else:
            # Just change weather type if already running
            self.set_weather_type(weather_type)

    def stop_animation(self):
        """Stop the weather animation and clean up resources."""
        self.is_running = False
        
        # Cancel the animation loop
        if self.animation_id:
            try:
                self.canvas.after_cancel(self.animation_id)
            except:
                pass
            self.animation_id = None
        
        # Clean up all particles
        self._cleanup_particles()

    def set_weather_type(self, weather_type):
        """
        Change weather type and reinitialize particles.
        
        Args:
            weather_type (str): New weather type to display
        """
        if weather_type != self.current_weather:
            self.current_weather = weather_type
            self._cleanup_particles()
            self._initialize_particles()

    def _start_animation_loop(self):
        """Start the main animation loop."""
        if self.is_running:
            self._animate_frame()

    def _animate_frame(self):
        """
        Animate a single frame.
        
        This is called repeatedly (30 times per second) to create smooth animation.
        Each frame updates particle positions, draws them, and handles special effects.
        """
        if not self.is_running:
            return

        try:
            self.frame_count += 1
            
            # Clear previous frame
            self.canvas.delete("particle")
            self.canvas.delete("background")
            
            # Draw background and update colors
            self._draw_background()
            
            # Update and draw all particles
            active_particles = 0
            particles_to_remove = []
            
            for i, particle in enumerate(self.particles):
                if not hasattr(particle, 'active') or particle.active:
                    try:
                        particle.update()  # Move the particle
                        particle.draw(self.canvas)  # Draw the particle
                        active_particles += 1
                        
                        # Mark particles that have moved off-screen for removal
                        if particle.is_off_screen():
                            particles_to_remove.append(i)
                    except Exception as e:
                        # If a particle causes errors, remove it
                        particles_to_remove.append(i)
                else:
                    particles_to_remove.append(i)
            
            # Remove inactive particles (in reverse order to maintain indices)
            for i in reversed(particles_to_remove):
                if i < len(self.particles):
                    try:
                        self.particles[i].cleanup(self.canvas)
                    except:
                        pass
                    del self.particles[i]
            
            # Add new particles if needed to maintain particle count
            self._maintain_particle_count()
            
            # Handle special weather effects
            if self.current_weather == "storm":
                self._draw_lightning()
            
            # Schedule the next animation frame
            self.animation_id = self.canvas.after(self.frame_delay, self._animate_frame)
            
        except Exception as e:
            # If something goes wrong, try to continue the animation
            if self.is_running:
                self.animation_id = self.canvas.after(self.frame_delay, self._animate_frame)

    def _initialize_particles(self):
        """Initialize particles based on current weather type."""
        # Clean up any existing particles first
        self._cleanup_particles()
        self.lightning_timer = 0
        
        # Map weather types to particle creation functions
        weather_handlers = {
            "rain": self._create_rain_particles,
            "snow": self._create_snow_particles,
            "storm": self._create_storm_particles,
            "cloudy": self._create_cloud_particles,
            "mist": self._create_mist_particles,
            "sunny": self._create_clear_particles,
            "clear": self._create_clear_particles
        }
        
        # Get the appropriate handler for current weather
        handler = weather_handlers.get(self.current_weather, self._create_clear_particles)
        handler()

    def _create_rain_particles(self):
        """Create raindrops for rainy weather."""
        # Create a reasonable number of raindrops based on canvas size
        count = min(100, max(30, self.width // 10))
        for _ in range(count):
            # Start raindrops above and around the visible area
            x = random.randint(-100, self.width + 100)
            y = random.randint(-200, self.height)
            self.particles.append(RainDrop(x, y, self.width, self.height))

    def _create_snow_particles(self):
        """Create snowflakes for snowy weather."""
        count = min(80, max(20, self.width // 15))
        for _ in range(count):
            x = random.randint(-50, self.width + 50)
            y = random.randint(-100, self.height)
            self.particles.append(SnowFlake(x, y, self.width, self.height))

    def _create_storm_particles(self):
        """Create particles for stormy weather (rain + dark clouds)."""
        # Add heavy rain
        self._create_rain_particles()
        # Add storm clouds
        for _ in range(3):
            x = random.randint(-150, self.width)
            y = random.randint(20, self.height // 4)
            self.particles.append(CloudParticle(x, y, self.width, self.height))

    def _create_cloud_particles(self):
        """Create clouds for cloudy weather."""
        count = min(6, max(2, self.width // 200))
        for _ in range(count):
            x = random.randint(-200, self.width)
            y = random.randint(50, self.height // 2)
            self.particles.append(CloudParticle(x, y, self.width, self.height))

    def _create_mist_particles(self):
        """Create mist effect with slow-moving clouds."""
        count = min(15, max(5, self.width // 80))
        for _ in range(count):
            x = random.randint(-150, self.width)
            y = random.randint(self.height // 2, self.height)
            particle = CloudParticle(x, y, self.width, self.height)
            particle.speed = random.uniform(0.1, 0.5)  # Slower movement for mist
            self.particles.append(particle)

    def _create_clear_particles(self):
        """Create minimal particles for clear weather."""
        # Just a few gentle clouds for atmosphere
        for _ in range(2):
            x = random.randint(-200, self.width)
            y = random.randint(50, self.height // 3)
            particle = CloudParticle(x, y, self.width, self.height)
            particle.speed = random.uniform(0.2, 0.6)
            self.particles.append(particle)

    def _maintain_particle_count(self):
        """Maintain appropriate number of particles for current weather."""
        # Define target particle counts for each weather type
        target_counts = {
            "rain": min(100, max(30, self.width // 10)),
            "snow": min(80, max(20, self.width // 15)),
            "storm": min(120, max(40, self.width // 8)),
            "cloudy": min(6, max(2, self.width // 200)),
            "mist": min(15, max(5, self.width // 80)),
            "sunny": 2,
            "clear": 2
        }
        
        target = target_counts.get(self.current_weather, 10)
        current = len(self.particles)
        
        # Add particles if we're below the target (but don't add too many at once)
        if current < target and current < self.max_particles:
            needed = min(target - current, 5)  # Add maximum 5 per frame for smooth performance
            for _ in range(needed):
                self._add_single_particle()

    def _add_single_particle(self):
        """Add a single particle of the current weather type."""
        if self.current_weather == "rain":
            x = random.randint(-100, self.width + 100)
            y = random.randint(-200, -50)
            self.particles.append(RainDrop(x, y, self.width, self.height))
        elif self.current_weather == "snow":
            x = random.randint(-50, self.width + 50)
            y = random.randint(-100, -20)
            self.particles.append(SnowFlake(x, y, self.width, self.height))
        elif self.current_weather in ["cloudy", "mist", "clear", "sunny"]:
            x = random.randint(-200, self.width)
            y = random.randint(50, self.height // 2)
            self.particles.append(CloudParticle(x, y, self.width, self.height))

    def _draw_background(self):
        """
        Draw weather-appropriate background and notify GUI of color changes.
        
        This function sets the background color based on weather conditions
        and tells the main app to update all label backgrounds to match.
        """
        # Define background colors for different weather types
        colors = {
            "rain": "#4A6741",      # Dark green-grey for rainy atmosphere
            "snow": "#F0F8FF",      # Alice blue for snowy conditions
            "storm": "#2C3E50",     # Dark blue-grey for stormy weather
            "cloudy": "#B0C4DE",    # Light steel blue for cloudy skies
            "mist": "#D3D3D3",      # Light grey for misty conditions
            "sunny": "#87CEEB",     # Sky blue for sunny weather
            "clear": "#87CEEB"      # Sky blue for clear conditions
        }
        
        bg_color = colors.get(self.current_weather, "#87CEEB")
        
        try:
            # Draw background rectangle to fill the entire canvas
            self.canvas.create_rectangle(
                0, 0, self.width, self.height,
                fill=bg_color, outline="", tags="background"
            )
            
            # Update canvas background color
            self.canvas.configure(bg=bg_color)
            
            # Notify the main app to update all label backgrounds
            # This prevents ugly blue boxes around text labels
            if self.app and hasattr(self.app, 'update_all_label_backgrounds'):
                self.app.update_all_label_backgrounds(bg_color)
            
            # Draw special elements for certain weather types
            if self.current_weather in ["sunny", "clear"]:
                self._draw_sun()
                
        except Exception as e:
            # If background drawing fails, just continue - not critical
            pass

    def _draw_sun(self):
        """Draw animated sun with rays for sunny weather."""
        try:
            # Position the sun in the upper right area
            sun_x = self.width - 120
            sun_y = 80
            sun_radius = 40
            
            # Draw sun rays extending outward
            for i in range(12):
                angle = i * (2 * math.pi / 12)  # Divide circle into 12 rays
                
                # Calculate ray start and end positions
                start_x = sun_x + math.cos(angle) * (sun_radius + 15)
                start_y = sun_y + math.sin(angle) * (sun_radius + 15)
                end_x = sun_x + math.cos(angle) * (sun_radius + 35)
                end_y = sun_y + math.sin(angle) * (sun_radius + 35)
                
                # Draw each ray as a line
                self.canvas.create_line(
                    start_x, start_y, end_x, end_y,
                    fill="#FFD700", width=3, tags="background"
                )
            
            # Draw the main sun circle
            self.canvas.create_oval(
                sun_x - sun_radius, sun_y - sun_radius,
                sun_x + sun_radius, sun_y + sun_radius,
                fill="#FFD700", outline="#FFA500", width=2, tags="background"
            )
        except Exception as e:
            # If sun drawing fails, just continue
            pass

    def _draw_lightning(self):
        """Draw lightning effects for storm weather."""
        self.lightning_timer += 1
        
        # Create random lightning every 2-4 seconds (at 30 FPS, this is 60-120 frames)
        if self.lightning_timer > 60 and random.random() < 0.03:  # 3% chance per frame
            try:
                self.lightning_timer = 0  # Reset timer
                
                # Create lightning bolt starting from random position in upper area
                start_x = random.randint(self.width // 4, 3 * self.width // 4)
                start_y = random.randint(0, self.height // 4)
                
                # Create jagged lightning path
                points = [(start_x, start_y)]
                current_x, current_y = start_x, start_y
                
                # Create 3-6 segments for the lightning bolt
                for _ in range(random.randint(3, 6)):
                    # Add random jagged movement
                    current_x += random.randint(-40, 40)
                    current_y += random.randint(40, 80)  # Always move downward
                    points.append((current_x, current_y))
                    
                    # Stop if lightning reaches bottom of screen
                    if current_y >= self.height:
                        break
                
                # Draw lightning as connected line segments
                for i in range(len(points) - 1):
                    self.canvas.create_line(
                        points[i][0], points[i][1],
                        points[i+1][0], points[i+1][1],
                        fill="#FFFF00", width=random.randint(2, 5),  # Vary thickness
                        tags="background"
                    )
                
            except Exception as e:
                # If lightning drawing fails, just continue
                pass

    def _cleanup_particles(self):
        """Clean up all particles and canvas elements."""
        try:
            # Clean up individual particles
            for particle in self.particles:
                if hasattr(particle, 'cleanup'):
                    particle.cleanup(self.canvas)
            
            # Clear particle list
            self.particles.clear()
            
            # Clear canvas elements
            self.canvas.delete("particle")
            self.canvas.delete("background")
            
        except Exception as e:
            # If cleanup fails, just continue - not critical
            pass

    # Public interface methods for external use
    
    def get_particle_count(self):
        """
        Get the current number of active particles.
        
        Returns:
            int: Number of particles currently being animated
        """
        return len(self.particles)

    def is_animation_running(self):
        """
        Check if animation is currently running.
        
        Returns:
            bool: True if animation is active, False otherwise
        """
        return self.is_running

    def get_current_weather(self):
        """
        Get the current weather type being animated.
        
        Returns:
            str: Current weather type ("rain", "snow", "clear", etc.)
        """
        return self.current_weather