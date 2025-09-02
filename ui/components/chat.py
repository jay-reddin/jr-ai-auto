"""
Chat Component for JR AI Control - Toga Implementation

This module provides the chat interface component with scrollable message display,
proper message alignment, and support for screenshots and message actions using Toga widgets.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime
import os


class ChatComponent:
    """
    Chat component that displays conversation history in a scrollable format
    with proper message alignment and support for screenshots and actions.
    """
    
    def __init__(self, app_instance):
        """
        Initialize the chat component.
        
        Args:
            app_instance: The main application instance for accessing configuration and services
        """
        self.app = app_instance
        self.theme_mode = app_instance.theme_mode
        
        # Initialize component references
        self.chat_container = None
        self.messages_box = None
        self.message_widgets = []  # Keep track of message widgets for management
        
        # Create the chat layout
        self.create_chat_layout()
    
    def create_chat_layout(self):
        """
        Create scrollable chat container using toga.ScrollContainer.
        Replace tk.Text widget with toga.ScrollContainer.
        Implement chat message container using toga.Box with COLUMN direction.
        Set up automatic scrolling to bottom for new messages.
        Configure proper sizing and flex properties for responsive layout.
        
        Returns:
            toga.ScrollContainer: The complete chat container
        """
        # Create scrollable container for chat messages (flexible height)
        # Takes all remaining space between header and input sections
        self.chat_container = toga.ScrollContainer(
            style=Pack(
                flex=1,  # Takes all remaining space between header and input
                margin=(8, 16, 8, 16),
                background_color=self._get_chat_bg_color()
            )
        )
        
        # Create box to hold messages with proper spacing using COLUMN direction
        # This container will grow as messages are added
        self.messages_box = toga.Box(style=Pack(
            direction=COLUMN,
            margin=8
        ))
        
        # Set the messages box as the content of the scroll container
        self.chat_container.content = self.messages_box
        
        return self.chat_container
    
    def add_message(self, sender, content, is_user=False, screenshot_id=None, tokens=0):
        """
        Add new message to chat display with proper alignment and styling.
        
        Args:
            sender (str): The sender of the message
            content (str): The message content
            is_user (bool): Whether this is a user message (affects alignment)
            screenshot_id (str, optional): Screenshot ID if message includes image
            tokens (int, optional): Number of tokens used for this message
            
        Returns:
            MessageWidget: The created message widget
        """
        # Create message data dictionary
        message_data = {
            'sender': sender,
            'content': content,
            'is_user': is_user,
            'screenshot_id': screenshot_id,
            'tokens': tokens,
            'timestamp': datetime.now()
        }
        
        # Create message widget
        message_widget = self.create_message_widget(message_data)
        
        # Add to messages container
        self.messages_box.add(message_widget.get_container())
        
        # Keep track of message widgets
        self.message_widgets.append(message_widget)
        
        # Automatically scroll to bottom to show new message
        self.scroll_to_bottom()
        
        return message_widget
    
    def create_message_widget(self, message_data):
        """
        Create individual message widget with proper styling and alignment.
        
        Args:
            message_data (dict): Dictionary containing message information
            
        Returns:
            MessageWidget: The created message widget
        """
        from .message_widget import MessageWidget
        return MessageWidget(self, message_data)
    
    def scroll_to_bottom(self):
        """
        Scroll chat to show latest message automatically.
        This ensures new messages are always visible to the user.
        """
        # Note: Toga's ScrollContainer doesn't have direct scroll control
        # The container should automatically show the bottom when content is added
        # This is a placeholder for future implementation if Toga adds scroll control
        pass
    
    def clear_chat(self):
        """
        Clear all messages from the chat display.
        Useful for starting fresh conversations or cleanup.
        """
        # Remove all message widgets from the container
        for widget in self.message_widgets:
            try:
                self.messages_box.remove(widget.get_container())
            except Exception as e:
                print(f"Error removing message widget: {e}")
        
        # Clear the message widgets list
        self.message_widgets.clear()
    
    def update_theme(self, theme_mode):
        """
        Update chat styling according to the current theme.
        
        Args:
            theme_mode (str): The theme mode ('dark' or 'light')
        """
        self.theme_mode = theme_mode
        
        # Update chat container background
        if self.chat_container:
            self.chat_container.style.background_color = self._get_chat_bg_color()
        
        # Update all existing message widgets
        for message_widget in self.message_widgets:
            if hasattr(message_widget, 'update_theme'):
                message_widget.update_theme(theme_mode)
    
    def get_message_count(self):
        """
        Get the current number of messages in the chat.
        
        Returns:
            int: Number of messages currently displayed
        """
        return len(self.message_widgets)
    
    def remove_message(self, message_widget):
        """
        Remove a specific message from the chat display.
        
        Args:
            message_widget: The MessageWidget instance to remove
        """
        try:
            # Remove from UI
            self.messages_box.remove(message_widget.get_container())
            
            # Remove from tracking list
            if message_widget in self.message_widgets:
                self.message_widgets.remove(message_widget)
                
        except Exception as e:
            print(f"Error removing message: {e}")
    
    def _get_chat_bg_color(self):
        """Get chat background color based on theme."""
        return '#1a1a1a' if self.theme_mode == 'dark' else '#ffffff'
    
    def get_container(self):
        """
        Get the chat container widget.
        
        Returns:
            toga.ScrollContainer: The chat container
        """
        return self.chat_container