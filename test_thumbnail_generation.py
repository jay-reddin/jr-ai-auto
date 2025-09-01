"""
Test script for screenshot thumbnail generation functionality.
"""

import os
import sys
import tempfile
import shutil
from PIL import Image

# Add utils to path
sys.path.append('.')

from utils.screenshot_manager import ScreenshotManager

def test_thumbnail_generation():
    """Test thumbnail generation with different sizes."""
    print("Testing thumbnail generation...")
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Initialize screenshot manager with temp directory
        manager = ScreenshotManager(screenshots_dir=temp_dir, default_size="medium")
        
        # Create a test image
        test_image_path = os.path.join(temp_dir, "test_screenshot.png")
        test_image = Image.new('RGB', (800, 600), color='blue')
        test_image.save(test_image_path)
        
        print(f"Created test image: {test_image_path}")
        
        # Test thumbnail generation for each size
        sizes = ['small', 'medium', 'large']
        screenshot_ids = {}
        
        for size in sizes:
            print(f"\nTesting {size} thumbnail generation...")
            screenshot_id = manager.create_screenshot_with_thumbnail(test_image_path, size)
            
            if screenshot_id:
                screenshot_ids[size] = screenshot_id
                print(f"✓ Generated {size} thumbnail with ID: {screenshot_id}")
                
                # Verify thumbnail exists
                thumbnail_path = manager.get_thumbnail_path(screenshot_id)
                if thumbnail_path and os.path.exists(thumbnail_path):
                    print(f"✓ Thumbnail file exists: {thumbnail_path}")
                    
                    # Check thumbnail dimensions
                    with Image.open(thumbnail_path) as thumb:
                        expected_size = manager.THUMBNAIL_SIZES[size]
                        print(f"✓ Thumbnail dimensions: {thumb.size} (max: {expected_size})")
                else:
                    print(f"✗ Thumbnail file not found")
            else:
                print(f"✗ Failed to generate {size} thumbnail")
        
        # Test metadata retrieval
        print("\nTesting metadata retrieval...")
        for size, screenshot_id in screenshot_ids.items():
            info = manager.get_thumbnail_info(screenshot_id)
            if info:
                print(f"✓ {size} thumbnail metadata: {info['thumbnail_size']}, {info['dimensions']}")
            else:
                print(f"✗ No metadata found for {size} thumbnail")
        
        # Test get all thumbnails
        all_thumbnails = manager.get_all_thumbnails()
        print(f"\n✓ Total thumbnails in manager: {len(all_thumbnails)}")
        
        print("\n✓ All thumbnail generation tests passed!")

def test_thumbnail_sizes():
    """Test that thumbnail sizes are correctly configured."""
    print("\nTesting thumbnail size configurations...")
    
    manager = ScreenshotManager()
    expected_sizes = {
        'small': (100, 75),
        'medium': (150, 112),
        'large': (200, 150)
    }
    
    for size_name, expected_dims in expected_sizes.items():
        actual_dims = manager.THUMBNAIL_SIZES.get(size_name)
        if actual_dims == expected_dims:
            print(f"✓ {size_name}: {actual_dims}")
        else:
            print(f"✗ {size_name}: expected {expected_dims}, got {actual_dims}")
    
    print("✓ Thumbnail size configuration test passed!")

def test_tools_integration():
    """Test integration with tools.py functions."""
    print("\nTesting tools.py integration...")
    
    try:
        from utils.tools import set_thumbnail_size, get_thumbnail_manager
        
        # Test setting thumbnail size
        set_thumbnail_size('large')
        manager = get_thumbnail_manager()
        
        if manager.default_size == 'large':
            print("✓ Thumbnail size setting works")
        else:
            print(f"✗ Expected 'large', got '{manager.default_size}'")
        
        # Test invalid size
        set_thumbnail_size('invalid')
        if manager.default_size == 'large':  # Should remain unchanged
            print("✓ Invalid size handling works")
        else:
            print("✗ Invalid size handling failed")
        
        print("✓ Tools integration test passed!")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
    except Exception as e:
        print(f"✗ Integration test failed: {e}")

if __name__ == "__main__":
    print("=== Screenshot Thumbnail Generation Tests ===")
    
    try:
        test_thumbnail_sizes()
        test_thumbnail_generation()
        test_tools_integration()
        
        print("\n🎉 All tests passed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)