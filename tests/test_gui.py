from core.gui import build_gui
import customtkinter as ctk
from core.theme import LIGHT_THEME

def test_build_gui_creates_widgets():
    app = ctk.CTk()
    app.theme = LIGHT_THEME
    app.city_var = ctk.StringVar(value="New York")
    app.metric_value_labels = {}
    app.toggle_theme = lambda: None
    app.update_weather_history = lambda: None
    app.temp_unit = "C"
    app.toggle_temp_unit = lambda event=None: None

    build_gui(app)
    assert len(app.winfo_children()) > 0
