"""
Integrated Map View
==================

Complete map view implementation that combines the map controller with 
the information panel for a full interactive map experience.

Features:
- Interactive map with weather overlays
- Dynamic information panel that updates with overlay selection
- Base map info displayed first, overlay-specific info shown when filters are applied
- Full translation support for all components
- Coordinated updates between map and information panel
"""

import tkinter as tk
from tkinter import ttk

from .controller import MapController
from .map_info_panel import MapInfoPanel

class IntegratedMapView:
    def __init__(self, parent, get_city_callback, api_key, translation_manager):
        """Initialize the complete map view with controller and info panel"""
        self.tr = translation_manager
        self.get_city_callback = get_city_callback
        self.api_key = api_key
        
        # Create main container
        self.main_frame = ttk.Frame(parent)
        self.main_frame.pack(fill="both", expand=True)
        
        # Create paned window for resizable layout
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel: Map controller
        self.map_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.map_frame, weight=2)
        
        # Right panel: Information panel  
        self.info_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.info_frame, weight=1)
        
        # Initialize map controller
        self.map_controller = MapController(
            parent=self.map_frame,
            get_city_callback=self.get_city_callback,
            api_key=self.api_key,
            translation_manager=self.tr
        )
        
        # Initialize info panel
        self.info_panel = MapInfoPanel(
            parent=self.info_frame,
            map_controller=self.map_controller,
            translation_manager=self.tr
        )
        
        # Set up coordination between components
        self.setup_component_coordination()

    def setup_component_coordination(self):
        """Set up coordination between map controller and info panel"""
        # Override the map controller's overlay update method to also update info panel
        original_update_overlay = self.map_controller.update_weather_overlay
        
        def coordinated_overlay_update():
            # Update the map overlay
            original_update_overlay()
            # Update the info panel
            self.info_panel.update_overlay_info()
        
        self.map_controller.update_weather_overlay = coordinated_overlay_update
        
        # Also update info panel when map is refreshed
        original_refresh = self.map_controller.refresh
        
        def coordinated_refresh():
            original_refresh()
            self.info_panel.update_overlay_info()
        
        self.map_controller.refresh = coordinated_refresh

    def update_language(self, translation_manager):
        """Update language for all components"""
        self.tr = translation_manager
        
        # Update map controller language
        if hasattr(self.map_controller, 'update_language'):
            self.map_controller.update_language(translation_manager)
        
        # Update info panel language
        if hasattr(self.info_panel, 'update_language'):
            self.info_panel.update_language(translation_manager)

    def refresh_all(self):
        """Refresh both map and information display"""
        if self.map_controller:
            self.map_controller.refresh()

    def get_current_overlay(self):
        """Get the currently selected overlay"""
        if self.map_controller:
            return self.map_controller.layer_var.get()
        return None

    def set_overlay(self, overlay_name):
        """Set a specific overlay programmatically"""
        if self.map_controller and overlay_name in self.map_controller.overlay_mapping:
            self.map_controller.layer_var.set(overlay_name)
            self.map_controller.update_weather_overlay()

    def show_overlay_help(self, overlay_type):
        """Show detailed help for a specific overlay type"""
        if self.info_panel:
            help_info = self.info_panel.get_overlay_help_text(overlay_type)
            # Could open a popup window or update the info panel with detailed help
            return help_info
        return None

    def cleanup(self):
        """Clean up all resources"""
        if self.map_controller:
            self.map_controller.cleanup()


# Example usage and integration into main application
class MapPageExample:
    """Example of how to integrate the map view into your main weather application"""
    
    def __init__(self, parent, main_app_instance):
        self.main_app = main_app_instance
        self.parent = parent
        
        # Create the complete map view
        self.map_view = IntegratedMapView(
            parent=self.parent,
            get_city_callback=self.get_current_city,  # Method from main app
            api_key=self.main_app.api_key,  # API key from main app
            translation_manager=self.main_app.translation_manager  # Translation from main app
        )
        
        # Add any additional controls or features specific to your app
        self.setup_additional_controls()

    def get_current_city(self):
        """Get the currently selected city from the main application"""
        # This should return the city name that's currently selected in your main app
        if hasattr(self.main_app, 'get_current_city'):
            return self.main_app.get_current_city()
        elif hasattr(self.main_app, 'current_city'):
            return self.main_app.current_city
        else:
            return "New York"  # Default fallback

    def setup_additional_controls(self):
        """Add any additional controls specific to your application"""
        # Example: Add a frame for additional controls at the bottom
        controls_frame = ttk.Frame(self.parent)
        controls_frame.pack(fill="x", padx=5, pady=5)
        
        # Example: Add preset city buttons
        preset_cities = ["New York", "London", "Tokyo", "Sydney", "Mumbai"]
        for city in preset_cities:
            btn = ttk.Button(
                controls_frame, 
                text=city, 
                command=lambda c=city: self.load_city(c),
                width=10
            )
            btn.pack(side="left", padx=2)

    def load_city(self, city_name):
        """Load a specific city in the map"""
        # Update main app's current city
        if hasattr(self.main_app, 'set_current_city'):
            self.main_app.set_current_city(city_name)
        
        # Refresh the map
        if self.map_view:
            self.map_view.refresh_all()

    def on_language_change(self, new_translation_manager):
        """Handle language changes from the main application"""
        if self.map_view:
            self.map_view.update_language(new_translation_manager)

    def cleanup(self):
        """Clean up when the map page is closed"""
        if self.map_view:
            self.map_view.cleanup()


# Integration instructions for main application:
"""
To integrate this map view into your main weather application:

1. In your main app navigation, add a method to create the map page:

def show_map_view(self):
    # Clear current content
    self.clear_content()
    
    # Create map page
    self.map_page = MapPageExample(self.content_frame, self)
    
    # Update current page reference
    self.current_page = "map"

2. Update your language change handler to include map updates:

def on_language_change(self, new_language):
    # Update translation manager
    self.translation_manager.set_language(new_language)
    
    # Update current page if it's the map
    if hasattr(self, 'map_page') and self.map_page:
        self.map_page.on_language_change(self.translation_manager)

3. Ensure your main app has these methods available:
   - get_current_city() or current_city attribute
   - api_key attribute for weather API
   - translation_manager attribute

4. Add the map view button to your navigation:

map_btn = ttk.Button(nav_frame, text=self.tr("map_view"), command=self.show_map_view)
map_btn.pack(side="left", padx=5)
"""