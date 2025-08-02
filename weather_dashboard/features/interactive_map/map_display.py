"""
Interactive Map Display Widget
=============================

Enhanced map display component with weather overlays and information panel.

Features:
- Interactive map widget with weather overlay support
- Information button with detailed overlay descriptions
- Automatic city location lookup and display
- Weather data visualization with multiple overlay types
- Fallback handling for map initialization errors
- Integrated popup information system

This module provides complete map display functionality including
weather overlays and user information interfaces.
"""

import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
import os

class MapDisplay:
    def __init__(self, parent, get_city_callback, language_controller, app_reference):
        """
        Initialize the enhanced map display with weather overlays.
        
        Args:
            parent: Parent widget to contain the map
            get_city_callback: Function to get current city name
            language_controller: Language controller for translations
            app_reference: Reference to main app for styling
        """
        self.parent = parent
        self.get_city_callback = get_city_callback
        self.language_controller = language_controller
        self.app = app_reference
        self.widgets = []
        
        # Get window dimensions for responsive design
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        # Initialize map controller
        self.map_controller = None
        
        # Build the map display
        self._build_map_display(window_width, window_height)

    def _build_map_display(self, window_width, window_height):
        """Build the complete map display with information button."""
        # Map display area
        map_y_position = window_height/2 + 40
        
        # Get canvas background color for consistency
        canvas_bg = "#87CEEB"
        if hasattr(self.app, 'bg_canvas') and self.app.bg_canvas:
            try:
                canvas_bg = self.app.bg_canvas.cget("bg")
            except:
                canvas_bg = "#87CEEB"
        
        # Create map frame
        map_frame = tk.Frame(
            self.parent,
            bg=canvas_bg,
            relief="solid",
            borderwidth=2,
            highlightthickness=0
        )
        map_frame.place(x=window_width/2, y=map_y_position, anchor="center", width=600, height=400)
        self.widgets.append(map_frame)
        
        # Try to initialize map controller
        try:
            from weather_dashboard.features.interactive_map.controller import MapController
            api_key = os.getenv("weatherdb_api_key")
            
            # Initialize map controller with translation function
            self.map_controller = MapController(
                map_frame, 
                self.get_city_callback, 
                api_key, 
                show_grid=True,
                translate_func=self.language_controller.get_text
            )
            
            # Info button - placed in map display
            info_btn = tk.Button(
                self.parent,
                text="i",
                command=self._show_detailed_map_info_popup,
                bg="grey",
                fg="black",
                font=("Arial", 12, "bold"),
                relief="raised",
                borderwidth=2,
                width=3,
                height=1,
                activeforeground="black",
                activebackground="lightgrey",
                highlightthickness=0
            )
            info_btn.place(x=window_width/2 + 180, y=100, anchor="center")
            self.widgets.append(info_btn)
            
        except Exception as e:
            # Show fallback placeholder with translated text
            map_unavailable_text = self.language_controller.get_text("map_unavailable")
            map_placeholder = self._create_label(
                map_frame,
                text=f"🗺️\n{map_unavailable_text}",
                font=("Arial", int(16 + window_width/80)),
                fg=self.app.text_color,
                x=300,
                y=200
            )
            
            # Fallback info button that shows simple popup
            info_text = self.language_controller.get_text("map_info")
            info_btn = tk.Button(
                self.parent,
                text="i",
                command=lambda: self._show_map_info(info_text),
                bg="grey",
                fg="black",
                font=("Arial", 12, "bold"),
                relief="raised",
                borderwidth=2,
                width=3,
                height=1,
                activeforeground="black",
                activebackground="lightgrey",
                highlightthickness=0
            )
            info_btn.place(x=window_width/2 + 180, y=100, anchor="center")
            self.widgets.append(info_btn)

    def _create_label(self, parent, text, font, fg, x, y, anchor="center", **kwargs):
        """
        Create a label with transparent background - NO BLUE BOXES!
        
        Args:
            parent: The widget to put this label in
            text: The text to display (should be properly translated)
            font: Font specification (family, size, style)
            fg: Text color
            x, y: Position where to place the label
            anchor: How to position the label relative to x,y
            **kwargs: Any additional label options
            
        Returns:
            tk.Label: The created label widget
        """
        # Get the current canvas background color
        canvas_bg = "#87CEEB"  # Default sky blue
        if hasattr(self.app, 'bg_canvas') and self.app.bg_canvas:
            try:
                canvas_bg = self.app.bg_canvas.cget("bg")
            except:
                canvas_bg = "#87CEEB"
        
        # Create the label with matching background
        label = tk.Label(
            parent,
            text=text,
            font=font,
            fg=fg,
            bg=canvas_bg,  # This prevents ugly blue boxes!
            anchor=anchor,
            relief="flat",        # No 3D border effect
            borderwidth=0,        # No border
            highlightthickness=0, # No highlight border
            **kwargs
        )
        
        # Position the label
        label.place(x=x, y=y, anchor=anchor)
        return label

    def _show_detailed_map_info_popup(self):
        """Show detailed map information in a styled popup window matching the design."""
        # Create popup window
        popup = tk.Toplevel(self.app)
        popup.title(self.language_controller.get_text("map_information"))
        popup.geometry("900x600")
        popup.resizable(True, True)
        popup.configure(bg="#404040")  # Dark gray background
        
        # Center the popup on the parent window
        popup.transient(self.app)
        popup.grab_set()  # Make it modal
        
        # Get current overlay selection if map controller exists
        current_overlay = "none"
        if hasattr(self, 'map_controller') and self.map_controller and hasattr(self.map_controller, 'layer_var'):
            current_overlay_display = self.map_controller.layer_var.get()
            # Find the key for the display value
            for key, value in self.map_controller.layer_options.items():
                if value == current_overlay_display:
                    current_overlay = key
                    break
        
        # Main content frame
        main_frame = tk.Frame(popup, bg="#404040")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Title with rocket icon
        title_frame = tk.Frame(main_frame, bg="#404040")
        title_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Rocket emoji (using a large font)
        rocket_label = tk.Label(
            title_frame,
            text="🚀",
            font=("Arial", 48),
            bg="#404040",
            fg="white"
        )
        rocket_label.pack(side=tk.LEFT, padx=(0, 20))
        
        # Title text - using translated text
        title_text = self.language_controller.get_text("base_map_info")
        title_label = tk.Label(
            title_frame,
            text=title_text,
            font=("Arial", 24, "bold"),
            bg="#404040",
            fg="white",
            anchor="w"
        )
        title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # What This Shows section
        shows_frame = tk.Frame(main_frame, bg="#404040")
        shows_frame.pack(fill=tk.X, pady=(0, 30), anchor="w")
        
        # Chart icon and "What This Shows:" header
        shows_header_frame = tk.Frame(shows_frame, bg="#404040")
        shows_header_frame.pack(fill=tk.X, pady=(0, 15))
        
        chart_icon = tk.Label(
            shows_header_frame,
            text="📊",
            font=("Arial", 20),
            bg="#404040",
            fg="white"
        )
        chart_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        shows_header_text = self.language_controller.get_text("map_features")
        shows_header = tk.Label(
            shows_header_frame,
            text=f"{shows_header_text}:",
            font=("Arial", 20, "bold"),
            bg="#404040",
            fg="white",
            anchor="w"
        )
        shows_header.pack(side=tk.LEFT)
        
        # Bullet points for "What This Shows" - using translated features
        features = [
            self.language_controller.get_text('feature_navigation'),
            self.language_controller.get_text('feature_overlays'),
            self.language_controller.get_text('feature_tracking'),
            self.language_controller.get_text('feature_integration')
        ]
        
        for feature in features:
            point_frame = tk.Frame(shows_frame, bg="#404040")
            point_frame.pack(fill=tk.X, pady=2, padx=(30, 0))
            
            bullet = tk.Label(
                point_frame,
                text="•",
                font=("Arial", 18),
                bg="#404040",
                fg="white"
            )
            bullet.pack(side=tk.LEFT, padx=(0, 10))
            
            point_label = tk.Label(
                point_frame,
                text=feature,
                font=("Arial", 18),
                bg="#404040",
                fg="white",
                anchor="w",
                wraplength=800,
                justify="left"
            )
            point_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Understanding the Map section
        understanding_frame = tk.Frame(main_frame, bg="#404040")
        understanding_frame.pack(fill=tk.X, pady=(0, 40), anchor="w")
        
        # Graph icon and "Understanding the Map:" header
        understanding_header_frame = tk.Frame(understanding_frame, bg="#404040")
        understanding_header_frame.pack(fill=tk.X, pady=(0, 15))
        
        graph_icon = tk.Label(
            understanding_header_frame,
            text="📈",
            font=("Arial", 20),
            bg="#404040",
            fg="white"
        )
        graph_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        overlay_info_text = self.language_controller.get_text("overlay_information")
        understanding_header = tk.Label(
            understanding_header_frame,
            text=f"{overlay_info_text}:",
            font=("Arial", 20, "bold"),
            bg="#404040",
            fg="white",
            anchor="w"
        )
        understanding_header.pack(side=tk.LEFT)
        
        # Show current overlay status
        current_display = self.language_controller.get_text('overlay_none')
        if hasattr(self, 'map_controller') and self.map_controller and hasattr(self.map_controller, 'layer_options'):
            if current_overlay in self.map_controller.layer_options:
                current_display = self.map_controller.layer_options[current_overlay]
        
        current_overlay_text = self.language_controller.get_text('current_overlay')
        current_status = f"{current_overlay_text}: {current_display}"
        
        current_frame = tk.Frame(understanding_frame, bg="#404040")
        current_frame.pack(fill=tk.X, pady=2, padx=(30, 0))
        
        bullet = tk.Label(
            current_frame,
            text="•",
            font=("Arial", 18),
            bg="#404040",
            fg="white"
        )
        bullet.pack(side=tk.LEFT, padx=(0, 10))
        
        current_label = tk.Label(
            current_frame,
            text=current_status,
            font=("Arial", 18),
            bg="#404040",
            fg="#4CAF50",  # Green color for current status
            anchor="w",
            wraplength=800,
            justify="left"
        )
        current_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Add overlay-specific information if available
        if current_overlay != "none":
            overlay_info = self._get_overlay_info_for_popup(current_overlay)
            if overlay_info:
                # Add description
                desc_frame = tk.Frame(understanding_frame, bg="#404040")
                desc_frame.pack(fill=tk.X, pady=2, padx=(30, 0))
                
                desc_bullet = tk.Label(
                    desc_frame,
                    text="•",
                    font=("Arial", 18),
                    bg="#404040",
                    fg="white"
                )
                desc_bullet.pack(side=tk.LEFT, padx=(0, 10))
                
                desc_label = tk.Label(
                    desc_frame,
                    text=overlay_info['description'],
                    font=("Arial", 18),
                    bg="#404040",
                    fg="white",
                    anchor="w",
                    wraplength=800,
                    justify="left"
                )
                desc_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        else:
            # Show "no overlay selected" message
            no_overlay_text = self.language_controller.get_text('no_overlay_selected')
            no_frame = tk.Frame(understanding_frame, bg="#404040")
            no_frame.pack(fill=tk.X, pady=2, padx=(30, 0))
            
            no_bullet = tk.Label(
                no_frame,
                text="•",
                font=("Arial", 18),
                bg="#404040",
                fg="white"
            )
            no_bullet.pack(side=tk.LEFT, padx=(0, 10))
            
            no_label = tk.Label(
                no_frame,
                text=no_overlay_text,
                font=("Arial", 18),
                bg="#404040",
                fg="white",
                anchor="w",
                wraplength=800,
                justify="left"
            )
            no_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # OK button at bottom right (styled like the image)
        button_frame = tk.Frame(main_frame, bg="#404040")
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        ok_button = tk.Button(
            button_frame,
            text="OK",
            command=popup.destroy,
            bg="#2196F3",  # Blue background
            fg="white",
            font=("Arial", 16, "bold"),
            relief="flat",
            borderwidth=0,
            width=8,
            height=2,
            cursor="hand2",
            activebackground="#1976D2",  # Darker blue when pressed
            activeforeground="white"
        )
        ok_button.pack(side=tk.RIGHT, padx=(0, 0), pady=(20, 0))
        
        # Center the popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        
        # Focus on the OK button for keyboard accessibility
        ok_button.focus_set()
        
        # Allow Enter key to close the popup
        popup.bind('<Return>', lambda e: popup.destroy())
        popup.bind('<Escape>', lambda e: popup.destroy())

    def _get_overlay_info_for_popup(self, layer_key):
        """Get detailed information about a specific weather overlay for popup."""
        overlay_data = {
            "temp_new": {
                "title": self.language_controller.get_text("temperature_overlay_info"),
                "description": self.language_controller.get_text("temperature_overlay_desc"),
                "features": self.language_controller.get_text("temperature_overlay_features")
            },
            "wind_new": {
                "title": self.language_controller.get_text("wind_overlay_info"),
                "description": self.language_controller.get_text("wind_overlay_desc"),
                "features": self.language_controller.get_text("wind_overlay_features")
            },
            "precipitation_new": {
                "title": self.language_controller.get_text("precipitation_overlay_info"),
                "description": self.language_controller.get_text("precipitation_overlay_desc"),
                "features": self.language_controller.get_text("precipitation_overlay_features")
            },
            "clouds_new": {
                "title": self.language_controller.get_text("clouds_overlay_info"),
                "description": self.language_controller.get_text("clouds_overlay_desc"),
                "features": self.language_controller.get_text("clouds_overlay_features")
            },
            "pressure_new": {
                "title": self.language_controller.get_text("pressure_overlay_info"),
                "description": self.language_controller.get_text("pressure_overlay_desc"),
                "features": self.language_controller.get_text("pressure_overlay_features")
            },
            "snow_new": {
                "title": self.language_controller.get_text("snow_overlay_info"),
                "description": self.language_controller.get_text("snow_overlay_desc"),
                "features": self.language_controller.get_text("snow_overlay_features")
            },
            "dewpoint_new": {
                "title": self.language_controller.get_text("dewpoint_overlay_info"),
                "description": self.language_controller.get_text("dewpoint_overlay_desc"),
                "features": self.language_controller.get_text("dewpoint_overlay_features")
            }
        }
        
        return overlay_data.get(layer_key)

    def _show_map_info(self, info_text=None):
        """Show detailed map information popup - redirects to our detailed popup."""
        self._show_detailed_map_info_popup()

    def get_widgets(self):
        """Get the list of widgets for cleanup."""
        return self.widgets

    def cleanup(self):
        """Clean up map display resources."""
        # Clean up map controller if it exists
        if hasattr(self, 'map_controller') and self.map_controller:
            try:
                self.map_controller.cleanup()
            except:
                pass
        
        # Destroy widgets
        for widget in self.widgets:
            try:
                widget.destroy()
            except:
                pass
        self.widgets.clear()

    def refresh_map(self):
        """Refresh the map display."""
        if hasattr(self, 'map_controller') and self.map_controller:
            try:
                self.map_controller.refresh()
            except:
                pass