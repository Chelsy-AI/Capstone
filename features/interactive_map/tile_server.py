from flask import Flask, send_file
import requests
from io import BytesIO
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env from current working directory

app = Flask(__name__)

weatherdb_api_key = os.getenv("weatherdb_api_key")
weatherdb_base_url = os.getenv("weatherdb_base_url")
weatherdb_tile_url = os.getenv("weatherdb_tile_url")  # ✅ Load the tile URL properly

OSM_BASE_TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"

HEADERS = {
    "User-Agent": "MyWeatherApp/1.0 (contact@example.com)"
}

@app.route('/tiles/<layer>/<int:z>/<int:x>/<int:y>.png')
def serve_tile(layer, z, x, y):
    try:
        osm_url = OSM_BASE_TILE_URL.format(z=z, x=x, y=y)
        base_resp = requests.get(osm_url, headers=HEADERS)
        if base_resp.status_code != 200:
            app.logger.error(f"Failed to fetch OSM base tile {osm_url}: {base_resp.status_code}")
            return "Base tile not found", 404
        base_img = Image.open(BytesIO(base_resp.content)).convert("RGBA")

        # ✅ FIXED: use tile URL instead of base weather API
        overlay_url = f"{weatherdb_tile_url}/{layer}/{z}/{x}/{y}.png?appid={weatherdb_api_key}"
        overlay_resp = requests.get(overlay_url, headers=HEADERS)
        if overlay_resp.status_code != 200:
            output = BytesIO()
            base_img.save(output, format="PNG")
            output.seek(0)
            return send_file(output, mimetype='image/png')

        overlay_img = Image.open(BytesIO(overlay_resp.content)).convert("RGBA")
        base_img.paste(overlay_img, (0, 0), overlay_img)

        output = BytesIO()
        base_img.save(output, format="PNG")
        output.seek(0)
        return send_file(output, mimetype='image/png')

    except Exception as e:
        app.logger.error(f"Error merging tiles: {e}")
        return "Internal Server Error", 500

def start_tile_server(*args, **kwargs):
    print("[TileServer] Starting tile server on http://127.0.0.1:5005")
    app.run(host="127.0.0.1", port=5005, debug=False, use_reloader=False)

if __name__ == "__main__":
    start_tile_server()
