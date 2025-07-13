import threading
import customtkinter as ctk
from .animation_gui import SmartBackground
from .gui_builder import build_gui

def setup_widgets_and_functions(app):
    row = 6  # continuing from last row in build_gui()

    # === THEME TOGGLE BUTTON ===
    def safe_toggle_theme():
        """Enhanced theme toggle with background integration"""
        try:
            if hasattr(app, 'toggle_theme'):
                app.toggle_theme()
            
            current_condition = getattr(app, 'current_weather_condition', 'clear')
            new_theme = app.smart_background.get_adaptive_theme(current_condition)
            app.theme.update(new_theme)
            app.smart_background.update_background(current_condition)
            
            # Optionally rebuild GUI
            # app.after(100, lambda: build_gui(app))
        except Exception as e:
            print(f"Theme toggle error: {e}")
    
    theme_btn = ctk.CTkButton(
        app.scrollable_frame,
        text="🎨 Smart Theme",
        command=safe_toggle_theme,
        fg_color=app.theme.get("button_bg", "#4169E1"),
        text_color=app.theme.get("button_fg", "#FFFFFF"),
        hover_color=app.theme.get("accent", "#6495ED"),
        width=160,
        height=45,
        corner_radius=22,
        font=("Arial", 13, "bold"),
        border_width=2,
        border_color=app.theme.get("accent", "#6495ED")
    )
    theme_btn.grid(row=row, column=0, pady=20)
    row += 1

    # === CITY INPUT SECTION ===
    input_frame = ctk.CTkFrame(app.scrollable_frame, fg_color="transparent")
    input_frame.grid(row=row, column=0, pady=15)
    
    app.city_entry = ctk.CTkEntry(
        input_frame,
        textvariable=app.city_var,
        font=("Arial", 26, "bold"),
        width=350,
        height=50,
        fg_color=app.theme.get("entry_bg", "#FFFFFF"),
        border_width=3,
        border_color=app.theme.get("accent", "#6495ED"),
        justify="center",
        text_color=app.theme.get("entry_fg", "#1A1A1A"),
        corner_radius=25,
        placeholder_text="Enter city name...",
        placeholder_text_color=app.theme.get("text_fg", "#1A1A1A")
    )
    app.city_entry.pack(pady=8)
    
    def safe_update_weather():
        try:
            if hasattr(app, 'update_weather'):
                app.update_weather()
            current_condition = getattr(app, 'current_weather_condition', 'clear')
            new_theme = app.smart_background.get_adaptive_theme(current_condition)
            app.theme.update(new_theme)
            app.smart_background.update_background(current_condition)
        except Exception as e:
            print(f"Weather update error: {e}")
    
    app.city_entry.bind("<Return>", lambda e: safe_update_weather())
    row += 1
    
    # === CURRENT TEMPERATURE DISPLAY ===
    temp_frame = ctk.CTkFrame(app.scrollable_frame, fg_color="transparent")
    temp_frame.grid(row=row, column=0, pady=20)
    
    app.temp_label = ctk.CTkLabel(
        temp_frame,
        text="-- °C",
        font=("Arial", 54, "bold"),
        text_color=app.theme.get("fg", "#1A1A1A"),
        cursor="hand2",
    )
    app.temp_label.pack()
    
    def safe_toggle_temp():
        try:
            if hasattr(app, 'toggle_temp_unit'):
                app.toggle_temp_unit()
        except Exception as e:
            print(f"Temperature toggle error: {e}")
    
    app.temp_label.bind("<Button-1>", lambda e: safe_toggle_temp())
    row += 1
    
    # === WEATHER DESCRIPTION ===
    app.desc_label = ctk.CTkLabel(
        app.scrollable_frame,
        text="",
        font=("Arial", 22, "italic"),
        text_color=app.theme.get("fg", "#1A1A1A"),
    )
    app.desc_label.grid(row=row, column=0, pady=12)
    row += 1
    
    # === LAST UPDATED TIMESTAMP ===
    app.update_label = ctk.CTkLabel(
        app.scrollable_frame,
        text="",
        font=("Arial", 12),
        text_color=app.theme.get("fg", "#1A1A1A"),
    )
    app.update_label.grid(row=row, column=0, pady=8)
    row += 1
    
    # === WEATHER ICON DISPLAY ===
    app.icon_label = ctk.CTkLabel(app.scrollable_frame, text="", image=None)
    app.icon_label.grid(row=row, column=0, pady=15)
    row += 1
    
    # === TOMORROW'S PREDICTION SECTION ===
    try:
        from features.tomorrows_guess.predictor import get_tomorrows_prediction
        app.tomorrow_guess_frame = create_tomorrow_guess_frame(app.scrollable_frame, app.theme)
        app.tomorrow_guess_frame.grid(row=row, column=0, pady=25, sticky="ew", padx=15)
        row += 1
        
        update_tomorrow_guess_display(app.tomorrow_guess_frame, "N/A", "N/A", "N/A")
    except Exception as e:
        print(f"Tomorrow's prediction frame error: {e}")
        app.tomorrow_guess_frame = ctk.CTkFrame(
            app.scrollable_frame, 
            fg_color=app.theme.get("text_bg", "#F0F0F0"),
            corner_radius=15,
            border_width=1,
            border_color=app.theme.get("accent", "#6495ED")
        )
        app.tomorrow_guess_frame.grid(row=row, column=0, pady=25, sticky="ew", padx=15)
        
        placeholder_label = ctk.CTkLabel(
            app.tomorrow_guess_frame, 
            text="🔮 Tomorrow's Prediction", 
            font=("Arial", 18, "bold"),
            text_color=app.theme.get("text_fg", "#1A1A1A")
        )
        placeholder_label.pack(pady=15)
        
        status_label = ctk.CTkLabel(
            app.tomorrow_guess_frame, 
            text="Loading prediction...", 
            font=("Arial", 12),
            text_color=app.theme.get("text_fg", "#1A1A1A")
        )
        status_label.pack(pady=(0, 15))
        row += 1
    
    # === WEATHER HISTORY SECTION ===
    app.history_frame = ctk.CTkFrame(
        app.scrollable_frame, 
        fg_color=app.theme.get("text_bg", "#F0F8FF"), 
        corner_radius=15,
        border_width=1,
        border_color=app.theme.get("accent", "#6495ED")
    )
    app.history_frame.grid(row=row, column=0, sticky="ew", pady=(15, 40), padx=15)
    row += 1
    
    app.scrollable_frame.grid_columnconfigure(0, weight=1)
    
    # Tomorrow's prediction async update
    def update_tomorrow_async(city):
        try:
            predicted_temp, confidence, accuracy = get_tomorrows_prediction(city)
            def update_display():
                try:
                    update_tomorrow_guess_display(
                        app.tomorrow_guess_frame,
                        predicted_temp,
                        confidence,
                        accuracy,
                    )
                except Exception as e:
                    print(f"Tomorrow's display update error: {e}")
            app.after(0, update_display)
        except Exception as e:
            print(f"Tomorrow's prediction error: {e}")
    
    try:
        city = app.city_var.get() if hasattr(app, 'city_var') else "London"
        threading.Thread(target=update_tomorrow_async, args=(city,), daemon=True).start()
    except Exception as e:
        print(f"Tomorrow's prediction thread error: {e}")
    
    # === PERIODIC UPDATES ===
    def periodic_background_update():
        try:
            current_condition = getattr(app, 'current_weather_condition', 'clear')
            new_theme = app.smart_background.get_adaptive_theme(current_condition)
            if hasattr(app, 'theme'):
                app.theme.update(new_theme)
            app.smart_background.update_background(current_condition)
        except Exception as e:
            print(f"Periodic background update error: {e}")
        app.after(300000, periodic_background_update)  # every 5 min
    
    app.after(10000, periodic_background_update)  # start after 10s
    
    # === HELPER FUNCTIONS ===
    def update_weather_condition(condition):
        try:
            app.current_weather_condition = condition
            new_theme = app.smart_background.get_adaptive_theme(condition)
            app.theme.update(new_theme)
            app.smart_background.update_background(condition)
            update_widget_colors()
        except Exception as e:
            print(f"Weather condition update error: {e}")
    
    def update_widget_colors():
        try:
            if hasattr(app, 'city_entry'):
                app.city_entry.configure(
                    fg_color=app.theme.get("entry_bg", "#FFFFFF"),
                    text_color=app.theme.get("entry_fg", "#1A1A1A"),
                    border_color=app.theme.get("accent", "#6495ED")
                )
            if hasattr(app, 'temp_label'):
                app.temp_label.configure(text_color=app.theme.get("fg", "#1A1A1A"))
            if hasattr(app, 'desc_label'):
                app.desc_label.configure(text_color=app.theme.get("fg", "#1A1A1A"))
            if hasattr(app, 'update_label'):
                app.update_label.configure(text_color=app.theme.get("fg", "#1A1A1A"))
            if hasattr(app, 'metric_value_labels'):
                for label in app.metric_value_labels.values():
                    label.configure(text_color=app.theme.get("text_fg", "#1A1A1A"))
        except Exception as e:
            print(f"Widget color update error: {e}")
    
    def get_current_theme():
        try:
            current_condition = getattr(app, 'current_weather_condition', 'clear')
            return app.smart_background.get_adaptive_theme(current_condition)
        except Exception as e:
            print(f"Get current theme error: {e}")
            return app.theme if hasattr(app, 'theme') else {}
    
    def force_background_refresh():
        try:
            if hasattr(app, 'smart_background') and app.smart_background.canvas:
                current_condition = getattr(app, 'current_weather_condition', 'clear')
                app.smart_background.update_background(current_condition)
        except Exception as e:
            print(f"Force background refresh error: {e}")
    
    # Save helpers on app object
    app.update_weather_condition = update_weather_condition
    app.update_widget_colors = update_widget_colors
    app.get_current_theme = get_current_theme
    app.force_background_refresh = force_background_refresh
    
    # === RESPONSIVE DESIGN ===
    def on_window_resize():
        try:
            app.after(300, force_background_refresh)
        except Exception as e:
            print(f"Window resize handler error: {e}")
    app.bind("<Configure>", lambda e: on_window_resize() if e.widget == app else None)
    
    # === ACCESSIBILITY ===
    def toggle_high_contrast():
        try:
            if not hasattr(app, 'high_contrast_mode'):
                app.high_contrast_mode = False
            app.high_contrast_mode = not app.high_contrast_mode
            if app.high_contrast_mode:
                high_contrast_theme = {
                    "bg": "#000000",
                    "fg": "#FFFFFF",
                    "text_bg": "#1A1A1A",
                    "text_fg": "#FFFFFF",
                    "button_bg": "#FFFFFF",
                    "button_fg": "#000000",
                    "entry_bg": "#1A1A1A",
                    "entry_fg": "#FFFFFF",
                    "accent": "#FFFF00"
                }
                app.theme.update(high_contrast_theme)
            else:
                current_condition = getattr(app, 'current_weather_condition', 'clear')
                adaptive_theme = app.smart_background.get_adaptive_theme(current_condition)
                app.theme.update(adaptive_theme)
            update_widget_colors()
        except Exception as e:
            print(f"High contrast toggle error: {e}")
    
    app.toggle_high_contrast = toggle_high_contrast
    
    # === PERFORMANCE OPTIMIZATION ===
    def optimize_performance():
        try:
            if hasattr(app, 'performance_mode'):
                if app.performance_mode:
                    app.smart_background.animation_running = False
                    return 600000  # 10 minutes
            return 300000  # 5 minutes (normal)
        except Exception as e:
            print(f"Performance optimization error: {e}")
            return 300000
    
    # === INITIALIZATION COMPLETE ===
    print("Enhanced Smart Background GUI initialized successfully!")
    print(f"Current theme: {app.theme.get('bg', 'Unknown')}")
    print(f"Time period: {app.smart_background.get_time_period()}")
    print(f"Season: {app.smart_background.get_season()}")
    
    try:
        app.after(500, lambda: app.smart_background.update_background())
        if hasattr(app, 'city_entry'):
            app.city_entry.focus_set()
    except Exception as e:
        print(f"Final setup error: {e}")
