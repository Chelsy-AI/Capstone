#!/usr/bin/env python3
"""
Fixed Weather Animation System
This version addresses all previous issues and provides working animations
"""

import tkinter as tk
import random
import math
import time


class AnimationParticle:
    """Improved base class for weather particles"""
    def __init__(self, x, y, canvas_width, canvas_height):
        self.x = x
        self.y = y
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.id = None
        self.active = True

    def update(self):
        """Update particle position - override in subclasses"""
        pass

    def draw(self, canvas):
        """Draw particle - override in subclasses"""
        pass

    def cleanup(self, canvas):
        """Clean up particle resources"""
        if self.id:
            try:
                canvas.delete(self.id)
            except:
                pass
            self.id = None

    def is_off_screen(self):
        """Check if particle is off screen with larger buffer"""
        buffer = 200
        return (self.x < -buffer or self.x > self.canvas_width + buffer or 
                self.y < -buffer or self.y > self.canvas_height + buffer)


class RainDrop(AnimationParticle):
    """Enhanced rain drop particle"""
    def __init__(self, x, y, canvas_width, canvas_height):
        super().__init__(x, y, canvas_width, canvas_height)
        self.length = random.randint(15, 30)
        self.speed = random.uniform(8, 20)
        self.wind = random.uniform(-3, 3)
        self.color = random.choice(["#1E90FF", "#4169E1", "#0000CD"])

    def update(self):
        if not self.active:
            return
        
        self.y += self.speed
        self.x += self.wind
        
        # Reset position if off screen
        if self.y > self.canvas_height + 100:
            self.y = random.randint(-200, -50)
            self.x = random.randint(-100, self.canvas_width + 100)

    def draw(self, canvas):
        if not self.active:
            return
        
        try:
            if self.id:
                canvas.delete(self.id)
            
            self.id = canvas.create_line(
                self.x, self.y,
                self.x + self.wind * 2, self.y + self.length,
                fill=self.color, width=2, tags="particle"
            )
        except:
            self.active = False


class SnowFlake(AnimationParticle):
    """Enhanced snow flake particle"""
    def __init__(self, x, y, canvas_width, canvas_height):
        super().__init__(x, y, canvas_width, canvas_height)
        self.size = random.randint(3, 10)
        self.speed = random.uniform(1, 5)
        self.drift = random.uniform(-1.5, 1.5)
        self.phase = random.uniform(0, 2 * math.pi)
        self.rotation = 0

    def update(self):
        if not self.active:
            return
        
        self.y += self.speed
        self.phase += 0.02
        self.x += self.drift + math.sin(self.phase) * 1.5
        self.rotation += 0.1
        
        # Reset if off screen
        if self.y > self.canvas_height + 50:
            self.y = random.randint(-100, -20)
            self.x = random.randint(-50, self.canvas_width + 50)

    def draw(self, canvas):
        if not self.active:
            return
        
        try:
            if self.id:
                canvas.delete(self.id)
            
            self.id = canvas.create_oval(
                self.x - self.size, self.y - self.size,
                self.x + self.size, self.y + self.size,
                fill="white", outline="lightblue", width=1, tags="particle"
            )
        except:
            self.active = False


