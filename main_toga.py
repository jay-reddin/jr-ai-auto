"""
JR AI Control - Toga-based Cross-Platform Application

This is the main Toga application file that replaces the Tkinter-based UI
with a modern, cross-platform Toga interface while preserving all functionality.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import os
import threading
import uuid
from datetime import datetime
from pathlib import Path

# Import existing backend services
from utils.agent import create_jr_ai_agent
from utils.config_manager import ConfigurationManager
from utils.token_tracker import get_token_tracker
from utils.performance_monitor import get_performance_optimizer
from voice.voice_manager import get_voice_manager

# Import UI components
from ui.components.header import HeaderComponent
from ui.components.chat import ChatComponent


class JRAIControlApp(toga.App):
    """
    Main Toga application class for JR AI Control.
    
    This class inherits from toga.App and provides the core application
    structure, lifecycle management, and integration with existing backend services.
    """
    
    def startup(self):
        """
        Initialize the application and create the main window.
        
        This method is called automatically by Toga when the app starts.
        It sets up all the core components and creates the main interface.
        """
        # Initialize backend services
        self.initialize_backend_services()
        
        # Load configuration and settings
        self.load_settings()
        
        # Set up voice system
        self.setup_voice_system()
        
        # Create main window
        self.main_window = self.create_main_window()
        
        # Initialize agent if API key is available
        if self.current_api_key and self.current_api_key != "your_api_key_here":
            self.initialize_agent()
        
        # Show the main window
        self.main_window.show()
        
        # Add welcome messages after UI is ready
        self.add_welcome_messages()
        
        # Refresh token displays with current data
        self.refresh_token_displays()
    
    def initialize_backend_services(self):
        """Initialize all backend services and managers."""
        # Configuration manager
        self.config_manager = ConfigurationManager()
        
        # Token tracking
        self.token_tracker = get_token_tracker()
        
        # Performance monitoring
        self.performance_optimizer = get_performance_optimizer()
        
        # Voice system
        self.voice_manager = get_voice_manager()
        
        # Screenshot manager
        from utils.screenshot_manager import ScreenshotManager
        self.screenshot_manager = ScreenshotManager()
        
        # Application state
        self.agent_executor = None
        self.current_message_id = None
        self.is_listening = False
        
        # UI components
        self.header_component = None
        self.chat_component = None
        
        # Setup configuration change observer
        self.config_manager.add_observer(self._on_config_change)
        
        # Default configuration values
        self.current_api_key = ""
        self.current_model = "gemini-2.0-flash-exp"
        self.available_models = [
            "gemini-2.0-flash-exp",
            "gemini-1.5-pro", 
            "gemini-1.5-flash",
            "gemini-1.0-pro"
        ]
        self.theme_mode = "dark"
        self.speech_enabled = True
        self.speech_muted = False
        self.screenshot_size = "medium"
        self.screenshot_wait_duration = 3
        self.notifications_enabled = True
        self.font_size = 14
        self.window_opacity = 1.0
    
    def load_settings(self):
        """Load settings from the configuration manager."""
        try:
            config = self.config_manager.load_settings()
            
            # Load all settings from config manager
            self.current_api_key = config.get('api_key', '')
            self.current_model = config.get('model', 'gemini-2.0-flash-exp')
            self.theme_mode = config.get('theme_mode', 'dark')
            self.speech_enabled = config.get('speech_enabled', True)
            self.speech_muted = config.get('speech_muted', False)
            
            # UI settings
            self.screenshot_size = config.get('screenshot_size', 'medium')
            self.screenshot_wait_duration = config.get('screenshot_wait_duration', 3)
            self.notifications_enabled = config.get('notification_enabled', True)
            self.font_size = config.get('font_size', 14)
            self.window_opacity = config.get('window_opacity', 1.0)
            
            # Load voice settings
            if hasattr(self.voice_manager, 'voice_rate'):
                self.voice_manager.voice_rate = config.get('voice_rate', 200)
            if hasattr(self.voice_manager, 'voice_volume'):
                self.voice_manager.voice_volume = config.get('voice_volume', 0.8)
            if hasattr(self.voice_manager, 'recognition_language'):
                self.voice_manager.recognition_language = config.get('voice_language', 'en-US')
                
            # Load token tracking
            if hasattr(self.token_tracker, 'total_tokens'):
                self.token_tracker.total_tokens = config.get('total_tokens_used', 0)
            
            print("Settings loaded successfully")
            
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def _on_config_change(self, event_type, data):
        """Handle configuration changes for real-time updates."""
        try:
            if event_type == 'setting_changed':
                key = data.get('key')
                value = data.get('value')
                
                # Update application state based on changed setting
                if key == 'theme_mode':
                    self.theme_mode = value
                    # Update header component theme
                    if self.header_component:
                        self.header_component.update_theme(value)
                    # Update chat component theme
                    if self.chat_component:
                        self.chat_component.update_theme(value)
                elif key == 'speech_enabled':
                    self.speech_enabled = value
                    if self.voice_manager:
                        self.voice_manager.toggle_speech_enabled(value)
                elif key == 'speech_muted':
                    self.speech_muted = value
                    if self.voice_manager:
                        self.voice_manager.toggle_speech_muted(value)
                elif key == 'font_size':
                    self.font_size = value
                    # Font size updates would be applied to UI components here
                elif key == 'window_opacity':
                    self.window_opacity = value
                    # Window opacity updates would be applied here
                    
        except Exception as e:
            print(f"Error handling config change: {e}")
    
    def setup_voice_system(self):
        """Initialize voice system integration."""
        try:
            if self.voice_manager.is_voice_available():
                # Set up voice callbacks
                self.voice_manager.on_speech_recognized = self.on_speech_recognized
                self.voice_manager.on_listening_start = self.on_listening_start
                self.voice_manager.on_listening_stop = self.on_listening_stop
                self.voice_manager.on_error = self.on_voice_error
                
                # Apply saved voice settings
                self.voice_manager.toggle_speech_enabled(self.speech_enabled)
                self.voice_manager.toggle_speech_muted(self.speech_muted)
                
                print("Voice system initialized successfully")
            else:
                print("Voice system unavailable - continuing without voice features")
                
        except Exception as e:
            print(f"Error setting up voice system: {e}")
    
    def create_main_window(self):
        """
        Create and configure the main application window with proper layout system.
        
        Returns:
            toga.MainWindow: The configured main window
        """
        try:
            # Create main window with proper title and sizing
            main_window = toga.MainWindow(title=self.formal_name)
            
            # Set window size and position (similar to original Tkinter version)
            main_window.size = (600, 800)  # Width x Height
            main_window.position = (100, 100)  # X, Y position
            
            # Create main layout container using Pack layout with COLUMN direction
            main_box = toga.Box(style=Pack(
                direction=COLUMN,
                background_color='#1e1e1e' if self.theme_mode == 'dark' else '#ffffff'
            ))
            
            # Add header section (fixed height)
            self.header_component = HeaderComponent(self)
            header_section = self.header_component.get_container()
            main_box.add(header_section)
            
            # Add chat section (flexible, takes remaining space)
            self.chat_component = ChatComponent(self)
            chat_section = self.chat_component.get_container()
            main_box.add(chat_section)
            
            # Add input section (fixed height)
            input_section = self.create_input_section()
            main_box.add(input_section)
            
            # Set window content
            main_window.content = main_box
            
            return main_window
            
        except Exception as e:
            print(f"Error creating main window: {e}")
            return self.create_error_window(f"Failed to create main window: {e}")
    

 
   
    def create_input_section(self):
        """
        Create the input section with text field and controls.
        
        Returns:
            toga.Box: The input container with flexible height for multiline input
        """
        # Input container with flexible height and proper styling
        input_box = toga.Box(style=Pack(
            direction=ROW,
            margin=(16, 16, 16, 16),
            background_color='#2b2b2b' if self.theme_mode == 'dark' else '#f5f5f5',
            min_height=80,  # Minimum height for input area
            align_items='stretch'  # Allow components to stretch to container height
        ))
        
        # Multiline text input field (flexible width and height)
        self.input_field = toga.MultilineTextInput(
            placeholder="Type your message here...",
            style=Pack(
                flex=1, 
                margin_right=12,
                min_height=60,  # Minimum height for multiline input
                background_color='#404040' if self.theme_mode == 'dark' else '#ffffff',
                color='#ffffff' if self.theme_mode == 'dark' else '#000000'
            )
        )
        
        # Add input validation and character limit handling
        self._setup_input_validation()
        
        input_box.add(self.input_field)
        
        # Voice controls container (if available)
        if self.voice_manager.is_voice_available():
            voice_box = toga.Box(style=Pack(
                direction=ROW,
                margin_right=12
            ))
            
            self.mic_button = toga.Button(
                "🎤",
                on_press=self.toggle_listening,
                style=Pack(
                    width=50,
                    height=40,
                    background_color='#404040' if self.theme_mode == 'dark' else '#e0e0e0'
                )
            )
            voice_box.add(self.mic_button)
            input_box.add(voice_box)
        
        # Send button (fixed width)
        self.send_button = toga.Button(
            "Send",
            on_press=self.send_message,
            style=Pack(
                width=80,
                height=40,
                background_color='#0066cc',
                color='#ffffff'
            )
        )
        input_box.add(self.send_button)
        
        return input_box
    
    def _setup_input_validation(self):
        """Set up input validation and character limit handling for the multiline input."""
        # Character limit for input (to prevent extremely long messages)
        self.max_input_length = 10000
        
        # Store original on_change handler if it exists
        self._original_on_change = getattr(self.input_field, 'on_change', None)
        
        # Set up input change handler for validation
        self.input_field.on_change = self._on_input_change
    
    def _on_input_change(self, widget):
        """
        Handle input field changes for validation and character limiting.
        
        Args:
            widget: The MultilineTextInput widget that changed
        """
        try:
            current_text = widget.value or ""
            
            # Check character limit
            if len(current_text) > self.max_input_length:
                # Truncate to max length
                widget.value = current_text[:self.max_input_length]
                # Show warning message
                self.add_message("System", 
                    f"Message truncated to {self.max_input_length} characters maximum.")
            
            # Update send button state based on content
            if hasattr(self, 'send_button'):
                has_content = bool(current_text.strip())
                self.send_button.enabled = has_content and self.send_button.text == "Send"
            
            # Call original handler if it exists
            if self._original_on_change:
                self._original_on_change(widget)
                
        except Exception as e:
            print(f"Error in input validation: {e}")
    
    def add_welcome_messages(self):
        """Add welcome messages to the chat."""
        self.add_message("System", "Welcome to JR AI Control! 🚀")
        
        if self.voice_manager.is_voice_available():
            self.add_message("Voice System", 
                "Voice interaction ready! Click the microphone button to start listening.")
        else:
            self.add_message("Voice System", 
                "Voice features unavailable. Install speech_recognition, pyttsx3, and pyaudio for voice interaction.")
        
        if not self.current_api_key:
            self.add_message("System", 
                "Please configure your Gemini API key in settings to get started.")
    
    def add_message(self, sender, message, is_user=False, screenshot_id=None, tokens=0):
        """
        Add a message to the chat display using the new ChatComponent.
        
        Args:
            sender (str): The sender of the message
            message (str): The message content
            is_user (bool): Whether this is a user message
            screenshot_id (str, optional): Screenshot ID if message includes image
            tokens (int, optional): Number of tokens used for this message
        """
        if self.chat_component:
            # Use the new chat component to add messages
            self.chat_component.add_message(sender, message, is_user, screenshot_id, tokens)
            
            # Update token display if tokens were provided
            if tokens > 0:
                self.update_token_display(tokens)
        else:
            print(f"Chat component not available. Message: {sender}: {message}")
    
    def update_token_display(self, message_tokens):
        """Update the token display in the header."""
        if self.header_component:
            total_tokens = self.token_tracker.get_total_tokens() if self.token_tracker else 0
            self.header_component.update_token_display(message_tokens, total_tokens)
    
    def initialize_agent(self):
        """Initialize the AI agent with the current API key."""
        try:
            self.agent_executor = create_jr_ai_agent(
                api_key=self.current_api_key,
                model=self.current_model
            )
            self.add_message("System", f"AI agent initialized with {self.current_model}")
            
            # Update model display
            if self.header_component:
                self.header_component.update_model_display(self.current_model)
                self.header_component.update_connection_status(True)
            
        except Exception as e:
            self.add_message("System", f"Failed to initialize AI agent: {str(e)}")
    
    def send_message(self, widget):
        """
        Send a message to the AI agent.
        
        Args:
            widget: The button widget that triggered this action
        """
        # Get and validate message content
        message = self.input_field.value.strip() if self.input_field.value else ""
        if not message:
            return
        
        if not self.agent_executor:
            self.add_message("System", "Please configure your API key in settings first.")
            return
        
        # Validate message length
        if len(message) > self.max_input_length:
            self.add_message("System", 
                f"Message too long. Maximum {self.max_input_length} characters allowed.")
            return
        
        # Clear input field
        self.input_field.value = ""
        
        # Add user message (preserve line breaks for multiline messages)
        self.add_message("You", message, is_user=True)
        
        # Disable send button while processing
        self.send_button.text = "Thinking..."
        self.send_button.enabled = False
        
        # Process message in background thread
        threading.Thread(
            target=self.process_message_async,
            args=(message,),
            daemon=True
        ).start()
    
    def process_message_async(self, message):
        """
        Process the message with the AI agent in a background thread.
        
        Args:
            message (str): The user message to process
        """
        try:
            # Generate unique message ID
            self.current_message_id = str(uuid.uuid4())
            
            # Get AI response
            response = self.agent_executor.invoke({"input": message})
            output = response.get('output', 'No response received.')
            
            # Extract screenshot ID from intermediate steps if available
            screenshot_id = None
            intermediate_steps = response.get('intermediate_steps', [])
            
            for step in intermediate_steps:
                if len(step) >= 2:
                    action, observation = step
                    # Check if this was a get_screen_info tool call
                    if hasattr(action, 'tool') and action.tool == 'get_screen_info':
                        # The observation should be the tool result
                        if isinstance(observation, dict) and 'screenshot_id' in observation:
                            screenshot_id = observation['screenshot_id']
                            break
                        elif isinstance(observation, str):
                            # Try to parse if it's a string representation of dict
                            try:
                                import ast
                                parsed = ast.literal_eval(observation)
                                if isinstance(parsed, dict) and 'screenshot_id' in parsed:
                                    screenshot_id = parsed['screenshot_id']
                                    break
                            except:
                                pass
            
            # Track tokens
            tokens_used = 0
            if self.current_message_id and self.token_tracker:
                tokens_used = self.token_tracker.track_message(
                    self.current_message_id, message, output, self.current_model
                )
            
            # Update UI in main thread
            self.main_window.app.add_background_task(
                self.update_ui_after_response(output, tokens_used, screenshot_id)
            )
            
        except Exception as e:
            # Handle errors in main thread
            self.main_window.app.add_background_task(
                self.handle_response_error(str(e))
            )
    
    async def update_ui_after_response(self, output, tokens_used, screenshot_id=None):
        """
        Update the UI after receiving an AI response.
        
        Args:
            output (str): The AI response
            tokens_used (int): Number of tokens used
            screenshot_id (str, optional): Screenshot ID if response includes image
        """
        # Add AI response with screenshot if available
        self.add_message("AI", output, is_user=False, screenshot_id=screenshot_id, tokens=tokens_used)
        
        # Update token display
        if tokens_used > 0:
            self.update_token_display(tokens_used)
        
        # Re-enable send button
        self.send_button.text = "Send"
        self.send_button.enabled = True
    
    async def handle_response_error(self, error_message):
        """
        Handle errors from AI response processing.
        
        Args:
            error_message (str): The error message
        """
        self.add_message("System", f"Error: {error_message}")
        
        # Re-enable send button
        self.send_button.text = "Send"
        self.send_button.enabled = True
    
    def toggle_listening(self, widget):
        """
        Toggle voice listening on/off.
        
        Args:
            widget: The button widget that triggered this action
        """
        if not self.voice_manager.is_voice_available():
            self.add_message("Voice System", "Voice functionality not available.")
            return
        
        try:
            if self.is_listening:
                self.voice_manager.stop_listening()
                self.is_listening = False
                self.mic_button.text = "🎤"
            else:
                self.voice_manager.start_listening()
                self.is_listening = True
                self.mic_button.text = "🔴"
            
            # Update header component voice status
            if self.header_component:
                self.header_component.update_voice_status(self.is_listening)
                
        except Exception as e:
            self.add_message("Voice System", f"Voice error: {str(e)}")
    
    def on_speech_recognized(self, text):
        """Handle recognized speech from voice system."""
        if hasattr(self, 'input_field') and text:
            # Get current input content
            current_text = self.input_field.value or ""
            
            # If there's existing text, add the new text on a new line
            if current_text.strip():
                new_text = current_text + "\n" + text
            else:
                new_text = text
            
            # Update input field with recognized text
            self.input_field.value = new_text
            
            # Optionally auto-send the message (disabled by default for multiline)
            # self.send_message(None)
    
    def refresh_token_displays(self):
        """Refresh token displays with current data."""
        if self.header_component:
            self.header_component.refresh_token_display()
    
    def on_listening_start(self):
        """Handle voice listening start."""
        self.is_listening = True
        if hasattr(self, 'mic_button'):
            self.mic_button.text = "🔴"  # Red dot for recording
            # Update button styling to indicate active listening
            self.mic_button.style.background_color = '#ff4444'
    
    def on_listening_stop(self):
        """Handle voice listening stop."""
        self.is_listening = False
        if hasattr(self, 'mic_button'):
            self.mic_button.text = "🎤"  # Microphone icon
            # Reset button styling
            self.mic_button.style.background_color = '#404040' if self.theme_mode == 'dark' else '#e0e0e0'
    
    def on_voice_error(self, error_message):
        """Handle voice system errors."""
        self.add_message("Voice System", f"Voice Error: {error_message}")
        # Reset listening state on error
        self.is_listening = False
        if hasattr(self, 'mic_button'):
            self.mic_button.text = "🎤"
            self.mic_button.style.background_color = '#404040' if self.theme_mode == 'dark' else '#e0e0e0'
    
    def toggle_theme(self, widget):
        """
        Toggle between light and dark themes.
        
        Args:
            widget: The button widget that triggered this action
        """
        # Toggle theme mode
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        
        # Update header component theme
        if self.header_component:
            self.header_component.update_theme(self.theme_mode)
        
        # Update chat component theme
        if self.chat_component:
            self.chat_component.update_theme(self.theme_mode)
        
        # Update input field theme
        self._update_input_theme()
        
        # Save theme preference
        if self.config_manager:
            self.config_manager.set_setting('theme_mode', self.theme_mode)
        
        # Add message about theme change
        self.add_message("System", f"Switched to {self.theme_mode} theme")
    
    def _update_input_theme(self):
        """Update input field styling based on current theme."""
        if hasattr(self, 'input_field'):
            # Update input field colors
            self.input_field.style.background_color = (
                '#404040' if self.theme_mode == 'dark' else '#ffffff'
            )
            self.input_field.style.color = (
                '#ffffff' if self.theme_mode == 'dark' else '#000000'
            )
        
        # Update voice button theme if it exists
        if hasattr(self, 'mic_button'):
            self.mic_button.style.background_color = (
                '#404040' if self.theme_mode == 'dark' else '#e0e0e0'
            )
    
    def open_settings(self, widget):
        """
        Open the settings window.
        
        Args:
            widget: The button widget that triggered this action
        """
        # For now, just show a placeholder message
        # This will be implemented in later tasks
        self.add_message("System", "Settings window will be implemented in the next phase.")
    
    def create_error_window(self, error_message):
        """
        Create a simple error display window.
        
        Args:
            error_message (str): The error message to display
            
        Returns:
            toga.MainWindow: Error window
        """
        try:
            error_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
            
            error_label = toga.Label(
                f"Error: {error_message}",
                style=Pack(padding=10, text_align="center")
            )
            error_box.add(error_label)
            
            close_button = toga.Button(
                "Close",
                on_press=self.exit,
                style=Pack(padding=10)
            )
            error_box.add(close_button)
            
            error_window = toga.MainWindow(title="JR AI Control - Error")
            error_window.content = error_box
            
            return error_window
            
        except Exception as e:
            print(f"Failed to create error window: {e}")
            # Return a minimal window as fallback
            return toga.MainWindow(title="JR AI Control - Critical Error")
    
    def save_configuration(self):
        """Save current configuration using config manager."""
        try:
            config_updates = {
                'api_key': self.current_api_key,
                'model': self.current_model,
                'theme_mode': self.theme_mode,
                'speech_enabled': self.speech_enabled,
                'speech_muted': self.speech_muted,
                'font_size': self.font_size,
                'window_opacity': self.window_opacity,
                'screenshot_size': self.screenshot_size,
                'screenshot_wait_duration': self.screenshot_wait_duration,
                'notification_enabled': self.notifications_enabled,
            }
            
            # Add voice settings if available
            if self.voice_manager:
                config_updates.update({
                    'voice_rate': getattr(self.voice_manager, 'voice_rate', 200),
                    'voice_volume': getattr(self.voice_manager, 'voice_volume', 0.8),
                    'voice_language': getattr(self.voice_manager, 'recognition_language', 'en-US'),
                })
            
            # Add token tracking
            if self.token_tracker:
                config_updates['total_tokens_used'] = getattr(self.token_tracker, 'total_tokens', 0)
            
            success = self.config_manager.save_settings(config_updates)
            if not success:
                print("Warning: Failed to save settings")
                
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def get_setting(self, key, default=None):
        """Get a setting value from config manager."""
        return self.config_manager.get_setting(key, default)
    
    def set_setting(self, key, value, save_immediately=True):
        """Set a setting value using config manager."""
        return self.config_manager.set_setting(key, value, save_immediately)
    
    def cleanup_resources(self):
        """Clean up resources when application exits."""
        try:
            # Save current configuration
            self.save_configuration()
            
            # Stop voice system
            if self.voice_manager and self.is_listening:
                self.voice_manager.stop_listening()
            
            # Clean up screenshot manager caches
            if hasattr(self.screenshot_manager, '_cleanup_cache'):
                self.screenshot_manager._cleanup_cache()
            
            # Stop performance monitoring
            if hasattr(self.performance_optimizer, 'stop_monitoring'):
                self.performance_optimizer.stop_monitoring()
                
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    def on_exit(self):
        """Handle application exit."""
        self.cleanup_resources()
        return True


def main():
    """Main entry point for the Toga application."""
    return JRAIControlApp(
        'JR AI Control',
        'com.jraicontrol.toga'
    )


if __name__ == '__main__':
    app = main()
    app.main_loop()