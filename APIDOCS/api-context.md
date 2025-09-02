# Toga API Context Documentation

## Overview
Toga is a Python native, OS native, cross-platform GUI toolkit. This document provides a comprehensive context for understanding and using the Toga API based on the official documentation and examples.

## Installation

### Basic Installation
```bash
pip install toga
```

### Platform-Specific Backends
Toga requires platform-specific backends for different operating systems:

- **macOS**: `toga-cocoa` (Python 3.10+, macOS 11+)
- **Linux**: `toga-gtk` 
- **Windows**: `toga-winforms`
- **Android**: `toga-android`
- **iOS**: `toga-iOS`
- **Web**: `toga-web`
- **Terminal**: `toga-textual`
- **Testing**: `toga-dummy`

### Development Installation
```bash
# For development with specific backends
pip install -e "./core[dev]" -e ./dummy -e ./cocoa -e ./travertino  # macOS
pip install -e "./core[dev]" -e ./dummy -e ./gtk -e ./travertino    # Linux
pip install -e "./core[dev]" -e ./dummy -e ./winforms -e ./travertino  # Windows
```

## Core Architecture

### Three-Layer Architecture
1. **Interface Layer**: Public API (e.g., `toga.Button`)
2. **Implementation Layer**: Platform-specific implementation (e.g., `toga-gtk.widgets.Button`)
3. **Native Layer**: Native toolkit widget (e.g., `Gtk.Button`)

### Key Principles
- **Pythonic**: Uses snake_case, properties over getters/setters
- **Cross-platform**: Single codebase runs on multiple platforms
- **Native**: Uses platform-native widgets for authentic look and feel
- **Simple**: Minimal installation requirements, no C extensions needed

## Application Structure

### Basic App Template
```python
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class MyApp(toga.App):
    def startup(self):
        # Create main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # Create widgets
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        
        # Add content to main window
        self.main_window.content = main_box
        
        # Show the main window
        self.main_window.show()

def main():
    return MyApp("App Name", "com.example.app")

if __name__ == "__main__":
    main().main_loop()
```

### App Initialization Patterns
```python
# Basic app
app = toga.App("Simple App", "com.example.simple")
app.main_loop()

# App with startup content
def create_content(app):
    return toga.Box(children=[toga.Label("Hello!")])

app = toga.App("Simple App", "com.example.simple", startup=create_content)
app.main_loop()
```

## Core Widgets

### Input Widgets
- **TextInput**: Single-line text input
- **MultilineTextInput**: Multi-line text input
- **PasswordInput**: Password input field
- **NumberInput**: Numeric input field
- **Switch**: Toggle switch
- **Slider**: Value slider
- **Selection**: Dropdown selection

### Display Widgets
- **Label**: Text display
- **ImageView**: Image display
- **WebView**: Web content display
- **Canvas**: Custom drawing surface
- **ProgressBar**: Progress indication
- **ActivityIndicator**: Loading indicator

### Container Widgets
- **Box**: Layout container
- **ScrollContainer**: Scrollable container
- **SplitContainer**: Resizable split panes
- **OptionContainer**: Tabbed container

### Interactive Widgets
- **Button**: Clickable button
- **Table**: Data table
- **Tree**: Hierarchical tree view
- **DetailedList**: Rich list view

### Date/Time Widgets
- **DateInput**: Date picker
- **TimeInput**: Time picker

## Widget Usage Examples

### Button Widget
```python
import toga

def button_handler(widget):
    print("Button clicked!")

button = toga.Button(
    'Click Me',
    on_press=button_handler,
    style=Pack(width=200, height=50)
)

# Disabled button
disabled_button = toga.Button(
    'Disabled Button',
    enabled=False,
    style=Pack(width=200, height=50)
)
```

### TextInput Widget
```python
# Basic text input
text_input = toga.TextInput(
    placeholder="Enter text here...",
    style=Pack(flex=1)
)

# Read-only text input
readonly_input = toga.TextInput(
    value="Read-only content",
    readonly=True
)
```

### Table Widget
```python
table = toga.Table(
    headings=['Name', 'Age', 'City'],
    data=[
        ('Alice', 25, 'New York'),
        ('Bob', 30, 'San Francisco'),
        ('Charlie', 35, 'Chicago')
    ],
    style=Pack(flex=1)
)
```

