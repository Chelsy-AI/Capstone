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
        self.max_scroll = 500  # Increased to accommodate more content
        
        # Store widget references to prevent garbage collection
        self.widgets = []
        
        # Build GUI
        self.build_gui()
        
        # Auto-load weather
        self.after(1000, self.fetch_and_display)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_gui(self):
        """Build responsive GUI with centered, scalable layout"""
        
        # Clear existing widgets but preserve canvas and scrollbar
        for widget in self.winfo_children():
            if not hasattr(widget, '_preserve') and widget != getattr(self, 'bg_canvas', None) and widget != getattr(self, 'scrollbar', None):
                widget.destroy()
        self.widgets.clear()
        
        # Bind resize event to handle responsive layout
        self.bind("<Configure>", self._on_window_resize)
        
        # === Animation Background ===
        if not hasattr(self, 'bg_canvas'):
            self.bg_canvas = tk.Canvas(self, highlightthickness=0, bg="#87CEEB")
            self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_canvas._preserve = True
            
            try:
                self.smart_bg = WeatherAnimation(self.bg_canvas)
                self.after(500, lambda: self.smart_bg.start_animation("clear"))
                print("🎬 Animation ready")
            except Exception as e:
                print(f"❌ Animation failed: {e}")
                self.smart_bg = None

        # Add scrollbar
        if not hasattr(self, 'scrollbar'):
            self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._on_scroll)
            self.scrollbar.place(relx=0.98, y=0, relheight=1, width=20)
            self.scrollbar._preserve = True

            # Bind mousewheel
            self.bind_all("<MouseWheel>", self._on_mousewheel)
            self.bind_all("<Button-4>", self._on_mousewheel)
            self.bind_all("<Button-5>", self._on_mousewheel)

        # Build responsive layout
        self._build_responsive_layout()

        print("[GUI] Responsive centered GUI ready")

    def _build_responsive_layout(self):
        """Build the responsive, centered layout"""
        # Get current window dimensions
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        
        # === RESPONSIVE WEATHER METRICS LAYOUT ===
        
        # Calculate responsive positioning for weather metrics only (6 columns)
        metrics_count = 6  # humidity, wind, pressure, visibility, uv, precipitation
        
        # Calculate column width based on window size
        available_width = window_width - 40  # Leave 20px margin on each side
        col_width = available_width / metrics_count
        
        # Center the entire metrics row
        start_x = 20  # Left margin
        
        # Row 1: Headers (Weather Metrics Only)
        metric_headers = ["Humidity", "Wind", "Press.", "Visibility", "UV Index", "Precip."]
        for i, header in enumerate(metric_headers):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            header_widget = tk.Label(
                self, text=header, 
                font=("Arial", int(10 + window_width/100), "bold"), 
                fg=self.text_color, bg="#87CEEB",
                anchor="center"
            )
            header_widget.place(x=x_pos, y=30 - self.scroll_offset, anchor="center")
            self.widgets.append(header_widget)
        
        # Row 2: Emojis (Weather Metrics Only)
        metric_emojis = ["💧", "🌬️", "🧭", "👁️", "☀️", "🌧️"]
        for i, emoji in enumerate(metric_emojis):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            emoji_widget = tk.Label(
                self, text=emoji, 
                font=("Arial", int(16 + window_width/80)), 
                bg="#87CEEB",
                anchor="center"
            )
            emoji_widget.place(x=x_pos, y=55 - self.scroll_offset, anchor="center")
            self.widgets.append(emoji_widget)
        
        # Row 3: Values (Weather Metrics Only)
        value_positions = []
        for i in range(metrics_count):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            value_positions.append((x_pos, 80 - self.scroll_offset))
        
        self.humidity_value = tk.Label(
            self, text="--", 
            font=("Arial", int(10 + window_width/120)), 
            fg=self.text_color, bg="#87CEEB", anchor="center"
        )
        self.humidity_value.place(x=value_positions[0][0], y=value_positions[0][1], anchor="center")
        self.widgets.append(self.humidity_value)
        
        self.wind_value = tk.Label(
            self, text="--", 
            font=("Arial", int(10 + window_width/120)), 
            fg=self.text_color, bg="#87CEEB", anchor="center"
        )
        self.wind_value.place(x=value_positions[1][0], y=value_positions[1][1], anchor="center")
        self.widgets.append(self.wind_value)
        
        self.pressure_value = tk.Label(
            self, text="--", 
            font=("Arial", int(10 + window_width/120)), 
            fg=self.text_color, bg="#87CEEB", anchor="center"
        )
        self.pressure_value.place(x=value_positions[2][0], y=value_positions[2][1], anchor="center")
        self.widgets.append(self.pressure_value)
        
        self.visibility_value = tk.Label(
            self, text="--", 
            font=("Arial", int(10 + window_width/120)), 
            fg=self.text_color, bg="#87CEEB", anchor="center"
        )
        self.visibility_value.place(x=value_positions[3][0], y=value_positions[3][1], anchor="center")
        self.widgets.append(self.visibility_value)
        
        self.uv_value = tk.Label(
            self, text="--", 
            font=("Arial", int(10 + window_width/120)), 
            fg=self.text_color, bg="#87CEEB", anchor="center"
        )
        self.uv_value.place(x=value_positions[4][0], y=value_positions[4][1], anchor="center")
        self.widgets.append(self.uv_value)
        
        self.precipitation_value = tk.Label(
            self, text="--", 
            font=("Arial", int(10 + window_width/120)), 
            fg=self.text_color, bg="#87CEEB", anchor="center"
        )
        self.precipitation_value.place(x=value_positions[5][0], y=value_positions[5][1], anchor="center")
        self.widgets.append(self.precipitation_value)

        # === CENTERED CONTROLS ===
        
        # Toggle Theme Button (centered)
        self.theme_btn = tk.Button(
            self,
            text="Toggle Theme",
            command=self.toggle_theme,
            bg="darkblue",
            fg="white",
            font=("Arial", int(10 + window_width/120), "bold")
        )
        self.theme_btn.place(x=window_width/2, y=120 - self.scroll_offset, anchor="center")
        self.widgets.append(self.theme_btn)

        # City Input (centered) - removed "City:" label
        self.city_entry = tk.Entry(
            self,
            textvariable=self.city_var,
            font=("Arial", int(14 + window_width/80)),
            width=max(15, int(window_width/50)),
            justify="center",
            bg="white",
            fg="black"
        )
        self.city_entry.place(x=window_width/2, y=160 - self.scroll_offset, anchor="center")
        self.city_entry.bind("<Return>", lambda e: self.fetch_and_display())
        self.widgets.append(self.city_entry)

        # === CENTERED WEATHER DISPLAY ===
        
        # Weather Icon (centered)
        self.icon_label = tk.Label(
            self, text="🌤️", 
            font=("Arial", int(40 + window_width/25)), 
            bg="#87CEEB",
            anchor="center"
        )
        self.icon_label.place(x=window_width/2, y=220 - self.scroll_offset, anchor="center")
        self.widgets.append(self.icon_label)

        # Temperature (centered)
        self.temp_label = tk.Label(
            self,
            text="Loading...",
            font=("Arial", int(40 + window_width/25), "bold"),
            fg=self.text_color,
            bg="#87CEEB",
            cursor="hand2",
            anchor="center"
        )
        self.temp_label.place(x=window_width/2, y=290 - self.scroll_offset, anchor="center")
        self.temp_label.bind("<Button-1>", lambda e: self.toggle_unit())
        self.widgets.append(self.temp_label)

        # Description (centered)
        self.desc_label = tk.Label(
            self,
            text="Fetching weather...",
            font=("Arial", int(16 + window_width/60)),
            fg=self.text_color,
            bg="#87CEEB",
            anchor="center"
        )
        self.desc_label.place(x=window_width/2, y=350 - self.scroll_offset, anchor="center")
        self.widgets.append(self.desc_label)

        # === TOMORROW'S PREDICTION SECTION (MOVED BELOW TODAY'S WEATHER) ===
        
        # Tomorrow's Prediction Title
        prediction_title = tk.Label(
            self, text="Tomorrow's Prediction", 
            font=("Arial", int(18 + window_width/60), "bold"), 
            fg=self.text_color, bg="#87CEEB",
            anchor="center"
        )
        prediction_title.place(x=window_width/2, y=410 - self.scroll_offset, anchor="center")
        self.widgets.append(prediction_title)

        # Prediction metrics layout (3 columns)
        prediction_count = 3
        pred_col_width = available_width / prediction_count
        pred_start_x = 20
        
        # Prediction Headers
        prediction_headers = ["Temperature", "Accuracy", "Confidence"]
        for i, header in enumerate(prediction_headers):
            x_pos = pred_start_x + (i * pred_col_width) + (pred_col_width / 2)
            header_widget = tk.Label(
                self, text=header, 
                font=("Arial", int(10 + window_width/100), "bold"), 
                fg=self.text_color, bg="#87CEEB",
                anchor="center"
            )
            header_widget.place(x=x_pos, y=440 - self.scroll_offset, anchor="center")
            self.widgets.append(header_widget)
        
        # Prediction Emojis
        prediction_emojis = ["🌡️", "💯", "😎"]
        for i, emoji in enumerate(prediction_emojis):
            x_pos = pred_start_x + (i * pred_col_width) + (pred_col_width / 2)
            emoji_widget = tk.Label(
                self, text=emoji, 
                font=("Arial", int(16 + window_width/80)), 
                bg="#87CEEB",
                anchor="center"
            )
            emoji_widget.place(x=x_pos, y=465 - self.scroll_offset, anchor="center")
            self.widgets.append(emoji_widget)

        # Prediction Values
        prediction_positions = []
        for i in range(prediction_count):
            x_pos = pred_start_x + (i * pred_col_width) + (pred_col_width / 2)
            prediction_positions.append((x_pos, 490 - self.scroll_offset))
        
        self.temp_prediction = tk.Label(
            self, text="--", 
            font=("Arial", int(10 + window_width/120)), 
            fg=self.text_color, bg="#87CEEB", anchor="center"
        )
        self.temp_prediction.place(x=prediction_positions[0][0], y=prediction_positions[0][1], anchor="center")
        self.widgets.append(self.temp_prediction)
        
        self.accuracy_prediction = tk.Label(
            self, text="--", 
            font=("Arial", int(10 + window_width/120)), 
            fg=self.text_color, bg="#87CEEB", anchor="center"
        )
        self.accuracy_prediction.place(x=prediction_positions[1][0], y=prediction_positions[1][1], anchor="center")
        self.widgets.append(self.accuracy_prediction)
        
        self.confidence_prediction = tk.Label(
            self, text="--", 
            font=("Arial", int(10 + window_width/120)), 
            fg=self.text_color, bg="#87CEEB", anchor="center"
        )
        self.confidence_prediction.place(x=prediction_positions[2][0], y=prediction_positions[2][1], anchor="center")
        self.widgets.append(self.confidence_prediction)

        # === CENTERED HISTORY TITLE ===
        
        # 7-Day History
        history_title = tk.Label(
            self, text="7-Day History", 
            font=("Arial", int(18 + window_width/60), "bold"), 
            fg=self.text_color, bg="#87CEEB",
            anchor="center"
        )
        history_title.place(x=window_width/2, y=550 - self.scroll_offset, anchor="center")
        self.widgets.append(history_title)

        # History labels will be created in update_history_display
        self.history_labels = []

    def _on_window_resize(self, event):
        """Handle window resize events"""
        if event.widget == self:
            # Rebuild layout when window is resized
            self.after_idle(self._rebuild_layout_on_resize)

    def _rebuild_layout_on_resize(self):
        """Rebuild the layout when window is resized"""
        try:
            # Clear existing widgets first to prevent duplicates
            for widget in self.winfo_children():
                if widget != self.bg_canvas and widget != self.scrollbar:
                    widget.destroy()
            self.widgets.clear()
            
            # Clear history labels
            self.history_labels.clear()
            
            # Rebuild layout
            self._build_responsive_layout()
            
            # Restore current data
            if self.current_weather_data:
                self.update_weather_display(self.current_weather_data)
            if self.current_prediction_data:
                predicted_temp, confidence, accuracy = self.current_prediction_data
                self.update_tomorrow_prediction_direct(predicted_temp, confidence, accuracy)
            if self.current_history_data:
                self._restore_history_data()
        except Exception as e:
            print(f"❌ Resize error: {e}")

    def _restore_history_data(self):
        """Restore history data without fetching again"""
        try:
            if not self.current_history_data:
                return
                
            window_width = self.winfo_width()
            days_to_show = len(self.current_history_data)
            
            for col, (date, max_temp, min_temp, unit_symbol, avg_temp) in enumerate(self.current_history_data):
                if col >= 7:  # Limit to 7 days
                    break
                    
                font_size = int(10 + window_width/120)
                
                # Create labels for this day
                date_label = tk.Label(
                    self, text=f"📅 {date}", 
                    font=("Arial", font_size, "bold"),
                    fg=self.text_color, bg="#87CEEB", anchor="center"
                )
                self.history_labels.append(date_label)
                
                max_label = tk.Label(
                    self, text=f"🔺 {max_temp}{unit_symbol}", 
                    font=("Arial", font_size),
                    fg=self.text_color, bg="#87CEEB", anchor="center"
                )
                self.history_labels.append(max_label)
                
                min_label = tk.Label(
                    self, text=f"🔻 {min_temp}{unit_symbol}", 
                    font=("Arial", font_size),
                    fg=self.text_color, bg="#87CEEB", anchor="center"
                )
                self.history_labels.append(min_label)
                
                if avg_temp:
                    avg_label = tk.Label(
                        self, text=f"🌡️ {avg_temp}{unit_symbol}", 
                        font=("Arial", font_size),
                        fg=self.text_color, bg="#87CEEB", anchor="center"
                    )
                    self.history_labels.append(avg_label)
            
            # Position the history labels
            self._update_history_positions()
            
        except Exception as e:
            print(f"❌ History restore error: {e}")

    def update_tomorrow_prediction_direct(self, predicted_temp, confidence, accuracy):
        """Update prediction values directly without fetching"""
        try:
            # Update temperature display
            if predicted_temp:
                if self.unit == "C":
                    temp_text = f"{predicted_temp}°C"
                else:
                    temp_f = round((predicted_temp * 9/5) + 32, 1)
                    temp_text = f"{temp_f}°F"
                
                self.temp_prediction.configure(text=temp_text)
            else:
                self.temp_prediction.configure(text="--")
            
            # Update accuracy display
            if isinstance(accuracy, (int, float)):
                self.accuracy_prediction.configure(text=f"{accuracy}%")
            else:
                self.accuracy_prediction.configure(text="--")
            
            # Update confidence display
            if confidence and confidence != "N/A":
                conf_text = str(confidence).replace('%', '') + '%'
                self.confidence_prediction.configure(text=conf_text)
            else:
                self.confidence_prediction.configure(text="--")
                
        except Exception as e:
            print(f"❌ Direct prediction update error: {e}")

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
        """Update all widget positions based on scroll offset - ALL elements scroll consistently"""
        try:
            window_width = self.winfo_width()
            
            # Calculate responsive positioning values
            metrics_count = 6
            available_width = window_width - 40
            col_width = available_width / metrics_count
            start_x = 20
            
            # For prediction section (3 columns)
            prediction_count = 3
            pred_col_width = available_width / prediction_count
            pred_start_x = 20
            
            # Define base Y positions for ALL elements (before scroll offset)
            base_positions = {
                # Weather metrics
                'metric_headers': 30,
                'metric_emojis': 55,
                'metric_values': 80,
                # Controls
                'theme_btn': 120,
                'city_entry': 160,
                # Today's weather
                'icon_label': 220,
                'temp_label': 290,
                'desc_label': 350,
                # Tomorrow's prediction
                'prediction_title': 410,
                'prediction_headers': 440,
                'prediction_emojis': 465,
                'prediction_values': 490,
                # History
                'history_title': 550,
                'history_start': 590
            }
            
            # Update ALL widgets in the widgets list with consistent scrolling
            for i, widget in enumerate(self.widgets):
                try:
                    place_info = widget.place_info()
                    if place_info:
                        current_x = float(place_info.get('x', 0))
                        
                        # Determine base Y position based on widget index and type
                        if i < 6:  # Weather metric headers
                            base_y = base_positions['metric_headers']
                        elif i < 12:  # Weather metric emojis
                            base_y = base_positions['metric_emojis']
                        elif i < 18:  # Weather metric values
                            base_y = base_positions['metric_values']
                        elif i == 18:  # Theme button
                            base_y = base_positions['theme_btn']
                        elif i == 19:  # City entry
                            base_y = base_positions['city_entry']
                        elif i == 20:  # Icon label
                            base_y = base_positions['icon_label']
                        elif i == 21:  # Temp label
                            base_y = base_positions['temp_label']
                        elif i == 22:  # Description label
                            base_y = base_positions['desc_label']
                        elif i == 23:  # Prediction title
                            base_y = base_positions['prediction_title']
                        elif i < 27:  # Prediction headers
                            base_y = base_positions['prediction_headers']
                        elif i < 30:  # Prediction emojis
                            base_y = base_positions['prediction_emojis']
                        elif i < 33:  # Prediction values
                            base_y = base_positions['prediction_values']
                        elif i == 33:  # History title
                            base_y = base_positions['history_title']
                        else:
                            # For any other widgets, maintain relative positioning
                            base_y = float(place_info.get('y', 0)) + self.scroll_offset
                        
                        # Apply scroll offset consistently
                        new_y = base_y - self.scroll_offset
                        widget.place(x=current_x, y=new_y, anchor="center")
                        
                except Exception:
                    pass
            
            # Update specific named widgets with consistent scrolling
            named_widgets = [
                (getattr(self, 'humidity_value', None), start_x + (0 * col_width) + (col_width / 2), base_positions['metric_values']),
                (getattr(self, 'wind_value', None), start_x + (1 * col_width) + (col_width / 2), base_positions['metric_values']),
                (getattr(self, 'pressure_value', None), start_x + (2 * col_width) + (col_width / 2), base_positions['metric_values']),
                (getattr(self, 'visibility_value', None), start_x + (3 * col_width) + (col_width / 2), base_positions['metric_values']),
                (getattr(self, 'uv_value', None), start_x + (4 * col_width) + (col_width / 2), base_positions['metric_values']),
                (getattr(self, 'precipitation_value', None), start_x + (5 * col_width) + (col_width / 2), base_positions['metric_values']),
                (getattr(self, 'theme_btn', None), window_width / 2, base_positions['theme_btn']),
                (getattr(self, 'city_entry', None), window_width / 2, base_positions['city_entry']),
                (getattr(self, 'icon_label', None), window_width / 2, base_positions['icon_label']),
                (getattr(self, 'temp_label', None), window_width / 2, base_positions['temp_label']),
                (getattr(self, 'desc_label', None), window_width / 2, base_positions['desc_label']),
                (getattr(self, 'temp_prediction', None), pred_start_x + (0 * pred_col_width) + (pred_col_width / 2), base_positions['prediction_values']),
                (getattr(self, 'accuracy_prediction', None), pred_start_x + (1 * pred_col_width) + (pred_col_width / 2), base_positions['prediction_values']),
                (getattr(self, 'confidence_prediction', None), pred_start_x + (2 * pred_col_width) + (pred_col_width / 2), base_positions['prediction_values']),
            ]
            
            # Apply consistent scrolling to all named widgets
            for widget, x, base_y in named_widgets:
                if widget:
                    try:
                        new_y = base_y - self.scroll_offset
                        widget.place(x=x, y=new_y, anchor="center")
                    except Exception:
                        pass
            
            # Update history labels with consistent scrolling
            self._update_history_positions()
                
        except Exception as e:
            print(f"❌ Position update error: {e}")

    def _update_history_positions(self):
        """Update history label positions for responsive layout"""
        try:
            window_width = self.winfo_width()
            start_y = 590  # Updated to match base_positions
            
            # Calculate responsive positioning for history
            history_count = min(7, len(self.history_labels) // 4) if self.history_labels else 0
            if history_count > 0:
                available_width = window_width - 40
                col_width = available_width / history_count
                start_x = 20
                
                for col in range(history_count):
                    col_start_idx = col * 4
                    if col_start_idx + 3 < len(self.history_labels):
                        x_pos = start_x + (col * col_width) + (col_width / 2)
                        
                        # Apply consistent scroll offset to all history elements
                        # Date label
                        self.history_labels[col_start_idx].place(
                            x=x_pos, y=start_y - self.scroll_offset, anchor="center"
                        )
                        # Max temp
                        self.history_labels[col_start_idx + 1].place(
                            x=x_pos, y=(start_y + 25) - self.scroll_offset, anchor="center"
                        )
                        # Min temp
                        self.history_labels[col_start_idx + 2].place(
                            x=x_pos, y=(start_y + 50) - self.scroll_offset, anchor="center"
                        )
                        # Avg temp
                        if col_start_idx + 3 < len(self.history_labels):
                            self.history_labels[col_start_idx + 3].place(
                                x=x_pos, y=(start_y + 75) - self.scroll_offset, anchor="center"
                            )
        except Exception as e:
            print(f"❌ History position update error: {e}")

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
        """Update tomorrow's prediction metrics"""
        try:
            predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)
            
            # Store data for preservation
            self.current_prediction_data = (predicted_temp, confidence, accuracy)
            
            # Update using the direct method
            self.update_tomorrow_prediction_direct(predicted_temp, confidence, accuracy)
                
        except Exception as e:
            print(f"❌ Prediction error: {e}")

    def update_history_display(self, city):
        """Update 7-day history with responsive layout"""
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
                
                window_width = self.winfo_width()
                days_to_show = min(7, len(times))
                
                for col in range(days_to_show):
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
                        
                        # Create responsive positioned labels
                        font_size = int(10 + window_width/120)
                        
                        # Date with emoji
                        date_label = tk.Label(
                            self, text=f"📅 {date}", 
                            font=("Arial", font_size, "bold"),
                            fg=self.text_color, bg="#87CEEB", anchor="center"
                        )
                        self.history_labels.append(date_label)
                        
                        # Max temp with emoji
                        max_label = tk.Label(
                            self, text=f"🔺 {max_temp}{unit_symbol}", 
                            font=("Arial", font_size),
                            fg=self.text_color, bg="#87CEEB", anchor="center"
                        )
                        self.history_labels.append(max_label)
                        
                        # Min temp with emoji
                        min_label = tk.Label(
                            self, text=f"🔻 {min_temp}{unit_symbol}", 
                            font=("Arial", font_size),
                            fg=self.text_color, bg="#87CEEB", anchor="center"
                        )
                        self.history_labels.append(min_label)
                        
                        # Average temp with emoji
                        if avg_temp:
                            avg_label = tk.Label(
                                self, text=f"🌡️ {avg_temp}{unit_symbol}", 
                                font=("Arial", font_size),
                                fg=self.text_color, bg="#87CEEB", anchor="center"
                            )
                            self.history_labels.append(avg_label)
                
                # Position the history labels responsively
                self._update_history_positions()
                        
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
        print("🚀 Starting Weather App with Responsive Layout...")
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