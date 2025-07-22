from flask import Flask, send_file
import requests
from io import BytesIO
from PIL import Image, ImageEnhance
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

weatherdb_api_key = os.getenv("weatherdb_api_key")
weatherdb_base_url = os.getenv("weatherdb_base_url")
weatherdb_tile_url = os.getenv("weatherdb_tile_url")

OSM_BASE_TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"

HEADERS = {
    "User-Agent": "MyWeatherApp/1.0 (contact@example.com)"
}

@app.route('/tiles/<layer>/<int:z>/<int:x>/<int:y>.png')
def serve_tile(layer, z, x, y):
    try:
        # Fetch base tile
        osm_url = OSM_BASE_TILE_URL.format(z=z, x=x, y=y)
        base_resp = requests.get(osm_url, headers=HEADERS)
        if base_resp.status_code != 200:
            app.logger.error(f"Failed to fetch OSM base tile {osm_url}: {base_resp.status_code}")
            return "Base tile not found", 404
        base_img = Image.open(BytesIO(base_resp.content)).convert("RGBA")

        # Fetch overlay tile
        overlay_url = f"{weatherdb_tile_url}/{layer}/{z}/{x}/{y}.png?appid={weatherdb_api_key}"
        overlay_resp = requests.get(overlay_url, headers=HEADERS)
        if overlay_resp.status_code != 200:
            output = BytesIO()
            base_img.save(output, format="PNG")
            output.seek(0)
            return send_file(output, mimetype='image/png')

        # Make the overlay MUCH DARKER (2+ shades darker as requested)
        overlay_img = Image.open(BytesIO(overlay_resp.content)).convert("RGBA")
        
        # Apply much stronger darkening - 2+ shades darker
        enhancer = ImageEnhance.Brightness(overlay_img)
        much_darker_overlay = enhancer.enhance(0.3)  # Much darker than before (was 0.5, now 0.3)
        
        # Optional: Also reduce contrast slightly for better visibility
        contrast_enhancer = ImageEnhance.Contrast(much_darker_overlay)
        final_overlay = contrast_enhancer.enhance(0.8)  # Slightly reduce contrast

        # Composite overlay on top of base
        base_img.paste(final_overlay, (0, 0), final_overlay)

        # Return the combined image
        output = BytesIO()
        base_img.save(output, format="PNG")
        output.seek(0)
        return send_file(output, mimetype='image/png')

    except Exception as e:
        app.logger.error(f"Error merging tiles: {e}")
        return "Internal Server Error", 500

def start_tile_server(*args, **kwargs):
    app.run(host="127.0.0.1", port=5005, debug=False, use_reloader=False)

if __name__ == "__main__":
    start_tile_server()