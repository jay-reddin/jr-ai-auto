#!/usr/bin/env python3
"""
JR AI Control - Enhanced Main Application
Material Design 3 UI with integrated voice, notifications, and token tracking
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import argparse
import os
import json
from datetime import datetime

from utils.agent import create_agent
from utils.contants import MODELS, VERSION, LAST_CHANGES
from ui.material_design import get_theme_manager, apply_global_theme
from ui.enhanced_components import EnhancedChatInterface
from utils.token_tracker import get_token_tracker
from utils.notifications import get_notification_manager
from voice.voice_manager import get_voice_manager

class JRAIControlEnhancedApp:
    """Enhanced JR AI Control application with Material Design 3 UI"""
    
    def __init__(self):
        self.root = tk.Tk()
        
        # Initialize managers
        self.theme_manager = get_theme_manager()
        self.token_tracker = get_token_tracker()
        self.notification_manager = get_notification_manager()
        self.voice_manager = get_voice_manager()
        
        # Application state
        self.agent_executor = None
        self.current_api_key = ""
        self.current_model = "gemini-2.0-flash-exp"
        self.available_models = list(MODELS.keys())
        
        # Load settings
        self.load_settings()
        
        # Setup main window
        self.setup_main_window()
        
        # Create enhanced UI
        self.create_enhanced_ui()
        
        # Initialize agent if API key is available
        if self.current_api_key and self.current_api_key != "your_api_key_here":
            self.initialize_agent()
        
        # Show welcome notification
        self.notification_manager.show_info_notification(
            "JR AI Control Started", 
            "Enhanced AI assistant is ready!"
        )
    
    def setup_main_window(self):
        """Setup the main application window"""
        self.root.title("JR AI Control")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Apply Material Design 3 theme
        self.theme_manager.apply_theme(self.root)
        
        # Set window icon (if available)
        try:
            if os.path.exists("assets/icon.ico"):
                self.root.iconbitmap("assets/icon.ico")
        except Exception:
            pass
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_enhanced_ui(self):
        """Create the enhanced user interface"""
        # Create main container
        main_container = tk.Frame(self.root, bg=self.theme_manager.get_color('background'))
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create enhanced chat interface
        self.chat_interface = EnhancedChatInterface(
            main_container, 
            on_message_send=self.handle_user_message
        )
        self.chat_interface.pack(fill=tk.BOTH, expand=True)
        
        # Add welcome message
        self.chat_interface.add_message(
            "System", 
            "Welcome to JR AI Control! 🚀\\n\\nThis enhanced AI assistant features:\\n• Material Design 3 UI\\n• Voice interaction (if available)\\n• Token tracking\\n• Smart notifications\\n\\nType a message or use voice input to get started!",
            "system"
        )
    
    def handle_user_message(self, message: str):
        """Handle user message and generate AI response"""
        if not self.agent_executor:
            self.chat_interface.add_message(
                "System", 
                "❌ No AI agent available. Please configure your API key in settings.",
                "system"
            )
            return
        
        try:
            # Show typing indicator (could be enhanced with animation)
            self.chat_interface.add_message("JR AI", "Thinking...", "ai")
            
            # Generate response in background thread
            def generate_response():
                try:
                    # Get AI response
                    response = self.agent_executor.invoke({"input": message})
                    ai_response = response.get("output", "I apologize, but I couldn't generate a response.")
                    
                    # Update the last message with actual response
                    self.root.after(0, lambda: self.update_ai_response(ai_response))
                    
                    # Track tokens
                    message_id = f"msg_{int(time.time())}"
                    tokens_used = self.token_tracker.add_message_tokens(
                        message_id, message, ai_response
                    )
                    
                    # Show completion notification
                    self.notification_manager.show_task_completion(
                        "AI Response Generated",
                        f"Used {tokens_used} tokens"
                    )
                    
                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    self.root.after(0, lambda: self.update_ai_response(error_msg))
                    
                    # Show error notification
                    self.notification_manager.show_error_notification(
                        f"AI Error: {str(e)}"
                    )
            
            # Start response generation in background
            threading.Thread(target=generate_response, daemon=True).start()
            
        except Exception as e:
            self.chat_interface.add_message(
                "System", 
                f"❌ Error: {str(e)}",
                "system"
            )
    
    def update_ai_response(self, response: str):
        """Update the AI response in the chat interface"""
        # Remove the "Thinking..." message and add actual response
        # This is a simplified approach - in a full implementation, 
        # we'd want to replace the last message
        self.chat_interface.add_message("JR AI", response, "ai")
    
    def initialize_agent(self):
        """Initialize the AI agent"""
        try:
            # Set environment variable
            os.environ["GOOGLE_API_KEY"] = self.current_api_key
            
            # Create agent
            self.agent_executor = create_agent(self.current_model)
            
            # Update status
            self.notification_manager.show_info_notification(
                "Agent Initialized", 
                f"Connected with {self.current_model}"
            )
            
            return True
            
        except Exception as e:
            self.notification_manager.show_error_notification(
                f"Failed to initialize agent: {str(e)}"
            )
            return False
    
    def load_settings(self):
        """Load application settings"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
                
                self.current_api_key = config.get('api_key', '')
                self.current_model = config.get('model', 'gemini-2.0-flash-exp')
                
                # Load theme preference
                theme_mode = config.get('theme_mode', 'dark')
                if theme_mode != self.theme_manager.theme_mode:
                    self.theme_manager.switch_theme(theme_mode)
                
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save application settings"""
        try:
            config = {
                'api_key': self.current_api_key,
                'model': self.current_model,
                'theme_mode': self.theme_manager.theme_mode,
                'version': VERSION,
                'last_updated': datetime.now().isoformat()
            }
            
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
                
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        try:
            # Save settings
            self.save_settings()
            
            # Cleanup resources
            if hasattr(self, 'voice_manager'):
                self.voice_manager.cleanup()
            
            if hasattr(self, 'notification_manager'):
                self.notification_manager.cleanup()
            
            # Show goodbye notification
            self.notification_manager.show_info_notification(
                "JR AI Control", 
                "Goodbye! See you next time.",
                duration=2
            )
            
            # Small delay to show notification
            self.root.after(1000, self.root.destroy)
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
            self.root.destroy()
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
        except Exception as e:
            print(f"Application error: {e}")
            self.on_closing()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Launch the JR AI Control application with enhanced features.")
    parser.add_argument("--model", choices=list(MODELS.keys()), default="gemini-2.0-flash-exp",
                       help="AI model to use (default: gemini-2.0-flash-exp)")
    parser.add_argument("--theme", choices=["dark", "light"], default="dark",
                       help="UI theme mode (default: dark)")
    parser.add_argument("--voice", action="store_true", 
                       help="Enable voice interaction on startup")
    
    args = parser.parse_args()
    
    # Print startup information
    print("=" * 50)
    print("🚀 JR AI Control - Enhanced Edition")
    print(f"Version: {VERSION}")
    print(f"Model: {args.model}")
    print(f"Theme: {args.theme}")
    print(f"Voice: {'Enabled' if args.voice else 'Disabled'}")
    print("=" * 50)
    
    # Create and run application
    app = JRAIControlEnhancedApp()
    
    # Apply command line arguments
    if args.theme != app.theme_manager.theme_mode:
        app.theme_manager.switch_theme(args.theme)
        app.theme_manager.apply_theme(app.root)
    
    if args.voice and app.voice_manager.is_voice_available():
        app.voice_manager.toggle_speech(True)
    
    app.current_model = args.model
    
    # Run the application
    app.run()

if __name__ == "__main__":
    main()