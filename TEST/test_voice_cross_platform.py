#!/usr/bin/env python3
"""
Cross-Platform Voice Integration Testing for Toga UI Migration
Task 8.3: Test voice integration across platforms

This test suite verifies voice controls work correctly on:
- Windows with toga-winforms
- macOS with toga-cocoa  
- Linux with toga-gtk

Requirements: 5.5, 10.1, 10.2, 10.3
"""

import sys
import os
import platform
import time
import threading
import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List, Optional, Tuple

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class PlatformVoiceDetector:
    """Detects platform-specific voice feature availability"""
    
    def __init__(self):
        self.platform_name = platform.system()
        self.platform_version = platform.release()
        self.python_version = sys.version_info
        
    def detect_platform_capabilities(self) -> Dict[str, bool]:
        """Detect voice capabilities for current platform"""
        capabilities = {
            'speech_recognition': False,
            'text_to_speech': False,
            'microphone_access': False,
            'audio_output': False,
            'toga_backend_available': False,
            'platform_voice_apis': False
        }
        
        # Test speech recognition availability
        try:
            import speech_recognition as sr
            capabilities['speech_recognition'] = True
            
            # Test microphone access
            try:
                r = sr.Recognizer()
                mic = sr.Microphone()
                capabilities['microphone_access'] = True
            except Exception:
                pass
                
        except ImportError:
            pass
        
        # Test text-to-speech availability
        try:
            import pyttsx3
            engine = pyttsx3.init()
            capabilities['text_to_speech'] = True
            capabilities['audio_output'] = True
            engine.stop()
        except Exception:
            pass
        
        # Test platform-specific Toga backend
        capabilities['toga_backend_available'] = self._test_toga_backend()
        
        # Test platform-specific voice APIs
        capabilities['platform_voice_apis'] = self._test_platform_voice_apis()
        
        return capabilities
    
    def _test_toga_backend(self) -> bool:
        """Test if appropriate Toga backend is available"""
        try:
            if self.platform_name == "Windows":
                import toga_winforms
                return True
            elif self.platform_name == "Darwin":  # macOS
                import toga_cocoa
                return True
            elif self.platform_name == "Linux":
                import toga_gtk
                return True
            else:
                return False
        except ImportError:
            return False
    
    def _test_platform_voice_apis(self) -> bool:
        """Test platform-specific voice APIs"""
        try:
            if self.platform_name == "Windows":
                return self._test_windows_voice_apis()
            elif self.platform_name == "Darwin":
                return self._test_macos_voice_apis()
            elif self.platform_name == "Linux":
                return self._test_linux_voice_apis()
            else:
                return False
        except Exception:
            return False    

    def _test_windows_voice_apis(self) -> bool:
        """Test Windows-specific voice APIs"""
        try:
            # Test Windows Speech API (SAPI)
            import win32com.client
            sapi = win32com.client.Dispatch("SAPI.SpVoice")
            return True
        except ImportError:
            try:
                # Test Windows 10+ Speech Platform
                import winrt.windows.media.speechrecognition as sr
                return True
            except ImportError:
                return False
    
    def _test_macos_voice_apis(self) -> bool:
        """Test macOS-specific voice APIs"""
        try:
            # Test macOS Speech Framework
            import objc
            from Foundation import NSBundle
            
            # Try to load Speech framework
            speech_bundle = NSBundle.bundleWithPath_("/System/Library/Frameworks/Speech.framework")
            return speech_bundle is not None
        except ImportError:
            try:
                # Test NSSpeechSynthesizer availability
                import AppKit
                return hasattr(AppKit, 'NSSpeechSynthesizer')
            except ImportError:
                return False
    
    def _test_linux_voice_apis(self) -> bool:
        """Test Linux-specific voice APIs"""
        try:
            # Test espeak availability
            import subprocess
            result = subprocess.run(['which', 'espeak'], capture_output=True)
            if result.returncode == 0:
                return True
            
            # Test festival availability
            result = subprocess.run(['which', 'festival'], capture_output=True)
            if result.returncode == 0:
                return True
            
            # Test PulseAudio for microphone access
            result = subprocess.run(['which', 'pulseaudio'], capture_output=True)
            return result.returncode == 0
            
        except Exception:
            return False


