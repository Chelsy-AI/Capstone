"""
Theme Configuration Module
==========================

This module defines color schemes and appearance settings for the weather app.

Key features:
- Pre-defined color schemes for different preferences
- Easy theme switching throughout the app
- Accessibility-focused high contrast options
- Utility functions to apply themes to widgets
- Extensible system for adding new themes

Each theme defines colors for:
- Background and text colors
- Button and input field styling
- Accent colors for highlights
- Data display areas
- Special UI elements
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LIGHT THEME - PERFECT FOR DAYTIME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LIGHT_THEME = {
    # Main colors - the foundation of the light theme
    "bg": "#ffffff",           # Pure white background - clean and bright
    "fg": "#1a1a1a",           # Very dark gray text - easier on eyes than pure black
    "accent": "#3399ff",       # Bright blue for buttons, links, and highlights
    
    # Button styling - how clickable elements look
    "button_bg": "#e6e6e6",    # Light gray button background - subtle but visible
    "button_fg": "#1a1a1a",    # Dark text on buttons for good contrast
    
    # Input field styling - where users type text
    "entry_bg": "#f2f2f2",     # Very light gray for text input backgrounds
    
    # Data display areas - where weather information is shown
    "text_bg": "#dddddd",      # Light gray background for weather data containers
    "text_fg": "#111111"       # Deep black text for excellent readability
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DARK THEME - PERFECT FOR NIGHTTIME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DARK_THEME = {
    # Main colors - foundation of the dark theme
    "bg": "#121212",           # Very dark gray (not pure black) - easier on eyes
    "fg": "#f2f2f2",           # Light gray text for excellent readability on dark background
    "accent": "#3399ff",       # Same bright blue accent - works well on dark backgrounds
    
    # Button styling for dark theme
    "button_bg": "#2c2c2c",    # Medium dark gray for buttons - visible but not harsh
    "button_fg": "#f2f2f2",    # Light text on dark buttons
    
    # Input field styling for dark theme
    "entry_bg": "#1e1e1e",     # Dark gray for text input - comfortable for typing
    
    # Data display areas for dark theme
    "text_bg": "#1a1a1a",      # Slightly lighter than main background for contrast
    "text_fg": "#f2f2f2"       # Light text for good readability
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HIGH CONTRAST THEME - MAXIMUM ACCESSIBILITY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HIGH_CONTRAST_THEME = {
    # Main colors - maximum contrast for accessibility
    "bg": "#000000",           # Pure black background
    "fg": "#ffffff",           # Pure white text - maximum contrast
    "accent": "#ffff00",       # Bright yellow accent - highly visible
    
    # Button styling for high contrast
    "button_bg": "#ffffff",    # White buttons stand out strongly
    "button_fg": "#000000",    # Black text on white buttons
    
    # Input field styling for high contrast
    "entry_bg": "#ffffff",     # White input backgrounds for clarity
    
    # Data display areas for high contrast
    "text_bg": "#333333",      # Dark gray containers for some visual separation
    "text_fg": "#ffffff"       # White text for maximum readability
}

def get_theme(theme_name):
    """
    Get a theme dictionary by name.
    
    Args:
        theme_name (str): Name of the theme ("light", "dark", "blue", etc.)
        
    Returns:
        dict: Theme color dictionary
    """
    # Convert theme name to lowercase for consistent matching
    theme_name = theme_name.lower()
    
    # Return the appropriate theme dictionary
    if theme_name == "dark":
        return DARK_THEME
    elif theme_name == "high_contrast":
        return HIGH_CONTRAST_THEME
    else:
        # Default to light theme if theme name isn't recognized
        return LIGHT_THEME


def get_available_themes():
    """
    Get a list of all available theme names.
    
    Returns:
        list: List of available theme names
    """
    return ["light", "dark", "blue", "high_contrast", "sunset", "forest"]


def apply_theme_to_widget(widget, theme, widget_type="default"):
    """
    Apply theme colors to a specific tkinter widget.
        
    Args:
        widget: The tkinter widget to style
        theme (dict): Theme color dictionary
        widget_type (str): Type of widget ("button", "entry", "text", or "default")
    """
    try:
        if widget_type == "button":
            # Style buttons with specific button colors
            widget.configure(
                bg=theme["button_bg"],           # Button background color
                fg=theme["button_fg"],           # Button text color
                activebackground=theme["accent"], # Color when button is clicked
                activeforeground=theme["bg"]       # Text color when button is clicked
            )
        elif widget_type == "entry":
            # Style text input fields
            widget.configure(
                bg=theme["entry_bg"],            # Input field background
                fg=theme["fg"],                  # Text color inside input
                insertbackground=theme["fg"]     # Cursor color
            )
        elif widget_type == "text":
            # Style text display areas (like weather data)
            widget.configure(
                bg=theme["text_bg"],             # Background for data areas
                fg=theme["text_fg"]              # Text color for data
            )
        else:
            # Default styling for labels, frames, etc.
            widget.configure(
                bg=theme["bg"],                  # Main background color
                fg=theme["fg"]                   # Main text color
            )
    except Exception:
        # If styling fails, just continue
        pass


def get_contrasting_color(background_color):
    """
    Get a contrasting text color for a given background color.
    
    Args:
        background_color (str): Hex color code (like "#ffffff")
        
    Returns:
        str: Either "#000000" (black) or "#ffffff" (white) for best contrast
    """
    try:
        # Remove # symbol if present
        color = background_color.lstrip('#')
        
        # Convert hex to RGB values
        r = int(color[0:2], 16)  # Red component
        g = int(color[2:4], 16)  # Green component
        b = int(color[4:6], 16)  # Blue component
        
        # Calculate relative luminance
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        
        # If the background is bright, use black text; if dark, use white text
        return "#000000" if luminance > 0.5 else "#ffffff"
        
    except Exception:
        # If color parsing fails, default to black text
        return "#000000"


def blend_colors(color1, color2, ratio=0.5):
    """
    Blend two colors together to create a new color.
    
    Args:
        color1 (str): First hex color (like "#ff0000" for red)
        color2 (str): Second hex color (like "#0000ff" for blue)
        ratio (float): How much of color2 to use (0.0 = all color1, 1.0 = all color2)
        
    Returns:
        str: Blended hex color
    """
    try:
        # Remove # symbols
        c1 = color1.lstrip('#')
        c2 = color2.lstrip('#')
        
        # Convert to RGB values
        r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
        r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)
        
        # Blend the colors
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
        
    except Exception:
        # If blending fails, return the first color
        return color1


def create_custom_theme(base_theme_name, customizations):
    """
    Create a custom theme by modifying an existing theme.
    
    Args:
        base_theme_name (str): Name of the theme to start with
        customizations (dict): Colors to override (like {"bg": "#ff0000"})
        
    Returns:
        dict: New custom theme dictionary
    """
    try:
        # Start with the base theme
        base_theme = get_theme(base_theme_name)
        
        # Create a copy so we don't modify the original
        custom_theme = base_theme.copy()
        
        # Apply customizations
        for key, value in customizations.items():
            if key in custom_theme:
                custom_theme[key] = value
        
        return custom_theme
        
    except Exception:
        # If customization fails, return the base theme
        return get_theme(base_theme_name)


def get_theme_preview(theme_name):
    """
    Get a preview description of what a theme looks like.
    
    Args:
        theme_name (str): Name of the theme
        
    Returns:
        dict: Theme preview information
    """
    previews = {
        "light": {
            "description": "Clean and bright with white backgrounds - perfect for daytime use",
            "best_for": "Bright environments, daytime use, traditional preference",
            "colors": "White background, dark text, blue accents"
        },
        "dark": {
            "description": "Easy on the eyes with dark backgrounds and light text",
            "best_for": "Low light environments, nighttime use, reduced eye strain",
            "colors": "Dark gray background, light text, blue accents"
        },
        "high_contrast": {
            "description": "Maximum contrast for excellent accessibility and readability",
            "best_for": "Visual impairments, maximum readability, accessibility needs",
            "colors": "Black background, white text, yellow accents"
        },
    }
    
    return previews.get(theme_name.lower(), {
        "description": "Unknown theme",
        "best_for": "Unknown",
        "colors": "Unknown"
    })


def get_all_themes():
    """
    Get a dictionary containing all available themes.
    
    Returns:
        dict: Dictionary mapping theme names to theme dictionaries
    """
    return {
        "light": LIGHT_THEME,
        "dark": DARK_THEME,
        "high_contrast": HIGH_CONTRAST_THEME,
    }


def validate_theme(theme_dict):
    """
    Validate that a theme dictionary has all required colors.
    
    Args:
        theme_dict (dict): Theme dictionary to validate
        
    Returns:
        tuple: (is_valid, missing_keys) - True/False and list of missing colors
    """
    # Required keys that every theme must have
    required_keys = [
        "bg", "fg", "accent",
        "button_bg", "button_fg",
        "entry_bg",
        "text_bg", "text_fg"
    ]
    
    # Check which keys are missing
    missing_keys = [key for key in required_keys if key not in theme_dict]
    
    # Theme is valid if no keys are missing
    is_valid = len(missing_keys) == 0
    
    return is_valid, missing_keys


def get_theme_recommendations(preferences):
    """
    Get theme recommendations based on user preferences.
    
    Args:
        preferences (dict): User preferences like {"time_of_use": "night", "priority": "accessibility"}
        
    Returns:
        list: Recommended theme names in order of preference
    """
    recommendations = []
    
    # Check for accessibility needs first
    if preferences.get("accessibility_needs"):
        recommendations.append("high_contrast")
    
    # Check time of use preference
    time_of_use = preferences.get("time_of_use", "").lower()
    if time_of_use in ["night", "evening", "dark"]:
        recommendations.extend(["dark", "sunset", "forest"])
    elif time_of_use in ["day", "daytime", "bright"]:
        recommendations.extend(["light", "blue"])
    
    # Check color preferences
    favorite_color = preferences.get("favorite_color", "").lower()
    if "blue" in favorite_color:
        recommendations.append("blue")
    elif "green" in favorite_color:
        recommendations.append("forest")
    elif "purple" in favorite_color:
        recommendations.append("sunset")
    
    # Always include light and dark as fallbacks
    if "light" not in recommendations:
        recommendations.append("light")
    if "dark" not in recommendations:
        recommendations.append("dark")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_recommendations = []
    for theme in recommendations:
        if theme not in seen:
            seen.add(theme)
            unique_recommendations.append(theme)
    
    return unique_recommendations
