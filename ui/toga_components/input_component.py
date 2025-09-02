"""
Input Component for Toga-based JR AI Control
Manages text input, voice controls, and message sending
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import threading
import uuid
from typing import Optional


class InputComponent:
    """
    Input component that handles user message input and voice controls
    """
    
    def __init__(self, app_instance, chat_component):
        self.app = app_instance
        self.chat_component = chat_component
        self.text_input: Optional[toga.MultilineTextInput] = None
        self.send_button: Optional[toga.Button] = None
        self.mic_button: Optional[toga.Button] = None
        self.voice_status_label: Optional[toga.Label] = None
        self.is_processing = False
        self.current_message_id: Optional[str] = None
    
    def create_input_layout(self) -> toga.Box:
        """Create the input area layout with text field and controls"""
        try:
            # Main input container
            input_box = toga.Box(
                style=Pack(
                    direction=ROW,
                    padding=(10, 0, 0, 0),
                    alignment="center"
                )
            )
            
            # Text input field
            self.text_input = toga.MultilineTextInput(
                placeholder="Type your message here...",
                style=Pack(
                    flex=1,
                    height=60,
                    padding=(0, 10, 0, 0)
                )
            )
            input_box.add(self.text_input)
            
            # Controls container
            controls_box = toga.Box(
                style=Pack(
                    direction=COLUMN,
                    padding=(0, 0, 0, 10)
                )
            )
            
            # Voice controls (if available)
            if self.app.voice_manager and self.app.voice_manager.is_voice_available():
                voice_box = self._create_voice_controls()
                controls_box.add(voice_box)
            
            # Send button
            self.send_button = toga.Button(
                "Send",
                on_press=self._send_message,
                style=Pack(
                    width=80,
                    padding=(5, 0, 0, 0)
                )
            )
            controls_box.add(self.send_button)
            
            input_box.add(controls_box)
            
            return input_box
            
        except Exception as e:
            print(f"Error creating input layout: {e}")
            # Return a simple fallback
            return self._create_fallback_input()
    
    def _create_voice_controls(self) -> toga.Box:
        """Create voice control widgets"""
        voice_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding=(0, 0, 5, 0)
            )
        )
        
        # Microphone button
        self.mic_button = toga.Button(
            "🎤",
            on_press=self._toggle_voice_listening,
            style=Pack(
                width=40,
                padding=(0, 5, 0, 0)
            )
        )
        voice_box.add(self.mic_button)
        
        # Voice status indicator
        self.voice_status_label = toga.Label(
            "Ready",
            style=Pack(
                font_size=10,
                padding=(0, 0, 0, 5)
            )
        )
        voice_box.add(self.voice_status_label)
        
        return voice_box
    
    def _create_fallback_input(self) -> toga.Box:
        """Create a simple fallback input if main creation fails"""
        fallback_box = toga.Box(style=Pack(direction=ROW, padding=10))
        
        text_input = toga.TextInput(
            placeholder="Type message...",
            style=Pack(flex=1, padding=(0, 10, 0, 0))
        )
        fallback_box.add(text_input)
        
        send_button = toga.Button(
            "Send",
            style=Pack(width=60)
        )
        fallback_box.add(send_button)
        
        return fallback_box
    
    def _send_message(self, widget):
        """Handle send button press"""
        try:
            if self.is_processing:
                return
            
            message_text = self.text_input.value.strip() if self.text_input else ""
            if not message_text:
                return
            
            # Check if agent is available
            if not hasattr(self.app, 'agent_executor') or not self.app.agent_executor:
                if not self.app.api_key:
                    self.chat_component.add_system_message(
                        "Please configure your API key in settings first."
                    )
                else:
                    self.chat_component.add_system_message(
                        "AI agent not initialized. Please check your configuration."
                    )
                return
            
            # Generate unique message ID
            self.current_message_id = str(uuid.uuid4())
            
            # Clear input and disable controls
            self.text_input.value = ""
            self._set_processing_state(True)
            
            # Add user message to chat
            self.chat_component.add_user_message(message_text)
            
            # Process message in background thread
            threading.Thread(
                target=self._process_message_async,
                args=(message_text,),
                daemon=True
            ).start()
            
        except Exception as e:
            print(f"Error sending message: {e}")
            self.chat_component.add_system_message(f"Error sending message: {e}")
            self._set_processing_state(False)
    
    def _process_message_async(self, message_text: str):
        """Process the message with the AI agent in a background thread"""
        try:
            # This would integrate with the existing agent system
            # For now, we'll create a placeholder response
            
            # Simulate processing time
            import time
            time.sleep(1)
            
            # Add AI response (placeholder)
            response_text = f"This is a placeholder response to: {message_text}"
            
            # Update UI in main thread
            self.app.main_window.app.add_background_task(
                self._add_ai_response,
                response_text,
                0  # tokens placeholder
            )
            
        except Exception as e:
            print(f"Error processing message: {e}")
            # Add error message
            self.app.main_window.app.add_background_task(
                self._add_error_response,
                str(e)
            )
        finally:
            # Re-enable controls
            self.app.main_window.app.add_background_task(
                self._set_processing_state,
                False
            )
    
    async def _add_ai_response(self, response_text: str, tokens: int):
        """Add AI response to chat (called from main thread)"""
        try:
            self.chat_component.add_ai_message(response_text, tokens)
            
            # Update token display in header
            if hasattr(self.app, 'main_window') and self.app.main_window.header_component:
                total_tokens = self.app.token_tracker.get_total_tokens() if self.app.token_tracker else 0
                self.app.main_window.header_component.update_token_display(tokens, total_tokens)
                
        except Exception as e:
            print(f"Error adding AI response: {e}")
    
    async def _add_error_response(self, error_message: str):
        """Add error response to chat (called from main thread)"""
        try:
            self.chat_component.add_system_message(f"Error: {error_message}")
        except Exception as e:
            print(f"Error adding error response: {e}")
    
    async def _set_processing_state(self, processing: bool):
        """Set the processing state and update UI accordingly"""
        try:
            self.is_processing = processing
            
            if self.send_button:
                self.send_button.text = "Thinking..." if processing else "Send"
                self.send_button.enabled = not processing
            
            if self.text_input:
                self.text_input.enabled = not processing
                
        except Exception as e:
            print(f"Error setting processing state: {e}")
    
    def _toggle_voice_listening(self, widget):
        """Handle microphone button press"""
        try:
            if not self.app.voice_manager or not self.app.voice_manager.is_voice_available():
                self.chat_component.add_system_message(
                    "Voice functionality not available. Please install required packages."
                )
                return
            
            # Toggle listening state
            if hasattr(self.app.voice_manager, 'is_listening') and self.app.voice_manager.is_listening:
                self.app.voice_manager.stop_listening()
            else:
                success = self.app.voice_manager.start_listening()
                if not success:
                    self.chat_component.add_system_message(
                        "Failed to start voice recognition."
                    )
                    
        except Exception as e:
            print(f"Error toggling voice listening: {e}")
            self.chat_component.add_system_message(f"Voice error: {e}")
    
    def set_input_text(self, text: str):
        """Set text in the input field (used by voice recognition)"""
        try:
            if self.text_input:
                self.text_input.value = text
        except Exception as e:
            print(f"Error setting input text: {e}")
    
    def clear_input(self):
        """Clear the input field"""
        try:
            if self.text_input:
                self.text_input.value = ""
        except Exception as e:
            print(f"Error clearing input: {e}")
    
    def update_voice_status(self, status: str):
        """Update voice status display"""
        try:
            if self.voice_status_label:
                self.voice_status_label.text = status.title()
            
            # Update microphone button appearance
            if self.mic_button:
                if status == "listening":
                    self.mic_button.text = "🔴"  # Red dot for recording
                else:
                    self.mic_button.text = "🎤"  # Microphone icon
                    
        except Exception as e:
            print(f"Error updating voice status: {e}")
    
    def update_theme(self, theme_name: str):
        """Update input component styling for new theme"""
        try:
            # Theme-specific styling updates would go here
            pass
        except Exception as e:
            print(f"Error updating input theme: {e}")
    
    def cleanup(self):
        """Clean up input component resources"""
        try:
            # Stop any ongoing voice operations
            if self.app.voice_manager and hasattr(self.app.voice_manager, 'stop_listening'):
                self.app.voice_manager.stop_listening()
        except Exception as e:
            print(f"Error during input cleanup: {e}")