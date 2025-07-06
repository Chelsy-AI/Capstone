"""
Error Handler Module
===================

This module provides error handling functionality for the Weather App.
It uses Tkinter's messagebox to display user-friendly error messages
when things go wrong (API failures, network issues, etc.).

Key Features:
- Centralized error message display
- User-friendly error dialogs
- Consistent error handling across the application

"""

from tkinter import messagebox


def handle_errors(error):
    """
    Display an error message in a pop-up dialog box
    
    This function creates a standardized error dialog that shows error messages
    to the user in a clear, user-friendly way. It's used throughout the application
    to handle various types of errors like API failures, network issues, or
    invalid user input.
    
    Note:
        - The dialog box has a title "Error" and shows the provided error message
        - The dialog is modal, meaning users must close it before continuing
        - Uses Tkinter's messagebox for consistency with the GUI framework
        
    """
    # Display an error message dialog with the given error text
    # The first parameter "Error" is the dialog title
    # The second parameter is the error message to display
    messagebox.showerror("Error", error)