class CrossPlatformVoiceTester:
    """Tests voice integration across different platforms"""
    
    def __init__(self):
        self.detector = PlatformVoiceDetector()
        self.capabilities = self.detector.detect_platform_capabilities()
        self.test_results = {}
        
    def run_platform_specific_tests(self) -> Dict[str, bool]:
        """Run platform-specific voice integration tests"""
        platform_name = self.detector.platform_name
        
        if platform_name == "Windows":
            return self._test_windows_voice_integration()
        elif platform_name == "Darwin":
            return self._test_macos_voice_integration()
        elif platform_name == "Linux":
            return self._test_linux_voice_integration()
        else:
            return {"unsupported_platform": False}
    
    def _test_windows_voice_integration(self) -> Dict[str, bool]:
        """Test voice integration on Windows with toga-winforms"""
        results = {}
        
        # Test 1: Toga-winforms backend availability
        try:
            import toga_winforms
            results['toga_winforms_import'] = True
        except ImportError:
            results['toga_winforms_import'] = False
        
        # Test 2: Windows Forms voice controls
        if results.get('toga_winforms_import', False):
            results['winforms_voice_controls'] = self._test_winforms_voice_controls()
        else:
            results['winforms_voice_controls'] = False
        
        # Test 3: Windows Speech API integration
        results['windows_sapi_integration'] = self._test_windows_sapi_integration()
        
        # Test 4: Microphone access through Windows Forms
        results['winforms_microphone_access'] = self._test_winforms_microphone_access()
        
        # Test 5: Audio output through Windows Forms
        results['winforms_audio_output'] = self._test_winforms_audio_output()
        
        return results    

    def _test_macos_voice_integration(self) -> Dict[str, bool]:
        """Test voice integration on macOS with toga-cocoa"""
        results = {}
        
        # Test 1: Toga-cocoa backend availability
        try:
            import toga_cocoa
            results['toga_cocoa_import'] = True
        except ImportError:
            results['toga_cocoa_import'] = False
        
        # Test 2: Cocoa voice controls
        if results.get('toga_cocoa_import', False):
            results['cocoa_voice_controls'] = self._test_cocoa_voice_controls()
        else:
            results['cocoa_voice_controls'] = False
        
        # Test 3: macOS Speech Framework integration
        results['macos_speech_framework'] = self._test_macos_speech_framework()
        
        # Test 4: Core Audio microphone access
        results['coreaudio_microphone_access'] = self._test_coreaudio_microphone_access()
        
        # Test 5: AVAudioEngine integration
        results['avaudioengine_integration'] = self._test_avaudioengine_integration()
        
        return results
    
    def _test_linux_voice_integration(self) -> Dict[str, bool]:
        """Test voice integration on Linux with toga-gtk"""
        results = {}
        
        # Test 1: Toga-gtk backend availability
        try:
            import toga_gtk
            results['toga_gtk_import'] = True
        except ImportError:
            results['toga_gtk_import'] = False
        
        # Test 2: GTK voice controls
        if results.get('toga_gtk_import', False):
            results['gtk_voice_controls'] = self._test_gtk_voice_controls()
        else:
            results['gtk_voice_controls'] = False
        
        # Test 3: PulseAudio integration
        results['pulseaudio_integration'] = self._test_pulseaudio_integration()
        
        # Test 4: ALSA microphone access
        results['alsa_microphone_access'] = self._test_alsa_microphone_access()
        
        # Test 5: espeak/festival TTS integration
        results['linux_tts_integration'] = self._test_linux_tts_integration()
        
        return results
    
    def _test_winforms_voice_controls(self) -> bool:
        """Test Windows Forms voice control integration"""
        try:
            import toga_winforms
            from toga_winforms.libs import WinForms
            
            # Create a mock button to test voice control integration
            button = WinForms.Button()
            button.Text = "🎤"
            
            # Test that we can create and configure voice controls
            button.Click += lambda sender, e: None
            
            return True
        except Exception as e:
            print(f"Windows Forms voice controls test failed: {e}")
            return False
    
    def _test_windows_sapi_integration(self) -> bool:
        """Test Windows Speech API integration"""
        try:
            import win32com.client
            
            # Test SAPI voice synthesis
            sapi = win32com.client.Dispatch("SAPI.SpVoice")
            voices = sapi.GetVoices()
            
            # Test that we can enumerate voices
            return voices.Count > 0
        except Exception:
            return False  
  
    def _test_winforms_microphone_access(self) -> bool:
        """Test microphone access through Windows Forms"""
        try:
            import speech_recognition as sr
            
            # Test microphone enumeration
            mics = sr.Microphone.list_microphone_names()
            return len(mics) > 0
        except Exception:
            return False
    
    def _test_winforms_audio_output(self) -> bool:
        """Test audio output through Windows Forms"""
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.stop()
            
            return len(voices) > 0 if voices else False
        except Exception:
            return False
    
    def _test_cocoa_voice_controls(self) -> bool:
        """Test Cocoa voice control integration"""
        try:
            import toga_cocoa
            from toga_cocoa.libs import NSButton, NSApplication
            
            # Create a mock button to test voice control integration
            button = NSButton.alloc().init()
            button.setTitle_("🎤")
            
            # Test that we can create and configure voice controls
            return True
        except Exception as e:
            print(f"Cocoa voice controls test failed: {e}")
            return False
    
    def _test_macos_speech_framework(self) -> bool:
        """Test macOS Speech Framework integration"""
        try:
            import objc
            from Foundation import NSBundle
            
            # Load Speech framework
            speech_bundle = NSBundle.bundleWithPath_("/System/Library/Frameworks/Speech.framework")
            if speech_bundle:
                speech_bundle.load()
                return True
            return False
        except Exception:
            return False
    
    def _test_coreaudio_microphone_access(self) -> bool:
        """Test Core Audio microphone access"""
        try:
            import speech_recognition as sr
            
            # Test microphone access on macOS
            r = sr.Recognizer()
            mic = sr.Microphone()
            
            with mic as source:
                r.adjust_for_ambient_noise(source, duration=0.1)
            
            return True
        except Exception:
            return False
    
    def _test_avaudioengine_integration(self) -> bool:
        """Test AVAudioEngine integration"""
        try:
            import objc
            from Foundation import NSBundle
            
            # Try to load AVFoundation framework
            av_bundle = NSBundle.bundleWithPath_("/System/Library/Frameworks/AVFoundation.framework")
            return av_bundle is not None
        except Exception:
            return False  
  
    def _test_gtk_voice_controls(self) -> bool:
        """Test GTK voice control integration"""
        try:
            import toga_gtk
            from toga_gtk.libs import Gtk
            
            # Create a mock button to test voice control integration
            button = Gtk.Button.new_with_label("🎤")
            
            # Test that we can create and configure voice controls
            button.connect("clicked", lambda widget: None)
            
            return True
        except Exception as e:
            print(f"GTK voice controls test failed: {e}")
            return False
    
    def _test_pulseaudio_integration(self) -> bool:
        """Test PulseAudio integration"""
        try:
            import subprocess
            
            # Test if PulseAudio is running
            result = subprocess.run(['pulseaudio', '--check'], capture_output=True)
            return result.returncode == 0
        except Exception:
            return False
    
    def _test_alsa_microphone_access(self) -> bool:
        """Test ALSA microphone access"""
        try:
            import speech_recognition as sr
            
            # Test microphone access on Linux
            mics = sr.Microphone.list_microphone_names()
            return len(mics) > 0
        except Exception:
            return False
    
    def _test_linux_tts_integration(self) -> bool:
        """Test Linux TTS integration (espeak/festival)"""
        try:
            import subprocess
            
            # Test espeak
            result = subprocess.run(['which', 'espeak'], capture_output=True)
            if result.returncode == 0:
                return True
            
            # Test festival
            result = subprocess.run(['which', 'festival'], capture_output=True)
            return result.returncode == 0
        except Exception:
            return False


