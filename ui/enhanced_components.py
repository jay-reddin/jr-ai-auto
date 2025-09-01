"""
Enhanced UI components with Material Design 3 styling
Provides custom widgets with MD3 design principles
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Dict, Any
from ui.material_design import get_theme, create_md3_widget_config, apply_md3_to_widget

class MD3ScrolledText(tk.Frame):
    """Material Design 3 styled scrolled text widget with hidden scrollbars"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        
        self.theme = get_theme()
        
        # Configure frame
        self.configure(bg=self.theme.colors['surface'])
        
        # Create text widget
        text_config = create_md3_widget_config('Text', self.theme)
        text_config.update(kwargs)
        
        self.text_widget = tk.Text(self, **text_config)
        
        # Create custom scrollbar (hidden by default)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=self.scrollbar.set)
        
        # Style scrollbar to be minimal
        self.scrollbar.configure(
            bg=self.theme.colors['surface'],
            troughcolor=self.theme.colors['surface'],
            activebackground=self.theme.colors['outline_variant'],
            width=8,
            borderwidth=0,
            highlightthickness=0
        )
        
        # Pack widgets
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind events for scrollbar visibility
        self.bind_scrollbar_events()
    
    def bind_scrollbar_events(self):
        """Bind events to show/hide scrollbar on hover"""
        def on_enter(event):
            try:
                if self.scrollbar.winfo_exists():
                    self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            except tk.TclError:
                pass
        
        def on_leave(event):
            try:
                # Only hide if not actively scrolling
                if (self.scrollbar.winfo_exists() and 
                    not hasattr(self, '_scrolling')):
                    self.scrollbar.pack_forget()
            except tk.TclError:
                pass
        
        def on_scroll_start(event):
            self._scrolling = True
        
        def on_scroll_end(event):
            self._scrolling = False
            try:
                self.after(1000, lambda: self.scrollbar.pack_forget() 
                          if (not hasattr(self, '_scrolling') or 
                              not self._scrolling) else None)
            except tk.TclError:
                pass
        
        try:
            self.bind('<Enter>', on_enter)
            self.bind('<Leave>', on_leave)
            self.text_widget.bind('<Enter>', on_enter)
            self.text_widget.bind('<Leave>', on_leave)
            self.scrollbar.bind('<Button-1>', on_scroll_start)
            self.scrollbar.bind('<ButtonRelease-1>', on_scroll_end)
        except tk.TclError:
            pass
    
    def insert(self, index, text, *args):
        """Insert text into the text widget"""
        return self.text_widget.insert(index, text, *args)
    
    def delete(self, start, end=None):
        """Delete text from the text widget"""
        return self.text_widget.delete(start, end)
    
    def get(self, start, end=None):
        """Get text from the text widget"""
        return self.text_widget.get(start, end)
    
    def config(self, **kwargs):
        """Configure the text widget"""
        if hasattr(self, 'text_widget'):
            return self.text_widget.config(**kwargs)
        else:
            return super().config(**kwargs)
    
    def configure(self, **kwargs):
        """Configure the text widget"""
        if hasattr(self, 'text_widget'):
            return self.text_widget.configure(**kwargs)
        else:
            return super().configure(**kwargs)
    
    def see(self, index):
        """Scroll to make index visible"""
        return self.text_widget.see(index)
    
    def tag_config(self, tagname, **kwargs):
        """Configure text tags"""
        return self.text_widget.tag_config(tagname, **kwargs)

class MD3Button(tk.Button):
    """Material Design 3 styled button with hover effects"""
    
    def __init__(self, parent, style='primary', **kwargs):
        self.theme = get_theme()
        self.button_style = style
        
        # Get appropriate configuration
        if style == 'primary':
            config = create_md3_widget_config('Button', self.theme)
        elif style == 'secondary':
            config = create_md3_widget_config('SecondaryButton', self.theme)
        else:
            config = create_md3_widget_config('Button', self.theme)
        
        config.update(kwargs)
        
        super().__init__(parent, **config)
        
        # Add hover effects
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)
    
    def _on_enter(self, event):
        """Handle mouse enter event"""
        if self.button_style == 'primary':
            self.configure(bg=self.theme.colors['primary_container'])
        else:
            self.configure(bg=self.theme.colors['surface_variant'])
    
    def _on_leave(self, event):
        """Handle mouse leave event"""
        if self.button_style == 'primary':
            self.configure(bg=self.theme.colors['primary'])
        else:
            self.configure(bg=self.theme.colors['surface'])
    
    def _on_press(self, event):
        """Handle button press event"""
        # Add slight visual feedback
        self.configure(relief='sunken')
    
    def _on_release(self, event):
        """Handle button release event"""
        self.configure(relief='flat')

class MD3Entry(tk.Entry):
    """Material Design 3 styled entry widget with focus effects"""
    
    def __init__(self, parent, **kwargs):
        self.theme = get_theme()
        
        config = create_md3_widget_config('Entry', self.theme)
        config.update(kwargs)
        
        super().__init__(parent, **config)
        
        # Add focus effects
        self.bind('<FocusIn>', self._on_focus_in)
        self.bind('<FocusOut>', self._on_focus_out)
    
    def _on_focus_in(self, event):
        """Handle focus in event"""
        self.configure(
            highlightcolor=self.theme.colors['primary'],
            highlightbackground=self.theme.colors['primary']
        )
    
    def _on_focus_out(self, event):
        """Handle focus out event"""
        self.configure(
            highlightcolor=self.theme.colors['outline'],
            highlightbackground=self.theme.colors['outline']
        )

