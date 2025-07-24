"""
Graphs Controller - Manages the graphs page logic and coordinates between GUI and data

This controller handles the weather data visualization system, providing interactive
charts and graphs based on real weather data. It coordinates between the graph
generator (which creates matplotlib charts) and the GUI display system.

The controller is optimized for performance and includes beginner-friendly comments
to help understand how data visualization systems work in GUI applications.
"""

import tkinter as tk
from tkinter import ttk
import threading
import traceback
from typing import Optional, Dict, Any, Tuple

try:
    from .graph_generator import WeatherGraphGenerator
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class GraphsController:
    """
    Controller for the Weather Graphs feature.
    
    This class manages the entire graph visualization experience:
    - Checking for required dependencies (matplotlib, numpy, pandas)
    - Generating different types of weather data visualizations
    - Managing graph display and user interactions
    - Providing information about available graph types
    - Handling theme changes and cleanup
    
    Think of this as the "coordinator" between data analysis and visual presentation.
    """
    
    def __init__(self, app, gui_controller):
        """
        Initialize the graphs controller with necessary components.
        
        Args:
            app: Main application object (provides GUI container and utilities)
            gui_controller: GUI management system (handles page navigation and widgets)
        """
        # Store references to main app components
        self.app = app
        self.gui = gui_controller
        
        # Initialize graph generator if matplotlib is available
        if MATPLOTLIB_AVAILABLE:
            self.graph_generator = WeatherGraphGenerator(app)
            print("✓ Graph generator initialized with matplotlib support")
        else:
            self.graph_generator = None
            print("❌ Matplotlib not available - graph features disabled")
        
        # Define available graph types with user-friendly names
        # Maps display names to internal graph type identifiers
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
        
    def build_page(self, window_width: int, window_height: int):
        """
        Build the main graphs page interface.
        
        This method creates all visual elements for the graphs page including
        navigation, controls, and the graph display area.
        
        Args:
            window_width: Width of the application window (for responsive layout)
            window_height: Height of the application window (for responsive layout)
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
            
            # Load default graph after short delay (allows GUI to finish building)
            self.app.after(500, self._load_selected_graph)
            
        except Exception as e:
            print(f"Error building graphs page: {e}")
            traceback.print_exc()
    
    def _show_dependency_error(self, window_width: int, window_height: int):
        """
        Show helpful error message when required libraries are missing.
        
        This provides clear instructions for users on how to install
        the required dependencies for graph functionality.
        
        Args:
            window_width: Window width for responsive positioning
            window_height: Window height for centering
        """
        # Create error container frame
        error_frame = tk.Frame(
            self.app,
            bg=self._get_canvas_bg_color(),
            relief="solid",
            borderwidth=2,
            highlightthickness=0
        )
        error_frame.place(x=50, y=200, width=window_width-100, height=300)
        self.gui.widgets.append(error_frame)
        
        # Detailed error message with installation instructions
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
        
        Provides consistent navigation throughout the application.
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
        
        Args:
            window_width: Window width for responsive font sizing and positioning
        """
        # Calculate responsive font size
        title_font_size = int(28 + window_width/40)
        
        # Main page title
        title_main = self._create_black_label(
            self.app,
            text="Weather Graphs",
            font=("Arial", title_font_size, "bold"),
            x=window_width/2,
            y=80
        )
        self.gui.widgets.append(title_main)
        
        # Information button for graph explanations
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
        
        Creates an intuitive interface for users to choose which type
        of weather visualization they want to see.
        
        Args:
            window_width: Window width for responsive positioning
        """
        # Label for dropdown
        dropdown_label = self._create_black_label(
            self.app,
            text="Select Graph Type:",
            font=("Arial", 16, "bold"),
            x=window_width/2 - 150,
            y=130
        )
        self.gui.widgets.append(dropdown_label)
        
        # Dropdown combobox with available graph types
        self.dropdown = ttk.Combobox(
            self.app,
            textvariable=self.selected_graph,
            values=list(self.graph_options.keys()),
            state="readonly",  # Prevent user from typing custom values
            width=35,
            font=("Arial", 12)
        )
        self.dropdown.place(x=window_width/2 + 20, y=130, anchor="w")
        
        # Bind selection change event to update graph
        self.dropdown.bind("<<ComboboxSelected>>", self._on_graph_selection_changed)
        self.gui.widgets.append(self.dropdown)
    
    def _build_graph_display_area(self, window_width: int, window_height: int):
        """
        Build the main area where graphs will be displayed.
        
        Creates a properly sized container that can hold matplotlib
        visualizations with appropriate padding and styling.
        
        Args:
            window_width: Total window width
            window_height: Total window height
        """
        # Calculate responsive dimensions
        graph_start_y = 170
        graph_height = window_height - 220  # Leave space for header and footer
        graph_width = window_width - 100    # Margins on sides
        
        # Create main graph container with styling
        canvas_bg_color = self._get_canvas_bg_color()
        self.graph_frame = tk.Frame(
            self.app,
            bg=canvas_bg_color,
            relief="solid",  # Visible border
            borderwidth=2,
            highlightthickness=0
        )
        self.graph_frame.place(
            x=50,  # Left margin
            y=graph_start_y,
            width=graph_width,
            height=graph_height
        )
        self.gui.widgets.append(self.graph_frame)
        
        # Show initial loading message
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
        
        This event handler is called whenever the user chooses a new
        graph type from the dropdown menu.
        
        Args:
            event: Tkinter event object (not used but required by binding)
        """
        print(f"Graph selection changed to: {self.selected_graph.get()}")
        self._load_selected_graph()
    
    def _load_selected_graph(self):
        """
        Load and display the currently selected graph type.
        
        This method coordinates the graph generation process by:
        - Getting the selected graph type
        - Showing a loading message
        - Starting background graph generation
        - Updating the display when complete
        """
        if not self.graph_generator:
            print("❌ Graph generator not available")
            return
        
        # Get selected graph information
        selected_name = self.selected_graph.get()
        graph_type = self.graph_options.get(selected_name, "temperature_trend")
        
        print(f"Loading graph: {selected_name} (type: {graph_type})")
        
        # Check cache first for performance optimization
        cache_key = f"{graph_type}_{self.app.city_var.get().strip()}"
        cached_result = self._get_cached_graph(cache_key)
        
        if cached_result:
            print(f"Using cached graph for {cache_key}")
            fig, success, error_msg = cached_result
            self._display_graph_result(fig, success, error_msg, selected_name)
            return
        
        # Not in cache - show loading and generate new graph
        self._show_loading_message()
        
        # Start background graph generation to keep GUI responsive
        threading.Thread(
            target=self._generate_graph_background,
            args=(graph_type, selected_name, cache_key),
            daemon=True
        ).start()
    
    def _generate_graph_background(self, graph_type: str, graph_name: str, cache_key: str):
        """
        Generate graph in background thread to prevent GUI freezing.
        
        This method runs in a separate thread so the main GUI stays responsive
        while potentially time-consuming graph generation happens.
        
        Args:
            graph_type: Internal identifier for graph type
            graph_name: User-friendly name for display
            cache_key: Key for caching the result
        """
        try:
            # Get current city for graph generation
            city = self.app.city_var.get().strip() or "New York"
            print(f"Generating {graph_type} graph for {city}")
            
            # Generate the graph using the graph generator
            fig, success, error_msg = self.graph_generator.generate_graph(graph_type, city)
            
            # Cache successful results for performance
            if success and fig:
                self._cache_graph(cache_key, (fig, success, error_msg))
            
            # Update UI on main thread (required for thread safety)
            self.app.after(0, lambda: self._display_graph_result(fig, success, error_msg, graph_name))
            
        except Exception as e:
            error_message = f"Error generating graph: {str(e)}"
            print(f"Graph generation error: {e}")
            traceback.print_exc()
            
            # Show error on main thread
            self.app.after(0, lambda: self._display_graph_result(None, False, error_message, graph_name))
    
    def _display_graph_result(self, fig, success: bool, error_msg: Optional[str], graph_name: str):
        """
        Display the graph generation result in the GUI.
        
        This method handles both successful graph display and error cases,
        providing appropriate feedback to the user.
        
        Args:
            fig: Matplotlib figure object (or None if error)
            success: Whether graph generation was successful
            error_msg: Error message if generation failed
            graph_name: User-friendly name of the graph for error messages
        """
        try:
            # Clear existing content from graph frame
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            
            if success and fig:
                # Successfully generated graph - display it
                print(f"✓ Displaying {graph_name} graph")
                self._display_matplotlib_graph(fig)
            else:
                # Error occurred - show error message
                print(f"❌ Error displaying {graph_name}: {error_msg}")
                self._display_graph_error(graph_name, error_msg)
                
        except Exception as e:
            print(f"Error in display_graph_result: {e}")
            self._display_fallback_error(str(e))
    
    def _display_matplotlib_graph(self, fig):
        """
        Display a matplotlib figure in the tkinter GUI.
        
        This method embeds the matplotlib graph into the tkinter interface
        using the FigureCanvasTkAgg backend.
        
        Args:
            fig: Matplotlib figure object to display
        """
        try:
            # Import matplotlib tkinter backend
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            # Create canvas that connects matplotlib to tkinter
            canvas = FigureCanvasTkAgg(fig, self.graph_frame)
            canvas.draw()  # Render the graph
            
            # Pack the widget with padding for nice appearance
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            print("✓ Matplotlib graph displayed successfully")
            
        except Exception as e:
            print(f"Error displaying matplotlib graph: {e}")
            self._display_fallback_error(f"Error displaying graph: {str(e)}")
    
    def _display_graph_error(self, graph_name: str, error_msg: Optional[str]):
        """
        Display user-friendly error message when graph generation fails.
        
        Args:
            graph_name: Name of the graph that failed to generate
            error_msg: Technical error message
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
            x=200,  # Reasonable default position
            y=150,
            justify="center"
        )
    
    def _display_fallback_error(self, error_msg: str):
        """
        Display fallback error message when normal error display fails.
        
        Args:
            error_msg: Error message to display
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
        
        Provides user feedback during potentially time-consuming operations.
        """
        try:
            # Clear existing content
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            
            # Show loading message with animation suggestion
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
        
        Provides educational content about what each graph shows and
        how to interpret the data visualization.
        """
        from tkinter import messagebox
        
        selected_graph = self.selected_graph.get()
        city = self.app.city_var.get().strip() or "New York"
        
        # Generate appropriate info text based on selected graph
        info_text = self._get_graph_info_text(selected_graph, city)
        
        # Display in popup dialog
        messagebox.showinfo("Graph Information", info_text)
    
    def _get_graph_info_text(self, graph_name: str, city: str) -> str:
        """
        Get detailed information text for a specific graph type.
        
        Args:
            graph_name: Name of the graph to get info for
            city: Current city for contextualized information
            
        Returns:
            Formatted information text for display
        """
        # Comprehensive information for each graph type
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
    
    # ────────────────────────────────────────────────────────────────────────────── 
    # PERFORMANCE OPTIMIZATION METHODS
    # ────────────────────────────────────────────────────────────────────────────── 
    
    def _get_cached_graph(self, cache_key: str) -> Optional[Tuple[Any, bool, Optional[str]]]:
        """
        Get cached graph result if available and not expired.
        
        This improves performance by avoiding regenerating the same graphs
        repeatedly within a short time period.
        
        Args:
            cache_key: Unique identifier for the cached graph
            
        Returns:
            Cached graph tuple (fig, success, error_msg) or None if not available
        """
        import time
        
        if cache_key in self._graph_cache:
            cached_data, timestamp = self._graph_cache[cache_key]
            
            # Check if cache is still valid (not expired)
            if time.time() - timestamp < self._cache_timeout:
                return cached_data
            else:
                # Cache expired, remove it
                del self._graph_cache[cache_key]
        
        return None
    
    def _cache_graph(self, cache_key: str, graph_data: Tuple[Any, bool, Optional[str]]):
        """
        Store graph result in cache for future use.
        
        Args:
            cache_key: Unique identifier for caching
            graph_data: Graph result tuple to cache
        """
        import time
        
        # Limit cache size to prevent memory issues
        if len(self._graph_cache) >= 10:
            # Remove oldest entry
            oldest_key = min(self._graph_cache.keys(), 
                           key=lambda k: self._graph_cache[k][1])
            del self._graph_cache[oldest_key]
        
        self._graph_cache[cache_key] = (graph_data, time.time())
        print(f"Cached graph result for {cache_key}")
    
    def clear_graph_cache(self):
        """
        Clear the graph cache to free memory or force fresh generation.
        
        Useful for debugging or when data sources have been updated.
        """
        self._graph_cache.clear()
        print("Graph cache cleared")
    
    # ────────────────────────────────────────────────────────────────────────────── 
    # GUI UTILITY METHODS
    # ────────────────────────────────────────────────────────────────────────────── 
    
    def _create_black_label(self, parent, text: str, font: tuple, x: float, y: float, 
                           anchor: str = "center", **kwargs) -> tk.Label:
        """
        Create a label with black text and transparent background.
        
        This is a utility method that creates consistently styled labels
        throughout the graphs interface.
        
        Args:
            parent: Parent widget to contain the label
            text: Text content for the label
            font: Font specification tuple (family, size, style)
            x: Horizontal position
            y: Vertical position
            anchor: Anchor point for positioning
            **kwargs: Additional label configuration options
            
        Returns:
            Created label widget
        """
        canvas_bg = self._get_canvas_bg_color()
        
        label = tk.Label(
            parent,
            text=text,
            font=font,
            fg="black",              # Always black text for readability
            bg=canvas_bg,            # Match canvas background
            anchor=anchor,
            relief="flat",           # No border
            borderwidth=0,
            highlightthickness=0,    # No focus outline
            **kwargs
        )
        
        label.place(x=x, y=y, anchor=anchor)
        return label
    
    def _get_canvas_bg_color(self) -> str:
        """
        Get the current canvas background color for consistent theming.
        
        This ensures all visual elements match the current theme.
        
        Returns:
            Hex color code for background color
        """
        try:
            if self.gui.bg_canvas:
                return self.gui.bg_canvas.cget("bg")
            return "#87CEEB"  # Default sky blue
        except:
            return "#87CEEB"  # Fallback color
    
    # ────────────────────────────────────────────────────────────────────────────── 
    # THEME AND CLEANUP MANAGEMENT
    # ────────────────────────────────────────────────────────────────────────────── 
    
    def handle_theme_change(self):
        """
        Handle application theme changes by updating visual elements.
        
        This method is called when the user switches between light and dark themes,
        ensuring the graphs page appearance stays consistent with the app theme.
        """
        try:
            # Update background colors to match new theme
            canvas_bg = self._get_canvas_bg_color()
            
            if self.graph_frame:
                self.graph_frame.configure(bg=canvas_bg)
            
            # Clear cache to force regeneration with new theme colors
            # (Future enhancement: graphs could be theme-aware)
            self.clear_graph_cache()
            
            print("Graphs page updated for theme change")
                
        except Exception as e:
            print(f"Error handling theme change in graphs: {e}")
    
    def cleanup(self):
        """
        Clean up resources when graphs page is closed or app shuts down.
        
        This method ensures proper cleanup of matplotlib figures, cached data,
        and GUI resources to prevent memory leaks.
        """
        try:
            # Clear matplotlib figures from memory
            if self.graph_frame:
                for widget in self.graph_frame.winfo_children():
                    widget.destroy()
            
            # Clear cached graphs to free memory
            self.clear_graph_cache()
            
            # Reset component references
            self.dropdown = None
            self.graph_frame = None
            
            print("Graphs controller cleanup completed")
            
        except Exception as e:
            print(f"Error during graphs cleanup: {e}")
    
    # ────────────────────────────────────────────────────────────────────────────── 
    # DEVELOPER UTILITIES AND DEBUGGING
    # ────────────────────────────────────────────────────────────────────────────── 
    
    def get_available_graph_types(self) -> list:
        """
        Get list of available graph types for external use.
        
        Useful for other parts of the application that need to know
        what graph types are available.
        
        Returns:
            List of user-friendly graph type names
        """
        return list(self.graph_options.keys())
    
    def is_graph_available(self, graph_name: str) -> bool:
        """
        Check if a specific graph type is available.
        
        Args:
            graph_name: User-friendly name of the graph type
            
        Returns:
            True if graph type is available, False otherwise
        """
        return graph_name in self.graph_options
    
    def get_dependency_status(self) -> Dict[str, Any]:
        """
        Get status information about required dependencies.
        
        Useful for debugging and system information display.
        
        Returns:
            Dictionary with dependency status information
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
        
        Useful for debugging or when data sources have been updated
        and you want to see fresh results immediately.
        """
        try:
            # Clear cache for current selection
            selected_name = self.selected_graph.get()
            city = self.app.city_var.get().strip() or "New York"
            cache_key = f"{self.graph_options.get(selected_name, 'temperature_trend')}_{city}"
            
            if cache_key in self._graph_cache:
                del self._graph_cache[cache_key]
                print(f"Cleared cache for {cache_key}")
            
            # Reload the graph
            self._load_selected_graph()
            
        except Exception as e:
            print(f"Error forcing graph refresh: {e}")
    
    def export_graph_info(self) -> Dict[str, Any]:
        """
        Export current graph information for sharing or debugging.
        
        Returns:
            Dictionary with current graph state information
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


# ────────────────────────────────────────────────────────────────────────────── 
# STANDALONE UTILITY FUNCTIONS
# ────────────────────────────────────────────────────────────────────────────── 

def check_matplotlib_dependencies() -> Tuple[bool, list]:
    """
    Check if required dependencies for graph functionality are available.
    
    This function can be called independently to verify system requirements
    before initializing the graphs controller.
    
    Returns:
        Tuple of (all_available: bool, missing_packages: list)
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
    
    Returns:
        Formatted string with installation commands
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