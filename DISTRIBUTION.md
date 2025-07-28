# Speech2Text - Distribution Guide

## 📦 Creating the Executable

### Quick Build
Double-click `build.bat` or run:
```bash
uv run python build_exe.py
```

### Manual Build
```bash
# Install PyInstaller (already included in dependencies)
uv add pyinstaller

# Build the executable
uv run python build_exe.py
```

## 📁 Distribution Files

After building, you'll find:
- `dist/Speech2Text.exe` - The standalone executable (30.9 MB)

## 🚀 How to Distribute

### Single File Distribution
1. Copy `Speech2Text.exe` from the `dist` folder
2. Send it to any Windows computer (Windows 10/11)
3. No Python installation required!

### What Users Need
- **Windows 10 or 11** (64-bit)
- **Internet connection** (for OpenAI API calls)
- **OpenAI API key** (get from https://platform.openai.com/api-keys)
- **Microphone** (for speech input)

## 📋 User Instructions

### First Run
1. Double-click `Speech2Text.exe`
2. Click the ⚙️ (Settings) button
3. Enter your OpenAI API key in the "🔑 API" tab
4. Click "OK" to save

### Usage
- **Click "🎤 Start Recording"** to begin speech-to-text
- **Press Ctrl+Win** anywhere on your system to toggle recording
- **Real-time audio visualization** shows voice detection
- **Activity history** tracks all transcriptions
- **Settings**: Configure language, audio quality, output format

### Features Included
- ✅ Modern dark theme interface
- ✅ Real-time audio level monitoring
- ✅ Global hotkey (Ctrl+Win) for system-wide recording
- ✅ English transcription by default (configurable)
- ✅ Secure encrypted settings storage
- ✅ Activity history with timestamps
- ✅ Multiple language support
- ✅ Auto-save and manual save options
- ✅ Smooth animations and transitions

## 🔧 Troubleshooting

### Common Issues

**"Missing API Key" Error**
- Solution: Go to Settings → API tab → Enter your OpenAI API key

**"Recording Error" or No Audio**
- Solution: Check microphone permissions in Windows Settings
- Make sure microphone is not being used by another application

**Global Hotkey Not Working**
- Solution: Run as Administrator (right-click → "Run as administrator")
- Some systems may require elevated permissions for global hotkeys

**App Won't Start**
- Solution: Make sure Windows Defender/antivirus isn't blocking it
- Check Windows Event Viewer for detailed error messages

### System Requirements
- **OS**: Windows 10 (1809) or Windows 11
- **Architecture**: x64 (64-bit)
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 100MB free space
- **Internet**: Required for OpenAI API calls

## 🏗️ Build Details

- **PyInstaller Version**: 6.14.2
- **Python Version**: 3.13.5
- **Build Type**: One-file executable
- **Console**: Hidden (GUI only)
- **UPX Compression**: Enabled
- **File Size**: ~31 MB
- **Import Handling**: Fixed for PyInstaller packaging
- **All Modules**: Included via hiddenimports

## 📄 License

MIT License - Free to distribute and modify.

## 🆘 Support

For issues or questions:
1. Check this troubleshooting guide
2. Verify all requirements are met
3. Test with a simple voice recording first