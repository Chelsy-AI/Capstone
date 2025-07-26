"""
Language Controller - Main Language Management System
====================================================

Main controller that manages language selection, translation, and coordination
between different components of the weather application.
"""

import json
import os
import tkinter as tk
from tkinter import ttk
from .translations import TRANSLATIONS, SUPPORTED_LANGUAGES


class LanguageController:
    """
    Main Language Controller for Weather App
    
    Manages language selection and translation of ALL text elements
    with proper consistency and fallback handling.
    """
    
    def __init__(self, app, gui_controller):
        """
        Initialize the language controller.
        
        Args:
            app: Main weather application instance
            gui_controller: GUI controller that manages the interface
        """
        self.app = app
        self.gui = gui_controller
        
        # Language data
        self.supported_languages = SUPPORTED_LANGUAGES
        self.translations = TRANSLATIONS
        
        # Current language (default to English)
        self.current_language = "English"
        
        # Language settings file path
        self.settings_file = "language_settings.json"
        
        # Widget references for the language selection page
        self.language_widgets = []
        self.language_dropdown = None
        self.language_var = None
        
        # Load saved language settings
        self.load_settings()

    def get_text(self, key, fallback_to_english=True):
        """
        Get translated text for a given key with proper fallback handling.
        
        Args:
            key (str): Text key to translate
            fallback_to_english (bool): Whether to fallback to English if translation missing
            
        Returns:
            str: Translated text, English fallback, or key if nothing found
        """
        try:
            # Try to get translation in current language
            translation = self.translations.get(self.current_language, {}).get(key)
            
            if translation:
                return translation
            
            # Fallback to English if translation missing and fallback enabled
            if fallback_to_english and self.current_language != "English":
                english_translation = self.translations.get("English", {}).get(key)
                if english_translation:
                    return english_translation
            
            # Return the key itself if no translation found
            return key
            
        except Exception:
            # If anything goes wrong, return the key
            return key

    def update_all_translatable_widgets(self):
        """
        Update ALL widgets in the app that contain translatable text.
        
        This is called when language changes to ensure EVERY text element
        is properly updated throughout the entire application.
        """
        try:
            # Update app title
            self.update_app_title()
            
            # Get current page and trigger complete rebuild
            current_page = self.gui.current_page
            
            # Force complete page rebuild with new language
            self.gui.show_page(current_page)
            
            # Update any existing weather data display with new units
            if hasattr(self.app, 'current_weather_data') and self.app.current_weather_data:
                self.gui.update_weather_display(self.app.current_weather_data)
            
            # Update prediction display if available
            if hasattr(self.app, 'current_prediction_data') and self.app.current_prediction_data:
                predicted_temp, confidence, accuracy = self.app.current_prediction_data
                self.gui.update_tomorrow_prediction_direct(predicted_temp, confidence, accuracy)
            
        except Exception as e:
            # If update fails, continue gracefully
            pass

    def build_page(self, window_width, window_height):
        """
        Build the language selection page with proper translations.
        """
        # Clear existing widgets first
        self._clear_widgets()
        
        # Add back button
        self._add_back_button()
        
        # Page title
        title_text = self.get_text("language_selection")
        title = self._create_label(
            self.app,
            text=title_text,
            font=("Arial", int(24 + window_width/50), "bold"),
            fg=self.app.text_color,
            x=window_width/2,
            y=150
        )
        self.language_widgets.append(title)
        
        # Language selection label
        select_text = self.get_text("select_language")
        select_label = self._create_label(
            self.app,
            text=select_text,
            font=("Arial", int(16 + window_width/60)),
            fg=self.app.text_color,
            x=window_width/2,
            y=220
        )
        self.language_widgets.append(select_label)
        
        # Language dropdown
        self._create_language_dropdown(window_width, window_height)
        
        # Apply button
        self._create_apply_button(window_width, window_height)
        
        # Current language indicator
        current_text = f"{self.get_text('current_language')}: {self.current_language}"
        current_label = self._create_label(
            self.app,
            text=current_text,
            font=("Arial", int(14 + window_width/70)),
            fg=self.app.text_color,
            x=window_width/2,
            y=400
        )
        self.language_widgets.append(current_label)

    def _create_language_dropdown(self, window_width, window_height):
        """Create the language selection dropdown."""
        canvas_bg = "#87CEEB"
        if hasattr(self.gui, 'bg_canvas') and self.gui.bg_canvas:
            try:
                canvas_bg = self.gui.bg_canvas.cget("bg")
            except:
                canvas_bg = "#87CEEB"
        
        dropdown_frame = tk.Frame(
            self.app,
            bg=canvas_bg,
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        dropdown_frame.place(x=window_width/2, y=280, anchor="center")
        
        self.language_var = tk.StringVar(value=self.current_language)
        
        self.language_dropdown = ttk.Combobox(
            dropdown_frame,
            textvariable=self.language_var,
            values=self.get_supported_language_names(),
            state="readonly",
            font=("Arial", int(14 + window_width/80)),
            width=15,
            justify="center"
        )
        self.language_dropdown.pack()
        
        self.language_widgets.append(dropdown_frame)

    def _create_apply_button(self, window_width, window_height):
        """Create the apply language button."""
        apply_text = self.get_text("apply")
        apply_btn = tk.Button(
            self.app,
            text=apply_text,
            command=self.apply_language_change,
            bg="grey",
            fg="black",
            font=("Arial", int(14 + window_width/70), "bold"),
            relief="raised",
            borderwidth=2,
            width=12,
            height=2,
            activeforeground="black",
            activebackground="lightgrey",
            highlightthickness=0
        )
        apply_btn.place(x=window_width/2, y=340, anchor="center")
        self.language_widgets.append(apply_btn)

    def _add_back_button(self):
        """Add a back button to return to the main page."""
        back_text = self.get_text("back")
        back_btn = tk.Button(
            self.app,
            text=back_text,
            command=self._go_back_to_main,
            bg="grey",
            fg="black",
            font=("Arial", 12, "bold"),
            relief="raised",
            borderwidth=2,
            width=8,
            height=1,
            activeforeground="black",
            activebackground="lightgrey",
            highlightthickness=0
        )
        back_btn.place(x=50, y=50, anchor="center")
        self.language_widgets.append(back_btn)

    def _go_back_to_main(self):
        """Go back to main page and ensure language widgets are cleared."""
        self._clear_widgets()
        self.gui.show_page("main")

    def _create_label(self, parent, text, font, fg, x, y, anchor="center", **kwargs):
        """Create a label with transparent background."""
        canvas_bg = "#87CEEB"
        if hasattr(self.gui, 'bg_canvas') and self.gui.bg_canvas:
            try:
                canvas_bg = self.gui.bg_canvas.cget("bg")
            except:
                canvas_bg = "#87CEEB"
        
        label = tk.Label(
            parent,
            text=text,
            font=font,
            fg=fg,
            bg=canvas_bg,
            anchor=anchor,
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            **kwargs
        )
        label.place(x=x, y=y, anchor=anchor)
        return label

    def _clear_widgets(self):
        """Clear language selection widgets."""
        for widget in self.language_widgets:
            try:
                widget.destroy()
            except:
                pass
        self.language_widgets.clear()
        
        self.language_dropdown = None
        self.language_var = None

    def apply_language_change(self):
        """Apply the selected language change and update ALL translatable text."""
        try:
            if self.language_var:
                new_language = self.language_var.get()
                if new_language != self.current_language:
                    # Change language
                    self.current_language = new_language
                    self.save_settings()
                    
                    # Clear language page widgets first
                    self._clear_widgets()
                    
                    # Update ALL translatable text throughout the app
                    self.update_all_translatable_widgets()
                    
                    # Fetch weather data in new language
                    if hasattr(self.app, 'fetch_and_display'):
                        self.app.fetch_and_display()
                else:
                    # No change, just go back
                    self._go_back_to_main()
        except Exception as e:
            # If something goes wrong, just go back to main
            self._go_back_to_main()

    def get_language_code(self):
        """Get the OpenWeatherMap API language code for current language."""
        return self.supported_languages.get(self.current_language, "en")

    def update_app_title(self):
        """Update the application window title."""
        try:
            title = self.get_text("weather_app_title")
            self.app.title(title)
        except:
            pass

    def save_settings(self):
        """Save language settings to file."""
        try:
            settings = {"current_language": self.current_language}
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def load_settings(self):
        """Load language settings from file."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_language = settings.get("current_language", "English")
        except Exception:
            self.current_language = "English"

    def cleanup(self):
        """Clean up language controller resources."""
        self._clear_widgets()

    def get_moon_phase_translation(self, phase_name):
        """
        Get translated moon phase name.
        
        Args:
            phase_name (str): English moon phase name
            
        Returns:
            str: Translated moon phase name
        """
        # Normalize phase name to lowercase and replace spaces with underscores
        normalized_phase = phase_name.lower().replace(" ", "_")
        return self.get_text(normalized_phase, fallback_to_english=True)

    def get_weather_condition_translation(self, condition):
        """
        Get translated weather condition.
        
        Args:
            condition (str): English weather condition
            
        Returns:
            str: Translated weather condition
        """
        # Normalize condition to lowercase and replace spaces with underscores
        normalized_condition = condition.lower().replace(" ", "_")
        return self.get_text(normalized_condition, fallback_to_english=True)

    def get_unit_translation(self, unit):
        """
        Get translated unit symbol.
        
        Args:
            unit (str): Unit identifier
            
        Returns:
            str: Translated unit symbol
        """
        return self.get_text(unit, fallback_to_english=True)

    def get_direction_translation(self, direction):
        """
        Get translated direction name.
        
        Args:
            direction (str): Direction name (e.g., "East", "West")
            
        Returns:
            str: Translated direction name
        """
        normalized_direction = direction.lower()
        return self.get_text(normalized_direction, fallback_to_english=True)

    def get_season_translation(self, season):
        """
        Get translated season name.
        
        Args:
            season (str): Season name
            
        Returns:
            str: Translated season name
        """
        normalized_season = season.lower()
        return self.get_text(normalized_season, fallback_to_english=True)

    def format_time_with_translation(self, time_str, period=None):
        """
        Format time string with translated period indicators.
        
        Args:
            time_str (str): Time string
            period (str): Optional period indicator ("morning", "evening")
            
        Returns:
            str: Formatted time string with translations
        """
        if not time_str:
            return self.get_text("not_available")
        
        if period:
            period_translation = self.get_text(period.lower(), fallback_to_english=True)
            return f"{time_str} ({period_translation})"
        
        return time_str

    def validate_translation_key(self, key):
        """
        Check if a translation key exists in current language.
        
        Args:
            key (str): Translation key to check
            
        Returns:
            bool: True if key exists, False otherwise
        """
        return key in self.translations.get(self.current_language, {})

    def get_all_available_keys(self):
        """
        Get all available translation keys for current language.
        
        Returns:
            list: List of available translation keys
        """
        return list(self.translations.get(self.current_language, {}).keys())

    def get_language_display_name(self, language_code):
        """
        Get display name for a language code.
        
        Args:
            language_code (str): Language code (e.g., "en", "es", "hi")
            
        Returns:
            str: Display name of the language
        """
        for display_name, code in self.supported_languages.items():
            if code == language_code:
                return display_name
        return "English"  # Default fallback

    def is_rtl_language(self):
        """
        Check if current language is right-to-left.
        
        Returns:
            bool: True if RTL language, False otherwise
        """
        # Hindi uses Devanagari script which is left-to-right
        # Spanish and English are also left-to-right
        # Add RTL languages here if needed in the future
        return False

    def get_font_family_for_language(self):
        """
        Get appropriate font family for current language.
        
        Returns:
            str: Font family name
        """
        if self.current_language == "Hindi":
            # Use fonts that support Devanagari script
            return "Noto Sans Devanagari"
        elif self.current_language == "Spanish":
            return "Arial"
        else:  # English
            return "Arial"

    def format_number_with_locale(self, number, unit_key=None):
        """
        Format number according to current language locale.
        
        Args:
            number (float/int): Number to format
            unit_key (str): Optional unit key for translation
            
        Returns:
            str: Formatted number with optional unit
        """
        try:
            if isinstance(number, (int, float)):
                formatted_number = f"{number:.1f}" if isinstance(number, float) else str(number)
                
                if unit_key:
                    unit = self.get_text(unit_key, fallback_to_english=True)
                    return f"{formatted_number}{unit}"
                
                return formatted_number
            else:
                return str(number)
        except:
            return str(number)

    def get_error_message(self, error_type):
        """
        Get localized error message.
        
        Args:
            error_type (str): Type of error
            
        Returns:
            str: Localized error message
        """
        error_messages = {
            "network": "network_error",
            "city_not_found": "city_not_found", 
            "loading": "error_loading_data",
            "general": "error"
        }
        
        key = error_messages.get(error_type, "error")
        return self.get_text(key)

    def get_status_message(self, status_type):
        """
        Get localized status message.
        
        Args:
            status_type (str): Type of status
            
        Returns:
            str: Localized status message
        """
        status_messages = {
            "loading": "loading",
            "fetching": "fetching_weather",
            "refresh": "refresh",
            "try_again": "try_again"
        }
        
        key = status_messages.get(status_type, "loading")
        return self.get_text(key)

    def get_supported_language_codes(self):
        """
        Get list of supported language codes.
        
        Returns:
            list: List of language codes
        """
        return list(self.supported_languages.values())

    def get_supported_language_names(self):
        """
        Get list of supported language display names.
        
        Returns:
            list: List of language display names
        """
        return list(self.supported_languages.keys())

    def reset_to_defaults(self):
        """Reset language settings to defaults."""
        self.current_language = "English"
        self.save_settings()
        self.update_all_translatable_widgets()