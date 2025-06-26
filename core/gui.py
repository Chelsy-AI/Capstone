import customtkinter as ctk
from PIL import Image, ImageTk

def build_gui(app):
    for widget in app.root.winfo_children():
        widget.destroy()

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    ctk.CTkLabel(app.root, text="Label", text_color=app.theme["fg"], fg_color="transparent")
    ctk.CTkEntry(app.root, text_color=app.theme["fg"], fg_color=app.theme["entry_bg"])
    ctk.CTkButton(app.root, text="Search", fg_color=app.theme["button_bg"], text_color=app.theme["fg"])

    app.root.configure(fg_color=app.theme["bg"])

    # Toggle Theme Button
    theme_btn = ctk.CTkButton(
        master=app.root,
        text="Toggle Theme",
        command=app.toggle_theme,
        fg_color=app.theme["button_bg"],
        text_color=app.theme["button_fg"],
        width=120
    )
    theme_btn.pack(pady=10)

    # City Entry
    app.city_entry = ctk.CTkEntry(
        master=app.root,
        textvariable=app.city_var,
        font=("Arial", 24, "bold"),
        width=300,
        fg_color="transparent",
        border_width=0,
        justify="center",
        text_color=app.theme["fg"]
    )
    app.city_entry.pack(pady=(10, 20))
    app.city_entry.bind("<Return>", lambda e: app.fetch_and_display())

    # Weather Icon Label
    app.icon_label = ctk.CTkLabel(app.root, text="", image=None)
    app.icon_label.configure(text="")  # Ensure no default text shows
    app.icon_label.pack(pady=5)

    # Initialize rotation angle and image if not present
    if not hasattr(app, "icon_rotation_angle"):
        app.icon_rotation_angle = 0
    if not hasattr(app, "weather_icon_img_original"):
        # Placeholder transparent 64x64 PNG if no icon loaded yet
        app.weather_icon_img_original = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    
    app.humidity_label = ctk.CTkLabel(
        parent_frame,
        text="Humidity",
        text_color=app.theme["text_fg"],
        fg_color=app.theme["text_bg"]
    )
    app.humidity_label.pack()  # or .grid(...)

    app.wind_label = ctk.CTkLabel(
        parent_frame,
        text="Wind Speed",
        text_color=app.theme["text_fg"],
        fg_color=app.theme["text_bg"]
    )
    app.wind_label.pack()

    app.pressure_label = ctk.CTkLabel(
        parent_frame,
        text="Pressure",
        text_color=app.theme["text_fg"],
        fg_color=app.theme["text_bg"]
    )
    app.pressure_label.pack()

    app.visibility_label = ctk.CTkLabel(
        parent_frame,
        text="Visibility",
        text_color=app.theme["text_fg"],
        fg_color=app.theme["text_bg"]
    )
    app.visibility_label.pack()

    app.uv_label = ctk.CTkLabel(
        parent_frame,
        text="UV Index",
        text_color=app.theme["text_fg"],
        fg_color=app.theme["text_bg"]
    )
    app.uv_label.pack()

    app.pollen_label = ctk.CTkLabel(
        parent_frame,
        text="Pollen Count",
        text_color=app.theme["text_fg"],
        fg_color=app.theme["text_bg"]
    )
    app.pollen_label.pack()

    app.bug_label = ctk.CTkLabel(
        parent_frame,
        text="Bug Index",
        text_color=app.theme["text_fg"],
        fg_color=app.theme["text_bg"]
    )
    app.bug_label.pack()

    app.precipitation_label = ctk.CTkLabel(
        parent_frame,
        text="Precipitation",
        text_color=app.theme["text_fg"],
        fg_color=app.theme["text_bg"]
    )
    app.precipitation.pack()

    app.icon_label = ctk.CTkLabel(app.root, text="")
    app.icon_label.pack()


    def rotate_icon():
        rotated = app.weather_icon_img_original.rotate(app.icon_rotation_angle)
        app.weather_icon_img = ImageTk.PhotoImage(rotated)
        app.icon_label.configure(image=app.weather_icon_img)
        app.icon_rotation_angle = (app.icon_rotation_angle + 10) % 360
        app.root.after(100, rotate_icon)

    rotate_icon()

    # Temperature Label
    app.temp_label = ctk.CTkLabel(
        master=app.root,
        text="",
        font=("Arial", 32),
        text_color=app.theme["fg"],
        cursor="hand2"
    )
    app.temp_label.pack(pady=5)

    app.temp_label.bind("<Button-1>", lambda e: toggle_unit(app))

    # Description Label
    app.desc_label = ctk.CTkLabel(
        master=app.root,
        text="",
        font=("Arial", 20),
        text_color=app.theme["fg"]
    )
    app.desc_label.pack(pady=5)

    # Last Update Label
    app.update_label = ctk.CTkLabel(
        master=app.root,
        text="",
        font=("Arial", 14),
        text_color=app.theme["fg"]
    )
    app.update_label.pack(pady=5)

    # History Textbox
    app.history_text = ctk.CTkTextbox(
        master=app.root,
        height=150,
        width=500,
        fg_color=app.theme["text_bg"],
        text_color=app.theme["text_fg"]
    )
    app.history_text.pack(pady=10)

    # Show History Button
    history_btn = ctk.CTkButton(
        master=app.root,
        text="Show History",
        command=app.show_weather_history,
        fg_color=app.theme["button_bg"],
        text_color=app.theme["button_fg"],
        width=120
    )
    history_btn.pack(pady=10)

    # Initial fetch & display
    app.fetch_and_display()

def toggle_unit(app):
    app.unit = "F" if app.unit == "C" else "C"
    app.fetch_and_display()
