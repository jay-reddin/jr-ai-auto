"""
Material Design 3 theme system for JR AI Control
Implements MD3 color schemes, typography, and component styling
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any

# Material Design 3 Color Schemes
MD3_DARK_THEME = {
    'primary': '#BB86FC',
    'on_primary': '#000000',
    'primary_container': '#3700B3',
    'on_primary_container': '#FFFFFF',
    
    'secondary': '#03DAC6',
    'on_secondary': '#000000',
    'secondary_container': '#018786',
    'on_secondary_container': '#FFFFFF',
    
    'tertiary': '#CF6679',
    'on_tertiary': '#000000',
    'tertiary_container': '#B00020',
    'on_tertiary_container': '#FFFFFF',
    
    'error': '#CF6679',
    'on_error': '#000000',
    'error_container': '#B00020',
    'on_error_container': '#FFFFFF',
    
    'background': '#121212',
    'on_background': '#FFFFFF',
    'surface': '#1E1E1E',
    'on_surface': '#FFFFFF',
    'surface_variant': '#2C2C2C',
    'on_surface_variant': '#E0E0E0',
    
    'outline': '#737373',
    'outline_variant': '#404040',
    'shadow': '#000000',
    'scrim': '#000000',
    
    'inverse_surface': '#FFFFFF',
    'inverse_on_surface': '#000000',
    'inverse_primary': '#6200EE'
}

MD3_LIGHT_THEME = {
    'primary': '#6200EE',
    'on_primary': '#FFFFFF',
    'primary_container': '#BB86FC',
    'on_primary_container': '#000000',
    
    'secondary': '#018786',
    'on_secondary': '#FFFFFF',
    'secondary_container': '#03DAC6',
    'on_secondary_container': '#000000',
    
    'tertiary': '#B00020',
    'on_tertiary': '#FFFFFF',
    'tertiary_container': '#CF6679',
    'on_tertiary_container': '#000000',
    
    'error': '#B00020',
    'on_error': '#FFFFFF',
    'error_container': '#CF6679',
    'on_error_container': '#000000',
    
    'background': '#FFFFFF',
    'on_background': '#000000',
    'surface': '#F5F5F5',
    'on_surface': '#000000',
    'surface_variant': '#E0E0E0',
    'on_surface_variant': '#404040',
    
    'outline': '#737373',
    'outline_variant': '#C0C0C0',
    'shadow': '#000000',
    'scrim': '#000000',
    
    'inverse_surface': '#121212',
    'inverse_on_surface': '#FFFFFF',
    'inverse_primary': '#BB86FC'
}

# Material Design 3 Typography Scale
MD3_TYPOGRAPHY = {
    'display_large': ('Segoe UI', 57, 'normal'),
    'display_medium': ('Segoe UI', 45, 'normal'),
    'display_small': ('Segoe UI', 36, 'normal'),
    
    'headline_large': ('Segoe UI', 32, 'normal'),
    'headline_medium': ('Segoe UI', 28, 'normal'),
    'headline_small': ('Segoe UI', 24, 'normal'),
    
    'title_large': ('Segoe UI', 22, 'bold'),
    'title_medium': ('Segoe UI', 16, 'bold'),
    'title_small': ('Segoe UI', 14, 'bold'),
    
    'body_large': ('Segoe UI', 16, 'normal'),
    'body_medium': ('Segoe UI', 14, 'normal'),
    'body_small': ('Segoe UI', 12, 'normal'),
    
    'label_large': ('Segoe UI', 14, 'bold'),
    'label_medium': ('Segoe UI', 12, 'bold'),
    'label_small': ('Segoe UI', 11, 'bold')
}

class MaterialDesign3Theme:
    def __init__(self, theme_mode: str = 'dark'):
        self.theme_mode = theme_mode
        self.colors = self._get_color_scheme()
        self.typography = MD3_TYPOGRAPHY
        self.style = None
        self.root_widget = None
        self.theme_change_callbacks = []
    
    def _get_color_scheme(self) -> Dict[str, str]:
        """Get the appropriate color scheme based on theme mode"""
        return MD3_DARK_THEME if self.theme_mode == 'dark' else MD3_LIGHT_THEME
    
    def switch_theme(self, new_mode: str):
        """Switch between dark and light themes with smooth transitions"""
        if new_mode in ['dark', 'light'] and new_mode != self.theme_mode:
            old_mode = self.theme_mode
            self.theme_mode = new_mode
            self.colors = self._get_color_scheme()
            
            # Re-apply theme to root widget if available
            if self.root_widget:
                self.apply_theme(self.root_widget)
            
            # Notify all registered callbacks about theme change
            for callback in self.theme_change_callbacks:
                try:
                    callback(old_mode, new_mode, self.colors)
                except Exception as e:
                    print(f"Error in theme change callback: {e}")
    
    def register_theme_change_callback(self, callback):
        """Register a callback to be called when theme changes"""
        if callback not in self.theme_change_callbacks:
            self.theme_change_callbacks.append(callback)
    
    def unregister_theme_change_callback(self, callback):
        """Unregister a theme change callback"""
        if callback in self.theme_change_callbacks:
            self.theme_change_callbacks.remove(callback)
    
    def apply_theme(self, root_widget: tk.Tk):
        """Apply Material Design 3 theme to the application"""
        # Store reference to root widget for theme switching
        self.root_widget = root_widget
        
        # Configure root window with smooth transition
        self._apply_smooth_background_change(root_widget, self.colors['background'])
        
        # Create and configure ttk styles
        if self.style is None:
            self.style = ttk.Style()
            self.style.theme_use('clam')
        
        # Configure all component styles
        self._configure_button_styles()
        self._configure_label_styles()
        self._configure_entry_styles()
        self._configure_frame_styles()
        self._configure_combobox_styles()
        self._configure_scrollbar_styles()
        self._configure_notebook_styles()
    
    def _apply_smooth_background_change(self, widget, new_color):
        """Apply background color change with smooth transition effect"""
        try:
            # For now, apply directly - can be enhanced with animation later
            widget.configure(bg=new_color)
        except tk.TclError:
            # Some widgets might not support bg configuration
            pass
    
    def _configure_button_styles(self):
        """Configure Material Design 3 button styles"""
        # Primary button (filled)
        self.style.configure('MD3.Primary.TButton',
                           background=self.colors['primary'],
                           foreground=self.colors['on_primary'],
                           font=self.typography['label_large'],
                           borderwidth=0,
                           focuscolor='none',
                           padding=(16, 8))
        
        self.style.map('MD3.Primary.TButton',
                      background=[('active', self.colors['primary_container']),
                                ('pressed', self.colors['primary_container'])])
        
        # Secondary button (outlined)
        self.style.configure('MD3.Secondary.TButton',
                           background=self.colors['surface'],
                           foreground=self.colors['primary'],
                           font=self.typography['label_large'],
                           borderwidth=1,
                           relief='solid',
                           focuscolor='none',
                           padding=(16, 8))
        
        self.style.map('MD3.Secondary.TButton',
                      background=[('active', self.colors['surface_variant']),
                                ('pressed', self.colors['surface_variant'])])
        
        # Tertiary button (text)
        self.style.configure('MD3.Tertiary.TButton',
                           background=self.colors['surface'],
                           foreground=self.colors['primary'],
                           font=self.typography['label_large'],
                           borderwidth=0,
                           focuscolor='none',
                           padding=(12, 8))
        
        self.style.map('MD3.Tertiary.TButton',
                      background=[('active', self.colors['surface_variant']),
                                ('pressed', self.colors['surface_variant'])])
    
    def _configure_label_styles(self):
        """Configure Material Design 3 label styles"""
        # Display styles
        self.style.configure('MD3.Display.Large.TLabel',
                           background=self.colors['surface'],
                           foreground=self.colors['on_surface'],
                           font=self.typography['display_large'])
        
        # Headline styles
        self.style.configure('MD3.Headline.Large.TLabel',
                           background=self.colors['surface'],
                           foreground=self.colors['on_surface'],
                           font=self.typography['headline_large'])
        
        self.style.configure('MD3.Headline.Medium.TLabel',
                           background=self.colors['surface'],
                           foreground=self.colors['on_surface'],
                           font=self.typography['headline_medium'])
        
        self.style.configure('MD3.Headline.Small.TLabel',
                           background=self.colors['surface'],
                           foreground=self.colors['on_surface'],
                           font=self.typography['headline_small'])
        
        # Title styles
        self.style.configure('MD3.Title.Large.TLabel',
                           background=self.colors['surface'],
                           foreground=self.colors['on_surface'],
                           font=self.typography['title_large'])
        
        self.style.configure('MD3.Title.Medium.TLabel',
                           background=self.colors['surface'],
                           foreground=self.colors['on_surface'],
                           font=self.typography['title_medium'])
        
        self.style.configure('MD3.Title.Small.TLabel',
                           background=self.colors['surface'],
                           foreground=self.colors['on_surface'],
                           font=self.typography['title_small'])
        
        # Body styles
        self.style.configure('MD3.Body.Large.TLabel',
                           background=self.colors['surface'],
                           foreground=self.colors['on_surface'],
                           font=self.typography['body_large'])
        
        self.style.configure('MD3.Body.Medium.TLabel',
                           background=self.colors['surface'],
                           foreground=self.colors['on_surface'],
                           font=self.typography['body_medium'])
        
        self.style.configure('MD3.Body.Small.TLabel',
                           background=self.colors['surface'],
                           foreground=self.colors['on_surface'],
                           font=self.typography['body_small'])
    
    def _configure_entry_styles(self):
        """Configure Material Design 3 entry styles"""
        self.style.configure('MD3.TEntry',
                           fieldbackground=self.colors['surface_variant'],
                           foreground=self.colors['on_surface_variant'],
                           bordercolor=self.colors['outline'],
                           lightcolor=self.colors['outline'],
                           darkcolor=self.colors['outline'],
                           borderwidth=1,
                           insertcolor=self.colors['on_surface_variant'])
        
        self.style.map('MD3.TEntry',
                      fieldbackground=[('focus', self.colors['surface']),
                                     ('active', self.colors['surface'])],
                      bordercolor=[('focus', self.colors['primary']),
                                 ('active', self.colors['primary'])])
    
    def _configure_frame_styles(self):
        """Configure Material Design 3 frame styles"""
        self.style.configure('MD3.TFrame',
                           background=self.colors['surface'],
                           borderwidth=0)
        
        self.style.configure('MD3.Card.TFrame',
                           background=self.colors['surface_variant'],
                           borderwidth=1,
                           relief='solid')
    
    def _configure_combobox_styles(self):
        """Configure Material Design 3 combobox styles"""
        self.style.configure('MD3.TCombobox',
                           fieldbackground=self.colors['surface_variant'],
                           foreground=self.colors['on_surface_variant'],
                           bordercolor=self.colors['outline'],
                           lightcolor=self.colors['outline'],
                           darkcolor=self.colors['outline'],
                           borderwidth=1,
                           arrowcolor=self.colors['on_surface_variant'])
        
        self.style.map('MD3.TCombobox',
                      fieldbackground=[('focus', self.colors['surface']),
                                     ('active', self.colors['surface'])],
                      bordercolor=[('focus', self.colors['primary']),
                                 ('active', self.colors['primary'])])
    
    def _configure_scrollbar_styles(self):
        """Configure Material Design 3 scrollbar styles (hidden by default)"""
        # Configure vertical scrollbar
        self.style.configure('MD3.Vertical.TScrollbar',
                           background=self.colors['surface_variant'],
                           troughcolor=self.colors['surface'],
                           bordercolor=self.colors['outline_variant'],
                           arrowcolor=self.colors['on_surface_variant'],
                           darkcolor=self.colors['surface_variant'],
                           lightcolor=self.colors['surface_variant'])
        
        # Configure horizontal scrollbar
        self.style.configure('MD3.Horizontal.TScrollbar',
                           background=self.colors['surface_variant'],
                           troughcolor=self.colors['surface'],
                           bordercolor=self.colors['outline_variant'],
                           arrowcolor=self.colors['on_surface_variant'],
                           darkcolor=self.colors['surface_variant'],
                           lightcolor=self.colors['surface_variant'])
    
    def _configure_notebook_styles(self):
        """Configure Material Design 3 notebook (tab) styles"""
        self.style.configure('MD3.TNotebook',
                           background=self.colors['surface'],
                           borderwidth=0,
                           tabmargins=[0, 0, 0, 0])
        
        self.style.configure('MD3.TNotebook.Tab',
                           background=self.colors['surface_variant'],
                           foreground=self.colors['on_surface_variant'],
                           padding=[16, 8],
                           font=self.typography['label_large'])
        
        self.style.map('MD3.TNotebook.Tab',
                      background=[('selected', self.colors['primary_container']),
                                ('active', self.colors['surface'])],
                      foreground=[('selected', self.colors['on_primary_container']),
                                ('active', self.colors['on_surface'])])
    
    def get_color(self, color_name: str) -> str:
        """Get a color from the current theme"""
        return self.colors.get(color_name, '#000000')
    
    def get_font(self, typography_name: str) -> tuple:
        """Get a font from the typography scale"""
        return self.typography.get(typography_name, ('Segoe UI', 12, 'normal'))

# Global theme instance
_md3_theme = None

def get_theme(theme_mode: str = 'dark') -> MaterialDesign3Theme:
    """Get the global Material Design 3 theme instance"""
    global _md3_theme
    if _md3_theme is None or _md3_theme.theme_mode != theme_mode:
        _md3_theme = MaterialDesign3Theme(theme_mode)
    return _md3_theme

def apply_md3_theme(root_widget: tk.Tk, theme_mode: str = 'dark'):
    """Apply Material Design 3 theme to the application"""
    theme = get_theme(theme_mode)
    theme.apply_theme(root_widget)
    return theme

def switch_theme(new_mode: str):
    """Switch the global theme mode with smooth transitions"""
    global _md3_theme
    if _md3_theme:
        _md3_theme.switch_theme(new_mode)
    return _md3_theme

def register_global_theme_callback(callback):
    """Register a callback for global theme changes"""
    global _md3_theme
    if _md3_theme:
        _md3_theme.register_theme_change_callback(callback)

def create_smooth_theme_switcher(parent_widget, initial_mode='dark'):
    """Create a theme switcher widget with smooth transitions"""
    theme = get_theme(initial_mode)
    
    def toggle_theme():
        new_mode = 'light' if theme.theme_mode == 'dark' else 'dark'
        switch_theme(new_mode)
        # Update button text
        if hasattr(toggle_theme, 'button'):
            toggle_theme.button.config(text=f"🌙" if new_mode == 'dark' else "☀️")
    
    # Create theme toggle button
    button_config = create_md3_widget_config('Button', theme)
    button = tk.Button(parent_widget, 
                      text="🌙" if initial_mode == 'dark' else "☀️",
                      command=toggle_theme,
                      **button_config)
    
    # Store button reference for updates
    toggle_theme.button = button
    
    return button

def create_md3_widget_config(widget_type: str, theme: MaterialDesign3Theme = None) -> Dict[str, Any]:
    """Create Material Design 3 configuration for standard tkinter widgets"""
    if theme is None:
        theme = get_theme()
    
    configs = {
        'Frame': {
            'bg': theme.colors['surface'],
            'highlightthickness': 0
        },
        'Label': {
            'bg': theme.colors['surface'],
            'fg': theme.colors['on_surface'],
            'font': theme.typography['body_medium']
        },
        'Button': {
            'bg': theme.colors['primary'],
            'fg': theme.colors['on_primary'],
            'font': theme.typography['label_large'],
            'borderwidth': 0,
            'highlightthickness': 0,
            'activebackground': theme.colors['primary_container'],
            'activeforeground': theme.colors['on_primary_container'],
            'relief': 'flat',
            'cursor': 'hand2'
        },
        'SecondaryButton': {
            'bg': theme.colors['surface'],
            'fg': theme.colors['primary'],
            'font': theme.typography['label_large'],
            'borderwidth': 1,
            'highlightthickness': 0,
            'activebackground': theme.colors['surface_variant'],
            'activeforeground': theme.colors['primary'],
            'relief': 'solid',
            'cursor': 'hand2'
        },
        'Entry': {
            'bg': theme.colors['surface_variant'],
            'fg': theme.colors['on_surface_variant'],
            'font': theme.typography['body_large'],
            'borderwidth': 1,
            'highlightthickness': 1,
            'highlightcolor': theme.colors['primary'],
            'insertbackground': theme.colors['on_surface_variant'],
            'relief': 'solid'
        },
        'Text': {
            'bg': theme.colors['surface_variant'],
            'fg': theme.colors['on_surface_variant'],
            'font': theme.typography['body_medium'],
            'borderwidth': 1,
            'highlightthickness': 1,
            'highlightcolor': theme.colors['primary'],
            'insertbackground': theme.colors['on_surface_variant'],
            'selectbackground': theme.colors['primary_container'],
            'selectforeground': theme.colors['on_primary_container'],
            'relief': 'solid'
        },
        'Listbox': {
            'bg': theme.colors['surface_variant'],
            'fg': theme.colors['on_surface_variant'],
            'font': theme.typography['body_medium'],
            'borderwidth': 1,
            'highlightthickness': 1,
            'highlightcolor': theme.colors['primary'],
            'selectbackground': theme.colors['primary_container'],
            'selectforeground': theme.colors['on_primary_container'],
            'relief': 'solid'
        },
        'Canvas': {
            'bg': theme.colors['surface'],
            'highlightthickness': 0,
            'borderwidth': 0
        }
    }
    
    return configs.get(widget_type, {})

def apply_md3_to_widget(widget, widget_type: str, theme: MaterialDesign3Theme = None):
    """Apply Material Design 3 styling to an existing widget"""
    config = create_md3_widget_config(widget_type, theme)
    try:
        widget.configure(**config)
    except tk.TclError as e:
        # Some configuration options might not be supported by all widgets
        print(f"Warning: Could not apply some MD3 styles to {widget_type}: {e}")

def create_md3_elevation_effect(widget, elevation_level: int = 1):
    """Create Material Design 3 elevation effect for widgets"""
    if elevation_level <= 0:
        return
    
    # Simple shadow effect using frames
    shadow_color = get_theme().colors['shadow']
    
    # Create shadow frame
    shadow_frame = tk.Frame(widget.master, bg=shadow_color, height=elevation_level, width=elevation_level)
    
    # Position shadow slightly offset
    widget.bind('<Map>', lambda e: shadow_frame.place(
        x=widget.winfo_x() + elevation_level,
        y=widget.winfo_y() + elevation_level,
        width=widget.winfo_width(),
        height=widget.winfo_height()
    ))
    
    return shadow_frame