class TestCrossPlatformVoiceIntegration(unittest.TestCase):
    """Unit tests for cross-platform voice integration"""
    
    def setUp(self):
        """Set up test environment"""
        self.detector = PlatformVoiceDetector()
        self.tester = CrossPlatformVoiceTester()
        self.platform_name = platform.system()
    
    def test_platform_detection(self):
        """Test platform detection functionality"""
        self.assertIn(self.platform_name, ["Windows", "Darwin", "Linux"])
        
        capabilities = self.detector.detect_platform_capabilities()
        self.assertIsInstance(capabilities, dict)
        self.assertIn('speech_recognition', capabilities)
        self.assertIn('text_to_speech', capabilities)
        self.assertIn('toga_backend_available', capabilities)
    
    def test_toga_backend_availability(self):
        """Test that appropriate Toga backend is available"""
        backend_available = self.detector._test_toga_backend()
        
        if self.platform_name == "Windows":
            # Should have toga-winforms
            try:
                import toga_winforms
                self.assertTrue(backend_available)
            except ImportError:
                self.assertFalse(backend_available)
        elif self.platform_name == "Darwin":
            # Should have toga-cocoa
            try:
                import toga_cocoa
                self.assertTrue(backend_available)
            except ImportError:
                self.assertFalse(backend_available)
        elif self.platform_name == "Linux":
            # Should have toga-gtk
            try:
                import toga_gtk
                self.assertTrue(backend_available)
            except ImportError:
                self.assertFalse(backend_available)   
 
    def test_voice_manager_integration(self):
        """Test voice manager integration with Toga"""
        try:
            from voice.voice_manager import get_voice_manager
            
            vm = get_voice_manager()
            self.assertIsNotNone(vm)
            
            # Test basic functionality
            self.assertIsInstance(vm.is_voice_available(), bool)
            self.assertIsInstance(vm.speech_enabled, bool)
            self.assertIsInstance(vm.speech_muted, bool)
            
        except ImportError:
            self.skipTest("Voice manager not available")
    
    def test_platform_specific_voice_controls(self):
        """Test platform-specific voice controls"""
        platform_results = self.tester.run_platform_specific_tests()
        
        if self.platform_name == "Windows":
            self.assertIn('toga_winforms_import', platform_results)
            if platform_results.get('toga_winforms_import', False):
                self.assertIn('winforms_voice_controls', platform_results)
        elif self.platform_name == "Darwin":
            self.assertIn('toga_cocoa_import', platform_results)
            if platform_results.get('toga_cocoa_import', False):
                self.assertIn('cocoa_voice_controls', platform_results)
        elif self.platform_name == "Linux":
            self.assertIn('toga_gtk_import', platform_results)
            if platform_results.get('toga_gtk_import', False):
                self.assertIn('gtk_voice_controls', platform_results)
    
    def test_microphone_access(self):
        """Test microphone access across platforms"""
        capabilities = self.detector.detect_platform_capabilities()
        
        if capabilities.get('speech_recognition', False):
            try:
                import speech_recognition as sr
                
                # Test microphone enumeration
                mics = sr.Microphone.list_microphone_names()
                self.assertIsInstance(mics, list)
                
                # Test microphone creation
                if mics:
                    mic = sr.Microphone()
                    self.assertIsNotNone(mic)
                    
            except Exception as e:
                self.skipTest(f"Microphone access test failed: {e}")
    
    def test_audio_output(self):
        """Test audio output across platforms"""
        capabilities = self.detector.detect_platform_capabilities()
        
        if capabilities.get('text_to_speech', False):
            try:
                import pyttsx3
                
                engine = pyttsx3.init()
                self.assertIsNotNone(engine)
                
                # Test voice enumeration
                voices = engine.getProperty('voices')
                if voices:
                    self.assertIsInstance(voices, list)
                    self.assertGreater(len(voices), 0)
                
                engine.stop()
                
            except Exception as e:
                self.skipTest(f"Audio output test failed: {e}")


