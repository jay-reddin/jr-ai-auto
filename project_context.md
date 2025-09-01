# Clevrr Computer - Project Analysis & Migration Context

## Current State Analysis

### Architecture Overview
The Clevrr Computer is a multi-modal AI automation agent that:
- Uses PyAutoGUI for system automation (mouse, keyboard, screen interactions)
- Employs LangChain framework for agent orchestration
- Supports both Azure OpenAI and Google Gemini models
- Has a Tkinter-based floating UI for user interaction
- Takes screenshots with coordinate grids for visual understanding

### Current Code Structure
```
├── main.py                 # Entry point with GUI and argument parsing
├── utils/
│   ├── agent.py           # Agent creation and executor setup
│   ├── contants.py        # Model configurations and UI constants
│   ├── prompt.py          # Prompt template construction
│   └── tools.py           # Screen capture and analysis tools
├── requirements.txt       # Dependencies (mixed OpenAI/Gemini)
├── .env_dev              # Environment variables template
└── README.md             # Documentation
```

### Current Dependencies Analysis
**LLM/AI Related:**
- langchain (0.2.11) - Core framework
- langchain-openai (0.1.19) - Azure OpenAI integration
- langchain-google-genai (1.0.8) - Gemini integration
- openai (1.37.1) - OpenAI client
- google-generativeai (0.7.2) - Gemini client

**System Automation:**
- pyautogui (0.9.54) - Cross-platform automation
- PIL/Pillow (via dependencies) - Image processing

**UI:**
- tkinter (built-in Python) - GUI framework

### Platform Compatibility Issues Identified

#### Windows-Specific Concerns:
1. **PyAutoGUI**: Generally cross-platform but may need Windows-specific configurations
2. **Font Loading**: `arial.ttf` path in tools.py may not work on all Windows systems
3. **Screenshot Handling**: Should work on Windows but needs testing
4. **Hotkey Combinations**: Some key combinations might differ on Windows

#### Current Issues Found:
1. **Agent Creation Bug**: In `agent.py`, line 15 hardcodes `MODELS["openai"]` instead of using the passed model parameter
2. **Mixed Dependencies**: Both OpenAI and Gemini dependencies present even when only one is needed
3. **Environment Variables**: Azure-specific variables not needed if going Gemini-only

## Planned Changes

### 1. Platform Optimization for Windows
- Update font loading to use Windows-compatible fonts
- Test and optimize PyAutoGUI settings for Windows
- Ensure proper Windows key handling

### 2. Gemini-Only Migration
- Remove all Azure OpenAI dependencies and code
- Simplify model configuration to Gemini-only
- Update environment variables to only include Gemini API key
- Fix agent creation bug to properly use Gemini model

### 3. Code Structure Improvements
- Fix the hardcoded model bug in agent.py
- Clean up unused imports and dependencies
- Optimize requirements.txt for Windows + Gemini only
- Update documentation to reflect changes

### 4. Dependencies to Remove
- langchain-openai
- openai
- Azure-related packages
- Unused Google Cloud packages (if any)

### 5. Dependencies to Keep/Update
- langchain-google-genai (Gemini integration)
- google-generativeai (Gemini client)
- pyautogui (system automation)
- tkinter (GUI - built-in)
- PIL/Pillow (image processing)

## Next Steps
1. Create a spec for the migration project
2. Update requirements.txt for Windows + Gemini-only
3. Remove Azure OpenAI code and configurations
4. Fix agent creation bug
5. Test Windows compatibility
6. Update documentation