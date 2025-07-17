#!/usr/bin/env python3
"""
Simple animation test to verify the weather animation system works
Run this to see if animations are displaying properly
"""

import tkinter as tk
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from gui.weather_animation import WeatherAnimation
    print("✓ Weather animation module imported successfully")
except ImportError as e:
    print(f"❌ Failed to import weather animation: {e}")
    sys.exit(1)


def main():
    print("🌤️ Testing Weather Animations")
    print("=" * 50)
    
    # Create main window
    root = tk.Tk()
    root.title("Weather Animation Test")
    root.geometry("800x600")
    root.configure(bg='black')
    
    # Create canvas for animation
    canvas = tk.Canvas(
        root, 
        bg='skyblue', 
        highlightthickness=0,
        width=800,
        height=600
    )
    canvas.pack(fill=tk.BOTH, expand=True)
    
    # Create animation system
    try:
        animation = WeatherAnimation(canvas)
        print("✓ Animation system created")
    except Exception as e:
        print(f"❌ Failed to create animation system: {e}")
        return
    
    # Test weather types
    weather_types = [
        ("clear", "Clear Sky"),
        ("rain", "Rainy Weather"),
        ("snow", "Snowy Weather"), 
        ("storm", "Thunderstorm"),
        ("cloudy", "Cloudy Sky"),
        ("sunny", "Sunny Day"),
        ("mist", "Misty Weather")
    ]
    
    current_index = 0
    
    def cycle_weather():
        nonlocal current_index
        weather_type, description = weather_types[current_index]
        
        print(f"Testing: {description} ({weather_type})")
        animation.set_weather_type(weather_type)
        root.title(f"Animation Test - {description}")
        
        # Show particle count for debugging
        particle_count = animation.get_particle_count()
        print(f"  - Particles: {particle_count}")
        print(f"  - Animation running: {animation.is_animation_running()}")
        
        # Move to next weather type
        current_index = (current_index + 1) % len(weather_types)
        
        # Schedule next change
        root.after(4000, cycle_weather)
    
    # Create control frame
    control_frame = tk.Frame(root, bg='white', height=60)
    control_frame.pack(side=tk.BOTTOM, fill=tk.X)
    control_frame.pack_propagate(False)
    
    # Instructions
    instructions = tk.Label(
        control_frame,
        text="Weather animations will cycle every 4 seconds. Click buttons for manual control.",
        bg='white',
        font=('Arial', 12)
    )
    instructions.pack(pady=5)
    
    # Manual control buttons
    button_frame = tk.Frame(control_frame, bg='white')
    button_frame.pack()
    
    for weather_type, description in weather_types:
        color = {
            'clear': '#87CEEB',
            'rain': '#4A90E2', 
            'snow': '#E8F4F8',
            'storm': '#2C3E50',
            'cloudy': '#95A5A6',
            'sunny': '#FFD700',
            'mist': '#BDC3C7'
        }.get(weather_type, '#CCCCCC')
        
        btn = tk.Button(
            button_frame,
            text=description.split()[0],
            command=lambda w=weather_type, d=description: [
                animation.set_weather_type(w),
                root.title(f"Animation Test - {d}"),
                print(f"Manual: {d} ({w})")
            ],
            bg=color,
            fg='black' if weather_type == 'sunny' else 'white',
            font=('Arial', 9, 'bold'),
            width=8,
            relief='raised',
            bd=2
        )
        btn.pack(side=tk.LEFT, padx=2)
    
    # Start/Stop controls
    start_btn = tk.Button(
        button_frame,
        text="Start",
        command=lambda: [
            animation.start_animation("clear"),
            print("Animation started")
        ],
        bg='lightgreen',
        font=('Arial', 9, 'bold'),
        width=6
    )
    start_btn.pack(side=tk.RIGHT, padx=5)
    
    stop_btn = tk.Button(
        button_frame,
        text="Stop", 
        command=lambda: [
            animation.stop_animation(),
            print("Animation stopped")
        ],
        bg='lightcoral',
        font=('Arial', 9, 'bold'),
        width=6
    )
    stop_btn.pack(side=tk.RIGHT, padx=2)
    
    # Start animation and cycling
    print("Starting animation test...")
    animation.start_animation("clear")
    root.after(2000, cycle_weather)  # Start cycling after 2 seconds
    
    def on_closing():
        print("Stopping animation...")
        animation.stop_animation()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    print("✓ Animation test window created")
    print("Close the window to exit")
    print("")
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        print("Animation test completed")


if __name__ == "__main__":
    main()