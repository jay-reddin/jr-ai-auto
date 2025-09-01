#!/usr/bin/env python3
"""
Test main application integration with thumbnail support
"""

import os
import sys
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_main_import():
    """Test importing main application"""
    try:
        # Create minimal config for testing
        config = {
            "api_key": "test_key",
            "model": "gemini-2.0-flash-exp",
            "theme_mode": "dark",
            "speech_enabled": False,
            "speech_muted": False
        }
        
        with open('config_test.json', 'w') as f:
            json.dump(config, f)
        
        # Test import (this will test all the integration)
        import main
        print("✓ Main application imports successfully")
        
        # Test creating app instance (without running mainloop)
        app = main.JRAIControlApp()
        print("✓ Application instance created successfully")
        
        # Test add_message with thumbnail
        app.add_message("Test", "Test message", screenshot_id="test_id", tokens=25)
        print("✓ add_message with thumbnail works")
        
        # Cleanup
        app.root.destroy()
        
        # Remove test config
        if os.path.exists('config_test.json'):
            os.remove('config_test.json')
        
        return True
        
    except Exception as e:
        print(f"✗ Main integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Testing main application integration...")
    
    success = test_main_import()
    
    if success:
        print("\n✓ All integration tests passed!")
        print("The thumbnail integration is working correctly.")
    else:
        print("\n✗ Integration tests failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())