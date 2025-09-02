"""
Header Component for Toga UI

This component manages the application header with title, model info,
token displays, and control buttons.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class HeaderComponent:
    """
    Header component that displays app title, model info, token counts, and controls.
    
    This replaces the header section from the Tkinter version with native Toga widgets.
    """
    
    def __init__(self, app):
        """
        Initialize the header component.
        
        Args:
            app: The main JRAIControlApp instance
        """
        self.app = app
        
        # Header widgets
        self.title_label = None
        self.model_label = None
        self.token_label = None
        self.total_token_label = None
        self.connection_status = None
        self.settings_button = None
        self.theme_button = None
        
        # Current state
        self.current_theme = app.theme_mode
        self.is_connected = False
    
    def create_header(self):
        """
        Create the header layout with all components.
        
        Returns:
            toga.Box: The header container
        """
        # Main header container
        header_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding=10,
                background_color='#2b2b2b' if self.current_theme == 'dark' else '#f5f5f5'
            )
        )
        
        # Left side - Title and info
        info_box = self.create_info_section()
        header_box.add(info_box)
        
        # Right side - Controls
        controls_box = self.create_controls_section()
        header_box.add(controls_box)
        
        return header_box
    
    def create_info_section(self):
        """
        Create the left side info section with title, model, and tokens.
        
        Returns:
            toga.Box: The info section container
        """
        info_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                flex=1,
                padding_right=20
            )
        )
        
        # Application title
        self.title_label = toga.Label(
            "JR AI Control",
            style=Pack(
                font_size=18,
                font_weight='bold',
                color='#ffffff' if self.current_theme == 'dark' else '#000000',
                padding_bottom=5
            )
        )
        info_box.add(self.title_label)
        
        # Model display
        self.model_label = toga.Label(
            f"Model: {self.app.current_model}",
            style=Pack(
                font_size=12,
                color='#cccccc' if self.current_theme == 'dark' else '#666666',
                padding_bottom=5
            )
        )
        info_box.add(self.model_label)
        
        # Token displays
        token_box = toga.Box(style=Pack(direction=ROW))
        
        self.token_label = toga.Label(
            "Message: 0 tokens",
            style=Pack(
                font_size=10,
                color='#aaaaaa' if self.current_theme == 'dark' else '#888888',
                padding_right=10
            )
        )
        token_box.add(self.token_label)
        
        # Separator
        separator = toga.Label(
            "•",
            style=Pack(
                font_size=10,
                color='#aaaaaa' if self.current_theme == 'dark' else '#888888',
                padding_right=10
            )
        )
        token_box.add(separator)
        
        total_tokens = self.app.token_tracker.get_total_tokens()
        self.total_token_label = toga.Label(
            f"Total: {total_tokens:,} tokens",
            style=Pack(
                font_size=10,
                color='#aaaaaa' if self.current_theme == 'dark' else '#888888'
            )
        )
        token_box.add(self.total_token_label)
        
        info_box.add(token_box)
        
        return info_box
    
    def create_controls_section(self):
        """
        Create the right side controls section with buttons and status.
        
        Returns:
            toga.Box: The controls section container
        """
        controls_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding_left=20
            )
        )
        
        # Connection status indicator
        self.connection_status = toga.Label(
            "●",
            style=Pack(
                font_size=16,
                color='#ff4444' if not self.is_connected else '#44ff44',
                padding_right=10
            )
        )
        controls_box.add(self.connection_status)
        
        # Theme toggle button
        theme_text = "🌙" if self.current_theme == 'light' else "☀️"
        self.theme_button = toga.Button(
            theme_text,
            on_press=self.toggle_theme,
            style=Pack(
                width=40,
                padding_right=5
            )
        )
        controls_box.add(self.theme_button)
        
        # Settings button
        self.settings_button = toga.Button(
            "⚙️",
            on_press=self.open_settings,
            style=Pack(
                width=40
            )
        )
        controls_box.add(self.settings_button)
        
        return controls_box
    
    def update_model_display(self, model_name):
        """
        Update the displayed model name.
        
        Args:
            model_name: Name of the current model
        """
        if self.model_label:
            self.model_label.text = f"Model: {model_name}"
    
    def update_token_display(self, message_tokens, total_tokens=None):
        """
        Update the token usage displays.
        
        Args:
            message_tokens: Number of tokens used in the last message
            total_tokens: Total tokens used (optional, will get from tracker if not provided)
        """
        if self.token_label:
            self.token_label.text = f"Message: {message_tokens:,} tokens"
        
        if self.total_token_label:
            if total_tokens is None:
                total_tokens = self.app.token_tracker.get_total_tokens()
            self.total_token_label.text = f"Total: {total_tokens:,} tokens"
    
    def update_connection_status(self, connected):
        """
        Update the connection status indicator.
        
        Args:
            connected: True if connected to AI service, False otherwise
        """
        self.is_connected = connected
        if self.connection_status:
            color = '#44ff44' if connected else '#ff4444'
            self.connection_status.style.color = color
    
    def toggle_theme(self, widget):
        """
        Handle theme toggle button press.
        
        Args:
            widget: The button widget that was pressed
        """
        new_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.current_theme = new_theme
        self.app.theme_mode = new_theme
        
        # Update theme button text
        theme_text = "🌙" if new_theme == 'light' else "☀️"
        self.theme_button.text = theme_text
        
        # Apply theme to app
        if hasattr(self.app, 'theme_manager'):
            self.app.theme_manager.switch_theme(new_theme)
        
        # Save settings
        self.app.save_settings()
    
    def open_settings(self, widget):
        """
        Handle settings button press.
        
        Args:
            widget: The button widget that was pressed
        """
        self.app.open_settings()
    
    def update_theme(self, theme_name):
        """
        Update the header appearance for the new theme.
        
        Args:
            theme_name: Name of the theme ('dark' or 'light')
        """
        self.current_theme = theme_name
        
        # Update colors for theme
        if self.title_label:
            self.title_label.style.color = '#ffffff' if theme_name == 'dark' else '#000000'
        
        if self.model_label:
            self.model_label.style.color = '#cccccc' if theme_name == 'dark' else '#666666'
        
        if self.token_label:
            self.token_label.style.color = '#aaaaaa' if theme_name == 'dark' else '#888888'
        
        if self.total_token_label:
            self.total_token_label.style.color = '#aaaaaa' if theme_name == 'dark' else '#888888'
        
        # Update theme button text
        theme_text = "🌙" if theme_name == 'light' else "☀️"
        if self.theme_button:
            self.theme_button.text = theme_text