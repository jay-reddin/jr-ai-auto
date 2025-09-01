#!/usr/bin/env python3
"""
Simple test for thumbnail integration
"""

import os
import sys
from PIL import Image
import tempfile

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_screenshot_manager():
    """Test screenshot manager functionality"""
    from utils.screenshot_manager import ScreenshotManager
    
    # Create temporary directory
    test_dir = tempfile.mkdtemp(prefix="thumb_test_")
    print(f"Test directory: {test_dir}")
    
    # Initialize manager
    manager = ScreenshotManager(test_dir)
    
    # Create test image
    test_image = Image.new('RGB', (400, 300), (100, 150, 200))
    test_path = os.path.join(test_dir, "test.png")
    test_image.save(test_path)
    
    # Generate thumbnail
    screenshot_id = manager.create_screenshot_with_thumbnail(test_path)
    
    if screenshot_id:
        print(f"✓ Thumbnail generated with ID: {screenshot_id}")
        
        # Test thumbnail path
        thumb_path = manager.get_thumbnail_path(screenshot_id)
        if thumb_path and os.path.exists(thumb_path):
            print(f"✓ Thumbnail file exists: {thumb_path}")
            
            # Test thumbnail info
            info = manager.get_thumbnail_info(screenshot_id)
            if info:
                print(f"✓ Thumbnail info: {info}")
            else:
                print("✗ Could not get thumbnail info")
        else:
            print("✗ Thumbnail file not found")
    else:
        print("✗ Failed to generate thumbnail")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    print("✓ Cleanup completed")

def test_chat_interface_creation():
    """Test chat interface creation without GUI"""
    try:
        import tkinter as tk
        from ui.chat_interface import ChatInterface
        from ui.material_design import apply_md3_theme
        
        # Create root window (but don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Apply theme
        apply_md3_theme(root, "dark")
        
        # Create chat interface
        chat = ChatInterface(root)
        
        print("✓ Chat interface created successfully")
        
        # Test adding a message
        message_widget = chat.add_message(
            sender="Test",
            message="Test message",
            is_user=False,
            tokens=25
        )
        
        if message_widget:
            print("✓ Message added successfully")
        else:
            print("✗ Failed to add message")
        
        # Cleanup
        root.destroy()
        
    except Exception as e:
        print(f"✗ Chat interface test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("Running simple thumbnail integration tests...")
    
    print("\n1. Testing Screenshot Manager:")
    test_screenshot_manager()
    
    print("\n2. Testing Chat Interface:")
    test_chat_interface_creation()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main()