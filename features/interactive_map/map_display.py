from tkintermapview import TkinterMapView

class MapDisplay:
    def __init__(self, parent):
        self.map_widget = TkinterMapView(parent, width=600, height=300, corner_radius=10)
        self.map_widget.pack(pady=10)
        self.marker = None
        self.set_location("New York")  # default location

    def set_location(self, city_name):
        if not city_name:
            return

        self.map_widget.set_address(city_name)

        if self.marker:
            self.map_widget.delete(self.marker)

        self.marker = self.map_widget.set_address(city_name, marker=True)
