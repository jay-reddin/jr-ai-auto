#!/usr/bin/env python3
"""
JR AI Control - Voice Demo Version
Shows the voice interaction features with Material Design 3 interface
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import os
import threading
import time
from datetime import datetime
import argparse
import uuid

# Import our utilities
from utils.token_tracker import get_token_tracker, track_message_tokens
from ui.material_design import apply_md3_theme, get_theme, create_md3_widget_config
from voice.voice_manager import get_voice_manager, is_voice_available

class JRAIControlVoiceDemo:
    def __init__(self):
        self.root = tk.Tk()
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
        
        # Voice system
        self.voice_manager = get_voice_manager()
        self.voice_enabled = is_voice_available()
        self.is_listening = False
        
        # UI components
        self.model_label = None
        self.token_display = None
        self.total_token_display = None
        self.voice_button = None
        self.voice_status_label = None
        
        # Message tracking
        self.current_message_id = None
        
        # Setup voice callbacks
        if self.voice_enabled:
            self.setup_voice_callbacks()
        
        # Load saved settings
        self.load_settings()
        
        # Setup the main window and theme
        self.setup_main_window()
        
        # Create the UI
        self.create_ui()
    
    def setup_voice_callbacks(self):
        """Setup voice manager callbacks"""
        self.voice_manager.on_speech_recognized = self.on_speech_recognized
        self.voice_manager.on_listening_start = self.on_listening_start
        self.voice_manager.on_listening_stop = self.on_listening_stop
        self.voice_manager.on_error = self.on_voice_error
    
    def on_speech_recognized(self, text):
        """Handle recognized speech"""
        self.root.after(0, lambda: self.process_voice_input(text))
    
    def on_listening_start(self):
        """Handle listening start"""
        self.root.after(0, self.update_voice_status_listening)
    
    def on_listening_stop(self):
        """Handle listening stop"""
        self.root.after(0, self.update_voice_status_idle)
    
    def on_voice_error(self, error):
        """Handle voice errors"""
        self.root.after(0, lambda: self.add_message("Voice System", f"Error: {error}", get_theme().colors['error']))
    
    def process_voice_input(self, text):
        """Process voice input as if it was typed"""
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, text)
        self.add_message("You (Voice)", text, get_theme().colors['primary'])
        self.send_message()
    
    def update_voice_status_listening(self):
        """Update UI to show listening status"""
        if self.voice_status_label:
            self.voice_status_label.config(text="🎤 Listening...")
        if self.voice_button:
            self.voice_button.config(text="🔴", style='MD3.Secondary.TButton')
    
    def update_voice_status_idle(self):
        """Update UI to show idle status"""
        if self.voice_status_label:
            self.voice_status_label.config(text="🎤 Ready")
        if self.voice_button:
            self.voice_button.config(text="🎤", style='MD3.Primary.TButton')
    
    def toggle_voice_listening(self):
        """Toggle voice listening on/off"""
        if not self.voice_enabled:
            self.add_message("System", "Voice features not available. Install speech_recognition and pyttsx3.", 
                           get_theme().colors['error'])
            return
        
        if self.is_listening:
            self.voice_manager.stop_listening()
            self.is_listening = False
        else:
            if self.voice_manager.start_listening():
                self.is_listening = True
            else:
                self.add_message("System", "Failed to start voice recognition", get_theme().colors['error'])
    
    def load_settings(self):
        """Load settings from config file"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
                    self.current_api_key = config.get('api_key', '')
                    self.current_model = config.get('model', 'gemini-2.0-flash-exp')
                    self.theme_mode = config.get('theme_mode', 'dark')
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to config file"""
        try:
            config = {
                'api_key': self.current_api_key,
                'model': self.current_model,
                'theme_mode': self.theme_mode
            }
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def setup_main_window(self):
        """Setup the main application window"""
        self.root.title("JR AI Control - Voice Demo")
        
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
    
    def create_ui(self):
        """Create the main user interface"""
        # Main container with MD3 styling
        main_frame = tk.Frame(self.root, **create_md3_widget_config('Frame', get_theme()))
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header frame
        header_frame = tk.Frame(main_frame, **create_md3_widget_config('Frame', get_theme()))
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title and model info section
        title_section = tk.Frame(header_frame, **create_md3_widget_config('Frame', get_theme()))
        title_section.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Main title
        title_label = ttk.Label(title_section, text="JR AI Control", style='MD3.Headline.Medium.TLabel')
        title_label.pack(anchor=tk.W)
        
        # Model name display
        self.model_label = ttk.Label(title_section, text=f"Model: {self.current_model}", 
                                   style='MD3.Body.Medium.TLabel')
        self.model_label.pack(anchor=tk.W)
        
        # Token usage display
        token_frame = tk.Frame(title_section, **create_md3_widget_config('Frame', get_theme()))
        token_frame.pack(anchor=tk.W, pady=(2, 0))
        
        self.token_display = ttk.Label(token_frame, text="Message: 0 tokens", 
                                     style='MD3.Body.Small.TLabel')
        self.token_display.pack(side=tk.LEFT)
        
        ttk.Label(token_frame, text=" | ", style='MD3.Body.Small.TLabel').pack(side=tk.LEFT)
        
        total_tokens = self.token_tracker.get_total_tokens()
        self.total_token_display = ttk.Label(token_frame, text=f"Total: {total_tokens:,} tokens", 
                                           style='MD3.Body.Small.TLabel')
        self.total_token_display.pack(side=tk.LEFT)
        
        # Voice status
        voice_frame = tk.Frame(title_section, **create_md3_widget_config('Frame', get_theme()))
        voice_frame.pack(anchor=tk.W, pady=(2, 0))
        
        voice_status_text = "🎤 Ready" if self.voice_enabled else "🎤 Unavailable"
        self.voice_status_label = ttk.Label(voice_frame, text=voice_status_text, 
                                          style='MD3.Body.Small.TLabel')
        self.voice_status_label.pack(side=tk.LEFT)
        
        # Settings button
        settings_btn = ttk.Button(header_frame, text="⚙️", style='MD3.Secondary.TButton',
                                 command=self.open_settings, width=3)
        settings_btn.pack(side=tk.RIGHT)
        
        # Voice button
        voice_btn_text = "🎤" if self.voice_enabled else "🚫"
        voice_btn_style = 'MD3.Primary.TButton' if self.voice_enabled else 'MD3.Tertiary.TButton'
        self.voice_button = ttk.Button(header_frame, text=voice_btn_text, style=voice_btn_style,
                                     command=self.toggle_voice_listening, width=3)
        self.voice_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Status indicator
        self.status_frame = tk.Frame(header_frame, **create_md3_widget_config('Frame', get_theme()))
        self.status_frame.pack(side=tk.RIGHT, padx=(0, 10))
        
        status_color = get_theme().colors['tertiary'] if not self.current_api_key else get_theme().colors['secondary']
        self.status_indicator = tk.Label(self.status_frame, text="●", 
                                       fg=status_color,
                                       bg=get_theme().colors['surface'], 
                                       font=get_theme().typography['body_medium'])
        self.status_indicator.pack(side=tk.LEFT)
        
        status_text = "Voice Demo" if not self.current_api_key else "Connected"
        self.status_label = tk.Label(self.status_frame, text=status_text,
                                   **create_md3_widget_config('Label', get_theme()))
        self.status_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Chat display area
        chat_frame = tk.Frame(main_frame, **create_md3_widget_config('Frame', get_theme()))
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create custom scrolled text with MD3 styling
        text_config = create_md3_widget_config('Text', get_theme())
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            **text_config
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Hide scrollbar for cleaner look
        self.chat_display.vbar.pack_forget()
        
        # Input frame
        input_frame = tk.Frame(main_frame, **create_md3_widget_config('Frame', get_theme()))
        input_frame.pack(fill=tk.X)
        
        # Input entry with MD3 styling
        entry_config = create_md3_widget_config('Entry', get_theme())
        self.input_entry = tk.Entry(input_frame, **entry_config)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind('<Return>', self.send_message)
        
        # Send button
        self.send_btn = ttk.Button(input_frame, text="Send", style='MD3.Primary.TButton',
                                  command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT)
        
        # Add welcome messages
        self.add_message("System", "Welcome to JR AI Control! 🚀", get_theme().colors['primary'])
        self.add_message("System", "🎤 Voice interaction enabled!" if self.voice_enabled else "🎤 Voice not available", 
                        get_theme().colors['secondary'] if self.voice_enabled else get_theme().colors['error'])
        self.add_message("System", "✨ Material Design 3 Interface", get_theme().colors['tertiary'])
        self.add_message("System", "📊 Token tracking active", get_theme().colors['outline'])
        
        if self.voice_enabled:
            self.add_message("System", "Click the 🎤 button to start voice recognition", get_theme().colors['secondary'])
    
    def add_message(self, sender, message, color="#ffffff"):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        
        # Add sender and timestamp
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, f"{sender}: ", "sender")
        self.chat_display.insert(tk.END, f"{message}\n\n", "message")
        
        # Configure tags for styling
        self.chat_display.tag_config("timestamp", foreground=get_theme().colors['outline'], 
                                   font=get_theme().typography['body_small'])
        self.chat_display.tag_config("sender", foreground=color, 
                                   font=get_theme().typography['label_medium'])
        self.chat_display.tag_config("message", foreground=get_theme().colors['on_surface'], 
                                   font=get_theme().typography['body_medium'])
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_message(self, event=None):
        """Send a demo message"""
        message = self.input_entry.get().strip()
        if not message:
            return
        
        # Generate unique message ID
        self.current_message_id = str(uuid.uuid4())
        
        # Clear input
        self.input_entry.delete(0, tk.END)
        
        # Add user message (if not already added by voice)
        if not message.startswith("You (Voice)"):
            self.add_message("You", message, get_theme().colors['primary'])
        
        # Disable send button while processing
        self.send_btn.config(state='disabled', text="Thinking...")
        self.input_entry.config(state='disabled')
        
        # Process message in separate thread
        threading.Thread(target=self.process_demo_message, args=(message,), daemon=True).start()
    
    def process_demo_message(self, message):
        """Process demo message with simulated AI response"""
        try:
            time.sleep(1)  # Simulate processing time
            
            # Generate demo response
            voice_responses = [
                "I can hear you loud and clear! Voice recognition is working perfectly! 🎤",
                "Your voice input has been processed successfully! This is amazing! ✨",
                "Speaking to me is so much more natural than typing, isn't it? 🗣️",
                "I love our voice conversation! The speech recognition is very accurate! 🎯",
                "Voice interaction makes our chat feel more human and engaging! 🤖"
            ]
            
            text_responses = [
                "This is a demo of the new JR AI Control interface! 🎨",
                "The Material Design 3 theme looks fantastic! ✨",
                "Token tracking is working perfectly - check the counts above! 📊",
                "The new UI is incredibly modern and user-friendly! 🚀",
                "Try the voice button to experience speech recognition! 🎤"
            ]
            
            import random
            # Use voice responses if message came from voice input
            if "voice" in message.lower() or self.is_listening:
                output = random.choice(voice_responses)
            else:
                output = random.choice(text_responses)
            
            # Simulate token tracking
            if self.current_message_id:
                tokens_used = self.token_tracker.track_message(
                    self.current_message_id, message, output, self.current_model
                )
                
                # Update token displays in main thread
                self.root.after(0, lambda: self.update_token_displays(tokens_used))
            
            # Update UI in main thread
            self.root.after(0, lambda: self.add_message("JR AI", output, get_theme().colors['secondary']))
            
            # Speak the response if voice is enabled
            if self.voice_enabled and self.voice_manager.speech_enabled:
                self.voice_manager.speak_text(output)
            
        except Exception as e:
            error_msg = f"Demo Error: {str(e)}"
            self.root.after(0, lambda: self.add_message("System", error_msg, get_theme().colors['error']))
        
        finally:
            # Re-enable controls
            self.root.after(0, self.enable_input)
    
    def enable_input(self):
        """Re-enable input controls"""
        self.send_btn.config(state='normal', text="Send")
        self.input_entry.config(state='normal')
        self.input_entry.focus()
    
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
        """Open the settings popup"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings - Voice Demo")
        settings_window.configure(bg=get_theme().colors['background'])
        settings_window.geometry("500x500")
        settings_window.resizable(False, False)
        
        # Center the window
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(settings_window, **create_md3_widget_config('Frame', get_theme()))
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="Settings", style='MD3.Headline.Small.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Voice settings section
        voice_frame = tk.Frame(main_frame, **create_md3_widget_config('Frame', get_theme()))
        voice_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(voice_frame, text="🎤 Voice Settings:", style='MD3.Title.Medium.TLabel').pack(anchor=tk.W)
        
        # Voice enabled toggle
        voice_enabled_frame = tk.Frame(voice_frame, **create_md3_widget_config('Frame', get_theme()))
        voice_enabled_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Label(voice_enabled_frame, text="Speech Output:", style='MD3.Label.Large.TLabel').pack(side=tk.LEFT)
        
        voice_enabled_var = tk.BooleanVar(value=self.voice_manager.speech_enabled if self.voice_enabled else False)
        voice_enabled_check = ttk.Checkbutton(voice_enabled_frame, variable=voice_enabled_var,
                                            command=lambda: self.toggle_voice_output(voice_enabled_var.get()))
        voice_enabled_check.pack(side=tk.RIGHT)
        
        # Voice status
        voice_status_text = "Available" if self.voice_enabled else "Not Available (install speech_recognition & pyttsx3)"
        voice_status_color = get_theme().colors['secondary'] if self.voice_enabled else get_theme().colors['error']
        voice_status_label = ttk.Label(voice_frame, text=f"Status: {voice_status_text}", 
                                     style='MD3.Body.Small.TLabel')
        voice_status_label.pack(anchor=tk.W, pady=(5, 0))
        
        # API Key section
        api_frame = tk.Frame(main_frame, **create_md3_widget_config('Frame', get_theme()))
        api_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(api_frame, text="Gemini API Key:", style='MD3.Label.Large.TLabel').pack(anchor=tk.W)
        
        api_entry_frame = tk.Frame(api_frame, **create_md3_widget_config('Frame', get_theme()))
        api_entry_frame.pack(fill=tk.X, pady=(5, 0))
        
        api_entry = tk.Entry(api_entry_frame, **create_md3_widget_config('Entry', get_theme()))
        api_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        api_entry.insert(0, "demo-api-key-placeholder")
        
        # Test button
        test_btn = ttk.Button(api_entry_frame, text="Test", style='MD3.Primary.TButton',
                             command=lambda: self.demo_test_api(test_status))
        test_btn.pack(side=tk.RIGHT)
        
        # Test status
        test_status = ttk.Label(api_frame, text="", style='MD3.Body.Small.TLabel')
        test_status.pack(anchor=tk.W, pady=(5, 0))
        
        # Model selection
        model_frame = tk.Frame(main_frame, **create_md3_widget_config('Frame', get_theme()))
        model_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(model_frame, text="Model:", style='MD3.Label.Large.TLabel').pack(anchor=tk.W)
        
        model_var = tk.StringVar(value=self.current_model)
        model_combo = ttk.Combobox(model_frame, textvariable=model_var, 
                                  values=self.available_models, 
                                  state='readonly', style='MD3.TCombobox')
        model_combo.pack(fill=tk.X, pady=(5, 0))
        
        # Buttons frame
        btn_frame = tk.Frame(main_frame, **create_md3_widget_config('Frame', get_theme()))
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Cancel button
        cancel_btn = ttk.Button(btn_frame, text="Cancel", style='MD3.Tertiary.TButton',
                               command=settings_window.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Save button
        save_btn = ttk.Button(btn_frame, text="Save", style='MD3.Primary.TButton',
                             command=lambda: self.demo_save_settings(
                                 api_entry.get(), model_var.get(), settings_window))
        save_btn.pack(side=tk.RIGHT)
    
    def toggle_voice_output(self, enabled):
        """Toggle voice output on/off"""
        if self.voice_enabled:
            self.voice_manager.toggle_speech_enabled(enabled)
            status = "enabled" if enabled else "disabled"
            self.add_message("System", f"Voice output {status}", get_theme().colors['secondary'])
    
    def demo_test_api(self, status_label):
        """Demo API key test"""
        status_label.config(text="Testing...")
        
        def test():
            time.sleep(1)
            self.root.after(0, lambda: status_label.config(text="✓ Demo API Key Valid"))
        
        threading.Thread(target=test, daemon=True).start()
    
    def demo_save_settings(self, api_key, model, window):
        """Demo save settings"""
        self.current_api_key = api_key.strip()
        self.current_model = model
        
        # Save to file
        self.save_settings()
        
        # Update displays
        self.update_model_display()
        
        # Close dialog
        window.destroy()
        
        # Show success message
        self.add_message("System", "Settings saved! (Voice Demo)", get_theme().colors['secondary'])
    
    def run(self):
        """Start the application"""
        # Focus on input
        self.input_entry.focus()
        
        # Cleanup on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start the main loop
        self.root.mainloop()
    
    def on_closing(self):
        """Handle application closing"""
        if self.voice_enabled:
            self.voice_manager.cleanup()
        self.root.destroy()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Launch JR AI Control Voice Demo with Material Design 3 UI.")
    parser.add_argument('--theme', type=str, default='dark', choices=['dark', 'light'],
                        help="Theme mode: dark or light. Default is dark.")
    
    args = parser.parse_args()
    
    # Create and run the demo application
    app = JRAIControlVoiceDemo()
    app.theme_mode = args.theme
    
    app.run()

if __name__ == "__main__":
    main()