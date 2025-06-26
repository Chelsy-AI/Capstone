import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage

# ──────────────────────────────────────────────────────────────────────────────
# Creates a single feature box with a title, icon, and dynamic value label.
# Returns the frame and the label for updating the value later.
#
# Parameters:
# - parent: parent container where this box is placed
# - title: string title of the feature (e.g., "Hum")
# - icon_img: CTkImage instance to display
# - value: initial text value (e.g., "--%")
# - theme: dictionary of colors for styling
# ──────────────────────────────────────────────────────────────────────────────
def create_feature_box(parent, title, icon_img, value, theme):
    frame = ctk.CTkFrame(parent, fg_color=theme["entry_bg"], corner_radius=10, width=80, height=120)
    frame.grid_propagate(False)  # Prevent frame from resizing to contents

    label_title = ctk.CTkLabel(
        frame,
        text=title,
        text_color=theme["text_fg"],
        font=ctk.CTkFont(size=14, weight="bold")
    )
    label_title.grid(row=0, column=0, pady=(8, 2))

    label_icon = ctk.CTkLabel(frame, image=icon_img, text="")
    label_icon.grid(row=1, column=0, pady=2)

    label_value = ctk.CTkLabel(
        frame,
        text=value,
        text_color=theme["text_fg"],
        font=ctk.CTkFont(size=12)
    )
    label_value.grid(row=2, column=0, pady=(2, 8))

    return frame, label_value


# ──────────────────────────────────────────────────────────────────────────────
# Builds a horizontal row of feature boxes (humidity, wind, pressure).
# Should be called once during GUI setup.
# Loads icons from image files and creates feature boxes.
#
# Parameters:
# - app: main app object which holds root window and theme, and stores label references
# ──────────────────────────────────────────────────────────────────────────────
def build_feature_row(app):
    container = ctk.CTkFrame(app.root, fg_color="transparent")
    container.pack(pady=20)

    # TODO: Replace "path/to/..." with the correct paths to your local icon images.
    # Make sure these images exist and are accessible, or else handle missing images gracefully.
    hum_icon = CTkImage(Image.open("path/to/humidity.png").resize((32, 32)))
    wind_icon = CTkImage(Image.open("path/to/wind.png").resize((32, 32)))
    press_icon = CTkImage(Image.open("path/to/pressure.png").resize((32, 32)))

    # Create individual feature boxes and assign their value labels to the app object for updates
    hum_box, app.humidity_label = create_feature_box(container, "Hum", hum_icon, "--%", app.theme)
    wind_box, app.wind_label = create_feature_box(container, "Wind", wind_icon, "-- m/s", app.theme)
    press_box, app.pressure_label = create_feature_box(container, "Press", press_icon, "-- hPa", app.theme)

    # Arrange boxes horizontally with spacing
    hum_box.grid(row=0, column=0, padx=10)
    wind_box.grid(row=0, column=1, padx=10)
    press_box.grid(row=0, column=2, padx=10)
