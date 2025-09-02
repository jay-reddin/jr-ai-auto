"""
Main Window Component for Toga-based JR AI Control
Manages the primary application window layout and coordination
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from typing import Optional

from .header_component import HeaderComponent
from .chat_component import ChatComponent
from .input_component import InputComponent


class MainWindow:
    """
    Main window component that coordinates the application layout
    Manages header, chat, and input areas using Toga widgets
    """
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.header_component: Optional[HeaderComponent] = None
        self.chat_component: Optional[ChatComponent] = None
        self.input_component: Optional[InputComponent] = None
        
        # Create the main window
        self.window = toga.MainWindow(title="JR AI Control")
        self.app.main_window = self.window
    
    def create_layout(self):
        """Create the main window layout with header, chat, and input areas"""
        try:
            # Main container with vertical layout
            main_container = toga.Box(
                style=Pack(
                    direction=COLUMN,
                    padding=10,
                    flex=1
                )
            )
            
            # Create header component
            self.header_component = HeaderComponent(self.app)
            header_widget = self.header_component.create_header_layout()
            main_container.add(header_widget)
            
            # Create chat component (takes most of the space)
            self.chat_component = ChatComponent(self.app)
            chat_widget = self.chat_component.create_chat_layout()
            main_container.add(chat_widget)
            
            # Create input component
            self.input_component = InputComponent(self.app, self.chat_component)
            input_widget = self.input_component.create_input_layout()
            main_container.add(input_widget)
            
            # Set the main window content
            self.window.content = main_container
            
            # Show the window
            self.window.show()
            
            # Add welcome messages
            self._add_welcome_messages()
            
        except Exception as e:
            print(f"Error creating main window layout: {e}")
            self._create_error_layout(str(e))
    
    def _create_error_layout(self, error_message: str):
        """Create a simple error layout if main layout creation fails"""
        try:
            error_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
            
            error_label = toga.Label(
                f"Failed to create main layout: {error_message}",
                style=Pack(padding=10, text_align="center")
            )
            error_box.add(error_label)
            
            retry_button = toga.Button(
                "Retry",
                on_press=self._retry_layout_creation,
                style=Pack(padding=10)
            )
            error_box.add(retry_button)
            
            self.window.content = error_box
            self.window.show()
            
        except Exception as e:
            print(f"Failed to create error layout: {e}")
    
    def _retry_layout_creation(self, widget):
        """Retry creating the main layout"""
        self.create_layout()
    
    def _add_welcome_messages(self):
        """Add welcome messages to the chat"""
        try:
            if self.chat_component:
                # Welcome message
                self.chat_component.add_system_message(
                    "Welcome to JR AI Control (Toga Edition)! 🚀"
                )
                
                # Voice system status
                if self.app.voice_manager and self.app.voice_manager.is_voice_available():
                    self.chat_component.add_system_message(
                        "Voice interaction ready! Use the microphone button to start voice input."
                    )
                else:
                    self.chat_component.add_system_message(
                        "Voice features unavailable. Install speech_recognition, pyttsx3, and pyaudio for voice interaction."
                    )
                
                # API key status
                if not self.app.api_key or self.app.api_key == "your_api_key_here":
                    self.chat_component.add_system_message(
                        "Please configure your Gemini API key in settings to get started."
                    )
                else:
                    self.chat_component.add_system_message(
                        f"Connected with model: {self.app.current_model}"
                    )
                    
        except Exception as e:
            print(f"Error adding welcome messages: {e}")
    
    def update_theme(self, theme_name: str):
        """Update the theme for all components"""
        try:
            if self.header_component:
                self.header_component.update_theme(theme_name)
            if self.chat_component:
                self.chat_component.update_theme(theme_name)
            if self.input_component:
                self.input_component.update_theme(theme_name)
                
        except Exception as e:
            print(f"Error updating theme: {e}")
    
    def cleanup(self):
        """Clean up resources when the window is closed"""
        try:
            if self.chat_component:
                self.chat_component.cleanup()
            if self.input_component:
                self.input_component.cleanup()
            if self.header_component:
                self.header_component.cleanup()
                
        except Exception as e:
            print(f"Error during cleanup: {e}")