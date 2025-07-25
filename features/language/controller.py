"""
Language Selection Controller - Fixed Comprehensive Translation System
====================================================================

This module manages language selection for weather descriptions and ALL UI text.
Supports English, Spanish, and Hindi with complete consistency across the app.

Key fixes:
- Centralized translation system with fallbacks
- Consistent text updates when language changes
- Proper widget reference management
- Complete translation coverage for all text elements
"""

import tkinter as tk
from tkinter import ttk
import json
import os


class LanguageController:
    """
    Comprehensive Language Controller for Weather App
    
    Manages language selection and translation of ALL text elements
    with proper consistency and fallback handling.
    """
    
    def __init__(self, app, gui_controller):
        """
        Initialize the language controller.
        
        Args:
            app: Main weather application instance
            gui_controller: GUI controller that manages the interface
        """
        self.app = app
        self.gui = gui_controller
        
        # Supported languages with their OpenWeatherMap API codes
        self.supported_languages = {
            "English": "en",
            "Spanish": "es", 
            "Hindi": "hi"
        }
        
        # Current language (default to English)
        self.current_language = "English"
        
        # Language settings file path
        self.settings_file = "language_settings.json"
        
        # Complete UI translations - EVERY text element in the app
        self.translations = {
            "English": {
                # App Title
                "weather_app_title": "Smart Weather App with Sun & Moon Phases",
                
                # Language Selection Page
                "language_selection": "Language Selection",
                "select_language": "Select Language:",
                "apply": "Apply",
                "back": "← Back",
                "current_language": "Current",
                
                # Main Page - Weather Metrics
                "humidity": "Humidity",
                "wind": "Wind", 
                "pressure": "Press.",
                "visibility": "Visibility",
                "uv_index": "UV Index",
                "precipitation": "Precip.",
                
                # Main Page - Navigation Buttons
                "toggle_theme": "Toggle Theme",
                "tomorrow_prediction": "Tomorrow's Prediction",
                "weather_history": "Weather History",
                "weather_quiz": "Weather Quiz",
                "weather_graphs": "Weather Graphs",
                "map_view": "Map View",
                "sun_moon": "Sun & Moon",
                "language": "Language",
                
                # Prediction Page
                "tomorrow_weather_prediction": "Tomorrow's Weather Prediction",
                "temperature": "Temperature",
                "accuracy": "Accuracy",
                "confidence": "Confidence",
                
                # History Page
                "weather_history_title": "Weather History",
                "no_history_data": "📊 Weather History\n\nNo historical data available for this location.\nTry refreshing or selecting a different city.",
                
                # Sun & Moon Page
                "sun_moon_phases": "Sun & Moon Phases",
                "sunrise": "Sunrise",
                "sunset": "Sunset",
                "moon_phase": "Moon Phase",
                "moonrise": "Moonrise",
                "moonset": "Moonset",
                
                # Quiz Page
                "weather_quiz_title": "Weather Quiz",
                "start_quiz": "Start Quiz",
                "next_question": "Next Question",
                "submit_answer": "Submit Answer",
                "quiz_score": "Score",
                "correct": "Correct!",
                "incorrect": "Incorrect",
                
                # Map Page
                "weather_map": "Weather Map",
                "map_info": "Map Info",
                "map_unavailable": "Interactive Map\n(Map temporarily unavailable)",
                
                # Graphs Page
                "weather_graphs_title": "Weather Graphs",
                "temperature_graph": "Temperature Trends",
                "humidity_graph": "Humidity Levels", 
                "pressure_graph": "Pressure Changes",
                
                # Common UI Elements
                "loading": "Loading...",
                "fetching_weather": "Fetching weather...",
                "no_description": "No description",
                "not_available": "N/A",
                "error": "Error",
                "city_not_found": "City not found",
                "network_error": "Network error",
                "try_again": "Try again",
                "refresh": "Refresh",
                
                # Weather Conditions (fallbacks)
                "clear_sky": "Clear sky",
                "few_clouds": "Few clouds",
                "scattered_clouds": "Scattered clouds",
                "broken_clouds": "Broken clouds",
                "shower_rain": "Shower rain",
                "rain": "Rain",
                "thunderstorm": "Thunderstorm",
                "snow": "Snow",
                "mist": "Mist",
                
                # Units
                "celsius": "°C",
                "fahrenheit": "°F",
                "kmh": "km/h",
                "ms": "m/s",
                "hpa": "hPa",
                "meters": "m",
                "mm": "mm",
                "percent": "%"
            },
            
            "Spanish": {
                # App Title
                "weather_app_title": "Aplicación Meteorológica Inteligente con Fases del Sol y Luna",
                
                # Language Selection Page
                "language_selection": "Selección de Idioma",
                "select_language": "Seleccionar idioma:",
                "apply": "Aplicar",
                "back": "← Atrás",
                "current_language": "Actual",
                
                # Main Page - Weather Metrics
                "humidity": "Humedad",
                "wind": "Viento",
                "pressure": "Presión",
                "visibility": "Visibilidad",
                "uv_index": "Índice UV",
                "precipitation": "Precipitación",
                
                # Main Page - Navigation Buttons
                "toggle_theme": "Cambiar Tema",
                "tomorrow_prediction": "Predicción de Mañana",
                "weather_history": "Historial del Clima",
                "weather_quiz": "Quiz del Clima",
                "weather_graphs": "Gráficos del Clima",
                "map_view": "Vista del Mapa",
                "sun_moon": "Sol y Luna",
                "language": "Idioma",
                
                # Prediction Page
                "tomorrow_weather_prediction": "Predicción del Clima para Mañana",
                "temperature": "Temperatura",
                "accuracy": "Precisión",
                "confidence": "Confianza",
                
                # History Page
                "weather_history_title": "Historial del Clima",
                "no_history_data": "📊 Historial del Clima\n\nNo hay datos históricos disponibles para esta ubicación.\nIntenta actualizar o seleccionar una ciudad diferente.",
                
                # Sun & Moon Page
                "sun_moon_phases": "Fases del Sol y Luna",
                "sunrise": "Amanecer",
                "sunset": "Atardecer",
                "moon_phase": "Fase Lunar",
                "moonrise": "Salida de Luna",
                "moonset": "Puesta de Luna",
                
                # Quiz Page
                "weather_quiz_title": "Quiz del Clima",
                "start_quiz": "Iniciar Quiz",
                "next_question": "Siguiente Pregunta",
                "submit_answer": "Enviar Respuesta",
                "quiz_score": "Puntuación",
                "correct": "¡Correcto!",
                "incorrect": "Incorrecto",
                
                # Map Page
                "weather_map": "Mapa del Clima",
                "map_info": "Info del Mapa",
                "map_unavailable": "Mapa Interactivo\n(Mapa temporalmente no disponible)",
                
                # Graphs Page
                "weather_graphs_title": "Gráficos del Clima",
                "temperature_graph": "Tendencias de Temperatura",
                "humidity_graph": "Niveles de Humedad",
                "pressure_graph": "Cambios de Presión",
                
                # Common UI Elements
                "loading": "Cargando...",
                "fetching_weather": "Obteniendo clima...",
                "no_description": "Sin descripción",
                "not_available": "N/D",
                "error": "Error",
                "city_not_found": "Ciudad no encontrada",
                "network_error": "Error de red",
                "try_again": "Intentar de nuevo",
                "refresh": "Actualizar",
                
                # Weather Conditions
                "clear_sky": "Cielo despejado",
                "few_clouds": "Pocas nubes",
                "scattered_clouds": "Nubes dispersas",
                "broken_clouds": "Nubes fragmentadas",
                "shower_rain": "Lluvia ligera",
                "rain": "Lluvia",
                "thunderstorm": "Tormenta",
                "snow": "Nieve",
                "mist": "Neblina",
                
                # Units
                "celsius": "°C",
                "fahrenheit": "°F",
                "kmh": "km/h",
                "ms": "m/s",
                "hpa": "hPa",
                "meters": "m",
                "mm": "mm",
                "percent": "%"
            },
            
            "Hindi": {
                # App Title
                "weather_app_title": "सूर्य और चंद्रमा चरणों के साथ स्मार्ट मौसम ऐप",
                
                # Language Selection Page
                "language_selection": "भाषा चयन",
                "select_language": "भाषा चुनें:",
                "apply": "लागू करें",
                "back": "← वापस",
                "current_language": "वर्तमान",
                
                # Main Page - Weather Metrics
                "humidity": "आर्द्रता",
                "wind": "हवा",
                "pressure": "दबाव",
                "visibility": "दृश्यता",
                "uv_index": "यूवी सूचकांक",
                "precipitation": "वर्षा",
                
                # Main Page - Navigation Buttons
                "toggle_theme": "थीम बदलें",
                "tomorrow_prediction": "कल की भविष्यवाणी",
                "weather_history": "मौसम इतिहास",
                "weather_quiz": "मौसम प्रश्नोत्तरी",
                "weather_graphs": "मौसम चार्ट",
                "map_view": "मानचित्र दृश्य",
                "sun_moon": "सूर्य और चंद्रमा",
                "language": "भाषा",
                
                # Prediction Page
                "tomorrow_weather_prediction": "कल के मौसम की भविष्यवाणी",
                "temperature": "तापमान",
                "accuracy": "सटीकता",
                "confidence": "विश्वास",
                
                # History Page
                "weather_history_title": "मौसम इतिहास",
                "no_history_data": "📊 मौसम इतिहास\n\nइस स्थान के लिए कोई ऐतिहासिक डेटा उपलब्ध नहीं है।\nकृपया रीफ्रेश करें या कोई अन्य शहर चुनें।",
                
                # Sun & Moon Page
                "sun_moon_phases": "सूर्य और चंद्रमा के चरण",
                "sunrise": "सूर्योदय",
                "sunset": "सूर्यास्त",
                "moon_phase": "चंद्र कला",
                "moonrise": "चंद्रोदय",
                "moonset": "चंद्रास्त",
                
                # Quiz Page
                "weather_quiz_title": "मौसम प्रश्नोत्तरी",
                "start_quiz": "प्रश्नोत्तरी शुरू करें",
                "next_question": "अगला प्रश्न",
                "submit_answer": "उत्तर जमा करें",
                "quiz_score": "स्कोर",
                "correct": "सही!",
                "incorrect": "गलत",
                
                # Map Page
                "weather_map": "मौसम मानचित्र",
                "map_info": "मानचित्र जानकारी",
                "map_unavailable": "इंटरैक्टिव मानचित्र\n(मानचित्र अस्थायी रूप से अनुपलब्ध)",
                
                # Graphs Page
                "weather_graphs_title": "मौसम चार्ट",
                "temperature_graph": "तापमान रुझान",
                "humidity_graph": "आर्द्रता स्तर",
                "pressure_graph": "दबाव परिवर्तन",
                
                # Common UI Elements
                "loading": "लोड हो रहा है...",
                "fetching_weather": "मौसम प्राप्त कर रहे हैं...",
                "no_description": "कोई विवरण नहीं",
                "not_available": "उपलब्ध नहीं",
                "error": "त्रुटि",
                "city_not_found": "शहर नहीं मिला",
                "network_error": "नेटवर्क त्रुटि",
                "try_again": "पुनः प्रयास करें",
                "refresh": "रीफ्रेश करें",
                
                # Weather Conditions
                "clear_sky": "साफ आकाश",
                "few_clouds": "कुछ बादल",
                "scattered_clouds": "बिखरे हुए बादल",
                "broken_clouds": "टूटे हुए बादल",
                "shower_rain": "हल्की बारिश",
                "rain": "बारिश",
                "thunderstorm": "तूफान",
                "snow": "बर्फ",
                "mist": "कोहरा",
                
                # Units
                "celsius": "°से",
                "fahrenheit": "°फा",
                "kmh": "किमी/घं",
                "ms": "मी/से",
                "hpa": "एचपीए",
                "meters": "मी",
                "mm": "मिमी",
                "percent": "%"
            }
        }
        
        # Load saved language settings
        self.load_settings()
        
        # Widget references for the language selection page
        self.language_widgets = []
        self.language_dropdown = None
        self.language_var = None

    def get_text(self, key, fallback_to_english=True):
        """
        Get translated text for a given key with proper fallback handling.
        
        Args:
            key (str): Text key to translate
            fallback_to_english (bool): Whether to fallback to English if translation missing
            
        Returns:
            str: Translated text, English fallback, or key if nothing found
        """
        try:
            # Try to get translation in current language
            translation = self.translations.get(self.current_language, {}).get(key)
            
            if translation:
                return translation
            
            # Fallback to English if translation missing and fallback enabled
            if fallback_to_english and self.current_language != "English":
                english_translation = self.translations.get("English", {}).get(key)
                if english_translation:
                    return english_translation
            
            # Return the key itself if no translation found
            return key
            
        except Exception:
            # If anything goes wrong, return the key
            return key

    def update_all_translatable_widgets(self):
        """
        Update ALL widgets in the app that contain translatable text.
        
        This is called when language changes to ensure EVERY text element
        is properly updated throughout the entire application.
        """
        try:
            # Update app title
            self.update_app_title()
            
            # Get current page and trigger complete rebuild
            current_page = self.gui.current_page
            
            # Force complete page rebuild with new language
            self.gui.show_page(current_page)
            
            # Update any existing weather data display with new units
            if self.app.current_weather_data:
                self.gui.update_weather_display(self.app.current_weather_data)
            
            # Update prediction display if available
            if hasattr(self.app, 'current_prediction_data') and self.app.current_prediction_data:
                predicted_temp, confidence, accuracy = self.app.current_prediction_data
                self.gui.update_tomorrow_prediction_direct(predicted_temp, confidence, accuracy)
            
        except Exception as e:
            # If update fails, continue gracefully
            pass

    def build_page(self, window_width, window_height):
        """
        Build the language selection page with proper translations.
        """
        # Clear existing widgets first
        self._clear_widgets()
        
        # Add back button
        self._add_back_button()
        
        # Page title
        title_text = self.get_text("language_selection")
        title = self._create_label(
            self.app,
            text=title_text,
            font=("Arial", int(24 + window_width/50), "bold"),
            fg=self.app.text_color,
            x=window_width/2,
            y=150
        )
        self.language_widgets.append(title)
        
        # Language selection label
        select_text = self.get_text("select_language")
        select_label = self._create_label(
            self.app,
            text=select_text,
            font=("Arial", int(16 + window_width/60)),
            fg=self.app.text_color,
            x=window_width/2,
            y=220
        )
        self.language_widgets.append(select_label)
        
        # Language dropdown
        self._create_language_dropdown(window_width, window_height)
        
        # Apply button
        self._create_apply_button(window_width, window_height)
        
        # Current language indicator
        current_text = f"{self.get_text('current_language')}: {self.current_language}"
        current_label = self._create_label(
            self.app,
            text=current_text,
            font=("Arial", int(14 + window_width/70)),
            fg=self.app.text_color,
            x=window_width/2,
            y=400
        )
        self.language_widgets.append(current_label)

    def _create_language_dropdown(self, window_width, window_height):
        """Create the language selection dropdown."""
        canvas_bg = "#87CEEB"
        if self.gui.bg_canvas:
            try:
                canvas_bg = self.gui.bg_canvas.cget("bg")
            except:
                canvas_bg = "#87CEEB"
        
        dropdown_frame = tk.Frame(
            self.app,
            bg=canvas_bg,
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        dropdown_frame.place(x=window_width/2, y=280, anchor="center")
        
        self.language_var = tk.StringVar(value=self.current_language)
        
        self.language_dropdown = ttk.Combobox(
            dropdown_frame,
            textvariable=self.language_var,
            values=list(self.supported_languages.keys()),
            state="readonly",
            font=("Arial", int(14 + window_width/80)),
            width=15,
            justify="center"
        )
        self.language_dropdown.pack()
        
        self.language_widgets.append(dropdown_frame)

    def _create_apply_button(self, window_width, window_height):
        """Create the apply language button."""
        apply_text = self.get_text("apply")
        apply_btn = tk.Button(
            self.app,
            text=apply_text,
            command=self.apply_language_change,
            bg="grey",
            fg="black",
            font=("Arial", int(14 + window_width/70), "bold"),
            relief="raised",
            borderwidth=2,
            width=12,
            height=2,
            activeforeground="black",
            activebackground="lightgrey",
            highlightthickness=0
        )
        apply_btn.place(x=window_width/2, y=340, anchor="center")
        self.language_widgets.append(apply_btn)

    def _add_back_button(self):
        """Add a back button to return to the main page."""
        back_text = self.get_text("back")
        back_btn = tk.Button(
            self.app,
            text=back_text,
            command=self._go_back_to_main,
            bg="grey",
            fg="black",
            font=("Arial", 12, "bold"),
            relief="raised",
            borderwidth=2,
            width=8,
            height=1,
            activeforeground="black",
            activebackground="lightgrey",
            highlightthickness=0
        )
        back_btn.place(x=50, y=50, anchor="center")
        self.language_widgets.append(back_btn)

    def _go_back_to_main(self):
        """Go back to main page and ensure language widgets are cleared."""
        self._clear_widgets()
        self.gui.show_page("main")

    def _create_label(self, parent, text, font, fg, x, y, anchor="center", **kwargs):
        """Create a label with transparent background."""
        canvas_bg = "#87CEEB"
        if self.gui.bg_canvas:
            try:
                canvas_bg = self.gui.bg_canvas.cget("bg")
            except:
                canvas_bg = "#87CEEB"
        
        label = tk.Label(
            parent,
            text=text,
            font=font,
            fg=fg,
            bg=canvas_bg,
            anchor=anchor,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            **kwargs
        )
        label.place(x=x, y=y, anchor=anchor)
        return label

    def _clear_widgets(self):
        """Clear language selection widgets."""
        for widget in self.language_widgets:
            try:
                widget.destroy()
            except:
                pass
        self.language_widgets.clear()
        
        self.language_dropdown = None
        self.language_var = None

    def apply_language_change(self):
        """Apply the selected language change and update ALL translatable text."""
        try:
            if self.language_var:
                new_language = self.language_var.get()
                if new_language != self.current_language:
                    # Change language
                    self.current_language = new_language
                    self.save_settings()
                    
                    # Clear language page widgets first
                    self._clear_widgets()
                    
                    # Update ALL translatable text throughout the app
                    self.update_all_translatable_widgets()
                    
                    # Fetch weather data in new language
                    self.app.fetch_and_display()
                else:
                    # No change, just go back
                    self._go_back_to_main()
        except Exception as e:
            # If something goes wrong, just go back to main
            self._go_back_to_main()

    def get_language_code(self):
        """Get the OpenWeatherMap API language code for current language."""
        return self.supported_languages.get(self.current_language, "en")

    def update_app_title(self):
        """Update the application window title."""
        try:
            title = self.get_text("weather_app_title")
            self.app.title(title)
        except:
            pass

    def save_settings(self):
        """Save language settings to file."""
        try:
            settings = {"current_language": self.current_language}
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def load_settings(self):
        """Load language settings from file."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_language = settings.get("current_language", "English")
        except Exception:
            self.current_language = "English"

    def cleanup(self):
        """Clean up language controller resources."""
        self._clear_widgets()