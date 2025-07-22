import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import requests


class WeatherDisplay:
    """
    Weather Display Manager - Blue Box Background Fix
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

    def _create_transparent_label(self, parent, text, font, fg, x, y, anchor="center", **kwargs):
        """Create a label with transparent background that matches canvas"""
        canvas_bg = self._get_canvas_bg_color()
        
        label = tk.Label(
            parent,
            text=text,
            font=font,
            fg=fg,
            bg=canvas_bg,  # Always use canvas background - this removes blue boxes
            anchor=anchor,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            **kwargs
        )
        
        label.place(x=x, y=y, anchor=anchor)
        return label

    def update_weather_display(self, weather_data):
        """Update the main weather display with current data"""
        try:
            
            self._update_temperature_display(weather_data)
            self._update_description_display(weather_data)
            self._update_weather_metrics(weather_data)
            self._update_weather_icon(weather_data.get("icon"))
            
            description = weather_data.get("description", "No description")
            
        except Exception as e:
            pass

    def _update_temperature_display(self, weather_data):
        """Update temperature labels"""
        temp_c = weather_data.get("temperature")
        if temp_c is not None and self.gui.temp_label:
            self.app.temp_c = round(temp_c, 1)
            self.app.temp_f = round((temp_c * 9 / 5) + 32, 1)
            
            try:
                if self.app.unit == "C":
                    self.gui.temp_label.configure(text=f"{self.app.temp_c}°C")
                else:
                    self.gui.temp_label.configure(text=f"{self.app.temp_f}°F")
                # Fix blue box behind temperature
                self.gui.temp_label.configure(bg=self._get_canvas_bg_color())
            except tk.TclError:
                pass

    def _update_description_display(self, weather_data):
        """Update weather description"""
        if self.gui.desc_label:
            try:
                description = weather_data.get("description", "No description")
                self.gui.desc_label.configure(text=description)
                # Fix blue box behind description
                self.gui.desc_label.configure(bg=self._get_canvas_bg_color())
            except tk.TclError:
                pass

    def _update_weather_metrics(self, weather_data):
        """Update weather metrics display"""
        humidity = weather_data.get("humidity", "N/A")
        wind = weather_data.get("wind_speed", "N/A")
        pressure = weather_data.get("pressure", "N/A")
        visibility = weather_data.get("visibility", "N/A")
        uv = weather_data.get("uv_index", "N/A")
        precipitation = weather_data.get("precipitation", "N/A")
        
        metric_updates = [
            (self.gui.humidity_value, f"{humidity}%" if humidity != "N/A" else "--"),
            (self.gui.wind_value, f"{wind} m/s" if wind != "N/A" else "--"),
            (self.gui.pressure_value, f"{pressure} hPa" if pressure != "N/A" else "--"),
            (self.gui.visibility_value, f"{visibility} m" if visibility != "N/A" else "--"),
            (self.gui.uv_value, f"{uv}" if uv != "N/A" else "--"),
            (self.gui.precipitation_value, f"{precipitation} mm" if precipitation != "N/A" else "--")
        ]
        
        canvas_bg = self._get_canvas_bg_color()
        
        for widget, text in metric_updates:
            if widget:
                try:
                    widget.configure(text=text)
                    # Fix blue box behind metrics
                    widget.configure(bg=canvas_bg)
                except tk.TclError:
                    pass

    def _update_weather_icon(self, icon_code):
        """Update weather icon"""
        if not icon_code or not self.gui.icon_label:
            return
            
        try:
            url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            pil_img = Image.open(BytesIO(response.content))
            icon_image = ImageTk.PhotoImage(pil_img)
            
            self.gui.icon_label.configure(image=icon_image, text="")
            self.gui.icon_label.image = icon_image
            # Fix blue box behind icon
            self.gui.icon_label.configure(bg=self._get_canvas_bg_color())
            
        except Exception as e:
            try:
                self.gui.icon_label.configure(text="🌤️", image="")
                # Fix blue box behind fallback icon
                self.gui.icon_label.configure(bg=self._get_canvas_bg_color())
            except tk.TclError:
                pass

    def update_tomorrow_prediction_direct(self, predicted_temp, confidence, accuracy):
        """Update tomorrow's prediction display"""
        try:
            
            self.app.current_prediction_data = (predicted_temp, confidence, accuracy)
            
            if self.gui.current_page == "prediction":
                canvas_bg = self._get_canvas_bg_color()
                
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
                        # Fix blue box
                        self.gui.temp_prediction.configure(bg=canvas_bg)
                    except tk.TclError:
                        pass
                
                # Update accuracy prediction
                if hasattr(self.gui, 'accuracy_prediction') and self.gui.accuracy_prediction:
                    try:
                        if isinstance(accuracy, (int, float)):
                            self.gui.accuracy_prediction.configure(text=f"{accuracy}%")
                        else:
                            self.gui.accuracy_prediction.configure(text="--")
                        # Fix blue box
                        self.gui.accuracy_prediction.configure(bg=canvas_bg)
                    except tk.TclError:
                        pass
                
                # Update confidence prediction
                if hasattr(self.gui, 'confidence_prediction') and self.gui.confidence_prediction:
                    try:
                        if confidence and confidence != "N/A":
                            conf_text = str(confidence).replace('%', '') + '%'
                            self.gui.confidence_prediction.configure(text=conf_text)
                        else:
                            self.gui.confidence_prediction.configure(text="--")
                        # Fix blue box
                        self.gui.confidence_prediction.configure(bg=canvas_bg)
                    except tk.TclError:
                        pass
                                            
        except Exception as e:
            pass

    def update_history_display(self, city):
        """Update weather history display"""
        try:
            
            if self.gui.current_page != "history":
                return
            
            self._clear_history_labels()
            
            from features.history_tracker.api import fetch_world_history
            history_data = fetch_world_history(city)
            
            if history_data and "time" in history_data:
                self._create_history_display_directly(history_data)
            else:
                self._show_history_error()
            
            
        except Exception as e:
            self._show_history_error()

    def _create_history_display_directly(self, history_data):
        """Create history display with transparent backgrounds"""
        try:
            
            times = history_data.get("time", [])
            max_temps = history_data.get("temperature_2m_max", [])
            min_temps = history_data.get("temperature_2m_min", [])
            
            if not times or not max_temps or not min_temps:
                self._show_history_error()
                return
            
            window_width = self.app.winfo_width()
            days_to_show = min(7, len(times))
            
            start_y = 200
            available_width = window_width - 60
            col_width = available_width / days_to_show
            start_x = 30
            
            for col in range(days_to_show):
                if col < len(max_temps) and col < len(min_temps):
                    date = times[col][-5:] if len(times[col]) > 5 else times[col]
                    max_temp = max_temps[col]
                    min_temp = min_temps[col]
                    
                    x_pos = start_x + (col * col_width) + (col_width / 2)
                    self._create_day_labels(date, max_temp, min_temp, x_pos, start_y, window_width)
            
            
        except Exception as e:
            self._show_history_error()

    def _create_day_labels(self, date, max_temp, min_temp, x_pos, y_start, window_width):
        """Create labels for a single day with transparent backgrounds"""
        try:
            font_size = int(12 + window_width/100)
            canvas_bg = self._get_canvas_bg_color()  # Get current canvas background
            
            # Handle None values
            if max_temp is None or min_temp is None:
                max_text = "N/A"
                min_text = "N/A"
                avg_text = "N/A"
                max_color = self.app.text_color
                min_color = self.app.text_color
                avg_color = self.app.text_color
            else:
                # Convert temperatures if needed
                if self.app.unit == "F":
                    max_temp = round(max_temp * 9/5 + 32, 1)
                    min_temp = round(min_temp * 9/5 + 32, 1)
                    avg_temp = round((max_temp + min_temp) / 2, 1)
                    unit_symbol = "°F"
                else:
                    max_temp = round(max_temp, 1)
                    min_temp = round(min_temp, 1)
                    avg_temp = round((max_temp + min_temp) / 2, 1)
                    unit_symbol = "°C"
                
                max_text = f"{max_temp}{unit_symbol}"
                min_text = f"{min_temp}{unit_symbol}"
                avg_text = f"{avg_temp}{unit_symbol}"
                max_color = "#FF6B6B" if self.app.text_color == "black" else "#FF8E8E"
                min_color = "#4ECDC4" if self.app.text_color == "black" else "#6EDDD6"
                avg_color = self.app.text_color
            
            # Create all labels with transparent canvas background
            date_label = self._create_transparent_label(
                self.app,
                text=f"📅 {date}",
                font=("Arial", font_size, "bold"),
                fg=self.app.text_color,
                x=x_pos,
                y=y_start
            )
            self.gui.history_labels.append(date_label)
            
            max_label = self._create_transparent_label(
                self.app,
                text=f"🔺 {max_text}",
                font=("Arial", font_size),
                fg=max_color,
                x=x_pos,
                y=y_start + 40
            )
            self.gui.history_labels.append(max_label)
            
            min_label = self._create_transparent_label(
                self.app,
                text=f"🔻 {min_text}",
                font=("Arial", font_size),
                fg=min_color,
                x=x_pos,
                y=y_start + 80
            )
            self.gui.history_labels.append(min_label)
            
            avg_label = self._create_transparent_label(
                self.app,
                text=f"🌡️ {avg_text}",
                font=("Arial", font_size),
                fg=avg_color,
                x=x_pos,
                y=y_start + 120
            )
            self.gui.history_labels.append(avg_label)
            
        except Exception as e:
            pass

    def _show_history_error(self):
        """Show error message with transparent background"""
        try:
            window_width = self.app.winfo_width()
            
            error_label = self._create_transparent_label(
                self.app,
                text="📊 Weather History\n\nNo historical data available for this location.\nTry refreshing or selecting a different city.",
                font=("Arial", 16),
                fg=self.app.text_color,
                x=window_width/2,
                y=300,
                justify="center"
            )
            self.gui.history_labels.append(error_label)
            
        except Exception as e:
            pass
    
    def _clear_history_labels(self):
        """Clear existing history labels"""
        for label in self.gui.history_labels:
            try:
                label.destroy()
            except:
                pass
        self.gui.history_labels.clear()
        if hasattr(self.app, 'current_history_data'):
            self.app.current_history_data.clear()

    def toggle_theme(self):
        """Toggle application theme and fix all blue boxes"""
        
        # Toggle text color
        self.app.text_color = "white" if self.app.text_color == "black" else "black"
        
        # Update ALL widget backgrounds to match canvas
        self._fix_all_blue_boxes()
        

    def _fix_all_blue_boxes(self):
        """Fix blue boxes on ALL widgets by setting canvas background"""
        canvas_bg = self._get_canvas_bg_color()
        
        # Fix main display widgets
        widgets_to_fix = [
            self.gui.humidity_value, self.gui.wind_value, self.gui.pressure_value,
            self.gui.visibility_value, self.gui.uv_value, self.gui.precipitation_value,
            self.gui.temp_label, self.gui.desc_label, self.gui.icon_label,
            self.gui.temp_prediction, self.gui.confidence_prediction, self.gui.accuracy_prediction
        ]
        
        for widget in widgets_to_fix:
            if widget:
                try:
                    widget.configure(fg=self.app.text_color, bg=canvas_bg)
                except (tk.TclError, AttributeError):
                    pass
        
        # Fix widgets in main widgets list
        for widget in self.gui.widgets:
            try:
                if hasattr(widget, 'configure'):
                    widget_class = widget.winfo_class()
                    if widget_class == 'Label':
                        # Skip buttons and entries, only fix labels
                        if not hasattr(widget, 'invoke'):  # Not a button
                            widget.configure(fg=self.app.text_color, bg=canvas_bg)
            except (tk.TclError, AttributeError):
                pass
        
        # Fix history labels
        for label in self.gui.history_labels:
            try:
                current_text = label.cget("text")
                if "🔺" in current_text:  # Max temp
                    color = "#FF6B6B" if self.app.text_color == "black" else "#FF8E8E"
                    label.configure(fg=color, bg=canvas_bg)
                elif "🔻" in current_text:  # Min temp
                    color = "#4ECDC4" if self.app.text_color == "black" else "#6EDDD6"
                    label.configure(fg=color, bg=canvas_bg)
                else:  # Date and average labels
                    label.configure(fg=self.app.text_color, bg=canvas_bg)
            except (tk.TclError, AttributeError):
                pass

    def clear_all_displays(self):
        """Clear all weather displays and fix blue boxes"""
        canvas_bg = self._get_canvas_bg_color()
        
        # Clear and fix main display
        if self.gui.temp_label:
            try:
                self.gui.temp_label.configure(text="--", bg=canvas_bg)
            except (tk.TclError, AttributeError):
                pass
        if self.gui.desc_label:
            try:
                self.gui.desc_label.configure(text="--", bg=canvas_bg)
            except (tk.TclError, AttributeError):
                pass
        if self.gui.icon_label:
            try:
                self.gui.icon_label.configure(text="🌤️", image="", bg=canvas_bg)
            except (tk.TclError, AttributeError):
                pass
        
        # Clear and fix metrics
        metric_widgets = [
            self.gui.humidity_value, self.gui.wind_value, self.gui.pressure_value,
            self.gui.visibility_value, self.gui.uv_value, self.gui.precipitation_value
        ]
        for widget in metric_widgets:
            if widget:
                try:
                    widget.configure(text="--", bg=canvas_bg)
                except (tk.TclError, AttributeError):
                    pass
        
        # Clear and fix predictions
        prediction_widgets = [
            self.gui.temp_prediction, self.gui.accuracy_prediction, self.gui.confidence_prediction
        ]
        for widget in prediction_widgets:
            if widget:
                try:
                    widget.configure(text="--", bg=canvas_bg)
                except (tk.TclError, AttributeError):
                    pass
        
        # Clear history
        self._clear_history_labels()