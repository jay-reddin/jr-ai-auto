# JR AI Control

JR AI Control is an advanced AI-powered automation assistant that helps you control your Windows computer using natural language commands. Featuring a modern Material Design 3 interface, voice interaction capabilities, screenshot analysis, and comprehensive automation tools powered by Google's Gemini AI model.

## Features

### 🎯 **Core Automation**
- **Windows-optimized automation** with precise mouse movements, clicks, and keyboard inputs
- **Google Gemini-powered** screen analysis and intelligent task execution
- **Screenshot analysis** with thumbnail previews and click-to-expand functionality
- **Coordinate grid overlay** for accurate positioning and visual feedback

### 🎤 **Voice Interaction**
- **Speech Recognition** - Speak commands naturally using Windows Speech Recognition
- **Text-to-Speech** - Hear AI responses with customizable voice settings
- **Hands-free Operation** - Continuous listening mode for seamless interaction
- **Voice Controls** - Microphone button with visual feedback and status indicators

### 🎨 **Modern Interface**
- **Material Design 3** - Beautiful, modern interface with smooth animations
- **Dark/Light Themes** - Seamless theme switching with system integration
- **Chat Bubbles** - Modern speech bubble interface with message actions
- **Token Tracking** - Monitor AI usage with per-message and total token counts

### 🔧 **Advanced Settings**
- **Tabbed Settings** - Comprehensive settings organized in AI, UI, and About tabs
- **Real-time Updates** - Settings apply immediately without restart
- **Voice Customization** - Adjust speech rate, volume, and voice selection
- **Screenshot Configuration** - Customizable thumbnail sizes and wait durations

### 📱 **Smart Notifications**
- **Task Completion Alerts** - Windows toast notifications for completed tasks
- **Progress Updates** - Real-time status updates for long-running operations
- **Notification Queue** - Intelligent notification management with priority support

### 🔒 **Security & Privacy**
- **Local Processing** - Voice recognition and TTS processed locally on Windows
- **Secure API Key Management** - Encrypted storage with connection testing
- **Privacy Controls** - User control over data retention and screenshot storage

## Installation (Windows)

> [!CAUTION]
> JR AI Control is a beta feature. Please be aware that JR AI Control poses unique risks that are distinct from standard API features or chat interfaces. These risks are heightened when using JR AI Control to interact with the internet. To minimize risks, consider taking precautions such as:
>
> - Use a dedicated virtual machine or container with minimal privileges to prevent direct system attacks or accidents.
> - Avoid giving the model access to sensitive data, such as account login information, to prevent information theft.
> - Limit internet access to an allowlist of domains to reduce exposure to malicious content.
> - Ask a human to confirm decisions that may result in meaningful real-world consequences as well as any tasks requiring affirmative consent, such as accepting cookies, executing financial transactions, or agreeing to terms of service.
>
> In some circumstances, JR AI Control will follow commands found in content even if it conflicts with the user's instructions. For example, instructions on webpages or contained in images may override user instructions or cause JR AI Control to make mistakes. We suggest taking precautions to isolate JR AI Control from sensitive data and actions to avoid risks related to prompt injection.

### Prerequisites

- **Windows 10 or later** (optimized for Windows systems)
- **Python 3.8 or later** installed on your Windows system
- **Google API Key** for Gemini access

### Installation Steps

1. **Clone the repository:**

   ```cmd
   git clone https://github.com/JayRay1987/JR-AI-Control.git
   cd JR-AI-Control
   ```

2. **Install dependencies:**

   ```cmd
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   Rename the `.env_dev` file to `.env` and add your Google API key:

   ```plaintext
   GOOGLE_API_KEY=<YOUR_GEMINI_API_KEY>
   VERSION=1.0.0
   LAST_CHANGES=["Enhanced Material Design 3 UI", "Voice interaction system", "Screenshot thumbnails", "Comprehensive settings management"]
   ```

4. **Configure Windows Speech Recognition (Optional):**

   For voice features, ensure Windows Speech Recognition is enabled:
   - Go to Windows Settings → Privacy & Security → Speech
   - Enable "Online speech recognition"
   - Go to Time & Language → Speech
   - Set up speech recognition if not already configured

   **Note:** This application uses Google Gemini exclusively with enhanced Windows integration and modern UI features.

## Usage

### Quick Start

1. **Launch the Application:**

   ```cmd
   python main.py
   ```

   The application will open with the modern Material Design 3 interface.

2. **Initial Setup:**
   - Click the **Settings** button in the top toolbar
   - Go to the **AI** tab and enter your Google API key
   - Test the connection using the "Test API Key" button
   - Configure voice settings if desired

3. **Start Automating:**
   - Type commands in natural language: "Take a screenshot and tell me what you see"
   - Use voice input by clicking the microphone button
   - View screenshot thumbnails inline with chat messages
   - Monitor token usage in the header display

### Command Line Options

```cmd
# Default run with enhanced UI
python main.py

# Specify Gemini model explicitly
python main.py --model gemini

# Disable floating UI behavior
python main.py --float-ui 0

