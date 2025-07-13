# features/smart_background/__init__.py

"""
Smart Background Module

Provides dynamic animated backgrounds that change based on weather conditions.
No external GIF files required - all animations are generated programmatically.
"""

from .manager import DynamicBackgroundManager
from .integration import SmartBackgroundIntegration

__all__ = ['DynamicBackgroundManager', 'SmartBackgroundIntegration']

__version__ = '1.0.0'
__author__ = 'Weather App Team'