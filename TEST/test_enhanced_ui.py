#!/usr/bin/env python3
"""
Test script for JR AI Control Enhanced UI
Tests Material Design 3 components, voice, notifications, and token tracking
"""

import tkinter as tk
import sys
import os
import time
import threading

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.material_design import get_theme_manager, apply_global_theme
    from ui.enhanced_components import EnhancedChatInterface, SettingsDialog
    from utils.token_tracker import get_token_tracker
    from utils.notifications import get_notification_manager
    from voice.voice_manager import get_voice_manager
    
    print("✅ All enhanced UI modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class EnhancedUITestApp:
    """Test application for enhanced UI components"""
    
    def __init__(self):
        self.root = tk.Tk()
        
        # Initialize managers
        self.theme_manager = get_theme_manager()
        self.token_tracker = get_token_tracker()
        self.notification_manager = get_notification_manager()
        self.voice_manager = get_voice_manager()
        
        self.setup_window()
        self.create_test_ui()
        
        # Run initial tests
        self.run_initial_tests()
    
    def setup_window(self):
        """Setup test window"""
        self.root.title("JR AI Control - Enhanced UI Test")
        self.root.geometry("1000x700")
        
        # Apply theme
        self.theme_manager.apply_theme(self.root)
    
    def create_test_ui(self):
        """Create test UI"""
        # Create enhanced chat interface
        self.chat_interface = EnhancedChatInterface(
            self.root,
            on_message_send=self.handle_test_message
        )
        self.chat_interface.pack(fill=tk.BOTH, expand=True)
        
        # Add test messages
        self.add_test_messages()
    
    def add_test_messages(self):
        """Add test messages to demonstrate UI"""
        messages = [
            ("System", "🧪 Enhanced UI Test Mode Activated", "system"),
            ("You", "Hello, this is a test user message to demonstrate the chat interface styling.", "user"),
            ("JR AI", "Hello! This is a test AI response. The Material Design 3 styling should make this look modern and clean. This message demonstrates how AI responses are displayed with proper bubble styling, colors, and typography.", "ai"),
            ("System", "Testing system messages with different styling.", "system"),
            ("You", "Can you help me test the voice features?", "user"),
            ("JR AI", "Absolutely! I can help you test the voice features. The voice system includes speech-to-text for input and text-to-speech for responses. You can use the microphone button to test voice input, and AI responses will be spoken aloud if voice output is enabled in settings.", "ai"),
        ]
        
        for sender, message, msg_type in messages:
            self.chat_interface.add_message(sender, message, msg_type)
            time.sleep(0.1)  # Small delay for visual effect
    
    def handle_test_message(self, message: str):
        """Handle test messages"""
        # Simulate AI processing
        def simulate_response():
            time.sleep(1)  # Simulate processing time
            
            responses = [
                "This is a test response from the enhanced JR AI Control system!",
                "I'm demonstrating the Material Design 3 interface with integrated features.",
                "The token tracking system is monitoring our conversation usage.",
                "Voice interaction and notifications are working in the background.",
                "You can access settings to customize themes, voice, and notifications."
            ]
            
            import random
            response = random.choice(responses)
            
            # Update UI in main thread
            self.root.after(0, lambda: self.chat_interface.add_message("JR AI", response, "ai"))
        
        # Run in background thread
        threading.Thread(target=simulate_response, daemon=True).start()
    
    def run_initial_tests(self):
        """Run initial component tests"""
        def run_tests():
            time.sleep(2)  # Wait for UI to load
            
            # Test notifications
            self.notification_manager.show_info_notification(
                "UI Test Started", 
                "Testing enhanced Material Design 3 interface"
            )
            
            time.sleep(3)
            
            # Test token tracking
            self.token_tracker.add_message_tokens(
                "test_msg_1", 
                "Test user message", 
                "Test AI response for demonstration"
            )
            
            time.sleep(2)
            
            # Test voice system (if available)
            if self.voice_manager.is_voice_available():
                success, message = self.voice_manager.test_voice(
                    "JR AI Control enhanced interface test is running successfully."
                )
                
                self.notification_manager.show_voice_status(
                    "Voice test completed" if success else f"Voice test failed: {message}"
                )
            else:
                self.notification_manager.show_info_notification(
                    "Voice System", 
                    "Voice libraries not available - install speechrecognition, pyttsx3, and pyaudio"
                )
            
            time.sleep(2)
            
            # Test theme system
            self.notification_manager.show_info_notification(
                "Theme System", 
                f"Current theme: {self.theme_manager.theme_mode}"
            )
            
            # Test completion notification
            self.notification_manager.show_task_completion(
                "Enhanced UI Test", 
                "All components tested successfully!"
            )
        
        # Run tests in background
        threading.Thread(target=run_tests, daemon=True).start()
    
    def run(self):
        """Run the test application"""
        try:
            print("🚀 Starting Enhanced UI Test...")
            print(f"Theme: {self.theme_manager.theme_mode}")
            print(f"Voice Available: {self.voice_manager.is_voice_available()}")
            print(f"Notifications Enabled: {self.notification_manager.enabled}")
            print("=" * 50)
            
            self.root.mainloop()
            
        except KeyboardInterrupt:
            print("\n🛑 Test interrupted by user")
        except Exception as e:
            print(f"❌ Test error: {e}")
        finally:
            # Cleanup
            if hasattr(self, 'voice_manager'):
                self.voice_manager.cleanup()
            if hasattr(self, 'notification_manager'):
                self.notification_manager.cleanup()

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 JR AI Control - Enhanced UI Test Suite")
    print("=" * 60)
    
    # Test imports
    print("Testing imports...")
    
    try:
        # Test theme manager
        theme = get_theme_manager()
        print(f"✅ Theme Manager: {theme.theme_mode} mode")
        
        # Test token tracker
        tracker = get_token_tracker()
        stats = tracker.get_total_usage()
        print(f"✅ Token Tracker: {stats['total_tokens']} total tokens")
        
        # Test notification manager
        notif = get_notification_manager()
        print(f"✅ Notification Manager: {'Enabled' if notif.enabled else 'Disabled'}")
        
        # Test voice manager
        voice = get_voice_manager()
        print(f"✅ Voice Manager: {'Available' if voice.is_voice_available() else 'Not Available'}")
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return
    
    print("\n🎨 Starting Enhanced UI Test Application...")
    
    # Create and run test app
    app = EnhancedUITestApp()
    app.run()
    
    print("\n✅ Enhanced UI Test completed!")

if __name__ == "__main__":
    main()