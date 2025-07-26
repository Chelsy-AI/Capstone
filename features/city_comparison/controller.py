"""
City Comparison Feature Module
==============================

This module provides city-to-city weather comparison functionality.
Users can compare current weather conditions between multiple cities
with side-by-side displays showing temperature, humidity, wind, and more.

Features:
- Compare up to 2 cities simultaneously
- Side-by-side weather metrics display
- Multi-language support
- Real-time weather data fetching
- Error handling for invalid cities
- Responsive design
"""

from .controller import CityComparisonController

__all__ = ['CityComparisonController']


# ===================================================================
# FILE 2: features/city_comparison/controller.py
# ===================================================================
"""
City Comparison Controller
==========================

Main controller for the city comparison feature. Manages the UI,
coordinates data fetching, and handles user interactions.
"""

import tkinter as tk
import threading
from .api import fetch_comparison_data
from .display import ComparisonDisplay


class CityComparisonController:
    """
    City Comparison Controller Class
    
    This controller manages the city comparison feature, handling UI creation,
    data fetching, and result display coordination.
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
        self.display = ComparisonDisplay(app, gui_controller)
        
        # Variables for city inputs
        self.city1_var = None
        self.city2_var = None
        
        # Track comparison widgets for cleanup
        self.comparison_widgets = []

    def build_page(self, window_width, window_height):
        """
        Build the city comparison page with translated text.
        
        Args:
            window_width: Current window width
            window_height: Current window height
        """
        # Clear any existing comparison widgets
        self._clear_widgets()
        
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
        
        # Initialize city variables if not already done
        if not hasattr(self, 'city1_var') or self.city1_var is None:
            self.city1_var = tk.StringVar(value="New York")
        
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
            self.city2_var = tk.StringVar(value="London")
        
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
        """
        Perform the actual city comparison.
        
        Fetches weather data for both cities and displays results.
        """
        try:
            city1 = self.city1_var.get().strip() or "New York"
            city2 = self.city2_var.get().strip() or "London"
            
            # Clear existing results
            self._clear_results()
            
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
            self.display.show_error(error_text)

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
            weather1, weather2 = fetch_comparison_data(city1, city2, language_code)
            
            # Update display on main thread
            self.app.after(0, lambda: self._display_results(
                city1, weather1, city2, weather2
            ))
            
        except Exception as e:
            # Show error on main thread
            error_text = self.gui.language_controller.get_text("comparison_error")
            self.app.after(0, lambda: self.display.show_error(error_text))

    def _display_results(self, city1, weather1, city2, weather2):
        """
        Display comparison results using the display module.
        
        Args:
            city1: First city name
            weather1: First city weather data
            city2: Second city name  
            weather2: Second city weather data
        """
        try:
            # Clear loading message
            self._clear_results()
            
            # Check for errors in weather data
            if weather1.get("error") or weather2.get("error"):
                error_text = self.gui.language_controller.get_text("comparison_error")
                self.display.show_error(error_text)
                return
            
            # Display comparison using display module
            comparison_widgets = self.display.create_side_by_side_display(
                city1, weather1, city2, weather2
            )
            
            # Track the new widgets for cleanup
            self.comparison_widgets.extend(comparison_widgets)
            
        except Exception as e:
            error_text = self.gui.language_controller.get_text("comparison_error")
            self.display.show_error(error_text)

    def _show_loading_message(self):
        """Show loading message while fetching data."""
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

    def _clear_results(self):
        """Clear comparison results while keeping input fields."""
        # Only clear widgets that are not input-related
        widgets_to_keep = []
        for widget in self.comparison_widgets:
            try:
                # Keep labels and entry widgets for inputs
                if (hasattr(widget, 'winfo_class') and 
                    widget.winfo_class() in ['Label', 'Entry', 'Button'] and
                    widget.winfo_y() < 250):  # Keep widgets in input area
                    widgets_to_keep.append(widget)
                else:
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
            command=lambda: self.gui.show_page("main"),
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
        """Clean up comparison widgets and resources."""
        self._clear_widgets()

    def _clear_widgets(self):
        """Clear all comparison widgets."""
        for widget in self.comparison_widgets:
            try:
                widget.destroy()
            except:
                pass
        self.comparison_widgets.clear()


# ===================================================================
# FILE 3: features/city_comparison/api.py
# ===================================================================
"""
City Comparison API Module
===========================

Handles weather data fetching for city comparison feature.
"""

from config.api import get_current_weather


def fetch_comparison_data(city1, city2, language_code="en"):
    """
    Fetch weather data for two cities for comparison.
    
    Args:
        city1 (str): First city name
        city2 (str): Second city name
        language_code (str): Language code for API requests
        
    Returns:
        tuple: (weather1_data, weather2_data)
    """
    try:
        # Fetch weather data for both cities
        weather1 = get_current_weather(city1, language_code)
        weather2 = get_current_weather(city2, language_code)
        
        return weather1, weather2
        
    except Exception as e:
        # Return error data for both cities
        error_data = {"error": str(e)}
        return error_data, error_data


def validate_city_name(city_name):
    """
    Validate city name format.
    
    Args:
        city_name (str): City name to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not city_name or not isinstance(city_name, str):
        return False
    
    # Remove extra whitespace
    city_name = city_name.strip()
    
    # Check minimum length
    if len(city_name) < 2:
        return False
    
    # Check for valid characters (letters, spaces, hyphens, apostrophes)
    import re
    pattern = r"^[a-zA-Z\s\-'\.]+$"
    return bool(re.match(pattern, city_name))


