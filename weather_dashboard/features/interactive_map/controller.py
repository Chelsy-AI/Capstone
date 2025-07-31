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
- Full translation support for all UI elements and messages

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
    def __init__(self, parent, get_city_callback, api_key, translation_manager, show_grid=True):
        # Store the callback function that tells us which city to show
        self.get_city_callback = get_city_callback
        # Store the API key for weather data
        self.api_key = api_key
        # Store translation manager for multilingual support
        self.tr = translation_manager
        # Store whether to show grid lines
        self.show_grid = show_grid

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
        self.overlay_label = ttk.Label(control_frame, text=self.tr("weather_overlay"))
        self.overlay_label.pack(side="left", padx=(0, 5))

        # Create dropdown menu for selecting weather overlays
        self.layer_var = tk.StringVar(value=self.tr("overlay_none"))  # Default to no overlay
        self.layer_dropdown = ttk.Combobox(control_frame, textvariable=self.layer_var, state="readonly", width=20)
        
        # Set available weather overlay options with translations
        self.overlay_mapping = {
            self.tr("overlay_none"): "none",
            self.tr("overlay_temperature"): "temp_new",
            self.tr("overlay_wind"): "wind_new",
            self.tr("overlay_precipitation"): "precipitation_new",
            self.tr("overlay_clouds"): "clouds_new",
            self.tr("overlay_pressure"): "pressure_new",
            self.tr("overlay_snow"): "snow_new",
            self.tr("overlay_dewpoint"): "dewpoint_new"
        }
        
        # Set dropdown values to translated overlay names
        self.layer_dropdown['values'] = list(self.overlay_mapping.keys())
        self.layer_dropdown.pack(side="left", padx=(0, 10))
        
        # When user selects a different overlay, update the map
        self.layer_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_weather_overlay())

        # Add a refresh button to update the map
        self.refresh_button = ttk.Button(control_frame, text=self.tr("refresh"), command=self.refresh)
        self.refresh_button.pack(side="left")

        # Create a container frame for the map widget
        self.map_container = tk.Frame(self.frame, bg='gray')
        self.map_container.pack(fill="both", expand=True)

        # Create the actual map widget
        self.map_view = TkinterMapView(self.map_container, width=600, height=350, corner_radius=0)
        self.map_view.place(x=0, y=0, relwidth=1, relheight=1)

        # Variable to store the current map marker (pin showing city location)
        self.marker = None

        # Status label for showing loading messages
        self.status_label = ttk.Label(self.frame, text="", foreground="blue")
        self.status_label.pack(pady=(5, 0))

        # Start our local tile server that combines map and weather data
        self.tile_server_port = 5005
        self.tile_server_url = f"http://localhost:{self.tile_server_port}"
        # Run the tile server in a separate thread so it doesn't block the GUI
        threading.Thread(target=start_tile_server, args=(self.api_key, self.tile_server_port), daemon=True).start()

        # Set up the basic map display
        self.setup_base_map()
        # Update the map to show the current city
        self.update_map()

    def setup_base_map(self):
        """Set up the basic map without any weather overlays"""
        self.show_status(self.tr("map_loading"))
        try:
            # Tell the map widget where to get basic map tiles from
            self.map_view.set_tile_server(self.base_tile_server, max_zoom=22)
            # Set the initial zoom level
            self.map_view.set_zoom(self.current_zoom)
            self.clear_status()
        except Exception as e:
            self.show_error(self.tr("map_loading_error"))

    def update_map(self):
        """Update the map to show the current selected city"""
        # Get the city name from the main application
        city = self.get_city_callback()
        if not city:
            return
            
        self.show_status(self.tr("geocoding_city"))
        
        # Convert city name to latitude/longitude coordinates
        coords = self.geocode_city(city)

        # If we successfully got coordinates
        if coords:
            self.show_status(self.tr("updating_location"))
            try:
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
                self.clear_status()
            except Exception as e:
                self.show_error(self.tr("map_loading_error"))
        else:
            self.show_error(self.tr("geocoding_failed"))

    def update_weather_overlay(self):
        """Change the weather overlay displayed on the map"""
        # Get the selected overlay type from the dropdown (translated name)
        selected_translated = self.layer_var.get()
        # Convert to internal layer name
        layer = self.overlay_mapping.get(selected_translated, "none")

        self.show_status(self.tr("overlay_loading"))
        
        try:
            # If "none" is selected, show just the basic map
            if layer == "none":
                self.map_view.set_tile_server(self.base_tile_server, max_zoom=22)
            else:
                # Build URL for our custom tile server that combines map + weather data
                composite_url = f"{self.tile_server_url}/tiles/{layer}/{{z}}/{{x}}/{{y}}.png"
                # Switch the map to use our custom tiles with weather overlay
                self.map_view.set_tile_server(composite_url, max_zoom=10)
            self.clear_status()
        except Exception as e:
            self.show_error(self.tr("overlay_loading_error"))

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
        except requests.RequestException:
            # Network error
            return None
        except (ValueError, KeyError, IndexError):
            # Data parsing error
            return None
        except Exception as e:
            # Any other error
            return None
        
        return None

    def refresh(self):
        """Refresh both the map location and weather overlay"""
        self.show_status(self.tr("refreshing_data"))
        try:
            self.update_map()
            self.update_weather_overlay()
            self.clear_status()
        except Exception as e:
            self.show_error(self.tr("map_refresh_failed"))

    def show_status(self, message):
        """Display a status message to the user"""
        self.status_label.config(text=message, foreground="blue")
        self.status_label.update()

    def show_error(self, message):
        """Display an error message to the user"""
        self.status_label.config(text=message, foreground="red")

    def clear_status(self):
        """Clear the status message"""
        self.status_label.config(text="")

    def update_language(self, translation_manager):
        """Update all UI elements when language changes"""
        self.tr = translation_manager
        
        # Update UI labels
        self.overlay_label.config(text=self.tr("weather_overlay"))
        self.refresh_button.config(text=self.tr("refresh"))
        
        # Store current selection before updating dropdown
        current_layer = self.overlay_mapping.get(self.layer_var.get(), "none")
        
        # Update overlay mapping with new translations
        self.overlay_mapping = {
            self.tr("overlay_none"): "none",
            self.tr("overlay_temperature"): "temp_new", 
            self.tr("overlay_wind"): "wind_new",
            self.tr("overlay_precipitation"): "precipitation_new",
            self.tr("overlay_clouds"): "clouds_new",
            self.tr("overlay_pressure"): "pressure_new",
            self.tr("overlay_snow"): "snow_new",
            self.tr("overlay_dewpoint"): "dewpoint_new"
        }
        
        # Update dropdown values
        self.layer_dropdown['values'] = list(self.overlay_mapping.keys())
        
        # Restore selection with new translation
        reverse_mapping = {v: k for k, v in self.overlay_mapping.items()}
        new_selection = reverse_mapping.get(current_layer, self.tr("overlay_none"))
        self.layer_var.set(new_selection)

    def get_current_overlay_info(self):
        """Get information about the currently selected overlay"""
        selected_translated = self.layer_var.get()
        layer = self.overlay_mapping.get(selected_translated, "none")
        
        if layer == "none":
            return {
                "name": self.tr("overlay_none"),
                "description": self.tr("no_overlay_selected"),
                "features": ""
            }
        elif layer == "temp_new":
            return {
                "name": self.tr("temperature_overlay_info"),
                "description": self.tr("temperature_overlay_desc"),
                "features": self.tr("temperature_overlay_features")
            }
        elif layer == "wind_new":
            return {
                "name": self.tr("wind_overlay_info"),
                "description": self.tr("wind_overlay_desc"),
                "features": self.tr("wind_overlay_features")
            }
        elif layer == "precipitation_new":
            return {
                "name": self.tr("precipitation_overlay_info"),
                "description": self.tr("precipitation_overlay_desc"),
                "features": self.tr("precipitation_overlay_features")
            }
        elif layer == "clouds_new":
            return {
                "name": self.tr("clouds_overlay_info"),
                "description": self.tr("clouds_overlay_desc"),
                "features": self.tr("clouds_overlay_features")
            }
        elif layer == "pressure_new":
            return {
                "name": self.tr("pressure_overlay_info"),
                "description": self.tr("pressure_overlay_desc"),
                "features": self.tr("pressure_overlay_features")
            }
        elif layer == "snow_new":
            return {
                "name": self.tr("snow_overlay_info"),
                "description": self.tr("snow_overlay_desc"),
                "features": self.tr("snow_overlay_features")
            }
        elif layer == "dewpoint_new":
            return {
                "name": self.tr("dewpoint_overlay_info"),
                "description": self.tr("dewpoint_overlay_desc"),
                "features": self.tr("dewpoint_overlay_features")
            }
        else:
            return {
                "name": self.tr("unknown"),
                "description": self.tr("no_description"),
                "features": ""
            }

    def cleanup(self):
        """Clean up resources when the map is closed"""
        if self.map_view:
            self.map_view.destroy()
            