### Tree Widget
```python
tree = toga.Tree(
    headings=["Name", "Age"],
    data={
        "Earth": {
           ("Arthur Dent", 42): None,
        },
        "Betelgeuse Five": {
           ("Ford Prefect", 37): None,
           ("Zaphod Beeblebrox", 47): None,
        },
    }
)
```

### Canvas Widget
```python
canvas = toga.Canvas(style=Pack(flex=1))

# Drawing operations
with canvas.fill(color="white") as context:
    context.arc(50, 50, 25)  # Draw circle

with canvas.stroke(color="black", width=2) as context:
    context.move_to(0, 0)
    context.line_to(100, 100)
```

### WebView Widget
```python
webview = toga.WebView()

# Load URL
webview.url = "https://beeware.org"

# Load URL asynchronously
await webview.load_url("https://beeware.org")

# Load HTML content
webview.set_content("https://example.com", "<html>...</html>")
```

### ProgressBar Widget
```python
# Determinate progress bar
progress = toga.ProgressBar(max=100, value=1)
progress.start()
progress.value = 50  # Update progress
progress.stop()

# Indeterminate progress bar
progress = toga.ProgressBar(max=None)
progress.start()  # Continuous animation
progress.stop()
```

### ActivityIndicator Widget
```python
indicator = toga.ActivityIndicator()
indicator.start()  # Start animation
indicator.stop()   # Stop animation
```

### Slider Widget
```python
def slider_changed(slider):
    print(f"Slider value: {slider.value}")

# Continuous slider
slider = toga.Slider(
    min=-5, 
    max=10, 
    value=7, 
    on_change=slider_changed
)

# Discrete slider
discrete_slider = toga.Slider(
    min=0, 
    max=7.5, 
    tick_count=6
)
```

## Layout and Styling

### Pack Layout System
```python
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

# Vertical layout
vertical_box = toga.Box(
    style=Pack(direction=COLUMN, padding=10)
)

# Horizontal layout
horizontal_box = toga.Box(
    style=Pack(direction=ROW, padding=5)
)

# Flexible sizing
flexible_widget = toga.TextInput(
    style=Pack(flex=1, padding=5)
)
```

### Common Style Properties
- **direction**: COLUMN, ROW
- **padding**: Spacing around widget
- **margin**: External spacing
- **flex**: Flexible sizing (0-1)
- **width/height**: Fixed dimensions
- **background_color**: Background color
- **color**: Text color

## Event Handling

### Event Handler Pattern
```python
def event_handler(widget, **kwargs):
    # Handle event
    print(f"Event from {widget}")

# Event handlers should include **kwargs for forward compatibility
widget.on_press = event_handler
```

### Common Events
- **on_press**: Button clicks
- **on_change**: Value changes (TextInput, Slider, Switch)
- **on_select**: Selection changes (Table, Tree)

## File Management

### Application Paths
```python
class MyApp(toga.App):
    def startup(self):
        # Access application paths
        app_path = self.paths.app          # Application directory
        config_path = self.paths.config    # User config directory
        data_path = self.paths.data        # User data directory
        cache_path = self.paths.cache      # Cache directory
        logs_path = self.paths.logs        # Logs directory
```

### File Operations
```python
from pathlib import Path

# Load configuration
def load_config(self):
    config_file = self.paths.config / "config.toml"
    if config_file.exists():
        content = config_file.read_text(encoding="utf-8")
    else:
        # Fallback to bundled config
        default_config = self.paths.app / "resources/default_config.toml"
        content = default_config.read_text(encoding="utf-8")
    return content

# Save configuration
def save_config(self, content):
    config_file = self.paths.config / "config.toml"
    config_file.write_text(content, encoding="utf-8")
```

## Hardware Integration

### Location Services
```python
class MyApp(toga.App):
    async def location_update(self, location, altitude, **kwargs):
        print(f"Location: {location}, Altitude: {altitude}m")

    def start_location_tracking(self):
        try:
            self.location.on_change = self.location_update
            self.location.start_tracking()
        except PermissionError:
            print("Location permission not granted")

    def stop_location_tracking(self):
        self.location.stop_tracking()
```

## Platform-Specific Features

