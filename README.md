# JR AI Control

JR AI Control is an advanced automation agent designed to perform precise and efficient system actions on behalf of the user using the PyAutoGUI library. It can automate keyboard, mouse, and screen interactions while ensuring safety and accuracy in every task.

## Features

- **Windows-optimized automation** with mouse movements, clicks, and keyboard inputs
- **Google Gemini-powered** screen analysis and task execution
- **Simplified setup** with single API key requirement (Google API Key only)
- **Native Windows compatibility** with optimized font rendering and system interactions
- **Reduced memory footprint** with streamlined dependencies
- **Graceful error handling** and user feedback
- **Maximum precision** to avoid unintentional actions
- **Screenshot management** with coordinate grid overlay for accurate positioning

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
   VERSION=0.9.2
   LAST_CHANGES=["Migrated to Gemini-only operation", "Windows optimization", "Removed Azure OpenAI dependencies"]
   ```

   **Note:** This application now uses Google Gemini exclusively for optimal Windows performance and simplified setup.

## Usage

1. **Run the Application:**

   You can run the application using the following command:

   ```cmd
   python main.py
   ```

   This will use the Google Gemini model and enable the floating UI by default.

2. **Optional Arguments:**

    - **Model Selection:**
    The application now uses Google Gemini exclusively. You can explicitly specify the model if needed:

    ```cmd
    python main.py --model gemini
    ```

    - **Floating UI:**
    The TKinter UI will be floating and remain on top of the screen by default. You can disable this behavior by passing the `--float-ui` flag as `0`. By default it will be `1`.

    ```cmd
    python main.py --float-ui 0
    ```

### Windows-Specific Features

- **Optimized font rendering** for Windows systems
- **Windows-compatible PyAutoGUI operations** with proper key combinations
- **Reduced memory footprint** with streamlined dependencies
- **Native Windows font fallbacks** for coordinate grid display


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


## Troubleshooting (Windows)

### Common Issues

1. **Font rendering problems:**
   - The application automatically falls back to Windows system fonts if custom fonts are unavailable
   - Coordinate grids should display correctly with Arial or default Windows fonts

2. **PyAutoGUI issues:**
   - Ensure your Windows system allows automation (some security software may block it)
   - The application is optimized for Windows key combinations and screen handling

3. **API Key issues:**
   - Make sure your `GOOGLE_API_KEY` is valid and has access to Gemini models
   - Check that the `.env` file is in the root directory of the project

4. **Dependencies:**
   - If installation fails, try updating pip: `python -m pip install --upgrade pip`
   - Ensure you're using Python 3.8 or later

## Configuration Examples

### Basic .env file:
```plaintext
GOOGLE_API_KEY=your_actual_gemini_api_key_here
VERSION=0.9.2
LAST_CHANGES=["Migrated to Gemini-only operation", "Windows optimization", "Removed Azure OpenAI dependencies"]
```

### Running with different options:
```cmd
# Default run (Gemini model, floating UI)
python main.py

# Explicit Gemini model
python main.py --model gemini

# Disable floating UI
python main.py --float-ui 0

# Combine options
python main.py --model gemini --float-ui 0
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## Contact

For any questions or issues, please contact [yurvaj@getclevrr.com](mailto:yurvaj@getclevrr.com).
