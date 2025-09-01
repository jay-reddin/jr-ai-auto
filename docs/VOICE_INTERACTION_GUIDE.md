# JR AI Control - Voice Interaction Guide

## Table of Contents
1. [Overview](#overview)
2. [System Requirements](#system-requirements)
3. [Initial Setup](#initial-setup)
4. [Voice Input Configuration](#voice-input-configuration)
5. [Text-to-Speech Setup](#text-to-speech-setup)
6. [Using Voice Commands](#using-voice-commands)
7. [Voice Control Features](#voice-control-features)
8. [Troubleshooting Voice Issues](#troubleshooting-voice-issues)
9. [Advanced Voice Settings](#advanced-voice-settings)
10. [Best Practices](#best-practices)

## Overview

JR AI Control's voice interaction system allows you to communicate with the AI using natural speech and receive audio responses. The system uses Windows' built-in Speech Recognition API for speech-to-text conversion and Windows SAPI (Speech API) for text-to-speech output.

### Key Voice Features
- **Speech Recognition**: Convert your voice to text automatically
- **Text-to-Speech**: Hear AI responses spoken aloud
- **Continuous Listening**: Keep the microphone active for hands-free operation
- **Voice Activity Detection**: Automatic start/stop based on speech
- **Multiple Voice Options**: Choose from installed Windows voices
- **Customizable Settings**: Adjust speech rate, volume, and recognition sensitivity

## System Requirements

### Hardware Requirements
- **Microphone**: Built-in or external microphone
- **Audio Output**: Speakers, headphones, or audio system
- **Sound Card**: Windows-compatible audio device

### Software Requirements
- **Windows 10 or later**: Required for modern speech APIs
- **Windows Speech Recognition**: Enabled in Windows settings
- **Audio Drivers**: Up-to-date audio drivers for your system
- **Python Audio Libraries**: Automatically installed with JR AI Control

### Recommended Setup
- **Quiet Environment**: Minimize background noise for better recognition
- **Quality Microphone**: USB or headset microphone for clearer input
- **Stable Internet**: Required for AI processing (voice processing is local)

## Initial Setup

### 1. Enable Windows Speech Recognition
1. Open **Windows Settings** (Windows + I)
2. Go to **Privacy & Security** → **Speech**
3. Enable **Online speech recognition**
4. Go to **Time & Language** → **Speech**
5. Set up speech recognition if not already configured

### 2. Configure Audio Devices
1. Right-click the speaker icon in system tray
2. Select **Open Sound settings**
3. Set your preferred microphone as default input device
4. Set your preferred speakers/headphones as default output device
5. Test microphone levels and adjust sensitivity

### 3. Enable Voice in JR AI Control
1. Launch JR AI Control
2. Click **Settings** button
3. Go to **AI** tab
4. Toggle **Enable Speech** to ON
5. Configure voice settings as needed

## Voice Input Configuration

### Microphone Setup
1. **Test Microphone**: Use Windows Sound settings to test microphone
2. **Adjust Levels**: Set microphone volume to 70-80% for optimal recognition
3. **Noise Suppression**: Enable if available in your audio driver settings
4. **Positioning**: Place microphone 6-12 inches from your mouth

### Speech Recognition Settings
Access through **Settings** → **AI** tab:

- **Recognition Language**: Set to your preferred language (default: English US)
- **Recognition Sensitivity**: Adjust how easily the system detects speech
- **Timeout Settings**: Configure how long to wait for speech input
- **Background Noise**: Enable noise filtering for better accuracy

### Using the Microphone Button
1. **Click to Start**: Click the microphone button to begin listening
2. **Visual Feedback**: Button turns red and shows "Listening..."
3. **Speak Clearly**: Talk at normal pace and volume
4. **Auto-Stop**: Recognition stops automatically after silence
5. **Manual Stop**: Click microphone again to stop listening immediately

## Text-to-Speech Setup

### Voice Selection
1. Go to **Settings** → **AI** tab
2. Find **Voice Selection** dropdown
3. Choose from available Windows voices:
   - **David** (Male, English US)
   - **Zira** (Female, English US)
   - **Mark** (Male, English US)
   - Additional voices if installed

### Speech Rate Configuration
- **Slow (50-100 WPM)**: For careful listening or learning
- **Normal (150-200 WPM)**: Standard conversational pace
- **Fast (250-300 WPM)**: Quick information delivery
- **Custom**: Set specific words per minute

### Volume Control
- **System Volume**: Controls overall application audio
- **Speech Volume**: Specific volume for AI voice responses
- **Mute Option**: Disable speech while keeping recognition active

### Speech Queue Management
- **Sequential Playback**: Responses play in order received
- **Interrupt Capability**: New speech can interrupt current playback
- **Queue Status**: Visual indicator shows pending speech

## Using Voice Commands

### Basic Voice Interaction
1. **Activate Microphone**: Click microphone button or use Ctrl+M
2. **Wait for Indicator**: Ensure "Listening..." appears
3. **Speak Command**: Use natural language
4. **Automatic Processing**: Speech converts to text and sends to AI
5. **Audio Response**: AI responds both in text and speech

### Natural Language Examples
```
"Take a screenshot and tell me what applications are open"
"Click on the start button"
"Open the calculator"
"Type 'Hello World' in the current window"
"Press Alt+Tab to switch between windows"
"Scroll down on this page"
"Find the save button and click it"
"What's the weather like today?"
"Help me organize these files"
"Show me how to change my desktop wallpaper"
```

### Voice Command Categories

#### **Screen Analysis**
- "What do you see on my screen?"
- "Describe the current window"
- "What applications are running?"
- "Read the text on screen"

#### **Mouse Operations**
- "Click on [element name]"
- "Right-click on the desktop"
- "Double-click the file icon"
- "Drag this window to the left"

#### **Keyboard Operations**
- "Type [your text here]"
- "Press Enter"
- "Use Ctrl+C to copy"
- "Press the Windows key"

#### **Application Control**
- "Open [application name]"
- "Close the current window"
- "Switch to [application name]"
- "Minimize all windows"

## Voice Control Features

### Continuous Listening Mode
- **Always On**: Keep microphone active for hands-free operation
- **Wake Word**: Configure optional wake word to activate
- **Auto-Timeout**: Automatically stop after period of silence
- **Battery Consideration**: May impact laptop battery life

### Voice Activity Detection
- **Automatic Start**: Begin recognition when speech is detected
- **Silence Detection**: Stop recording after speech ends
- **Noise Filtering**: Ignore background sounds and focus on speech
- **Sensitivity Adjustment**: Configure detection threshold

### Speech Feedback
- **Visual Indicators**: Microphone button changes color when active
- **Status Messages**: "Listening...", "Processing...", "Speaking..."
- **Error Notifications**: Clear messages for recognition failures
- **Confidence Levels**: System confidence in speech recognition

### Multi-Modal Interaction
- **Voice + Text**: Switch between voice and typing seamlessly
- **Voice + Screenshots**: Combine voice commands with visual analysis
- **Voice + Automation**: Use voice to control complex automation sequences

## Troubleshooting Voice Issues

### Common Speech Recognition Problems

#### **Microphone Not Detected**
1. Check microphone connection
2. Verify default input device in Windows Sound settings
3. Restart JR AI Control
4. Test microphone in other applications

#### **Poor Recognition Accuracy**
1. Speak more clearly and slowly
2. Reduce background noise
3. Adjust microphone position
4. Increase microphone volume in Windows settings
5. Train Windows Speech Recognition

#### **No Audio Response**
1. Check speaker/headphone connection
2. Verify default output device in Windows Sound settings
3. Check volume levels (system and application)
4. Test audio in other applications
5. Restart audio services

### Advanced Troubleshooting

#### **Speech Recognition Service Issues**
1. Open **Services** (services.msc)
2. Find **Windows Speech Recognition**
3. Restart the service
4. Set startup type to **Automatic**

#### **Audio Driver Problems**
1. Update audio drivers through Device Manager
2. Reinstall audio drivers from manufacturer
3. Check for Windows updates
4. Run Windows Audio troubleshooter

#### **Python Audio Library Issues**
1. Reinstall JR AI Control dependencies
2. Check Python audio library versions
3. Run application as administrator
4. Check antivirus software interference

### Error Messages and Solutions

#### **"Microphone access denied"**
- Grant microphone permissions in Windows Privacy settings
- Check application permissions for JR AI Control

#### **"Speech recognition not available"**
- Enable Windows Speech Recognition in system settings
- Install language packs if using non-English languages

#### **"Audio device not found"**
- Check audio device connections
- Update audio drivers
- Restart Windows Audio service

## Advanced Voice Settings

### Custom Voice Training
1. **Windows Speech Recognition Training**: Improve accuracy for your voice
2. **Accent Adaptation**: Train system for regional accents
3. **Vocabulary Expansion**: Add technical terms and proper names
4. **Personal Dictionary**: Add frequently used words

### Performance Optimization
- **Recognition Timeout**: Adjust for faster/slower speakers
- **Processing Delay**: Configure delay between recognition and processing
- **Audio Buffer Size**: Optimize for system performance
- **Background Processing**: Enable/disable background speech processing

### Integration Settings
- **Hotkey Configuration**: Set custom keyboard shortcuts for voice control
- **Application Integration**: Configure voice control for specific applications
- **Automation Triggers**: Use voice commands to trigger automation sequences

## Best Practices

### For Better Recognition
1. **Speak Naturally**: Use normal conversational tone and pace
2. **Clear Pronunciation**: Articulate words clearly without over-emphasizing
3. **Consistent Volume**: Maintain steady speaking volume
4. **Pause Between Commands**: Allow processing time between requests
5. **Use Complete Sentences**: Full sentences work better than fragments

### Environment Optimization
1. **Quiet Space**: Minimize background noise and distractions
2. **Microphone Position**: Keep consistent distance and angle
3. **Room Acoustics**: Avoid echoing rooms or hard surfaces
4. **Interference**: Keep away from fans, air conditioning, or electronic noise

### Effective Voice Commands
1. **Be Specific**: "Click the blue Save button" vs "click something"
2. **Use Context**: Reference what's currently visible on screen
3. **Natural Language**: Speak as you would to a human assistant
4. **Confirm Actions**: Ask for confirmation before destructive operations
5. **Break Down Complex Tasks**: Split complicated requests into steps

### Voice Etiquette
1. **Wait for Responses**: Allow AI to complete responses before new commands
2. **Use Please/Thank You**: Natural politeness improves interaction
3. **Correct Mistakes**: If recognition is wrong, speak the correction clearly
4. **Be Patient**: Voice processing may take a moment, especially for complex requests

### Security Considerations
1. **Sensitive Information**: Be cautious speaking passwords or personal data
2. **Public Spaces**: Consider privacy when using voice in shared environments
3. **Recording Awareness**: Remember that voice input is processed (but not stored)
4. **Microphone Control**: Use mute when not actively using voice features

---

For additional help with voice features, see the main [User Manual](USER_MANUAL.md) or [Troubleshooting Guide](TROUBLESHOOTING.md).