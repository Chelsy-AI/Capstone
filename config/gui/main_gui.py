import tkinter as tk
from tkinter import ttk

from .weather_display import WeatherDisplay
from .animation_controller import AnimationController
from features.sun_moon_phases.controller import SunMoonController
from features.graphs.controller import GraphsController
from features.weather_quiz.controller import WeatherQuizController


class WeatherGUI:
    """
    Main GUI Controller with Transparent Label Fix and Sun/Moon Integration
    """
    
    def __init__(self, parent_app):
        """Initialize GUI with reference to parent application"""
        self.app = parent_app
        
        # Initialize GUI components
        self.weather_display = WeatherDisplay(self.app, self)
        self.animation_controller = AnimationController(self.app, self)
        self.sun_moon_controller = SunMoonController(self.app, self)
        self.weather_quiz_controller = WeatherQuizController(self.app, self)
        
        # Page management
        self.current_page = "main"
        self.pages = {}
        
        # GUI state tracking
        self.widgets = []
        self.history_labels = []
        
        # Background elements
        self.bg_canvas = None
        
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
        
        self._clear_widgets()
        self.app.bind("<Configure>", self._on_window_resize)
        self._setup_background()
        self.show_page("main")
        
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
        
        self._cleanup_page_resources()
        self._clear_page_widgets()
        self.current_page = page_name
        
        if page_name == "main":
            self._build_main_page()
        elif page_name == "prediction":
            self._build_prediction_page()
        elif page_name == "history":
            self._build_history_page()
        elif page_name == "map":
            self._build_map_page()
        elif page_name == "sun_moon":
            self._build_sun_moon_page()
        elif page_name == "graphs":
            self._build_graphs_page()
        elif page_name == "quiz":
            self._build_quiz_page()
        
        self._restore_current_data()

    def _cleanup_page_resources(self):
        """Clean up page-specific resources like map controllers"""
        if hasattr(self, 'map_controller'):
            try:
                del self.map_controller
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

    def _create_label(self, parent, text, font, fg, x, y, anchor="center", **kwargs):
        """Helper method to create truly transparent labels - NO BLUE BOXES!"""
        
        # Get the actual canvas background color
        canvas_bg = "#87CEEB"  # Default sky blue
        if self.bg_canvas:
            try:
                canvas_bg = self.bg_canvas.cget("bg")
            except:
                canvas_bg = "#87CEEB"
        
        label = tk.Label(
            parent,
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

    def _build_main_page(self):
        """Build the main page with transparent labels"""
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
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
            borderwidth=1,
            highlightthickness=0
        )
        city_entry.place(x=window_width/2, y=30, anchor="center")
        city_entry.bind("<Return>", lambda e: self.app.fetch_and_display())
        self.widgets.append(city_entry)
        self.city_entry = city_entry
        
        # Weather metrics section
        self._build_weather_metrics_section(window_width, y_start=70)
        
        # Main weather display
        self._build_main_weather_display(window_width, y_start=170)
        
        # Navigation buttons
        self._build_navigation_buttons(window_width, y_start=350)

    def _build_weather_metrics_section(self, window_width, y_start):
        """Build weather metrics section with transparent labels"""
        available_width = window_width - 40
        col_width = available_width / 6
        start_x = 20
        
        # Headers - TRANSPARENT backgrounds
        metric_headers = ["Humidity", "Wind", "Press.", "Visibility", "UV Index", "Precip."]
        for i, header in enumerate(metric_headers):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            header_widget = self._create_label(
                self.app,
                text=header,
                font=("Arial", int(10 + window_width/100), "bold"),
                fg=self.app.text_color,
                x=x_pos,
                y=y_start
            )
            self.widgets.append(header_widget)
        
        # Emojis - TRANSPARENT backgrounds
        metric_emojis = ["💧", "🌬️", "🧭", "👁️", "☀️", "🌧️"]
        for i, emoji in enumerate(metric_emojis):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            emoji_widget = self._create_label(
                self.app,
                text=emoji,
                font=("Arial", int(16 + window_width/80)),
                fg=self.app.text_color,
                x=x_pos,
                y=y_start + 25
            )
            self.widgets.append(emoji_widget)
        
        # Values - TRANSPARENT backgrounds
        value_widgets = []
        for i in range(6):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            value_widget = self._create_label(
                self.app,
                text="--",
                font=("Arial", int(10 + window_width/120)),
                fg=self.app.text_color,
                x=x_pos,
                y=y_start + 50
            )
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

    def _build_main_weather_display(self, window_width, y_start):
        """Build main weather display with transparent labels"""
        y_offset = 60
        
        # Weather icon - TRANSPARENT background
        icon_label = self._create_label(
            self.app,
            text="🌤️",
            font=("Arial", int(40 + window_width/25)),
            fg=self.app.text_color,
            x=window_width/2,
            y=y_start + y_offset
        )
        self.widgets.append(icon_label)
        
        # Temperature (clickable) - MATCH CANVAS BACKGROUND
        canvas_bg = "#87CEEB"  # Default
        if self.bg_canvas:
            try:
                canvas_bg = self.bg_canvas.cget("bg")
            except:
                canvas_bg = "#87CEEB"
        
        temp_label = tk.Label(
            self.app,
            text="Loading...",
            font=("Arial", int(40 + window_width/25), "bold"),
            fg=self.app.text_color,
            bg=canvas_bg,  # Match canvas background!
            cursor="hand2",
            anchor="center",
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        temp_label.place(x=window_width/2, y=y_start + 70 + y_offset, anchor="center")
        temp_label.bind("<Button-1>", lambda e: [self.app.toggle_unit(), self.app.focus_set()])
        temp_label.bind("<FocusIn>", lambda e: self.app.focus_set())
        self.widgets.append(temp_label)
        
        # Description - TRANSPARENT background
        desc_label = self._create_label(
            self.app,
            text="Fetching weather...",
            font=("Arial", int(16 + window_width/60)),
            fg=self.app.text_color,
            x=window_width/2,
            y=y_start + 130 + y_offset
        )
        self.widgets.append(desc_label)
        
        # Set widget references
        widget_refs = {
            'icon_label': icon_label,
            'temp_label': temp_label,
            'desc_label': desc_label
        }
        self.set_widget_references(widget_refs)

    def _build_navigation_buttons(self, window_width, y_start):
        """Build navigation buttons including Weather Quiz"""
        button_width = 150
        button_height = 40
        button_spacing = 60
        
        center_x = window_width / 2
        left_x = center_x - button_width/2 - button_spacing/2
        right_x = center_x + button_width/2 + button_spacing/2
        
        y_start += 60
        
        buttons = [
            ("Toggle Theme", lambda: self.app.toggle_theme(), left_x, y_start),
            ("Tomorrow's Prediction", lambda: self.show_page("prediction"), right_x, y_start),
            ("Weather History", lambda: self.show_page("history"), left_x, y_start + button_height + 30),
            ("Weather Quiz", lambda: self.show_page("quiz"), right_x, y_start + button_height + 30),
            ("Weather Graphs", lambda: self.show_page("graphs"), left_x, y_start + (button_height + 30) * 2),
            ("Map View", lambda: self.show_page("map"), right_x, y_start + (button_height + 30) * 2),
            ("Sun & Moon", lambda: self.show_page("sun_moon"), left_x, y_start + (button_height + 30) * 3)
        ]
        
        for text, command, x, y in buttons:
            btn = tk.Button(
                self.app,
                text=text,
                command=command,
                bg="grey",
                fg="black",
                font=("Arial", int(10 + window_width/120), "bold"),
                relief="raised",
                borderwidth=2,
                width=15,
                height=2,
                activeforeground="black",
                activebackground="lightgrey",
                highlightthickness=0
            )
            btn.place(x=x, y=y, anchor="center")
            self.widgets.append(btn)
        
        self.theme_btn = buttons[0]

    def _build_prediction_page(self):
        """Build tomorrow's prediction page with transparent labels"""
        window_width = self.app.winfo_width()
        
        # Back button
        self._add_back_button()
        
        # Title - TRANSPARENT
        title = self._create_label(
            self.app,
            text="Tomorrow's Weather Prediction",
            font=("Arial", int(24 + window_width/50), "bold"),
            fg=self.app.text_color,
            x=window_width/2,
            y=100
        )
        self.widgets.append(title)
        
        # Prediction grid
        self._build_prediction_grid(window_width, y_start=200)

    def _build_prediction_grid(self, window_width, y_start):
        """Build prediction display grid with transparent labels"""
        available_width = window_width - 40
        col_width = available_width / 3
        start_x = 20
        
        # Headers - TRANSPARENT
        prediction_headers = ["Temperature", "Accuracy", "Confidence"]
        for i, header in enumerate(prediction_headers):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            header_widget = self._create_label(
                self.app,
                text=header,
                font=("Arial", int(16 + window_width/80), "bold"),
                fg=self.app.text_color,
                x=x_pos,
                y=y_start
            )
            self.widgets.append(header_widget)
        
        # Emojis - TRANSPARENT
        prediction_emojis = ["🌡️", "🎯", "😎"]
        for i, emoji in enumerate(prediction_emojis):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            emoji_widget = self._create_label(
                self.app,
                text=emoji,
                font=("Arial", int(24 + window_width/60)),
                fg=self.app.text_color,
                x=x_pos,
                y=y_start + 40
            )
            self.widgets.append(emoji_widget)
        
        # Values - TRANSPARENT
        prediction_widgets = []
        for i in range(3):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            prediction_widget = self._create_label(
                self.app,
                text="--",
                font=("Arial", int(20 + window_width/80), "bold"),
                fg=self.app.text_color,
                x=x_pos,
                y=y_start + 80
            )
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
        """Build weather history page with transparent labels"""
        window_width = self.app.winfo_width()
        
        # Back button
        self._add_back_button()
        
        # Title - TRANSPARENT
        title = self._create_label(
            self.app,
            text="Weather History",
            font=("Arial", int(24 + window_width/50), "bold"),
            fg=self.app.text_color,
            x=window_width/2,
            y=100
        )
        self.widgets.append(title)
        
        # Force update history display when building history page
        city = self.app.city_var.get()
        self.app.after(100, lambda: self.update_history_display(city))

    def _build_map_page(self):
        """Build map view page"""
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        # Back button
        self._add_back_button()
        
        # Title - TRANSPARENT
        title = self._create_label(
            self.app,
            text="Weather Map",
            font=("Arial", int(24 + window_width/50), "bold"),
            fg=self.app.text_color,
            x=window_width/2,
            y=100
        )
        self.widgets.append(title)
        
        # Info button
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
            activebackground="lightgrey",
            highlightthickness=0
        )
        info_btn.place(x=window_width/2 + 180, y=100, anchor="center")
        self.widgets.append(info_btn)
        
        # Map frame
        map_y_position = window_height/2 + 40
        
        # Get canvas background for map frame
        canvas_bg = "#87CEEB"
        if self.bg_canvas:
            try:
                canvas_bg = self.bg_canvas.cget("bg")
            except:
                canvas_bg = "#87CEEB"
        
        map_frame = tk.Frame(
            self.app,
            bg=canvas_bg,  # Match canvas background
            relief="solid",
            borderwidth=2,
            highlightthickness=0
        )
        map_frame.place(x=window_width/2, y=map_y_position, anchor="center", width=600, height=400)
        self.widgets.append(map_frame)
        
        # Initialize map controller
        try:
            from features.interactive_map.controller import MapController
            import os
            api_key = os.getenv("weatherdb_api_key")
            
            self.map_controller = MapController(map_frame, self.app.city_var.get, api_key, show_grid=True)
        except Exception as e:
            # Fallback placeholder - TRANSPARENT
            map_placeholder = self._create_label(
                map_frame,
                text="🗺️\nInteractive Map\n(Map temporarily unavailable)",
                font=("Arial", int(16 + window_width/80)),
                fg=self.app.text_color,
                x=300,
                y=200
            )

    def _build_sun_moon_page(self):
        """Build sun/moon phases page"""
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        
        # Use the controller to build the page
        self.sun_moon_controller.build_page(window_width, window_height)
        
        # Update display with current city
        city = self.app.city_var.get().strip() or "New York"
        self.sun_moon_controller.update_display(city)

    def _build_graphs_page(self):
        """Build graphs page with controller"""
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        # Initialize graphs controller if not exists
        if not hasattr(self, 'graphs_controller'):
            self.graphs_controller = GraphsController(self.app, self)
        
        # Build the graphs page
        self.graphs_controller.build_page(window_width, window_height)

    def _build_quiz_page(self):
        """Build weather quiz page"""
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        # Build the quiz page
        self.weather_quiz_controller.build_page(window_width, window_height)

    def _show_map_info(self):
        """Show map overlay information"""
        from tkinter import messagebox
        messagebox.showinfo("Map Info", "Weather overlay information would go here.")

    def _add_back_button(self):
        """Add back button to return to main page"""
        back_btn = tk.Button(
            self.app,
            text="← Back",
            command=lambda: self.show_page("main"),
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
        self.widgets.append(back_btn)

    def _on_window_resize(self, event):
        """Handle window resize events"""
        if event.widget == self.app:
            self.app.after_idle(self._rebuild_current_page)

    def _rebuild_current_page(self):
        """Rebuild current page when window is resized"""
        try:
            current_page = self.current_page
            self.show_page(current_page)
            self._restore_current_data()
        except Exception as e:
            pass

    def _restore_current_data(self):
        """Restore current data after page rebuild"""
        if self.app.current_weather_data:
            self.weather_display.update_weather_display(self.app.current_weather_data)
        
        if self.app.current_prediction_data:
            predicted_temp, confidence, accuracy = self.app.current_prediction_data
            self.weather_display.update_tomorrow_prediction_direct(
                predicted_temp, confidence, accuracy
            )

    # Public interface methods
    def update_weather_display(self, weather_data):
        """Update weather display"""
        self.weather_display.update_weather_display(weather_data)

    def update_tomorrow_prediction_direct(self, predicted_temp, confidence, accuracy):
        """Update prediction display"""
        self.weather_display.update_tomorrow_prediction_direct(
            predicted_temp, confidence, accuracy
        )

    def update_history_display(self, city):
        """Update history display"""
        self.weather_display.update_history_display(city)

    def update_background_animation(self, weather_data):
        """Update background animation"""
        self.animation_controller.update_background_animation(weather_data)

    def update_sun_moon_display(self, city):
        """Update sun/moon display"""
        if hasattr(self, 'sun_moon_controller'):
            self.sun_moon_controller.update_display(city)

    def toggle_theme(self):
        """Toggle theme"""
        self.weather_display.toggle_theme()

    def cleanup_animation(self):
        """Clean up animation resources"""
        self.animation_controller.cleanup_animation()
        
        # Clean up sun/moon controller
        if hasattr(self, 'sun_moon_controller'):
            self.sun_moon_controller.cleanup()
        
        # Clean up graphs controller
        if hasattr(self, 'graphs_controller'):
            self.graphs_controller.cleanup()
        
        # Clean up quiz controller
        if hasattr(self, 'weather_quiz_controller'):
            self.weather_quiz_controller.cleanup()

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