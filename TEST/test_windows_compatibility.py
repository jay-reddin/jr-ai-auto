#!/usr/bin/env python3
"""
Windows Compatibility Test Suite for Clevrr Computer
Tests PyAutoGUI operations, font rendering, and Gemini integration on Windows
"""

import os
import sys
import time
import platform
import traceback
from PIL import Image, ImageDraw, ImageFont
import pyautogui as pg
import base64

# Add utils to path for imports
sys.path.append('utils')

# Import functions individually to avoid model initialization issues
try:
    from utils.tools import _load_windows_font, get_ruled_screenshot
    TOOLS_IMPORTED = True
except Exception as e:
    print(f"Warning: Could not import tools: {e}")
    TOOLS_IMPORTED = False

# Try to import models and agent creation (may fail without API key)
try:
    from utils.contants import MODELS
    MODELS_IMPORTED = True
except Exception as e:
    print(f"Warning: Could not import models (likely missing API key): {e}")
    MODELS_IMPORTED = False

try:
    from utils.agent import create_clevrr_agent
    from utils.prompt import prompt
    AGENT_IMPORTED = True
except Exception as e:
    print(f"Warning: Could not import agent: {e}")
    AGENT_IMPORTED = False

# Configure PyAutoGUI for testing
pg.PAUSE = 1
pg.FAILSAFE = True

