"""
Animated Weather Icon System
===========================

Dynamic weather visualization system that creates beautiful animated icons matching current conditions.

Features:
- Hand-drawn weather icons using canvas graphics
- Multiple weather condition support (sunny, rainy, cloudy, snowy, stormy)
- Custom geometric shapes and artistic elements
- Real-time icon updates based on weather changes
- Canvas clearing and redraw functionality
- Extensible design for future animation features
- Fallback displays for unknown weather conditions

The system creates visually appealing weather representations using
mathematical drawing functions for crisp, scalable graphics.
"""

from .canvas_icons import draw_weather_icon

__all__ = [
    "draw_weather_icon",
    "animate_weather_icon", 
    "clear_icon_canvas",
]

import customtkinter as ctk

# Main function that draws weather icons on a canvas based on weather conditions

def draw_weather_icon(canvas, condition):
    """
    Creates visual weather icons by drawing shapes on a canvas.
    Takes a canvas widget and a weather condition string.

    """
    
    clear_icon_canvas(canvas)
    
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    if condition == "sunny":
        canvas.create_oval(w*0.3, h*0.3, w*0.7, h*0.7, fill="yellow", outline="")
        
        for i in range(8):
            angle = i * 45
            canvas.create_line(w*0.5, h*0.5, w*0.5 + 30 * ctk.cos(angle), h*0.5 - 30 * ctk.sin(angle), fill="orange", width=2)

    elif condition == "rain":
        canvas.create_oval(w*0.3, h*0.4, w*0.7, h*0.6, fill="gray", outline="")
        
        for i in range(3):
            x = w*0.4 + i*20
            canvas.create_line(x, h*0.6, x, h*0.8, fill="blue", width=3)

    elif condition == "cloudy":
        canvas.create_oval(w*0.3, h*0.4, w*0.7, h*0.6, fill="lightgray", outline="")
        canvas.create_oval(w*0.4, h*0.3, w*0.8, h*0.5, fill="lightgray", outline="")

    elif condition == "snow":
        x, y = w*0.5, h*0.5
        size = 20
        
        for angle in [0, 45, 90, 135]:
            canvas.create_line(x - size, y, x + size, y, fill="white", width=2)
            canvas.create_line(x, y - size, x, y + size, fill="white", width=2)
            canvas.create_line(x - size*0.7, y - size*0.7, x + size*0.7, y + size*0.7, fill="white", width=2)
            canvas.create_line(x - size*0.7, y + size*0.7, x + size*0.7, y - size*0.7, fill="white", width=2)

    elif condition == "storm":
        canvas.create_oval(w*0.3, h*0.4, w*0.7, h*0.6, fill="darkgray", outline="")
        
        points = [w*0.5, h*0.6, w*0.55, h*0.7, w*0.48, h*0.7, w*0.52, h*0.8]
        canvas.create_polygon(points, fill="yellow")

    else:
        canvas.create_text(w*0.5, h*0.5, text="?", font=("Arial", 32), fill="red")

# Utility function to clear all drawings from the canvas

def clear_icon_canvas(canvas):
    """
    Removes all drawings from the canvas to prepare for new icon.
    This prevents icons from overlapping when conditions change.

    """
    canvas.delete("all")

# Placeholder function for future animation features
def animate_weather_icon(canvas, condition):
    """
    Future function to add animations to weather icons.
    Could include features like:
    - Blinking sun rays
    - Falling raindrops
    - Moving clouds
    - Sparkling snow
    
    """
    pass