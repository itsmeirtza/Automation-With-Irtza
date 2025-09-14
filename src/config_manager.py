"""
Configuration management module.

This module handles loading and managing configuration settings
for the automation framework.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Configuration manager class."""
    
    def __init__(self, config_path: str = "config/default.json"):
        """Initialize the configuration manager."""
        self.config_path = Path(config_path)
        self.logger = logging.getLogger(__name__)
        self.config = {}
        self._loaded = False
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                self.logger.info(f"Configuration loaded from {self.config_path}")
            else:
                # Use default configuration
                self.config = self._get_default_config()
                self.logger.info("Using default configuration")
            
            self._loaded = True
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {str(e)}")
            self.config = self._get_default_config()
            self._loaded = False
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "app_name": "Automation Framework",
            "version": "1.0.0",
            "log_level": "INFO",
            "default_workflow": ["hello_world", "system_check"],
            "task_settings": {
                "hello_world": {
                    "enabled": True
                },
                "system_check": {
                    "enabled": True,
                    "check_disk_space": True,
                    "check_memory": True
                },
                "cleanup": {
                    "enabled": True,
                    "cleanup_logs": True,
                    "cleanup_temp_files": True
                }
            },
            "automation_settings": {
                "max_retries": 3,
                "retry_delay": 5,
                "timeout": 300
            }
        }
    
    def get_config(self) -> Dict[str, Any]:
        """Return the current configuration."""
        return self.config.copy()
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a specific setting from configuration."""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def update_setting(self, key: str, value: Any) -> None:
        """Update a specific setting in configuration."""
        keys = key.split('.')
        config_ref = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]
        
        # Set the final key
        config_ref[keys[-1]] = value
        self.logger.info(f"Updated setting '{key}' = {value}")
    
    def save_config(self, path: Optional[str] = None) -> None:
        """Save current configuration to file."""
        save_path = Path(path) if path else self.config_path
        
        try:
            # Ensure directory exists
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            
            self.logger.info(f"Configuration saved to {save_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {str(e)}")
    
    def is_loaded(self) -> bool:
        """Check if configuration was loaded successfully."""
        return self._loaded
    
    def reload_config(self) -> None:
        """Reload configuration from file."""
        self.load_config()
    
    def get_task_setting(self, task_name: str, setting_key: str, default: Any = None) -> Any:
        """Get a setting for a specific task."""
        return self.get_setting(f"task_settings.{task_name}.{setting_key}", default)