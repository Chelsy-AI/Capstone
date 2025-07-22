"""
Sun and Moon Phases Display Module - Improved Layout
Enhanced sky/horizon visualization with clean text-only layout (no boxes)
"""

import tkinter as tk
import math
import random
from .api import get_moon_phase_emoji, format_time_for_display, calculate_golden_hour


class SunMoonDisplay:
    """
    Improved Sun and Moon Display with enhanced visualization and clean text layout
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
        """Build the improved sun/moon phases page"""
        
        # Back button
        self._add_back_button()
        
        # Main title
        self._build_page_header(window_width)
        
        # Enhanced celestial visualization
        self._build_enhanced_celestial_display(window_width, window_height)
        
        # Clean text-only information sections
        self._build_text_sections(window_width, window_height)
            
    def _build_page_header(self, window_width):
        """Build the page header"""
        # Main title
        title_main = self._create_black_label(
            self.app,
            text="☀️ Astronomical Data 🌙",
            font=("Arial", int(28 + window_width/40), "bold"),
            x=window_width/2,
            y=80
        )
        self.gui.widgets.append(title_main)
        
        # Subtitle with current time
        self.time_label = self._create_black_label(
            self.app,
            text="Loading celestial information...",
            font=("Arial", int(14 + window_width/80)),
            x=window_width/2,
            y=120
        )
        self.gui.widgets.append(self.time_label)
    
    def _build_enhanced_celestial_display(self, window_width, window_height):
        """Build enhanced celestial visualization with improved sky/horizon/ground"""
        viz_y = 160
        viz_height = 200
        center_x = window_width // 2
        
        # Sky dome with gradient effect using multiple rectangles
        sky_colors = ["#87CEEB", "#B0E0E6", "#ADD8E6", "#E0F6FF"]
        for i, color in enumerate(sky_colors):
            sky_section = tk.Frame(
                self.app,
                height=viz_height//4,
                bg=color,
                relief="flat",
                borderwidth=0
            )
            sky_section.place(x=50, y=viz_y + i*(viz_height//4), width=window_width-100)
            self.gui.widgets.append(sky_section)
        
        # Horizon line with enhanced styling
        horizon_y = viz_y + viz_height - 50
        horizon_line = tk.Frame(
            self.app,
            height=4,
            bg="#8B4513",  # Earth brown
            relief="raised",
            borderwidth=1
        )
        horizon_line.place(x=80, y=horizon_y, width=window_width-160)
        self.gui.widgets.append(horizon_line)
        
        # Ground with textured appearance
        ground_colors = ["#8B4513", "#A0522D", "#CD853F"]
        for i, color in enumerate(ground_colors):
            ground_section = tk.Frame(
                self.app,
                height=15,
                bg=color,
                relief="flat",
                borderwidth=0
            )
            ground_section.place(x=50, y=horizon_y + 4 + i*15, width=window_width-100)
            self.gui.widgets.append(ground_section)
        
        # Enhanced directional indicators
        directions = [
            ("🌅 East", 120, horizon_y - 10),
            ("🌇 West", window_width - 120, horizon_y - 10),
            ("⬆️ Zenith", center_x, viz_y + 20),
            ("⬇️ Nadir", center_x, horizon_y + 60)
        ]
        
        for direction, x, y in directions:
            dir_label = self._create_black_label(
                self.app,
                text=direction,
                font=("Arial", int(12 + window_width/100), "bold"),
                x=x,
                y=y
            )
            self.gui.widgets.append(dir_label)
        
        # Elevation grid lines for reference
        for elevation in [30, 60]:
            grid_y = horizon_y - (elevation / 90) * (viz_height - 50)
            grid_line = tk.Frame(
                self.app,
                height=1,
                bg="#CCCCCC",
                relief="flat",
                borderwidth=0
            )
            grid_line.place(x=100, y=grid_y, width=window_width-200)
            self.gui.widgets.append(grid_line)
            
            # Elevation labels
            elev_label = self._create_black_label(
                self.app,
                text=f"{elevation}°",
                font=("Arial", 10),
                x=90,
                y=grid_y
            )
            self.gui.widgets.append(elev_label)
        
        # Enhanced atmosphere indicators
        atmosphere_labels = [
            ("🌌 Deep Sky", center_x, viz_y + 30),
            ("☁️ Cloud Layer", center_x, viz_y + 80),
            ("🌊 Atmosphere", center_x, horizon_y - 30),
            ("🌍 Earth Surface", center_x, horizon_y + 25)
        ]
        
        for label_text, x, y in atmosphere_labels:
            atmo_label = self._create_black_label(
                self.app,
                text=label_text,
                font=("Arial", int(11 + window_width/120)),
                x=x,
                y=y
            )
            self.gui.widgets.append(atmo_label)
        
        # Enhanced sun indicator with glow effect
        self.sun_indicator = self._create_black_label(
            self.app,
            text="☀️",
            font=("Arial", int(40 + window_width/25)),
            x=window_width/3,
            y=horizon_y - 60
        )
        self.gui.widgets.append(self.sun_indicator)
        
        # Enhanced moon indicator
        self.moon_indicator = self._create_black_label(
            self.app,
            text="🌙",
            font=("Arial", int(40 + window_width/25)),
            x=2*window_width/3,
            y=horizon_y - 40
        )
        self.gui.widgets.append(self.moon_indicator)
        
        # Compass rose for better orientation
        compass_elements = [
            ("N", center_x, viz_y - 20),
            ("S", center_x, horizon_y + 80),
            ("E", window_width - 80, horizon_y),
            ("W", 80, horizon_y)
        ]
        
        for direction, x, y in compass_elements:
            compass_label = self._create_black_label(
                self.app,
                text=f"🧭 {direction}",
                font=("Arial", 10, "bold"),
                x=x,
                y=y
            )
            self.gui.widgets.append(compass_label)
    
    def _build_text_sections(self, window_width, window_height):
        """Build clean text-only information sections (no boxes)"""
        sections_y = 400
        section_spacing = 30
        
        # Calculate positioning for 4 sections in 2x2 grid
        available_width = window_width - 80
        section_width = available_width // 2
        
        left_x = 60
        right_x = left_x + section_width
        top_y = sections_y
        bottom_y = sections_y + 100
        
        # Section positions
        sections = [
            ("sun_section", "☀️ Solar Data", left_x, top_y),
            ("moon_section", "🌙 Lunar Data", right_x, top_y),
            ("position_section", "🧭 Celestial Positions", left_x, bottom_y),
            ("time_section", "⏰ Rise & Set Times", right_x, bottom_y)
        ]
        
        for section_id, title, x, y in sections:
            self._create_text_section(section_id, title, x, y)
    
    def _create_text_section(self, section_id, title, x, y):
        """Create a text-only information section"""
        # Section title (bold, larger)
        title_label = self._create_black_label(
            self.app,
            text=title,
            font=("Arial", 16, "bold"),
            x=x,
            y=y,
            anchor="w"
        )
        self.gui.widgets.append(title_label)
        
        # Content area for data
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
            fg="black",  # Always black text
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
        """Update the improved display with new data"""
        try:
            
            if sun_moon_data.get("error"):
                self._show_error_display(sun_moon_data["error"])
                return
            
            # Update header time display
            self._update_header_time(sun_moon_data)
            
            # Update celestial positions
            self._update_celestial_positions(sun_moon_data)
            
            # Update text sections
            self._update_text_sections(sun_moon_data)
                        
        except Exception as e:
            self._show_error_display(str(e))
    
    def _update_header_time(self, data):
        """Update the header time information"""
        try:
            if hasattr(self, 'time_label'):
                current_time = data.get("current_time", "")
                city = data.get("city", "Unknown")
                
                try:
                    import datetime
                    dt = datetime.datetime.fromisoformat(current_time.replace('Z', '+00:00'))
                    time_str = dt.strftime("%A, %B %d, %Y • %I:%M %p")
                    
                    # Add day/night indicator
                    day_night = "🌞 Daytime" if data.get("is_daytime", True) else "🌙 Nighttime"
                    
                    self.time_label.configure(text=f"{city} • {time_str} • {day_night}")
                except:
                    self.time_label.configure(text=f"{city} • Current Astronomical Data")
        except Exception as e:
            pass
    
    def _update_text_sections(self, data):
        """Update all text sections with organized data"""
        try:
            # Sun Section
            if "sun_section" in self.info_sections:
                sunrise = format_time_for_display(data.get("sunrise"))
                sunset = format_time_for_display(data.get("sunset"))
                solar_noon = format_time_for_display(data.get("solar_noon"))
                
                sun_content = f"""🌅 Sunrise: {sunrise}
