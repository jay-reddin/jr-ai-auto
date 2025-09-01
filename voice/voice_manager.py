"""
Voice interaction system for JR AI Control
Handles speech recognition (STT) and text-to-speech (TTS) functionality
"""

import threading
import time
import queue
from typing import Callable, Optional, List
import os

# Voice recognition and TTS imports
try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("Voice libraries not available. Install speech_recognition and pyttsx3 for voice features.")

class VoiceManager:
    def __init__(self):
        self.voice_available = VOICE_AVAILABLE
        self.is_listening = False
        self.speech_enabled = True
        self.speech_muted = False
        
        # Callbacks
        self.on_speech_recognized: Optional[Callable[[str], None]] = None
        self.on_listening_start: Optional[Callable[[], None]] = None
        self.on_listening_stop: Optional[Callable[[], None]] = None
        self.on_error: Optional[Callable[[str], None]] = None
        
        # Voice settings
        self.voice_rate = 200
        self.voice_volume = 0.8
        self.recognition_language = "en-US"
        
        # Initialize components
        self.recognizer = None
        self.microphone = None
        self.tts_engine = None
        self.speech_queue = queue.Queue()
        self.listening_thread = None
        self.tts_thread = None
        
        if self.voice_available:
            self._initialize_voice_components()
    
    def _initialize_voice_components(self):
        """Initialize speech recognition and TTS components"""
        try:
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Initialize TTS engine
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', self.voice_rate)
            self.tts_engine.setProperty('volume', self.voice_volume)
            
            # Start TTS processing thread
            self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
            self.tts_thread.start()
            
            print("Voice components initialized successfully")
            
        except Exception as e:
            print(f"Error initializing voice components: {e}")
            self.voice_available = False
    
    def start_listening(self):
        """Start continuous speech recognition"""
        if not self.voice_available or self.is_listening:
            return False
        
        self.is_listening = True
        self.listening_thread = threading.Thread(target=self._listening_worker, daemon=True)
        self.listening_thread.start()
        
        if self.on_listening_start:
            self.on_listening_start()
        
        return True
    
    def stop_listening(self):
        """Stop speech recognition"""
        self.is_listening = False
        
        if self.on_listening_stop:
            self.on_listening_stop()
    
    def _listening_worker(self):
        """Worker thread for continuous speech recognition with enhanced performance optimization"""
        consecutive_errors = 0
        max_consecutive_errors = 5
        error_backoff_time = 0.1
        
        # Performance optimization: pre-allocate audio buffer
        audio_buffer_size = 4096
        
        # Adaptive timeout based on performance
        base_timeout = 0.3
        adaptive_timeout = base_timeout
        
        while self.is_listening:
            try:
                # Dynamic timeout adjustment based on system performance
                start_time = time.time()
                
                # Listen for audio with optimized timeout and buffer size
                with self.microphone as source:
                    # Use adaptive timeout for better responsiveness
                    audio = self.recognizer.listen(
                        source, 
                        timeout=adaptive_timeout, 
                        phrase_time_limit=3,
                        snowboy_configuration=None  # Disable snowboy for better performance
                    )
                
                # Measure audio capture time for adaptive timeout
                capture_time = time.time() - start_time
                
                # Adjust timeout based on capture performance
                if capture_time > adaptive_timeout * 0.8:
                    adaptive_timeout = min(adaptive_timeout * 1.1, 1.0)
                else:
                    adaptive_timeout = max(adaptive_timeout * 0.95, base_timeout)
                
                # Process audio recognition asynchronously with thread pool
                recognition_thread = threading.Thread(
                    target=self._process_audio_recognition,
                    args=(audio,),
                    daemon=True
                )
                recognition_thread.start()
                
                # Reset error counter on successful audio capture
                consecutive_errors = 0
                error_backoff_time = 0.1
                    
            except sr.WaitTimeoutError:
                # No speech detected within timeout - this is normal
                # Reduce timeout slightly for better responsiveness
                adaptive_timeout = max(adaptive_timeout * 0.98, base_timeout)
                pass
            except Exception as e:
                consecutive_errors += 1
                if self.on_error and consecutive_errors <= max_consecutive_errors:
                    self.on_error(f"Listening error: {e}")
                
                # Exponential backoff for repeated errors
                time.sleep(min(error_backoff_time * (2 ** consecutive_errors), 2.0))
                
                # Stop listening if too many consecutive errors
                if consecutive_errors > max_consecutive_errors:
                    self.is_listening = False
                    if self.on_error:
                        self.on_error("Too many consecutive errors, stopping voice recognition")
    
    def _process_audio_recognition(self, audio):
        """Process audio recognition in separate thread for better performance"""
        try:
            text = self.recognizer.recognize_google(audio, language=self.recognition_language)
            if text and self.on_speech_recognized:
                self.on_speech_recognized(text)
        except sr.UnknownValueError:
            # Speech was unintelligible - this is normal
            pass
        except sr.RequestError as e:
            if self.on_error:
                self.on_error(f"Speech recognition error: {e}")
        except Exception as e:
            if self.on_error:
                self.on_error(f"Audio processing error: {e}")
    
    def speak_text(self, text: str):
        """Add text to speech queue"""
        if not self.voice_available or self.speech_muted or not self.speech_enabled:
            return False
        
        self.speech_queue.put(text)
        return True
    
    def _tts_worker(self):
        """Worker thread for text-to-speech processing with enhanced performance optimization"""
        # Performance optimization: batch processing and queue management
        batch_size = 3
        batch_timeout = 0.5
        
        while True:
            try:
                # Collect batch of texts for more efficient processing
                texts_batch = []
                batch_start = time.time()
                
                # Get first text (blocking)
                try:
                    first_text = self.speech_queue.get(timeout=1)
                    if first_text:
                        texts_batch.append(first_text)
                except queue.Empty:
                    continue
                
                # Try to get additional texts for batch processing
                while (len(texts_batch) < batch_size and 
                       time.time() - batch_start < batch_timeout):
                    try:
                        additional_text = self.speech_queue.get_nowait()
                        if additional_text:
                            texts_batch.append(additional_text)
                    except queue.Empty:
                        break
                
                # Process batch if speech is enabled
                if texts_batch and not self.speech_muted and self.speech_enabled:
                    # Combine texts for more efficient speech synthesis
                    combined_text = self._combine_texts_for_speech(texts_batch)
                    
                    if combined_text:
                        # Use optimized TTS settings for better performance
                        self.tts_engine.say(combined_text)
                        self.tts_engine.runAndWait()
                
                # Mark all tasks as done
                for _ in texts_batch:
                    self.speech_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                if self.on_error:
                    self.on_error(f"TTS error: {e}")
                # Mark tasks as done even on error to prevent queue backup
                for _ in texts_batch:
                    try:
                        self.speech_queue.task_done()
                    except ValueError:
                        pass
    
    def _optimize_text_for_speech(self, text: str) -> str:
        """Optimize text for speech synthesis with enhanced performance"""
        if not text:
            return ""
        
        # Limit text length for better performance (max ~500 chars)
        if len(text) > 500:
            text = text[:497] + "..."
        
        # Clean up text with optimized regex
        import re
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove or replace problematic characters for TTS
        text = text.replace('\n', '. ')
        text = text.replace('\t', ' ')
        
        # Remove markdown formatting for better speech
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
        text = re.sub(r'`(.*?)`', r'\1', text)        # Code
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Links
        
        # Replace common abbreviations for better pronunciation
        replacements = {
            'API': 'A P I',
            'UI': 'U I',
            'URL': 'U R L',
            'JSON': 'J S O N',
            'HTML': 'H T M L',
            'CSS': 'C S S',
            'JS': 'JavaScript',
            'AI': 'A I'
        }
        
        for abbrev, replacement in replacements.items():
            text = text.replace(abbrev, replacement)
        
        return text
    
    def _combine_texts_for_speech(self, texts: List[str]) -> str:
        """Combine multiple texts for efficient batch speech synthesis"""
        if not texts:
            return ""
        
        # Optimize each text first
        optimized_texts = [self._optimize_text_for_speech(text) for text in texts if text]
        
        if not optimized_texts:
            return ""
        
        # Combine with appropriate pauses
        combined = ". ".join(optimized_texts)
        
        # Final length check
        if len(combined) > 800:
            combined = combined[:797] + "..."
        
        return combined
    
    def toggle_speech_enabled(self, enabled: bool):
        """Enable or disable speech output"""
        self.speech_enabled = enabled
    
    def toggle_speech_muted(self, muted: bool):
        """Mute or unmute speech output"""
        self.speech_muted = muted
    
    def set_voice_settings(self, rate: int = None, volume: float = None, language: str = None):
        """Update voice settings"""
        if rate is not None:
            self.voice_rate = rate
            if self.tts_engine:
                self.tts_engine.setProperty('rate', rate)
        
        if volume is not None:
            self.voice_volume = volume
            if self.tts_engine:
                self.tts_engine.setProperty('volume', volume)
        
        if language is not None:
            self.recognition_language = language
    
    def get_available_voices(self):
        """Get list of available TTS voices"""
        if not self.voice_available or not self.tts_engine:
            return []
        
        try:
            voices = self.tts_engine.getProperty('voices')
            return [(voice.id, voice.name) for voice in voices] if voices else []
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []
    
    def set_voice(self, voice_id: str):
        """Set TTS voice by ID"""
        if not self.voice_available or not self.tts_engine:
            return False
        
        try:
            self.tts_engine.setProperty('voice', voice_id)
            return True
        except Exception as e:
            print(f"Error setting voice: {e}")
            return False
    
    def is_voice_available(self) -> bool:
        """Check if voice functionality is available"""
        return self.voice_available
    
    def get_microphone_list(self):
        """Get list of available microphones"""
        if not self.voice_available:
            return []
        
        try:
            return sr.Microphone.list_microphone_names()
        except Exception as e:
            print(f"Error getting microphones: {e}")
            return []
    
    def set_microphone(self, device_index: int):
        """Set microphone by device index"""
        if not self.voice_available:
            return False
        
        try:
            self.microphone = sr.Microphone(device_index=device_index)
            # Re-adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            return True
        except Exception as e:
            print(f"Error setting microphone: {e}")
            return False
    
    def cleanup(self):
        """Clean up voice resources"""
        self.stop_listening()
        
        if self.tts_engine:
            try:
                self.tts_engine.stop()
            except:
                pass

# Global voice manager instance
_voice_manager = None

def get_voice_manager() -> VoiceManager:
    """Get the global voice manager instance"""
    global _voice_manager
    if _voice_manager is None:
        _voice_manager = VoiceManager()
    return _voice_manager

def is_voice_available() -> bool:
    """Check if voice functionality is available"""
    return VOICE_AVAILABLE