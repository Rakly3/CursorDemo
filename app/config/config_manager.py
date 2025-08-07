"""
Configuration Management System
==============================

This module provides a comprehensive configuration management system for the
Cursor IDE demo application. It handles loading, parsing, and managing
application settings from configuration files and environment variables.

Author: Cursor IDE Demo
Version: 1.0.0
"""

import os
import configparser
import logging
from typing import Dict, Any, Optional, Union
from pathlib import Path


class ConfigManager:
    """
    Advanced configuration management system
    
    This class provides comprehensive configuration management including:
    - Loading from INI files
    - Environment variable overrides
    - Type conversion and validation
    - Default value management
    - Configuration hot-reloading
    """
    
    def __init__(self, config_file: str = "config.ini"):
        """
        Initialize the configuration manager
        
        Args:
            config_file: Path to the configuration file
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self._defaults: Dict[str, Dict[str, Any]] = {}
        self._loaded = False
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.load_config()
    
    def load_config(self) -> bool:
        """
        Load configuration from file
        
        Returns:
            True if configuration loaded successfully, False otherwise
        """
        try:
            # Get the path to the config file
            config_path = Path(__file__).parent / self.config_file
            
            if not config_path.exists():
                self.logger.warning(f"Configuration file not found: {config_path}")
                self._create_default_config(config_path)
            
            # Read the configuration file
            self.config.read(config_path, encoding='utf-8')
            
            # Set up default values
            self._setup_defaults()
            
            # Override with environment variables
            self._apply_environment_overrides()
            
            self._loaded = True
            self.logger.info(f"Configuration loaded successfully from {config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            self._setup_defaults()
            return False
    
    def _create_default_config(self, config_path: Path) -> None:
        """Create a default configuration file"""
        try:
            # Create default configuration
            default_config = configparser.ConfigParser()
            
            # Display settings
            default_config['Display'] = {
                'width': '1280',
                'height': '720',
                'fullscreen': 'false',
                'vsync': 'true',
                'double_buffer': 'true',
                'target_fps': '60'
            }
            
            # Graphics settings
            default_config['Graphics'] = {
                'texture_quality': 'high',
                'particle_count': '1000',
                'bloom_effect': 'true',
                'motion_blur': 'false',
                'anti_aliasing': 'true'
            }
            
            # Audio settings
            default_config['Audio'] = {
                'enabled': 'true',
                'volume': '0.7',
                'sample_rate': '44100',
                'channels': '2',
                'buffer_size': '1024'
            }
            
            # Performance settings
            default_config['Performance'] = {
                'multithreading': 'true',
                'hardware_acceleration': 'true',
                'debug_mode': 'false',
                'profiling': 'false'
            }
            
            # Demo settings
            default_config['Demo'] = {
                'auto_start': 'true',
                'demo_duration': '30',
                'show_fps': 'true',
                'show_platform_info': 'true',
                'interactive_mode': 'true'
            }
            
            # Input settings
            default_config['Input'] = {
                'mouse_sensitivity': '1.0',
                'keyboard_repeat_delay': '500',
                'keyboard_repeat_interval': '50'
            }
            
            # Logging settings
            default_config['Logging'] = {
                'level': 'INFO',
                'file_output': 'true',
                'console_output': 'true',
                'log_file': 'demo.log'
            }
            
            # Write the default configuration
            with open(config_path, 'w', encoding='utf-8') as f:
                default_config.write(f)
            
            self.logger.info(f"Created default configuration file: {config_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to create default configuration: {e}")
    
    def _setup_defaults(self) -> None:
        """Set up default configuration values"""
        self._defaults = {
            'Display': {
                'width': 1280,
                'height': 720,
                'fullscreen': False,
                'vsync': True,
                'double_buffer': True,
                'target_fps': 60
            },
            'Graphics': {
                'texture_quality': 'high',
                'particle_count': 1000,
                'bloom_effect': True,
                'motion_blur': False,
                'anti_aliasing': True
            },
            'Audio': {
                'enabled': True,
                'volume': 0.7,
                'sample_rate': 44100,
                'channels': 2,
                'buffer_size': 1024
            },
            'Performance': {
                'multithreading': True,
                'hardware_acceleration': True,
                'debug_mode': False,
                'profiling': False
            },
            'Demo': {
                'auto_start': True,
                'demo_duration': 30,
                'show_fps': True,
                'show_platform_info': True,
                'interactive_mode': True
            },
            'Input': {
                'mouse_sensitivity': 1.0,
                'keyboard_repeat_delay': 500,
                'keyboard_repeat_interval': 50
            },
            'Logging': {
                'level': 'INFO',
                'file_output': True,
                'console_output': True,
                'log_file': 'demo.log'
            }
        }
    
    def _apply_environment_overrides(self) -> None:
        """Apply environment variable overrides to configuration"""
        # Common environment variable patterns
        env_mappings = {
            'CURSOR_DEMO_WIDTH': ('Display', 'width'),
            'CURSOR_DEMO_HEIGHT': ('Display', 'height'),
            'CURSOR_DEMO_FULLSCREEN': ('Display', 'fullscreen'),
            'CURSOR_DEMO_VSYNC': ('Display', 'vsync'),
            'CURSOR_DEMO_TARGET_FPS': ('Display', 'target_fps'),
            'CURSOR_DEMO_PARTICLE_COUNT': ('Graphics', 'particle_count'),
            'CURSOR_DEMO_VOLUME': ('Audio', 'volume'),
            'CURSOR_DEMO_DEBUG': ('Performance', 'debug_mode'),
            'CURSOR_DEMO_DURATION': ('Demo', 'demo_duration'),
            'CURSOR_DEMO_LOG_LEVEL': ('Logging', 'level')
        }
        
        for env_var, (section, key) in env_mappings.items():
            if env_var in os.environ:
                value = os.environ[env_var]
                # Convert value to appropriate type
                converted_value = self._convert_value(value, self._defaults[section][key])
                self.set(section, key, converted_value)
                self.logger.debug(f"Applied environment override: {env_var}={value}")
    
    def _convert_value(self, value: str, target_type: Any) -> Any:
        """Convert string value to appropriate type"""
        if isinstance(target_type, bool):
            return value.lower() in ('true', '1', 'yes', 'on')
        elif isinstance(target_type, int):
            return int(value)
        elif isinstance(target_type, float):
            return float(value)
        else:
            return value
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found
            
        Returns:
            Configuration value
        """
        try:
            if not self._loaded:
                self.load_config()
            
            # Try to get from config file
            if self.config.has_section(section) and self.config.has_option(section, key):
                value = self.config.get(section, key)
                # Convert to appropriate type based on defaults
                if section in self._defaults and key in self._defaults[section]:
                    return self._convert_value(value, self._defaults[section][key])
                return value
            
            # Return default value
            if default is not None:
                return default
            
            # Return from defaults
            if section in self._defaults and key in self._defaults[section]:
                return self._defaults[section][key]
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting config value {section}.{key}: {e}")
            return default
    
    def set(self, section: str, key: str, value: Any) -> bool:
        """
        Set a configuration value
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.config.has_section(section):
                self.config.add_section(section)
            
            self.config.set(section, key, str(value))
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting config value {section}.{key}: {e}")
            return False
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get all values from a section
        
        Args:
            section: Configuration section
            
        Returns:
            Dictionary of section values
        """
        result = {}
        if self.config.has_section(section):
            for key in self.config.options(section):
                result[key] = self.get(section, key)
        return result
    
    def save_config(self) -> bool:
        """
        Save configuration to file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            config_path = Path(__file__).parent / self.config_file
            with open(config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
            
            self.logger.info(f"Configuration saved to {config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            return False
    
    def reload_config(self) -> bool:
        """
        Reload configuration from file
        
        Returns:
            True if successful, False otherwise
        """
        self._loaded = False
        return self.load_config()
    
    def get_all_config(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all configuration values
        
        Returns:
            Dictionary of all configuration sections and values
        """
        result = {}
        for section in self.config.sections():
            result[section] = self.get_section(section)
        return result


# Global configuration manager instance
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """Get the global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def get_config(section: str, key: str, default: Any = None) -> Any:
    """Get a configuration value"""
    return get_config_manager().get(section, key, default)


def set_config(section: str, key: str, value: Any) -> bool:
    """Set a configuration value"""
    return get_config_manager().set(section, key, value)


def get_config_section(section: str) -> Dict[str, Any]:
    """Get all values from a configuration section"""
    return get_config_manager().get_section(section)


if __name__ == "__main__":
    # Test the configuration manager
    print("🧪 Testing Configuration Manager...")
    config = ConfigManager()
    
    print("\n" + "="*50)
    print("CONFIGURATION VALUES:")
    print("="*50)
    
    for section in ['Display', 'Graphics', 'Audio', 'Performance', 'Demo']:
        print(f"\n[{section}]")
        section_data = config.get_section(section)
        for key, value in section_data.items():
            print(f"  {key} = {value}")
    
    print("="*50) 