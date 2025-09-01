import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import threading
import time
from datetime import datetime
import argparse
import uuid

# Import our utilities
from utils.agent import create_jr_ai_agent
from utils.prompt import prompt
from utils.contants import *
from utils.config_manager import ConfigurationManager
from utils.token_tracker import get_token_tracker, track_message_tokens
from utils.performance_monitor import get_performance_optimizer, start_performance_monitoring
from utils.performance_optimizer import get_performance_manager, start_performance_optimization, register_component_for_optimization
from ui.material_design import apply_md3_theme, get_theme, create_md3_widget_config, switch_theme, register_global_theme_callback, create_smooth_theme_switcher
from ui.enhanced_components import MD3ScrolledText, MD3Button, MD3Entry, MD3Frame, MD3StatusIndicator, MD3Card, create_md3_tooltip, animate_widget_transition
from ui.chat_interface import ChatInterface
from ui.settings_tabs import SettingsTabManager
from voice.voice_manager import get_voice_manager, is_voice_available

import pyautogui as pg
pg.PAUSE = 2

class JRAIControlApp:
    def __init__(self):
        self.root = tk.Tk()
        self.agent_executor = None
        
        # Initialize configuration manager
        self.config_manager = ConfigurationManager()
        
        # Configuration variables (will be loaded from config manager)
        self.current_api_key = ""
        self.current_model = "gemini-2.0-flash-exp"
        self.available_models = [
            "gemini-2.0-flash-exp",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro"
        ]
        
        # Initialize theme and token tracking
        self.theme_mode = "dark"
        self.token_tracker = get_token_tracker()
        self.md3_theme = None
        
        # Initialize performance monitoring and optimization
        self.performance_optimizer = get_performance_optimizer()
        self.performance_manager = get_performance_manager()
        self.performance_monitoring_enabled = True
        
        # Voice system initialization
        self.voice_manager = get_voice_manager()
        self.speech_enabled = True
        self.speech_muted = False
        self.is_listening = False
        
        # UI components
        self.model_label = None
        self.token_display = None
        self.total_token_display = None
        self.mic_button = None
        self.voice_status_indicator = None
        
        # Message tracking
        self.current_message_id = None
        
        # Additional UI settings with defaults
        self.screenshot_size = "medium"
        self.screenshot_wait_duration = 3
        self.notification_enabled = True
        self.font_size = 14
        self.window_opacity = 1.0
        
        # Settings tab manager
        self.settings_tab_manager = None
        
        # Setup configuration change observer
        self.config_manager.add_observer(self._on_config_change)
        
        # Load saved settings
        self.load_settings()
        
        # Setup the main window and theme
        self.setup_main_window()
        
        # Initialize voice system callbacks
        self.setup_voice_callbacks()
        
        # Create the UI
        self.create_ui()
        
        # Initialize agent if API key is available and valid
        if self.current_api_key and self.current_api_key != "your_api_key_here":
            self.initialize_agent()
        
        # Start performance monitoring and optimization
        if self.performance_monitoring_enabled:
            self.start_performance_monitoring()
            
        # Register components for optimization
        register_component_for_optimization(self.chat_display)
        register_component_for_optimization(self.voice_manager)
        if hasattr(self.chat_display, 'screenshot_manager'):
            register_component_for_optimization(self.chat_display.screenshot_manager)
    
    def load_settings(self):
        """Load settings from config manager"""
        try:
            config = self.config_manager.load_settings()
            
            # Load all settings from config manager
            self.current_api_key = config.get('api_key', '')
            self.current_model = config.get('model', 'gemini-2.0-flash-exp')
            self.theme_mode = config.get('theme_mode', 'dark')
            self.speech_enabled = config.get('speech_enabled', True)
            self.speech_muted = config.get('speech_muted', False)
            
            # Load UI settings
            self.screenshot_size = config.get('screenshot_size', 'medium')
            self.screenshot_wait_duration = config.get('screenshot_wait_duration', 3)
            self.notification_enabled = config.get('notification_enabled', True)
            self.font_size = config.get('font_size', 14)
            self.window_opacity = config.get('window_opacity', 1.0)
            
            # Load voice settings
            if hasattr(self.voice_manager, 'voice_rate'):
                self.voice_manager.voice_rate = config.get('voice_rate', 200)
            if hasattr(self.voice_manager, 'voice_volume'):
                self.voice_manager.voice_volume = config.get('voice_volume', 0.8)
            if hasattr(self.voice_manager, 'recognition_language'):
                self.voice_manager.recognition_language = config.get('voice_language', 'en-US')
                
            # Load token tracking
            if hasattr(self.token_tracker, 'total_tokens'):
                self.token_tracker.total_tokens = config.get('total_tokens_used', 0)
                
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings using config manager"""
        try:
            config_updates = {
                'api_key': self.current_api_key,
                'model': self.current_model,
                'theme_mode': self.theme_mode,
                'speech_enabled': self.speech_enabled,
                'speech_muted': self.speech_muted,
                'screenshot_size': self.screenshot_size,
                'screenshot_wait_duration': self.screenshot_wait_duration,
                'notification_enabled': self.notification_enabled,
                'font_size': self.font_size,
                'window_opacity': self.window_opacity,
                # Voice settings
                'voice_rate': getattr(self.voice_manager, 'voice_rate', 200),
                'voice_volume': getattr(self.voice_manager, 'voice_volume', 0.8),
                'voice_language': getattr(self.voice_manager, 'recognition_language', 'en-US'),
                # Token tracking
                'total_tokens_used': getattr(self.token_tracker, 'total_tokens', 0)
            }
            
            success = self.config_manager.save_settings(config_updates)
            if not success:
                print("Warning: Failed to save settings")
                
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def _on_config_change(self, event_type, data):
        """Handle configuration changes for real-time updates"""
        try:
            if event_type == 'setting_changed':
                key = data.get('key')
                value = data.get('value')
                
                # Update UI elements based on changed setting
                if key == 'theme_mode' and hasattr(self, 'md3_theme'):
                    self.theme_mode = value
                    self.md3_theme.switch_theme(value)
                elif key == 'font_size' and hasattr(self, 'chat_interface'):
                    self.font_size = value
                    # Update font size in UI components
                elif key == 'window_opacity':
                    self.window_opacity = value
                    self.root.attributes('-alpha', value)
                elif key == 'speech_enabled':
                    self.speech_enabled = value
                    self.update_mic_button_state()
                elif key == 'speech_muted':
                    self.speech_muted = value
                    self.update_mic_button_state()
                    
        except Exception as e:
            print(f"Error handling config change: {e}")
    
    def get_setting(self, key, default=None):
        """Get a setting value from config manager"""
        return self.config_manager.get_setting(key, default)
    
    def set_setting(self, key, value, save_immediately=True):
        """Set a setting value using config manager"""
        return self.config_manager.set_setting(key, value, save_immediately)
    
    def setup_main_window(self):
        """Setup the main application window"""
        self.root.title("JR AI Control")
        
        # Apply Material Design 3 theme
        self.md3_theme = apply_md3_theme(self.root, self.theme_mode)
        
        # Set window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.35)
        window_height = screen_height - 100
        
        x = screen_width - window_width - 20
        y = 50
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(True, True)
        
        # Apply window opacity
        self.root.attributes('-alpha', self.window_opacity)
        
        # Configure additional styles
        self.setup_styles()
    
    def setup_voice_callbacks(self):
        """Setup voice system callbacks"""
        if self.voice_manager.is_voice_available():
            # Set up speech recognition callback
            self.voice_manager.on_speech_recognized = self.on_speech_recognized
            
            # Set up listening status callbacks
            self.voice_manager.on_listening_start = self.on_listening_start
            self.voice_manager.on_listening_stop = self.on_listening_stop
            
            # Set up error callback
            self.voice_manager.on_error = self.on_voice_error
            
            # Apply saved voice settings
            self.voice_manager.toggle_speech_enabled(self.speech_enabled)
            self.voice_manager.toggle_speech_muted(self.speech_muted)
    
    def on_speech_recognized(self, text):
        """Handle recognized speech"""
        # Update UI in main thread
        self.root.after(0, lambda: self.input_entry.delete(0, tk.END))
        self.root.after(0, lambda: self.input_entry.insert(0, text))
        # Automatically send the message
        self.root.after(100, self.send_message)
    
    def on_listening_start(self):
        """Handle listening start"""
        self.is_listening = True
        if self.mic_button:
            self.root.after(0, lambda: self.update_mic_button_state())
        if self.voice_status_indicator:
            self.root.after(0, lambda: self.voice_status_indicator.set_status('listening'))
    
    def on_listening_stop(self):
        """Handle listening stop"""
        self.is_listening = False
        if self.mic_button:
            self.root.after(0, lambda: self.update_mic_button_state())
        if self.voice_status_indicator:
            self.root.after(0, lambda: self.voice_status_indicator.set_status('idle'))
    
    def on_voice_error(self, error_message):
        """Handle voice system errors"""
        self.root.after(0, lambda: self.add_message("Voice System", 
                                                   f"Error: {error_message}", 
                                                   get_theme().colors['error']))
    
    def setup_styles(self):
        """Setup custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       background='#2b2b2b', 
                       foreground='#ffffff', 
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure('Modern.TButton',
                       background='#4a9eff',
                       foreground='white',
                       font=('Segoe UI', 10),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Modern.TButton',
                 background=[('active', '#3d8bdb'),
                           ('pressed', '#2e6ba8')])
        
        style.configure('Settings.TButton',
                       background='#6c757d',
                       foreground='white',
                       font=('Segoe UI', 10),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Settings.TButton',
                 background=[('active', '#5a6268'),
                           ('pressed', '#495057')])
    
    def create_ui(self):
        """Create the main user interface with Material Design 3 styling"""
        # Main container with MD3 styling and proper spacing
        main_frame = MD3Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
        
        # Header card with elevation
        header_card = MD3Card(main_frame)
        header_card.pack(fill=tk.X, pady=(0, 16))
        
        # Header content with proper spacing
        header_content = MD3Frame(header_card)
        header_content.pack(fill=tk.X, padx=16, pady=12)
        
        # Title section with visual hierarchy
        title_section = MD3Frame(header_content)
        title_section.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Main title with MD3 typography
        title_label = ttk.Label(title_section, text="JR AI Control", style='MD3.Headline.Medium.TLabel')
        title_label.pack(anchor=tk.W)
        
        # Model name display with proper spacing
        self.model_label = ttk.Label(title_section, text=f"Model: {self.current_model}", 
                                   style='MD3.Body.Medium.TLabel')
        self.model_label.pack(anchor=tk.W, pady=(4, 0))
        
        # Token usage display with improved layout
        token_frame = MD3Frame(title_section)
        token_frame.pack(anchor=tk.W, pady=(8, 0))
        
        self.token_display = ttk.Label(token_frame, text="Message: 0 tokens", 
                                     style='MD3.Body.Small.TLabel')
        self.token_display.pack(side=tk.LEFT)
        
        # Separator with MD3 styling
        separator = ttk.Label(token_frame, text=" • ", style='MD3.Body.Small.TLabel')
        separator.pack(side=tk.LEFT)
        
        total_tokens = self.token_tracker.get_total_tokens()
        self.total_token_display = ttk.Label(token_frame, text=f"Total: {total_tokens:,} tokens", 
                                           style='MD3.Body.Small.TLabel')
        self.total_token_display.pack(side=tk.LEFT)
        
        # Control buttons section
        controls_frame = MD3Frame(header_content)
        controls_frame.pack(side=tk.RIGHT)
        
        # Theme toggle button
        self.theme_btn = create_smooth_theme_switcher(controls_frame, self.theme_mode)
        self.theme_btn.pack(side=tk.RIGHT, padx=(0, 8))
        create_md3_tooltip(self.theme_btn, "Toggle dark/light theme")
        
        # Settings button with MD3 styling
        settings_btn = MD3Button(controls_frame, text="⚙️", style='secondary', width=3,
                               command=self.open_settings)
        settings_btn.pack(side=tk.RIGHT, padx=(0, 8))
        create_md3_tooltip(settings_btn, "Open settings")
        
        # Status indicator with MD3 component
        status = 'active' if self.current_api_key else 'inactive'
        self.status_indicator = MD3StatusIndicator(controls_frame, status=status)
        self.status_indicator.pack(side=tk.RIGHT, padx=(0, 8))
        
        # Chat display area with elevation and proper spacing
        chat_card = MD3Card(main_frame)
        chat_card.pack(fill=tk.BOTH, expand=True, pady=(0, 16))
        
        # Chat content with padding
        chat_content = MD3Frame(chat_card)
        chat_content.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)
        
        # Create enhanced chat interface with thumbnail support
        self.chat_display = ChatInterface(chat_content)
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Set up chat interface callbacks
        self.chat_display.set_resend_callback(self.resend_message)
        self.chat_display.set_delete_callback(self.delete_message)
        
        # Input area with elevation
        input_card = MD3Card(main_frame)
        input_card.pack(fill=tk.X)
        
        # Input content with proper spacing
        input_content = MD3Frame(input_card)
        input_content.pack(fill=tk.X, padx=16, pady=12)
        
        # Input entry with MD3 styling and focus effects
        self.input_entry = MD3Entry(input_content, font=get_theme().typography['body_large'])
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 12))
        self.input_entry.bind('<Return>', self.send_message)
        create_md3_tooltip(self.input_entry, "Type your message and press Enter")
        
        # Voice controls frame
        voice_frame = MD3Frame(input_content)
        voice_frame.pack(side=tk.RIGHT, padx=(0, 12))
        
        # Microphone button with visual feedback
        if self.voice_manager.is_voice_available():
            self.mic_button = MD3Button(voice_frame, text="🎤", style='secondary', width=3,
                                      command=self.toggle_listening)
            self.mic_button.pack(side=tk.LEFT, padx=(0, 8))
            create_md3_tooltip(self.mic_button, "Toggle voice input (Ctrl+M)\nCtrl+Shift+S: Toggle speech\nCtrl+Shift+M: Toggle mute")
            
            # Voice status indicator
            self.voice_status_indicator = MD3StatusIndicator(voice_frame, status='idle')
            self.voice_status_indicator.pack(side=tk.LEFT, padx=(0, 8))
            create_md3_tooltip(self.voice_status_indicator, "Voice system status")
        
        # Send button with primary styling
        self.send_btn = MD3Button(input_content, text="Send", style='primary',
                                command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT)
        create_md3_tooltip(self.send_btn, "Send message (Enter)")
        
        # Register theme change callback for dynamic updates
        register_global_theme_callback(self._on_theme_change)
        
        # Setup keyboard shortcuts
        self.setup_keyboard_shortcuts()
        
        # Add welcome messages with smooth animation
        self.root.after(100, self._add_welcome_messages)
    
    def _on_theme_change(self, old_mode, new_mode, colors):
        """Handle theme change events"""
        self.theme_mode = new_mode
        
        # Update status indicator
        if hasattr(self, 'status_indicator'):
            status = 'active' if self.current_api_key else 'inactive'
            self.status_indicator.set_status(status)
        
        # Save theme preference
        self.save_settings()
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for voice controls"""
        # Ctrl+M for microphone toggle
        self.root.bind('<Control-m>', lambda e: self.toggle_listening())
        self.root.bind('<Control-M>', lambda e: self.toggle_listening())
        
        # Ctrl+Shift+S for speech toggle
        self.root.bind('<Control-Shift-S>', lambda e: self.toggle_speech_enabled())
        self.root.bind('<Control-Shift-s>', lambda e: self.toggle_speech_enabled())
        
        # Ctrl+Shift+M for speech mute toggle
        self.root.bind('<Control-Shift-M>', lambda e: self.toggle_speech_muted())
        self.root.bind('<Control-Shift-m>', lambda e: self.toggle_speech_muted())
    
    def toggle_listening(self):
        """Toggle voice listening on/off"""
        if not self.voice_manager.is_voice_available():
            self.add_message("Voice System", "Voice functionality not available. Please install required packages.", 
                           get_theme().colors['error'])
            return
        
        if self.is_listening:
            self.voice_manager.stop_listening()
        else:
            success = self.voice_manager.start_listening()
            if not success:
                self.add_message("Voice System", "Failed to start voice recognition.", 
                               get_theme().colors['error'])
    
    def toggle_speech_enabled(self):
        """Toggle speech output on/off"""
        if not self.voice_manager.is_voice_available():
            return
        
        self.speech_enabled = not self.speech_enabled
        self.voice_manager.toggle_speech_enabled(self.speech_enabled)
        
        status = "enabled" if self.speech_enabled else "disabled"
        self.add_message("Voice System", f"Speech output {status}", 
                        get_theme().colors['secondary'])
        
        # Save settings
        self.save_settings()
    
    def toggle_speech_muted(self):
        """Toggle speech mute on/off"""
        if not self.voice_manager.is_voice_available():
            return
        
        self.speech_muted = not self.speech_muted
        self.voice_manager.toggle_speech_muted(self.speech_muted)
        
        status = "muted" if self.speech_muted else "unmuted"
        self.add_message("Voice System", f"Speech output {status}", 
                        get_theme().colors['secondary'])
        
        # Save settings
        self.save_settings()
    
    def update_mic_button_state(self):
        """Update microphone button appearance based on listening state"""
        if not self.mic_button:
            return
        
        if self.is_listening:
            self.mic_button.configure(text="🔴")  # Red dot for recording
            # Apply listening state styling
            theme = get_theme()
            animate_widget_transition(self.mic_button, 'bg', 
                                    theme.colors['secondary'], 
                                    theme.colors['error'], 200)
        else:
            self.mic_button.configure(text="🎤")  # Microphone icon
            # Apply idle state styling
            theme = get_theme()
            animate_widget_transition(self.mic_button, 'bg', 
                                    theme.colors['error'], 
                                    theme.colors['secondary'], 200)
    
    def _add_welcome_messages(self):
        """Add welcome messages with animation"""
        self.add_message("System", "Welcome to JR AI Control! 🚀", get_theme().colors['primary'])
        
        # Voice system status message
        if self.voice_manager.is_voice_available():
            self.root.after(300, lambda: self.add_message("Voice System", 
                "Voice interaction ready! Use Ctrl+M to toggle microphone, Ctrl+Shift+S to toggle speech.", 
                get_theme().colors['secondary']))
        else:
            self.root.after(300, lambda: self.add_message("Voice System", 
                "Voice features unavailable. Install speech_recognition, pyttsx3, and pyaudio for voice interaction.", 
                get_theme().colors['tertiary']))
        
        if not self.current_api_key:
            self.root.after(600, lambda: self.add_message("System", 
                "Please configure your Gemini API key in settings to get started.", 
                get_theme().colors['tertiary']))
    
    def add_message(self, sender, message, color=None, screenshot_id=None, tokens=0):
        """Add a message to the chat display with thumbnail support"""
        is_user = sender == "You"
        
        # Add message to chat interface
        message_widget = self.chat_display.add_message(
            sender=sender,
            message=message,
            is_user=is_user,
            screenshot_id=screenshot_id,
            tokens=tokens
        )
        
        # Update token display if tokens were provided
        if tokens > 0:
            self.update_token_display(tokens)
        
        return message_widget
    
    def resend_message(self, message_text):
        """Callback for resending a message"""
        # Set the message in the input field and send it
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, message_text)
        self.send_message()
    
    def delete_message(self, message_widget):
        """Callback for deleting a message"""
        # Remove the message widget from the chat
        message_widget.pack_forget()
        message_widget.destroy()
        
        # Remove from messages list if it exists
        if hasattr(self.chat_display, 'messages') and message_widget in self.chat_display.messages:
            self.chat_display.messages.remove(message_widget)
    
    def send_message(self, event=None):
        """Send a message to the AI agent"""
        message = self.input_entry.get().strip()
        if not message:
            return
        
        if not self.agent_executor:
            self.add_message("System", "Please configure your API key in settings first.", get_theme().colors['error'])
            return
        
        # Generate unique message ID
        self.current_message_id = str(uuid.uuid4())
        
        # Clear input
        self.input_entry.delete(0, tk.END)
        
        # Add user message
        self.add_message("You", message, get_theme().colors['primary'])
        
        # Disable send button while processing with visual feedback
        self.send_btn.configure(text="Thinking...")
        self.send_btn.config(state='disabled')
        self.input_entry.config(state='disabled')
        
        # Add visual feedback with animation
        animate_widget_transition(self.send_btn, 'bg', 
                                get_theme().colors['primary'], 
                                get_theme().colors['outline'], 200)
        
        # Process message in separate thread
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
    
    def process_message(self, message):
        """Process the message with the AI agent with performance monitoring"""
        try:
            # Time the AI response processing
            with self.performance_optimizer.time_operation('response_times'):
                response = self.agent_executor.invoke({"input": message})
                output = response.get('output', 'No response received.')
            
            # Extract screenshot ID from intermediate steps if available
            screenshot_id = None
            intermediate_steps = response.get('intermediate_steps', [])
            
            for step in intermediate_steps:
                if len(step) >= 2:
                    action, observation = step
                    # Check if this was a get_screen_info tool call
                    if hasattr(action, 'tool') and action.tool == 'get_screen_info':
                        # The observation should be the tool result
                        if isinstance(observation, dict) and 'screenshot_id' in observation:
                            screenshot_id = observation['screenshot_id']
                            break
                        elif isinstance(observation, str):
                            # Try to parse if it's a string representation of dict
                            try:
                                import ast
                                parsed = ast.literal_eval(observation)
                                if isinstance(parsed, dict) and 'screenshot_id' in parsed:
                                    screenshot_id = parsed['screenshot_id']
                                    break
                            except:
                                pass
            
            # Track tokens for this message exchange
            tokens_used = 0
            if self.current_message_id:
                with self.performance_optimizer.time_operation('token_processing_times'):
                    tokens_used = self.token_tracker.track_message(
                        self.current_message_id, message, output, self.current_model
                    )
                
                # Update token displays in main thread
                self.root.after(0, lambda: self.update_token_displays(tokens_used))
            
            # Update UI in main thread with screenshot ID if available
            with self.performance_optimizer.time_operation('ui_render_times'):
                self.root.after(0, lambda: self.add_message("JR AI", output, 
                                                           get_theme().colors['secondary'], 
                                                           screenshot_id=screenshot_id,
                                                           tokens=tokens_used))
            
            # Speak the response if speech is enabled
            if self.speech_enabled and self.voice_manager.is_voice_available():
                with self.performance_optimizer.time_operation('voice_processing_times'):
                    self.voice_manager.speak_text(output)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.add_message("System", error_msg, get_theme().colors['error']))
        
        finally:
            # Re-enable controls
            self.root.after(0, self.enable_input)
    
    def enable_input(self):
        """Re-enable input controls with smooth animation"""
        self.send_btn.configure(text="Send")
        self.send_btn.config(state='normal')
        self.input_entry.config(state='normal')
        self.input_entry.focus()
        
        # Restore button color with animation
        animate_widget_transition(self.send_btn, 'bg', 
                                get_theme().colors['outline'], 
                                get_theme().colors['primary'], 200)
    
    def start_performance_monitoring(self):
        """Start comprehensive performance monitoring and optimization"""
        try:
            # Add performance optimization callbacks
            self.performance_optimizer.add_optimization_callback(self._on_performance_optimization)
            self.performance_manager.add_optimization_callback(self._on_system_optimization)
            
            # lf.performance_optimizer.start_monitoring()
            
            # Schedule periodic optimization checks
            self.schedule_performance_check()
            
            print("Performance monitoring started")
            
        except Exception as e:
            print(f"Error starting performance monitoring: {e}")
    
    def _on_performance_optimization(self, results):
        """Handle performance optimization results"""
        try:
            memory_freed = results.get('memory_optimization', {}).get('memory_freed_mb', 0)
            if memory_freed > 10:  # Only show notification for significant memory savings
                self.add_message("System", 
                               f"Performance optimization completed. {memory_freed:.1f}MB memory freed.", 
                               get_theme().colors['secondary'])
        except Exception as e:
            print(f"Error handling performance optimization: {e}")
    
    def schedule_performance_check(self):
        """Schedule periodic performance checks"""
        try:
            # Check if optimization is needed
            if hasattr(self.performance_optimizer, 'memory_manager'):
                if self.performance_optimizer.memory_manager.should_cleanup():
                    self.performance_optimizer.optimize_performance()
            
            # Schedule next check in 5 minutes
            self.root.after(300000, self.schedule_performance_check)  # 5 minutes = 300000ms
            
        except Exception as e:
            print(f"Error in performance check: {e}")
            # Reschedule anyway
            self.root.after(300000, self.schedule_performance_check)
    
    def update_token_display(self, message_tokens):
        """Update token display for a single message"""
        if self.token_display:
            self.token_display.config(text=f"Message: {message_tokens:,} tokens")
        
        # Also update total
        if self.total_token_display:
            total_tokens = self.token_tracker.get_total_tokens()
            self.total_token_display.config(text=f"Total: {total_tokens:,} tokens")
    
    def update_token_displays(self, message_tokens):
        """Update token display labels"""
        if self.token_display:
            self.token_display.config(text=f"Message: {message_tokens:,} tokens")
        
        if self.total_token_display:
            total_tokens = self.token_tracker.get_total_tokens()
            self.total_token_display.config(text=f"Total: {total_tokens:,} tokens")
    
    def update_model_display(self):
        """Update the model name display"""
        if self.model_label:
            self.model_label.config(text=f"Model: {self.current_model}")
    
    def open_settings(self):
        """Open the tabbed settings interface"""
        if not self.settings_tab_manager:
            self.settings_tab_manager = SettingsTabManager(self.root, self)
        
        self.settings_tab_manager.open_settings()    

    
    def update_status(self):
        """Update the connection status indicator"""
        if hasattr(self, 'status_indicator'):
            status = 'active' if self.current_api_key else 'inactive'
            self.status_indicator.set_status(status)
    
    def initialize_agent(self):
        """Initialize the AI agent with current settings"""
        if not self.current_api_key or self.current_api_key == "your_api_key_here":
            self.add_message("System", "Please set a valid API key in settings to use the agent", "#ffc107")
            self.agent_executor = None
            return
            
        try:
            # Update the global GEMINI model with current settings
            from langchain_google_genai import ChatGoogleGenerativeAI
            
            updated_model = ChatGoogleGenerativeAI(
                model=self.current_model,
                google_api_key=self.current_api_key
            )
            
            # Update the MODELS dictionary
            MODELS["gemini"] = updated_model
            
            # Create the agent
            self.agent_executor = create_jr_ai_agent(updated_model, prompt)
            
            self.add_message("System", f"Agent initialized with {self.current_model}", "#28a745")
            
        except Exception as e:
            self.add_message("System", f"Failed to initialize agent: {str(e)}", "#dc3545")
            self.agent_executor = None
    
    def run(self):
        """Start the application"""
        # Set window to stay on top initially
        self.root.attributes('-topmost', True)
        self.root.after(1000, lambda: self.root.attributes('-topmost', False))  # Remove after 1 second
        
        # Focus on input
        self.input_entry.focus()
        
        # Start the main loop
        self.root.mainloop()

def main():
    """Main function with command line argument support"""
    parser = argparse.ArgumentParser(description="Launch the JR AI Control application with Gemini AI model.")
    parser.add_argument('--float-ui', type=int, default=0, choices=[0, 1],
                        help="Enable or disable the float UI. Default is 0 (disabled).")
    
    args = parser.parse_args()
    
    # Create and run the application
    app = JRAIControlApp()
    
    if args.float_ui:
        app.root.attributes('-topmost', True)
    
    app.run()

if __name__ == "__main__":
    main()