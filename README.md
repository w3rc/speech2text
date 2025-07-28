# Speech2Text

A modern Windows desktop application for real-time speech-to-text transcription using OpenAI's Whisper API.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

## Features

- **Real-time Speech Recognition**: High-quality transcription using OpenAI Whisper API
- **User-friendly GUI**: Clean, intuitive interface built with tkinter
- **Secure Settings**: API key management through encrypted local storage
- **Audio Recording**: Direct microphone input with customizable parameters
- **Text Management**: Save, clear, and export transcribed text
- **Error Handling**: Comprehensive error handling with user-friendly feedback
- **Cross-session Persistence**: Settings saved between application sessions

## Quick Start

### Prerequisites

- **Python 3.13+** installed on your system
- **uv** package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- **OpenAI API key** ([get one here](https://platform.openai.com/api-keys))
- **Working microphone** for audio input

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/speech2text.git
   cd speech2text
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Run the application**
   ```bash
   uv run python speech_to_text_app.py
   ```

4. **Configure your API key**
   - Go to Settings > API Configuration
   - Enter your OpenAI API key
   - Click Save

## Usage

1. **Start the application** and configure your OpenAI API key in Settings
2. **Click "Start Recording"** and speak clearly into your microphone
3. **Click "Stop Recording"** when finished speaking
4. **View the transcription** in the text area
5. **Save or clear** the text as needed

### Keyboard Shortcuts

- `Ctrl+N` - Start new recording
- `Ctrl+S` - Save text to file
- `Ctrl+,` - Open Settings
- `F1` - Show Help/About

## Configuration

The application stores settings in a local configuration file:
- **Windows**: `%APPDATA%\Speech2Text\config.json`

### Configurable Options

- **API Key**: Your OpenAI API key (encrypted storage)
- **Audio Quality**: Sample rate and channels
- **Output Format**: Text formatting preferences
- **Recording Settings**: Buffer size and audio parameters

## Development

### Project Structure

```
speech2text/
├── speech_to_text_app.py   # Main application
├── settings.py             # Configuration management
├── settings_dialog.py      # Settings UI
├── pyproject.toml         # Project configuration
├── README.md              # This file
├── LICENSE                # MIT license
├── CONTRIBUTING.md        # Contribution guidelines
└── CHANGELOG.md           # Version history
```

### Setting up Development Environment

1. **Fork and clone** the repository
2. **Install development dependencies**
   ```bash
   uv sync --dev
   ```
3. **Run tests**
   ```bash
   uv run pytest
   ```
4. **Run the application in development mode**
   ```bash
   uv run python speech_to_text_app.py
   ```

### Code Style

This project follows:
- **PEP 8** for Python code style
- **Type hints** for better code documentation
- **Docstrings** for all public functions and classes

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Ways to Contribute

- Report bugs by opening an issue
- Suggest features via feature requests
- Submit pull requests for bug fixes or improvements
- Improve documentation and examples
- Add translations for internationalization

## Requirements

### System Requirements

- **Operating System**: Windows 10/11 (primary), macOS/Linux (experimental)
- **Python**: 3.13 or higher
- **Memory**: 256MB RAM minimum
- **Storage**: 50MB free space
- **Network**: Internet connection for API calls

### Python Dependencies

- `openai` - OpenAI API client
- `pyaudio` - Audio recording and playback
- `cryptography` - Secure settings storage
- `tkinter` - GUI framework (included with Python)

## Privacy & Security

- **API Key Security**: Keys are encrypted and stored locally
- **Audio Privacy**: Audio is processed by OpenAI's API (see their privacy policy)
- **Local Storage**: No audio files are permanently stored on your device
- **Network**: Only API calls to OpenAI servers, no other external connections

## API Usage & Costs

This application uses OpenAI's Whisper API:
- **Pricing**: $0.006 per minute of audio
- **Rate Limits**: Varies by account type
- **Supported Formats**: WAV, MP3, M4A, and more
- **Maximum File Size**: 25MB per request

## Troubleshooting

### Common Issues

**"No API key configured"**
- Go to Settings and enter your OpenAI API key
- Ensure the key starts with `sk-`
- Check your internet connection

**"Audio device error"**
- Check microphone permissions in Windows settings
- Ensure no other application is using the microphone
- Try running as administrator if needed

**"PyAudio installation failed"**
```bash
# On Windows, try:
uv add --dev pipwin
uv run pipwin install pyaudio
```

For more issues, check our [Issues page](https://github.com/yourusername/speech2text/issues).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OpenAI** for providing the Whisper API
- **Python community** for excellent libraries
- **Contributors** who help improve this project

## Support

- Email: support@yourproject.com
- Discussions: [GitHub Discussions](https://github.com/yourusername/speech2text/discussions)
- Bug Reports: [GitHub Issues](https://github.com/yourusername/speech2text/issues)

---

**Made with care for the open source community**