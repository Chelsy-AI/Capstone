#!/usr/bin/env python3
"""
Enhanced Weather Animation System for Weather Dashboard
Provides realistic animated backgrounds that change based on weather conditions.
"""

import tkinter as tk
import random
import math
import time


class Particle:
    """Base class for weather particles"""
    def __init__(self, x, y, canvas_width, canvas_height):
        self.x = x
        self.y = y
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.id = None

    def update(self):
        """Update particle position - to be overridden"""
        pass

    def draw(self, canvas):
        """Draw particle on canvas - to be overridden"""
        pass

    def is_off_screen(self):
        """Check if particle is off screen"""
        return (self.x < -100 or self.x > self.canvas_width + 100 or 
                self.y < -100 or self.y > self.canvas_height + 100)


class RainDrop(Particle):
    """Rain drop particle"""
    def __init__(self, x, y, canvas_width, canvas_height):
        super().__init__(x, y, canvas_width, canvas_height)
        self.length = random.randint(20, 35)
        self.speed = random.uniform(10, 18)
        self.wind = random.uniform(-3, 3)

    def update(self):
        self.y += self.speed
        self.x += self.wind
        
        # Reset if off screen
        if self.y > self.canvas_height + 50:
            self.y = random.randint(-150, -50)
            self.x = random.randint(-100, self.canvas_width + 100)

    def draw(self, canvas):
        if self.id:
            canvas.delete(self.id)
        self.id = canvas.create_line(
            self.x, self.y,
            self.x + self.wind * 2, self.y + self.length,
            fill="#1E90FF", width=3, tags="weather_particle"
        )


class SnowFlake(Particle):
    """Snow flake particle"""
    def __init__(self, x, y, canvas_width, canvas_height):
        super().__init__(x, y, canvas_width, canvas_height)
        self.size = random.randint(4, 12)
        self.speed = random.uniform(2, 6)
        self.drift = random.uniform(-2, 2)
        self.drift_phase = random.uniform(0, 2 * math.pi)
        self.rotation = random.uniform(0, 2 * math.pi)

    def update(self):
        self.y += self.speed
        self.drift_phase += 0.03
        self.x += self.drift + math.sin(self.drift_phase) * 1.5
        self.rotation += 0.1
        
        # Reset if off screen
        if self.y > self.canvas_height + 50:
            self.y = random.randint(-100, -50)
            self.x = random.randint(-50, self.canvas_width + 50)

    def draw(self, canvas):
        if self.id:
            canvas.delete(self.id)
        
        # Draw snowflake as a star pattern
        points = []
        for i in range(6):
            angle = (i * math.pi / 3) + self.rotation
            x1 = self.x + math.cos(angle) * self.size
            y1 = self.y + math.sin(angle) * self.size
            points.extend([x1, y1])
        
        if len(points) >= 6:
            self.id = canvas.create_polygon(
                points, fill="white", outline="lightblue", 
                width=1, tags="weather_particle"
            )


