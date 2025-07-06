"""
User Preferences Module

Handles persistent storage and retrieval of user theme preferences.
Provides a robust system for saving user settings to disk and loading them
on application startup.

Features:
    - JSON-based preference storage
    - Automatic directory creation
    - Error handling and validation
    - Backup and recovery mechanisms
    - Cross-platform compatibility

Storage Format:
    Preferences are stored as JSON in the user's application data directory.
"""

import json
import logging
import os
from pathlib import Path
from typing import Optional, Dict, Any
import tempfile

# Configure logging for preference operations
logger = logging.getLogger(__name__)

# Constants for preference management
PREFERENCES_FILENAME = "weather_app_preferences.json"
BACKUP_FILENAME = "weather_app_preferences_backup.json"
DEFAULT_THEME = "light"

# Valid theme values for validation
VALID_THEMES = {"light", "dark", "system"}


def save_user_theme_preference(theme: str) -> bool:
    """
    Save the user's theme preference to persistent storage.
    
    Stores the theme preference in a JSON file in the user's application
    data directory. Creates necessary directories if they don't exist.
    
    """
    # Validate theme input
    if theme not in VALID_THEMES:
        logger.error(f"Invalid theme '{theme}'. Valid themes: {VALID_THEMES}")
        raise ValueError(f"Invalid theme: {theme}")
    
    try:
        # Get preferences file path
        prefs_path = get_preference_file_path()
        
        # Load existing preferences or create new ones
        preferences = _load_preferences_dict() or {}
        
        # Create backup before modifying
        _create_backup(preferences)
        
        # Update theme preference
        preferences["theme"] = theme
        preferences["last_updated"] = _get_timestamp()
        
        # Ensure parent directory exists
        prefs_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save preferences to file
        with open(prefs_path, 'w', encoding='utf-8') as f:
            json.dump(preferences, f, indent=2)
        
        logger.info(f"Theme preference '{theme}' saved successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error saving theme preference: {e}")
        return False


def load_user_theme_preference() -> Optional[str]:
    """
    Load the user's saved theme preference.
    
    Retrieves the theme preference from persistent storage.
    Returns None if no preference is found or if loading fails.
    
    """
    try:
        preferences = _load_preferences_dict()
        
        if not preferences:
            logger.info("No preferences file found")
            return None
        
        theme = preferences.get("theme")
        
        # Validate loaded theme
        if theme and theme in VALID_THEMES:
            logger.info(f"Loaded theme preference: {theme}")
            return theme
        else:
            logger.warning(f"Invalid theme in preferences: {theme}")
            return None
            
    except Exception as e:
        logger.error(f"Error loading theme preference: {e}")
        return None


def clear_user_preferences() -> bool:
    """
    Clear all user preferences.
    
    Removes the preferences file from storage. Useful for reset functionality
    or when troubleshooting preference-related issues.
    
    """
    try:
        prefs_path = get_preference_file_path()
        
        if prefs_path.exists():
            # Create backup before deletion
            preferences = _load_preferences_dict()
            if preferences:
                _create_backup(preferences)
            
            # Remove preferences file
            prefs_path.unlink()
            logger.info("User preferences cleared successfully")
            return True
        else:
            logger.info("No preferences file to clear")
            return True
            
    except Exception as e:
        logger.error(f"Error clearing preferences: {e}")
        return False


def get_preference_file_path() -> Path:
    """
    Get the full path to the preferences file.
    
    Determines the appropriate location for storing preferences based on
    the operating system and user environment.
    
    """
    try:
        # Try to get user-specific application data directory
        if os.name == 'nt':  # Windows
            app_data = os.environ.get('APPDATA')
            if app_data:
                base_dir = Path(app_data) / "WeatherApp"
            else:
                base_dir = Path.home() / ".weather_app"
        else:  # macOS, Linux, etc.
            base_dir = Path.home() / ".weather_app"
        
        return base_dir / PREFERENCES_FILENAME
        
    except Exception as e:
        logger.error(f"Error determining preferences path: {e}")
        # Fallback to temp directory
        return Path(tempfile.gettempdir()) / PREFERENCES_FILENAME


def backup_preferences() -> bool:
    """
    Create a backup of current preferences.
    
    Creates a backup copy of the preferences file for recovery purposes.
    
    """
    try:
        preferences = _load_preferences_dict()
        if not preferences:
            logger.info("No preferences to backup")
            return True
        
        return _create_backup(preferences)
        
    except Exception as e:
        logger.error(f"Error creating preferences backup: {e}")
        return False


