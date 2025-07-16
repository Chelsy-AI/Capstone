import random
import tkinter as tk
import math

class SmartBackground:
    def __init__(self, app, canvas):
        self.app = app
        self.canvas = canvas
        self.animation_running = False
        self.animation_id = None
        self.weather_condition = "clear"
        self.width = self.canvas.winfo_width() or 800
        self.height = self.canvas.winfo_height() or 600

        # Particles list for different weather effects
        self.particles = []
        self.clouds = []
        self.lightning_timer = 0
        
        # Bind to canvas resize
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def _on_canvas_resize(self, event):
        """Handle canvas resize events"""
        self.width = event.width
        self.height = event.height
        if self.animation_running:
            self._init_particles()

    def start_animation(self, weather_condition):
        """Start the animation with given weather condition"""
        print(f"[SmartBackground] Starting animation: {weather_condition}")
        self.weather_condition = self._normalize_weather_condition(weather_condition)
        if self.animation_running:
            return
        self.animation_running = True

        # Update size in case window resized
        self.width = self.canvas.winfo_width() or 800
        self.height = self.canvas.winfo_height() or 600

        self._init_particles()
        self._animate()

    def stop_animation(self):
        """Stop the animation"""
        self.animation_running = False
        if self.animation_id is not None:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None
        try:
            self.canvas.delete("weather_effect")
        except Exception:
            pass

    def update_background(self, weather_condition):
        """Update the background animation based on weather condition"""
        normalized_condition = self._normalize_weather_condition(weather_condition)
        if normalized_condition != self.weather_condition:
            self.weather_condition = normalized_condition
            self.width = self.canvas.winfo_width() or 800
            self.height = self.canvas.winfo_height() or 600
            self._init_particles()

    def _normalize_weather_condition(self, condition):
        """Normalize weather condition to standard types"""
        if not condition:
            return "clear"
        
        condition = condition.lower()
        
        # Rain patterns
        if any(word in condition for word in ["rain", "drizzle", "shower", "precipitation"]):
            return "rain"
        
        # Snow patterns
        elif any(word in condition for word in ["snow", "sleet", "blizzard", "flurries"]):
            return "snow"
        
        # Storm patterns
        elif any(word in condition for word in ["thunder", "storm", "lightning"]):
            return "storm"
        
        # Cloud patterns
        elif any(word in condition for word in ["cloud", "overcast", "partly cloudy", "mostly cloudy"]):
            return "cloudy"
        
        # Fog/Mist patterns
        elif any(word in condition for word in ["fog", "mist", "haze"]):
            return "fog"
        
        # Clear/Sunny patterns
        elif any(word in condition for word in ["clear", "sunny", "sun"]):
            return "sunny"
        
        # Default
        else:
            return "clear"

    def _init_particles(self):
        """Initialize particles based on weather condition"""
        self.particles.clear()
        self.clouds.clear()
        self.lightning_timer = 0
        
        if self.weather_condition == "rain":
            self._init_rain_particles()
        elif self.weather_condition == "snow":
            self._init_snow_particles()
        elif self.weather_condition == "storm":
            self._init_storm_particles()
        elif self.weather_condition == "cloudy":
            self._init_cloud_particles()
        elif self.weather_condition == "fog":
            self._init_fog_particles()
        elif self.weather_condition == "sunny":
            self._init_sunny_particles()

    def _init_rain_particles(self):
        """Initialize rain particles"""
        count = min(150, max(50, self.width // 8))
        for _ in range(count):
            x = random.randint(-50, self.width + 50)
            y = random.randint(-100, self.height)
            length = random.randint(15, 25)
            speed = random.uniform(8, 15)
            wind = random.uniform(-2, 2)
            self.particles.append({
                "x": x, "y": y, "length": length, "speed": speed, "wind": wind, "type": "rain"
            })

    def _init_snow_particles(self):
        """Initialize snow particles"""
        count = min(100, max(30, self.width // 12))
        for _ in range(count):
            x = random.randint(-20, self.width + 20)
            y = random.randint(-50, self.height)
            size = random.randint(3, 8)
            speed = random.uniform(1, 4)
            drift = random.uniform(-1, 1)
            drift_phase = random.uniform(0, 2 * math.pi)
            self.particles.append({
                "x": x, "y": y, "size": size, "speed": speed, "drift": drift, 
                "drift_phase": drift_phase, "type": "snow"
            })

    def _init_storm_particles(self):
        """Initialize storm particles (rain + clouds + lightning)"""
        # Rain particles
        self._init_rain_particles()
        # Add some clouds
        self._init_cloud_particles()
        # Lightning will be handled in animation

    def _init_cloud_particles(self):
        """Initialize cloud particles"""
        count = min(8, max(3, self.width // 200))
        for _ in range(count):
            x = random.randint(-100, self.width + 100)
            y = random.randint(20, self.height // 3)
            size = random.randint(80, 150)
            speed = random.uniform(0.5, 2)
            opacity = random.uniform(0.3, 0.8)
            self.clouds.append({
                "x": x, "y": y, "size": size, "speed": speed, "opacity": opacity, "type": "cloud"
            })

    def _init_fog_particles(self):
        """Initialize fog particles"""
        count = min(20, max(8, self.width // 60))
        for _ in range(count):
            x = random.randint(-50, self.width + 50)
            y = random.randint(self.height // 2, self.height)
            width = random.randint(100, 200)
            height = random.randint(30, 60)
            speed = random.uniform(0.2, 0.8)
            opacity = random.uniform(0.1, 0.4)
            self.particles.append({
                "x": x, "y": y, "width": width, "height": height, 
                "speed": speed, "opacity": opacity, "type": "fog"
            })

    def _init_sunny_particles(self):
        """Initialize sunny particles (sun rays)"""
        # Sun rays will be drawn statically, no particles needed
        pass

    def _animate(self):
        """Main animation loop"""
        if not self.animation_running:
            return

        # Clear previous weather effects
        self.canvas.delete("weather_effect")

        # Draw background
        self._draw_background()

        # Update and draw particles
        self._update_particles()
        self._draw_particles()

        # Draw clouds
        self._update_clouds()
        self._draw_clouds()

        # Handle special effects
        if self.weather_condition == "storm":
            self._draw_lightning()
        elif self.weather_condition == "sunny":
            self._draw_sun()

        # Schedule next frame (30 FPS)
        self.animation_id = self.canvas.after(33, self._animate)

    def _draw_background(self):
        """Draw the background color based on weather"""
        if self.weather_condition == "rain":
            bg_color = "#2c3e50"  # Dark blue-grey
        elif self.weather_condition == "snow":
            bg_color = "#ecf0f1"  # Light grey
        elif self.weather_condition == "storm":
            bg_color = "#1a1a2e"  # Very dark
        elif self.weather_condition == "cloudy":
            bg_color = "#95a5a6"  # Grey
        elif self.weather_condition == "fog":
            bg_color = "#bdc3c7"  # Light grey
        elif self.weather_condition == "sunny":
            bg_color = "#f39c12"  # Orange/yellow
        else:
            bg_color = "#3498db"  # Clear blue

        self.canvas.create_rectangle(
            0, 0, self.width, self.height, 
            fill=bg_color, outline="", tags="weather_effect"
        )

    def _update_particles(self):
        """Update particle positions"""
        for particle in self.particles:
            if particle["type"] == "rain":
                particle["y"] += particle["speed"]
                particle["x"] += particle["wind"]
                
                # Reset if off screen
                if particle["y"] > self.height + 50:
                    particle["y"] = random.randint(-100, -50)
                    particle["x"] = random.randint(-50, self.width + 50)
                    
            elif particle["type"] == "snow":
                particle["y"] += particle["speed"]
                particle["drift_phase"] += 0.02
                particle["x"] += particle["drift"] + math.sin(particle["drift_phase"]) * 0.5
                
                # Reset if off screen
                if particle["y"] > self.height + 20:
                    particle["y"] = random.randint(-50, -20)
                    particle["x"] = random.randint(-20, self.width + 20)
                    
            elif particle["type"] == "fog":
                particle["x"] += particle["speed"]
                
                # Reset if off screen
                if particle["x"] > self.width + particle["width"]:
                    particle["x"] = -particle["width"]
                    particle["y"] = random.randint(self.height // 2, self.height)

    def _draw_particles(self):
        """Draw particles based on their type"""
        for particle in self.particles:
            if particle["type"] == "rain":
                # Draw rain as blue lines
                self.canvas.create_line(
                    particle["x"], particle["y"],
                    particle["x"] + particle["wind"], particle["y"] + particle["length"],
                    fill="#74b9ff", width=2, tags="weather_effect"
                )
                
            elif particle["type"] == "snow":
                # Draw snow as white circles
                size = particle["size"]
                self.canvas.create_oval(
                    particle["x"] - size, particle["y"] - size,
                    particle["x"] + size, particle["y"] + size,
                    fill="white", outline="", tags="weather_effect"
                )
                
            elif particle["type"] == "fog":
                # Draw fog as semi-transparent rectangles
                self.canvas.create_rectangle(
                    particle["x"], particle["y"],
                    particle["x"] + particle["width"], particle["y"] + particle["height"],
                    fill="#ecf0f1", outline="", tags="weather_effect"
                )

    def _update_clouds(self):
        """Update cloud positions"""
        for cloud in self.clouds:
            cloud["x"] += cloud["speed"]
            
            # Reset if off screen
            if cloud["x"] > self.width + cloud["size"]:
                cloud["x"] = -cloud["size"]
                cloud["y"] = random.randint(20, self.height // 3)

    def _draw_clouds(self):
        """Draw clouds"""
        for cloud in self.clouds:
            # Draw cloud as multiple overlapping circles
            size = cloud["size"]
            x, y = cloud["x"], cloud["y"]
            
            # Cloud color based on weather
            if self.weather_condition == "storm":
                color = "#34495e"  # Dark grey
            else:
                color = "#ecf0f1"  # Light grey
            
            # Draw multiple circles to form cloud shape
            for i in range(5):
                offset_x = random.randint(-size//4, size//4)
                offset_y = random.randint(-size//6, size//6)
                circle_size = size // 3 + random.randint(-10, 10)
                
                self.canvas.create_oval(
                    x + offset_x, y + offset_y,
                    x + offset_x + circle_size, y + offset_y + circle_size,
                    fill=color, outline="", tags="weather_effect"
                )

    def _draw_lightning(self):
        """Draw lightning for storm weather"""
        self.lightning_timer += 1
        
        # Lightning strikes randomly
        if self.lightning_timer > 60 and random.random() < 0.05:  # Random lightning
            self.lightning_timer = 0
            
            # Create lightning bolt
            start_x = random.randint(self.width // 4, 3 * self.width // 4)
            start_y = random.randint(0, self.height // 4)
            
            # Create jagged lightning path
            points = [(start_x, start_y)]
            current_x, current_y = start_x, start_y
            
            while current_y < self.height:
                # Add some randomness to the path
                current_x += random.randint(-30, 30)
                current_y += random.randint(20, 60)
                points.append((current_x, current_y))
            
            # Draw lightning bolt
            for i in range(len(points) - 1):
                self.canvas.create_line(
                    points[i][0], points[i][1],
                    points[i+1][0], points[i+1][1],
                    fill="#fff700", width=random.randint(2, 4), tags="weather_effect"
                )
            
            # Brief flash effect
            self.canvas.create_rectangle(
                0, 0, self.width, self.height,
                fill="white", stipple="gray25", outline="", tags="weather_effect"
            )

    def _draw_sun(self):
        """Draw sun for sunny weather"""
        # Draw sun in upper right corner
        sun_x = self.width - 100
        sun_y = 80
        sun_radius = 40
        
        # Draw sun rays
        for i in range(8):
            angle = i * (2 * math.pi / 8)
            start_x = sun_x + math.cos(angle) * (sun_radius + 10)
            start_y = sun_y + math.sin(angle) * (sun_radius + 10)
            end_x = sun_x + math.cos(angle) * (sun_radius + 30)
            end_y = sun_y + math.sin(angle) * (sun_radius + 30)
            
            self.canvas.create_line(
                start_x, start_y, end_x, end_y,
                fill="#f1c40f", width=3, tags="weather_effect"
            )
        
        # Draw sun circle
        self.canvas.create_oval(
            sun_x - sun_radius, sun_y - sun_radius,
            sun_x + sun_radius, sun_y + sun_radius,
            fill="#f1c40f", outline="", tags="weather_effect"
        )