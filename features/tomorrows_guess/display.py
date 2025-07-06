import customtkinter as ctk

def create_tomorrow_guess_frame(parent, theme):
    """
    Creates a frame (container) to display tomorrow's weather prediction.
    
    """
    
    # Create the main container frame with background color from theme
    frame = ctk.CTkFrame(parent, fg_color=theme["bg"])
    
    # Create a label to show the predicted temperature
    temp_label = ctk.CTkLabel(
        frame, 
        text="--", 
        font=("Arial", 24, "bold"), 
        text_color=theme["text_fg"]
    )
    # Position the temperature label with padding 
    temp_label.pack(pady=(10, 5))
    
    # Create a label to show how confident we are in the prediction
    confidence_label = ctk.CTkLabel(
        frame, 
        text="Confidence: --", 
        font=("Arial", 16), 
        text_color=theme["text_fg"]
    )
    # Position with equal padding above and below 
    confidence_label.pack(pady=5)
    
    # Create a label to show how accurate our predictions have been historically
    accuracy_label = ctk.CTkLabel(
        frame, 
        text="Accuracy: --%", 
        font=("Arial", 16), 
        text_color=theme["text_fg"]
    )
    # Position with 5 pixels above, 10 pixels below 
    accuracy_label.pack(pady=(5, 10))
    
    # IMPORTANT: Store references to the labels ON the frame object
    # This allows us to update these labels later from other functions
    frame.temp_label = temp_label
    frame.confidence_label = confidence_label
    frame.accuracy_label = accuracy_label
    
    # Return the complete frame so it can be used by the main application
    return frame

def update_tomorrow_guess_display(frame, predicted_temp, confidence, accuracy):
    """
    Updates the weather display with new prediction data.
    
    """
    
    # Update the temperature display
    frame.temp_label.configure(text=predicted_temp or "N/A")
    
    # Update the confidence display
    frame.confidence_label.configure(text=f"Confidence: {confidence}")
    
    # Update the accuracy display
    frame.accuracy_label.configure(text=f"Accuracy: {accuracy}")
