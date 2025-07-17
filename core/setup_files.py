#!/usr/bin/env python3
"""
Setup script to create necessary directories and files for the Weather App
Run this script to set up the project structure properly.
"""

import os
import sys

def create_directory_structure():
    """Create the necessary directory structure"""
    directories = [
        "gui",
        "core", 
        "features/tomorrows_guess",
        "features/history_tracker",
        "features/weather_icons",
        "features/theme_switcher", 
        "tests",
        "data"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_init_files():
    """Create __init__.py files for Python packages"""
    init_files = [
        "core/__init__.py",
        "gui/__init__.py", 
        "features/__init__.py",
        "features/tomorrows_guess/__init__.py",
        "features/history_tracker/__init__.py",
        "features/weather_icons/__init__.py",
        "features/theme_switcher/__init__.py",
        "tests/__init__.py"
    ]
    
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# Package initialization\n')
            print(f"✓ Created: {init_file}")

def create_weather_animation_file():
    """Create the weather animation file if it doesn't exist"""
    animation_file = "gui/weather_animation.py"
    
    if not os.path.exists(animation_file):
        # The content from the artifact above
        animation_content = '''#!/usr/bin/env python3
"""
Weather Animation System for Weather Dashboard
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
        return (self.x < -50 or self.x > self.canvas_width + 50 or 
                self.y < -50 or self.y > self.canvas_height + 50)


class RainDrop(Particle):
    """Rain drop particle"""
    def __init__(self, x, y, canvas_width, canvas_height):
        super().__init__(x, y, canvas_width, canvas_height)
        self.length = random.randint(15, 25)
        self.speed = random.uniform(8, 15)
        self.wind = random.uniform(-2, 2)

    def update(self):
        self.y += self.speed
        self.x += self.wind
        
        # Reset if off screen
        if self.y > self.canvas_height + 50:
            self.y = random.randint(-100, -50)
            self.x = random.randint(-50, self.canvas_width + 50)

    def draw(self, canvas):
        if self.id:
            canvas.delete(self.id)
        self.id = canvas.create_line(
            self.x, self.y,
            self.x + self.wind, self.y + self.length,
            fill="#4A90E2", width=2, tags="weather_particle"
        )


class SnowFlake(Particle):
    """Snow flake particle"""
    def __init__(self, x, y, canvas_width, canvas_height):
        super().__init__(x, y, canvas_width, canvas_height)
        self.size = random.randint(3, 8)
        self.speed = random.uniform(1, 4)
        self.drift = random.uniform(-1, 1)
        self.drift_phase = random.uniform(0, 2 * math.pi)

    def update(self):
        self.y += self.speed
        self.drift_phase += 0.02
        self.x += self.drift + math.sin(self.drift_phase) * 0.5
        
        # Reset if off screen
        if self.y > self.canvas_height + 20:
            self.y = random.randint(-50, -20)
            self.x = random.randint(-20, self.canvas_width + 20)

    def draw(self, canvas):
        if self.id:
            canvas.delete(self.id)
        self.id = canvas.create_oval(
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size,
            fill="white", outline="", tags="weather_particle"
        )


class Cloud(Particle):
    """Cloud particle"""
    def __init__(self, x, y, canvas_width, canvas_height):
        super().__init__(x, y, canvas_width, canvas_height)
        self.width = random.randint(100, 180)
        self.height = random.randint(40, 80)
        self.speed = random.uniform(0.3, 1.0)
        self.opacity = random.uniform(0.3, 0.7)

    def update(self):
        self.x += self.speed
        
        # Reset if off screen
        if self.x > self.canvas_width + self.width:
            self.x = -self.width
            self.y = random.randint(20, self.canvas_height // 3)

    def draw(self, canvas):
        if self.id:
            canvas.delete(self.id)
        
        # Draw cloud as multiple overlapping circles
        cloud_items = []
        for i in range(4):
            offset_x = i * (self.width // 5)
            offset_y = random.randint(-self.height//4, self.height//4)
            circle_size = self.height + random.randint(-10, 10)
            
            item_id = canvas.create_oval(
                self.x + offset_x, self.y + offset_y,
                self.x + offset_x + circle_size, self.y + offset_y + circle_size,
                fill="#D3D3D3", outline="", tags="weather_particle"
            )
            cloud_items.append(item_id)
        
        self.id = cloud_items[0]  # Store first item for deletion


class Mist(Particle):
    """Mist particle"""
    def __init__(self, x, y, canvas_width, canvas_height):
        super().__init__(x, y, canvas_width, canvas_height)
        self.width = random.randint(80, 150)
        self.height = random.randint(30, 60)
        self.speed = random.uniform(0.2, 0.8)
        self.opacity = random.uniform(0.1, 0.4)

    def update(self):
        self.x += self.speed
        
        # Reset if off screen
        if self.x > self.canvas_width + self.width:
            self.x = -self.width
            self.y = random.randint(self.canvas_height // 2, self.canvas_height)

    def draw(self, canvas):
        if self.id:
            canvas.delete(self.id)
        self.id = canvas.create_oval(
            self.x, self.y,
            self.x + self.width, self.y + self.height,
            fill="#E6E6FA", outline="", tags="weather_particle"
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
        self.sun_rays = []
        
        # Animation settings
        self.fps = 30
        self.frame_delay = int(1000 / self.fps)
        
        # Bind canvas resize
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def _on_canvas_resize(self, event):
        """Handle canvas resize"""
        self.width = event.width
        self.height = event.height
        # Update particle boundaries
        for particle in self.particles:
            particle.canvas_width = self.width
            particle.canvas_height = self.height

    def update_size(self, width, height):
        """Update animation size"""
        self.width = width
        self.height = height
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

    def update_theme(self, theme):
        """Update animation colors based on theme"""
        # This can be expanded to adjust colors based on light/dark theme
        pass

    def _initialize_particles(self):
        """Initialize particles based on weather type"""
        self.particles.clear()
        self.lightning_timer = 0
        
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

    def _create_rain_particles(self):
        """Create rain particles"""
        particle_count = min(100, max(30, self.width // 10))
        for _ in range(particle_count):
            x = random.randint(-50, self.width + 50)
            y = random.randint(-100, self.height)
            self.particles.append(RainDrop(x, y, self.width, self.height))

    def _create_snow_particles(self):
        """Create snow particles"""
        particle_count = min(80, max(20, self.width // 15))
        for _ in range(particle_count):
            x = random.randint(-20, self.width + 20)
            y = random.randint(-50, self.height)
            self.particles.append(SnowFlake(x, y, self.width, self.height))

    def _create_storm_particles(self):
        """Create storm particles (rain + clouds)"""
        # Add rain
        self._create_rain_particles()
        # Add some clouds
        for _ in range(3):
            x = random.randint(-100, self.width)
            y = random.randint(20, self.height // 4)
            self.particles.append(Cloud(x, y, self.width, self.height))

    def _create_cloud_particles(self):
        """Create cloud particles"""
        cloud_count = min(6, max(2, self.width // 200))
        for _ in range(cloud_count):
            x = random.randint(-150, self.width)
            y = random.randint(20, self.height // 2)
            self.particles.append(Cloud(x, y, self.width, self.height))

    def _create_mist_particles(self):
        """Create mist particles"""
        mist_count = min(15, max(5, self.width // 80))
        for _ in range(mist_count):
            x = random.randint(-100, self.width)
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
            # Clear previous frame
            self.canvas.delete("weather_particle")
            self.canvas.delete("weather_background")
            
            # Draw background
            self._draw_background()
            
            # Update and draw particles
            for particle in self.particles[:]:  # Use slice to avoid modification during iteration
                particle.update()
                particle.draw(self.canvas)
                
                # Remove particles that are way off screen (memory cleanup)
                if particle.is_off_screen():
                    if hasattr(particle, 'id') and particle.id:
                        self.canvas.delete(particle.id)

            # Handle special effects
            if self.current_weather == "storm":
                self._draw_lightning()
            
            # Schedule next frame
            self.animation_id = self.canvas.after(self.frame_delay, self._animate)
            
        except Exception as e:
            print(f"[WeatherAnimation] Animation error: {e}")
            # Continue animation even if there's an error
            self.animation_id = self.canvas.after(self.frame_delay, self._animate)

    def _draw_background(self):
        """Draw weather-appropriate background"""
        # Determine background color based on weather
        if self.current_weather == "rain":
            bg_color = "#4A6741"  # Dark green-grey
        elif self.current_weather == "snow":
            bg_color = "#E8F4F8"  # Light blue-white
        elif self.current_weather == "storm":
            bg_color = "#2C3E50"  # Dark blue-grey
        elif self.current_weather == "cloudy":
            bg_color = "#95A5A6"  # Grey
        elif self.current_weather == "mist":
            bg_color = "#BDC3C7"  # Light grey
        elif self.current_weather == "sunny":
            bg_color = "#87CEEB"  # Sky blue
        else:  # clear
            bg_color = "#87CEEB"  # Sky blue

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
        sun_x = self.width - 120
        sun_y = 100
        sun_radius = 50
        
        # Draw sun rays
        for i in range(12):
            angle = i * (2 * math.pi / 12)
            start_x = sun_x + math.cos(angle) * (sun_radius + 15)
            start_y = sun_y + math.sin(angle) * (sun_radius + 15)
            end_x = sun_x + math.cos(angle) * (sun_radius + 35)
            end_y = sun_y + math.sin(angle) * (sun_radius + 35)
            
            self.canvas.create_line(
                start_x, start_y, end_x, end_y,
                fill="#FFD700", width=4, tags="weather_background"
            )
        
        # Draw sun circle
        self.canvas.create_oval(
            sun_x - sun_radius, sun_y - sun_radius,
            sun_x + sun_radius, sun_y + sun_radius,
            fill="#FFD700", outline="#FFA500", width=2, tags="weather_background"
        )

    def _draw_lightning(self):
        """Draw lightning for storm weather"""
        self.lightning_timer += 1
        
        # Random lightning strikes
        if self.lightning_timer > 60 and random.random() < 0.03:
            self.lightning_timer = 0
            
            # Create lightning bolt
            start_x = random.randint(self.width // 4, 3 * self.width // 4)
            start_y = random.randint(0, self.height // 4)
            
            # Create jagged lightning path
            points = [(start_x, start_y)]
            current_x, current_y = start_x, start_y
            
            segments = random.randint(4, 8)
            for _ in range(segments):
                current_x += random.randint(-40, 40)
                current_y += random.randint(30, 80)
                points.append((current_x, current_y))
                
                if current_y >= self.height:
                    break
            
            # Draw lightning bolt
            for i in range(len(points) - 1):
                self.canvas.create_line(
                    points[i][0], points[i][1],
                    points[i+1][0], points[i+1][1],
                    fill="#FFFF00", width=random.randint(3, 6), 
                    tags="weather_background"
                )
            
            # Brief flash effect
            self.canvas.create_rectangle(
                0, 0, self.width, self.height,
                fill="white", stipple="gray25", outline="", 
                tags="weather_background"
            )
            # Remove flash after short delay
            self.canvas.after(100, lambda: self.canvas.delete("flash"))

    def _clear_particles(self):
        """Clear all particles and effects"""
        try:
            self.canvas.delete("weather_particle")
            self.canvas.delete("weather_background")
            self.particles.clear()
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
        root.title("Weather Animation Test")
        root.geometry("800x600")
        
        canvas = tk.Canvas(root, bg='skyblue')
        canvas.pack(fill=tk.BOTH, expand=True)
        
        animation = WeatherAnimation(canvas)
        animation.start_animation("rain")
        
        def change_weather():
            weathers = ["rain", "snow", "storm", "cloudy", "sunny", "mist", "clear"]
            current = weathers[int(time.time() / 3) % len(weathers)]
            animation.set_weather_type(current)
            root.title(f"Weather Animation Test - {current}")
            root.after(3000, change_weather)
        
        root.after(1000, change_weather)
        root.mainloop()
    
    test_animation()
'''
        
        with open(animation_file, 'w') as f:
            f.write(animation_content)
        print(f"✓ Created: {animation_file}")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def main():
    """Main setup function"""
    print("🌤️  Weather App Setup")
    print("=" * 50)
    
    if not check_python_version():
        return
    
    create_directory_structure()
    create_init_files()
    create_weather_animation_file()
    
    print("\n✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the app: python3 main.py")
    print("3. Test animations: python3 gui/weather_animation.py")

if __name__ == "__main__":
    main()