#!/usr/bin/env python3
"""
Test script for the migrated chat interface components.

This script tests the new ChatComponent and MessageWidget implementations
to ensure they work correctly with the Toga framework.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.components.chat import ChatComponent
from ui.components.message_widget import MessageWidget


class TestChatApp(toga.App):
    """Test application for chat component migration."""
    
    def startup(self):
        """Initialize the test application."""
        # Mock app properties needed by chat component
        self.theme_mode = "dark"
        self.screenshot_manager = None
        self.token_tracker = None
        self.voice_manager = None
        self.config_manager = None
        
        # Create main window
        self.main_window = toga.MainWindow(title="Chat Migration Test")
        
        # Create main container
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        
        # Add title
        title_label = toga.Label(
            "Chat Component Migration Test",
            style=Pack(
                font_size=18,
                font_weight='bold',
                margin_bottom=20,
                text_align='center'
            )
        )
        main_box.add(title_label)
        
        # Create chat component
        self.chat_component = ChatComponent(self)
        chat_container = self.chat_component.get_container()
        main_box.add(chat_container)
        
        # Add test controls
        controls_box = toga.Box(style=Pack(
            direction=ROW,
            margin_top=20,
            align_items='center'
        ))
        
        # Add test message buttons
        add_user_btn = toga.Button(
            "Add User Message",
            on_press=self.add_test_user_message,
            style=Pack(margin_right=10)
        )
        controls_box.add(add_user_btn)
        
        add_ai_btn = toga.Button(
            "Add AI Message",
            on_press=self.add_test_ai_message,
            style=Pack(margin_right=10)
        )
        controls_box.add(add_ai_btn)
        
        clear_btn = toga.Button(
            "Clear Chat",
            on_press=self.clear_chat,
            style=Pack(margin_right=10)
        )
        controls_box.add(clear_btn)
        
        theme_btn = toga.Button(
            "Toggle Theme",
            on_press=self.toggle_theme,
        )
        controls_box.add(theme_btn)
        
        main_box.add(controls_box)
        
        # Set window content
        self.main_window.content = main_box
        self.main_window.show()
        
        # Add initial test messages
        self.add_initial_messages()
    
    def add_initial_messages(self):
        """Add some initial test messages."""
        self.chat_component.add_message(
            "System",
            "Welcome to the Chat Component Migration Test! 🚀",
            is_user=False
        )
        
        self.chat_component.add_message(
            "You",
            "Hello, this is a test user message with some longer content to test text wrapping and layout.",
            is_user=True,
            tokens=25
        )
        
        self.chat_component.add_message(
            "AI",
            "This is a test AI response. The chat component has been successfully migrated to use Toga widgets with proper scrolling, message alignment, and action buttons.",
            is_user=False,
            tokens=42
        )
    
    def add_test_user_message(self, widget):
        """Add a test user message."""
        import random
        messages = [
            "This is a test user message.",
            "Can you help me with something?",
            "How does the new chat interface work?",
            "Testing the message action buttons.",
            "This is a longer message to test text wrapping and see how it displays in the new Toga-based chat interface."
        ]
        
        message = random.choice(messages)
        tokens = random.randint(10, 50)
        
        self.chat_component.add_message(
            "You",
            message,
            is_user=True,
            tokens=tokens
        )
    
    def add_test_ai_message(self, widget):
        """Add a test AI message."""
        import random
        messages = [
            "This is a test AI response using the new Toga components.",
            "The chat interface has been successfully migrated! All message features are working correctly.",
            "You can use the action buttons to resend, copy, or delete messages.",
            "The new implementation supports proper message alignment, timestamps, and token counting.",
            "Screenshots will be displayed as clickable thumbnails when available."
        ]
        
        message = random.choice(messages)
        tokens = random.randint(20, 80)
        
        self.chat_component.add_message(
            "AI",
            message,
            is_user=False,
            tokens=tokens
        )
    
    def clear_chat(self, widget):
        """Clear all chat messages."""
        self.chat_component.clear_chat()
        self.chat_component.add_message(
            "System",
            "Chat cleared! Add new messages using the buttons above.",
            is_user=False
        )
    
    def toggle_theme(self, widget):
        """Toggle between dark and light themes."""
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        self.chat_component.update_theme(self.theme_mode)
        
        self.chat_component.add_message(
            "System",
            f"Theme switched to {self.theme_mode} mode",
            is_user=False
        )


def main():
    """Run the test application."""
    app = TestChatApp("Chat Migration Test", "org.example.chattest")
    app.main_loop()


if __name__ == "__main__":
    main()