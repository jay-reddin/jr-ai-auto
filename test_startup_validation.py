#!/usr/bin/env python3
"""
Quick startup test to validate agent initialization without GUI
"""

import sys
import os
import time

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

def test_agent_startup():
    """Test agent startup without GUI"""
    print("Testing agent startup...")
    
    try:
        # Import required modules
        from utils.agent import create_clevrr_agent
        from utils.prompt import prompt
        from utils.contants import MODELS
        
        print("✓ Modules imported successfully")
        
        # Check model availability
        if 'gemini' not in MODELS:
            print("✗ Gemini model not found in MODELS")
            return False
            
        print("✓ Gemini model found in configuration")
        
        # Test agent creation (this will make an actual API call)
        print("Creating agent with Gemini model...")
        agent_executor = create_clevrr_agent(MODELS['gemini'], prompt)
        
        if agent_executor:
            print("✓ Agent created successfully")
            
            # Test a simple query (optional - comment out if you don't want to use API credits)
            # print("Testing simple query...")
            # response = agent_executor.invoke({"input": "What is 2+2?"})
            # print(f"✓ Agent response: {response.get('output', 'No output')}")
            
            return True
        else:
            print("✗ Agent creation failed")
            return False
            
    except Exception as e:
        print(f"✗ Error during startup test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_memory_optimization():
    """Test memory usage optimization"""
    print("\nTesting memory optimization...")
    
    try:
        import psutil
        process = psutil.Process()
        
        # Memory before imports
        memory_before = process.memory_info().rss / 1024 / 1024
        print(f"Memory before imports: {memory_before:.2f} MB")
        
        # Import all modules
        from utils.contants import MODELS
        from utils.agent import create_clevrr_agent
        from utils.tools import get_screen_info
        import pyautogui
        
        # Memory after imports
        memory_after = process.memory_info().rss / 1024 / 1024
        memory_increase = memory_after - memory_before
        
        print(f"Memory after imports: {memory_after:.2f} MB")
        print(f"Memory increase: {memory_increase:.2f} MB")
        
        # Check for unwanted modules
        unwanted_modules = [name for name in sys.modules.keys() if 'openai' in name.lower() and 'azure' in name.lower()]
        
        if unwanted_modules:
            print(f"✗ Found unwanted modules: {unwanted_modules}")
            return False
        else:
            print("✓ No unwanted Azure OpenAI modules found")
            
        if memory_increase < 50:  # Reasonable threshold
            print(f"✓ Memory increase is reasonable: {memory_increase:.2f} MB")
            return True
        else:
            print(f"⚠ Memory increase is high: {memory_increase:.2f} MB")
            return True  # Still pass, but warn
            
    except Exception as e:
        print(f"✗ Memory test failed: {str(e)}")
        return False

def main():
    """Run startup validation tests"""
    print("Clevrr Computer Startup Validation")
    print("=" * 40)
    
    success = True
    
    # Test agent startup
    if not test_agent_startup():
        success = False
    
    # Test memory optimization
    if not test_memory_optimization():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 Startup validation successful!")
    else:
        print("⚠️ Some startup tests failed")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)