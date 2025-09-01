#!/usr/bin/env python3
"""
Test script for voice interaction system integration
Tests speech recognition, text-to-speech, and UI integration
"""

import sys
import os
import time
import threading
from unittest.mock import Mock, patch

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_voice_manager_import():
    """Test that voice manager can be imported"""
    try:
        from voice.voice_manager import get_voice_manager, is_voice_available
        print("✓ Voice manager import successful")
        return True
    except ImportError as e:
        print(f"✗ Voice manager import failed: {e}")
        return False

def test_voice_manager_initialization():
    """Test voice manager initialization"""
    try:
        from voice.voice_manager import get_voice_manager
        
        voice_manager = get_voice_manager()
        print(f"✓ Voice manager initialized, available: {voice_manager.is_voice_available()}")
        
        # Test basic properties
        assert hasattr(voice_manager, 'speech_enabled')
        assert hasattr(voice_manager, 'speech_muted')
        assert hasattr(voice_manager, 'is_listening')
        print("✓ Voice manager has required properties")
        
        return True
    except Exception as e:
        print(f"✗ Voice manager initialization failed: {e}")
        return False

def test_voice_callbacks():
    """Test voice callback system"""
    try:
        from voice.voice_manager import get_voice_manager
        
        voice_manager = get_voice_manager()
        
        # Test callback assignment
        callback_called = False
        
        def test_callback(text):
            nonlocal callback_called
            callback_called = True
        
        voice_manager.on_speech_recognized = test_callback
        
        # Simulate speech recognition (if available)
        if voice_manager.is_voice_available():
            print("✓ Voice callbacks can be assigned")
        else:
            print("✓ Voice callbacks can be assigned (voice not available)")
        
        return True
    except Exception as e:
        print(f"✗ Voice callback test failed: {e}")
        return False

def test_voice_settings():
    """Test voice settings functionality"""
    try:
        from voice.voice_manager import get_voice_manager
        
        voice_manager = get_voice_manager()
        
        # Test settings methods
        voice_manager.toggle_speech_enabled(True)
        voice_manager.toggle_speech_muted(False)
        
        if voice_manager.is_voice_available():
            voice_manager.set_voice_settings(rate=200, volume=0.8)
            voices = voice_manager.get_available_voices()
            print(f"✓ Voice settings work, {len(voices)} voices available")
        else:
            print("✓ Voice settings work (voice not available)")
        
        return True
    except Exception as e:
        print(f"✗ Voice settings test failed: {e}")
        return False

def test_main_app_voice_integration():
    """Test voice integration in main application"""
    try:
        # Mock tkinter to avoid GUI creation
        with patch('tkinter.Tk'), patch('tkinter.ttk.Style'):
            from main import JRAIControlApp
            
            # Create app instance (mocked)
            app = JRAIControlApp()
            
            # Test voice manager integration
            assert hasattr(app, 'voice_manager')
            assert hasattr(app, 'speech_enabled')
            assert hasattr(app, 'speech_muted')
            assert hasattr(app, 'is_listening')
            
            # Test voice methods
            assert hasattr(app, 'toggle_listening')
            assert hasattr(app, 'toggle_speech_enabled')
            assert hasattr(app, 'toggle_speech_muted')
            
            print("✓ Main app voice integration successful")
            return True
            
    except Exception as e:
        print(f"✗ Main app voice integration failed: {e}")
        return False

def test_voice_ui_components():
    """Test voice UI components"""
    try:
        # Test that voice UI components can be imported and have required methods
        from ui.enhanced_components import MD3Button, MD3StatusIndicator
        
        # Test that classes exist and can be imported
        assert MD3Button is not None
        assert MD3StatusIndicator is not None
        
        print("✓ Voice UI components can be imported")
        return True
            
    except Exception as e:
        print(f"✗ Voice UI components test failed: {e}")
        return False

def test_keyboard_shortcuts():
    """Test keyboard shortcut functionality"""
    try:
        with patch('tkinter.Tk'), patch('tkinter.ttk.Style'):
            from main import JRAIControlApp
            
            app = JRAIControlApp()
            
            # Test that keyboard shortcut methods exist
            assert hasattr(app, 'setup_keyboard_shortcuts')
            
            # Test shortcut methods
            app.toggle_listening()  # Should not crash
            app.toggle_speech_enabled()  # Should not crash
            app.toggle_speech_muted()  # Should not crash
            
            print("✓ Keyboard shortcuts work")
            return True
            
    except Exception as e:
        print(f"✗ Keyboard shortcuts test failed: {e}")
        return False

def run_all_tests():
    """Run all voice integration tests"""
    print("=== Voice Integration Test Suite ===\n")
    
    tests = [
        test_voice_manager_import,
        test_voice_manager_initialization,
        test_voice_callbacks,
        test_voice_settings,
        test_main_app_voice_integration,
        test_voice_ui_components,
        test_keyboard_shortcuts
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} crashed: {e}")
        print()
    
    print(f"=== Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("🎉 All voice integration tests passed!")
        return True
    else:
        print("❌ Some voice integration tests failed")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)