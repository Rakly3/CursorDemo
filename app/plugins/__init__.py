"""
Plugin System
============

This module provides a plugin system for the Cursor IDE demo application.
Plugins can be loaded dynamically from the plugins folder to extend
functionality without modifying the core application.

Author: Cursor IDE Demo
Version: 1.0.0
"""

from .plugin_manager import PluginManager, get_plugin_manager
from .base_plugin import BasePlugin

__all__ = ['PluginManager', 'get_plugin_manager', 'BasePlugin'] 