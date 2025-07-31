"""
Basic Map Display Widget
=======================

Simple map display component for showing city locations with interactive markers.

Features:
- Clean map widget with rounded corners
- Automatic city location lookup and display
- Interactive location markers with city labels
- Default New York City positioning
- Easy location updates via city name input
- Multi-language status messages and error handling

This module provides the foundational map display functionality without
weather overlays, perfect for basic location visualization needs.
"""

from tkintermapview import TkinterMapView
import tkinter as tk
from tkinter import ttk

class MapDisplay:
    def __init__(self, parent, translation_manager=None):
        self.tr = translation_manager if translation_manager else lambda x: x
        
        # Create the map widget with specific size and rounded corners
        self.map_widget = TkinterMapView(parent, width=600, height=300, corner_radius=10)
        # Add the map widget to the parent window with some padding
        self.map_widget.pack(pady=10)
        
        # Variable to store the current location marker (pin on the map)
        self.marker = None
        
        # Status label for showing loading/error messages
        self.status_label = ttk.Label(parent, text="", foreground="blue")
        self.status_label.pack(pady=(5, 0))
        
        # Set New York as the default location when the map first loads
        self.set_location("New York")

    def set_location(self, city_name):
        """Update the map to show a new city location"""
        # If no city name is provided, don't do anything
        if not city_name:
            self.show_error(self.tr("city_not_found") if self.tr else "City not found")
            return

        try:
            self.show_status(self.tr("updating_location") if self.tr else "Updating location...")
            
            # Move the map to show the specified city
            self.map_widget.set_address(city_name)

            # Remove the old marker if one exists
            if self.marker:
                self.map_widget.delete(self.marker)

            # Add a new marker at the city location
            self.marker = self.map_widget.set_address(city_name, marker=True)
            
            self.clear_status()
            
        except Exception as e:
            self.show_error(self.tr("location_not_found") if self.tr else "Location not found")

    def show_status(self, message):
        """Display a status message to the user"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message, foreground="blue")
            self.status_label.update()

    def show_error(self, message):
        """Display an error message to the user"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message, foreground="red")

    def clear_status(self):
        """Clear the status message"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text="")

    def update_language(self, translation_manager):
        """Update language for status messages"""
        self.tr = translation_manager

    def cleanup(self):
        """Clean up resources when the map is closed"""
        if self.map_widget:
            self.map_widget.destroy()
            