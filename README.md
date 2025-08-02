# 🎤 VoiceForge

> **Transform your voice into text with professional accuracy and style**

VoiceForge is a powerful, modern desktop application for real-time speech-to-text transcription using OpenAI's cutting-edge Whisper API. Built with Electron and featuring a sleek macOS Dark-inspired interface, VoiceForge makes voice transcription effortless and professional.

![Electron](https://img.shields.io/badge/electron-28.0+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)

## ✨ Features

### 🎯 **Core Functionality**
- **Real-time Speech Recognition** - Powered by OpenAI Whisper API
- **High-Quality Transcription** - Professional-grade accuracy
- **Multi-language Support** - Auto-detect or choose from 10+ languages
- **Voice Activity Detection** - Smart recording start/stop
- **Live Audio Visualization** - Real-time frequency analysis

### 🎨 **Modern Interface**
- **macOS Dark Theme** - Sleek, professional appearance
- **Glassmorphism Effects** - Beautiful backdrop blur and transparency
- **Seamless Design** - No harsh borders or edges
- **Responsive Layout** - Adapts to different window sizes
- **Smooth Animations** - Polished micro-interactions

### 🔧 **Advanced Features**
- **Activity History** - Persistent transcription history with one-click copy
- **Usage Statistics** - Track your requests, costs, and sessions
- **Auto-Save** - Automatic saving to various formats (TXT, MD, JSON)
- **Customizable Settings** - Audio quality, model selection, and more
- **Global Shortcuts** - Control recording from anywhere
- **Secure Storage** - Encrypted local storage for API keys

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v16 or higher)
- **npm** or **yarn**
- **OpenAI API Key** (get one at [platform.openai.com](https://platform.openai.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/voiceforge.git
   cd voiceforge
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Configure your API key**
   - Open VoiceForge
   - Click the ⚙️ Settings button
   - Navigate to "API Settings"
   - Enter your OpenAI API key
   - Click "Test" to verify

## 🎮 How to Use

### First Time Setup

1. **Launch VoiceForge**
2. **Configure API Settings:**
   - Go to Settings → API Settings
   - Paste your OpenAI API key
   - Test the connection
   - Save changes

3. **Adjust Audio Settings (Optional):**
   - Go to Settings → Audio
   - Choose sample rate (44100 Hz recommended)
   - Enable noise suppression and echo cancellation if needed

4. **Set Output Preferences (Optional):**
   - Go to Settings → Auto-Save
   - Choose save directory and file format
   - Enable automatic saving if desired

### Recording and Transcription

#### Method 1: Click to Record
1. Click the **audio visualizer circle** at the bottom
2. Speak clearly into your microphone
3. Click again to stop recording
4. Your transcription will appear in the main text area

#### Method 2: Global Shortcuts
- **Ctrl + Super + Space** (Windows/Linux) - Toggle recording
- **Cmd + Ctrl + Space** (macOS) - Toggle recording
- **Escape** - Stop recording immediately

#### Method 3: Menu Controls
- Use the **Recording** menu for start/stop options
- Access via the application menu bar

### Managing Transcriptions

#### Viewing Results
- Transcribed text appears in the main text area
- Scroll through longer transcriptions
- Text is automatically selected for easy copying

#### Activity History
- View all past transcriptions in the right panel
- Click any history item to copy the full text
- Use the "Clear" button to reset history

#### Saving Transcriptions
- **Manual Save:** Ctrl + S or File → Save Text
- **Auto-Save:** Enable in Settings → Auto-Save
- **Copy to Clipboard:** Click history items

## ⚙️ Settings Reference

### 🔑 API Settings
- **API Key:** Your OpenAI API key (stored securely)
- **Model:** Whisper v1 (currently available)
- **Language:** Auto-detect or specific language
- **Temperature:** Creativity level (0 = precise, 1 = creative)
- **Custom Prompt:** Context to improve accuracy

### 🎤 Audio Settings
- **Sample Rate:** 
  - 44100 Hz - CD Quality (Recommended)
  - 22050 Hz - Standard Quality
  - 16000 Hz - Speech Optimized
- **Buffer Size:** Processing chunk size
- **Noise Suppression:** Reduce background noise
- **Echo Cancellation:** Remove room acoustics

### 💾 File Management
- **Auto-Save:** Automatically save each transcription
- **Save Directory:** Choose where files are saved
- **File Format:** TXT, Markdown, or JSON
- **Filename Template:** Use variables like {{timestamp}}

### 🎨 Appearance
- **Theme:** Dark theme (Light theme coming soon)
- **Window Size:** Default application dimensions
- **Accessibility:** Reduce animations, high contrast

## ⌨️ Keyboard Shortcuts

### Global (Work Anywhere)
| Shortcut | Action |
|----------|--------|
| `Ctrl + Super + Space` | Toggle Recording |
| `Cmd + Ctrl + Space` | Toggle Recording (macOS) |

### Application
| Shortcut | Action |
|----------|--------|
| `Ctrl + N` | Start/Stop Recording |
| `Escape` | Stop Recording |
| `Ctrl + S` | Save Text |
| `Ctrl + ,` | Open Settings |
| `F1` | Show About Dialog |

## 📊 Usage Statistics

VoiceForge tracks your usage to help you monitor:

- **Requests Today:** Number of transcriptions
- **Estimated Cost:** Approximate API costs
- **Total Sessions:** Lifetime transcription count

*All statistics are stored locally and never shared.*

## 🛠️ Development

### Project Structure
```
voiceforge/
├── electron/           # Main process files
│   ├── main.js        # Electron main process
│   └── preload.js     # Preload script
├── renderer/          # Renderer process files
│   ├── index.html     # Main HTML
│   ├── src/
│   │   ├── js/        # JavaScript modules
│   │   └── styles/    # CSS stylesheets
├── assets/            # Static assets
├── build-electron.bat # Build script
└── package.json       # Project configuration
```

### Available Scripts

```bash
# Development
npm run dev              # Start development server
npm run electron-dev     # Start Electron in dev mode

# Building
npm run build           # Build for production
npm run build-renderer  # Build renderer only
npm run build-main      # Build main process only

# Distribution
npm run pack           # Package without installer
npm run dist           # Create installer
npm run dist-all       # Build for all platforms
```

### Technologies Used

- **Electron** - Cross-platform desktop framework
- **OpenAI Whisper API** - Speech recognition
- **Web Audio API** - Audio processing and visualization
- **CSS Custom Properties** - Design system
- **LocalStorage** - Data persistence
- **IPC** - Inter-process communication

## 🔐 Privacy & Security

- **Local Storage:** All data stays on your device
- **Encrypted Keys:** API keys are encrypted locally
- **No Telemetry:** No usage data is sent to external servers
- **Open Source:** Fully auditable codebase

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

VoiceForge is open source software licensed under the [MIT License](LICENSE).

## 🆘 Support

### Common Issues

**Q: My API key isn't working**
- Verify you have credits in your OpenAI account
- Check the API key is correctly copied (no extra spaces)
- Ensure you have access to the Whisper API

**Q: Audio isn't being detected**
- Check microphone permissions in your system settings
- Try a different sample rate in Audio Settings
- Ensure your microphone is the default recording device

**Q: Global shortcuts don't work**
- Try the alternative shortcut (Ctrl + Alt + Space)
- Check if another application is using the same shortcut
- Restart the application

**Q: Poor transcription quality**
- Use a higher sample rate (44100 Hz)
- Enable noise suppression
- Speak closer to the microphone
- Add context via custom prompts

### Getting Help

- 📖 Check this README for detailed instructions
- 🐛 [Report bugs](https://github.com/your-username/voiceforge/issues)
- 💡 [Request features](https://github.com/your-username/voiceforge/issues)
- 💬 [Join discussions](https://github.com/your-username/voiceforge/discussions)

## 🏆 Acknowledgments

- **OpenAI** for the incredible Whisper API
- **Electron** team for the cross-platform framework
- **Contributors** who help improve VoiceForge

---

<div align="center">

**Made with ❤️ by the VoiceForge team**

*Transform your voice into text with professional accuracy and style*

</div>