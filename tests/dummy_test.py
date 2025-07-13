import pytest
from core.app import WeatherApp  # adjust import to your actual app class location
from core.gui import draw_background
import customtkinter as ctk
from core.gui import SmartBackground


def test_draw_background(app):
    app = WeatherApp()
    canvas = app.smart_background.canvas
    if not canvas:
        print("No canvas to draw on yet")
        return

    width = canvas.winfo_width()
    height = canvas.winfo_height()
    if width <= 1 or height <= 1:
        print("Canvas size too small, retrying in 100ms")
        app.after(100, lambda: test_draw_background(app))
        return

    colors = ["#ff0000", "#0000ff"]  # Simple red to blue gradient
    steps = 50
    canvas.delete("background")
    for i in range(steps):
        ratio = i / steps
        r = int(255 * (1 - ratio))
        b = int(255 * ratio)
        color = f"#{r:02x}00{b:02x}"
        y1 = int(height * i / steps)
        y2 = int(height * (i + 1) / steps)
        canvas.create_rectangle(0, y1, width, y2, fill=color, outline="", tags="background")
    print("Test background drawn.")

def test_app():
    app = ctk.CTk()
    app.geometry("400x400")
    return app

def test_draw_background_runs_without_crash(test_app):
    draw_background(test_app)
    # Just checking that it runs; you could assert presence of canvas if exposed
    test_app.after(1000, test_app.destroy)
    test_app.mainloop()

def test_background_animator_runs():
    app = ctk.CTk()
    app.geometry("400x400")

    animator = BackgroundAnimator(app, "path/to/your.gif")
    animator.animate()

    app.after(1000, app.destroy)
    app.mainloop()

# Then call this after GUI is built:
app = ctk.CTk()
app.geometry("400x400")
app.after(1000, lambda: test_draw_background(app))
