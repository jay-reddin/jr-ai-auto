#!/usr/bin/env python3
"""
Validation test for Material Design 3 interface implementation
Tests the MD3 components without GUI interaction
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_md3_imports():
    """Test that all MD3 components can be imported"""
    try:
        from ui.material_design import (
            apply_md3_theme, get_theme, switch_theme, 
            create_smooth_theme_switcher, MD3_DARK_THEME, MD3_LIGHT_THEME
        )
        from ui.enhanced_components import (
            MD3ScrolledText, MD3Button, MD3Entry, MD3Frame, 
            MD3StatusIndicator, MD3Card, create_md3_tooltip
        )
        print("✓ All MD3 components imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_theme_system():
    """Test the theme system functionality"""
    try:
        from ui.material_design import get_theme, MD3_DARK_THEME, MD3_LIGHT_THEME
        
        # Test dark theme
        dark_theme = get_theme('dark')
        assert dark_theme.theme_mode == 'dark'
        assert dark_theme.colors == MD3_DARK_THEME
        print("✓ Dark theme system working")
        
        # Test light theme
        light_theme = get_theme('light')
        assert light_theme.theme_mode == 'light'
        assert light_theme.colors == MD3_LIGHT_THEME
        print("✓ Light theme system working")
        
        # Test theme switching
        dark_theme.switch_theme('light')
        assert dark_theme.theme_mode == 'light'
        print("✓ Theme switching working")
        
        return True
    except Exception as e:
        print(f"✗ Theme system error: {e}")
        return False

def test_color_schemes():
    """Test that color schemes have all required colors"""
    try:
        from ui.material_design import MD3_DARK_THEME, MD3_LIGHT_THEME
        
        required_colors = [
            'primary', 'on_primary', 'primary_container', 'on_primary_container',
            'secondary', 'on_secondary', 'secondary_container', 'on_secondary_container',
            'tertiary', 'on_tertiary', 'tertiary_container', 'on_tertiary_container',
            'error', 'on_error', 'error_container', 'on_error_container',
            'background', 'on_background', 'surface', 'on_surface',
            'surface_variant', 'on_surface_variant', 'outline', 'outline_variant'
        ]
        
        # Test dark theme colors
        for color in required_colors:
            assert color in MD3_DARK_THEME, f"Missing {color} in dark theme"
        print("✓ Dark theme has all required colors")
        
        # Test light theme colors
        for color in required_colors:
            assert color in MD3_LIGHT_THEME, f"Missing {color} in light theme"
        print("✓ Light theme has all required colors")
        
        return True
    except Exception as e:
        print(f"✗ Color scheme error: {e}")
        return False

def test_typography_system():
    """Test the typography system"""
    try:
        from ui.material_design import MD3_TYPOGRAPHY
        
        required_styles = [
            'display_large', 'display_medium', 'display_small',
            'headline_large', 'headline_medium', 'headline_small',
            'title_large', 'title_medium', 'title_small',
            'body_large', 'body_medium', 'body_small',
            'label_large', 'label_medium', 'label_small'
        ]
        
        for style in required_styles:
            assert style in MD3_TYPOGRAPHY, f"Missing {style} in typography"
            font_tuple = MD3_TYPOGRAPHY[style]
            assert len(font_tuple) == 3, f"Invalid font tuple for {style}"
            assert isinstance(font_tuple[0], str), f"Font family should be string for {style}"
            assert isinstance(font_tuple[1], int), f"Font size should be int for {style}"
            assert isinstance(font_tuple[2], str), f"Font weight should be string for {style}"
        
        print("✓ Typography system has all required styles")
        return True
    except Exception as e:
        print(f"✗ Typography system error: {e}")
        return False

def test_widget_configs():
    """Test widget configuration generation"""
    try:
        from ui.material_design import create_md3_widget_config, get_theme
        
        theme = get_theme('dark')
        
        # Test different widget types
        widget_types = ['Frame', 'Label', 'Button', 'SecondaryButton', 'Entry', 'Text']
        
        for widget_type in widget_types:
            config = create_md3_widget_config(widget_type, theme)
            assert isinstance(config, dict), f"Config should be dict for {widget_type}"
            print(f"✓ {widget_type} configuration generated")
        
        return True
    except Exception as e:
        print(f"✗ Widget config error: {e}")
        return False

def test_main_app_imports():
    """Test that main app can import MD3 components"""
    try:
        # Test the imports used in main.py
        from ui.material_design import (
            apply_md3_theme, get_theme, create_md3_widget_config, 
            switch_theme, register_global_theme_callback, create_smooth_theme_switcher
        )
        from ui.enhanced_components import (
            MD3ScrolledText, MD3Button, MD3Entry, MD3Frame, 
            MD3StatusIndicator, MD3Card, create_md3_tooltip, animate_widget_transition
        )
        print("✓ Main app MD3 imports working")
        return True
    except ImportError as e:
        print(f"✗ Main app import error: {e}")
        return False

def run_all_tests():
    """Run all validation tests"""
    tests = [
        ("MD3 Imports", test_md3_imports),
        ("Theme System", test_theme_system),
        ("Color Schemes", test_color_schemes),
        ("Typography System", test_typography_system),
        ("Widget Configs", test_widget_configs),
        ("Main App Imports", test_main_app_imports)
    ]
    
    passed = 0
    total = len(tests)
    
    print("Material Design 3 Interface Validation")
    print("=" * 50)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED: {e}")
    
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All MD3 interface validation tests passed!")
        return True
    else:
        print("❌ Some MD3 interface validation tests failed!")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)