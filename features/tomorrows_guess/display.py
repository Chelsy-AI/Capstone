import customtkinter as ctk

def create_tomorrow_guess_frame(parent, theme):
    """
    Creates a transparent frame to display tomorrow's weather prediction.
    """
    
    # Create the main container frame - transparent
    frame = ctk.CTkFrame(parent, fg_color="transparent", corner_radius=0)
    
    # Create prediction info grid - transparent
    info_grid = ctk.CTkFrame(frame, fg_color="transparent")
    info_grid.pack(fill="x", padx=10)
    
    # Configure grid columns
    info_grid.grid_columnconfigure((0, 1, 2), weight=1)
    
    # Temperature prediction - transparent
    temp_section = ctk.CTkFrame(
        info_grid, 
        fg_color="transparent",
        corner_radius=0
    )
    temp_section.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
    
    ctk.CTkLabel(
        temp_section,
        text="🌡️",
        font=("Arial", 24),
        text_color="white",
        fg_color="transparent"
    ).pack(pady=(5, 0))
    
    ctk.CTkLabel(
        temp_section,
        text="Temperature",
        font=("Arial", 12, "bold"),
        text_color="white",
        fg_color="transparent"
    ).pack()
    
    temp_label = ctk.CTkLabel(
        temp_section, 
        text="--", 
        font=("Arial", 16, "bold"), 
        text_color="yellow",
        fg_color="transparent"
    )
    temp_label.pack(pady=(0, 5))
    
    # Confidence section - transparent
    confidence_section = ctk.CTkFrame(
        info_grid,
        fg_color="transparent",
        corner_radius=0
    )
    confidence_section.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
    
    ctk.CTkLabel(
        confidence_section,
        text="📊",
        font=("Arial", 24),
        text_color="white",
        fg_color="transparent"
    ).pack(pady=(5, 0))
    
    ctk.CTkLabel(
        confidence_section,
        text="Confidence",
        font=("Arial", 12, "bold"),
        text_color="white",
        fg_color="transparent"
    ).pack()
    
    confidence_label = ctk.CTkLabel(
        confidence_section, 
        text="--", 
        font=("Arial", 14), 
        text_color="lightgreen",
        fg_color="transparent"
    )
    confidence_label.pack(pady=(0, 5))
    
    # Accuracy section - transparent
    accuracy_section = ctk.CTkFrame(
        info_grid,
        fg_color="transparent",
        corner_radius=0
    )
    accuracy_section.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
    
    ctk.CTkLabel(
        accuracy_section,
        text="🎯",
        font=("Arial", 24),
        text_color="white",
        fg_color="transparent"
    ).pack(pady=(5, 0))
    
    ctk.CTkLabel(
        accuracy_section,
        text="Accuracy",
        font=("Arial", 12, "bold"),
        text_color="white",
        fg_color="transparent"
    ).pack()
    
    accuracy_label = ctk.CTkLabel(
        accuracy_section, 
        text="--%", 
        font=("Arial", 14), 
        text_color="lightcoral",
        fg_color="transparent"
    )
    accuracy_label.pack(pady=(0, 5))
    
    # Store references to the labels ON the frame object
    frame.temp_label = temp_label
    frame.confidence_label = confidence_label
    frame.accuracy_label = accuracy_label
    
    return frame

def update_tomorrow_guess_display(frame, predicted_temp, confidence, accuracy):
    """
    Updates the weather display with new prediction data.
    """
    
    # Update the temperature display
    if hasattr(frame, 'temp_label'):
        frame.temp_label.configure(text=str(predicted_temp) if predicted_temp != "N/A" else "N/A")
    
    # Update the confidence display
    if hasattr(frame, 'confidence_label'):
        frame.confidence_label.configure(text=str(confidence) if confidence != "N/A" else "N/A")
    
    # Update the accuracy display
    if hasattr(frame, 'accuracy_label'):
        if isinstance(accuracy, (int, float)):
            frame.accuracy_label.configure(text=f"{accuracy}%")
        else:
            frame.accuracy_label.configure(text=str(accuracy) if accuracy != "N/A" else "N/A")