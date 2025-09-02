"""
Message Widget Component for JR AI Control - Toga Implementation

This module provides individual message widgets with proper alignment, styling,
timestamp display, and support for screenshots and message actions.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime
import os


class MessageWidget:
    """
    Individual message widget using toga.Box containers with proper alignment
    for AI messages (left-aligned) and user messages (right-aligned).
    """
    
    def __init__(self, chat_component, message_data):
        """
        Initialize the message widget.
        
        Args:
            chat_component: The parent chat component instance
            message_data (dict): Dictionary containing message information:
                - sender (str): The sender of the message
                - content (str): The message content
                - is_user (bool): Whether this is a user message
                - screenshot_id (str, optional): Screenshot ID if message includes image
                - tokens (int, optional): Number of tokens used
                - timestamp (datetime): When the message was created
        """
        self.chat_component = chat_component
        self.app = chat_component.app
        self.theme_mode = chat_component.theme_mode
        self.message_data = message_data
        
        # Extract message data
        self.sender = message_data['sender']
        self.content = message_data['content']
        self.is_user = message_data['is_user']
        self.screenshot_id = message_data.get('screenshot_id')
        self.tokens = message_data.get('tokens', 0)
        self.timestamp = message_data.get('timestamp', datetime.now())
        
        # Initialize widget references
        self.message_container = None
        self.message_box = None
        self.sender_label = None
        self.content_label = None
        self.timestamp_label = None
        self.token_label = None
        self.screenshot_view = None
        self.actions_box = None
        
        # Create the message layout
        self.create_message_layout()
    
    def create_message_layout(self):
        """
        Create message layout with content and proper alignment.
        Implement left-aligned AI messages and right-aligned user messages.
        Add timestamp display using toga.Label for each message.
        Create message content display with proper text wrapping.
        
        Returns:
            toga.Box: The complete message container
        """
        # Create message container with proper alignment for user vs AI messages
        self.message_container = toga.Box(style=Pack(
            direction=ROW,
            margin=(8, 16, 8, 16)
        ))
        
        # Create message bubble with appropriate styling
        self.message_box = toga.Box(style=Pack(
            direction=COLUMN,
            padding=12,
            background_color=self._get_message_bg_color(),
            width=400 if not self.is_user else 350,  # Different widths for alignment
            margin=(0, 8)
        ))
        
        # Add sender label with proper styling
        self.sender_label = toga.Label(
            self.sender,
            style=Pack(
                font_weight='bold',
                font_size=13,
                color=self._get_sender_text_color(),
                margin_bottom=6
            )
        )
        self.message_box.add(self.sender_label)
        
        # Add message content with proper text wrapping
        self.content_label = toga.Label(
            self.content,
            style=Pack(
                font_size=14,
                color=self._get_content_text_color(),
                margin_bottom=8 if not self.screenshot_id else 4
            )
        )
        self.message_box.add(self.content_label)
        
        # Add screenshot thumbnail if provided
        if self.screenshot_id:
            self._add_screenshot_thumbnail()
        
        # Add bottom info row with timestamp and token count
        self._add_info_row()
        
        # Add message action buttons (resend, copy, delete)
        self._add_action_buttons()
        
        # Handle message alignment (left for AI, right for user)
        if self.is_user:
            # Add spacer for right alignment
            spacer = toga.Box(style=Pack(flex=1))
            self.message_container.add(spacer)
            self.message_container.add(self.message_box)
        else:
            # Left alignment for AI messages
            self.message_container.add(self.message_box)
            spacer = toga.Box(style=Pack(flex=1))
            self.message_container.add(spacer)
        
        return self.message_container
    
    def _add_screenshot_thumbnail(self):
        """
        Replace custom image display with toga.ImageView widgets.
        Implement clickable thumbnails that open full-size images.
        Create thumbnail sizing and aspect ratio management.
        Add image loading error handling and placeholder display.
        """
        try:
            # Get screenshot thumbnail path from screenshot manager
            if hasattr(self.app, 'screenshot_manager'):
                thumbnail_path = self.app.screenshot_manager.get_thumbnail_path(self.screenshot_id)
                
                if thumbnail_path and os.path.exists(thumbnail_path):
                    # Create ImageView for thumbnail with proper sizing
                    screenshot_image = toga.ImageView(
                        image=toga.Image(thumbnail_path),
                        style=Pack(
                            width=150,
                            height=112,  # Maintain 4:3 aspect ratio
                            margin_bottom=8
                        )
                    )
                    
                    # Make thumbnail clickable to open full-size image
                    # Note: Toga ImageView doesn't have direct click events
                    # We'll add a button overlay for click handling
                    screenshot_container = toga.Box(style=Pack(
                        direction=COLUMN,
                        margin_bottom=8
                    ))
                    
                    screenshot_container.add(screenshot_image)
                    
                    # Add click button for full-size view
                    view_button = toga.Button(
                        "🔍 View Full Size",
                        on_press=self.handle_thumbnail_click,
                        style=Pack(
                            width=150,
                            height=25,
                            background_color=self._get_action_button_bg_color(),
                            color=self._get_action_button_text_color(),
                            font_size=10
                        )
                    )
                    screenshot_container.add(view_button)
                    
                    self.message_box.add(screenshot_container)
                    self.screenshot_view = screenshot_container
                    
                else:
                    # Add placeholder for missing screenshot with error handling
                    self._add_screenshot_error_placeholder("Screenshot file not found")
                    
            else:
                # Add placeholder when screenshot manager is not available
                self._add_screenshot_error_placeholder("Screenshot manager unavailable")
                
        except Exception as e:
            print(f"Error loading screenshot thumbnail: {e}")
            # Add error placeholder with proper error handling
            self._add_screenshot_error_placeholder(f"Error loading screenshot: {str(e)}")
    
    def _add_screenshot_error_placeholder(self, error_message):
        """
        Add error placeholder for screenshot loading issues.
        
        Args:
            error_message (str): The error message to display
        """
        placeholder_label = toga.Label(
            f"📷 {error_message}",
            style=Pack(
                font_size=12,
                color='#ff6666',  # Red color for errors
                margin_bottom=8
            )
        )
        self.message_box.add(placeholder_label)
    
    def handle_thumbnail_click(self, widget):
        """
        Handle thumbnail click to show full-size image.
        
        Args:
            widget: The button widget that triggered this action
        """
        try:
            # Get full-size screenshot path
            if hasattr(self.app, 'screenshot_manager'):
                full_path = self.app.screenshot_manager.get_screenshot_path(self.screenshot_id)
                
                if full_path and os.path.exists(full_path):
                    # Create new window for full-size image viewing
                    self._show_full_size_image(full_path)
                else:
                    # Show error message
                    if hasattr(self.chat_component, 'add_message'):
                        self.chat_component.add_message(
                            "System", 
                            "Full-size screenshot not found",
                            is_user=False
                        )
            
        except Exception as e:
            print(f"Error opening full-size image: {e}")
            if hasattr(self.chat_component, 'add_message'):
                self.chat_component.add_message(
                    "System", 
                    f"Error opening image: {str(e)}",
                    is_user=False
                )
    
    def _show_full_size_image(self, image_path):
        """
        Show full-size image in a new window.
        
        Args:
            image_path (str): Path to the full-size image
        """
        try:
            # Create new window for image viewing
            image_window = toga.Window(
                title=f"Screenshot - {self.screenshot_id}",
                size=(800, 600)
            )
            
            # Create container for image
            image_container = toga.Box(style=Pack(
                direction=COLUMN,
                padding=20
            ))
            
            # Create ImageView for full-size image
            full_image = toga.ImageView(
                image=toga.Image(image_path),
                style=Pack(
                    flex=1
                )
            )
            image_container.add(full_image)
            
            # Add close button
            close_button = toga.Button(
                "Close",
                on_press=lambda widget: image_window.close(),
                style=Pack(
                    width=100,
                    height=40,
                    margin_top=10
                )
            )
            image_container.add(close_button)
            
            image_window.content = image_container
            image_window.show()
            
        except Exception as e:
            print(f"Error creating image window: {e}")
    
    def _add_info_row(self):
        """
        Add bottom info row with timestamp and token count using toga.Label.
        """
        # Bottom info row (timestamp and tokens)
        info_box = toga.Box(style=Pack(direction=ROW))
        
        # Add timestamp display using toga.Label
        timestamp_str = self.timestamp.strftime("%H:%M:%S")
        self.timestamp_label = toga.Label(
            timestamp_str,
            style=Pack(
                font_size=11,
                color=self._get_secondary_text_color(),
                margin_right=12
            )
        )
        info_box.add(self.timestamp_label)
        
        # Add token count if provided
        if self.tokens > 0:
            self.token_label = toga.Label(
                f"{self.tokens} tokens",
                style=Pack(
                    font_size=11,
                    color=self._get_secondary_text_color()
                )
            )
            info_box.add(self.token_label)
        
        self.message_box.add(info_box)
    
    def _add_action_buttons(self):
        """
        Add message action buttons using Toga buttons.
        Implement resend button using toga.Button for each message.
        Add copy button using toga.Button with clipboard integration.
        Create delete button using toga.Button with confirmation.
        Layout action buttons below each message using toga.Box with ROW direction.
        """
        # Create actions container with ROW direction for horizontal layout
        self.actions_box = toga.Box(style=Pack(
            direction=ROW,
            margin_top=8,
            align_items='center'
        ))
        
        # Resend button - allows user to resend the message
        self.resend_button = toga.Button(
            "🔄 Resend",
            on_press=self.handle_resend,
            style=Pack(
                width=80,
                height=30,
                margin_right=8,
                background_color=self._get_action_button_bg_color(),
                color=self._get_action_button_text_color(),
                font_size=11
            )
        )
        self.actions_box.add(self.resend_button)
        
        # Copy button - copies message content to clipboard
        self.copy_button = toga.Button(
            "📋 Copy",
            on_press=self.handle_copy,
            style=Pack(
                width=80,
                height=30,
                margin_right=8,
                background_color=self._get_action_button_bg_color(),
                color=self._get_action_button_text_color(),
                font_size=11
            )
        )
        self.actions_box.add(self.copy_button)
        
        # Delete button - removes message with confirmation
        self.delete_button = toga.Button(
            "🗑️ Delete",
            on_press=self.handle_delete,
            style=Pack(
                width=80,
                height=30,
                background_color='#d32f2f',  # Red background for delete
                color='#ffffff',
                font_size=11
            )
        )
        self.actions_box.add(self.delete_button)
        
        # Add actions to message box
        self.message_box.add(self.actions_box)
    
    def update_theme(self, theme_mode):
        """
        Update message styling according to the current theme.
        
        Args:
            theme_mode (str): The theme mode ('dark' or 'light')
        """
        self.theme_mode = theme_mode
        
        # Update message box background
        if self.message_box:
            self.message_box.style.background_color = self._get_message_bg_color()
        
        # Update text colors
        if self.sender_label:
            self.sender_label.style.color = self._get_sender_text_color()
        
        if self.content_label:
            self.content_label.style.color = self._get_content_text_color()
        
        if self.timestamp_label:
            self.timestamp_label.style.color = self._get_secondary_text_color()
        
        if self.token_label:
            self.token_label.style.color = self._get_secondary_text_color()
        
        # Update action button colors
        if hasattr(self, 'resend_button') and self.resend_button:
            self.resend_button.style.background_color = self._get_action_button_bg_color()
            self.resend_button.style.color = self._get_action_button_text_color()
        
        if hasattr(self, 'copy_button') and self.copy_button:
            self.copy_button.style.background_color = self._get_action_button_bg_color()
            self.copy_button.style.color = self._get_action_button_text_color()
    
    def get_container(self):
        """
        Get the message container widget.
        
        Returns:
            toga.Box: The message container
        """
        return self.message_container
    
    def get_message_data(self):
        """
        Get the message data dictionary.
        
        Returns:
            dict: The message data
        """
        return self.message_data
    
    def _get_message_bg_color(self):
        """Get message background color based on sender and theme."""
        if self.is_user:
            return '#0066cc'  # Blue for user messages
        else:
            return '#404040' if self.theme_mode == 'dark' else '#f0f0f0'
    
    def _get_sender_text_color(self):
        """Get sender text color based on message type and theme."""
        if self.is_user:
            return '#ffffff'  # White text on blue background
        else:
            return '#ffffff' if self.theme_mode == 'dark' else '#333333'
    
    def _get_content_text_color(self):
        """Get content text color based on message type and theme."""
        if self.is_user:
            return '#ffffff'  # White text on blue background
        else:
            return '#ffffff' if self.theme_mode == 'dark' else '#333333'
    
    def _get_secondary_text_color(self):
        """Get secondary text color for timestamps and tokens."""
        if self.is_user:
            return '#cccccc'  # Light gray on blue background
        else:
            return '#cccccc' if self.theme_mode == 'dark' else '#666666'
    
    def _get_action_button_bg_color(self):
        """Get action button background color based on theme."""
        return '#555555' if self.theme_mode == 'dark' else '#e0e0e0'
    
    def _get_action_button_text_color(self):
        """Get action button text color based on theme."""
        return '#ffffff' if self.theme_mode == 'dark' else '#000000'
    
    def handle_resend(self, widget):
        """
        Handle resend button click - resends the message content.
        
        Args:
            widget: The button widget that triggered this action
        """
        try:
            # Only allow resending user messages
            if self.is_user and hasattr(self.app, 'input_field'):
                # Set the input field to the message content
                self.app.input_field.value = self.content
                
                # Optionally auto-send the message
                # self.app.send_message(None)
                
                # Add feedback message
                if hasattr(self.chat_component, 'add_message'):
                    self.chat_component.add_message(
                        "System", 
                        f"Message '{self.content[:50]}...' loaded into input field",
                        is_user=False
                    )
            else:
                # For AI messages, we could implement a different behavior
                if hasattr(self.chat_component, 'add_message'):
                    self.chat_component.add_message(
                        "System", 
                        "Cannot resend AI messages. Use the original user message instead.",
                        is_user=False
                    )
                    
        except Exception as e:
            print(f"Error handling resend: {e}")
            if hasattr(self.chat_component, 'add_message'):
                self.chat_component.add_message(
                    "System", 
                    f"Error resending message: {str(e)}",
                    is_user=False
                )
    
    def handle_copy(self, widget):
        """
        Handle copy button click - copies message content to clipboard.
        
        Args:
            widget: The button widget that triggered this action
        """
        try:
            # Copy message content to clipboard
            # Note: Toga doesn't have built-in clipboard support yet
            # This is a placeholder for future implementation
            
            # For now, we'll use a system-specific approach
            import platform
            import subprocess
            
            system = platform.system()
            
            if system == "Windows":
                # Windows clipboard
                subprocess.run(['clip'], input=self.content.encode('utf-8'), check=True)
            elif system == "Darwin":  # macOS
                # macOS clipboard
                subprocess.run(['pbcopy'], input=self.content.encode('utf-8'), check=True)
            elif system == "Linux":
                # Linux clipboard (requires xclip)
                try:
                    subprocess.run(['xclip', '-selection', 'clipboard'], 
                                 input=self.content.encode('utf-8'), check=True)
                except FileNotFoundError:
                    # Fallback to xsel if xclip is not available
                    subprocess.run(['xsel', '--clipboard', '--input'], 
                                 input=self.content.encode('utf-8'), check=True)
            
            # Add feedback message
            if hasattr(self.chat_component, 'add_message'):
                self.chat_component.add_message(
                    "System", 
                    "Message copied to clipboard",
                    is_user=False
                )
                
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            if hasattr(self.chat_component, 'add_message'):
                self.chat_component.add_message(
                    "System", 
                    f"Error copying to clipboard: {str(e)}",
                    is_user=False
                )
    
    def handle_delete(self, widget):
        """
        Handle delete button click - removes message with confirmation.
        
        Args:
            widget: The button widget that triggered this action
        """
        try:
            # For now, we'll implement immediate deletion
            # In a full implementation, this would show a confirmation dialog
            
            # Remove this message from the chat
            if hasattr(self.chat_component, 'remove_message'):
                self.chat_component.remove_message(self)
                
                # Add feedback message
                self.chat_component.add_message(
                    "System", 
                    "Message deleted",
                    is_user=False
                )
            
        except Exception as e:
            print(f"Error deleting message: {e}")
            if hasattr(self.chat_component, 'add_message'):
                self.chat_component.add_message(
                    "System", 
                    f"Error deleting message: {str(e)}",
                    is_user=False
                )