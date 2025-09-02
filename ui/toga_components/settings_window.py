"""
Settings Window Component for Toga-based JR AI Control
Provides tabbed interface for application configuration
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from typing import Optional, Dict, Any


class SettingsWindow:
    """
    Settings window with tabbed interface for configuration options
    """
    
    def __init__(self, app_instance):
        self.app = app_instance
        self.window: Optional[toga.Window] = None
        self.option_container: Optional[toga.OptionContainer] = None
        
        # Setting widgets
        self.api_key_input: Optional[toga.TextInput] = None
        self.model_selection: Optional[toga.Selection] = None
        self.theme_selection: Optional[toga.Selection] = None
        self.font_size_slider: Optional[toga.Slider] = None
        self.voice_enabled_switch: Optional[toga.Switch] = None
        self.voice_muted_switch: Optional[toga.Switch] = None
    
    def show(self):
        """Show the settings window"""
        try:
            if not self.window:
                self._create_window()
            
            self.window.show()
            self._load_current_settings()
            
        except Exception as e:
            print(f"Error showing settings window: {e}")
            # Show error message as fallback
            if hasattr(self.app, 'add_message'):
                self.app.add_message("System", f"Failed to open settings window: {e}")
    
    def _create_window(self):
        """Create the settings window and its content"""
        try:
            # Create the window
            self.window = toga.Window(
                title="Settings - JR AI Control",
                size=(600, 500),
                resizable=True
            )
            
            # Create main container
            main_box = toga.Box(
                style=Pack(
                    direction=COLUMN,
                    padding=10
                )
            )
            
            # Create tabbed interface
            self.option_container = toga.OptionContainer(
                style=Pack(flex=1)
            )
            
            # Create tabs
            ai_tab = self._create_ai_tab()
            ui_tab = self._create_ui_tab()
            about_tab = self._create_about_tab()
            
            # Add tabs to container
            self.option_container.add("AI Settings", ai_tab)
            self.option_container.add("UI Settings", ui_tab)
            self.option_container.add("About", about_tab)
            
            main_box.add(self.option_container)
            
            # Create buttons row
            buttons_box = self._create_buttons_row()
            main_box.add(buttons_box)
            
            # Set window content
            self.window.content = main_box
            
        except Exception as e:
            print(f"Error creating settings window: {e}")
            raise
    
    def _create_ai_tab(self) -> toga.Box:
        """Create the AI settings tab"""
        tab_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=15
            )
        )
        
        # API Key section
        api_section = toga.Box(style=Pack(direction=COLUMN, padding=(0, 0, 15, 0)))
        
        api_label = toga.Label(
            "Gemini API Key:",
            style=Pack(padding=(0, 0, 5, 0), font_weight="bold")
        )
        api_section.add(api_label)
        
        self.api_key_input = toga.TextInput(
            placeholder="Enter your Gemini API key...",
            style=Pack(width=400, padding=(0, 0, 5, 0))
        )
        api_section.add(self.api_key_input)
        
        api_help = toga.Label(
            "Get your API key from Google AI Studio",
            style=Pack(font_size=10, padding=(0, 0, 10, 0))
        )
        api_section.add(api_help)
        
        tab_box.add(api_section)
        
        # Model selection section
        model_section = toga.Box(style=Pack(direction=COLUMN, padding=(0, 0, 15, 0)))
        
        model_label = toga.Label(
            "AI Model:",
            style=Pack(padding=(0, 0, 5, 0), font_weight="bold")
        )
        model_section.add(model_label)
        
        model_options = [
            "gemini-2.0-flash-exp",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro"
        ]
        
        self.model_selection = toga.Selection(
            items=model_options,
            style=Pack(width=300, padding=(0, 0, 10, 0))
        )
        model_section.add(self.model_selection)
        
        tab_box.add(model_section)
        
        # Voice settings section
        if self.app.voice_manager and self.app.voice_manager.is_voice_available():
            voice_section = self._create_voice_settings_section()
            tab_box.add(voice_section)
        
        return tab_box
    
    def _create_voice_settings_section(self) -> toga.Box:
        """Create voice settings section"""
        voice_section = toga.Box(style=Pack(direction=COLUMN, padding=(0, 0, 15, 0)))
        
        voice_title = toga.Label(
            "Voice Settings:",
            style=Pack(padding=(0, 0, 10, 0), font_weight="bold")
        )
        voice_section.add(voice_title)
        
        # Voice enabled switch
        voice_enabled_box = toga.Box(style=Pack(direction=ROW, padding=(0, 0, 5, 0)))
        
        voice_enabled_label = toga.Label(
            "Enable Voice Output:",
            style=Pack(padding=(0, 10, 0, 0), width=150)
        )
        voice_enabled_box.add(voice_enabled_label)
        
        self.voice_enabled_switch = toga.Switch(
            style=Pack(padding=(0, 0, 0, 10))
        )
        voice_enabled_box.add(self.voice_enabled_switch)
        
        voice_section.add(voice_enabled_box)
        
        # Voice muted switch
        voice_muted_box = toga.Box(style=Pack(direction=ROW, padding=(0, 0, 5, 0)))
        
        voice_muted_label = toga.Label(
            "Mute Voice Output:",
            style=Pack(padding=(0, 10, 0, 0), width=150)
        )
        voice_muted_box.add(voice_muted_label)
        
        self.voice_muted_switch = toga.Switch(
            style=Pack(padding=(0, 0, 0, 10))
        )
        voice_muted_box.add(self.voice_muted_switch)
        
        voice_section.add(voice_muted_box)
        
        return voice_section
    
    def _create_ui_tab(self) -> toga.Box:
        """Create the UI settings tab"""
        tab_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=15
            )
        )
        
        # Theme selection
        theme_section = toga.Box(style=Pack(direction=COLUMN, padding=(0, 0, 15, 0)))
        
        theme_label = toga.Label(
            "Theme:",
            style=Pack(padding=(0, 0, 5, 0), font_weight="bold")
        )
        theme_section.add(theme_label)
        
        theme_options = ["dark", "light"]
        self.theme_selection = toga.Selection(
            items=theme_options,
            style=Pack(width=200, padding=(0, 0, 10, 0))
        )
        theme_section.add(self.theme_selection)
        
        tab_box.add(theme_section)
        
        # Font size
        font_section = toga.Box(style=Pack(direction=COLUMN, padding=(0, 0, 15, 0)))
        
        font_label = toga.Label(
            "Font Size:",
            style=Pack(padding=(0, 0, 5, 0), font_weight="bold")
        )
        font_section.add(font_label)
        
        self.font_size_slider = toga.Slider(
            min_value=10,
            max_value=24,
            style=Pack(width=300, padding=(0, 0, 10, 0))
        )
        font_section.add(self.font_size_slider)
        
        font_value_label = toga.Label(
            "14px",
            style=Pack(padding=(0, 0, 10, 0))
        )
        font_section.add(font_value_label)
        
        tab_box.add(font_section)
        
        return tab_box
    
    def _create_about_tab(self) -> toga.Box:
        """Create the about tab"""
        tab_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=15
            )
        )
        
        # App info
        app_title = toga.Label(
            "JR AI Control (Toga Edition)",
            style=Pack(
                font_size=18,
                font_weight="bold",
                padding=(0, 0, 10, 0)
            )
        )
        tab_box.add(app_title)
        
        version_label = toga.Label(
            "Version: 2.0.0",
            style=Pack(padding=(0, 0, 5, 0))
        )
        tab_box.add(version_label)
        
        description = toga.Label(
            "AI-powered desktop assistant with voice interaction, built with Toga for cross-platform compatibility.",
            style=Pack(padding=(0, 0, 15, 0))
        )
        tab_box.add(description)
        
        # Token usage info
        if self.app.token_tracker:
            total_tokens = self.app.token_tracker.get_total_tokens()
            token_info = toga.Label(
                f"Total Tokens Used: {total_tokens:,}",
                style=Pack(padding=(0, 0, 10, 0))
            )
            tab_box.add(token_info)
        
        # Keyboard shortcuts
        shortcuts_title = toga.Label(
            "Keyboard Shortcuts:",
            style=Pack(
                font_weight="bold",
                padding=(0, 0, 5, 0)
            )
        )
        tab_box.add(shortcuts_title)
        
        shortcuts_text = """
