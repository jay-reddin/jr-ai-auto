"""
Platform-Specific Voice Feature Availability Detection
Task 8.3: Implement platform-specific voice feature availability detection

This module detects and reports available voice features for each platform:
- Windows with toga-winforms
- macOS with toga-cocoa
- Linux with toga-gtk
"""

import platform
import sys
import subprocess
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class VoiceCapabilities:
    """Data class for voice capabilities"""
    speech_recognition: bool = False
    text_to_speech: bool = False
    microphone_access: bool = False
    audio_output: bool = False
    toga_backend_available: bool = False
    platform_voice_apis: bool = False
    available_voices: List[str] = None
    available_microphones: List[str] = None
    platform_specific_features: Dict[str, bool] = None
    
    def __post_init__(self):
        if self.available_voices is None:
            self.available_voices = []
        if self.available_microphones is None:
            self.available_microphones = []
        if self.platform_specific_features is None:
            self.platform_specific_features = {}


class PlatformVoiceDetector:
    """Detects platform-specific voice feature availability for Toga integration"""
    
    def __init__(self):
        self.platform_name = platform.system()
        self.platform_version = platform.release()
        self.python_version = sys.version_info
        self._capabilities_cache = None
    
    def get_voice_capabilities(self, force_refresh: bool = False) -> VoiceCapabilities:
        """Get comprehensive voice capabilities for current platform"""
        if self._capabilities_cache is None or force_refresh:
            self._capabilities_cache = self._detect_all_capabilities()
        return self._capabilities_cache
    
    def _detect_all_capabilities(self) -> VoiceCapabilities:
        """Detect all voice capabilities for current platform"""
        capabilities = VoiceCapabilities()
        
        # Test basic voice libraries
        capabilities.speech_recognition = self._test_speech_recognition()
        capabilities.text_to_speech = self._test_text_to_speech()
        capabilities.microphone_access = self._test_microphone_access()
        capabilities.audio_output = self._test_audio_output()
        
        # Test Toga backend availability
        capabilities.toga_backend_available = self._test_toga_backend()
        
        # Test platform-specific voice APIs
        capabilities.platform_voice_apis = self._test_platform_voice_apis()
        
        # Get available voices and microphones
        capabilities.available_voices = self._get_available_voices()
        capabilities.available_microphones = self._get_available_microphones()
        
        # Get platform-specific features
        capabilities.platform_specific_features = self._get_platform_specific_features()
        
        return capabilities
    
    def _test_speech_recognition(self) -> bool:
        """Test speech recognition availability"""
        try:
            import speech_recognition as sr
            return True
        except ImportError:
            return False
    
    def _test_text_to_speech(self) -> bool:
        """Test text-to-speech availability"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.stop()
            return True
        except Exception:
            return False
    
    def _test_microphone_access(self) -> bool:
        """Test microphone access"""
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            mic = sr.Microphone()
            return True
        except Exception:
            return False
    
    def _test_audio_output(self) -> bool:
        """Test audio output capability"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.stop()
            return voices is not None and len(voices) > 0
        except Exception:
            return False
    
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
        if self.platform_name == "Windows":
            return self._test_windows_voice_apis()
        elif self.platform_name == "Darwin":
            return self._test_macos_voice_apis()
        elif self.platform_name == "Linux":
            return self._test_linux_voice_apis()
        else:
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
            result = subprocess.run(['which', 'espeak'], capture_output=True, timeout=5)
            if result.returncode == 0:
                return True
            
            # Test festival availability
            result = subprocess.run(['which', 'festival'], capture_output=True, timeout=5)
            if result.returncode == 0:
                return True
            
            # Test PulseAudio for microphone access
            result = subprocess.run(['which', 'pulseaudio'], capture_output=True, timeout=5)
            return result.returncode == 0
            
        except Exception:
            return False
    
    def _get_available_voices(self) -> List[str]:
        """Get list of available TTS voices"""
        voices = []
        
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voice_objects = engine.getProperty('voices')
            
            if voice_objects:
                for voice in voice_objects:
                    if hasattr(voice, 'name'):
                        voices.append(voice.name)
                    elif hasattr(voice, 'id'):
                        voices.append(voice.id)
            
            engine.stop()
            
        except Exception:
            pass
        
        return voices
    
    def _get_available_microphones(self) -> List[str]:
        """Get list of available microphones"""
        microphones = []
        
        try:
            import speech_recognition as sr
            microphones = sr.Microphone.list_microphone_names()
        except Exception:
            pass
        
        return microphones
    
    def _get_platform_specific_features(self) -> Dict[str, bool]:
        """Get platform-specific voice features"""
        if self.platform_name == "Windows":
            return self._get_windows_features()
        elif self.platform_name == "Darwin":
            return self._get_macos_features()
        elif self.platform_name == "Linux":
            return self._get_linux_features()
        else:
            return {}
    
    def _get_windows_features(self) -> Dict[str, bool]:
        """Get Windows-specific voice features"""
        features = {}
        
        # Windows Speech API (SAPI)
        try:
            import win32com.client
            sapi = win32com.client.Dispatch("SAPI.SpVoice")
            features['windows_sapi'] = True
        except ImportError:
            features['windows_sapi'] = False
        
        # Windows 10+ Speech Recognition
        try:
            import winrt.windows.media.speechrecognition
            features['windows_speech_recognition'] = True
        except ImportError:
            features['windows_speech_recognition'] = False
        
        # DirectSound for audio
        features['directsound_available'] = True  # Assume available on Windows
        
        # Windows Forms integration
        try:
            import toga_winforms
            from toga_winforms.libs import WinForms
            features['winforms_integration'] = True
        except ImportError:
            features['winforms_integration'] = False
        
        return features
    
    def _get_macos_features(self) -> Dict[str, bool]:
        """Get macOS-specific voice features"""
        features = {}
        
        # macOS Speech Framework
        try:
            import objc
            from Foundation import NSBundle
            speech_bundle = NSBundle.bundleWithPath_("/System/Library/Frameworks/Speech.framework")
            features['macos_speech_framework'] = speech_bundle is not None
        except ImportError:
            features['macos_speech_framework'] = False
        
        # Core Audio
        try:
            import objc
            from Foundation import NSBundle
            ca_bundle = NSBundle.bundleWithPath_("/System/Library/Frameworks/CoreAudio.framework")
            features['core_audio'] = ca_bundle is not None
        except ImportError:
            features['core_audio'] = False
        
        # AVFoundation
        try:
            import objc
            from Foundation import NSBundle
            av_bundle = NSBundle.bundleWithPath_("/System/Library/Frameworks/AVFoundation.framework")
            features['avfoundation'] = av_bundle is not None
        except ImportError:
            features['avfoundation'] = False
        
        # Cocoa integration
        try:
            import toga_cocoa
            from toga_cocoa.libs import NSButton
            features['cocoa_integration'] = True
        except ImportError:
            features['cocoa_integration'] = False
        
        return features
    
    def _get_linux_features(self) -> Dict[str, bool]:
        """Get Linux-specific voice features"""
        features = {}
        
        # PulseAudio
        try:
            result = subprocess.run(['which', 'pulseaudio'], capture_output=True, timeout=5)
            features['pulseaudio'] = result.returncode == 0
        except Exception:
            features['pulseaudio'] = False
        
        # ALSA
        try:
            result = subprocess.run(['which', 'aplay'], capture_output=True, timeout=5)
            features['alsa'] = result.returncode == 0
        except Exception:
            features['alsa'] = False
        
        # espeak TTS
        try:
            result = subprocess.run(['which', 'espeak'], capture_output=True, timeout=5)
            features['espeak'] = result.returncode == 0
        except Exception:
            features['espeak'] = False
        
        # Festival TTS
        try:
            result = subprocess.run(['which', 'festival'], capture_output=True, timeout=5)
            features['festival'] = result.returncode == 0
        except Exception:
            features['festival'] = False
        
        # GTK integration
        try:
            import toga_gtk
            from toga_gtk.libs import Gtk
            features['gtk_integration'] = True
        except ImportError:
            features['gtk_integration'] = False
        
        return features
    
    def is_voice_fully_supported(self) -> bool:
        """Check if voice functionality is fully supported on current platform"""
        capabilities = self.get_voice_capabilities()
        
        return (
            capabilities.speech_recognition and
            capabilities.text_to_speech and
            capabilities.microphone_access and
            capabilities.audio_output and
            capabilities.toga_backend_available
        )
    
    def get_voice_support_status(self) -> Dict[str, str]:
        """Get detailed voice support status with recommendations"""
        capabilities = self.get_voice_capabilities()
        status = {}
        
        # Overall status
        if self.is_voice_fully_supported():
            status['overall'] = "fully_supported"
        elif capabilities.toga_backend_available and (capabilities.speech_recognition or capabilities.text_to_speech):
            status['overall'] = "partially_supported"
        else:
            status['overall'] = "not_supported"
        
        # Individual feature status
        status['speech_recognition'] = "available" if capabilities.speech_recognition else "unavailable"
        status['text_to_speech'] = "available" if capabilities.text_to_speech else "unavailable"
        status['microphone_access'] = "available" if capabilities.microphone_access else "unavailable"
        status['audio_output'] = "available" if capabilities.audio_output else "unavailable"
        status['toga_backend'] = "available" if capabilities.toga_backend_available else "unavailable"
        
        # Platform-specific recommendations
        if not capabilities.toga_backend_available:
            if self.platform_name == "Windows":
                status['recommendation'] = "Install toga-winforms: pip install toga-winforms"
            elif self.platform_name == "Darwin":
                status['recommendation'] = "Install toga-cocoa: pip install toga-cocoa"
            elif self.platform_name == "Linux":
                status['recommendation'] = "Install toga-gtk: pip install toga-gtk"
        elif not capabilities.speech_recognition:
            status['recommendation'] = "Install speech recognition: pip install SpeechRecognition"
        elif not capabilities.text_to_speech:
            status['recommendation'] = "Install text-to-speech: pip install pyttsx3"
        else:
            status['recommendation'] = "Voice functionality is ready to use"
        
        return status
    
    def print_voice_capabilities_report(self):
        """Print a comprehensive voice capabilities report"""
        capabilities = self.get_voice_capabilities()
        status = self.get_voice_support_status()
        
        print("=" * 60)
        print("VOICE CAPABILITIES REPORT")
        print("=" * 60)
        print(f"Platform: {self.platform_name} {self.platform_version}")
        print(f"Python: {sys.version}")
        print(f"Overall Status: {status['overall'].replace('_', ' ').title()}")
        print()
        
        print("Core Capabilities:")
        print(f"  Speech Recognition: {'✓' if capabilities.speech_recognition else '✗'}")
        print(f"  Text-to-Speech: {'✓' if capabilities.text_to_speech else '✗'}")
        print(f"  Microphone Access: {'✓' if capabilities.microphone_access else '✗'}")
        print(f"  Audio Output: {'✓' if capabilities.audio_output else '✗'}")
        print(f"  Toga Backend: {'✓' if capabilities.toga_backend_available else '✗'}")
        print(f"  Platform Voice APIs: {'✓' if capabilities.platform_voice_apis else '✗'}")
        print()
        
        if capabilities.available_voices:
            print(f"Available Voices ({len(capabilities.available_voices)}):")
            for i, voice in enumerate(capabilities.available_voices[:5]):  # Show first 5
                print(f"  {i+1}. {voice}")
            if len(capabilities.available_voices) > 5:
                print(f"  ... and {len(capabilities.available_voices) - 5} more")
            print()
        
        if capabilities.available_microphones:
            print(f"Available Microphones ({len(capabilities.available_microphones)}):")
            for i, mic in enumerate(capabilities.available_microphones[:3]):  # Show first 3
                print(f"  {i+1}. {mic}")
            if len(capabilities.available_microphones) > 3:
                print(f"  ... and {len(capabilities.available_microphones) - 3} more")
            print()
        
        if capabilities.platform_specific_features:
            print("Platform-Specific Features:")
            for feature, available in capabilities.platform_specific_features.items():
                status_icon = "✓" if available else "✗"
                print(f"  {status_icon} {feature.replace('_', ' ').title()}")
            print()
        
        print(f"Recommendation: {status['recommendation']}")
        print("=" * 60)


# Global detector instance
_platform_voice_detector = None

def get_platform_voice_detector() -> PlatformVoiceDetector:
    """Get the global platform voice detector instance"""
    global _platform_voice_detector
    if _platform_voice_detector is None:
        _platform_voice_detector = PlatformVoiceDetector()
    return _platform_voice_detector

def is_voice_fully_supported() -> bool:
    """Check if voice functionality is fully supported on current platform"""
    detector = get_platform_voice_detector()
    return detector.is_voice_fully_supported()

def get_voice_capabilities() -> VoiceCapabilities:
    """Get voice capabilities for current platform"""
    detector = get_platform_voice_detector()
    return detector.get_voice_capabilities()

def print_voice_report():
    """Print voice capabilities report for current platform"""
    detector = get_platform_voice_detector()
    detector.print_voice_capabilities_report()


if __name__ == "__main__":
    # Run voice capabilities report when executed directly
    print_voice_report()