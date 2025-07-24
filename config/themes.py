"""
Theme Configuration Module
==========================

This module defines color schemes and appearance settings for the weather app.
It's like having a wardrobe of different "outfits" that the app can wear!

Think of themes as different moods for your app:
- Light theme: Clean, bright, perfect for daytime use
- Dark theme: Easy on the eyes, great for nighttime or low-light environments
- Blue theme: Cool and calming, ocean-inspired colors
- High contrast theme: Maximum readability for accessibility

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

Think of this as your app's "interior decorator" that makes everything look good!
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
# BLUE THEME - OCEAN-INSPIRED DESIGN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BLUE_THEME = {
    # Main colors - blue ocean theme
    "bg": "#1e3a8a",           # Deep blue background - like deep ocean water
    "fg": "#f1f5f9",           # Light blue-gray text - like seafoam
    "accent": "#60a5fa",       # Bright blue accent - like ocean waves
    
    # Button styling for blue theme
    "button_bg": "#3b82f6",    # Medium blue buttons - like clear sky
    "button_fg": "#ffffff",    # White text on blue buttons for contrast
    
    # Input field styling for blue theme
    "entry_bg": "#1e40af",     # Darker blue for inputs - like deep water
    
    # Data display areas for blue theme
    "text_bg": "#2563eb",      # Blue containers - like ocean depths
    "text_fg": "#f1f5f9"       # Light text for good readability
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

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SUNSET THEME - WARM AND COZY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUNSET_THEME = {
    # Main colors - warm sunset colors
    "bg": "#2d1b69",           # Deep purple background - like evening sky
    "fg": "#fbbf24",           # Golden yellow text - like sunset light
    "accent": "#f59e0b",       # Orange accent - like setting sun
    
    # Button styling for sunset theme
    "button_bg": "#7c3aed",    # Purple buttons - like twilight sky
    "button_fg": "#fbbf24",    # Golden text on purple buttons
    
    # Input field styling for sunset theme
    "entry_bg": "#1e1b4b",     # Dark purple for inputs
    
    # Data display areas for sunset theme
    "text_bg": "#4c1d95",      # Purple containers
    "text_fg": "#fbbf24"       # Golden text
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOREST THEME - NATURE-INSPIRED
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FOREST_THEME = {
    # Main colors - forest and nature theme
    "bg": "#1f2937",           # Dark gray-green background - like forest floor
    "fg": "#d1fae5",           # Light green text - like new leaves
    "accent": "#10b981",       # Emerald green accent - like fresh foliage
    
    # Button styling for forest theme
    "button_bg": "#059669",    # Green buttons - like tree bark
    "button_fg": "#ffffff",    # White text for contrast
    
    # Input field styling for forest theme
    "entry_bg": "#374151",     # Dark gray-green inputs
    
    # Data display areas for forest theme
    "text_bg": "#065f46",      # Dark green containers
    "text_fg": "#d1fae5"       # Light green text
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# THEME UTILITY FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_theme(theme_name):
    """
    Get a theme dictionary by name.
    
    This function acts like a theme "wardrobe" - you tell it what
    theme you want, and it gives you all the colors for that theme.
    
    Args:
        theme_name (str): Name of the theme ("light", "dark", "blue", etc.)
        
    Returns:
        dict: Theme color dictionary
        
    Example:
        dark_colors = get_theme("dark")
        print(f"Dark theme background: {dark_colors['bg']}")
        # Prints: Dark theme background: #121212
    """
    # Convert theme name to lowercase for consistent matching
    theme_name = theme_name.lower()
    
    # Return the appropriate theme dictionary
    if theme_name == "dark":
        return DARK_THEME
    elif theme_name == "blue":
        return BLUE_THEME
    elif theme_name == "high_contrast":
        return HIGH_CONTRAST_THEME
    elif theme_name == "sunset":
        return SUNSET_THEME
    elif theme_name == "forest":
        return FOREST_THEME
    else:
        # Default to light theme if theme name isn't recognized
        return LIGHT_THEME


def get_available_themes():
    """
    Get a list of all available theme names.
    
    This function returns all the themes you can choose from.
    Useful for creating theme selection menus or dropdowns.
    
    Returns:
        list: List of available theme names
        
    Example:
        themes = get_available_themes()
        print(f"Available themes: {', '.join(themes)}")
        # Prints: Available themes: light, dark, blue, high_contrast, sunset, forest
    """
    return ["light", "dark", "blue", "high_contrast", "sunset", "forest"]


def apply_theme_to_widget(widget, theme, widget_type="default"):
    """
    Apply theme colors to a specific tkinter widget.
    
    This function acts like a "painter" that applies the theme colors
    to individual widgets in the user interface.
    
    Args:
        widget: The tkinter widget to style
        theme (dict): Theme color dictionary
        widget_type (str): Type of widget ("button", "entry", "text", or "default")
        
    Example:
        # Apply dark theme to a button
        dark_theme = get_theme("dark")
        apply_theme_to_widget(my_button, dark_theme, "button")
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
        # If styling fails (widget doesn't support these options), just continue
        pass


