"""
City Comparison Controller
===============================================================

Main controller for the city comparison feature.
"""

import tkinter as tk
import threading
from config.api import get_current_weather


class CityComparisonController:
    """
    City Comparison Controller Class
    
    This controller manages the city comparison feature with results that
    persist until user inputs new cities and performs a new comparison.
    """
    
    def __init__(self, app, gui_controller):
        """
        Initialize the city comparison controller.
        
        Args:
            app: Main weather application instance
            gui_controller: GUI controller that manages the interface
        """
        self.app = app
        self.gui = gui_controller
        
        # Variables for city inputs
        self.city1_var = None
        self.city2_var = None
        
        # Track comparison widgets for cleanup
        self.comparison_widgets = []
        
        # Store last comparison results for persistence
        self.last_comparison_data = None
        
        # Track the cities that were last compared
        self.last_compared_cities = None
        
        # Track if we're currently on the comparison page
        self.is_active = False

    def build_page(self, window_width, window_height):
        """
        Build the city comparison page with translated text.
        
        Args:
            window_width: Current window width
            window_height: Current window height
        """
        # Mark that we're now active
        self.is_active = True
        
        # Clear any existing comparison widgets first
        self._clear_all_widgets()
        
        # Add back button
        self._add_back_button()
        
        # Page title with translated text
        title_text = self.gui.language_controller.get_text("city_comparison_title")
        title = self._create_label(
            text=title_text,
            font=("Arial", int(24 + window_width/50), "bold"),
            fg=self.app.text_color,
            x=window_width/2,
            y=100
        )
        self.comparison_widgets.append(title)
        
        # Instructions with translated text
        instructions_text = self.gui.language_controller.get_text("comparison_instructions")
        instructions = self._create_label(
            text=instructions_text,
            font=("Arial", int(12 + window_width/100)),
            fg=self.app.text_color,
            x=window_width/2,
            y=140
        )
        self.comparison_widgets.append(instructions)
        
        # Build input section
        self._build_city_inputs(window_width, 180)
        
        # If we have previous comparison data, show it
        if self.last_comparison_data:
            self._restore_previous_comparison()
        else:
            # Build results placeholder
            self._build_results_placeholder(window_width, 280)

    def _build_city_inputs(self, window_width, y_start):
        """
        Build input fields for city comparison.
        
        Args:
            window_width: Current window width
            y_start: Y position to start building inputs
        """
        # City 1 input
        city1_label = self._create_label(
            text=self.gui.language_controller.get_text("city_1"),
            font=("Arial", int(14 + window_width/80), "bold"),
            fg=self.app.text_color,
            x=window_width/4,
            y=y_start
        )
        self.comparison_widgets.append(city1_label)
        
        # Initialize city variables - use last compared cities if available
        if not hasattr(self, 'city1_var') or self.city1_var is None:
            default_city1 = "New York"
            if self.last_compared_cities:
                default_city1 = self.last_compared_cities[0]
            self.city1_var = tk.StringVar(value=default_city1)
        
        city1_entry = tk.Entry(
            self.app,
            textvariable=self.city1_var,
            font=("Arial", int(12 + window_width/100)),
            width=20,
            justify="center",
            bg="white",
            fg="black",
            relief="solid",
            borderwidth=1,
            highlightthickness=0
        )
        city1_entry.place(x=window_width/4, y=y_start + 30, anchor="center")
        self.comparison_widgets.append(city1_entry)
        
        # City 2 input  
        city2_label = self._create_label(
            text=self.gui.language_controller.get_text("city_2"),
            font=("Arial", int(14 + window_width/80), "bold"),
            fg=self.app.text_color,
            x=3*window_width/4,
            y=y_start
        )
        self.comparison_widgets.append(city2_label)
        
        if not hasattr(self, 'city2_var') or self.city2_var is None:
            default_city2 = "London"
            if self.last_compared_cities:
                default_city2 = self.last_compared_cities[1]
            self.city2_var = tk.StringVar(value=default_city2)
        
        city2_entry = tk.Entry(
            self.app,
            textvariable=self.city2_var,
            font=("Arial", int(12 + window_width/100)),
            width=20,
            justify="center",
            bg="white",
            fg="black",
            relief="solid",
            borderwidth=1,
            highlightthickness=0
        )
        city2_entry.place(x=3*window_width/4, y=y_start + 30, anchor="center")
        self.comparison_widgets.append(city2_entry)
        
        # Compare button
        compare_btn = tk.Button(
            self.app,
            text=self.gui.language_controller.get_text("compare_cities"),
            command=self.perform_comparison,
            bg="grey",
            fg="black",
            font=("Arial", int(12 + window_width/100), "bold"),
            relief="raised",
            borderwidth=2,
            width=15,
            height=2,
            activeforeground="black",
            activebackground="lightgrey",
            highlightthickness=0,
            cursor="hand2"
        )
        compare_btn.place(x=window_width/2, y=y_start + 30, anchor="center")
        self.comparison_widgets.append(compare_btn)

    def _build_results_placeholder(self, window_width, y_start):
        """
        Build placeholder for comparison results.
        
        Args:
            window_width: Current window width
            y_start: Y position to start building placeholder
        """
        placeholder_text = self.gui.language_controller.get_text("comparison_placeholder")
        placeholder = self._create_label(
            text=placeholder_text,
            font=("Arial", int(14 + window_width/80)),
            fg=self.app.text_color,
            x=window_width/2,
            y=y_start + 100
        )
        self.comparison_widgets.append(placeholder)

    def perform_comparison(self):
        """Perform the actual city comparison."""
        # Only perform comparison if we're on the comparison page
        if not self.is_active:
            return
            
        try:
            city1 = self.city1_var.get().strip() or "New York"
            city2 = self.city2_var.get().strip() or "London"
            
            current_cities = (city1.lower(), city2.lower())
            
            # Check if these are the same cities as last comparison
            if (self.last_compared_cities and 
                (current_cities[0] == self.last_compared_cities[0].lower() and 
                 current_cities[1] == self.last_compared_cities[1].lower()) and
                self.last_comparison_data):
                
                # Same cities - just redisplay existing results
                self._clear_results_only()
                self._restore_previous_comparison()
                return
            
            # Different cities - fetch new data
            self.last_compared_cities = (city1, city2)
            
            # Clear existing results when starting new comparison
            self._clear_results_only()
            
            # Show loading message
            self._show_loading_message()
            
            # Start comparison in background thread
            threading.Thread(
                target=self._fetch_and_display,
                args=(city1, city2),
                daemon=True
            ).start()
            
        except Exception as e:
            error_text = self.gui.language_controller.get_text("comparison_error")
            self._show_error(error_text)

    def _fetch_and_display(self, city1, city2):
        """
        Fetch weather data and display results in background thread.
        
        Args:
            city1: First city to compare
            city2: Second city to compare
        """
        try:
            # Get language code for API requests
            language_code = self.app.get_current_language_code()
            
            # Fetch weather data for both cities
            weather1 = get_current_weather(city1, language_code)
            weather2 = get_current_weather(city2, language_code)
            
            # Update display on main thread ONLY if still active
            if self.is_active:
                self.app.after(0, lambda: self._display_results(
                    city1, weather1, city2, weather2
                ))
            
        except Exception as e:
            # Show error on main thread ONLY if still active
            if self.is_active:
                error_text = self.gui.language_controller.get_text("comparison_error")
                self.app.after(0, lambda: self._show_error(error_text))

    def _display_results(self, city1, weather1, city2, weather2):
        """
        Display comparison results.
        
        Args:
            city1: First city name
            weather1: First city weather data
            city2: Second city name  
            weather2: Second city weather data
        """
        # Only display if we're still on the comparison page
        if not self.is_active:
            return
            
        try:
            # Clear loading message
            self._clear_results_only()
            
            # Check for errors in weather data
            if weather1.get("error") or weather2.get("error"):
                error_text = self.gui.language_controller.get_text("comparison_error")
                self._show_error(error_text)
                return
            
            # Store comparison data for persistence
            self.last_comparison_data = {
                'city1': city1,
                'weather1': weather1,
                'city2': city2,
                'weather2': weather2
            }
            
            # Display comparison
            self._create_side_by_side_display(city1, weather1, city2, weather2)
            
        except Exception as e:
            error_text = self.gui.language_controller.get_text("comparison_error")
            self._show_error(error_text)

    def _restore_previous_comparison(self):
        """Restore the previous comparison results."""
        if self.last_comparison_data and self.is_active:
            data = self.last_comparison_data
            self._create_side_by_side_display(
                data['city1'], data['weather1'], 
                data['city2'], data['weather2']
            )

    def _create_side_by_side_display(self, city1, weather1, city2, weather2):
        """
        Create side-by-side weather comparison display.
        
        Args:
            city1 (str): First city name
            weather1 (dict): First city weather data
            city2 (str): Second city name
            weather2 (dict): Second city weather data
        """
        # Only create if we're still active
        if not self.is_active:
            return
            
        window_width = self.app.winfo_width()
        y_start = 320
        
        # City headers
        city1_header = self._create_label(
            text=f"🏙️ {city1.title()}",
            font=("Arial", int(18 + window_width/70), "bold"),
            fg=self.app.text_color,
            x=window_width/4,
            y=y_start
        )
        self.comparison_widgets.append(city1_header)
        
        city2_header = self._create_label(
            text=f"🏙️ {city2.title()}",
            font=("Arial", int(18 + window_width/70), "bold"),
            fg=self.app.text_color,
            x=3*window_width/4,
            y=y_start
        )
        self.comparison_widgets.append(city2_header)
        
        # Temperature comparison
        self._create_temperature_comparison(weather1, weather2, window_width, y_start + 40)
        
        # Description comparison
        self._create_description_comparison(weather1, weather2, window_width, y_start + 80)
        
        # Metrics comparison
        self._create_metrics_comparison(weather1, weather2, window_width, y_start + 120)

    def _create_temperature_comparison(self, weather1, weather2, window_width, y_pos):
        """Create temperature comparison labels."""
        if not self.is_active:
            return
            
        # Extract and convert temperatures
        temp1 = weather1.get("temperature", 0)
        temp2 = weather2.get("temperature", 0)
        
        if self.app.unit == "F":
            temp1 = round(temp1 * 9/5 + 32, 1) if temp1 else 0
            temp2 = round(temp2 * 9/5 + 32, 1) if temp2 else 0
            unit = "°F"
        else:
            temp1 = round(temp1, 1) if temp1 else 0
            temp2 = round(temp2, 1) if temp2 else 0
            unit = "°C"
        
        # Create temperature labels
        temp1_label = self._create_label(
            text=f"🌡️ {temp1}{unit}",
            font=("Arial", int(16 + window_width/80)),
            fg=self.app.text_color,
            x=window_width/4,
            y=y_pos
        )
        self.comparison_widgets.append(temp1_label)
        
        temp2_label = self._create_label(
            text=f"🌡️ {temp2}{unit}",
            font=("Arial", int(16 + window_width/80)),
            fg=self.app.text_color,
            x=3*window_width/4,
            y=y_pos
        )
        self.comparison_widgets.append(temp2_label)

    def _create_description_comparison(self, weather1, weather2, window_width, y_pos):
        """Create weather description comparison labels."""
        if not self.is_active:
            return
            
        desc1 = weather1.get("description", "N/A")
        desc2 = weather2.get("description", "N/A")
        
        desc1_label = self._create_label(
            text=f"☁️ {desc1}",
            font=("Arial", int(14 + window_width/90)),
            fg=self.app.text_color,
            x=window_width/4,
            y=y_pos
        )
        self.comparison_widgets.append(desc1_label)
        
        desc2_label = self._create_label(
            text=f"☁️ {desc2}",
            font=("Arial", int(14 + window_width/90)),
            fg=self.app.text_color,
            x=3*window_width/4,
            y=y_pos
        )
        self.comparison_widgets.append(desc2_label)

    def _create_metrics_comparison(self, weather1, weather2, window_width, y_start):
        """Create weather metrics comparison labels."""
        if not self.is_active:
            return
            
        # Define metrics to compare
        metrics = [
            ("💧", "humidity", "%"),
            ("🌬️", "wind_speed", " m/s"),
            ("🧭", "pressure", " hPa")
        ]
        
        for i, (emoji, key, unit_suffix) in enumerate(metrics):
            val1 = weather1.get(key, "N/A")
            val2 = weather2.get(key, "N/A")
            
            val1_text = f"{val1}{unit_suffix}" if val1 != "N/A" else "N/A"
            val2_text = f"{val2}{unit_suffix}" if val2 != "N/A" else "N/A"
            
            metric1_label = self._create_label(
                text=f"{emoji} {val1_text}",
                font=("Arial", int(12 + window_width/100)),
                fg=self.app.text_color,
                x=window_width/4,
                y=y_start + (i * 30)
            )
            self.comparison_widgets.append(metric1_label)
            
            metric2_label = self._create_label(
                text=f"{emoji} {val2_text}",
                font=("Arial", int(12 + window_width/100)),
                fg=self.app.text_color,
                x=3*window_width/4,
                y=y_start + (i * 30)
            )
            self.comparison_widgets.append(metric2_label)

    def _show_loading_message(self):
        """Show loading message while fetching data."""
        if not self.is_active:
            return
            
        window_width = self.app.winfo_width()
        loading_text = self.gui.language_controller.get_text("loading_comparison")
        
        loading_label = self._create_label(
            text=loading_text,
            font=("Arial", int(14 + window_width/80)),
            fg=self.app.text_color,
            x=window_width/2,
            y=400
        )
        self.comparison_widgets.append(loading_label)

    def _show_error(self, error_text):
        """
        Show error message for comparison failures.
        
        Args:
            error_text (str): Error message to display
        """
        if not self.is_active:
            return
            
        window_width = self.app.winfo_width()
        
        error_label = self._create_label(
            text=f"❌ {error_text}",
            font=("Arial", int(14 + window_width/80)),
            fg=self.app.text_color,
            x=window_width/2,
            y=400
        )
        self.comparison_widgets.append(error_label)

    def _clear_results_only(self):
        """Clear comparison results while keeping input fields and headers."""
        # Only clear widgets that are results (not inputs, headers, or buttons)
        widgets_to_keep = []
        for widget in self.comparison_widgets:
            try:
                # Keep inputs, labels, and buttons in the upper area (y < 300)
                if (hasattr(widget, 'winfo_y') and widget.winfo_y() < 300):
                    widgets_to_keep.append(widget)
                else:
                    widget.destroy()
            except:
                # If we can't check position, assume it's a result widget and remove it
                try:
                    widget.destroy()
                except:
                    pass
        
        self.comparison_widgets = widgets_to_keep

    def _add_back_button(self):
        """Add back button to return to main page."""
        back_text = self.gui.language_controller.get_text("back")
        back_btn = tk.Button(
            self.app,
            text=back_text,
            command=self._go_back_to_main,
            bg="grey",
            fg="black",
            font=("Arial", 12, "bold"),
            relief="raised",
            borderwidth=2,
            width=8,
            height=1,
            activeforeground="black",
            activebackground="lightgrey",
            highlightthickness=0
        )
        back_btn.place(x=50, y=50, anchor="center")
        self.comparison_widgets.append(back_btn)

    def _go_back_to_main(self):
        """Go back to main page."""
        # Mark as inactive
        self.is_active = False
        
        # Only clear widgets, not the stored data
        self._clear_all_widgets()
        
        # Navigate to main page
        self.gui.show_page("main")

    def _create_label(self, text, font, fg, x, y, anchor="center", **kwargs):
        """
        Create a label with transparent background matching canvas.
        
        Args:
            text: Label text
            font: Font specification
            fg: Text color
            x, y: Position coordinates
            anchor: Positioning anchor
            **kwargs: Additional label options
            
        Returns:
            tk.Label: Created label widget
        """
        # Get canvas background color
        canvas_bg = "#87CEEB"
        if hasattr(self.gui, 'bg_canvas') and self.gui.bg_canvas:
            try:
                canvas_bg = self.gui.bg_canvas.cget("bg")
            except:
                canvas_bg = "#87CEEB"
        
        label = tk.Label(
            self.app,
            text=text,
            font=font,
            fg=fg,
            bg=canvas_bg,
            anchor=anchor,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            **kwargs
        )
        label.place(x=x, y=y, anchor=anchor)
        return label

    def cleanup(self):
        """Clean up comparison widgets but preserve data for returning to page."""
        # Mark as inactive
        self.is_active = False
        
        # Clear widgets but KEEP comparison data and last compared cities
        self._clear_all_widgets()

    def force_clear_data(self):
        """Force clear all comparison data - use this when app is closing."""
        self.last_comparison_data = None
        self.last_compared_cities = None
        self.cleanup()

    def _clear_all_widgets(self):
        """Clear all comparison widgets completely."""
        for widget in self.comparison_widgets:
            try:
                widget.destroy()
            except:
                pass
        self.comparison_widgets.clear()