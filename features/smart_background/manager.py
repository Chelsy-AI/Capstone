import tkinter as tk
import random
import math

class WeatherParticle:
    def __init__(self, x, y, p_type, width, height):
        self.x = x
        self.y = y
        self.type = p_type
        self.canvas_width = width
        self.canvas_height = height

        if p_type == "rain":
            self.length = random.randint(10, 20)
            self.speed = random.uniform(6, 12)
            self.wind = random.uniform(-0.5, 0.5)
        elif p_type == "snow":
            self.size = random.randint(2, 6)
            self.speed = random.uniform(1, 3)
            self.drift_phase = random.uniform(0, 2 * math.pi)
        elif p_type == "cloud":
            self.width = 80
            self.height = 40
            self.speed = random.uniform(0.3, 0.7)
        elif p_type == "lightning":
            self.flash_timer = 0
            self.flash_duration = random.randint(2, 5)
        elif p_type == "mist":
            self.width = 60
            self.height = 20
            self.speed = random.uniform(0.1, 0.3)
        else:
            self.speed = 1  # default

    def update(self):
        if self.type == "rain":
            self.y += self.speed
            self.x += self.wind
            if self.y > self.canvas_height:
                self.y = random.uniform(-20, 0)
                self.x = random.uniform(0, self.canvas_width)
        elif self.type == "snow":
            self.y += self.speed
            self.x += math.sin(self.drift_phase) * 0.5
            self.drift_phase += 0.1
            if self.y > self.canvas_height:
                self.y = random.uniform(-10, 0)
                self.x = random.uniform(0, self.canvas_width)
        elif self.type == "cloud":
            self.x += self.speed
            if self.x > self.canvas_width:
                self.x = -self.width
        elif self.type == "lightning":
            self.flash_timer += 1
            if self.flash_timer > self.flash_duration * 10:
                self.flash_timer = 0
                self.flash_duration = random.randint(2, 5)
        elif self.type == "mist":
            self.x += self.speed
            if self.x > self.canvas_width + self.width:
                self.x = -self.width

    def draw(self, canvas):
        if self.type == "rain":
            canvas.create_line(
                self.x, self.y,
                self.x, self.y + self.length,
                fill="#4169E1", width=1, tags="weather"
            )
        elif self.type == "snow":
            canvas.create_oval(
                self.x - self.size, self.y - self.size,
                self.x + self.size, self.y + self.size,
                fill="white", outline="", tags="weather"
            )
        elif self.type == "cloud":
            ox, oy = self.x, self.y
            for dx, dy in [(0,0), (20,-10), (40,0), (60,-5)]:
                canvas.create_oval(
                    ox + dx, oy + dy,
                    ox + dx + 50, oy + dy + 30,
                    fill="#F0F0F0", outline="", tags="weather"
                )
        elif self.type == "lightning":
            if random.random() < 0.1:
                x = random.uniform(0.25 * self.canvas_width, 0.75 * self.canvas_width)
                y = random.uniform(0, 0.3 * self.canvas_height)
                points = [
                    (x, y),
                    (x + 10, y + 20),
                    (x - 10, y + 30),
                    (x + 10, y + 50),
                ]
                for i in range(len(points) - 1):
                    canvas.create_line(
                        points[i][0], points[i][1], points[i+1][0], points[i+1][1],
                        fill="#FFFF00", width=3, tags="weather"
                    )
        elif self.type == "mist":
            canvas.create_oval(
                self.x, self.y,
                self.x + self.width, self.y + self.height,
                fill="#E6E6FA", outline="", tags="weather"
            )

class DynamicBackgroundManager:
    def __init__(self, canvas, app=None):
        self.canvas = canvas
        self.app = app
        self.width = canvas.winfo_width() or 800
        self.height = canvas.winfo_height() or 600
        self.particles = []
        self.is_running = False
        self.current_weather = "clear"
        self.fps = 30

        self.canvas.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height

    def set_weather(self, weather_condition):
        self.current_weather = weather_condition.lower()
        self.particles.clear()

        if any(x in self.current_weather for x in ["rain", "drizzle", "shower"]):
            for _ in range(max(50, self.width // 5)):
                self.particles.append(WeatherParticle(random.uniform(0, self.width), random.uniform(0, self.height), "rain", self.width, self.height))
        elif "snow" in self.current_weather:
            for _ in range(max(40, self.width // 10)):
                self.particles.append(WeatherParticle(random.uniform(0, self.width), random.uniform(0, self.height), "snow", self.width, self.height))
        elif any(x in self.current_weather for x in ["cloud", "overcast"]):
            for _ in range(max(5, self.width // 150)):
                self.particles.append(WeatherParticle(random.uniform(0, self.width), random.uniform(0, self.height//2), "cloud", self.width, self.height))
        elif any(x in self.current_weather for x in ["thunder", "storm"]):
            for _ in range(max(40, self.width // 5)):
                self.particles.append(WeatherParticle(random.uniform(0, self.width), random.uniform(0, self.height), "rain", self.width, self.height))
            for _ in range(max(5, self.width // 150)):
                self.particles.append(WeatherParticle(random.uniform(0, self.width), random.uniform(0, self.height//2), "cloud", self.width, self.height))
            for _ in range(2):
                self.particles.append(WeatherParticle(random.uniform(self.width*0.25, self.width*0.75), random.uniform(0, self.height//3), "lightning", self.width, self.height))
        elif any(x in self.current_weather for x in ["mist", "fog", "haze"]):
            for _ in range(max(10, self.width // 100)):
                self.particles.append(WeatherParticle(random.uniform(0, self.width), random.uniform(0, self.height), "mist", self.width, self.height))
        else:
            for _ in range(max(3, self.width // 200)):
                self.particles.append(WeatherParticle(random.uniform(0, self.width), random.uniform(0, self.height // 3), "cloud", self.width, self.height))

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.animate()

    def stop(self):
        self.is_running = False

    def animate(self):
        if not self.is_running:
            return

        try:
            self.canvas.delete("weather")
            for particle in self.particles:
                particle.update()
                particle.draw(self.canvas)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.stop()
            return  # Stop further animation on fatal error

        self.canvas.after(int(1000 / self.fps), self.animate)
