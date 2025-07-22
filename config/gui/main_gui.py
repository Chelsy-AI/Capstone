import tkinter as tk
from tkinter import ttk

from .weather_display import WeatherDisplay
from .animation_controller import AnimationController


class WeatherGUI:
    """
    Main GUI Controller with Page-Based Navigation
    
    This class coordinates all GUI components and serves as the main
    interface between the application logic and the user interface.
    Now uses a page-based system instead of scrolling.
    """
    
    def __init__(self, parent_app):
        """Initialize GUI with reference to parent application"""
        self.app = parent_app
        
        # Initialize GUI components
        self.weather_display = WeatherDisplay(self.app, self)
        self.animation_controller = AnimationController(self.app, self)
        
        # Page management
        self.current_page = "main"
        self.pages = {}
        
        # GUI state tracking
        self.widgets = []
        self.history_labels = []
        
        # Background elements
        self.bg_canvas = None
        self.scrollbar = None  # Will be removed since we don't need scrolling
        
        # Main weather display widgets (references)
        self.humidity_value = None
        self.wind_value = None
        self.pressure_value = None
        self.visibility_value = None
        self.uv_value = None
        self.precipitation_value = None
        
        self.theme_btn = None
        self.city_entry = None
        self.icon_label = None
        self.temp_label = None
        self.desc_label = None
        
        self.temp_prediction = None
        self.accuracy_prediction = None
        self.confidence_prediction = None
        
        self.main_frame = None

    def build_gui(self):
        """Build the complete GUI interface with page system"""
        print("[GUI] Building paginated interface...")
        
        # Clear existing widgets
        self._clear_widgets()
        
        # Bind window events
        self.app.bind("<Configure>", self._on_window_resize)
        
        # Setup background
        self._setup_background()
        
        # Build the main page
        self.show_page("main")
        
        print("[GUI] Paginated interface ready")

    def _clear_widgets(self):
        """Clear existing widgets while preserving special elements"""
        for widget in self.app.winfo_children():
            if (not hasattr(widget, '_preserve') and 
                widget != self.bg_canvas):
                widget.destroy()
        self.widgets.clear()
        self.pages.clear()

    def _setup_background(self):
        """Setup background canvas and animation"""
        if not self.bg_canvas:
            self.bg_canvas = tk.Canvas(
                self.app, 
                highlightthickness=0, 
                bg="#87CEEB"
            )
            self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_canvas._preserve = True
            
            # Initialize animation system
            self.animation_controller.setup_animation(self.bg_canvas)

    def show_page(self, page_name):
        """Show a specific page"""
        print(f"[GUI] Showing page: {page_name}")
        
        # Clean up any page-specific resources
        self._cleanup_page_resources()
        
        # Clear current widgets but preserve background
        self._clear_page_widgets()
        
        # Update current page
        self.current_page = page_name
        
        # Build the requested page
        if page_name == "main":
            self._build_main_page()
        elif page_name == "prediction":
            self._build_prediction_page()
        elif page_name == "history":
            self._build_history_page()
        elif page_name == "map":
            self._build_map_page()
        
        # Restore current data after building the page
        self._restore_current_data()

    def _cleanup_page_resources(self):
        """Clean up page-specific resources like map controllers"""
        # Clean up map controller if it exists
        if hasattr(self, 'map_controller'):
            try:
                del self.map_controller
                print("🗑️ Map controller cleaned up")
            except:
                pass

    def _clear_page_widgets(self):
        """Clear page widgets but preserve background"""
        for widget in self.widgets:
            widget.destroy()
        for widget in self.history_labels:
            widget.destroy()
        self.widgets.clear()
        self.history_labels.clear()

    def _build_main_page(self):
        """Build the main page with metrics, weather, and navigation buttons"""
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        bg_color = self._get_canvas_bg_color()
        
        # City input at top
        city_entry = tk.Entry(
            self.app,
            textvariable=self.app.city_var,
            font=("Arial", int(14 + window_width/80)),
            width=max(15, int(window_width/50)),
            justify="center",
            bg="white",
            fg="black",
            relief="solid",
            borderwidth=1
        )
        city_entry.place(x=window_width/2, y=30, anchor="center")
        city_entry.bind("<Return>", lambda e: self.app.fetch_and_display())
        self.widgets.append(city_entry)
        self.city_entry = city_entry
        
        # Weather metrics section
        self._build_weather_metrics_section(window_width, bg_color, y_start=70)
        
        # Main weather display
        self._build_main_weather_display(window_width, bg_color, y_start=170)
        
        # Navigation buttons
        self._build_navigation_buttons(window_width, bg_color, y_start=350)

    def _build_weather_metrics_section(self, window_width, bg_color, y_start):
        """Build weather metrics section"""
        available_width = window_width - 40
        col_width = available_width / 6
        start_x = 20
        
        # Headers
        metric_headers = ["Humidity", "Wind", "Press.", "Visibility", "UV Index", "Precip."]
        for i, header in enumerate(metric_headers):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            header_widget = tk.Label(
                self.app,
                text=header,
                font=("Arial", int(10 + window_width/100), "bold"),
                fg=self.app.text_color, 
                bg=bg_color,
                anchor="center",
                relief="flat",
                borderwidth=0
            )
            header_widget.place(x=x_pos, y=y_start, anchor="center")
            self.widgets.append(header_widget)
        
        # Emojis
        metric_emojis = ["💧", "🌬️", "🧭", "👁️", "☀️", "🌧️"]
        for i, emoji in enumerate(metric_emojis):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            emoji_widget = tk.Label(
                self.app,
                text=emoji,
                font=("Arial", int(16 + window_width/80)),
                bg=bg_color,
                anchor="center",
                relief="flat",
                borderwidth=0
            )
            emoji_widget.place(x=x_pos, y=y_start + 25, anchor="center")
            self.widgets.append(emoji_widget)
        
        # Values
        value_widgets = []
        for i in range(6):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            value_widget = tk.Label(
                self.app,
                text="--",
                font=("Arial", int(10 + window_width/120)),
                fg=self.app.text_color, 
                bg=bg_color,
                anchor="center",
                relief="flat",
                borderwidth=0
            )
            value_widget.place(x=x_pos, y=y_start + 50, anchor="center")
            self.widgets.append(value_widget)
            value_widgets.append(value_widget)
        
        # Set widget references
        widget_refs = {
            'humidity_value': value_widgets[0],
            'wind_value': value_widgets[1],
            'pressure_value': value_widgets[2],
            'visibility_value': value_widgets[3],
            'uv_value': value_widgets[4],
            'precipitation_value': value_widgets[5]
        }
        self.set_widget_references(widget_refs)

    def _build_main_weather_display(self, window_width, bg_color, y_start):
        """Build main weather display section - moved down by 2 rows"""
        # Add extra spacing to move everything down by 2 rows (about 60px)
        y_offset = 60
        
        # Weather icon
        icon_label = tk.Label(
            self.app,
            text="🌤️",
            font=("Arial", int(40 + window_width/25)),
            bg=bg_color,
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        icon_label.place(x=window_width/2, y=y_start + y_offset, anchor="center")
        self.widgets.append(icon_label)
        
        # Temperature
        temp_label = tk.Label(
            self.app,
            text="Loading...",
            font=("Arial", int(40 + window_width/25), "bold"),
            fg=self.app.text_color,
            bg=bg_color,
            cursor="hand2",
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        temp_label.place(x=window_width/2, y=y_start + 70 + y_offset, anchor="center")
        temp_label.bind("<Button-1>", lambda e: self.app.toggle_unit())
        self.widgets.append(temp_label)
        
        # Description
        desc_label = tk.Label(
            self.app,
            text="Fetching weather...",
            font=("Arial", int(16 + window_width/60)),
            fg=self.app.text_color,
            bg=bg_color,
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        desc_label.place(x=window_width/2, y=y_start + 130 + y_offset, anchor="center")
        self.widgets.append(desc_label)
        
        # Set widget references
        widget_refs = {
            'icon_label': icon_label,
            'temp_label': temp_label,
            'desc_label': desc_label
        }
        self.set_widget_references(widget_refs)

    def _build_navigation_buttons(self, window_width, bg_color, y_start):
        """Build navigation buttons for different pages with better spacing and black text"""
        button_width = 150
        button_height = 40
        button_spacing = 60  # Increased spacing between buttons
        
        # Calculate positions for 2x2 grid with more spacing
        center_x = window_width / 2
        left_x = center_x - button_width/2 - button_spacing/2
        right_x = center_x + button_width/2 + button_spacing/2
        
        # Move buttons down since weather display moved down
        y_start += 60  # Adjust for weather display offset
        
        buttons = [
            ("Toggle Theme", lambda: self.app.toggle_theme(), left_x, y_start),
            ("Tomorrow's Prediction", lambda: self.show_page("prediction"), right_x, y_start),
            ("Weather History", lambda: self.show_page("history"), left_x, y_start + button_height + 30),
            ("Map View", lambda: self.show_page("map"), right_x, y_start + button_height + 30)
        ]
        
        for text, command, x, y in buttons:
            btn = tk.Button(
                self.app,
                text=text,
                command=command,
                bg="grey",  # Grey background for all buttons
                fg="black",  # Black text on all buttons
                font=("Arial", int(10 + window_width/120), "bold"),
                relief="raised",
                borderwidth=2,
                width=15,
                height=2,
                activeforeground="black",  # Black text when button is pressed
                activebackground="lightgrey"  # Light grey background when pressed
            )
            btn.place(x=x, y=y, anchor="center")
            self.widgets.append(btn)
        
        # Store theme button reference
        self.theme_btn = buttons[0]

    def _build_prediction_page(self):
        """Build tomorrow's prediction page"""
        window_width = self.app.winfo_width()
        bg_color = self._get_canvas_bg_color()
        
        # Back button
        self._add_back_button()
        
        # Title
        title = tk.Label(
            self.app,
            text="Tomorrow's Weather Prediction",
            font=("Arial", int(24 + window_width/50), "bold"),
            fg=self.app.text_color,
            bg=bg_color,
            anchor="center"
        )
        title.place(x=window_width/2, y=100, anchor="center")
        self.widgets.append(title)
        
        # Prediction grid
        self._build_prediction_grid(window_width, bg_color, y_start=200)

    def _build_prediction_grid(self, window_width, bg_color, y_start):
        """Build prediction display grid"""
        available_width = window_width - 40
        col_width = available_width / 3
        start_x = 20
        
        # Headers
        prediction_headers = ["Temperature", "Accuracy", "Confidence"]
        for i, header in enumerate(prediction_headers):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            header_widget = tk.Label(
                self.app,
                text=header,
                font=("Arial", int(16 + window_width/80), "bold"),
                fg=self.app.text_color, 
                bg=bg_color,
                anchor="center"
            )
            header_widget.place(x=x_pos, y=y_start, anchor="center")
            self.widgets.append(header_widget)
        
        # Emojis
        prediction_emojis = ["🌡️", "💯", "😎"]
        for i, emoji in enumerate(prediction_emojis):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            emoji_widget = tk.Label(
                self.app,
                text=emoji,
                font=("Arial", int(24 + window_width/60)),
                bg=bg_color,
                anchor="center"
            )
            emoji_widget.place(x=x_pos, y=y_start + 40, anchor="center")
            self.widgets.append(emoji_widget)
        
        # Values
        prediction_widgets = []
        for i in range(3):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            prediction_widget = tk.Label(
                self.app,
                text="--",
                font=("Arial", int(20 + window_width/80), "bold"),
                fg=self.app.text_color, 
                bg=bg_color,
                anchor="center"
            )
            prediction_widget.place(x=x_pos, y=y_start + 80, anchor="center")
            self.widgets.append(prediction_widget)
            prediction_widgets.append(prediction_widget)
        
        # Set widget references
        widget_refs = {
            'temp_prediction': prediction_widgets[0],
            'accuracy_prediction': prediction_widgets[1],
            'confidence_prediction': prediction_widgets[2]
        }
        self.set_widget_references(widget_refs)

    def _build_history_page(self):
        """Build weather history page"""
        window_width = self.app.winfo_width()
        bg_color = self._get_canvas_bg_color()
        
        # Back button
        self._add_back_button()
        
        # Title
        title = tk.Label(
            self.app,
            text="Weather History",
            font=("Arial", int(24 + window_width/50), "bold"),
            fg=self.app.text_color,
            bg=bg_color,
            anchor="center"
        )
        title.place(x=window_width/2, y=100, anchor="center")
        self.widgets.append(title)
        
        # Force update history display when building history page
        city = self.app.city_var.get()
        print(f"[GUI] History page built, fetching history for '{city}'")
        # Use after to ensure the page is built first
        self.app.after(100, lambda: self.update_history_display(city))

    def _build_map_page(self):
        """Build map view page"""
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        bg_color = self._get_canvas_bg_color()
        
        # Back button
        self._add_back_button()
        
        # Title
        title = tk.Label(
            self.app,
            text="Weather Map",
            font=("Arial", int(24 + window_width/50), "bold"),
            fg=self.app.text_color,
            bg=bg_color,
            anchor="center"
        )
        title.place(x=window_width/2, y=100, anchor="center")
        self.widgets.append(title)
        
        # Info button next to title
        info_btn = tk.Button(
            self.app,
            text="i",
            command=self._show_map_info,
            bg="grey",
            fg="black",
            font=("Arial", int(16 + window_width/80), "bold"),
            relief="raised",
            borderwidth=2,
            width=3,
            height=1,
            activeforeground="black",
            activebackground="lightgrey"
        )
        info_btn.place(x=window_width/2 + 180, y=100, anchor="center")  # Moved 9 more spaces right
        self.widgets.append(info_btn)
        
        # Move map down 2 rows (approximately 80px) from the title
        map_y_position = window_height/2 + 40  # Moving down 2 rows from center
        
        # Create map frame container - positioned lower
        map_frame = tk.Frame(
            self.app,
            bg=bg_color,
            relief="solid",
            borderwidth=2
        )
        map_frame.place(x=window_width/2, y=map_y_position, anchor="center", width=600, height=400)
        self.widgets.append(map_frame)
        
        # Initialize map controller only for this page
        try:
            from features.interactive_map.controller import MapController
            import os
            api_key = os.getenv("weatherdb_api_key")
            
            # Create map controller with the frame as parent and grid visibility enabled
            self.map_controller = MapController(map_frame, self.app.city_var.get, api_key, show_grid=True)
            print("✅ Map controller initialized for map page with grid visibility")
        except Exception as e:
            print(f"❌ Map controller error: {e}")
            # Fallback to placeholder
            map_placeholder = tk.Label(
                map_frame,
                text="🗺️\nInteractive Map\n(Map temporarily unavailable)",
                font=("Arial", int(16 + window_width/80)),
                fg=self.app.text_color,
                bg=bg_color,
                anchor="center",
                justify="center"
            )
            map_placeholder.pack(expand=True, fill="both")

    def _show_map_info(self):
        """Show information about the currently selected map weather overlay"""
        from tkinter import messagebox
        
        # Get current overlay selection from map controller if available
        current_overlay = "none"
        if hasattr(self, 'map_controller') and hasattr(self.map_controller, 'layer_var'):
            current_overlay = self.map_controller.layer_var.get()
        
        # Define overlay information
        overlay_info = {
            "none": {
                "title": "Base Map View",
                "description": "📍 Standard OpenStreetMap view showing geographical features, roads, and city locations without weather overlays."
            },
            "temp_new": {
                "title": "🔵 TEMPERATURE Overlay",
                "description": """Shows current air temperature across the region:

• Blue: Cold temperatures (below 0°C/32°F)
• Green: Cool temperatures (0-15°C/32-59°F)
• Yellow: Mild temperatures (15-25°C/59-77°F)
• Orange: Warm temperatures (25-35°C/77-95°F)
• Red: Hot temperatures (above 35°C/95°F)

This overlay helps you see temperature variations across different areas and plan accordingly for weather-sensitive activities."""
            },
            "wind_new": {
                "title": "💨 WIND Overlay",
                "description": """Displays wind speed and direction patterns:

• Light Blue: Calm winds (0-10 km/h)
• Blue: Light winds (10-20 km/h)
• Green: Moderate winds (20-40 km/h)
• Yellow: Strong winds (40-60 km/h)
• Red: Very strong winds (60+ km/h)

Useful for outdoor activities, sailing, flying, and understanding weather movement patterns."""
            },
            "precipitation_new": {
                "title": "🌧️ PRECIPITATION Overlay",
                "description": """Shows current rainfall and snowfall intensity:

• Transparent: No precipitation
• Light Blue: Light rain/snow (0.1-1 mm/h)
• Blue: Moderate rain/snow (1-5 mm/h)
• Dark Blue: Heavy rain/snow (5-10 mm/h)
• Purple: Very heavy rain/snow (10+ mm/h)

Essential for planning outdoor events and understanding current weather conditions."""
            },
            "clouds_new": {
                "title": "☁️ CLOUDS Overlay",
                "description": """Displays cloud coverage percentage across the region:

• Clear: No clouds (0-10% coverage)
• Light Grey: Few clouds (10-25% coverage)
• Grey: Scattered clouds (25-50% coverage)
• Dark Grey: Broken clouds (50-75% coverage)
• Very Dark: Overcast (75-100% coverage)

Helps predict sunshine, photography conditions, and general weather patterns."""
            },
            "pressure_new": {
                "title": "🌡️ PRESSURE Overlay",
                "description": """Shows atmospheric pressure patterns:

• Blue: Low pressure (below 1000 hPa) - Often brings storms
• Green: Normal pressure (1000-1020 hPa) - Stable weather
• Yellow: High pressure (1020-1040 hPa) - Clear, calm weather
• Red: Very high pressure (above 1040 hPa) - Very stable conditions

Pressure patterns help predict weather changes and storm systems."""
            },
            "snow_new": {
                "title": "❄️ SNOW Overlay",
                "description": """Displays snow depth and accumulation:

• White: Light snow (0-5 cm depth)
• Light Blue: Moderate snow (5-15 cm depth)
• Blue: Heavy snow (15-30 cm depth)
• Dark Blue: Very heavy snow (30+ cm depth)

Critical for winter travel planning and snow-related activities."""
            },
            "dewpoint_new": {
                "title": "💧 DEW POINT Overlay",
                "description": """Shows humidity and comfort levels:

• Blue: Very dry (below 0°C/32°F) - Low humidity
• Green: Comfortable (0-15°C/32-59°F) - Ideal humidity
• Yellow: Slightly humid (15-20°C/59-68°F) - Noticeable humidity
• Orange: Humid (20-25°C/68-77°F) - High humidity
• Red: Very humid (above 25°C/77°F) - Uncomfortable humidity

Dew point indicates how the air will feel and potential for fog formation."""
            }
        }
        
        # Get info for current overlay
        if current_overlay in overlay_info:
            info = overlay_info[current_overlay]
            title = f"Map Info: {info['title']}"
            message = info['description']
        else:
            title = "Map Information"
            message = "No overlay information available for the current selection."
        
        messagebox.showinfo(title, message)

    def _add_back_button(self):
        """Add back button to return to main page"""
        back_btn = tk.Button(
            self.app,
            text="← Back",
            command=lambda: self.show_page("main"),
            bg="grey",  # Grey background for back button
            fg="black",  # Black text for back button
            font=("Arial", 12, "bold"),
            relief="raised",
            borderwidth=2,
            width=8,
            height=1,
            activeforeground="black",  # Black text when pressed
            activebackground="lightgrey"  # Light grey when pressed
        )
        back_btn.place(x=50, y=50, anchor="center")
        self.widgets.append(back_btn)

    def _get_canvas_bg_color(self):
        """Get the current canvas background color"""
        try:
            if self.bg_canvas:
                return self.bg_canvas.cget("bg")
            return "#87CEEB"
        except:
            return "#87CEEB"

    def _on_window_resize(self, event):
        """Handle window resize events"""
        if event.widget == self.app:
            self.app.after_idle(self._rebuild_current_page)

    def _rebuild_current_page(self):
        """Rebuild current page when window is resized"""
        try:
            print(f"[GUI] Rebuilding page for resize: {self.current_page}")
            current_page = self.current_page
            self.show_page(current_page)
            self._restore_current_data()
        except Exception as e:
            print(f"❌ Resize error: {e}")

    def _restore_current_data(self):
        """Restore current data after page rebuild"""
        if self.app.current_weather_data:
            self.weather_display.update_weather_display(self.app.current_weather_data)
        
        if self.app.current_prediction_data:
            predicted_temp, confidence, accuracy = self.app.current_prediction_data
            self.weather_display.update_tomorrow_prediction_direct(
                predicted_temp, confidence, accuracy
            )

    # Public interface methods for weather updates
    def update_weather_display(self, weather_data):
        """Update weather display - delegates to weather_display component"""
        self.weather_display.update_weather_display(weather_data)

    def update_tomorrow_prediction_direct(self, predicted_temp, confidence, accuracy):
        """Update prediction display - delegates to weather_display component"""
        self.weather_display.update_tomorrow_prediction_direct(
            predicted_temp, confidence, accuracy
        )

    def update_history_display(self, city):
        """Update history display - delegates to weather_display component"""
        self.weather_display.update_history_display(city)

    def update_background_animation(self, weather_data):
        """Update background animation - delegates to animation_controller"""
        self.animation_controller.update_background_animation(weather_data)

    def toggle_theme(self):
        """Toggle theme - delegates to weather_display component"""
        self.weather_display.toggle_theme()

    def cleanup_animation(self):
        """Clean up animation resources"""
        self.animation_controller.cleanup_animation()

    def get_widgets(self):
        """Get the widgets list"""
        return self.widgets

    def get_history_labels(self):
        """Get the history labels list"""
        return self.history_labels

    def set_widget_references(self, widget_refs):
        """Set widget references from layout manager"""
        for attr_name, widget in widget_refs.items():
            setattr(self, attr_name, widget)