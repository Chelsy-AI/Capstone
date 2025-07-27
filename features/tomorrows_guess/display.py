"""
Tomorrow's Weather Guess Display
================================================================

This file creates a visual table showing our prediction for tomorrow's weather.
Presented in a simple table format that shows:
- What temperature we think it will be tomorrow
- How accurate our predictions usually are
- How confident we are in this specific prediction
"""

import tkinter as tk


def create_tomorrow_guess_frame(parent, theme):
    """
    Create the main frame that holds our tomorrow's weather prediction table.
    
    This builds a 3-column table with:
    - Column 1: Temperature prediction
    - Column 2: Historical accuracy percentage  
    - Column 3: Confidence level for this prediction
    
    Each column has a header, an emoji icon, and a value that gets updated later.
    
    Args:
        parent: The parent widget where this frame will be placed
        theme: Theme settings (currently not used, but kept for compatibility)
        
    Returns:
        tk.Frame: The complete table frame with all elements
    """
    
    # Create the main container frame with sky blue background to match the app
    frame = tk.Frame(parent, bg="#87CEEB")
    
    # Define the table structure
    headers = ["Temperature", "Accuracy", "Confidence"]  # Column titles
    emojis = ["🌡️", "🎯", "😎"]  # Icons to make it more visual and friendly
    
    # Configure grid layout for equal column spacing
    for col in range(3):
        frame.grid_columnconfigure(col, weight=1)  # Make columns expand equally
    
    # Row 1: Create header labels
    for col, header in enumerate(headers):
        header_label = tk.Label(
            frame, 
            text=header, 
            font=("Arial", 12, "bold"),  # Bold text for headers
            fg="black",  # Black text for readability
            bg="#87CEEB",  # Match frame background
            relief="solid",  # Solid border for table appearance
            borderwidth=1,
            width=12,  # Fixed width for consistent appearance
            height=1
        )
        header_label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
    
    # Row 2: Create emoji icons for visual appeal
    for col, emoji in enumerate(emojis):
        emoji_label = tk.Label(
            frame, 
            text=emoji, 
            font=("Arial", 18),  # Larger font for emojis
            fg="black", 
            bg="#87CEEB",
            relief="solid",
            borderwidth=1,
            width=12,
            height=1
        )
        emoji_label.grid(row=1, column=col, sticky="nsew", padx=1, pady=1)
    
    # Row 3: Create value labels that will be updated with actual data
    
    # Temperature value label
    temp_label = tk.Label(
        frame, 
        text="--",  # Placeholder until we get real data
        font=("Arial", 14, "bold"),  # Bold and larger for important values
        fg="black", 
        bg="#87CEEB",
        relief="solid",
        borderwidth=1,
        width=12,
        height=1
    )
    temp_label.grid(row=2, column=0, sticky="nsew", padx=1, pady=1)
    
    # Accuracy percentage label
    accuracy_label = tk.Label(
        frame, 
        text="--",  # Placeholder until we get real data
        font=("Arial", 14, "bold"), 
        fg="black", 
        bg="#87CEEB",
        relief="solid",
        borderwidth=1,
        width=12,
        height=1
    )
    accuracy_label.grid(row=2, column=1, sticky="nsew", padx=1, pady=1)
    
    # Confidence level label
    confidence_label = tk.Label(
        frame, 
        text="--",  # Placeholder until we get real data
        font=("Arial", 14, "bold"), 
        fg="black", 
        bg="#87CEEB",
        relief="solid",
        borderwidth=1,
        width=12,
        height=1
    )
    confidence_label.grid(row=2, column=2, sticky="nsew", padx=1, pady=1)
    
    # Store references to the value labels on the frame object itself
    frame.temp_label = temp_label
    frame.accuracy_label = accuracy_label  
    frame.confidence_label = confidence_label
    
    return frame


def update_tomorrow_guess_display(frame, predicted_temp, confidence, accuracy):
    """
    Update the prediction table with new data.
    
    This function is called whenever we have new prediction data to show.
    It finds the value labels in the table and updates them with the latest information.
    
    Args:
        frame: The table frame created by create_tomorrow_guess_frame()
        predicted_temp: Tomorrow's predicted temperature (number or None)
        confidence: How confident we are in this prediction (string with %)
        accuracy: Historical accuracy percentage (number or None)
    """
    
    # Update the temperature display
    if hasattr(frame, 'temp_label'):
        if predicted_temp is not None:
            # Format temperature with degree symbol and unit
            # We assume Fahrenheit here, but this could be made configurable
            frame.temp_label.configure(text=f"{predicted_temp}°F")
        else:
            # Show placeholder if no temperature data available
            frame.temp_label.configure(text="--")
    
    # Update the accuracy display
    if hasattr(frame, 'accuracy_label'):
        if isinstance(accuracy, (int, float)):
            # Format as percentage
            frame.accuracy_label.configure(text=f"{accuracy}%")
        else:
            # Show placeholder if no accuracy data available
            frame.accuracy_label.configure(text="--")
    
    # Update the confidence display
    if hasattr(frame, 'confidence_label'):
        if confidence and confidence != "N/A":
            # Clean up confidence text and ensure it has % symbol
            conf_text = str(confidence).replace('%', '') + '%'
            frame.confidence_label.configure(text=conf_text)
        else:
            # Show placeholder if no confidence data available
            frame.confidence_label.configure(text="--")


