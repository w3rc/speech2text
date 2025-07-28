# Changelog

All notable changes to Speech2Text will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite
- Continuous integration setup
- Multi-language support
- Dark mode theme
- Voice activity detection
- Real-time transcription display
- Export to multiple formats (PDF, DOCX)
- Keyboard shortcuts customization
- Audio preprocessing options
- Batch processing for multiple files

### Changed
- Improved error handling and user feedback
- Enhanced settings validation
- Better audio quality detection
- Optimized memory usage during recording

### Fixed
- Audio device selection on some Windows systems
- Settings persistence across application restarts
- Memory leaks in long recording sessions

## [0.1.0] - 2025-01-28

### Added
- **Core Features**
  - Real-time speech-to-text transcription using OpenAI Whisper API
  - Desktop GUI built with tkinter
  - Secure API key management with encrypted local storage
  - Configurable audio recording parameters (sample rate, channels, buffer size)
  - Multiple output formats (TXT, MD, RTF)
  - Auto-save functionality with timestamp-based filenames

- **User Interface**
  - Clean, intuitive main window with recording controls
  - Comprehensive settings dialog with tabbed interface
  - Menu bar with File, Settings, and Help menus
  - Keyboard shortcuts for common actions (Ctrl+N, Ctrl+S, Ctrl+,, F1)
  - Status indicators for API configuration and recording state
  - Scrollable text area for transcription display

- **Settings Management**
  - Encrypted API key storage using cryptography library
  - Persistent configuration with JSON-based settings file
  - Cross-platform config directory support (Windows/macOS/Linux)
  - Import/export settings functionality
  - Reset to defaults option
  - Settings validation and error handling

- **Audio Processing**
  - PyAudio integration for microphone recording
  - Configurable audio parameters (44.1kHz default, mono/stereo support)
  - Temporary file handling for API uploads
  - Automatic cleanup of temporary audio files
  - Support for various audio buffer sizes

- **File Management**
  - Save transcriptions with file dialog
  - Auto-save to configurable directory
  - Multiple file format support
  - Timestamp-based automatic naming
  - Configurable save directories

- **Developer Experience**
  - Modern Python packaging with pyproject.toml
  - uv package manager support
  - Type hints throughout codebase
  - Comprehensive docstrings
  - MIT license for open source distribution
  - Modular architecture with separate settings and UI components

- **Documentation**
  - Comprehensive README with installation and usage instructions
  - Contributing guidelines for open source development
  - Keyboard shortcuts help dialog
  - About dialog with project information
  - Inline code documentation

### Technical Details
- **Requirements**: Python 3.8+, OpenAI API key
- **Dependencies**: openai, pyaudio, cryptography, tkinter (built-in)
- **Platform Support**: Windows (primary), macOS/Linux (experimental)
- **Configuration**: ~/.config/speech2text/ or %APPDATA%/Speech2Text/
- **Security**: AES encryption for API keys, PBKDF2 key derivation

### Known Limitations
- Windows-focused (primary development platform)
- Requires stable internet connection for API calls
- Limited to OpenAI Whisper API (no local processing)
- No real-time streaming transcription
- Single audio input device support

---

## Version Format

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- **MAJOR**: Incompatible API changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## Release Process

1. Update version in `pyproject.toml`
2. Update this CHANGELOG.md
3. Create GitHub release with tag
4. Build and distribute packages

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.