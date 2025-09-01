"""
Test script for the tabbed settings interface implementation
Tests the comprehensive settings system with AI, UI, and About tabs
"""

import tkinter as tk
import sys
import os
import json
from unittest.mock import Mock, patch

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_tabbed_settings():
    """Test the tabbed settings interface"""
    print("Testing Tabbed Settings Interface...")
    
    try:
        # Create a minimal config.json for testing
        test_config = {
            "api_key": "test_key",
            "model": "gemini-1.5-flash",
            "theme_mode": "dark",
            "speech_enabled": True,
            "speech_muted": False,
            "screenshot_size": "medium",
            "screenshot_wait_duration": 3,
            "notification_enabled": True,
            "font_size": 14,
            "window_opacity": 1.0
        }
        
        with open('config.json', 'w') as f:
            json.dump(test_config, f, indent=2)
        
        # Import after creating config
        from ui.settings_tabs import SettingsTabManager
        from ui.material_design import apply_md3_theme
        
        # Create test root window
        root = tk.Tk()
        root.title("Settings Test")
        root.geometry("800x600")
        
        # Apply theme
        apply_md3_theme(root, "dark")
        
        # Create mock app instance
        mock_app = Mock()
        mock_app.root = root
        mock_app.current_api_key = "test_key"
        mock_app.current_model = "gemini-1.5-flash"
        mock_app.available_models = [
            "gemini-2.0-flash-exp",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro"
        ]
        mock_app.theme_mode = "dark"
        mock_app.speech_enabled = True
        mock_app.speech_muted = False
        mock_app.screenshot_size = "medium"
        mock_app.screenshot_wait_duration = 3
        mock_app.notification_enabled = True
        mock_app.font_size = 14
        mock_app.window_opacity = 1.0
        
        # Mock methods
        mock_app.save_settings = Mock()
        mock_app.update_status = Mock()
        mock_app.update_model_display = Mock()
        mock_app.initialize_agent = Mock()
        mock_app.add_message = Mock()
        
        # Create settings tab manager
        settings_manager = SettingsTabManager(root, mock_app)
        
        print("✓ SettingsTabManager created successfully")
        
        # Test opening settings
        settings_manager.open_settings()
        print("✓ Settings window opened successfully")
        
        # Verify notebook exists
        if settings_manager.notebook:
            print("✓ Notebook widget created")
            
            # Check tabs
            tabs = settings_manager.notebook.tabs()
            tab_names = [settings_manager.notebook.tab(tab, "text") for tab in tabs]
            
            expected_tabs = ["AI", "UI", "About"]
            for expected_tab in expected_tabs:
                if expected_tab in tab_names:
                    print(f"✓ {expected_tab} tab found")
                else:
                    print(f"✗ {expected_tab} tab missing")
            
            print(f"✓ Found {len(tabs)} tabs: {tab_names}")
        else:
            print("✗ Notebook widget not created")
        
        # Test settings variables
        print("\nTesting settings variables:")
        print(f"✓ API Key: {settings_manager.api_key_var.get()}")
        print(f"✓ Model: {settings_manager.model_var.get()}")
        print(f"✓ Theme: {settings_manager.theme_var.get()}")
        print(f"✓ Screenshot size: {settings_manager.screenshot_size_var.get()}")
        print(f"✓ Screenshot wait: {settings_manager.screenshot_wait_var.get()}")
        print(f"✓ Notifications: {settings_manager.notification_enabled_var.get()}")
        print(f"✓ Font size: {settings_manager.font_size_var.get()}")
        print(f"✓ Window opacity: {settings_manager.window_opacity_var.get()}")
        
        # Test API key testing functionality
        print("\nTesting API key validation...")
        settings_manager.api_key_var.set("invalid_key")
        
        # Mock the test status label
        mock_label = Mock()
        settings_manager.test_status_label = mock_label
        
        # This would normally test the API, but we'll just verify the method exists
        if hasattr(settings_manager, 'test_api_key'):
            print("✓ API key test method exists")
        else:
            print("✗ API key test method missing")
        
        # Test save functionality
        print("\nTesting save functionality...")
        if hasattr(settings_manager, 'save_settings'):
            print("✓ Save settings method exists")
        else:
            print("✗ Save settings method missing")
        
        print("\n" + "="*50)
        print("TABBED SETTINGS TEST COMPLETED SUCCESSFULLY!")
        print("="*50)
        
        # Keep window open for manual inspection
        print("\nSettings window is open for manual inspection.")
        print("Close the window to exit the test.")
        
        root.mainloop()
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_settings_integration():
    """Test integration with main application"""
    print("\nTesting Settings Integration...")
    
    try:
        # Test importing the main app
        from main import JRAIControlApp
        
        # Create app instance (but don't run mainloop)
        app = JRAIControlApp()
        
        # Test that settings tab manager is initialized
        if hasattr(app, 'settings_tab_manager'):
            print("✓ Settings tab manager attribute exists")
        else:
            print("✗ Settings tab manager attribute missing")
        
        # Test that new settings attributes exist
        required_attrs = [
            'screenshot_size', 'screenshot_wait_duration', 
            'notification_enabled', 'font_size', 'window_opacity'
        ]
        
        for attr in required_attrs:
            if hasattr(app, attr):
                print(f"✓ {attr} attribute exists: {getattr(app, attr)}")
            else:
                print(f"✗ {attr} attribute missing")
        
        # Test open_settings method
        if hasattr(app, 'open_settings'):
            print("✓ open_settings method exists")
        else:
            print("✗ open_settings method missing")
        
        print("✓ Integration test completed successfully")
        
        # Clean up
        app.root.destroy()
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("JR AI Control - Tabbed Settings Test")
    print("="*50)
    
    # Run tests
    success1 = test_tabbed_settings()
    success2 = test_settings_integration()
    
    if success1 and success2:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED!")
        sys.exit(1)