• Enter: Send message
• Ctrl+M: Toggle microphone
• Ctrl+Shift+S: Toggle speech output
• Ctrl+Shift+M: Toggle speech mute
        """.strip()
        
        shortcuts_label = toga.Label(
            shortcuts_text,
            style=Pack(padding=(0, 0, 10, 0))
        )
        tab_box.add(shortcuts_label)
        
        return tab_box
    
    def _create_buttons_row(self) -> toga.Box:
        """Create the buttons row at the bottom"""
        buttons_box = toga.Box(
            style=Pack(
                direction=ROW,
                padding=(10, 0, 0, 0),
                alignment="right"
            )
        )
        
        # Cancel button
        cancel_button = toga.Button(
            "Cancel",
            on_press=self._cancel_settings,
            style=Pack(
                width=80,
                padding=(0, 10, 0, 0)
            )
        )
        buttons_box.add(cancel_button)
        
        # Save button
        save_button = toga.Button(
            "Save",
            on_press=self._save_settings,
            style=Pack(width=80)
        )
        buttons_box.add(save_button)
        
        return buttons_box
    
    def _load_current_settings(self):
        """Load current settings into the form"""
        try:
            # Load API key
            if self.api_key_input:
                self.api_key_input.value = self.app.current_api_key or ""
            
            # Load model selection
            if self.model_selection:
                self.model_selection.value = self.app.current_model
            
            # Load theme selection
            if self.theme_selection:
                self.theme_selection.value = self.app.theme_mode
            
            # Load font size
            if self.font_size_slider:
                self.font_size_slider.value = self.app.font_size
            
            # Load voice settings
            if self.voice_enabled_switch:
                self.voice_enabled_switch.value = self.app.speech_enabled
            
            if self.voice_muted_switch:
                self.voice_muted_switch.value = self.app.speech_muted
                
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def _save_settings(self, widget):
        """Save settings and apply changes"""
        try:
            # Save API key
            if self.api_key_input:
                self.app.current_api_key = self.api_key_input.value.strip()
            
            # Save model selection
            if self.model_selection:
                self.app.current_model = self.model_selection.value
            
            # Save theme selection
            if self.theme_selection and self.theme_selection.value != self.app.theme_mode:
                # Use the existing toggle_theme method to change theme
                if self.theme_selection.value != self.app.theme_mode:
                    self.app.toggle_theme(None)
            
            # Save font size
            if self.font_size_slider:
                self.app.font_size = int(self.font_size_slider.value)
            
            # Save voice settings
            if self.voice_enabled_switch:
                self.app.speech_enabled = self.voice_enabled_switch.value
                if self.app.voice_manager:
                    self.app.voice_manager.toggle_speech_enabled(self.voice_enabled_switch.value)
            
            if self.voice_muted_switch:
                self.app.speech_muted = self.voice_muted_switch.value
                if self.app.voice_manager:
                    self.app.voice_manager.toggle_speech_muted(self.voice_muted_switch.value)
            
            # Save configuration
            self.app.save_configuration()
            
            # Reinitialize agent if API key was changed
            if self.api_key_input and self.api_key_input.value.strip():
                if hasattr(self.app, 'initialize_agent'):
                    self.app.initialize_agent()
            
            # Update header display
            if hasattr(self.app, 'header_component') and self.app.header_component:
                self.app.header_component.update_model_display(self.app.current_model)
                self.app.header_component.update_connection_status(bool(self.app.current_api_key))
            
            # Close window
            self.window.close()
            
        except Exception as e:
            print(f"Error saving settings: {e}")
            if hasattr(self.app, 'add_message'):
                self.app.add_message("System", f"Failed to save settings: {e}")
    
    def _cancel_settings(self, widget):
        """Cancel settings changes and close window"""
        try:
            self.window.close()
        except Exception as e:
            print(f"Error canceling settings: {e}")