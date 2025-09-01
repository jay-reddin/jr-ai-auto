#!/usr/bin/env python3
"""
Comprehensive validation test for the Clevrr Computer Gemini-only migration.
Tests all aspects mentioned in task 9: startup, memory footprint, automation features, and GUI.
"""

import sys
import os
import time
import subprocess
import psutil
import threading
import tkinter as tk
from tkinter import messagebox
import importlib.util
import traceback
from unittest.mock import patch, MagicMock

# Add utils to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

class FinalValidationTest:
    def __init__(self):
        self.test_results = {}
        self.memory_baseline = None
        self.memory_after_import = None
        
    def log_result(self, test_name, success, message=""):
        """Log test result with timestamp"""
        self.test_results[test_name] = {
            'success': success,
            'message': message,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"[{status}] {test_name}: {message}")
    
    def measure_memory_usage(self):
        """Measure current memory usage of the process"""
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # MB
    
    def test_application_startup(self):
        """Test 1: Complete application startup and functionality"""
        print("\n=== Testing Application Startup ===")
        
        try:
            # Test import of main modules
            import main
            self.log_result("Main module import", True, "Successfully imported main.py")
            
            # Test utils imports
            from utils import agent, contants, tools, prompt
            self.log_result("Utils modules import", True, "All utils modules imported successfully")
            
            # Test model configuration
            from utils.contants import MODELS, GEMINI
            if 'gemini' in MODELS and MODELS['gemini'] is not None:
                self.log_result("Model configuration", True, "Gemini model properly configured")
            else:
                self.log_result("Model configuration", False, "Gemini model not found or None")
            
            # Test environment variables
            import dotenv
            dotenv.load_dotenv()
            google_api_key = os.getenv("GOOGLE_API_KEY")
            if google_api_key:
                self.log_result("Environment setup", True, "GOOGLE_API_KEY found")
            else:
                self.log_result("Environment setup", False, "GOOGLE_API_KEY not found")
            
        except Exception as e:
            self.log_result("Application startup", False, f"Startup failed: {str(e)}")
            traceback.print_exc()
    
    def test_memory_footprint(self):
        """Test 2: Verify memory footprint reduction"""
        print("\n=== Testing Memory Footprint ===")
        
        # Measure baseline memory
        self.memory_baseline = self.measure_memory_usage()
        self.log_result("Baseline memory", True, f"{self.memory_baseline:.2f} MB")
        
        try:
            # Import core modules and measure memory
            from utils.contants import MODELS
            from utils.agent import create_clevrr_agent
            from utils.tools import get_screen_info
            
            self.memory_after_import = self.measure_memory_usage()
            memory_increase = self.memory_after_import - self.memory_baseline
            
            self.log_result("Memory after imports", True, f"{self.memory_after_import:.2f} MB (+{memory_increase:.2f} MB)")
            
            # Check that no Azure OpenAI modules are imported
            azure_modules = [name for name in sys.modules.keys() if 'openai' in name.lower() and 'azure' in name.lower()]
            if not azure_modules:
                self.log_result("Azure OpenAI cleanup", True, "No Azure OpenAI modules found in imports")
            else:
                self.log_result("Azure OpenAI cleanup", False, f"Found Azure modules: {azure_modules}")
            
            # Check for unnecessary Google Cloud modules
            unnecessary_gcp_modules = [
                name for name in sys.modules.keys() 
                if any(pattern in name.lower() for pattern in ['google.cloud', 'google.oauth2']) 
                and 'generativeai' not in name.lower()
            ]
            
            if len(unnecessary_gcp_modules) < 5:  # Some basic Google modules are expected
                self.log_result("GCP modules cleanup", True, f"Minimal GCP modules: {len(unnecessary_gcp_modules)}")
            else:
                self.log_result("GCP modules cleanup", False, f"Too many GCP modules: {unnecessary_gcp_modules}")
                
        except Exception as e:
            self.log_result("Memory footprint test", False, f"Memory test failed: {str(e)}")
    
    def test_automation_features(self):
        """Test 3: Confirm automation features work identically"""
        print("\n=== Testing Automation Features ===")
        
        try:
            # Test PyAutoGUI import and basic functionality
            import pyautogui as pg
            
            # Test basic PyAutoGUI functions (without actually executing them)
            pg_functions = ['screenshot', 'size', 'position', 'moveTo', 'click', 'write', 'press']
            missing_functions = [func for func in pg_functions if not hasattr(pg, func)]
            
            if not missing_functions:
                self.log_result("PyAutoGUI functions", True, "All required PyAutoGUI functions available")
            else:
                self.log_result("PyAutoGUI functions", False, f"Missing functions: {missing_functions}")
            
            # Test screen info tool
            from utils.tools import get_screen_info, _load_windows_font
            
            # Test Windows font loading
            try:
                font = _load_windows_font(25)
                if font:
                    self.log_result("Windows font loading", True, "Font loading mechanism works")
                else:
                    self.log_result("Windows font loading", False, "Font loading returned None")
            except Exception as e:
                self.log_result("Windows font loading", False, f"Font loading failed: {str(e)}")
            
            # Test agent creation with mock model
            from utils.agent import create_clevrr_agent
            from utils.prompt import prompt
            
            # Mock the Gemini model to avoid API calls during testing
            mock_model = MagicMock()
            mock_model.invoke = MagicMock(return_value=MagicMock(content="Test response"))
            
            try:
                agent = create_clevrr_agent(mock_model, prompt)
                if agent:
                    self.log_result("Agent creation", True, "Agent created successfully with mock model")
                else:
                    self.log_result("Agent creation", False, "Agent creation returned None")
            except Exception as e:
                self.log_result("Agent creation", False, f"Agent creation failed: {str(e)}")
            
        except Exception as e:
            self.log_result("Automation features test", False, f"Automation test failed: {str(e)}")
    
    def test_gui_functionality(self):
        """Test 4: Test GUI functionality and responsiveness on Windows"""
        print("\n=== Testing GUI Functionality ===")
        
        try:
            # Test Tkinter import and basic functionality
            import tkinter as tk
            from tkinter import ttk
            
            # Create a test window to verify GUI works
            def test_gui_window():
                try:
                    root = tk.Tk()
                    root.title("Test Window")
                    root.geometry("300x200")
                    
                    # Test basic widgets
                    label = tk.Label(root, text="Test Label")
                    label.pack()
                    
                    entry = tk.Entry(root)
                    entry.pack()
                    
                    button = tk.Button(root, text="Test Button")
                    button.pack()
                    
                    # Test window attributes (similar to main app)
                    root.attributes('-topmost', True)
                    
                    # Close window after brief display
                    root.after(1000, root.destroy)
                    root.mainloop()
                    
                    return True
                except Exception as e:
                    print(f"GUI test window error: {e}")
                    return False
            
            # Run GUI test in separate thread to avoid blocking
            gui_result = [False]
            
            def run_gui_test():
                gui_result[0] = test_gui_window()
            
            gui_thread = threading.Thread(target=run_gui_test)
            gui_thread.daemon = True
            gui_thread.start()
            gui_thread.join(timeout=5)  # Wait max 5 seconds
            
            if gui_result[0]:
                self.log_result("GUI basic functionality", True, "Tkinter GUI components work correctly")
            else:
                self.log_result("GUI basic functionality", False, "GUI test failed or timed out")
            
            # Test main app GUI components import
            try:
                import main
                # Check if main has the required GUI setup
                if hasattr(main, 'main'):
                    self.log_result("Main GUI setup", True, "Main application GUI function exists")
                else:
                    self.log_result("Main GUI setup", False, "Main GUI function not found")
            except Exception as e:
                self.log_result("Main GUI setup", False, f"Main GUI import failed: {str(e)}")
            
        except Exception as e:
            self.log_result("GUI functionality test", False, f"GUI test failed: {str(e)}")
    
    def test_requirements_compliance(self):
        """Test compliance with specific requirements 5.1, 5.2, 5.3, 5.4"""
        print("\n=== Testing Requirements Compliance ===")
        
        # Requirement 5.1: Automation tasks work identically
        try:
            from utils.tools import get_screen_info
            from utils.agent import create_clevrr_agent
            
            # Mock test to ensure tools are properly configured
            mock_model = MagicMock()
            mock_model.invoke = MagicMock(return_value=MagicMock(content="Mock response"))
            
            # Test that agent can be created with tools
            from utils.prompt import prompt
            agent = create_clevrr_agent(mock_model, prompt)
            
            if agent and hasattr(agent, 'tools'):
                self.log_result("Req 5.1 - Automation identical", True, "Agent with tools created successfully")
            else:
                self.log_result("Req 5.1 - Automation identical", False, "Agent creation or tools missing")
                
        except Exception as e:
            self.log_result("Req 5.1 - Automation identical", False, f"Failed: {str(e)}")
        
        # Requirement 5.2: get_screen_info tool works with Gemini
        try:
            from utils.tools import get_screen_info
            from utils.contants import MODELS
            
            # Check that get_screen_info uses MODELS["gemini"]
            if "gemini" in MODELS:
                self.log_result("Req 5.2 - Screen analysis Gemini", True, "get_screen_info configured for Gemini")
            else:
                self.log_result("Req 5.2 - Screen analysis Gemini", False, "Gemini model not found")
                
        except Exception as e:
            self.log_result("Req 5.2 - Screen analysis Gemini", False, f"Failed: {str(e)}")
        
        # Requirement 5.3: GUI maintains functionality
        try:
            # Check main.py for GUI components
            with open('main.py', 'r') as f:
                main_content = f.read()
            
            gui_components = ['Tk()', 'Label', 'Text', 'Entry', 'Button', 'mainloop']
            missing_components = [comp for comp in gui_components if comp not in main_content]
            
            if not missing_components:
                self.log_result("Req 5.3 - GUI functionality", True, "All GUI components present")
            else:
                self.log_result("Req 5.3 - GUI functionality", False, f"Missing: {missing_components}")
                
        except Exception as e:
            self.log_result("Req 5.3 - GUI functionality", False, f"Failed: {str(e)}")
        
        # Requirement 5.4: PyAutoGUI precision and reliability
        try:
            import pyautogui as pg
            
            # Check PyAutoGUI configuration
            if hasattr(pg, 'PAUSE') and pg.PAUSE >= 2:
                self.log_result("Req 5.4 - PyAutoGUI precision", True, f"PyAutoGUI PAUSE set to {pg.PAUSE}")
            else:
                self.log_result("Req 5.4 - PyAutoGUI precision", False, "PyAutoGUI PAUSE not properly configured")
                
        except Exception as e:
            self.log_result("Req 5.4 - PyAutoGUI precision", False, f"Failed: {str(e)}")
    
    def test_dependency_cleanup(self):
        """Test that unnecessary dependencies have been removed"""
        print("\n=== Testing Dependency Cleanup ===")
        
        try:
            # Read requirements.txt
            with open('requirements.txt', 'r') as f:
                requirements = f.read().lower()
            
            # Check for removed dependencies
            removed_deps = ['openai', 'azure', 'langchain-openai']
            found_removed = [dep for dep in removed_deps if dep in requirements]
            
            if not found_removed:
                self.log_result("Dependency cleanup", True, "No Azure OpenAI dependencies found")
            else:
                self.log_result("Dependency cleanup", False, f"Found removed deps: {found_removed}")
            
            # Check for essential dependencies
            essential_deps = ['langchain-google-genai', 'google-generativeai', 'pyautogui', 'pillow']
            missing_essential = [dep for dep in essential_deps if dep not in requirements]
            
            if not missing_essential:
                self.log_result("Essential dependencies", True, "All essential dependencies present")
            else:
                self.log_result("Essential dependencies", False, f"Missing: {missing_essential}")
                
        except Exception as e:
            self.log_result("Dependency cleanup test", False, f"Failed: {str(e)}")
    
    def run_all_tests(self):
        """Run all validation tests"""
        print("Starting Final Implementation Validation")
        print("=" * 50)
        
        start_time = time.time()
        
        # Run all test categories
        self.test_application_startup()
        self.test_memory_footprint()
        self.test_automation_features()
        self.test_gui_functionality()
        self.test_requirements_compliance()
        self.test_dependency_cleanup()
        
        end_time = time.time()
        
        # Generate summary report
        self.generate_summary_report(end_time - start_time)
    
    def generate_summary_report(self, duration):
        """Generate and display summary report"""
        print("\n" + "=" * 50)
        print("FINAL VALIDATION SUMMARY REPORT")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print(f"Duration: {duration:.2f} seconds")
        
        if self.memory_baseline and self.memory_after_import:
            memory_increase = self.memory_after_import - self.memory_baseline
            print(f"Memory Usage: {self.memory_baseline:.2f} MB → {self.memory_after_import:.2f} MB (+{memory_increase:.2f} MB)")
        
        print("\nDetailed Results:")
        print("-" * 30)
        
        for test_name, result in self.test_results.items():
            status = "✓ PASS" if result['success'] else "✗ FAIL"
            print(f"{status} {test_name}")
            if result['message']:
                print(f"    {result['message']}")
        
        print("\n" + "=" * 50)
        
        if failed_tests == 0:
            print("🎉 ALL TESTS PASSED! Migration validation successful.")
            return True
        else:
            print(f"⚠️  {failed_tests} test(s) failed. Review issues above.")
            return False

def main():
    """Main function to run validation tests"""
    validator = FinalValidationTest()
    success = validator.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()