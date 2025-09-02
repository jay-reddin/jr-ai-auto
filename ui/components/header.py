"""
Header Component for JR AI Control - Toga Implementation

This module provides the header component with application title, model info,
connection status, token displays, and control buttons using Toga widgets.
"""

import toga
from toga.style import Pack
from toga.style.pack import ROW, COLUMN


class HeaderComponent:
    """
    Header component that displays application title, model info, connection status,
    token usage, and control buttons using Toga widgets with ROW layout.
    """
    
    def __init__(self, app_instance):
        """
        Initialize the header component.
        
        Args:
            app_instance: The main application instance for accessing configuration and services
        """
        self.app = app_instance
        self.theme_mode = app_instance.theme_mode
        
        # Initialize component references
        self.header_container = None
        self.title_label = None
        self.model_display = None
        self.connection_status = None
        self.token_display = None
        self.total_token_display = None
        self.settings_btn = None
        self.theme_btn = None
        self.voice_btn = None
        
        # Create the header layout
        self.create_header_layout()
    
    def create_header_layout(self):
        """
        Create header layout using toga.Box with ROW direction.
        
        Returns:
            toga.Box: The complete header container
        """
        # Main header container with ROW direction and proper styling
        self.header_container = toga.Box(style=Pack(
            direction=ROW,
            margin=(16, 16, 16, 16),
            background_color=self._get_header_bg_color(),
            height=120,  # Fixed height for header
            align_items='center'
        ))
        
        # Left section - title and info (flexible width)
        left_section = self._create_title_section()
        self.header_container.add(left_section)
        
        # Center section - token displays (fixed width)
        center_section = self._create_token_section()
        self.header_container.add(center_section)
        
        # Right section - control buttons (fixed width)
        right_section = self._create_controls_section()
        self.header_container.add(right_section)
        
        return self.header_container
    
    def _create_title_section(self):
        """
        Create the title section with app title, model info, and connection status.
        
        Returns:
            toga.Box: The title section container
        """
        title_box = toga.Box(style=Pack(
            direction=COLUMN,
            flex=1,
            margin_right=16
        ))
        
        # Application title with appropriate styling
        self.title_label = toga.Label(
            "JR AI Control",
            style=Pack(
                font_size=20,
                font_weight='bold',
                color=self._get_primary_text_color(),
                margin_bottom=4
            )
        )
        title_box.add(self.title_label)
        
        # Model display label showing current model
        model_text = f"Model: {self.app.current_model}"
        self.model_display = toga.Label(
            model_text,
            style=Pack(
                font_size=14,
                color=self._get_secondary_text_color(),
                margin_bottom=4
            )
        )
        title_box.add(self.model_display)
        
        # Connection status indicator with color coding
        self.connection_status = toga.Label(
            self._get_connection_status_text(),
            style=Pack(
                font_size=12,
                color=self._get_connection_status_color(),
                margin_bottom=4
            )
        )
        title_box.add(self.connection_status)
        
        return title_box
    
    def _create_token_section(self):
        """
        Create the token display section with message and total token counters.
        
        Returns:
            toga.Box: The token section container
        """
        token_box = toga.Box(style=Pack(
            direction=COLUMN,
            width=200,  # Fixed width for token displays
            margin_right=16,
            align_items='center'
        ))
        
        # Token section title
        token_title = toga.Label(
            "Token Usage",
            style=Pack(
                font_size=13,
                font_weight='bold',
                color=self._get_primary_text_color(),
                margin_bottom=6,
                text_align='center'
            )
        )
        token_box.add(token_title)
        
        # Message token counter using toga.Label
        self.token_display = toga.Label(
            "Message: 0 tokens",
            style=Pack(
                font_size=12,
                color=self._get_secondary_text_color(),
                margin_bottom=4,
                text_align='center'
            )
        )
        token_box.add(self.token_display)
        
        # Total token usage display using toga.Label
        total_tokens = self.app.token_tracker.get_total_tokens() if self.app.token_tracker else 0
        self.total_token_display = toga.Label(
            f"Total: {total_tokens:,} tokens",
            style=Pack(
                font_size=12,
                color=self._get_secondary_text_color(),
                text_align='center'
            )
        )
        token_box.add(self.total_token_display)
        
        return token_box
    
    def _create_controls_section(self):
        """
        Create the control buttons section with settings, theme, and voice buttons.
        Create header button layout with proper spacing using Pack styling.
        
        Returns:
            toga.Box: The controls section container
        """
        controls_box = toga.Box(style=Pack(
            direction=ROW,
            align_items='center',
            margin_left=16,
            margin_right=8
        ))
        
        # Settings button using toga.Button with callback
        self.settings_btn = toga.Button(
            "⚙️ Settings",
            on_press=self._on_settings_clicked,
            style=Pack(
                width=100,
                height=40,
                margin_right=8,
                background_color=self._get_button_bg_color(),
                color=self._get_button_text_color(),
                font_size=12
            )
        )
        controls_box.add(self.settings_btn)
        
        # Theme toggle button using toga.Button
        theme_text = "🌙 Light" if self.theme_mode == "dark" else "☀️ Dark"
        self.theme_btn = toga.Button(
            theme_text,
            on_press=self._on_theme_clicked,
            style=Pack(
                width=100,
                height=40,
                margin_right=8,
                background_color=self._get_button_bg_color(),
                color=self._get_button_text_color(),
                font_size=12
            )
        )
        controls_box.add(self.theme_btn)
        
        # Voice control toggle button (if voice is available)
        if self.app.voice_manager and self.app.voice_manager.is_voice_available():
            voice_text = "🎤 Voice" if not self.app.is_listening else "🔴 Stop"
            self.voice_btn = toga.Button(
                voice_text,
                on_press=self._on_voice_clicked,
                style=Pack(
                    width=100,
                    height=40,
                    background_color=self._get_voice_button_color(),
                    color=self._get_button_text_color(),
                    font_size=12
                )
            )
            controls_box.add(self.voice_btn)
        
        return controls_box
    
    def update_model_display(self, model_name):
        """
        Update the displayed model name.
        
        Args:
            model_name (str): The new model name to display
        """
        if self.model_display:
            self.model_display.text = f"Model: {model_name}"
    
    def update_connection_status(self, connected):
        """
        Update the connection status indicator with color coding.
        
        Args:
            connected (bool): Whether the agent is connected/initialized
        """
        if self.connection_status:
            if connected:
                self.connection_status.text = "Status: Connected ✅"
                self.connection_status.style.color = '#4CAF50'  # Green
            else:
                self.connection_status.text = "Status: Disconnected ❌"
                self.connection_status.style.color = '#F44336'  # Red
    
    def update_token_display(self, message_tokens, total_tokens=None):
        """
        Update token displays with real-time data from TokenTracker.
        
        Args:
            message_tokens (int): Number of tokens used in the last message
            total_tokens (int, optional): Total tokens used (if not provided, fetched from tracker)
        """
        # Update message token display
        if self.token_display:
            self.token_display.text = f"Message: {message_tokens:,} tokens"
        
        # Update total token display
        if self.total_token_display:
            if total_tokens is None and self.app.token_tracker:
                total_tokens = self.app.token_tracker.get_total_tokens()
            
            if total_tokens is not None:
                self.total_token_display.text = f"Total: {total_tokens:,} tokens"
    
    def refresh_token_display(self):
        """
        Refresh token displays with current data from TokenTracker.
        This method provides real-time token updates.
        """
        if self.app.token_tracker:
            total_tokens = self.app.token_tracker.get_total_tokens()
            if self.total_token_display:
                self.total_token_display.text = f"Total: {total_tokens:,} tokens"
    
    def reset_message_tokens(self):
        """Reset the message token display to zero."""
        if self.token_display:
            self.token_display.text = "Message: 0 tokens"
    
    def update_theme(self, theme_mode):
        """
        Update the header styling according to the current theme.
        
        Args:
            theme_mode (str): The theme mode ('dark' or 'light')
        """
        self.theme_mode = theme_mode
        
        # Update header container background
        if self.header_container:
            self.header_container.style.background_color = self._get_header_bg_color()
        
        # Update text colors
        if self.title_label:
            self.title_label.style.color = self._get_primary_text_color()
        
        if self.model_display:
            self.model_display.style.color = self._get_secondary_text_color()
        
        # Update token display colors according to current theme
        if self.token_display:
            self.token_display.style.color = self._get_secondary_text_color()
        
        if self.total_token_display:
            self.total_token_display.style.color = self._get_secondary_text_color()
        
        # Update button colors
        button_bg = self._get_button_bg_color()
        button_text = self._get_button_text_color()
        
        for btn in [self.settings_btn, self.theme_btn, self.voice_btn]:
            if btn:
                btn.style.background_color = button_bg
                btn.style.color = button_text
        
        # Update theme button text
        if self.theme_btn:
            self.theme_btn.text = "🌙 Light" if theme_mode == "dark" else "☀️ Dark"
    
    def update_voice_status(self, is_listening):
        """
        Update the voice button to reflect listening state.
        
        Args:
            is_listening (bool): Whether voice recognition is currently active
        """
        if self.voice_btn:
            self.voice_btn.text = "🔴 Stop" if is_listening else "🎤 Voice"
            self.voice_btn.style.background_color = self._get_voice_button_color()
    
    def _get_connection_status_text(self):
        """Get the connection status text based on agent state."""
        if self.app.agent_executor:
            return "Status: Connected ✅"
        else:
            return "Status: Disconnected ❌"
    
    def _get_connection_status_color(self):
        """Get the connection status color based on agent state."""
        if self.app.agent_executor:
            return '#4CAF50'  # Green for connected
        else:
            return '#F44336'  # Red for disconnected
    
    def _get_header_bg_color(self):
        """Get header background color based on theme."""
        return '#2b2b2b' if self.theme_mode == 'dark' else '#f5f5f5'
    
    def _get_primary_text_color(self):
        """Get primary text color based on theme."""
        return '#ffffff' if self.theme_mode == 'dark' else '#1a1a1a'
    
    def _get_secondary_text_color(self):
        """Get secondary text color based on theme."""
        return '#cccccc' if self.theme_mode == 'dark' else '#666666'
    
    def _get_button_bg_color(self):
        """Get button background color based on theme."""
        return '#404040' if self.theme_mode == 'dark' else '#e0e0e0'
    
    def _get_button_text_color(self):
        """Get button text color based on theme."""
        return '#ffffff' if self.theme_mode == 'dark' else '#000000'
    
    def _get_voice_button_color(self):
        """Get voice button background color based on listening state."""
        if self.app.is_listening:
            return '#d32f2f'  # Red when listening
        else:
            return self._get_button_bg_color()  # Normal button color
    
    def _on_settings_clicked(self, widget):
        """Handle settings button click."""
        if hasattr(self.app, 'open_settings'):
            self.app.open_settings(widget)
    
    def _on_theme_clicked(self, widget):
        """Handle theme toggle button click."""
        if hasattr(self.app, 'toggle_theme'):
            self.app.toggle_theme(widget)
    
    def _on_voice_clicked(self, widget):
        """Handle voice toggle button click."""
        if hasattr(self.app, 'toggle_listening'):
            self.app.toggle_listening(widget)
    
    def get_container(self):
        """
        Get the header container widget.
        
        Returns:
            toga.Box: The header container
        """
        return self.header_container