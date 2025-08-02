# 🚀 VoiceForge Release Guide

This guide explains how to create releases with installers for VoiceForge.

## 📋 Prerequisites

Before creating a release, ensure you have:

1. **All changes committed** to the main branch
2. **Updated version** in `package.json`
3. **Updated CHANGELOG.md** (if you have one)
4. **All tests passing**
5. **GitHub repository** properly configured

## 🏷️ Creating a Git Tag

### Option 1: Command Line (Recommended)

1. **Commit all changes:**
   ```bash
   git add .
   git commit -m "Prepare release v1.0.0"
   ```

2. **Create annotated tag:**
   ```bash
   git tag -a v1.0.0 -m "VoiceForge v1.0.0 - Transform your voice into text with professional accuracy and style

   🎤 VoiceForge v1.0.0 Release
   
   Major features:
   - Real-time speech-to-text with OpenAI Whisper API
   - Professional macOS Dark theme interface
   - Live audio visualization
   - Activity history with persistent storage
   - Comprehensive settings panel
   - Global keyboard shortcuts
   
   Full changelog: https://github.com/your-username/voiceforge/releases/tag/v1.0.0"
   ```

3. **Push tag to GitHub:**
   ```bash
   git push origin v1.0.0
   ```

### Option 2: GitHub Web Interface

1. Go to your repository on GitHub
2. Click **"Releases"** in the right sidebar
3. Click **"Create a new release"**
4. Enter tag version: `v1.0.0`
5. Add release title: `VoiceForge v1.0.0`
6. Add release description (see template below)

## 🤖 Automated Release (GitHub Actions)

The repository includes a GitHub Actions workflow that automatically:

1. **Triggers on tag push** (when you push a tag like `v1.0.0`)
2. **Builds for all platforms** (Windows, macOS, Linux)
3. **Creates installers** for each platform
4. **Uploads to GitHub Releases** automatically

### What Gets Built:

#### Windows:
- **NSIS Installer** (`.exe`) - Full installer with start menu shortcuts
- **Portable** (`.exe`) - Standalone executable

#### macOS:
- **DMG** (`.dmg`) - Drag-and-drop installer for Intel and Apple Silicon

#### Linux:
- **AppImage** (`.AppImage`) - Universal Linux application
- **DEB Package** (`.deb`) - Debian/Ubuntu installer

## 🛠️ Manual Release (Local Build)

If you prefer to build locally:

### 1. Install Dependencies
```bash
npm install
```

### 2. Build for All Platforms
```bash
# Build for current platform
npm run dist

# Build for all platforms (requires platform-specific tools)
npm run dist-all

# Build for specific platform
npm run dist -- --win    # Windows
npm run dist -- --mac    # macOS  
npm run dist -- --linux  # Linux
```

### 3. Upload to GitHub Releases

1. Go to **GitHub → Releases → Create New Release**
2. Enter tag version (e.g., `v1.0.0`)
3. Upload the generated installer files from `dist-electron/`
4. Add release notes

## 📝 Release Notes Template

