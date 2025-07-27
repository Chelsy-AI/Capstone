import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
import requests
import threading

from .tile_server import start_tile_server

class MapController:
    def __init__(self, parent, get_city_callback, api_key, show_grid=True):
        # Store the callback function that tells us which city to show
        self.get_city_callback = get_city_callback
        # Store the API key for weather data
        self.api_key = api_key
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
        ttk.Label(control_frame, text="Weather Overlay:").pack(side="left", padx=(0, 5))

        # Create dropdown menu for selecting weather overlays
        self.layer_var = tk.StringVar(value="none")  # Default to no overlay
        self.layer_dropdown = ttk.Combobox(control_frame, textvariable=self.layer_var, state="readonly", width=20)
        # Set available weather overlay options
        self.layer_dropdown['values'] = [
            "none", "temp_new", "wind_new", "precipitation_new", 
            "clouds_new", "pressure_new", "snow_new", "dewpoint_new"
        ]
        self.layer_dropdown.pack(side="left", padx=(0, 10))
        # When user selects a different overlay, update the map
        self.layer_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_weather_overlay())

        # Add a refresh button to update the map
        refresh_button = ttk.Button(control_frame, text="Refresh", command=self.refresh)
        refresh_button.pack(side="left")

        # Create a container frame for the map widget
        self.map_container = tk.Frame(self.frame, bg='gray')
        self.map_container.pack(fill="both", expand=True)

        # Create the actual map widget
        self.map_view = TkinterMapView(self.map_container, width=600, height=350, corner_radius=0)
        self.map_view.place(x=0, y=0, relwidth=1, relheight=1)

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
        # Get the selected overlay type from the dropdown
        layer = self.layer_var.get()

        # If "none" is selected, show just the basic map
        if layer == "none":
            self.map_view.set_tile_server(self.base_tile_server, max_zoom=22)
        else:
            # Build URL for our custom tile server that combines map + weather data
            composite_url = f"{self.tile_server_url}/tiles/{layer}/{{z}}/{{x}}/{{y}}.png"
            # Switch the map to use our custom tiles with weather overlay
            self.map_view.set_tile_server(composite_url, max_zoom=10)

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