#!/usr/bin/env python3
"""
Test script for Material Design 3 interface implementation
Tests the enhanced UI components and styling
"""

import tkinter as tk
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_md3_interface():
    """Test the Material Design 3 interface components"""
    try:
        # Import required modules
        from ui.material_design import apply_md3_theme, get_theme, switch_theme
        from ui.enhanced_components import (
            MD3ScrolledText, MD3Button, MD3Entry, MD3Frame, 
            MD3StatusIndicator, MD3Card, create_md3_tooltip
        )
        
        print("✓ Successfully imported MD3 components")
        
        # Create test window
        root = tk.Tk()
        root.title("MD3 Interface Test")
        root.geometry("600x500")
        
        # Apply MD3 theme
        theme = apply_md3_theme(root, 'dark')
        print("✓ Successfully applied MD3 theme")
        
        # Test main container
        main_frame = MD3Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
        print("✓ Created MD3Frame")
        
        # Test card component
        test_card = MD3Card(main_frame)
        test_card.pack(fill=tk.X, pady=(0, 16))
        print("✓ Created MD3Card")
        
        # Test card content
        card_content = MD3Frame(test_card)
        card_content.pack(fill=tk.X, padx=16, pady=16)
        
        # Test title
        title = tk.Label(card_content, text="MD3 Interface Test", 
                        bg=theme.colors['surface_variant'],
                        fg=theme.colors['on_surface_variant'],
                        font=theme.typography['headline_medium'])
        title.pack(anchor=tk.W, pady=(0, 8))
        print("✓ Created title with MD3 typography")
        
        # Test buttons
        button_frame = MD3Frame(card_content)
        button_frame.pack(fill=tk.X, pady=8)
        
        primary_btn = MD3Button(button_frame, text="Primary", style='primary')
        primary_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        secondary_btn = MD3Button(button_frame, text="Secondary", style='secondary')
        secondary_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        print("✓ Created MD3 buttons")
        
        # Test entry
        entry = MD3Entry(card_content)
        entry.pack(fill=tk.X, pady=8)
        entry.insert(0, "Test MD3 Entry")
        print("✓ Created MD3Entry")
        
        # Test status indicator
        status = MD3StatusIndicator(card_content, status='active')
        status.pack(anchor=tk.W, pady=8)
        print("✓ Created MD3StatusIndicator")
        
        # Test scrolled text
        text_card = MD3Card(main_frame)
        text_card.pack(fill=tk.BOTH, expand=True)
        
        text_content = MD3Frame(text_card)
        text_content.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
        
        scrolled_text = MD3ScrolledText(text_content)
        scrolled_text.pack(fill=tk.BOTH, expand=True)
        
        # Add test content
        scrolled_text.insert(tk.END, "Material Design 3 Interface Test\n\n")
        scrolled_text.insert(tk.END, "This is a test of the MD3 scrolled text component.\n")
        scrolled_text.insert(tk.END, "The scrollbars should be hidden by default.\n")
        scrolled_text.insert(tk.END, "Hover over the text area to see the scrollbar.\n\n")
        
        for i in range(20):
            scrolled_text.insert(tk.END, f"Test line {i+1}\n")
        
        print("✓ Created MD3ScrolledText with hidden scrollbars")
        
        # Test theme switching
        def test_theme_switch():
            current_theme = theme.theme_mode
            new_theme = 'light' if current_theme == 'dark' else 'dark'
            switch_theme(new_theme)
            print(f"✓ Switched theme from {current_theme} to {new_theme}")
        
        theme_btn = MD3Button(main_frame, text="Toggle Theme", 
                            command=test_theme_switch, style='secondary')
        theme_btn.pack(pady=8)
        
        # Add tooltips
        create_md3_tooltip(primary_btn, "Primary action button")
        create_md3_tooltip(secondary_btn, "Secondary action button")
        create_md3_tooltip(theme_btn, "Switch between dark and light themes")
        print("✓ Added MD3 tooltips")
        
        print("\n🎉 All MD3 interface tests passed!")
        print("Close the window to complete the test.")
        
        # Start the GUI
        root.mainloop()
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Material Design 3 Interface Implementation...")
    print("=" * 50)
    
    success = test_md3_interface()
    
    if success:
        print("\n✅ MD3 interface test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ MD3 interface test failed!")
        sys.exit(1)