class MD3Frame(tk.Frame):
    """Material Design 3 styled frame with elevation support"""
    
    def __init__(self, parent, elevation=0, **kwargs):
        self.theme = get_theme()
        
        config = create_md3_widget_config('Frame', self.theme)
        config.update(kwargs)
        
        super().__init__(parent, **config)
        
        if elevation > 0:
            self._create_elevation_effect(elevation)
    
    def _create_elevation_effect(self, level):
        """Create elevation shadow effect"""
        # Simple implementation - can be enhanced with gradients
        shadow_color = self.theme.colors['shadow']
        
        # Create shadow frames
        for i in range(level):
            shadow = tk.Frame(self.master, bg=shadow_color, height=1)
            shadow.place(in_=self, x=i+1, y=i+1, relwidth=1.0, relheight=1.0)
            shadow.lower(self)

class MD3Card(MD3Frame):
    """Material Design 3 card component"""
    
    def __init__(self, parent, **kwargs):
        # Set default card styling
        card_config = {
            'bg': get_theme().colors['surface_variant'],
            'relief': 'flat',
            'borderwidth': 1,
            'highlightthickness': 0
        }
        card_config.update(kwargs)
        
        super().__init__(parent, elevation=1, **card_config)

class MD3StatusIndicator(tk.Frame):
    """Material Design 3 status indicator with color coding"""
    
    def __init__(self, parent, status='inactive', **kwargs):
        super().__init__(parent, **kwargs)
        
        self.theme = get_theme()
        self.configure(bg=self.theme.colors['surface'])
        
        # Create indicator dot
        self.indicator = tk.Label(self, text="●", font=('Segoe UI', 12))
        self.indicator.pack(side=tk.LEFT)
        
        # Create status label
        self.status_label = tk.Label(self, font=self.theme.typography['body_medium'])
        self.status_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Set initial status
        self.set_status(status)
    
    def set_status(self, status, text=None):
        """Set the status indicator color and text"""
        status_config = {
            'active': {
                'color': self.theme.colors['secondary'],
                'text': text or 'Connected'
            },
            'inactive': {
                'color': self.theme.colors['error'],
                'text': text or 'Not Connected'
            },
            'warning': {
                'color': self.theme.colors['tertiary'],
                'text': text or 'Warning'
            },
            'processing': {
                'color': self.theme.colors['primary'],
                'text': text or 'Processing'
            }
        }
        
        config = status_config.get(status, status_config['inactive'])
        
        self.indicator.configure(
            fg=config['color'],
            bg=self.theme.colors['surface']
        )
        
        self.status_label.configure(
            text=config['text'],
            fg=self.theme.colors['on_surface'],
            bg=self.theme.colors['surface']
        )

class MD3ProgressBar(tk.Frame):
    """Material Design 3 progress bar"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.theme = get_theme()
        self.configure(bg=self.theme.colors['surface'])
        
        # Create progress track
        self.track = tk.Frame(self, 
                             bg=self.theme.colors['outline_variant'],
                             height=4)
        self.track.pack(fill=tk.X, pady=2)
        
        # Create progress indicator
        self.indicator = tk.Frame(self.track,
                                 bg=self.theme.colors['primary'],
                                 height=4)
        
        self.progress = 0
    
    def set_progress(self, value):
        """Set progress value (0-100)"""
        self.progress = max(0, min(100, value))
        
        # Update indicator width
        if self.progress > 0:
            self.indicator.place(x=0, y=0, relwidth=self.progress/100, height=4)
        else:
            self.indicator.place_forget()

def create_md3_tooltip(widget, text):
    """Create a Material Design 3 styled tooltip for a widget"""
    def show_tooltip(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.configure(bg=get_theme().colors['inverse_surface'])
        
        label = tk.Label(tooltip, 
                        text=text,
                        bg=get_theme().colors['inverse_surface'],
                        fg=get_theme().colors['inverse_on_surface'],
                        font=get_theme().typography['body_small'],
                        padx=8,
                        pady=4)
        label.pack()
        
        # Position tooltip
        x = event.x_root + 10
        y = event.y_root + 10
        tooltip.geometry(f"+{x}+{y}")
        
        # Auto-hide after 3 seconds
        tooltip.after(3000, tooltip.destroy)
        
        # Store reference to destroy on leave
        widget.tooltip = tooltip
    
    def hide_tooltip(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            delattr(widget, 'tooltip')
    
    widget.bind('<Enter>', show_tooltip)
    widget.bind('<Leave>', hide_tooltip)

def animate_widget_transition(widget, property_name, start_value, end_value, duration=300, steps=20):
    """Animate a widget property transition"""
    step_size = (end_value - start_value) / steps
    step_duration = duration // steps
    
    def animate_step(current_step):
        if current_step <= steps:
            current_value = start_value + (step_size * current_step)
            try:
                widget.configure(**{property_name: current_value})
                widget.after(step_duration, lambda: animate_step(current_step + 1))
            except tk.TclError:
                # Animation interrupted or widget destroyed
                pass
    
    animate_step(0)