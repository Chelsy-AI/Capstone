import tkinter as tk


class LayoutManager:
    """
    Layout Manager
    
    Handles responsive layout creation and widget positioning
    for the weather application GUI.
    """
    
    def __init__(self, app, gui_controller):
        self.app = app
        self.gui = gui_controller
        
        # Layout constants
        self.METRICS_COUNT = 6
        self.PREDICTION_COUNT = 3
        self.LEFT_MARGIN = 20
        self.RIGHT_MARGIN = 20
        
        # Responsive font size calculation
        self.base_font_size = 10

    def build_responsive_layout(self):
        """Build the complete responsive layout"""
        print("[Layout] Building responsive layout...")
        
        # Get current window dimensions
        self.app.update_idletasks()
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        # Calculate responsive values
        available_width = window_width - (self.LEFT_MARGIN + self.RIGHT_MARGIN)
        
        # Build layout sections
        self._build_weather_metrics_section(window_width, available_width)
        self._build_controls_section(window_width)
        self._build_weather_display_section(window_width)
        self._build_prediction_section(window_width, available_width)
        self._build_history_section(window_width)
        
        print("[Layout] Responsive layout complete")

    def _get_canvas_bg_color(self):
        """Get the current canvas background color"""
        try:
            if self.gui.bg_canvas:
                return self.gui.bg_canvas.cget("bg")
            return "#87CEEB"  # Default fallback
        except:
            return "#87CEEB"  # Safe fallback

    def _get_dynamic_bg(self):
        """Get dynamic background color based on current animation"""
        # This will be updated by the animation controller
        return getattr(self.app, 'current_bg_color', self._get_canvas_bg_color())

    def _build_weather_metrics_section(self, window_width, available_width):
        """Build the weather metrics section (humidity, wind, etc.)"""
        # Calculate positioning
        col_width = available_width / self.METRICS_COUNT
        start_x = self.LEFT_MARGIN
        scroll_offset = self.gui.scroll_handler.get_scroll_offset()
        bg_color = self._get_canvas_bg_color()
        
        # Headers with canvas background color
        metric_headers = ["Humidity", "Wind", "Press.", "Visibility", "UV Index", "Precip."]
        for i, header in enumerate(metric_headers):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            header_widget = tk.Label(
                self.app,  # Place on main app for proper event handling
                text=header,
                font=("Arial", int(self.base_font_size + window_width/100), "bold"),
                fg=self.app.text_color, 
                bg=bg_color,  # Use canvas background color
                anchor="center",
                relief="flat",  # Flat relief for seamless look
                borderwidth=0
            )
            header_widget.place(x=x_pos, y=30 - scroll_offset, anchor="center")
            self.gui.widgets.append(header_widget)
        
        # Emojis with canvas background color
        metric_emojis = ["💧", "🌬️", "🧭", "👁️", "☀️", "🌧️"]
        for i, emoji in enumerate(metric_emojis):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            emoji_widget = tk.Label(
                self.app,  # Place on main app for proper event handling
                text=emoji,
                font=("Arial", int(16 + window_width/80)),
                bg=bg_color,  # Use canvas background color
                anchor="center",
                relief="flat",
                borderwidth=0
            )
            emoji_widget.place(x=x_pos, y=55 - scroll_offset, anchor="center")
            self.gui.widgets.append(emoji_widget)
        
        # Value widgets
        value_widgets = self._create_metric_value_widgets(
            window_width, col_width, start_x, scroll_offset, bg_color
        )
        
        # Set widget references
        widget_refs = {
            'humidity_value': value_widgets[0],
            'wind_value': value_widgets[1],
            'pressure_value': value_widgets[2],
            'visibility_value': value_widgets[3],
            'uv_value': value_widgets[4],
            'precipitation_value': value_widgets[5]
        }
        self.gui.set_widget_references(widget_refs)

    def _create_metric_value_widgets(self, window_width, col_width, start_x, scroll_offset, bg_color):
        """Create metric value widgets with canvas background color"""
        value_widgets = []
        
        for i in range(self.METRICS_COUNT):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            value_widget = tk.Label(
                self.app,  # Place on main app for proper event handling
                text="--",
                font=("Arial", int(self.base_font_size + window_width/120)),
                fg=self.app.text_color, 
                bg=bg_color,  # Use canvas background color
                anchor="center",
                relief="flat",
                borderwidth=0
            )
            value_widget.place(x=x_pos, y=80 - scroll_offset, anchor="center")
            self.gui.widgets.append(value_widget)
            value_widgets.append(value_widget)
        
        return value_widgets

    def _build_controls_section(self, window_width):
        """Build the controls section (theme button, city input)"""
        scroll_offset = self.gui.scroll_handler.get_scroll_offset()
        
        # Theme button - keep solid background for buttons
        theme_btn = tk.Button(
            self.app,
            text="Toggle Theme",
            command=self.app.toggle_theme,
            bg="darkblue",
            fg="white",
            font=("Arial", int(self.base_font_size + window_width/120), "bold"),
            relief="raised",
            borderwidth=2
        )
        theme_btn.place(x=window_width/2, y=120 - scroll_offset, anchor="center")
        self.gui.widgets.append(theme_btn)
        
        # City input - keep solid background for input
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
        city_entry.place(x=window_width/2, y=160 - scroll_offset, anchor="center")
        city_entry.bind("<Return>", lambda e: self.app.fetch_and_display())
        self.gui.widgets.append(city_entry)
        
        # Set widget references
        widget_refs = {
            'theme_btn': theme_btn,
            'city_entry': city_entry
        }
        self.gui.set_widget_references(widget_refs)

    def _build_weather_display_section(self, window_width):
        """Build the main weather display section"""
        scroll_offset = self.gui.scroll_handler.get_scroll_offset()
        bg_color = self._get_canvas_bg_color()
        
        # Weather icon - canvas background color
        icon_label = tk.Label(
            self.app,  # Place on main app for proper event handling
            text="🌤️",
            font=("Arial", int(40 + window_width/25)),
            bg=bg_color,  # Use canvas background color
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        icon_label.place(x=window_width/2, y=220 - scroll_offset, anchor="center")
        self.gui.widgets.append(icon_label)
        
        # Temperature - canvas background color
        temp_label = tk.Label(
            self.app,  # Place on main app for proper event handling
            text="Loading...",
            font=("Arial", int(40 + window_width/25), "bold"),
            fg=self.app.text_color,
            bg=bg_color,  # Use canvas background color
            cursor="hand2",
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        temp_label.place(x=window_width/2, y=290 - scroll_offset, anchor="center")
        temp_label.bind("<Button-1>", lambda e: self.app.toggle_unit())
        self.gui.widgets.append(temp_label)
        
        # Description - canvas background color
        desc_label = tk.Label(
            self.app,  # Place on main app for proper event handling
            text="Fetching weather...",
            font=("Arial", int(16 + window_width/60)),
            fg=self.app.text_color,
            bg=bg_color,  # Use canvas background color
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        desc_label.place(x=window_width/2, y=350 - scroll_offset, anchor="center")
        self.gui.widgets.append(desc_label)
        
        # Set widget references
        widget_refs = {
            'icon_label': icon_label,
            'temp_label': temp_label,
            'desc_label': desc_label
        }
        self.gui.set_widget_references(widget_refs)

    def _build_prediction_section(self, window_width, available_width):
        """Build the tomorrow's prediction section"""
        scroll_offset = self.gui.scroll_handler.get_scroll_offset()
        bg_color = self._get_canvas_bg_color()
        
        # Prediction title - canvas background color
        prediction_title = tk.Label(
            self.app,  # Place on main app for proper event handling
            text="Tomorrow's Prediction",
            font=("Arial", int(18 + window_width/60), "bold"),
            fg=self.app.text_color, 
            bg=bg_color,  # Use canvas background color
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        prediction_title.place(x=window_width/2, y=410 - scroll_offset, anchor="center")
        self.gui.widgets.append(prediction_title)
        
        # Prediction layout
        pred_col_width = available_width / self.PREDICTION_COUNT
        pred_start_x = self.LEFT_MARGIN
        
        # Headers - canvas background color
        prediction_headers = ["Temperature", "Accuracy", "Confidence"]
        for i, header in enumerate(prediction_headers):
            x_pos = pred_start_x + (i * pred_col_width) + (pred_col_width / 2)
            header_widget = tk.Label(
                self.app,  # Place on main app for proper event handling
                text=header,
                font=("Arial", int(self.base_font_size + window_width/100), "bold"),
                fg=self.app.text_color, 
                bg=bg_color,  # Use canvas background color
                anchor="center",
                relief="flat",
                borderwidth=0
            )
            header_widget.place(x=x_pos, y=440 - scroll_offset, anchor="center")
            self.gui.widgets.append(header_widget)
        
        # Emojis - canvas background color
        prediction_emojis = ["🌡️", "💯", "😎"]
        for i, emoji in enumerate(prediction_emojis):
            x_pos = pred_start_x + (i * pred_col_width) + (pred_col_width / 2)
            emoji_widget = tk.Label(
                self.app,  # Place on main app for proper event handling
                text=emoji,
                font=("Arial", int(16 + window_width/80)),
                bg=bg_color,  # Use canvas background color
                anchor="center",
                relief="flat",
                borderwidth=0
            )
            emoji_widget.place(x=x_pos, y=465 - scroll_offset, anchor="center")
            self.gui.widgets.append(emoji_widget)
        
        # Prediction values
        prediction_widgets = self._create_prediction_value_widgets(
            window_width, pred_col_width, pred_start_x, scroll_offset, bg_color
        )
        
        # Set widget references
        widget_refs = {
            'temp_prediction': prediction_widgets[0],
            'accuracy_prediction': prediction_widgets[1],
            'confidence_prediction': prediction_widgets[2]
        }
        self.gui.set_widget_references(widget_refs)

    def _create_prediction_value_widgets(self, window_width, col_width, start_x, scroll_offset, bg_color):
        """Create prediction value widgets with canvas background color"""
        prediction_widgets = []
        
        for i in range(self.PREDICTION_COUNT):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            prediction_widget = tk.Label(
                self.app,  # Place on main app for proper event handling
                text="--",
                font=("Arial", int(self.base_font_size + window_width/120)),
                fg=self.app.text_color, 
                bg=bg_color,  # Use canvas background color
                anchor="center",
                relief="flat",
                borderwidth=0
            )
            prediction_widget.place(x=x_pos, y=490 - scroll_offset, anchor="center")
            self.gui.widgets.append(prediction_widget)
            prediction_widgets.append(prediction_widget)
        
        return prediction_widgets

    def _build_history_section(self, window_width):
        """Build the history section header"""
        scroll_offset = self.gui.scroll_handler.get_scroll_offset()
        bg_color = self._get_canvas_bg_color()
        
        # History title - canvas background color
        history_title = tk.Label(
            self.app,  # Place on main app for proper event handling
            text="7-Day History",
            font=("Arial", int(18 + window_width/60), "bold"),
            fg=self.app.text_color, 
            bg=bg_color,  # Use canvas background color
            anchor="center",
            relief="flat",
            borderwidth=0
        )
        history_title.place(x=window_width/2, y=550 - scroll_offset, anchor="center")
        self.gui.widgets.append(history_title)

    def get_responsive_font_size(self, base_size, window_width, scale_factor=100):
        """Calculate responsive font size based on window width"""
        return int(base_size + window_width / scale_factor)

    def calculate_column_positions(self, window_width, column_count, margin=20):
        """Calculate column positions for responsive layout"""
        available_width = window_width - (margin * 2)
        col_width = available_width / column_count
        start_x = margin
        
        positions = []
        for i in range(column_count):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            positions.append(x_pos)
        
        return positions, col_width
    