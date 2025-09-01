#!/usr/bin/env python3
"""
Test the GUI without making API calls
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime

class TestClevrrGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_main_window()
        self.create_ui()
    
    def setup_main_window(self):
        """Setup the main application window"""
        self.root.title("Clevrr Computer - GUI Test")
        self.root.configure(bg='#2b2b2b')
        
        # Set window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.35)
        window_height = screen_height - 100
        
        x = screen_width - window_width - 20
        y = 50
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(True, True)
        
        # Configure styles
        self.setup_styles()
    
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
        """Create the main user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header frame
        header_frame = tk.Frame(main_frame, bg='#2b2b2b')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = ttk.Label(header_frame, text="Clevrr Computer", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Settings button
        settings_btn = ttk.Button(header_frame, text="⚙️", style='Settings.TButton',
                                 command=self.open_settings, width=3)
        settings_btn.pack(side=tk.RIGHT)
        
        # Status indicator
        status_frame = tk.Frame(header_frame, bg='#2b2b2b')
        status_frame.pack(side=tk.RIGHT, padx=(0, 10))
        
        status_indicator = tk.Label(status_frame, text="●", 
                                   fg='#28a745',
                                   bg='#2b2b2b', font=('Segoe UI', 12))
        status_indicator.pack(side=tk.LEFT)
        
        status_label = tk.Label(status_frame, 
                               text="GUI Test Mode",
                               fg='#ffffff', bg='#2b2b2b', font=('Segoe UI', 9))
        status_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Chat display area
        chat_frame = tk.Frame(main_frame, bg='#2b2b2b')
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            bg='#1e1e1e',
            fg='#ffffff',
            font=('Segoe UI', 10),
            borderwidth=1,
            relief='solid',
            insertbackground='#ffffff'
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg='#2b2b2b')
        input_frame.pack(fill=tk.X)
        
        # Input entry
        self.input_entry = tk.Entry(
            input_frame,
            bg='#3c3c3c',
            fg='#ffffff',
            font=('Segoe UI', 11),
            borderwidth=1,
            relief='solid',
            insertbackground='#ffffff'
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind('<Return>', self.send_test_message)
        
        # Send button
        send_btn = ttk.Button(input_frame, text="Send", style='Modern.TButton',
                             command=self.send_test_message)
        send_btn.pack(side=tk.RIGHT)
        
        # Add welcome messages
        self.add_message("System", "Welcome to Clevrr Computer! 🚀", "#4a9eff")
        self.add_message("System", "GUI Test Mode - Type anything to test the interface", "#ffc107")
    
    def add_message(self, sender, message, color="#ffffff"):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        
        # Add sender and timestamp
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, f"{sender}: ", "sender")
        self.chat_display.insert(tk.END, f"{message}\n\n", "message")
        
        # Configure tags for styling
        self.chat_display.tag_config("timestamp", foreground="#888888", font=('Segoe UI', 9))
        self.chat_display.tag_config("sender", foreground=color, font=('Segoe UI', 10, 'bold'))
        self.chat_display.tag_config("message", foreground="#ffffff", font=('Segoe UI', 10))
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_test_message(self, event=None):
        """Send a test message"""
        message = self.input_entry.get().strip()
        if not message:
            return
        
        # Clear input
        self.input_entry.delete(0, tk.END)
        
        # Add user message
        self.add_message("You", message, "#4a9eff")
        
        # Add mock AI response
        responses = [
            "This is a test response from the AI! 🤖",
            "GUI is working perfectly! ✨",
            "I can see your message clearly! 👀",
            "The interface looks great! 🎨",
            "Ready for automation tasks! ⚡"
        ]
        
        import random
        response = random.choice(responses)
        self.add_message("Clevrr", response, "#28a745")
    
    def open_settings(self):
        """Open the settings popup"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.configure(bg='#2b2b2b')
        settings_window.geometry("500x400")
        settings_window.resizable(False, False)
        
        # Center the window
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(settings_window, bg='#2b2b2b', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Settings", 
                              bg='#2b2b2b', fg='#ffffff', 
                              font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # API Key section
        api_frame = tk.Frame(main_frame, bg='#2b2b2b')
        api_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(api_frame, text="Gemini API Key:", 
                bg='#2b2b2b', fg='#ffffff', 
                font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W)
        
        api_entry_frame = tk.Frame(api_frame, bg='#2b2b2b')
        api_entry_frame.pack(fill=tk.X, pady=(5, 0))
        
        api_entry = tk.Entry(api_entry_frame, 
                           bg='#3c3c3c', fg='#ffffff', 
                           font=('Segoe UI', 10),
                           insertbackground='#ffffff')
        api_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        api_entry.insert(0, "your-api-key-here")
        
        # Test button
        test_btn = ttk.Button(api_entry_frame, text="Test", style='Modern.TButton',
                             command=lambda: self.test_api_key_mock(test_status))
        test_btn.pack(side=tk.RIGHT)
        
        # Test status
        test_status = tk.Label(api_frame, text="", bg='#2b2b2b', font=('Segoe UI', 9))
        test_status.pack(anchor=tk.W, pady=(5, 0))
        
        # Model selection
        model_frame = tk.Frame(main_frame, bg='#2b2b2b')
        model_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(model_frame, text="Model:", 
                bg='#2b2b2b', fg='#ffffff', 
                font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W)
        
        model_var = tk.StringVar(value="gemini-2.0-flash-exp")
        available_models = [
            "gemini-2.0-flash-exp",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro"
        ]
        model_combo = ttk.Combobox(model_frame, textvariable=model_var, 
                                  values=available_models, 
                                  state='readonly', font=('Segoe UI', 10))
        model_combo.pack(fill=tk.X, pady=(5, 0))
        
        # Buttons frame
        btn_frame = tk.Frame(main_frame, bg='#2b2b2b')
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Cancel button
        cancel_btn = ttk.Button(btn_frame, text="Cancel", style='Settings.TButton',
                               command=settings_window.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Save button
        save_btn = ttk.Button(btn_frame, text="Save", style='Modern.TButton',
                             command=lambda: self.save_test_settings(settings_window))
        save_btn.pack(side=tk.RIGHT)
    
    def test_api_key_mock(self, status_label):
        """Mock API key test"""
        status_label.config(text="Testing...", fg='#ffc107')
        self.root.after(1000, lambda: status_label.config(text="✓ API Key Valid (Mock)", fg='#28a745'))
    
    def save_test_settings(self, window):
        """Save test settings"""
        window.destroy()
        self.add_message("System", "Settings saved successfully! (Test Mode)", "#28a745")
    
    def run(self):
        """Start the application"""
        self.input_entry.focus()
        self.root.mainloop()

if __name__ == "__main__":
    app = TestClevrrGUI()
    app.run()