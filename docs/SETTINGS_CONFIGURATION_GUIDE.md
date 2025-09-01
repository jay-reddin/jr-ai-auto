# JR AI Control - Settings Configuration Guide

## Table of Contents
1. [Overview](#overview)
2. [Accessing Settings](#accessing-settings)
3. [AI Settings Tab](#ai-settings-tab)
4. [UI Settings Tab](#ui-settings-tab)
5. [About Tab](#about-tab)
6. [Configuration File Structure](#configuration-file-structure)
7. [Advanced Configuration](#advanced-configuration)
8. [Settings Import/Export](#settings-importexport)
9. [Troubleshooting Settings](#troubleshooting-settings)
10. [Default Settings](#default-settings)

## Overview

JR AI Control provides comprehensive settings management through a modern tabbed interface. All settings are automatically saved and synchronized across the application in real-time, with no restart required for most changes.

### Settings Categories
- **AI Settings**: Model configuration, API keys, and voice controls
- **UI Settings**: Theme, appearance, and interface customization
- **About**: Application information, usage statistics, and help resources

### Key Features
- **Real-time Updates**: Changes apply immediately without restart
- **Persistent Storage**: Settings saved automatically to `config.json`
- **Validation**: Input validation prevents invalid configurations
- **Backup/Restore**: Export and import settings for backup or sharing
- **Reset Options**: Restore individual settings or all settings to defaults

## Accessing Settings

### Opening Settings Window
1. **Main Interface**: Click the **Settings** button in the top toolbar
2. **Keyboard Shortcut**: Press `Ctrl+S`
3. **Menu**: Right-click in chat area → Settings (if context menu enabled)

### Settings Window Layout
- **Tabbed Interface**: Three main tabs (AI, UI, About)
- **Apply/Cancel Buttons**: Save or discard changes
- **Reset Buttons**: Restore individual sections to defaults
- **Help Links**: Quick access to relevant documentation

## AI Settings Tab

### Model Configuration

#### **Model Selection**
- **Current Options**: Gemini models (gemini-2.0-flash-exp, gemini-1.5-pro-latest)
- **Default**: gemini-2.0-flash-exp
- **Description**: Choose the AI model for processing requests
- **Impact**: Different models may have varying capabilities and costs

#### **API Key Management**
- **Google API Key**: Required for Gemini model access
- **Input Field**: Secure text field (masked input)
- **Test Button**: Verify API key validity and connection
- **Status Indicator**: Shows connection status (Connected/Failed/Testing)

**Setting up API Key:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable the Gemini API
4. Create an API key in Credentials section
5. Copy and paste the key into JR AI Control
6. Click "Test API Key" to verify

### Voice Configuration

#### **Speech Recognition Settings**
- **Enable Speech Recognition**: Toggle voice input on/off
- **Recognition Language**: Set language for speech recognition (default: English US)
- **Microphone Sensitivity**: Adjust detection threshold (1-10 scale)
- **Timeout Duration**: How long to wait for speech input (1-30 seconds)

#### **Text-to-Speech Settings**
- **Enable Speech Output**: Toggle AI voice responses on/off
- **Voice Selection**: Choose from available Windows voices
  - David (Male, English US)
  - Zira (Female, English US)
  - Mark (Male, English US)
  - Additional voices if installed
- **Speech Rate**: Words per minute (50-300 WPM)
  - Slow: 50-100 WPM
  - Normal: 150-200 WPM
  - Fast: 250-300 WPM
- **Speech Volume**: Audio output level (0-100%)
- **Mute Speech**: Disable audio while keeping recognition active

#### **Advanced Voice Settings**
- **Voice Activity Detection**: Automatic speech start/stop detection
- **Noise Suppression**: Filter background noise during recognition
- **Echo Cancellation**: Prevent feedback from speakers to microphone
- **Continuous Listening**: Keep microphone active for hands-free operation

## UI Settings Tab

### Theme Configuration

#### **Theme Selection**
- **Dark Theme**: Dark background with light text (default)
- **Light Theme**: Light background with dark text
- **Auto Theme**: Follow system theme settings (if supported)
- **Custom Theme**: Advanced users can modify theme files

#### **Theme Customization**
- **Primary Color**: Main accent color for buttons and highlights
- **Secondary Color**: Secondary accent color for less prominent elements
- **Background Color**: Main background color for the interface
- **Text Color**: Primary text color for readability

### Interface Settings

#### **Chat Interface**
- **Message Bubble Style**: Modern speech bubbles (fixed)
- **Font Size**: Text size in chat area (8-24pt)
- **Message Spacing**: Vertical space between messages (compact/normal/spacious)
- **Timestamp Format**: How message times are displayed
  - 12-hour format (2:30 PM)
  - 24-hour format (14:30)
  - Relative time (2 minutes ago)

#### **Window Settings**
- **Window Opacity**: Transparency level (50-100%)
- **Always on Top**: Keep window above other applications
- **Minimize to Tray**: Hide to system tray instead of taskbar
- **Start Minimized**: Launch application minimized

### Screenshot Configuration

#### **Screenshot Settings**
- **Thumbnail Size**: Preview image size in chat
  - Small: 100x75 pixels
  - Medium: 150x100 pixels (default)
  - Large: 200x150 pixels
- **Screenshot Wait Duration**: Delay before taking screenshot (1-10 seconds)
- **Auto-save Screenshots**: Automatically save full-size images
- **Screenshot Quality**: JPEG compression level (1-100%)
- **Screenshot Format**: File format for saved images (PNG/JPEG)

#### **Screenshot Storage**
- **Storage Location**: Where screenshots are saved (default: screenshots/)
- **Filename Pattern**: How screenshot files are named
- **Automatic Cleanup**: Delete old screenshots after specified days
- **Maximum Storage**: Limit total screenshot storage size

### Notification Settings

#### **System Notifications**
- **Enable Notifications**: Toggle Windows toast notifications
- **Notification Duration**: How long notifications stay visible (1-30 seconds)
- **Notification Position**: Screen corner for notification display
- **Sound Alerts**: Play sound with notifications

#### **Notification Types**
- **Task Completion**: Notify when AI completes automation tasks
- **Process Updates**: Show progress for long-running operations
- **Error Alerts**: Display error messages as notifications
- **Voice Status**: Notify about voice recognition status changes

## About Tab

### Application Information

#### **Version Details**
- **Application Version**: Current JR AI Control version
- **Build Date**: When this version was compiled
- **Python Version**: Python interpreter version
- **Platform**: Operating system and architecture

#### **Developer Information**
- **Developer**: Application creator and maintainer details
- **Contact**: Support email and website links
- **License**: Software license information
- **Credits**: Third-party libraries and contributors

### Usage Statistics

#### **Token Usage**
- **Current Session**: Tokens used in current session
- **Total Usage**: All-time token consumption
- **Average per Message**: Typical token usage per interaction
- **Cost Estimation**: Approximate cost based on usage (if available)

#### **Session Statistics**
- **Messages Sent**: Number of user messages
- **AI Responses**: Number of AI responses received
- **Screenshots Taken**: Total screenshots captured
- **Voice Commands**: Number of voice interactions

#### **Reset Options**
- **Reset Token Counter**: Clear token usage statistics
- **Clear Chat History**: Remove all chat messages
- **Reset All Statistics**: Clear all usage data

### Help and Support

#### **Documentation Links**
- **User Manual**: Complete application guide
- **Voice Interaction Guide**: Voice feature documentation
- **Troubleshooting Guide**: Common issues and solutions
- **Developer Documentation**: Technical documentation

#### **Tips and Shortcuts**
- **Keyboard Shortcuts**: Quick reference for hotkeys
- **Voice Commands**: Examples of effective voice commands
- **Best Practices**: Tips for optimal application usage
- **Performance Tips**: Optimize application performance

## Configuration File Structure

### config.json Format
```json
{
  "api_key": "your_google_api_key_here",
  "model": "gemini-2.0-flash-exp",
  "theme_mode": "dark",
  "speech_enabled": true,
  "speech_muted": false,
  "voice_rate": 200,
  "voice_volume": 0.8,
  "voice_selection": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0",
  "recognition_language": "en-US",
  "microphone_sensitivity": 5,
  "screenshot_size": "medium",
  "screenshot_wait_duration": 3,
  "screenshot_quality": 85,
  "screenshot_format": "PNG",
  "notification_enabled": true,
  "notification_duration": 5,
  "window_opacity": 1.0,
  "always_on_top": false,
  "font_size": 12,
  "message_spacing": "normal",
  "timestamp_format": "12hour",
  "total_tokens_used": 15420,
  "session_start_time": "2024-01-15T10:30:00Z",
  "auto_save_screenshots": true,
  "screenshot_cleanup_days": 30,
  "max_screenshot_storage_mb": 1000
}
```

### Configuration Validation

#### **Required Fields**
- `api_key`: Must be valid Google API key
- `model`: Must be supported model name
- `theme_mode`: Must be "dark" or "light"

#### **Value Ranges**
- `voice_rate`: 50-300 (words per minute)
- `voice_volume`: 0.0-1.0 (volume level)
- `screenshot_wait_duration`: 1-10 (seconds)
- `microphone_sensitivity`: 1-10 (sensitivity level)
- `window_opacity`: 0.5-1.0 (transparency level)

#### **Default Fallbacks**
If configuration file is missing or corrupted, the application will:
1. Create new config.json with default values
2. Prompt user to enter API key
3. Use system defaults for voice and UI settings

## Advanced Configuration

### Manual Configuration Editing

#### **Backup Configuration**
Before manual editing:
```bash
copy config.json config.json.backup
```

#### **Edit Configuration**
1. Close JR AI Control completely
2. Open config.json in text editor
3. Make desired changes
4. Validate JSON syntax
5. Save file
6. Restart JR AI Control

#### **Configuration Validation**
The application validates configuration on startup:
- **Syntax Check**: Ensures valid JSON format
- **Value Validation**: Checks ranges and types
- **Key Validation**: Ensures required keys exist
- **Migration**: Updates old configuration formats

### Environment Variables

#### **Override Settings**
Environment variables can override config.json settings:
```bash
set JR_AI_GOOGLE_API_KEY=your_api_key
set JR_AI_THEME_MODE=dark
set JR_AI_VOICE_ENABLED=true
```

#### **Debug Settings**
```bash
set JR_AI_DEBUG=true
set JR_AI_LOG_LEVEL=DEBUG
set JR_AI_PERFORMANCE_MONITORING=true
```

### Registry Settings (Windows)

#### **Voice Configuration**
Windows voice settings stored in registry:
```
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\
```

#### **Application Settings**
JR AI Control may store some settings in:
```
HKEY_CURRENT_USER\SOFTWARE\JR AI Control\
```

## Settings Import/Export

### Export Settings

#### **Full Export**
1. Go to Settings → About tab
2. Click "Export Settings"
3. Choose location and filename
4. Settings saved as JSON file

#### **Selective Export**
1. Choose specific setting categories
2. Export only AI settings, UI settings, or statistics
3. Create partial configuration files

### Import Settings

#### **Full Import**
1. Go to Settings → About tab
2. Click "Import Settings"
3. Select previously exported JSON file
4. Confirm import and restart if required

#### **Merge Import**
1. Choose to merge with existing settings
2. Resolve conflicts (keep existing vs. import new)
3. Validate imported settings

### Sharing Settings

#### **Team Configuration**
1. Export settings from configured installation
2. Share JSON file with team members
3. Team members import settings
4. Consistent configuration across team

#### **Backup Strategy**
1. Regular exports to backup location
2. Version control for configuration files
3. Cloud storage for cross-device sync

## Troubleshooting Settings

### Common Issues

#### **Settings Not Saving**
1. Check file permissions on config.json
2. Ensure application has write access to directory
3. Verify disk space availability
4. Run application as administrator if needed

#### **Settings Reset on Restart**
1. Check for multiple config.json files
2. Verify configuration file location
3. Check for file corruption
4. Review antivirus software interference

#### **Invalid Configuration**
1. Validate JSON syntax using online validator
2. Check for missing required fields
3. Verify value ranges and types
4. Restore from backup if necessary

### Recovery Procedures

#### **Reset to Defaults**
1. Close JR AI Control
2. Rename config.json to config.json.old
3. Restart application
4. New default configuration created

#### **Partial Recovery**
1. Open corrupted config.json
2. Copy valid sections to new file
3. Fill missing sections with defaults
4. Validate and test new configuration

#### **Backup Restoration**
1. Locate backup configuration file
2. Replace current config.json with backup
3. Restart application
4. Verify settings restored correctly

## Default Settings

### Factory Defaults
```json
{
  "api_key": "",
  "model": "gemini-2.0-flash-exp",
  "theme_mode": "dark",
  "speech_enabled": false,
  "speech_muted": false,
  "voice_rate": 200,
  "voice_volume": 0.8,
  "voice_selection": "default",
  "recognition_language": "en-US",
  "microphone_sensitivity": 5,
  "screenshot_size": "medium",
  "screenshot_wait_duration": 3,
  "screenshot_quality": 85,
  "screenshot_format": "PNG",
  "notification_enabled": true,
  "notification_duration": 5,
  "window_opacity": 1.0,
  "always_on_top": false,
  "font_size": 12,
  "message_spacing": "normal",
  "timestamp_format": "12hour",
  "total_tokens_used": 0,
  "auto_save_screenshots": true,
  "screenshot_cleanup_days": 30,
  "max_screenshot_storage_mb": 1000
}
```

### Recommended Settings

#### **For New Users**
- Enable speech recognition and TTS for full experience
- Use medium screenshot size for balance of quality and performance
- Keep notifications enabled for task completion alerts
- Start with dark theme (easier on eyes)

#### **For Performance**
- Disable speech features if not needed
- Use small screenshot size
- Reduce screenshot quality to 70%
- Limit screenshot storage to 500MB

#### **For Privacy**
- Disable notifications in shared environments
- Turn off auto-save screenshots for sensitive work
- Use local-only voice processing
- Regular cleanup of chat history and screenshots

---

For additional help with settings, see the [User Manual](USER_MANUAL.md) or [Troubleshooting Guide](TROUBLESHOOTING.md).