import tkinter as tk
from tkinter import Canvas
import math
import random
import threading
import time
from typing import Dict, List, Tuple, Optional

class WeatherParticle:
    """Individual weather particle (raindrop, snowflake, etc.)"""
    def __init__(self, x: float, y: float, particle_type: str):
        self.x = x
        self.y = y
        self.type = particle_type
        self.speed = random.uniform(2, 8)
        self.size = random.uniform(2, 6)
        self.angle = random.uniform(0, 2 * math.pi)
        self.phase = random.uniform(0, 2 * math.pi)
        self.opacity = random.uniform(0.3, 1.0)
        
        # Type-specific properties
        if particle_type == "rain":
            self.speed = random.uniform(8, 15)
            self.size = random.uniform(1, 3)
            self.wind_drift = random.uniform(-0.5, 0.5)
        elif particle_type == "snow":
            self.speed = random.uniform(1, 4)
            self.size = random.uniform(3, 8)
            self.drift = random.uniform(-1, 1)
        elif particle_type == "cloud":
            self.speed = random.uniform(0.5, 2)
            self.size = random.uniform(40, 80)
            self.y_drift = random.uniform(-0.2, 0.2)

class DynamicBackgroundManager:
    """Advanced weather animation manager with realistic effects"""
    
    def __init__(self, canvas: Canvas, width: int = 800, height: int = 600):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.is_running = False
        self.current_weather = "clear"
        self.animation_thread = None
        self.time_step = 0.0
        self.fps = 30
        
        # Animation elements
        self.particles: List[WeatherParticle] = []
        self.sun_angle = 0
        self.cloud_positions = []
        self.lightning_flash = 0
        self.rain_intensity = 0
        
        # Weather configurations
        self.weather_configs = {
            "clear": {"bg_color": "#87CEEB", "particles": 0},
            "sunny": {"bg_color": "#87CEEB", "particles": 0},
            "cloudy": {"bg_color": "#B0C4DE", "particles": 15},
            "rainy": {"bg_color": "#4682B4", "particles": 100},
            "snowy": {"bg_color": "#F0F8FF", "particles": 60},
            "stormy": {"bg_color": "#2F4F4F", "particles": 150}
        }
        
        self.init_weather_elements()
        
    def init_weather_elements(self):
        """Initialize weather-specific elements"""
        # Initialize cloud positions
        self.cloud_positions = []
        for i in range(5):
            self.cloud_positions.append({
                'x': random.randint(-100, self.width + 100),
                'y': random.randint(50, 200),
                'speed': random.uniform(0.5, 2),
                'size': random.uniform(0.8, 1.5)
            })
    
    def set_weather(self, weather_condition: str):
        """Set weather condition and initialize appropriate animations"""
        weather_condition = weather_condition.lower()
        
        # Map common weather terms
        weather_map = {
            "clear": "clear",
            "sunny": "sunny", 
            "sun": "sunny",
            "cloud": "cloudy",
            "cloudy": "cloudy",
            "overcast": "cloudy",
            "rain": "rainy",
            "rainy": "rainy",
            "drizzle": "rainy",
            "shower": "rainy",
            "snow": "snowy",
            "snowy": "snowy",
            "blizzard": "snowy",
            "storm": "stormy",
            "stormy": "stormy",
            "thunder": "stormy",
            "lightning": "stormy"
        }
        
        # Find matching weather condition
        for key, value in weather_map.items():
            if key in weather_condition:
                self.current_weather = value
                break
        else:
            self.current_weather = "clear"
        
        # Initialize particles for this weather
        self.init_particles()
        
        # Set canvas background (only if canvas still exists)
        if self.canvas.winfo_exists():
            bg_color = self.weather_configs[self.current_weather]["bg_color"]
            self.canvas.configure(bg=bg_color)
    
    def init_particles(self):
        """Initialize particles based on current weather"""
        self.particles = []
        config = self.weather_configs[self.current_weather]
        particle_count = config["particles"]
        
        if self.current_weather == "rainy":
            for _ in range(particle_count):
                particle = WeatherParticle(
                    random.randint(0, self.width),
                    random.randint(-100, 0),
                    "rain"
                )
                self.particles.append(particle)
                
        elif self.current_weather == "snowy":
            for _ in range(particle_count):
                particle = WeatherParticle(
                    random.randint(0, self.width),
                    random.randint(-100, 0),
                    "snow"
                )
                self.particles.append(particle)
                
        elif self.current_weather == "cloudy":
            for _ in range(particle_count):
                particle = WeatherParticle(
                    random.randint(-100, self.width + 100),
                    random.randint(50, 200),
                    "cloud"
                )
                self.particles.append(particle)
                
        elif self.current_weather == "stormy":
            # Add both rain and storm effects
            for _ in range(particle_count):
                particle = WeatherParticle(
                    random.randint(0, self.width),
                    random.randint(-100, 0),
                    "rain"
                )
                particle.speed *= 1.5  # Faster rain in storms
                self.particles.append(particle)
    
    def start_animation(self):
        """Start the weather animation"""
        if not self.is_running:
            self.is_running = True
            self.animation_thread = threading.Thread(target=self._animation_loop, daemon=True)
            self.animation_thread.start()
    
    def stop_animation(self):
        """Stop the weather animation"""
        self.is_running = False
        if self.animation_thread:
            self.animation_thread.join(timeout=1.0)
    
    def _animation_loop(self):
        """Main animation loop"""
        while self.is_running:
            try:
                # Only schedule update if canvas still exists
                if self.canvas.winfo_exists():
                    self.canvas.after_idle(self._update_frame)
                else:
                    self.is_running = False
                    break
                time.sleep(1.0 / self.fps)
            except Exception as e:
                print(f"Animation error: {e}")
                break
    
    def _update_frame(self):
        """Update single animation frame"""
        if not self.is_running:
            return
        
        try:
            # Only update if canvas still exists
            if not self.canvas.winfo_exists():
                self.is_running = False
                return
            
            # Clear previous frame
            self.canvas.delete("weather_animation")
            
            # Update time
            self.time_step += 0.1
            
            # Draw weather-specific animations
            if self.current_weather == "sunny":
                self._draw_sunny_weather()
            elif self.current_weather == "cloudy":
                self._draw_cloudy_weather()
            elif self.current_weather == "rainy":
                self._draw_rainy_weather()
            elif self.current_weather == "snowy":
                self._draw_snowy_weather()
            elif self.current_weather == "stormy":
                self._draw_stormy_weather()
            elif self.current_weather == "clear":
                self._draw_clear_weather()
                
        except Exception as e:
            print(f"Frame update error: {e}")
    
    def _draw_sunny_weather(self):
        """Draw sunny weather with moving sun and rays"""
        canvas_width = self.canvas.winfo_width() or self.width
        canvas_height = self.canvas.winfo_height() or self.height
        
        # Draw sun
        sun_x = canvas_width - 150
        sun_y = 100
        sun_radius = 40
        
        # Sun body
        self.canvas.create_oval(
            sun_x - sun_radius, sun_y - sun_radius,
            sun_x + sun_radius, sun_y + sun_radius,
            fill="#FFD700", outline="#FFA500", width=2,
            tags="weather_animation"
        )
        
        # Rotating sun rays
        self.sun_angle += 0.05
        for i in range(8):
            angle = self.sun_angle + (i * math.pi / 4)
            start_x = sun_x + math.cos(angle) * (sun_radius + 10)
            start_y = sun_y + math.sin(angle) * (sun_radius + 10)
            end_x = sun_x + math.cos(angle) * (sun_radius + 25)
            end_y = sun_y + math.sin(angle) * (sun_radius + 25)
            
            self.canvas.create_line(
                start_x, start_y, end_x, end_y,
                fill="#FFD700", width=3,
                tags="weather_animation"
            )
        
        # Add some floating light particles
        for i in range(10):
            particle_x = random.randint(0, canvas_width)
            particle_y = random.randint(0, canvas_height)
            brightness = math.sin(self.time_step + i) * 0.3 + 0.7
            
            self.canvas.create_oval(
                particle_x - 2, particle_y - 2,
                particle_x + 2, particle_y + 2,
                fill="#FFFF99", outline="",
                tags="weather_animation"
            )
    
    def _draw_cloudy_weather(self):
        """Draw moving clouds"""
        canvas_width = self.canvas.winfo_width() or self.width
        
        # Update and draw clouds
        for i, cloud in enumerate(self.cloud_positions):
            cloud['x'] += cloud['speed']
            
            # Reset cloud position when it goes off screen
            if cloud['x'] > canvas_width + 100:
                cloud['x'] = -100
                cloud['y'] = random.randint(50, 200)
            
            # Draw cloud (multiple overlapping circles)
            cloud_x = cloud['x']
            cloud_y = cloud['y']
            size = cloud['size']
            
            # Cloud circles
            circles = [
                (cloud_x, cloud_y, 30 * size),
                (cloud_x + 20 * size, cloud_y, 35 * size),
                (cloud_x + 40 * size, cloud_y, 30 * size),
                (cloud_x + 10 * size, cloud_y - 15 * size, 25 * size),
                (cloud_x + 30 * size, cloud_y - 15 * size, 25 * size)
            ]
            
            for cx, cy, radius in circles:
                self.canvas.create_oval(
                    cx - radius, cy - radius,
                    cx + radius, cy + radius,
                    fill="#FFFFFF", outline="#E0E0E0", width=1,
                    tags="weather_animation"
                )
    
    def _draw_rainy_weather(self):
        """Draw falling rain"""
        canvas_width = self.canvas.winfo_width() or self.width
        canvas_height = self.canvas.winfo_height() or self.height
        
        # Add some clouds first
        self._draw_rain_clouds()
        
        # Update and draw rain particles
        for particle in self.particles:
            # Update rain position
            particle.y += particle.speed
            particle.x += getattr(particle, 'wind_drift', 0)
            
            # Reset rain when it goes off screen
            if particle.y > canvas_height + 10:
                particle.y = random.randint(-50, -10)
                particle.x = random.randint(0, canvas_width)
            
            # Draw raindrop
            self.canvas.create_line(
                particle.x, particle.y,
                particle.x, particle.y + particle.size * 3,
                fill="#4682B4", width=2,
                tags="weather_animation"
            )
    
    def _draw_rain_clouds(self):
        """Draw rain clouds"""
        canvas_width = self.canvas.winfo_width() or self.width
        
        # Draw darker clouds for rain
        for i in range(3):
            cloud_x = i * (canvas_width // 3) + random.randint(-50, 50)
            cloud_y = random.randint(20, 80)
            
            # Dark cloud circles
            circles = [
                (cloud_x, cloud_y, 40),
                (cloud_x + 30, cloud_y, 45),
                (cloud_x + 60, cloud_y, 40),
                (cloud_x + 15, cloud_y - 20, 30),
                (cloud_x + 45, cloud_y - 20, 30)
            ]
            
            for cx, cy, radius in circles:
                self.canvas.create_oval(
                    cx - radius, cy - radius,
                    cx + radius, cy + radius,
                    fill="#696969", outline="#555555", width=1,
                    tags="weather_animation"
                )
    
    def _draw_snowy_weather(self):
        """Draw falling snow"""
        canvas_width = self.canvas.winfo_width() or self.width
        canvas_height = self.canvas.winfo_height() or self.height
        
        # Update and draw snow particles
        for particle in self.particles:
            # Update snow position with drift
            particle.y += particle.speed
            particle.x += math.sin(self.time_step + particle.phase) * 0.5
            
            # Reset snow when it goes off screen
            if particle.y > canvas_height + 10:
                particle.y = random.randint(-50, -10)
                particle.x = random.randint(0, canvas_width)
            
            # Draw snowflake
            self.canvas.create_oval(
                particle.x - particle.size/2, particle.y - particle.size/2,
                particle.x + particle.size/2, particle.y + particle.size/2,
                fill="#FFFFFF", outline="#E0E0E0", width=1,
                tags="weather_animation"
            )
            
            # Add snowflake arms
            arm_length = particle.size
            for i in range(6):
                angle = i * math.pi / 3
                end_x = particle.x + math.cos(angle) * arm_length
                end_y = particle.y + math.sin(angle) * arm_length
                
                self.canvas.create_line(
                    particle.x, particle.y, end_x, end_y,
                    fill="#FFFFFF", width=1,
                    tags="weather_animation"
                )
    
    def _draw_stormy_weather(self):
        """Draw stormy weather with lightning and heavy rain"""
        canvas_width = self.canvas.winfo_width() or self.width
        canvas_height = self.canvas.winfo_height() or self.height
        
        # Draw heavy rain
        self._draw_rainy_weather()
        
        # Add lightning flashes
        if random.random() < 0.02:  # 2% chance per frame
            self.lightning_flash = 10
        
        if self.lightning_flash > 0:
            # Draw lightning bolt
            lightning_x = random.randint(100, canvas_width - 100)
            lightning_points = [
                (lightning_x, 0),
                (lightning_x + random.randint(-30, 30), canvas_height // 4),
                (lightning_x + random.randint(-50, 50), canvas_height // 2),
                (lightning_x + random.randint(-30, 30), canvas_height * 3 // 4),
                (lightning_x + random.randint(-20, 20), canvas_height)
            ]
            
            for i in range(len(lightning_points) - 1):
                self.canvas.create_line(
                    lightning_points[i][0], lightning_points[i][1],
                    lightning_points[i + 1][0], lightning_points[i + 1][1],
                    fill="#FFFF00", width=3,
                    tags="weather_animation"
                )
            
            # Flash effect
            self.canvas.create_rectangle(
                0, 0, canvas_width, canvas_height,
                fill="#FFFFFF", stipple="gray25",
                tags="weather_animation"
            )
            
            self.lightning_flash -= 1
    
    def _draw_clear_weather(self):
        """Draw clear weather with subtle effects"""
        canvas_width = self.canvas.winfo_width() or self.width
        canvas_height = self.canvas.winfo_height() or self.height
        
        # Draw gentle floating particles (dust motes in sunlight)
        for i in range(15):
            particle_x = (i * 50 + self.time_step * 10) % canvas_width
            particle_y = 100 + math.sin(self.time_step + i) * 50
            
            self.canvas.create_oval(
                particle_x - 1, particle_y - 1,
                particle_x + 1, particle_y + 1,
                fill="#FFD700", outline="",
                tags="weather_animation"
            )
    
    def get_current_weather(self) -> str:
        """Get current weather condition"""
        return self.current_weather
    
    def set_fps(self, fps: int):
        """Set animation frame rate"""
        # Fix to ensure fps is always between 1 and 60
        if fps < 1:
            fps = 1
        elif fps > 60:
            fps = 60
        self.fps = fps