def format_city_name(city_name):
    """
    Format city name for API requests.
    
    Args:
        city_name (str): Raw city name input
        
    Returns:
        str: Formatted city name
    """
    if not city_name:
        return ""
    
    # Remove extra whitespace and convert to title case
    formatted = city_name.strip().title()
    
    # Handle special cases
    formatted = formatted.replace("'S", "'s")  # Fix possessives
    formatted = formatted.replace(" Of ", " of ")  # Fix prepositions
    formatted = formatted.replace(" The ", " the ")  # Fix articles
    
    return formatted


# ===================================================================
# FILE 4: features/city_comparison/display.py
# ===================================================================
"""
City Comparison Display Module
===============================

Handles the visual display of city comparison results.
"""

import tkinter as tk


class ComparisonDisplay:
    """
    City Comparison Display Manager
    
    Handles creating and managing the visual display of weather
    comparison data between cities.
    """
    
    def __init__(self, app, gui_controller):
        """
        Initialize comparison display manager.
        
        Args:
            app: Main weather application instance
            gui_controller: GUI controller instance
        """
        self.app = app
        self.gui = gui_controller

    def create_side_by_side_display(self, city1, weather1, city2, weather2):
        """
        Create side-by-side weather comparison display.
        
        Args:
            city1 (str): First city name
            weather1 (dict): First city weather data
            city2 (str): Second city name
            weather2 (dict): Second city weather data
            
        Returns:
            list: List of created widgets for tracking
        """
        widgets = []
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
        widgets.append(city1_header)
        
        city2_header = self._create_label(
            text=f"🏙️ {city2.title()}",
            font=("Arial", int(18 + window_width/70), "bold"),
            fg=self.app.text_color,
            x=3*window_width/4,
            y=y_start
        )
        widgets.append(city2_header)
        
        # Temperature comparison
        temp_widgets = self._create_temperature_comparison(
            weather1, weather2, window_width, y_start + 40
        )
        widgets.extend(temp_widgets)
        
        # Description comparison
        desc_widgets = self._create_description_comparison(
            weather1, weather2, window_width, y_start + 80
        )
        widgets.extend(desc_widgets)
        
        # Metrics comparison
        metrics_widgets = self._create_metrics_comparison(
            weather1, weather2, window_width, y_start + 120
        )
        widgets.extend(metrics_widgets)
        
        return widgets

    def _create_temperature_comparison(self, weather1, weather2, window_width, y_pos):
        """Create temperature comparison labels."""
        widgets = []
        
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
        widgets.append(temp1_label)
        
        temp2_label = self._create_label(
            text=f"🌡️ {temp2}{unit}",
            font=("Arial", int(16 + window_width/80)),
            fg=self.app.text_color,
            x=3*window_width/4,
            y=y_pos
        )
        widgets.append(temp2_label)
        
        return widgets

    def _create_description_comparison(self, weather1, weather2, window_width, y_pos):
        """Create weather description comparison labels."""
        widgets = []
        
        desc1 = weather1.get("description", "N/A")
        desc2 = weather2.get("description", "N/A")
        
        desc1_label = self._create_label(
            text=f"☁️ {desc1}",
            font=("Arial", int(14 + window_width/90)),
            fg=self.app.text_color,
            x=window_width/4,
            y=y_pos
        )
        widgets.append(desc1_label)
        
        desc2_label = self._create_label(
            text=f"☁️ {desc2}",
            font=("Arial", int(14 + window_width/90)),
            fg=self.app.text_color,
            x=3*window_width/4,
            y=y_pos
        )
        widgets.append(desc2_label)
        
        return widgets

    def _create_metrics_comparison(self, weather1, weather2, window_width, y_start):
        """Create weather metrics comparison labels."""
        widgets = []
        
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
            widgets.append(metric1_label)
            
            metric2_label = self._create_label(
                text=f"{emoji} {val2_text}",
                font=("Arial", int(12 + window_width/100)),
                fg=self.app.text_color,
                x=3*window_width/4,
                y=y_start + (i * 30)
            )
            widgets.append(metric2_label)
        
        return widgets

    def show_error(self, error_text):
        """
        Show error message for comparison failures.
        
        Args:
            error_text (str): Error message to display
        """
        window_width = self.app.winfo_width()
        
        error_label = self._create_label(
            text=f"❌ {error_text}",
            font=("Arial", int(14 + window_width/80)),
            fg=self.app.text_color,
            x=window_width/2,
            y=400
        )
        
        # Add to GUI widgets for tracking
        if hasattr(self.gui, 'widgets'):
            self.gui.widgets.append(error_label)

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