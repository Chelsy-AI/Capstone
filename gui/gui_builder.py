import customtkinter as ctk
import threading
from features.tomorrows_guess.display import create_tomorrow_guess_frame, update_tomorrow_guess_display


def build_gui(app):
    """
    Build GUI with transparent elements and theme-based text colors
    """

    # Destroy old widgets, but preserve the background canvas
    for widget in app.winfo_children():
        if widget != getattr(app, 'bg_canvas', None):
            widget.destroy()

    # Get theme-based colors
    text_color = app.get_text_color()
    value_color = app.get_value_color()

    # Create main scrollable frame - completely transparent
    main_frame = ctk.CTkScrollableFrame(
        app,
        fg_color="transparent",
        corner_radius=0,
        scrollbar_button_color="gray50",
        scrollbar_button_hover_color="gray30"
    )
    main_frame.place(x=0, y=0, relwidth=1, relheight=1)

    # Reset metric labels dictionary
    app.metric_value_labels = {}

    row = 0

    # Title - theme-based text color
    title_label = ctk.CTkLabel(
        main_frame,
        text="🌤️ Weather Dashboard",
        font=("Arial", 32, "bold"),
        text_color=text_color,
        fg_color="transparent"
    )
    title_label.grid(row=row, column=0, pady=(30, 20), padx=20)
    row += 1

    # City Entry - minimal transparent frame
    entry_frame = ctk.CTkFrame(
        main_frame, 
        fg_color="transparent",
        corner_radius=0
    )
    entry_frame.grid(row=row, column=0, pady=15, padx=20, sticky="ew")
    
    ctk.CTkLabel(
        entry_frame,
        text="🌍 Enter City:",
        font=("Arial", 18, "bold"),
        text_color=text_color,
        fg_color="transparent"
    ).pack(pady=(0, 5))

    app.city_entry = ctk.CTkEntry(
        entry_frame,
        textvariable=app.city_var,
        font=("Arial", 18),
        width=300,
        height=40,
        justify="center",
        fg_color="white",  # Keep entry visible
        text_color="black",
        corner_radius=15,
        border_width=2,
        border_color="lightblue"
    )
    app.city_entry.pack(pady=(0, 10))
    app.city_entry.bind("<Return>", lambda e: threading.Thread(target=app.safe_update_weather, daemon=True).start())
    row += 1

    # Temperature Display - theme-based text color
    app.temp_label = ctk.CTkLabel(
        main_frame,
        text="-- °C",
        font=("Arial", 56, "bold"),
        text_color=text_color,
        fg_color="transparent",
        cursor="hand2"
    )
    app.temp_label.grid(row=row, column=0, pady=20, padx=20)
    app.temp_label.bind("<Button-1>", app.toggle_temp_unit)
    row += 1

    # Weather Description - theme-based text color
    app.desc_label = ctk.CTkLabel(
        main_frame,
        text="Loading weather...",
        font=("Arial", 22, "italic"),
        text_color=text_color,
        fg_color="transparent"
    )
    app.desc_label.grid(row=row, column=0, pady=10, padx=20)
    row += 1

    # Weather Icon
    app.icon_label = ctk.CTkLabel(
        main_frame, 
        text="", 
        image=None,
        fg_color="transparent"
    )
    app.icon_label.grid(row=row, column=0, pady=10, padx=20)
    row += 1

    # Weather Metrics - theme-based text colors
    metrics_title = ctk.CTkLabel(
        main_frame,
        text="📊 Weather Details",
        font=("Arial", 24, "bold"),
        text_color=text_color,
        fg_color="transparent"
    )
    metrics_title.grid(row=row, column=0, pady=(20, 15), padx=20)
    row += 1

    # Metrics Grid - transparent frame
    metrics_grid = ctk.CTkFrame(main_frame, fg_color="transparent")
    metrics_grid.grid(row=row, column=0, pady=10, padx=20, sticky="ew")

    features = [
        ("humidity", "💧", "Humidity"),
        ("wind", "💨", "Wind"),
        ("pressure", "🧭", "Pressure"),
        ("visibility", "👁️", "Visibility"),
        ("uv", "🕶️", "UV Index"),
        ("precipitation", "☔", "Precipitation"),
    ]

    # Configure grid columns
    for i in range(3):
        metrics_grid.grid_columnconfigure(i, weight=1)

    # Create metric displays - theme-based text colors
    for idx, (key, icon, label) in enumerate(features):
        row_pos = idx // 3
        col_pos = idx % 3
        
        # Container for each metric - transparent
        metric_container = ctk.CTkFrame(
            metrics_grid,
            fg_color="transparent",
            corner_radius=0
        )
        metric_container.grid(row=row_pos, column=col_pos, padx=15, pady=10, sticky="nsew")
        
        # Icon
        ctk.CTkLabel(
            metric_container,
            text=icon,
            font=("Arial", 28),
            text_color=text_color,
            fg_color="transparent"
        ).pack(pady=(0, 5))
        
        # Label
        ctk.CTkLabel(
            metric_container,
            text=label,
            font=("Arial", 14, "bold"),
            text_color=text_color,
            fg_color="transparent"
        ).pack()
        
        # Value - special value color
        value_label = ctk.CTkLabel(
            metric_container,
            text="--",
            font=("Arial", 16, "bold"),
            text_color=value_color,
            fg_color="transparent"
        )
        value_label.pack(pady=(5, 0))
        
        app.metric_value_labels[key] = value_label

    row += 1

    # Tomorrow's Prediction - theme-based text color
    prediction_title = ctk.CTkLabel(
        main_frame,
        text="🔮 Tomorrow's Prediction",
        font=("Arial", 22, "bold"),
        text_color=text_color,
        fg_color="transparent"
    )
    prediction_title.grid(row=row, column=0, pady=(30, 10), padx=20)
    row += 1

    # Create a transparent frame for tomorrow's prediction
    try:
        prediction_container = ctk.CTkFrame(
            main_frame,
            fg_color="transparent",
            corner_radius=0
        )
        prediction_container.grid(row=row, column=0, pady=10, padx=20, sticky="ew")

        app.tomorrow_guess_frame = create_tomorrow_guess_frame(prediction_container, app.theme)
        app.tomorrow_guess_frame.pack(pady=10, padx=20, fill="x")
        update_tomorrow_guess_display(app.tomorrow_guess_frame, "N/A", "N/A", "N/A")
        
    except Exception as e:
        print(f"Error creating tomorrow's prediction frame: {e}")
        app.tomorrow_guess_frame = None

    row += 1

    # Weather History - theme-based text color
    history_title = ctk.CTkLabel(
        main_frame,
        text="📈 7-Day Weather History",
        font=("Arial", 22, "bold"),
        text_color=text_color,
        fg_color="transparent"
    )
    history_title.grid(row=row, column=0, pady=(30, 10), padx=20)
    row += 1

    app.history_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent",
        corner_radius=0
    )
    app.history_frame.grid(row=row, column=0, pady=10, padx=20, sticky="ew")
    row += 1

    # Last Updated - theme-based text color
    app.update_label = ctk.CTkLabel(
        main_frame,
        text="",
        font=("Arial", 14),
        text_color=text_color,
        fg_color="transparent"
    )
    app.update_label.grid(row=row, column=0, pady=15, padx=20)
    row += 1

    # Theme Toggle Button - keep this visible
    theme_btn = ctk.CTkButton(
        main_frame,
        text="🎨 Toggle Theme",
        command=app.toggle_theme,
        fg_color="darkblue",
        text_color="white",
        hover_color="blue",
        width=150,
        height=40,
        corner_radius=15,
        font=("Arial", 14, "bold")
    )
    theme_btn.grid(row=row, column=0, pady=20, padx=20)
    row += 1

    # Configure main frame column
    main_frame.grid_columnconfigure(0, weight=1)

    # Add bottom padding
    ctk.CTkLabel(
        main_frame, 
        text="", 
        height=50, 
        fg_color="transparent"
    ).grid(row=row, column=0)

    print(f"[GUI] Built transparent interface with theme-based colors: text={text_color}, values={value_color}")
    