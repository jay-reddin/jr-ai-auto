"""
Theme Manager for Toga-based JR AI Control
Manages application themes and styling across all components
"""

import toga
from toga.style import Pack
from typing import Dict, Any, List, Callable


class ThemeManager:
    """
    Manages application themes and provides consistent styling
    """
    
    def __init__(self, initial_theme: str = "dark"):
        self.current_theme = initial_theme
        self.theme_callbacks: List[Callable] = []
        self.themes = self._initialize_themes()
    
    def _initialize_themes(self) -> Dict[str, Dict[str, Any]]:
        """Initialize theme configurations"""
        return {
            "dark": {
                "name": "Dark Theme",
                "colors": {
                    "background": "#1e1e1e",
                    "surface": "#2d2d2d",
                    "primary": "#4a9eff",
                    "secondary": "#6c757d",
                    "text_primary": "#ffffff",
                    "text_secondary": "#b0b0b0",
                    "accent": "#00d4aa",
                    "error": "#ff6b6b",
                    "warning": "#ffa726",
                    "success": "#4caf50",
                    "border": "#404040"
                },
                "fonts": {
                    "title": ("Segoe UI", 18, "bold"),
                    "heading": ("Segoe UI", 16, "bold"),
                    "body": ("Segoe UI", 14, "normal"),
                    "caption": ("Segoe UI", 12, "normal"),
                    "small": ("Segoe UI", 10, "normal")
                },
                "spacing": {
                    "xs": 2,
                    "sm": 5,
                    "md": 10,
                    "lg": 15,
                    "xl": 20
                }
            },
            "light": {
                "name": "Light Theme",
                "colors": {
                    "background": "#ffffff",
                    "surface": "#f5f5f5",
                    "primary": "#1976d2",
                    "secondary": "#757575",
                    "text_primary": "#212121",
                    "text_secondary": "#757575",
                    "accent": "#00acc1",
                    "error": "#d32f2f",
                    "warning": "#f57c00",
                    "success": "#388e3c",
                    "border": "#e0e0e0"
                },
                "fonts": {
                    "title": ("Segoe UI", 18, "bold"),
                    "heading": ("Segoe UI", 16, "bold"),
                    "body": ("Segoe UI", 14, "normal"),
                    "caption": ("Segoe UI", 12, "normal"),
                    "small": ("Segoe UI", 10, "normal")
                },
                "spacing": {
                    "xs": 2,
                    "sm": 5,
                    "md": 10,
                    "lg": 15,
                    "xl": 20
                }
            }
        }
    
    def get_current_theme(self) -> Dict[str, Any]:
        """Get the current theme configuration"""
        return self.themes.get(self.current_theme, self.themes["dark"])
    
    def get_color(self, color_key: str) -> str:
        """Get a color value from the current theme"""
        theme = self.get_current_theme()
        return theme["colors"].get(color_key, "#000000")
    
    def get_font(self, font_key: str) -> tuple:
        """Get a font specification from the current theme"""
        theme = self.get_current_theme()
        return theme["fonts"].get(font_key, ("Segoe UI", 14, "normal"))
    
    def get_spacing(self, spacing_key: str) -> int:
        """Get a spacing value from the current theme"""
        theme = self.get_current_theme()
        return theme["spacing"].get(spacing_key, 10)
    
    def switch_theme(self, theme_name: str):
        """Switch to a different theme"""
        if theme_name in self.themes:
            old_theme = self.current_theme
            self.current_theme = theme_name
            
            # Notify all registered callbacks
            self._notify_theme_change(old_theme, theme_name)
        else:
            print(f"Theme '{theme_name}' not found")
    
    def register_theme_callback(self, callback: Callable):
        """Register a callback to be notified of theme changes"""
        if callback not in self.theme_callbacks:
            self.theme_callbacks.append(callback)
    
    def unregister_theme_callback(self, callback: Callable):
        """Unregister a theme change callback"""
        if callback in self.theme_callbacks:
            self.theme_callbacks.remove(callback)
    
    def _notify_theme_change(self, old_theme: str, new_theme: str):
        """Notify all registered callbacks of theme change"""
        for callback in self.theme_callbacks:
            try:
                callback(old_theme, new_theme, self.get_current_theme())
            except Exception as e:
                print(f"Error in theme callback: {e}")
    
    def create_styled_pack(self, **kwargs) -> Pack:
        """Create a Pack style with theme-aware defaults"""
        theme = self.get_current_theme()
        
        # Apply theme defaults
        styled_kwargs = {
            "background_color": theme["colors"]["background"],
            "color": theme["colors"]["text_primary"],
            **kwargs
        }
        
        return Pack(**styled_kwargs)
    
    def apply_button_style(self, button: toga.Button, style_type: str = "primary"):
        """Apply theme-appropriate styling to a button"""
        try:
            theme = self.get_current_theme()
            
            if style_type == "primary":
                # Primary button styling would go here
                # Note: Toga's styling system is still evolving
                pass
            elif style_type == "secondary":
                # Secondary button styling would go here
                pass
            
        except Exception as e:
            print(f"Error applying button style: {e}")
    
    def apply_label_style(self, label: toga.Label, style_type: str = "body"):
        """Apply theme-appropriate styling to a label"""
        try:
            theme = self.get_current_theme()
            font_spec = theme["fonts"].get(style_type, theme["fonts"]["body"])
            
            # Apply font styling
            # Note: Toga's font styling is still being developed
            
        except Exception as e:
            print(f"Error applying label style: {e}")
    
    def apply_container_style(self, container: toga.Box, style_type: str = "default"):
        """Apply theme-appropriate styling to a container"""
        try:
            theme = self.get_current_theme()
            
            # Container styling would go here
            # This is a placeholder for when Toga supports more styling options
            
        except Exception as e:
            print(f"Error applying container style: {e}")
    
    def get_message_style(self, is_user: bool = False, is_system: bool = False) -> Dict[str, Any]:
        """Get styling configuration for chat messages"""
        theme = self.get_current_theme()
        
        if is_system:
            return {
                "background_color": theme["colors"]["surface"],
                "text_color": theme["colors"]["text_secondary"],
                "border_color": theme["colors"]["border"]
            }
        elif is_user:
            return {
                "background_color": theme["colors"]["primary"],
                "text_color": "#ffffff",
                "border_color": theme["colors"]["primary"]
            }
        else:
            return {
                "background_color": theme["colors"]["surface"],
                "text_color": theme["colors"]["text_primary"],
                "border_color": theme["colors"]["border"]
            }
    
    def get_input_style(self) -> Dict[str, Any]:
        """Get styling configuration for input fields"""
        theme = self.get_current_theme()
        
        return {
            "background_color": theme["colors"]["surface"],
            "text_color": theme["colors"]["text_primary"],
            "border_color": theme["colors"]["border"],
            "focus_color": theme["colors"]["primary"]
        }
    
    def get_available_themes(self) -> List[str]:
        """Get list of available theme names"""
        return list(self.themes.keys())
    
    def add_custom_theme(self, name: str, theme_config: Dict[str, Any]):
        """Add a custom theme configuration"""
        if self._validate_theme_config(theme_config):
            self.themes[name] = theme_config
        else:
            print(f"Invalid theme configuration for '{name}'")
    
    def _validate_theme_config(self, config: Dict[str, Any]) -> bool:
        """Validate a theme configuration"""
        required_keys = ["colors", "fonts", "spacing"]
        return all(key in config for key in required_keys)
    
    def export_theme(self, theme_name: str) -> Dict[str, Any]:
        """Export a theme configuration"""
        return self.themes.get(theme_name, {})
    
    def import_theme(self, theme_name: str, theme_config: Dict[str, Any]):
        """Import a theme configuration"""
        self.add_custom_theme(theme_name, theme_config)