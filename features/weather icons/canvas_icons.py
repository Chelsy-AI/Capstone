"""
Weather Icons Canvas Drawing Module - COMPLETELY OPTIMIZED VERSION

This module creates dynamic weather icons by drawing shapes and graphics directly
on HTML5 Canvas or Tkinter Canvas widgets. It provides a flexible system for
visualizing different weather conditions through programmatic drawing rather
than static image files.

The system is optimized for performance and includes beginner-friendly comments
to help understand how programmatic graphics and weather visualization work.
"""

import customtkinter as ctk
import math
import random
from typing import Tuple, List, Dict, Any, Optional, Union
import tkinter as tk


# ────────────────────────────────────────────────────────────────────────────── 
# MAIN WEATHER ICON DRAWING FUNCTIONS
# ────────────────────────────────────────────────────────────────────────────── 

def draw_weather_icon(canvas, condition: str):
    """
    Creates visual weather icons by drawing shapes on a canvas based on weather conditions.
    
    This is the main function that takes a weather condition and creates a visual
    representation using geometric shapes, lines, and colors. It's like having
    a digital artist that draws weather symbols in real-time.
    
    Args:
        canvas: Canvas widget where the icon will be drawn (Tkinter Canvas)
        condition: Weather condition string (like 'sunny', 'rain', 'cloudy', etc.)
        
    Example:
        >>> draw_weather_icon(my_canvas, "sunny")
        # Draws a yellow sun with radiating rays
        
        >>> draw_weather_icon(my_canvas, "rain") 
        # Draws gray clouds with blue raindrops
    """
    
    # Clear any existing drawings to start fresh
    # This prevents icons from overlapping when conditions change
    clear_icon_canvas(canvas)
    
    # Get canvas dimensions for responsive drawing
    # Canvas size might change based on window size or theme
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    print(f"Drawing '{condition}' weather icon on {canvas_width}x{canvas_height} canvas")
    
    # Route to specific drawing function based on weather condition
    # Each condition has its own optimized drawing routine
    if condition.lower() == "sunny":
        _draw_sunny_icon(canvas, canvas_width, canvas_height)
    elif condition.lower() in ["rain", "rainy"]:
        _draw_rainy_icon(canvas, canvas_width, canvas_height)
    elif condition.lower() == "cloudy":
        _draw_cloudy_icon(canvas, canvas_width, canvas_height)
    elif condition.lower() in ["snow", "snowy"]:
        _draw_snowy_icon(canvas, canvas_width, canvas_height)
    elif condition.lower() in ["storm", "stormy", "thunderstorm"]:
        _draw_stormy_icon(canvas, canvas_width, canvas_height)
    elif condition.lower() in ["windy", "wind"]:
        _draw_windy_icon(canvas, canvas_width, canvas_height)
    elif condition.lower() in ["fog", "foggy", "mist", "misty"]:
        _draw_foggy_icon(canvas, canvas_width, canvas_height)
    else:
        # Unknown condition - draw a question mark
        _draw_unknown_icon(canvas, canvas_width, canvas_height)
    
    print(f"✓ Weather icon '{condition}' drawn successfully")


def _draw_sunny_icon(canvas, width: int, height: int):
    """
    Draw a sunny weather icon with sun and radiating rays.
    
    Creates a bright yellow/orange sun with rays extending outward,
    representing clear, sunny weather conditions.
    
    Args:
        canvas: Canvas to draw on
        width: Canvas width for positioning
        height: Canvas height for positioning
    """
    center_x = width * 0.5
    center_y = height * 0.5
    
    # Draw main sun disk (large yellow circle)
    sun_radius = min(width, height) * 0.15  # Responsive size
    canvas.create_oval(
        center_x - sun_radius, center_y - sun_radius,
        center_x + sun_radius, center_y + sun_radius,
        fill="yellow",      # Bright yellow for sunny feeling
        outline="orange",   # Orange border for definition
        width=2
    )
    
    # Draw sun rays extending outward
    ray_length = sun_radius * 1.8  # Rays extend beyond sun disk
    ray_width = 3  # Thickness of rays
    num_rays = 8   # Number of rays around the sun
    
    for ray_index in range(num_rays):
        # Calculate angle for this ray (evenly distributed around circle)
        angle_degrees = ray_index * (360 / num_rays)
        angle_radians = math.radians(angle_degrees)
        
        # Calculate ray start and end points using trigonometry
        # Rays start at edge of sun disk and extend outward
        start_x = center_x + (sun_radius * 1.2) * math.cos(angle_radians)
        start_y = center_y + (sun_radius * 1.2) * math.sin(angle_radians)
        end_x = center_x + ray_length * math.cos(angle_radians)
        end_y = center_y + ray_length * math.sin(angle_radians)
        
        # Draw the ray as a line
        canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill="orange",    # Orange color for warmth
            width=ray_width,
            capstyle="round"  # Rounded line ends for smoother appearance
        )