class CloudParticle(AnimationParticle):
    """Enhanced cloud particle"""
    def __init__(self, x, y, canvas_width, canvas_height):
        super().__init__(x, y, canvas_width, canvas_height)
        self.width = random.randint(80, 150)
        self.height = random.randint(30, 60)
        self.speed = random.uniform(0.2, 1.0)
        self.parts = []

    def update(self):
        if not self.active:
            return
        
        self.x += self.speed
        
        # Reset if completely off screen
        if self.x > self.canvas_width + self.width + 100:
            self.x = -self.width - 100
            self.y = random.randint(20, self.canvas_height // 3)

    def draw(self, canvas):
        if not self.active:
            return
        
        try:
            # Clean up old parts
            for part_id in self.parts:
                canvas.delete(part_id)
            self.parts.clear()
            
            # Draw cloud as overlapping circles
            num_circles = random.randint(3, 5)
            for i in range(num_circles):
                offset_x = i * (self.width // num_circles)
                offset_y = random.randint(-self.height//4, self.height//4)
                size = self.height + random.randint(-10, 10)
                
                part_id = canvas.create_oval(
                    self.x + offset_x, self.y + offset_y,
                    self.x + offset_x + size, self.y + offset_y + size,
                    fill="#E0E0E0", outline="#D0D0D0", width=1, tags="particle"
                )
                self.parts.append(part_id)
            
            self.id = self.parts[0] if self.parts else None
        except:
            self.active = False

    def cleanup(self, canvas):
        """Override cleanup to handle multiple parts"""
        for part_id in self.parts:
            try:
                canvas.delete(part_id)
            except:
                pass
        self.parts.clear()
        super().cleanup(canvas)


class WeatherAnimation:
    """Fixed weather animation controller"""
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = 800
        self.height = 600
        self.particles = []
        self.is_running = False
        self.animation_id = None
        self.current_weather = "clear"
        self.frame_count = 0
        self.lightning_timer = 0
        
        # Performance settings
        self.fps = 30
        self.frame_delay = int(1000 / self.fps)
        self.max_particles = 150
        
        print(f"[WeatherAnimation] Initialized animation system")
        
        # Bind events
        try:
            self.canvas.bind("<Configure>", self._on_canvas_resize)
        except:
            pass

    def _on_canvas_resize(self, event):
        """Handle canvas resize"""
        if event.widget == self.canvas:
            self.width = max(event.width, 100)
            self.height = max(event.height, 100)
            print(f"[WeatherAnimation] Canvas resized to: {self.width}x{self.height}")
            
            # Update all particles with new boundaries
            for particle in self.particles:
                if hasattr(particle, 'canvas_width'):
                    particle.canvas_width = self.width
                    particle.canvas_height = self.height

    def update_size(self, width, height):
        """Update animation size"""
        self.width = max(width, 100)
        self.height = max(height, 100)
        print(f"[WeatherAnimation] Size updated to: {self.width}x{self.height}")
        
        # Update particles
        for particle in self.particles:
            if hasattr(particle, 'canvas_width'):
                particle.canvas_width = self.width
                particle.canvas_height = self.height

    def start_animation(self, weather_type="clear"):
        """Start weather animation"""
        print(f"[WeatherAnimation] Starting animation: {weather_type}")
        
        self.current_weather = weather_type
        
        # Initialize particles if not running
        if not self.is_running:
            self.is_running = True
            self._initialize_particles()
            self._start_animation_loop()
            print(f"[WeatherAnimation] Animation started with {len(self.particles)} particles")
        else:
            # Just change weather type if already running
            self.set_weather_type(weather_type)

    def stop_animation(self):
        """Stop weather animation"""
        print("[WeatherAnimation] Stopping animation")
        self.is_running = False
        
        # Cancel animation loop
        if self.animation_id:
            try:
                self.canvas.after_cancel(self.animation_id)
            except:
                pass
            self.animation_id = None
        
        # Clean up particles
        self._cleanup_particles()

    def set_weather_type(self, weather_type):
        """Change weather type and reinitialize particles"""
        if weather_type != self.current_weather:
            print(f"[WeatherAnimation] Changing weather type: {self.current_weather} -> {weather_type}")
            self.current_weather = weather_type
            self._cleanup_particles()
            self._initialize_particles()
            print(f"[WeatherAnimation] Particles reinitialized: {len(self.particles)}")

    def _start_animation_loop(self):
        """Start the main animation loop"""
        if self.is_running:
            self._animate_frame()

    def _animate_frame(self):
        """Single animation frame"""
        if not self.is_running:
            return

        try:
            self.frame_count += 1
            
            # Clear previous particles
            self.canvas.delete("particle")
            self.canvas.delete("background")
            
            # Draw background
            self._draw_background()
            
            # Update and draw particles
            active_particles = 0
            particles_to_remove = []
            
            for i, particle in enumerate(self.particles):
                if not hasattr(particle, 'active') or particle.active:
                    try:
                        particle.update()
                        particle.draw(self.canvas)
                        active_particles += 1
                        
                        # Remove particles that are way off screen
                        if particle.is_off_screen():
                            particles_to_remove.append(i)
                    except Exception as e:
                        print(f"[WeatherAnimation] Particle error: {e}")
                        particles_to_remove.append(i)
                else:
                    particles_to_remove.append(i)
            
            # Remove inactive particles
            for i in reversed(particles_to_remove):
                if i < len(self.particles):
                    try:
                        self.particles[i].cleanup(self.canvas)
                    except:
                        pass
                    del self.particles[i]
            
            # Add new particles if needed
            self._maintain_particle_count()
            
            # Handle special effects
            if self.current_weather == "storm":
                self._draw_lightning()
            
            # Schedule next frame
            self.animation_id = self.canvas.after(self.frame_delay, self._animate_frame)
            
        except Exception as e:
            print(f"[WeatherAnimation] Animation error: {e}")
            # Try to continue animation
            if self.is_running:
                self.animation_id = self.canvas.after(self.frame_delay, self._animate_frame)

    def _initialize_particles(self):
        """Initialize particles based on weather type"""
        self._cleanup_particles()
        self.lightning_timer = 0
        
        print(f"[WeatherAnimation] Initializing particles for: {self.current_weather}")
        
        weather_handlers = {
            "rain": self._create_rain_particles,
            "snow": self._create_snow_particles,
            "storm": self._create_storm_particles,
            "cloudy": self._create_cloud_particles,
            "mist": self._create_mist_particles,
            "sunny": self._create_clear_particles,
            "clear": self._create_clear_particles
        }
        
        handler = weather_handlers.get(self.current_weather, self._create_clear_particles)
        handler()
        
        print(f"[WeatherAnimation] Created {len(self.particles)} particles")

    def _create_rain_particles(self):
        """Create rain particles"""
        count = min(100, max(30, self.width // 10))
        for _ in range(count):
            x = random.randint(-100, self.width + 100)
            y = random.randint(-200, self.height)
            self.particles.append(RainDrop(x, y, self.width, self.height))

    def _create_snow_particles(self):
        """Create snow particles"""
        count = min(80, max(20, self.width // 15))
        for _ in range(count):
            x = random.randint(-50, self.width + 50)
            y = random.randint(-100, self.height)
            self.particles.append(SnowFlake(x, y, self.width, self.height))

    def _create_storm_particles(self):
        """Create storm particles (rain + clouds)"""
        # Add rain
        self._create_rain_particles()
        # Add storm clouds
        for _ in range(3):
            x = random.randint(-150, self.width)
            y = random.randint(20, self.height // 4)
            self.particles.append(CloudParticle(x, y, self.width, self.height))

    def _create_cloud_particles(self):
        """Create cloud particles"""
        count = min(6, max(2, self.width // 200))
        for _ in range(count):
            x = random.randint(-200, self.width)
            y = random.randint(50, self.height // 2)
            self.particles.append(CloudParticle(x, y, self.width, self.height))

    def _create_mist_particles(self):
        """Create mist effect"""
        # Create gentle cloud-like particles for mist
        count = min(15, max(5, self.width // 80))
        for _ in range(count):
            x = random.randint(-150, self.width)
            y = random.randint(self.height // 2, self.height)
            particle = CloudParticle(x, y, self.width, self.height)
            particle.speed = random.uniform(0.1, 0.5)  # Slower for mist
            self.particles.append(particle)

    def _create_clear_particles(self):
        """Create minimal particles for clear weather"""
        # Just a few gentle clouds for clear weather
        for _ in range(2):
            x = random.randint(-200, self.width)
            y = random.randint(50, self.height // 3)
            particle = CloudParticle(x, y, self.width, self.height)
            particle.speed = random.uniform(0.2, 0.6)
            self.particles.append(particle)

    def _maintain_particle_count(self):
        """Maintain appropriate particle count"""
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
        
        # Add particles if below target
        if current < target and current < self.max_particles:
            needed = min(target - current, 5)  # Add max 5 per frame
            for _ in range(needed):
                self._add_single_particle()

    def _add_single_particle(self):
        """Add a single particle of current weather type"""
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
        """Draw weather-appropriate background"""
        colors = {
            "rain": "#4A6741",      # Dark green-grey
            "snow": "#F0F8FF",      # Alice blue  
            "storm": "#2C3E50",     # Dark blue-grey
            "cloudy": "#B0C4DE",    # Light steel blue
            "mist": "#D3D3D3",      # Light grey
            "sunny": "#87CEEB",     # Sky blue
            "clear": "#87CEEB"      # Sky blue
        }
        
        bg_color = colors.get(self.current_weather, "#87CEEB")
        
        try:
            # Draw background rectangle
            self.canvas.create_rectangle(
                0, 0, self.width, self.height,
                fill=bg_color, outline="", tags="background"
            )
            
            # Draw sun for sunny weather
            if self.current_weather in ["sunny", "clear"]:
                self._draw_sun()
                
        except Exception as e:
            print(f"[WeatherAnimation] Background draw error: {e}")

    def _draw_sun(self):
        """Draw sun for sunny weather"""
        try:
            sun_x = self.width - 120
            sun_y = 80
            sun_radius = 40
            
            # Draw sun rays
            for i in range(12):
                angle = i * (2 * math.pi / 12)
                start_x = sun_x + math.cos(angle) * (sun_radius + 15)
                start_y = sun_y + math.sin(angle) * (sun_radius + 15)
                end_x = sun_x + math.cos(angle) * (sun_radius + 35)
                end_y = sun_y + math.sin(angle) * (sun_radius + 35)
                
                self.canvas.create_line(
                    start_x, start_y, end_x, end_y,
                    fill="#FFD700", width=3, tags="background"
                )
            
            # Draw sun circle
            self.canvas.create_oval(
                sun_x - sun_radius, sun_y - sun_radius,
                sun_x + sun_radius, sun_y + sun_radius,
                fill="#FFD700", outline="#FFA500", width=2, tags="background"
            )
        except Exception as e:
            print(f"[WeatherAnimation] Sun draw error: {e}")

    def _draw_lightning(self):
        """Draw lightning for storms"""
        self.lightning_timer += 1
        
        # Random lightning every 2-4 seconds
        if self.lightning_timer > 60 and random.random() < 0.03:
            try:
                self.lightning_timer = 0
                
                # Create lightning bolt
                start_x = random.randint(self.width // 4, 3 * self.width // 4)
                start_y = random.randint(0, self.height // 4)
                
                # Create jagged path
                points = [(start_x, start_y)]
                current_x, current_y = start_x, start_y
                
                for _ in range(random.randint(3, 6)):
                    current_x += random.randint(-40, 40)
                    current_y += random.randint(40, 80)
                    points.append((current_x, current_y))
                    
                    if current_y >= self.height:
                        break
                
                # Draw lightning
                for i in range(len(points) - 1):
                    self.canvas.create_line(
                        points[i][0], points[i][1],
                        points[i+1][0], points[i+1][1],
                        fill="#FFFF00", width=random.randint(2, 5),
                        tags="background"
                    )
                
                print("[WeatherAnimation] Lightning strike!")
                
            except Exception as e:
                print(f"[WeatherAnimation] Lightning error: {e}")

    def _cleanup_particles(self):
        """Clean up all particles"""
        try:
            # Clean up individual particles
            for particle in self.particles:
                if hasattr(particle, 'cleanup'):
                    particle.cleanup(self.canvas)
            
            # Clear particle list
            self.particles.clear()
            
            # Clear canvas tags
            self.canvas.delete("particle")
            self.canvas.delete("background")
            
        except Exception as e:
            print(f"[WeatherAnimation] Cleanup error: {e}")

    # Public interface methods
    def get_particle_count(self):
        """Get current particle count"""
        return len(self.particles)

    def is_animation_running(self):
        """Check if animation is running"""
        return self.is_running

    def get_current_weather(self):
        """Get current weather type"""
        return self.current_weather
    