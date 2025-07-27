from tkintermapview import TkinterMapView

class MapDisplay:
    def __init__(self, parent):
        # Create the map widget with specific size and rounded corners
        self.map_widget = TkinterMapView(parent, width=600, height=300, corner_radius=10)
        # Add the map widget to the parent window with some padding
        self.map_widget.pack(pady=10)
        
        # Variable to store the current location marker (pin on the map)
        self.marker = None
        
        # Set New York as the default location when the map first loads
        self.set_location("New York")

    def set_location(self, city_name):
        """Update the map to show a new city location"""
        # If no city name is provided, don't do anything
        if not city_name:
            return

        # Move the map to show the specified city
        self.map_widget.set_address(city_name)

        # Remove the old marker if one exists
        if self.marker:
            self.map_widget.delete(self.marker)

        # Add a new marker at the city location
        self.marker = self.map_widget.set_address(city_name, marker=True)
        