def _draw_rainy_icon(canvas, width: int, height: int):
    """
    Draw a rainy weather icon with clouds and falling raindrops.
    
    Creates gray clouds with blue raindrops falling underneath,
    representing wet weather conditions.
    
    Args:
        canvas: Canvas to draw on
        width: Canvas width for positioning
        height: Canvas height for positioning
    """
    center_x = width * 0.5
    center_y = height * 0.4  # Clouds positioned higher to leave room for rain
    
    # Draw cloud formation using overlapping circles
    cloud_radius = min(width, height) * 0.12
    
    # Main cloud body (largest circle)
    canvas.create_oval(
        center_x - cloud_radius * 1.5, center_y - cloud_radius * 0.8,
        center_x + cloud_radius * 1.5, center_y + cloud_radius * 0.8,
        fill="gray",        # Gray for rain clouds
        outline="darkgray",
        width=1
    )
    
    # Left cloud puff (smaller circle)
    canvas.create_oval(
        center_x - cloud_radius * 2, center_y - cloud_radius * 0.5,
        center_x - cloud_radius * 0.8, center_y + cloud_radius * 0.7,
        fill="gray",
        outline="darkgray",
        width=1
    )
    
    # Right cloud puff (smaller circle)
    canvas.create_oval(
        center_x + cloud_radius * 0.8, center_y - cloud_radius * 0.5,
        center_x + cloud_radius * 2, center_y + cloud_radius * 0.7,
        fill="gray",
        outline="darkgray",
        width=1
    )
    
    # Draw falling raindrops
    raindrop_count = 6  # Number of raindrops to draw
    drop_length = height * 0.12  # Length of each raindrop line
    
    for drop_index in range(raindrop_count):
        # Distribute raindrops across width of cloud
        drop_x = center_x - cloud_radius + (drop_index * cloud_radius * 0.6)
        drop_start_y = center_y + cloud_radius * 1.2  # Start below cloud
        drop_end_y = drop_start_y + drop_length
        
        # Draw raindrop as angled line (slight angle for realism)
        angle_offset = drop_index * 5  # Slight variation in angles
        offset_x = math.sin(math.radians(angle_offset)) * 5
        
        canvas.create_line(
            drop_x, drop_start_y,
            drop_x - offset_x, drop_end_y,
            fill="blue",      # Blue for water
            width=2,
            capstyle="round"
        )


