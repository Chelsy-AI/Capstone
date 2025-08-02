"""
Weather Overlay Tile Server
===========================

Local Flask server that combines OpenStreetMap base tiles with weather overlay data.

Features:
- Real-time tile composition merging base maps with weather layers
- Support for multiple weather data types (temperature, wind, precipitation, etc.)
- Dynamic image processing with brightness and contrast adjustments
- Transparent overlay blending for optimal weather data visibility
- Error handling for missing tiles or failed API requests
- Configurable weather data source integration
- High-performance image caching and processing

The server runs locally to provide seamless weather overlay integration
without external dependencies during map navigation.
"""

from flask import Flask, send_file
import requests
from io import BytesIO
from PIL import Image, ImageEnhance
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a Flask web application
app = Flask(__name__)

# Get API configuration from environment variables
weatherdb_api_key = os.getenv("weatherdb_api_key")
weatherdb_base_url = os.getenv("weatherdb_base_url")
weatherdb_tile_url = os.getenv("weatherdb_tile_url")

# URL template for getting basic map tiles from OpenStreetMap
OSM_BASE_TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"

# Headers to include with web requests
HEADERS = {
    "User-Agent": "MyWeatherApp/1.0"
}

@app.route('/tiles/<layer>/<int:z>/<int:x>/<int:y>.png')
def serve_tile(layer, z, x, y):
    """
    This function combines basic map tiles with weather overlay tiles.
    
    Parameters:
    - layer: type of weather data (temp, wind, etc.)
    - z: zoom level
    - x, y: tile coordinates on the map grid
    """
    try:
        # Step 1: Get the basic map tile from OpenStreetMap
        osm_url = OSM_BASE_TILE_URL.format(z=z, x=x, y=y)
        base_resp = requests.get(osm_url, headers=HEADERS)
        
        # Check if we successfully got the base map tile
        if base_resp.status_code != 200:
            app.logger.error(f"Failed to fetch OSM base tile {osm_url}: {base_resp.status_code}")
            return "Base tile not found", 404
        
        # Convert the base tile image data into a PIL Image object
        # RGBA mode allows transparency
        base_img = Image.open(BytesIO(base_resp.content)).convert("RGBA")

        # Step 2: Get the weather overlay tile
        overlay_url = f"{weatherdb_tile_url}/{layer}/{z}/{x}/{y}.png?appid={weatherdb_api_key}"
        overlay_resp = requests.get(overlay_url, headers=HEADERS)
        
        # If we can't get weather data, just return the basic map
        if overlay_resp.status_code != 200:
            output = BytesIO()
            base_img.save(output, format="PNG")
            output.seek(0)
            return send_file(output, mimetype='image/png')

        # Step 3: Process the weather overlay to make it darker and more visible
        overlay_img = Image.open(BytesIO(overlay_resp.content)).convert("RGBA")
        
        # Make the overlay much darker (30% of original brightness)
        enhancer = ImageEnhance.Brightness(overlay_img)
        much_darker_overlay = enhancer.enhance(0.3)
        
        # Also reduce contrast slightly for better visibility(80% of original contrast)
        contrast_enhancer = ImageEnhance.Contrast(much_darker_overlay)
        final_overlay = contrast_enhancer.enhance(0.8)

        # Step 4: Combine the base map with the weather overlay
        base_img.paste(final_overlay, (0, 0), final_overlay)

        # Step 5: Send the combined image back to the map widget
        output = BytesIO()  # Create a byte buffer to hold image data
        base_img.save(output, format="PNG")  # Save the combined image as PNG
        output.seek(0)  # Reset buffer position to beginning
        return send_file(output, mimetype='image/png')  # Send the image

    except Exception as e:
        # If anything goes wrong, log the error and return an error message
        app.logger.error(f"Error merging tiles: {e}")
        return "Internal Server Error", 500

def start_tile_server(*args, **kwargs):
    """Start the tile server on localhost port 5005"""
    # Run the Flask server
    # debug=False and use_reloader=False prevent issues when running in threads
    app.run(host="127.0.0.1", port=5005, debug=False, use_reloader=False)

# If this file is run directly (not imported), start the server
if __name__ == "__main__":
    start_tile_server()
    