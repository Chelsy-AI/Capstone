from tkinter import messagebox

# Displays an error message in a pop-up alert box using Tkinter.
def handle_errors(error):
    """
    Show an error message dialog with the given error text.
    """
    messagebox.showerror("Error", error)
