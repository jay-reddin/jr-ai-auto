# JR AI Control - Enhanced Features Requirements Document

## Introduction

This project involves enhancing the JR AI Control application (formerly Clevrr Computer) with advanced features including voice interaction, modern Material Design 3 UI, token tracking, screenshot thumbnails, notifications, and comprehensive settings management. The application will maintain its Windows-optimized, Gemini-only implementation while adding significant user experience improvements.

## Requirements

### Requirement 1

**User Story:** As a Windows user, I want the Clevrr Computer to work seamlessly on my Windows system without Linux/Ubuntu-specific dependencies or configurations.

#### Acceptance Criteria

1. WHEN the application runs on Windows THEN it SHALL use Windows-compatible font loading mechanisms
2. WHEN PyAutoGUI operations are performed THEN they SHALL work correctly with Windows-specific key combinations and screen handling
3. WHEN screenshots are taken THEN the coordinate grid overlay SHALL display correctly on Windows systems
4. WHEN the application starts THEN it SHALL not require any Linux-specific packages or configurations

### Requirement 2

**User Story:** As a developer, I want to use only Google Gemini as the AI provider to simplify the codebase and reduce dependencies.

#### Acceptance Criteria

1. WHEN the application initializes THEN it SHALL only use Google Gemini models for AI processing
2. WHEN model selection occurs THEN it SHALL default to Gemini and not offer Azure OpenAI options
3. WHEN environment variables are loaded THEN it SHALL only require GOOGLE_API_KEY
4. WHEN dependencies are installed THEN they SHALL not include Azure OpenAI or unused Google Cloud packages

### Requirement 3

**User Story:** As a user, I want the agent to correctly use the model I specify in the command line arguments.

#### Acceptance Criteria

1. WHEN I specify a model via command line THEN the agent SHALL use that exact model
2. WHEN no model is specified THEN the agent SHALL default to Gemini
3. WHEN the agent is created THEN it SHALL not hardcode a specific model but use the parameter passed to it
4. WHEN the application starts THEN it SHALL display which model is being used

### Requirement 4

**User Story:** As a developer, I want a clean, minimal dependency list that only includes packages necessary for Windows and Gemini operation.

#### Acceptance Criteria

1. WHEN requirements.txt is processed THEN it SHALL only contain dependencies needed for Gemini and Windows operation
2. WHEN the application installs THEN it SHALL not install Azure OpenAI or unused cloud service packages
3. WHEN dependencies are analyzed THEN they SHALL be compatible with Windows systems
4. WHEN the application runs THEN it SHALL not import or reference removed dependencies

### Requirement 5

**User Story:** As a user, I want the application to maintain all existing automation capabilities while using the optimized Gemini-only setup.

#### Acceptance Criteria

1. WHEN automation tasks are performed THEN they SHALL work identically to the previous version
2. WHEN screen analysis is needed THEN the get_screen_info tool SHALL function correctly with Gemini
3. WHEN the GUI is displayed THEN it SHALL maintain the same functionality and appearance
4. WHEN PyAutoGUI operations execute THEN they SHALL have the same precision and reliability

### Requirement 6

**User Story:** As a developer, I want clear documentation that reflects the new Windows-optimized, Gemini-only setup.

#### Acceptance Criteria

1. WHEN the README is read THEN it SHALL only mention Gemini as the AI provider
2. WHEN installation instructions are followed THEN they SHALL be specific to Windows systems
3. WHEN environment setup is described THEN it SHALL only reference the GOOGLE_API_KEY variable
4. WHEN examples are shown THEN they SHALL reflect the simplified Gemini-only configuration
##
# Requirement 7

**User Story:** As a user, I want to see the currently selected AI model name displayed in the header and track token usage for each message and total usage.

#### Acceptance Criteria

1. WHEN the application starts THEN it SHALL display the current model name as a text label in the header
2. WHEN the model is changed in settings THEN the header label SHALL update to reflect the new model name
3. WHEN a message is sent or received THEN it SHALL display the token count for that specific message
4. WHEN tokens are used THEN the application SHALL maintain and display a running total of token usage
5. WHEN the application restarts THEN it SHALL persist and restore the total token usage count

### Requirement 8

**User Story:** As a user, I want to interact with the AI using voice commands and receive audio responses for a more natural conversation experience.

