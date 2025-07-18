import customtkinter as ctk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from datetime import datetime
import threading
import tkinter as tk
import traceback
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from features.history_tracker.api import fetch_world_history
from features.tomorrows_guess.predictor import get_tomorrows_prediction
from core.theme import LIGHT_THEME, DARK_THEME
from core.api import get_current_weather

# Import weather animation
ANIMATION_AVAILABLE = False
WeatherAnimation = None

try:
    from gui.weather_animation import WeatherAnimation
    ANIMATION_AVAILABLE = True
    print("✅ Weather animation loaded")
except ImportError as e:
    print(f"❌ Animation not available: {e}")


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Smart Weather App")
        self.geometry("800x600")
        self.minsize(700, 500)
        
        # Initialize variables
        self.city_var = tk.StringVar(value="New York")
        self.unit = "C"
        self.temp_c = None
        self.temp_f = None
        self.is_dark_theme = False
        
        # Build GUI
        self.build_gui()
        
        # Auto-load weather
        self.after(1000, self.fetch_and_display)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def get_text_color(self):
        """Get text color based on theme"""
        return "white" if self.is_dark_theme else "black"

    def build_gui(self):
        """Build with WORKING animations"""
        
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Configure main window
        self.configure(bg="#87CEEB")
        
        # === ANIMATION CANVAS BACKGROUND ===
        if ANIMATION_AVAILABLE:
            # Create canvas that fills entire window
            self.animation_canvas = tk.Canvas(
                self, 
                width=800, 
                height=600,
                highlightthickness=0,
                bg="#87CEEB"
            )
            self.animation_canvas.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Initialize animation system
            try:
                self.smart_bg = WeatherAnimation(self.animation_canvas)
                print("🎬 Animation system created")
                
                # Start animation after a delay
                self.after(1000, self.start_initial_animation)
                
            except Exception as e:
                print(f"❌ Animation initialization failed: {e}")
                traceback.print_exc()
                self.smart_bg = None
        else:
            print("❌ No animation available")
            self.smart_bg = None

        # === CONTENT OVERLAY ===
        # Create a frame that sits on top of the animation
        self.overlay_frame = tk.Frame(self, bg="")
        self.overlay_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Make overlay transparent
        try:
            self.overlay_frame.configure(bg="#87CEEB")
        except:
            pass

        # Create scrollable content
        self.canvas = tk.Canvas(self.overlay_frame, highlightthickness=0, bg="#87CEEB")
        self.scrollbar = tk.Scrollbar(self.overlay_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#87CEEB")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        self.bind_all("<MouseWheel>", self._on_mousewheel)

        # === BUILD CONTENT ===
        self.create_content()

        print("[GUI] Built with animation background")

    def start_initial_animation(self):
        """Start the initial animation"""
        if self.smart_bg:
            try:
                print("🎬 Starting rain animation...")
                self.smart_bg.start_animation("rain")
                
                # Verify animation started
                self.after(2000, self.check_animation_status)
                
            except Exception as e:
                print(f"❌ Failed to start animation: {e}")
                traceback.print_exc()

    def check_animation_status(self):
        """Check if animation is running"""
        if self.smart_bg:
            running = self.smart_bg.is_animation_running()
            particles = self.smart_bg.get_particle_count()
            print(f"🎬 Animation status: Running={running}, Particles={particles}")

    def create_content(self):
        """Create all content elements"""
        
        # 1. ALL METRICS IN ONE ROW
        self.create_metrics_row()
        
        # 2. TOGGLE MODE BUTTON
        self.create_toggle_button()
        
        # 3. CITY ENTRY (no text box)
        self.create_city_field()
        
        # 4. WEATHER DISPLAY
        self.create_weather_info()
        
        # 5. TOMORROW'S PREDICTION
        self.create_prediction_info()
        
        # 6. WEATHER HISTORY
        self.create_history_info()

    def create_metrics_row(self):
        """All 6 metrics in one row"""
        metrics_container = tk.Frame(self.scrollable_frame, bg="#87CEEB")
        metrics_container.pack(pady=30)
        
        # Configure 6 columns
        for i in range(6):
            metrics_container.grid_columnconfigure(i, weight=1, minsize=120)
        
        metrics = [
            ("Humidity", "💧", "humidity_value"),
            ("Wind", "🌬️", "wind_value"), 
            ("Pressure", "🧭", "pressure_value"),  # Compass symbol back
            ("Visibility", "👁️", "visibility_value"),
            ("UV Index", "☀️", "uv_value"),
            ("Precipitation", "☔", "precipitation_value")
        ]
        
        for col, (header, icon, attr_name) in enumerate(metrics):
            # Header
            tk.Label(metrics_container, text=header, font=("Arial", 12, "bold"), 
                    fg=self.get_text_color(), bg="#87CEEB").grid(row=0, column=col, padx=8, pady=5)
            
            # Icon
            tk.Label(metrics_container, text=icon, font=("Arial", 20), 
                    bg="#87CEEB").grid(row=1, column=col, pady=8)
            
            # Value
            value_label = tk.Label(metrics_container, text="--", font=("Arial", 14, "bold"), 
                                 fg=self.get_text_color(), bg="#87CEEB")
            value_label.grid(row=2, column=col, pady=5)
            
            # Store reference
            setattr(self, attr_name, value_label)

    def create_toggle_button(self):
        """Toggle Mode button"""
        self.theme_btn = tk.Button(
            self.scrollable_frame,
            text="Toggle Mode",
            command=self.toggle_theme,
            bg="darkblue",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3,
            width=12
        )
        self.theme_btn.pack(pady=30)

    def create_city_field(self):
        """City entry - same color as background"""
        self.city_entry = tk.Entry(
            self.scrollable_frame,
            textvariable=self.city_var,
            font=("Arial", 20, "bold"),
            width=20,
            justify="center",
            bg="#87CEEB",
            fg=self.get_text_color(),
            relief="flat",
            bd=0
        )
        self.city_entry.pack(pady=20)
        self.city_entry.bind("<Return>", lambda e: self.fetch_and_display())

    def create_weather_info(self):
        """Weather display"""
        
        # Weather Icon
        self.icon_label = tk.Label(self.scrollable_frame, text="🌤️", font=("Arial", 48), bg="#87CEEB")
        self.icon_label.pack(pady=15)

        # Temperature
        self.temp_label = tk.Label(
            self.scrollable_frame,
            text="Loading...",
            font=("Arial", 36, "bold"),
            fg=self.get_text_color(),
            bg="#87CEEB",
            cursor="hand2"
        )
        self.temp_label.pack(pady=10)
        self.temp_label.bind("<Button-1>", lambda e: self.toggle_unit())

        # Description
        self.desc_label = tk.Label(
            self.scrollable_frame,
            text="Fetching weather...",
            font=("Arial", 18),
            fg=self.get_text_color(),
            bg="#87CEEB"
        )
        self.desc_label.pack(pady=10)

        # Last Update
        self.update_label = tk.Label(
            self.scrollable_frame,
            text="Starting...",
            font=("Arial", 12),
            fg=self.get_text_color(),
            bg="#87CEEB"
        )
        self.update_label.pack(pady=5)

    def create_prediction_info(self):
        """Tomorrow's prediction - no emoji"""
        tk.Label(self.scrollable_frame, text="Tomorrow's Prediction", 
                font=("Arial", 18, "bold"), fg=self.get_text_color(), bg="#87CEEB").pack(pady=(40,15))
        
        self.prediction_label = tk.Label(
            self.scrollable_frame,
            text="Loading prediction...",
            font=("Arial", 16),
            fg=self.get_text_color(),
            bg="#87CEEB"
        )
        self.prediction_label.pack(pady=10)

    def create_history_info(self):
        """Weather history - no emoji"""
        tk.Label(self.scrollable_frame, text="Weather History", 
                font=("Arial", 18, "bold"), fg=self.get_text_color(), bg="#87CEEB").pack(pady=(40,15))
        
        self.history_container = tk.Frame(self.scrollable_frame, bg="#87CEEB")
        self.history_container.pack(pady=15)
        
        for i in range(7):
            self.history_container.grid_columnconfigure(i, weight=1, minsize=90)
        
        self.history_labels = []

    def _on_mousewheel(self, event):
        """Handle scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def fetch_and_display(self):
        """Fetch weather data"""
        threading.Thread(target=self._fetch_weather, daemon=True).start()

    def _fetch_weather(self):
        """Background weather fetch"""
        try:
            city = self.city_var.get().strip() or "New York"
            weather_data = get_current_weather(city)
            
            if weather_data.get("error"):
                print(f"❌ Error: {weather_data['error']}")
                return
            
            self.after(0, lambda: self.update_displays(weather_data, city))
            
        except Exception as e:
            print(f"❌ Fetch error: {e}")

    def update_displays(self, weather_data, city):
        """Update all displays"""
        # Update weather
        temp_c = weather_data.get("temperature")
        if temp_c is not None:
            self.temp_c = round(temp_c, 1)
            self.temp_f = round((temp_c * 9 / 5) + 32, 1)
            
            if self.unit == "C":
                self.temp_label.configure(text=f"{self.temp_c}°C")
            else:
                self.temp_label.configure(text=f"{self.temp_f}°F")
        
        description = weather_data.get("description", "No description")
        self.desc_label.configure(text=description)
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.update_label.configure(text=f"Updated: {timestamp}")
        
        # Update metrics
        humidity = weather_data.get("humidity", "N/A")
        wind = weather_data.get("wind_speed", "N/A") 
        pressure = weather_data.get("pressure", "N/A")
        visibility = weather_data.get("visibility", "N/A")
        uv = weather_data.get("uv_index", "N/A")
        precipitation = weather_data.get("precipitation", "N/A")
        
        self.humidity_value.configure(text=f"{humidity}%" if humidity != "N/A" else "--")
        self.wind_value.configure(text=f"{wind} m/s" if wind != "N/A" else "--")
        self.pressure_value.configure(text=f"{pressure} hPa" if pressure != "N/A" else "--")
        self.visibility_value.configure(text=f"{visibility} m" if visibility != "N/A" else "--")
        self.uv_value.configure(text=str(uv) if uv != "N/A" else "--")
        self.precipitation_value.configure(text=f"{precipitation} mm" if precipitation != "N/A" else "--")
        
        # Update icon
        self._update_weather_icon(weather_data.get("icon"))
        
        # Update prediction
        self.update_prediction(city)
        
        # Update history
        self.update_history(city)
        
        # Update animation
        self.update_animation(weather_data)

    def update_prediction(self, city):
        """Update prediction"""
        try:
            predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)
            
            if predicted_temp:
                if self.unit == "C":
                    temp_text = f"{predicted_temp}°C"
                else:
                    temp_f = round((predicted_temp * 9/5) + 32, 1)
                    temp_text = f"{temp_f}°F"
                
                pred_text = f"{temp_text} | {confidence} | {accuracy}%"
            else:
                pred_text = "No prediction available"
                
            self.prediction_label.configure(text=pred_text)
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")

    def update_history(self, city):
        """Update history - black and white only"""
        try:
            for label in self.history_labels:
                label.destroy()
            self.history_labels.clear()
            
            history_data = fetch_world_history(city)
            
            if history_data and "time" in history_data:
                times = history_data.get("time", [])
                max_temps = history_data.get("temperature_2m_max", [])
                min_temps = history_data.get("temperature_2m_min", [])
                mean_temps = history_data.get("temperature_2m_mean", [])
                
                for col in range(min(7, len(times))):
                    if col < len(max_temps) and col < len(min_temps):
                        date = times[col][-5:] if len(times[col]) > 5 else times[col]
                        max_temp = max_temps[col]
                        min_temp = min_temps[col] 
                        avg_temp = mean_temps[col] if col < len(mean_temps) else None
                        
                        if self.unit == "F":
                            max_temp = round(max_temp * 9/5 + 32, 1)
                            min_temp = round(min_temp * 9/5 + 32, 1)
                            avg_temp = round(avg_temp * 9/5 + 32, 1) if avg_temp else None
                        else:
                            max_temp = round(max_temp, 1)
                            min_temp = round(min_temp, 1)
                            avg_temp = round(avg_temp, 1) if avg_temp else None
                        
                        unit_symbol = "°F" if self.unit == "F" else "°C"
                        
                        # Date
                        date_label = tk.Label(self.history_container, text=f"📅{date}", 
                                            font=("Arial", 9, "bold"), fg=self.get_text_color(), bg="#87CEEB")
                        date_label.grid(row=0, column=col, padx=3, pady=2)
                        self.history_labels.append(date_label)
                        
                        # Max - BLACK/WHITE ONLY
                        max_label = tk.Label(self.history_container, text=f"🔺{max_temp}{unit_symbol}", 
                                           font=("Arial", 9), fg=self.get_text_color(), bg="#87CEEB")
                        max_label.grid(row=1, column=col, padx=3, pady=1)
                        self.history_labels.append(max_label)
                        
                        # Min - BLACK/WHITE ONLY
                        min_label = tk.Label(self.history_container, text=f"🔻{min_temp}{unit_symbol}", 
                                           font=("Arial", 9), fg=self.get_text_color(), bg="#87CEEB")
                        min_label.grid(row=2, column=col, padx=3, pady=1)
                        self.history_labels.append(min_label)
                        
                        # Avg
                        if avg_temp:
                            avg_label = tk.Label(self.history_container, text=f"🌡️{avg_temp}{unit_symbol}", 
                                               font=("Arial", 9), fg=self.get_text_color(), bg="#87CEEB")
                            avg_label.grid(row=3, column=col, padx=3, pady=1)
                            self.history_labels.append(avg_label)
                        
        except Exception as e:
            print(f"❌ History error: {e}")

    def update_animation(self, weather_data):
        """Update animation based on weather"""
        if not self.smart_bg:
            print("❌ No animation system available")
            return
            
        try:
            description = weather_data.get("description", "").lower()
            
            if any(word in description for word in ["rain", "drizzle", "shower"]):
                animation_type = "rain"
            elif any(word in description for word in ["snow", "blizzard", "sleet"]):
                animation_type = "snow"
            elif any(word in description for word in ["thunder", "storm", "lightning"]):
                animation_type = "storm"
            elif any(word in description for word in ["cloud", "overcast", "broken"]):
                animation_type = "cloudy"
            elif any(word in description for word in ["clear", "sun", "sunny"]):
                animation_type = "sunny"
            elif any(word in description for word in ["mist", "fog", "haze"]):
                animation_type = "mist"
            else:
                animation_type = "clear"
            
            print(f"🎬 Updating animation to: {animation_type}")
            
            if self.smart_bg.is_animation_running():
                self.smart_bg.set_weather_type(animation_type)
            else:
                self.smart_bg.start_animation(animation_type)
                
            # Log animation status
            particles = self.smart_bg.get_particle_count()
            print(f"🎬 Animation updated: {particles} particles")
            
        except Exception as e:
            print(f"❌ Animation update error: {e}")
            traceback.print_exc()

    def toggle_theme(self):
        """Toggle theme"""
        self.is_dark_theme = not self.is_dark_theme
        self.build_gui()
        
        # Refresh data
        if hasattr(self, 'temp_c') and self.temp_c is not None:
            self.fetch_and_display()
        
        print(f"🎨 Theme: {'dark' if self.is_dark_theme else 'light'}")

    def toggle_unit(self):
        """Toggle temperature unit"""
        self.unit = "F" if self.unit == "C" else "C"
        self.fetch_and_display()

    def _update_weather_icon(self, icon_code):
        """Update weather icon"""
        if not icon_code:
            return
            
        try:
            url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            pil_img = Image.open(BytesIO(response.content))
            icon_image = ImageTk.PhotoImage(pil_img)
            
            self.icon_label.configure(image=icon_image, text="")
            self.icon_label.image = icon_image
            
        except Exception as e:
            print(f"Icon error: {e}")
            self.icon_label.configure(text="🌤️", image="")

    def on_close(self):
        """Clean up"""
        if self.smart_bg:
            try:
                self.smart_bg.stop_animation()
                print("🎬 Animation stopped")
            except:
                pass
        self.destroy()


def run_app():
    """Main entry point"""
    try:
        print("🚀 Starting Weather App...")
        app = WeatherApp()
        print("✅ App started successfully")
        app.mainloop()
    except Exception as e:
        print(f"💥 Error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    run_app()