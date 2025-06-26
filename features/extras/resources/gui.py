import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage

def create_feature_box(parent, title, icon_img, value, theme):
    frame = ctk.CTkFrame(parent, fg_color=theme["entry_bg"], corner_radius=10, width=80, height=120)
    frame.grid_propagate(False)  # Fix size

    label_title = ctk.CTkLabel(frame, text=title, text_color=theme["text_fg"], font=ctk.CTkFont(size=14, weight="bold"))
    label_title.grid(row=0, column=0, pady=(8, 2))

    label_icon = ctk.CTkLabel(frame, image=icon_img, text="")
    label_icon.grid(row=1, column=0, pady=2)

    label_value = ctk.CTkLabel(frame, text=value, text_color=theme["text_fg"], font=ctk.CTkFont(size=12))
    label_value.grid(row=2, column=0, pady=(2, 8))

    return frame, label_value

def build_feature_row(app):
    container = ctk.CTkFrame(app.root, fg_color="transparent")
    container.pack(pady=20)

    # Example icons, replace with your actual image paths or CTkImage objects
    hum_icon = CTkImage(Image.open("path/to/humidity.png").resize((32, 32)))
    wind_icon = CTkImage(Image.open("path/to/wind.png").resize((32, 32)))
    press_icon = CTkImage(Image.open("path/to/pressure.png").resize((32, 32)))

    # Create feature boxes
    hum_box, app.humidity_label = create_feature_box(container, "Hum", hum_icon, "--%", app.theme)
    wind_box, app.wind_label = create_feature_box(container, "Wind", wind_icon, "-- m/s", app.theme)
    press_box, app.pressure_label = create_feature_box(container, "Press", press_icon, "-- hPa", app.theme)

    # Arrange horizontally with padding
    hum_box.grid(row=0, column=0, padx=10)
    wind_box.grid(row=0, column=1, padx=10)
    press_box.grid(row=0, column=2, padx=10)