def restore_preferences_from_backup() -> bool:
    """
    Restore preferences from backup file.
    
    Attempts to restore preferences from the backup file if the main
    preferences file is corrupted or missing.
    
    """
    try:
        backup_path = get_preference_file_path().parent / BACKUP_FILENAME
        
        if not backup_path.exists():
            logger.warning("No backup file found")
            return False
        
        # Load backup preferences
        with open(backup_path, 'r', encoding='utf-8') as f:
            backup_preferences = json.load(f)
        
        # Validate backup data
        if not isinstance(backup_preferences, dict):
            logger.error("Invalid backup file format")
            return False
        
        # Restore preferences
        prefs_path = get_preference_file_path()
        prefs_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(prefs_path, 'w', encoding='utf-8') as f:
            json.dump(backup_preferences, f, indent=2)
        
        logger.info("Preferences restored from backup successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error restoring preferences from backup: {e}")
        return False


def get_preferences_info() -> Dict[str, Any]:
    """
    Get information about the current preferences setup.
    
    Returns diagnostic information about preferences including file paths,
    existence status, and current settings.
    
    """
    try:
        prefs_path = get_preference_file_path()
        backup_path = prefs_path.parent / BACKUP_FILENAME
        
        info = {
            "preferences_file": str(prefs_path),
            "backup_file": str(backup_path),
            "preferences_exists": prefs_path.exists(),
            "backup_exists": backup_path.exists(),
            "current_theme": load_user_theme_preference(),
            "file_size": prefs_path.stat().st_size if prefs_path.exists() else 0,
            "last_modified": None
        }
        
        # Get last modified time if file exists
        if prefs_path.exists():
            info["last_modified"] = prefs_path.stat().st_mtime
        
        return info
        
    except Exception as e:
        logger.error(f"Error getting preferences info: {e}")
        return {"error": str(e)}


def _load_preferences_dict() -> Optional[Dict[str, Any]]:
    """
    Load preferences dictionary from file.
    
    Internal function to load and validate the preferences file.
    
    """
    try:
        prefs_path = get_preference_file_path()
        
        if not prefs_path.exists():
            return None
        
        with open(prefs_path, 'r', encoding='utf-8') as f:
            preferences = json.load(f)
        
        # Validate that preferences is a dictionary
        if not isinstance(preferences, dict):
            logger.error("Preferences file contains invalid data format")
            return None
        
        return preferences
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in preferences file: {e}")
        # Try to restore from backup
        if restore_preferences_from_backup():
            return _load_preferences_dict()  # Recursive call after restore
        return None
        
    except Exception as e:
        logger.error(f"Error loading preferences: {e}")
        return None


def _create_backup(preferences: Dict[str, Any]) -> bool:
    """
    Create a backup of the preferences dictionary.
    
    Internal function to create a backup copy of preferences.
    
    """
    try:
        backup_path = get_preference_file_path().parent / BACKUP_FILENAME
        
        # Ensure parent directory exists
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(preferences, f, indent=2)
        
        logger.info("Preferences backup created successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error creating backup: {e}")
        return False


def _get_timestamp() -> str:
    """
    Get current timestamp as ISO format string.
    
    """
    from datetime import datetime
    return datetime.now().isoformat()


def _validate_preferences_structure(preferences: Dict[str, Any]) -> bool:
    """
    Validate the structure of preferences dictionary.
    
    """
    try:
        # Check if theme is valid if present
        if "theme" in preferences:
            return preferences["theme"] in VALID_THEMES
        return True
        
    except Exception:
        return False


# Migration functions for handling preference format changes
def migrate_old_preferences() -> bool:
    """
    Migrate old preference formats to current format.
    
    Handles migration from older versions of the preferences file format.
    
    """
    try:
        preferences = _load_preferences_dict()
        
        if not preferences:
            return True  # No migration needed
        
        # Check if migration is needed
        if "version" not in preferences:
            # Add version and other new fields
            preferences["version"] = "1.0"
            preferences["last_updated"] = _get_timestamp()
            
            # Save migrated preferences
            prefs_path = get_preference_file_path()
            with open(prefs_path, 'w', encoding='utf-8') as f:
                json.dump(preferences, f, indent=2)
            
            logger.info("Preferences migrated to new format")
        
        return True
        
    except Exception as e:
        logger.error(f"Error migrating preferences: {e}")
        return False