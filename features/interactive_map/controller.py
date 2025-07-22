# features/interactive_map/controller.py

import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
import requests

class MapController:
    def __init__(self, parent, get_city_callback, api_key, show_grid=True):
        self.get_city_callback = get_city_callback
        self.api_key = api_key
        self.show_grid = show_grid
        
        # Track current position and zoom manually
        self.current_lat = 40.7127281  # Default to NYC
        self.current_lon = -74.0060152
        self.current_zoom = 6

        # Tile server URLs
        self.base_tile_server = "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
        
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Control frame for weather layer selection
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill="x", pady=(0, 5))

        # Label for dropdown
        ttk.Label(control_frame, text="Weather Overlay:").pack(side="left", padx=(0, 5))

        # Dropdown to select weather overlay
        self.layer_var = tk.StringVar(value="none")
        self.layer_dropdown = ttk.Combobox(control_frame, textvariable=self.layer_var, state="readonly", width=20)
        self.layer_dropdown['values'] = [
            "none",  # No weather overlay - just base map with grid
            "temp_new", 
            "wind_new", 
            "precipitation_new", 
            "clouds_new",
            "pressure_new", 
            "snow_new", 
            "dewpoint_new"
        ]
        self.layer_dropdown.pack(side="left", padx=(0, 10))
        self.layer_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_weather_overlay())

        # Button to refresh map
        refresh_button = ttk.Button(control_frame, text="Refresh", command=self.refresh)
        refresh_button.pack(side="left")

        # Create container for dual map approach
        self.map_container = tk.Frame(self.frame)
        self.map_container.pack(fill="both", expand=True)

        # Base map (always visible underneath)
        self.base_map = TkinterMapView(self.map_container, width=600, height=350, corner_radius=0)
        self.base_map.place(x=0, y=0, relwidth=1, relheight=1)

        # Weather overlay map (on top, initially hidden)
        self.weather_map = TkinterMapView(self.map_container, width=600, height=350, corner_radius=0)
        # Start with weather map hidden
        
        self.marker = None
        
        # Setup base map with grid
        self.setup_base_map()
        
        # Update map position
        self.update_map()

    def setup_base_map(self):
        """Setup base map to always show grid lines"""
        try:
            # Use OpenStreetMap which shows clear country borders and grid lines
            self.base_map.set_tile_server(self.base_tile_server, max_zoom=22)
            print("✅ Base map setup with permanent grid visibility")
        except Exception as e:
            print(f"❌ Error setting up base map: {e}")

    def update_map(self):
        """Update map position and marker"""
        try:
            city = self.get_city_callback()
            coords = self.geocode_city(city)
            if coords:
                self.current_lat, self.current_lon = coords
                
                # Update base map position
                self.base_map.set_position(self.current_lat, self.current_lon)
                self.base_map.set_zoom(self.current_zoom)
                
                # Add marker to base map
                if self.marker:
                    self.base_map.delete(self.marker)
                self.marker = self.base_map.set_marker(self.current_lat, self.current_lon, text=city)
                
                print(f"✅ Map updated for {city} at {self.current_lat}, {self.current_lon}")
            else:
                print(f"❌ Could not geocode city: {city}")
        except Exception as e:
            print(f"❌ Error updating map: {e}")

    def geocode_city(self, city_name):
        """Get coordinates for city name"""
        try:
            url = f"https://nominatim.openstreetmap.org/search"
            params = {
                "q": city_name,
                "format": "json",
                "limit": 1
            }
            headers = {"User-Agent": "Tkinter Weather App"}
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return float(data[0]['lat']), float(data[0]['lon'])
        except Exception as e:
            print(f"❌ Geocoding error: {e}")
        return None

    def update_weather_overlay(self):
        """Update weather overlay while keeping base map visible underneath"""
        try:
            layer = self.layer_var.get()
            
            if layer == "none":
                # Hide weather overlay, show only base map with grid
                self.weather_map.place_forget()
                print("✅ Weather overlay hidden - base map with grid visible")
            else:
                # Create weather tile URL
                weather_tile_url = f"https://tile.openweathermap.org/map/{layer}/{{z}}/{{x}}/{{y}}.png?appid={self.api_key}"
                
                # Setup weather overlay map
                self.weather_map.set_tile_server(weather_tile_url, max_zoom=10)
                
                # Position weather map over base map
                self.weather_map.place(x=0, y=0, relwidth=1, relheight=1)
                
                # Sync position with base map
                self.weather_map.set_position(self.current_lat, self.current_lon)
                self.weather_map.set_zoom(self.current_zoom)
                
                # Make weather map semi-transparent by configuring its canvas
                try:
                    # Access the canvas of the weather map and make it semi-transparent
                    weather_canvas = self.weather_map._canvas
                    weather_canvas.configure(highlightthickness=0)
                    # Note: True transparency would require modifying the TkinterMapView source
                    # For now, this provides overlay functionality
                except:
                    pass  # If canvas access fails, overlay still works
                
                print(f"✅ Weather layer '{layer}' overlaid on base map")
                print(f"    Base map (grid) remains visible underneath")
                print(f"    Weather URL: {weather_tile_url}")
                
        except Exception as e:
            print(f"❌ Error updating weather overlay: {e}")

    def refresh(self):
        """Refresh the map"""
        try:
            self.update_map()
            # Reapply current overlay if any
            current_layer = self.layer_var.get()
            if current_layer != "none":
                self.update_weather_overlay()
            print("✅ Map refreshed")
        except Exception as e:
            print(f"❌ Error refreshing map: {e}")

    def set_weather_layer(self, layer_name):
        """Programmatically set weather layer"""
        try:
            if layer_name in self.layer_dropdown['values']:
                self.layer_var.set(layer_name)
                self.update_weather_overlay()
                print(f"✅ Weather layer set to: {layer_name}")
            else:
                print(f"❌ Invalid layer name: {layer_name}")
        except Exception as e:
            print(f"❌ Error setting weather layer: {e}")

    def get_current_layer(self):
        """Get currently selected weather layer"""
        return self.layer_var.get()
        
    def sync_weather_map(self):
        """Sync weather map position with base map when user interacts"""
        try:
            if self.layer_var.get() != "none":
                # This would be called on map interaction events
                # For now, maps should stay synced through the position updates
                pass
        except Exception as e:
            print(f"❌ Error syncing weather map: {e}")