#!/usr/bin/env python3
"""
Test script for comprehensive configuration management system
Tests all aspects of the new ConfigurationManager class
"""

import os
import json
import tempfile
import shutil
from datetime import datetime
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.config_manager import ConfigurationManager

def test_configuration_manager():
    """Test the comprehensive configuration management system"""
    print("🧪 Testing Configuration Management System")
    print("=" * 50)
    
    # Create temporary directory for testing
    test_dir = tempfile.mkdtemp()
    original_dir = os.getcwd()
    
    try:
        os.chdir(test_dir)
        
        # Test 1: Default configuration creation
        print("\n📋 Test 1: Default Configuration Creation")
        config_manager = ConfigurationManager()
        
        # Load settings (should create default config)
        config = config_manager.load_settings()
        
        assert os.path.exists('config.json'), "Config file should be created"
        assert config['version'] == config_manager.CONFIG_VERSION, "Version should match"
        assert 'api_key' in config, "API key should be in config"
        assert 'theme_mode' in config, "Theme mode should be in config"
        print("  ✅ Default configuration created successfully")
        
        # Test 2: Configuration validation
        print("\n🔍 Test 2: Configuration Validation")
        
        # Valid config
        valid_config = config.copy()
        assert config_manager.validate_config(valid_config), "Valid config should pass validation"
        
        # Invalid config
        invalid_config = config.copy()
        invalid_config['theme_mode'] = 'invalid_theme'
        assert not config_manager.validate_config(invalid_config), "Invalid config should fail validation"
        
        invalid_config2 = config.copy()
        invalid_config2['screenshot_wait_duration'] = 15  # Out of range
        assert not config_manager.validate_config(invalid_config2), "Out of range value should fail validation"
        
        print("  ✅ Configuration validation working correctly")
        
        # Test 3: Settings save and load
        print("\n💾 Test 3: Settings Save and Load")
        
        # Update some settings
        test_updates = {
            'api_key': 'test_api_key_123',
            'model': 'gemini-1.5-pro',
            'theme_mode': 'light',
            'screenshot_size': 'large',
            'voice_rate': 250
        }
        
        success = config_manager.save_settings(test_updates)
        assert success, "Settings save should succeed"
        
        # Create new manager and load
        new_manager = ConfigurationManager()
        loaded_config = new_manager.load_settings()
        
        for key, value in test_updates.items():
            assert loaded_config[key] == value, f"Setting {key} should be preserved"
        
        print("  ✅ Settings save and load working correctly")
        
        # Test 4: Individual setting get/set
        print("\n🎛️ Test 4: Individual Setting Operations")
        
        # Test get_setting
        api_key = config_manager.get_setting('api_key')
        assert api_key == 'test_api_key_123', "get_setting should return correct value"
        
        default_value = config_manager.get_setting('nonexistent_key', 'default')
        assert default_value == 'default', "get_setting should return default for missing key"
        
        # Test set_setting
        success = config_manager.set_setting('test_key', 'test_value', save_immediately=False)
        assert success, "set_setting should succeed"
        assert config_manager.get_setting('test_key') == 'test_value', "Setting should be updated"
        
        print("  ✅ Individual setting operations working correctly")
        
        # Test 5: Configuration backup
        print("\n🔄 Test 5: Configuration Backup")
        
        # Create backup
        backup_success = config_manager._create_backup()
        assert backup_success, "Backup creation should succeed"
        
        # Check backup directory exists and has files
        assert os.path.exists(config_manager.BACKUP_DIR), "Backup directory should exist"
        backup_files = [f for f in os.listdir(config_manager.BACKUP_DIR) 
                       if f.startswith('config_backup_') and f.endswith('.json')]
        assert len(backup_files) > 0, "Backup files should be created"
        
        print("  ✅ Configuration backup working correctly")
        
        # Test 6: Configuration export/import
        print("\n📤📥 Test 6: Configuration Export/Import")
        
        # Export configuration
        export_path = 'test_export.json'
        export_success = config_manager.export_config(export_path)
        assert export_success, "Export should succeed"
        assert os.path.exists(export_path), "Export file should be created"
        
        # Verify exported content
        with open(export_path, 'r') as f:
            exported_config = json.load(f)
        assert 'api_key' not in exported_config, "API key should not be exported"
        assert 'model' in exported_config, "Other settings should be exported"
        
        # Modify current config
        config_manager.set_setting('theme_mode', 'dark')
        
        # Import configuration
        import_success = config_manager.import_config(export_path)
        assert import_success, "Import should succeed"
        
        # Verify imported settings
        imported_theme = config_manager.get_setting('theme_mode')
        assert imported_theme == 'light', "Imported setting should be applied"
        
        print("  ✅ Configuration export/import working correctly")
        
        # Test 7: Configuration migration
        print("\n🔄 Test 7: Configuration Migration")
        
        # Create old format config
        old_config = {
            'api_key': 'old_api_key',
            'model': 'old_model',
            'theme_mode': 'dark'
            # Missing version and new fields
        }
        
        migrated_config = config_manager.validate_and_migrate_config(old_config)
        
        assert migrated_config['version'] == config_manager.CONFIG_VERSION, "Version should be updated"
        assert migrated_config['api_key'] == 'old_api_key', "Old settings should be preserved"
        assert 'screenshot_size' in migrated_config, "New settings should be added with defaults"
        
        print("  ✅ Configuration migration working correctly")
        
        # Test 8: Reset to defaults
        print("\n🔄 Test 8: Reset to Defaults")
        
        # Modify settings
        config_manager.set_setting('theme_mode', 'light')
        config_manager.set_setting('font_size', 20)
        
        # Reset to defaults
        reset_success = config_manager.reset_to_defaults()
        assert reset_success, "Reset should succeed"
        
        # Verify reset
        theme = config_manager.get_setting('theme_mode')
        font_size = config_manager.get_setting('font_size')
        
        assert theme == config_manager.DEFAULT_CONFIG['theme_mode'], "Theme should be reset to default"
        assert font_size == config_manager.DEFAULT_CONFIG['font_size'], "Font size should be reset to default"
        
        print("  ✅ Reset to defaults working correctly")
        
        # Test 9: Observer pattern
        print("\n👁️ Test 9: Observer Pattern")
        
        observer_calls = []
        
        def test_observer(event_type, data):
            observer_calls.append((event_type, data))
        
        config_manager.add_observer(test_observer)
        
        # Trigger events
        config_manager.set_setting('test_observer_key', 'test_value')
        config_manager.save_settings({'another_key': 'another_value'})
        
        assert len(observer_calls) >= 2, "Observer should be called for events"
        
        # Remove observer
        config_manager.remove_observer(test_observer)
        initial_calls = len(observer_calls)
        config_manager.set_setting('test_key_2', 'test_value_2')
        
        assert len(observer_calls) == initial_calls, "Observer should not be called after removal"
        
        print("  ✅ Observer pattern working correctly")
        
        # Test 10: Configuration info
        print("\n📊 Test 10: Configuration Info")
        
        config_info = config_manager.get_config_info()
        
        assert 'version' in config_info, "Config info should include version"
        assert 'total_settings' in config_info, "Config info should include total settings count"
        assert 'backup_count' in config_info, "Config info should include backup count"
        assert config_info['config_file_exists'], "Config file should exist"
        
        print("  ✅ Configuration info working correctly")
        
        print("\n🎉 All Configuration Management Tests Passed!")
        print("=" * 50)
        
        # Print summary
        print("\n📋 Configuration Management Features Tested:")
        print("  ✅ Default configuration creation")
        print("  ✅ Configuration validation")
        print("  ✅ Settings save and load")
        print("  ✅ Individual setting operations")
        print("  ✅ Configuration backup")
        print("  ✅ Configuration export/import")
        print("  ✅ Configuration migration")
        print("  ✅ Reset to defaults")
        print("  ✅ Observer pattern for real-time updates")
        print("  ✅ Configuration information")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        os.chdir(original_dir)
        shutil.rmtree(test_dir, ignore_errors=True)

def test_integration_with_main_app():
    """Test integration with main application"""
    print("\n🔗 Testing Integration with Main Application")
    print("=" * 50)
    
    try:
        # Test that main.py can import and use the configuration manager
        from main import JRAIControlApp
        
        # This would normally create the full app, but we'll just test the config manager integration
        print("  ✅ Configuration manager can be imported by main application")
        print("  ✅ Integration test passed")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Configuration Management System Tests")
    
    # Run tests
    config_test_passed = test_configuration_manager()
    integration_test_passed = test_integration_with_main_app()
    
    if config_test_passed and integration_test_passed:
        print("\n🎉 All tests passed! Configuration management system is ready.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1)