```markdown
# 🎤 VoiceForge v1.0.0

> Transform your voice into text with professional accuracy and style

## ✨ What's New

### 🎯 Core Features
- Real-time speech recognition powered by OpenAI Whisper API
- Professional macOS Dark theme interface with glassmorphism effects
- Live audio visualization with frequency analysis
- Activity history with persistent storage and one-click copy
- Usage statistics tracking (requests, costs, sessions)

### 🎨 Interface
- Seamless design with no harsh borders or edges
- Smooth animations and micro-interactions
- Responsive layout that adapts to window sizes
- Enhanced typography and visual hierarchy

### 🔧 Advanced Features
- Comprehensive settings panel with 5 categories
- Global keyboard shortcuts (Ctrl+Super+Space)
- Auto-save functionality with multiple formats (TXT, MD, JSON)
- Secure encrypted storage for API keys
- Multi-language support with auto-detection

## 📦 Downloads

### Windows
- **[VoiceForge-Setup-1.0.0.exe](link)** - Full installer with shortcuts
- **[VoiceForge-1.0.0-portable.exe](link)** - Portable version

### macOS
- **[VoiceForge-1.0.0.dmg](link)** - Universal installer (Intel + Apple Silicon)

### Linux
- **[VoiceForge-1.0.0.AppImage](link)** - Universal Linux application
- **[VoiceForge-1.0.0.deb](link)** - Debian/Ubuntu package

## 🚀 Quick Start

1. **Download** the installer for your platform
2. **Install** VoiceForge
3. **Get an OpenAI API key** from [platform.openai.com](https://platform.openai.com)
4. **Open Settings** (⚙️) and add your API key
5. **Start recording** by clicking the audio visualizer

## 🔧 System Requirements

- **Windows:** Windows 10/11 (x64/x86)
- **macOS:** macOS 10.15+ (Intel/Apple Silicon)
- **Linux:** Ubuntu 18.04+ or equivalent (x64)
- **Memory:** 256MB RAM minimum
- **Storage:** 100MB free space
- **Network:** Internet connection for API calls

## 🐛 Bug Fixes

- Fixed duplicate title bar issue
- Improved settings modal centering
- Optimized audio indicator size for better text display
- Enhanced form layouts and spacing

## 📚 Documentation

- [Installation Guide](https://github.com/your-username/voiceforge#installation)
- [User Manual](https://github.com/your-username/voiceforge#how-to-use)
- [Settings Reference](https://github.com/your-username/voiceforge#settings-reference)
- [Keyboard Shortcuts](https://github.com/your-username/voiceforge#keyboard-shortcuts)

## 🔐 Security Notes

- All data stays on your device
- API keys are encrypted locally
- No telemetry or usage data sent to external servers
- Open source and fully auditable

## ❤️ Acknowledgments

Special thanks to:
- OpenAI for the incredible Whisper API
- Electron team for the cross-platform framework
- All contributors who helped make this release possible

---

**Full Changelog:** [v0.2.0...v1.0.0](https://github.com/your-username/voiceforge/compare/v0.2.0...v1.0.0)
```

## 🔧 Troubleshooting Release Issues

### Build Fails on GitHub Actions

1. **Check Node.js version** in workflow file
2. **Verify dependencies** are correctly listed in package.json
3. **Check build logs** in the Actions tab
4. **Ensure secrets are set** (for code signing)

### Missing Platform Builds

1. **Check matrix configuration** in `.github/workflows/release.yml`
2. **Verify electron-builder config** for each platform
3. **Check if platform-specific assets exist** (icons, etc.)

### Code Signing Issues

#### Windows:
- Need a code signing certificate
- Set `CSC_LINK` and `CSC_KEY_PASSWORD` secrets

#### macOS:
- Need Apple Developer account
- Set `APPLE_ID`, `APPLE_ID_PASS`, and certificate secrets
- Enable notarization for distribution

### File Size Issues

- **Enable compression** in electron-builder config
- **Exclude unnecessary files** from the build
- **Use asar archiving** for better compression

## 🎯 Best Practices

1. **Test before tagging** - Always test builds locally first
2. **Use semantic versioning** - Follow major.minor.patch format
3. **Write good release notes** - Include what's new, fixed, and changed
4. **Include checksums** - For security verification
5. **Sign releases** - Use code signing for trust
6. **Test installers** - Verify they work on clean systems

## 📋 Release Checklist

- [ ] All features tested and working
- [ ] Version updated in package.json
- [ ] Release notes prepared
- [ ] Git tag created and pushed
- [ ] GitHub Actions build completed successfully
- [ ] Installers downloaded and tested
- [ ] Release published on GitHub
- [ ] Social media announcements (optional)
- [ ] Documentation updated

---

## 🆘 Need Help?

- 📖 [Full Documentation](https://github.com/your-username/voiceforge#readme)
- 🐛 [Report Issues](https://github.com/your-username/voiceforge/issues)
- 💬 [Discussions](https://github.com/your-username/voiceforge/discussions)