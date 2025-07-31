"""
Map Information Panel
====================

Displays detailed information about current map overlay and features.
Shows base map information first, then overlay-specific details when filters are selected.

Features:
- Base map capabilities and feature descriptions
- Dynamic overlay-specific information updates
- Multi-language support for all content
- Clean, organized information display
- Automatic updates when overlay selection changes
"""

import tkinter as tk
from tkinter import ttk

class MapInfoPanel:
    def __init__(self, parent, map_controller, translation_manager):
        """Initialize the map information panel"""
        self.map_controller = map_controller
        self.tr = translation_manager
        
        # Create the main info panel frame
        self.frame = ttk.LabelFrame(parent, text=self.tr("map_information"))
        self.frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create scrollable content area
        self.canvas = tk.Canvas(self.frame, height=300)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollable components
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Initialize content
        self.setup_base_info()
        self.setup_overlay_info()
        
        # Bind to overlay changes
        if hasattr(map_controller, 'layer_dropdown'):
            map_controller.layer_dropdown.bind("<<ComboboxSelected>>", self.on_overlay_change)

    def setup_base_info(self):
        """Set up the base map information section"""
        # Base Map Information Section
        base_frame = ttk.LabelFrame(self.scrollable_frame, text=self.tr("base_map_info"))
        base_frame.pack(fill="x", padx=5, pady=5)
        
        # Base map description
        desc_label = ttk.Label(base_frame, text=self.tr("base_map_description"), 
                              wraplength=400, justify="left")
        desc_label.pack(anchor="w", padx=10, pady=5)
        
        # Map features header
        features_label = ttk.Label(base_frame, text=self.tr("map_features"), 
                                 font=("TkDefaultFont", 9, "bold"))
        features_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Feature list
        features = [
            self.tr("feature_navigation"),
            self.tr("feature_overlays"),
            self.tr("feature_tracking"),
            self.tr("feature_integration"),
            self.tr("feature_geocoding"),
            self.tr("feature_markers"),
            self.tr("feature_updates"),
            self.tr("feature_basemap")
        ]
        
        for feature in features:
            feature_label = ttk.Label(base_frame, text=feature, wraplength=400, justify="left")
            feature_label.pack(anchor="w", padx=20, pady=1)

    def setup_overlay_info(self):
        """Set up the overlay-specific information section"""
        # Overlay Information Section
        self.overlay_frame = ttk.LabelFrame(self.scrollable_frame, text=self.tr("overlay_information"))
        self.overlay_frame.pack(fill="x", padx=5, pady=5)
        
        # Current overlay header
        self.current_overlay_label = ttk.Label(self.overlay_frame, 
                                             text=f"{self.tr('current_overlay')}: {self.tr('overlay_none')}", 
                                             font=("TkDefaultFont", 9, "bold"))
        self.current_overlay_label.pack(anchor="w", padx=10, pady=5)
        
        # Overlay description area
        self.overlay_desc_label = ttk.Label(self.overlay_frame, 
                                          text=self.tr("select_overlay_for_info"),
                                          wraplength=400, justify="left")
        self.overlay_desc_label.pack(anchor="w", padx=10, pady=5)
        
        # Overlay features area (initially hidden)
        self.overlay_features_frame = ttk.Frame(self.overlay_frame)
        self.overlay_features_label = ttk.Label(self.overlay_features_frame, text="", 
                                               wraplength=400, justify="left")

    def on_overlay_change(self, event=None):
        """Handle overlay selection changes"""
        if self.map_controller:
            self.update_overlay_info()

    def update_overlay_info(self):
        """Update the overlay information section"""
        if not self.map_controller:
            return
            
        # Get current overlay information
        overlay_info = self.map_controller.get_current_overlay_info()
        
        # Update current overlay display
        self.current_overlay_label.config(
            text=f"{self.tr('current_overlay')}: {overlay_info['name']}"
        )
        
        # Update description
        self.overlay_desc_label.config(text=overlay_info['description'])
        
        # Handle features display
        if overlay_info['features']:
            # Show features if available
            self.overlay_features_label.config(text=overlay_info['features'])
            self.overlay_features_frame.pack(fill="x", padx=10, pady=5)
            self.overlay_features_label.pack(anchor="w")
        else:
            # Hide features section if no features
            self.overlay_features_frame.pack_forget()

    def update_language(self, translation_manager):
        """Update all text when language changes"""
        self.tr = translation_manager
        
        # Update frame title
        self.frame.config(text=self.tr("map_information"))
        
        # Clear and rebuild all content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        # Rebuild content with new translations
        self.setup_base_info()
        self.setup_overlay_info()
        self.update_overlay_info()

    def show_base_info(self):
        """Show only base map information (no overlay selected)"""
        self.update_overlay_info()

    def get_overlay_help_text(self, overlay_type):
        """Get help text for specific overlay type"""
        help_mapping = {
            "temp_new": {
                "title": self.tr("temperature_overlay_info"),
                "description": self.tr("temperature_overlay_desc"),
                "features": self.tr("temperature_overlay_features")
            },
            "wind_new": {
                "title": self.tr("wind_overlay_info"),
                "description": self.tr("wind_overlay_desc"),
                "features": self.tr("wind_overlay_features")
            },
            "precipitation_new": {
                "title": self.tr("precipitation_overlay_info"),
                "description": self.tr("precipitation_overlay_desc"),
                "features": self.tr("precipitation_overlay_features")
            },
            "clouds_new": {
                "title": self.tr("clouds_overlay_info"),
                "description": self.tr("clouds_overlay_desc"),
                "features": self.tr("clouds_overlay_features")
            },
            "pressure_new": {
                "title": self.tr("pressure_overlay_info"),
                "description": self.tr("pressure_overlay_desc"),
                "features": self.tr("pressure_overlay_features")
            },
            "snow_new": {
                "title": self.tr("snow_overlay_info"),
                "description": self.tr("snow_overlay_desc"),
                "features": self.tr("snow_overlay_features")
            },
            "dewpoint_new": {
                "title": self.tr("dewpoint_overlay_info"),
                "description": self.tr("dewpoint_overlay_desc"),
                "features": self.tr("dewpoint_overlay_features")
            }
        }
        
        return help_mapping.get(overlay_type, {
            "title": self.tr("unknown"),
            "description": self.tr("no_description"),
            "features": ""
        })
    