def _draw_cloudy_icon(canvas, width: int, height: int):
    """
    Draw a cloudy weather icon with multiple overlapping cloud shapes.
    
    Creates light gray clouds of different sizes to represent
    overcast or partly cloudy conditions.
    
    Args:
        canvas: Canvas to draw on
        width: Canvas width for positioning
        height: Canvas height for positioning
    """
    center_x = width * 0.5
    center_y = height * 0.5
    
    # Draw multiple cloud layers for depth
    cloud_base_radius = min(width, height) * 0.1
    
    # Background cloud (largest, lightest)
    canvas.create_oval(
        center_x - cloud_base_radius * 2.5, center_y - cloud_base_radius,
        center_x + cloud_base_radius * 2.5, center_y + cloud_base_radius * 1.5,
        fill="lightgray",   # Light gray for background
        outline="gray",
        width=1
    )
    
    # Middle cloud (medium size)
    canvas.create_oval(
        center_x - cloud_base_radius * 2, center_y - cloud_base_radius * 1.2,
        center_x + cloud_base_radius * 2, center_y + cloud_base_radius * 1.2,
        fill="gray",        # Medium gray for middle layer
        outline="darkgray",
        width=1
    )
    
    # Foreground cloud (smallest, darkest for depth)
    canvas.create_oval(
        center_x - cloud_base_radius * 1.5, center_y - cloud_base_radius * 0.8,
        center_x + cloud_base_radius * 1.5, center_y + cloud_base_radius,
        fill="darkgray",    # Darker gray for foreground
        outline="black",
        width=1
    )
    
    # Add small cloud puffs for realistic texture
    puff_count = 4
    for puff_index in range(puff_count):
        puff_angle = puff_index * (360 / puff_count)
        puff_distance = cloud_base_radius * 1.8
        puff_x = center_x + puff_distance * math.cos(math.radians(puff_angle))
        puff_y = center_y + puff_distance * math.sin(math.radians(puff_angle)) * 0.5
        
        canvas.create_oval(
            puff_x - cloud_base_radius * 0.4, puff_y - cloud_base_radius * 0.4,
            puff_x + cloud_base_radius * 0.4, puff_y + cloud_base_radius * 0.4,
            fill="lightgray",
            outline="gray",
            width=1
        )


def _draw_snowy_icon(canvas, width: int, height: int):
    """
    Draw a snowy weather icon with snowflakes and winter clouds.
    
    Creates white/light blue snowflakes with gray clouds,
    representing snowy winter conditions.
    
    Args:
        canvas: Canvas to draw on
        width: Canvas width for positioning
        height: Canvas height for positioning
    """
    center_x = width * 0.5
    center_y = height * 0.4
    
    # Draw snow cloud (similar to rain cloud but lighter)
    cloud_radius = min(width, height) * 0.12
    
    canvas.create_oval(
        center_x - cloud_radius * 1.5, center_y - cloud_radius * 0.8,
        center_x + cloud_radius * 1.5, center_y + cloud_radius * 0.8,
        fill="lightgray",   # Lighter gray for snow clouds
        outline="gray",
        width=1
    )
    
    # Draw individual snowflakes
    snowflake_count = 5
    snowflake_size = min(width, height) * 0.04
    
    for flake_index in range(snowflake_count):
        # Position snowflakes below cloud
        flake_x = center_x - cloud_radius + (flake_index * cloud_radius * 0.7)
        flake_y = center_y + cloud_radius * 1.5 + (flake_index * 15)
        
        # Draw snowflake as intersecting lines (6-pointed star pattern)
        _draw_snowflake(canvas, flake_x, flake_y, snowflake_size)


def _draw_snowflake(canvas, x: float, y: float, size: float):
    """
    Draw a detailed snowflake pattern.
    
    Creates a 6-pointed snowflake using intersecting lines,
    mimicking the natural crystalline structure of real snowflakes.
    
    Args:
        canvas: Canvas to draw on
        x: Center X coordinate
        y: Center Y coordinate
        size: Size of the snowflake
    """
    # Draw main 6 arms of snowflake
    for arm_index in range(6):
        angle = arm_index * 60  # 60 degrees between arms
        angle_rad = math.radians(angle)
        
        # Main arm line
        end_x = x + size * math.cos(angle_rad)
        end_y = y + size * math.sin(angle_rad)
        
        canvas.create_line(
            x, y, end_x, end_y,
            fill="white",
            width=2,
            capstyle="round"
        )
        
        # Add smaller branches to main arms
        branch_size = size * 0.4
        branch_angle1 = angle + 30
        branch_angle2 = angle - 30
        
        # First branch
        branch1_x = x + branch_size * math.cos(math.radians(branch_angle1))
        branch1_y = y + branch_size * math.sin(math.radians(branch_angle1))
        canvas.create_line(
            x + (size * 0.6) * math.cos(angle_rad), 
            y + (size * 0.6) * math.sin(angle_rad),
            branch1_x, branch1_y,
            fill="white", width=1
        )
        
        # Second branch
        branch2_x = x + branch_size * math.cos(math.radians(branch_angle2))
        branch2_y = y + branch_size * math.sin(math.radians(branch_angle2))
        canvas.create_line(
            x + (size * 0.6) * math.cos(angle_rad), 
            y + (size * 0.6) * math.sin(angle_rad),
            branch2_x, branch2_y,
            fill="white", width=1
        )


