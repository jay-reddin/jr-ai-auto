#!/usr/bin/env python3
"""
Test script for thumbnail integration in chat interface.
Tests the complete thumbnail workflow from screenshot generation to chat display.
"""

import tkinter as tk
import os
import sys
import tempfile
import shutil
from PIL import Image
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.chat_interface import ChatInterface, ThumbnailViewer
from ui.material_design import apply_md3_theme
from utils.screenshot_manager import ScreenshotManager

class ThumbnailIntegrationTest:
    """Test class for thumbnail integration functionality"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Thumbnail Integration Test")
        self.root.geometry("800x600")
        
        # Apply MD3 theme
        apply_md3_theme(self.root, "dark")
        
        # Create test directory
        self.test_dir = tempfile.mkdtemp(prefix="thumbnail_test_")
        self.screenshots_dir = os.path.join(self.test_dir, "screenshots")
        
        # Initialize screenshot manager
        self.screenshot_manager = ScreenshotManager(self.screenshots_dir)
        
        # Create chat interface
        self.chat_interface = ChatInterface(self.root)
        self.chat_interface.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Set up callbacks
        self.chat_interface.set_resend_callback(self.on_resend)
        self.chat_interface.set_delete_callback(self.on_delete)
        
        # Create test UI
        self.create_test_controls()
        
        # Run tests
        self.run_tests()
    
    def create_test_controls(self):
        """Create test control buttons"""
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Test buttons
        tk.Button(control_frame, text="Test Basic Message", 
                 command=self.test_basic_message).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Test Message with Thumbnail", 
                 command=self.test_message_with_thumbnail).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Test Multiple Thumbnails", 
                 command=self.test_multiple_thumbnails).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Test Thumbnail Viewer", 
                 command=self.test_thumbnail_viewer).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="Clear Chat", 
                 command=self.clear_chat).pack(side=tk.LEFT, padx=5)
    
    def create_test_image(self, filename, size=(400, 300), color=(100, 150, 200)):
        """Create a test image for thumbnail testing"""
        image = Image.new('RGB', size, color)
        
        # Add some text to make it identifiable
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(image)
        
        try:
            # Try to load a font
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        text = f"Test Image\n{filename}\n{datetime.now().strftime('%H:%M:%S')}"
        draw.text((10, 10), text, fill=(255, 255, 255), font=font)
        
        # Save image
        image_path = os.path.join(self.test_dir, filename)
        image.save(image_path)
        return image_path
    
    def test_basic_message(self):
        """Test adding a basic message without thumbnail"""
        self.chat_interface.add_message(
            sender="Test User",
            message="This is a basic test message without any thumbnail.",
            is_user=True
        )
        
        self.chat_interface.add_message(
            sender="Test AI",
            message="This is an AI response without thumbnail.",
            is_user=False,
            tokens=25
        )
        
        print("✓ Basic message test completed")
    
    def test_message_with_thumbnail(self):
        """Test adding a message with a thumbnail"""
        # Create test image
        image_path = self.create_test_image("test_screenshot_1.png")
        
        # Generate thumbnail
        screenshot_id = self.screenshot_manager.create_screenshot_with_thumbnail(image_path)
        
        if screenshot_id:
            self.chat_interface.add_message(
                sender="Test AI",
                message="I took a screenshot and generated a thumbnail. Click the thumbnail to view the full image.",
                is_user=False,
                screenshot_id=screenshot_id,
                tokens=42
            )
            print(f"✓ Message with thumbnail test completed (ID: {screenshot_id})")
        else:
            print("✗ Failed to generate thumbnail")
    
    def test_multiple_thumbnails(self):
        """Test multiple messages with different thumbnails"""
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
        
        for i, color in enumerate(colors):
            # Create test image with different color
            image_path = self.create_test_image(f"test_screenshot_{i+2}.png", color=color)
            
            # Generate thumbnail
            screenshot_id = self.screenshot_manager.create_screenshot_with_thumbnail(image_path)
            
            if screenshot_id:
                self.chat_interface.add_message(
                    sender="Test AI",
                    message=f"Screenshot #{i+1} with color {color}. This tests multiple thumbnails in the chat.",
                    is_user=False,
                    screenshot_id=screenshot_id,
                    tokens=35 + i * 5
                )
        
        print("✓ Multiple thumbnails test completed")
    
    def test_thumbnail_viewer(self):
        """Test the thumbnail viewer modal"""
        # Create a larger test image
        image_path = self.create_test_image("large_test.png", size=(800, 600), color=(200, 100, 50))
        
        # Test the viewer directly
        try:
            viewer = ThumbnailViewer(self.root, image_path, "Test Thumbnail Viewer")
            print("✓ Thumbnail viewer test completed")
        except Exception as e:
            print(f"✗ Thumbnail viewer test failed: {e}")
    
    def test_thumbnail_caching(self):
        """Test thumbnail caching and loading"""
        # Create test image
        image_path = self.create_test_image("cache_test.png")
        
        # Generate thumbnail
        screenshot_id = self.screenshot_manager.create_screenshot_with_thumbnail(image_path)
        
        if screenshot_id:
            # Test getting thumbnail path
            thumbnail_path = self.screenshot_manager.get_thumbnail_path(screenshot_id)
            if thumbnail_path and os.path.exists(thumbnail_path):
                print("✓ Thumbnail caching test completed")
                
                # Test thumbnail info
                info = self.screenshot_manager.get_thumbnail_info(screenshot_id)
                if info:
                    print(f"  - Thumbnail info: {info['dimensions']}, {info['file_size']} bytes")
                else:
                    print("✗ Failed to get thumbnail info")
            else:
                print("✗ Thumbnail caching test failed - thumbnail not found")
        else:
            print("✗ Thumbnail caching test failed - could not generate thumbnail")
    
    def clear_chat(self):
        """Clear all messages from chat"""
        self.chat_interface.clear_messages()
        print("✓ Chat cleared")
    
    def on_resend(self, message_text):
        """Handle message resend"""
        print(f"Resend requested: {message_text[:50]}...")
        # Add the message back as user message
        self.chat_interface.add_message(
            sender="Resent User",
            message=message_text,
            is_user=True
        )
    
    def on_delete(self, message_widget):
        """Handle message delete"""
        print("Delete requested for message")
        message_widget.pack_forget()
        message_widget.destroy()
    
    def run_tests(self):
        """Run all automated tests"""
        print("Running thumbnail integration tests...")
        
        # Add initial test messages
        self.root.after(500, self.test_basic_message)
        self.root.after(1000, self.test_message_with_thumbnail)
        self.root.after(1500, self.test_thumbnail_caching)
        
        print("Tests scheduled. Use the buttons to run additional tests.")
    
    def cleanup(self):
        """Clean up test files"""
        try:
            shutil.rmtree(self.test_dir)
            print(f"✓ Cleaned up test directory: {self.test_dir}")
        except Exception as e:
            print(f"Warning: Could not clean up test directory: {e}")
    
    def run(self):
        """Run the test application"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nTest interrupted by user")
        finally:
            self.cleanup()
    
    def on_closing(self):
        """Handle window closing"""
        self.cleanup()
        self.root.destroy()

def main():
    """Main test function"""
    print("Starting Thumbnail Integration Test...")
    print("This test will:")
    print("1. Create a chat interface with thumbnail support")
    print("2. Test basic message display")
    print("3. Test messages with thumbnails")
    print("4. Test thumbnail click-to-expand functionality")
    print("5. Test message actions (resend, copy, delete)")
    print()
    
    # Check dependencies
    try:
        from ui.chat_interface import ChatInterface
        from utils.screenshot_manager import ScreenshotManager
        print("✓ All required modules imported successfully")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return 1
    
    # Run test
    test = ThumbnailIntegrationTest()
    test.run()
    
    return 0

if __name__ == "__main__":
    exit(main())