🌇 Sunset: {sunset}
🌞 Solar Noon: {solar_noon}
☀️ Status: {'Above Horizon' if data.get('is_daytime') else 'Below Horizon'}"""
                
                self.info_sections["sun_section"]["content"].configure(text=sun_content)
            
            # Moon Section
            if "moon_section" in self.info_sections:
                moon_phase_name = data.get("moon_phase_name", "Unknown")
                moon_illumination = data.get("moon_illumination", 0)
                moon_emoji = get_moon_phase_emoji(data.get("moon_phase", 0))
                
                moon_content = f"""{moon_emoji} Phase: {moon_phase_name}
💡 Illumination: {moon_illumination:.1f}%
🌙 Cycle: {data.get('moon_phase', 0):.3f}
✨ Visibility: {'Visible' if data.get('moon_position', {}).get('elevation', 0) > 0 else 'Below Horizon'}"""
                
                self.info_sections["moon_section"]["content"].configure(text=moon_content)
            
            # Position Section
            if "position_section" in self.info_sections:
                sun_pos = data.get("sun_position", {})
                moon_pos = data.get("moon_position", {})
                
                position_content = f"""☀️ Sun Elevation: {sun_pos.get('elevation', 0):.1f}°
🧭 Sun Azimuth: {sun_pos.get('azimuth', 0):.1f}°
🌙 Moon Elevation: {moon_pos.get('elevation', 0):.1f}°
🧭 Moon Azimuth: {moon_pos.get('azimuth', 0):.1f}°"""
                
                self.info_sections["position_section"]["content"].configure(text=position_content)
            
            # Time Section with Golden Hour
            if "time_section" in self.info_sections:
                golden_hour = calculate_golden_hour(data.get("sunrise"), data.get("sunset"))
                
                time_content = f"""🌅 Golden Hour Morning:
   {golden_hour.get('morning_start', 'N/A')} - {golden_hour.get('morning_end', 'N/A')}