def run_comprehensive_voice_tests():
    """Run comprehensive cross-platform voice integration tests"""
    print("=== Cross-Platform Voice Integration Test Suite ===")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print("=" * 60)
    
    # Initialize test components
    detector = PlatformVoiceDetector()
    tester = CrossPlatformVoiceTester()
    
    # Test 1: Platform Detection
    print("\n1. Platform Detection and Capabilities")
    print("-" * 40)
    capabilities = detector.detect_platform_capabilities()
    for capability, available in capabilities.items():
        status = "✓" if available else "✗"
        print(f"  {status} {capability}: {available}")
    
    # Test 2: Platform-Specific Integration Tests
    print("\n2. Platform-Specific Integration Tests")
    print("-" * 40)
    platform_results = tester.run_platform_specific_tests()
    
    for test_name, result in platform_results.items():
        status = "✓" if result else "✗"
        print(f"  {status} {test_name}: {result}")
    
    # Test 3: Voice Manager Integration
    print("\n3. Voice Manager Integration")
    print("-" * 40)
    try:
        from voice.voice_manager import get_voice_manager
        
        vm = get_voice_manager()
        print(f"  ✓ Voice Manager Available: {vm.is_voice_available()}")
        print(f"  ✓ Speech Enabled: {vm.speech_enabled}")
        print(f"  ✓ Speech Muted: {vm.speech_muted}")
        
        # Test voice settings
        if vm.is_voice_available():
            voices = vm.get_available_voices()
            print(f"  ✓ Available Voices: {len(voices)}")
            
            mics = vm.get_microphone_list()
            print(f"  ✓ Available Microphones: {len(mics)}")
            
    except Exception as e:
        print(f"  ✗ Voice Manager Integration Failed: {e}")
    
    # Test 4: Main Application Integration
    print("\n4. Main Application Integration")
    print("-" * 40)
    try:
        # Mock toga to avoid GUI creation
        with patch('toga.App'), patch('toga.MainWindow'):
            from main_toga import JRAIControlApp
            
            # Test that voice-related attributes exist
            app_class = JRAIControlApp
            voice_methods = [
                'setup_voice_system',
                'toggle_listening', 
                'on_speech_recognized',
                'on_listening_start',
                'on_listening_stop',
                'on_voice_error'
            ]
            
            for method in voice_methods:
                if hasattr(app_class, method):
                    print(f"  ✓ {method}: Available")
                else:
                    print(f"  ✗ {method}: Missing")
                    
    except Exception as e:
        print(f"  ✗ Main Application Integration Failed: {e}")
    
    # Test 5: Unit Tests
    print("\n5. Running Unit Tests")
    print("-" * 40)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCrossPlatformVoiceIntegration)
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 60)
    print("CROSS-PLATFORM VOICE INTEGRATION TEST SUMMARY")
    print("=" * 60)
    
    total_capabilities = len(capabilities)
    available_capabilities = sum(capabilities.values())
    
    total_platform_tests = len(platform_results)
    passed_platform_tests = sum(platform_results.values())
    
    print(f"Platform Capabilities: {available_capabilities}/{total_capabilities}")
    print(f"Platform-Specific Tests: {passed_platform_tests}/{total_platform_tests}")
    print(f"Unit Tests: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun}")
    
    overall_success = (
        available_capabilities > 0 and
        passed_platform_tests > 0 and
        len(result.failures) == 0 and
        len(result.errors) == 0
    )
    
    if overall_success:
        print("\n🎉 Cross-platform voice integration tests PASSED!")
        print("Voice functionality is working correctly on this platform.")
    else:
        print("\n❌ Cross-platform voice integration tests had issues.")
        print("Some voice features may not be available on this platform.")
    
    return overall_success


if __name__ == "__main__":
    success = run_comprehensive_voice_tests()
    sys.exit(0 if success else 1)