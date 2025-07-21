# features/interactive_map/controller.py

import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
import requests

class MapController:
    def __init__(self, parent, get_city_callback, api_key):
        self.get_city_callback = get_city_callback
        self.api_key = api_key

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Dropdown to select weather layer
        self.layer_var = tk.StringVar(value="temp_new")
        self.layer_dropdown = ttk.Combobox(self.frame, textvariable=self.layer_var, state="readonly")
        self.layer_dropdown['values'] = [
            "temp_new", "wind_new", "precipitation_new", "clouds_new",
            "pressure_new", "snow_new", "dewpoint_new"
        ]
        self.layer_dropdown.pack(anchor="w")
        self.layer_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_tile_layer())

        # Map widget
        self.map_widget = TkinterMapView(self.frame, width=600, height=300, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)

        self.tile_server_template = (
        "https://tile.openweathermap.org/map/{layer}/{{z}}/{{x}}/{{y}}.png?appid={api_key}"
        )

        self.marker = None
        self.update_map()

    def update_map(self):
        city = self.get_city_callback()
        coords = self.geocode_city(city)
        if coords:
            lat, lon = coords
            self.map_widget.set_position(lat, lon)
            self.map_widget.set_zoom(6)
            if self.marker:
                self.map_widget.delete(self.marker)
            self.marker = self.map_widget.set_marker(lat, lon, text=city)
            self.update_tile_layer()

    def geocode_city(self, city_name):
        try:
            url = f"https://nominatim.openstreetmap.org/search"
            params = {
                "q": city_name,
                "format": "json",
                "limit": 1
            }
            headers = {"User-Agent": "Tkinter Weather App"}
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return float(data[0]['lat']), float(data[0]['lon'])
        except Exception as e:
            print(f"Geocoding error: {e}")
        return None

    def update_tile_layer(self):
        layer = self.layer_var.get()
        tile_url = self.tile_server_template.format(layer=layer, api_key=self.api_key)
        self.map_widget.set_tile_server(tile_url, max_zoom=10)

    def refresh(self):
        self.update_map()
