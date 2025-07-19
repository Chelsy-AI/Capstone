import tkinter as tk
from tkinter import ttk

from .layout_manager import LayoutManager
from .scroll_handler import ScrollHandler
from .weather_display import WeatherDisplay
from .animation_controller import AnimationController


class WeatherGUI:
    """
    Main GUI Controller
    
    This class coordinates all GUI components and serves as the main
    interface between the application logic and the user interface.
    It delegates specific responsibilities to specialized components.
    """
    
    def __init__(self, parent_app):
        """Initialize GUI with reference to parent application"""
        self.app = parent_app
        
        # Initialize GUI components
        self.layout_manager = LayoutManager(self.app, self)
        self.scroll_handler = ScrollHandler(self.app, self)
        self.weather_display = WeatherDisplay(self.app, self)
        self.animation_controller = AnimationController(self.app, self)
        
        # GUI state tracking
        self.widgets = []
        self.history_labels = []
        
        # Background elements
        self.bg_canvas = None
        self.scrollbar = None
        
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

    def build_gui(self):
        """Build the complete GUI interface"""
        print("[GUI] Building main interface...")
        
        # Clear existing widgets but preserve special elements
        self._clear_widgets()
        
        # Bind window events
        self.app.bind("<Configure>", self._on_window_resize)
        
        # Setup background and scrolling
        self._setup_background()
        self._setup_scrolling()
        
        # Build the main layout
        self.layout_manager.build_responsive_layout()
        
        print("[GUI] Main interface ready")

    def _clear_widgets(self):
        """Clear existing widgets while preserving special elements"""
        for widget in self.app.winfo_children():
            if (not hasattr(widget, '_preserve') and 
                widget != self.bg_canvas and 
                widget != self.scrollbar):
                widget.destroy()
        self.widgets.clear()

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

    def _setup_scrolling(self):
        """Setup scrollbar and scroll handling"""
        if not self.scrollbar:
            self.scrollbar = ttk.Scrollbar(
                self.app, 
                orient="vertical", 
                command=self.scroll_handler.on_scroll
            )
            self.scrollbar.place(relx=0.98, y=0, relheight=1, width=20)
            self.scrollbar._preserve = True

            # Bind scroll events
            self.scroll_handler.bind_scroll_events()

    def _on_window_resize(self, event):
        """Handle window resize events"""
        if event.widget == self.app:
            self.app.after_idle(self._rebuild_layout_on_resize)

    def _rebuild_layout_on_resize(self):
        """Rebuild layout when window is resized"""
        try:
            print("[GUI] Rebuilding layout for resize...")
            
            # Clear widgets but preserve special elements
            self._clear_widgets()
            self.history_labels.clear()
            
            # Rebuild layout
            self.layout_manager.build_responsive_layout()
            
            # Restore current data
            self._restore_current_data()
            
        except Exception as e:
            print(f"❌ Resize error: {e}")

    def _restore_current_data(self):
        """Restore current data after layout rebuild"""
        if self.app.current_weather_data:
            self.weather_display.update_weather_display(self.app.current_weather_data)
        
        if self.app.current_prediction_data:
            predicted_temp, confidence, accuracy = self.app.current_prediction_data
            self.weather_display.update_tomorrow_prediction_direct(
                predicted_temp, confidence, accuracy
            )
        
        if self.app.current_history_data:
            self.weather_display.restore_history_data()

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

    # Getter methods for layout manager access to widgets
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