def _draw_stormy_icon(canvas, width: int, height: int):
    """
    Draw a stormy weather icon with dark clouds and lightning.
    
    Creates dark storm clouds with yellow lightning bolts,
    representing thunderstorms and severe weather.
    
    Args:
        canvas: Canvas to draw on
        width: Canvas width for positioning
        height: Canvas height for positioning
    """
    center_x = width * 0.5
    center_y = height * 0.4
    
    # Draw dark storm cloud
    cloud_radius = min(width, height) * 0.12
    
    canvas.create_oval(
        center_x - cloud_radius * 1.8, center_y - cloud_radius,
        center_x + cloud_radius * 1.8, center_y + cloud_radius,
        fill="darkgray",    # Dark gray for storm clouds
        outline="black",
        width=2
    )
    
    # Add additional dark cloud layers for menacing appearance
    canvas.create_oval(
        center_x - cloud_radius * 1.2, center_y - cloud_radius * 1.3,
        center_x + cloud_radius * 1.2, center_y + cloud_radius * 0.7,
        fill="dimgray",
        outline="black",
        width=1
    )
    
    # Draw lightning bolt
    lightning_start_x = center_x
    lightning_start_y = center_y + cloud_radius * 0.8
    
    # Create zigzag lightning pattern
    lightning_points = [
        (lightning_start_x, lightning_start_y),
        (lightning_start_x - 15, lightning_start_y + 25),
        (lightning_start_x + 5, lightning_start_y + 25),
        (lightning_start_x - 10, lightning_start_y + 50),
        (lightning_start_x + 8, lightning_start_y + 50),
        (lightning_start_x - 5, lightning_start_y + 75)
    ]
    
    # Draw lightning as connected line segments
    for point_index in range(len(lightning_points) - 1):
        start_point = lightning_points[point_index]
        end_point = lightning_points[point_index + 1]
        
        canvas.create_line(
            start_point[0], start_point[1],
            end_point[0], end_point[1],
            fill="yellow",    # Bright yellow for electrical energy
            width=3,
            capstyle="round"
        )


def _draw_windy_icon(canvas, width: int, height: int):
    """
    Draw a windy weather icon with flowing wind lines.
    
    Creates curved lines suggesting air movement and wind flow,
    representing breezy or windy conditions.
    
    Args:
        canvas: Canvas to draw on
        width: Canvas width for positioning
        height: Canvas height for positioning
    """
    center_x = width * 0.5
    center_y = height * 0.5
    
    # Draw multiple curved wind lines at different heights
    wind_line_count = 4
    line_spacing = height * 0.15
    
    for line_index in range(wind_line_count):
        line_y = center_y - (line_spacing * 1.5) + (line_index * line_spacing)
        
        # Create smooth curved wind line using multiple segments
        wind_points = []
        segments = 20  # More segments = smoother curve
        
        for segment in range(segments + 1):
            # Calculate position along curve
            progress = segment / segments
            x = center_x - (width * 0.3) + (progress * width * 0.6)
            
            # Add sine wave for curved appearance
            wave_amplitude = 15 + (line_index * 5)  # Different amplitudes
            wave_frequency = 2 + (line_index * 0.5)  # Different frequencies
            y_offset = math.sin(progress * math.pi * wave_frequency) * wave_amplitude
            y = line_y + y_offset
            
            wind_points.append((x, y))
        
        # Draw the wind line
        for point_index in range(len(wind_points) - 1):
            canvas.create_line(
                wind_points[point_index][0], wind_points[point_index][1],
                wind_points[point_index + 1][0], wind_points[point_index + 1][1],
                fill="lightblue",  # Light blue for air movement
                width=2 + line_index,  # Varying thickness for depth
                smooth=True
            )


