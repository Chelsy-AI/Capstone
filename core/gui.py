"""
GUI Builder Module
==================

This module handles the complete GUI layout and widget creation for the Weather App.
It creates a scrollable interface with all the weather information displays,
controls, and interactive elements. The GUI is theme-aware and rebuilds
dynamically when themes are switched.

Key Features:
- Scrollable main interface for all content
- Weather metric cards with icons and values
- Theme toggle functionality
- City input with real-time updates
- Temperature display with unit conversion
- Weather icon display
- Tomorrow's weather prediction section
- Historical weather data display
- Thread-safe GUI updates

"""

import customtkinter as ctk
from features.tomorrows_guess.display import create_tomorrow_guess_frame, update_tomorrow_guess_display
import threading


def build_gui(app):
    """
    Build the complete GUI layout for the Weather App
    
    This function creates all the visual elements of the weather application,
    including the scrollable canvas, weather metric cards, input controls,
    and display areas. It's called both on app startup and when themes are
    switched to rebuild the interface with new styling.
            
    GUI Structure:
        - Scrollable canvas with vertical scrollbar
        - Weather metrics cards (humidity, wind, pressure, etc.)
        - Theme toggle button
        - City input field
        - Current temperature display
        - Weather description and last updated info
        - Weather icon display
        - Tomorrow's prediction section
        - Historical weather data section

    """
    # Clear previous widgets (essential for theme toggling or fresh build)
    for widget in app.winfo_children():
        widget.destroy()

    # Create main canvas with vertical scrollbar for scrolling all content
    # This allows the app to handle content that exceeds window height
    canvas = ctk.CTkCanvas(app, bg=app.theme["bg"], highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # Create vertical scrollbar and link it to the canvas
    scrollbar = ctk.CTkScrollbar(app, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure canvas to work with scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create scrollable frame inside canvas to hold all content
    scrollable_frame = ctk.CTkFrame(canvas, fg_color=app.theme["bg"])
    window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Configure scroll region update when frame size changes
    def on_frame_configure(event):
        """Update canvas scroll region when content size changes"""
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Adjust inner frame width to match canvas width (responsive design)
    def on_canvas_configure(event):
        """Adjust scrollable frame width when canvas is resized"""
        canvas.itemconfig(window, width=event.width)
    canvas.bind("<Configure>", on_canvas_configure)

    # Initialize row counter for grid layout
    row = 0

    # === WEATHER METRICS SECTION ===
    # Create frame to hold all weather metric cards
    features_frame = ctk.CTkFrame(scrollable_frame, fg_color=app.theme["bg"])
    features_frame.grid(row=row, column=0, sticky="ew", pady=10, padx=10)

    # Define all weather metrics with their icons and labels
    features = [
        ("humidity", "💧", "Humidity"),      # Water droplet for humidity
        ("wind", "💨", "Wind"),             # Wind symbol for wind speed
        ("pressure", "🧭", "Pressure"),     # Compass for atmospheric pressure
        ("visibility", "👁️", "Visibility"), # Eye for visibility distance
        ("uv", "🕶️", "UV Index"),          # Sunglasses for UV protection
        ("precipitation", "☔️", "Precipitation"),  # Rain for precipitation
    ]

    # Configure grid columns to have equal width (uniform sizing)
    features_frame.grid_columnconfigure(tuple(range(len(features))), weight=1, uniform="metrics")
    
    # Initialize dictionary to store metric value labels for updates
    app.metric_value_labels = {}

    # Create individual metric cards
    for col, (key, icon, label_text) in enumerate(features):
        # Create individual card frame for each metric
        frame = ctk.CTkFrame(features_frame, fg_color=app.theme["text_bg"], corner_radius=8)
        frame.grid(row=0, column=col, padx=6, pady=5, sticky="nsew")

        # Metric title label (e.g., "Humidity", "Wind Speed")
        label_title = ctk.CTkLabel(frame, text=label_text, text_color=app.theme["text_fg"], font=("Arial", 14))
        label_title.pack(pady=(5, 0))

        # Metric icon (emoji representing the weather aspect)
        label_icon = ctk.CTkLabel(frame, text=icon, font=("Arial", 24), text_color=app.theme["text_fg"])
        label_icon.pack()

        # Metric value label (will be updated with actual values)
        value_label = ctk.CTkLabel(frame, text="--", text_color=app.theme["text_fg"], font=("Arial", 16))
        value_label.pack(pady=(0, 5))

        # Store reference to value label for later updates
        app.metric_value_labels[key] = value_label

    row += 1

    # === THEME TOGGLE BUTTON ===
    # Button to switch between light and dark themes
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

    # === CITY INPUT SECTION ===
    # Entry field for city name input with theme-aware styling
    app.city_entry = ctk.CTkEntry(
        scrollable_frame,
        textvariable=app.city_var,    # Linked to app's city variable
        font=("Arial", 24, "bold"),   # Large, bold font for prominence
        width=300,
        fg_color=app.theme["entry_bg"],  # Theme-aware background
        border_width=0,               # Clean, borderless design
        justify="center",             # Center-aligned text
        text_color=app.theme["fg"],   # Theme-aware text color
    )
    app.city_entry.grid(row=row, column=0, pady=(10, 20))
    
    # Bind Enter key to trigger weather update
    app.city_entry.bind("<Return>", lambda e: app.update_weather())
    row += 1

    # === CURRENT TEMPERATURE DISPLAY ===
    # Large temperature display with click-to-toggle unit functionality
    app.temp_label = ctk.CTkLabel(
        scrollable_frame,
        text="-- °C",                 # Default placeholder text
        font=("Arial", 32),           # Large font for main temperature
        text_color=app.theme["fg"],   # Theme-aware text color
        cursor="hand2",               # Hand cursor to indicate clickability
    )
    app.temp_label.grid(row=row, column=0, pady=10)
    
    # Bind click event to toggle temperature unit (Celsius/Fahrenheit)
    app.temp_label.bind("<Button-1>", lambda e: app.toggle_temp_unit())
    row += 1

    # === WEATHER DESCRIPTION ===
    # Display current weather conditions (e.g., "Clear sky", "Light rain")
    app.desc_label = ctk.CTkLabel(
        scrollable_frame,
        text="",                      # Initially empty, filled by API
        font=("Arial", 20),           # Medium font for description
        text_color=app.theme["fg"],   # Theme-aware text color
    )
    app.desc_label.grid(row=row, column=0, pady=5)
    row += 1

    # === LAST UPDATED TIMESTAMP ===
    # Show when the weather data was last refreshed
    app.update_label = ctk.CTkLabel(
        scrollable_frame,
        text="",                      # Initially empty, filled with timestamp
        font=("Arial", 14),           # Small font for meta information
        text_color=app.theme["fg"],   # Theme-aware text color
    )
    app.update_label.grid(row=row, column=0, pady=5)
    row += 1

    # === WEATHER ICON DISPLAY ===
    # Visual representation of current weather conditions
    app.icon_label = ctk.CTkLabel(scrollable_frame, text="", image=None)
    app.icon_label.grid(row=row, column=0, pady=5)
    row += 1

    # === TOMORROW'S PREDICTION SECTION ===
    # Create frame for tomorrow's weather prediction feature
    app.tomorrow_guess_frame = create_tomorrow_guess_frame(scrollable_frame, app.theme)
    app.tomorrow_guess_frame.grid(row=row, column=0, pady=15, sticky="ew")
    row += 1

    # Initialize tomorrow's prediction display with placeholder values
    update_tomorrow_guess_display(app.tomorrow_guess_frame, "N/A", "N/A", "N/A")

    # === WEATHER HISTORY SECTION ===
    # Create frame for historical weather data display
    # Important: Create frame before any update calls to avoid reference errors
    app.history_frame = ctk.CTkFrame(scrollable_frame, fg_color=app.theme["bg"])
    app.history_frame.grid(row=row, column=0, sticky="ew", pady=(10, 20), padx=10)
    row += 1

    # Configure main column to expand and fill available space
    scrollable_frame.grid_columnconfigure(0, weight=1)

    # === THREAD-SAFE TOMORROW'S PREDICTION UPDATE ===
    def update_tomorrow_async(city):
        """
        Update tomorrow's prediction in a background thread
        
        This function safely updates the tomorrow's prediction display
        by fetching data in a background thread and updating the GUI
        on the main thread to prevent freezing.
        
        """
        # Import here to avoid circular imports
        from features.tomorrows_guess.predictor import get_tomorrows_prediction

        # Fetch prediction data in background thread
        predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)

        def update_display():
            """Update GUI elements on main thread (thread-safe)"""
            update_tomorrow_guess_display(
                app.tomorrow_guess_frame,
                predicted_temp,
                confidence,
                accuracy,
            )

        # Schedule GUI update on main thread
        app.after(0, update_display)

    # Start prediction update in a separate thread with current city
    city = app.city_var.get()
    threading.Thread(target=update_tomorrow_async, args=(city,), daemon=True).start()
