"""
Graphs Controller - Simple Fix with Direct Translation
====================================================

Simple logical fix: check if language controller exists, get current language,
and directly translate the text without overcomplicating.
"""

import tkinter as tk
from tkinter import ttk
import threading
import traceback
import warnings
from typing import Optional, Dict, Any, Tuple

# Suppress matplotlib warnings before importing
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
warnings.filterwarnings('ignore', message='.*Glyph.*missing from font.*')
warnings.filterwarnings('ignore', message='.*Matplotlib currently does not support.*')
warnings.filterwarnings('ignore', message='.*DejaVu Sans.*')

try:
    from .graph_generator import WeatherGraphGenerator
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class GraphsController:
    """
    Controller for the Weather Graphs feature with simple direct translation.
    """
    
    def __init__(self, app, gui_controller):
        """
        Initialize the graphs controller.
        """
        self.app = app
        self.gui = gui_controller
        
        # Suppress matplotlib warnings before initializing generator
        self._suppress_warnings()
        
        # Initialize graph generator if matplotlib is available
        if MATPLOTLIB_AVAILABLE:
            self.graph_generator = WeatherGraphGenerator(app)
            print("✓ Graph generator initialized with matplotlib support")
        else:
            self.graph_generator = None
            print("❌ Matplotlib not available - graph features disabled")
        
        # Original graph options (keep this unchanged)
        self.graph_options = {
            "7-Day Temperature Trend": "temperature_trend",
            "Temperature Range Chart": "temperature_range", 
            "Humidity Trends": "humidity_trends",
            "Weather Conditions Distribution": "conditions_distribution",
            "Prediction Accuracy Chart": "prediction_accuracy"
        }
        
        # GUI component references
        self.dropdown: Optional[ttk.Combobox] = None
        self.graph_frame: Optional[tk.Frame] = None
        
        # Track selected graph type
        self.selected_graph = tk.StringVar(value="7-Day Temperature Trend")
        
        # Performance optimization: cache recently generated graphs
        self._graph_cache: Dict[str, Any] = {}
        self._cache_timeout = 300  # 5 minutes in seconds

    def _get_current_language(self):
        """Get current language from app."""
        print("=== DEBUG: Getting current language ===")
        
        # Try multiple ways to get the language
        try:
            # Method 1: Direct from app
            if hasattr(self.app, 'language_controller'):
                print(f"App has language_controller: {self.app.language_controller}")
                if self.app.language_controller:
                    lang = self.app.language_controller.current_language
                    print(f"Language from controller: {lang}")
                    return lang
        except Exception as e:
            print(f"Method 1 failed: {e}")
        
        try:
            # Method 2: Check if there's a language variable on app
            if hasattr(self.app, 'current_language'):
                lang = self.app.current_language
                print(f"Language from app.current_language: {lang}")
                return lang
        except Exception as e:
            print(f"Method 2 failed: {e}")
            
        try:
            # Method 3: Check GUI controller
            if hasattr(self.gui, 'language_controller'):
                print(f"GUI has language_controller: {self.gui.language_controller}")
                if self.gui.language_controller:
                    lang = self.gui.language_controller.current_language
                    print(f"Language from GUI controller: {lang}")
                    return lang
        except Exception as e:
            print(f"Method 3 failed: {e}")
        
        print("All methods failed, defaulting to English")
        return "English"

    def _translate_text(self, english_text):
        """Simple direct translation function."""
        current_lang = self._get_current_language()
        print(f"=== TRANSLATING: '{english_text}' in language '{current_lang}' ===")
        
        # Direct translation mappings
        translations = {
            "Hindi": {
                "Weather Graphs": "मौसम चार्ट",
                "Select Graph Type:": "चार्ट प्रकार चुनें:",
                "← Back": "← वापस",
                "7-Day Temperature Trend": "७-दिन तापमान रुझान",
                "Temperature Range Chart": "तापमान सीमा चार्ट", 
                "Humidity Trends": "आर्द्रता रुझान",
                "Weather Conditions Distribution": "मौसम स्थितियों का वितरण",
                "Prediction Accuracy Chart": "भविष्यवाणी सटीकता चार्ट",
                "Graph Information": "चार्ट की जानकारी"
            },
            "Spanish": {
                "Weather Graphs": "Gráficos del Clima",
                "Select Graph Type:": "Seleccionar tipo de gráfico:",
                "← Back": "← Atrás", 
                "7-Day Temperature Trend": "Tendencia de Temperatura de 7 Días",
                "Temperature Range Chart": "Gráfico de Rango de Temperatura",
                "Humidity Trends": "Tendencias de Humedad", 
                "Weather Conditions Distribution": "Distribución de Condiciones Climáticas",
                "Prediction Accuracy Chart": "Gráfico de Precisión de Predicción",
                "Graph Information": "Información del Gráfico"
            }
        }
        
        if current_lang in translations and english_text in translations[current_lang]:
            translated = translations[current_lang][english_text]
            print(f"FOUND TRANSLATION: '{english_text}' -> '{translated}'")
            return translated
        
        print(f"NO TRANSLATION FOUND, returning original: '{english_text}'")
        return english_text  # Return original if no translation
    
    def _suppress_warnings(self):
        """Suppress matplotlib font warnings."""
        warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
        warnings.filterwarnings('ignore', message='.*Glyph.*missing from font.*')
        warnings.filterwarnings('ignore', message='.*Matplotlib currently does not support.*')
        warnings.filterwarnings('ignore', message='.*DejaVu Sans.*')
        
    def build_page(self, window_width: int, window_height: int):
        """Build the main graphs page interface."""
        try:
            # Add navigation back button
            self._add_back_button()
            
            # Create page header with title and info button
            self._build_header(window_width)
            
            # Check if required dependencies are available
            if not MATPLOTLIB_AVAILABLE:
                self._show_dependency_error(window_width, window_height)
                return
            
            # Dependencies available - build full interface
            self._build_dropdown_selector(window_width)
            self._build_graph_display_area(window_width, window_height)
            
            # Load default graph after short delay
            self.app.after(500, self._load_selected_graph)
            
        except Exception as e:
            print(f"Error building graphs page: {e}")
            traceback.print_exc()
    
    def _show_dependency_error(self, window_width: int, window_height: int):
        """Show error message when required libraries are missing."""
        error_frame = tk.Frame(
            self.app,
            bg=self._get_canvas_bg_color(),
            relief="solid",
            borderwidth=2,
            highlightthickness=0
        )
        error_frame.place(x=50, y=200, width=window_width-100, height=300)
        self.gui.widgets.append(error_frame)
        
        title_text = self._translate_text("Weather Graphs")
        error_text = (
            f"📊 {title_text}\n\n"
            f"❌ Missing Dependencies\n\n"
            f"To use the graphs feature, please install:\n\n"
            f"pip3 install matplotlib numpy pandas\n\n"
            f"Then restart the application."
        )
        
        error_label = self._create_black_label(
            error_frame,
            text=error_text,
            font=("Arial", 16),
            x=(window_width-100)/2,
            y=150
        )
    
    def _add_back_button(self):
        """Add navigation back button."""
        back_text = self._translate_text("← Back")
        back_button = tk.Button(
            self.app,
            text=back_text,
            command=lambda: self.gui.show_page("main"),
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
        back_button.place(x=50, y=30, anchor="center")
        self.gui.widgets.append(back_button)
    
    def _build_header(self, window_width: int):
        """Build page header."""
        title_font_size = int(28 + window_width/40)
        
        # Translate the title
        title_text = self._translate_text("Weather Graphs")
        title_main = self._create_black_label(
            self.app,
            text=title_text,
            font=("Arial", title_font_size, "bold"),
            x=window_width/2,
            y=80
        )
        self.gui.widgets.append(title_main)
        
        info_button = tk.Button(
            self.app,
            text="i",
            command=self._show_graph_info,
            bg="lightblue",
            fg="black",
            font=("Arial", int(16 + window_width/80), "bold"),
            relief="raised",
            borderwidth=2,
            width=3,
            height=1,
            activeforeground="black",
            activebackground="lightcyan",
            highlightthickness=0
        )
        info_button.place(x=window_width/2 + 240, y=80, anchor="center")
        self.gui.widgets.append(info_button)
    
    def _build_dropdown_selector(self, window_width: int):
        """Build dropdown menu."""
        # Translate the label
        label_text = self._translate_text("Select Graph Type:")
        dropdown_label = self._create_black_label(
            self.app,
            text=label_text,
            font=("Arial", 16, "bold"),
            x=window_width/2 - 150,
            y=130
        )
        self.gui.widgets.append(dropdown_label)
        
        # Get translated dropdown options
        translated_options = []
        for english_option in self.graph_options.keys():
            translated_option = self._translate_text(english_option)
            translated_options.append(translated_option)
        
        # Set initial translated value
        initial_english = self.selected_graph.get()
        initial_translated = self._translate_text(initial_english)
        self.selected_graph.set(initial_translated)
        
        self.dropdown = ttk.Combobox(
            self.app,
            textvariable=self.selected_graph,
            values=translated_options,
            state="readonly",
            width=35,
            font=("Arial", 12)
        )
        self.dropdown.place(x=window_width/2 + 20, y=130, anchor="w")
        
        self.dropdown.bind("<<ComboboxSelected>>", self._on_graph_selection_changed)
        self.gui.widgets.append(self.dropdown)
    
    def _build_graph_display_area(self, window_width: int, window_height: int):
        """Build the main area where graphs will be displayed."""
        graph_start_y = 170
        graph_height = window_height - 220
        graph_width = window_width - 100
        
        canvas_bg_color = self._get_canvas_bg_color()
        self.graph_frame = tk.Frame(
            self.app,
            bg=canvas_bg_color,
            relief="solid",
            borderwidth=2,
            highlightthickness=0
        )
        self.graph_frame.place(
            x=50,
            y=graph_start_y,
            width=graph_width,
            height=graph_height
        )
        self.gui.widgets.append(self.graph_frame)
        
        loading_label = self._create_black_label(
            self.graph_frame,
            text="📊 Loading graph...\nPlease wait while we generate your visualization.",
            font=("Arial", 16),
            x=graph_width/2,
            y=graph_height/2
        )
    
    def _on_graph_selection_changed(self, event=None):
        """Handle user selecting a different graph type."""
        print(f"Graph selection changed to: {self.selected_graph.get()}")
        self._load_selected_graph()
    
    def _find_english_key_from_translated(self, translated_text):
        """Find the original English key from translated text."""
        for english_key in self.graph_options.keys():
            if self._translate_text(english_key) == translated_text:
                return english_key
        return "7-Day Temperature Trend"  # fallback
    
    def _load_selected_graph(self):
        """Load and display the currently selected graph type."""
        if not self.graph_generator:
            print("❌ Graph generator not available")
            return
        
        # Convert translated selection back to English key
        selected_translated = self.selected_graph.get()
        selected_english = self._find_english_key_from_translated(selected_translated)
        graph_type = self.graph_options[selected_english]
        
        print(f"Loading graph: {selected_translated} -> {selected_english} -> {graph_type}")
        
        # Check cache first
        cache_key = f"{graph_type}_{self.app.city_var.get().strip()}"
        cached_result = self._get_cached_graph(cache_key)
        
        if cached_result:
            print(f"Cached graph result for {cache_key}")
            fig, success, error_msg = cached_result
            self._display_graph_result(fig, success, error_msg, selected_translated)
            return
        
        # Not in cache - show loading and generate new graph
        self._show_loading_message()
        
        # Start background graph generation
        threading.Thread(
            target=self._generate_graph_background,
            args=(graph_type, selected_translated, cache_key),
            daemon=True
        ).start()
    
    def _generate_graph_background(self, graph_type: str, graph_name: str, cache_key: str):
        """Generate graph in background thread."""
        try:
            city = self.app.city_var.get().strip() or "New York"
            print(f"Generating {graph_type} graph for {city}")
            
            # Suppress warnings during graph generation
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                fig, success, error_msg = self.graph_generator.generate_graph(graph_type, city)
            
            # Cache successful results
            if success and fig:
                self._cache_graph(cache_key, (fig, success, error_msg))
            
            # Update UI on main thread
            self.app.after(0, lambda: self._display_graph_result(fig, success, error_msg, graph_name))
            
        except Exception as e:
            error_message = f"Error generating graph: {str(e)}"
            print(f"Graph generation error: {e}")
            traceback.print_exc()
            
            self.app.after(0, lambda: self._display_graph_result(None, False, error_message, graph_name))
    
    def _display_graph_result(self, fig, success: bool, error_msg: Optional[str], graph_name: str):
        """Display the graph generation result."""
        try:
            # Clear existing content from graph frame
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            
            if success and fig:
                print(f"✓ Displaying {graph_name} graph")
                self._display_matplotlib_graph(fig)
            else:
                print(f"❌ Error displaying {graph_name}: {error_msg}")
                self._display_graph_error(graph_name, error_msg)
                
        except Exception as e:
            print(f"Error in display_graph_result: {e}")
            self._display_fallback_error(str(e))
    
    def _display_matplotlib_graph(self, fig):
        """Display a matplotlib figure."""
        try:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            # Suppress warnings during canvas creation and drawing
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                canvas = FigureCanvasTkAgg(fig, self.graph_frame)
                canvas.draw()
            
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            print("✓ Matplotlib graph displayed successfully")
            
        except Exception as e:
            print(f"Error displaying matplotlib graph: {e}")
            self._display_fallback_error(f"Error displaying graph: {str(e)}")
    
    def _display_graph_error(self, graph_name: str, error_msg: Optional[str]):
        """Display error message when graph generation fails."""
        error_text = (
            f"❌ Error loading {graph_name}\n\n"
            f"{error_msg or 'Unknown error occurred'}\n\n"
            f"Please try refreshing or selecting a different graph."
        )
        
        error_label = self._create_black_label(
            self.graph_frame,
            text=error_text,
            font=("Arial", 14),
            x=200,
            y=150,
            justify="center"
        )
    
    def _display_fallback_error(self, error_msg: str):
        """Display fallback error message."""
        fallback_text = (
            f"❌ Unable to display graph\n\n"
            f"Error: {error_msg}\n\n"
            f"Please try again later."
        )
        
        fallback_label = self._create_black_label(
            self.graph_frame,
            text=fallback_text,
            font=("Arial", 14),
            x=200,
            y=150,
            justify="center"
        )
    
    def _show_loading_message(self):
        """Show loading message while graph is being generated."""
        try:
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            
            loading_label = self._create_black_label(
                self.graph_frame,
                text="📊 Generating graph...\n\nThis may take a few moments.\nPlease wait while we process your data.",
                font=("Arial", 16),
                x=200,
                y=150,
                justify="center"
            )
            
        except Exception as e:
            print(f"Error showing loading message: {e}")
    
    def _show_graph_info(self):
        """Show information about the currently selected graph."""
        from tkinter import messagebox
        
        selected_graph = self.selected_graph.get()
        city = self.app.city_var.get().strip() or "New York"
        
        info_title = self._translate_text("Graph Information")
        info_text = self._get_detailed_graph_info(selected_graph, city)
        
        messagebox.showinfo(info_title, info_text)
    
    def _get_detailed_graph_info(self, graph_name, city):
        """Get detailed information for each graph type in current language."""
        current_lang = self._get_current_language()
        
        # Find which English graph this corresponds to
        english_name = self._find_english_key_from_translated(graph_name)
        
        if current_lang == "Hindi":
            if english_name == "7-Day Temperature Trend":
                return f"""७-दिन तापमान रुझान - {city}

📊 यह क्या दिखाता है:
• लाल रेखा: दैनिक अधिकतम तापमान
• नीली रेखा: दैनिक न्यूनतम तापमान  
• हरी रेखा: दैनिक औसत तापमान

📋 डेटा स्रोत:
• प्राथमिक: ओपन-मेटिओ ऐतिहासिक मौसम API
• द्वितीयक: स्थानीय मौसम खोज इतिहास
• बैकअप: मौसम और स्थान के आधार पर यथार्थवादी नमूना डेटा

📈 चार्ट को समझना:
• पिछले 7 दिनों में तापमान पैटर्न दिखाता है
• तापमान सेल्सियस (°C) में प्रदर्शित
• प्रत्येक बिंदु एक दिन की तापमान रीडिंग दर्शाता है"""

            elif english_name == "Temperature Range Chart":
                return f"""तापमान सीमा चार्ट - {city}

📊 यह क्या दिखाता है:
• प्रत्येक बार दैनिक तापमान भिन्नता दर्शाता है
• बार की ऊंचाई = अधिकतम तापमान - न्यूनतम तापमान
• दिखाता है कि प्रत्येक दिन तापमान कितना बदलता है

📈 चार्ट को समझना:
• ऊंचे बार = उस दिन अधिक तापमान भिन्नता
• नीचे बार = अधिक स्थिर तापमान
• मान सेल्सियस डिग्री में अंतर दिखाते हैं"""

            elif english_name == "Humidity Trends":
                return f"""आर्द्रता रुझान - {city}

📊 यह क्या दिखाता है:
• हरी रेखा समय के साथ आर्द्रता प्रतिशत को ट्रैक करती है
• दिखाता है कि नमी का स्तर दिन-प्रतिदिन कैसे बदलता है
• मान 0% (बहुत शुष्क) से 100% (बहुत आर्द्र) तक होते हैं

📈 चार्ट को समझना:
• उच्च मान = अधिक आर्द्र स्थितियां
• कम मान = सूखी हवा
• सामान्य आरामदायक सीमा 30-60% है"""

            elif english_name == "Weather Conditions Distribution":
                return f"""मौसम स्थितियों का वितरण - {city}

📊 यह क्या दिखाता है:
• पाई चार्ट विभिन्न मौसम प्रकारों का प्रतिशत दिखाता है
• इस शहर के लिए आपके मौसम खोज इतिहास पर आधारित
• प्रत्येक टुकड़ा दर्शाता है कि वह स्थिति कितनी बार हुई

📈 चार्ट को समझना:
• बड़े टुकड़े = अधिक सामान्य मौसम स्थितियां
• प्रतिशत 100% तक जोड़ते हैं
• आपकी खोजों के दौरान मौसम पैटर्न को दर्शाता है"""

            elif english_name == "Prediction Accuracy Chart":
                return f"""भविष्यवाणी सटीकता चार्ट - {city}

📊 यह क्या दिखाता है:
• बैंगनी रेखा ट्रैक करती है कि हमारी मौसम भविष्यवाणियां कितनी सटीक रही हैं
• पिछले 2 सप्ताह में भविष्यवाणी प्रदर्शन दिखाता है
• मान सटीकता प्रतिशत दर्शाते हैं (उच्चतर = बेहतर भविष्यवाणियां)

📈 चार्ट को समझना:
• 90%+ = उत्कृष्ट भविष्यवाणी सटीकता
• 75%+ = अच्छी भविष्यवाणी सटीकता
• 60% से कम = मध्यम भविष्यवाणी सटीकता
• संदर्भ रेखाएं प्रदर्शन सीमा दिखाती हैं"""

        elif current_lang == "Spanish":
            if english_name == "7-Day Temperature Trend":
                return f"""Tendencia de Temperatura de 7 Días - {city}

📊 Lo que muestra:
• Línea roja: Temperaturas máximas diarias
• Línea azul: Temperaturas mínimas diarias
• Línea verde: Temperaturas promedio diarias

📋 Fuentes de Datos:
• Primaria: API histórica del clima Open-Meteo
• Secundaria: Historial local de búsquedas del clima
• Respaldo: Datos de muestra realistas basados en temporada y ubicación

📈 Entendiendo el Gráfico:
• Muestra patrones de temperatura durante los últimos 7 días
• Temperaturas mostradas en Celsius (°C)
• Cada punto representa la lectura de temperatura de un día"""

            elif english_name == "Temperature Range Chart":
                return f"""Gráfico de Rango de Temperatura - {city}

📊 Lo que muestra:
• Cada barra representa la variación diaria de temperatura
• Altura de barra = Temperatura máxima - Temperatura mínima
• Muestra cuánto fluctúan las temperaturas cada día

📈 Entendiendo el Gráfico:
• Barras más altas = más variación de temperatura ese día
• Barras más bajas = temperaturas más estables
• Los valores muestran la diferencia en grados Celsius"""

            elif english_name == "Humidity Trends":
                return f"""Tendencias de Humedad - {city}

📊 Lo que muestra:
• La línea verde rastrea el porcentaje de humedad a lo largo del tiempo
• Muestra cómo cambian los niveles de humedad día a día
• Los valores van de 0% (muy seco) a 100% (muy húmedo)

📈 Entendiendo el Gráfico:
• Valores más altos = condiciones más húmedas
• Valores más bajos = aire más seco
• El rango cómodo típico es 30-60%"""

            elif english_name == "Weather Conditions Distribution":
                return f"""Distribución de Condiciones Climáticas - {city}

📊 Lo que muestra:
• Gráfico circular mostrando porcentaje de diferentes tipos de clima
• Basado en su historial de búsquedas del clima para esta ciudad
• Cada porción representa qué tan frecuente ocurrió esa condición

📈 Entendiendo el Gráfico:
• Porciones más grandes = condiciones climáticas más comunes
• Los porcentajes suman 100%
• Refleja los patrones climáticos durante sus búsquedas"""

            elif english_name == "Prediction Accuracy Chart":
                return f"""Gráfico de Precisión de Predicción - {city}

📊 Lo que muestra:
• La línea púrpura rastrea qué tan precisas han sido nuestras predicciones del clima
• Muestra el rendimiento de predicción durante las últimas 2 semanas
• Los valores representan porcentaje de precisión (más alto = mejores predicciones)

📈 Entendiendo el Gráfico:
• 90%+ = Excelente precisión de predicción
• 75%+ = Buena precisión de predicción
• Menos del 60% = Precisión de predicción regular
• Las líneas de referencia muestran umbrales de rendimiento"""

        else:  # English
            if english_name == "7-Day Temperature Trend":
                return f"""7-Day Temperature Trend - {city}

📊 What This Shows:
• Red line: Daily maximum temperatures
• Blue line: Daily minimum temperatures  
• Green line: Daily average temperatures

📋 Data Sources:
• Primary: Open-Meteo historical weather API
• Secondary: Local weather search history
• Fallback: Realistic sample data based on season and location

📈 Understanding the Graph:
• Shows temperature patterns over the last 7 days
• Temperatures displayed in Celsius (°C)
• Each point represents one day's temperature reading"""

            elif english_name == "Temperature Range Chart":
                return f"""Temperature Range Chart - {city}

📊 What This Shows:
• Each bar represents the daily temperature variation
• Bar height = Maximum temperature - Minimum temperature
• Shows how much temperatures fluctuate each day

📈 Understanding the Graph:
• Higher bars = more temperature variation that day
• Lower bars = more stable temperatures
• Values show the difference in degrees Celsius"""

            elif english_name == "Humidity Trends":
                return f"""Humidity Trends - {city}

📊 What This Shows:
• Green line tracks humidity percentage over time
• Shows how moisture levels change day by day
• Values range from 0% (very dry) to 100% (very humid)

📈 Understanding the Graph:
• Higher values = more humid conditions
• Lower values = drier air
• Typical comfortable range is 30-60%"""

            elif english_name == "Weather Conditions Distribution":
                return f"""Weather Conditions Distribution - {city}

📊 What This Shows:
• Pie chart showing percentage of different weather types
• Based on your weather search history for this city
• Each slice represents how often that condition occurred

📈 Understanding the Graph:
• Larger slices = more common weather conditions
• Percentages add up to 100%
• Reflects the weather patterns during your searches"""

            elif english_name == "Prediction Accuracy Chart":
                return f"""Prediction Accuracy Chart - {city}

📊 What This Shows:
• Purple line tracks how accurate our weather predictions have been
• Shows prediction performance over the last 2 weeks
• Values represent accuracy percentage (higher = better predictions)

📈 Understanding the Graph:
• 90%+ = Excellent prediction accuracy
• 75%+ = Good prediction accuracy  
• Below 60% = Fair prediction accuracy
• Reference lines show performance thresholds"""

        # Fallback
        return f"""Graph Information - {city}

📊 Current Selection: {graph_name}

Select a specific graph type to see detailed information about that visualization."""
    
    def _get_cached_graph(self, cache_key: str) -> Optional[Tuple[Any, bool, Optional[str]]]:
        """Get cached graph result if available and not expired."""
        import time
        
        if cache_key in self._graph_cache:
            cached_data, timestamp = self._graph_cache[cache_key]
            
            if time.time() - timestamp < self._cache_timeout:
                return cached_data
            else:
                del self._graph_cache[cache_key]
        
        return None
    
    def _cache_graph(self, cache_key: str, graph_data: Tuple[Any, bool, Optional[str]]):
        """Store graph result in cache."""
        import time
        
        if len(self._graph_cache) >= 10:
            oldest_key = min(self._graph_cache.keys(), 
                           key=lambda k: self._graph_cache[k][1])
            del self._graph_cache[oldest_key]
        
        self._graph_cache[cache_key] = (graph_data, time.time())
        print(f"Cached graph result for {cache_key}")
    
    def clear_graph_cache(self):
        """Clear the graph cache."""
        self._graph_cache.clear()
        print("Graph cache cleared")
    
    def _create_black_label(self, parent, text: str, font: tuple, x: float, y: float, 
                           anchor: str = "center", **kwargs) -> tk.Label:
        """Create a label with black text and transparent background."""
        canvas_bg = self._get_canvas_bg_color()
        
        label = tk.Label(
            parent,
            text=text,
            font=font,
            fg="black",
            bg=canvas_bg,
            anchor=anchor,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            **kwargs
        )
        
        label.place(x=x, y=y, anchor=anchor)
        return label
    
    def _get_canvas_bg_color(self) -> str:
        """Get the current canvas background color."""
        try:
            if self.gui.bg_canvas:
                return self.gui.bg_canvas.cget("bg")
            return "#87CEEB"
        except:
            return "#87CEEB"
    
    def handle_theme_change(self):
        """Handle application theme changes."""
        try:
            canvas_bg = self._get_canvas_bg_color()
            
            if self.graph_frame:
                self.graph_frame.configure(bg=canvas_bg)
            
            self.clear_graph_cache()
            
            print("Graphs page updated for theme change")
                
        except Exception as e:
            print(f"Error handling theme change in graphs: {e}")
    
    def cleanup(self):
        """Clean up resources."""
        try:
            if self.graph_frame:
                for widget in self.graph_frame.winfo_children():
                    widget.destroy()
            
            self.clear_graph_cache()
            
            self.dropdown = None
            self.graph_frame = None
            
            print("Graphs controller cleanup completed")
            
        except Exception as e:
            print(f"Error during graphs cleanup: {e}")
    
    def get_available_graph_types(self) -> list:
        """Get list of available graph types."""
        return list(self.graph_options.keys())
    
    def is_graph_available(self, graph_name: str) -> bool:
        """Check if a specific graph type is available."""
        return graph_name in self.graph_options
    
    def get_dependency_status(self) -> Dict[str, Any]:
        """Get status information about required dependencies."""
        return {
            "matplotlib_available": MATPLOTLIB_AVAILABLE,
            "graph_generator_ready": self.graph_generator is not None,
            "cached_graphs": len(self._graph_cache),
            "available_graph_types": len(self.graph_options)
        }
    
    def force_refresh_current_graph(self):
        """Force refresh of the currently selected graph."""
        try:
            selected_translated = self.selected_graph.get()
            selected_english = self._find_english_key_from_translated(selected_translated)
            city = self.app.city_var.get().strip() or "New York"
            graph_type = self.graph_options[selected_english]
            cache_key = f"{graph_type}_{city}"
            
            if cache_key in self._graph_cache:
                del self._graph_cache[cache_key]
                print(f"Cleared cache for {cache_key}")
            
            self._load_selected_graph()
            
        except Exception as e:
            print(f"Error forcing graph refresh: {e}")
    
    def export_graph_info(self) -> Dict[str, Any]:
        """Export current graph information."""
        try:
            return {
                "selected_graph": self.selected_graph.get(),
                "current_city": self.app.city_var.get().strip(),
                "current_language": self._get_current_language(),
                "matplotlib_available": MATPLOTLIB_AVAILABLE,
                "cache_size": len(self._graph_cache),
                "available_options": [self._translate_text(opt) for opt in self.graph_options.keys()]
            }
        except Exception as e:
            return {"error": str(e)}