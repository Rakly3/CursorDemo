"""
Base Plugin Class
================

This module provides the base class for all plugins in the Cursor IDE demo
application. All plugins must inherit from this class and implement
the required methods.

Author: Cursor IDE Demo
Version: 1.0.0
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass


@dataclass
class PluginInfo:
    """Plugin information and metadata"""
    name: str
    version: str
    author: str
    description: str
    events: List[str]  # List of events this plugin handles


class BasePlugin(ABC):
    """
    Base class for all plugins
    
    This class provides the interface that all plugins must implement.
    Plugins can handle various events and extend application functionality.
    """
    
    def __init__(self):
        """Initialize the plugin"""
        self.logger = logging.getLogger(f"Plugin.{self.__class__.__name__}")
        self.enabled = True
        self.info = self.get_plugin_info()
        self.logger.info(f"Plugin '{self.info.name}' v{self.info.version} initialized")
    
    @abstractmethod
    def get_plugin_info(self) -> PluginInfo:
        """
        Get plugin information
        
        Returns:
            PluginInfo object with plugin metadata
        """
        pass
    
    def on_load(self, app_context: Dict[str, Any]) -> bool:
        """
        Called when the plugin is loaded
        
        Args:
            app_context: Application context with shared objects
            
        Returns:
            True if plugin loaded successfully, False otherwise
        """
        self.logger.info(f"Plugin '{self.info.name}' loaded")
        return True
    
    def on_unload(self) -> bool:
        """
        Called when the plugin is unloaded
        
        Returns:
            True if plugin unloaded successfully, False otherwise
        """
        self.logger.info(f"Plugin '{self.info.name}' unloaded")
        return True
    
    def on_enable(self) -> bool:
        """
        Called when the plugin is enabled
        
        Returns:
            True if plugin enabled successfully, False otherwise
        """
        self.enabled = True
        self.logger.info(f"Plugin '{self.info.name}' enabled")
        return True
    
    def on_disable(self) -> bool:
        """
        Called when the plugin is disabled
        
        Returns:
            True if plugin disabled successfully, False otherwise
        """
        self.enabled = False
        self.logger.info(f"Plugin '{self.info.name}' disabled")
        return True
    
    def on_event(self, event_name: str, event_data: Dict[str, Any]) -> bool:
        """
        Handle application events
        
        Args:
            event_name: Name of the event
            event_data: Event data
            
        Returns:
            True if event was handled, False otherwise
        """
        if not self.enabled:
            return False
        
        # Default implementation - plugins should override this
        return False
    
    def on_mouse_click(self, button: int, pos: Tuple[int, int], app_context: Dict[str, Any]) -> bool:
        """
        Handle mouse click events
        
        Args:
            button: Mouse button (1=left, 2=middle, 3=right)
            pos: Mouse position (x, y)
            app_context: Application context
            
        Returns:
            True if event was handled, False otherwise
        """
        if not self.enabled:
            return False
        
        # Default implementation - plugins should override this
        return False
    
    def on_key_press(self, key: int, app_context: Dict[str, Any]) -> bool:
        """
        Handle key press events
        
        Args:
            key: Key code
            app_context: Application context
            
        Returns:
            True if event was handled, False otherwise
        """
        if not self.enabled:
            return False
        
        # Default implementation - plugins should override this
        return False
    
    def on_update(self, dt: float, app_context: Dict[str, Any]) -> bool:
        """
        Called every frame for plugin updates
        
        Args:
            dt: Delta time
            app_context: Application context
            
        Returns:
            True if update was handled, False otherwise
        """
        if not self.enabled:
            return False
        
        # Default implementation - plugins should override this
        return False
    
    def on_render(self, surface, app_context: Dict[str, Any]) -> bool:
        """
        Called every frame for plugin rendering
        
        Args:
            surface: Pygame surface to render on
            app_context: Application context
            
        Returns:
            True if rendering was handled, False otherwise
        """
        if not self.enabled:
            return False
        
        # Default implementation - plugins should override this
        return False
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get plugin configuration
        
        Returns:
            Plugin configuration dictionary
        """
        return {}
    
    def set_config(self, config: Dict[str, Any]) -> bool:
        """
        Set plugin configuration
        
        Args:
            config: Plugin configuration dictionary
            
        Returns:
            True if configuration was set successfully, False otherwise
        """
        return True 