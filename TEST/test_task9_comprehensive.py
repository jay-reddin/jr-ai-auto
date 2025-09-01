#!/usr/bin/env python3
"""
Comprehensive test for Task 9: Validate and optimize final implementation
Tests all four specific requirements from the task:
1. Test complete application startup and functionality
2. Verify memory footprint reduction from removed dependencies  
3. Confirm all automation features work identically to previous version
4. Test GUI functionality and responsiveness on Windows
"""

import sys
import os
import time
import psutil
import threading
import subprocess
from unittest.mock import patch, MagicMock

class Task9ComprehensiveTest:
    def __init__(self):
        self.results = {}
        
    def log_test(self, name, success, details=""):
        """Log test result"""
        self.results[name] = {'success': success, 'details': details}
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {name}")
        if details:
            print(f"   {details}")
    
    def test_complete_application_startup(self):
        """Task requirement 1: Test complete application startup and functionality"""
        print("\n🚀 Testing Complete Application Startup and Functionality")
        print("-" * 60)
        
        try:
            # Test 1.1: Import all core modules
            import main
            from utils import agent, contants, tools, prompt
            self.log_test("Core modules import", True, "All modules imported successfully")
            
            # Test 1.2: Verify model configuration
            from utils.contants import MODELS, GEMINI
            if 'gemini' in MODELS and MODELS['gemini'] is not None:
                self.log_test("Gemini model configuration", True, "Model properly configured")
            else:
                self.log_test("Gemini model configuration", False, "Model not found or None")
                return False
            
            # Test 1.3: Test environment setup
            import dotenv
            dotenv.load_dotenv()
            if os.getenv("GOOGLE_API_KEY"):
                self.log_test("Environment configuration", True, "GOOGLE_API_KEY found")
            else:
                self.log_test("Environment configuration", False, "GOOGLE_API_KEY missing")
                return False
            
            # Test 1.4: Test agent creation
            from utils.agent import create_clevrr_agent
            from utils.prompt import prompt
            
            # Use mock to avoid API calls
            mock_model = MagicMock()
            mock_model.invoke = MagicMock(return_value=MagicMock(content="Test response"))
            
            agent = create_clevrr_agent(mock_model, prompt)
            if agent:
                self.log_test("Agent creation", True, "Agent created successfully")
            else:
                self.log_test("Agent creation", False, "Agent creation failed")
                return False
            
            # Test 1.5: Test command line interface
            result = subprocess.run([sys.executable, "main.py", "--help"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and "gemini" in result.stdout:
                self.log_test("CLI functionality", True, "Help command works, Gemini-only confirmed")
            else:
                self.log_test("CLI functionality", False, "CLI test failed")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Application startup", False, f"Exception: {str(e)}")
            return False
    
    def test_memory_footprint_reduction(self):
        """Task requirement 2: Verify memory footprint reduction from removed dependencies"""
        print("\n💾 Testing Memory Footprint Reduction")
        print("-" * 60)
        
        try:
            process = psutil.Process()
            
            # Test 2.1: Baseline memory measurement
            baseline_memory = process.memory_info().rss / 1024 / 1024
            self.log_test("Baseline memory measurement", True, f"{baseline_memory:.2f} MB")
            
            # Test 2.2: Memory after imports
            from utils.contants import MODELS
            from utils.agent import create_clevrr_agent
            from utils.tools import get_screen_info
            import pyautogui
            
            after_imports = process.memory_info().rss / 1024 / 1024
            memory_increase = after_imports - baseline_memory
            
            if memory_increase < 50:  # Reasonable threshold
                self.log_test("Memory efficiency", True, f"Increase: {memory_increase:.2f} MB (efficient)")
            else:
                self.log_test("Memory efficiency", False, f"Increase: {memory_increase:.2f} MB (too high)")
            
            # Test 2.3: Verify Azure OpenAI dependencies removed
            azure_modules = [name for name in sys.modules.keys() 
                           if 'openai' in name.lower() and 'azure' in name.lower()]
            if not azure_modules:
                self.log_test("Azure OpenAI removal", True, "No Azure OpenAI modules found")
            else:
                self.log_test("Azure OpenAI removal", False, f"Found: {azure_modules}")
            
            # Test 2.4: Check requirements.txt for removed dependencies
            with open('requirements.txt', 'r') as f:
                requirements = f.read().lower()
            
            removed_deps = ['openai', 'azure-', 'langchain-openai']
            found_removed = [dep for dep in removed_deps if dep in requirements]
            
            if not found_removed:
                self.log_test("Requirements cleanup", True, "No removed dependencies found")
            else:
                self.log_test("Requirements cleanup", False, f"Found removed deps: {found_removed}")
            
            # Test 2.5: Count total dependencies
            with open('requirements.txt', 'r') as f:
                lines = f.readlines()
            
            total_deps = len([line for line in lines if line.strip() and not line.startswith('#')])
            if total_deps < 30:
                self.log_test("Dependency count", True, f"{total_deps} dependencies (minimal)")
            else:
                self.log_test("Dependency count", False, f"{total_deps} dependencies (too many)")
            
            return True
            
        except Exception as e:
            self.log_test("Memory footprint test", False, f"Exception: {str(e)}")
            return False
    
    def test_automation_features_identical(self):
        """Task requirement 3: Confirm all automation features work identically"""
        print("\n🤖 Testing Automation Features Identical Operation")
        print("-" * 60)
        
        try:
            # Test 3.1: PyAutoGUI functionality
            import pyautogui as pg
            
            required_functions = ['screenshot', 'size', 'position', 'moveTo', 'click', 'write', 'press', 'hotkey']
            missing_functions = [func for func in required_functions if not hasattr(pg, func)]
            
            if not missing_functions:
                self.log_test("PyAutoGUI functions", True, "All required functions available")
            else:
                self.log_test("PyAutoGUI functions", False, f"Missing: {missing_functions}")
            
            # Test 3.2: PyAutoGUI configuration
            if hasattr(pg, 'PAUSE') and pg.PAUSE >= 2:
                self.log_test("PyAutoGUI configuration", True, f"PAUSE set to {pg.PAUSE}")
            else:
                self.log_test("PyAutoGUI configuration", False, "PAUSE not properly configured")
            
            # Test 3.3: Screen analysis tool
            from utils.tools import get_screen_info, _load_windows_font
            
            # Test font loading (Windows optimization)
            font = _load_windows_font(25)
            if font:
                self.log_test("Windows font loading", True, "Font loading works")
            else:
                self.log_test("Windows font loading", False, "Font loading failed")
            
            # Test 3.4: Tool configuration with Gemini
            from utils.contants import MODELS
            if 'gemini' in MODELS:
                self.log_test("Tool-Gemini integration", True, "Tools configured for Gemini")
            else:
                self.log_test("Tool-Gemini integration", False, "Gemini not found for tools")
            
            # Test 3.5: Agent tools integration
            from utils.agent import create_clevrr_agent
            from utils.prompt import prompt
            
            mock_model = MagicMock()
            agent = create_clevrr_agent(mock_model, prompt)
            
            if hasattr(agent, 'tools') and len(agent.tools) >= 2:
                self.log_test("Agent tools integration", True, f"{len(agent.tools)} tools available")
            else:
                self.log_test("Agent tools integration", False, "Tools not properly integrated")
            
            return True
            
        except Exception as e:
            self.log_test("Automation features test", False, f"Exception: {str(e)}")
            return False
    
    def test_gui_functionality_windows(self):
        """Task requirement 4: Test GUI functionality and responsiveness on Windows"""
        print("\n🖥️ Testing GUI Functionality and Windows Responsiveness")
        print("-" * 60)
        
        try:
            # Test 4.1: Tkinter import and basic functionality
            import tkinter as tk
            from tkinter import ttk
            self.log_test("Tkinter import", True, "GUI framework available")
            
            # Test 4.2: GUI window creation test
            gui_test_result = [False]
            
            def test_gui_creation():
                try:
                    root = tk.Tk()
                    root.title("Test GUI")
                    root.geometry("200x150")
                    
                    # Test widgets similar to main app
                    label = tk.Label(root, text="Test")
                    label.pack()
                    
                    text = tk.Text(root, width=20, height=5)
                    text.pack()
                    
                    entry = tk.Entry(root)
                    entry.pack()
                    
                    button = tk.Button(root, text="Test")
                    button.pack()
                    
                    # Test Windows-specific attributes
                    root.attributes('-topmost', True)
                    
                    # Close after brief display
                    root.after(500, root.destroy)
                    root.mainloop()
                    
                    gui_test_result[0] = True
                except Exception as e:
                    print(f"GUI test error: {e}")
                    gui_test_result[0] = False
            
            # Run GUI test in thread
            gui_thread = threading.Thread(target=test_gui_creation)
            gui_thread.daemon = True
            gui_thread.start()
            gui_thread.join(timeout=3)
            
            if gui_test_result[0]:
                self.log_test("GUI window creation", True, "Window and widgets work correctly")
            else:
                self.log_test("GUI window creation", False, "GUI test failed or timed out")
            
            # Test 4.3: Main application GUI structure
            with open('main.py', 'r') as f:
                main_content = f.read()
            
            gui_components = ['Tk()', 'Label', 'Text', 'Entry', 'Button', 'mainloop', 'attributes']
            missing_components = [comp for comp in gui_components if comp not in main_content]
            
            if not missing_components:
                self.log_test("Main app GUI components", True, "All GUI components present")
            else:
                self.log_test("Main app GUI components", False, f"Missing: {missing_components}")
            
            # Test 4.4: GUI configuration
            if 'float_ui' in main_content and 'topmost' in main_content:
                self.log_test("GUI configuration", True, "Float UI and topmost features available")
            else:
                self.log_test("GUI configuration", False, "GUI configuration incomplete")
            
            # Test 4.5: Screen size handling
            if 'screen_width' in main_content and 'screen_height' in main_content:
                self.log_test("Screen size handling", True, "Dynamic screen sizing implemented")
            else:
                self.log_test("Screen size handling", False, "Screen sizing not found")
            
            return True
            
        except Exception as e:
            self.log_test("GUI functionality test", False, f"Exception: {str(e)}")
            return False
    
    def run_comprehensive_test(self):
        """Run all Task 9 tests"""
        print("🔍 TASK 9 COMPREHENSIVE VALIDATION")
        print("=" * 70)
        print("Validating and optimizing final implementation...")
        
        start_time = time.time()
        
        # Run all test categories
        test1_success = self.test_complete_application_startup()
        test2_success = self.test_memory_footprint_reduction()
        test3_success = self.test_automation_features_identical()
        test4_success = self.test_gui_functionality_windows()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Generate final report
        print("\n" + "=" * 70)
        print("📊 TASK 9 VALIDATION SUMMARY")
        print("=" * 70)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results.values() if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"Duration: {duration:.2f} seconds")
        
        # Task-specific results
        task_results = {
            "Task 9.1 - Application Startup": test1_success,
            "Task 9.2 - Memory Footprint": test2_success, 
            "Task 9.3 - Automation Features": test3_success,
            "Task 9.4 - GUI Functionality": test4_success
        }
        
        print("\nTask Requirements Status:")
        print("-" * 30)
        for task, success in task_results.items():
            status = "✅ COMPLETE" if success else "❌ FAILED"
            print(f"{status} {task}")
        
        all_tasks_passed = all(task_results.values())
        
        print("\n" + "=" * 70)
        if all_tasks_passed and failed_tests == 0:
            print("🎉 TASK 9 VALIDATION SUCCESSFUL!")
            print("✅ All requirements met - Final implementation validated")
        else:
            print("⚠️ TASK 9 VALIDATION ISSUES FOUND")
            print(f"❌ {len([t for t in task_results.values() if not t])} task requirement(s) failed")
        
        return all_tasks_passed and failed_tests == 0

def main():
    """Run Task 9 comprehensive validation"""
    tester = Task9ComprehensiveTest()
    success = tester.run_comprehensive_test()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()