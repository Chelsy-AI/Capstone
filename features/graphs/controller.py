"""
Graphs Controller - Fixed Version with Enhanced Error Handling
============================================================

This controller handles the weather data visualization system with improved
error handling and font management to prevent terminal warnings.
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
    Controller for the Weather Graphs feature with enhanced error handling.
    """
    
    def __init__(self, app, gui_controller):
        """
        Initialize the graphs controller with necessary components.
        """
        # Store references to main app components
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
        
        # Define available graph types with user-friendly names
        self.graph_options = {
            "7-Day Temperature Trend": "temperature_trend",
            "Temperature Range Chart": "temperature_range", 
            "Humidity Trends": "humidity_trends",
            "Weather Conditions Distribution": "conditions_distribution",
            "Prediction Accuracy Chart": "prediction_accuracy"
        }
        
        # GUI component references - will be set when page is built
        self.dropdown: Optional[ttk.Combobox] = None
        self.graph_frame: Optional[tk.Frame] = None
        
        # Track selected graph type
        self.selected_graph = tk.StringVar(value="7-Day Temperature Trend")
        
        # Performance optimization: cache recently generated graphs
        self._graph_cache: Dict[str, Any] = {}
        self._cache_timeout = 300  # 5 minutes in seconds
    
    def _suppress_warnings(self):
        """
        Suppress matplotlib font warnings to clean up terminal output.
        """
        # Filter out matplotlib warnings about missing fonts
        warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')
        warnings.filterwarnings('ignore', message='.*Glyph.*missing from font.*')
        warnings.filterwarnings('ignore', message='.*Matplotlib currently does not support.*')
        warnings.filterwarnings('ignore', message='.*DejaVu Sans.*')
        
    def build_page(self, window_width: int, window_height: int):
        """
        Build the main graphs page interface with enhanced error handling.
        """
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
        """
        Show helpful error message when required libraries are missing.
        """
        error_frame = tk.Frame(
            self.app,
            bg=self._get_canvas_bg_color(),
            relief="solid",
            borderwidth=2,
            highlightthickness=0
        )
        error_frame.place(x=50, y=200, width=window_width-100, height=300)
        self.gui.widgets.append(error_frame)
        
        error_text = (
            "📊 Weather Graphs Feature\n\n"
            "❌ Missing Dependencies\n\n"
            "To use the graphs feature, please install:\n\n"
            "pip3 install matplotlib numpy pandas\n\n"
            "Then restart the application."
        )
        
        error_label = self._create_black_label(
            error_frame,
            text=error_text,
            font=("Arial", 16),
            x=(window_width-100)/2,
            y=150
        )
    
    def _add_back_button(self):
        """
        Add navigation back button to return to main page.
        """
        back_button = tk.Button(
            self.app,
            text="← Back",
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
        """
        Build clean page header with title and information button.
        """
        title_font_size = int(28 + window_width/40)
        
        title_main = self._create_black_label(
            self.app,
            text="Weather Graphs",
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
        """
        Build dropdown menu for selecting graph types.
        """
        dropdown_label = self._create_black_label(
            self.app,
            text="Select Graph Type:",
            font=("Arial", 16, "bold"),
            x=window_width/2 - 150,
            y=130
        )
        self.gui.widgets.append(dropdown_label)
        
        self.dropdown = ttk.Combobox(
            self.app,
            textvariable=self.selected_graph,
            values=list(self.graph_options.keys()),
            state="readonly",
            width=35,
            font=("Arial", 12)
        )
        self.dropdown.place(x=window_width/2 + 20, y=130, anchor="w")
        
        self.dropdown.bind("<<ComboboxSelected>>", self._on_graph_selection_changed)
        self.gui.widgets.append(self.dropdown)
    
    def _build_graph_display_area(self, window_width: int, window_height: int):
        """
        Build the main area where graphs will be displayed.
        """
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
        """
        Handle user selecting a different graph type from dropdown.
        """
        print(f"Graph selection changed to: {self.selected_graph.get()}")
        self._load_selected_graph()
    
    def _load_selected_graph(self):
        """
        Load and display the currently selected graph type.
        """
        if not self.graph_generator:
            print("❌ Graph generator not available")
            return
        
        selected_name = self.selected_graph.get()
        graph_type = self.graph_options.get(selected_name, "temperature_trend")
        
        print(f"Loading graph: {selected_name} (type: {graph_type})")
        
        # Check cache first
        cache_key = f"{graph_type}_{self.app.city_var.get().strip()}"
        cached_result = self._get_cached_graph(cache_key)
        
        if cached_result:
            print(f"Cached graph result for {cache_key}")
            fig, success, error_msg = cached_result
            self._display_graph_result(fig, success, error_msg, selected_name)
            return
        
        # Not in cache - show loading and generate new graph
        self._show_loading_message()
        
        # Start background graph generation
        threading.Thread(
            target=self._generate_graph_background,
            args=(graph_type, selected_name, cache_key),
            daemon=True
        ).start()
    
    def _generate_graph_background(self, graph_type: str, graph_name: str, cache_key: str):
        """
        Generate graph in background thread to prevent GUI freezing.
        """
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
        """
        Display the graph generation result in the GUI.
        """
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
        """
        Display a matplotlib figure in the tkinter GUI with error suppression.
        """
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
        """
        Display user-friendly error message when graph generation fails.
        """
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
        """
        Display fallback error message when normal error display fails.
        """
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
        """
        Show loading message while graph is being generated.
        """
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
        """
        Show detailed information about the currently selected graph.
        """
        from tkinter import messagebox
        
        selected_graph = self.selected_graph.get()
        city = self.app.city_var.get().strip() or "New York"
        
        info_text = self._get_graph_info_text(selected_graph, city)
        
        messagebox.showinfo("Graph Information", info_text)
    
    def _get_graph_info_text(self, graph_name: str, city: str) -> str:
        """
        Get detailed information text for a specific graph type.
        """
        if graph_name == "7-Day Temperature Trend":
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

        elif graph_name == "Temperature Range Chart":
            return f"""Temperature Range Chart - {city}

📊 What This Shows:
• Each bar represents the daily temperature variation
• Bar height = Maximum temperature - Minimum temperature
• Shows how much temperatures fluctuate each day

📋 Data Sources:
• Calculated from daily max and min temperatures
• Uses the same data sources as Temperature Trend
• Range values typically between 5-20°C for most locations

📈 Understanding the Graph:
• Higher bars = more temperature variation that day
• Lower bars = more stable temperatures
• Values show the difference in degrees Celsius"""

        elif graph_name == "Humidity Trends":
            return f"""Humidity Trends - {city}

📊 What This Shows:
• Green line tracks humidity percentage over time
• Shows how moisture levels change day by day
• Values range from 0% (very dry) to 100% (very humid)

📋 Data Sources:
• Your local weather search history when available
• Realistic humidity patterns based on location and season
• Updated each time you search for weather in this city

📈 Understanding the Graph:
• Higher values = more humid conditions
• Lower values = drier air
• Typical comfortable range is 30-60%"""

        elif graph_name == "Weather Conditions Distribution":
            return f"""Weather Conditions Distribution - {city}

📊 What This Shows:
• Pie chart showing percentage of different weather types
• Based on your weather search history for this city
• Each slice represents how often that condition occurred

📋 Data Sources:
• Your local weather search history
• Weather descriptions from your past searches
• Shows patterns in the weather you've experienced

📈 Understanding the Graph:
• Larger slices = more common weather conditions
• Percentages add up to 100%
• Reflects the weather patterns during your searches"""

        elif graph_name == "Prediction Accuracy Chart":
            return f"""Prediction Accuracy Chart - {city}

📊 What This Shows:
• Purple line tracks how accurate our weather predictions have been
• Shows prediction performance over the last 2 weeks
• Values represent accuracy percentage (higher = better predictions)

📋 Data Sources:
• Calculated from our prediction algorithm performance
• Based on how well predictions matched actual weather
• Updated as we make new predictions and verify results

📈 Understanding the Graph:
• 90%+ = Excellent prediction accuracy
• 75%+ = Good prediction accuracy  
• Below 60% = Fair prediction accuracy
• Reference lines show performance thresholds"""

        else:
            return f"""Weather Graph Information - {city}

📊 Current Selection: {graph_name}

📋 Data Sources:
• Real weather data from APIs when available
• Local weather search history
• Realistic sample data as fallback

Select a specific graph type to see detailed information about that visualization."""
    
    def _get_cached_graph(self, cache_key: str) -> Optional[Tuple[Any, bool, Optional[str]]]:
        """
        Get cached graph result if available and not expired.
        """
        import time
        
        if cache_key in self._graph_cache:
            cached_data, timestamp = self._graph_cache[cache_key]
            
            if time.time() - timestamp < self._cache_timeout:
                return cached_data
            else:
                del self._graph_cache[cache_key]
        
        return None
    
    def _cache_graph(self, cache_key: str, graph_data: Tuple[Any, bool, Optional[str]]):
        """
        Store graph result in cache for future use.
        """
        import time
        
        if len(self._graph_cache) >= 10:
            oldest_key = min(self._graph_cache.keys(), 
                           key=lambda k: self._graph_cache[k][1])
            del self._graph_cache[oldest_key]
        
        self._graph_cache[cache_key] = (graph_data, time.time())
        print(f"Cached graph result for {cache_key}")
    
    def clear_graph_cache(self):
        """
        Clear the graph cache to free memory or force fresh generation.
        """
        self._graph_cache.clear()
        print("Graph cache cleared")
    
    def _create_black_label(self, parent, text: str, font: tuple, x: float, y: float, 
                           anchor: str = "center", **kwargs) -> tk.Label:
        """
        Create a label with black text and transparent background.
        """
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
        """
        Get the current canvas background color for consistent theming.
        """
        try:
            if self.gui.bg_canvas:
                return self.gui.bg_canvas.cget("bg")
            return "#87CEEB"
        except:
            return "#87CEEB"
    
    def handle_theme_change(self):
        """
        Handle application theme changes by updating visual elements.
        """
        try:
            canvas_bg = self._get_canvas_bg_color()
            
            if self.graph_frame:
                self.graph_frame.configure(bg=canvas_bg)
            
            self.clear_graph_cache()
            
            print("Graphs page updated for theme change")
                
        except Exception as e:
            print(f"Error handling theme change in graphs: {e}")
    
    def cleanup(self):
        """
        Clean up resources when graphs page is closed or app shuts down.
        """
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
        """
        Get list of available graph types for external use.
        """
        return list(self.graph_options.keys())
    
    def is_graph_available(self, graph_name: str) -> bool:
        """
        Check if a specific graph type is available.
        """
        return graph_name in self.graph_options
    
    def get_dependency_status(self) -> Dict[str, Any]:
        """
        Get status information about required dependencies.
        """
        return {
            "matplotlib_available": MATPLOTLIB_AVAILABLE,
            "graph_generator_ready": self.graph_generator is not None,
            "cached_graphs": len(self._graph_cache),
            "available_graph_types": len(self.graph_options)
        }
    
    def force_refresh_current_graph(self):
        """
        Force refresh of the currently selected graph, bypassing cache.
        """
        try:
            selected_name = self.selected_graph.get()
            city = self.app.city_var.get().strip() or "New York"
            cache_key = f"{self.graph_options.get(selected_name, 'temperature_trend')}_{city}"
            
            if cache_key in self._graph_cache:
                del self._graph_cache[cache_key]
                print(f"Cleared cache for {cache_key}")
            
            self._load_selected_graph()
            
        except Exception as e:
            print(f"Error forcing graph refresh: {e}")
    
    def export_graph_info(self) -> Dict[str, Any]:
        """
        Export current graph information for sharing or debugging.
        """
        try:
            return {
                "selected_graph": self.selected_graph.get(),
                "current_city": self.app.city_var.get().strip(),
                "matplotlib_available": MATPLOTLIB_AVAILABLE,
                "cache_size": len(self._graph_cache),
                "available_options": list(self.graph_options.keys())
            }
        except Exception as e:
            return {"error": str(e)}


def check_matplotlib_dependencies() -> Tuple[bool, list]:
    """
    Check if required dependencies for graph functionality are available.
    """
    missing_packages = []
    
    try:
        import matplotlib
    except ImportError:
        missing_packages.append("matplotlib")
    
    try:
        import numpy
    except ImportError:
        missing_packages.append("numpy")
    
    try:
        import pandas
    except ImportError:
        missing_packages.append("pandas")
    
    all_available = len(missing_packages) == 0
    return all_available, missing_packages


def get_installation_instructions() -> str:
    """
    Get user-friendly installation instructions for missing dependencies.
    """
    available, missing = check_matplotlib_dependencies()
    
    if available:
        return "✓ All required dependencies are installed!"
    
    instructions = "To enable graph functionality, please install:\n\n"
    
    if "matplotlib" in missing:
        instructions += "📊 Matplotlib (for creating graphs):\n"
        instructions += "   pip install matplotlib\n\n"
    
    if "numpy" in missing:
        instructions += "🔢 NumPy (for numerical calculations):\n"
        instructions += "   pip install numpy\n\n"
    
    if "pandas" in missing:
        instructions += "📋 Pandas (for data processing):\n"
        instructions += "   pip install pandas\n\n"
    
    instructions += "Or install all at once:\n"
    instructions += "pip install matplotlib numpy pandas\n\n"
    instructions += "After installation, restart the application."
    
    return instructions