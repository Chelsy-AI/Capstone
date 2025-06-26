import os
from customtkinter import CTkImage
from PIL import Image

ICON_PATH = os.path.join(os.path.dirname(__file__), "resources")

def load_icon(name, size=(32, 32)):
    icon_path = os.path.join("resources", "icons", f"{name}.png")
    if os.path.exists(icon_path):
        img = Image.open(icon_path).convert("RGBA")
        return CTkImage(img, size=size)
    return None
    # Example for humidity icon
    humidity_icon = load_icon("humidity")
    if humidity_icon:
        humidity_label = ctk.CTkLabel(master=app.root, image=humidity_icon)
        humidity_label.pack(side="left", padx=5)
