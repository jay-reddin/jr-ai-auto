#!/usr/bin/env python3
"""
Simple test for JR AI Control UI components
"""

try:
    print("Testing basic imports...")
    
    import tkinter as tk
    from tkinter import ttk
    print("✓ tkinter imported")
    
    # Test our UI module
    from ui.material_design import get_theme, create_md3_widget_config
    print("✓ material_design imported")
    
    # Test token tracker
    from utils.token_tracker import get_token_tracker
    print("✓ token_tracker imported")
    
    print("\n🎉 Basic imports successful!")
    
    # Test creating a simple window
    print("\nTesting UI creation...")
    
    root = tk.Tk()
    root.title("JR AI Control - Test")
    
    # Apply theme
    theme = get_theme('dark')
    theme.apply_theme(root)
    
    # Create a simple frame
    frame = tk.Frame(root, **create_md3_widget_config('Frame', theme))
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Add a label
    label = ttk.Label(frame, text="JR AI Control", style='MD3.Headline.Medium.TLabel')
    label.pack(pady=10)
    
    # Add a button
    button = ttk.Button(frame, text="Test Button", style='MD3.Primary.TButton')
    button.pack(pady=10)
    
    print("✓ UI components created successfully")
    
    # Test token tracker
    tracker = get_token_tracker()
    print(f"✓ Token tracker initialized, total tokens: {tracker.get_total_tokens()}")
    
    print("\n🎉 All tests passed! Close the window to continue.")
    
    # Show the window briefly
    root.geometry("400x300")
    root.after(3000, root.destroy)  # Auto-close after 3 seconds
    root.mainloop()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()