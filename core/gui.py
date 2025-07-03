import customtkinter as ctk
from features.tomorrows_guess.display import create_tomorrow_guess_frame, update_tomorrow_guess_display
import threading

def build_gui(app):
    # Clear previous widgets (for theme toggling or fresh build)
    for widget in app.winfo_children():
        widget.destroy()

    # Create canvas + vertical scrollbar for scrolling all content
    canvas = ctk.CTkCanvas(app, bg=app.theme["bg"], highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(app, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame inside canvas to hold everything
    scrollable_frame = ctk.CTkFrame(canvas, fg_color=app.theme["bg"])
    window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Scroll region update when frame size changes
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Adjust inner frame width to canvas width
    def on_canvas_configure(event):
        canvas.itemconfig(window, width=event.width)
    canvas.bind("<Configure>", on_canvas_configure)

    row = 0

    # Features row: All your metric cards
    features_frame = ctk.CTkFrame(scrollable_frame, fg_color=app.theme["bg"])
    features_frame.grid(row=row, column=0, sticky="ew", pady=10, padx=10)

    features = [
        ("humidity", "💧", "Humidity"),
        ("wind", "💨", "Wind"),
        ("pressure", "🧭", "Pressure"),
        ("visibility", "👁️", "Visibility"),
        ("uv", "🕶️", "UV Index"),
        ("precipitation", "☔️", "Precipitation"),
    ]

    features_frame.grid_columnconfigure(tuple(range(len(features))), weight=1, uniform="metrics")
    app.metric_value_labels = {}

    for col, (key, icon, label_text) in enumerate(features):
        frame = ctk.CTkFrame(features_frame, fg_color=app.theme["text_bg"], corner_radius=8)
        frame.grid(row=0, column=col, padx=6, pady=5, sticky="nsew")

        label_title = ctk.CTkLabel(frame, text=label_text, text_color=app.theme["text_fg"], font=("Arial", 14))
        label_title.pack(pady=(5, 0))

        label_icon = ctk.CTkLabel(frame, text=icon, font=("Arial", 24), text_color=app.theme["text_fg"])
        label_icon.pack()

        value_label = ctk.CTkLabel(frame, text="--", text_color=app.theme["text_fg"], font=("Arial", 16))
        value_label.pack(pady=(0, 5))

        app.metric_value_labels[key] = value_label

    row += 1

    # Toggle Theme button
    theme_btn = ctk.CTkButton(
        scrollable_frame,
        text="Toggle Theme",
        command=app.toggle_theme,
        fg_color=app.theme["button_bg"],
        text_color=app.theme["button_fg"],
        width=120,
    )
    theme_btn.grid(row=row, column=0, pady=10)
    row += 1

    # City entry (use theme entry_bg to respond to theme changes)
    app.city_entry = ctk.CTkEntry(
        scrollable_frame,
        textvariable=app.city_var,
        font=("Arial", 24, "bold"),
        width=300,
        fg_color=app.theme["entry_bg"],
        border_width=0,
        justify="center",
        text_color=app.theme["fg"],
    )
    app.city_entry.grid(row=row, column=0, pady=(10, 20))
    app.city_entry.bind("<Return>", lambda e: app.update_weather())
    row += 1

    # Today's temperature label
    app.temp_label = ctk.CTkLabel(
        scrollable_frame,
        text="-- °C",
        font=("Arial", 32),
        text_color=app.theme["fg"],
        cursor="hand2",
    )
    app.temp_label.grid(row=row, column=0, pady=10)
    app.temp_label.bind("<Button-1>", lambda e: app.toggle_temp_unit())
    row += 1

    # Weather description
    app.desc_label = ctk.CTkLabel(
        scrollable_frame,
        text="",
        font=("Arial", 20),
        text_color=app.theme["fg"],
    )
    app.desc_label.grid(row=row, column=0, pady=5)
    row += 1

    # Last updated label
    app.update_label = ctk.CTkLabel(
        scrollable_frame,
        text="",
        font=("Arial", 14),
        text_color=app.theme["fg"],
    )
    app.update_label.grid(row=row, column=0, pady=5)
    row += 1

    # Weather icon
    app.icon_label = ctk.CTkLabel(scrollable_frame, text="", image=None)
    app.icon_label.grid(row=row, column=0, pady=5)
    row += 1

    # Tomorrow's prediction
    app.tomorrow_guess_frame = create_tomorrow_guess_frame(scrollable_frame, app.theme)
    app.tomorrow_guess_frame.grid(row=row, column=0, pady=15, sticky="ew")
    row += 1

    update_tomorrow_guess_display(app.tomorrow_guess_frame, "N/A", "N/A", "N/A")

    # Weather history display — make sure frame exists before update calls
    app.history_frame = ctk.CTkFrame(scrollable_frame, fg_color=app.theme["bg"])
    app.history_frame.grid(row=row, column=0, sticky="ew", pady=(10, 20), padx=10)
    row += 1

    scrollable_frame.grid_columnconfigure(0, weight=1)

    # THREAD-SAFE async update of tomorrow's prediction
    def update_tomorrow_async(city):
        from features.tomorrows_guess.predictor import get_tomorrows_prediction

        predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)

        def update_display():
            # Must update GUI elements in main thread
            update_tomorrow_guess_display(
                app.tomorrow_guess_frame,
                predicted_temp,
                confidence,
                accuracy,
            )

        app.after(0, update_display)

    # Start update in a separate thread passing city safely
    city = app.city_var.get()
    threading.Thread(target=update_tomorrow_async, args=(city,), daemon=True).start()