class Cloud(Particle):
    """Cloud particle"""
    def __init__(self, x, y, canvas_width, canvas_height):
        super().__init__(x, y, canvas_width, canvas_height)
        self.width = random.randint(120, 220)
        self.height = random.randint(60, 100)
        self.speed = random.uniform(0.5, 1.5)
        self.opacity = random.uniform(0.4, 0.8)
        self.cloud_parts = []

    def update(self):
        self.x += self.speed
        
        # Reset if off screen
        if self.x > self.canvas_width + self.width:
            self.x = -self.width - 50
            self.y = random.randint(50, self.canvas_height // 2)

    def draw(self, canvas):
        # Delete previous cloud parts
        for part_id in self.cloud_parts:
            canvas.delete(part_id)
        self.cloud_parts.clear()
        
        # Draw cloud as multiple overlapping circles
        for i in range(6):
            offset_x = i * (self.width // 7)
            offset_y = random.randint(-self.height//3, self.height//3)
            circle_size = self.height + random.randint(-15, 15)
            
            part_id = canvas.create_oval(
                self.x + offset_x, self.y + offset_y,
                self.x + offset_x + circle_size, self.y + offset_y + circle_size,
                fill="#E5E5E5", outline="#D0D0D0", width=2, tags="weather_particle"
            )
            self.cloud_parts.append(part_id)
        
        self.id = self.cloud_parts[0] if self.cloud_parts else None


class Mist(Particle):
    """Mist particle"""
    def __init__(self, x, y, canvas_width, canvas_height):
        super().__init__(x, y, canvas_width, canvas_height)
        self.width = random.randint(100, 200)
        self.height = random.randint(40, 80)
        self.speed = random.uniform(0.3, 1.2)
        self.opacity = random.uniform(0.2, 0.6)
        self.phase = random.uniform(0, 2 * math.pi)

    def update(self):
        self.x += self.speed
        self.phase += 0.02
        self.y += math.sin(self.phase) * 0.5
        
        # Reset if off screen
        if self.x > self.canvas_width + self.width:
            self.x = -self.width
            self.y = random.randint(self.canvas_height // 2, self.canvas_height - 100)

    def draw(self, canvas):
        if self.id:
            canvas.delete(self.id)
        self.id = canvas.create_oval(
            self.x, self.y,
            self.x + self.width, self.y + self.height,
            fill="#F0F8FF", outline="", tags="weather_particle"
        )


class WeatherAnimation:
    """Main weather animation controller"""
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = 800
        self.height = 600
        self.particles = []
        self.is_running = False
        self.animation_id = None
        self.current_weather = "clear"
        self.lightning_timer = 0
        self.frame_count = 0
        
        # Animation settings
        self.fps = 30
        self.frame_delay = int(1000 / self.fps)
        
        print(f"[WeatherAnimation] Initialized with canvas size: {self.width}x{self.height}")
        
        # Bind canvas resize
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def _on_canvas_resize(self, event):
        """Handle canvas resize"""
        self.width = event.width
        self.height = event.height
        print(f"[WeatherAnimation] Canvas resized to: {self.width}x{self.height}")
        # Update particle boundaries
        for particle in self.particles:
            particle.canvas_width = self.width
            particle.canvas_height = self.height

    def update_size(self, width, height):
        """Update animation size"""
        self.width = width
        self.height = height
        print(f"[WeatherAnimation] Size updated to: {width}x{height}")
        for particle in self.particles:
            particle.canvas_width = width
            particle.canvas_height = height

    def start_animation(self, weather_type="clear"):
        """Start weather animation"""
        print(f"[WeatherAnimation] Starting animation: {weather_type}")
        self.current_weather = weather_type
        if not self.is_running:
            self.is_running = True
            self._initialize_particles()
            self._animate()
            print(f"[WeatherAnimation] Animation started with {len(self.particles)} particles")

    def stop_animation(self):
        """Stop weather animation"""
        print("[WeatherAnimation] Stopping animation")
        self.is_running = False
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None
        self._clear_particles()

    def set_weather_type(self, weather_type):
        """Change weather type and reinitialize particles"""
        print(f"[WeatherAnimation] Setting weather type: {weather_type}")
        if weather_type != self.current_weather:
            self.current_weather = weather_type
            self._clear_particles()
            self._initialize_particles()
            print(f"[WeatherAnimation] Particles reinitialized: {len(self.particles)}")

    def update_theme(self, theme):
        """Update animation colors based on theme"""
        # This can be expanded to adjust colors based on light/dark theme
        pass

    def _initialize_particles(self):
        """Initialize particles based on weather type"""
        self.particles.clear()
        self.lightning_timer = 0
        
        print(f"[WeatherAnimation] Initializing particles for: {self.current_weather}")
        
        if self.current_weather == "rain":
            self._create_rain_particles()
        elif self.current_weather == "snow":
            self._create_snow_particles()
        elif self.current_weather == "storm":
            self._create_storm_particles()
        elif self.current_weather == "cloudy":
            self._create_cloud_particles()
        elif self.current_weather == "mist":
            self._create_mist_particles()
        elif self.current_weather == "sunny":
            self._create_sun_elements()
        
        print(f"[WeatherAnimation] Created {len(self.particles)} particles")

    def _create_rain_particles(self):
        """Create rain particles"""
        particle_count = min(150, max(50, self.width // 8))
        for _ in range(particle_count):
            x = random.randint(-100, self.width + 100)
            y = random.randint(-200, self.height)
            self.particles.append(RainDrop(x, y, self.width, self.height))

    def _create_snow_particles(self):
        """Create snow particles"""
        particle_count = min(120, max(30, self.width // 12))
        for _ in range(particle_count):
            x = random.randint(-50, self.width + 50)
            y = random.randint(-100, self.height)
            self.particles.append(SnowFlake(x, y, self.width, self.height))

    def _create_storm_particles(self):
        """Create storm particles (rain + clouds)"""
        # Add rain
        self._create_rain_particles()
        # Add some dark clouds
        for _ in range(4):
            x = random.randint(-150, self.width)
            y = random.randint(30, self.height // 3)
            self.particles.append(Cloud(x, y, self.width, self.height))

    def _create_cloud_particles(self):
        """Create cloud particles"""
        cloud_count = min(8, max(3, self.width // 150))
        for _ in range(cloud_count):
            x = random.randint(-200, self.width)
            y = random.randint(50, self.height // 2)
            self.particles.append(Cloud(x, y, self.width, self.height))

    def _create_mist_particles(self):
        """Create mist particles"""
        mist_count = min(20, max(8, self.width // 60))
        for _ in range(mist_count):
            x = random.randint(-150, self.width)
            y = random.randint(self.height // 2, self.height)
            self.particles.append(Mist(x, y, self.width, self.height))

    def _create_sun_elements(self):
        """Create sun elements"""
        # Sun will be drawn statically in _draw_background
        pass

    def _animate(self):
        """Main animation loop"""
        if not self.is_running:
            return

        try:
            self.frame_count += 1
            
            # Clear previous frame
            self.canvas.delete("weather_particle")
            self.canvas.delete("weather_background")
            
            # Draw background
            self._draw_background()
            
            # Update and draw particles
            active_particles = 0
            for particle in self.particles[:]:  # Use slice to avoid modification during iteration
                particle.update()
                particle.draw(self.canvas)
                active_particles += 1
                
                # Remove particles that are way off screen (memory cleanup)
                if particle.is_off_screen():
                    if hasattr(particle, 'id') and particle.id:
                        self.canvas.delete(particle.id)

            # Handle special effects
            if self.current_weather == "storm":
                self._draw_lightning()
            
            # Debug info every 2 seconds
            if self.frame_count % (self.fps * 2) == 0:
                print(f"[WeatherAnimation] Frame {self.frame_count}: {active_particles} particles, {self.current_weather}")
            
            # Schedule next frame
            self.animation_id = self.canvas.after(self.frame_delay, self._animate)
            
        except Exception as e:
            print(f"[WeatherAnimation] Animation error: {e}")
            import traceback
            traceback.print_exc()
            # Continue animation even if there's an error
            self.animation_id = self.canvas.after(self.frame_delay, self._animate)

    def _draw_background(self):
        """Draw weather-appropriate background"""
        # Determine background color based on weather
        colors = {
            "rain": "#2F4F4F",      # Dark slate gray
            "snow": "#F0F8FF",      # Alice blue
            "storm": "#1C1C1C",     # Very dark gray
            "cloudy": "#B0C4DE",    # Light steel blue
            "mist": "#D3D3D3",      # Light gray
            "sunny": "#87CEEB",     # Sky blue
            "clear": "#87CEEB"      # Sky blue
        }
        
        bg_color = colors.get(self.current_weather, "#87CEEB")

        # Draw background
        self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            fill=bg_color, outline="", tags="weather_background"
        )

        # Draw sun for sunny weather
        if self.current_weather == "sunny":
            self._draw_sun()

    def _draw_sun(self):
        """Draw sun for sunny weather"""
        sun_x = self.width - 150
        sun_y = 120
        sun_radius = 60
        
        # Draw sun rays
        for i in range(16):
            angle = i * (2 * math.pi / 16)
            start_x = sun_x + math.cos(angle) * (sun_radius + 20)
            start_y = sun_y + math.sin(angle) * (sun_radius + 20)
            end_x = sun_x + math.cos(angle) * (sun_radius + 50)
            end_y = sun_y + math.sin(angle) * (sun_radius + 50)
            
            self.canvas.create_line(
                start_x, start_y, end_x, end_y,
                fill="#FFD700", width=5, tags="weather_background"
            )
        
        # Draw sun circle
        self.canvas.create_oval(
            sun_x - sun_radius, sun_y - sun_radius,
            sun_x + sun_radius, sun_y + sun_radius,
            fill="#FFD700", outline="#FFA500", width=3, tags="weather_background"
        )

    def _draw_lightning(self):
        """Draw lightning for storm weather"""
        self.lightning_timer += 1
        
        # Random lightning strikes
        if self.lightning_timer > 45 and random.random() < 0.05:
            self.lightning_timer = 0
            
            # Create lightning bolt
            start_x = random.randint(self.width // 4, 3 * self.width // 4)
            start_y = random.randint(0, self.height // 4)
            
            # Create jagged lightning path
            points = [(start_x, start_y)]
            current_x, current_y = start_x, start_y
            
            segments = random.randint(5, 10)
            for _ in range(segments):
                current_x += random.randint(-50, 50)
                current_y += random.randint(40, 100)
                points.append((current_x, current_y))
                
                if current_y >= self.height:
                    break
            
            # Draw lightning bolt
            for i in range(len(points) - 1):
                self.canvas.create_line(
                    points[i][0], points[i][1],
                    points[i+1][0], points[i+1][1],
                    fill="#FFFF00", width=random.randint(4, 8), 
                    tags="weather_background"
                )
            
            # Brief flash effect
            flash_id = self.canvas.create_rectangle(
                0, 0, self.width, self.height,
                fill="white", stipple="gray25", outline="", 
                tags="weather_background"
            )
            # Remove flash after short delay
            self.canvas.after(150, lambda: self.canvas.delete(flash_id))
            
            print("[WeatherAnimation] Lightning strike!")

    def _clear_particles(self):
        """Clear all particles and effects"""
        try:
            self.canvas.delete("weather_particle")
            self.canvas.delete("weather_background")
            self.particles.clear()
            print("[WeatherAnimation] Particles cleared")
        except Exception as e:
            print(f"[WeatherAnimation] Error clearing particles: {e}")

    def get_particle_count(self):
        """Get current particle count for debugging"""
        return len(self.particles)

    def is_animation_running(self):
        """Check if animation is currently running"""
        return self.is_running


# Test function
if __name__ == "__main__":
    def test_animation():
        root = tk.Tk()
        root.title("Enhanced Weather Animation Test")
        root.geometry("900x700")
        
        canvas = tk.Canvas(root, bg='skyblue')
        canvas.pack(fill=tk.BOTH, expand=True)
        
        animation = WeatherAnimation(canvas)
        animation.start_animation("rain")
        
        def change_weather():
            weathers = ["rain", "snow", "storm", "cloudy", "sunny", "mist", "clear"]
            current = weathers[int(time.time() / 4) % len(weathers)]
            animation.set_weather_type(current)
            root.title(f"Enhanced Animation Test - {current.title()}")
            root.after(4000, change_weather)
        
        root.after(2000, change_weather)
        
        def show_stats():
            count = animation.get_particle_count()
            running = animation.is_animation_running()
            print(f"Stats: {count} particles, running: {running}")
            root.after(5000, show_stats)
        
        root.after(1000, show_stats)
        root.mainloop()
    
    test_animation()