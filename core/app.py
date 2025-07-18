import tkinter as tk
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

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from features.history_tracker.api import fetch_world_history
from features.tomorrows_guess.predictor import get_tomorrows_prediction
from core.theme import LIGHT_THEME, DARK_THEME
from core.api import get_current_weather
from core.storage import save_weather


# ===== WORKING ANIMATION SYSTEM =====
class WeatherParticle:
    def __init__(self, x, y, canvas_width, canvas_height):
        self.x = x
        self.y = y
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.id = None

    def update(self):
        pass

    def draw(self, canvas):
        pass

    def is_off_screen(self):
        return (self.x < -100 or self.x > self.canvas_width + 100 or 
                self.y < -100 or self.y > self.canvas_height + 100)


class RainDrop(WeatherParticle):
    def __init__(self, x, y, canvas_width, canvas_height):
        super().__init__(x, y, canvas_width, canvas_height)
        self.length = random.randint(15, 25)
        self.speed = random.uniform(8, 15)
        self.wind = random.uniform(-2, 2)

    def update(self):
        self.y += self.speed
        self.x += self.wind
        if self.y > self.canvas_height + 50:
            self.y = random.randint(-100, -50)
            self.x = random.randint(-50, self.canvas_width + 50)

    def draw(self, canvas):
        if self.id:
            canvas.delete(self.id)
        self.id = canvas.create_line(
            self.x, self.y, self.x + self.wind, self.y + self.length,
            fill="#4A90E2", width=2, tags="particle"
        )


class SnowFlake(WeatherParticle):
    def __init__(self, x, y, canvas_width, canvas_height):
        super().__init__(x, y, canvas_width, canvas_height)
        self.size = random.randint(3, 8)
        self.speed = random.uniform(1, 4)
        self.drift = random.uniform(-1, 1)
        self.phase = random.uniform(0, 2 * math.pi)

    def update(self):
        self.y += self.speed
        self.phase += 0.02
        self.x += self.drift + math.sin(self.phase) * 0.5
        if self.y > self.canvas_height + 20:
            self.y = random.randint(-50, -20)
            self.x = random.randint(-20, self.canvas_width + 20)

    def draw(self, canvas):
        if self.id:
            canvas.delete(self.id)
        self.id = canvas.create_oval(
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size,
            fill="white", outline="", tags="particle"
        )