#### Acceptance Criteria

1. WHEN I speak to the application THEN it SHALL convert my speech to text and send it to the AI model
2. WHEN the AI responds THEN it SHALL convert the text response to speech and play it audibly
3. WHEN I enable speech mode THEN the AI SHALL both type and speak its responses
4. WHEN I disable speech mode THEN the AI SHALL only provide text responses
5. WHEN speech is muted for the model THEN it SHALL not play audio responses but continue speech recognition
6. WHEN speech recognition is active THEN it SHALL provide visual feedback indicating listening status

### Requirement 9

**User Story:** As a user, I want to see thumbnail images of screenshots taken by the AI in the chat display for better context and interaction.

#### Acceptance Criteria

1. WHEN the AI takes a screenshot THEN it SHALL display a small thumbnail image in the chat
2. WHEN I click on a screenshot thumbnail THEN it SHALL open the full-size image for viewing
3. WHEN screenshots are displayed THEN they SHALL be properly sized and formatted for the chat interface
4. WHEN multiple screenshots are taken THEN each SHALL be displayed as a separate thumbnail with timestamps
5. WHEN the chat is scrolled THEN screenshot thumbnails SHALL load efficiently without performance issues

### Requirement 10

**User Story:** As a user, I want to receive notifications when the AI completes tasks or processes to stay informed of progress.

#### Acceptance Criteria

1. WHEN the AI completes a task THEN it SHALL display a system notification
2. WHEN a process finishes THEN the notification SHALL include relevant completion details
3. WHEN notifications are shown THEN they SHALL not interfere with the main application workflow
4. WHEN multiple tasks complete THEN notifications SHALL be queued and displayed appropriately
5. WHEN the user is away THEN notifications SHALL persist until acknowledged

### Requirement 11

**User Story:** As a user, I want a modern, beautiful interface with Material Design 3 styling, dark/light themes, and improved visual design.

#### Acceptance Criteria

1. WHEN the application loads THEN it SHALL display a modern Material Design 3 interface
2. WHEN I switch themes THEN the application SHALL seamlessly transition between dark and light modes
3. WHEN scrolling is needed THEN scrollbars SHALL be hidden for a cleaner appearance
4. WHEN interacting with UI elements THEN they SHALL provide appropriate Material Design feedback and animations
5. WHEN the interface is displayed THEN it SHALL maintain consistent spacing, typography, and color schemes

### Requirement 12

**User Story:** As a user, I want comprehensive settings organized in tabs (AI, UI, About) with various customization options.

#### Acceptance Criteria

1. WHEN I open settings THEN it SHALL display tabbed interface with AI, UI, and About sections
2. WHEN in the AI tab THEN I SHALL be able to toggle model speech on/off
3. WHEN in the UI tab THEN I SHALL be able to switch between dark/light themes
4. WHEN in the UI tab THEN I SHALL be able to adjust screenshot image size via slider
5. WHEN in the UI tab THEN I SHALL be able to set screenshot wait duration (1-10 seconds)
6. WHEN in the About tab THEN I SHALL see application information, tips, and developer details

### Requirement 13

**User Story:** As a user, I want chat messages displayed in modern speech bubbles with proper alignment and interaction options.

#### Acceptance Criteria

1. WHEN messages are displayed THEN AI responses SHALL appear on the left in speech bubbles
2. WHEN messages are displayed THEN user messages SHALL appear on the right in speech bubbles
3. WHEN messages are shown THEN each SHALL have the sender name and timestamp above the bubble
4. WHEN viewing messages THEN each SHALL have resend, copy, and delete buttons below the bubble
5. WHEN I click message action buttons THEN they SHALL perform the appropriate action (resend, copy, delete)

### Requirement 14

**User Story:** As a user, I want the application to be rebranded as "JR AI Control" throughout all files and interfaces.

#### Acceptance Criteria

1. WHEN the application starts THEN it SHALL display "JR AI Control" as the application name
2. WHEN viewing any interface element THEN it SHALL reference "JR AI Control" instead of previous names
3. WHEN reading documentation THEN it SHALL consistently use "JR AI Control" branding
4. WHEN checking file headers and comments THEN they SHALL reflect the new application name
5. WHEN the application is installed THEN it SHALL appear as "JR AI Control" in system menus