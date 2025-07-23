"""
Graphs Controller - Manages the graphs page logic and coordinates between GUI and data
"""

import tkinter as tk
from tkinter import ttk
import threading
import traceback

try:
    from .graph_generator import WeatherGraphGenerator
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class GraphsController:
    """
    Controller for the Weather Graphs feature
    Manages graph generation, display updates, and user interactions
    """
    
    def __init__(self, app, gui_controller):
        self.app = app
        self.gui = gui_controller
        
        if MATPLOTLIB_AVAILABLE:
            self.graph_generator = WeatherGraphGenerator(app)
        else:
            self.graph_generator = None
        
        # Available graphs
        self.graph_options = {
            "7-Day Temperature Trend": "temperature_trend",
            "Temperature Range Chart": "temperature_range",
            "Humidity Trends": "humidity_trends",
            "Weather Conditions Distribution": "conditions_distribution",
            "Prediction Accuracy Chart": "prediction_accuracy"
        }
        
        # GUI components
        self.dropdown = None
        self.graph_frame = None
        self.selected_graph = tk.StringVar(value="7-Day Temperature Trend")
        
    def build_page(self, window_width, window_height):
        """Build the graphs page"""
        try:
            self._add_back_button()
            self._build_header(window_width)
            
            if not MATPLOTLIB_AVAILABLE:
                self._show_dependency_error(window_width, window_height)
                return
            
            self._build_dropdown_selector(window_width)
            self._build_graph_display_area(window_width, window_height)
            
            # Load default graph
            self.app.after(500, self._load_selected_graph)
            
        except Exception as e:
            traceback.print_exc()
    
    def _show_dependency_error(self, window_width, window_height):
        """Show error message when matplotlib is not available"""
        error_frame = tk.Frame(
            self.app,
            bg=self._get_canvas_bg_color(),
            relief="solid",
            borderwidth=2,
            highlightthickness=0
        )
        error_frame.place(x=50, y=200, width=window_width-100, height=300)
        self.gui.widgets.append(error_frame)
        
        error_label = self._create_black_label(
            error_frame,
            text="📊 Weather Graphs Feature\n\n❌ Missing Dependencies\n\nTo use the graphs feature, please install:\n\npip3 install matplotlib numpy pandas\n\nThen restart the application.",
            font=("Arial", 16),
            x=(window_width-100)/2,
            y=150
        )
    
    def _add_back_button(self):
        """Add back button to return to main page"""
        back_btn = tk.Button(
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
        back_btn.place(x=50, y=30, anchor="center")
        self.gui.widgets.append(back_btn)
    
    def _build_header(self, window_width):
        """Build clean header with info button"""
        # Main title
        title_main = self._create_black_label(
            self.app,
            text="Weather Graphs",
            font=("Arial", int(28 + window_width/40), "bold"),
            x=window_width/2,
            y=80
        )
        self.gui.widgets.append(title_main)
        
        # Info button - moved 2 more spaces right
        info_btn = tk.Button(
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
        info_btn.place(x=window_width/2 + 240, y=80, anchor="center")
        self.gui.widgets.append(info_btn)
    
    def _build_dropdown_selector(self, window_width):
        """Build dropdown selector for graph types"""
        # Dropdown label
        dropdown_label = self._create_black_label(
            self.app,
            text="Select Graph Type:",
            font=("Arial", 16, "bold"),
            x=window_width/2 - 150,
            y=130
        )
        self.gui.widgets.append(dropdown_label)
        
        # Dropdown menu
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
    
    def _build_graph_display_area(self, window_width, window_height):
        """Build the main graph display area"""
        graph_y = 170
        graph_height = window_height - 220
        graph_width = window_width - 100
        
        # Create frame for graph with padding
        canvas_bg = self._get_canvas_bg_color()
        self.graph_frame = tk.Frame(
            self.app,
            bg=canvas_bg,
            relief="solid",
            borderwidth=2,
            highlightthickness=0
        )
        self.graph_frame.place(
            x=50,
            y=graph_y, 
            width=graph_width, 
            height=graph_height
        )
        self.gui.widgets.append(self.graph_frame)
        
        # Loading message
        loading_label = self._create_black_label(
            self.graph_frame,
            text="📊 Loading graph...\nPlease wait while we generate your visualization.",
            font=("Arial", 16),
            x=graph_width/2,
            y=graph_height/2
        )
    
    def _on_graph_selection_changed(self, event=None):
        """Handle graph selection change"""
        self._load_selected_graph()
    
    def _load_selected_graph(self):
        """Load the selected graph in background thread"""
        if not self.graph_generator:
            return
            
        selected_name = self.selected_graph.get()
        graph_type = self.graph_options.get(selected_name, "temperature_trend")
        
        # Show loading message
        self._show_loading_message()
        
        # Load graph in background thread
        threading.Thread(
            target=self._generate_graph_background,
            args=(graph_type, selected_name),
            daemon=True
        ).start()
    
    def _generate_graph_background(self, graph_type, graph_name):
        """Generate graph in background thread"""
        try:
            # Get current city
            city = self.app.city_var.get().strip() or "New York"
            
            # Generate the graph
            fig, success, error_msg = self.graph_generator.generate_graph(graph_type, city)
            
            # Update UI on main thread
            self.app.after(0, lambda: self._display_graph_result(fig, success, error_msg, graph_name))
            
        except Exception as e:
            error_msg = f"Error generating graph: {str(e)}"
            self.app.after(0, lambda: self._display_graph_result(None, False, error_msg, graph_name))
    
    def _display_graph_result(self, fig, success, error_msg, graph_name):
        """Display the graph result"""
        try:
            # Clear existing content
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            
            if success and fig:
                # Import matplotlib components
                from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
                
                # Create canvas
                canvas = FigureCanvasTkAgg(fig, self.graph_frame)
                canvas.draw()
                
                # Pack widget with padding
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
            else:
                # Show error message
                error_label = self._create_black_label(
                    self.graph_frame,
                    text=f"❌ Error loading {graph_name}\n\n{error_msg}\n\nPlease try refreshing or selecting a different graph.",
                    font=("Arial", 14),
                    x=self.graph_frame.winfo_reqwidth()/2,
                    y=self.graph_frame.winfo_reqheight()/2
                )
                
        except Exception as e:
            # Show fallback error
            fallback_label = self._create_black_label(
                self.graph_frame,
                text=f"❌ Unable to display graph\n\nError: {str(e)}\n\nPlease try again later.",
                font=("Arial", 14),
                x=200,
                y=150
            )
    
    def _show_loading_message(self):
        """Show loading message while graph generates"""
        try:
            # Clear existing content
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            
            # Show loading message
            loading_label = self._create_black_label(
                self.graph_frame,
                text="📊 Generating graph...\n\nThis may take a few moments.\nPlease wait while we process your data.",
                font=("Arial", 16),
                x=200,
                y=150
            )
            
        except Exception as e:
            pass
    
    def _show_graph_info(self):
        """Show information about the currently selected graph"""
        from tkinter import messagebox
        
        selected_graph = self.selected_graph.get()
        city = self.app.city_var.get().strip() or "New York"
        
        # Get info based on currently selected graph
        if selected_graph == "7-Day Temperature Trend":
            info_text = f"""7-Day Temperature Trend - {city}

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

        elif selected_graph == "Temperature Range Chart":
            info_text = f"""Temperature Range Chart - {city}

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

        elif selected_graph == "Humidity Trends":
            info_text = f"""Humidity Trends - {city}

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

        elif selected_graph == "Weather Conditions Distribution":
            info_text = f"""Weather Conditions Distribution - {city}

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

        elif selected_graph == "Prediction Accuracy Chart":
            info_text = f"""Prediction Accuracy Chart - {city}

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
            info_text = f"""Weather Graph Information - {city}

📊 Current Selection: {selected_graph}

📋 Data Sources:
• Real weather data from APIs when available
• Local weather search history
• Realistic sample data as fallback

Select a specific graph type to see detailed information about that visualization."""

        messagebox.showinfo("Graph Information", info_text)
    
    def _create_black_label(self, parent, text, font, x, y, anchor="center", **kwargs):
        """Create a label with black text and transparent background"""
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
    
    def _get_canvas_bg_color(self):
        """Get the current canvas background color"""
        try:
            if self.gui.bg_canvas:
                return self.gui.bg_canvas.cget("bg")
            return "#87CEEB"
        except:
            return "#87CEEB"
    
    def handle_theme_change(self):
        """Handle theme changes"""
        try:
            # Update background colors
            canvas_bg = self._get_canvas_bg_color()
            if self.graph_frame:
                self.graph_frame.configure(bg=canvas_bg)
                
        except Exception as e:
            pass
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.graph_frame:
                for widget in self.graph_frame.winfo_children():
                    widget.destroy()
            
        except Exception as e:
            pass