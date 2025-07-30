"""
Language Utilities - Advanced Translation Functions
=================================================

Contains utility functions for advanced language operations,
analytics, import/export, and specialized translation features.
"""

import json
from .translations import TRANSLATIONS, SUPPORTED_LANGUAGES


class LanguageUtils:
    """
    Utility class for advanced language operations.
    """
    
    def __init__(self, language_controller):
        """
        Initialize language utilities.
        
        Args:
            language_controller: Main language controller instance
        """
        self.lang_ctrl = language_controller
        self.translations = TRANSLATIONS
        self.supported_languages = SUPPORTED_LANGUAGES

    def get_translation_completeness(self):
        """
        Get translation completeness statistics.
        
        Returns:
            dict: Statistics about translation completeness
        """
        english_keys = set(self.translations.get("English", {}).keys())
        stats = {}
        
        for lang in self.supported_languages.keys():
            lang_keys = set(self.translations.get(lang, {}).keys())
            missing_keys = english_keys - lang_keys
            completeness = (len(lang_keys) / len(english_keys)) * 100 if english_keys else 0
            
            stats[lang] = {
                "total_keys": len(english_keys),
                "translated_keys": len(lang_keys),
                "missing_keys": len(missing_keys),
                "completeness_percent": round(completeness, 2),
                "missing_key_list": list(missing_keys)
            }
        
        return stats

    def export_translations(self, filename=None):
        """
        Export translations to JSON file.
        
        Args:
            filename (str): Output filename
            
        Returns:
            bool: Success status
        """
        if not filename:
            filename = f"translations_export_{self.lang_ctrl.current_language.lower()}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.translations, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def import_translations(self, filename):
        """
        Import translations from JSON file.
        
        Args:
            filename (str): Input filename
            
        Returns:
            bool: Success status
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_translations = json.load(f)
            
            # Validate structure
            if isinstance(imported_translations, dict):
                self.translations.update(imported_translations)
                self.lang_ctrl.translations = self.translations
                return True
            return False
        except Exception:
            return False

    def validate_translations(self):
        """
        Validate translation data for consistency and completeness.
        
        Returns:
            dict: Validation results
        """
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "stats": {}
        }
        
        try:
            english_keys = set(self.translations.get("English", {}).keys())
            
            for lang_name, lang_code in self.supported_languages.items():
                lang_translations = self.translations.get(lang_name, {})
                lang_keys = set(lang_translations.keys())
                
                # Check for missing keys
                missing_keys = english_keys - lang_keys
                if missing_keys:
                    results["warnings"].append(
                        f"{lang_name} missing {len(missing_keys)} translations: {list(missing_keys)[:5]}..."
                    )
                
                # Check for extra keys
                extra_keys = lang_keys - english_keys
                if extra_keys:
                    results["warnings"].append(
                        f"{lang_name} has {len(extra_keys)} extra keys: {list(extra_keys)[:5]}..."
                    )
                
                # Check for empty translations
                empty_translations = [key for key, value in lang_translations.items() if not value or not str(value).strip()]
                if empty_translations:
                    results["errors"].append(
                        f"{lang_name} has empty translations for: {empty_translations[:5]}..."
                    )
                    results["valid"] = False
                
                results["stats"][lang_name] = {
                    "total_keys": len(lang_keys),
                    "missing_keys": len(missing_keys),
                    "extra_keys": len(extra_keys),
                    "empty_translations": len(empty_translations)
                }
        
        except Exception as e:
            results["valid"] = False
            results["errors"].append(f"Validation error: {str(e)}")
        
        return results

    def find_similar_keys(self, search_term):
        """
        Find translation keys similar to search term.
        
        Args:
            search_term (str): Term to search for
            
        Returns:
            list: List of similar keys
        """
        search_lower = search_term.lower()
        english_keys = self.translations.get("English", {}).keys()
        
        similar_keys = []
        for key in english_keys:
            if search_lower in key.lower():
                similar_keys.append(key)
        
        return sorted(similar_keys)

    def get_translation_coverage_report(self):
        """
        Generate a detailed translation coverage report.
        
        Returns:
            str: Formatted coverage report
        """
        stats = self.get_translation_completeness()
        
        report_lines = ["Translation Coverage Report", "=" * 30, ""]
        
        for lang, data in stats.items():
            report_lines.append(f"{lang}:")
            report_lines.append(f"  Total Keys: {data['total_keys']}")
            report_lines.append(f"  Translated: {data['translated_keys']}")
            report_lines.append(f"  Missing: {data['missing_keys']}")
            report_lines.append(f"  Coverage: {data['completeness_percent']}%")
            
            if data['missing_key_list']:
                report_lines.append(f"  Missing Keys: {', '.join(data['missing_key_list'][:10])}")
                if len(data['missing_key_list']) > 10:
                    report_lines.append(f"    ... and {len(data['missing_key_list']) - 10} more")
            
            report_lines.append("")
        
        return "\n".join(report_lines)

    def backup_translations(self, backup_filename=None):
        """
        Create a backup of current translations.
        
        Args:
            backup_filename (str): Backup filename
            
        Returns:
            bool: Success status
        """
        if not backup_filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"translations_backup_{timestamp}.json"
        
        return self.export_translations(backup_filename)

    def restore_translations(self, backup_filename):
        """
        Restore translations from backup.
        
        Args:
            backup_filename (str): Backup filename
            
        Returns:
            bool: Success status
        """
        return self.import_translations(backup_filename)

    def merge_translations(self, new_translations):
        """
        Merge new translations with existing ones.
        
        Args:
            new_translations (dict): New translation data
            
        Returns:
            bool: Success status
        """
        try:
            if not isinstance(new_translations, dict):
                return False
            
            for lang, translations in new_translations.items():
                if lang in self.translations:
                    self.translations[lang].update(translations)
                else:
                    self.translations[lang] = translations
            
            self.lang_ctrl.translations = self.translations
            return True
        except Exception:
            return False

    def get_language_statistics(self):
        """
        Get comprehensive language statistics.
        
        Returns:
            dict: Language statistics
        """
        stats = {
            "total_languages": len(self.supported_languages),
            "supported_codes": list(self.supported_languages.values()),
            "current_language": self.lang_ctrl.current_language,
            "total_translation_keys": len(self.translations.get("English", {})),
            "languages": {}
        }
        
        for lang in self.supported_languages.keys():
            lang_data = self.translations.get(lang, {})
            stats["languages"][lang] = {
                "code": self.supported_languages[lang],
                "key_count": len(lang_data),
                "has_rtl_support": False,  # Can be extended for RTL languages
                "font_family": self._get_font_for_language(lang),
                "character_count": sum(len(str(value)) for value in lang_data.values())
            }
        
        return stats

    def _get_font_for_language(self, language):
        """Get appropriate font for a specific language."""
        font_mapping = {
            "Hindi": "Noto Sans Devanagari",
            "Spanish": "Arial",
            "English": "Arial"
        }
        return font_mapping.get(language, "Arial")

    def search_translations(self, search_text, language=None):
        """
        Search for translations containing specific text.
        
        Args:
            search_text (str): Text to search for
            language (str): Specific language to search in (optional)
            
        Returns:
            dict: Search results
        """
        results = {}
        search_lower = search_text.lower()
        
        languages_to_search = [language] if language else self.supported_languages.keys()
        
        for lang in languages_to_search:
            if lang not in self.translations:
                continue
                
            lang_results = []
            for key, value in self.translations[lang].items():
                if search_lower in str(value).lower() or search_lower in key.lower():
                    lang_results.append({
                        "key": key,
                        "value": value,
                        "match_in_key": search_lower in key.lower(),
                        "match_in_value": search_lower in str(value).lower()
                    })
            
            if lang_results:
                results[lang] = lang_results
        
        return results

    def generate_missing_translations_template(self, target_language):
        """
        Generate a template for missing translations in a target language.
        
        Args:
            target_language (str): Target language name
            
        Returns:
            dict: Template with missing translations
        """
        if target_language not in self.supported_languages:
            return {}
        
        english_keys = set(self.translations.get("English", {}).keys())
        target_keys = set(self.translations.get(target_language, {}).keys())
        missing_keys = english_keys - target_keys
        
        template = {}
        for key in missing_keys:
            english_value = self.translations["English"].get(key, "")
            template[key] = f"TODO: Translate '{english_value}'"
        
        return template

    def count_translation_characters(self, language=None):
        """
        Count total characters in translations.
        
        Args:
            language (str): Specific language (optional)
            
        Returns:
            dict: Character counts
        """
        if language:
            if language in self.translations:
                lang_data = self.translations[language]
                return {
                    language: sum(len(str(value)) for value in lang_data.values())
                }
            return {}
        
        counts = {}
        for lang, lang_data in self.translations.items():
            counts[lang] = sum(len(str(value)) for value in lang_data.values())
        
        return counts

    def optimize_translations(self):
        """
        Optimize translations by removing duplicates and cleaning up.
        
        Returns:
            dict: Optimization results
        """
        results = {
            "duplicates_removed": 0,
            "empty_values_cleaned": 0,
            "whitespace_trimmed": 0
        }
        
        for lang in self.translations:
            lang_data = self.translations[lang]
            keys_to_remove = []
            
            for key, value in lang_data.items():
                # Remove empty values
                if not value or not str(value).strip():
                    keys_to_remove.append(key)
                    results["empty_values_cleaned"] += 1
                else:
                    # Trim whitespace
                    trimmed_value = str(value).strip()
                    if trimmed_value != str(value):
                        lang_data[key] = trimmed_value
                        results["whitespace_trimmed"] += 1
            
            # Remove empty keys
            for key in keys_to_remove:
                del lang_data[key]
        
        return results

    def create_translation_diff(self, old_translations, new_translations):
        """
        Create a diff between old and new translations.
        
        Args:
            old_translations (dict): Old translation data
            new_translations (dict): New translation data
            
        Returns:
            dict: Diff results
        """
        diff = {
            "added": {},
            "removed": {},
            "modified": {},
            "unchanged": {}
        }
        
        for lang in set(list(old_translations.keys()) + list(new_translations.keys())):
            old_lang = old_translations.get(lang, {})
            new_lang = new_translations.get(lang, {})
            
            all_keys = set(list(old_lang.keys()) + list(new_lang.keys()))
            
            lang_diff = {
                "added": [],
                "removed": [],
                "modified": [],
                "unchanged": []
            }
            
            for key in all_keys:
                old_value = old_lang.get(key)
                new_value = new_lang.get(key)
                
                if old_value is None and new_value is not None:
                    lang_diff["added"].append({key: new_value})
                elif old_value is not None and new_value is None:
                    lang_diff["removed"].append({key: old_value})
                elif old_value != new_value:
                    lang_diff["modified"].append({
                        key: {"old": old_value, "new": new_value}
                    })
                else:
                    lang_diff["unchanged"].append({key: old_value})
            
            diff[lang] = lang_diff
        
        return diff