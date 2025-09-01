#!/usr/bin/env python3
"""
Test imports for JR AI Control
"""

try:
    print("Testing imports...")
    
    # Test basic imports
    import tkinter as tk
    print("✓ tkinter imported")
    
    import uuid
    print("✓ uuid imported")
    
    # Test our custom modules
    from utils.token_tracker import get_token_tracker
    print("✓ token_tracker imported")
    
    from ui.material_design import apply_md3_theme, get_theme
    print("✓ material_design imported")
    
    from utils.agent import create_jr_ai_agent
    print("✓ agent imported")
    
    from utils.contants import MODELS
    print("✓ contants imported")
    
    print("\n🎉 All imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()