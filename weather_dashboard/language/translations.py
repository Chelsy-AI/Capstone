"""
Language Translations Data
========================================================================

Contains all translation data for the weather application.
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
        "city_comparison": "City Comparison",

        # City Comparison Page
        "city_comparison_title": "City Weather Comparison",
        "comparison_instructions": "Compare weather conditions between two cities",
        "city_1": "City 1",
        "city_2": "City 2",
        "compare_cities": "Compare Cities",
        "comparison_placeholder": "Enter two cities above and click Compare to see side-by-side weather data",
        "loading_comparison": "📊 Loading comparison data...\nPlease wait while we fetch weather for both cities.",
        "comparison_error": "Unable to compare cities. Please check city names and try again.",

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
        "percent": "%",

        # Map Controls and Interface
        "weather_overlay": "Weather Overlay:",
        "weather_overlay_select": "Select Weather Overlay",
        "map_controls": "Map Controls",
        "zoom_in": "Zoom In",
        "zoom_out": "Zoom Out",
        "reset_view": "Reset View",
        "current_location": "Current Location",
        
        # Weather Overlay Types
        "overlay_none": "No Overlay",
        "overlay_temperature": "Temperature",
        "overlay_wind": "Wind Speed",
        "overlay_precipitation": "Precipitation",
        "overlay_clouds": "Cloud Cover",
        "overlay_pressure": "Atmospheric Pressure",
        "overlay_snow": "Snow Cover",
        "overlay_dewpoint": "Dew Point",
        
        # Map Information Panel
        "map_information": "Map Information",
        "base_map_info": "Base Map Information",
        "base_map_description": "Interactive map with city location markers and weather overlays",
        "map_features": "Map Features:",
        "feature_navigation": "• Interactive navigation with zoom and pan controls",
        "feature_overlays": "• Multiple weather overlay options available",
        "feature_tracking": "• Real-time city location tracking with GPS coordinates",
        "feature_integration": "• Custom weather data visualization integration",
        "feature_geocoding": "• Automatic city name to coordinates conversion",
        "feature_markers": "• Dynamic location markers for selected cities",
        "feature_updates": "• Live weather data refresh functionality",
        "feature_basemap": "• High-quality OpenStreetMap base tiles",
        
        # Weather Overlay Information
        "overlay_information": "Weather Overlay Information",
        "current_overlay": "Current Overlay",
        "overlay_description": "Overlay Description",
        "no_overlay_selected": "No weather overlay currently selected",
        "select_overlay_for_info": "Select a weather overlay to see detailed information about that data layer.",
        
        # Individual Overlay Descriptions
        "temperature_overlay_info": "Temperature Overlay",
        "temperature_overlay_desc": "Shows real-time temperature data across the map region. Warmer areas appear in red/orange, cooler areas in blue. Data refreshes automatically with weather updates.",
        "temperature_overlay_features": "• Color-coded temperature visualization\n• Real-time data from weather stations\n• Celsius/Fahrenheit display options\n• High-resolution thermal mapping",
        
        "wind_overlay_info": "Wind Speed Overlay",
        "wind_overlay_desc": "Displays wind speed patterns and directions across the region. Shows both wind velocity and directional flow patterns for weather analysis.",
        "wind_overlay_features": "• Wind speed intensity mapping\n• Directional flow indicators\n• Real-time wind pattern updates\n• Storm system tracking capabilities",
        
        "precipitation_overlay_info": "Precipitation Overlay",
        "precipitation_overlay_desc": "Shows current and forecast precipitation including rain, snow, and other forms of moisture. Intensity levels are color-coded for easy interpretation.",
        "precipitation_overlay_features": "• Real-time precipitation tracking\n• Intensity level color coding\n• Rain and snow differentiation\n• Forecast precipitation zones",
        
        "clouds_overlay_info": "Cloud Cover Overlay",
        "clouds_overlay_desc": "Displays cloud coverage patterns and density across the map area. Shows both current conditions and cloud movement patterns.",
        "clouds_overlay_features": "• Cloud density visualization\n• Coverage percentage mapping\n• Satellite-based cloud data\n• Clear sky identification zones",
        
        "pressure_overlay_info": "Atmospheric Pressure Overlay",
        "pressure_overlay_desc": "Shows atmospheric pressure variations across the region. High and low pressure systems are clearly marked for weather pattern analysis.",
        "pressure_overlay_features": "• Pressure system visualization\n• High/low pressure identification\n• Isobar mapping display\n• Weather front tracking",
        
        "snow_overlay_info": "Snow Cover Overlay",
        "snow_overlay_desc": "Displays snow coverage and accumulation data. Shows both current snow depth and forecast snowfall patterns for winter weather planning.",
        "snow_overlay_features": "• Snow depth visualization\n• Accumulation forecasting\n• Winter storm tracking\n• Ski condition monitoring",
        
        "dewpoint_overlay_info": "Dew Point Overlay",
        "dewpoint_overlay_desc": "Shows dew point temperatures across the map region. Indicates humidity comfort levels and potential for fog or moisture formation.",
        "dewpoint_overlay_features": "• Humidity comfort mapping\n• Fog formation prediction\n• Moisture level visualization\n• Air quality correlation data",
        
        # Map Error Messages
        "map_loading_error": "Error loading map",
        "overlay_loading_error": "Error loading weather overlay",
        "location_not_found": "Location not found on map",
        "geocoding_failed": "Failed to find city coordinates",
        "tile_server_error": "Weather tile server unavailable",
        "map_refresh_failed": "Failed to refresh map data",
        
        # Map Status Messages
        "map_loading": "Loading interactive map...",
        "overlay_loading": "Loading weather overlay...",
        "geocoding_city": "Finding city location...",
        "updating_location": "Updating map location...",
        "refreshing_data": "Refreshing weather data...",

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
        "city_comparison": "Comparación de Ciudades",
        
        # City Comparison Page - CORRECTED
        "city_comparison_title": "Comparación del Clima entre Ciudades",
        "comparison_instructions": "Compara las condiciones meteorológicas entre dos ciudades",
        "city_1": "Ciudad 1",
        "city_2": "Ciudad 2",
        "compare_cities": "Comparar Ciudades",
        "comparison_placeholder": "Ingresa dos ciudades arriba y haz clic en Comparar para ver los datos meteorológicos lado a lado",
        "loading_comparison": "📊 Cargando datos de comparación...\nPor favor espera mientras obtenemos el clima de ambas ciudades.",
        "comparison_error": "No se pueden comparar las ciudades. Por favor verifica los nombres de las ciudades e intenta de nuevo.",

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
        
        # Weather Conditions - CORRECTED
        "clear_sky": "Cielo despejado",
        "few_clouds": "Pocas nubes",
        "scattered_clouds": "Nubes dispersas",
        "broken_clouds": "Nubes fragmentadas",
        "overcast_clouds": "Cielo nublado",
        "shower_rain": "Lluvia ligera",
        "rain": "Lluvia",
        "light_rain": "Lluvia ligera",
        "moderate_rain": "Lluvia moderada",
        "heavy_rain": "Lluvia intensa",
        "thunderstorm": "Tormenta",
        "snow": "Nieve",
        "light_snow": "Nevada ligera",
        "mist": "Neblina",
        "fog": "Niebla",
        "haze": "Bruma",
        
        # Units
        "celsius": "°C",
        "fahrenheit": "°F",
        "kmh": "km/h",
        "ms": "m/s",
        "hpa": "hPa",
        "meters": "m",
        "mm": "mm",
        "percent": "%",

        # Map Controls and Interface
        "weather_overlay": "Superposición del Clima:",
        "weather_overlay_select": "Seleccionar Superposición del Clima",
        "map_controls": "Controles del Mapa",
        "zoom_in": "Acercar",
        "zoom_out": "Alejar",
        "reset_view": "Restablecer Vista",
        "current_location": "Ubicación Actual",
        
        # Weather Overlay Types
        "overlay_none": "Sin Superposición",
        "overlay_temperature": "Temperatura",
        "overlay_wind": "Velocidad del Viento",
        "overlay_precipitation": "Precipitación",
        "overlay_clouds": "Cobertura de Nubes",
        "overlay_pressure": "Presión Atmosférica",
        "overlay_snow": "Cobertura de Nieve",
        "overlay_dewpoint": "Punto de Rocío",
        
        # Map Information Panel
        "map_information": "Información del Mapa",
        "base_map_info": "Información del Mapa Base",
        "base_map_description": "Mapa interactivo con marcadores de ubicación de ciudades y superposiciones meteorológicas",
        "map_features": "Características del Mapa:",
        "feature_navigation": "• Navegación interactiva con controles de zoom y desplazamiento",
        "feature_overlays": "• Múltiples opciones de superposición meteorológica disponibles",
        "feature_tracking": "• Seguimiento de ubicación de ciudad en tiempo real con coordenadas GPS",
        "feature_integration": "• Integración personalizada de visualización de datos meteorológicos",
        "feature_geocoding": "• Conversión automática de nombre de ciudad a coordenadas",
        "feature_markers": "• Marcadores de ubicación dinámicos para ciudades seleccionadas",
        "feature_updates": "• Funcionalidad de actualización de datos meteorológicos en vivo",
        "feature_basemap": "• Tiles base de OpenStreetMap de alta calidad",
        
        # Weather Overlay Information
        "overlay_information": "Información de Superposición Meteorológica",
        "current_overlay": "Superposición Actual",
        "overlay_description": "Descripción de Superposición",
        "no_overlay_selected": "No hay superposición meteorológica seleccionada actualmente",
        "select_overlay_for_info": "Seleccione una superposición meteorológica para ver información detallada sobre esa capa de datos.",
        
        # Individual Overlay Descriptions
        "temperature_overlay_info": "Superposición de Temperatura",
        "temperature_overlay_desc": "Muestra datos de temperatura en tiempo real en toda la región del mapa. Las áreas más cálidas aparecen en rojo/naranja, las áreas más frías en azul. Los datos se actualizan automáticamente con las actualizaciones meteorológicas.",
        "temperature_overlay_features": "• Visualización de temperatura codificada por colores\n• Datos en tiempo real de estaciones meteorológicas\n• Opciones de visualización Celsius/Fahrenheit\n• Mapeo térmico de alta resolución",
        
        "wind_overlay_info": "Superposición de Velocidad del Viento",
        "wind_overlay_desc": "Muestra patrones de velocidad y dirección del viento en toda la región. Muestra tanto la velocidad del viento como los patrones de flujo direccional para análisis meteorológico.",
        "wind_overlay_features": "• Mapeo de intensidad de velocidad del viento\n• Indicadores de flujo direccional\n• Actualizaciones de patrones de viento en tiempo real\n• Capacidades de seguimiento de sistemas de tormenta",
        
        "precipitation_overlay_info": "Superposición de Precipitación",
        "precipitation_overlay_desc": "Muestra precipitación actual y pronosticada incluyendo lluvia, nieve y otras formas de humedad. Los niveles de intensidad están codificados por colores para fácil interpretación.",
        "precipitation_overlay_features": "• Seguimiento de precipitación en tiempo real\n• Codificación de colores de nivel de intensidad\n• Diferenciación de lluvia y nieve\n• Zonas de precipitación pronosticada",
        
        "clouds_overlay_info": "Superposición de Cobertura de Nubes",
        "clouds_overlay_desc": "Muestra patrones de cobertura de nubes y densidad en toda el área del mapa. Muestra tanto las condiciones actuales como los patrones de movimiento de nubes.",
        "clouds_overlay_features": "• Visualización de densidad de nubes\n• Mapeo de porcentaje de cobertura\n• Datos de nubes basados en satélite\n• Zonas de identificación de cielo despejado",
        
        "pressure_overlay_info": "Superposición de Presión Atmosférica",
        "pressure_overlay_desc": "Muestra variaciones de presión atmosférica en toda la región. Los sistemas de alta y baja presión están claramente marcados para análisis de patrones meteorológicos.",
        "pressure_overlay_features": "• Visualización de sistemas de presión\n• Identificación de presión alta/baja\n• Visualización de mapeo de isobaras\n• Seguimiento de frentes meteorológicos",
        
        "snow_overlay_info": "Superposición de Cobertura de Nieve",
        "snow_overlay_desc": "Muestra datos de cobertura y acumulación de nieve. Muestra tanto la profundidad actual de nieve como los patrones de nevada pronosticados para planificación meteorológica invernal.",
        "snow_overlay_features": "• Visualización de profundidad de nieve\n• Pronóstico de acumulación\n• Seguimiento de tormentas invernales\n• Monitoreo de condiciones de esquí",
        
        "dewpoint_overlay_info": "Superposición de Punto de Rocío",
        "dewpoint_overlay_desc": "Muestra temperaturas de punto de rocío en toda la región del mapa. Indica niveles de comodidad de humedad y potencial para formación de niebla o humedad.",
        "dewpoint_overlay_features": "• Mapeo de comodidad de humedad\n• Predicción de formación de niebla\n• Visualización de nivel de humedad\n• Datos de correlación de calidad del aire",
        
        # Map Error Messages
        "map_loading_error": "Error al cargar el mapa",
        "overlay_loading_error": "Error al cargar la superposición meteorológica",
        "location_not_found": "Ubicación no encontrada en el mapa",
        "geocoding_failed": "Falló al encontrar coordenadas de la ciudad",
        "tile_server_error": "Servidor de tiles meteorológicos no disponible",
        "map_refresh_failed": "Falló al actualizar datos del mapa",
        
        # Map Status Messages
        "map_loading": "Cargando mapa interactivo...",
        "overlay_loading": "Cargando superposición meteorológica...",
        "geocoding_city": "Encontrando ubicación de la ciudad...",
        "updating_location": "Actualizando ubicación del mapa...",
        "refreshing_data": "Actualizando datos meteorológicos...",

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
        "city_comparison": "शहर तुलना",
        
        # City Comparison Page - CORRECTED
        "city_comparison_title": "शहरों की मौसम तुलना",
        "comparison_instructions": "दो शहरों के बीच मौसम की स्थिति की तुलना करें",
        "city_1": "शहर 1",
        "city_2": "शहर 2",
        "compare_cities": "शहरों की तुलना करें",
        "comparison_placeholder": "ऊपर दो शहर दर्ज करें और साइड-बाई-साइड मौसम डेटा देखने के लिए तुलना पर क्लिक करें",
        "loading_comparison": "📊 तुलना डेटा लोड हो रहा है...\nकृपया प्रतीक्षा करें जब तक हम दोनों शहरों का मौसम प्राप्त करते हैं।",
        "comparison_error": "शहरों की तुलना करने में असमर्थ। कृपया शहर के नाम जांचें और पुनः प्रयास करें।",

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
        
        # Weather Conditions - CORRECTED AND COMPLETE
        "clear_sky": "साफ आकाश",
        "clear": "साफ",
        "few_clouds": "कुछ बादल",
        "scattered_clouds": "बिखरे हुए बादल",
        "broken_clouds": "टूटे हुए बादल",
        "overcast_clouds": "घने बादल",
        "overcast": "बादल छाए हुए",
        "shower_rain": "हल्की बारिश",
        "rain": "बारिश",
        "light_rain": "हल्की बारिश",
        "moderate_rain": "मध्यम बारिश",
        "heavy_rain": "भारी बारिश",
        "drizzle": "फुहार",
        "light_intensity_drizzle": "हल्की फुहार",
        "thunderstorm": "तूफान",
        "thunderstorm_with_light_rain": "हल्की बारिश के साथ तूफान",
        "thunderstorm_with_rain": "बारिश के साथ तूफान",
        "thunderstorm_with_heavy_rain": "भारी बारिश के साथ तूफान",
        "snow": "बर्फ",
        "light_snow": "हल्की बर्फबारी",
        "heavy_snow": "भारी बर्फबारी",
        "sleet": "ओलावृष्टि",
        "mist": "कोहरा",
        "fog": "धुंध",
        "haze": "धुंध",
        "smoke": "धुआं",
        "sand": "रेत की आंधी",
        "dust": "धूल",
        "tornado": "बवंडर",
        "squall": "तेज हवा",
        
        # Detailed weather descriptions that might come from API
        "light_intensity_shower_rain": "हल्की बारिश की बौछार",
        "shower_rain": "बारिश की बौछार",
        "heavy_intensity_shower_rain": "भारी बारिश की बौछार",
        "ragged_shower_rain": "अनियमित बारिश",
        "light_intensity_drizzle_rain": "हल्की फुहार के साथ बारिश",
        "drizzle_rain": "फुहार के साथ बारिश",
        "heavy_intensity_drizzle_rain": "भारी फुहार के साथ बारिश",
        "shower_rain_and_drizzle": "बौछार और फुहार",
        "heavy_shower_rain_and_drizzle": "भारी बौछार और फुहार",
        "shower_drizzle": "फुहार की बौछार",
        
        # Units
        "celsius": "°से",
        "fahrenheit": "°फा", 
        "kmh": "किमी/घं",
        "ms": "मी/से",
        "hpa": "एचपीए",
        "meters": "मी",
        "mm": "मिमी",
        "percent": "%",

        # Map Controls and Interface
        "weather_overlay": "मौसम आवरण:",
        "weather_overlay_select": "मौसम आवरण चुनें",
        "map_controls": "मानचित्र नियंत्रण",
        "zoom_in": "ज़ूम इन",
        "zoom_out": "ज़ूम आउट",
        "reset_view": "दृश्य रीसेट करें",
        "current_location": "वर्तमान स्थान",
        
        # Weather Overlay Types
        "overlay_none": "कोई आवरण नहीं",
        "overlay_temperature": "तापमान",
        "overlay_wind": "हवा की गति",
        "overlay_precipitation": "वर्षा",
        "overlay_clouds": "बादल आवरण",
        "overlay_pressure": "वायुमंडलीय दबाव",
        "overlay_snow": "बर्फ आवरण",
        "overlay_dewpoint": "ओस बिंदु",
        
        # Map Information Panel
        "map_information": "मानचित्र जानकारी",
        "base_map_info": "बेस मानचित्र जानकारी",
        "base_map_description": "शहर स्थान मार्कर और मौसम आवरण के साथ इंटरैक्टिव मानचित्र",
        "map_features": "मानचित्र विशेषताएं:",
        "feature_navigation": "• ज़ूम और पैन नियंत्रण के साथ इंटरैक्टिव नेवीगेशन",
        "feature_overlays": "• कई मौसम आवरण विकल्प उपलब्ध",
        "feature_tracking": "• GPS निर्देशांक के साथ रीयल-टाइम शहर स्थान ट्रैकिंग",
        "feature_integration": "• कस्टम मौसम डेटा विज़ुअलाइज़ेशन एकीकरण",
        "feature_geocoding": "• शहर के नाम से निर्देशांक में स्वचालित रूपांतरण",
        "feature_markers": "• चयनित शहरों के लिए डायनामिक स्थान मार्कर",
        "feature_updates": "• लाइव मौसम डेटा रिफ्रेश कार्यक्षमता",
        "feature_basemap": "• उच्च गुणवत्ता OpenStreetMap बेस टाइल्स",
        
        # Weather Overlay Information
        "overlay_information": "मौसम आवरण जानकारी",
        "current_overlay": "वर्तमान आवरण",
        "overlay_description": "आवरण विवरण",
        "no_overlay_selected": "वर्तमान में कोई मौसम आवरण चयनित नहीं है",
        "select_overlay_for_info": "उस डेटा परत के बारे में विस्तृत जानकारी देखने के लिए मौसम आवरण चुनें।",
        
        # Individual Overlay Descriptions
        "temperature_overlay_info": "तापमान आवरण",
        "temperature_overlay_desc": "मानचित्र क्षेत्र में रीयल-टाइम तापमान डेटा दिखाता है। गर्म क्षेत्र लाल/नारंगी में दिखाई देते हैं, ठंडे क्षेत्र नीले में। डेटा मौसम अपडेट के साथ स्वचालित रूप से रीफ्रेश होता है।",
        "temperature_overlay_features": "• रंग-कोडित तापमान विज़ुअलाइज़ेशन\n• मौसम स्टेशनों से रीयल-टाइम डेटा\n• सेल्सियस/फारेनहाइट प्रदर्शन विकल्प\n• उच्च-रिज़ॉल्यूशन थर्मल मैपिंग",
        
        "wind_overlay_info": "हवा की गति आवरण",
        "wind_overlay_desc": "क्षेत्र में हवा की गति पैटर्न और दिशा प्रदर्शित करता है। मौसम विश्लेषण के लिए हवा की गति और दिशात्मक प्रवाह पैटर्न दोनों दिखाता है।",
        "wind_overlay_features": "• हवा की गति तीव्रता मैपिंग\n• दिशात्मक प्रवाह संकेतक\n• रीयल-टाइम हवा पैटर्न अपडेट\n• तूफान प्रणाली ट्रैकिंग क्षमताएं",
        
        "precipitation_overlay_info": "वर्षा आवरण",
        "precipitation_overlay_desc": "वर्तमान और पूर्वानुमानित वर्षा दिखाता है जिसमें बारिश, बर्फ और नमी के अन्य रूप शामिल हैं। तीव्रता के स्तर आसान व्याख्या के लिए रंग-कोडित हैं।",
        "precipitation_overlay_features": "• रीयल-टाइम वर्षा ट्रैकिंग\n• तीव्रता स्तर रंग कोडिंग\n• बारिश और बर्फ अंतर\n• पूर्वानुमानित वर्षा क्षेत्र",
        
        "clouds_overlay_info": "बादल आवरण आवरण",
        "clouds_overlay_desc": "मानचित्र क्षेत्र में बादल आवरण पैटर्न और घनत्व प्रदर्शित करता है। वर्तमान स्थितियों और बादल गति पैटर्न दोनों दिखाता है।",
        "clouds_overlay_features": "• बादल घनत्व विज़ुअलाइज़ेशन\n• कवरेज प्रतिशत मैपिंग\n• उपग्रह-आधारित बादल डेटा\n• साफ आकाश पहचान क्षेत्र",
        
        "pressure_overlay_info": "वायुमंडलीय दबाव आवरण",
        "pressure_overlay_desc": "क्षेत्र में वायुमंडलीय दबाव भिन्नताएं दिखाता है। मौसम पैटर्न विश्लेषण के लिए उच्च और निम्न दबाव प्रणालियां स्पष्ट रूप से चिह्नित हैं।",
        "pressure_overlay_features": "• दबाव प्रणाली विज़ुअलाइज़ेशन\n• उच्च/निम्न दबाव पहचान\n• आइसोबार मैपिंग प्रदर्शन\n• मौसम मोर्चा ट्रैकिंग",
        
        "snow_overlay_info": "बर्फ आवरण आवरण",
        "snow_overlay_desc": "बर्फ कवरेज और संचय डेटा प्रदर्शित करता है। शीतकालीन मौसम योजना के लिए वर्तमान बर्फ की गहराई और पूर्वानुमानित हिमपात पैटर्न दोनों दिखाता है।",
        "snow_overlay_features": "• बर्फ की गहराई विज़ुअलाइज़ेशन\n• संचय पूर्वानुमान\n• शीतकालीन तूफान ट्रैकिंग\n• स्की स्थिति मॉनिटरिंग",
        
        "dewpoint_overlay_info": "ओस बिंदु आवरण",
        "dewpoint_overlay_desc": "मानचित्र क्षेत्र में ओस बिंदु तापमान दिखाता है। आर्द्रता आराम स्तर और कोहरे या नमी गठन की संभावना का संकेत देता है।",
        "dewpoint_overlay_features": "• आर्द्रता आराम मैपिंग\n• कोहरा गठन भविष्यवाणी\n• नमी स्तर विज़ुअलाइज़ेशन\n• वायु गुणवत्ता सहसंबंध डेटा",
        
        # Map Error Messages
        "map_loading_error": "मानचित्र लोड करने में त्रुटि",
        "overlay_loading_error": "मौसम आवरण लोड करने में त्रुटि",
        "location_not_found": "मानचित्र पर स्थान नहीं मिला",
        "geocoding_failed": "शहर के निर्देशांक खोजने में विफल",
        "tile_server_error": "मौसम टाइल सर्वर अनुपलब्ध",
        "map_refresh_failed": "मानचित्र डेटा रिफ्रेश करने में विफल",
        
        # Map Status Messages
        "map_loading": "इंटरैक्टिव मानचित्र लोड हो रहा है...",
        "overlay_loading": "मौसम आवरण लोड हो रहा है...",
        "geocoding_city": "शहर का स्थान खोज रहे हैं...",
        "updating_location": "मानचित्र स्थान अपडेट कर रहे हैं...",
        "refreshing_data": "मौसम डेटा रिफ्रेश कर रहे हैं...",
    
    }
}

# Supported languages with their OpenWeatherMap API codes
SUPPORTED_LANGUAGES = {
    "English": "en",
    "Spanish": "es", 
    "Hindi": "hi"
}