class CloudParticle(WeatherParticle):
    def __init__(self, x, y, canvas_width, canvas_height):
        super().__init__(x, y, canvas_width, canvas_height)
        self.width = random.randint(100, 180)
        self.height = random.randint(40, 80)
        self.speed = random.uniform(0.3, 1.0)

    def update(self):
        self.x += self.speed
        if self.x > self.canvas_width + self.width:
            self.x = -self.width
            self.y = random.randint(20, self.canvas_height // 3)

    def draw(self, canvas):
        if self.id:
            canvas.delete(self.id)
        cloud_items = []
        for i in range(4):
            offset_x = i * (self.width // 5)
            offset_y = random.randint(-self.height//4, self.height//4)
            circle_size = self.height + random.randint(-10, 10)
            item_id = canvas.create_oval(
                self.x + offset_x, self.y + offset_y,
                self.x + offset_x + circle_size, self.y + offset_y + circle_size,
                fill="#D3D3D3", outline="", tags="particle"
            )
            cloud_items.append(item_id)
        self.id = cloud_items[0]


class WeatherAnimation:
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = 800
        self.height = 600
        self.particles = []
        self.is_running = False
        self.animation_id = None
        self.current_weather = "clear"
        self.lightning_timer = 0
        self.fps = 30
        self.frame_delay = int(1000 / self.fps)
        print("[WeatherAnimation] Animation system initialized")

    def start_animation(self, weather_type="clear"):
        print(f"[WeatherAnimation] Starting animation: {weather_type}")
        self.current_weather = weather_type
        if not self.is_running:
            self.is_running = True
            self._initialize_particles()
            self._animate()

    def stop_animation(self):
        print("[WeatherAnimation] Stopping animation")
        self.is_running = False
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None
        self._clear_particles()

    def set_weather_type(self, weather_type):
        if weather_type != self.current_weather:
            print(f"[WeatherAnimation] Changing to: {weather_type}")
            self.current_weather = weather_type
            self._clear_particles()
            self._initialize_particles()

    def _initialize_particles(self):
        self.particles.clear()
        if self.current_weather == "rain":
            self._create_rain_particles()
        elif self.current_weather == "snow":
            self._create_snow_particles()
        elif self.current_weather == "storm":
            self._create_storm_particles()
        elif self.current_weather == "cloudy":
            self._create_cloud_particles()

    def _create_rain_particles(self):
        for _ in range(80):
            x = random.randint(-50, self.width + 50)
            y = random.randint(-100, self.height)
            self.particles.append(RainDrop(x, y, self.width, self.height))

    def _create_snow_particles(self):
        for _ in range(60):
            x = random.randint(-20, self.width + 20)
            y = random.randint(-50, self.height)
            self.particles.append(SnowFlake(x, y, self.width, self.height))

    def _create_storm_particles(self):
        self._create_rain_particles()
        for _ in range(3):
            x = random.randint(-100, self.width)
            y = random.randint(20, self.height // 4)
            self.particles.append(CloudParticle(x, y, self.width, self.height))

    def _create_cloud_particles(self):
        for _ in range(4):
            x = random.randint(-150, self.width)
            y = random.randint(20, self.height // 2)
            self.particles.append(CloudParticle(x, y, self.width, self.height))

    def _animate(self):
        if not self.is_running:
            return
        try:
            self.canvas.delete("particle")
            self.canvas.delete("background")
            self._draw_background()
            for particle in self.particles:
                particle.update()
                particle.draw(self.canvas)
                if particle.is_off_screen():
                    if hasattr(particle, 'id') and particle.id:
                        self.canvas.delete(particle.id)
            if self.current_weather == "storm":
                self._draw_lightning()
            self.animation_id = self.canvas.after(self.frame_delay, self._animate)
        except Exception as e:
            print(f"[WeatherAnimation] Animation error: {e}")
            self.animation_id = self.canvas.after(self.frame_delay, self._animate)

    def _draw_background(self):
        colors = {
            "rain": "#4A6741", "snow": "#E8F4F8", "storm": "#2C3E50",
            "cloudy": "#95A5A6", "mist": "#BDC3C7", "sunny": "#87CEEB", "clear": "#87CEEB"
        }
        bg_color = colors.get(self.current_weather, "#87CEEB")
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill=bg_color, outline="", tags="background")
        if self.current_weather in ["sunny", "clear"]:
            self._draw_sun()

    def _draw_sun(self):
        sun_x = self.width - 120
        sun_y = 100
        sun_radius = 50
        for i in range(12):
            angle = i * (2 * math.pi / 12)
            start_x = sun_x + math.cos(angle) * (sun_radius + 15)
            start_y = sun_y + math.sin(angle) * (sun_radius + 15)
            end_x = sun_x + math.cos(angle) * (sun_radius + 35)
            end_y = sun_y + math.sin(angle) * (sun_radius + 35)
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="#FFD700", width=4, tags="background")
        self.canvas.create_oval(sun_x - sun_radius, sun_y - sun_radius, sun_x + sun_radius, sun_y + sun_radius, fill="#FFD700", outline="#FFA500", width=2, tags="background")

    def _draw_lightning(self):
        self.lightning_timer += 1
        if self.lightning_timer > 60 and random.random() < 0.03:
            self.lightning_timer = 0
            start_x = random.randint(self.width // 4, 3 * self.width // 4)
            start_y = random.randint(0, self.height // 4)
            points = [(start_x, start_y)]
            current_x, current_y = start_x, start_y
            for _ in range(random.randint(4, 8)):
                current_x += random.randint(-40, 40)
                current_y += random.randint(30, 80)
                points.append((current_x, current_y))
                if current_y >= self.height:
                    break
            for i in range(len(points) - 1):
                self.canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], fill="#FFFF00", width=random.randint(3, 6), tags="background")

    def _clear_particles(self):
        try:
            self.canvas.delete("particle")
            self.canvas.delete("background")
            self.particles.clear()
        except Exception as e:
            print(f"[WeatherAnimation] Clear error: {e}")

    def get_particle_count(self):
        return len(self.particles)

    def is_animation_running(self):
        return self.is_running


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Weather App")
        self.geometry("800x600")
        self.minsize(700, 500)
        self.city_var = tk.StringVar(value="New York")
        self.unit = "C"
        self.temp_c = None
        self.temp_f = None
        self.theme = LIGHT_THEME
        self.is_dark_theme = False
        self.build_gui()
        self.after(1000, self.fetch_and_display)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def get_text_color(self):
        return "white" if self.is_dark_theme else "black"

    def build_gui(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.bg_canvas = tk.Canvas(self, highlightthickness=0, bg="#87CEEB")
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        try:
            self.smart_bg = WeatherAnimation(self.bg_canvas)
            self.after(500, lambda: self.smart_bg.start_animation("clear"))
            print("🎬 Animation ready")
        except Exception as e:
            print(f"❌ Animation failed: {e}")
            self.smart_bg = None

        self.overlay_frame = tk.Frame(self, bg="")
        self.overlay_frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.canvas = tk.Canvas(self.overlay_frame, highlightthickness=0, bg="", bd=0)
        self.scrollbar = tk.Scrollbar(self.overlay_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.bind_all("<MouseWheel>", self._on_mousewheel)

        self.create_metrics_row()
        self.create_toggle_button()
        self.create_city_field()
        self.create_todays_weather()
        self.create_tomorrows_prediction()
        self.create_history()

    def create_metrics_row(self):
        metrics_container = tk.Frame(self.scrollable_frame, bg="")
        metrics_container.pack(pady=20, padx=20, fill="x")
        for i in range(6):
            metrics_container.grid_columnconfigure(i, weight=1)
        metrics = [("Wind", "wind_value"), ("Humidity", "humidity_value"), ("Pressure", "pressure_value"), ("Visibility", "visibility_value"), ("UV Index", "uv_value"), ("Precipitation", "precipitation_value")]
        for col, (label_text, attr_name) in enumerate(metrics):
            label = tk.Label(metrics_container, text=label_text, font=("Arial", 14, "bold"), fg=self.get_text_color(), bg="")
            label.grid(row=0, column=col, padx=10, pady=5)
            value_label = tk.Label(metrics_container, text="--", font=("Arial", 16, "bold"), fg=self.get_text_color(), bg="")
            value_label.grid(row=1, column=col, padx=10, pady=5)
            setattr(self, attr_name, value_label)

    def create_toggle_button(self):
        self.theme_btn = tk.Button(self.scrollable_frame, text="Toggle Theme", command=self.toggle_theme, bg="gray", fg="white", font=("Arial", 14, "bold"), pady=10)
        self.theme_btn.pack(pady=20)

    def create_city_field(self):
        self.city_entry = tk.Entry(self.scrollable_frame, textvariable=self.city_var, font=("Arial", 24, "bold"), width=20, justify="center", bg="white", fg="black", bd=2)
        self.city_entry.pack(pady=20)
        self.city_entry.bind("<Return>", lambda e: self.fetch_and_display())

    def create_todays_weather(self):
        self.icon_label = tk.Label(self.scrollable_frame, text="🌤️", font=("Arial", 48), bg="")
        self.icon_label.pack(pady=15)
        self.temp_label = tk.Label(self.scrollable_frame, text="Loading...", font=("Arial", 48, "bold"), fg=self.get_text_color(), bg="", cursor="hand2")
        self.temp_label.pack(pady=10)
        self.temp_label.bind("<Button-1>", lambda e: self.toggle_unit())
        self.desc_label = tk.Label(self.scrollable_frame, text="Fetching weather...", font=("Arial", 20), fg=self.get_text_color(), bg="")
        self.desc_label.pack(pady=10)
        self.update_label = tk.Label(self.scrollable_frame, text="Starting...", font=("Arial", 14), fg=self.get_text_color(), bg="")
        self.update_label.pack(pady=5)

    def create_tomorrows_prediction(self):
        pred_container = tk.Frame(self.scrollable_frame, bg="")
        pred_container.pack(pady=30, padx=20, fill="x")
        for i in range(3):
            pred_container.grid_columnconfigure(i, weight=1)
        
        tk.Label(pred_container, text="Temperature", font=("Arial", 16, "bold"), fg=self.get_text_color(), bg="").grid(row=0, column=0, padx=10, pady=5)
        self.pred_temp_label = tk.Label(pred_container, text="--", font=("Arial", 16, "bold"), fg=self.get_text_color(), bg="")
        self.pred_temp_label.grid(row=1, column=0, pady=5)
        
        tk.Label(pred_container, text="Confidence", font=("Arial", 16, "bold"), fg=self.get_text_color(), bg="").grid(row=0, column=1, padx=10, pady=5)
        self.pred_conf_label = tk.Label(pred_container, text="--", font=("Arial", 16, "bold"), fg=self.get_text_color(), bg="")
        self.pred_conf_label.grid(row=1, column=1, pady=5)
        
        tk.Label(pred_container, text="Accuracy", font=("Arial", 16, "bold"), fg=self.get_text_color(), bg="").grid(row=0, column=2, padx=10, pady=5)
        self.pred_acc_label = tk.Label(pred_container, text="--", font=("Arial", 16, "bold"), fg=self.get_text_color(), bg="")
        self.pred_acc_label.grid(row=1, column=2, pady=5)

    def create_history(self):
        tk.Label(self.scrollable_frame, text="History", font=("Arial", 18, "bold"), fg=self.get_text_color(), bg="").pack(pady=(40, 15))
        self.history_container = tk.Frame(self.scrollable_frame, bg="")
        self.history_container.pack(pady=15, padx=20, fill="x")
        for i in range(7):
            self.history_container.grid_columnconfigure(i, weight=1)
        self.history_labels = []

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def fetch_and_display(self):
        threading.Thread(target=self._fetch_weather, daemon=True).start()

    def _fetch_weather(self):
        try:
            city = self.city_var.get().strip() or "New York"
            weather_data = get_current_weather(city)
            if weather_data.get("error"):
                print(f"❌ Error: {weather_data['error']}")
                return
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
        try:
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
            
            self._update_weather_icon(weather_data.get("icon"))
        except Exception as e:
            print(f"❌ Display update error: {e}")

    def update_tomorrow_prediction(self, city):
        try:
            predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)
            if predicted_temp:
                if self.unit == "C":
                    temp_text = f"{predicted_temp}°C"
                else:
                    temp_f = round((predicted_temp * 9/5) + 32, 1)
                    temp_text = f"{temp_f}°F"
                self.pred_temp_label.configure(text=temp_text)
                self.pred_conf_label.configure(text=str(confidence))
                if isinstance(accuracy, (int, float)):
                    self.pred_acc_label.configure(text=f"{accuracy}%")
                else:
                    self.pred_acc_label.configure(text=str(accuracy))
            else:
                self.pred_temp_label.configure(text="N/A")
                self.pred_conf_label.configure(text="N/A")
                self.pred_acc_label.configure(text="N/A")
        except Exception as e:
            print(f"❌ Prediction error: {e}")

    def update_history_display(self, city):
        try:
            for label in self.history_labels:
                label.destroy()
            self.history_labels.clear()
            
            history_data = fetch_world_history(city)
            if history_data and "time" in history_data:
                times = history_data.get("time", [])
                max_temps = history_data.get("temperature_2m_max", [])
                min_temps = history_data.get("temperature_2m_min", [])
                
                for col in range(min(7, len(times))):
                    if col < len(max_temps) and col < len(min_temps):
                        date = times[col][-5:] if len(times[col]) > 5 else times[col]
                        max_temp = max_temps[col]
                        min_temp = min_temps[col]
                        
                        if self.unit == "F":
                            max_temp = round(max_temp * 9/5 + 32, 1)
                            min_temp = round(min_temp * 9/5 + 32, 1)
                        else:
                            max_temp = round(max_temp, 1)
                            min_temp = round(min_temp, 1)
                        
                        unit_symbol = "°F" if self.unit == "F" else "°C"
                        
                        date_label = tk.Label(self.history_container, text=f"{date}", font=("Arial", 14, "bold"), fg=self.get_text_color(), bg="")
                        date_label.grid(row=0, column=col, padx=5, pady=2)
                        self.history_labels.append(date_label)
                        
                        max_label = tk.Label(self.history_container, text=f"Max: {max_temp}{unit_symbol}", font=("Arial", 12), fg=self.get_text_color(), bg="")
                        max_label.grid(row=1, column=col, padx=5, pady=1)
                        self.history_labels.append(max_label)
                        
                        min_label = tk.Label(self.history_container, text=f"Min: {min_temp}{unit_symbol}", font=("Arial", 12), fg=self.get_text_color(), bg="")
                        min_label.grid(row=2, column=col, padx=5, pady=1)
                        self.history_labels.append(min_label)
        except Exception as e:
            print(f"❌ History error: {e}")

    def update_background_animation(self, weather_data):
        if not self.smart_bg:
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
            
            if self.smart_bg.is_animation_running():
                self.smart_bg.set_weather_type(animation_type)
            else:
                self.smart_bg.start_animation(animation_type)
        except Exception as e:
            print(f"❌ Animation error: {e}")

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        text_color = self.get_text_color()
        for widget in self.scrollable_frame.winfo_children():
            self._update_widget_colors(widget, text_color)
        if hasattr(self, 'temp_c') and self.temp_c is not None:
            self.fetch_and_display()

    def _update_widget_colors(self, widget, text_color):
        try:
            if isinstance(widget, tk.Label):
                widget.configure(fg=text_color)
            elif hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    self._update_widget_colors(child, text_color)
        except:
            pass

    def toggle_unit(self):
        self.unit = "F" if self.unit == "C" else "C"
        self.fetch_and_display()

    def _update_weather_icon(self, icon_code):
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
            self.icon_label.configure(text="🌤️", image="")

    def on_close(self):
        if self.smart_bg:
            try:
                self.smart_bg.stop_animation()
            except:
                pass
        self.destroy()


def run_app():
    try:
        print("🚀 Starting Weather App with WORKING ANIMATIONS...")
        app = WeatherApp()
        print("✅ App started successfully")
        app.mainloop()
    except Exception as e:
        print(f"💥 Error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    run_app()