import tkinter as tk

def create_tomorrow_guess_frame(parent, theme):
    """
    Creates a table-style frame to display tomorrow's weather prediction.
    Format:
    | Temperature | Accuracy | Confidence |
    | 🌡️          | 💯       | 😎         |
    | 80.9F       | 85%      | 90%        |
    """
    
    # Create the main container frame - transparent
    frame = tk.Frame(parent, bg="#87CEEB")
    
    # Table headers
    headers = ["Temperature", "Accuracy", "Confidence"]
    emojis = ["🌡️", "💯", "😎"]
    
    # Header row
    for col, header in enumerate(headers):
        header_label = tk.Label(
            frame, 
            text=header, 
            font=("Arial", 12, "bold"), 
            fg="black", 
            bg="#87CEEB",
            relief="solid",
            borderwidth=1,
            width=12,
            height=1
        )
        header_label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
    
    # Emoji row
    for col, emoji in enumerate(emojis):
        emoji_label = tk.Label(
            frame, 
            text=emoji, 
            font=("Arial", 18), 
            fg="black", 
            bg="#87CEEB",
            relief="solid",
            borderwidth=1,
            width=12,
            height=1
        )
        emoji_label.grid(row=1, column=col, sticky="nsew", padx=1, pady=1)
    
    # Value row - create labels that we can update
    temp_label = tk.Label(
        frame, 
        text="--", 
        font=("Arial", 14, "bold"), 
        fg="black", 
        bg="#87CEEB",
        relief="solid",
        borderwidth=1,
        width=12,
        height=1
    )
    temp_label.grid(row=2, column=0, sticky="nsew", padx=1, pady=1)
    
    accuracy_label = tk.Label(
        frame, 
        text="--", 
        font=("Arial", 14, "bold"), 
        fg="black", 
        bg="#87CEEB",
        relief="solid",
        borderwidth=1,
        width=12,
        height=1
    )
    accuracy_label.grid(row=2, column=1, sticky="nsew", padx=1, pady=1)
    
    confidence_label = tk.Label(
        frame, 
        text="--", 
        font=("Arial", 14, "bold"), 
        fg="black", 
        bg="#87CEEB",
        relief="solid",
        borderwidth=1,
        width=12,
        height=1
    )
    confidence_label.grid(row=2, column=2, sticky="nsew", padx=1, pady=1)
    
    # Configure grid weights for proper sizing
    for col in range(3):
        frame.grid_columnconfigure(col, weight=1)
    
    # Store references to the value labels ON the frame object
    frame.temp_label = temp_label
    frame.accuracy_label = accuracy_label
    frame.confidence_label = confidence_label
    
    return frame


def update_tomorrow_guess_display(frame, predicted_temp, confidence, accuracy):
    """
    Updates the table display with new prediction data.
    """
    
    # Update the temperature display
    if hasattr(frame, 'temp_label'):
        if predicted_temp is not None:
            # Format temperature with unit (assuming Fahrenheit as shown in example)
            frame.temp_label.configure(text=f"{predicted_temp}°F")
        else:
            frame.temp_label.configure(text="--")
    
    # Update the accuracy display
    if hasattr(frame, 'accuracy_label'):
        if isinstance(accuracy, (int, float)):
            frame.accuracy_label.configure(text=f"{accuracy}%")
        else:
            frame.accuracy_label.configure(text="--")
    
    # Update the confidence display
    if hasattr(frame, 'confidence_label'):
        if confidence and confidence != "N/A":
            # Remove the % if it's already included
            conf_text = str(confidence).replace('%', '') + '%'
            frame.confidence_label.configure(text=conf_text)
        else:
            frame.confidence_label.configure(text="--")