import customtkinter as ctk

# ──────────────────────────────────────────────────────────────────────────────
# Draws a basic weather icon on the given canvas based on weather condition.
# ──────────────────────────────────────────────────────────────────────────────
def draw_weather_icon(canvas, condition):
    """
    Draws a canvas-based weather icon depending on the condition string.
    Supports conditions like 'sunny', 'rain', 'cloudy', 'snow', 'storm'.
    """
    clear_icon_canvas(canvas)
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    if condition == "sunny":
        # Draw sun (yellow circle with rays)
        canvas.create_oval(w*0.3, h*0.3, w*0.7, h*0.7, fill="yellow", outline="")
        for i in range(8):
            angle = i * 45
            canvas.create_line(w*0.5, h*0.5, w*0.5 + 30 * ctk.cos(angle), h*0.5 - 30 * ctk.sin(angle), fill="orange", width=2)

    elif condition == "rain":
        # Draw cloud and raindrops
        canvas.create_oval(w*0.3, h*0.4, w*0.7, h*0.6, fill="gray", outline="")
        for i in range(3):
            x = w*0.4 + i*20
            canvas.create_line(x, h*0.6, x, h*0.8, fill="blue", width=3)

    elif condition == "cloudy":
        # Draw clouds
        canvas.create_oval(w*0.3, h*0.4, w*0.7, h*0.6, fill="lightgray", outline="")
        canvas.create_oval(w*0.4, h*0.3, w*0.8, h*0.5, fill="lightgray", outline="")

    elif condition == "snow":
        # Draw snowflake (simple asterisk)
        x, y = w*0.5, h*0.5
        size = 20
        for angle in [0, 45, 90, 135]:
            canvas.create_line(x - size, y, x + size, y, fill="white", width=2)
            canvas.create_line(x, y - size, x, y + size, fill="white", width=2)
            canvas.create_line(x - size*0.7, y - size*0.7, x + size*0.7, y + size*0.7, fill="white", width=2)
            canvas.create_line(x - size*0.7, y + size*0.7, x + size*0.7, y - size*0.7, fill="white", width=2)

    elif condition == "storm":
        # Draw cloud and lightning bolt
        canvas.create_oval(w*0.3, h*0.4, w*0.7, h*0.6, fill="darkgray", outline="")
        points = [w*0.5, h*0.6, w*0.55, h*0.7, w*0.48, h*0.7, w*0.52, h*0.8]
        canvas.create_polygon(points, fill="yellow")

    else:
        # Default: question mark
        canvas.create_text(w*0.5, h*0.5, text="?", font=("Arial", 32), fill="red")

# ──────────────────────────────────────────────────────────────────────────────
# Clears all drawings from the icon canvas.
# ──────────────────────────────────────────────────────────────────────────────
def clear_icon_canvas(canvas):
    """
    Clears the canvas of any drawings.
    """
    canvas.delete("all")

# ──────────────────────────────────────────────────────────────────────────────
# Placeholder for simple animation of weather icons.
# ──────────────────────────────────────────────────────────────────────────────
def animate_weather_icon(canvas, condition):
    """
    Starts a simple animation on the weather icon canvas.
    (Example: blinking sun rays or raindrops falling)
    """
    # Implementation left as a future extension
    pass
