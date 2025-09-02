"""
Chat Component for Toga-based JR AI Control
Manages the chat display area with message history and scrolling
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime
from typing import List, Optional, Dict, Any


class MessageWidget:
    """Individual message widget for displaying chat messages"""
    
    def __init__(self, sender: str, content: str, is_user: bool, timestamp: datetime = None, tokens: int = 0):
        self.sender = sender
        self.content = content
        self.is_user = is_user
        self.timestamp = timestamp or datetime.now()
        self.tokens = tokens
        self.widget: Optional[toga.Box] = None
    
    def create_widget(self) -> toga.Box:
        """Create the Toga widget for this message"""
        try:
            # Main message container
            message_box = toga.Box(
                style=Pack(
                    direction=COLUMN,
                    padding=(5, 10, 5, 10),
                    alignment="right" if self.is_user else "left"
                )
            )
            
            # Message header with sender and timestamp
            header_box = toga.Box(style=Pack(direction=ROW))
            
            sender_label = toga.Label(
                self.sender,
                style=Pack(
                    font_weight="bold",
                    font_size=12,
                    padding=(0, 5, 0, 0)
                )
            )
            header_box.add(sender_label)
            
            time_str = self.timestamp.strftime("%H:%M:%S")
            time_label = toga.Label(
                time_str,
                style=Pack(
                    font_size=10,
                    padding=(0, 0, 0, 5)
                )
            )
            header_box.add(time_label)
            
            # Add token count if available
            if self.tokens > 0:
                token_label = toga.Label(
                    f"({self.tokens} tokens)",
                    style=Pack(
                        font_size=10,
                        padding=(0, 0, 0, 5)
                    )
                )
                header_box.add(token_label)
            
            message_box.add(header_box)
            
            # Message content
            content_label = toga.Label(
                self.content,
                style=Pack(
                    padding=(2, 0, 5, 0),
                    font_size=14
                )
            )
            message_box.add(content_label)
            
            # Message actions (for non-system messages)
            if self.sender not in ["System", "Voice System"]:
                actions_box = self._create_actions_box()
                message_box.add(actions_box)
            
            self.widget = message_box
            return message_box
            
        except Exception as e:
            print(f"Error creating message widget: {e}")
            # Return a simple fallback
            return toga.Box(
                children=[
                    toga.Label(f"{self.sender}: {self.content}")
                ],
                style=Pack(padding=5)
            )
    
    def _create_actions_box(self) -> toga.Box:
        """Create message action buttons"""
        actions_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding=(2, 0, 0, 0)
            )
        )
        
        # Copy button
        copy_button = toga.Button(
            "📋",
            on_press=self._copy_message,
            style=Pack(
                width=30,
                padding=(0, 2, 0, 0)
            )
        )
        actions_box.add(copy_button)
        
        # Resend button (for user messages)
        if self.is_user:
            resend_button = toga.Button(
                "🔄",
                on_press=self._resend_message,
                style=Pack(
                    width=30,
                    padding=(0, 2, 0, 0)
                )
            )
            actions_box.add(resend_button)
        
        # Delete button
        delete_button = toga.Button(
            "🗑️",
            on_press=self._delete_message,
            style=Pack(
                width=30,
                padding=(0, 0, 0, 2)
            )
        )
        actions_box.add(delete_button)
        
        return actions_box
    
    def _copy_message(self, widget):
        """Copy message content to clipboard"""
        try:
            # Note: Toga doesn't have built-in clipboard support yet
            # This would need to be implemented with platform-specific code
            print(f"Copy message: {self.content}")
        except Exception as e:
            print(f"Error copying message: {e}")
    
    def _resend_message(self, widget):
        """Resend this message"""
        try:
            # This would trigger a callback to resend the message
            print(f"Resend message: {self.content}")
        except Exception as e:
            print(f"Error resending message: {e}")
    
    def _delete_message(self, widget):
        """Delete this message"""
        try:
            if self.widget and self.widget.parent:
                self.widget.parent.remove(self.widget)
        except Exception as e:
            print(f"Error deleting message: {e}")


class ChatComponent:
    """
    Chat component that manages the conversation display
    """
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.messages: List[MessageWidget] = []
        self.chat_container: Optional[toga.ScrollContainer] = None
        self.messages_box: Optional[toga.Box] = None
    
    def create_chat_layout(self) -> toga.ScrollContainer:
        """Create the scrollable chat layout"""
        try:
            # Messages container box
            self.messages_box = toga.Box(
                style=Pack(
                    direction=COLUMN,
                    padding=5
                )
            )
            
            # Scrollable container for messages
            self.chat_container = toga.ScrollContainer(
                content=self.messages_box,
                style=Pack(
                    flex=1,
                    padding=(5, 0, 5, 0)
                )
            )
            
            return self.chat_container
            
        except Exception as e:
            print(f"Error creating chat layout: {e}")
            # Return a simple fallback
            fallback_box = toga.Box(
                children=[
                    toga.Label("Chat display error - please restart the application")
                ],
                style=Pack(padding=10)
            )
            return toga.ScrollContainer(content=fallback_box)
    
    def add_message(self, sender: str, content: str, is_user: bool = False, 
                   screenshot_id: str = None, tokens: int = 0) -> MessageWidget:
        """Add a new message to the chat"""
        try:
            # Create message widget
            message = MessageWidget(
                sender=sender,
                content=content,
                is_user=is_user,
                tokens=tokens
            )
            
            # Create and add the widget
            message_widget = message.create_widget()
            if self.messages_box:
                self.messages_box.add(message_widget)
            
            # Add to messages list
            self.messages.append(message)
            
            # Scroll to bottom to show new message
            self._scroll_to_bottom()
            
            return message
            
        except Exception as e:
            print(f"Error adding message: {e}")
            return None
    
    def add_system_message(self, content: str) -> MessageWidget:
        """Add a system message to the chat"""
        return self.add_message("System", content, is_user=False)
    
    def add_user_message(self, content: str) -> MessageWidget:
        """Add a user message to the chat"""
        return self.add_message("You", content, is_user=True)
    
    def add_ai_message(self, content: str, tokens: int = 0) -> MessageWidget:
        """Add an AI response message to the chat"""
        model_name = getattr(self.app, 'current_model', 'AI')
        return self.add_message(model_name, content, is_user=False, tokens=tokens)
    
    def _scroll_to_bottom(self):
        """Scroll the chat to show the latest message"""
        try:
            if self.chat_container:
                # Note: Toga's ScrollContainer doesn't have direct scroll control yet
                # This is a placeholder for when the feature becomes available
                pass
        except Exception as e:
            print(f"Error scrolling to bottom: {e}")
    
    def clear_chat(self):
        """Clear all messages from the chat"""
        try:
            if self.messages_box:
                # Remove all message widgets
                for message in self.messages:
                    if message.widget:
                        self.messages_box.remove(message.widget)
            
            # Clear messages list
            self.messages.clear()
            
        except Exception as e:
            print(f"Error clearing chat: {e}")
    
    def get_message_count(self) -> int:
        """Get the current number of messages"""
        return len(self.messages)
    
    def get_last_message(self) -> Optional[MessageWidget]:
        """Get the last message in the chat"""
        return self.messages[-1] if self.messages else None
    
    def remove_message(self, message: MessageWidget):
        """Remove a specific message from the chat"""
        try:
            if message in self.messages:
                # Remove widget from UI
                if message.widget and self.messages_box:
                    self.messages_box.remove(message.widget)
                
                # Remove from messages list
                self.messages.remove(message)
                
        except Exception as e:
            print(f"Error removing message: {e}")
    
    def update_theme(self, theme_name: str):
        """Update chat styling for new theme"""
        try:
            # Theme-specific styling updates would go here
            # For now, this is a placeholder
            pass
        except Exception as e:
            print(f"Error updating chat theme: {e}")
    
    def cleanup(self):
        """Clean up chat resources"""
        try:
            self.clear_chat()
        except Exception as e:
            print(f"Error during chat cleanup: {e}")