🌇 Golden Hour Evening:
   {golden_hour.get('evening_start', 'N/A')} - {golden_hour.get('evening_end', 'N/A')}"""
                
                self.info_sections["time_section"]["content"].configure(text=time_content)
            
        except Exception as e:
            pass
    
    def _update_celestial_positions(self, data):
        """Update sun and moon positions with enhanced calculations"""
        try:
            window_width = self.app.winfo_width()
            
            # Get position data
            sun_pos = data.get("sun_position", {})
            sun_elevation = sun_pos.get("elevation", 45)
            sun_azimuth = sun_pos.get("azimuth", 180)
            
            moon_pos = data.get("moon_position", {})
            moon_elevation = moon_pos.get("elevation", 30)
            moon_azimuth = moon_pos.get("azimuth", 90)
            
            # Calculate screen positions with better mapping
            horizon_y = 310  # Horizon line position
            sky_height = 150  # Available sky space above horizon
            
            # Sun position calculation
            if sun_elevation >= 0:  # Above horizon
                sun_y = horizon_y - (sun_elevation / 90) * sky_height
                # Map azimuth to screen position (0° = North, 90° = East, 180° = South, 270° = West)
                azimuth_factor = (sun_azimuth - 90) / 180  # Convert to -1 to 1 range for East-West
                sun_x = window_width/2 + azimuth_factor * (window_width/4)
            else:  # Below horizon
                sun_y = horizon_y + abs(sun_elevation / 90) * 30
                sun_x = window_width/3
            
            # Moon position calculation
            if moon_elevation >= 0:
                moon_y = horizon_y - (moon_elevation / 90) * sky_height
                moon_azimuth_factor = (moon_azimuth - 90) / 180
                moon_x = window_width/2 + moon_azimuth_factor * (window_width/4)
            else:
                moon_y = horizon_y + abs(moon_elevation / 90) * 30
                moon_x = 2*window_width/3
            
            # Update positions
            if hasattr(self, 'sun_indicator'):
                self.sun_indicator.place(x=sun_x, y=sun_y, anchor="center")
            
            if hasattr(self, 'moon_indicator'):
                # Update moon with phase
                moon_phase = data.get("moon_phase", 0.25)
                moon_emoji = get_moon_phase_emoji(moon_phase)
                
                self.moon_indicator.configure(text=moon_emoji)
                self.moon_indicator.place(x=moon_x, y=moon_y, anchor="center")
            
        except Exception as e:
            pass
    
    def _show_error_display(self, error_msg):
        """Show error message"""
        try:
            if hasattr(self, 'time_label'):
                self.time_label.configure(text=f"❌ Error: {error_msg}")
            
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
            
            # Update time label
            if hasattr(self, 'time_label'):
                self.time_label.configure(fg="black", bg=canvas_bg)
                        
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
        """Start enhanced celestial animations"""
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
        """Animate enhanced background effects"""
        if not self.animation_running:
            return
        
        try:
            # Enhanced star twinkling
            if hasattr(self.gui, 'bg_canvas') and self.gui.bg_canvas:
                self._add_enhanced_stars()
            
            # Schedule next frame
            self.animation_id = self.app.after(4000, self._animate_celestial_background)
            
        except Exception as e:
            pass
    
    def _add_enhanced_stars(self):
        """Add enhanced twinkling star effects"""
        try:
            canvas = self.gui.bg_canvas
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            # Remove old stars
            canvas.delete("star")
            
            # Add subtle star patterns
            for _ in range(random.randint(6, 15)):
                x = random.randint(100, width - 100)
                y = random.randint(50, height//2)
                
                # Small, subtle stars
                size = random.choice([1, 2])
                colors = ["#FFFFFF", "#FFFFCC", "#E6E6FA"]
                color = random.choice(colors)
                
                # Create main star
                canvas.create_oval(
                    x - size, y - size, x + size, y + size,
                    fill=color, outline="", tags="star"
                )
                
                # Occasional sparkle
                if size == 2 and random.random() < 0.3:
                    canvas.create_line(
                        x - 4, y, x + 4, y,
                        fill=color, width=1, tags="star"
                    )
                    canvas.create_line(
                        x, y - 4, x, y + 4,
                        fill=color, width=1, tags="star"
                    )
            
        except Exception as e:
            pass
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self.stop_celestial_animation()
            
            # Clear section references
            self.info_sections.clear()
                        
        except Exception as e:
            pass
        