### Android Integration
```python
from android.content import Intent
from android.net import Uri

def start_android_activity(self):
    intent = Intent(Intent.ACTION_DIAL)
    intent.setData(Uri.parse("tel:0123456789"))
    
    def activity_complete(result, data):
        print(f"Activity result: {result}")
    
    self.app._impl.start_activity(intent, on_complete=activity_complete)
```

## Document-Based Applications

### Document App Structure
```python
import toga

class ExampleDocument(toga.Document):
    description = "Example Document"
    extensions = ["mydoc", "mydocument"]

    def create(self):
        self.main_window = toga.DocumentMainWindow(
            doc=self,
            content=toga.MultilineTextInput(on_change=self.touch),
        )

    def read(self):
        with self.path.open() as f:
            self.main_window.content.value = f.read()

    def write(self):
        with self.path.open("w") as f:
            f.write(self.main_window.content.value)
```

## Testing and Development

### Using Dummy Backend
```bash
# Install dummy backend for testing
pip install toga-dummy

# Set environment variable
export TOGA_BACKEND=toga_dummy  # Linux/macOS
set TOGA_BACKEND=toga_dummy     # Windows
```

### Running Examples
```bash
# Install and run any example
pip install toga
python -m <example_name>

# Available examples include:
# - button, canvas, colors, dialogs, font
# - imageview, layout, progressbar, slider
# - table, textinput, tree, webview, etc.
```

### Development Setup
```bash
# Clone repository
git clone https://github.com/beeware/toga.git
cd toga

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install development dependencies
python -m pip install -e "./core[dev]" -e ./dummy -e ./cocoa -e ./travertino

# Install pre-commit hooks
pre-commit install
```

## Best Practices

### API Design Principles
1. **Pythonic**: Use snake_case, properties over methods
2. **Consistent**: Similar widgets have similar APIs
3. **Flexible**: Constructor arguments for all writable properties
4. **Forward-compatible**: Event handlers use **kwargs

### Error Handling
```python
try:
    # Toga operations
    widget.configure(**config)
except toga.TclError as e:
    print(f"Configuration error: {e}")
```

### Performance Considerations
- Use appropriate container widgets for layout
- Minimize widget creation in loops
- Use data sources for large datasets in tables/trees
- Implement proper cleanup in event handlers

## Common Patterns

### Temperature Converter Example
```python
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class TemperatureConverter(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # Create widgets
        self.fahrenheit_input = toga.TextInput(style=Pack(flex=1))
        self.celsius_input = toga.TextInput(style=Pack(flex=1))
        
        convert_button = toga.Button(
            'Convert',
            on_press=self.convert_temperature,
            style=Pack(padding=5)
        )
        
        # Layout
        main_box = toga.Box(
            children=[
                toga.Label('Fahrenheit:', style=Pack(padding=(0, 5))),
                self.fahrenheit_input,
                toga.Label('Celsius:', style=Pack(padding=(0, 5))),
                self.celsius_input,
                convert_button
            ],
            style=Pack(direction=COLUMN, padding=10)
        )
        
        self.main_window.content = main_box
        self.main_window.show()

    def convert_temperature(self, widget):
        try:
            fahrenheit = float(self.fahrenheit_input.value)
            celsius = (fahrenheit - 32) * 5 / 9
            self.celsius_input.value = str(celsius)
        except ValueError:
            self.celsius_input.value = 'Invalid input'
```

## Resources and References

### Official Documentation
- Main Repository: https://github.com/beeware/toga
- Documentation: https://toga.readthedocs.io/
- Examples: https://github.com/beeware/toga/tree/main/examples

### Quick Demo
```bash
# Install and run the official demo
python -m pip install toga-demo
toga-demo
```

### Platform Requirements

#### Linux Prerequisites
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install git build-essential pkg-config python3-dev libgirepository1.0-dev libcairo2-dev gir1.2-gtk-3.0

# Fedora
sudo dnf install git gcc make pkg-config python3-devel gobject-introspection-devel cairo-gobject-devel gtk3

# Arch/Manjaro
sudo pacman -Syu git base-devel pkgconf python3 gobject-introspection cairo gtk3
```

#### macOS Prerequisites
```bash
# Install via Homebrew
brew install enchant
```

#### Windows Prerequisites
- No additional system dependencies required
- WebView2 Runtime required for WebView widget

This documentation provides a comprehensive overview of the Toga API and its usage patterns. For the most up-to-date information, always refer to the official Toga documentation and examples.