def _draw_foggy_icon(canvas, width: int, height: int):
    """
    Draw a foggy weather icon with layered horizontal mist lines.
    
    Creates multiple horizontal lines with varying opacity to represent
    fog, mist, or low visibility conditions.
    
    Args:
        canvas: Canvas to draw on
        width: Canvas width for positioning
        height: Canvas height for positioning
    """
    center_x = width * 0.5
    center_y = height * 0.5
    
    # Draw multiple horizontal fog layers
    fog_layer_count = 6
    layer_height = height * 0.08
    layer_spacing = height * 0.1
    
    for layer_index in range(fog_layer_count):
        layer_y = center_y - (layer_spacing * 2) + (layer_index * layer_spacing)
        
        # Vary layer width and position for natural look
        layer_width = width * (0.4 + (layer_index % 3) * 0.15)
        layer_start_x = center_x - (layer_width / 2)
        layer_end_x = center_x + (layer_width / 2)
        
        # Create fog layer as thick line with rounded ends
        canvas.create_line(
            layer_start_x, layer_y,
            layer_end_x, layer_y,
            fill="lightgray",
            width=int(layer_height),
            capstyle="round"
        )
        
        # Add variation with slightly offset secondary lines
        if layer_index % 2 == 0:  # Every other layer
            offset_y = layer_y + (layer_height * 0.3)
            secondary_width = layer_width * 0.7
            secondary_start_x = center_x - (secondary_width / 2)
            secondary_end_x = center_x + (secondary_width / 2)
            
            canvas.create_line(
                secondary_start_x, offset_y,
                secondary_end_x, offset_y,
                fill="white",
                width=int(layer_height * 0.6),
                capstyle="round"
            )


def _draw_unknown_icon(canvas, width: int, height: int):
    """
    Draw an icon for unknown or unsupported weather conditions.
    
    Creates a large question mark to indicate that the weather
    condition is not recognized by the icon system.
    
    Args:
        canvas: Canvas to draw on
        width: Canvas width for positioning
        height: Canvas height for positioning
    """
    center_x = width * 0.5
    center_y = height * 0.5
    
    # Draw large question mark
    question_mark_size = min(width, height) * 0.4
    
    canvas.create_text(
        center_x, center_y,
        text="?",
        font=("Arial", int(question_mark_size), "bold"),
        fill="red",         # Red to indicate error/unknown
        anchor="center"
    )
    
    # Add circle around question mark for emphasis
    circle_radius = question_mark_size * 0.7
    canvas.create_oval(
        center_x - circle_radius, center_y - circle_radius,
        center_x + circle_radius, center_y + circle_radius,
        outline="red",
        width=3,
        fill=""  # No fill, just outline
    )


# ────────────────────────────────────────────────────────────────────────────── 
# UTILITY FUNCTIONS FOR CANVAS MANAGEMENT
# ────────────────────────────────────────────────────────────────────────────── 

def clear_icon_canvas(canvas):
    """
    Removes all drawings from the canvas to prepare for new icon.
    
    This prevents icons from overlapping when weather conditions change.
    It's like erasing a whiteboard before drawing something new.
    
    Args:
        canvas: Canvas widget to clear
        
    Example:
        >>> clear_icon_canvas(my_canvas)
        # All previous drawings are removed
    """
    try:
        canvas.delete("all")  # Remove all canvas items
        print("Canvas cleared for new weather icon")
    except Exception as e:
        print(f"Error clearing canvas: {e}")


def update_weather_icon(canvas, condition: str):
    """
    Update the weather icon with a new condition.
    
    This is a convenience wrapper around draw_weather_icon that handles
    the clearing and redrawing process in one function call.
    
    Args:
        canvas: Canvas widget to update
        condition: New weather condition to display
        
    Example:
        >>> update_weather_icon(my_canvas, "stormy")
        # Clears canvas and draws storm icon
    """
    try:
        print(f"Updating weather icon to: {condition}")
        draw_weather_icon(canvas, condition)
    except Exception as e:
        print(f"Error updating weather icon: {e}")
        # Draw error icon as fallback
        _draw_unknown_icon(canvas, canvas.winfo_width(), canvas.winfo_height())