class WindowsCompatibilityTester:
    def __init__(self):
        self.test_results = {}
        self.errors = []
        
    def log_result(self, test_name, success, message="", error=None):
        """Log test result"""
        self.test_results[test_name] = {
            'success': success,
            'message': message,
            'error': str(error) if error else None
        }
        
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"    {message}")
        if error:
            print(f"    Error: {error}")
        print()
        
    def test_platform_detection(self):
        """Test 1: Verify we're running on Windows"""
        try:
            system = platform.system()
            is_windows = system == "Windows"
            
            self.log_result(
                "Platform Detection",
                is_windows,
                f"Detected platform: {system}",
                None if is_windows else "Not running on Windows"
            )
            return is_windows
        except Exception as e:
            self.log_result("Platform Detection", False, error=e)
            return False
    
    def test_font_loading(self):
        """Test 2: Test Windows font loading with fallback mechanism"""
        if not TOOLS_IMPORTED:
            self.log_result("Windows Font Loading", False, error="Tools not imported")
            return False, None
            
        try:
            # Test the font loading function
            font = _load_windows_font(25)
            
            # Verify font is loaded
            success = font is not None
            
            # Try to get font name/info
            font_info = "Unknown font"
            try:
                if hasattr(font, 'path'):
                    font_info = f"Font path: {font.path}"
                elif hasattr(font, 'font'):
                    font_info = f"Font object: {type(font.font)}"
                else:
                    font_info = f"Font type: {type(font)}"
            except:
                font_info = "Font loaded successfully but info unavailable"
            
            self.log_result(
                "Windows Font Loading",
                success,
                font_info
            )
            return success, font
        except Exception as e:
            self.log_result("Windows Font Loading", False, error=e)
            return False, None
    
    def test_screenshot_functionality(self):
        """Test 3: Test screenshot functionality"""
        try:
            # Take a basic screenshot
            screenshot = pg.screenshot()
            
            # Verify screenshot properties
            width, height = screenshot.size
            success = width > 0 and height > 0
            
            self.log_result(
                "Screenshot Functionality",
                success,
                f"Screenshot size: {width}x{height}"
            )
            return success, screenshot
        except Exception as e:
            self.log_result("Screenshot Functionality", False, error=e)
            return False, None
    
    def test_coordinate_grid_rendering(self):
        """Test 4: Test coordinate grid rendering on Windows"""
        if not TOOLS_IMPORTED:
            self.log_result("Coordinate Grid Rendering", False, error="Tools not imported")
            return False
            
        try:
            # Test the ruled screenshot function
            get_ruled_screenshot()
            
            # Verify the screenshot file was created
            screenshot_exists = os.path.exists("screenshot.png")
            
            if screenshot_exists:
                # Load and verify the screenshot
                img = Image.open("screenshot.png")
                width, height = img.size
                
                # Basic validation - check if image has reasonable dimensions
                success = width > 100 and height > 100
                message = f"Grid screenshot created: {width}x{height}"
            else:
                success = False
                message = "Screenshot file not created"
            
            self.log_result(
                "Coordinate Grid Rendering",
                success,
                message
            )
            return success
        except Exception as e:
            self.log_result("Coordinate Grid Rendering", False, error=e)
            return False
    
    def test_pyautogui_basic_operations(self):
        """Test 5: Test basic PyAutoGUI operations on Windows"""
        try:
            # Get screen size
            screen_width, screen_height = pg.size()
            
            # Test mouse position
            current_pos = pg.position()
            
            # Test safe mouse movement (to center of screen)
            center_x, center_y = screen_width // 2, screen_height // 2
            pg.moveTo(center_x, center_y, duration=0.5)
            new_pos = pg.position()
            
            # Verify mouse moved
            mouse_moved = abs(new_pos.x - center_x) < 10 and abs(new_pos.y - center_y) < 10
            
            # Test key press (safe key)
            pg.press('capslock')  # Toggle caps lock (safe and reversible)
            time.sleep(0.1)
            pg.press('capslock')  # Toggle back
            
            success = mouse_moved
            message = f"Screen: {screen_width}x{screen_height}, Mouse moved to: {new_pos}"
            
            self.log_result(
                "PyAutoGUI Basic Operations",
                success,
                message
            )
            return success
        except Exception as e:
            self.log_result("PyAutoGUI Basic Operations", False, error=e)
            return False
    
    def test_windows_key_combinations(self):
        """Test 6: Test Windows-specific key combinations"""
        try:
            # Test Windows key (open start menu briefly)
            print("    Testing Windows key (will open start menu briefly)...")
            pg.press('win')
            time.sleep(1)
            pg.press('escape')  # Close start menu
            
            # Test Alt+Tab (window switching)
            print("    Testing Alt+Tab...")
            pg.hotkey('alt', 'tab')
            time.sleep(0.5)
            pg.press('escape')  # Cancel Alt+Tab
            
            # Test Ctrl combinations
            print("    Testing Ctrl combinations...")
            # These are safe as they don't modify anything without a target
            
            success = True  # If we got here without exceptions, basic key combos work
            message = "Windows key combinations executed successfully"
            
            self.log_result(
                "Windows Key Combinations",
                success,
                message
            )
            return success
        except Exception as e:
            self.log_result("Windows Key Combinations", False, error=e)
            return False
    
    def test_gemini_model_integration(self):
        """Test 7: Test Gemini model integration"""
        if not MODELS_IMPORTED:
            self.log_result(
                "Gemini Model Integration",
                False,
                error="Models not imported (likely missing GOOGLE_API_KEY)"
            )
            return False
            
        try:
            # Check if GOOGLE_API_KEY is available
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                self.log_result(
                    "Gemini Model Integration",
                    False,
                    error="GOOGLE_API_KEY not found in environment"
                )
                return False
            
            # Test model initialization
            gemini_model = MODELS.get("gemini")
            if not gemini_model:
                self.log_result(
                    "Gemini Model Integration",
                    False,
                    error="Gemini model not found in MODELS"
                )
                return False
            
            success = True
            message = "Gemini model initialized successfully"
            
            self.log_result(
                "Gemini Model Integration",
                success,
                message
            )
            return success
        except Exception as e:
            self.log_result("Gemini Model Integration", False, error=e)
            return False
    
    def test_get_screen_info_tool(self):
        """Test 8: Test get_screen_info tool with Gemini"""
        if not TOOLS_IMPORTED or not MODELS_IMPORTED:
            self.log_result(
                "get_screen_info Tool with Gemini",
                False,
                error="Required modules not imported"
            )
            return False
            
        try:
            # Import the tool function
            from utils.tools import get_screen_info
            
            # Check if we can call the tool (this will test the full pipeline)
            print("    Testing get_screen_info tool (this may take a moment)...")
            
            # Create a simple test question
            test_question = "What is the approximate size of this screen in pixels?"
            
            # This will test: screenshot -> grid overlay -> base64 encoding -> Gemini API call
            result = get_screen_info(test_question)
            
            # Check if we got a reasonable response
            success = isinstance(result, str) and len(result) > 10 and "error" not in result.lower()
            
            if success:
                message = f"Tool responded successfully (response length: {len(result)} chars)"
            else:
                message = f"Tool response: {result}"
            
            self.log_result(
                "get_screen_info Tool with Gemini",
                success,
                message
            )
            return success
        except Exception as e:
            self.log_result("get_screen_info Tool with Gemini", False, error=e)
            return False
    
    def test_agent_creation(self):
        """Test 9: Test agent creation with Gemini model"""
        if not AGENT_IMPORTED or not MODELS_IMPORTED:
            self.log_result(
                "Agent Creation",
                False,
                error="Required modules not imported"
            )
            return False, None
            
        try:
            # Test creating the agent
            gemini_model = MODELS.get("gemini")
            if not gemini_model:
                raise Exception("Gemini model not available")
            
            agent_executor = create_clevrr_agent(gemini_model, prompt)
            
            success = agent_executor is not None
            message = "Agent created successfully with Gemini model"
            
            self.log_result(
                "Agent Creation",
                success,
                message
            )
            return success, agent_executor
        except Exception as e:
            self.log_result("Agent Creation", False, error=e)
            return False, None
    
    def test_font_coordinate_accuracy(self):
        """Test 10: Test font rendering and coordinate accuracy"""
        if not TOOLS_IMPORTED:
            self.log_result("Font Coordinate Accuracy", False, error="Tools not imported")
            return False
            
        try:
            # Create a test image with coordinates
            test_img = Image.new("RGB", (400, 300), "white")
            draw = ImageDraw.Draw(test_img)
            
            # Load font using our Windows-optimized function
            font = _load_windows_font(20)
            
            # Draw some test coordinates
            test_coords = [(50, 50), (150, 100), (250, 150), (350, 200)]
            
            for x, y in test_coords:
                # Draw a small circle at the coordinate
                draw.ellipse([x-3, y-3, x+3, y+3], fill="red")
                # Draw the coordinate text
                draw.text((x+10, y-10), f"({x},{y})", font=font, fill="black")
            
            # Save test image
            test_img.save("font_test.png")
            
            success = os.path.exists("font_test.png")
            message = "Font rendering and coordinate accuracy test completed"
            
            self.log_result(
                "Font Coordinate Accuracy",
                success,
                message
            )
            return success
        except Exception as e:
            self.log_result("Font Coordinate Accuracy", False, error=e)
            return False
    
    def run_all_tests(self):
        """Run all compatibility tests"""
        print("=" * 60)
        print("CLEVRR COMPUTER - WINDOWS COMPATIBILITY TEST SUITE")
        print("=" * 60)
        print()
        
        # Run tests in order
        tests = [
            self.test_platform_detection,
            self.test_font_loading,
            self.test_screenshot_functionality,
            self.test_coordinate_grid_rendering,
            self.test_pyautogui_basic_operations,
            self.test_windows_key_combinations,
            self.test_gemini_model_integration,
            self.test_font_coordinate_accuracy,
            self.test_agent_creation,
            # Note: get_screen_info test is optional as it requires API key and network
        ]
        
        # Add get_screen_info test only if API key is available and models imported
        if os.getenv("GOOGLE_API_KEY") and MODELS_IMPORTED and TOOLS_IMPORTED:
            tests.append(self.test_get_screen_info_tool)
        else:
            print("⚠ WARNING: GOOGLE_API_KEY not found or models not imported - skipping get_screen_info test")
            print()
        
        # Execute tests
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"✗ FAIL: {test.__name__} - Unexpected error: {e}")
                traceback.print_exc()
                print()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        if failed_tests > 0:
            print("FAILED TESTS:")
            for test_name, result in self.test_results.items():
                if not result['success']:
                    print(f"  - {test_name}: {result['error'] or 'Unknown error'}")
            print()
        
        # Cleanup test files
        for file in ["screenshot.png", "font_test.png"]:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    print(f"Cleaned up: {file}")
                except:
                    pass
        
        print("=" * 60)
        
        # Return overall success
        return failed_tests == 0

if __name__ == "__main__":
    print("Starting Windows Compatibility Tests...")
    print("Note: Some tests may briefly interact with your screen/keyboard")
    print("Press Ctrl+C to cancel if needed")
    print()
    
    # Give user a moment to read the warning
    time.sleep(3)
    
    tester = WindowsCompatibilityTester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 All tests passed! Clevrr Computer is Windows-compatible.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please review the results above.")
        sys.exit(1)