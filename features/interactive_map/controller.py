import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
import requests
import os
import threading

# Local composite tile server
from .tile_server import start_tile_server

class MapController:
    def __init__(self, parent, get_city_callback, api_key, show_grid=True):
        self.get_city_callback = get_city_callback
        self.api_key = api_key
        self.show_grid = show_grid

        self.current_lat = 40.7127281
        self.current_lon = -74.0060152
        self.current_zoom = 6

        self.base_tile_server = "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
        self.composite_tile_url = None

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill="x", pady=(0, 5))

        ttk.Label(control_frame, text="Weather Overlay:").pack(side="left", padx=(0, 5))

        self.layer_var = tk.StringVar(value="none")
        self.layer_dropdown = ttk.Combobox(control_frame, textvariable=self.layer_var, state="readonly", width=20)
        self.layer_dropdown['values'] = [
            "none", "temp_new", "wind_new", "precipitation_new", 
            "clouds_new", "pressure_new", "snow_new", "dewpoint_new"
        ]
        self.layer_dropdown.pack(side="left", padx=(0, 10))
        self.layer_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_weather_overlay())

        refresh_button = ttk.Button(control_frame, text="Refresh", command=self.refresh)
        refresh_button.pack(side="left")

        self.map_container = tk.Frame(self.frame, bg='gray')
        self.map_container.pack(fill="both", expand=True)

        self.map_view = TkinterMapView(self.map_container, width=600, height=350, corner_radius=0)
        self.map_view.place(x=0, y=0, relwidth=1, relheight=1)

        self.marker = None

        # Start tile server
        self.tile_server_port = 5005
        self.tile_server_url = f"http://localhost:{self.tile_server_port}"
        threading.Thread(target=start_tile_server, args=(self.api_key, self.tile_server_port), daemon=True).start()

        self.setup_base_map()
        self.update_map()

    def setup_base_map(self):
        self.map_view.set_tile_server(self.base_tile_server, max_zoom=22)
        self.map_view.set_zoom(self.current_zoom)

    def update_map(self):
        city = self.get_city_callback()
        coords = self.geocode_city(city)

        if coords:
            self.current_lat, self.current_lon = coords
            self.map_view.set_position(self.current_lat, self.current_lon)
            self.map_view.set_zoom(self.current_zoom)

            if self.marker:
                self.map_view.delete(self.marker)
            self.marker = self.map_view.set_marker(self.current_lat, self.current_lon, text=city)

    def update_weather_overlay(self):
        layer = self.layer_var.get()

        if layer == "none":
            self.map_view.set_tile_server(self.base_tile_server, max_zoom=22)
        else:
            composite_url = f"{self.tile_server_url}/tiles/{layer}/{{z}}/{{x}}/{{y}}.png"
            self.map_view.set_tile_server(composite_url, max_zoom=10)

    def geocode_city(self, city_name):
        try:
            url = f"https://nominatim.openstreetmap.org/search"
            params = {"q": city_name, "format": "json", "limit": 1}
            headers = {"User-Agent": "Tkinter Weather App 1.0"}

            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return lat, lon
        except Exception as e:
            return None

    def refresh(self):
        self.update_map()
        self.update_weather_overlay()

    def cleanup(self):
        if self.map_view:
            self.map_view.destroy()
