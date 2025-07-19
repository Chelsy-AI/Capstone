import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
from datetime import datetime
import threading
import traceback
import sys
import os
import random
import math
import time

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from features.history_tracker.api import fetch_world_history
from features.tomorrows_guess.predictor import get_tomorrows_prediction
from config.themes import LIGHT_THEME, DARK_THEME
from config.api import get_current_weather
from config.storage import save_weather
from config.animations import WeatherAnimation

# ===== WEATHER APP WITH TABLE-STYLE METRICS =====
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
        self.theme = LIGHT_THEME
        self.text_color = "black"
        
        # Data storage to preserve across rebuilds
        self.current_weather_data = {}
        self.current_prediction_data = {}
        self.current_history_data = []
        
        # Scroll offset for scrolling
        self.scroll_offset = 0
        self.max_scroll = 300  # Maximum scroll distance
        
        # Store widget references to prevent garbage collection
        self.widgets = []
        
        # Build GUI
        self.build_gui()
        
        # Auto-load weather
        self.after(1000, self.fetch_and_display)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_gui(self):
        """Build GUI with table-style metrics layout"""
        
        # Clear existing widgets but preserve references
        for widget in self.winfo_children():
            widget.destroy()
        self.widgets.clear()
        
        # === Animation Background ===
        self.bg_canvas = tk.Canvas(self, highlightthickness=0, bg="#87CEEB")
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        try:
            self.smart_bg = WeatherAnimation(self.bg_canvas)
            self.after(500, lambda: self.smart_bg.start_animation("clear"))
            print("🎬 Animation ready")
        except Exception as e:
            print(f"❌ Animation failed: {e}")
            self.smart_bg = None

        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._on_scroll)
        self.scrollbar.place(x=780, y=0, height=600)

        # Bind mousewheel
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind_all("<Button-4>", self._on_mousewheel)
        self.bind_all("<Button-5>", self._on_mousewheel)

        # === TABLE-STYLE METRICS LAYOUT ===
        
        # Row 1: Headers
        widgets = [
            tk.Label(self, text="Humidity", font=("Arial", 12, "bold"), fg=self.text_color, bg="#87CEEB"),
            tk.Label(self, text="Wind", font=("Arial", 12, "bold"), fg=self.text_color, bg="#87CEEB"),
            tk.Label(self, text="Press.", font=("Arial", 12, "bold"), fg=self.text_color, bg="#87CEEB"),
            tk.Label(self, text="Visibility", font=("Arial", 12, "bold"), fg=self.text_color, bg="#87CEEB"),
            tk.Label(self, text="UV Index", font=("Arial", 12, "bold"), fg=self.text_color, bg="#87CEEB"),
            tk.Label(self, text="Precip.", font=("Arial", 12, "bold"), fg=self.text_color, bg="#87CEEB")
        ]
        positions = [(80, 30), (200, 30), (300, 30), (400, 30), (500, 30), (600, 30)]
        
        for widget, (x, y) in zip(widgets, positions):
            widget.place(x=x, y=y - self.scroll_offset)
            self.widgets.append(widget)
        
        # Row 2: Emojis
        emoji_widgets = [
            tk.Label(self, text="💧", font=("Arial", 18), bg="#87CEEB"),
            tk.Label(self, text="🌬️", font=("Arial", 18), bg="#87CEEB"),
            tk.Label(self, text="🧭", font=("Arial", 18), bg="#87CEEB"),
            tk.Label(self, text="👁️", font=("Arial", 18), bg="#87CEEB"),
            tk.Label(self, text="☀️", font=("Arial", 18), bg="#87CEEB"),
            tk.Label(self, text="🌧️", font=("Arial", 18), bg="#87CEEB")
        ]
        emoji_positions = [(95, 50), (210, 50), (315, 50), (425, 50), (525, 50), (620, 50)]
        
        for widget, (x, y) in zip(emoji_widgets, emoji_positions):
            widget.place(x=x, y=y - self.scroll_offset)
            self.widgets.append(widget)
        
        # Row 3: Values
        self.humidity_value = tk.Label(self, text="--", font=("Arial", 12), fg=self.text_color, bg="#87CEEB")
        self.humidity_value.place(x=85, y=75 - self.scroll_offset)
        self.widgets.append(self.humidity_value)
        
        self.wind_value = tk.Label(self, text="--", font=("Arial", 12), fg=self.text_color, bg="#87CEEB")
        self.wind_value.place(x=195, y=75 - self.scroll_offset)
        self.widgets.append(self.wind_value)
        
        self.pressure_value = tk.Label(self, text="--", font=("Arial", 12), fg=self.text_color, bg="#87CEEB")
        self.pressure_value.place(x=295, y=75 - self.scroll_offset)
        self.widgets.append(self.pressure_value)
        
        self.visibility_value = tk.Label(self, text="--", font=("Arial", 12), fg=self.text_color, bg="#87CEEB")
        self.visibility_value.place(x=410, y=75 - self.scroll_offset)
        self.widgets.append(self.visibility_value)
        
        self.uv_value = tk.Label(self, text="--", font=("Arial", 12), fg=self.text_color, bg="#87CEEB")
        self.uv_value.place(x=530, y=75 - self.scroll_offset)
        self.widgets.append(self.uv_value)
        
        self.precipitation_value = tk.Label(self, text="--", font=("Arial", 12), fg=self.text_color, bg="#87CEEB")
        self.precipitation_value.place(x=615, y=75 - self.scroll_offset)
        self.widgets.append(self.precipitation_value)

        # Toggle Theme Button
        self.theme_btn = tk.Button(
            self,
            text="Toggle Theme",
            command=self.toggle_theme,
            bg="darkblue",
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.theme_btn.place(x=350, y=110 - self.scroll_offset)
        self.widgets.append(self.theme_btn)

        # City Input
        city_label = tk.Label(self, text="City:", font=("Arial", 16), fg=self.text_color, bg="#87CEEB")
        city_label.place(x=320, y=150 - self.scroll_offset)
        self.widgets.append(city_label)
        
        self.city_entry = tk.Entry(
            self,
            textvariable=self.city_var,
            font=("Arial", 16),
            width=20,
            justify="center",
            bg="white",
            fg="black"
        )
        self.city_entry.place(x=270, y=175 - self.scroll_offset)
        self.city_entry.bind("<Return>", lambda e: self.fetch_and_display())
        self.widgets.append(self.city_entry)

        # Today's Weather
        # Weather Icon
        self.icon_label = tk.Label(self, text="🌤️", font=("Arial", 48), bg="#87CEEB")
        self.icon_label.place(x=350, y=220 - self.scroll_offset)
        self.widgets.append(self.icon_label)

        # Temperature
        self.temp_label = tk.Label(
            self,
            text="Loading...",
            font=("Arial", 48, "bold"),
            fg=self.text_color,
            bg="#87CEEB",
            cursor="hand2"
        )
        self.temp_label.place(x=300, y=290 - self.scroll_offset)
        self.temp_label.bind("<Button-1>", lambda e: self.toggle_unit())
        self.widgets.append(self.temp_label)

        # Description
        self.desc_label = tk.Label(
            self,
            text="Fetching weather...",
            font=("Arial", 20),
            fg=self.text_color,
            bg="#87CEEB"
        )
        self.desc_label.place(x=250, y=360 - self.scroll_offset)
        self.widgets.append(self.desc_label)

        # Tomorrow's Prediction
        # Temperature
        temp_pred_label = tk.Label(self, text="Temperature:", font=("Arial", 16), fg=self.text_color, bg="#87CEEB")
        temp_pred_label.place(x=100, y=400 - self.scroll_offset)
        self.widgets.append(temp_pred_label)
        
        self.temp_prediction = tk.Label(self, text="Loading...", font=("Arial", 14), fg=self.text_color, bg="#87CEEB")
        self.temp_prediction.place(x=220, y=400 - self.scroll_offset)
        self.widgets.append(self.temp_prediction)
        
        # Confidence
        conf_label = tk.Label(self, text="Confidence:", font=("Arial", 16), fg=self.text_color, bg="#87CEEB")
        conf_label.place(x=100, y=430 - self.scroll_offset)
        self.widgets.append(conf_label)
        
        self.confidence_prediction = tk.Label(self, text="Loading...", font=("Arial", 14), fg=self.text_color, bg="#87CEEB")
        self.confidence_prediction.place(x=200, y=430 - self.scroll_offset)
        self.widgets.append(self.confidence_prediction)
        
        # Accuracy
        acc_label = tk.Label(self, text="Accuracy:", font=("Arial", 16), fg=self.text_color, bg="#87CEEB")
        acc_label.place(x=100, y=460 - self.scroll_offset)
        self.widgets.append(acc_label)
        
        self.accuracy_prediction = tk.Label(self, text="Loading...", font=("Arial", 14), fg=self.text_color, bg="#87CEEB")
        self.accuracy_prediction.place(x=180, y=460 - self.scroll_offset)
        self.widgets.append(self.accuracy_prediction)

        # 7-Day History
        history_title = tk.Label(self, text="History", font=("Arial", 20, "bold"), fg=self.text_color, bg="#87CEEB")
        history_title.place(x=350, y=500 - self.scroll_offset)
        self.widgets.append(history_title)

        # 7-Day History - NO HEADER
        self.history_labels = []

        print("[GUI] Table-style metrics GUI ready")

    def _on_scroll(self, *args):
        """Handle scrollbar movement"""
        if len(args) >= 2:
            scroll_type = args[0]
            if scroll_type == "moveto":
                # Calculate new scroll position
                fraction = float(args[1])
                self.scroll_offset = int(fraction * self.max_scroll)
                self._update_widget_positions()
            elif scroll_type in ["scroll", "units"]:
                # Handle scroll up/down
                direction = int(args[1])
                scroll_amount = 20
                self.scroll_offset += direction * scroll_amount
                self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
                self._update_widget_positions()

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        # Determine scroll direction
        if event.delta:
            # Windows
            scroll_amount = -int(event.delta / 120) * 20
        elif event.num == 4:
            # Linux scroll up
            scroll_amount = -20
        elif event.num == 5:
            # Linux scroll down
            scroll_amount = 20
        else:
            return
        
        # Update scroll offset
        old_offset = self.scroll_offset
        self.scroll_offset += scroll_amount
        self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
        
        # Only update if scroll actually changed
        if self.scroll_offset != old_offset:
            self._update_widget_positions()
            # Update scrollbar position
            fraction = self.scroll_offset / self.max_scroll if self.max_scroll > 0 else 0
            self.scrollbar.set(fraction, fraction + 0.1)

    def _update_widget_positions(self):
        """Update all widget positions based on scroll offset"""
        try:
            # Original positions for each widget type
            positions = [
                # Headers
                (80, 30), (200, 30), (300, 30), (400, 30), (500, 30), (600, 30),
                # Emojis  
                (95, 50), (210, 50), (315, 50), (425, 50), (525, 50), (620, 50),
                # Values
                (85, 75), (195, 75), (295, 75), (410, 75), (530, 75), (615, 75),
                # Theme button
                (350, 110),
                # City
                (320, 150), (270, 175),
                # Weather display
                (350, 220), (300, 290), (250, 360),
                # Tomorrow's prediction
                (100, 400), (220, 400), (100, 430), (200, 430), (100, 460), (180, 460),
                # History title
                (350, 500)
            ]
            
            # Update positions for existing widgets
            for i, widget in enumerate(self.widgets):
                if i < len(positions):
                    x, y = positions[i]
                    widget.place(x=x, y=y - self.scroll_offset)
            
            # Update history labels if they exist
            start_y = 650
            for col, label in enumerate(self.history_labels):
                if col % 4 == 0:  # Date labels (every 4th label)
                    x_pos = 50 + (col // 4) * 100
                    y_pos = start_y
                elif col % 4 == 1:  # Max temp
                    x_pos = 50 + ((col - 1) // 4) * 100
                    y_pos = start_y + 20
                elif col % 4 == 2:  # Min temp
                    x_pos = 50 + ((col - 2) // 4) * 100
                    y_pos = start_y + 40
                else:  # Average temp
                    x_pos = 50 + ((col - 3) // 4) * 100
                    y_pos = start_y + 60
                
                label.place(x=x_pos, y=y_pos - self.scroll_offset)
                
        except Exception as e:
            print(f"❌ Position update error: {e}")

    def fetch_and_display(self):
        """Fetch and display weather data"""
        threading.Thread(target=self._fetch_weather, daemon=True).start()

    def _fetch_weather(self):
        """Fetch weather in background thread"""
        try:
            city = self.city_var.get().strip() or "New York"
            print(f"🌍 Fetching weather for: {city}")
            
            weather_data = get_current_weather(city)
            
            if weather_data.get("error"):
                print(f"❌ Error: {weather_data['error']}")
                return
            
            # Save to CSV
            try:
                save_weather(weather_data)
                print("✅ Weather data saved to CSV")
            except Exception as e:
                print(f"⚠️ CSV save error: {e}")
            
            self.after(0, lambda: self.update_weather_display(weather_data))
            self.after(0, lambda: self.update_tomorrow_prediction(city))
            self.after(0, lambda: self.update_history_display(city))
            self.after(0, lambda: self.update_background_animation(weather_data))
            
        except Exception as e:
            print(f"❌ Weather fetch error: {e}")

    def update_weather_display(self, weather_data):
        """Update weather display"""
        try:
            # Store data for preservation across rebuilds
            self.current_weather_data = weather_data
            
            # Temperature
            temp_c = weather_data.get("temperature")
            if temp_c is not None:
                self.temp_c = round(temp_c, 1)
                self.temp_f = round((temp_c * 9 / 5) + 32, 1)
                
                if self.unit == "C":
                    self.temp_label.configure(text=f"{self.temp_c}°C")
                else:
                    self.temp_label.configure(text=f"{self.temp_f}°F")
            
            # Description
            description = weather_data.get("description", "No description")
            self.desc_label.configure(text=description)
            
            # Metrics - Table format
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
            self.uv_value.configure(text=f"{uv}" if uv != "N/A" else "--")
            self.precipitation_value.configure(text=f"{precipitation} mm" if precipitation != "N/A" else "--")
            
            # Colorful weather icon
            self._update_weather_icon(weather_data.get("icon"))
            
            print(f"✅ Weather updated: {description}")
            
        except Exception as e:
            print(f"❌ Display update error: {e}")

    def update_tomorrow_prediction(self, city):
        """Update tomorrow's prediction"""
        try:
            predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)
            
            # Store data for preservation
            self.current_prediction_data = (predicted_temp, confidence, accuracy)
            
            if predicted_temp:
                if self.unit == "C":
                    temp_text = f"{predicted_temp}°C"
                else:
                    temp_f = round((predicted_temp * 9/5) + 32, 1)
                    temp_text = f"{temp_f}°F"
                
                self.temp_prediction.configure(text=temp_text)
                self.confidence_prediction.configure(text=confidence)
                self.accuracy_prediction.configure(text=f"{accuracy}%")
            else:
                self.temp_prediction.configure(text="No prediction available")
                self.confidence_prediction.configure(text="--")
                self.accuracy_prediction.configure(text="--")
                
        except Exception as e:
            print(f"❌ Prediction error: {e}")

    def update_history_display(self, city):
        """Update 7-day history"""
        try:
            # Clear old history
            for label in self.history_labels:
                label.destroy()
            self.history_labels.clear()
            self.current_history_data.clear()
            
            history_data = fetch_world_history(city)
            
            if history_data and "time" in history_data:
                times = history_data.get("time", [])
                max_temps = history_data.get("temperature_2m_max", [])
                min_temps = history_data.get("temperature_2m_min", [])
                
                start_y = 650
                for col in range(min(7, len(times))):
                    if col < len(max_temps) and col < len(min_temps):
                        date = times[col][-5:] if len(times[col]) > 5 else times[col]
                        max_temp = max_temps[col]
                        min_temp = min_temps[col]
                        avg_temp = round((max_temp + min_temp) / 2, 1) if max_temp and min_temp else None
                        
                        if self.unit == "F":
                            max_temp = round(max_temp * 9/5 + 32, 1)
                            min_temp = round(min_temp * 9/5 + 32, 1)
                            avg_temp = round(avg_temp * 9/5 + 32, 1) if avg_temp else None
                        else:
                            max_temp = round(max_temp, 1)
                            min_temp = round(min_temp, 1)
                        
                        unit_symbol = "°F" if self.unit == "F" else "°C"
                        
                        # Store data for preservation
                        self.current_history_data.append((date, max_temp, min_temp, unit_symbol, avg_temp))
                        
                        x_pos = 50 + col * 100
                        
                        # Date with emoji
                        date_label = tk.Label(self, text=f"📅 {date}", font=("Arial", 12, "bold"),
                                            fg=self.text_color, bg="#87CEEB")
                        date_label.place(x=x_pos, y=start_y - self.scroll_offset)
                        self.history_labels.append(date_label)
                        
                        # Max temp with emoji
                        max_label = tk.Label(self, text=f"🔺 {max_temp}{unit_symbol}", font=("Arial", 11),
                                           fg=self.text_color, bg="#87CEEB")
                        max_label.place(x=x_pos, y=start_y + 20 - self.scroll_offset)
                        self.history_labels.append(max_label)
                        
                        # Min temp with emoji
                        min_label = tk.Label(self, text=f"🔻 {min_temp}{unit_symbol}", font=("Arial", 11),
                                           fg=self.text_color, bg="#87CEEB")
                        min_label.place(x=x_pos, y=start_y + 40 - self.scroll_offset)
                        self.history_labels.append(min_label)
                        
                        # Average temp with emoji
                        if avg_temp:
                            avg_label = tk.Label(self, text=f"🌡️ {avg_temp}{unit_symbol}", font=("Arial", 11),
                                               fg=self.text_color, bg="#87CEEB")
                            avg_label.place(x=x_pos, y=start_y + 60 - self.scroll_offset)
                            self.history_labels.append(avg_label)
                        
        except Exception as e:
            print(f"❌ History error: {e}")

    def update_background_animation(self, weather_data):
        """Update background animation"""
        if not self.smart_bg:
            print("❌ No animation system")
            return
            
        try:
            description = weather_data.get("description", "").lower()
            print(f"🌤️ Weather description: {description}")
            
            # Map description to animation type
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
            
            print(f"🎬 Animation type: {animation_type}")
            
            if self.smart_bg.is_animation_running():
                self.smart_bg.set_weather_type(animation_type)
            else:
                self.smart_bg.start_animation(animation_type)
                
            # Debug info
            particles = self.smart_bg.get_particle_count()
            print(f"🎬 Particles: {particles}")
            
        except Exception as e:
            print(f"❌ Animation error: {e}")
            traceback.print_exc()

    def toggle_theme(self):
        """Toggle theme - changes all text from black to white"""
        self.text_color = "white" if self.text_color == "black" else "black"
        
        # Update text color for existing widgets instead of rebuilding
        widgets_to_update = [
            self.humidity_value, self.wind_value, self.pressure_value,
            self.visibility_value, self.uv_value, self.precipitation_value,
            self.temp_label, self.desc_label, self.temp_prediction,
            self.confidence_prediction, self.accuracy_prediction
        ]
        
        for widget in widgets_to_update:
            try:
                widget.configure(fg=self.text_color)
            except:
                pass
        
        # Update other colored widgets
        for widget in self.widgets:
            try:
                if hasattr(widget, 'configure'):
                    widget_class = widget.winfo_class()
                    if widget_class == 'Label' and widget != self.icon_label:
                        widget.configure(fg=self.text_color)
            except:
                pass
        
        # Update history labels
        for label in self.history_labels:
            try:
                label.configure(fg=self.text_color)
            except:
                pass
                
        print(f"🎨 Theme toggled to: {self.text_color}")

    def toggle_unit(self):
        """Toggle temperature unit"""
        self.unit = "F" if self.unit == "C" else "C"
        print(f"🌡️ Unit changed to: {self.unit}")
        self.fetch_and_display()

    def _update_weather_icon(self, icon_code):
        """Update colorful weather icon"""
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
        print("🚀 Starting Weather App with Table-Style Metrics...")
        app = WeatherApp()
        print("✅ App started successfully")
        app.mainloop()
    except Exception as e:
        print(f"💥 Error: {e}")
        traceback.print_exc()


# Make sure this is available for import
__all__ = ['run_app', 'WeatherApp']


if __name__ == "__main__":
    run_app()