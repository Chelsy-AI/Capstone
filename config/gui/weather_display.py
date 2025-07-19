import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import requests


class WeatherDisplay:
    """
    Weather Display Manager
    
    Handles all weather data visualization including current weather,
    predictions, history, and weather icon updates.
    """
    
    def __init__(self, app, gui_controller):
        self.app = app
        self.gui = gui_controller

    def _get_canvas_bg_color(self):
        """Get the current canvas background color"""
        try:
            if self.gui.bg_canvas:
                return self.gui.bg_canvas.cget("bg")
            return "#87CEEB"  # Default fallback
        except:
            return "#87CEEB"  # Safe fallback

    def update_weather_display(self, weather_data):
        """Update the main weather display with current data"""
        try:
            print("[WeatherDisplay] Updating weather display...")
            
            # Update temperature display
            self._update_temperature_display(weather_data)
            
            # Update weather description
            self._update_description_display(weather_data)
            
            # Update weather metrics (humidity, wind, etc.)
            self._update_weather_metrics(weather_data)
            
            # Update weather icon
            self._update_weather_icon(weather_data.get("icon"))
            
            description = weather_data.get("description", "No description")
            print(f"✅ Weather display updated: {description}")
            
        except Exception as e:
            print(f"❌ Weather display update error: {e}")

    def _update_temperature_display(self, weather_data):
        """Update temperature labels"""
        temp_c = weather_data.get("temperature")
        if temp_c is not None and self.gui.temp_label:
            self.app.temp_c = round(temp_c, 1)
            self.app.temp_f = round((temp_c * 9 / 5) + 32, 1)
            
            if self.app.unit == "C":
                self.gui.temp_label.configure(text=f"{self.app.temp_c}°C")
            else:
                self.gui.temp_label.configure(text=f"{self.app.temp_f}°F")

    def _update_description_display(self, weather_data):
        """Update weather description"""
        if self.gui.desc_label:
            description = weather_data.get("description", "No description")
            self.gui.desc_label.configure(text=description)

    def _update_weather_metrics(self, weather_data):
        """Update weather metrics display (humidity, wind, etc.)"""
        # Extract metric data
        humidity = weather_data.get("humidity", "N/A")
        wind = weather_data.get("wind_speed", "N/A")
        pressure = weather_data.get("pressure", "N/A")
        visibility = weather_data.get("visibility", "N/A")
        uv = weather_data.get("uv_index", "N/A")
        precipitation = weather_data.get("precipitation", "N/A")
        
        # Update metric widgets if they exist
        metric_updates = [
            (self.gui.humidity_value, f"{humidity}%" if humidity != "N/A" else "--"),
            (self.gui.wind_value, f"{wind} m/s" if wind != "N/A" else "--"),
            (self.gui.pressure_value, f"{pressure} hPa" if pressure != "N/A" else "--"),
            (self.gui.visibility_value, f"{visibility} m" if visibility != "N/A" else "--"),
            (self.gui.uv_value, f"{uv}" if uv != "N/A" else "--"),
            (self.gui.precipitation_value, f"{precipitation} mm" if precipitation != "N/A" else "--")
        ]
        
        for widget, text in metric_updates:
            if widget:
                widget.configure(text=text)

    def _update_weather_icon(self, icon_code):
        """Update weather icon from API or fallback to emoji"""
        if not icon_code or not self.gui.icon_label:
            return
            
        try:
            # Try to fetch icon from OpenWeatherMap
            url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            # Create image from response
            pil_img = Image.open(BytesIO(response.content))
            icon_image = ImageTk.PhotoImage(pil_img)
            
            # Update label with image
            self.gui.icon_label.configure(image=icon_image, text="")
            self.gui.icon_label.image = icon_image  # Keep reference
            
        except Exception as e:
            print(f"Icon fetch error: {e}")
            # Fallback to emoji
            self.gui.icon_label.configure(text="🌤️", image="")

    def update_tomorrow_prediction_direct(self, predicted_temp, confidence, accuracy):
        """Update tomorrow's prediction display"""
        try:
            print("[WeatherDisplay] Updating prediction display...")
            
            # Update temperature prediction
            if self.gui.temp_prediction:
                if predicted_temp:
                    if self.app.unit == "C":
                        temp_text = f"{predicted_temp}°C"
                    else:
                        temp_f = round((predicted_temp * 9/5) + 32, 1)
                        temp_text = f"{temp_f}°F"
                    self.gui.temp_prediction.configure(text=temp_text)
                else:
                    self.gui.temp_prediction.configure(text="--")
            
            # Update accuracy prediction
            if self.gui.accuracy_prediction:
                if isinstance(accuracy, (int, float)):
                    self.gui.accuracy_prediction.configure(text=f"{accuracy}%")
                else:
                    self.gui.accuracy_prediction.configure(text="--")
            
            # Update confidence prediction
            if self.gui.confidence_prediction:
                if confidence and confidence != "N/A":
                    conf_text = str(confidence).replace('%', '') + '%'
                    self.gui.confidence_prediction.configure(text=conf_text)
                else:
                    self.gui.confidence_prediction.configure(text="--")
                    
            print("✅ Prediction display updated")
                    
        except Exception as e:
            print(f"❌ Prediction update error: {e}")

    def update_history_display(self, city):
        """Update 7-day history display"""
        try:
            print(f"[WeatherDisplay] Updating history for {city}...")
            
            # Clear old history
            self._clear_history_labels()
            
            # Fetch new history data
            from features.history_tracker.api import fetch_world_history
            history_data = fetch_world_history(city)
            
            if history_data and "time" in history_data:
                self._create_history_labels(history_data)
                self._position_history_labels()
            
            print("✅ History display updated")
            
        except Exception as e:
            print(f"❌ History update error: {e}")

    def _clear_history_labels(self):
        """Clear existing history labels"""
        for label in self.gui.history_labels:
            label.destroy()
        self.gui.history_labels.clear()
        self.app.current_history_data.clear()

    def _create_history_labels(self, history_data):
        """Create history labels from data"""
        times = history_data.get("time", [])
        max_temps = history_data.get("temperature_2m_max", [])
        min_temps = history_data.get("temperature_2m_min", [])
        
        window_width = self.app.winfo_width()
        days_to_show = min(7, len(times))
        
        for col in range(days_to_show):
            if col < len(max_temps) and col < len(min_temps):
                # Process temperature data
                date = times[col][-5:] if len(times[col]) > 5 else times[col]
                max_temp = max_temps[col]
                min_temp = min_temps[col]
                avg_temp = round((max_temp + min_temp) / 2, 1) if max_temp and min_temp else None
                
                # Convert units if needed
                if self.app.unit == "F":
                    max_temp = round(max_temp * 9/5 + 32, 1)
                    min_temp = round(min_temp * 9/5 + 32, 1)
                    avg_temp = round(avg_temp * 9/5 + 32, 1) if avg_temp else None
                else:
                    max_temp = round(max_temp, 1)
                    min_temp = round(min_temp, 1)
                
                unit_symbol = "°F" if self.app.unit == "F" else "°C"
                
                # Store data for preservation
                self.app.current_history_data.append((date, max_temp, min_temp, unit_symbol, avg_temp))
                
                # Create labels
                self._create_history_labels_for_day(date, max_temp, min_temp, avg_temp, unit_symbol, window_width)

    def _create_history_labels_for_day(self, date, max_temp, min_temp, avg_temp, unit_symbol, window_width):
        """Create labels for a single day's history with canvas background color"""
        font_size = int(10 + window_width/120)
        bg_color = self._get_canvas_bg_color()
        
        # Date label - canvas background color
        date_label = tk.Label(
            self.app,  # Place on main app for proper event handling
            text=f"📅 {date}",
            font=("Arial", font_size, "bold"),
            fg=self.app.text_color, 
            bg=bg_color,  # Use canvas background color
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        self.gui.history_labels.append(date_label)
        
        # Max temperature label - canvas background color
        max_label = tk.Label(
            self.app,  # Place on main app for proper event handling
            text=f"🔺 {max_temp}{unit_symbol}",
            font=("Arial", font_size),
            fg=self.app.text_color, 
            bg=bg_color,  # Use canvas background color
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        self.gui.history_labels.append(max_label)
        
        # Min temperature label - canvas background color
        min_label = tk.Label(
            self.app,  # Place on main app for proper event handling
            text=f"🔻 {min_temp}{unit_symbol}",
            font=("Arial", font_size),
            fg=self.app.text_color, 
            bg=bg_color,  # Use canvas background color
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        self.gui.history_labels.append(min_label)
        
        # Average temperature label - canvas background color
        if avg_temp:
            avg_label = tk.Label(
                self.app,  # Place on main app for proper event handling
                text=f"🌡️ {avg_temp}{unit_symbol}",
                font=("Arial", font_size),
                fg=self.app.text_color, 
                bg=bg_color,  # Use canvas background color
                anchor="center",
                relief="flat",
                borderwidth=0
            )
            self.gui.history_labels.append(avg_label)

    def _position_history_labels(self):
        """Position history labels responsively"""
        # Delegate to scroll handler for positioning
        self.gui.scroll_handler._update_history_positions()

    def restore_history_data(self):
        """Restore history data without fetching again"""
        try:
            if not self.app.current_history_data:
                return
                
            print("[WeatherDisplay] Restoring history data...")
            
            window_width = self.app.winfo_width()
            
            for col, (date, max_temp, min_temp, unit_symbol, avg_temp) in enumerate(self.app.current_history_data):
                if col >= 7:  # Limit to 7 days
                    break
                
                # Create labels for this day
                self._create_history_labels_for_day(date, max_temp, min_temp, avg_temp, unit_symbol, window_width)
            
            # Position the labels
            self._position_history_labels()
            
            print("✅ History data restored")
            
        except Exception as e:
            print(f"❌ History restore error: {e}")

    def toggle_theme(self):
        """Toggle application theme"""
        print("[WeatherDisplay] Toggling theme...")
        
        # Toggle text color
        self.app.text_color = "white" if self.app.text_color == "black" else "black"
        
        # Update widget colors and backgrounds
        self._update_widget_colors()
        
        print(f"🎨 Theme toggled to: {self.app.text_color}")

    def _update_widget_colors(self):
        """Update colors for all relevant widgets"""
        bg_color = self._get_canvas_bg_color()
        
        # Main display widgets - use canvas background color
        widgets_to_update = [
            self.gui.humidity_value, self.gui.wind_value, self.gui.pressure_value,
            self.gui.visibility_value, self.gui.uv_value, self.gui.precipitation_value,
            self.gui.temp_label, self.gui.desc_label, self.gui.temp_prediction,
            self.gui.confidence_prediction, self.gui.accuracy_prediction
        ]
        
        for widget in widgets_to_update:
            if widget:
                try:
                    widget.configure(fg=self.app.text_color, bg=bg_color)
                except:
                    pass
        
        # Update widgets in main widgets list
        for widget in self.gui.widgets:
            try:
                if hasattr(widget, 'configure'):
                    widget_class = widget.winfo_class()
                    if widget_class == 'Label' and widget != self.gui.icon_label:
                        # Don't change button or entry backgrounds
                        if widget not in [self.gui.theme_btn, self.gui.city_entry]:
                            widget.configure(fg=self.app.text_color, bg=bg_color)
            except:
                pass
        
        # Update history labels
        for label in self.gui.history_labels:
            try:
                label.configure(fg=self.app.text_color, bg=bg_color)
            except:
                pass

    def clear_all_displays(self):
        """Clear all weather displays"""
        # Clear main display
        if self.gui.temp_label:
            self.gui.temp_label.configure(text="--")
        if self.gui.desc_label:
            self.gui.desc_label.configure(text="--")
        if self.gui.icon_label:
            self.gui.icon_label.configure(text="🌤️", image="")
        
        # Clear metrics
        metric_widgets = [
            self.gui.humidity_value, self.gui.wind_value, self.gui.pressure_value,
            self.gui.visibility_value, self.gui.uv_value, self.gui.precipitation_value
        ]
        for widget in metric_widgets:
            if widget:
                widget.configure(text="--")
        
        # Clear predictions
        prediction_widgets = [
            self.gui.temp_prediction, self.gui.accuracy_prediction, self.gui.confidence_prediction
        ]
        for widget in prediction_widgets:
            if widget:
                widget.configure(text="--")
        
        # Clear history
        self._clear_history_labels()