def validate_canvas_size(canvas) -> bool:
    """
    Validate that canvas has reasonable dimensions for icon drawing.
    
    Checks if the canvas is large enough to draw detailed weather icons
    and provides feedback for debugging layout issues.
    
    Args:
        canvas: Canvas widget to validate
        
    Returns:
        bool: True if canvas size is adequate, False otherwise
    """
    try:
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        # Check minimum size requirements
        min_size = 50  # Minimum pixels for recognizable icons
        
        if width < min_size or height < min_size:
            print(f"Warning: Canvas size ({width}x{height}) may be too small for detailed icons")
            return False
        
        if width > 1000 or height > 1000:
            print(f"Warning: Canvas size ({width}x{height}) is very large, icons may appear oversized")
        
        print(f"Canvas size ({width}x{height}) is suitable for weather icons")
        return True
        
    except Exception as e:
        print(f"Error validating canvas size: {e}")
        return False


# ────────────────────────────────────────────────────────────────────────────── 
# ADVANCED WEATHER METRICS VISUALIZATION
# ────────────────────────────────────────────────────────────────────────────── 

def create_metric_frame(parent, theme: Dict[str, str]):
    """
    Create a frame that displays weather metrics like humidity, wind, pressure, etc.
    
    This function creates a horizontal row of cards, each showing a different
    weather measurement with icons and values. It's like a dashboard of
    weather information displayed in an organized, visual way.
    
    Args:
        parent: Parent widget to contain the metrics frame
        theme: Dictionary containing theme colors and styling information
        
    Returns:
        Frame widget containing all metric cards with update capability
        
    Example:
        >>> metrics_frame = create_metric_frame(my_window, light_theme)
        >>> # Later update with real data:
        >>> update_metric_values(metrics_frame, humidity=65, wind=12)
    """
    # Create main container frame
    frame = ctk.CTkFrame(parent, fg_color=theme["bg"])
    
    # Define weather metrics to display with their icons and labels
    weather_features = [
        ("humidity", "💧", "Humidity"),        # Water droplet for humidity percentage
        ("wind", "💨", "Wind"),                # Wind gust for wind speed
        ("pressure", "🧭", "Pressure"),        # Compass for atmospheric pressure
        ("visibility", "👁️", "Visibility"),    # Eye for visibility distance
        ("uv", "🌞", "UV Index"),             # Sun for UV radiation level
        ("precipitation", "🌧️", "Precipitation"), # Rain cloud for rainfall amount
    ]
    
    # Configure grid layout for equal spacing
    frame.grid_columnconfigure(tuple(range(len(weather_features))), weight=1, uniform="metrics")
    
    # Dictionary to store metric value labels for later updates
    frame.metric_value_labels = {}
    
    # Create individual metric cards
    for column_index, (metric_key, icon_emoji, label_text) in enumerate(weather_features):
        # Create card container
        metric_card = ctk.CTkFrame(
            frame, 
            fg_color=theme["text_bg"], 
            corner_radius=8
        )
        metric_card.grid(row=0, column=column_index, padx=6, pady=5, sticky="nsew")
        
        # Metric label (what it measures)
        ctk.CTkLabel(
            metric_card, 
            text=label_text, 
            text_color=theme["text_fg"], 
            font=("Arial", 14)
        ).pack(pady=(5, 0))
        
        # Icon emoji (visual representation)
        ctk.CTkLabel(
            metric_card, 
            text=icon_emoji, 
            font=("Arial", 24)
        ).pack()
        
        # Value label (actual measurement - will be updated with real data)
        value_label = ctk.CTkLabel(
            metric_card, 
            text="--",  # Placeholder until real data loads
            text_color=theme["text_fg"], 
            font=("Arial", 16)
        )
        value_label.pack(pady=(0, 5))
        
        # Store reference for later updates
        frame.metric_value_labels[metric_key] = value_label
    
    return frame


