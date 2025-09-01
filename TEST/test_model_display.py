#!/usr/bin/env python3
"""
Test script to verify model name display functionality
Tests requirements 7.1 and 7.2 for task 12.1
"""

import tkinter as tk
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_model_display():
    """Test the model name display functionality"""
    print("Testing Model Name Display (Task 12.1)")
    print("=" * 50)
    
    try:
        # Import the main application
        from main import JRAIControlApp
        
        # Create application instance
        app = JRAIControlApp()
        
        # Test 1: Check if model label exists
        print("✓ Test 1: Model label creation")
        assert hasattr(app, 'model_label'), "Model label should exist"
        assert app.model_label is not None, "Model label should not be None"
        print(f"  Model label exists: {app.model_label}")
        
        # Test 2: Check initial model display
        print("✓ Test 2: Initial model display")
        initial_text = app.model_label.cget('text')
        expected_text = f"Model: {app.current_model}"
        assert initial_text == expected_text, f"Expected '{expected_text}', got '{initial_text}'"
        print(f"  Initial model display: {initial_text}")
        
        # Test 3: Check MD3 styling
        print("✓ Test 3: MD3 styling applied")
        style = app.model_label.cget('style')
        assert style == 'MD3.Body.Medium.TLabel', f"Expected MD3 style, got '{style}'"
        print(f"  MD3 style applied: {style}")
        
        # Test 4: Test model update functionality
        print("✓ Test 4: Model update functionality")
        old_model = app.current_model
        new_model = "gemini-1.5-pro" if old_model != "gemini-1.5-pro" else "gemini-2.0-flash-exp"
        
        # Update model
        app.current_model = new_model
        app.update_model_display()
        
        # Check if display updated
        updated_text = app.model_label.cget('text')
        expected_updated_text = f"Model: {new_model}"
        assert updated_text == expected_updated_text, f"Expected '{expected_updated_text}', got '{updated_text}'"
        print(f"  Model updated from '{old_model}' to '{new_model}'")
        print(f"  Display updated to: {updated_text}")
        
        # Test 5: Check if update_model_display method exists and works
        print("✓ Test 5: update_model_display method")
        assert hasattr(app, 'update_model_display'), "update_model_display method should exist"
        assert callable(app.update_model_display), "update_model_display should be callable"
        print("  update_model_display method exists and is callable")
        
        # Clean up
        app.root.destroy()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed! Task 12.1 is properly implemented.")
        print("\nImplemented features:")
        print("- ✅ Model name displayed in header with MD3 styling")
        print("- ✅ Dynamic model name label updates when model changes")
        print("- ✅ Proper Material Design 3 typography applied")
        print("- ✅ update_model_display() method works correctly")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_model_display()
    sys.exit(0 if success else 1)