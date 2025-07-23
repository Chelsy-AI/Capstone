"""
Sun and Moon Phases Display Module - COMPLETELY FIXED
NO MORE LONG DATE/TIME LINE - ONLY HEADING AND DAY/NIGHT
"""

import tkinter as tk
import math
import random
from .api import get_moon_phase_emoji, format_time_for_display, calculate_golden_hour


class SunMoonDisplay:
    """
    FIXED Sun and Moon Display - NO LONG DATE/TIME LINES
    """
    
    def __init__(self, app, gui_controller):
        self.app = app
        self.gui = gui_controller
        self.animation_running = False
        self.animation_particles = []
        self.animation_id = None
        
        # Text containers for organized layout
        self.info_sections = {}
        
        # Animation settings
        self.sun_x = 0
        self.sun_y = 0
        self.moon_x = 0
        self.moon_y = 0
        self.star_particles = []
        
    def build_sun_moon_page(self, window_width, window_height):
        """Build CLEAN sun/moon page - NO LONG DATE/TIME LINES"""
        
        # Back button
        self._add_back_button()
        
        # Clean header - ONLY title and day/night
        self._build_clean_header_fixed(window_width)
        
        # ORGANIZED celestial display - NO OVERLAPS
        self._build_clean_celestial_display(window_width, window_height)
        
        # Well-spaced information sections
        self._build_organized_text_sections(window_width, window_height)
            
    def _build_clean_header_fixed(self, window_width):
        """Build FIXED header - NO LONG DATE/TIME LINES"""
        # Main title - "Sun and Moon Phases"
        title_main = self._create_black_label(
            self.app,
            text="Sun and Moon Phases",
            font=("Arial", int(28 + window_width/40), "bold"),
            x=window_width/2,
            y=80
        )
        self.gui.widgets.append(title_main)
        
        # ONLY simple day/night indicator - NO CITY, NO DATE, NO TIME
        self.day_night_label = self._create_black_label(
            self.app,
            text="🌤️ Loading...",
            font=("Arial", int(16 + window_width/80), "bold"),
            x=window_width/2,
            y=120
        )
        self.gui.widgets.append(self.day_night_label)
    
    def _build_clean_celestial_display(self, window_width, window_height):
        """Build CLEAN celestial visualization - NO OVERLAPPING"""
        viz_y = 160
        viz_height = 180  # Smaller height for better organization
        center_x = window_width // 2
        
        # Clean sky with clear boundaries
        sky_frame = tk.Frame(
            self.app,
            height=viz_height,
            bg="#87CEEB",
            relief="solid",
            borderwidth=2
        )
        sky_frame.place(x=80, y=viz_y, width=window_width-160)
        self.gui.widgets.append(sky_frame)
        
        # Clear horizon line
        horizon_y = viz_y + viz_height - 30
        horizon_line = tk.Frame(
            self.app,
            height=4,
            bg="#8B4513",
            relief="solid",
            borderwidth=1
        )
        horizon_line.place(x=80, y=horizon_y, width=window_width-160)
        self.gui.widgets.append(horizon_line)
        
        # Clean ground
        ground_frame = tk.Frame(
            self.app,
            height=25,
            bg="#A0522D",
            relief="solid",
            borderwidth=1
        )
        ground_frame.place(x=80, y=horizon_y+4, width=window_width-160)
        self.gui.widgets.append(ground_frame)
        
        # CLEAN directional labels - NO OVERLAP
        # East - far left
        east_label = self._create_black_label(
            self.app,
            text="East",
            font=("Arial", 12, "bold"),
            x=100,
            y=horizon_y - 20
        )
        self.gui.widgets.append(east_label)
        
        # West - far right
        west_label = self._create_black_label(
            self.app,
            text="West", 
            font=("Arial", 12, "bold"),
            x=window_width - 100,
            y=horizon_y - 20
        )
        self.gui.widgets.append(west_label)
        
        # Zenith - top center
        zenith_label = self._create_black_label(
            self.app,
            text="Zenith",
            font=("Arial", 12, "bold"),
            x=center_x,
            y=viz_y + 15
        )
        self.gui.widgets.append(zenith_label)
        
        # Clean elevation markers - NO OVERLAP
        # 60° line
        grid_60_y = horizon_y - 90
        grid_60_line = tk.Frame(
            self.app,
            height=1,
            bg="#666666",
            relief="flat"
        )
        grid_60_line.place(x=100, y=grid_60_y, width=window_width-200)
        self.gui.widgets.append(grid_60_line)
        
        # 60° label - far left, no overlap
        deg_60_label = self._create_black_label(
            self.app,
            text="60°",
            font=("Arial", 10),
            x=75,
            y=grid_60_y
        )
        self.gui.widgets.append(deg_60_label)
        
        # 30° line
        grid_30_y = horizon_y - 45
        grid_30_line = tk.Frame(
            self.app,
            height=1,
            bg="#666666",
            relief="flat"
        )
        grid_30_line.place(x=100, y=grid_30_y, width=window_width-200)
        self.gui.widgets.append(grid_30_line)
        
        # 30° label - far left, no overlap
        deg_30_label = self._create_black_label(
            self.app,
            text="30°",
            font=("Arial", 10),
            x=75,
            y=grid_30_y
        )
        self.gui.widgets.append(deg_30_label)
        
        # Sun indicator - positioned clearly
        self.sun_indicator = self._create_black_label(
            self.app,
            text="☀️",
            font=("Arial", 35),
            x=window_width/3,
            y=horizon_y - 40
        )
        self.gui.widgets.append(self.sun_indicator)
        
        # Moon indicator - positioned clearly, no overlap
        self.moon_indicator = self._create_black_label(
            self.app,
            text="🌙",
            font=("Arial", 35),
            x=2*window_width/3,
            y=horizon_y - 40
        )
        self.gui.widgets.append(self.moon_indicator)
    
    def _build_organized_text_sections(self, window_width, window_height):
        """Build well-organized text sections with proper spacing"""
        sections_start_y = 380
        
        # Calculate clean layout
        available_width = window_width - 100
        section_width = available_width // 2
        
        left_x = 70
        right_x = left_x + section_width + 20
        
        # Row 1: Solar and Lunar Data
        row1_y = sections_start_y
        
        # Row 2: Positions and Times  
        row2_y = sections_start_y + 120
        
        # Create sections with clear spacing
        sections = [
            ("sun_section", "☀️ Solar Data", left_x, row1_y),
            ("moon_section", "🌙 Lunar Data", right_x, row1_y),
            ("position_section", "🧭 Positions", left_x, row2_y),
            ("time_section", "⏰ Golden Hours", right_x, row2_y)
        ]
        
        for section_id, title, x, y in sections:
            self._create_clean_text_section(section_id, title, x, y)
    
    def _create_clean_text_section(self, section_id, title, x, y):
        """Create a clean, well-spaced text section"""
        # Section title - clear positioning
        title_label = self._create_black_label(
            self.app,
            text=title,
            font=("Arial", 15, "bold"),
            x=x,
            y=y,
            anchor="nw"
        )
        self.gui.widgets.append(title_label)
        
        # Content area - properly spaced below title
        content_label = self._create_black_label(
            self.app,
            text="Loading...",
            font=("Arial", 11),
            x=x,
            y=y + 25,
            anchor="nw",
            justify="left"
        )
        self.gui.widgets.append(content_label)
        
        # Store references
        self.info_sections[section_id] = {
            'title': title_label,
            'content': content_label
        }
    
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
    
    def update_sun_moon_display(self, sun_moon_data):
        """Update display - ONLY SET DAY/NIGHT, NO LONG DATE/TIME LINES"""
        try:
            if sun_moon_data.get("error"):
                self._show_error_display(sun_moon_data["error"])
                return
            
            # UPDATE ONLY THE DAY/NIGHT LABEL - NO CITY, NO DATE, NO TIME
            if hasattr(self, 'day_night_label'):
                if sun_moon_data.get("is_daytime", True):
                    self.day_night_label.configure(text="☀️ Daytime")
                else:
                    self.day_night_label.configure(text="🌙 Nighttime")
            
            # Update celestial positions
            self._update_celestial_positions_clean(sun_moon_data)
            
            # Update text sections
            self._update_text_sections_clean(sun_moon_data)
                        
        except Exception as e:
            self._show_error_display(str(e))
    
    def _update_text_sections_clean(self, data):
        """Update text sections with clean formatting"""
        try:
            # Sun Section - clean format
            if "sun_section" in self.info_sections:
                sunrise = format_time_for_display(data.get("sunrise"))
                sunset = format_time_for_display(data.get("sunset"))
                solar_noon = format_time_for_display(data.get("solar_noon"))
                status = 'Above Horizon' if data.get('is_daytime') else 'Below Horizon'
                
                sun_content = f"""Sunrise: {sunrise}
Sunset: {sunset}
Solar Noon: {solar_noon}
Status: {status}"""
                
                self.info_sections["sun_section"]["content"].configure(text=sun_content)
            
            # Moon Section - clean format
            if "moon_section" in self.info_sections:
                moon_phase_name = data.get("moon_phase_name", "Unknown")
                moon_illumination = data.get("moon_illumination", 0)
                moon_emoji = get_moon_phase_emoji(data.get("moon_phase", 0))
                visibility = 'Visible' if data.get('moon_position', {}).get('elevation', 0) > 0 else 'Below Horizon'
                
                moon_content = f"""{moon_emoji} {moon_phase_name}
Illumination: {moon_illumination:.1f}%
Cycle: {data.get('moon_phase', 0):.3f}
Visibility: {visibility}"""
                
                self.info_sections["moon_section"]["content"].configure(text=moon_content)
            
            # Position Section - clean format
            if "position_section" in self.info_sections:
                sun_pos = data.get("sun_position", {})
                moon_pos = data.get("moon_position", {})
                
                position_content = f"""Sun: {sun_pos.get('elevation', 0):.1f}° / {sun_pos.get('azimuth', 0):.1f}°
Moon: {moon_pos.get('elevation', 0):.1f}° / {moon_pos.get('azimuth', 0):.1f}°

(Elevation / Azimuth)"""
                
                self.info_sections["position_section"]["content"].configure(text=position_content)
            
            # Time Section - clean format
            if "time_section" in self.info_sections:
                golden_hour = calculate_golden_hour(data.get("sunrise"), data.get("sunset"))
                
                time_content = f"""Morning:
{golden_hour.get('morning_start', 'N/A')} - {golden_hour.get('morning_end', 'N/A')}

Evening:
{golden_hour.get('evening_start', 'N/A')} - {golden_hour.get('evening_end', 'N/A')}"""
                
                self.info_sections["time_section"]["content"].configure(text=time_content)
            
        except Exception as e:
            pass
    
    def _update_celestial_positions_clean(self, data):
        """Update sun and moon positions with CLEAN positioning"""
        try:
            window_width = self.app.winfo_width()
            
            # Get position data
            sun_pos = data.get("sun_position", {})
            sun_elevation = max(0, sun_pos.get("elevation", 45))  # Keep above horizon for visibility
            sun_azimuth = sun_pos.get("azimuth", 180)
            
            moon_pos = data.get("moon_position", {})
            moon_elevation = max(0, moon_pos.get("elevation", 30))  # Keep above horizon for visibility
            moon_azimuth = moon_pos.get("azimuth", 90)
            
            # Calculate CLEAN screen positions
            horizon_y = 290  # Fixed horizon line position
            sky_height = 120  # Available sky space
            
            # Sun position - clean calculation
            sun_y = horizon_y - (sun_elevation / 90) * sky_height
            sun_x = 150 + (sun_azimuth / 360) * (window_width - 300)  # Keep in bounds
            
            # Moon position - clean calculation, avoid overlap
            moon_y = horizon_y - (moon_elevation / 90) * sky_height
            moon_x = 150 + (moon_azimuth / 360) * (window_width - 300)  # Keep in bounds
            
            # Ensure no overlap
            if abs(sun_x - moon_x) < 80:
                if moon_x > sun_x:
                    moon_x = sun_x + 80
                else:
                    moon_x = sun_x - 80
            
            # Update positions
            if hasattr(self, 'sun_indicator'):
                self.sun_indicator.place(x=sun_x, y=sun_y, anchor="center")
            
            if hasattr(self, 'moon_indicator'):
                moon_phase = data.get("moon_phase", 0.25)
                moon_emoji = get_moon_phase_emoji(moon_phase)
                
                self.moon_indicator.configure(text=moon_emoji)
                self.moon_indicator.place(x=moon_x, y=moon_y, anchor="center")
            
        except Exception as e:
            pass
    
    def _show_error_display(self, error_msg):
        """Show error message"""
        try:
            if hasattr(self, 'day_night_label'):
                self.day_night_label.configure(text="❌ Error loading data")
            
            # Update all sections to show error
            for section_id, section_data in self.info_sections.items():
                if 'content' in section_data:
                    section_data['content'].configure(text="Error loading data\nPlease try refreshing")
                    
        except Exception as e:
            pass
    
    def update_for_theme_change(self):
        """Update display for theme changes (keep text black)"""
        try:
            canvas_bg = self._get_canvas_bg_color()
            
            # Update all labels to maintain black text with new background
            for section_id, section_data in self.info_sections.items():
                if 'title' in section_data:
                    section_data['title'].configure(fg="black", bg=canvas_bg)
                if 'content' in section_data:
                    section_data['content'].configure(fg="black", bg=canvas_bg)
            
            # Update day/night label
            if hasattr(self, 'day_night_label'):
                self.day_night_label.configure(fg="black", bg=canvas_bg)
                        
        except Exception as e:
            pass
    
    # Helper methods
    def _get_canvas_bg_color(self):
        """Get the current canvas background color"""
        try:
            if self.gui.bg_canvas:
                return self.gui.bg_canvas.cget("bg")
            return "#87CEEB"
        except:
            return "#87CEEB"
    
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
    
    def start_celestial_animation(self):
        """Start celestial animations"""
        try:
            self.animation_running = True
            self._animate_celestial_background()
        except Exception as e:
            pass
    
    def stop_celestial_animation(self):
        """Stop celestial animations"""
        try:
            self.animation_running = False
            if self.animation_id:
                self.app.after_cancel(self.animation_id)
                self.animation_id = None
        except Exception as e:
            pass
    
    def _animate_celestial_background(self):
        """Animate background effects"""
        if not self.animation_running:
            return
        
        try:
            # Simple star twinkling
            if hasattr(self.gui, 'bg_canvas') and self.gui.bg_canvas:
                self._add_simple_stars()
            
            # Schedule next frame
            self.animation_id = self.app.after(4000, self._animate_celestial_background)
            
        except Exception as e:
            pass
    
    def _add_simple_stars(self):
        """Add simple star effects"""
        try:
            canvas = self.gui.bg_canvas
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            # Remove old stars
            canvas.delete("star")
            
            # Add a few simple stars
            for _ in range(random.randint(3, 8)):
                x = random.randint(100, width - 100)
                y = random.randint(50, height//2)
                
                canvas.create_oval(
                    x - 1, y - 1, x + 1, y + 1,
                    fill="white", outline="", tags="star"
                )
            
        except Exception as e:
            pass
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self.stop_celestial_animation()
            self.info_sections.clear()
        except Exception as e:
            pass