def get_table_dimensions():
    """
    Get the standard dimensions for the prediction table.
    
    Returns:
        dict: Dictionary with width, height, and other dimension info
    """
    return {
        'width': 320,  # Total table width in pixels
        'height': 90,  # Total table height in pixels  
        'columns': 3,  # Number of columns
        'rows': 3,     # Number of rows
        'cell_width': 12,  # Character width of each cell
        'cell_height': 1   # Character height of each cell
    }


def validate_prediction_data(predicted_temp, confidence, accuracy):
    """
    Check if prediction data is valid and reasonable.
    
    Args:
        predicted_temp: Temperature prediction to validate
        confidence: Confidence value to validate  
        accuracy: Accuracy value to validate
        
    Returns:
        tuple: (is_valid, error_message)
            - is_valid: True if data looks reasonable, False otherwise
            - error_message: Description of what's wrong (or None if valid)
    """
    
    # Check temperature range (should be reasonable for Earth weather)
    if predicted_temp is not None:
        if not isinstance(predicted_temp, (int, float)):
            return False, "Temperature must be a number"
        if predicted_temp < -100 or predicted_temp > 150:  # Extreme but possible range
            return False, f"Temperature {predicted_temp}°F seems unrealistic"
    
    # Check accuracy range (should be 0-100%)
    if accuracy is not None:
        if not isinstance(accuracy, (int, float)):
            return False, "Accuracy must be a number"
        if accuracy < 0 or accuracy > 100:
            return False, f"Accuracy {accuracy}% should be between 0-100%"
    
    # Check confidence format
    if confidence and confidence != "N/A":
        try:
            # Try to extract number from confidence string
            conf_num = float(str(confidence).replace('%', ''))
            if conf_num < 0 or conf_num > 100:
                return False, f"Confidence {confidence} should be between 0-100%"
        except ValueError:
            return False, f"Confidence '{confidence}' is not a valid percentage"
    
    # If we get here, everything looks reasonable
    return True, None


def format_temperature_for_display(temp_value, unit="F"):
    """
    Format a temperature value for display in the table.
    
    Args:
        temp_value: Temperature to format (number, string, or None)
        unit: Temperature unit ("F" for Fahrenheit, "C" for Celsius)
        
    Returns:
        str: Formatted temperature string ready for display
    """
    
    if temp_value is None:
        return "--"
    
    try:
        # Convert to number if it's a string
        if isinstance(temp_value, str):
            # Remove any existing degree symbols or units
            temp_clean = temp_value.replace('°', '').replace('F', '').replace('C', '').strip()
            temp_num = float(temp_clean)
        else:
            temp_num = float(temp_value)
        
        # Format with appropriate precision
        if temp_num == int(temp_num):
            # Show whole numbers without decimal
            return f"{int(temp_num)}°{unit}"
        else:
            # Show one decimal place for fractional temperatures
            return f"{temp_num:.1f}°{unit}"
            
    except (ValueError, TypeError):
        # If conversion fails, return placeholder
        return "--"


def format_percentage_for_display(percent_value):
    """
    Format a percentage value for display in the table.
        
    Args:
        percent_value: Percentage to format (number, string, or None)
        
    Returns:
        str: Formatted percentage string ready for display
    """
    
    if percent_value is None:
        return "--"
    
    try:
        # Convert to number if it's a string
        if isinstance(percent_value, str):
            # Remove any existing % symbols
            percent_clean = percent_value.replace('%', '').strip()
            percent_num = float(percent_clean)
        else:
            percent_num = float(percent_value)
        
        # Ensure it's within reasonable bounds
        percent_num = max(0, min(100, percent_num))
        
        # Format with appropriate precision
        if percent_num == int(percent_num):
            return f"{int(percent_num)}%"
        else:
            return f"{percent_num:.1f}%"
            
    except (ValueError, TypeError):
        return "--"


def create_enhanced_tomorrow_frame(parent, theme, show_details=False):
    """
    Create an enhanced version of the tomorrow's guess frame with optional details.
    
    Args:
        parent: Parent widget for the frame
        theme: Theme settings
        show_details: Whether to include additional detail rows
        
    Returns:
        tk.Frame: Enhanced prediction frame
    """
    
    # Start with the basic frame
    frame = create_tomorrow_guess_frame(parent, theme)
    
    if show_details:
        # Add additional information rows
        
        # Method used for prediction
        method_label = tk.Label(
            frame,
            text="Method: Machine Learning",
            font=("Arial", 10),
            fg="gray",
            bg="#87CEEB",
            anchor="w"
        )
        method_label.grid(row=3, column=0, columnspan=3, sticky="w", padx=5, pady=2)
        
        # Data freshness indicator
        freshness_label = tk.Label(
            frame,
            text="Data updated: Recently",
            font=("Arial", 10),
            fg="gray", 
            bg="#87CEEB",
            anchor="w"
        )
        freshness_label.grid(row=4, column=0, columnspan=3, sticky="w", padx=5, pady=2)
        
        # Store additional labels for updates
        frame.method_label = method_label
        frame.freshness_label = freshness_label
    
    return frame