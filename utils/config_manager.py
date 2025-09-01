"""
JR AI Control - Configuration Management System
Handles loading, saving, validation, and migration of application settings.
"""

import json
import os
import shutil
from datetime import datetime
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigurationManager:
    """Comprehensive configuration management system for JR AI Control"""
    
    # Configuration file paths
    CONFIG_FILE = 'config.json'
    BACKUP_DIR = 'config_backups'
    DEFAULT_CONFIG_FILE = 'config_default.json'
    
    # Current configuration version for migration
    CONFIG_VERSION = "1.0.0"
    
    # Default configuration template
    DEFAULT_CONFIG = {
        "version": CONFIG_VERSION,
        "api_key": "",
        "model": "gemini-2.0-flash-exp",
        
        # UI Settings
        "theme_mode": "dark",
        "font_size": 14,
        "window_opacity": 1.0,
        
        # Voice Settings
        "speech_enabled": True,
        "speech_muted": False,
        "voice_rate": 200,
        "voice_volume": 0.8,
        "voice_language": "en-US",
        
        # Screenshot Settings
        "screenshot_size": "medium",
        "screenshot_wait_duration": 3,
        
        # Notification Settings
        "notification_enabled": True,
        
        # Token Tracking
        "total_tokens_used": 0,
        
        # Advanced Settings
        "auto_save": True,
        "backup_enabled": True,
        "max_backups": 5,
        
        # Metadata
        "created_at": None,
        "last_modified": None
    }
    
    def __init__(self):
        """Initialize configuration manager"""
        self.config = {}
        self.config_loaded = False
        self.observers = []  # For real-time updates
        
        # Ensure backup directory exists
        if not os.path.exists(self.BACKUP_DIR):
            os.makedirs(self.BACKUP_DIR)
    
    def load_settings(self) -> Dict[str, Any]:
        """
        Load settings from config file with validation and migration
        Returns the loaded configuration dictionary
        """
        try:
            # Check if config file exists
            if not os.path.exists(self.CONFIG_FILE):
                logger.info("Config file not found, creating default configuration")
                self.create_default_config()
                return self.config.copy()
            
            # Load existing config
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
            
            # Validate and migrate if necessary
            self.config = self.validate_and_migrate_config(loaded_config)
            
            # Update last modified timestamp
            self.config['last_modified'] = datetime.now().isoformat()
            
            self.config_loaded = True
            logger.info("Configuration loaded successfully")
            
            # Notify observers of config load
            self._notify_observers('config_loaded', self.config)
            
            return self.config.copy()
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return self._handle_corrupted_config()
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            return self._handle_corrupted_config()
    
    def save_settings(self, config_updates: Optional[Dict[str, Any]] = None) -> bool:
        """
        Save settings to config file with backup and validation
        
        Args:
            config_updates: Optional dictionary of settings to update
            
        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            # Update config with new values if provided
            if config_updates:
                self.config.update(config_updates)
            
            # Validate configuration before saving
            if not self.validate_config(self.config):
                logger.error("Configuration validation failed, not saving")
                return False
            
            # Create backup if enabled
            if self.config.get('backup_enabled', True):
                self._create_backup()
            
            # Update metadata
            self.config['last_modified'] = datetime.now().isoformat()
            if not self.config.get('created_at'):
                self.config['created_at'] = datetime.now().isoformat()
            
            # Save to file
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            logger.info("Configuration saved successfully")
            
            # Notify observers of config save
            self._notify_observers('config_saved', self.config)
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate configuration values
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Check required fields
            required_fields = ['api_key', 'model', 'theme_mode']
            for field in required_fields:
                if field not in config:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Validate specific field values
            validations = {
                'theme_mode': lambda x: x in ['dark', 'light'],
                'screenshot_size': lambda x: x in ['small', 'medium', 'large'],
                'screenshot_wait_duration': lambda x: isinstance(x, int) and 1 <= x <= 10,
                'font_size': lambda x: isinstance(x, int) and 8 <= x <= 32,
                'window_opacity': lambda x: isinstance(x, (int, float)) and 0.1 <= x <= 1.0,
                'voice_rate': lambda x: isinstance(x, int) and 50 <= x <= 400,
                'voice_volume': lambda x: isinstance(x, (int, float)) and 0.0 <= x <= 1.0,
                'total_tokens_used': lambda x: isinstance(x, int) and x >= 0,
                'max_backups': lambda x: isinstance(x, int) and 1 <= x <= 20
            }
            
            for field, validator in validations.items():
                if field in config and not validator(config[field]):
                    logger.error(f"Invalid value for {field}: {config[field]}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating config: {e}")
            return False
    
    def validate_and_migrate_config(self, loaded_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and migrate configuration to current version
        
        Args:
            loaded_config: Configuration loaded from file
            
        Returns:
            Dict[str, Any]: Migrated and validated configuration
        """
        # Start with default config
        migrated_config = self.DEFAULT_CONFIG.copy()
        
        # Get version from loaded config
        loaded_version = loaded_config.get('version', '0.0.0')
        
        # Migrate based on version
        if loaded_version != self.CONFIG_VERSION:
            logger.info(f"Migrating config from version {loaded_version} to {self.CONFIG_VERSION}")
            migrated_config = self._migrate_config(loaded_config, loaded_version)
        else:
            # Update with loaded values, keeping defaults for missing keys
            for key, value in loaded_config.items():
                if key in migrated_config:
                    migrated_config[key] = value
        
        # Ensure version is current
        migrated_config['version'] = self.CONFIG_VERSION
        
        return migrated_config
    
    def _migrate_config(self, old_config: Dict[str, Any], old_version: str) -> Dict[str, Any]:
        """
        Migrate configuration from older versions
        
        Args:
            old_config: Old configuration dictionary
            old_version: Version of the old configuration
            
        Returns:
            Dict[str, Any]: Migrated configuration
        """
        migrated = self.DEFAULT_CONFIG.copy()
        
        # Migration logic for different versions
        if old_version == '0.0.0' or 'version' not in old_config:
            # Migrate from pre-versioned config
            logger.info("Migrating from pre-versioned configuration")
            
            # Map old keys to new keys if needed
            key_mappings = {
                # Add any key mappings for renamed settings
            }
            
            for old_key, new_key in key_mappings.items():
                if old_key in old_config:
                    migrated[new_key] = old_config[old_key]
            
            # Copy compatible settings
            for key, value in old_config.items():
                if key in migrated and key not in key_mappings:
                    migrated[key] = value
        
        # Add more migration logic for future versions here
        
        return migrated
    
    def create_default_config(self) -> bool:
        """
        Create default configuration file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.config = self.DEFAULT_CONFIG.copy()
            self.config['created_at'] = datetime.now().isoformat()
            self.config['last_modified'] = datetime.now().isoformat()
            
            # Save default config
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            # Also create a default template file
            with open(self.DEFAULT_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
            
            logger.info("Default configuration created")
            return True
            
        except Exception as e:
            logger.error(f"Error creating default config: {e}")
            return False
    
    def _create_backup(self) -> bool:
        """
        Create backup of current configuration
        
        Returns:
            bool: True if backup was successful, False otherwise
        """
        try:
            if not os.path.exists(self.CONFIG_FILE):
                return True  # No file to backup
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"config_backup_{timestamp}.json"
            backup_path = os.path.join(self.BACKUP_DIR, backup_filename)
            
            shutil.copy2(self.CONFIG_FILE, backup_path)
            
            # Clean up old backups
            self._cleanup_old_backups()
            
            logger.info(f"Configuration backup created: {backup_filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return False
    
    def _cleanup_old_backups(self):
        """Clean up old backup files based on max_backups setting"""
        try:
            max_backups = self.config.get('max_backups', 5)
            
            # Get all backup files
            backup_files = []
            for filename in os.listdir(self.BACKUP_DIR):
                if filename.startswith('config_backup_') and filename.endswith('.json'):
                    filepath = os.path.join(self.BACKUP_DIR, filename)
                    backup_files.append((filepath, os.path.getctime(filepath)))
            
            # Sort by creation time (newest first)
            backup_files.sort(key=lambda x: x[1], reverse=True)
            
            # Remove old backups
            for filepath, _ in backup_files[max_backups:]:
                os.remove(filepath)
                logger.info(f"Removed old backup: {os.path.basename(filepath)}")
                
        except Exception as e:
            logger.error(f"Error cleaning up backups: {e}")
    
    def _handle_corrupted_config(self) -> Dict[str, Any]:
        """
        Handle corrupted configuration file
        
        Returns:
            Dict[str, Any]: Default configuration
        """
        try:
            # Try to restore from backup
            if self._restore_from_backup():
                return self.config.copy()
            
            # If no backup available, create new default config
            logger.warning("Creating new default configuration due to corruption")
            self.create_default_config()
            return self.config.copy()
            
        except Exception as e:
            logger.error(f"Error handling corrupted config: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def _restore_from_backup(self) -> bool:
        """
        Restore configuration from most recent backup
        
        Returns:
            bool: True if restore was successful, False otherwise
        """
        try:
            # Find most recent backup
            backup_files = []
            for filename in os.listdir(self.BACKUP_DIR):
                if filename.startswith('config_backup_') and filename.endswith('.json'):
                    filepath = os.path.join(self.BACKUP_DIR, filename)
                    backup_files.append((filepath, os.path.getctime(filepath)))
            
            if not backup_files:
                return False
            
            # Get most recent backup
            most_recent_backup = max(backup_files, key=lambda x: x[1])[0]
            
            # Restore from backup
            shutil.copy2(most_recent_backup, self.CONFIG_FILE)
            
            # Load restored config
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            logger.info(f"Configuration restored from backup: {os.path.basename(most_recent_backup)}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring from backup: {e}")
            return False
    
    def export_config(self, export_path: str) -> bool:
        """
        Export configuration to specified path
        
        Args:
            export_path: Path to export configuration to
            
        Returns:
            bool: True if export was successful, False otherwise
        """
        try:
            # Create export data (exclude sensitive information)
            export_data = self.config.copy()
            export_data.pop('api_key', None)  # Don't export API key
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Configuration exported to: {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting config: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """
        Import configuration from specified path
        
        Args:
            import_path: Path to import configuration from
            
        Returns:
            bool: True if import was successful, False otherwise
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Merge with current config (preserve API key and add missing required fields)
            current_api_key = self.config.get('api_key', '')
            
            # Start with current config to ensure all required fields are present
            merged_config = self.config.copy()
            merged_config.update(imported_config)
            
            # Preserve API key if not in imported config
            if current_api_key and not imported_config.get('api_key'):
                merged_config['api_key'] = current_api_key
            
            # Validate merged config
            if not self.validate_config(merged_config):
                logger.error("Merged configuration is invalid")
                return False
            
            # Update current config
            self.config = merged_config
            
            # Save updated config
            return self.save_settings()
            
        except Exception as e:
            logger.error(f"Error importing config: {e}")
            return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Get a specific setting value
        
        Args:
            key: Setting key
            default: Default value if key not found
            
        Returns:
            Any: Setting value or default
        """
        return self.config.get(key, default)
    
    def set_setting(self, key: str, value: Any, save_immediately: bool = True) -> bool:
        """
        Set a specific setting value
        
        Args:
            key: Setting key
            value: Setting value
            save_immediately: Whether to save to file immediately
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.config[key] = value
            
            # Notify observers of setting change
            self._notify_observers('setting_changed', {'key': key, 'value': value})
            
            if save_immediately and self.config.get('auto_save', True):
                return self.save_settings()
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting {key}: {e}")
            return False
    
    def add_observer(self, observer_func):
        """
        Add observer for configuration changes
        
        Args:
            observer_func: Function to call when config changes
        """
        if observer_func not in self.observers:
            self.observers.append(observer_func)
    
    def remove_observer(self, observer_func):
        """
        Remove observer for configuration changes
        
        Args:
            observer_func: Function to remove from observers
        """
        if observer_func in self.observers:
            self.observers.remove(observer_func)
    
    def _notify_observers(self, event_type: str, data: Any):
        """
        Notify all observers of configuration changes
        
        Args:
            event_type: Type of event ('config_loaded', 'config_saved', 'setting_changed')
            data: Event data
        """
        for observer in self.observers:
            try:
                observer(event_type, data)
            except Exception as e:
                logger.error(f"Error notifying observer: {e}")
    
    def reset_to_defaults(self) -> bool:
        """
        Reset configuration to default values
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Preserve API key
            current_api_key = self.config.get('api_key', '')
            
            # Reset to defaults
            self.config = self.DEFAULT_CONFIG.copy()
            self.config['api_key'] = current_api_key
            self.config['created_at'] = datetime.now().isoformat()
            self.config['last_modified'] = datetime.now().isoformat()
            
            # Save reset config
            return self.save_settings()
            
        except Exception as e:
            logger.error(f"Error resetting to defaults: {e}")
            return False
    
    def get_config_info(self) -> Dict[str, Any]:
        """
        Get information about the current configuration
        
        Returns:
            Dict[str, Any]: Configuration metadata
        """
        return {
            'version': self.config.get('version', 'Unknown'),
            'created_at': self.config.get('created_at', 'Unknown'),
            'last_modified': self.config.get('last_modified', 'Unknown'),
            'total_settings': len(self.config),
            'config_file_exists': os.path.exists(self.CONFIG_FILE),
            'backup_count': len([f for f in os.listdir(self.BACKUP_DIR) 
                               if f.startswith('config_backup_') and f.endswith('.json')])
        }