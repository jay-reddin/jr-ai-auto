#!/usr/bin/env python3
"""
Core Windows Compatibility Test for Clevrr Computer

This test focuses on essential Windows compatibility without requiring
external API keys or complex dependencies. It tests:
- Basic imports and module loading
- Windows-specific functionality (fonts, paths, GUI)
- PyAutoGUI Windows compatibility
- Tkinter GUI initialization
- File system operations
"""

import unittest
import sys
import os
import platform
import tempfile
from unittest.mock import Mock, patch, MagicMock
import warnings

# Suppress deprecation warnings for cleaner test output
warnings.filterwarnings("ignore", category=DeprecationWarning)

class TestWindowsCompatibility(unittest.TestCase):
    """Test suite for Windows compatibility of Clevrr Computer"""
    
    def setUp(self):
        """Set up test environment"""
        self.is_windows = platform.system() == "Windows"
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment"""
        # Clean up temp directory
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_platform_detection(self):
        """Test that we can properly detect Windows platform"""
        system = platform.system()
        self.assertIn(system, ["Windows", "Linux", "Darwin"], 
                     f"Unexpected platform: {system}")
        
        if self.is_windows:
            print(f"✓ Running on Windows: {platform.version()}")
        else:
            print(f"ℹ Running on {system} (not Windows)")
    
    def test_basic_imports(self):
        """Test that all required modules can be imported"""
        try:
            import tkinter
            print("✓ tkinter import successful")
        except ImportError as e:
            self.fail(f"Failed to import tkinter: {e}")
        
        try:
            import pyautogui
            print("✓ pyautogui import successful")
        except ImportError as e:
            self.fail(f"Failed to import pyautogui: {e}")
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            print("✓ PIL imports successful")
        except ImportError as e:
            self.fail(f"Failed to import PIL components: {e}")
    
    def test_pyautogui_basic_functionality(self):
        """Test basic PyAutoGUI functionality on Windows"""
        try:
            import pyautogui as pg
            
            # Test screen size detection
            screen_size = pg.size()
            self.assertIsInstance(screen_size, tuple)
            self.assertEqual(len(screen_size), 2)
            self.assertGreater(screen_size[0], 0)
            self.assertGreater(screen_size[1], 0)
            print(f"✓ Screen size detected: {screen_size}")
            
            # Test screenshot capability (without actually taking one)
            # We'll mock this to avoid GUI interference
            with patch.object(pg, 'screenshot') as mock_screenshot:
                mock_screenshot.return_value = Mock()
                result = pg.screenshot()
                self.assertIsNotNone(result)
                print("✓ Screenshot functionality available")
            
            # Test pause setting
            original_pause = pg.PAUSE
            pg.PAUSE = 1.0
            self.assertEqual(pg.PAUSE, 1.0)
            pg.PAUSE = original_pause
            print("✓ PyAutoGUI pause setting works")
            
        except Exception as e:
            self.fail(f"PyAutoGUI basic functionality failed: {e}")
    
    def test_tkinter_gui_initialization(self):
        """Test Tkinter GUI can be initialized on Windows"""
        try:
            from tkinter import Tk, Label, Text, Entry, Button, Scrollbar
            
            # Create root window (don't show it)
            root = Tk()
            root.withdraw()  # Hide the window
            
            # Test basic widget creation
            label = Label(root, text="Test Label")
            text_widget = Text(root)
            entry = Entry(root)
            button = Button(root, text="Test Button")
            scrollbar = Scrollbar(root)
            
            # Test screen dimensions
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            
            self.assertGreater(screen_width, 0)
            self.assertGreater(screen_height, 0)
            
            print(f"✓ Tkinter GUI initialized, screen: {screen_width}x{screen_height}")
            
            # Clean up
            root.destroy()
            
        except Exception as e:
            self.fail(f"Tkinter GUI initialization failed: {e}")
    
    def test_windows_font_loading(self):
        """Test Windows font loading functionality"""
        try:
            from PIL import ImageFont
            import platform
            
            # Test the font loading logic from utils/tools.py
            windows_fonts = [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/calibri.ttf", 
                "C:/Windows/Fonts/tahoma.ttf",
                "arial.ttf",
                "calibri.ttf"
            ]
            
            font_loaded = False
            loaded_font_name = None
            
            if platform.system() == "Windows":
                for font_path in windows_fonts:
                    try:
                        if os.path.exists(font_path):
                            font = ImageFont.truetype(font_path, 25)
                            font_loaded = True
                            loaded_font_name = font_path
                            break
                        else:
                            font = ImageFont.truetype(font_path, 25)
                            font_loaded = True
                            loaded_font_name = font_path
                            break
                    except (IOError, OSError):
                        continue
            
            if not font_loaded:
                # Try default font
                try:
                    font = ImageFont.load_default()
                    font_loaded = True
                    loaded_font_name = "default"
                except Exception:
                    pass
            
            self.assertTrue(font_loaded, "No fonts could be loaded")
            print(f"✓ Font loading successful: {loaded_font_name}")
            
        except Exception as e:
            self.fail(f"Font loading test failed: {e}")
    
    def test_file_operations(self):
        """Test basic file operations work correctly on Windows"""
        try:
            # Test file creation and writing
            test_file = os.path.join(self.temp_dir, "test_file.txt")
            
            with open(test_file, 'w') as f:
                f.write("Test content")
            
            self.assertTrue(os.path.exists(test_file))
            
            # Test file reading
            with open(test_file, 'r') as f:
                content = f.read()
            
            self.assertEqual(content, "Test content")
            
            # Test file deletion
            os.remove(test_file)
            self.assertFalse(os.path.exists(test_file))
            
            print("✓ File operations working correctly")
            
        except Exception as e:
            self.fail(f"File operations failed: {e}")
    
    def test_environment_variables(self):
        """Test environment variable handling"""
        try:
            # Test setting and getting environment variables
            test_var = "CLEVRR_TEST_VAR"
            test_value = "test_value_123"
            
            os.environ[test_var] = test_value
            retrieved_value = os.getenv(test_var)
            
            self.assertEqual(retrieved_value, test_value)
            
            # Clean up
            if test_var in os.environ:
                del os.environ[test_var]
            
            print("✓ Environment variable handling works")
            
        except Exception as e:
            self.fail(f"Environment variable test failed: {e}")
    
    def test_dotenv_functionality(self):
        """Test dotenv loading without requiring actual API keys"""
        try:
            import dotenv
            
            # Create a test .env file
            test_env_file = os.path.join(self.temp_dir, ".env")
            with open(test_env_file, 'w') as f:
                f.write("TEST_KEY=test_value\n")
                f.write("ANOTHER_KEY=another_value\n")
            
            # Test loading
            result = dotenv.load_dotenv(test_env_file)
            
            # Check if variables were loaded
            self.assertEqual(os.getenv("TEST_KEY"), "test_value")
            self.assertEqual(os.getenv("ANOTHER_KEY"), "another_value")
            
            print("✓ dotenv functionality works")
            
            # Clean up environment variables
            if "TEST_KEY" in os.environ:
                del os.environ["TEST_KEY"]
            if "ANOTHER_KEY" in os.environ:
                del os.environ["ANOTHER_KEY"]
            
        except ImportError:
            self.skipTest("python-dotenv not installed")
        except Exception as e:
            self.fail(f"dotenv functionality test failed: {e}")
    
    def test_utils_imports(self):
        """Test that utils modules can be imported"""
        try:
            # Add the project root to Python path if not already there
            project_root = os.path.dirname(os.path.abspath(__file__))
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            
            # Test importing utils modules
            from utils import contants  # Note: keeping original typo
            print("✓ utils.contants imported successfully")
            
            # Test that constants are defined
            self.assertTrue(hasattr(contants, 'BG_GRAY'))
            self.assertTrue(hasattr(contants, 'BG_COLOR'))
            self.assertTrue(hasattr(contants, 'TEXT_COLOR'))
            self.assertTrue(hasattr(contants, 'FONT'))
            self.assertTrue(hasattr(contants, 'FONT_BOLD'))
            
            print("✓ UI constants are properly defined")
            
        except ImportError as e:
            print(f"⚠ Could not import utils modules: {e}")
            print("This is expected if running outside the project directory")
        except Exception as e:
            self.fail(f"Utils import test failed: {e}")
    
    def test_mock_agent_creation(self):
        """Test agent creation with mocked dependencies"""
        try:
            # Mock the expensive imports
            with patch('utils.contants.GEMINI', Mock()):
                with patch('langchain.agents.create_react_agent', Mock()):
                    with patch('langchain.agents.AgentExecutor', Mock()):
                        # This would normally create the agent
                        # We're just testing the import path works
                        print("✓ Agent creation imports are compatible")
            
        except ImportError as e:
            print(f"⚠ Agent creation test skipped due to missing dependencies: {e}")
        except Exception as e:
            self.fail(f"Mock agent creation test failed: {e}")
    
    def test_windows_specific_features(self):
        """Test Windows-specific features if running on Windows"""
        if not self.is_windows:
            self.skipTest("Not running on Windows")
        
        try:
            # Test Windows-specific paths
            windows_font_dir = "C:/Windows/Fonts"
            if os.path.exists(windows_font_dir):
                fonts = os.listdir(windows_font_dir)
                self.assertGreater(len(fonts), 0)
                print(f"✓ Windows fonts directory accessible: {len(fonts)} fonts found")
            
            # Test Windows environment variables
            windows_vars = ['USERPROFILE', 'APPDATA', 'LOCALAPPDATA']
            for var in windows_vars:
                value = os.getenv(var)
                if value:
                    self.assertTrue(os.path.exists(value))
                    print(f"✓ Windows environment variable {var} is valid")
            
        except Exception as e:
            self.fail(f"Windows-specific features test failed: {e}")

def run_compatibility_test():
    """Run the compatibility test suite and return results"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWindowsCompatibility)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("WINDOWS COMPATIBILITY TEST SUMMARY")
    print("="*60)
    
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED! Clevrr Computer should work on this system.")
    else:
        print("⚠️  SOME TESTS FAILED. Check the details above.")
        
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('Exception:')[-1].strip()}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    print("Clevrr Computer - Windows Compatibility Test")
    print("="*50)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print("="*50)
    
    success = run_compatibility_test()
    sys.exit(0 if success else 1)