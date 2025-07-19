# ────────────────────────────────────────────────────────────────────────────── 
# THEME CONFIGURATION MODULE
# 
# This module defines color schemes for light and dark themes.
# These dictionaries are used throughout the app to style all UI components.
# Having themes in a separate file makes it easy to:
# - Switch between light and dark modes
# - Add new themes later
# - Keep all colors organized in one place
# ────────────────────────────────────────────────────────────────────────────── 

# Light theme - designed for daytime use or bright environments
LIGHT_THEME = {
    # --- MAIN COLORS ---
    "bg": "#ffffff",           # App background (pure white)
    "fg": "#1a1a1a",           # Primary text color (very dark gray, easier on eyes than pure black)
    "accent": "#3399ff",       # Accent/highlight color (bright blue for buttons, links)
    
    # --- BUTTON COLORS ---
    "button_bg": "#e6e6e6",    # Button background (light gray)
    "button_fg": "#1a1a1a",    # Button text (same as primary text)
    
    # --- INPUT COLORS ---
    "entry_bg": "#f2f2f2",     # Text input background (very light gray)
    
    # --- DATA DISPLAY COLORS ---
    "text_bg": "#dddddd",      # Background for data containers (weather info boxes)
    "text_fg": "#111111"       # Text color for data (deep black for good contrast)
}

# Dark theme - designed for nighttime use or low-light environments
DARK_THEME = {
    # --- MAIN COLORS ---
    "bg": "#121212",           # App background (very dark gray, not pure black)
    "fg": "#f2f2f2",           # Primary text color (light gray for good readability)
    "accent": "#3399ff",       # Accent/highlight color (same blue as light theme)
    
    # --- BUTTON COLORS ---
    "button_bg": "#2c2c2c",    # Button background (medium dark gray)
    "button_fg": "#f2f2f2",    # Button text (same as primary text)
    
    # --- INPUT COLORS ---
    "entry_bg": "#1e1e1e",     # Text input background (darker gray)
    
    # --- DATA DISPLAY COLORS ---
    "text_bg": "#1a1a1a",      # Background for data containers (slightly lighter than main bg)
    "text_fg": "#f2f2f2"       # Text color for data (same as primary text)
}

# ────────────────────────────────────────────────────────────────────────────── 
# THEME UTILITY FUNCTIONS
# ────────────────────────────────────────────────────────────────────────────── 

def get_theme(theme_name):
    """
    Get a theme dictionary by name.
    
    """
    if theme_name.lower() == "dark":
        return DARK_THEME
    else:
        return LIGHT_THEME

def get_available_themes():
    """
    Get list of available theme names.
    
    """
    return ["light", "dark"]

def apply_theme_to_widget(widget, theme, widget_type="default"):
    """
    Apply theme colors to a Tkinter widget.
    
    """
    try:
        if widget_type == "button":
            # Style buttons with specific button colors
            widget.configure(
                bg=theme["button_bg"],
                fg=theme["button_fg"],
                activebackground=theme["accent"],  # Color when clicked
                activeforeground=theme["bg"]       # Text color when clicked
            )
        elif widget_type == "entry":
            # Style text input fields
            widget.configure(
                bg=theme["entry_bg"],
                fg=theme["fg"],
                insertbackground=theme["fg"]       # Cursor color
            )
        elif widget_type == "text":
            # Style text display areas
            widget.configure(
                bg=theme["text_bg"],
                fg=theme["text_fg"]
            )
        else:
            # Default styling for labels, frames, etc.
            widget.configure(
                bg=theme["bg"],
                fg=theme["fg"]
            )
    except:
        pass       

# ────────────────────────────────────────────────────────────────────────────── 
# ADVANCED THEME FEATURES (for future expansion)
# ────────────────────────────────────────────────────────────────────────────── 

# You can add more themes here as your app grows
BLUE_THEME = {
    "bg": "#1e3a8a",           # Deep blue background
    "fg": "#f1f5f9",           # Light blue-gray text
    "accent": "#60a5fa",       # Bright blue accent
    "button_bg": "#3b82f6",    # Medium blue buttons
    "button_fg": "#ffffff",    # White button text
    "entry_bg": "#1e40af",     # Darker blue inputs
    "text_bg": "#2563eb",      # Blue data containers
    "text_fg": "#f1f5f9"       # Light text
}

# High contrast theme for accessibility
HIGH_CONTRAST_THEME = {
    "bg": "#000000",           # Pure black background
    "fg": "#ffffff",           # Pure white text
    "accent": "#ffff00",       # Bright yellow accent
    "button_bg": "#ffffff",    # White buttons
    "button_fg": "#000000",    # Black button text
    "entry_bg": "#ffffff",     # White inputs
    "text_bg": "#333333",      # Dark gray containers
    "text_fg": "#ffffff"       # White text
}

# Function to get all available themes (including new ones)
def get_all_themes():
    """
    Get dictionary of all available themes.
    
    """
    return {
        "light": LIGHT_THEME,
        "dark": DARK_THEME,
        "blue": BLUE_THEME,
        "high_contrast": HIGH_CONTRAST_THEME
    }