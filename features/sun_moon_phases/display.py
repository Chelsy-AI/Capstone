"""
Sun and Moon Phases Display Module
===========================================================
"""

import tkinter as tk
import random
from .api import get_moon_phase_emoji, format_time_for_display, calculate_golden_hour


class SunMoonDisplay:
    """
    Main class that creates and manages the sun/moon display.
    
    This class is responsible for:
    - Building the visual sky display with sun and moon positions
    - Creating organized text sections with detailed information
    - Updating the display when new data arrives
    - Managing simple animations like twinkling stars
    - Properly handling language changes for text elements
    """
    
    def __init__(self, app, gui_controller):
        """
        Initialize the sun/moon display.
        
        Args:
            app: The main weather application window
            gui_controller: Controller that manages the GUI pages
        """
        self.app = app
        self.gui = gui_controller
        
        # Animation control variables
        self.animation_running = False
        self.animation_id = None
        
        # Store references to UI elements for easy updates
        self.info_sections = {}  # Will hold our text sections
        self.day_night_label = None
        self.sun_indicator = None
        self.moon_indicator = None
        
        # Store references to direction labels for translation updates
        self.direction_labels = {}
        self.degree_labels = {}
        
        # Pre-calculate some values for better performance
        self._cached_canvas_bg = None
        self._last_window_width = 0

    def get_translated_text(self, key):
        """Get translated text from the main app's language controller."""
        try:
            if hasattr(self.app, 'gui') and hasattr(self.app.gui, 'language_controller'):
                return self.app.gui.language_controller.get_text(key)
            return key
        except:
            return key
        
    def build_sun_moon_page(self, window_width, window_height):
        """
        Build the complete sun/moon page layout.
        
        This creates:
        1. A back button to return to main page  
        2. Clean header with title and day/night status
        3. Visual sky display with sun and moon positions
        4. Organized information sections below
        
        Args:
            window_width (int): Current window width in pixels
            window_height (int): Current window height in pixels
        """
        # Cache window width for performance optimization
        self._last_window_width = window_width
        
        # Add navigation
        self._add_back_button()
        
        # Create the main header section
        self._build_clean_header(window_width)
        
        # Create the visual sky display
        self._build_celestial_display(window_width, window_height)
        
        # Create the information sections below the sky
        self._build_text_sections(window_width, window_height)
            
    def _build_clean_header(self, window_width):
        """
        Build the page header with title and day/night indicator.
        
        Args:
            window_width (int): Current window width for positioning
        """
        # Main page title - scales with window size
        title_font_size = int(28 + window_width/40)
        title_main = self._create_label(
            text=self.get_translated_text("sun_moon_phases"),
            font=("Arial", title_font_size, "bold"),
            x=window_width/2,
            y=80
        )
        self.gui.widgets.append(title_main)
        
        # Simple day/night status indicator
        status_font_size = int(16 + window_width/80)
        self.day_night_label = self._create_label(
            text="🌤️ " + self.get_translated_text("loading"),
            font=("Arial", status_font_size, "bold"),
            x=window_width/2,
            y=120
        )
        self.gui.widgets.append(self.day_night_label)
    
    def _build_celestial_display(self, window_width, window_height):
        """
        Build the visual sky display showing sun and moon positions.
        
        This creates a simplified sky view with:
        - Blue sky background
        - Clear horizon line
        - Ground area
        - Directional labels (East, West, Zenith)
        - Elevation angle markers (30°, 60°) 
        - Sun and moon position indicators
        
        Args:
            window_width (int): Window width for sizing
            window_height (int): Window height for positioning
        """
        # Calculate display dimensions and positions
        viz_y = 160  # Y position where sky starts
        viz_height = 180  # Height of the sky area
        sky_width = window_width - 160  # Leave margins on sides
        center_x = window_width // 2
        
        # Create the sky background (light blue like daytime sky)
        sky_frame = tk.Frame(
            self.app,
            height=viz_height,
            bg="#87CEEB",  # Sky blue color
            relief="solid",
            borderwidth=2
        )
        sky_frame.place(x=80, y=viz_y, width=sky_width)
        self.gui.widgets.append(sky_frame)
        
        # Create the horizon line (separates sky from ground)
        horizon_y = viz_y + viz_height - 30
        horizon_line = tk.Frame(
            self.app,
            height=4,
            bg="#8B4513",  # Brown color for earth
            relief="solid",
            borderwidth=1
        )
        horizon_line.place(x=80, y=horizon_y, width=sky_width)
        self.gui.widgets.append(horizon_line)
        
        # Create the ground area below horizon
        ground_frame = tk.Frame(
            self.app,
            height=25,
            bg="#A0522D",  # Darker brown for ground
            relief="solid",
            borderwidth=1
        )
        ground_frame.place(x=80, y=horizon_y+4, width=sky_width)
        self.gui.widgets.append(ground_frame)
        
        # Add directional labels to help users understand the view
        self._add_direction_labels(center_x, horizon_y, viz_y)
        
        # Add elevation angle reference lines and labels
        self._add_elevation_markers(sky_width, horizon_y)
        
        # Add the sun and moon indicators (will be positioned later)
        self._create_celestial_indicators(center_x, horizon_y)
        
    def _add_direction_labels(self, center_x, horizon_y, viz_y):
        """
        Add directional labels (East, West, Zenith) to help orient users.
        
        Args:
            center_x (int): Center X coordinate
            horizon_y (int): Y coordinate of horizon line
            viz_y (int): Y coordinate where sky starts
        """
        # East label (left side) - NOW TRANSLATABLE
        east_label = self._create_label(
            text=self.get_translated_text("east"),
            font=("Arial", 12, "bold"),
            x=100,
            y=horizon_y - 20
        )
        self.gui.widgets.append(east_label)
        self.direction_labels["east"] = east_label
        
        # West label (right side)
        west_label = self._create_label(
            text=self.get_translated_text("west"), 
            font=("Arial", 12, "bold"),
            x=self._last_window_width - 100,
            y=horizon_y - 20
        )
        self.gui.widgets.append(west_label)
        self.direction_labels["west"] = west_label
        
        # Zenith label (top center - highest point in sky)
        zenith_label = self._create_label(
            text=self.get_translated_text("zenith"),
            font=("Arial", 12, "bold"),
            x=center_x,
            y=viz_y + 15
        )
        self.gui.widgets.append(zenith_label)
        self.direction_labels["zenith"] = zenith_label
    
    def _add_elevation_markers(self, sky_width, horizon_y):
        """
        Add elevation angle markers to show 30° and 60° above horizon.
        
        These help users understand how high objects are in the sky.
        The degree symbols stay the same but labels are stored for consistency.
        
        Args:
            sky_width (int): Width of sky area
            horizon_y (int): Y coordinate of horizon line
        """
        # 60° elevation line (higher in sky)
        grid_60_y = horizon_y - 90
        grid_60_line = tk.Frame(
            self.app,
            height=1,
            bg="#666666",  # Gray reference line
            relief="flat"
        )
        grid_60_line.place(x=100, y=grid_60_y, width=sky_width - 40)
        self.gui.widgets.append(grid_60_line)
        
        # 60° label
        deg_60_label = self._create_label(
            text="60°",
            font=("Arial", 10),
            x=75,
            y=grid_60_y
        )
        self.gui.widgets.append(deg_60_label)
        self.degree_labels["60"] = deg_60_label
        
        # 30° elevation line (lower in sky)
        grid_30_y = horizon_y - 45
        grid_30_line = tk.Frame(
            self.app,
            height=1,
            bg="#666666",  # Gray reference line
            relief="flat"
        )
        grid_30_line.place(x=100, y=grid_30_y, width=sky_width - 40)
        self.gui.widgets.append(grid_30_line)
        
        # 30° label 
        deg_30_label = self._create_label(
            text="30°",
            font=("Arial", 10),
            x=75,
            y=grid_30_y
        )
        self.gui.widgets.append(deg_30_label)
        self.degree_labels["30"] = deg_30_label
    
    def _create_celestial_indicators(self, center_x, horizon_y):
        """
        Create the sun and moon indicator icons.
        
        These will be positioned later based on actual astronomical data.
        
        Args:
            center_x (int): Center X coordinate for initial positioning
            horizon_y (int): Horizon Y coordinate for reference
        """
        # Sun indicator (initially positioned in approximate location)
        self.sun_indicator = self._create_label(
            text="☀️",
            font=("Arial", 35),
            x=center_x - 100,  # Offset from center
            y=horizon_y - 40
        )
        self.gui.widgets.append(self.sun_indicator)
        
        # Moon indicator (initially positioned to avoid overlap with sun)
        self.moon_indicator = self._create_label(
            text="🌙",
            font=("Arial", 35),
            x=center_x + 100,  # Offset from center, opposite side from sun
            y=horizon_y - 40
        )
        self.gui.widgets.append(self.moon_indicator)
    
    def _build_text_sections(self, window_width, window_height):
        """
        Build organized information sections below the sky display.
        
        This creates a grid of information boxes showing:
        - Solar data (sunrise, sunset, solar noon)
        - Lunar data (moon phase, illumination)
        - Position data (elevation and azimuth angles)
        - Golden hour times (for photography)
        
        Args:
            window_width (int): Window width for layout calculations
            window_height (int): Window height for positioning
        """
        sections_start_y = 380  # Y coordinate where text sections begin
        
        # Calculate layout for two columns of information
        available_width = window_width - 100  # Leave margins
        section_width = available_width // 2   # Two sections per row
        
        # Column positions
        left_x = 70
        right_x = left_x + section_width + 20
        
        # Row positions
        row1_y = sections_start_y
        row2_y = sections_start_y + 120  # Space rows apart
        
        # Define the information sections to create
        sections_config = [
            ("sun_section", "☀️ " + self.get_translated_text("solar_data"), left_x, row1_y),
            ("moon_section", "🌙 " + self.get_translated_text("moon_phase"), right_x, row1_y),
            ("position_section", "🧭 " + self.get_translated_text("positions"), left_x, row2_y),
            ("time_section", "⏰ " + self.get_translated_text("golden_hours"), right_x, row2_y)
        ]
        
        # Create each information section
        for section_id, title, x, y in sections_config:
            self._create_text_section(section_id, title, x, y)
    
    def _create_text_section(self, section_id, title, x, y):
        """
        Create a single text information section.
        
        Each section has a title and content area that can be updated
        when new data arrives.
        
        Args:
            section_id (str): Unique identifier for this section
            title (str): Display title for the section
            x (int): X coordinate for positioning
            y (int): Y coordinate for positioning
        """
        # Create section title label
        title_label = self._create_label(
            text=title,
            font=("Arial", 15, "bold"),
            x=x,
            y=y,
            anchor="nw"  # Anchor to top-left for easier text layout
        )
        self.gui.widgets.append(title_label)
        
        # Create content area below the title
        content_label = self._create_label(
            text=self.get_translated_text("loading"),
            font=("Arial", 11),
            x=x,
            y=y + 25,  # Position below title
            anchor="nw",
            justify="left"  # Left-align multi-line text
        )
        self.gui.widgets.append(content_label)
        
        # Store references for easy updating later
        self.info_sections[section_id] = {
            'title': title_label,
            'content': content_label
        }
    
    def _create_label(self, text, font, x, y, anchor="center", **kwargs):
        """
        Create a text label with consistent styling.
        
        Args:
            text (str): Text to display
            font (tuple): Font specification (family, size, style)
            x (int): X coordinate
            y (int): Y coordinate  
            anchor (str): How to position the label relative to x,y
            **kwargs: Additional label options
            
        Returns:
            tk.Label: The created label widget
        """
        # Get current background color for transparency
        canvas_bg = self._get_canvas_bg_color()
        
        label = tk.Label(
            self.app,
            text=text,
            font=font,
            fg="black",  # Always use black text for readability
            bg=canvas_bg,  # Match background
            anchor=anchor,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            **kwargs
        )
        
        label.place(x=x, y=y, anchor=anchor)
        return label
    
    def update_sun_moon_display(self, sun_moon_data):
        """
        Update the entire display with new sun/moon data.
        
        Args:
            sun_moon_data (dict): Dictionary containing astronomical data
        """
        try:
            # Check if we received an error instead of data
            if sun_moon_data.get("error"):
                self._show_error_display(sun_moon_data["error"])
                return
            
            # Update the simple day/night indicator
            self._update_day_night_status(sun_moon_data)
            
            # Update positions of sun and moon in the sky display
            self._update_celestial_positions(sun_moon_data)
            
            # Update all text information sections
            self._update_text_sections(sun_moon_data)
                        
        except Exception as e:
            self._show_error_display(str(e))
    
    def _update_day_night_status(self, data):
        """
        Update the simple day/night status indicator.
        
        Args:
            data (dict): Sun/moon data containing daytime status
        """
        if self.day_night_label:
            is_daytime = data.get("is_daytime", True)
            if is_daytime:
                status_text = "☀️ " + self.get_translated_text("daytime")
            else:
                status_text = "🌙 " + self.get_translated_text("nighttime")
            
            self.day_night_label.configure(text=status_text)
    
    def _update_text_sections(self, data):
        """
        Update all text information sections with new data.
        
        This efficiently updates each section only if it exists and
        formats the data in a clean, readable way using proper translations.
        
        Args:
            data (dict): Sun/moon data dictionary
        """
        try:
            # Update sun section with solar information
            self._update_sun_section(data)
            
            # Update moon section with lunar information  
            self._update_moon_section(data)
            
            # Update position section with coordinate information
            self._update_position_section(data)
            
            # Update time section with golden hour information
            self._update_time_section(data)
            
        except Exception as e:
            pass  # Fail silently to avoid disrupting display
    
    def _update_sun_section(self, data):
        """Update the solar data section with proper translations."""
        if "sun_section" not in self.info_sections:
            return
            
        # Extract and format solar times with proper error handling
        sunrise = format_time_for_display(data.get("sunrise", "N/A"))
        sunset = format_time_for_display(data.get("sunset", "N/A"))
        solar_noon = format_time_for_display(data.get("solar_noon", "N/A"))
        
        # Determine sun status based on elevation - USING TRANSLATIONS
        sun_elevation = data.get('sun_position', {}).get('elevation', 0)
        if sun_elevation > 0:
            status = self.get_translated_text("above_horizon")
        else:
            status = self.get_translated_text("below_horizon")
        
        # Create formatted text content - ALL LABELS NOW TRANSLATED
        sun_content = (f"{self.get_translated_text('sunrise')}: {sunrise}\n"
                      f"{self.get_translated_text('sunset')}: {sunset}\n"
                      f"{self.get_translated_text('solar_noon')}: {solar_noon}\n"
                      f"{self.get_translated_text('status')}: {status}")
        
        # Update the display
        self.info_sections["sun_section"]["content"].configure(text=sun_content)
        
        # Update section title with current translation
        title_text = "☀️ " + self.get_translated_text("solar_data")
        self.info_sections["sun_section"]["title"].configure(text=title_text)
    
    def _update_moon_section(self, data):
        """Update the lunar data section with proper translations."""
        if "moon_section" not in self.info_sections:
            return
            
        # Extract and format lunar information with proper defaults
        moon_phase_name_key = data.get("moon_phase_name", "unknown")
        moon_phase_name = self.get_translated_text(moon_phase_name_key)
        moon_illumination = data.get("moon_illumination", 0)
        moon_phase = data.get("moon_phase", 0)
        moon_emoji = get_moon_phase_emoji(moon_phase)
        
        # Determine moon visibility - USING TRANSLATIONS
        moon_elevation = data.get('moon_position', {}).get('elevation', 0)
        if moon_elevation > 0:
            visibility = self.get_translated_text("visible")
        else:
            visibility = self.get_translated_text("below_horizon")
        
        # Create formatted text content - ALL LABELS NOW TRANSLATED
        moon_content = (f"{moon_emoji} {moon_phase_name}\n"
                       f"{self.get_translated_text('illumination')}: {moon_illumination:.1f}%\n"
                       f"{self.get_translated_text('cycle')}: {moon_phase:.3f}\n"
                       f"{self.get_translated_text('visibility')}: {visibility}")
        
        # Update the display
        self.info_sections["moon_section"]["content"].configure(text=moon_content)
        
        # Update section title with current translation
        title_text = "🌙 " + self.get_translated_text("moon_phase")
        self.info_sections["moon_section"]["title"].configure(text=title_text)
    
    def _update_position_section(self, data):
        """Update the position data section with proper translations."""
        if "position_section" not in self.info_sections:
            return
            
        # Extract position coordinates with defaults
        sun_pos = data.get("sun_position", {})
        moon_pos = data.get("moon_position", {})
        
        sun_elevation = sun_pos.get('elevation', 0)
        sun_azimuth = sun_pos.get('azimuth', 0)
        moon_elevation = moon_pos.get('elevation', 0)
        moon_azimuth = moon_pos.get('azimuth', 0)
        
        # Create formatted text content - ALL LABELS NOW TRANSLATED
        position_content = (f"{self.get_translated_text('sun')}: {sun_elevation:.1f}° / {sun_azimuth:.1f}°\n"
                           f"{self.get_translated_text('moon')}: {moon_elevation:.1f}° / {moon_azimuth:.1f}°\n\n"
                           f"({self.get_translated_text('elevation')} / {self.get_translated_text('azimuth')})")
        
        # Update the display
        self.info_sections["position_section"]["content"].configure(text=position_content)
        
        # Update section title with current translation
        title_text = "🧭 " + self.get_translated_text("positions")
        self.info_sections["position_section"]["title"].configure(text=title_text)
    
    def _update_time_section(self, data):
        """Update the golden hour times section with proper translations."""
        if "time_section" not in self.info_sections:
            return
            
        # Calculate golden hour times with proper error handling
        sunrise = data.get("sunrise")
        sunset = data.get("sunset")
        
        if sunrise and sunset:
            golden_hour = calculate_golden_hour(sunrise, sunset)
        else:
            golden_hour = {
                'morning_start': 'N/A',
                'morning_end': 'N/A',
                'evening_start': 'N/A',
                'evening_end': 'N/A'
            }
        
        # Create formatted text content - ALL LABELS NOW TRANSLATED
        time_content = (f"{self.get_translated_text('morning')}:\n"
                       f"{golden_hour.get('morning_start', 'N/A')} - {golden_hour.get('morning_end', 'N/A')}\n\n"
                       f"{self.get_translated_text('evening')}:\n"
                       f"{golden_hour.get('evening_start', 'N/A')} - {golden_hour.get('evening_end', 'N/A')}")
        
        # Update the display
        self.info_sections["time_section"]["content"].configure(text=time_content)
        
        # Update section title with current translation
        title_text = "⏰ " + self.get_translated_text("golden_hours")
        self.info_sections["time_section"]["title"].configure(text=title_text)
    
    def _update_celestial_positions(self, data):
        """
        Update the positions of sun and moon indicators in the sky display.
        
        This calculates where to position the sun and moon icons based on  
        their elevation and azimuth angles, ensuring they don't overlap.
        
        Args:
            data (dict): Sun/moon data with position information
        """
        try:
            # Get current window width
            window_width = self.app.winfo_width()
            if window_width <= 1:  # Window not ready yet
                return
            
            # Extract position data from the data dictionary
            sun_pos = data.get("sun_position", {})
            sun_elevation = max(0, min(90, sun_pos.get("elevation", 45)))  # Clamp between 0-90
            sun_azimuth = sun_pos.get("azimuth", 180)
            
            moon_pos = data.get("moon_position", {})
            moon_elevation = max(0, min(90, moon_pos.get("elevation", 30)))  # Clamp between 0-90
            moon_azimuth = moon_pos.get("azimuth", 90)
            
            # Calculate screen positions from astronomical coordinates
            horizon_y = 290  # Fixed Y coordinate of horizon line
            sky_height = 120  # Available vertical space in sky area
            
            # Convert elevation angle to Y position
            sun_y = horizon_y - (sun_elevation / 90) * sky_height
            moon_y = horizon_y - (moon_elevation / 90) * sky_height
            
            # Convert azimuth angle to X position (0° = North, 90° = East, etc.)
            display_width = window_width - 300  # Usable width for positioning
            sun_x = 150 + (sun_azimuth / 360) * display_width
            moon_x = 150 + (moon_azimuth / 360) * display_width
            
            # Prevent sun and moon from overlapping on screen
            min_separation = 80
            if abs(sun_x - moon_x) < min_separation:
                if moon_x > sun_x:
                    moon_x = sun_x + min_separation
                else:
                    moon_x = sun_x - min_separation
                
                # Ensure moon doesn't go off screen
                moon_x = max(150, min(moon_x, window_width - 150))
            
            # Update sun position
            if self.sun_indicator:
                self.sun_indicator.place(x=sun_x, y=sun_y, anchor="center")
            
            # Update moon position and emoji based on phase
            if self.moon_indicator:
                moon_phase = data.get("moon_phase", 0.25)
                moon_emoji = get_moon_phase_emoji(moon_phase)
                
                self.moon_indicator.configure(text=moon_emoji)
                self.moon_indicator.place(x=moon_x, y=moon_y, anchor="center")
            
        except Exception as e:
            pass  # Fail silently if positioning fails
    
    def _show_error_display(self, error_msg):
        """
        Show error message when data loading fails.
        
        Args:
            error_msg (str): Error message to display
        """
        try:
            # Update day/night label to show error
            if self.day_night_label:
                self.day_night_label.configure(text="❌ " + self.get_translated_text("error_loading_data"))
            
            # Update all information sections to show error
            error_text = (self.get_translated_text("error_loading_data") + "\n" + 
                         self.get_translated_text("please_try_refreshing"))
            
            for section_id, section_data in self.info_sections.items():
                if 'content' in section_data and section_data['content']:
                    section_data['content'].configure(text=error_text)
                    
        except Exception as e:
            pass  # Even error handling can fail
    
    def update_for_theme_change(self):
        """
        Update the display when the app theme changes.
        
        This ensures text remains readable and backgrounds match the new theme.
        """
        try:
            # Get the new background color
            canvas_bg = self._get_canvas_bg_color()
            
            # Update all text labels to use new background
            for section_id, section_data in self.info_sections.items():
                if 'title' in section_data and section_data['title']:
                    section_data['title'].configure(fg="black", bg=canvas_bg)
                if 'content' in section_data and section_data['content']:
                    section_data['content'].configure(fg="black", bg=canvas_bg)
            
            # Update day/night label
            if self.day_night_label:
                self.day_night_label.configure(fg="black", bg=canvas_bg)
            
            # Update direction labels
            for label in self.direction_labels.values():
                if label:
                    label.configure(fg="black", bg=canvas_bg)
            
            # Update degree labels
            for label in self.degree_labels.values():
                if label:
                    label.configure(fg="black", bg=canvas_bg)
                        
        except Exception as e:
            pass  # Theme updates shouldn't break the display
    
    def update_for_language_change(self):
        """
        This method updates every text element that should change with language,
        including direction labels, section titles, and content.
        """
        try:
            # Update direction labels with new translations
            if "east" in self.direction_labels and self.direction_labels["east"]:
                self.direction_labels["east"].configure(text=self.get_translated_text("east"))
            
            if "west" in self.direction_labels and self.direction_labels["west"]:
                self.direction_labels["west"].configure(text=self.get_translated_text("west"))
            
            if "zenith" in self.direction_labels and self.direction_labels["zenith"]:
                self.direction_labels["zenith"].configure(text=self.get_translated_text("zenith"))
            
            # Update section titles with new translations
            if "sun_section" in self.info_sections:
                title_text = "☀️ " + self.get_translated_text("solar_data")
                self.info_sections["sun_section"]["title"].configure(text=title_text)
            
            if "moon_section" in self.info_sections:
                title_text = "🌙 " + self.get_translated_text("moon_phase")
                self.info_sections["moon_section"]["title"].configure(text=title_text)
            
            if "position_section" in self.info_sections:
                title_text = "🧭 " + self.get_translated_text("positions")
                self.info_sections["position_section"]["title"].configure(text=title_text)
            
            if "time_section" in self.info_sections:
                title_text = "⏰ " + self.get_translated_text("golden_hours")
                self.info_sections["time_section"]["title"].configure(text=title_text)
            
            # Update day/night status if currently displayed
            if self.day_night_label:
                current_text = self.day_night_label.cget("text")
                if "☀️" in current_text:
                    self.day_night_label.configure(text="☀️ " + self.get_translated_text("daytime"))
                elif "🌙" in current_text:
                    self.day_night_label.configure(text="🌙 " + self.get_translated_text("nighttime"))
                else:
                    self.day_night_label.configure(text="🌤️ " + self.get_translated_text("loading"))
                        
        except Exception as e:
            pass  # Language updates shouldn't break the display
    
    def _get_canvas_bg_color(self):
        """
        Get the current background color from the main canvas.
        
        This allows our labels to blend in with the current theme.
        
        Returns:
            str: Background color (hex code or color name)
        """
        try:
            if hasattr(self.gui, 'bg_canvas') and self.gui.bg_canvas:
                return self.gui.bg_canvas.cget("bg")
            return "#87CEEB"  # Default sky blue if canvas not available
        except:
            return "#87CEEB"  # Safe fallback color
    
    def _add_back_button(self):
        """
        Add a back button to return to the main weather page.
        
        This provides easy navigation back to the main application.
        """
        # Get the translated "back" text and ensure no extra arrows
        back_text = self.get_translated_text("back")
        
        # Remove any existing arrows from the translated text
        back_text = back_text.replace("←", "").replace("→", "").strip()
        
        # Create button text with single arrow
        button_text = f"← {back_text}"
        
        back_btn = tk.Button(
            self.app,
            text=button_text,  # Controlled button text
            command=self._handle_back_button_click,
            bg="grey",
            fg="black", 
            font=("Arial", 12, "bold"),
            relief="raised",
            borderwidth=2,
            width=8,
            height=1,
            activeforeground="black",
            activebackground="lightgrey",
            highlightthickness=0,
            cursor="hand2"  # Show pointer cursor on hover
        )
        back_btn.place(x=50, y=30, anchor="center")
        self.gui.widgets.append(back_btn)
    
    def _handle_back_button_click(self):
        """
        Handle back button click with proper cleanup.
        
        This ensures animations are stopped and resources are cleaned up
        before navigating back to the main page.
        """
        try:
            # Stop any running animations before leaving
            self.stop_celestial_animation()
            
            # Navigate back to main page
            if hasattr(self.gui, 'show_page'):
                self.gui.show_page("main")
            
        except Exception as e:
            # If navigation fails, try direct fallback
            pass
    
    def start_celestial_animation(self):
        """
        Start simple background animations like twinkling stars.
        
        This adds a bit of visual interest without being distracting.
        """
        try:
            if not self.animation_running:
                self.animation_running = True
                self._animate_celestial_background()
        except Exception as e:
            pass  # Animation is optional, don't break if it fails
    
    def stop_celestial_animation(self):
        """
        Stop all background animations.
        
        This is called when leaving the page or closing the app.
        """
        try:
            self.animation_running = False
            if self.animation_id:
                self.app.after_cancel(self.animation_id)
                self.animation_id = None
        except Exception as e:
            pass
    
    def _animate_celestial_background(self):
        """
        Create simple twinkling star effects in the background.
        
        This runs periodically to add/remove stars for a subtle animation effect.
        """
        if not self.animation_running:
            return
        
        try:
            # Only animate if we have access to the background canvas
            if hasattr(self.gui, 'bg_canvas') and self.gui.bg_canvas:
                self._add_simple_stars()
            
            # Schedule next animation frame (every 4 seconds for subtle effect)
            self.animation_id = self.app.after(4000, self._animate_celestial_background)
            
        except Exception as e:
            pass  # Don't let animation errors break the display
    
    def _add_simple_stars(self):
        """
        Add simple star effects to the background canvas.
        
        This creates small white dots that appear randomly in the upper part
        of the display to simulate twinkling stars.
        """
        try:
            canvas = self.gui.bg_canvas
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            # Validate canvas dimensions
            if width <= 1 or height <= 1:
                return
            
            # Remove any existing stars to prevent accumulation
            canvas.delete("star")
            
            # Add a small random number of stars
            num_stars = random.randint(3, 8)
            for _ in range(num_stars):
                # Position stars in upper portion of screen (sky area)
                x = random.randint(100, width - 100)
                y = random.randint(50, height//2)
                
                # Create small white star dots
                canvas.create_oval(
                    x - 1, y - 1, x + 1, y + 1,
                    fill="white", outline="", tags="star"
                )
            
        except Exception as e:
            pass  # Animation failures shouldn't affect main functionality
    
    def cleanup(self):
        """Clean up resources when the display is no longer needed."""
        try:
            # Stop any running animations
            self.stop_celestial_animation()
            
            # Clear stored references to UI elements
            self.info_sections.clear()
            self.direction_labels.clear()
            self.degree_labels.clear()
            self.day_night_label = None
            self.sun_indicator = None
            self.moon_indicator = None
            
            # Clear cache
            self._cached_canvas_bg = None
            
        except Exception as e:
            pass  # Cleanup should never raise exceptions
        