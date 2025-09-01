# JR AI Control - Developer Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Development Setup](#development-setup)
5. [Code Standards](#code-standards)
6. [Testing Framework](#testing-framework)
7. [Build and Deployment](#build-and-deployment)
8. [API Documentation](#api-documentation)
9. [Extension Points](#extension-points)
10. [Contributing Guidelines](#contributing-guidelines)

## Architecture Overview

JR AI Control follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   UI Layer      │    │  Business Logic │    │   Data Layer    │
│                 │    │                 │    │                 │
│ - Material UI   │◄──►│ - Agent Manager │◄──►│ - Config Files  │
│ - Chat Interface│    │ - Voice System  │    │ - Screenshots   │
│ - Settings      │    │ - Token Tracker │    │ - Logs          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  External APIs  │
                    │                 │
                    │ - Google Gemini │
                    │ - Windows APIs  │
                    │ - PyAutoGUI     │
                    └─────────────────┘
```

### Key Design Principles
- **Modularity**: Each component has a single responsibility
- **Extensibility**: Easy to add new features and AI models
- **Maintainability**: Clean code with comprehensive documentation
- **Performance**: Efficient resource usage and responsive UI
- **Security**: Secure handling of API keys and user data

## Project Structure

```
JR_AI_Control/
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── config.json                 # User configuration
├── .env                       # Environment variables
├── 
├── ui/                        # User Interface Components
│   ├── __init__.py
│   ├── material_design.py     # MD3 theme system
│   ├── chat_interface.py      # Chat bubble interface
│   ├── settings_tabs.py       # Tabbed settings window
│   └── enhanced_components.py # Custom UI widgets
│
├── utils/                     # Core Utilities
│   ├── __init__.py
│   ├── agent.py              # AI agent creation and management
│   ├── config_manager.py     # Configuration handling
│   ├── constants.py          # Application constants
│   ├── tools.py              # Automation tools (screenshots, etc.)
│   ├── token_tracker.py      # Token usage tracking
│   ├── notifications.py      # System notifications
│   ├── screenshot_manager.py # Screenshot and thumbnail handling
│   └── performance_monitor.py # Performance optimization
│
├── voice/                     # Voice Interaction System
│   ├── __init__.py
│   └── voice_manager.py      # Speech recognition and TTS
│
├── docs/                      # Documentation
│   ├── USER_MANUAL.md
│   ├── VOICE_INTERACTION_GUIDE.md
│   ├── SETTINGS_CONFIGURATION_GUIDE.md
│   ├── TROUBLESHOOTING.md
│   └── DEVELOPER_DOCUMENTATION.md
│
├── tests/                     # Test Suite
│   ├── __init__.py
│   ├── test_agent.py
│   ├── test_voice.py
│   ├── test_ui.py
│   └── test_integration.py
│
└── screenshots/               # Screenshot Storage
    ├── thumbnails/           # Generated thumbnails
    └── metadata.json         # Screenshot metadata
```

## Core Components

### 1. Main Application (main.py)

The entry point that initializes all components and starts the GUI.

```python
class JRAIControlApp:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.voice_manager = VoiceManager()
        self.token_tracker = TokenTracker()
        self.agent = None
        
    def initialize_ui(self):
        # Initialize Material Design 3 interface
        
    def create_agent(self, model_name):
        # Create AI agent with specified model
        
    def run(self):
        # Start the application main loop
```

### 2. Agent Management (utils/agent.py)

Handles AI model initialization and agent creation.

```python
def create_clevrr_agent(model, prompt):
    """
    Create a LangChain agent with the specified model and tools.
    
    Args:
        model: The AI model instance (e.g., ChatGoogleGenerativeAI)
        prompt: The system prompt for the agent
        
    Returns:
        AgentExecutor: Configured agent ready for use
    """
    tools = [get_screen_info, ...]
    agent = create_react_agent(model, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
```

### 3. Voice System (voice/voice_manager.py)

Manages speech recognition and text-to-speech functionality.

```python
class VoiceManager:
    def __init__(self):
        self.stt_engine = speech_recognition.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.is_listening = False
        
    def start_listening(self, callback):
        """Start continuous speech recognition"""
        
    def speak_text(self, text):
        """Convert text to speech and play"""
        
    def configure_voice(self, rate, volume, voice_id):
        """Configure TTS settings"""
```

### 4. UI Components (ui/)

Material Design 3 interface components with theme support.

```python
class MaterialDesign3Theme:
    def __init__(self, theme_mode='dark'):
        self.theme_mode = theme_mode
        self.colors = self.load_color_scheme()
        
    def apply_theme(self, root):
        """Apply MD3 styling to all widgets"""
        
    def switch_theme(self, new_mode):
        """Dynamically switch between themes"""
```

### 5. Configuration Management (utils/config_manager.py)

Handles loading, saving, and validating configuration settings.

```python
class ConfigManager:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file with validation"""
        
    def save_config(self):
        """Save current configuration to file"""
        
    def get(self, key, default=None):
        """Get configuration value with default"""
        
    def set(self, key, value):
        """Set configuration value with validation"""
```

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git for version control
- Virtual environment tool (venv or conda)
- Code editor with Python support (VS Code recommended)

### Environment Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-repo/jr-ai-control.git
   cd jr-ai-control
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Environment Variables**
   ```bash
   copy .env.example .env
   # Edit .env with your API keys and settings
   ```

5. **Run Tests**
   ```bash
   python -m pytest tests/
   ```

6. **Start Development Server**
   ```bash
   python main.py --debug
   ```

### Development Dependencies

```txt
# requirements-dev.txt
pytest>=7.0.0
pytest-cov>=4.0.0
black>=22.0.0
flake8>=5.0.0
mypy>=0.991
pre-commit>=2.20.0
sphinx>=5.0.0
```

## Code Standards

### Python Style Guide
- Follow PEP 8 style guidelines
- Use Black for code formatting
- Maximum line length: 88 characters
- Use type hints for all function parameters and return values

### Naming Conventions
- **Classes**: PascalCase (e.g., `VoiceManager`)
- **Functions/Methods**: snake_case (e.g., `create_agent`)
- **Variables**: snake_case (e.g., `api_key`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_MODEL`)
- **Private methods**: Leading underscore (e.g., `_internal_method`)

### Documentation Standards
- All public functions must have docstrings
- Use Google-style docstrings
- Include type information in docstrings
- Document complex algorithms and business logic

```python
def create_agent(model: str, config: Dict[str, Any]) -> AgentExecutor:
    """
    Create a new AI agent with the specified configuration.
    
    Args:
        model: The name of the AI model to use (e.g., 'gemini-2.0-flash-exp')
        config: Configuration dictionary containing agent settings
        
    Returns:
        AgentExecutor: Configured agent ready for task execution
        
    Raises:
        ValueError: If model name is not supported
        ConfigurationError: If config is invalid
        
    Example:
        >>> agent = create_agent('gemini-2.0-flash-exp', {'temperature': 0.7})
        >>> response = agent.run("Take a screenshot")
    """
```

### Error Handling
- Use specific exception types
- Provide meaningful error messages
- Log errors with appropriate severity levels
- Implement graceful degradation where possible

```python
try:
    agent = create_agent(model_name, config)
except ValueError as e:
    logger.error(f"Invalid model configuration: {e}")
    raise ConfigurationError(f"Failed to create agent: {e}")
except Exception as e:
    logger.exception("Unexpected error during agent creation")
    raise
```

## Testing Framework

### Test Structure
- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **UI Tests**: Test user interface functionality
- **End-to-End Tests**: Test complete user workflows

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=utils --cov=ui --cov=voice

# Run specific test file
python -m pytest tests/test_agent.py

# Run tests with verbose output
python -m pytest -v

# Run tests matching pattern
python -m pytest -k "test_voice"
```

### Test Examples

```python
# tests/test_agent.py
import pytest
from unittest.mock import Mock, patch
from utils.agent import create_clevrr_agent

class TestAgentCreation:
    def test_create_agent_with_valid_model(self):
        """Test agent creation with valid model"""
        mock_model = Mock()
        agent = create_clevrr_agent(mock_model, "test prompt")
        assert agent is not None
        
    def test_create_agent_with_invalid_model(self):
        """Test agent creation with invalid model"""
        with pytest.raises(ValueError):
            create_clevrr_agent(None, "test prompt")
            
    @patch('utils.agent.create_react_agent')
    def test_agent_tools_configuration(self, mock_create):
        """Test that agent is configured with correct tools"""
        mock_model = Mock()
        create_clevrr_agent(mock_model, "test prompt")
        mock_create.assert_called_once()
        args, kwargs = mock_create.call_args
        assert len(args[1]) > 0  # Tools list should not be empty
```

### Mocking Guidelines
- Mock external dependencies (APIs, file system, etc.)
- Use dependency injection to make testing easier
- Create fixtures for common test data
- Test both success and failure scenarios

## Build and Deployment

### Building for Distribution

1. **Create Executable**
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed main.py
   ```

2. **Build Installer**
   ```bash
   # Using NSIS (Windows)
   makensis installer.nsi
   ```

3. **Package for Distribution**
   ```bash
   python setup.py sdist bdist_wheel
   ```

### Continuous Integration

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
        
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
        
    - name: Run tests
      run: pytest --cov=. --cov-report=xml
      
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### Release Process

1. **Version Bumping**
   ```bash
   # Update version in utils/constants.py
   VERSION = "1.2.0"
   ```

2. **Create Release Notes**
   - Document new features
   - List bug fixes
   - Note breaking changes
   - Include upgrade instructions

3. **Tag Release**
   ```bash
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```

## API Documentation

### Core APIs

#### Agent API
```python
# Create agent
agent = create_clevrr_agent(model, prompt)

# Execute task
result = agent.run("Take a screenshot and describe what you see")

# Get agent status
status = agent.get_status()
```

#### Voice API
```python
# Initialize voice manager
voice = VoiceManager()

# Start listening
voice.start_listening(callback=on_speech_recognized)

# Speak text
voice.speak_text("Hello, how can I help you?")

# Configure voice settings
voice.configure_voice(rate=200, volume=0.8, voice_id="HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0")
```

#### Configuration API
```python
# Load configuration
config = ConfigManager()

# Get setting
api_key = config.get('api_key')

# Set setting
config.set('theme_mode', 'dark')

# Save configuration
config.save_config()
```

### Event System

The application uses an event-driven architecture for component communication:

```python
# Event types
class EventType(Enum):
    AGENT_RESPONSE = "agent_response"
    VOICE_INPUT = "voice_input"
    THEME_CHANGED = "theme_changed"
    SETTINGS_UPDATED = "settings_updated"

# Event dispatcher
class EventDispatcher:
    def __init__(self):
        self.listeners = defaultdict(list)
        
    def subscribe(self, event_type: EventType, callback: Callable):
        self.listeners[event_type].append(callback)
        
    def emit(self, event_type: EventType, data: Any):
        for callback in self.listeners[event_type]:
            callback(data)
```

## Extension Points

### Adding New AI Models

1. **Create Model Configuration**
   ```python
   # utils/constants.py
   NEW_MODEL = ChatNewProvider(
       model="new-model-name",
       api_key=os.getenv("NEW_API_KEY"),
   )
   
   MODELS = {
       "gemini": GEMINI,
       "new_model": NEW_MODEL,
   }
   ```

2. **Update UI**
   ```python
   # ui/settings_tabs.py
   model_choices = ["gemini", "new_model"]
   ```

3. **Add Tests**
   ```python
   # tests/test_models.py
   def test_new_model_integration():
       # Test new model functionality
   ```

### Adding New Tools

1. **Create Tool Function**
   ```python
   # utils/tools.py
   @tool
   def new_automation_tool(instruction: str) -> str:
       """
       Description of what the tool does.
       
       Args:
           instruction: What the tool should do
           
       Returns:
           Result of the operation
       """
       # Implementation
       return "Tool result"
   ```

2. **Register Tool**
   ```python
   # utils/agent.py
   tools = [
       get_screen_info,
       new_automation_tool,  # Add new tool
   ]
   ```

### Adding New UI Components

1. **Create Component**
   ```python
   # ui/new_component.py
   class NewComponent(ttk.Frame):
       def __init__(self, parent, **kwargs):
           super().__init__(parent, **kwargs)
           self.setup_ui()
           
       def setup_ui(self):
           # Component implementation
   ```

2. **Apply Theme**
   ```python
   # ui/material_design.py
   def apply_theme_to_new_component(self, component):
       # Apply MD3 styling
   ```

## Contributing Guidelines

### Getting Started
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation
7. Commit changes (`git commit -m 'Add amazing feature'`)
8. Push to branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Pull Request Process
1. **Description**: Provide clear description of changes
2. **Testing**: Include test results and coverage information
3. **Documentation**: Update relevant documentation
4. **Breaking Changes**: Clearly mark any breaking changes
5. **Review**: Address all review comments

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New functionality has tests
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance impact considered
- [ ] Backward compatibility maintained

### Issue Reporting
- Use issue templates
- Provide minimal reproduction steps
- Include system information
- Attach relevant logs or screenshots

---

For questions about development, please see the [User Manual](USER_MANUAL.md) or contact the development team.
