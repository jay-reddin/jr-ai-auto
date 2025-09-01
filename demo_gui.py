#!/usr/bin/env python3
"""
Demo version of Clevrr Computer GUI - Works without API keys
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import os
import threading
import time
from datetime import datetime

class ClevrrComputerDemo:
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
        
        self.setup_main_window()
        self.create_ui()
    
    def setup_main_window(self):
        """Setup the main application window"""
        self.root.title("Clevrr Computer - Demo")
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
        
        self.setup_styles()
    
    def setup_styles(self):
        """Setup custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', 
                       background='#2b2b2b', 
                       foreground='#ffffff', 
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure('Modern.TButton',
                       background='#4a9eff',
                       foreground='white',
                       font=('Segoe UI', 10),
                       borderwidth=0)
        
        style.map('Modern.TButton',
                 background=[('active', '#3d8bdb')])
        
        style.configure('Settings.TButton',
                       background='#6c757d',
                       foreground='white',
                       font=('Segoe UI', 10),
                       borderwidth=0)
    
    def create_ui(self):
        """Create the main user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2b2b2b')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="Clevrr Computer", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        settings_btn = ttk.Button(header_frame, text="⚙️", style='Settings.TButton',
                                 command=self.open_settings, width=3)
        settings_btn.pack(side=tk.RIGHT)
        
        # Status
        self.status_frame = tk.Frame(header_frame, bg='#2b2b2b')
        self.status_frame.pack(side=tk.RIGHT, padx=(0, 10))
        
        self.status_indicator = tk.Label(self.status_frame, text="●", 
                                       fg='#ffc107', bg='#2b2b2b', font=('Segoe UI', 12))
        self.status_indicator.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(self.status_frame, text="Demo Mode",
                                   fg='#ffffff', bg='#2b2b2b', font=('Segoe UI', 9))
        self.status_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Chat display
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
        
        # Input
        input_frame = tk.Frame(main_frame, bg='#2b2b2b')
        input_frame.pack(fill=tk.X)
        
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
        self.input_entry.bind('<Return>', self.send_message)
        
        self.send_btn = ttk.Button(input_frame, text="Send", style='Modern.TButton',
                                  command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT)
        
        # Welcome messages
        self.add_message("System", "🚀 Welcome to Clevrr Computer!", "#4a9eff")
        self.add_message("System", "✨ This is a demo of the new interface", "#ffc107")
        self.add_message("System", "💡 Try typing a message to see the chat interface in action", "#28a745")
        self.add_message("System", "⚙️ Click the settings icon to see the configuration panel", "#6c757d")
    
    def add_message(self, sender, message, color="#ffffff"):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, f"{sender}: ", "sender")
        self.chat_display.insert(tk.END, f"{message}\n\n", "message")
        
        self.chat_display.tag_config("timestamp", foreground="#888888", font=('Segoe UI', 9))
        self.chat_display.tag_config("sender", foreground=color, font=('Segoe UI', 10, 'bold'))
        self.chat_display.tag_config("message", foreground="#ffffff", font=('Segoe UI', 10))
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_message(self, event=None):
        """Send a demo message"""
        message = self.input_entry.get().strip()
        if not message:
            return
        
        self.input_entry.delete(0, tk.END)
        self.add_message("You", message, "#4a9eff")
        
        # Simulate thinking
        self.send_btn.config(state='disabled', text="Thinking...")
        
        def respond():
            time.sleep(1)
            responses = [
                "This is a demo response! The real app would use AI here. 🤖",
                "Great question! In the full version, I'd help with automation tasks. ⚡",
                "I can see your message clearly! The interface is working perfectly. ✨",
                "In demo mode, I can only show you how the chat works. Try the settings! ⚙️",
                "The real Clevrr Computer would help automate your computer tasks! 🖥️"
            ]
            
            import random
            response = random.choice(responses)
            
            self.root.after(0, lambda: self.add_message("Clevrr Demo", response, "#28a745"))
            self.root.after(0, lambda: self.send_btn.config(state='normal', text="Send"))
        
        threading.Thread(target=respond, daemon=True).start()
    
    def open_settings(self):
        """Open settings demo"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings - Demo")
        settings_window.configure(bg='#2b2b2b')
        settings_window.geometry("500x400")
        settings_window.resizable(False, False)
        
        settings_window.transient(self.root)
        settings_window.grab_set()
        
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
        api_entry.insert(0, "demo-api-key-placeholder")
        
        test_btn = ttk.Button(api_entry_frame, text="Test", style='Modern.TButton',
                             command=lambda: self.demo_test_api(test_status))
        test_btn.pack(side=tk.RIGHT)
        
        test_status = tk.Label(api_frame, text="", bg='#2b2b2b', font=('Segoe UI', 9))
        test_status.pack(anchor=tk.W, pady=(5, 0))
        
        # Model selection
        model_frame = tk.Frame(main_frame, bg='#2b2b2b')
        model_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(model_frame, text="Model:", 
                bg='#2b2b2b', fg='#ffffff', 
                font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W)
        
        model_var = tk.StringVar(value=self.current_model)
        model_combo = ttk.Combobox(model_frame, textvariable=model_var, 
                                  values=self.available_models, 
                                  state='readonly', font=('Segoe UI', 10))
        model_combo.pack(fill=tk.X, pady=(5, 0))
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg='#2b2b2b')
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        cancel_btn = ttk.Button(btn_frame, text="Cancel", style='Settings.TButton',
                               command=settings_window.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        save_btn = ttk.Button(btn_frame, text="Save", style='Modern.TButton',
                             command=lambda: self.demo_save(settings_window))
        save_btn.pack(side=tk.RIGHT)
    
    def demo_test_api(self, status_label):
        """Demo API test"""
        status_label.config(text="Testing...", fg='#ffc107')
        
        def test():
            time.sleep(1)
            self.root.after(0, lambda: status_label.config(text="✓ Demo API Key Valid", fg='#28a745'))
        
        threading.Thread(target=test, daemon=True).start()
    
    def demo_save(self, window):
        """Demo save"""
        window.destroy()
        self.add_message("System", "Settings saved! (Demo mode)", "#28a745")
    
    def run(self):
        """Start the demo"""
        self.input_entry.focus()
        self.root.mainloop()

if __name__ == "__main__":
    print("Starting Clevrr Computer Demo...")
    print("This demo shows the new interface without requiring API keys.")
    app = ClevrrComputerDemo()
    app.run()