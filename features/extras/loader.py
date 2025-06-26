import os
from customtkinter import CTkImage
from PIL import Image

# Base folder where your icons are stored (adjust as needed)
ICON_PATH = os.path.join(os.path.dirname(__file__), "resources", "icons")

def load_icon(name, size=(32, 32)):
    """
    Load an icon image by name from the resources/icons folder,
    resize it, and convert to CTkImage for use in CustomTkinter widgets.
    
    Args:
        name (str): Icon filename without extension (e.g. "humidity")
        size (tuple): Desired size (width, height)
    
    Returns:
        CTkImage or None: Loaded and resized icon image or None if not found
    """
    icon_path = os.path.join(ICON_PATH, f"{name}.png")
    if os.path.exists(icon_path):
        img = Image.open(icon_path).convert("RGBA")
        return CTkImage(img, size=size)
    else:
        print(f"Warning: Icon not found: {icon_path}")
        return None
