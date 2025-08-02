# Speech2Text Electron Application

This is the Electron version of Speech2Text, providing a modern cross-platform desktop application for real-time speech-to-text transcription using OpenAI Whisper API.

## Features

- **Modern UI**: Clean, dark-themed interface built with HTML/CSS/JavaScript
- **Cross-platform**: Runs on Windows, macOS, and Linux
- **Real-time Audio**: Live audio level monitoring and voice activity detection
- **Secure Settings**: Encrypted settings storage using electron-store
- **Global Shortcuts**: System-wide hotkeys for recording control
- **Activity History**: Track and manage transcription history
- **Auto-save**: Automatic transcript saving with configurable options
- **Menu Integration**: Native menu bar with full functionality

## Architecture

### File Structure
```
├── electron/
│   ├── main.js          # Main Electron process
│   └── preload.js       # Preload script for secure IPC
├── renderer/
│   ├── index.html       # Main UI
│   └── src/
│       ├── styles/      # CSS styles
│       └── js/          # JavaScript logic
├── assets/              # Application assets
├── package.json         # Dependencies and scripts
└── webpack.*.js         # Build configuration
```

### Main Process (`electron/main.js`)
- Window management and lifecycle
- Settings storage with encryption
- OpenAI API integration
- Global keyboard shortcuts
- File operations and dialogs
- IPC communication handling

### Renderer Process (`renderer/`)
- Modern web-based UI
- Audio recording and visualization
- Real-time transcription display
- Settings management interface
- Activity history tracking

### Security
- Context isolation enabled
- Node integration disabled
- Secure IPC communication via preload script
- Encrypted settings storage

## Getting Started

### Prerequisites
- Node.js 16 or higher
- npm or yarn package manager
- Microphone access for audio recording

### Installation & Development

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Development Mode**
   ```bash
   # Start development server
   npm run dev
   
   # Or run Electron directly
   npm run electron
   ```

3. **Build for Production**
   ```bash
   # Build renderer and main process
   npm run build
   
   # Create distribution packages
   npm run dist
   
   # Or use the batch script (Windows)
   build-electron.bat
   ```

### Configuration

1. **OpenAI API Key**: Configure in Settings panel (⚙️ button)
2. **Audio Settings**: Adjust sample rate and quality
3. **Output Settings**: Configure auto-save and file formats
4. **Global Shortcuts**: Ctrl+Win+Space (Windows) / Cmd+Ctrl+Space (macOS)

## Usage

### Recording Controls
- **Start/Stop Recording**: Click audio meter or Ctrl+N
- **Global Hotkey**: Ctrl+Win+Space (configurable)
- **Stop Recording**: Escape key
- **Visual Feedback**: Audio level meter and status indicators

### Text Management
- **Auto-copy**: Transcriptions automatically copied to clipboard
- **Save Text**: Ctrl+S or File menu
- **Activity History**: Click history items to copy full text
- **Auto-save**: Configurable in settings

### Keyboard Shortcuts
- `Ctrl+N`: Toggle recording
- `Ctrl+S`: Save transcription
- `Ctrl+,`: Open settings
- `Escape`: Stop recording
- `F1`: Show keyboard shortcuts
- `Ctrl+Win+Space`: Global toggle (Windows)

## Original Python App Migration

This Electron version maintains full compatibility with the original Python/tkinter application:

### Migrated Features
✅ **UI Components**: All original UI elements recreated in HTML/CSS
✅ **Audio Recording**: Web Audio API replaces PyAudio
✅ **Real-time Visualization**: Audio level meter with voice detection
✅ **Settings Management**: Secure storage replaces Python settings
✅ **Global Hotkeys**: System-wide shortcuts maintained
✅ **Dark Theme**: Consistent dark theme styling
✅ **Activity History**: Enhanced with clickable history items
✅ **Auto-save**: Configurable automatic saving
✅ **Clipboard Integration**: Auto-copy functionality
✅ **Error Handling**: Comprehensive error management
✅ **Window Management**: Proper window state persistence

### Enhanced Features
🚀 **Cross-platform**: Better OS integration than Python version
🚀 **Performance**: Faster startup and lower memory usage
🚀 **Modern UI**: More responsive and polished interface
🚀 **Security**: Encrypted settings and secure IPC
🚀 **Distribution**: Easy packaging for all platforms
🚀 **Updates**: Auto-updater support ready

## Build Scripts

### Available Scripts
```bash
npm run electron         # Run in development
npm run electron-dev     # Run with dev tools
npm run build           # Build for production
npm run build-renderer  # Build renderer only
npm run build-main      # Build main process only
npm run pack           # Package without installer
npm run dist           # Create distribution packages
npm run dist-all       # Build for all platforms
```

### Platform-specific Building
```bash
# Windows
npm run dist -- --win

# macOS
npm run dist -- --mac

# Linux
npm run dist -- --linux
```

## Troubleshooting

### Common Issues

1. **Microphone Access Denied**
   - Grant microphone permissions in system settings
   - Restart the application after granting permissions

2. **API Key Not Working**
   - Verify OpenAI API key in Settings
   - Check internet connection
   - Ensure API key has proper permissions

3. **Recording Not Starting**
   - Check microphone is not in use by other applications
   - Verify audio settings in the Settings panel
   - Try different sample rates

4. **Build Errors**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Update Node.js to latest LTS version
   - Check webpack configuration for missing dependencies

## Contributing

This Electron version maintains the same contribution guidelines as the original Python application. See CONTRIBUTING.md for details.

## License

MIT License - same as the original Python application.

---

**Migration Complete**: All original functionality has been successfully migrated to Electron with enhanced features and better cross-platform support.