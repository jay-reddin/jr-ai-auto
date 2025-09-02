"""
Chat Component for Toga UI

This component manages the chat interface with message display,
screenshot thumbnails, and message actions.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime


class MessageWidget:
    """
    Individual message widget for displaying chat messages.
    
    This replaces the custom message widgets from the Tkinter version.
    """
    
    def __init__(self, parent, sender, message, is_user=False, screenshot_id=None, tokens=0, is_error=False):
        """
        Initialize a message widget.
        
        Args:
            parent: Parent container
            sender: Message sender name
            message: Message content
            is_user: True if this is a user message
            screenshot_id: ID of associated screenshot (optional)
            tokens: Number of tokens used (optional)
            is_error: True if this is an error message
        """
        self.parent = parent
        self.sender = sender
        self.message = message
        self.is_user = is_user
        self.screenshot_id = screenshot_id
        self.tokens = tokens
        self.is_error = is_error
        self.timestamp = datetime.now()
        
        # Create the message widget
        self.widget = self.create_message_widget()
    
    def create_message_widget(self):
        """
        Create the message widget layout.
        
        Returns:
            toga.Box: The message widget container
        """
        # Message container
        message_container = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=10,
                background_color=self.get_background_color()
            )
        )
        
        # Header with sender and timestamp
        header_box = toga.Box(style=Pack(direction=ROW, padding_bottom=5))
        
        sender_label = toga.Label(
            self.sender,
            style=Pack(
                font_weight='bold',
                color=self.get_text_color(),
                flex=1
            )
        )
        header_box.add(sender_label)
        
        timestamp_label = toga.Label(
            self.timestamp.strftime("%H:%M:%S"),
            style=Pack(
                font_size=10,
                color=self.get_secondary_text_color()
            )
        )
        header_box.add(timestamp_label)
        
        message_container.add(header_box)
        
        # Message content
        content_label = toga.Label(
            self.message,
            style=Pack(
                color=self.get_text_color(),
                padding_bottom=5,
                text_align='left' if not self.is_user else 'right'
            )
        )
        message_container.add(content_label)
        
        # Screenshot thumbnail if available
        if self.screenshot_id:
            screenshot_widget = self.create_screenshot_thumbnail()
            if screenshot_widget:
                message_container.add(screenshot_widget)
        
        # Token count if available
        if self.tokens > 0:
            token_label = toga.Label(
                f"Tokens: {self.tokens:,}",
                style=Pack(
                    font_size=10,
                    color=self.get_secondary_text_color(),
                    padding_bottom=5
                )
            )
            message_container.add(token_label)
        
        # Message actions
        actions_box = self.create_message_actions()
        if actions_box:
            message_container.add(actions_box)
        
        return message_container
    
    def create_screenshot_thumbnail(self):
        """
        Create a screenshot thumbnail widget.
        
        Returns:
            toga.ImageView or None: The thumbnail widget
        """
        try:
            # Try to load the screenshot image
            # Note: This would need to be implemented with actual screenshot loading
            # For now, we'll create a placeholder
            placeholder = toga.Label(
                f"📷 Screenshot: {self.screenshot_id[:8]}...",
                style=Pack(
                    padding=5,
                    background_color='#444444',
                    color='#ffffff'
                )
            )
            return placeholder
        except Exception as e:
            print(f"Error creating screenshot thumbnail: {e}")
            return None
    
    def create_message_actions(self):
        """
        Create message action buttons.
        
        Returns:
            toga.Box: Container with action buttons
        """
        actions_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding_top=5
            )
        )
        
        # Copy button
        copy_button = toga.Button(
            "📋",
            on_press=self.handle_copy,
            style=Pack(
                width=30,
                padding_right=5
            )
        )
        actions_box.add(copy_button)
        
        # Resend button (only for user messages)
        if self.is_user:
            resend_button = toga.Button(
                "🔄",
                on_press=self.handle_resend,
                style=Pack(
                    width=30,
                    padding_right=5
                )
            )
            actions_box.add(resend_button)
        
        # Delete button
        delete_button = toga.Button(
            "🗑️",
            on_press=self.handle_delete,
            style=Pack(
                width=30
            )
        )
        actions_box.add(delete_button)
        
        return actions_box
    
    def handle_copy(self, widget):
        """Handle copy button press."""
        # Copy message to clipboard
        # Note: Toga doesn't have built-in clipboard support yet
        # This would need to be implemented with platform-specific code
        print(f"Copy message: {self.message}")
    
    def handle_resend(self, widget):
        """Handle resend button press."""
        # Trigger resend callback if available
        if hasattr(self.parent, 'resend_callback'):
            self.parent.resend_callback(self.message)
    
    def handle_delete(self, widget):
        """Handle delete button press."""
        # Remove this message widget
        if hasattr(self.parent, 'remove_message'):
            self.parent.remove_message(self)
    
    def get_background_color(self):
        """Get background color based on message type."""
        if self.is_error:
            return '#ffebee'  # Light red for errors
        elif self.is_user:
            return '#e3f2fd'  # Light blue for user messages
        else:
            return '#f5f5f5'  # Light gray for AI messages
    
    def get_text_color(self):
        """Get text color based on message type."""
        if self.is_error:
            return '#d32f2f'  # Red for errors
        else:
            return '#000000'  # Black for normal text
    
    def get_secondary_text_color(self):
        """Get secondary text color for timestamps, etc."""
        return '#666666'


class ChatComponent:
    """
    Chat component that manages the conversation display.
    
    This replaces the ChatInterface from the Tkinter version with Toga widgets.
    """
    
    def __init__(self, app):
        """
        Initialize the chat component.
        
        Args:
            app: The main JRAIControlApp instance
        """
        self.app = app
        self.messages = []
        self.chat_container = None
        self.scroll_container = None
        
        # Callbacks
        self.resend_callback = None
        self.delete_callback = None
    
    def create_chat_area(self):
        """
        Create the main chat area with scrolling.
        
        Returns:
            toga.ScrollContainer: The chat area container
        """
        # Create scrollable container
        self.scroll_container = toga.ScrollContainer(
            style=Pack(
                flex=1,
                padding=10
            )
        )
        
        # Create chat messages container
        self.chat_container = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=5
            )
        )
        
        self.scroll_container.content = self.chat_container
        
        return self.scroll_container
    
    def add_message(self, sender, message, is_user=False, screenshot_id=None, tokens=0, is_error=False):
        """
        Add a new message to the chat.
        
        Args:
            sender: Message sender name
            message: Message content
            is_user: True if this is a user message
            screenshot_id: ID of associated screenshot (optional)
            tokens: Number of tokens used (optional)
            is_error: True if this is an error message
            
        Returns:
            MessageWidget: The created message widget
        """
        # Create message widget
        message_widget = MessageWidget(
            parent=self,
            sender=sender,
            message=message,
            is_user=is_user,
            screenshot_id=screenshot_id,
            tokens=tokens,
            is_error=is_error
        )
        
        # Add to chat container
        if self.chat_container:
            self.chat_container.add(message_widget.widget)
        
        # Add to messages list
        self.messages.append(message_widget)
        
        # Scroll to bottom
        self.scroll_to_bottom()
        
        return message_widget
    
    def remove_message(self, message_widget):
        """
        Remove a message from the chat.
        
        Args:
            message_widget: The MessageWidget to remove
        """
        if message_widget in self.messages:
            self.messages.remove(message_widget)
        
        # Remove from UI
        if self.chat_container and message_widget.widget:
            self.chat_container.remove(message_widget.widget)
    
    def clear_chat(self):
        """Clear all messages from the chat."""
        # Clear messages list
        self.messages.clear()
        
        # Clear UI
        if self.chat_container:
            # Remove all children
            for child in list(self.chat_container.children):
                self.chat_container.remove(child)
    
    def scroll_to_bottom(self):
        """Scroll the chat to the bottom to show the latest message."""
        # Note: Toga ScrollContainer doesn't have direct scroll control yet
        # This would need to be implemented when the feature becomes available
        pass
    
    def set_resend_callback(self, callback):
        """
        Set the callback for message resend actions.
        
        Args:
            callback: Function to call when a message should be resent
        """
        self.resend_callback = callback
    
    def set_delete_callback(self, callback):
        """
        Set the callback for message delete actions.
        
        Args:
            callback: Function to call when a message should be deleted
        """
        self.delete_callback = callback
    
    def update_theme(self, theme_name):
        """
        Update the chat appearance for the new theme.
        
        Args:
            theme_name: Name of the theme ('dark' or 'light')
        """
        # Update background colors for existing messages
        for message_widget in self.messages:
            # Theme updates would be applied here
            # For now, Toga uses native platform theming
            pass
    
    def get_message_count(self):
        """
        Get the number of messages in the chat.
        
        Returns:
            int: Number of messages
        """
        return len(self.messages)
    
    def get_messages(self):
        """
        Get all messages in the chat.
        
        Returns:
            list: List of MessageWidget instances
        """
        return self.messages.copy()