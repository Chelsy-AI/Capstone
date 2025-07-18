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
try:
    from gui.weather_animation import WeatherAnimation
    ANIMATION_AVAILABLE = True
    print("✅ Weather animation loaded successfully")
except ImportError:
    print("⚠️ Weather animation module not found. Using fallback.")
    ANIMATION_AVAILABLE = False


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Weather App")
        self.geometry("900x700")
        self.configure(bg="#87CEEB")

        self.city_var = tk.StringVar(value="New York")
        self.unit = "C"
        self.temp_c = None
        self.temp_f = None
        self.metric_value_labels = {}
        self.icon_cache = {}
        self.current_weather_condition = "rain"
        self.history_data = {}

        # Create animation canvas as background
        self.bg_canvas = tk.Canvas(self, highlightthickness=0, bg="#87CEEB")
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Initialize weather animation
        if ANIMATION_AVAILABLE:
            self.smart_background = WeatherAnimation(self.bg_canvas)
            print("🎬 Starting rain animation...")
            self.smart_background.start_animation("rain")
        else:
            self.smart_background = None

        # Create text overlay frame directly on the main window (NOT on canvas)
        self.text_frame = tk.Frame(self, bg="")
        self.text_frame.place(x=0, y=0, relwidth=1, relheight=1)

        # Make frame transparent by using system default background
        try:
            self.text_frame.configure(bg=self.cget('bg'))
        except:
            pass

        # Build GUI
        self.build_gui()

        # Start weather updates
        self.after(2000, lambda: threading.Thread(target=self.safe_update_weather, daemon=True).start())

        # Handle window events
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind("<Configure>", self.on_window_resize)

    def build_gui(self):
        """Build text interface that floats over animation"""
        
        # Clear existing widgets in text frame
        for widget in self.text_frame.winfo_children():
            widget.destroy()

        # Create scrollable area
        canvas = tk.Canvas(self.text_frame, highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(self.text_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Configure canvas to be transparent
        try:
            canvas.configure(bg=self.cget('bg'))
            scrollable_frame.configure(bg=self.cget('bg'))
        except:
            canvas.configure(bg="#87CEEB")
            scrollable_frame.configure(bg="#87CEEB")

        self.metric_value_labels = {}
        row = 0

        # Title
        title_label = tk.Label(
            scrollable_frame,
            text="🌤️ Weather Dashboard",
            font=("Arial", 32, "bold"),
            fg="black",
            bg="#87CEEB"
        )
        title_label.grid(row=row, column=0, pady=30, padx=20)
        row += 1

        # City Entry
        city_label = tk.Label(
            scrollable_frame,
            text="🌍 Enter City:",
            font=("Arial", 18, "bold"),
            fg="black",
            bg="#87CEEB"
        )
        city_label.grid(row=row, column=0, pady=10, padx=20)
        row += 1

        self.city_entry = tk.Entry(
            scrollable_frame,
            textvariable=self.city_var,
            font=("Arial", 16),
            width=25,
            justify="center",
            bg="white",
            fg="black"
        )
        self.city_entry.grid(row=row, column=0, pady=10, padx=20)
        self.city_entry.bind("<Return>", lambda e: threading.Thread(target=self.safe_update_weather, daemon=True).start())
        row += 1

        # Temperature
        self.temp_label = tk.Label(
            scrollable_frame,
            text="Loading...",
            font=("Arial", 48, "bold"),
            fg="black",
            bg="#87CEEB",
            cursor="hand2"
        )
        self.temp_label.grid(row=row, column=0, pady=20, padx=20)
        self.temp_label.bind("<Button-1>", self.toggle_temp_unit)
        row += 1

        # Weather Description
        self.desc_label = tk.Label(
            scrollable_frame,
            text="Fetching weather...",
            font=("Arial", 20, "italic"),
            fg="black",
            bg="#87CEEB"
        )
        self.desc_label.grid(row=row, column=0, pady=10, padx=20)
        row += 1

        # Weather Icon
        self.icon_label = tk.Label(
            scrollable_frame,
            text="",
            bg="#87CEEB"
        )
        self.icon_label.grid(row=row, column=0, pady=10, padx=20)
        row += 1

        # Weather Details Title
        details_title = tk.Label(
            scrollable_frame,
            text="📊 Weather Details",
            font=("Arial", 20, "bold"),
            fg="black",
            bg="#87CEEB"
        )
        details_title.grid(row=row, column=0, pady=20, padx=20)
        row += 1

        # Weather Metrics Grid
        metrics_frame = tk.Frame(scrollable_frame, bg="#87CEEB")
        metrics_frame.grid(row=row, column=0, pady=10, padx=20)
        
        features = [
            ("humidity", "💧", "Humidity"),
            ("wind", "💨", "Wind"),
            ("pressure", "🧭", "Pressure"),
            ("visibility", "👁️", "Visibility"),
            ("uv", "🕶️", "UV Index"),
            ("precipitation", "☔", "Precipitation"),
        ]

        for i in range(3):
            metrics_frame.grid_columnconfigure(i, weight=1)

        for idx, (key, icon, label) in enumerate(features):
            r = idx // 3
            c = idx % 3
            
            container = tk.Frame(metrics_frame, bg="#87CEEB")
            container.grid(row=r, column=c, padx=10, pady=5, sticky="nsew")
            
            tk.Label(container, text=icon, font=("Arial", 24), fg="black", bg="#87CEEB").pack()
            tk.Label(container, text=label, font=("Arial", 12, "bold"), fg="black", bg="#87CEEB").pack()
            
            value_label = tk.Label(container, text="--", font=("Arial", 14), fg="black", bg="#87CEEB")
            value_label.pack()
            
            self.metric_value_labels[key] = value_label
        
        row += 1

        # Tomorrow's Prediction
        pred_title = tk.Label(
            scrollable_frame,
            text="🔮 Tomorrow's Prediction",
            font=("Arial", 18, "bold"),
            fg="black",
            bg="#87CEEB"
        )
        pred_title.grid(row=row, column=0, pady=20, padx=20)
        row += 1

        pred_frame = tk.Frame(scrollable_frame, bg="#87CEEB")
        pred_frame.grid(row=row, column=0, pady=10, padx=20)
        
        for i in range(3):
            pred_frame.grid_columnconfigure(i, weight=1)

        # Temperature prediction
        temp_frame = tk.Frame(pred_frame, bg="#87CEEB")
        temp_frame.grid(row=0, column=0, padx=10)
        tk.Label(temp_frame, text="🌡️", font=("Arial", 20), fg="black", bg="#87CEEB").pack()
        tk.Label(temp_frame, text="Temperature", font=("Arial", 10, "bold"), fg="black", bg="#87CEEB").pack()
        self.pred_temp_label = tk.Label(temp_frame, text="--", font=("Arial", 12), fg="black", bg="#87CEEB")
        self.pred_temp_label.pack()

        # Confidence
        conf_frame = tk.Frame(pred_frame, bg="#87CEEB")
        conf_frame.grid(row=0, column=1, padx=10)
        tk.Label(conf_frame, text="📊", font=("Arial", 20), fg="black", bg="#87CEEB").pack()
        tk.Label(conf_frame, text="Confidence", font=("Arial", 10, "bold"), fg="black", bg="#87CEEB").pack()
        self.pred_confidence_label = tk.Label(conf_frame, text="--", font=("Arial", 12), fg="black", bg="#87CEEB")
        self.pred_confidence_label.pack()

        # Accuracy
        acc_frame = tk.Frame(pred_frame, bg="#87CEEB")
        acc_frame.grid(row=0, column=2, padx=10)
        tk.Label(acc_frame, text="🎯", font=("Arial", 20), fg="black", bg="#87CEEB").pack()
        tk.Label(acc_frame, text="Accuracy", font=("Arial", 10, "bold"), fg="black", bg="#87CEEB").pack()
        self.pred_accuracy_label = tk.Label(acc_frame, text="--", font=("Arial", 12), fg="black", bg="#87CEEB")
        self.pred_accuracy_label.pack()

        row += 1

        # Weather History
        hist_title = tk.Label(
            scrollable_frame,
            text="📈 7-Day Weather History",
            font=("Arial", 18, "bold"),
            fg="black",
            bg="#87CEEB"
        )
        hist_title.grid(row=row, column=0, pady=20, padx=20)
        row += 1

        self.history_frame = tk.Frame(scrollable_frame, bg="#87CEEB")
        self.history_frame.grid(row=row, column=0, pady=10, padx=20)
        row += 1

        # Last Updated
        self.update_label = tk.Label(
            scrollable_frame,
            text="Starting up...",
            font=("Arial", 12),
            fg="black",
            bg="#87CEEB"
        )
        self.update_label.grid(row=row, column=0, pady=20, padx=20)
        row += 1

        # Theme Toggle
        theme_btn = tk.Button(
            scrollable_frame,
            text="🎨 Toggle Theme",
            command=self.toggle_theme,
            bg="darkgreen",
            fg="white",
            font=("Arial", 12, "bold")
        )
        theme_btn.grid(row=row, column=0, pady=20, padx=20)

        scrollable_frame.grid_columnconfigure(0, weight=1)
        print("[GUI] Built text overlay over animation background")

    def on_window_resize(self, event):
        """Handle window resize"""
        if event.widget == self and self.smart_background:
            self.smart_background.update_size(event.width, event.height)

    def toggle_theme(self):
        """Toggle theme - rebuild GUI"""
        print("🎨 Theme toggled")
        self.build_gui()

    def toggle_temp_unit(self, event=None):
        """Toggle between C and F"""
        self.unit = "F" if self.unit == "C" else "C"
        self.update_temperature_label()
        print(f"🌡️ Unit changed to: {self.unit}")

    def update_temperature_label(self):
        """Update temperature display"""
        if not hasattr(self, "temp_label"):
            return
        if self.temp_c is None:
            self.temp_label.configure(text="N/A")
        elif self.unit == "C":
            self.temp_label.configure(text=f"{self.temp_c}°C")
        else:
            self.temp_label.configure(text=f"{self.temp_f}°F")

    def safe_update_weather(self):
        """Safe weather update"""
        try:
            self.update_weather()
        except Exception as e:
            print(f"❌ Weather error: {e}")

    def update_weather(self):
        """Main weather update function"""
        city = self.city_var.get().strip() or "New York"
        print(f"🌍 Updating weather for: {city}")
        
        # Get weather data
        data = get_current_weather(city)
        self.history_data = fetch_world_history(city)

        if data.get("error"):
            print(f"❌ Error: {data['error']}")
            return

        # Update temperature
        temp_c = data.get("temperature")
        if temp_c is not None:
            self.temp_c = round(temp_c, 1)
            self.temp_f = round((temp_c * 9 / 5) + 32, 1)

        self.update_temperature_label()

        # Update description
        description = data.get("description", "No description")
        if hasattr(self, "desc_label"):
            self.desc_label.configure(text=description)

        # Update timestamp
        if hasattr(self, "update_label"):
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.update_label.configure(text=f"Updated: {timestamp}")

        # Update weather icon
        self._update_weather_icon(data.get("icon"))

        # Update metrics
        self._update_weather_metrics(data)

        # UPDATE ANIMATION BASED ON WEATHER
        weather_condition = description.lower() if description else "rain"
        animation_type = self.map_weather_to_animation(weather_condition)
        self.current_weather_condition = animation_type
        
        if self.smart_background:
            print(f"🎬 Changing animation to: {animation_type}")
            self.smart_background.set_weather_type(animation_type)

        # Update predictions and history
        self.update_tomorrow_prediction(city)
        self.update_weather_history()

    def map_weather_to_animation(self, weather_condition):
        """Map weather to animation type"""
        condition = weather_condition.lower()
        
        if any(word in condition for word in ["rain", "drizzle", "shower"]):
            return "rain"
        elif any(word in condition for word in ["snow", "blizzard", "sleet"]):
            return "snow"
        elif any(word in condition for word in ["thunder", "storm", "lightning"]):
            return "storm"
        elif any(word in condition for word in ["cloud", "overcast", "broken"]):
            return "cloudy"
        elif any(word in condition for word in ["sun", "sunny", "clear"]):
            return "sunny"
        elif any(word in condition for word in ["mist", "fog", "haze"]):
            return "mist"
        else:
            return "rain"

    def update_tomorrow_prediction(self, city):
        """Update prediction display"""
        try:
            predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)
            
            if hasattr(self, "pred_temp_label"):
                temp_display = f"{predicted_temp}°C" if predicted_temp else "N/A"
                if self.unit == "F" and predicted_temp:
                    temp_display = f"{round((predicted_temp * 9/5) + 32, 1)}°F"
                
                self.pred_temp_label.configure(text=temp_display)
                self.pred_confidence_label.configure(text=str(confidence))
                self.pred_accuracy_label.configure(text=f"{accuracy}%")
        except Exception as e:
            print(f"🔮 Prediction error: {e}")

    def update_weather_history(self):
        """Update history display"""
        if not hasattr(self, "history_frame"):
            return
            
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        if not isinstance(self.history_data, dict):
            return

        times = self.history_data.get("time", [])
        max_temps = self.history_data.get("temperature_2m_max", [])
        min_temps = self.history_data.get("temperature_2m_min", [])
        
        for col in range(min(7, len(times))):
            if col < len(times):
                date = times[col][-5:] if len(times[col]) > 5 else times[col]  # Get MM-DD
                max_temp = max_temps[col] if col < len(max_temps) else "N/A"
                min_temp = min_temps[col] if col < len(min_temps) else "N/A"
                
                if max_temp != "N/A":
                    max_temp = f"{round(max_temp)}°" if self.unit == "C" else f"{round(max_temp * 9/5 + 32)}°"
                if min_temp != "N/A":
                    min_temp = f"{round(min_temp)}°" if self.unit == "C" else f"{round(min_temp * 9/5 + 32)}°"
                
                tk.Label(self.history_frame, text=date, font=("Arial", 10, "bold"), fg="black", bg="#87CEEB").grid(row=0, column=col, padx=5)
                tk.Label(self.history_frame, text=f"↑{max_temp}", fg="red", bg="#87CEEB").grid(row=1, column=col, padx=5)
                tk.Label(self.history_frame, text=f"↓{min_temp}", fg="blue", bg="#87CEEB").grid(row=2, column=col, padx=5)

    def _update_weather_icon(self, icon_code):
        """Update weather icon"""
        if not icon_code or not hasattr(self, "icon_label"):
            return

        try:
            url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            pil_img = Image.open(BytesIO(response.content))
            icon_image = ImageTk.PhotoImage(pil_img)
            self.icon_label.configure(image=icon_image)
            self.icon_label.image = icon_image
        except:
            self.icon_label.configure(text="🌤️")

    def _update_weather_metrics(self, data):
        """Update weather metrics"""
        metrics = {
            "humidity": f"{data.get('humidity')}%" if data.get("humidity") else "N/A",
            "wind": f"{data.get('wind_speed')} m/s" if data.get("wind_speed") else "N/A",
            "pressure": f"{data.get('pressure')} hPa" if data.get("pressure") else "N/A",
            "visibility": f"{data.get('visibility')} m" if data.get("visibility") else "N/A",
            "uv": str(data.get("uv_index")) if data.get("uv_index") else "N/A",
            "precipitation": f"{data.get('precipitation')} mm" if data.get("precipitation") else "N/A",
        }

        for key, val in metrics.items():
            if key in self.metric_value_labels:
                self.metric_value_labels[key].configure(text=val)

    def on_close(self):
        """Handle app close"""
        print("👋 Closing app...")
        if self.smart_background:
            self.smart_background.stop_animation()
        self.destroy()


def run_app():
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