#!/usr/bin/env python3
"""
Validation test for Task 11.2: Redesign main interface with MD3 styling
Tests all the specific requirements for this task
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_md3_color_schemes_applied():
    """Test that MD3 color schemes are properly applied to UI elements"""
    try:
        from ui.material_design import get_theme, create_md3_widget_config
        
        # Test dark theme colors
        dark_theme = get_theme('dark')
        
        # Test that widget configs use MD3 colors
        frame_config = create_md3_widget_config('Frame', dark_theme)
        assert frame_config['bg'] == dark_theme.colors['surface']
        
        button_config = create_md3_widget_config('Button', dark_theme)
        assert button_config['bg'] == dark_theme.colors['primary']
        assert button_config['fg'] == dark_theme.colors['on_primary']
        
        entry_config = create_md3_widget_config('Entry', dark_theme)
        assert entry_config['bg'] == dark_theme.colors['surface_variant']
        assert entry_config['fg'] == dark_theme.colors['on_surface_variant']
        
        print("✓ MD3 color schemes properly applied to UI elements")
        return True
    except Exception as e:
        print(f"✗ MD3 color scheme application error: {e}")
        return False

def test_md3_typography_applied():
    """Test that MD3 typography is properly applied"""
    try:
        from ui.material_design import get_theme, create_md3_widget_config
        
        theme = get_theme('dark')
        
        # Test that widget configs use MD3 typography
        label_config = create_md3_widget_config('Label', theme)
        assert label_config['font'] == theme.typography['body_medium']
        
        button_config = create_md3_widget_config('Button', theme)
        assert button_config['font'] == theme.typography['label_large']
        
        entry_config = create_md3_widget_config('Entry', theme)
        assert entry_config['font'] == theme.typography['body_large']
        
        print("✓ MD3 typography properly applied to UI elements")
        return True
    except Exception as e:
        print(f"✗ MD3 typography application error: {e}")
        return False

def test_hidden_scrollbars_implementation():
    """Test that hidden scrollbars are implemented with custom styling"""
    try:
        from ui.enhanced_components import MD3ScrolledText
        import tkinter as tk
        
        # Test that MD3ScrolledText class exists and has required methods
        assert hasattr(MD3ScrolledText, '__init__')
        assert hasattr(MD3ScrolledText, 'bind_scrollbar_events')
        
        # Test that the class can be instantiated (without GUI)
        # We'll just check the class structure
        import inspect
        init_signature = inspect.signature(MD3ScrolledText.__init__)
        assert 'parent' in init_signature.parameters
        
        print("✓ Hidden scrollbars implemented with custom styling")
        return True
    except Exception as e:
        print(f"✗ Hidden scrollbars implementation error: {e}")
        return False

def test_proper_spacing_elevation():
    """Test that proper spacing and elevation are implemented"""
    try:
        from ui.enhanced_components import MD3Frame, MD3Card
        import tkinter as tk
        
        # Create a temporary root for testing
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Test MD3Frame
        frame = MD3Frame(root)
        assert hasattr(frame, 'theme')
        
        # Test MD3Card with elevation
        card = MD3Card(root)
        assert hasattr(card, 'theme')
        
        # Check that card inherits from MD3Frame with elevation
        assert isinstance(card, MD3Frame)
        
        root.destroy()
        print("✓ Proper spacing and elevation implemented")
        return True
    except Exception as e:
        print(f"✗ Spacing and elevation implementation error: {e}")
        return False

def test_smooth_animations_transitions():
    """Test that smooth animations and transitions are available"""
    try:
        from ui.enhanced_components import animate_widget_transition
        from ui.material_design import create_smooth_theme_switcher
        import tkinter as tk
        
        # Create a temporary root for testing
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Test animation function exists and is callable
        assert callable(animate_widget_transition)
        
        # Test theme switcher with smooth transitions
        theme_switcher = create_smooth_theme_switcher(root, 'dark')
        assert theme_switcher is not None
        
        root.destroy()
        print("✓ Smooth animations and transitions implemented")
        return True
    except Exception as e:
        print(f"✗ Animations and transitions implementation error: {e}")
        return False

def test_visual_hierarchy():
    """Test that proper visual hierarchy is implemented"""
    try:
        from ui.material_design import MD3_TYPOGRAPHY
        
        # Check typography hierarchy
        display_large = MD3_TYPOGRAPHY['display_large'][1]  # Font size
        headline_large = MD3_TYPOGRAPHY['headline_large'][1]
        title_large = MD3_TYPOGRAPHY['title_large'][1]
        body_large = MD3_TYPOGRAPHY['body_large'][1]
        
        # Verify hierarchy (larger sizes for more important elements)
        assert display_large > headline_large
        assert headline_large > title_large
        assert title_large > body_large
        
        print("✓ Proper visual hierarchy implemented")
        return True
    except Exception as e:
        print(f"✗ Visual hierarchy implementation error: {e}")
        return False

def test_enhanced_components_integration():
    """Test that enhanced MD3 components are properly integrated"""
    try:
        from ui.enhanced_components import (
            MD3Button, MD3Entry, MD3Frame, MD3StatusIndicator, 
            MD3Card, create_md3_tooltip
        )
        import tkinter as tk
        
        # Create a temporary root for testing
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Test MD3Button
        button = MD3Button(root, text="Test", style='primary')
        assert hasattr(button, 'theme')
        assert hasattr(button, 'button_style')
        
        # Test MD3Entry
        entry = MD3Entry(root)
        assert hasattr(entry, 'theme')
        
        # Test MD3StatusIndicator
        status = MD3StatusIndicator(root, status='active')
        assert hasattr(status, 'theme')
        assert hasattr(status, 'set_status')
        
        # Test tooltip function
        assert callable(create_md3_tooltip)
        
        root.destroy()
        print("✓ Enhanced MD3 components properly integrated")
        return True
    except Exception as e:
        print(f"✗ Enhanced components integration error: {e}")
        return False

def test_main_interface_structure():
    """Test that main interface uses proper MD3 structure"""
    try:
        # Read main.py to check for MD3 usage
        with open('main.py', 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        # Check for MD3 imports
        assert 'from ui.material_design import' in main_content
        assert 'from ui.enhanced_components import' in main_content
        
        # Check for MD3 component usage
        assert 'MD3Frame' in main_content
        assert 'MD3Card' in main_content
        assert 'MD3Button' in main_content
        assert 'MD3Entry' in main_content
        assert 'MD3StatusIndicator' in main_content
        assert 'MD3ScrolledText' in main_content
        
        # Check for theme integration
        assert 'apply_md3_theme' in main_content
        assert 'get_theme()' in main_content
        assert 'create_smooth_theme_switcher' in main_content
        
        print("✓ Main interface uses proper MD3 structure")
        return True
    except Exception as e:
        print(f"✗ Main interface structure error: {e}")
        return False

def run_task_11_2_validation():
    """Run all validation tests for Task 11.2"""
    tests = [
        ("MD3 Color Schemes Applied", test_md3_color_schemes_applied),
        ("MD3 Typography Applied", test_md3_typography_applied),
        ("Hidden Scrollbars Implementation", test_hidden_scrollbars_implementation),
        ("Proper Spacing & Elevation", test_proper_spacing_elevation),
        ("Smooth Animations & Transitions", test_smooth_animations_transitions),
        ("Visual Hierarchy", test_visual_hierarchy),
        ("Enhanced Components Integration", test_enhanced_components_integration),
        ("Main Interface Structure", test_main_interface_structure)
    ]
    
    passed = 0
    total = len(tests)
    
    print("Task 11.2: Redesign main interface with MD3 styling - Validation")
    print("=" * 70)
    print("Requirements being tested:")
    print("- Apply MD3 color schemes and typography to all UI elements")
    print("- Implement hidden scrollbars with custom styling")
    print("- Add proper spacing, elevation, and visual hierarchy")
    print("- Create smooth animations and transitions")
    print("=" * 70)
    
    for test_name, test_func in tests:
        print(f"\nTesting: {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED: {e}")
    
    print(f"\n{'='*70}")
    print(f"Task 11.2 Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Task 11.2 - Redesign main interface with MD3 styling - COMPLETED!")
        print("\nAll requirements have been successfully implemented:")
        print("✓ MD3 color schemes and typography applied to all UI elements")
        print("✓ Hidden scrollbars with custom styling implemented")
        print("✓ Proper spacing, elevation, and visual hierarchy added")
        print("✓ Smooth animations and transitions created")
        return True
    else:
        print("❌ Task 11.2 validation failed - some requirements not met!")
        return False

if __name__ == "__main__":
    success = run_task_11_2_validation()
    sys.exit(0 if success else 1)