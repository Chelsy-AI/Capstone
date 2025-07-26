"""
Updated Language Translations Data with Graph Support
====================================================

Contains all translation data for the weather application including 
comprehensive translations for the graphs page and all UI elements.
"""

TRANSLATIONS = {
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
        
        # Graphs Page - Main Elements
        "weather_graphs_title": "Weather Graphs",
        "select_graph_type": "Select Graph Type:",
        "graph_information": "Graph Information",
        
        # Graph Types (for dropdown)
        "7_day_temperature_trend": "7-Day Temperature Trend",
        "temperature_range_chart": "Temperature Range Chart",
        "humidity_trends": "Humidity Trends",
        "weather_conditions_distribution": "Weather Conditions Distribution",
        "prediction_accuracy_chart": "Prediction Accuracy Chart",
        
        # Graph Loading and Error Messages
        "loading_graph": "📊 Loading graph...\nPlease wait while we generate your visualization.",
        "generating_graph": "📊 Generating graph...",
        "processing_data_wait": "This may take a few moments.\nPlease wait while we process your data.",
        "error_loading_graph": "❌ Error loading graph",
        "try_refresh_or_different_graph": "Please try refreshing or selecting a different graph.",
        "unable_to_display_graph": "❌ Unable to display graph",
        "try_again_later": "Please try again later.",
        
        # Dependency Error Messages
        "missing_dependencies": "Missing Dependencies",
        "install_matplotlib": "To use the graphs feature, please install:",
        "restart_application": "Then restart the application.",
        
        # Graph Information Tooltips - Temperature Trend
        "temp_trend_what_shows": "What This Shows:",
        "red_line_max_temp": "• Red line: Daily maximum temperatures",
        "blue_line_min_temp": "• Blue line: Daily minimum temperatures", 
        "green_line_avg_temp": "• Green line: Daily average temperatures",
        "data_sources": "Data Sources:",
        "primary_open_meteo": "• Primary: Open-Meteo historical weather API",
        "secondary_local_history": "• Secondary: Local weather search history",
        "fallback_sample_data": "• Fallback: Realistic sample data based on season and location",
        "understanding_graph": "Understanding the Graph:",
        "temp_patterns_7_days": "• Shows temperature patterns over the last 7 days",
        "temp_displayed_celsius": "• Temperatures displayed in Celsius (°C)",
        "each_point_one_day": "• Each point represents one day's temperature reading",
        
        # Graph Information - Temperature Range
        "temp_range_what_shows": "What This Shows:",
        "bar_represents_daily_variation": "• Each bar represents the daily temperature variation",
        "bar_height_max_min_diff": "• Bar height = Maximum temperature - Minimum temperature",
        "shows_temp_fluctuation": "• Shows how much temperatures fluctuate each day",
        "higher_bars_more_variation": "• Higher bars = more temperature variation that day",
        "lower_bars_stable_temps": "• Lower bars = more stable temperatures",
        "values_celsius_difference": "• Values show the difference in degrees Celsius",
        
        # Graph Information - Humidity
        "humidity_what_shows": "What This Shows:",
        "green_line_humidity_percent": "• Green line tracks humidity percentage over time",
        "shows_moisture_changes": "• Shows how moisture levels change day by day",
        "humidity_range_0_to_100": "• Values range from 0% (very dry) to 100% (very humid)",
        "higher_values_humid": "• Higher values = more humid conditions",
        "lower_values_dry": "• Lower values = drier air",
        "comfortable_range_30_60": "• Typical comfortable range is 30-60%",
        
        # Graph Information - Weather Conditions
        "conditions_what_shows": "What This Shows:",
        "pie_chart_weather_types": "• Pie chart showing percentage of different weather types",
        "based_on_search_history": "• Based on your weather search history for this city",
        "slice_represents_frequency": "• Each slice represents how often that condition occurred",
        "larger_slices_common": "• Larger slices = more common weather conditions",
        "percentages_add_to_100": "• Percentages add up to 100%",
        "reflects_search_patterns": "• Reflects the weather patterns during your searches",
        
        # Graph Information - Prediction Accuracy
        "accuracy_what_shows": "What This Shows:",
        "purple_line_accuracy": "• Purple line tracks how accurate our weather predictions have been",
        "performance_2_weeks": "• Shows prediction performance over the last 2 weeks",
        "accuracy_percentage_higher_better": "• Values represent accuracy percentage (higher = better predictions)",
        "excellent_90_plus": "• 90%+ = Excellent prediction accuracy",
        "good_75_plus": "• 75%+ = Good prediction accuracy", 
        "fair_below_60": "• Below 60% = Fair prediction accuracy",
        "reference_lines_thresholds": "• Reference lines show performance thresholds",
        
        # General Graph Information
        "weather_graph_information": "Weather Graph Information",
        "current_selection": "Current Selection",
        "select_specific_graph_info": "Select a specific graph type to see detailed information about that visualization.",
        
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
        "solar_noon": "Solar Noon",
        "status": "Status",
        "above_horizon": "Above Horizon",
        "below_horizon": "Below Horizon",
        "daytime": "Daytime",
        "nighttime": "Nighttime",
        "east": "East",
        "west": "West",
        "zenith": "Zenith",
        "sun_data": "Solar Data",
        "positions": "Positions",
        "golden_hours": "Golden Hours",
        "illumination": "Illumination",
        "cycle": "Cycle",
        "sun": "Sun",
        "moon": "Moon",
        "elevation": "Elevation",
        "azimuth": "Azimuth",
        "morning": "Morning",
        "evening": "Evening",
        
        # Moon Phases
        "new_moon": "New Moon",
        "waxing_crescent": "Waxing Crescent",
        "first_quarter": "First Quarter",
        "waxing_gibbous": "Waxing Gibbous",
        "full_moon": "Full Moon",
        "waning_gibbous": "Waning Gibbous",
        "last_quarter": "Last Quarter",
        "waning_crescent": "Waning Crescent",
        
        # Seasons
        "spring": "Spring",
        "summer": "Summer",
        "fall": "Fall",
        "winter": "Winter",
        
        # Quiz Page
        "weather_quiz_title": "Weather Quiz",
        "quiz_ready": "Quiz Ready!",
        "quiz_description": "This comprehensive weather quiz is based on meteorological data from five major global cities: Phoenix, Ahmedabad, Denver, Columbus, and Lebrija. Test your knowledge of climate patterns, temperature variations, and weather phenomena.",
        "click_start_to_begin": "Click Start to begin the quiz!",
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
        "visible": "Visible",
        "unknown": "Unknown",
        "unknown_error": "Unknown error occurred",
        "error_loading_data": "Error loading data",
        "please_try_refreshing": "Please try refreshing",
        
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
        
        # Graphs Page - Main Elements
        "weather_graphs_title": "Gráficos del Clima",
        "select_graph_type": "Seleccionar tipo de gráfico:",
        "graph_information": "Información del Gráfico",
        
        # Graph Types (for dropdown)
        "7_day_temperature_trend": "Tendencia de Temperatura de 7 Días",
        "temperature_range_chart": "Gráfico de Rango de Temperatura",
        "humidity_trends": "Tendencias de Humedad",
        "weather_conditions_distribution": "Distribución de Condiciones Climáticas",
        "prediction_accuracy_chart": "Gráfico de Precisión de Predicción",
        
        # Graph Loading and Error Messages
        "loading_graph": "📊 Cargando gráfico...\nPor favor espere mientras generamos su visualización.",
        "generating_graph": "📊 Generando gráfico...",
        "processing_data_wait": "Esto puede tomar unos momentos.\nPor favor espere mientras procesamos sus datos.",
        "error_loading_graph": "❌ Error al cargar el gráfico",
        "try_refresh_or_different_graph": "Por favor intente actualizar o seleccionar un gráfico diferente.",
        "unable_to_display_graph": "❌ No se puede mostrar el gráfico",
        "try_again_later": "Por favor intente de nuevo más tarde.",
        
        # Dependency Error Messages
        "missing_dependencies": "Dependencias Faltantes",
        "install_matplotlib": "Para usar la función de gráficos, por favor instale:",
        "restart_application": "Luego reinicie la aplicación.",
        
        # Graph Information Tooltips - Temperature Trend
        "temp_trend_what_shows": "Lo que muestra:",
        "red_line_max_temp": "• Línea roja: Temperaturas máximas diarias",
        "blue_line_min_temp": "• Línea azul: Temperaturas mínimas diarias",
        "green_line_avg_temp": "• Línea verde: Temperaturas promedio diarias",
        "data_sources": "Fuentes de Datos:",
        "primary_open_meteo": "• Primaria: API histórica del clima Open-Meteo",
        "secondary_local_history": "• Secundaria: Historial local de búsquedas del clima",
        "fallback_sample_data": "• Respaldo: Datos de muestra realistas basados en temporada y ubicación",
        "understanding_graph": "Entendiendo el Gráfico:",
        "temp_patterns_7_days": "• Muestra patrones de temperatura durante los últimos 7 días",
        "temp_displayed_celsius": "• Temperaturas mostradas en Celsius (°C)",
        "each_point_one_day": "• Cada punto representa la lectura de temperatura de un día",
        
        # Graph Information - Temperature Range
        "temp_range_what_shows": "Lo que muestra:",
        "bar_represents_daily_variation": "• Cada barra representa la variación diaria de temperatura",
        "bar_height_max_min_diff": "• Altura de barra = Temperatura máxima - Temperatura mínima",
        "shows_temp_fluctuation": "• Muestra cuánto fluctúan las temperaturas cada día",
        "higher_bars_more_variation": "• Barras más altas = más variación de temperatura ese día",
        "lower_bars_stable_temps": "• Barras más bajas = temperaturas más estables",
        "values_celsius_difference": "• Los valores muestran la diferencia en grados Celsius",
        
        # Graph Information - Humidity
        "humidity_what_shows": "Lo que muestra:",
        "green_line_humidity_percent": "• La línea verde rastrea el porcentaje de humedad a lo largo del tiempo",
        "shows_moisture_changes": "• Muestra cómo cambian los niveles de humedad día a día",
        "humidity_range_0_to_100": "• Los valores van de 0% (muy seco) a 100% (muy húmedo)",
        "higher_values_humid": "• Valores más altos = condiciones más húmedas",
        "lower_values_dry": "• Valores más bajos = aire más seco",
        "comfortable_range_30_60": "• El rango cómodo típico es 30-60%",
        
        # Graph Information - Weather Conditions
        "conditions_what_shows": "Lo que muestra:",
        "pie_chart_weather_types": "• Gráfico circular mostrando porcentaje de diferentes tipos de clima",
        "based_on_search_history": "• Basado en su historial de búsquedas del clima para esta ciudad",
        "slice_represents_frequency": "• Cada porción representa qué tan frecuente ocurrió esa condición",
        "larger_slices_common": "• Porciones más grandes = condiciones climáticas más comunes",
        "percentages_add_to_100": "• Los porcentajes suman 100%",
        "reflects_search_patterns": "• Refleja los patrones climáticos durante sus búsquedas",
        
        # Graph Information - Prediction Accuracy
        "accuracy_what_shows": "Lo que muestra:",
        "purple_line_accuracy": "• La línea púrpura rastrea qué tan precisas han sido nuestras predicciones del clima",
        "performance_2_weeks": "• Muestra el rendimiento de predicción durante las últimas 2 semanas",
        "accuracy_percentage_higher_better": "• Los valores representan porcentaje de precisión (más alto = mejores predicciones)",
        "excellent_90_plus": "• 90%+ = Excelente precisión de predicción",
        "good_75_plus": "• 75%+ = Buena precisión de predicción",
        "fair_below_60": "• Menos del 60% = Precisión de predicción regular",
        "reference_lines_thresholds": "• Las líneas de referencia muestran umbrales de rendimiento",
        
        # General Graph Information
        "weather_graph_information": "Información del Gráfico del Clima",
        "current_selection": "Selección Actual",
        "select_specific_graph_info": "Seleccione un tipo específico de gráfico para ver información detallada sobre esa visualización.",
        
        # Prediction Page
        "tomorrow_weather_prediction": "Predicción del Clima para Mañana",
        "temperature": "Temperatura",
        "accuracy": "Precisión",
        "confidence": "Confianza",
        
        # History Page
        "weather_history_title": "Historial del Clima",
        "no_history_data": "📊 Historial del Clima\n\nNo hay datos históricos disponibles para esta ubicación.\nIntenta actualizar o seleccionar una ciudad diferente.",
        
        # Sun & Moon Page
        "sun_moon_phases": "Fases del Sol y la Luna",
        "sunrise": "Amanecer",
        "sunset": "Atardecer",
        "moon_phase": "Fase Lunar",
        "moonrise": "Salida de Luna",
        "moonset": "Puesta de Luna",
        "solar_noon": "Mediodía Solar",
        "status": "Estado",
        "above_horizon": "Sobre el Horizonte",
        "below_horizon": "Bajo el Horizonte",
        "daytime": "Día",
        "nighttime": "Noche",
        "east": "Este",
        "west": "Oeste",
        "zenith": "Cenit",
        "sun_data": "Datos Solares",
        "positions": "Posiciones",
        "golden_hours": "Horas Doradas",
        "illumination": "Iluminación",
        "cycle": "Ciclo",
        "sun": "Sol",
        "moon": "Luna",
        "elevation": "Elevación",
        "azimuth": "Azimut",
        "morning": "Mañana",
        "evening": "Tarde",
        
        # Moon Phases
        "new_moon": "Luna Nueva",
        "waxing_crescent": "Luna Creciente",
        "first_quarter": "Cuarto Creciente",
        "waxing_gibbous": "Gibosa Creciente",
        "full_moon": "Luna Llena",
        "waning_gibbous": "Gibosa Menguante",
        "last_quarter": "Cuarto Menguante",
        "waning_crescent": "Luna Menguante",
        
        # Seasons
        "spring": "Primavera",
        "summer": "Verano",
        "fall": "Otoño",
        "winter": "Invierno",
        
        # Quiz Page
        "weather_quiz_title": "Quiz del Clima",
        "quiz_ready": "¡Quiz Listo!",
        "quiz_description": "Este quiz meteorológico integral está basado en datos climáticos de cinco importantes ciudades globales: Phoenix, Ahmedabad, Denver, Columbus y Lebrija. Pon a prueba tu conocimiento sobre patrones climáticos, variaciones de temperatura y fenómenos meteorológicos.",
        "click_start_to_begin": "¡Haz clic en Iniciar para comenzar el quiz!",
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
        "visible": "Visible",
        "unknown": "Desconocido",
        "unknown_error": "Error desconocido ocurrido",
        "error_loading_data": "Error al cargar datos",
        "please_try_refreshing": "Por favor, intente actualizar",
        
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
        
        # Graphs Page - Main Elements
        "weather_graphs_title": "मौसम चार्ट",
        "select_graph_type": "चार्ट प्रकार चुनें:",
        "graph_information": "चार्ट की जानकारी",
        
        # Graph Types (for dropdown)
        "7_day_temperature_trend": "७-दिन तापमान रुझान",
        "temperature_range_chart": "तापमान सीमा चार्ट",
        "humidity_trends": "आर्द्रता रुझान",
        "weather_conditions_distribution": "मौसम स्थितियों का वितरण",
        "prediction_accuracy_chart": "भविष्यवाणी सटीकता चार्ट",
        
        # Graph Loading and Error Messages
        "loading_graph": "📊 चार्ट लोड हो रहा है...\nकृपया प्रतीक्षा करें जब तक हम आपका दृश्य तैयार करते हैं।",
        "generating_graph": "📊 चार्ट बना रहे हैं...",
        "processing_data_wait": "इसमें कुछ समय लग सकता है।\nकृपया प्रतीक्षा करें जब तक हम आपका डेटा प्रोसेस करते हैं।",
        "error_loading_graph": "❌ चार्ट लोड करने में त्रुटि",
        "try_refresh_or_different_graph": "कृपया रीफ्रेश करने या एक अलग चार्ट चुनने का प्रयास करें।",
        "unable_to_display_graph": "❌ चार्ट प्रदर्शित करने में असमर्थ",
        "try_again_later": "कृपया बाद में पुनः प्रयास करें।",
        
        # Dependency Error Messages
        "missing_dependencies": "अनुपस्थित निर्भरताएं",
        "install_matplotlib": "चार्ट सुविधा का उपयोग करने के लिए, कृपया स्थापित करें:",
        "restart_application": "फिर एप्लिकेशन को पुनः आरंभ करें।",
        
        # Graph Information Tooltips - Temperature Trend
        "temp_trend_what_shows": "यह क्या दिखाता है:",
        "red_line_max_temp": "• लाल रेखा: दैनिक अधिकतम तापमान",
        "blue_line_min_temp": "• नीली रेखा: दैनिक न्यूनतम तापमान",
        "green_line_avg_temp": "• हरी रेखा: दैनिक औसत तापमान",
        "data_sources": "डेटा स्रोत:",
        "primary_open_meteo": "• प्राथमिक: ओपन-मेटिओ ऐतिहासिक मौसम एपीआई",
        "secondary_local_history": "• द्वितीयक: स्थानीय मौसम खोज इतिहास",
        "fallback_sample_data": "• बैकअप: मौसम और स्थान के आधार पर यथार्थवादी नमूना डेटा",
        "understanding_graph": "चार्ट को समझना:",
        "temp_patterns_7_days": "• पिछले 7 दिनों में तापमान पैटर्न दिखाता है",
        "temp_displayed_celsius": "• तापमान सेल्सियस (°C) में प्रदर्शित",
        "each_point_one_day": "• प्रत्येक बिंदु एक दिन की तापमान रीडिंग दर्शाता है",
        
        # Graph Information - Temperature Range
        "temp_range_what_shows": "यह क्या दिखाता है:",
        "bar_represents_daily_variation": "• प्रत्येक बार दैनिक तापमान भिन्नता दर्शाता है",
        "bar_height_max_min_diff": "• बार की ऊंचाई = अधिकतम तापमान - न्यूनतम तापमान",
        "shows_temp_fluctuation": "• दिखाता है कि प्रत्येक दिन तापमान कितना बदलता है",
        "higher_bars_more_variation": "• ऊंचे बार = उस दिन अधिक तापमान भिन्नता",
        "lower_bars_stable_temps": "• नीचे बार = अधिक स्थिर तापमान",
        "values_celsius_difference": "• मान सेल्सियस डिग्री में अंतर दिखाते हैं",
        
        # Graph Information - Humidity
        "humidity_what_shows": "यह क्या दिखाता है:",
        "green_line_humidity_percent": "• हरी रेखा समय के साथ आर्द्रता प्रतिशत को ट्रैक करती है",
        "shows_moisture_changes": "• दिखाता है कि नमी का स्तर दिन-प्रतिदिन कैसे बदलता है",
        "humidity_range_0_to_100": "• मान 0% (बहुत शुष्क) से 100% (बहुत आर्द्र) तक होते हैं",
        "higher_values_humid": "• उच्च मान = अधिक आर्द्र स्थितियां",
        "lower_values_dry": "• कम मान = सूखी हवा",
        "comfortable_range_30_60": "• सामान्य आरामदायक सीमा 30-60% है",
        
        # Graph Information - Weather Conditions
        "conditions_what_shows": "यह क्या दिखाता है:",
        "pie_chart_weather_types": "• पाई चार्ट विभिन्न मौसम प्रकारों का प्रतिशत दिखाता है",
        "based_on_search_history": "• इस शहर के लिए आपके मौसम खोज इतिहास पर आधारित",
        "slice_represents_frequency": "• प्रत्येक टुकड़ा दर्शाता है कि वह स्थिति कितनी बार हुई",
        "larger_slices_common": "• बड़े टुकड़े = अधिक सामान्य मौसम स्थितियां",
        "percentages_add_to_100": "• प्रतिशत 100% तक जोड़ते हैं",
        "reflects_search_patterns": "• आपकी खोजों के दौरान मौसम पैटर्न को दर्शाता है",
        
        # Graph Information - Prediction Accuracy
        "accuracy_what_shows": "यह क्या दिखाता है:",
        "purple_line_accuracy": "• बैंगनी रेखा ट्रैक करती है कि हमारी मौसम भविष्यवाणियां कितनी सटीक रही हैं",
        "performance_2_weeks": "• पिछले 2 सप्ताह में भविष्यवाणी प्रदर्शन दिखाता है",
        "accuracy_percentage_higher_better": "• मान सटीकता प्रतिशत दर्शाते हैं (उच्चतर = बेहतर भविष्यवाणियां)",
        "excellent_90_plus": "• 90%+ = उत्कृष्ट भविष्यवाणी सटीकता",
        "good_75_plus": "• 75%+ = अच्छी भविष्यवाणी सटीकता",
        "fair_below_60": "• 60% से कम = मध्यम भविष्यवाणी सटीकता",
        "reference_lines_thresholds": "• संदर्भ रेखाएं प्रदर्शन सीमा दिखाती हैं",
        
        # General Graph Information
        "weather_graph_information": "मौसम चार्ट की जानकारी",
        "current_selection": "वर्तमान चयन",
        "select_specific_graph_info": "उस दृश्यकरण के बारे में विस्तृत जानकारी देखने के लिए एक विशिष्ट चार्ट प्रकार चुनें।",
        
        # Prediction Page
        "tomorrow_weather_prediction": "कल के मौसम की भविष्यवाणी",
        "temperature": "तापमान",
        "accuracy": "सटीकता",
        "confidence": "विश्वास",
        
        # History Page
        "weather_history_title": "मौसम इतिहास",
        "no_history_data": "📊 मौसम इतिहास\n\nइस स्थान के लिए कोई ऐतिहासिक डेटा उपलब्ध नहीं है।\nकृपया रीफ्रेश करें या कोई अन्य शहर चुनें।",
        
        # Sun & Moon Page
        "sun_moon_phases": "सूर्य और चंद्रमा की स्थिति",
        "sunrise": "सूर्योदय",
        "sunset": "सूर्यास्त",
        "moon_phase": "चंद्र कला",
        "moonrise": "चंद्रोदय",
        "moonset": "चंद्रास्त",
        "solar_noon": "सौर मध्याह्न",
        "status": "स्थिति",
        "above_horizon": "क्षितिज के ऊपर",
        "below_horizon": "क्षितिज के नीचे",
        "daytime": "दिन का समय",
        "nighttime": "रात का समय",
        "east": "पूर्व",
        "west": "पश्चिम",
        "zenith": "शीर्ष",
        "sun_data": "सूर्य की जानकारी",
        "positions": "स्थितियाँ",
        "golden_hours": "स्वर्णिम घंटे",
        "illumination": "प्रकाश",
        "cycle": "चक्र",
        "sun": "सूर्य",
        "moon": "चंद्रमा",
        "elevation": "उन्नयन",
        "azimuth": "दिगंश",
        "morning": "सुबह",
        "evening": "शाम",
        
        # Moon Phases
        "new_moon": "अमावस्या",
        "waxing_crescent": "बढ़ता चांद",
        "first_quarter": "प्रथम चतुर्थांश",
        "waxing_gibbous": "बढ़ता पूर्ण चांद",
        "full_moon": "पूर्णिमा",
        "waning_gibbous": "घटता पूर्ण चांद",
        "last_quarter": "अंतिम चतुर्थांश",
        "waning_crescent": "घटता चांद",
        
        # Seasons
        "spring": "बसंत",
        "summer": "गर्मी",
        "fall": "शरद",
        "winter": "सर्दी",
        
        # Quiz Page
        "weather_quiz_title": "मौसम प्रश्नोत्तरी",
        "quiz_ready": "प्रश्नोत्तरी तैयार!",
        "quiz_description": "यह व्यापक मौसम प्रश्नोत्तरी पांच प्रमुख वैश्विक शहरों के मौसम विज्ञान डेटा पर आधारित है: फीनिक्स, अहमदाबाद, डेनवर, कोलंबस और लेब्रिजा। जलवायु पैटर्न, तापमान विविधताओं और मौसम घटनाओं के अपने ज्ञान का परीक्षण करें।",
        "click_start_to_begin": "प्रश्नोत्तरी शुरू करने के लिए स्टार्ट पर क्लिक करें!",
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
        "visible": "दिखाई दे रहा",
        "unknown": "अज्ञात",
        "unknown_error": "अज्ञात त्रुटि हुई",
        "error_loading_data": "डेटा लोड करने में त्रुटि",
        "please_try_refreshing": "कृपया रीफ्रेश करने का प्रयास करें",
        
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

# Supported languages with their OpenWeatherMap API codes
SUPPORTED_LANGUAGES = {
    "English": "en",
    "Spanish": "es", 
    "Hindi": "hi"
}