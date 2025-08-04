"""
Weather Display Manager
=======================

This module handles updating all the visual elements that show weather information.

Key responsibilities:
- Update temperature displays with proper units (°C or °F)
- Show weather descriptions and icons
- Display weather metrics (humidity, wind, pressure, etc.)
- Handle tomorrow's weather predictions
- Show historical weather data
- Manage theme changes (light/dark mode)
- Ensure all text has transparent backgrounds (no ugly blue boxes!)
"""

import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import requests


class WeatherDisplay:
    """
    Weather Display Manager Class
    
    This class manages all the visual updates for weather information.
    It takes weather data (numbers and text) and displays it beautifully
    on the screen with proper formatting and colors.
    """
    
    def __init__(self, app, gui_controller):
        """
        Initialize the weather display manager.
        
        Args:
            app: The main weather application
            gui_controller: The main GUI controller that manages the interface
        """
        self.app = app              # Reference to main app
        self.gui = gui_controller   # Reference to GUI controller

    def _get_canvas_bg_color(self):
        """
        Get the current background color of the animated canvas.
        
        Returns:
            str: Current background color (like "#87CEEB" for sky blue)
        """
        try:
            if self.gui.bg_canvas:
                return self.gui.bg_canvas.cget("bg")
            return "#87CEEB"  # Default sky blue color
        except:
            return "#87CEEB"  # Safe fallback

    def _create_transparent_label(self, parent, text, font, fg, x, y, anchor="center", **kwargs):
        """
        Create a text label with transparent background that matches the canvas.
        
        This is the secret to preventing ugly blue boxes around text!
        By setting the label background to match the canvas background,
        the text appears to float naturally on the animated background.
        
        Args:
            parent: Widget to put this label in
            text: Text to display
            font: Font specification (family, size, style)
            fg: Text color
            x, y: Position coordinates
            anchor: How to position relative to x,y
            **kwargs: Additional label options
            
        Returns:
            tk.Label: The created transparent label
        """
        # Get the current canvas background color
        canvas_bg = self._get_canvas_bg_color()
        
        # Create label with matching background
        label = tk.Label(
            parent,
            text=text,
            font=font,
            fg=fg,
            bg=canvas_bg,         # This is the key - match the canvas background!
            anchor=anchor,
            relief="flat",        # No 3D border effects
            borderwidth=0,        # No border
            highlightthickness=0, # No highlight border
            **kwargs
        )
        
        # Position the label
        label.place(x=x, y=y, anchor=anchor)
        return label

    def update_weather_display(self, weather_data):
        """
        Update the main weather display with current data.
        
        This is the main function that updates all the weather information
        on the screen when new data arrives from the weather APIs.
        
        Args:
            weather_data (dict): Dictionary containing weather information
            like temperature, humidity, description, etc.
        """
        try:
            # Update different parts of the weather display
            self._update_temperature_display(weather_data)
            self._update_description_display(weather_data)
            self._update_weather_metrics(weather_data)
            self._update_weather_icon(weather_data.get("icon"))
            
            # Get description for logging (optional)
            description = weather_data.get("description", "No description")
            
        except Exception as e:
            # If updating fails, just continue - the app won't crash
            pass

    def _update_temperature_display(self, weather_data):
        """
        Update the temperature labels with current temperature.
        
        This handles converting between Celsius and Fahrenheit based on
        user preference and updates the clickable temperature display.
        
        Args:
            weather_data (dict): Weather data containing temperature
        """
        # Get temperature in Celsius from the weather data
        temp_c = weather_data.get("temperature")
        
        # Only update if we have valid temperature data and a temperature label
        if temp_c is not None and self.gui.temp_label:
            # Store both Celsius and Fahrenheit versions in the app
            self.app.temp_c = round(temp_c, 1)
            self.app.temp_f = round((temp_c * 9 / 5) + 32, 1)  # Convert C to F
            
            try:
                # Display temperature in user's preferred unit
                if self.app.unit == "C":
                    self.gui.temp_label.configure(text=f"{self.app.temp_c}°C")
                else:
                    self.gui.temp_label.configure(text=f"{self.app.temp_f}°F")
                
                # Fix background color to prevent blue boxes
                self.gui.temp_label.configure(bg=self._get_canvas_bg_color())
            except tk.TclError:
                # If updating the label fails, just skip it
                pass

    def _update_description_display(self, weather_data):
        """
        Update the weather description text.
        
        Args:
            weather_data (dict): Weather data containing description
        """
        if self.gui.desc_label:
            try:
                # Get description from weather data
                description = weather_data.get("description", "No description")
                self.gui.desc_label.configure(text=description)
                
                # Fix background color to prevent blue boxes
                self.gui.desc_label.configure(bg=self._get_canvas_bg_color())
            except tk.TclError:
                # If updating fails, just skip it
                pass

    def _update_weather_metrics(self, weather_data):
        """
        Update all the weather metrics display.
                
        Args:
            weather_data (dict): Weather data containing all metrics
        """
        # Extract metric values from weather data, using "N/A" if missing
        humidity = weather_data.get("humidity", "N/A")
        wind = weather_data.get("wind_speed", "N/A")
        pressure = weather_data.get("pressure", "N/A")
        visibility = weather_data.get("visibility", "N/A")
        uv = weather_data.get("uv_index", "N/A")
        precipitation = weather_data.get("precipitation", "N/A")
        
        # Create list of (widget, formatted_text) pairs for easy updating
        metric_updates = [
            (self.gui.humidity_value, f"{humidity}%" if humidity != "N/A" else "--"),
            (self.gui.wind_value, f"{wind} m/s" if wind != "N/A" else "--"),
            (self.gui.pressure_value, f"{pressure} hPa" if pressure != "N/A" else "--"),
            (self.gui.visibility_value, f"{visibility} m" if visibility != "N/A" else "--"),
            (self.gui.uv_value, f"{uv}" if uv != "N/A" else "--"),
            (self.gui.precipitation_value, f"{precipitation} mm" if precipitation != "N/A" else "--")
        ]
        
        # Get current canvas background color for consistency
        canvas_bg = self._get_canvas_bg_color()
        
        # Update each metric widget
        for widget, text in metric_updates:
            if widget:  # Make sure widget exists
                try:
                    widget.configure(text=text)
                    # Fix background color to prevent blue boxes
                    widget.configure(bg=canvas_bg)
                except tk.TclError:
                    # If updating this widget fails, just skip it
                    pass

    def _update_weather_icon(self, icon_code):
        """
        Update the weather icon display.
        
        Args:
            icon_code (str): Icon code from weather API (like "01d" for sunny)
        """
        # Don't try to update if we don't have an icon code or icon label
        if not icon_code or not self.gui.icon_label:
            return
            
        try:
            # Build URL for weather icon from OpenWeatherMap
            url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            
            # Download the icon image
            response = requests.get(url, timeout=5)  # 5 second timeout
            response.raise_for_status()  # Raise exception if download failed
            
            # Convert downloaded data to an image
            pil_img = Image.open(BytesIO(response.content))
            icon_image = ImageTk.PhotoImage(pil_img)
            
            # Display the downloaded icon
            self.gui.icon_label.configure(image=icon_image, text="")
            self.gui.icon_label.image = icon_image  # Keep reference to prevent garbage collection
            
            # Fix background color to prevent blue boxes
            self.gui.icon_label.configure(bg=self._get_canvas_bg_color())
            
        except Exception as e:
            # If icon download fails, show emoji fallback
            try:
                self.gui.icon_label.configure(text="🌤️", image="")
                # Fix background color for fallback emoji too
                self.gui.icon_label.configure(bg=self._get_canvas_bg_color())
            except tk.TclError:
                # If even the fallback fails, just skip it
                pass

    def update_tomorrow_prediction_direct(self, predicted_temp, confidence, accuracy):
        """
        Update tomorrow's weather prediction display.
        
        Args:
            predicted_temp (float): Predicted temperature for tomorrow
            confidence (str): Confidence level (like "85%")
            accuracy (int): Accuracy percentage of our predictions
        """
        try:
            # Store the prediction data in the app for later reference
            self.app.current_prediction_data = (predicted_temp, confidence, accuracy)
            
            # Only update if we're currently on the prediction page
            if self.gui.current_page == "prediction":
                canvas_bg = self._get_canvas_bg_color()
                
                # Update temperature prediction
                if hasattr(self.gui, 'temp_prediction') and self.gui.temp_prediction:
                    try:
                        if predicted_temp:
                            # Display in user's preferred unit
                            if self.app.unit == "C":
                                temp_text = f"{predicted_temp}°C"
                            else:
                                # Convert Celsius prediction to Fahrenheit
                                temp_f = round((predicted_temp * 9/5) + 32, 1)
                                temp_text = f"{temp_f}°F"
                            self.gui.temp_prediction.configure(text=temp_text)
                        else:
                            self.gui.temp_prediction.configure(text="--")
                        
                        # Fix background color
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
                        
                        # Fix background color
                        self.gui.accuracy_prediction.configure(bg=canvas_bg)
                    except tk.TclError:
                        pass
                
                # Update confidence prediction
                if hasattr(self.gui, 'confidence_prediction') and self.gui.confidence_prediction:
                    try:
                        if confidence and confidence != "N/A":
                            # Ensure percentage sign is included
                            conf_text = str(confidence).replace('%', '') + '%'
                            self.gui.confidence_prediction.configure(text=conf_text)
                        else:
                            self.gui.confidence_prediction.configure(text="--")
                        
                        # Fix background color
                        self.gui.confidence_prediction.configure(bg=canvas_bg)
                    except tk.TclError:
                        pass
                                            
        except Exception as e:
            # If prediction update fails, just continue
            pass

    def update_history_display(self, city):
        """
        Update the weather history display for a specific city.
        
        This shows historical weather data in a grid format with
        dates, high/low temperatures, and averages for the past week.
        
        Args:
            city (str): Name of the city to show history for
        """
        try:
            # Only update if we're currently on the history page
            if self.gui.current_page != "history":
                return
            
            # Clear any existing history displays first
            self._clear_history_labels()
            
            # Get historical weather data from our API
            from features.history_tracker.api import fetch_world_history
            history_data = fetch_world_history(city)
            
            # Check if we got valid historical data
            if history_data and "time" in history_data:
                self._create_history_display_directly(history_data)
            else:
                self._show_history_error()
            
        except Exception as e:
            # If history update fails, show error message
            self._show_history_error()

    def _create_history_display_directly(self, history_data):
        """
        Create the historical weather display with ALL BLACK TEXT.
        
        This creates a grid showing weather history for the past week
        with dates, temperatures, and ensures all text is black for readability.
        
        Args:
            history_data (dict): Historical weather data from API
        """
        try:
            # Extract data arrays from the API response
            times = history_data.get("time", [])
            max_temps = history_data.get("temperature_2m_max", [])
            min_temps = history_data.get("temperature_2m_min", [])
            
            # Validate we have the required data
            if not times or not max_temps or not min_temps:
                self._show_history_error()
                return
            
            # Set up layout parameters
            window_width = self.app.winfo_width()
            days_to_show = min(7, len(times))  # Show up to 7 days
            
            start_y = 200
            available_width = window_width - 60
            col_width = available_width / days_to_show
            start_x = 30
            
            # Create a column for each day
            for col in range(days_to_show):
                if col < len(max_temps) and col < len(min_temps):
                    # Extract data for this day
                    date = times[col][-5:] if len(times[col]) > 5 else times[col]  # Last 5 chars (MM-DD)
                    max_temp = max_temps[col]
                    min_temp = min_temps[col]
                    
                    # Calculate position for this column
                    x_pos = start_x + (col * col_width) + (col_width / 2)
                    
                    # Create labels for this day
                    self._create_day_labels(date, max_temp, min_temp, x_pos, start_y, window_width)
            
        except Exception as e:
            # If history display creation fails, show error
            self._show_history_error()

    def _create_day_labels(self, date, max_temp, min_temp, x_pos, y_start, window_width):
        """
        Create labels for a single day with ALL BLACK TEXT.
        
        This creates the date, high temperature, low temperature, and average
        temperature labels for one day in the history display.
        
        Args:
            date (str): Date string for this day
            max_temp (float): Maximum temperature for this day
            min_temp (float): Minimum temperature for this day
            x_pos (int): X position for this column
            y_start (int): Y position to start labels
            window_width (int): Width of window for responsive font sizing
        """
        try:
            # Calculate responsive font size
            font_size = int(12 + window_width/100)
            canvas_bg = self._get_canvas_bg_color()
            
            # Handle missing temperature data
            if max_temp is None or min_temp is None:
                max_text = "N/A"
                min_text = "N/A"
                avg_text = "N/A"
            else:
                # Convert temperatures to user's preferred unit
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
                
                # Format temperature strings
                max_text = f"{max_temp}{unit_symbol}"
                min_text = f"{min_temp}{unit_symbol}"
                avg_text = f"{avg_temp}{unit_symbol}"
            
            # Create all labels with BLACK TEXT for readability
            date_label = self._create_transparent_label(
                self.app,
                text=f"📅 {date}",
                font=("Arial", font_size, "bold"),
                fg="black",  # FORCE BLACK TEXT
                x=x_pos,
                y=y_start
            )
            self.gui.history_labels.append(date_label)
            
            max_label = self._create_transparent_label(
                self.app,
                text=f"🔺 {max_text}",
                font=("Arial", font_size),
                fg="black",  # FORCE BLACK TEXT
                x=x_pos,
                y=y_start + 40
            )
            self.gui.history_labels.append(max_label)
            
            min_label = self._create_transparent_label(
                self.app,
                text=f"🔻 {min_text}",
                font=("Arial", font_size),
                fg="black",  # FORCE BLACK TEXT
                x=x_pos,
                y=y_start + 80
            )
            self.gui.history_labels.append(min_label)
            
            avg_label = self._create_transparent_label(
                self.app,
                text=f"🌡️ {avg_text}",
                font=("Arial", font_size),
                fg="black",  # FORCE BLACK TEXT
                x=x_pos,
                y=y_start + 120
            )
            self.gui.history_labels.append(avg_label)
            
        except Exception as e:
            # If creating day labels fails, just skip this day
            pass

    def _show_history_error(self):
        """Show error message when historical data is not available."""
        try:
            window_width = self.app.winfo_width()
            
            # Create error message with BLACK TEXT
            error_label = self._create_transparent_label(
                self.app,
                text="📊 Weather History\n\nNo historical data available for this location.\nTry refreshing or selecting a different city.",
                font=("Arial", 16),
                fg="black",  # FORCE BLACK TEXT
                x=window_width/2,
                y=300,
                justify="center"
            )
            self.gui.history_labels.append(error_label)
            
        except Exception as e:
            # If even error display fails, just continue
            pass
    
    def _clear_history_labels(self):
        """Clear existing history labels before showing new ones."""
        # Remove all existing history labels
        for label in self.gui.history_labels:
            try:
                label.destroy()
            except:
                pass
        
        # Clear the list and any stored history data
        self.gui.history_labels.clear()
        if hasattr(self.app, 'current_history_data'):
            self.app.current_history_data.clear()

    def toggle_text(self):
        """
        Toggle between light and dark themes.
        
        This switches the text color throughout the app and fixes
        all background colors to prevent blue boxes.
        """
        # Toggle text color between black and white
        self.app.text_color = "white" if self.app.text_color == "black" else "black"
        
        # Update all widget backgrounds to match the new theme
        self._fix_all_blue_boxes()

    def _fix_all_blue_boxes(self):
        """
        Fix blue boxes on ALL widgets by setting proper background colors.
        
        This is the master function that ensures no text labels have
        ugly blue backgrounds by setting them all to match the canvas.
        """
        canvas_bg = self._get_canvas_bg_color()
        
        # List of main display widgets to fix
        widgets_to_fix = [
            self.gui.humidity_value, self.gui.wind_value, self.gui.pressure_value,
            self.gui.visibility_value, self.gui.uv_value, self.gui.precipitation_value,
            self.gui.temp_label, self.gui.desc_label, self.gui.icon_label,
            self.gui.temp_prediction, self.gui.confidence_prediction, self.gui.accuracy_prediction
        ]
        
        # Fix each main widget
        for widget in widgets_to_fix:
            if widget:
                try:
                    widget.configure(fg=self.app.text_color, bg=canvas_bg)
                except (tk.TclError, AttributeError):
                    pass
        
        # Fix widgets in the main widgets list
        for widget in self.gui.widgets:
            try:
                if hasattr(widget, 'configure'):
                    widget_class = widget.winfo_class()
                    # Only fix labels (not buttons or entries)
                    if widget_class == 'Label':
                        # Make sure it's not a button (buttons have invoke method)
                        if not hasattr(widget, 'invoke'):
                            widget.configure(fg=self.app.text_color, bg=canvas_bg)
            except (tk.TclError, AttributeError):
                pass
        
        # Fix history labels - FORCE ALL TO BLACK for readability
        for label in self.gui.history_labels:
            try:
                # History labels are always black for best readability
                label.configure(fg="black", bg=canvas_bg)
            except (tk.TclError, AttributeError):
                pass

    def clear_all_displays(self):
        """
        Clear all weather displays and fix background colors.
        
        This resets all weather displays to show placeholder text
        and ensures all backgrounds are properly transparent.
        """
        canvas_bg = self._get_canvas_bg_color()
        
        # Clear and fix main temperature display
        if self.gui.temp_label:
            try:
                self.gui.temp_label.configure(text="--", bg=canvas_bg)
            except (tk.TclError, AttributeError):
                pass
        
        # Clear and fix weather description
        if self.gui.desc_label:
            try:
                self.gui.desc_label.configure(text="--", bg=canvas_bg)
            except (tk.TclError, AttributeError):
                pass
        
        # Clear and fix weather icon
        if self.gui.icon_label:
            try:
                self.gui.icon_label.configure(text="🌤️", image="", bg=canvas_bg)
            except (tk.TclError, AttributeError):
                pass
        
        # Clear and fix all metric widgets
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
        
        # Clear and fix prediction widgets
        prediction_widgets = [
            self.gui.temp_prediction, self.gui.accuracy_prediction, self.gui.confidence_prediction
        ]
        for widget in prediction_widgets:
            if widget:
                try:
                    widget.configure(text="--", bg=canvas_bg)
                except (tk.TclError, AttributeError):
                    pass
        
        # Clear history display
        self._clear_history_labels()