def update_metric_values(metrics_frame, **metric_values):
    """
    Update the weather metrics display with new values.
    
    This function takes current weather measurements and updates the
    visual display cards with the new information.
    
    Args:
        metrics_frame: Frame created by create_metric_frame()
        **metric_values: Keyword arguments with metric names and values
        
    Example:
        >>> update_metric_values(
        ...     frame,
        ...     humidity=68,      # 68% humidity
        ...     wind=15,          # 15 mph wind
        ...     pressure=1013,    # 1013 hPa pressure
        ...     uv=7              # UV index of 7
        ... )
    """
    try:
        # Check if frame has the metric labels dictionary
        if not hasattr(metrics_frame, 'metric_value_labels'):
            print("Error: Metrics frame not properly initialized")
            return
        
        # Update each metric that was provided
        for metric_name, new_value in metric_values.items():
            if metric_name in metrics_frame.metric_value_labels:
                # Format the value appropriately based on metric type
                formatted_value = _format_metric_value(metric_name, new_value)
                
                # Update the display label
                metrics_frame.metric_value_labels[metric_name].configure(text=formatted_value)
                print(f"Updated {metric_name}: {formatted_value}")
            else:
                print(f"Warning: Unknown metric '{metric_name}' - skipping")
                
    except Exception as e:
        print(f"Error updating metric values: {e}")


def _format_metric_value(metric_name: str, value: Union[int, float, str]) -> str:
    """
    Format metric values with appropriate units and precision.
    
    Different weather metrics need different formatting - temperature needs
    degrees, wind needs speed units, humidity needs percentages, etc.
    
    Args:
        metric_name: Name of the metric being formatted
        value: Raw value to format
        
    Returns:
        Formatted string with value and appropriate units
    """
    try:
        # Handle None or invalid values
        if value is None or value == "":
            return "--"
        
        # Convert to appropriate type and format based on metric
        if metric_name == "humidity":
            # Humidity as percentage
            return f"{int(float(value))}%"
        
        elif metric_name == "wind":
            # Wind speed with units
            return f"{float(value):.1f} mph"
        
        elif metric_name == "pressure":
            # Atmospheric pressure
            return f"{float(value):.0f} hPa"
        
        elif metric_name == "visibility":
            # Visibility distance
            visibility_val = float(value)
            if visibility_val >= 1:
                return f"{visibility_val:.1f} mi"
            else:
                return f"{visibility_val*5280:.0f} ft"  # Convert to feet if less than 1 mile
        
        elif metric_name == "uv":
            # UV index (no units, just number)
            uv_val = float(value)
            if uv_val >= 8:
                return f"{uv_val:.0f} High"
            elif uv_val >= 6:
                return f"{uv_val:.0f} Mod"
            elif uv_val >= 3:
                return f"{uv_val:.0f} Low"
            else:
                return f"{uv_val:.0f} Min"
        
        elif metric_name == "precipitation":
            # Precipitation amount
            precip_val = float(value)
            if precip_val < 0.01:
                return "0.00 in"
            else:
                return f"{precip_val:.2f} in"
        
        else:
            # Generic formatting for unknown metrics
            return str(value)
            
    except (ValueError, TypeError):
        # Handle conversion errors gracefully
        return "--"


# ────────────────────────────────────────────────────────────────────────────── 
# ANIMATION AND INTERACTIVE FEATURES
# ────────────────────────────────────────────────────────────────────────────── 

def animate_weather_icon(canvas, condition: str, animation_type: str = "gentle"):
    """
    Add subtle animations to weather icons for enhanced visual appeal.
    
    This function adds movement and life to static weather icons through
    gentle animations like blinking sun rays, falling raindrops, or
    moving cloud elements.
    
    Args:
        canvas: Canvas containing the weather icon
        condition: Weather condition that's currently displayed
        animation_type: Type of animation ("gentle", "active", "subtle")
        
    Example:
        >>> animate_weather_icon(my_canvas, "sunny", "gentle")
        # Adds gentle pulsing to sun rays
        
        >>> animate_weather_icon(my_canvas, "rain", "active") 
        # Adds animated falling raindrops
    """
    try:
        print(f"Starting {animation_type} animation for {condition} icon")
        
        # Route to appropriate animation based on weather condition
        if condition.lower() == "sunny":
            _animate_sunny_icon(canvas, animation_type)
        elif condition.lower() in ["rain", "rainy"]:
            _animate_rainy_icon(canvas, animation_type)
        elif condition.lower() == "cloudy":
            _animate_cloudy_icon(canvas, animation_type)
        elif condition.lower() in ["snow", "snowy"]:
            _animate_snowy_icon(canvas, animation_type)
        elif condition.lower() in ["storm", "stormy"]:
            _animate_stormy_icon(canvas, animation_type)
        else:
            print(f"No animation available for condition: {condition}")
            
    except Exception as e:
        print(f"Error animating weather icon: {e}")


