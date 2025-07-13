import random
from datetime import datetime, time

class SmartBackground:
    """Handles intelligent background generation and animation of weather backgrounds"""
    
    def __init__(self, app, canvas):
        self.app = app
        self.canvas = canvas
        
        self.current_weather = None
        self.animation_running = False
        
        self.weather_effects = []  # List of dicts for moving weather elements (raindrops, snowflakes, etc)
        self.animation_speed = 50  # milliseconds per frame
        
    def get_time_period(self):
        now = datetime.now().time()
        if time(5, 30) <= now < time(8, 0):
            return "dawn"
        elif time(8, 0) <= now < time(17, 0):
            return "day"
        elif time(17, 0) <= now < time(20, 0):
            return "dusk"
        else:
            return "night"
    
    def get_weather_colors(self, weather_condition, time_period):
        """
        Return a list of colors (hex strings) based on the weather condition and time of day.
        This is a simple example. You can expand it for richer palettes.
        """
        weather_condition = (weather_condition or "clear").lower()
        if "rain" in weather_condition or "drizzle" in weather_condition or "shower" in weather_condition:
            base = "#5F9EA0"  # CadetBlue
            accent = "#4682B4"  # SteelBlue
            button = "#4169E1"  # RoyalBlue
        elif "snow" in weather_condition:
            base = "#E0FFFF"  # LightCyan
            accent = "#AFEEEE"  # PaleTurquoise
            button = "#B0E0E6"  # PowderBlue
        elif "cloud" in weather_condition or "overcast" in weather_condition:
            base = "#B0C4DE"  # LightSteelBlue
            accent = "#778899"  # LightSlateGray
            button = "#708090"  # SlateGray
        elif "thunder" in weather_condition or "storm" in weather_condition:
            base = "#2F4F4F"  # DarkSlateGray
            accent = "#696969"  # DimGray
            button = "#556B2F"  # DarkOliveGreen
        elif "mist" in weather_condition or "fog" in weather_condition or "haze" in weather_condition:
            base = "#F5F5F5"  # WhiteSmoke
            accent = "#DCDCDC"  # Gainsboro
            button = "#C0C0C0"  # Silver
        else:  # clear or default
            if time_period == "dawn":
                base = "#FFA07A"  # LightSalmon
                accent = "#FF7F50"  # Coral
                button = "#FF6347"  # Tomato
            elif time_period == "day":
                base = "#87CEEB"  # SkyBlue
                accent = "#6495ED"  # CornflowerBlue
                button = "#4169E1"  # RoyalBlue
            elif time_period == "dusk":
                base = "#FF4500"  # OrangeRed
                accent = "#FF6347"  # Tomato
                button = "#CD5C5C"  # IndianRed
            else:  # night
                base = "#191970"  # MidnightBlue
                accent = "#000080"  # Navy
                button = "#00008B"  # DarkBlue
        return [base, accent, button]

    def hex_to_rgb(self, hex_color):
        try:
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        except Exception:
            return (135, 206, 235)

    def create_gradient_background(self, colors):
        if not self.canvas.winfo_exists():
            return
        
        self.canvas.delete("background_gradient")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        steps = max(20, min(50, height // 10))
        
        for i in range(steps):
            ratio = i / steps
            r1, g1, b1 = self.hex_to_rgb(colors[0])
            r2, g2, b2 = self.hex_to_rgb(colors[-1])
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            y1 = int(height * i / steps)
            y2 = int(height * (i + 1) / steps)
            self.canvas.create_rectangle(0, y1, width, y2, fill=color, outline="", tags="background_gradient")

    def init_weather_effects(self, weather_condition):
        self.weather_effects.clear()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        weather_lower = (weather_condition or "clear").lower()
        
        if "rain" in weather_lower or "drizzle" in weather_lower or "shower" in weather_lower:
            # Create raindrops with random start positions and speeds
            for _ in range(max(20, width // 10)):
                drop = {
                    "x": random.randint(0, width),
                    "y": random.randint(0, height),
                    "length": random.randint(10, 20),
                    "speed": random.uniform(4, 8),
                    "id": None
                }
                self.weather_effects.append(("rain", drop))
        
        elif "snow" in weather_lower:
            # Create snowflakes with random start positions and speeds
            for _ in range(max(15, width // 20)):
                flake = {
                    "x": random.randint(0, width),
                    "y": random.randint(0, height),
                    "size": random.randint(2, 5),
                    "speed": random.uniform(1, 3),
                    "id": None
                }
                self.weather_effects.append(("snow", flake))
        
        elif "cloud" in weather_lower or "overcast" in weather_lower:
            # Static clouds for now (optional animation can be added)
            for _ in range(max(3, width // 150)):
                cloud = {
                    "x": random.randint(0, width-100),
                    "y": random.randint(0, height//2),
                    "id": None
                }
                self.weather_effects.append(("cloud", cloud))
        
        elif "thunder" in weather_lower or "storm" in weather_lower:
            # Static lightning flashes - we will animate flashes on update
            for _ in range(3):
                lightning = {
                    "x": random.randint(width//4, 3*width//4),
                    "y": random.randint(0, height//3),
                    "flash_on": False,
                    "id": None
                }
                self.weather_effects.append(("lightning", lightning))
        
        elif "mist" in weather_lower or "fog" in weather_lower or "haze" in weather_lower:
            for _ in range(8):
                mist = {
                    "x": random.randint(0, width),
                    "y": random.randint(0, height),
                    "id": None
                }
                self.weather_effects.append(("mist", mist))
    
    def animate(self):
        if not self.animation_running or not self.canvas.winfo_exists():
            return
        
        self.canvas.delete("weather_effects")
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        for effect_type, effect in self.weather_effects:
            if effect_type == "rain":
                x = effect["x"]
                y = effect["y"]
                length = effect["length"]
                # Draw raindrop line
                effect["id"] = self.canvas.create_line(
                    x, y, x+2, y+length, fill="#4169E1", width=1, tags="weather_effects"
                )
                # Move raindrop down by speed
                effect["y"] += effect["speed"]
                if effect["y"] > height:
                    effect["y"] = -length
                    effect["x"] = random.randint(0, width)
            
            elif effect_type == "snow":
                x = effect["x"]
                y = effect["y"]
                size = effect["size"]
                effect["id"] = self.canvas.create_oval(
                    x - size, y - size, x + size, y + size,
                    fill="white", outline="", tags="weather_effects"
                )
                effect["y"] += effect["speed"]
                effect["x"] += random.uniform(-1, 1)  # slight horizontal drift
                if effect["y"] > height:
                    effect["y"] = -size * 2
                    effect["x"] = random.randint(0, width)
            
            elif effect_type == "cloud":
                x = effect["x"]
                y = effect["y"]
                # Draw cloud with overlapping ovals
                offsets = [(0, 0), (20, -5), (40, 0), (60, -3)]
                for ox, oy in offsets:
                    self.canvas.create_oval(
                        x+ox, y+oy, x+ox+40, y+oy+20,
                        fill="#F0F0F0", outline="", tags="weather_effects"
                    )
                # Slowly move clouds horizontally
                effect["x"] += 0.5
                if effect["x"] > width:
                    effect["x"] = -100
            
            elif effect_type == "lightning":
                # Randomly flash lightning lines
                if random.random() < 0.05:
                    effect["flash_on"] = True
                else:
                    effect["flash_on"] = False
                
                if effect["flash_on"]:
                    x = effect["x"]
                    y = effect["y"]
                    self.canvas.create_line(
                        x, y, x+random.randint(-20, 20), y+30,
                        fill="#FFFF00", width=3, tags="weather_effects"
                    )
            
            elif effect_type == "mist":
                x = effect["x"]
                y = effect["y"]
                self.canvas.create_oval(
                    x-30, y-10, x+30, y+10,
                    fill="#E6E6FA", outline="", tags="weather_effects"
                )
                # Mist can drift slowly
                effect["x"] += 0.2
                if effect["x"] > width:
                    effect["x"] = -30

        # Schedule next animation frame
        self.app.after(self.animation_speed, self.animate)
    
    def start_animation(self, weather_condition="clear"):
        if not self.canvas.winfo_exists():
            return
        self.animation_running = True
        time_period = self.get_time_period()
        colors = self.get_weather_colors(weather_condition, time_period)
        self.create_gradient_background(colors)
        self.init_weather_effects(weather_condition)
        self.animate()
    
    def stop_animation(self):
        self.animation_running = False
    
    def update_weather(self, weather_condition):
        # Stop current animation then restart with new condition
        self.stop_animation()
        self.start_animation(weather_condition)

    def get_adaptive_theme(self, weather_condition="clear"):
        """Return a theme dict adapted to weather and time with good contrast"""
        try:
            time_period = self.get_time_period()
            colors = self.get_weather_colors(weather_condition, time_period)

            # Convert first color to RGB to check brightness
            r, g, b = self.hex_to_rgb(colors[0] if colors else "#87CEEB")
            brightness = (r * 299 + g * 587 + b * 114) / 1000

            if brightness > 128:
                # Light background — dark text
                return {
                    "bg": colors[0],
                    "fg": "#1A1A1A",
                    "text_bg": f"#{min(255, r+20):02x}{min(255, g+20):02x}{min(255, b+20):02x}",
                    "text_fg": "#1A1A1A",
                    "button_bg": colors[2] if len(colors) > 2 else "#4169E1",
                    "button_fg": "#FFFFFF",
                    "entry_bg": "#FFFFFF",
                    "entry_fg": "#1A1A1A",
                    "accent": colors[1] if len(colors) > 1 else "#6495ED"
                }
            else:
                # Dark background — light text
                return {
                    "bg": colors[0],
                    "fg": "#F5F5F5",
                    "text_bg": f"#{max(0, r-20):02x}{max(0, g-20):02x}{max(0, b-20):02x}",
                    "text_fg": "#F5F5F5",
                    "button_bg": colors[2] if len(colors) > 2 else "#4169E1",
                    "button_fg": "#FFFFFF",
                    "entry_bg": "#2F2F2F",
                    "entry_fg": "#F5F5F5",
                    "accent": colors[1] if len(colors) > 1 else "#6495ED"
                }
        except Exception as e:
            print(f"Adaptive theme error: {e}")
            # Return a safe fallback theme
            return {
                "bg": "#87CEEB",
                "fg": "#1A1A1A",
                "text_bg": "#F0F8FF",
                "text_fg": "#1A1A1A",
                "button_bg": "#4169E1",
                "button_fg": "#FFFFFF",
                "entry_bg": "#FFFFFF",
                "entry_fg": "#1A1A1A",
                "accent": "#6495ED"
            }
    def update_background(self, weather_condition):
        """Update the background animation with a new weather condition."""
        self.update_weather(weather_condition)

    def lower_background(self):
        try:
            self.canvas.tag_lower("background_gradient")
        except Exception:
            pass
