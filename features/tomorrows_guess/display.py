# display.py
import customtkinter as ctk

def create_tomorrow_guess_frame(parent, theme):
    frame = ctk.CTkFrame(parent, fg_color=theme["text_bg"], corner_radius=8)
    frame.pack(pady=10, fill="x", padx=10)

    temp_label = ctk.CTkLabel(frame, text="--", font=("Arial", 24, "bold"), text_color=theme["text_fg"])
    temp_label.pack(pady=(10, 5))

    confidence_label = ctk.CTkLabel(frame, text="Confidence: --", font=("Arial", 16), text_color=theme["text_fg"])
    confidence_label.pack(pady=5)

    accuracy_label = ctk.CTkLabel(frame, text="Accuracy: --%", font=("Arial", 16), text_color=theme["text_fg"])
    accuracy_label.pack(pady=(5, 10))

    frame.temp_label = temp_label
    frame.confidence_label = confidence_label
    frame.accuracy_label = accuracy_label

    return frame

def update_tomorrow_guess_display(frame, predicted_temp, confidence, accuracy):
    frame.temp_label.configure(text=predicted_temp or "N/A")
    frame.confidence_label.configure(text=f"Confidence: {confidence}")
    frame.accuracy_label.configure(text=f"Accuracy: {accuracy}")
