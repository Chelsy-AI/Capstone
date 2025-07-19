import customtkinter as ctk
import math

def draw_weather_icon(canvas, condition):
    """
    This function draws different weather icons on a canvas based on the condition.
    
    """
    
    canvas.delete("all")
    
    w = int(canvas.cget("width"))
    h = int(canvas.cget("height"))
    
    center_x, center_y = w // 2, h // 2
    
    if condition == "sunny":
        
        canvas.create_oval(center_x - 40, center_y - 40, center_x + 40, center_y + 40, 
                          fill="yellow", outline="")
        
        for angle in range(0, 360, 45):
            x_end = center_x + 60 * math.cos(angle * 3.1416 / 180)
            y_end = center_y + 60 * math.sin(angle * 3.1416 / 180)
            
            canvas.create_line(center_x, center_y, x_end, y_end, fill="orange", width=3)
    
    elif condition == "cloudy":
        canvas.create_oval(center_x - 50, center_y - 20, center_x + 20, center_y + 40, 
                          fill="lightgray", outline="")
        canvas.create_oval(center_x - 30, center_y - 40, center_x + 40, center_y + 20, 
                          fill="gray", outline="")
        canvas.create_oval(center_x - 10, center_y - 30, center_x + 60, center_y + 30, 
                          fill="darkgray", outline="")
    
    elif condition == "rainy":
        
        canvas.create_oval(center_x - 50, center_y - 40, center_x + 50, center_y + 10, 
                          fill="gray", outline="")
        
        for i in range(-30, 31, 20):
            canvas.create_line(center_x + i, center_y + 10, center_x + i - 5, center_y + 30, 
                              fill="blue", width=2)
    
    else:
        canvas.create_text(center_x, center_y, text="?", font=("Arial", 48), fill="red")

def update_weather_icon(canvas, condition):
    """
    This is a simple wrapper function that calls draw_weather_icon.
    It's useful if we want to add more functionality later (like animations).
    
    """
    draw_weather_icon(canvas, condition)

def create_metric_frame(parent, theme):
    """
    This function creates a frame that displays weather metrics like humidity, wind, etc.
    It creates a row of cards, each showing a different weather measurement.
    
    """
    
    frame = ctk.CTkFrame(parent, fg_color=theme["bg"])
    
    features = [
        ("humidity", "💧", "Humidity"),        # Water droplet for humidity
        ("wind", "💨", "Wind"),                # Wind gust for wind speed
        ("pressure", "🧭", "Pressure"),        # Compass for atmospheric pressure
        ("visibility", "👁️", "Visibility"),    # Eye for how far you can see
        ("uv", "🌞", "UV Index"),             # Sun for UV radiation level
        ("precipitation", "🌧️", "Precipitation"), # Rain cloud for rainfall
    ]
    
    frame.grid_columnconfigure(tuple(range(len(features))), weight=1, uniform="metrics")
    
    frame.metric_value_labels = {}
    
    for col, (key, icon, label_text) in enumerate(features):
        card = ctk.CTkFrame(frame, fg_color=theme["text_bg"], corner_radius=8)
        card.grid(row=0, column=col, padx=6, pady=5, sticky="nsew")
        
        ctk.CTkLabel(card, text=label_text, text_color=theme["text_fg"], 
                    font=("Arial", 14)).pack(pady=(5, 0))
        
        ctk.CTkLabel(card, text=icon, font=("Arial", 24)).pack()
        
        value_label = ctk.CTkLabel(card, text="--", text_color=theme["text_fg"], 
                                  font=("Arial", 16))
        value_label.pack(pady=(0, 5))
        
        frame.metric_value_labels[key] = value_label
    
    return frame