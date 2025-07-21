import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import requests


class WeatherDisplay:
    """
    Weather Display Manager for Paginated System
    
    Handles all weather data visualization including current weather,
    predictions, history, and weather icon updates across different pages.
    """
    
    def __init__(self, app, gui_controller):
        self.app = app
        self.gui = gui_controller

    def _get_canvas_bg_color(self):
        """Get the current canvas background color"""
        try:
            if self.gui.bg_canvas:
                return self.gui.bg_canvas.cget("bg")
            return "#87CEEB"
        except:
            return "#87CEEB"

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
            
            # Always store the data first
            self.app.current_prediction_data = (predicted_temp, confidence, accuracy)
            
            # Only update widgets if we're on the prediction page and widgets exist
            if self.gui.current_page == "prediction":
                # Check if widgets still exist before updating
                # Update temperature prediction
                if hasattr(self.gui, 'temp_prediction') and self.gui.temp_prediction:
                    try:
                        if predicted_temp:
                            if self.app.unit == "C":
                                temp_text = f"{predicted_temp}°C"
                            else:
                                temp_f = round((predicted_temp * 9/5) + 32, 1)
                                temp_text = f"{temp_f}°F"
                            self.gui.temp_prediction.configure(text=temp_text)
                        else:
                            self.gui.temp_prediction.configure(text="--")
                    except tk.TclError:
                        # Widget was destroyed, skip update
                        pass
                
                # Update accuracy prediction
                if hasattr(self.gui, 'accuracy_prediction') and self.gui.accuracy_prediction:
                    try:
                        if isinstance(accuracy, (int, float)):
                            self.gui.accuracy_prediction.configure(text=f"{accuracy}%")
                        else:
                            self.gui.accuracy_prediction.configure(text="--")
                    except tk.TclError:
                        # Widget was destroyed, skip update
                        pass
                
                # Update confidence prediction
                if hasattr(self.gui, 'confidence_prediction') and self.gui.confidence_prediction:
                    try:
                        if confidence and confidence != "N/A":
                            conf_text = str(confidence).replace('%', '') + '%'
                            self.gui.confidence_prediction.configure(text=conf_text)
                        else:
                            self.gui.confidence_prediction.configure(text="--")
                    except tk.TclError:
                        # Widget was destroyed, skip update
                        pass
                        
                print("✅ Prediction display updated on prediction page")
            else:
                print("✅ Prediction data stored (not on prediction page)")
                    
        except Exception as e:
            print(f"❌ Prediction update error: {e}")

    def update_history_display(self, city):
        """Update 7-day history display from Open-Meteo API"""
        try:
            print(f"[WeatherDisplay] Fetching 7-day history for {city}...")
            
            # Fetch new history data from Open-Meteo API
            from features.history_tracker.api import fetch_world_history
            history_data = fetch_world_history(city)
            
            print(f"[WeatherDisplay] Raw history data: {history_data}")
            
            if history_data and "time" in history_data:
                print(f"[WeatherDisplay] Found history data with {len(history_data['time'])} days")
                
                # Store the history data
                self._store_history_data(history_data)
                
                # Only create visual display if we're on history page
                if self.gui.current_page == "history":
                    print("[WeatherDisplay] Creating history display for history page")
                    self._clear_history_labels()
                    self._create_history_labels_for_page(history_data)
                else:
                    print(f"[WeatherDisplay] History data stored (currently on {self.gui.current_page} page)")
            else:
                print("[WeatherDisplay] No history data received from API")
                # Try to show an error message on history page
                if self.gui.current_page == "history":
                    self._show_history_error()
            
            print("✅ History update process completed")
            
        except Exception as e:
            print(f"❌ History update error: {e}")
            import traceback
            traceback.print_exc()
            if self.gui.current_page == "history":
                self._show_history_error()

    def _show_history_error(self):
        """Show error message on history page"""
        try:
            window_width = self.app.winfo_width()
            bg_color = self._get_canvas_bg_color()
            
            error_label = tk.Label(
                self.app,
                text="❌ Unable to load 7-day history data\nPlease check your internet connection",
                font=("Arial", 16),
                fg="red",
                bg=bg_color,
                anchor="center",
                justify="center"
            )
            error_label.place(x=window_width/2, y=300, anchor="center")
            self.gui.history_labels.append(error_label)
            
        except Exception as e:
            print(f"Error showing history error message: {e}")
    
    def _store_history_data(self, history_data):
        """Store history data for later restoration"""
        try:
            print("[WeatherDisplay] Processing history data for storage...")
            
            times = history_data.get("time", [])
            max_temps = history_data.get("temperature_2m_max", [])
            min_temps = history_data.get("temperature_2m_min", [])
            
            print(f"[WeatherDisplay] Times: {times}")
            print(f"[WeatherDisplay] Max temps: {max_temps}")
            print(f"[WeatherDisplay] Min temps: {min_temps}")
            
            if not times or not max_temps or not min_temps:
                print("[WeatherDisplay] Missing required temperature data")
                return
            
            # Clear existing stored data
            self.app.current_history_data.clear()
            
            days_to_show = min(7, len(times))
            print(f"[WeatherDisplay] Processing {days_to_show} days")
            
            for col in range(days_to_show):
                if col < len(max_temps) and col < len(min_temps):
                    # Process temperature data with None checks
                    date = times[col][-5:] if len(times[col]) > 5 else times[col]
                    max_temp = max_temps[col]
                    min_temp = min_temps[col]
                    
                    print(f"[WeatherDisplay] Day {col}: {date}, Max: {max_temp}, Min: {min_temp}")
                    
                    # Handle None values by showing "N/A" instead of skipping
                    if max_temp is None or min_temp is None:
                        print(f"[WeatherDisplay] Day {col} has None values, storing as N/A")
                        self.app.current_history_data.append((date, "N/A", "N/A", "°C", "N/A"))
                        continue
                        
                    avg_temp = round((max_temp + min_temp) / 2, 1)
                    
                    # Store in Celsius first, convert for display later
                    unit_symbol = "°C"
                    
                    # Store data for preservation
                    self.app.current_history_data.append((date, max_temp, min_temp, unit_symbol, avg_temp))
                    print(f"[WeatherDisplay] Stored: {date} - Max: {max_temp}°C, Min: {min_temp}°C, Avg: {avg_temp}°C")
                    
            print(f"✅ Stored {len(self.app.current_history_data)} days of history data")
            
        except Exception as e:
            print(f"❌ History data storage error: {e}")
            import traceback
            traceback.print_exc()

    def _clear_history_labels(self):
        """Clear existing history labels"""
        for label in self.gui.history_labels:
            label.destroy()
        self.gui.history_labels.clear()
        self.app.current_history_data.clear()

    def _create_history_labels_for_page(self, history_data):
        """Create history labels optimized for page display"""
        times = history_data.get("time", [])
        max_temps = history_data.get("temperature_2m_max", [])
        min_temps = history_data.get("temperature_2m_min", [])
        
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        days_to_show = min(7, len(times))
        
        # Calculate layout for history page
        start_y = 150
        available_width = window_width - 60
        col_width = available_width / days_to_show
        start_x = 30
        
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
                
                # Calculate position
                x_pos = start_x + (col * col_width) + (col_width / 2)
                
    def _create_history_labels_for_day_page(self, date, max_temp, min_temp, avg_temp, unit_symbol, x_pos, y_start, window_width):
        """Create labels for a single day's history optimized for page layout"""
        font_size = int(12 + window_width/100)
        bg_color = self._get_canvas_bg_color()
        
        # Handle N/A values
        if max_temp == "N/A" or min_temp == "N/A" or avg_temp == "N/A":
            max_text = "N/A"
            min_text = "N/A"
            avg_text = "N/A"
        else:
            # Convert temperatures based on current unit setting
            if self.app.unit == "F" and unit_symbol == "°C":
                # Convert from Celsius to Fahrenheit
                max_temp = round(max_temp * 9/5 + 32, 1)
                min_temp = round(min_temp * 9/5 + 32, 1)
                avg_temp = round(avg_temp * 9/5 + 32, 1)
                unit_symbol = "°F"
            elif self.app.unit == "C" and unit_symbol == "°F":
                # Convert from Fahrenheit to Celsius
                max_temp = round((max_temp - 32) * 5/9, 1)
                min_temp = round((min_temp - 32) * 5/9, 1)
                avg_temp = round((avg_temp - 32) * 5/9, 1)
                unit_symbol = "°C"
            
            max_text = f"{max_temp}{unit_symbol}"
            min_text = f"{min_temp}{unit_symbol}"
            avg_text = f"{avg_temp}{unit_symbol}"
        
        print(f"[WeatherDisplay] Creating labels for {date}: Max {max_text}, Min {min_text}, Avg {avg_text}")
        
        # Date label
        date_label = tk.Label(
            self.app,
            text=f"📅 {date}",
            font=("Arial", font_size, "bold"),
            fg=self.app.text_color, 
            bg=bg_color,
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        date_label.place(x=x_pos, y=y_start, anchor="center")
        self.gui.history_labels.append(date_label)
        
        # Max temperature label
        max_label = tk.Label(
            self.app,
            text=f"🔺 {max_text}",
            font=("Arial", font_size),
            fg="red" if max_text != "N/A" else "gray", 
            bg=bg_color,
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        max_label.place(x=x_pos, y=y_start + 40, anchor="center")
        self.gui.history_labels.append(max_label)
        
        # Min temperature label
        min_label = tk.Label(
            self.app,
            text=f"🔻 {min_text}",
            font=("Arial", font_size),
            fg="blue" if min_text != "N/A" else "gray", 
            bg=bg_color,
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        min_label.place(x=x_pos, y=y_start + 80, anchor="center")
        self.gui.history_labels.append(min_label)
        
        # Average temperature label
        avg_label = tk.Label(
            self.app,
            text=f"🌡️ {avg_text}",
            font=("Arial", font_size),
            fg=self.app.text_color if avg_text != "N/A" else "gray", 
            bg=bg_color,
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        avg_label.place(x=x_pos, y=y_start + 120, anchor="center")
        self.gui.history_labels.append(avg_label)

    def restore_history_data(self):
        """Restore history data without fetching again"""
        try:
            if not self.app.current_history_data or self.gui.current_page != "history":
                return
                
            print("[WeatherDisplay] Restoring history data...")
            
            window_width = self.app.winfo_width()
            start_y = 150
            available_width = window_width - 60
            days_count = len(self.app.current_history_data)
            col_width = available_width / days_count
            start_x = 30
            
            for col, (date, max_temp, min_temp, unit_symbol, avg_temp) in enumerate(self.app.current_history_data):
                if col >= 7:  # Limit to 7 days
                    break
                
                x_pos = start_x + (col * col_width) + (col_width / 2)
                
                # Create labels for this day
                self._create_history_labels_for_day_page(
                    date, max_temp, min_temp, avg_temp, unit_symbol,
                    x_pos, start_y, window_width
                )
            
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
        """Update colors for all relevant widgets across all pages"""
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