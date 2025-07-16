import tkinter as tk
import random

class SmartBackground:
    def __init__(self, canvas):
        self.canvas = canvas
        self.animation_running = False
        self.animation_id = None
        self.width = self.canvas.winfo_width() or 800
        self.height = self.canvas.winfo_height() or 600
        self.particles = []
        self.weather_condition = "rain"

    def start_animation(self):
        if self.animation_running:
            return
        self.animation_running = True
        self.width = self.canvas.winfo_width() or 800
        self.height = self.canvas.winfo_height() or 600
        self._init_particles()
        self._animate()

    def stop_animation(self):
        self.animation_running = False
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None
        self.canvas.delete("all")

    def _init_particles(self):
        self.particles.clear()
        count = 100
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            length = random.randint(10, 20)
            speed = random.uniform(4, 8)
            self.particles.append({"x": x, "y": y, "length": length, "speed": speed})

    def _animate(self):
        if not self.animation_running:
            return
        self.width = self.canvas.winfo_width() or 800
        self.height = self.canvas.winfo_height() or 600

        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#2f4f6f", outline="")
        for p in self.particles:
            x, y, length, speed = p["x"], p["y"], p["length"], p["speed"]
            self.canvas.create_line(x, y, x, y + length, fill="#a0c8ff", width=2)
            p["y"] += speed
            if p["y"] > self.height:
                p["y"] = random.randint(-20, 0)
                p["x"] = random.randint(0, self.width)
        self.animation_id = self.canvas.after(50, self._animate)

def main():
    root = tk.Tk()
    root.geometry("800x600")
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)
    canvas.lower()

    bg = SmartBackground(canvas)
    bg.start_animation()

    root.mainloop()

if __name__ == "__main__":
    main()
