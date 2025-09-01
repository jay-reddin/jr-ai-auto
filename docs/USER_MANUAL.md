# JR AI Control - User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Main Interface](#main-interface)
4. [Voice Interaction](#voice-interaction)
5. [Chat Interface](#chat-interface)
6. [Screenshot Features](#screenshot-features)
7. [Settings Configuration](#settings-configuration)
8. [Token Tracking](#token-tracking)
9. [Notifications](#notifications)
10. [Keyboard Shortcuts](#keyboard-shortcuts)
11. [Tips and Best Practices](#tips-and-best-practices)

## Introduction

JR AI Control is an advanced AI-powered automation assistant that helps you control your Windows computer using natural language commands. The application features a modern Material Design 3 interface, voice interaction capabilities, screenshot analysis, and comprehensive automation tools powered by Google's Gemini AI model.

### Key Features
- **Voice Interaction**: Speak to the AI and receive audio responses
- **Screenshot Analysis**: AI can see and analyze your screen with thumbnail previews
- **Modern UI**: Material Design 3 interface with dark/light themes
- **Token Tracking**: Monitor AI usage and costs
- **Smart Notifications**: Get notified when tasks complete
- **Comprehensive Settings**: Customize every aspect of your experience

## Getting Started

### System Requirements
- Windows 10 or later
- Python 3.8 or higher
- Microphone (for voice features)
- Speakers or headphones (for audio responses)
- Google API key for Gemini

### First Launch
1. Launch JR AI Control from your desktop or start menu
2. The application will open with the main chat interface
3. If this is your first time, you'll need to configure your API key in Settings
4. The current AI model will be displayed in the header

### Initial Setup
1. Click the **Settings** button in the top toolbar
2. Go to the **AI** tab
3. Enter your Google API key in the provided field
4. Test the connection using the "Test API Key" button
5. Configure your preferred voice and UI settings

## Main Interface

### Header Section
- **Application Title**: "JR AI Control" with current version
- **Model Display**: Shows the currently active AI model (e.g., "gemini-2.0-flash-exp")
- **Token Counter**: Displays total tokens used in current session
- **Theme Toggle**: Switch between dark and light themes
- **Settings Button**: Access comprehensive settings

### Chat Area
The main chat area displays your conversation with the AI in modern speech bubbles:
- **User Messages**: Right-aligned blue bubbles with your input
- **AI Responses**: Left-aligned gray bubbles with AI responses
- **Timestamps**: Each message shows when it was sent
- **Token Count**: Individual message token usage displayed
- **Screenshot Thumbnails**: Inline preview of any screenshots taken

### Input Section
- **Text Input**: Type your commands and questions
- **Microphone Button**: Click to start voice input (turns red when listening)
- **Send Button**: Submit your message to the AI

## Voice Interaction

### Enabling Voice Features
1. Open **Settings** → **AI** tab
2. Toggle "Enable Speech" to activate voice features
3. Configure voice settings:
   - **Speech Rate**: How fast the AI speaks (50-300 words per minute)
   - **Speech Volume**: Audio output level (0-100%)
   - **Voice Selection**: Choose from available system voices

### Using Voice Input
1. Click the microphone button in the input area
2. The button turns red and shows "Listening..."
3. Speak your command clearly
4. The AI will convert your speech to text automatically
5. Click the microphone again to stop listening

### Voice Responses
- When speech is enabled, the AI will both type and speak responses
- Use the "Mute Speech" option to disable audio while keeping speech recognition
- Voice responses are queued and played in order

### Voice Commands
You can use natural language for any automation task:
- "Take a screenshot and tell me what you see"
- "Open the calculator application"
- "Click on the start button"
- "Type 'Hello World' in the current window"
- "Press Alt+Tab to switch windows"

## Chat Interface

### Message Bubbles
- **User Messages**: Appear on the right in blue bubbles
- **AI Messages**: Appear on the left in gray bubbles
- **Sender Names**: Displayed above each bubble
- **Timestamps**: Show when each message was sent

### Message Actions
Each message has action buttons below it:
- **Resend**: Send the same message again (user messages only)
- **Copy**: Copy message text to clipboard
- **Delete**: Remove the message from chat history

### Screenshot Integration
When the AI takes screenshots:
- Thumbnail images appear inline with messages
- Click thumbnails to view full-size images
- Screenshots are automatically saved to the screenshots folder
- Thumbnail size can be adjusted in UI settings

## Screenshot Features

### Automatic Screenshots
The AI automatically takes screenshots when:
- You ask it to analyze your screen
- It needs to see the current state for automation
- You request visual information about your desktop

### Screenshot Analysis
The AI can:
- Identify applications and windows
- Read text from images
- Locate buttons and interface elements
- Provide detailed descriptions of screen content
- Guide you through complex interfaces

### Screenshot Settings
Configure screenshot behavior in **Settings** → **UI**:
- **Thumbnail Size**: Small, Medium, or Large preview images
- **Wait Duration**: How long to wait before taking screenshots (1-10 seconds)
- **Auto-save**: Screenshots are automatically saved with timestamps

## Settings Configuration

### AI Settings Tab
- **Model Selection**: Choose your preferred Gemini model
- **API Key Management**: Enter and test your Google API key
- **Speech Controls**: Enable/disable voice features
- **Voice Settings**: Configure speech rate, volume, and voice selection

### UI Settings Tab
- **Theme Selection**: Switch between dark and light themes
- **Screenshot Size**: Adjust thumbnail preview size
- **Screenshot Wait**: Set delay before taking screenshots
- **Notifications**: Enable/disable system notifications
- **Interface Options**: Customize UI behavior

### About Tab
- **Application Information**: Version, developer details
- **Usage Statistics**: Current token usage and session stats
- **Tips and Shortcuts**: Quick reference for keyboard shortcuts
- **Support Links**: Documentation and help resources

## Token Tracking

### Understanding Tokens
Tokens represent the cost of AI processing:
- Input tokens: Your messages and screenshots sent to AI
- Output tokens: AI responses and analysis
- Total usage: Cumulative tokens used across all sessions

### Token Display
- **Message Level**: Each message shows its token count
- **Session Total**: Running total displayed in header
- **Persistent Tracking**: Usage persists between application restarts

### Managing Usage
- Monitor token usage to control costs
- Longer conversations use more tokens
- Screenshots and image analysis consume additional tokens
- Reset token counter in About tab if needed

## Notifications

### Notification Types
- **Task Completion**: When automation tasks finish
- **Process Updates**: Progress indicators for long-running tasks
- **System Alerts**: Important status changes or errors

### Notification Settings
- Enable/disable notifications in **Settings** → **UI**
- Notifications appear as Windows toast messages
- Click notifications to return focus to JR AI Control
- Notifications queue automatically and don't interrupt workflow

## Keyboard Shortcuts

### Global Shortcuts
- **Ctrl+Enter**: Send message
- **Ctrl+M**: Toggle microphone
- **Ctrl+T**: Toggle theme (dark/light)
- **Ctrl+S**: Open settings
- **Ctrl+R**: Resend last message
- **Escape**: Stop current AI processing

### Chat Shortcuts
- **Up Arrow**: Edit last sent message
- **Ctrl+A**: Select all text in input
- **Ctrl+C**: Copy selected message
- **Delete**: Delete selected message

## Tips and Best Practices

### Effective Communication
- Be specific and clear in your requests
- Break complex tasks into smaller steps
- Use natural language - no special commands needed
- Provide context when asking about screen elements

### Voice Interaction Tips
- Speak clearly and at normal pace
- Use the microphone in a quiet environment
- Wait for the "Listening..." indicator before speaking
- You can interrupt AI speech by clicking the microphone

### Screenshot Optimization
- Ensure your screen is visible and unobstructed
- Close unnecessary windows for clearer analysis
- Use descriptive language when asking about screen elements
- Adjust screenshot wait time for slower systems

### Performance Tips
- Monitor token usage for cost control
- Clear chat history periodically for better performance
- Close unused applications to improve screenshot analysis
- Use specific requests rather than broad exploration

### Troubleshooting Quick Tips
- Restart the application if voice features stop working
- Check your internet connection if AI responses are slow
- Verify API key if you get authentication errors
- Update your graphics drivers if screenshots appear corrupted

### Security Best Practices
- Keep your API key secure and don't share it
- Be cautious when automating sensitive applications
- Review AI actions before confirming destructive operations
- Use the application responsibly and ethically

---

For additional help, see the [Troubleshooting Guide](TROUBLESHOOTING.md) or [Settings Configuration Guide](SETTINGS_CONFIGURATION_GUIDE.md).