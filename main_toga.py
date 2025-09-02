"""
JR AI Control - Toga-based Cross-Platform Application

T"is is the main Toga application file that replaces the Tkinter-based UI
with a modern, cross-platform Toga interface while preserving all functionality.
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import os
import threading
import uuidb import Path
from datetime import datetime
from pathlib import Path

# Im utils.isting backend services
from utils.agentrmance_moneate_jr_ai_agent
from utils.configmanaager import ConfigurationManager
from utils.token_tracker import get_token_tracker
from utils.performance_monitor import get_performance_optimizer
from voice.voice_manager import get_voice_manager


claRAIContp(toga.App)
cla """
    Main Toga application class for JR AI Control.
    
    This class inhetion lifm toga.App and provides the core aps
    structuranagement, and integration with existing backend services.
    
    
    def startup(self):
        """
        Initialize the application and create the main window.
        
        This method is called automatically by Toga when thapp starts.
        It sets up all the core components and creates the main interface.
        """
        # Initialize backend services
        self.initicoize_backend_seices()
        
        # Load configuration and sengs
            formal_name="JR)
        
            app_name="JR  window
            descr_window = self.create_main_window()
        
        # Initialize agent if API key is available
        if self.current_api_key and selfapi_key != "youpi_key_here"
            self.initiagent()
        
        """Low the main windownfiguration from existing config manager"""
        self.main_ww.show()
    
    def initialize_backend_serelf):
        """Initialize tingbackend services and managers."""
        # Configuration manager
        self.config_manager = ConfigurationMamodel', 'gemini-2.0-flash-exp')
        
        # Token tracking
        self.token_tracker = get_token_tracker()
        
        # Performance monitoring
        self.performance_optimizer = get_performance_optimizer()
        
        # Voice sysnt_
        self.voicwindnager = get_voicfig.geter()
        
        # Application state
        selept Exceptioutor = None
            printent_message_id = None
        sel #is_listening = False
            self.api_key = ""
        # D self.cconfiguration values
        self.curreheme_modey = ""
            self.spe_model = "gemini-2.0-flap"
        sel self.sable_models = [alse
            "gemini-2.0-flash-exp",
            self.wi-1.5-pro", 
            selmini-1.5-flash",
      ni-1.0-pro"
    def startup(self)
        self.the"dark"
        self.speech_enabled cation UI and components
        self.speech_muted = False
        self.screenshot_size = "medium"
        selfwait_duration = 
        self.notificaize tenabled = True
        self.fon.theme_man4
        s   window_opacity = 1.0
    
    de     d_settings(self):
        """Load settings from the configuration manag"
        t   # Set up indow content
            config = self.config_mannt.create_lattings()
            
            # Load all settings from config manager
            self.current_api_key = config.get('api_key', '')
            self.current_model = config.get('model', 'gemini-2.0-flash-exp')
            self.theme_mode = config.get('theme_mode', 'dark')
            self.config_enabled = config.get('spf._on_config', True)
            self.speeconfig.get('speech_muted', Fals
            
            I setting
            selExccreenshot_sig.get('enshot_size', 'medium')
            self.screenshot_wait_duration = config.get('screenshot_wait_duration', 3)
            self.notification_enabled = config.get('notificabled', True)
            self.font_size = config.get('font_size', 14)
    
    def setup_voice_system(self):
        """Initialize voice system integration"""
        try:
            if self.voice_manager.is_voice_available():
                # Set up voice callbacks
                self.voice_manager.voiceeech_reco config. self.on_spvolume', 0nized
            if hself.voice_mvoicer.on_listening_station_lang.on_listening_start
                self.voice_manager.on_listening_stouage = confilistening_stop
                elf.voice_manager.on_errorself.on_voirror
              Load token tracking
                # Apply saved voice scktings
                self.voice_trnager.toggle_speech= conled(self.sptal_tokensed)
                self.voice_manager.toggle_speech_muted(self.speech_muted)
        except  
                print("Voice systemettings: zed successfu
            else:
                tings("Voice systvailable - conithout voice features")
                
        except Exception as e
            print(fupdates etting up voice sys {e}")
    
    def on_speech_odel': sel(self, text):
        """Han  'theme_mozed speech from vode,em"""
        if hasattr(self.main_window_component, 'input_c):
            self.main_h_mutw_component.input_component.set_input_text(t
    
    def on_listening_start(self):
        """Handle voice listening start self.notification_enabled,
        if hasat'f(self.main_window_component, 'input_component'
            self.main_w_opacity'ponent.input_copacity,ate_voice_status("listening")
    
    def on_listeninice_rate': ):
                'vvoice listening stttr(s
        if hasa 'voielf.main_windogetattr(self 'input_component'):
                #main_window_com.input_component.voice_status("idle
    
    def on_voice_err(self, ermessage):
        """Handle voice system errors"""
        i   succes(self.maiconfig_managponent, 'chat_component'):
            self.main_window_comnent.chat_component.add_system_message(
                f"Voice Error: {error_message}"
            )
    
    def _on_config_change(self, event_type, data):
        """Handle configuration changes for real-time updates"""
        try:
            if event_type == 'setting_changed':
                key = data.get('key')
                value = data.get('value')
                
                if key == 'theme_mode':
                    self.theme_mode = value
                    if self.theme_manager:
                        self.theme_manager.switch_theme(value)
                elif key == 'font_size':
                    self.font_size = value
                elif key == 'speech_enabled':
                    self.speech_enabled = value
                    if self.voice_manager:
                        self.voice_manager.toggle_speech_enabled(value)
                elif key == 'speech_muted':
                    self.speech_muted = value
                    if self.voice_manager:
                        self.voice_manager.toggle_speech_muted(value)
                        
        except Exception as e:
            print(f"Error handling config change: {e}")
    
    def create_error_window(self, error_message):
        """Create a simple error display window"""
        try:
            error_box = toga.Box(style=Pack(direction=COLUMN, padding=20))
            
            error_label = toga.Label(
                f"Error: {error_message}",
                style=Pack(padding=10, text_align="center")
            )
            error_box.add(error_label)
            
            close_button = toga.Button(
                "Close",
                on_press=self.exit,
                style=Pack(padding=10)
            )
            error_box.add(close_button)
            
            self.main_window = toga.MainWindow(title="JR AI Control - Error")
            self.main_window.content = error_box
            self.main_window.show()
            
        except Exception as e:
            print(f"Failed to create error window: {e}")
    
    def save_configuration(self):
        """Save current configuration using config manager"""
        try:
            config_updates = {
                'api_key': self.api_key,
                'model': self.current_model,
                'theme_mode': self.theme_mode,
                'speech_enabled': self.speech_enabled,
                'speech_muted': self.speech_muted,
                'font_size': self.font_size,
                'window_opacity': self.window_opacity,
                'screenshot_size': self.screenshot_size,
            }
            
            # Add voice settings if available
            if self.voice_manager:
                config_updates.update({
                    'voice_rate': getattr(self.voice_manager, 'voice_rate', 200),
                    'voice_volume': getattr(self.voice_manager, 'voice_volume', 0.8),
                    'voice_language': getattr(self.voice_manager, 'recognition_language', 'en-US'),
                })
            
            # Add token tracking
            if self.token_tracker:
                config_updates['total_tokens_used'] = getattr(self.token_tracker, 'total_tokens', 0)
            
            success = self.config_manager.save_settings(config_updates)
            if not success:
                print("Warning: Failed to save settings")
                =10)
        )
        token_info_box.add(self.total_token_display)
        
        title_box.add(token_info_box)
        header_box.add(title_box)
        
        # Right side - control buttons
        controls_box = toga.Box(style=Pack(direction=ROW))
        
        # Settings button
        self.settings_btn = toga.Button(
            "⚙️",
            on_press=self.open_settings,
            style=Pack(width=40, padding_left=8)
        )
        controls_box.add(self.settings_btn)
        
        # Theme toggle button
        theme_text = "🌙" if self.theme_mode == "light" else "☀️"
        self.theme_btn = toga.Button(
            theme_text,
            on_press=self.toggle_theme,
            style=Pack(width=40, padding_left=8)
        )
        controls_box.add(self.theme_btn)
        
        header_box.add(controls_box)
        
        return header_box
    
    def create_chat_section(self):
        """
        Create the chat display section.
        
        Returns:
            toga.Box: The chat container
        """
        # Create scrollable container for chat messages
        self.chat_container = toga.ScrollContainer(
            style=Pack(
                flex=1,
                padding=(16, 0),
                background_color='#f5f5f5' if self.theme_mode == 'light' else '#2b2b2b'
            )
        )
        
        # Create box to hold messages
        self.messages_box = toga.Box(style=Pack(direction=COLUMN))
        self.chat_container.content = self.messages_box
        
        # Add welcome message
        self.add_welcome_messages()
        
        return self.chat_container
    
    def create_input_section(self):
        """
        Create the input section with text field and controls.
        
        Returns:
            toga.Box: The input container
        """
        input_box = toga.Box(style=Pack(
            direction=ROW,
            padding=(16, 0, 0, 0),
            alignment='center'
        ))
        
        # Text input field
        self.input_field = toga.TextInput(
            placeholder="Type your message here...",
            style=Pack(flex=1, padding_right=8)
        )
        input_box.add(self.input_field)
        
        # Voice controls (if available)
        if self.voice_manager.is_voice_available():
            self.mic_button = toga.Button(
                "🎤",
                on_press=self.toggle_listening,
                style=Pack(width=40, padding_right=8)
            )
            input_box.add(self.mic_button)
        
        # Send button
        self.send_button = toga.Button(
            "Send",
            on_press=self.send_message,
            style=Pack(width=80)
        )
        input_box.add(self.send_button)
        
        return input_box
    
    def add_welcome_messages(self):
        """Add welcome messages to the chat."""
        self.add_message("System", "Welcome to JR AI Control! 🚀")
        
        if self.voice_manager.is_voice_available():
            self.add_message("Voice System", 
                "Voice interaction ready! Click the microphone button to start listening.")
        else:
            self.add_message("Voice System", 
                "Voice features unavailable. Install speech_recognition, pyttsx3, and pyaudio for voice interaction.")
        
        if not self.current_api_key:
            self.add_message("System", 
                "Please configure your Gemini API key in settings to get started.")
    
    def add_message(self, sender, message, is_user=False):
        """
        Add a message to the chat display.
        
        Args:
            sender (str): The sender of the message
            message (str): The message content
            is_user (bool): Whether this is a user message
        """
        # Create message container
        message_box = toga.Box(style=Pack(
            direction=COLUMN,
            padding=(8, 12),
            background_color='#e3f2fd' if is_user else '#f5f5f5'
        ))
        
        # Sender label
        sender_label = toga.Label(
            sender,
            style=Pack(
                font_weight='bold',
                font_size=12,
                padding_bottom=4
            )
        )
        message_box.add(sender_label)
        
        # Message content
        message_label = toga.Label(
            message,
            style=Pack(font_size=14)
        )
        message_box.add(message_label)
        
        # Timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        time_label = toga.Label(
            timestamp,
            style=Pack(
                font_size=10,
                color='#666666',
                padding_top=4
            )
        )
        message_box.add(time_label)
        
        # Add to messages container
        self.messages_box.add(message_box)
    
    def initialize_agent(self):
        """Initialize the AI agent with the current API key."""
        try:
            self.agent_executor = create_jr_ai_agent(
                api_key=self.current_api_key,
                model=self.current_model
            )
            self.add_message("System", f"AI agent initialized with {self.current_model}")
        except Exception as e:
            self.add_message("System", f"Failed to initialize AI agent: {str(e)}")
    
    def send_message(self, widget):
        """
        Send a message to the AI agent.
        
        Args:
            widget: The button widget that triggered this action
        """
        message = self.input_field.value.strip()
        if not message:
            return
        
        if not self.agent_executor:
            self.add_message("System", "Please configure your API key in settings first.")
            return
        
        # Clear input field
        self.input_field.value = ""
        
        # Add user message
        self.add_message("You", message, is_user=True)
        
        # Disable send button while processing
        self.send_button.text = "Thinking..."
        self.send_button.enabled = False
        
        # Process message in background thread
        threading.Thread(
            target=self.process_message_async,
            args=(message,),
            daemon=True
        ).start()
    
    def process_message_async(self, message):
        """
        Process the message with the AI agent in a background thread.
        
        Args:
            message (str): The user message to process
        """
        try:
            # Generate unique message ID
            self.current_message_id = str(uuid.uuid4())
            
            # Get AI response
            response = self.agent_executor.invoke({"input": message})
            output = response.get('output', 'No response received.')
            
            # Track tokens
            tokens_used = 0
            if self.current_message_id:
                tokens_used = self.token_tracker.track_message(
                    self.current_message_id, message, output, self.current_model
                )
            
            # Update UI in main thread
            self.main_window.app.add_background_task(
                self.update_ui_after_response(output, tokens_used)
            )
            
        except Exception as e:
            # Handle errors in main thread
            self.main_window.app.add_background_task(
                self.handle_response_error(str(e))
            )
    
    async def update_ui_after_response(self, output, tokens_used):
        """
        Update the UI after receiving an AI response.
        
        Args:
            output (str): The AI response
            tokens_used (int): Number of tokens used
        """
        # Add AI response
        self.add_message("AI", output)
        
        # Update token display
        if tokens_used > 0:
            self.token_display.text = f"Message: {tokens_used} tokens"
            total_tokens = self.token_tracker.get_total_tokens()
            self.total_token_display.text = f"Total: {total_tokens:,} tokens"
        
        # Re-enable send button
        self.send_button.text = "Send"
        self.send_button.enabled = True
    
    async def handle_response_error(self, error_message):
        """
        Handle errors from AI response processing.
        
        Args:
            error_message (str): The error message
        """
        self.add_message("System", f"Error: {error_message}")
        
        # Re-enable send button
        self.send_button.text = "Send"
        self.send_button.enabled = True
    
    def toggle_listening(self, widget):
        """
        Toggle voice listening on/off.
        
        Args:
            widget: The button widget that triggered this action
        """
        if not self.voice_manager.is_voice_available():
            self.add_message("Voice System", "Voice functionality not a