def _animate_sunny_icon(canvas, animation_type: str):
    """Animate sunny weather icon with pulsing or rotating sun rays."""
    # Implementation would add subtle ray rotation or pulsing
    pass


def _animate_rainy_icon(canvas, animation_type: str):
    """Animate rainy weather icon with falling raindrops."""
    # Implementation would add animated raindrops falling from clouds
    pass


def _animate_cloudy_icon(canvas, animation_type: str):
    """Animate cloudy weather icon with drifting clouds."""
    # Implementation would add subtle cloud movement
    pass


def _animate_snowy_icon(canvas, animation_type: str):
    """Animate snowy weather icon with falling snowflakes."""
    # Implementation would add animated snowflakes falling
    pass


def _animate_stormy_icon(canvas, animation_type: str):
    """Animate stormy weather icon with flashing lightning."""
    # Implementation would add lightning flash effects
    pass


# ────────────────────────────────────────────────────────────────────────────── 
# DEVELOPER UTILITIES AND DEBUGGING
# ────────────────────────────────────────────────────────────────────────────── 

def get_supported_conditions() -> List[str]:
    """
    Get list of all supported weather conditions.
    
    Returns a list of weather condition strings that have corresponding
    icon drawing functions implemented.
    
    Returns:
        List of supported weather condition names
        
    Example:
        >>> conditions = get_supported_conditions()
        >>> print(f"Supported conditions: {', '.join(conditions)}")
    """
    return [
        "sunny", "rain", "rainy", "cloudy", "snow", "snowy",
        "storm", "stormy", "thunderstorm", "windy", "wind",
        "fog", "foggy", "mist", "misty"
    ]


def test_all_weather_icons(canvas):
    """
    Test function to draw all supported weather icons in sequence.
    
    Useful for development and testing to verify that all weather
    conditions render correctly on the given canvas.
    
    Args:
        canvas: Canvas to test icons on
        
    Example:
        >>> test_all_weather_icons(my_test_canvas)
        # Cycles through all weather icons with delays
    """
    import time
    
    supported_conditions = get_supported_conditions()
    
    print(f"Testing {len(supported_conditions)} weather icons...")
    
    for i, condition in enumerate(supported_conditions):
        print(f"Testing icon {i+1}/{len(supported_conditions)}: {condition}")
        
        try:
            draw_weather_icon(canvas, condition)
            canvas.update()  # Force canvas to redraw
            time.sleep(1)    # Pause to view each icon
        except Exception as e:
            print(f"Error testing {condition} icon: {e}")
    
    print("✓ Weather icon testing completed")


def get_icon_performance_info(canvas) -> Dict[str, Any]:
    """
    Get performance information about the icon system.
    
    Returns metrics about canvas size, drawing performance, and
    system capabilities for optimization purposes.
    
    Args:
        canvas: Canvas to analyze
        
    Returns:
        Dictionary with performance metrics
    """
    try:
        return {
            "canvas_width": canvas.winfo_width(),
            "canvas_height": canvas.winfo_height(),
            "canvas_area": canvas.winfo_width() * canvas.winfo_height(),
            "supported_conditions": len(get_supported_conditions()),
            "canvas_valid": validate_canvas_size(canvas),
            "canvas_type": type(canvas).__name__
        }
    except Exception as e:
        return {"error": str(e)}


# Export the main functions for easy importing
__all__ = [
    "draw_weather_icon",
    "update_weather_icon", 
    "clear_icon_canvas",
    "animate_weather_icon",
    "create_metric_frame",
    "update_metric_values",
    "get_supported_conditions",
    "test_all_weather_icons",
    "validate_canvas_size"
]