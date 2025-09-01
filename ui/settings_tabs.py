"""
Tabbed Settings Interface for JR AI Control
Implements comprehensive settings with AI, UI, and About tabs using Material Design 3
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import os
from datetime import datetime

from ui.material_design import get_theme, create_md3_widget_config
from ui.enhanced_components import MD3Frame, MD3Card, MD3Button, MD3Entry, create_md3_tooltip
from utils.token_tracker import get_token_tracker
from voice.voice_manager import get_voice_manager

# Google Generative AI will be imported only when needed
GENAI_AVAILABLE = True


class SettingsTabManager:
    """Manages the tabbed settings interface with AI, UI, and About tabs"""
    
    def __init__(self, parent_window, app_instance):
        self.parent = parent_window
        self.app = app_instance
        self.settings_window = None
        self.notebook = None
        
        # Voice manager reference
        self.voice_manager = get_voice_manager()
        
        # Token tracker reference
        self.token_tracker = get_token_tracker()
        
        # Settings variables
        self.api_key_var = tk.StringVar(value=self.app.current_api_key)
        self.model_var = tk.StringVar(value=self.app.current_model)
        self.theme_var = tk.StringVar(value=self.app.theme_mode)
        self.speech_enabled_var = tk.BooleanVar(value=self.app.speech_enabled)
        self.speech_muted_var = tk.BooleanVar(value=self.app.speech_muted)
        
        # UI settings variables with defaults
        self.screenshot_size_var = tk.StringVar(value=getattr(self.app, 'screenshot_size', 'medium'))
        self.screenshot_wait_var = tk.IntVar(value=getattr(self.app, 'screenshot_wait_duration', 3))
        self.notification_enabled_var = tk.BooleanVar(value=getattr(self.app, 'notification_enabled', True))
        self.font_size_var = tk.IntVar(value=getattr(self.app, 'font_size', 14))
        self.window_opacity_var = tk.DoubleVar(value=getattr(self.app, 'window_opacity', 1.0))
        
        # Voice settings variables
        self.voice_rate_var = tk.IntVar(value=getattr(self.voice_manager, 'voice_rate', 200))
        self.voice_volume_var = tk.DoubleVar(value=getattr(self.voice_manager, 'voice_volume', 0.8))
        self.voice_selection_var = tk.StringVar()
        
        # Voice mapping for ID to name conversion
        self.voice_mapping = {}
        
        # Test status label reference
        self.test_status_label = None
    
    def open_settings(self):
        """Open the tabbed settings window"""
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return
        
        self.create_settings_window()
    
    def create_settings_window(self):
        """Create the main settings window with tabbed interface"""
        self.settings_window = tk.Toplevel(self.parent)
        self.settings_window.title("Settings - JR AI Control")
        
        # Apply MD3 theme
        theme = get_theme()
        self.settings_window.configure(bg=theme.colors['surface'])
        self.settings_window.geometry("600x500")
        self.settings_window.resizable(True, True)
        
        # Center the window
        self.settings_window.transient(self.parent)
        self.settings_window.grab_set()
        
        # Main container
        main_container = MD3Frame(self.settings_window)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_container, text="Settings", style='MD3.Headline.Small.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.create_notebook(main_container)
        
        # Action buttons
        self.create_action_buttons(main_container)
        
        # Handle window close
        self.settings_window.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_notebook(self, parent):
        """Create the notebook widget with tabs"""
        # Create notebook with MD3 styling
        style = ttk.Style()
        
        # Configure notebook style for MD3
        theme = get_theme()
        style.configure('MD3.TNotebook', 
                       background=theme.colors['surface'],
                       borderwidth=0,
                       tabmargins=[2, 5, 2, 0])
        
        style.configure('MD3.TNotebook.Tab',
                       background=theme.colors['surface_variant'],
                       foreground=theme.colors['on_surface'],
                       padding=[20, 10],
                       font=theme.typography['title_medium'])
        
        style.map('MD3.TNotebook.Tab',
                 background=[('selected', theme.colors['primary_container']),
                           ('active', theme.colors['secondary_container'])],
                 foreground=[('selected', theme.colors['on_primary_container']),
                           ('active', theme.colors['on_secondary_container'])])
        
        self.notebook = ttk.Notebook(parent, style='MD3.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create tabs
        self.create_ai_tab()
        self.create_ui_tab()
        self.create_about_tab()
        
        # Add settings management buttons
        self.create_settings_management_buttons()
    
    def create_ai_tab(self):
        """Create the AI settings tab"""
        ai_frame = MD3Frame(self.notebook)
        self.notebook.add(ai_frame, text="AI")
        
        # Scrollable content
        canvas = tk.Canvas(ai_frame, bg=get_theme().colors['surface'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(ai_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = MD3Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 10))
        scrollbar.pack(side="right", fill="y")
        
        # API Key section
        self.create_api_key_section(scrollable_frame)
        
        # Model selection section
        self.create_model_section(scrollable_frame)
        
        # Voice settings section
        if self.voice_manager.is_voice_available():
            self.create_voice_settings_section(scrollable_frame)
    
    def create_api_key_section(self, parent):
        """Create API key configuration section"""
        api_card = MD3Card(parent)
        api_card.pack(fill=tk.X, pady=(0, 16))
        
        api_content = MD3Frame(api_card)
        api_content.pack(fill=tk.X, padx=16, pady=16)
        
        # API Key label
        api_label = ttk.Label(api_content, text="Gemini API Key", style='MD3.Title.Medium.TLabel')
        api_label.pack(anchor=tk.W, pady=(0, 8))
        
        # API Key input with test button
        api_input_frame = MD3Frame(api_content)
        api_input_frame.pack(fill=tk.X, pady=(0, 8))
        
        api_entry = MD3Entry(api_input_frame, textvariable=self.api_key_var,
                           show='*' if self.api_key_var.get() else '',
                           font=get_theme().typography['body_large'])
        api_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 12))
        create_md3_tooltip(api_entry, "Enter your Google Gemini API key")
        
        # Test button
        test_btn = MD3Button(api_input_frame, text="Test", style='secondary',
                           command=self.test_api_key)
        test_btn.pack(side=tk.RIGHT)
        create_md3_tooltip(test_btn, "Test API key validity")
        
        # Test status
        self.test_status_label = ttk.Label(api_content, text="", style='MD3.Body.Small.TLabel')
        self.test_status_label.pack(anchor=tk.W, pady=(4, 0))
    
    def create_model_section(self, parent):
        """Create model selection section"""
        model_card = MD3Card(parent)
        model_card.pack(fill=tk.X, pady=(0, 16))
        
        model_content = MD3Frame(model_card)
        model_content.pack(fill=tk.X, padx=16, pady=16)
        
        # Model label
        model_label = ttk.Label(model_content, text="AI Model", style='MD3.Title.Medium.TLabel')
        model_label.pack(anchor=tk.W, pady=(0, 8))
        
        # Model selection frame
        model_selection_frame = MD3Frame(model_content)
        model_selection_frame.pack(fill=tk.X, pady=(0, 8))
        
        # Model dropdown
        model_combo = ttk.Combobox(model_selection_frame, textvariable=self.model_var,
                                  values=self.app.available_models,
                                  state='readonly',
                                  style='MD3.TCombobox',
                                  font=get_theme().typography['body_large'])
        model_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        create_md3_tooltip(model_combo, "Select the Gemini model to use")
        
        # Refresh models button
        refresh_btn = MD3Button(model_selection_frame, text="🔄", 
                               command=self.refresh_available_models,
                               style='MD3.Outline.TButton')
        refresh_btn.pack(side=tk.RIGHT, padx=(8, 0))
        create_md3_tooltip(refresh_btn, "Refresh available models from Google")
    
    def create_voice_settings_section(self, parent):
        """Create voice settings section"""
        voice_card = MD3Card(parent)
        voice_card.pack(fill=tk.X, pady=(0, 16))
        
        voice_content = MD3Frame(voice_card)
        voice_content.pack(fill=tk.X, padx=16, pady=16)
        
        # Voice settings label
        voice_label = ttk.Label(voice_content, text="Voice Settings", style='MD3.Title.Medium.TLabel')
        voice_label.pack(anchor=tk.W, pady=(0, 12))
        
        # Speech enabled toggle
        speech_frame = MD3Frame(voice_content)
        speech_frame.pack(fill=tk.X, pady=(0, 8))
        
        speech_desc = ttk.Label(speech_frame, text="Enable speech output", style='MD3.Body.Medium.TLabel')
        speech_desc.pack(side=tk.LEFT)
        
        speech_check = ttk.Checkbutton(speech_frame, variable=self.speech_enabled_var, 
                                     style='MD3.TCheckbutton')
        speech_check.pack(side=tk.RIGHT)
        create_md3_tooltip(speech_check, "Enable AI voice responses")
        
        # Speech mute toggle
        mute_frame = MD3Frame(voice_content)
        mute_frame.pack(fill=tk.X, pady=(0, 12))
        
        mute_desc = ttk.Label(mute_frame, text="Mute speech output", style='MD3.Body.Medium.TLabel')
        mute_desc.pack(side=tk.LEFT)
        
        mute_check = ttk.Checkbutton(mute_frame, variable=self.speech_muted_var,
                                   style='MD3.TCheckbutton')
        mute_check.pack(side=tk.RIGHT)
        create_md3_tooltip(mute_check, "Mute voice output while keeping recognition active")
        
        # Voice rate slider
        rate_frame = MD3Frame(voice_content)
        rate_frame.pack(fill=tk.X, pady=(0, 8))
        
        rate_label = ttk.Label(rate_frame, text="Speech Rate", style='MD3.Body.Medium.TLabel')
        rate_label.pack(anchor=tk.W)
        
        rate_value_label = ttk.Label(rate_frame, text=f"{self.voice_rate_var.get()}", 
                                   style='MD3.Body.Small.TLabel')
        rate_value_label.pack(anchor=tk.E)
        
        rate_scale = ttk.Scale(rate_frame, from_=100, to=300, variable=self.voice_rate_var,
                             orient=tk.HORIZONTAL, style='MD3.Horizontal.TScale',
                             command=lambda v: self._update_voice_rate_display(rate_value_label, v))
        rate_scale.pack(fill=tk.X, pady=(4, 8))
        create_md3_tooltip(rate_scale, "Adjust speech rate (100-300 words per minute)")
        
        # Voice volume slider
        volume_frame = MD3Frame(voice_content)
        volume_frame.pack(fill=tk.X, pady=(0, 8))
        
        volume_label = ttk.Label(volume_frame, text="Speech Volume", style='MD3.Body.Medium.TLabel')
        volume_label.pack(anchor=tk.W)
        
        volume_value_label = ttk.Label(volume_frame, text=f"{self.voice_volume_var.get():.1f}", 
                                     style='MD3.Body.Small.TLabel')
        volume_value_label.pack(anchor=tk.E)
        
        volume_scale = ttk.Scale(volume_frame, from_=0.0, to=1.0, variable=self.voice_volume_var,
                               orient=tk.HORIZONTAL, style='MD3.Horizontal.TScale',
                               command=lambda v: self._update_voice_volume_display(volume_value_label, v))
        volume_scale.pack(fill=tk.X, pady=(4, 8))
        create_md3_tooltip(volume_scale, "Adjust speech volume (0.0-1.0)")
        
        # Voice selection dropdown
        voices = self.voice_manager.get_available_voices()
        if voices:
            voice_select_frame = MD3Frame(voice_content)
            voice_select_frame.pack(fill=tk.X)
            
            voice_select_label = ttk.Label(voice_select_frame, text="Voice", style='MD3.Body.Medium.TLabel')
            voice_select_label.pack(anchor=tk.W, pady=(0, 4))
            
            # Store voice mapping for later use
            self.voice_mapping = {name: voice_id for voice_id, name in voices}
            voice_names = [name for voice_id, name in voices]
            
            # Set default voice if not already set
            if voice_names and not self.voice_selection_var.get():
                self.voice_selection_var.set(voice_names[0])
            
            voice_combo = ttk.Combobox(voice_select_frame, textvariable=self.voice_selection_var,
                                     values=voice_names, state='readonly',
                                     style='MD3.TCombobox',
                                     font=get_theme().typography['body_medium'])
            voice_combo.pack(fill=tk.X)
            create_md3_tooltip(voice_combo, "Select voice for speech output")
    
    def _update_voice_rate_display(self, label, value):
        """Update voice rate display label"""
        label.config(text=f"{int(float(value))}")
    
    def _update_voice_volume_display(self, label, value):
        """Update voice volume display label"""
        label.config(text=f"{float(value):.1f}")
    
    def create_ui_tab(self):
        """Create the UI settings tab"""
        ui_frame = MD3Frame(self.notebook)
        self.notebook.add(ui_frame, text="UI")
        
        # Scrollable content
        canvas = tk.Canvas(ui_frame, bg=get_theme().colors['surface'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(ui_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = MD3Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 10))
        scrollbar.pack(side="right", fill="y")
        
        # Theme settings
        self.create_theme_section(scrollable_frame)
        
        # Screenshot settings
        self.create_screenshot_section(scrollable_frame)
        
        # Notification settings
        self.create_notification_section(scrollable_frame)
        
        # UI customization
        self.create_ui_customization_section(scrollable_frame)
    
    def create_theme_section(self, parent):
        """Create theme settings section"""
        theme_card = MD3Card(parent)
        theme_card.pack(fill=tk.X, pady=(0, 16))
        
        theme_content = MD3Frame(theme_card)
        theme_content.pack(fill=tk.X, padx=16, pady=16)
        
        # Theme label
        theme_label = ttk.Label(theme_content, text="Appearance", style='MD3.Title.Medium.TLabel')
        theme_label.pack(anchor=tk.W, pady=(0, 12))
        
        # Theme selection
        theme_frame = MD3Frame(theme_content)
        theme_frame.pack(fill=tk.X)
        
        theme_desc = ttk.Label(theme_frame, text="Dark mode", style='MD3.Body.Medium.TLabel')
        theme_desc.pack(side=tk.LEFT)
        
        # Theme toggle (simplified for now)
        theme_check = ttk.Checkbutton(theme_frame, 
                                    variable=tk.BooleanVar(value=self.theme_var.get() == 'dark'),
                                    style='MD3.TCheckbutton',
                                    command=self.toggle_theme)
        theme_check.pack(side=tk.RIGHT)
        create_md3_tooltip(theme_check, "Toggle between dark and light themes")
    
    def create_screenshot_section(self, parent):
        """Create screenshot settings section"""
        screenshot_card = MD3Card(parent)
        screenshot_card.pack(fill=tk.X, pady=(0, 16))
        
        screenshot_content = MD3Frame(screenshot_card)
        screenshot_content.pack(fill=tk.X, padx=16, pady=16)
        
        # Screenshot settings label
        screenshot_label = ttk.Label(screenshot_content, text="Screenshot Settings", 
                                   style='MD3.Title.Medium.TLabel')
        screenshot_label.pack(anchor=tk.W, pady=(0, 12))
        
        # Screenshot size selection
        size_frame = MD3Frame(screenshot_content)
        size_frame.pack(fill=tk.X, pady=(0, 8))
        
        size_label = ttk.Label(size_frame, text="Thumbnail Size", style='MD3.Body.Medium.TLabel')
        size_label.pack(anchor=tk.W)
        
        size_combo = ttk.Combobox(size_frame, textvariable=self.screenshot_size_var,
                                values=['small', 'medium', 'large'],
                                state='readonly',
                                style='MD3.TCombobox',
                                font=get_theme().typography['body_medium'])
        size_combo.pack(fill=tk.X, pady=(4, 0))
        create_md3_tooltip(size_combo, "Select thumbnail size for screenshots in chat")
        
        # Screenshot wait duration
        wait_frame = MD3Frame(screenshot_content)
        wait_frame.pack(fill=tk.X)
        
        wait_label = ttk.Label(wait_frame, text="Screenshot Wait Duration", style='MD3.Body.Medium.TLabel')
        wait_label.pack(anchor=tk.W)
        
        wait_value_label = ttk.Label(wait_frame, text=f"{self.screenshot_wait_var.get()}s", 
                                   style='MD3.Body.Small.TLabel')
        wait_value_label.pack(anchor=tk.E)
        
        wait_scale = ttk.Scale(wait_frame, from_=1, to=10, variable=self.screenshot_wait_var,
                             orient=tk.HORIZONTAL, style='MD3.Horizontal.TScale',
                             command=lambda v: wait_value_label.config(text=f"{int(float(v))}s"))
        wait_scale.pack(fill=tk.X, pady=(4, 0))
        create_md3_tooltip(wait_scale, "Time to wait before taking screenshots (1-10 seconds)")
    
    def create_notification_section(self, parent):
        """Create notification settings section"""
        notification_card = MD3Card(parent)
        notification_card.pack(fill=tk.X, pady=(0, 16))
        
        notification_content = MD3Frame(notification_card)
        notification_content.pack(fill=tk.X, padx=16, pady=16)
        
        # Notification label
        notification_label = ttk.Label(notification_content, text="Notifications", 
                                     style='MD3.Title.Medium.TLabel')
        notification_label.pack(anchor=tk.W, pady=(0, 12))
        
        # Notification toggle
        notification_frame = MD3Frame(notification_content)
        notification_frame.pack(fill=tk.X)
        
        notification_desc = ttk.Label(notification_frame, text="Enable notifications", 
                                    style='MD3.Body.Medium.TLabel')
        notification_desc.pack(side=tk.LEFT)
        
        notification_check = ttk.Checkbutton(notification_frame, variable=self.notification_enabled_var,
                                           style='MD3.TCheckbutton')
        notification_check.pack(side=tk.RIGHT)
        create_md3_tooltip(notification_check, "Enable system notifications for task completion")
    
    def create_ui_customization_section(self, parent):
        """Create UI customization section"""
        ui_card = MD3Card(parent)
        ui_card.pack(fill=tk.X, pady=(0, 16))
        
        ui_content = MD3Frame(ui_card)
        ui_content.pack(fill=tk.X, padx=16, pady=16)
        
        # UI customization label
        ui_label = ttk.Label(ui_content, text="UI Customization", style='MD3.Title.Medium.TLabel')
        ui_label.pack(anchor=tk.W, pady=(0, 12))
        
        # Font size slider
        font_frame = MD3Frame(ui_content)
        font_frame.pack(fill=tk.X, pady=(0, 8))
        
        font_label = ttk.Label(font_frame, text="Font Size", style='MD3.Body.Medium.TLabel')
        font_label.pack(anchor=tk.W)
        
        font_value_label = ttk.Label(font_frame, text=f"{self.font_size_var.get()}px", 
                                   style='MD3.Body.Small.TLabel')
        font_value_label.pack(anchor=tk.E)
        
        font_scale = ttk.Scale(font_frame, from_=10, to=20, variable=self.font_size_var,
                             orient=tk.HORIZONTAL, style='MD3.Horizontal.TScale',
                             command=lambda v: font_value_label.config(text=f"{int(float(v))}px"))
        font_scale.pack(fill=tk.X, pady=(4, 8))
        create_md3_tooltip(font_scale, "Adjust application font size")
        
        # Window opacity slider
        opacity_frame = MD3Frame(ui_content)
        opacity_frame.pack(fill=tk.X)
        
        opacity_label = ttk.Label(opacity_frame, text="Window Opacity", style='MD3.Body.Medium.TLabel')
        opacity_label.pack(anchor=tk.W)
        
        opacity_value_label = ttk.Label(opacity_frame, text=f"{self.window_opacity_var.get():.1f}", 
                                      style='MD3.Body.Small.TLabel')
        opacity_value_label.pack(anchor=tk.E)
        
        opacity_scale = ttk.Scale(opacity_frame, from_=0.5, to=1.0, variable=self.window_opacity_var,
                                orient=tk.HORIZONTAL, style='MD3.Horizontal.TScale',
                                command=lambda v: opacity_value_label.config(text=f"{float(v):.1f}"))
        opacity_scale.pack(fill=tk.X, pady=(4, 0))
        create_md3_tooltip(opacity_scale, "Adjust window transparency")
    
    def create_about_tab(self):
        """Create the About tab with app information"""
        about_frame = MD3Frame(self.notebook)
        self.notebook.add(about_frame, text="About")
        
        # Scrollable content
        canvas = tk.Canvas(about_frame, bg=get_theme().colors['surface'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(about_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = MD3Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 10))
        scrollbar.pack(side="right", fill="y")
        
        # App information
        self.create_app_info_section(scrollable_frame)
        
        # Tips and tricks
        self.create_tips_section(scrollable_frame)
        
        # Token usage statistics
        self.create_token_stats_section(scrollable_frame)
        
        # Developer information
        self.create_developer_section(scrollable_frame)
    
    def create_app_info_section(self, parent):
        """Create application information section"""
        app_card = MD3Card(parent)
        app_card.pack(fill=tk.X, pady=(0, 16))
        
        app_content = MD3Frame(app_card)
        app_content.pack(fill=tk.X, padx=16, pady=16)
        
        # App title
        app_title = ttk.Label(app_content, text="JR AI Control", style='MD3.Headline.Medium.TLabel')
        app_title.pack(anchor=tk.W, pady=(0, 8))
        
        # Version info from environment
        version = os.getenv("VERSION", "1.0.0")
        version_label = ttk.Label(app_content, text=f"Version: {version}", style='MD3.Body.Large.TLabel')
        version_label.pack(anchor=tk.W, pady=(0, 4))
        
        # Build date/last changes
        last_changes = os.getenv("LAST_CHANGES", "[]")
        try:
            import ast
            changes_list = ast.literal_eval(last_changes)
            if changes_list:
                changes_text = f"Latest: {changes_list[0]}"
                changes_label = ttk.Label(app_content, text=changes_text, style='MD3.Body.Medium.TLabel')
                changes_label.pack(anchor=tk.W, pady=(0, 8))
        except:
            pass
        
        # Description
        desc_text = ("Advanced AI-powered automation tool with voice interaction, "
                    "Material Design 3 interface, and comprehensive screenshot management.")
        desc_label = ttk.Label(app_content, text=desc_text, style='MD3.Body.Medium.TLabel', 
                             wraplength=500)
        desc_label.pack(anchor=tk.W, pady=(8, 0))
    
    def create_tips_section(self, parent):
        """Create tips and tricks section"""
        tips_card = MD3Card(parent)
        tips_card.pack(fill=tk.X, pady=(0, 16))
        
        tips_content = MD3Frame(tips_card)
        tips_content.pack(fill=tk.X, padx=16, pady=16)
        
        # Tips title
        tips_title = ttk.Label(tips_content, text="Tips & Keyboard Shortcuts", 
                             style='MD3.Title.Medium.TLabel')
        tips_title.pack(anchor=tk.W, pady=(0, 12))
        
        # Keyboard shortcuts section
        shortcuts_subtitle = ttk.Label(tips_content, text="Keyboard Shortcuts:", 
                                     style='MD3.Title.Small.TLabel')
        shortcuts_subtitle.pack(anchor=tk.W, pady=(0, 8))
        
        shortcuts = [
            "• Ctrl+M: Toggle microphone for voice input",
            "• Ctrl+Shift+S: Toggle speech output on/off", 
            "• Ctrl+Shift+M: Toggle speech mute",
            "• Ctrl+T: Switch between dark/light theme",
            "• Ctrl+S: Open settings window",
            "• Enter: Send message in chat",
            "• Ctrl+Enter: Send message without clearing input",
            "• Escape: Cancel current operation"
        ]
        
        for shortcut in shortcuts:
            shortcut_label = ttk.Label(tips_content, text=shortcut, style='MD3.Body.Medium.TLabel')
            shortcut_label.pack(anchor=tk.W, pady=1)
        
        # Features section
        features_subtitle = ttk.Label(tips_content, text="Features & Tips:", 
                                    style='MD3.Title.Small.TLabel')
        features_subtitle.pack(anchor=tk.W, pady=(12, 8))
        
        features = [
            "• Click screenshot thumbnails to view full size images",
            "• Use resend button to quickly repeat messages",
            "• Copy button copies message text to clipboard",
            "• Delete button removes messages from chat history",
            "• Voice recognition works continuously when enabled",
            "• Screenshot size can be adjusted in UI settings",
            "• Notifications show task completion status",
            "• Token usage is tracked and displayed per message",
            "• Settings are automatically saved and restored"
        ]
        
        for feature in features:
            feature_label = ttk.Label(tips_content, text=feature, style='MD3.Body.Medium.TLabel')
            feature_label.pack(anchor=tk.W, pady=1)
    
    def create_token_stats_section(self, parent):
        """Create token usage statistics section"""
        token_card = MD3Card(parent)
        token_card.pack(fill=tk.X, pady=(0, 16))
        
        token_content = MD3Frame(token_card)
        token_content.pack(fill=tk.X, padx=16, pady=16)
        
        # Token stats title
        token_title = ttk.Label(token_content, text="Token Usage Statistics", 
                              style='MD3.Title.Medium.TLabel')
        token_title.pack(anchor=tk.W, pady=(0, 12))
        
        # Get detailed statistics
        total_tokens = self.token_tracker.get_total_tokens()
        session_stats = self.token_tracker.get_session_stats()
        
        # Current session stats
        session_frame = MD3Frame(token_content)
        session_frame.pack(fill=tk.X, pady=(0, 8))
        
        session_label = ttk.Label(session_frame, text="Current Session:", 
                                style='MD3.Title.Small.TLabel')
        session_label.pack(anchor=tk.W, pady=(0, 4))
        
        session_tokens_label = ttk.Label(session_frame, 
                                       text=f"• Messages: {session_stats['messages_count']}", 
                                       style='MD3.Body.Medium.TLabel')
        session_tokens_label.pack(anchor=tk.W, pady=1)
        
        session_total_label = ttk.Label(session_frame, 
                                      text=f"• Session tokens: {session_stats['session_tokens']:,}", 
                                      style='MD3.Body.Medium.TLabel')
        session_total_label.pack(anchor=tk.W, pady=1)
        
        # Total stats
        total_frame = MD3Frame(token_content)
        total_frame.pack(fill=tk.X, pady=(8, 12))
        
        total_title_label = ttk.Label(total_frame, text="All Time:", 
                                    style='MD3.Title.Small.TLabel')
        total_title_label.pack(anchor=tk.W, pady=(0, 4))
        
        total_label = ttk.Label(total_frame, text=f"• Total tokens used: {total_tokens:,}", 
                              style='MD3.Body.Large.TLabel')
        total_label.pack(anchor=tk.W, pady=1)
        
        # Estimated cost (rough approximation for Gemini)
        estimated_cost = total_tokens * 0.000001  # Very rough estimate
        cost_label = ttk.Label(total_frame, 
                             text=f"• Estimated cost: ~${estimated_cost:.4f} USD", 
                             style='MD3.Body.Medium.TLabel')
        cost_label.pack(anchor=tk.W, pady=1)
        
        # Usage info
        info_label = ttk.Label(token_content, 
                             text="Note: Token counts are approximate for Gemini models", 
                             style='MD3.Body.Small.TLabel')
        info_label.pack(anchor=tk.W, pady=(0, 12))
        
        # Reset button
        reset_btn = MD3Button(token_content, text="Reset Token Counter", style='secondary',
                            command=self.reset_token_counter)
        reset_btn.pack(anchor=tk.W)
        create_md3_tooltip(reset_btn, "Reset the total token usage counter")
    
    def create_developer_section(self, parent):
        """Create developer information section"""
        dev_card = MD3Card(parent)
        dev_card.pack(fill=tk.X, pady=(0, 16))
        
        dev_content = MD3Frame(dev_card)
        dev_content.pack(fill=tk.X, padx=16, pady=16)
        
        # Developer title
        dev_title = ttk.Label(dev_content, text="Developer Information", 
                            style='MD3.Title.Medium.TLabel')
        dev_title.pack(anchor=tk.W, pady=(0, 12))
        
        # Technical details
        tech_info = [
            "Developed with ❤️ using Python and Tkinter",
            "Powered by Google Gemini AI (gemini-2.0-flash-exp)",
            "Material Design 3 interface implementation",
            "Voice interaction using Windows Speech API",
            "Screenshot management with PIL/Pillow",
            "Automation powered by PyAutoGUI"
        ]
        
        for info in tech_info:
            info_label = ttk.Label(dev_content, text=info, style='MD3.Body.Medium.TLabel')
            info_label.pack(anchor=tk.W, pady=1)
        
        # Contact information
        contact_subtitle = ttk.Label(dev_content, text="Contact & Support:", 
                                   style='MD3.Title.Small.TLabel')
        contact_subtitle.pack(anchor=tk.W, pady=(12, 8))
        
        contact_info = [
            "• Developer: JR Development Team",
            "• Email: support@jraicontrol.com (placeholder)",
            "• Website: https://jraicontrol.com (placeholder)"
        ]
        
        for contact in contact_info:
            contact_label = ttk.Label(dev_content, text=contact, style='MD3.Body.Medium.TLabel')
            contact_label.pack(anchor=tk.W, pady=1)
        
        # Links section
        links_subtitle = ttk.Label(dev_content, text="Documentation & Support:", 
                                 style='MD3.Title.Small.TLabel')
        links_subtitle.pack(anchor=tk.W, pady=(12, 8))
        
        links_info = [
            "• GitHub Repository: https://github.com/jr-dev/ai-control (placeholder)",
            "• User Documentation: https://docs.jraicontrol.com (placeholder)",
            "• Issue Tracker: https://github.com/jr-dev/ai-control/issues (placeholder)",
            "• Feature Requests: https://github.com/jr-dev/ai-control/discussions (placeholder)",
            "• Community Forum: https://community.jraicontrol.com (placeholder)"
        ]
        
        for link in links_info:
            link_label = ttk.Label(dev_content, text=link, style='MD3.Body.Medium.TLabel')
            link_label.pack(anchor=tk.W, pady=1)
        
        # License information
        license_subtitle = ttk.Label(dev_content, text="License & Legal:", 
                                   style='MD3.Title.Small.TLabel')
        license_subtitle.pack(anchor=tk.W, pady=(12, 8))
        
        license_info = [
            "• Licensed under MIT License",
            "• Copyright © 2024 JR Development Team",
            "• Third-party licenses available in documentation"
        ]
        
        for license_item in license_info:
            license_label = ttk.Label(dev_content, text=license_item, style='MD3.Body.Medium.TLabel')
            license_label.pack(anchor=tk.W, pady=1)
    
    def create_action_buttons(self, parent):
        """Create action buttons (Cancel, Save)"""
        btn_frame = MD3Frame(parent)
        btn_frame.pack(fill=tk.X, pady=(16, 0))
        
        # Cancel button
        cancel_btn = MD3Button(btn_frame, text="Cancel", style='secondary',
                             command=self.on_close)
        cancel_btn.pack(side=tk.RIGHT, padx=(12, 0))
        create_md3_tooltip(cancel_btn, "Cancel changes and close settings")
        
        # Save button
        save_btn = MD3Button(btn_frame, text="Save", style='primary',
                           command=self.save_settings)
        save_btn.pack(side=tk.RIGHT)
        create_md3_tooltip(save_btn, "Save all settings and apply changes")
    
    def toggle_theme(self):
        """Toggle theme between dark and light"""
        current_theme = self.theme_var.get()
        new_theme = 'light' if current_theme == 'dark' else 'dark'
        self.theme_var.set(new_theme)
    
    def test_api_key(self):
        """Test the API key validity"""
        api_key = self.api_key_var.get().strip()
        
        if not api_key:
            self.test_status_label.config(text="Please enter an API key", 
                                        foreground=get_theme().colors['error'])
            return
        
        self.test_status_label.config(text="Testing...", 
                                    foreground=get_theme().colors['primary'])
        
        def test_in_thread():
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                test_model = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash-exp",
                    google_api_key=api_key
                )
                
                # Simple test invoke
                response = test_model.invoke("Hello")
                
                # Update UI in main thread
                self.settings_window.after(0, lambda: self.test_status_label.config(
                    text="✓ API key is valid", 
                    foreground=get_theme().colors['secondary']))
                
            except Exception as e:
                error_msg = f"✗ API key test failed: {str(e)[:50]}..."
                self.settings_window.after(0, lambda: self.test_status_label.config(
                    text=error_msg, 
                    foreground=get_theme().colors['error']))
        
        # Run test in separate thread
        threading.Thread(target=test_in_thread, daemon=True).start()
    
    def reset_token_counter(self):
        """Reset the token usage counter"""
        if messagebox.askyesno("Reset Token Counter", 
                              "Are you sure you want to reset the token usage counter?\n\n"
                              "This will reset both session and total token counts to zero.",
                              parent=self.settings_window):
            try:
                self.token_tracker.reset_total_tokens()
                # Also clear message tokens for current session
                self.token_tracker.message_tokens = {}
                self.token_tracker.save_token_data()
                
                # Show success message
                messagebox.showinfo("Token Counter Reset", 
                                  "Token usage counter has been reset successfully.",
                                  parent=self.settings_window)
                
                # Refresh the display
                self.settings_window.destroy()
                self.open_settings()
                
            except Exception as e:
                messagebox.showerror("Error", 
                                   f"Failed to reset token counter: {str(e)}",
                                   parent=self.settings_window)
    
    def refresh_available_models(self):
        """Refresh the list of available Google Gemini models"""
        def refresh_in_thread():
            try:
                # Import genai only when needed
                try:
                    import google.generativeai as genai
                except ImportError:
                    messagebox.showwarning("Feature Unavailable", 
                                         "Google Generative AI library not available.\n"
                                         "Cannot refresh model list.",
                                         parent=self.settings_window)
                    return
                
                # Configure the API key
                api_key = self.api_key_var.get().strip()
                if not api_key:
                    messagebox.showwarning("API Key Required", 
                                         "Please enter your Google API key first.",
                                         parent=self.settings_window)
                    return
                
                genai.configure(api_key=api_key)
                
                # Get available models
                models = []
                try:
                    for model in genai.list_models():
                        if 'generateContent' in model.supported_generation_methods:
                            model_name = model.name.replace('models/', '')
                            if 'gemini' in model_name.lower():
                                models.append(model_name)
                except Exception as e:
                    print(f"Error listing models: {e}")
                    # Fallback to default models if API call fails
                    models = [
                        "gemini-2.0-flash-exp",
                        "gemini-1.5-pro",
                        "gemini-1.5-flash",
                        "gemini-1.0-pro"
                    ]
                
                if not models:
                    models = [
                        "gemini-2.0-flash-exp",
                        "gemini-1.5-pro", 
                        "gemini-1.5-flash",
                        "gemini-1.0-pro"
                    ]
                
                # Update the app's available models
                self.app.available_models = sorted(models)
                
                # Update the combobox values
                def update_ui():
                    try:
                        # Find the model combobox and update its values
                        for widget in self.settings_window.winfo_children():
                            self._update_combobox_values(widget, models)
                        
                        messagebox.showinfo("Models Refreshed", 
                                          f"Found {len(models)} available Gemini models.",
                                          parent=self.settings_window)
                    except Exception as e:
                        print(f"Error updating UI: {e}")
                
                # Schedule UI update on main thread
                self.settings_window.after(0, update_ui)
                
            except Exception as e:
                error_msg = f"Failed to refresh models: {str(e)}"
                print(error_msg)
                self.settings_window.after(0, lambda: messagebox.showerror("Refresh Failed", 
                                                                          error_msg,
                                                                          parent=self.settings_window))
        
        # Run in background thread
        threading.Thread(target=refresh_in_thread, daemon=True).start()
    
    def _update_combobox_values(self, widget, models):
        """Recursively find and update combobox values"""
        try:
            if isinstance(widget, ttk.Combobox) and hasattr(widget, 'configure'):
                current_values = widget['values']
                if current_values and any('gemini' in str(val).lower() for val in current_values):
                    widget.configure(values=models)
            
            # Recursively check children
            for child in widget.winfo_children():
                self._update_combobox_values(child, models)
        except Exception as e:
            print(f"Error updating combobox: {e}")
    
    def save_settings(self):
        """Save all settings and apply changes with real-time synchronization"""
        try:
            # Prepare settings updates for batch save
            settings_updates = {
                'api_key': self.api_key_var.get().strip(),
                'model': self.model_var.get(),
                'theme_mode': self.theme_var.get(),
                'speech_enabled': self.speech_enabled_var.get(),
                'speech_muted': self.speech_muted_var.get(),
                'screenshot_size': self.screenshot_size_var.get(),
                'screenshot_wait_duration': self.screenshot_wait_var.get(),
                'notification_enabled': self.notification_enabled_var.get(),
                'font_size': self.font_size_var.get(),
                'window_opacity': self.window_opacity_var.get()
            }
            
            # Add voice settings if available
            if self.voice_manager.is_voice_available():
                settings_updates.update({
                    'voice_rate': self.voice_rate_var.get(),
                    'voice_volume': self.voice_volume_var.get()
                })
                
                # Set voice if selected
                if hasattr(self, 'voice_mapping') and self.voice_selection_var.get():
                    selected_voice_name = self.voice_selection_var.get()
                    if selected_voice_name in self.voice_mapping:
                        voice_id = self.voice_mapping[selected_voice_name]
                        settings_updates['selected_voice_id'] = voice_id
            
            # Use configuration manager for batch update
            success = self.app.config_manager.save_settings(settings_updates)
            
            if success:
                # Update app instance variables (these will be updated by observer too)
                self.app.current_api_key = settings_updates['api_key']
                self.app.current_model = settings_updates['model']
                self.app.theme_mode = settings_updates['theme_mode']
                self.app.speech_enabled = settings_updates['speech_enabled']
                self.app.speech_muted = settings_updates['speech_muted']
                self.app.screenshot_size = settings_updates['screenshot_size']
                self.app.screenshot_wait_duration = settings_updates['screenshot_wait_duration']
                self.app.notification_enabled = settings_updates['notification_enabled']
                self.app.font_size = settings_updates['font_size']
                self.app.window_opacity = settings_updates['window_opacity']
                
                # Apply voice settings if available
                if self.voice_manager.is_voice_available():
                    self.voice_manager.toggle_speech_enabled(self.app.speech_enabled)
                    self.voice_manager.toggle_speech_muted(self.app.speech_muted)
                    
                    # Update voice settings
                    self.voice_manager.set_voice_settings(
                        rate=settings_updates.get('voice_rate', 200),
                        volume=settings_updates.get('voice_volume', 0.8)
                    )
                    
                    # Set voice if selected
                    if 'selected_voice_id' in settings_updates:
                        self.voice_manager.set_voice(settings_updates['selected_voice_id'])
                
                # Apply window opacity immediately
                self.app.root.attributes('-alpha', self.app.window_opacity)
                
                # Update app displays
                self.app.update_status()
                self.app.update_model_display()
                
                # Reinitialize agent if needed
                if self.app.current_api_key:
                    self.app.initialize_agent()
                    
                print("Settings saved and synchronized successfully")
            else:
                print("Warning: Settings save failed")
            
            # Close settings window
            self.on_close()
            
            # Show success message
            self.app.add_message("System", "Settings saved successfully!", 
                               get_theme().colors['secondary'])
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}", 
                               parent=self.settings_window)
    
    def on_close(self):
        """Handle settings window close"""
        if self.settings_window:
            self.settings_window.destroy()
            self.settings_window = None 
    
    def create_settings_management_buttons(self):
        """Create settings management buttons (backup, restore, export, import)"""
        try:
            # Create management frame at the bottom of the settings window
            mgmt_frame = MD3Frame(self.settings_window)
            mgmt_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
            
            # Title
            mgmt_title = ttk.Label(mgmt_frame, text="Settings Management", 
                                 style='MD3.Title.Medium.TLabel')
            mgmt_title.pack(anchor=tk.W, pady=(0, 10))
            
            # Button frame
            btn_frame = MD3Frame(mgmt_frame)
            btn_frame.pack(fill=tk.X)
            
            # Backup button
            backup_btn = MD3Button(btn_frame, text="Create Backup", style='secondary',
                                 command=self.create_settings_backup)
            backup_btn.pack(side=tk.LEFT, padx=(0, 10))
            create_md3_tooltip(backup_btn, "Create a backup of current settings")
            
            # Restore button
            restore_btn = MD3Button(btn_frame, text="Restore Backup", style='secondary',
                                  command=self.restore_settings_backup)
            restore_btn.pack(side=tk.LEFT, padx=(0, 10))
            create_md3_tooltip(restore_btn, "Restore settings from a backup")
            
            # Export button
            export_btn = MD3Button(btn_frame, text="Export Settings", style='secondary',
                                 command=self.export_settings)
            export_btn.pack(side=tk.LEFT, padx=(0, 10))
            create_md3_tooltip(export_btn, "Export settings to a file")
            
            # Import button
            import_btn = MD3Button(btn_frame, text="Import Settings", style='secondary',
                                 command=self.import_settings)
            import_btn.pack(side=tk.LEFT, padx=(0, 10))
            create_md3_tooltip(import_btn, "Import settings from a file")
            
            # Reset button
            reset_btn = MD3Button(btn_frame, text="Reset to Defaults", style='error',
                                command=self.reset_to_defaults)
            reset_btn.pack(side=tk.RIGHT)
            create_md3_tooltip(reset_btn, "Reset all settings to default values")
            
        except Exception as e:
            print(f"Error creating settings management buttons: {e}")
    
    def create_settings_backup(self):
        """Create a backup of current settings"""
        try:
            # Save current settings first
            self.save_settings()
            
            # Create backup using config manager
            success = self.app.config_manager._create_backup()
            
            if success:
                messagebox.showinfo("Backup Created", 
                                  "Settings backup created successfully!",
                                  parent=self.settings_window)
            else:
                messagebox.showerror("Backup Failed", 
                                   "Failed to create settings backup.",
                                   parent=self.settings_window)
                
        except Exception as e:
            print(f"Error creating backup: {e}")
            messagebox.showerror("Error", f"Failed to create backup: {str(e)}",
                               parent=self.settings_window)
    
    def restore_settings_backup(self):
        """Restore settings from a backup"""
        try:
            # Get list of available backups
            backup_dir = self.app.config_manager.BACKUP_DIR
            backup_files = []
            
            if os.path.exists(backup_dir):
                for filename in os.listdir(backup_dir):
                    if filename.startswith('config_backup_') and filename.endswith('.json'):
                        backup_files.append(filename)
            
            if not backup_files:
                messagebox.showinfo("No Backups", 
                                  "No backup files found.",
                                  parent=self.settings_window)
                return
            
            # Sort by date (newest first)
            backup_files.sort(reverse=True)
            
            # Create selection dialog
            backup_dialog = tk.Toplevel(self.settings_window)
            backup_dialog.title("Select Backup")
            backup_dialog.geometry("400x300")
            backup_dialog.transient(self.settings_window)
            backup_dialog.grab_set()
            
            # Center the dialog
            backup_dialog.geometry("+%d+%d" % (
                self.settings_window.winfo_rootx() + 50,
                self.settings_window.winfo_rooty() + 50
            ))
            
            # Apply theme
            self.app.md3_theme.apply_theme(backup_dialog)
            
            # Title
            title_label = ttk.Label(backup_dialog, text="Select Backup to Restore", 
                                  style='MD3.Title.Medium.TLabel')
            title_label.pack(pady=20)
            
            # Listbox frame
            list_frame = MD3Frame(backup_dialog)
            list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
            
            # Listbox with scrollbar
            scrollbar = ttk.Scrollbar(list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=listbox.yview)
            
            # Populate listbox
            for backup_file in backup_files:
                # Extract date from filename for display
                try:
                    date_part = backup_file.replace('config_backup_', '').replace('.json', '')
                    formatted_date = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]} {date_part[9:11]}:{date_part[11:13]}:{date_part[13:15]}"
                    display_text = f"{formatted_date} ({backup_file})"
                except:
                    display_text = backup_file
                
                listbox.insert(tk.END, display_text)
            
            # Button frame
            btn_frame = MD3Frame(backup_dialog)
            btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
            
            def restore_selected():
                selection = listbox.curselection()
                if not selection:
                    messagebox.showwarning("No Selection", "Please select a backup to restore.",
                                         parent=backup_dialog)
                    return
                
                selected_backup = backup_files[selection[0]]
                backup_path = os.path.join(backup_dir, selected_backup)
                
                # Confirm restore
                if messagebox.askyesno("Confirm Restore", 
                                     f"Are you sure you want to restore from {selected_backup}?\n\n"
                                     "This will overwrite your current settings.",
                                     parent=backup_dialog):
                    try:
                        # Restore from backup
                        import shutil
                        shutil.copy2(backup_path, self.app.config_manager.CONFIG_FILE)
                        
                        # Reload settings
                        self.app.load_settings()
                        self.load_current_settings()
                        
                        backup_dialog.destroy()
                        messagebox.showinfo("Restore Complete", 
                                          "Settings restored successfully!",
                                          parent=self.settings_window)
                        
                    except Exception as e:
                        messagebox.showerror("Restore Failed", 
                                           f"Failed to restore backup: {str(e)}",
                                           parent=backup_dialog)
            
            # Buttons
            restore_btn = MD3Button(btn_frame, text="Restore", style='primary',
                                  command=restore_selected)
            restore_btn.pack(side=tk.RIGHT, padx=(10, 0))
            
            cancel_btn = MD3Button(btn_frame, text="Cancel", style='secondary',
                                 command=backup_dialog.destroy)
            cancel_btn.pack(side=tk.RIGHT)
            
        except Exception as e:
            print(f"Error restoring backup: {e}")
            messagebox.showerror("Error", f"Failed to restore backup: {str(e)}",
                               parent=self.settings_window)
    
    def export_settings(self):
        """Export settings to a file"""
        try:
            from tkinter import filedialog
            
            # Get export path
            export_path = filedialog.asksaveasfilename(
                parent=self.settings_window,
                title="Export Settings",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if export_path:
                success = self.app.config_manager.export_config(export_path)
                
                if success:
                    messagebox.showinfo("Export Complete", 
                                      f"Settings exported successfully to:\n{export_path}",
                                      parent=self.settings_window)
                else:
                    messagebox.showerror("Export Failed", 
                                       "Failed to export settings.",
                                       parent=self.settings_window)
                    
        except Exception as e:
            print(f"Error exporting settings: {e}")
            messagebox.showerror("Error", f"Failed to export settings: {str(e)}",
                               parent=self.settings_window)
    
    def import_settings(self):
        """Import settings from a file"""
        try:
            from tkinter import filedialog
            
            # Get import path
            import_path = filedialog.askopenfilename(
                parent=self.settings_window,
                title="Import Settings",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if import_path:
                # Confirm import
                if messagebox.askyesno("Confirm Import", 
                                     f"Are you sure you want to import settings from:\n{import_path}\n\n"
                                     "This will overwrite your current settings.",
                                     parent=self.settings_window):
                    
                    success = self.app.config_manager.import_config(import_path)
                    
                    if success:
                        # Reload settings in UI
                        self.app.load_settings()
                        self.load_current_settings()
                        
                        messagebox.showinfo("Import Complete", 
                                          "Settings imported successfully!",
                                          parent=self.settings_window)
                    else:
                        messagebox.showerror("Import Failed", 
                                           "Failed to import settings. Please check the file format.",
                                           parent=self.settings_window)
                    
        except Exception as e:
            print(f"Error importing settings: {e}")
            messagebox.showerror("Error", f"Failed to import settings: {str(e)}",
                               parent=self.settings_window)
    
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        try:
            # Confirm reset
            if messagebox.askyesno("Confirm Reset", 
                                 "Are you sure you want to reset all settings to default values?\n\n"
                                 "This action cannot be undone.",
                                 parent=self.settings_window):
                
                success = self.app.config_manager.reset_to_defaults()
                
                if success:
                    # Reload settings in UI
                    self.app.load_settings()
                    self.load_current_settings()
                    
                    messagebox.showinfo("Reset Complete", 
                                      "Settings reset to defaults successfully!",
                                      parent=self.settings_window)
                else:
                    messagebox.showerror("Reset Failed", 
                                       "Failed to reset settings to defaults.",
                                       parent=self.settings_window)
                    
        except Exception as e:
            print(f"Error resetting settings: {e}")
            messagebox.showerror("Error", f"Failed to reset settings: {str(e)}",
                               parent=self.settings_window)
    
    def load_current_settings(self):
        """Load current settings into the UI controls"""
        try:
            # AI tab settings
            self.api_key_var.set(self.app.current_api_key)
            self.model_var.set(self.app.current_model)
            self.speech_enabled_var.set(self.app.speech_enabled)
            self.speech_muted_var.set(self.app.speech_muted)
            
            # UI tab settings
            self.theme_var.set(self.app.theme_mode)
            self.screenshot_size_var.set(self.app.screenshot_size)
            self.screenshot_wait_var.set(self.app.screenshot_wait_duration)
            self.notification_enabled_var.set(self.app.notification_enabled)
            self.font_size_var.set(self.app.font_size)
            self.window_opacity_var.set(self.app.window_opacity)
            
            # Voice settings if available
            if hasattr(self, 'voice_rate_var') and hasattr(self.app.voice_manager, 'voice_rate'):
                self.voice_rate_var.set(self.app.voice_manager.voice_rate)
            if hasattr(self, 'voice_volume_var') and hasattr(self.app.voice_manager, 'voice_volume'):
                self.voice_volume_var.set(self.app.voice_manager.voice_volume)
                
        except Exception as e:
            print(f"Error loading current settings: {e}")