"""
Header Component for Toga-based JR AI Control
Displays application title, model info, token usage, and control buttons
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from typing import Optional


class HeaderComponent:
    """
    Header component that displays app title, model info, and controls
    """
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.title_label: Optional[toga.Label] = None
        self.model_label: Optional[toga.Label] = None
        self.token_label: Optional[toga.Label] = None
        self.total_token_label: Optional[toga.Label] = None
        self.status_label: Optional[toga.Label] = None
        self.theme_button: Optional[toga.Button] = None
        self.settings_button: Optional[toga.Button] = None
    
    def create_header_layout(self) -> toga.Box:
        """Create the header layout with title, info, and controls"""
        try:
            # Main header container
            header_box = toga.Box(
                style=Pack(
                    direction=ROW,
                    padding=(10, 0, 10, 0),
                    alignment="center"
                )
            )
            
            # Left side - Title and info
            info_box = toga.Box(
                style=Pack(
                    direction=COLUMN,
                    flex=1,
                    padding=(0, 10, 0, 0)
                )
            )
            
            # App title
            self.title_label = toga.Label(
                "JR AI Control",
                style=Pack(
                    font_size=18,
                    font_weight="bold",
                    padding=(0, 0, 5, 0)
                )
            )
            info_box.add(self.title_label)
            
            # Model information
            model_text = f"Model: {self.app.current_model}"
            self.model_label = toga.Label(
                model_text,
                style=Pack(
                    font_size=12,
                    padding=(0, 0, 2, 0)
                )
            )
            info_box.add(self.model_label)
            
            # Token usage information
            token_box = toga.Box(style=Pack(direction=ROW))
            
            self.token_label = toga.Label(
                "Message: 0 tokens",
                style=Pack(
                    font_size=10,
                    padding=(0, 5, 0, 0)
                )
            )
            token_box.add(self.token_label)
            
            separator = toga.Label(
                " • ",
                style=Pack(font_size=10)
            )
            token_box.add(separator)
            
            total_tokens = self.app.token_tracker.get_total_tokens() if self.app.token_tracker else 0
            self.total_token_label = toga.Label(
                f"Total: {total_tokens:,} tokens",
                style=Pack(
                    font_size=10,
                    padding=(0, 0, 0, 5)
                )
            )
            token_box.add(self.total_token_label)
            
            info_box.add(token_box)
            
            # Connection status
            status_text = "Connected" if self.app.api_key else "Not Connected"
            self.status_label = toga.Label(
                f"Status: {status_text}",
                style=Pack(
                    font_size=10,
                    padding=(2, 0, 0, 0)
                )
            )
            info_box.add(self.status_label)
            
            header_box.add(info_box)
            
            # Right side - Control buttons
            controls_box = toga.Box(
                style=Pack(
                    direction=ROW,
                    padding=(0, 0, 0, 10)
                )
            )
            
            # Theme toggle button
            theme_text = "🌙" if self.app.theme_mode == "light" else "☀️"
            self.theme_button = toga.Button(
                theme_text,
                on_press=self._toggle_theme,
                style=Pack(
                    width=40,
                    padding=(0, 5, 0, 0)
                )
            )
            controls_box.add(self.theme_button)
            
            # Settings button
            self.settings_button = toga.Button(
                "⚙️",
                on_press=self._open_settings,
                style=Pack(
                    width=40,
                    padding=(0, 0, 0, 5)
                )
            )
            controls_box.add(self.settings_button)
            
            header_box.add(controls_box)
            
            return header_box
            
        except Exception as e:
            print(f"Error creating header layout: {e}")
            # Return a simple fallback header
            return self._create_fallback_header()
    
    def _create_fallback_header(self) -> toga.Box:
        """Create a simple fallback header if main creation fails"""
        fallback_box = toga.Box(style=Pack(direction=ROW, padding=10))
        
        title = toga.Label(
            "JR AI Control",
            style=Pack(font_size=16, font_weight="bold")
        )
        fallback_box.add(title)
        
        return fallback_box
    
    def _toggle_theme(self, widget):
        """Handle theme toggle button press"""
        try:
            new_theme = "light" if self.app.theme_mode == "dark" else "dark"
            self.app.theme_mode = new_theme
            
            # Update theme button text
            theme_text = "🌙" if new_theme == "light" else "☀️"
            self.theme_button.text = theme_text
            
            # Apply theme through theme manager
            if self.app.theme_manager:
                self.app.theme_manager.switch_theme(new_theme)
            
            # Save configuration
            self.app.save_configuration()
            
        except Exception as e:
            print(f"Error toggling theme: {e}")
    
    def _open_settings(self, widget):
        """Handle settings button press"""
        try:
            # Import and create settings window
            from .settings_window import SettingsWindow
            settings_window = SettingsWindow(self.app)
            settings_window.show()
            
        except Exception as e:
            print(f"Error opening settings: {e}")
            # Show a simple dialog as fallback
            self.app.main_window.info_dialog(
                "Settings",
                "Settings window not yet implemented. Please use configuration files for now."
            )
    
    def update_model_display(self, model_name: str):
        """Update the displayed model name"""
        try:
            if self.model_label:
                self.model_label.text = f"Model: {model_name}"
        except Exception as e:
            print(f"Error updating model display: {e}")
    
    def update_token_display(self, message_tokens: int, total_tokens: int = None):
        """Update token usage displays"""
        try:
            if self.token_label:
                self.token_label.text = f"Message: {message_tokens} tokens"
            
            if self.total_token_label and total_tokens is not None:
                self.total_token_label.text = f"Total: {total_tokens:,} tokens"
                
        except Exception as e:
            print(f"Error updating token display: {e}")
    
    def update_connection_status(self, connected: bool):
        """Update connection status display"""
        try:
            if self.status_label:
                status_text = "Connected" if connected else "Not Connected"
                self.status_label.text = f"Status: {status_text}"
                
        except Exception as e:
            print(f"Error updating connection status: {e}")
    
    def update_theme(self, theme_name: str):
        """Update component styling for new theme"""
        try:
            # Update theme button text
            if self.theme_button:
                theme_text = "🌙" if theme_name == "light" else "☀️"
                self.theme_button.text = theme_text
            
            # Additional theme-specific styling can be added here
            
        except Exception as e:
            print(f"Error updating header theme: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        # No specific cleanup needed for header component
        pass