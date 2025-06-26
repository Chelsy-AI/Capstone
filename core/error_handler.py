from tkinter import messagebox

# Displays an error message in a pop-up alert box using Tkinter.
def handle_errors(error):
    messagebox.showerror("Error", error)
