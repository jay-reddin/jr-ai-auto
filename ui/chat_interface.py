"""
Enhanced hat interface with screenshot thumbnail support for JR AI Control.
Provides modern chat bubbles with thumbnail integration and click-to-expand functionality.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import time
from datetime import datetime
from typing import Optional, Dict, Any, Callable
from ui.material_design import get_theme
from ui.enhanced_components import MD3Frame, MD3Card, MD3Button
from utils.screenshot_manager import ScreenshotManager

class ThumbnailViewer(tk.Toplevel):
    """Modal dialog for viewing full-size screenshots"""
    
    def __init__(self, parent, image_path: str, title: str = "Screenshot"):
        super().__init__(parent)
        
        self.title(title)
        self.transient(parent)
        self.grab_set()
        
        # Configure window
        theme = get_theme()
        self.configure(bg=theme.colors['surface'])
        
        # Load and display image
        self.setup_image_display(image_path)
        
        # Center window
        self.center_window()
        
        # Bind escape key to close
        self.bind('<Escape>', lambda e: self.destroy())
        self.bind('<Button-1>', lambda e: self.destroy())
    
    def setup_image_display(self, image_path: str):
        """Setup the image display with proper scaling"""
        try:
            # Load image
            with Image.open(image_path) as img:
                # Get screen dimensions for scaling
                screen_width = self.winfo_screenwidth()
                screen_height = self.winfo_screenheight()
                
                # Calculate max size (80% of screen)
                max_width = int(screen_width * 0.8)
                max_height = int(screen_height * 0.8)
                
                # Scale image if needed
                img_width, img_height = img.size
                if img_width > max_width or img_height > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                self.photo = ImageTk.PhotoImage(img)
                
                # Create label to display image
                image_label = tk.Label(self, image=self.photo, bg=get_theme().colors['surface'])
                image_label.pack(padx=10, pady=10)
                
                # Set window size
                self.geometry(f"{img.width + 20}x{img.height + 20}")
                
        except Exception as e:
            # Error loading image
            error_label = tk.Label(self, 
                                 text=f"Error loading image: {e}",
                                 bg=get_theme().colors['surface'],
                                 fg=get_theme().colors['error'],
                                 font=get_theme().typography['body_medium'])
            error_label.pack(padx=20, pady=20)
            self.geometry("300x100")
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

class ChatMessage(MD3Frame):
    """Individual chat message with thumbnail support"""
    
    def __init__(self, parent, sender: str, message: str, timestamp: datetime, 
                 screenshot_id: Optional[str] = None, is_user: bool = False, 
                 tokens: int = 0, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.sender = sender
        self.message = message
        self.timestamp = timestamp
        self.screenshot_id = screenshot_id
        self.is_user = is_user
        self.tokens = tokens
        self.screenshot_manager = ScreenshotManager()
        
        self.theme = get_theme()
        self.configure(bg=self.theme.colors['surface'])
        
        # Create message layout
        self.create_message_layout()
    
    def configure_message(self, sender: str, message: str, timestamp: datetime, 
                         screenshot_id: Optional[str] = None, is_user: bool = False, 
                         tokens: int = 0):
        """Reconfigure this message widget with new data for reuse"""
        self.sender = sender
        self.message = message
        self.timestamp = timestamp
        self.screenshot_id = screenshot_id
        self.is_user = is_user
        self.tokens = tokens
        
        # Clear existing content
        for child in self.winfo_children():
            child.destroy()
        
        # Recreate layout with new data
        self.create_message_layout()
    
    def create_message_layout(self):
        """Create the message layout with bubble styling"""
        # Message container with proper alignment
        message_container = MD3Frame(self)
        if self.is_user:
            message_container.pack(fill=tk.X, padx=(50, 10), pady=5, anchor='e')
        else:
            message_container.pack(fill=tk.X, padx=(10, 50), pady=5, anchor='w')
        
        # Timestamp and sender info
        info_frame = MD3Frame(message_container)
        if self.is_user:
            info_frame.pack(fill=tk.X, anchor='e')
        else:
            info_frame.pack(fill=tk.X, anchor='w')
        
        # Timestamp
        timestamp_str = self.timestamp.strftime("%H:%M")
        timestamp_label = tk.Label(info_frame, 
                                 text=timestamp_str,
                                 font=self.theme.typography['body_small'],
                                 fg=self.theme.colors['outline'],
                                 bg=self.theme.colors['surface'])
        
        # Sender name
        sender_label = tk.Label(info_frame,
                              text=self.sender,
                              font=self.theme.typography['label_medium'],
                              fg=self.theme.colors['primary'] if self.is_user else self.theme.colors['secondary'],
                              bg=self.theme.colors['surface'])
        
        if self.is_user:
            timestamp_label.pack(side=tk.RIGHT)
            sender_label.pack(side=tk.RIGHT, padx=(0, 8))
        else:
            sender_label.pack(side=tk.LEFT)
            timestamp_label.pack(side=tk.LEFT, padx=(8, 0))
        
        # Message bubble
        bubble_frame = MD3Card(message_container)
        bubble_frame.pack(fill=tk.X, pady=(2, 0))
        
        # Configure bubble colors
        if self.is_user:
            bubble_frame.configure(bg=self.theme.colors['primary_container'])
            text_color = self.theme.colors['on_primary_container']
        else:
            bubble_frame.configure(bg=self.theme.colors['surface_variant'])
            text_color = self.theme.colors['on_surface_variant']
        
        # Bubble content
        bubble_content = MD3Frame(bubble_frame)
        bubble_content.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        bubble_content.configure(bg=bubble_frame['bg'])
        
        # Message text
        message_label = tk.Label(bubble_content,
                               text=self.message,
                               font=self.theme.typography['body_medium'],
                               fg=text_color,
                               bg=bubble_frame['bg'],
                               wraplength=400,
                               justify=tk.LEFT,
                               anchor='w')
        message_label.pack(fill=tk.X, anchor='w')
        
        # Screenshot thumbnail if available
        if self.screenshot_id:
            self.add_thumbnail(bubble_content, bubble_frame['bg'])
        
        # Token count for AI messages
        if not self.is_user and self.tokens > 0:
            token_label = tk.Label(bubble_content,
                                 text=f"Tokens: {self.tokens:,}",
                                 font=self.theme.typography['body_small'],
                                 fg=self.theme.colors['outline'],
                                 bg=bubble_frame['bg'])
            token_label.pack(anchor='w', pady=(4, 0))
        
        # Message actions
        self.add_message_actions(message_container, bubble_frame['bg'])
    
    def add_thumbnail(self, parent, bg_color):
        """Add screenshot thumbnail to the message"""
        try:
            thumbnail_path = self.screenshot_manager.get_thumbnail_path(self.screenshot_id)
            if thumbnail_path and os.path.exists(thumbnail_path):
                # Load thumbnail image
                with Image.open(thumbnail_path) as img:
                    # Ensure thumbnail is not too large
                    img.thumbnail((200, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                
                # Create thumbnail frame
                thumbnail_frame = MD3Frame(parent)
                thumbnail_frame.pack(fill=tk.X, pady=(8, 0))
                thumbnail_frame.configure(bg=bg_color)
                
                # Thumbnail button (clickable)
                thumbnail_btn = tk.Button(thumbnail_frame,
                                        image=photo,
                                        bg=bg_color,
                                        relief='flat',
                                        borderwidth=1,
                                        cursor='hand2',
                                        command=self.show_full_image)
                thumbnail_btn.pack(anchor='w')
                
                # Keep reference to prevent garbage collection
                thumbnail_btn.image = photo
                self.thumbnail_button = thumbnail_btn
                
                # Add hover effects
                def on_enter(e):
                    thumbnail_btn.configure(relief='raised')
                
                def on_leave(e):
                    thumbnail_btn.configure(relief='flat')
                
                thumbnail_btn.bind('<Enter>', on_enter)
                thumbnail_btn.bind('<Leave>', on_leave)
                
                # Add thumbnail info
                info = self.screenshot_manager.get_thumbnail_info(self.screenshot_id)
                if info:
                    size_text = f"Screenshot • {info['dimensions'][0]}×{info['dimensions'][1]}"
                    size_label = tk.Label(thumbnail_frame,
                                        text=size_text,
                                        font=self.theme.typography['body_small'],
                                        fg=self.theme.colors['outline'],
                                        bg=bg_color)
                    size_label.pack(anchor='w', pady=(2, 0))
                
        except Exception as e:
            # Error loading thumbnail
            error_label = tk.Label(parent,
                                 text=f"Error loading screenshot: {e}",
                                 font=self.theme.typography['body_small'],
                                 fg=self.theme.colors['error'],
                                 bg=bg_color)
            error_label.pack(anchor='w', pady=(4, 0))
    
    def show_full_image(self):
        """Show full-size image in modal dialog"""
        try:
            info = self.screenshot_manager.get_thumbnail_info(self.screenshot_id)
            if info:
                original_path = info['original_path']
                if os.path.exists(original_path):
                    ThumbnailViewer(self.winfo_toplevel(), original_path, 
                                  f"Screenshot - {self.timestamp.strftime('%H:%M:%S')}")
                else:
                    # Try to find screenshot.png as fallback
                    if os.path.exists("screenshot.png"):
                        ThumbnailViewer(self.winfo_toplevel(), "screenshot.png",
                                      f"Screenshot - {self.timestamp.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"Error showing full image: {e}")
    
    def add_message_actions(self, parent, bg_color):
        """Add message action buttons"""
        actions_frame = MD3Frame(parent)
        actions_frame.pack(fill=tk.X, pady=(4, 0))
        actions_frame.configure(bg=self.theme.colors['surface'])
        
        # Action buttons with small styling
        button_style = {
            'font': self.theme.typography['body_small'],
            'bg': self.theme.colors['surface'],
            'fg': self.theme.colors['outline'],
            'relief': 'flat',
            'borderwidth': 0,
            'cursor': 'hand2',
            'padx': 8,
            'pady': 2
        }
        
        if self.is_user:
            # Resend button for user messages
            resend_btn = tk.Button(actions_frame, text="↻ Resend", 
                                 command=self.resend_message, **button_style)
            resend_btn.pack(side=tk.RIGHT, padx=(4, 0))
        
        # Copy button
        copy_btn = tk.Button(actions_frame, text="📋 Copy", 
                           command=self.copy_message, **button_style)
        copy_btn.pack(side=tk.RIGHT, padx=(4, 0))
        
        # Delete button
        delete_btn = tk.Button(actions_frame, text="🗑️ Delete", 
                             command=self.delete_message, **button_style)
        delete_btn.pack(side=tk.RIGHT, padx=(4, 0))
        
        # Add hover effects to buttons
        for btn in [copy_btn, delete_btn] + ([resend_btn] if self.is_user else []):
            def make_hover_handler(button):
                def on_enter(e):
                    button.configure(bg=self.theme.colors['surface_variant'])
                def on_leave(e):
                    button.configure(bg=self.theme.colors['surface'])
                return on_enter, on_leave
            
            enter_handler, leave_handler = make_hover_handler(btn)
            btn.bind('<Enter>', enter_handler)
            btn.bind('<Leave>', leave_handler)
    
    def resend_message(self):
        """Handle resend message action"""
        # This will be connected to the main app's resend functionality
        if hasattr(self.master, 'resend_message_callback'):
            self.master.resend_message_callback(self.message)
    
    def copy_message(self):
        """Copy message to clipboard"""
        try:
            self.clipboard_clear()
            self.clipboard_append(self.message)
        except Exception as e:
            print(f"Error copying message: {e}")
    
    def delete_message(self):
        """Delete this message"""
        # This will be connected to the main app's delete functionality
        if hasattr(self.master, 'delete_message_callback'):
            self.master.delete_message_callback(self)
        else:
            # Default behavior - just hide the message
            self.pack_forget()

class ChatInterface(MD3Frame):
    """Enhanced chat interface with thumbnail support and modern styling"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.theme = get_theme()
        self.configure(bg=self.theme.colors['surface'])
        
        self.messages = []
        self.resend_message_callback: Optional[Callable] = None
        self.delete_message_callback: Optional[Callable] = None
        
        # Enhanced performance optimization settings
        self.max_visible_messages = 75  # Reduced for better performance
        self.message_cache = {}  # Cache for message widgets
        self.lazy_load_threshold = 30  # Start lazy loading earlier
        
        # Virtual scrolling support with improved settings
        self.virtual_scrolling_enabled = True
        self.viewport_start = 0
        self.viewport_end = 30
        self.viewport_buffer = 10  # Buffer for smooth scrolling
        
        # Performance monitoring
        self.render_times = []
        self.last_render_time = 0
        
        # Message pooling for better memory management
        self.message_pool = []
        self.max_pool_size = 20
        
        # Batch rendering support
        self.pending_messages = []
        self.batch_render_timer = None
        self.batch_render_delay = 50  # ms
        
        # Create scrollable chat area
        self.create_chat_area()
    
    def create_chat_area(self):
        """Create the scrollable chat area"""
        # Create canvas and scrollbar for smooth scrolling
        self.canvas = tk.Canvas(self, bg=self.theme.colors['surface'], 
                              highlightthickness=0, borderwidth=0)
        
        # Custom scrollbar
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, 
                                    command=self.canvas.yview,
                                    bg=self.theme.colors['surface'],
                                    troughcolor=self.theme.colors['surface'],
                                    activebackground=self.theme.colors['outline_variant'],
                                    width=8, borderwidth=0, highlightthickness=0)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Scrollable frame
        self.scrollable_frame = MD3Frame(self.canvas)
        self.scrollable_frame.configure(bg=self.theme.colors['surface'])
        
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Pack canvas and scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind events
        self.scrollable_frame.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.bind_mousewheel()
        
        # Hide scrollbar initially
        self.bind_scrollbar_events()
    
    def bind_scrollbar_events(self):
        """Bind events to show/hide scrollbar on hover"""
        def on_enter(event):
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def on_leave(event):
            self.after(1000, lambda: self.scrollbar.pack_forget())
        
        self.bind('<Enter>', on_enter)
        self.bind('<Leave>', on_leave)
        self.canvas.bind('<Enter>', on_enter)
        self.canvas.bind('<Leave>', on_leave)
    
    def bind_mousewheel(self):
        """Bind mousewheel scrolling"""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind("<MouseWheel>", _on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
    
    def _on_frame_configure(self, event):
        """Handle frame resize"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Handle canvas resize"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
    
    def add_message(self, sender: str, message: str, is_user: bool = False, 
                   screenshot_id: Optional[str] = None, tokens: int = 0):
        """Add a new message to the chat interface with enhanced performance optimization"""
        timestamp = datetime.now()
        
        # Performance optimization: batch rendering for better responsiveness
        message_data = {
            'sender': sender,
            'message': message,
            'timestamp': timestamp,
            'screenshot_id': screenshot_id,
            'is_user': is_user,
            'tokens': tokens
        }
        
        # Add to pending messages for batch processing
        self.pending_messages.append(message_data)
        
        # Schedule batch render if not already scheduled
        if self.batch_render_timer is None:
            self.batch_render_timer = self.after(self.batch_render_delay, self._process_pending_messages)
        
        # Return placeholder for immediate feedback
        return None
    
    def _process_pending_messages(self):
        """Process pending messages in batch for better performance"""
        if not self.pending_messages:
            self.batch_render_timer = None
            return
        
        render_start = time.time()
        
        # Performance optimization: limit visible messages before adding new ones
        if len(self.messages) >= self.max_visible_messages:
            self._cleanup_old_messages()
        
        # Process messages in batch
        new_widgets = []
        for message_data in self.pending_messages:
            # Try to reuse widget from pool
            message_widget = self._get_pooled_message_widget()
            
            if message_widget is None:
                # Create new widget
                message_widget = ChatMessage(self.scrollable_frame, **message_data)
            else:
                # Reconfigure existing widget
                message_widget.configure_message(**message_data)
            
            message_widget.pack(fill=tk.X, pady=2)
            new_widgets.append(message_widget)
            
            # Store message reference
            self.messages.append(message_widget)
            
            # Cache message data for potential recreation
            message_id = len(self.messages) - 1
            self.message_cache[message_id] = message_data
        
        # Clear pending messages
        self.pending_messages.clear()
        self.batch_render_timer = None
        
        # Record render time for performance monitoring
        render_time = time.time() - render_start
        self.render_times.append(render_time)
        if len(self.render_times) > 50:
            self.render_times.pop(0)
        
        # Optimized scrolling - use after_idle for better performance
        self.after_idle(self._scroll_to_bottom)
        
        return new_widgets
    
    def _get_pooled_message_widget(self):
        """Get a reusable message widget from the pool"""
        if self.message_pool:
            return self.message_pool.pop()
        return None
    
    def _return_to_pool(self, widget):
        """Return a message widget to the pool for reuse"""
        if len(self.message_pool) < self.max_pool_size:
            # Reset widget state
            widget.pack_forget()
            self.message_pool.append(widget)
        else:
            # Pool is full, destroy widget
            widget.destroy()
    
    def _cleanup_old_messages(self):
        """Remove old message widgets to maintain performance with enhanced optimization"""
        if len(self.messages) < self.max_visible_messages:
            return
        
        # Remove oldest 25% of messages from display for better performance
        cleanup_count = max(1, len(self.messages) // 4)
        
        for i in range(cleanup_count):
            if self.messages:
                old_message = self.messages.pop(0)
                
                # Try to return to pool for reuse
                self._return_to_pool(old_message)
        
        # Clean up corresponding cache entries
        keys_to_remove = [k for k in self.message_cache.keys() if k < cleanup_count]
        for key in keys_to_remove:
            self.message_cache.pop(key, None)
        
        # Renumber remaining cache entries
        new_cache = {}
        for old_key, value in self.message_cache.items():
            new_key = old_key - cleanup_count
            if new_key >= 0:
                new_cache[new_key] = value
        self.message_cache = new_cache
        
        # Force garbage collection after cleanup (less frequently)
        if len(self.messages) % 20 == 0:
            import gc
            gc.collect()
    
    def get_average_render_time(self) -> float:
        """Get average render time for performance monitoring"""
        if not self.render_times:
            return 0.0
        return sum(self.render_times) / len(self.render_times)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for the chat interface"""
        return {
            'message_count': len(self.messages),
            'cached_messages': len(self.message_cache),
            'pooled_widgets': len(self.message_pool),
            'pending_messages': len(self.pending_messages),
            'average_render_time': self.get_average_render_time(),
            'virtual_scrolling_enabled': self.virtual_scrolling_enabled,
            'viewport_range': (self.viewport_start, self.viewport_end)
        }
    
    def _scroll_to_bottom(self):
        """Scroll to the bottom of the chat"""
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)
    
    def clear_messages(self):
        """Clear all messages from the chat"""
        for message in self.messages:
            message.destroy()
        self.messages.clear()
    
    def set_resend_callback(self, callback: Callable):
        """Set callback for message resend functionality"""
        self.resend_message_callback = callback
    
    def set_delete_callback(self, callback: Callable):
        """Set callback for message delete functionality"""
        self.delete_message_callback = callback