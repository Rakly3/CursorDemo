"""
Plugin Manager
=============

This module provides the plugin management system for the Cursor IDE demo
application. It handles loading plugins from the plugins folder, managing
their lifecycle, and coordinating events between plugins and the application.

Author: Cursor IDE Demo
Version: 1.0.0
"""

import os
import sys
import importlib
import importlib.util
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Type
from .base_plugin import BasePlugin, PluginInfo


class PluginManager:
    """
    Plugin management system
    
    This class handles loading, managing, and coordinating plugins.
    It provides a centralized way to interact with all loaded plugins.
    """
    
    def __init__(self, plugins_dir: str = "plugins"):
        """
        Initialize the plugin manager
        
        Args:
            plugins_dir: Directory containing plugins
        """
        self.plugins_dir = Path(plugins_dir)
        self.plugins: Dict[str, BasePlugin] = {}
        self.logger = logging.getLogger("PluginManager")
        # Ensure the logger has a handler
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        self.app_context: Dict[str, Any] = {}
        
        # Create plugins directory if it doesn't exist
        if not self.plugins_dir.exists():
            self.plugins_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created plugins directory: {self.plugins_dir}")
    
    def load_plugins(self, app_context: Dict[str, Any]) -> bool:
        """
        Load all plugins from the plugins directory
        
        Args:
            app_context: Application context to pass to plugins
            
        Returns:
            True if plugins loaded successfully, False otherwise
        """
        self.app_context = app_context
        self.logger.info(f"Loading plugins from: {self.plugins_dir}")
        
        try:
            # Get all Python files in the plugins directory
            plugin_files = list(self.plugins_dir.glob("*.py"))
            
            self.logger.info(f"Found {len(plugin_files)} Python files in plugins directory")
            for file in plugin_files:
                self.logger.info(f"  - {file.name}")
            
            if not plugin_files:
                self.logger.info("No plugin files found")
                return True
            
            # Load each plugin
            for plugin_file in plugin_files:
                if plugin_file.name.startswith("__"):
                    continue  # Skip __init__.py and other special files
                
                # Skip base plugin and plugin manager files
                if plugin_file.name in ["base_plugin.py", "plugin_manager.py", "__init__.py"]:
                    continue
                
                self.logger.info(f"Loading plugin from: {plugin_file.name}")
                self._load_plugin(plugin_file)
            
            self.logger.info(f"Loaded {len(self.plugins)} plugins")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading plugins: {e}")
            return False
    
    def _load_plugin(self, plugin_file: Path) -> bool:
        """
        Load a single plugin from file
        
        Args:
            plugin_file: Path to the plugin file
            
        Returns:
            True if plugin loaded successfully, False otherwise
        """
        try:
            # Load the module
            spec = importlib.util.spec_from_file_location(
                f"plugins.{plugin_file.stem}", 
                plugin_file
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find plugin classes (classes that inherit from BasePlugin)
            plugin_classes = []
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, BasePlugin) and 
                    attr != BasePlugin):
                    plugin_classes.append(attr)
            
            if not plugin_classes:
                self.logger.warning(f"No plugin classes found in {plugin_file}")
                return False
            
            # Create plugin instances
            for plugin_class in plugin_classes:
                try:
                    plugin = plugin_class()
                    plugin_name = plugin.info.name
                    
                    if plugin_name in self.plugins:
                        self.logger.warning(f"Plugin '{plugin_name}' already loaded, skipping")
                        continue
                    
                    # Load the plugin
                    if plugin.on_load(self.app_context):
                        self.plugins[plugin_name] = plugin
                        self.logger.info(f"Plugin '{plugin_name}' loaded successfully")
                    else:
                        self.logger.error(f"Failed to load plugin '{plugin_name}'")
                        
                except Exception as e:
                    self.logger.error(f"Error creating plugin instance from {plugin_file}: {e}")
                    continue
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading plugin from {plugin_file}: {e}")
            return False
    
    def unload_plugins(self) -> bool:
        """
        Unload all plugins
        
        Returns:
            True if plugins unloaded successfully, False otherwise
        """
        self.logger.info("Unloading plugins...")
        
        try:
            for plugin_name, plugin in list(self.plugins.items()):
                try:
                    if plugin.on_unload():
                        self.logger.info(f"Plugin '{plugin_name}' unloaded")
                    else:
                        self.logger.warning(f"Failed to unload plugin '{plugin_name}'")
                except Exception as e:
                    self.logger.error(f"Error unloading plugin '{plugin_name}': {e}")
                finally:
                    del self.plugins[plugin_name]
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error unloading plugins: {e}")
            return False
    
    def handle_mouse_click(self, button: int, pos: tuple) -> bool:
        """
        Handle mouse click events
        
        Args:
            button: Mouse button (1=left, 2=middle, 3=right)
            pos: Mouse position (x, y)
            
        Returns:
            True if any plugin handled the event, False otherwise
        """
        handled = False
        
        for plugin_name, plugin in self.plugins.items():
            try:
                if plugin.on_mouse_click(button, pos, self.app_context):
                    handled = True
                    self.logger.debug(f"Plugin '{plugin_name}' handled mouse click")
            except Exception as e:
                self.logger.error(f"Error in plugin '{plugin_name}' mouse click handler: {e}")
        
        return handled
    
    def handle_key_press(self, key: int) -> bool:
        """
        Handle key press events
        
        Args:
            key: Key code
            
        Returns:
            True if any plugin handled the event, False otherwise
        """
        handled = False
        
        for plugin_name, plugin in self.plugins.items():
            try:
                if plugin.on_key_press(key, self.app_context):
                    handled = True
                    self.logger.debug(f"Plugin '{plugin_name}' handled key press")
            except Exception as e:
                self.logger.error(f"Error in plugin '{plugin_name}' key press handler: {e}")
        
        return handled
    
    def update_plugins(self, dt: float) -> None:
        """
        Update all plugins
        
        Args:
            dt: Delta time
        """
        for plugin_name, plugin in self.plugins.items():
            try:
                plugin.on_update(dt, self.app_context)
            except Exception as e:
                self.logger.error(f"Error updating plugin '{plugin_name}': {e}")
    
    def render_plugins(self, surface) -> None:
        """
        Render all plugins
        
        Args:
            surface: Pygame surface to render on
        """
        for plugin_name, plugin in self.plugins.items():
            try:
                plugin.on_render(surface, self.app_context)
            except Exception as e:
                self.logger.error(f"Error rendering plugin '{plugin_name}': {e}")
    
    def handle_event(self, event_name: str, event_data: Dict[str, Any]) -> bool:
        """
        Handle application events
        
        Args:
            event_name: Name of the event
            event_data: Event data
            
        Returns:
            True if any plugin handled the event, False otherwise
        """
        handled = False
        
        for plugin_name, plugin in self.plugins.items():
            try:
                if plugin.on_event(event_name, event_data):
                    handled = True
                    self.logger.debug(f"Plugin '{plugin_name}' handled event '{event_name}'")
            except Exception as e:
                self.logger.error(f"Error in plugin '{plugin_name}' event handler: {e}")
        
        return handled
    
    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """
        Get a plugin by name
        
        Args:
            name: Plugin name
            
        Returns:
            Plugin instance or None if not found
        """
        return self.plugins.get(name)
    
    def get_plugin_list(self) -> List[PluginInfo]:
        """
        Get list of all loaded plugins
        
        Returns:
            List of plugin information
        """
        return [plugin.info for plugin in self.plugins.values()]
    
    def enable_plugin(self, name: str) -> bool:
        """
        Enable a plugin
        
        Args:
            name: Plugin name
            
        Returns:
            True if plugin enabled successfully, False otherwise
        """
        plugin = self.plugins.get(name)
        if plugin:
            return plugin.on_enable()
        return False
    
    def disable_plugin(self, name: str) -> bool:
        """
        Disable a plugin
        
        Args:
            name: Plugin name
            
        Returns:
            True if plugin disabled successfully, False otherwise
        """
        plugin = self.plugins.get(name)
        if plugin:
            return plugin.on_disable()
        return False
    
    def reload_plugins(self) -> bool:
        """
        Reload all plugins
        
        Returns:
            True if plugins reloaded successfully, False otherwise
        """
        self.logger.info("Reloading plugins...")
        
        # Unload current plugins
        if not self.unload_plugins():
            return False
        
        # Load plugins again
        return self.load_plugins(self.app_context)


# Global plugin manager instance
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager(plugins_dir: str = "plugins") -> PluginManager:
    """Get the global plugin manager instance"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager(plugins_dir)
    return _plugin_manager


if __name__ == "__main__":
    # Test the plugin manager
    print("🧪 Testing Plugin Manager...")
    
    manager = PluginManager()
    app_context = {"test": "data"}
    
    print(f"Plugins directory: {manager.plugins_dir}")
    print(f"Loaded plugins: {len(manager.plugins)}")
    
    for plugin_info in manager.get_plugin_list():
        print(f"  - {plugin_info.name} v{plugin_info.version} by {plugin_info.author}")
        print(f"    {plugin_info.description}")
        print(f"    Events: {', '.join(plugin_info.events)}") 