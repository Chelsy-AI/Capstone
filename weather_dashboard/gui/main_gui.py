"""
Main GUI Controller
===========================================

This is the "director" of the user interface with comprehensive translation support.
It manages all the visual elements you see on screen like buttons, labels, and different pages.

Key responsibilities:
- Creating and positioning buttons, labels, and input fields
- Switching between different pages (main weather, history, predictions, etc.)
- Making sure text labels have transparent backgrounds (no ugly blue boxes!)
- Coordinating with other controllers for specialized features
- Supporting full multi-language translation for ALL UI text consistently
- Proper widget cleanup and reference management
"""

import tkinter as tk
from tkinter import ttk

from weather_dashboard.gui.weather_display import WeatherDisplay
from weather_dashboard.gui.animation_controller import AnimationController
from weather_dashboard.features.sun_moon_phases.controller import SunMoonController
from weather_dashboard.features.graphs.controller import GraphsController
from weather_dashboard.features.weather_quiz.controller import WeatherQuizController
from weather_dashboard.language.controller import LanguageController
from weather_dashboard.features.city_comparison.controller import CityComparisonController



class WeatherGUI:
    """
    Main GUI Controller Class with Comprehensive Translation Support
    
    This class manages the entire user interface of the weather app.
    It creates different pages, handles page switching, and coordinates
    with specialized controllers for features like animations and sun/moon data.
    All text elements are properly translated and consistently updated.
    """
    
    def __init__(self, parent_app):
        """
        Initialize the GUI controller.
        
        Args:
            parent_app: The main WeatherApp instance that owns this GUI
        """
        # Store reference to the main app
        self.app = parent_app
        
        # Initialize specialized controllers for different features
        self.weather_display = WeatherDisplay(self.app, self)
        self.animation_controller = AnimationController(self.app, self)
        self.sun_moon_controller = SunMoonController(self.app, self)
        self.weather_quiz_controller = WeatherQuizController(self.app, self)
        self.language_controller = LanguageController(self.app, self)
        self.city_comparison_controller = CityComparisonController(self.app, self)

        # Page management - keep track of what page we're currently showing
        self.current_page = "main"  # Start on the main weather page
        self.pages = {}  # Dictionary to store page-specific data
        
        # GUI state tracking - keep lists of widgets for easy management
        self.widgets = []         # All widgets on the current page
        self.history_labels = []  # Widgets specifically for the history page
        
        # Background elements
        self.bg_canvas = None  # The animated background canvas
        
        # References to main weather display widgets
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
        
        # Prediction display widgets
        self.temp_prediction = None
        self.accuracy_prediction = None
        self.confidence_prediction = None
        
        self.main_frame = None

    def build_gui(self):
        """
        Build the complete GUI interface.
        
        This is the main function that creates the entire user interface.
        It sets up the background, creates the animated canvas, and shows
        the main weather page.
        """
        # Clear any existing widgets first
        self._clear_widgets()
        
        # Set up window resize handling
        self.app.bind("<Configure>", self._on_window_resize)
        
        # Set up the animated background
        self._setup_background()
        
        # Show the main weather page
        self.show_page("main")
        
    def _clear_widgets(self):
        """
        Clear existing widgets while preserving special elements.
        
        This removes all widgets from the window except for special ones
        like the background canvas that should persist between page changes.
        """
        # Go through all child widgets in the main window
        for widget in self.app.winfo_children():
            # Only destroy widgets that aren't marked as "preserve"
            if (not hasattr(widget, '_preserve') and 
                widget != self.bg_canvas):
                widget.destroy()
        
        # Clear our widget tracking lists
        self.widgets.clear()
        self.pages.clear()

    def _setup_background(self):
        """
        Set up the animated background canvas.
        
        This creates the canvas where weather animations (rain, snow, etc.)
        will be displayed. The canvas sits behind all other widgets.
        """
        # Only create the canvas if it doesn't exist yet
        if not self.bg_canvas:
            # Create a canvas that fills the entire window
            self.bg_canvas = tk.Canvas(
                self.app, 
                highlightthickness=0,  # No border
                bg="#87CEEB"          # Sky blue default color
            )
            # Position it to fill the entire window
            self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Mark it as "preserve" so it doesn't get deleted during page switches
            self.bg_canvas._preserve = True
            
            # Initialize the animation system
            self.animation_controller.setup_animation(self.bg_canvas)

    def show_page(self, page_name):
        """
        Switch to a different page in the app with proper cleanup.
        
        This is like changing channels on TV - it hides the current page
        and shows a different one based on what the user requested.
        All translations are properly handled during page switches.
        
        Args:
            page_name (str): Name of the page to show ("main", "history", etc.)
        """
        # Clean up language widgets specifically before switching
        if hasattr(self, 'language_controller'):
            try:
                self.language_controller._clear_widgets()
            except:
                pass
        
        # Clean up any resources from the current page
        self._cleanup_page_resources()
        
        # Remove all widgets from the current page
        self._clear_page_widgets()
        
        # Remember what page we're now showing
        self.current_page = page_name
        
        # Build the requested page with proper translations
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
        elif page_name == "language":
            self._build_language_page()
        elif page_name == "comparison":
            self._build_comparison_page()
        
        # Restore any data that should be shown on the new page
        self._restore_current_data()

    def _cleanup_page_resources(self):
        """Clean up page-specific resources like map controllers and language widgets."""
        # Clean up map controller if it exists
        if hasattr(self, 'map_controller'):
            try:
                del self.map_controller
            except:
                pass
        
        # Clean up language controller widgets when switching pages
        if hasattr(self, 'language_controller'):
            try:
                self.language_controller._clear_widgets()
            except:
                pass

        # Clean up city comparison controller when switching pages
        if hasattr(self, 'city_comparison_controller'):
            try:
                self.city_comparison_controller.cleanup()
            except:
                pass

    def _clear_page_widgets(self):
        """Clear page widgets but preserve the background."""
        # Clean up language widgets first
        if hasattr(self, 'language_controller'):
            try:
                self.language_controller._clear_widgets()
            except:
                pass
        
        # Destroy all widgets we've been tracking
        for widget in self.widgets:
            try:
                widget.destroy()
            except:
                pass
        for widget in self.history_labels:
            try:
                widget.destroy()
            except:
                pass
        
        # Clear the tracking lists
        self.widgets.clear()
        self.history_labels.clear()

    def _create_label(self, parent, text, font, fg, x, y, anchor="center", **kwargs):
        """
        Create a label with transparent background - NO BLUE BOXES!
        
        This is a helper function that creates text labels that blend
        seamlessly with the animated background. The key is setting
        the background color to match the canvas.
        
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
        if self.bg_canvas:
            try:
                canvas_bg = self.bg_canvas.cget("bg")
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

    def _build_main_page(self):
        """
        Build the main weather page with translated text.
        
        This creates the primary interface with:
        - City search input
        - Current weather display
        - Weather metrics (humidity, wind, etc.)
        - Navigation buttons to other pages
        """
        # Get current window size for responsive design
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        # Create city input field at the top
        city_entry = tk.Entry(
            self.app,
            textvariable=self.app.city_var,  # Connected to app's city variable
            font=("Arial", int(14 + window_width/80)),  # Responsive font size
            width=max(15, int(window_width/50)),        # Responsive width
            justify="center",
            bg="white",
            fg="black",
            relief="solid",
            borderwidth=1,
            highlightthickness=0
        )
        city_entry.place(x=window_width/2, y=30, anchor="center")
        
        # Make Enter key trigger weather search
        city_entry.bind("<Return>", lambda e: self.app.fetch_and_display())
        
        # Add to widget tracking and store reference
        self.widgets.append(city_entry)
        self.city_entry = city_entry
        
        # Build different sections of the main page
        self._build_weather_metrics_section(window_width, y_start=70)
        self._build_main_weather_display(window_width, y_start=170)
        self._build_navigation_buttons(window_width, y_start=370)

    def _build_weather_metrics_section(self, window_width, y_start):
        """
        Build the weather metrics section with fully translated labels.
        
        This creates a grid showing humidity, wind speed, pressure, etc.
        All labels use translated text and transparent backgrounds.
        
        Args:
            window_width: Current width of the window
            y_start: Y position where this section should start
        """
        # Calculate layout for 6 columns of metrics
        available_width = window_width - 40
        col_width = available_width / 6
        start_x = 20
        
        # Create headers row with translated text
        metric_headers = [
            self.language_controller.get_text("humidity"),
            self.language_controller.get_text("wind"),
            self.language_controller.get_text("pressure"),
            self.language_controller.get_text("visibility"),
            self.language_controller.get_text("uv_index"),
            self.language_controller.get_text("precipitation")
        ]
        
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
        
        # Create emoji row for visual appeal
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
        
        # Create value display widgets
        value_widgets = []
        for i in range(6):
            x_pos = start_x + (i * col_width) + (col_width / 2)
            value_widget = self._create_label(
                self.app,
                text="--",  # Default placeholder
                font=("Arial", int(10 + window_width/120)),
                fg=self.app.text_color,
                x=x_pos,
                y=y_start + 50
            )
            self.widgets.append(value_widget)
            value_widgets.append(value_widget)
        
        # Store references to value widgets so we can update them later
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
        """
        Build the main weather display with translated loading text.
        
        This creates the central weather display showing:
        - Weather icon
        - Current temperature (clickable to change units)
        - Weather description
        
        Args:
            window_width: Current width of the window
            y_start: Y position where this section should start
        """
        y_offset = 60
        
        # Weather icon display
        icon_label = self._create_label(
            self.app,
            text="🌤️",  # Default weather emoji
            font=("Arial", int(40 + window_width/25)),
            fg=self.app.text_color,
            x=window_width/2,
            y=y_start + y_offset
        )
        self.widgets.append(icon_label)
        
        # Temperature display (clickable to toggle between C and F)
        canvas_bg = "#87CEEB"  # Default background
        if self.bg_canvas:
            try:
                canvas_bg = self.bg_canvas.cget("bg")
            except:
                canvas_bg = "#87CEEB"
        
        # Use translated loading text
        loading_text = self.language_controller.get_text("loading")
        
        temp_label = tk.Label(
            self.app,
            text=loading_text,
            font=("Arial", int(40 + window_width/25), "bold"),
            fg=self.app.text_color,
            bg=canvas_bg,  # Match canvas background to prevent blue boxes
            cursor="hand2",  # Show hand cursor to indicate it's clickable
            anchor="center",
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        temp_label.place(x=window_width/2, y=y_start + 70 + y_offset, anchor="center")
        
        # Make temperature clickable to toggle between Celsius and Fahrenheit
        temp_label.bind("<Button-1>", lambda e: [self.app.toggle_unit(), self.app.focus_set()])
        temp_label.bind("<FocusIn>", lambda e: self.app.focus_set())
        
        self.widgets.append(temp_label)
        
        # Weather description with translated text
        fetching_text = self.language_controller.get_text("fetching_weather")
        desc_label = self._create_label(
            self.app,
            text=fetching_text,
            font=("Arial", int(16 + window_width/60)),
            fg=self.app.text_color,
            x=window_width/2,
            y=y_start + 130 + y_offset
        )
        self.widgets.append(desc_label)
        
        # Store references to these important widgets
        widget_refs = {
            'icon_label': icon_label,
            'temp_label': temp_label,
            'desc_label': desc_label
        }
        self.set_widget_references(widget_refs)

    def _build_navigation_buttons(self, window_width, y_start):
        """
        Build navigation buttons in a 3x3 grid format with city comparison feature.
    
        This creates a professional 3x3 grid of buttons that let users navigate 
        to different pages including the new city comparison feature. All button 
        text is properly translated based on the current language setting.
    
        Args:
            window_width: Current width of the window
            y_start: Y position where buttons should start
        """
        # Button layout configuration
        button_width = 160
        button_height = 35
        button_spacing_x = 40  # Increased horizontal spacing from 20 to 40
        button_spacing_y = 35  # Increased vertical spacing from 15 to 35
    
        # Calculate positions for 3-column layout
        total_button_width = (button_width * 3) + (button_spacing_x * 2)
        start_x = (window_width - total_button_width) / 2
    
        # Calculate column positions
        col1_x = start_x + (button_width / 2)
        col2_x = start_x + button_width + button_spacing_x + (button_width / 2)
        col3_x = start_x + (button_width * 2) + (button_spacing_x * 2) + (button_width / 2)

        # Calculate row positions (pushed down by 20 pixels)
        y_start += 80  # Increased from 60 to 80 (20 additional pixels down)
        row1_y = y_start
        row2_y = y_start + button_height + button_spacing_y
        row3_y = y_start + (button_height + button_spacing_y) * 2

        # Define all buttons with translated text, commands, and positions in 3x3 grid
        buttons = [
            # Row 1: Core Weather Features
            (self.language_controller.get_text("toggle_theme"), 
             lambda: self.app.toggle_theme(), col1_x, row1_y),
            (self.language_controller.get_text("tomorrow_prediction"), 
             lambda: self.show_page("prediction"), col2_x, row1_y),
            (self.language_controller.get_text("weather_history"), 
             lambda: self.show_page("history"), col3_x, row1_y),

            # Row 2: Analysis & Visualization
            (self.language_controller.get_text("city_comparison"), 
             lambda: self.show_page("comparison"), col1_x, row2_y),
            (self.language_controller.get_text("weather_graphs"), 
             lambda: self.show_page("graphs"), col2_x, row2_y),
            (self.language_controller.get_text("map_view"), 
             lambda: self.show_page("map"), col3_x, row2_y),

            # Row 3: Interactive & Settings
            (self.language_controller.get_text("weather_quiz"), 
             lambda: self.show_page("quiz"), col1_x, row3_y),
            (self.language_controller.get_text("sun_moon"), 
             lambda: self.show_page("sun_moon"), col2_x, row3_y),
            (self.language_controller.get_text("language"), 
             lambda: self.show_page("language"), col3_x, row3_y)
        ]

        # Create each button with consistent styling
        for text, command, x, y in buttons:
            btn = tk.Button(
                self.app,
                text=text,
                command=command,
                bg="grey",
                fg="black",
                font=("Arial", int(9 + window_width/150), "bold"),  # Slightly smaller font for 3x3 grid
                relief="raised",
                borderwidth=2,
                width=16,  # Slightly narrower to fit 3 columns
                height=2,
                highlightthickness=0,
                cursor="hand2"  # Show hand cursor on hover
            )
            btn.place(x=x, y=y, anchor="center")
            self.widgets.append(btn)

        # Store reference to theme button for later access
        self.theme_btn = buttons[0]

    def _build_prediction_page(self):
        """Build the tomorrow's weather prediction page with translated text."""
        window_width = self.app.winfo_width()
        
        # Add back button to return to main page
        self._add_back_button()
        
        # Page title with translated text
        title_text = self.language_controller.get_text("tomorrow_weather_prediction")
        title = self._create_label(
            self.app,
            text=title_text,
            font=("Arial", int(24 + window_width/50), "bold"),
            fg=self.app.text_color,
            x=window_width/2,
            y=100
        )
        self.widgets.append(title)
        
        # Build the prediction display grid
        self._build_prediction_grid(window_width, y_start=200)

    def _build_prediction_grid(self, window_width, y_start):
        """
        Build the prediction display grid with translated labels.
        """
        # Calculate layout for 3 columns
        available_width = window_width - 40
        col_width = available_width / 3
        start_x = 20
        
        # Headers with translated text
        prediction_headers = [
            self.language_controller.get_text("temperature"),
            self.language_controller.get_text("accuracy"),
            self.language_controller.get_text("confidence")
        ]
        
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
        
        # Emojis
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
        
        # Value displays
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
        
        # Store widget references
        widget_refs = {
            'temp_prediction': prediction_widgets[0],
            'accuracy_prediction': prediction_widgets[1],
            'confidence_prediction': prediction_widgets[2]
        }
        self.set_widget_references(widget_refs)

    def _build_history_page(self):
        """Build the weather history page with translated text."""
        window_width = self.app.winfo_width()
        
        # Add back button
        self._add_back_button()
        
        # Page title with translated text
        title_text = self.language_controller.get_text("weather_history_title")
        title = self._create_label(
            self.app,
            text=title_text,
            font=("Arial", int(24 + window_width/50), "bold"),
            fg=self.app.text_color,
            x=window_width/2,
            y=100
        )
        self.widgets.append(title)
        
        # Update history display when page is built
        city = self.app.city_var.get()
        self.app.after(100, lambda: self.update_history_display(city))

    def _build_comparison_page(self):
        """Build the city comparison page."""
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        # Use the specialized controller to build this page
        self.city_comparison_controller.build_page(window_width, window_height)

    def _build_map_page(self):
        """Build the interactive map page with translated text."""
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        # Add back button
        self._add_back_button()
        
        # Page title with translated text
        title_text = self.language_controller.get_text("weather_map")
        title = self._create_label(
            self.app,
            text=title_text,
            font=("Arial", int(24 + window_width/50), "bold"),
            fg=self.app.text_color,
            x=window_width/2,
            y=100
        )
        self.widgets.append(title)
        
        # Map display area
        map_y_position = window_height/2 + 40
        
        # Get canvas background color for consistency
        canvas_bg = "#87CEEB"
        if self.bg_canvas:
            try:
                canvas_bg = self.bg_canvas.cget("bg")
            except:
                canvas_bg = "#87CEEB"
        
        # Create map frame
        map_frame = tk.Frame(
            self.app,
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
            import os
            api_key = os.getenv("weatherdb_api_key")
            
            # Initialize map controller with translation function (but no side panel)
            self.map_controller = MapController(
                map_frame, 
                lambda: self.app.city_var.get(), 
                api_key, 
                show_grid=True,
                translate_func=self.language_controller.get_text
            )
            
            # Info button - connect to popup method instead of toggle panel
            info_btn = tk.Button(
                self.app,
                text="i",
                command=self._show_detailed_map_info_popup,  # Show popup instead
                bg="grey",
                fg="black",
                font=("Arial", 12, "bold"),  # Changed from int(16 + window_width/80) to 12
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
                self.app,
                text="i",
                command=lambda: self._show_map_info(info_text),
                bg="grey",
                fg="black",
                font=("Arial", 12, "bold"),  # Changed from int(16 + window_width/80) to 12
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
        if hasattr(self, 'map_controller') and hasattr(self.map_controller, 'layer_var'):
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
        if hasattr(self, 'map_controller') and hasattr(self.map_controller, 'layer_options'):
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

    def _build_map_info_content(self, current_overlay):
        """Build the content text for the map info popup."""
        content = ""
        
        # Base map information
        content += f"{self.language_controller.get_text('base_map_info')}\n"
        content += "=" * 30 + "\n\n"
        content += f"{self.language_controller.get_text('base_map_description')}\n\n"
        
        content += f"{self.language_controller.get_text('map_features')}\n"
        features = [
            self.language_controller.get_text('feature_navigation'),
            self.language_controller.get_text('feature_overlays'),
            self.language_controller.get_text('feature_tracking'),
            self.language_controller.get_text('feature_integration'),
            self.language_controller.get_text('feature_geocoding'),
            self.language_controller.get_text('feature_markers'),
            self.language_controller.get_text('feature_updates'),
            self.language_controller.get_text('feature_basemap')
        ]
        
        for feature in features:
            content += f"{feature}\n"
        
        # Weather overlay information
        content += f"\n{self.language_controller.get_text('overlay_information')}\n"
        content += "=" * 35 + "\n\n"
        
        # Get current overlay display name
        current_display = self.language_controller.get_text('overlay_none')
        if hasattr(self, 'map_controller') and hasattr(self.map_controller, 'layer_options'):
            if current_overlay in self.map_controller.layer_options:
                current_display = self.map_controller.layer_options[current_overlay]
        
        content += f"{self.language_controller.get_text('current_overlay')}: {current_display}\n\n"
        
        if current_overlay == "none":
            content += f"{self.language_controller.get_text('no_overlay_selected')}\n\n"
            content += f"{self.language_controller.get_text('select_overlay_for_info')}\n\n"
        else:
            # Get overlay-specific information
            overlay_info = self._get_overlay_info_for_popup(current_overlay)
            if overlay_info:
                content += f"{overlay_info['title']}\n"
                content += "-" * len(overlay_info['title']) + "\n\n"
                content += f"{overlay_info['description']}\n\n"
                content += f"{overlay_info['features']}\n\n"
        
        return content

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

    def _build_sun_moon_page(self):
        """Build the sun and moon phases page."""
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        # Use the specialized controller to build this page
        self.sun_moon_controller.build_page(window_width, window_height)
        
        # Update display with current city
        city = self.app.city_var.get().strip() or "New York"
        self.sun_moon_controller.update_display(city)

    def _build_graphs_page(self):
        """Build the weather graphs page."""
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        # Initialize graphs controller if it doesn't exist
        if not hasattr(self, 'graphs_controller'):
            self.graphs_controller = GraphsController(self.app, self)
        
        # Build the graphs page
        self.graphs_controller.build_page(window_width, window_height)

    def _build_quiz_page(self):
        """Build the weather quiz page."""
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        # Build the quiz page using the specialized controller
        self.weather_quiz_controller.build_page(window_width, window_height)

    def _build_language_page(self):
        """Build the language selection page."""
        window_width = self.app.winfo_width()
        window_height = self.app.winfo_height()
        
        # Build the language page using the specialized controller
        self.language_controller.build_page(window_width, window_height)

    def _show_map_info(self, info_text=None):
        """Show detailed map information popup - redirects to our detailed popup."""
        self._show_detailed_map_info_popup()

    def _add_back_button(self):
        """Add a back button to return to the main page with translated text."""
        back_text = self.language_controller.get_text("back")
        back_btn = tk.Button(
            self.app,
            text=back_text,
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
        """Handle window resize events by rebuilding the current page."""
        if event.widget == self.app:
            # Use after_idle to prevent too many rapid rebuilds
            self.app.after_idle(self._rebuild_current_page)

    def _rebuild_current_page(self):
        """Rebuild the current page when window is resized."""
        try:
            current_page = self.current_page
            self.show_page(current_page)
            self._restore_current_data()
        except Exception as e:
            pass

    def _restore_current_data(self):
        """Restore current data after page rebuild."""
        # Restore weather data if available
        if self.app.current_weather_data:
            self.weather_display.update_weather_display(self.app.current_weather_data)
        
        # Restore prediction data if available
        if self.app.current_prediction_data:
            predicted_temp, confidence, accuracy = self.app.current_prediction_data
            self.weather_display.update_tomorrow_prediction_direct(
                predicted_temp, confidence, accuracy
            )
    
    def update_weather_display(self, weather_data):
        """Update the weather display with new data."""
        self.weather_display.update_weather_display(weather_data)

    def update_tomorrow_prediction_direct(self, predicted_temp, confidence, accuracy):
        """Update the prediction display with new data."""
        self.weather_display.update_tomorrow_prediction_direct(
            predicted_temp, confidence, accuracy
        )

    def update_history_display(self, city):
        """Update the history display for a specific city."""
        self.weather_display.update_history_display(city)

    def update_background_animation(self, weather_data):
        """Update the background animation based on weather conditions."""
        self.animation_controller.update_background_animation(weather_data)

    def update_sun_moon_display(self, city):
        """Update the sun and moon display for a specific city."""
        if hasattr(self, 'sun_moon_controller'):
            self.sun_moon_controller.update_display(city)

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.weather_display.toggle_theme()

    def cleanup_animation(self):
        """Clean up animation resources when closing the app."""
        self.animation_controller.cleanup_animation()
        
        # Clean up other controllers
        if hasattr(self, 'sun_moon_controller'):
            self.sun_moon_controller.cleanup()
        
        if hasattr(self, 'graphs_controller'):
            self.graphs_controller.cleanup()
        
        if hasattr(self, 'weather_quiz_controller'):
            self.weather_quiz_controller.cleanup()
            
        if hasattr(self, 'language_controller'):
            self.language_controller.cleanup()

    def get_widgets(self):
        """Get the list of widgets for external access."""
        return self.widgets

    def get_history_labels(self):
        """Get the list of history labels for external access."""
        return self.history_labels

    def set_widget_references(self, widget_refs):
        """
        Set widget references for easy access by other components.
        
        Args:
            widget_refs (dict): Dictionary mapping attribute names to widgets
        """
        for attr_name, widget in widget_refs.items():
            setattr(self, attr_name, widget)