"""
Interactive Weather Map Controller
=================================

Advanced map control system with integrated weather overlays and real-time updates.

Features:
- Interactive map navigation with zoom and pan controls
- Multiple weather overlay options (temperature, wind, precipitation, clouds, pressure, snow, dewpoint)
- Real-time city location tracking with GPS coordinates
- Custom tile server integration for weather data visualization
- Automatic geocoding to convert city names to map coordinates
- Dynamic marker placement for selected cities
- Refresh functionality for live weather updates
- Seamless integration with OpenStreetMap base tiles

The controller manages all map interactions and coordinates between the UI,
weather data services, and the custom tile server for optimal performance.
"""

import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
import requests
import threading

from .tile_server import start_tile_server

class MapController:
    def __init__(self, parent, get_city_callback, api_key, show_grid=True, translate_func=None):
        # Store the callback function that tells us which city to show
        self.get_city_callback = get_city_callback
        # Store the API key for weather data
        self.api_key = api_key
        # Store whether to show grid lines
        self.show_grid = show_grid
        # Store translation function
        self.translate = translate_func or (lambda x: x)

        # Set default map position (New York City coordinates)
        self.current_lat = 40.7127281
        self.current_lon = -74.0060152
        self.current_zoom = 6

        # URL for getting basic map tiles from OpenStreetMap
        self.base_tile_server = "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
        # This will store the URL for our custom weather overlay tiles
        self.composite_tile_url = None

        # Create the main frame that holds all map components
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create a frame for control buttons at the top
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill="x", pady=(0, 5))

        # Add a label for the weather overlay dropdown
        ttk.Label(control_frame, text=self.translate("weather_overlay")).pack(side="left", padx=(0, 5))

        # Create dropdown menu for selecting weather overlays
        self.layer_var = tk.StringVar(value="none")  # Default to no overlay
        self.layer_dropdown = ttk.Combobox(control_frame, textvariable=self.layer_var, state="readonly", width=20)
        # Set available weather overlay options with translated labels
        self.layer_options = {
            "none": self.translate("overlay_none"),
            "temp_new": self.translate("overlay_temperature"),
            "wind_new": self.translate("overlay_wind"),
            "precipitation_new": self.translate("overlay_precipitation"),
            "clouds_new": self.translate("overlay_clouds"),
            "pressure_new": self.translate("overlay_pressure"),
            "snow_new": self.translate("overlay_snow"),
            "dewpoint_new": self.translate("overlay_dewpoint")
        }
        self.layer_dropdown['values'] = list(self.layer_options.values())
        self.layer_dropdown.pack(side="left", padx=(0, 10))
        # When user selects a different overlay, update the map
        self.layer_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_weather_overlay())

        # Add a refresh button to update the map
        refresh_button = ttk.Button(control_frame, text=self.translate("refresh"), command=self.refresh)
        refresh_button.pack(side="left")



        # Create main content frame
        content_frame = ttk.Frame(self.frame)
        content_frame.pack(fill="both", expand=True)

        # Create a container frame for the map widget
        self.map_container = tk.Frame(content_frame, bg='gray')
        self.map_container.pack(fill="both", expand=True)

        # Create the actual map widget
        self.map_view = TkinterMapView(self.map_container, width=600, height=350, corner_radius=0)
        self.map_view.place(x=0, y=0, relwidth=1, relheight=1)

        # Create information panel (initially hidden)
        self.info_panel_visible = False
        self.content_frame = content_frame
        self.info_frame = None

        # Variable to store the current map marker (pin showing city location)
        self.marker = None

        # Start our local tile server that combines map and weather data
        self.tile_server_port = 5005
        self.tile_server_url = f"http://localhost:{self.tile_server_port}"
        # Run the tile server in a separate thread so it doesn't block the GUI
        threading.Thread(target=start_tile_server, args=(self.api_key, self.tile_server_port), daemon=True).start()

        # Set up the basic map display
        self.setup_base_map()
        # Update the map to show the current city
        self.update_map()

    def toggle_info_panel(self):
        """Toggle the visibility of the information panel"""
        if self.info_panel_visible:
            # Hide the info panel
            if self.info_frame:
                self.info_frame.destroy()
                self.info_frame = None
            self.map_container.pack(fill="both", expand=True)
            self.info_panel_visible = False
        else:
            # Show the info panel
            self.map_container.pack(side="left", fill="both", expand=True)
            self.create_info_panel(self.content_frame)
            self.update_info_panel()
            self.info_panel_visible = True

    def create_info_panel(self, parent):
        """Create the information panel on the right side of the map"""
        # Create info panel frame
        self.info_frame = ttk.Frame(parent, width=300)
        self.info_frame.pack(side="right", fill="y", padx=(10, 0))
        self.info_frame.pack_propagate(False)  # Maintain fixed width

        # Info panel title
        title_label = ttk.Label(self.info_frame, text=self.translate("map_information"), 
                               font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))

        # Create scrollable text widget for information
        self.info_text = tk.Text(self.info_frame, wrap=tk.WORD, height=20, width=35, 
                                font=("Arial", 9), state=tk.DISABLED)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.info_frame, orient="vertical", command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        # Pack text widget and scrollbar
        self.info_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_info_panel(self):
        """Update the information panel content based on current overlay selection"""
        if not self.info_panel_visible or not hasattr(self, 'info_text'):
            return
            
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)

        # Get current overlay selection
        current_display = self.layer_var.get()
        current_layer = None
        for key, value in self.layer_options.items():
            if value == current_display:
                current_layer = key
                break

        # Base map information
        self.info_text.insert(tk.END, f"{self.translate('base_map_info')}\n", "title")
        self.info_text.insert(tk.END, "=" * 25 + "\n\n")
        
        self.info_text.insert(tk.END, f"{self.translate('base_map_description')}\n\n")
        
        self.info_text.insert(tk.END, f"{self.translate('map_features')}\n")
        features = [
            self.translate('feature_navigation'),
            self.translate('feature_overlays'),
            self.translate('feature_tracking'),
            self.translate('feature_integration'),
            self.translate('feature_geocoding'),
            self.translate('feature_markers'),
            self.translate('feature_updates'),
            self.translate('feature_basemap')
        ]
        
        for feature in features:
            self.info_text.insert(tk.END, f"{feature}\n")
        
        # Weather overlay information
        self.info_text.insert(tk.END, f"\n{self.translate('overlay_information')}\n", "title")
        self.info_text.insert(tk.END, "=" * 30 + "\n\n")
        
        self.info_text.insert(tk.END, f"{self.translate('current_overlay')}: {current_display}\n\n")

        if current_layer == "none":
            self.info_text.insert(tk.END, f"{self.translate('no_overlay_selected')}\n\n")
            self.info_text.insert(tk.END, f"{self.translate('select_overlay_for_info')}")
        else:
            # Get overlay-specific information
            overlay_info = self.get_overlay_info(current_layer)
            if overlay_info:
                self.info_text.insert(tk.END, f"{overlay_info['title']}\n", "subtitle")
                self.info_text.insert(tk.END, "-" * len(overlay_info['title']) + "\n\n")
                self.info_text.insert(tk.END, f"{overlay_info['description']}\n\n")
                self.info_text.insert(tk.END, f"{overlay_info['features']}")

        # Configure text tags for formatting
        self.info_text.tag_configure("title", font=("Arial", 10, "bold"))
        self.info_text.tag_configure("subtitle", font=("Arial", 9, "bold"))
        
        self.info_text.config(state=tk.DISABLED)

    def get_overlay_info(self, layer_key):
        """Get detailed information about a specific weather overlay"""
        overlay_data = {
            "temp_new": {
                "title": self.translate("temperature_overlay_info"),
                "description": self.translate("temperature_overlay_desc"),
                "features": self.translate("temperature_overlay_features")
            },
            "wind_new": {
                "title": self.translate("wind_overlay_info"),
                "description": self.translate("wind_overlay_desc"),
                "features": self.translate("wind_overlay_features")
            },
            "precipitation_new": {
                "title": self.translate("precipitation_overlay_info"),
                "description": self.translate("precipitation_overlay_desc"),
                "features": self.translate("precipitation_overlay_features")
            },
            "clouds_new": {
                "title": self.translate("clouds_overlay_info"),
                "description": self.translate("clouds_overlay_desc"),
                "features": self.translate("clouds_overlay_features")
            },
            "pressure_new": {
                "title": self.translate("pressure_overlay_info"),
                "description": self.translate("pressure_overlay_desc"),
                "features": self.translate("pressure_overlay_features")
            },
            "snow_new": {
                "title": self.translate("snow_overlay_info"),
                "description": self.translate("snow_overlay_desc"),
                "features": self.translate("snow_overlay_features")
            },
            "dewpoint_new": {
                "title": self.translate("dewpoint_overlay_info"),
                "description": self.translate("dewpoint_overlay_desc"),
                "features": self.translate("dewpoint_overlay_features")
            }
        }
        
        return overlay_data.get(layer_key)

    def setup_base_map(self):
        """Set up the basic map without any weather overlays"""
        # Tell the map widget where to get basic map tiles from
        self.map_view.set_tile_server(self.base_tile_server, max_zoom=22)
        # Set the initial zoom level
        self.map_view.set_zoom(self.current_zoom)

    def update_map(self):
        """Update the map to show the current selected city"""
        # Get the city name from the main application
        city = self.get_city_callback()
        # Convert city name to latitude/longitude coordinates
        coords = self.geocode_city(city)

        # If we successfully got coordinates
        if coords:
            # Update our stored coordinates
            self.current_lat, self.current_lon = coords
            # Move the map to show this location
            self.map_view.set_position(self.current_lat, self.current_lon)
            self.map_view.set_zoom(self.current_zoom)

            # Remove the old marker if it exists
            if self.marker:
                self.map_view.delete(self.marker)
            # Add a new marker at the city location
            self.marker = self.map_view.set_marker(self.current_lat, self.current_lon, text=city)

    def update_weather_overlay(self):
        """Change the weather overlay displayed on the map"""
        # Get the selected overlay display name
        overlay_display = self.layer_var.get()
        
        # Find the corresponding layer key
        layer_key = None
        for key, value in self.layer_options.items():
            if value == overlay_display:
                layer_key = key
                break

        # If "none" is selected, show just the basic map
        if layer_key == "none":
            self.map_view.set_tile_server(self.base_tile_server, max_zoom=22)
        else:
            # Build URL for our custom tile server that combines map + weather data
            composite_url = f"{self.tile_server_url}/tiles/{layer_key}/{{z}}/{{x}}/{{y}}.png"
            # Switch the map to use our custom tiles with weather overlay
            self.map_view.set_tile_server(composite_url, max_zoom=10)
        
        # Update the info panel to reflect the new overlay (only if visible)
        if self.info_panel_visible:
            self.update_info_panel()

    def geocode_city(self, city_name):
        """Convert a city name into latitude/longitude coordinates"""
        try:
            # Use OpenStreetMap's free geocoding service
            url = f"https://nominatim.openstreetmap.org/search"
            # Set up search parameters
            params = {"q": city_name, "format": "json", "limit": 1}
            # Include a user agent as required by the service
            headers = {"User-Agent": "Tkinter Weather App 1.0"}

            # Make the web request to get coordinates
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an error if request failed

            # Parse the JSON response
            data = response.json()
            # If we got results, extract the coordinates
            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return lat, lon
        except Exception as e:
            # If anything goes wrong, return None
            return None

    def refresh(self):
        """Refresh both the map location and weather overlay"""
        self.update_map()
        self.update_weather_overlay()

    def cleanup(self):
        """Clean up resources when the map is closed"""
        if self.map_view:
            self.map_view.destroy()