"""
Weather Overlay Tile Server - Fixed Version
==========================================

Fixed version with better error handling and fallback functionality.
"""

import sys
import os
from io import BytesIO

# Try to import Flask and PIL, handle gracefully if not available
try:
    from flask import Flask, send_file
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    print("Warning: Flask not installed. Weather overlays will not be available.")

try:
    from PIL import Image, ImageEnhance
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Warning: Pillow not installed. Image processing will not be available.")

import requests

# Create Flask app only if Flask is available
if HAS_FLASK:
    app = Flask(__name__)

    # Configuration - use provided API key or environment variables
    weatherdb_api_key = None
    weatherdb_base_url = "https://api.openweathermap.org"
    weatherdb_tile_url = "https://tile.openweathermap.org/map"

    # OpenStreetMap tile URL
    OSM_BASE_TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"

    HEADERS = {
        "User-Agent": "MyWeatherApp/1.0"
    }

    @app.route('/tiles/<layer>/<int:z>/<int:x>/<int:y>.png')
    def serve_tile(layer, z, x, y):
        """Serve combined map and weather tiles"""
        try:
            # Get base map tile
            osm_url = OSM_BASE_TILE_URL.format(z=z, x=x, y=y)
            base_resp = requests.get(osm_url, headers=HEADERS, timeout=10)
            
            if base_resp.status_code != 200:
                app.logger.error(f"Failed to fetch OSM base tile: {base_resp.status_code}")
                return "Base tile not found", 404
            
            # If PIL is not available, just return base tile
            if not HAS_PIL:
                return send_file(BytesIO(base_resp.content), mimetype='image/png')
            
            # Convert to PIL Image
            base_img = Image.open(BytesIO(base_resp.content)).convert("RGBA")

            # Try to get weather overlay if API key is available
            if weatherdb_api_key and layer != "none":
                overlay_url = f"{weatherdb_tile_url}/{layer}/{z}/{x}/{y}.png?appid={weatherdb_api_key}"
                
                try:
                    overlay_resp = requests.get(overlay_url, headers=HEADERS, timeout=10)
                    
                    if overlay_resp.status_code == 200:
                        # Process overlay
                        overlay_img = Image.open(BytesIO(overlay_resp.content)).convert("RGBA")
                        
                        # Make overlay darker and blend
                        enhancer = ImageEnhance.Brightness(overlay_img)
                        darker_overlay = enhancer.enhance(0.3)
                        
                        contrast_enhancer = ImageEnhance.Contrast(darker_overlay)
                        final_overlay = contrast_enhancer.enhance(0.8)

                        # Combine images
                        base_img.paste(final_overlay, (0, 0), final_overlay)
                
                except Exception as e:
                    app.logger.error(f"Failed to get weather overlay: {e}")
                    # Continue with base image only

            # Return combined image
            output = BytesIO()
            base_img.save(output, format="PNG")
            output.seek(0)
            return send_file(output, mimetype='image/png')

        except Exception as e:
            app.logger.error(f"Error serving tile: {e}")
            return "Internal Server Error", 500

    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return {"status": "ok", "has_api_key": weatherdb_api_key is not None}

def start_tile_server(api_key=None, port=5005):
    """Start the tile server"""
    global weatherdb_api_key
    
    if not HAS_FLASK:
        print("Flask not available - tile server cannot start")
        return
    
    # Set API key
    weatherdb_api_key = api_key
    
    try:
        # Run Flask server
        app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False, threaded=True)
    except Exception as e:
        print(f"Failed to start tile server: {e}")

if __name__ == "__main__":
    # Get API key from environment or command line
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    start_tile_server(api_key)