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
  "screenshot_size": "medium"