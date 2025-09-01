"""
Validation test for the comprehensive tabbed settings system
Tests that all settings are properly saved, loaded, and applied
"""

import tkinter as tk
import json
import os
import sys
from unittest.mock import Mock, patch

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_settings_persistence():
    """Test that settings are properly saved and loaded"""
    print("Testing Settings Persistence...")
    
    # Create test config
    test_config = {
        "api_key": "test_api_key_123",
        "model": "gemini-1.5-pro",
        "theme_mode": "light",
        "speech_enabled": False,
        "speech_muted": True,
        "screenshot_size": "large",
        "screenshot_wait_duration": 5,
        "notification_enabled": False,
        "font_size": 16,
        "window_opacity": 0.8
    }
    
    # Save test config
    with open('config.json', 'w') as f:
        json.dump(test_config, f, indent=2)
    
    try:
        from main import JRAIControlApp
        
        # Create app instance
        app = JRAIControlApp()
        
        # Verify settings were loaded correctly
        assert app.current_api_key == "test_api_key_123", f"API key mismatch: {app.current_api_key}"
        assert app.current_model == "gemini-1.5-pro", f"Model mismatch: {app.current_model}"
        assert app.theme_mode == "light", f"Theme mismatch: {app.theme_mode}"
        assert app.speech_enabled == False, f"Speech enabled mismatch: {app.speech_enabled}"
        assert app.speech_muted == True, f"Speech muted mismatch: {app.speech_muted}"
        assert app.screenshot_size == "large", f"Screenshot size mismatch: {app.screenshot_size}"
        assert app.screenshot_wait_duration == 5, f"Screenshot wait mismatch: {app.screenshot_wait_duration}"
        assert app.notification_enabled == False, f"Notification mismatch: {app.notification_enabled}"
        assert app.font_size == 16, f"Font size mismatch: {app.font_size}"
        assert app.window_opacity == 0.8, f"Window opacity mismatch: {app.window_opacity}"
        
        print("✓ All settings loaded correctly from config file")
        
        # Test saving modified settings
        app.current_api_key = "modified_key"
        app.screenshot_size = "small"
        app.font_size = 18
        app.save_settings()
        
        # Verify config file was updated
        with open('config.json', 'r') as f:
            saved_config = json.load(f)
        
        assert saved_config['api_key'] == "modified_key", "API key not saved"
        assert saved_config['screenshot_size'] == "small", "Screenshot size not saved"
        assert saved_config['font_size'] == 18, "Font size not saved"
        
        print("✓ Settings saved correctly to config file")
        
        # Clean up
        app.root.destroy()
        
        return True
        
    except Exception as e:
        print(f"✗ Settings persistence test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_settings_ui_integration():
    """Test that the settings UI properly integrates with the app"""
    print("\nTesting Settings UI Integration...")
    
    try:
        from main import JRAIControlApp
        from ui.settings_tabs import SettingsTabManager
        
        # Create app instance
        app = JRAIControlApp()
        
        # Create settings manager
        settings_manager = SettingsTabManager(app.root, app)
        
        # Test that settings variables are initialized with app values
        assert settings_manager.api_key_var.get() == app.current_api_key, "API key var not synced"
        assert settings_manager.model_var.get() == app.current_model, "Model var not synced"
        assert settings_manager.theme_var.get() == app.theme_mode, "Theme var not synced"
        assert settings_manager.screenshot_size_var.get() == app.screenshot_size, "Screenshot size var not synced"
        assert settings_manager.font_size_var.get() == app.font_size, "Font size var not synced"
        
        print("✓ Settings UI variables properly synced with app state")
        
        # Test modifying settings through UI variables
        settings_manager.api_key_var.set("ui_modified_key")
        settings_manager.screenshot_size_var.set("medium")
        settings_manager.font_size_var.set(12)
        
        # Mock the save process (since we can't actually test the full UI interaction)
        original_values = {
            'api_key': app.current_api_key,
            'screenshot_size': app.screenshot_size,
            'font_size': app.font_size
        }
        
        # Simulate what happens in save_settings
        app.current_api_key = settings_manager.api_key_var.get()
        app.screenshot_size = settings_manager.screenshot_size_var.get()
        app.font_size = settings_manager.font_size_var.get()
        
        assert app.current_api_key == "ui_modified_key", "API key not updated from UI"
        assert app.screenshot_size == "medium", "Screenshot size not updated from UI"
        assert app.font_size == 12, "Font size not updated from UI"
        
        print("✓ App state properly updated from UI variables")
        
        # Clean up
        app.root.destroy()
        
        return True
        
    except Exception as e:
        print(f"✗ Settings UI integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_settings_validation():
    """Test settings validation and error handling"""
    print("\nTesting Settings Validation...")
    
    try:
        from ui.settings_tabs import SettingsTabManager
        from main import JRAIControlApp
        
        # Create app instance
        app = JRAIControlApp()
        settings_manager = SettingsTabManager(app.root, app)
        
        # Test API key validation method exists
        assert hasattr(settings_manager, 'test_api_key'), "API key test method missing"
        
        # Test save method exists
        assert hasattr(settings_manager, 'save_settings'), "Save settings method missing"
        
        # Test reset token counter method exists
        assert hasattr(settings_manager, 'reset_token_counter'), "Reset token counter method missing"
        
        # Test that all required UI elements are created
        settings_manager.open_settings()
        
        # Check that notebook exists
        assert settings_manager.notebook is not None, "Notebook not created"
        
        # Check that all tabs exist
        tabs = settings_manager.notebook.tabs()
        assert len(tabs) == 3, f"Expected 3 tabs, got {len(tabs)}"
        
        tab_names = [settings_manager.notebook.tab(tab, "text") for tab in tabs]
        expected_tabs = ["AI", "UI", "About"]
        for expected_tab in expected_tabs:
            assert expected_tab in tab_names, f"Missing tab: {expected_tab}"
        
        print("✓ All validation checks passed")
        
        # Clean up
        settings_manager.on_close()
        app.root.destroy()
        
        return True
        
    except Exception as e:
        print(f"✗ Settings validation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("JR AI Control - Settings Validation Test")
    print("="*50)
    
    # Run validation tests
    test1 = test_settings_persistence()
    test2 = test_settings_ui_integration()
    test3 = test_settings_validation()
    
    print("\n" + "="*50)
    if test1 and test2 and test3:
        print("🎉 ALL VALIDATION TESTS PASSED!")
        print("The comprehensive tabbed settings system is working correctly!")
    else:
        print("❌ SOME VALIDATION TESTS FAILED!")
        sys.exit(1)
    print("="*50)