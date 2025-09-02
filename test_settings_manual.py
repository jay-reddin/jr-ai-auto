#!/usr/bin/env python3
"""
Manual test for settings window integration - opens the actual settings window.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ui.toga_components.settings_window import SettingsWindow


class SettingsTestApp(toga.App):
    """Test application for settings window."""
    
    def startup(self):
        """Initialize the test application."""
        # Mock app properties needed by settings window
        self.current_api_key = "test_api_key_12345"
        self.current_model = "gemini-2.0-flash-exp"
        self.theme_mode = "dark"
        self.font_size = 14
        self.speech_enabled = True
        self.speech_muted = False
        
        # Mock managers
        self.voice_manager = None
        self.token_tracker = None
        self.config_manager = None
        self.header_component = None
        
        # Create main window
        self.main_window = toga.MainWindow(title="Settings Integration Test")
        
        # Create main container
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
        
        # Add title
        title_label = toga.Label(
            "Settings Window Integration Test",
            style=Pack(
                font_size=18,
                font_weight='bold',
                margin_bottom=20,
                text_align='center'
            )
        )
        main_box.add(title_label)
        
        # Add instructions
        instructions = toga.Label(
            "Click the button below to test the settings window integration.",
            style=Pack(margin_bottom=20, text_align='center')
        )
        main_box.add(instructions)
        
        # Add test button
        test_button = toga.Button(
            "Open Settings Window",
            on_press=self.open_settings,
            style=Pack(
                width=200,
                height=50,
                margin_bottom=20
            )
        )
        main_box.add(test_button)
        
        # Add status label
        self.status_label = toga.Label(
            "Ready to test settings window...",
            style=Pack(margin_bottom=10, text_align='center')
        )
        main_box.add(self.status_label)
        
        # Set window content
        self.main_window.content = main_box
        self.main_window.show()
        
        # Initialize settings window
        self.settings_window = None
    
    def open_settings(self, widget):
        """Open the settings window (same as main app implementation)."""
        try:
            # Initialize settings window if not already created
            if not self.settings_window:
                self.settings_window = SettingsWindow(self)
                self.status_label.text = "Settings window created successfully!"
            
            # Show the settings window
            self.settings_window.show()
            self.status_label.text = "Settings window opened!"
            
        except Exception as e:
            print(f"Error opening settings window: {e}")
            self.status_label.text = f"Error: {str(e)}"
            import traceback
            traceback.print_exc()
    
    def save_configuration(self):
        """Mock save configuration method."""
        print("Mock: Configuration saved!")
        self.status_label.text = "Configuration saved (mock)"
    
    def initialize_agent(self):
        """Mock initialize agent method."""
        print("Mock: Agent initialized!")
        self.status_label.text = "Agent initialized (mock)"
    
    def add_message(self, sender, message):
        """Mock add message method."""
        print(f"Mock message - {sender}: {message}")
        self.status_label.text = f"Message: {message}"
    
    def toggle_theme(self, widget):
        """Mock toggle theme method."""
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        print(f"Mock: Theme toggled to {self.theme_mode}")
        self.status_label.text = f"Theme changed to {self.theme_mode}"


def main():
    """Run the test application."""
    app = SettingsTestApp("Settings Test", "org.example.settingstest")
    app.main_loop()


if __name__ == "__main__":
    main()