def get_contrasting_color(background_color):
    """
    Get a contrasting text color for a given background color.
    
    This function automatically determines whether black or white text
    would be more readable on a given background color.
    
    Args:
        background_color (str): Hex color code (like "#ffffff")
        
    Returns:
        str: Either "#000000" (black) or "#ffffff" (white) for best contrast
        
    Example:
        text_color = get_contrasting_color("#1a1a1a")  # Dark background
        # Returns: "#ffffff" (white text for dark background)
        
        text_color = get_contrasting_color("#f0f0f0")  # Light background
        # Returns: "#000000" (black text for light background)
    """
    try:
        # Remove # symbol if present
        color = background_color.lstrip('#')
        
        # Convert hex to RGB values
        r = int(color[0:2], 16)  # Red component
        g = int(color[2:4], 16)  # Green component
        b = int(color[4:6], 16)  # Blue component
        
        # Calculate relative luminance (how bright the color appears to human eyes)
        # This formula accounts for how our eyes perceive different colors
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        
        # If the background is bright, use black text; if dark, use white text
        return "#000000" if luminance > 0.5 else "#ffffff"
        
    except Exception:
        # If color parsing fails, default to black text
        return "#000000"


def blend_colors(color1, color2, ratio=0.5):
    """
    Blend two colors together to create a new color.
    
    This function mixes two colors like mixing paint. You can control
    how much of each color to use with the ratio parameter.
    
    Args:
        color1 (str): First hex color (like "#ff0000" for red)
        color2 (str): Second hex color (like "#0000ff" for blue)
        ratio (float): How much of color2 to use (0.0 = all color1, 1.0 = all color2)
        
    Returns:
        str: Blended hex color
        
    Example:
        purple = blend_colors("#ff0000", "#0000ff", 0.5)  # Mix red and blue equally
        # Returns: "#800080" (purple)
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
    
    This function lets you take an existing theme and change specific
    colors to create your own personalized theme.
    
    Args:
        base_theme_name (str): Name of the theme to start with
        customizations (dict): Colors to override (like {"bg": "#ff0000"})
        
    Returns:
        dict: New custom theme dictionary
        
    Example:
        # Create a custom theme based on dark theme but with red background
        my_theme = create_custom_theme("dark", {"bg": "#330000", "accent": "#ff6666"})
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
    
    This function provides human-readable descriptions of themes
    to help users choose which one they prefer.
    
    Args:
        theme_name (str): Name of the theme
        
    Returns:
        dict: Theme preview information
        
    Example:
        preview = get_theme_preview("dark")
        print(preview["description"])
        # Prints: "Easy on the eyes with dark backgrounds and light text"
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
        "blue": {
            "description": "Ocean-inspired with calming blue tones throughout",
            "best_for": "Ocean lovers, calming atmosphere, unique aesthetic",
            "colors": "Deep blue background, light blue text, bright blue accents"
        },
        "high_contrast": {
            "description": "Maximum contrast for excellent accessibility and readability",
            "best_for": "Visual impairments, maximum readability, accessibility needs",
            "colors": "Black background, white text, yellow accents"
        },
        "sunset": {
            "description": "Warm sunset colors with purple and golden tones",
            "best_for": "Evening use, warm atmosphere, unique visual appeal",
            "colors": "Purple background, golden text, orange accents"
        },
        "forest": {
            "description": "Nature-inspired with green tones and earthy colors",
            "best_for": "Nature lovers, calming green atmosphere, outdoor enthusiasts",
            "colors": "Dark green background, light green text, emerald accents"
        }
    }
    
    return previews.get(theme_name.lower(), {
        "description": "Unknown theme",
        "best_for": "Unknown",
        "colors": "Unknown"
    })


def get_all_themes():
    """
    Get a dictionary containing all available themes.
    
    This function returns every theme that's available in the system,
    useful for creating theme selection interfaces or for testing.
    
    Returns:
        dict: Dictionary mapping theme names to theme dictionaries
        
    Example:
        all_themes = get_all_themes()
        for name, theme in all_themes.items():
            print(f"{name}: background is {theme['bg']}")
    """
    return {
        "light": LIGHT_THEME,
        "dark": DARK_THEME,
        "blue": BLUE_THEME,
        "high_contrast": HIGH_CONTRAST_THEME,
        "sunset": SUNSET_THEME,
        "forest": FOREST_THEME
    }


def validate_theme(theme_dict):
    """
    Validate that a theme dictionary has all required colors.
    
    This function checks if a theme is complete and usable by
    verifying it has all the necessary color definitions.
    
    Args:
        theme_dict (dict): Theme dictionary to validate
        
    Returns:
        tuple: (is_valid, missing_keys) - True/False and list of missing colors
        
    Example:
        valid, missing = validate_theme(my_custom_theme)
        if not valid:
            print(f"Theme is missing: {', '.join(missing)}")
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
    
    This function suggests themes based on what the user tells
    us about their preferences and needs.
    
    Args:
        preferences (dict): User preferences like {"time_of_use": "night", "priority": "accessibility"}
        
    Returns:
        list: Recommended theme names in order of preference
        
    Example:
        recommendations = get_theme_recommendations({
            "time_of_use": "night",
            "accessibility_needs": True
        })
        # Returns: ["high_contrast", "dark", "light"]
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TESTING AND EXAMPLE USAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    """
    This section runs when you execute this file directly.
    It's useful for testing theme functions and seeing all available themes.
    """
    
    print("Testing Theme Configuration System")
    print("=" * 40)
    
    # Test all available themes
    print("\n🎨 Available Themes:")
    available_themes = get_available_themes()
    
    for theme_name in available_themes:
        theme = get_theme(theme_name)
        preview = get_theme_preview(theme_name)
        
        print(f"\n📋 {theme_name.title()} Theme:")
        print(f"  Description: {preview['description']}")
        print(f"  Best for: {preview['best_for']}")
        print(f"  Background: {theme['bg']}")
        print(f"  Text: {theme['fg']}")
        print(f"  Accent: {theme['accent']}")
    
    # Test theme validation
    print(f"\n🔍 Testing Theme Validation:")
    for theme_name in available_themes:
        theme = get_theme(theme_name)
        valid, missing = validate_theme(theme)
        status = "✅ Valid" if valid else f"❌ Missing: {', '.join(missing)}"
        print(f"  {theme_name}: {status}")
    
    # Test color utilities
    print(f"\n🌈 Testing Color Utilities:")
    
    # Test contrast calculation
    test_colors = ["#ffffff", "#000000", "#ff0000", "#0000ff"]
    for color in test_colors:
        contrast = get_contrasting_color(color)
        print(f"  Background {color} → Text {contrast}")
    
    # Test color blending
    red_blue_blend = blend_colors("#ff0000", "#0000ff", 0.5)
    print(f"  Red + Blue blend: {red_blue_blend}")
    
    # Test theme recommendations
    print(f"\n💡 Testing Theme Recommendations:")
    
    test_preferences = [
        {"time_of_use": "night"},
        {"accessibility_needs": True},
        {"favorite_color": "blue", "time_of_use": "day"},
        {"favorite_color": "green"}
    ]
    
    for i, prefs in enumerate(test_preferences, 1):
        recommendations = get_theme_recommendations(prefs)
        print(f"  Preference {i} {prefs}: {', '.join(recommendations[:3])}")
    
    # Test custom theme creation
    print(f"\n🔧 Testing Custom Theme Creation:")
    custom_theme = create_custom_theme("dark", {
        "accent": "#ff6b6b",
        "button_bg": "#ff4757"
    })
    
    print(f"  Custom theme accent: {custom_theme['accent']}")
    print(f"  Custom theme button: {custom_theme['button_bg']}")
    
    print(f"\n✅ Theme system testing completed!")
    print(f"\nNote: This theme system provides {len(available_themes)} themes")
    print(f"with utilities for customization, validation, and accessibility.")
    