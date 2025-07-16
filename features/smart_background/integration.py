import tkinter as tk
import random
import time
from typing import Optional, Dict, Any

# === Background Manager Implementation (Integrated here) ===

class Particle:
    def __init__(self, canvas, x, y, vx, vy, size, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.color = color
        self.id = self.canvas.create_oval(
            x, y, x + size, y + size, fill=color, outline=''
        )
    
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.canvas.move(self.id, self.vx, self.vy)
        
    def is_offscreen(self, width, height):
        return self.x > width or self.y > height or self.x < -self.size or self.y < -self.size
    
    def delete(self):
        self.canvas.delete(self.id)

class DynamicBackgroundManager:
    def __init__(self, canvas: tk.Canvas, width: int, height: int):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.weather = "clear"
        self.particles = []
        self.is_running = False
        self._animation_id = None
    
    def set_weather(self, weather_condition: str):
        self.weather = weather_condition.lower()
        self.clear_particles()
    
    def start_animation(self):
        if not self.is_running:
            self.is_running = True
            self.animate()
    
    def stop_animation(self):
        if self.is_running:
            self.is_running = False
            if self._animation_id:
                self.canvas.after_cancel(self._animation_id)
                self._animation_id = None
    
    def clear_particles(self):
        for p in self.particles:
            p.delete()
        self.particles.clear()
    
    def animate(self):
        if not self.is_running:
            return
        
        self.update_particles()
        self._animation_id = self.canvas.after(33, self.animate)  # ~30 FPS
    
    def update_particles(self):
        # Add new particles depending on weather
        if self.weather == "rainy":
            self.create_rain_particle()
        elif self.weather == "snowy":
            self.create_snow_particle()
        elif self.weather == "stormy":
            self.create_storm_particle()
        elif self.weather == "cloudy":
            self.create_cloud_particle()
        elif self.weather == "sunny":
            self.create_sun_particle()
        else:
            # clear or unknown - no particles or minimal
            pass
        
        # Move existing particles
        for p in self.particles[:]:
            p.move()
            if p.is_offscreen(self.width, self.height):
                p.delete()
                self.particles.remove(p)
    
    def create_rain_particle(self):
        x = random.randint(0, self.width)
        y = -10
        vx = 0
        vy = random.uniform(8, 12)
        size = random.randint(1, 2)
        color = '#0af'  # blueish rain drop
        p = Particle(self.canvas, x, y, vx, vy, size, color)
        self.particles.append(p)
    
    def create_snow_particle(self):
        x = random.randint(0, self.width)
        y = -10
        vx = random.uniform(-1, 1)
        vy = random.uniform(1, 3)
        size = random.randint(2, 4)
        color = 'white'
        p = Particle(self.canvas, x, y, vx, vy, size, color)
        self.particles.append(p)
    
    def create_storm_particle(self):
        # Combination of rain and occasional lightning flashes
        # For simplicity, spawn rain + draw occasional lightning rectangle
        self.create_rain_particle()
        if random.random() < 0.02:
            # flash lightning (just fill screen white for a short time)
            self.canvas.create_rectangle(
                0, 0, self.width, self.height,
                fill='white', stipple='gray50', outline=''
            )
    
    def create_cloud_particle(self):
        # Simple cloud drifting from left to right
        x = -50
        y = random.randint(50, 150)
        vx = random.uniform(1, 2)
        vy = 0
        size = random.randint(50, 100)
        color = '#bbb'  # gray cloud
        p = Particle(self.canvas, x, y, vx, vy, size, color)
        self.particles.append(p)
    
    def create_sun_particle(self):
        # Sun is static circle, no particles, but maybe rays moving
        # For simplicity, draw a sun in corner and skip particles
        self.canvas.delete('sun')
        self.canvas.create_oval(
            self.width - 100, 20, self.width - 40, 80,
            fill='yellow', outline='', tags='sun'
        )

# === Integration Class ===

class SmartBackgroundIntegration:
    """Integrates weather animations with weather app GUI"""
    
    def __init__(self, parent_widget: tk.Widget):
        self.parent = parent_widget
        self.canvas: Optional[tk.Canvas] = None
        self.bg_manager: Optional[DynamicBackgroundManager] = None
        self.is_enabled = True
        self.widget_frame: Optional[tk.Frame] = None
        print("[SmartBackground] __init__ called")

    def setup_canvas(self, width: int = 800, height: int = 600) -> tk.Canvas:
        """Setup canvas for weather animations"""
        if self.canvas:
            self.canvas.destroy()
            
        # Create main canvas for animations
        self.canvas = tk.Canvas(
            self.parent,
            width=width,
            height=height,
            highlightthickness=0,
            bg='#87CEEB'  # Sky blue default
        )
        
        # Initialize background manager
        self.bg_manager = DynamicBackgroundManager(self.canvas, width, height)
        
        return self.canvas
    
    def create_widget_frame(self, x: int = None, y: int = None, 
                          bg_color: str = 'white', alpha: float = 0.9) -> tk.Frame:
        """Create a frame for widgets on top of the animated background"""
        if not self.canvas:
            raise ValueError("Canvas must be setup first")
        
        # Default to center of canvas
        if x is None:
            x = self.canvas.winfo_reqwidth() // 2
        if y is None:
            y = self.canvas.winfo_reqheight() // 2
        
        # Create frame for widgets with background color
        self.widget_frame = tk.Frame(
            self.canvas,
            bg=bg_color,
            relief=tk.RAISED,
            bd=2,
            padx=20,
            pady=20
        )
        
        # Place frame on canvas
        self.canvas.create_window(x, y, window=self.widget_frame)
        
        return self.widget_frame
    
    def update_weather_background(self, weather_data: Dict[str, Any]):
        """Update background animation based on weather data"""
        if not self.bg_manager or not self.is_enabled:
            return
            
        # Extract weather condition from data
        weather_condition = self._extract_weather_condition(weather_data)
        
        # Update background
        self.bg_manager.set_weather(weather_condition)
        
        # Start animation if not running
        if not self.bg_manager.is_running:
            self.bg_manager.start_animation()
    
    def _extract_weather_condition(self, weather_data: Dict[str, Any]) -> str:
        """Extract weather condition from weather data"""
        if isinstance(weather_data, dict):
            # Check various possible keys for weather condition
            condition_keys = [
                'weather', 'condition', 'description', 'main',
                'weather_condition', 'current_condition', 'summary'
            ]
            
            for key in condition_keys:
                if key in weather_data:
                    condition = str(weather_data[key]).lower()
                    return condition
            
            # Handle OpenWeatherMap API format
            if 'weather' in weather_data and isinstance(weather_data['weather'], list):
                if len(weather_data['weather']) > 0:
                    weather_item = weather_data['weather'][0]
                    if 'main' in weather_item:
                        condition = str(weather_item['main']).lower()
                        return condition
                    elif 'description' in weather_item:
                        condition = str(weather_item['description']).lower()
                        return condition
            
            # Handle other nested formats
            if 'current' in weather_data:
                current = weather_data['current']
                if 'condition' in current:
                    condition = str(current['condition']).lower()
                    return condition
                elif 'text' in current:
                    condition = str(current['text']).lower()
                    return condition
            
            # Try to find any key that contains weather info
            for key, value in weather_data.items():
                if isinstance(value, str) and any(weather in value.lower() for weather in 
                    ['clear', 'sunny', 'cloudy', 'rainy', 'snowy', 'stormy', 'rain', 'snow', 'cloud', 'sun']):
                    condition = str(value).lower()
                    return condition
        
        return "clear"
    
    def set_weather_manually(self, weather_condition: str):
        """Manually set weather condition"""
        if self.bg_manager:
            self.bg_manager.set_weather(weather_condition)
            if not self.bg_manager.is_running and self.is_enabled:
                self.bg_manager.start_animation()
    
    def start_animation(self):
        print("[DEBUG] Starting SmartBackground animation")
        """Start weather animation"""
        if self.bg_manager and self.is_enabled:
            self.bg_manager.start_animation()
    
    def stop_animation(self):
        """Stop weather animation"""
        if self.bg_manager:
            self.bg_manager.stop_animation()
        print(f"[SmartBackground] Starting animation: {weather_condition}")

    def toggle_animation(self) -> bool:
        """Toggle animation on/off"""
        self.is_enabled = not self.is_enabled
        
        if self.is_enabled:
            self.start_animation()
        else:
            self.stop_animation()
            
        return self.is_enabled
    
    def get_canvas(self) -> Optional[tk.Canvas]:
        """Get the canvas widget"""
        return self.canvas
    
    def get_widget_frame(self) -> Optional[tk.Frame]:
        """Get the widget frame"""
        return self.widget_frame
    
    def destroy(self):
        """Clean up resources"""
        if self.bg_manager:
            self.bg_manager.stop_animation()
        if self.canvas:
            self.canvas.destroy()
            self.canvas = None
        self.bg_manager = None
        self.widget_frame = None

# === Test function with UI ===

def test_weather_animations():
    root = tk.Tk()
    root.title("Dynamic Weather Background Test")
    root.geometry("1000x700")
    root.configure(bg='black')
    
    smart_bg = SmartBackgroundIntegration(root)
    canvas = smart_bg.setup_canvas(1000, 700)
    canvas.pack(fill=tk.BOTH, expand=True)
    
    widget_frame = smart_bg.create_widget_frame(500, 350, bg_color='#f0f0f0', alpha=0.9)
    
    title = tk.Label(
        widget_frame,
        text="🌤️ Dynamic Weather Animation Test",
        font=('Arial', 18, 'bold'),
        bg='#f0f0f0',
        fg='#333333'
    )
    title.pack(pady=10)
    
    current_weather = tk.Label(
        widget_frame,
        text="Current Weather: Clear Sky",
        font=('Arial', 12, 'bold'),
        bg='#f0f0f0',
        fg='#2c3e50'
    )
    current_weather.pack(pady=5)
    
    weather_desc = tk.Label(
        widget_frame,
        text="Perfect clear sky with gentle breeze",
        font=('Arial', 10),
        bg='#f0f0f0',
        fg='#7f8c8d'
    )
    weather_desc.pack(pady=5)
    
    weather_types = [
        ("☀️ Clear", "clear", "Beautiful clear sky"),
        ("🌞 Sunny", "sunny", "Bright sunshine with animated sun"),
        ("☁️ Cloudy", "cloudy", "Overcast with moving clouds"),
        ("🌧️ Rainy", "rainy", "Heavy rain with falling drops"),
        ("❄️ Snowy", "snowy", "Gentle snowfall"),
        ("⛈️ Stormy", "stormy", "Thunderstorm with lightning")
    ]
    
    button_frame = tk.Frame(widget_frame, bg='#f0f0f0')
    button_frame.pack(pady=15)
    
    for i, (display_name, weather_code, description) in enumerate(weather_types):
        colors = {
            "clear": ("#3498db", "#2980b9"),
            "sunny": ("#f39c12", "#e67e22"),
            "cloudy": ("#95a5a6", "#7f8c8d"),
            "rainy": ("#34495e", "#2c3e50"),
            "snowy": ("#ecf0f1", "#bdc3c7"),
            "stormy": ("#8e44ad", "#732d91")
        }
        
        bg_color, hover_color = colors.get(weather_code, ("#3498db", "#2980b9"))
        
        btn = tk.Button(
            button_frame,
            text=display_name,
            command=lambda w=weather_code, d=display_name, desc=description: [
                smart_bg.set_weather_manually(w),
                current_weather.config(text=f"Current Weather: {d}"),
                weather_desc.config(text=desc)
            ],
            bg=bg_color,
            fg='white',
            font=('Arial', 10, 'bold'),
            width=12,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor="hand2"
        )
        btn.grid(row=i//3, column=i%3, padx=8, pady=5)
        
        def on_enter(event, btn=btn, color=hover_color):
            btn.config(bg=color)
        
        def on_leave(event, btn=btn, color=bg_color):
            btn.config(bg=color)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    control_frame = tk.Frame(widget_frame, bg='#f0f0f0')
    control_frame.pack(pady=15)
    
    auto_cycling = False
    cycle_index = 0
    
    def auto_cycle():
        nonlocal auto_cycling, cycle_index
        if auto_cycling:
            display_name, weather_code, description = weather_types[cycle_index]
            smart_bg.set_weather_manually(weather_code)
            current_weather.config(text=f"Auto-Cycle: {display_name}")
            weather_desc.config(text=description)
            cycle_index = (cycle_index + 1) % len(weather_types)
            root.after(5000, auto_cycle)
    
    def toggle_auto_cycle():
        nonlocal auto_cycling
        auto_cycling = not auto_cycling
        if auto_cycling:
            auto_cycle_btn.config(text="🔄 Stop Auto-Cycle", bg='#e74c3c')
            auto_cycle()
        else:
            auto_cycle_btn.config(text="🔄 Start Auto-Cycle", bg='#27ae60')
    
    auto_cycle_btn = tk.Button(
        control_frame,
        text="🔄 Start Auto-Cycle",
        command=toggle_auto_cycle,
        bg='#27ae60',
        fg='white',
        font=('Arial', 11, 'bold'),
        width=15,
        height=2,
        relief=tk.RAISED,
        bd=3,
        cursor="hand2"
    )
    auto_cycle_btn.pack(side=tk.LEFT, padx=5)
    
    def toggle_animation():
        enabled = smart_bg.toggle_animation()
        if enabled:
            animation_btn.config(text="⏸️ Pause Animation", bg='#f39c12')
        else:
            animation_btn.config(text="▶️ Resume Animation", bg='#27ae60')
    
    animation_btn = tk.Button(
        control_frame,
        text="⏸️ Pause Animation",
        command=toggle_animation,
        bg='#f39c12',
        fg='white',
        font=('Arial', 11, 'bold'),
        width=15,
        height=2,
        relief=tk.RAISED,
        bd=3,
        cursor="hand2"
    )
    animation_btn.pack(side=tk.LEFT, padx=5)
    
    instructions = tk.Label(
        widget_frame,
        text="🎯 Click weather buttons to see realistic animated backgrounds!\n"
             "🌟 Watch rain fall, snow drift, clouds move, and lightning strike!",
        font=('Arial', 9),
        bg='#f0f0f0',
        fg='#7f8c8d',
        justify=tk.CENTER
    )
    instructions.pack(pady=10)
    
    status_frame = tk.Frame(widget_frame, bg='#f0f0f0')
    status_frame.pack(pady=5, fill=tk.X)
    
    status_label = tk.Label(
        status_frame,
        text="Status: Animation Running | FPS: ~30 | Particles: Dynamic",
        font=('Arial', 8),
        bg='#f0f0f0',
        fg='#95a5a6'
    )
    status_label.pack()
    
    smart_bg.set_weather_manually("clear")
    
    def update_status():
        if smart_bg.bg_manager:
            particle_count = len(smart_bg.bg_manager.particles)
            animation_status = "Running" if smart_bg.bg_manager.is_running else "Paused"
            status_label.config(text=f"Status: {animation_status} | FPS: ~30 | Particles: {particle_count}")
        root.after(1000, update_status)
    
    update_status()
    
    def on_closing():
        smart_bg.destroy()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    test_weather_animations()