# Enable debug mode
python main.py --debug
```

### Interface Overview

#### **Header Section**
- **Application Title**: "JR AI Control" with version info
- **Model Display**: Shows current AI model (e.g., "gemini-2.0-flash-exp")
- **Token Counter**: Real-time token usage tracking
- **Theme Toggle**: Switch between dark/light themes
- **Settings Button**: Access comprehensive settings

#### **Chat Interface**
- **Speech Bubbles**: Modern chat interface with user (right) and AI (left) messages
- **Screenshot Thumbnails**: Inline preview images with click-to-expand
- **Message Actions**: Resend, copy, and delete buttons for each message
- **Voice Input**: Microphone button with visual feedback

#### **Input Section**
- **Text Input**: Type commands and questions
- **Microphone Button**: Voice input with "Listening..." indicator
- **Send Button**: Submit messages to AI

### Voice Interaction

#### **Enable Voice Features**
1. Open **Settings** → **AI** tab
2. Toggle "Enable Speech" to activate voice features
3. Configure voice settings (rate, volume, voice selection)

#### **Using Voice Commands**
- Click microphone button (turns red when listening)
- Speak naturally: "Open calculator and perform 25 + 37"
- AI responds both in text and speech
- Use "Mute Speech" to disable audio while keeping recognition

### Example Commands

```
# Screen Analysis
"Take a screenshot and describe what applications are open"
"What do you see on my screen right now?"

# Application Control  
"Open the calculator application"
"Switch to Google Chrome"
"Close the current window"

# Automation Tasks
"Click on the start button"
"Type 'Hello World' in the current text field"
"Press Alt+Tab to switch windows"
"Scroll down on this webpage"

# File Management
"Open File Explorer and navigate to Documents"
"Create a new folder called 'Projects'"
"Find and open the latest Word document"
```

### Enhanced Features

#### **Screenshot Thumbnails**
- Automatic thumbnail generation for all screenshots
- Configurable sizes (small/medium/large) in UI settings
- Click thumbnails to view full-size images
- Efficient caching and storage management

#### **Token Tracking**
- Per-message token counts displayed with each interaction
- Running total in header with persistent storage
- Usage statistics in About tab with reset options
- Cost estimation and usage analytics

#### **Notification System**
- Windows toast notifications for task completion
- Progress updates for long-running operations
- Configurable notification settings and duration
- Non-intrusive notification queue management


## Examples

![Demo](./examples/demo.gif)

![Demo 2](./examples/demo_2.gif)

![Example 1](./examples/2.png)

![Example 2](./examples/3.png)

![Example 3](./examples/4.png)

![Example 4](./examples/5.png)


## How it works?
It's a multi-modal AI Agent powered by Google Gemini running with a constant screenshot capturing mechanism to learn what it is seeing on the screen and direct the main action agent to function accordingly, using Python's `PyAutoGUI` library to perform actions.

- The agent is given a task to perform and it creates a chain of thought to perform the task using **Google Gemini's advanced vision capabilities**.
- It uses the `get_screen_info` tool to get information about the screen. This tool takes a screenshot of the current screen and uses a coordinate grid to mark the true coordinates. It then uses **Google Gemini's multi-modal capabilities** to understand the contents of the screen and provide answers based on the agent's questions.
- The chain of thought is then used to perform the task, supported by the `get_screen_info` tool and the `PythonREPLAst` tool, which is designed to perform actions using the `PyAutoGUI` library of Python.

### Windows Optimization
- **Native Windows font handling** ensures proper coordinate grid rendering
- **Windows-specific PyAutoGUI configurations** for optimal performance
- **Streamlined dependencies** focused only on Gemini and Windows compatibility


## Documentation

### Complete Guides
- **[User Manual](docs/USER_MANUAL.md)** - Comprehensive guide to all features
- **[Voice Interaction Guide](docs/VOICE_INTERACTION_GUIDE.md)** - Detailed voice setup and usage
- **[Settings Configuration Guide](docs/SETTINGS_CONFIGURATION_GUIDE.md)** - Complete settings reference
- **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Developer Documentation](docs/DEVELOPER_DOCUMENTATION.md)** - Technical documentation

### Quick Reference

#### **Keyboard Shortcuts**
- `Ctrl+Enter` - Send message
- `Ctrl+M` - Toggle microphone
- `Ctrl+T` - Toggle theme
- `Ctrl+S` - Open settings
- `Escape` - Stop current processing

#### **Voice Commands**
- Natural language works best: "Take a screenshot and tell me what you see"
- Be specific: "Click the blue Save button in the top toolbar"
- Use context: "What applications are currently open on my screen?"

## Troubleshooting

### Quick Fixes

#### **Application Won't Start**
```cmd
# Update dependencies
pip install -r requirements.txt --force-reinstall

# Run as administrator
# Right-click application → "Run as administrator"
```

#### **Voice Features Not Working**
1. Check Windows Speech Recognition is enabled
2. Verify microphone permissions in Windows Privacy settings
3. Test microphone in other applications
4. Update audio drivers

#### **API Connection Issues**
1. Verify Google API key in Settings → AI tab
2. Test API key using the "Test API Key" button
3. Check internet connection
4. Ensure Gemini API is enabled in Google Cloud Console

#### **Screenshot Problems**
1. Run application as administrator
2. Check display scaling settings
3. Update graphics drivers
4. Verify PyAutoGUI permissions

### Getting Help

For detailed troubleshooting, see the [Troubleshooting Guide](docs/TROUBLESHOOTING.md) or contact support.

## Configuration

### Environment Variables
```plaintext
# .env file
GOOGLE_API_KEY=your_actual_gemini_api_key_here
VERSION=1.0.0
LAST_CHANGES=["Enhanced Material Design 3 UI", "Voice interaction system", "Screenshot thumbnails"]

# Optional debug settings
JR_AI_DEBUG=true
JR_AI_LOG_LEVEL=DEBUG
```

### Settings File (config.json)
The application automatically creates and manages a `config.json` file with your preferences:
- API key and model selection
- Theme and UI preferences  
- Voice and speech settings
- Screenshot and notification configuration
- Token usage statistics

Settings can be exported/imported through the About tab for backup or sharing.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## Contact

For any questions or issues, please contact [yurvaj@getclevrr.com](mailto:yurvaj@getclevrr.com).
