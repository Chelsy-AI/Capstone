import random
import tkinter as tk

class SmartBackground:
    def __init__(self, app, canvas):
        self.app = app
        self.canvas = canvas
        self.animation_running = False
        self.animation_id = None
        self.weather_condition = "clear"
        self.width = self.canvas.winfo_width() or 800
        self.height = self.canvas.winfo_height() or 600

        # Particles list: each is dict with x, y, length, speed for raindrops or snowflakes
        self.particles = []

    def start_animation(self, weather_condition):
        print("[DEBUG] Animation started")
        self.weather_condition = weather_condition
        if self.animation_running:
            return
        self.animation_running = True

        # Update size in case window resized
        self.width = self.canvas.winfo_width() or 800
        self.height = self.canvas.winfo_height() or 600

        self._init_particles()
        self._animate()

    def stop_animation(self):
        self.animation_running = False
        if self.animation_id is not None:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None
        try:
            self.canvas.delete("all")
        except Exception:
            pass

    def update_background(self, weather_condition):
        self.weather_condition = weather_condition
        self.width = self.canvas.winfo_width() or 800
        self.height = self.canvas.winfo_height() or 600
        self._init_particles()

    def _init_particles(self):
        self.particles.clear()
        if self.weather_condition == "rain":
            count = 100
            for _ in range(count):
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                length = random.randint(10, 20)
                speed = random.uniform(4, 8)
                self.particles.append({"x": x, "y": y, "length": length, "speed": speed})
        elif self.weather_condition == "snow":
            count = 80
            for _ in range(count):
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                size = random.randint(2, 5)
                speed = random.uniform(1, 3)
                self.particles.append({"x": x, "y": y, "size": size, "speed": speed})
        else:
            # For clear or default, no particles
            self.particles = []

    def _animate(self):
        if not self.animation_running:
            return

        self.canvas.delete("all")

        # Draw background base color
        if self.weather_condition == "rain":
            self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#2f4f6f", outline="")
            self._draw_rain()
        elif self.weather_condition == "snow":
            self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#a0c8f0", outline="")
            self._draw_snow()
        elif self.weather_condition == "sun":
            self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#f9d71c", outline="")
            self._draw_sun()
        else:
            self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#444444", outline="")

        # Schedule next frame
        self.animation_id = self.canvas.after(50, self._animate)

    def _draw_rain(self):
        for p in self.particles:
            x = p["x"]
            y = p["y"]
            length = p["length"]
            speed = p["speed"]

            # Draw raindrop as a blue line
            self.canvas.create_line(x, y, x, y + length, fill="#a0c8ff", width=2)

            # Move particle down by speed
            p["y"] += speed
            if p["y"] > self.height:
                p["y"] = random.randint(-20, 0)
                p["x"] = random.randint(0, self.width)

    def _draw_snow(self):
        for p in self.particles:
            x = p["x"]
            y = p["y"]
            size = p["size"]
            speed = p["speed"]

            # Draw snowflake as white oval
            self.canvas.create_oval(x, y, x + size, y + size, fill="white", outline="")

            # Move particle down by speed
            p["y"] += speed
            if p["y"] > self.height:
                p["y"] = random.randint(-20, 0)
                p["x"] = random.randint(0, self.width)

    def _draw_sun(self):
        # Just draw a static sun in top right corner for demo
        r = 50
        cx = self.width - r - 20
        cy = r + 20
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#f9d71c", outline="")
        # You can add rays or animation if you want
