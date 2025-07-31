# Speech2Text - MSI Installer Guide

## 📦 Creating MSI Installers

This guide covers creating professional MSI installers for Speech2Text that provide a complete Windows installation experience.

## 🚀 Quick Start

### Option 1: Simple MSI Builder (Recommended)
```bash
# Build MSI using WiX Toolset
python build_msi_simple.py
```

### Option 2: cx_Freeze MSI Builder
```bash
# Build MSI using cx_Freeze
python build_msi.py
```

### Option 3: Batch File
```bash
# Double-click or run:
build_msi.bat
```

## 📋 Prerequisites

### For WiX Toolset Method (Recommended)
1. **WiX Toolset v3.11+**
   - Download: https://wixtoolset.org/
   - Or install via winget: `winget install Microsoft.WiX`
   - Or install via chocolatey: `choco install wixtoolset`

2. **Python Dependencies** (auto-installed)
   ```bash
   uv add pyinstaller  # For building the EXE first
   ```

### For cx_Freeze Method
1. **cx_Freeze** (auto-installed by script)
   ```bash
   uv add cx_Freeze
   ```

## 🛠️ Build Process

### Method 1: WiX Toolset (build_msi_simple.py)

**Steps:**
1. **Build EXE**: Creates standalone executable using PyInstaller
2. **Generate WiX Config**: Creates speech2text.wxs with installer configuration
3. **Compile**: Uses `candle.exe` to compile WiX source
4. **Link**: Uses `light.exe` to create final MSI

**Features:**
- ✅ Professional Windows installer UI
- ✅ Start Menu and Desktop shortcuts
- ✅ Add/Remove Programs integration
- ✅ Upgrade support with proper GUIDs
- ✅ Option to launch after installation
- ✅ Registry entries for proper uninstall

### Method 2: cx_Freeze (build_msi.py)

**Steps:**
1. **Configure**: Creates setup_msi.py with cx_Freeze configuration
2. **Build EXE**: Creates executable with cx_Freeze
3. **Build MSI**: Generates MSI installer directly

**Features:**
- ✅ Python-native MSI creation
- ✅ All dependencies bundled
- ✅ Desktop shortcut creation
- ✅ Program Files installation

## 📁 Output Files

After building, you'll find:

```
dist/
├── Speech2Text.msi       # MSI installer (recommended for distribution)
├── Speech2Text.exe       # Standalone executable (backup option)
└── [other build files]
```

## 🎯 MSI Installer Features

### Installation Experience
- **Welcome Dialog**: Professional installer welcome screen
- **License Agreement**: MIT license display
- **Installation Directory**: Customizable install location (default: Program Files)
- **Feature Selection**: Choose components to install
- **Progress Display**: Real-time installation progress
- **Completion**: Option to launch application after install

### System Integration
- **Start Menu**: Creates "Speech2Text" program group
- **Desktop Shortcut**: Optional desktop shortcut
- **Add/Remove Programs**: Proper Windows uninstall support
- **Registry Entries**: Clean installation tracking
- **File Associations**: Future expansion capability

### Upgrade Support
- **Version Detection**: Detects existing installations
- **Upgrade Path**: Smooth upgrades without losing settings
- **Uninstall Cleanup**: Complete removal of all components

## 📊 File Sizes (Approximate)

| File Type | Size | Description |
|-----------|------|-------------|
| EXE (standalone) | ~31 MB | Single executable file |
| MSI (installer) | ~32 MB | Complete installer package |
| Installed Size | ~35 MB | After installation on disk |

## 🚀 Distribution

### For End Users
1. **Download**: Provide the `.msi` file
2. **Install**: Double-click to run installer
3. **Configure**: Enter OpenAI API key on first run
4. **Use**: Launch from Start Menu or Desktop

### For IT Deployment
```bash
# Silent installation
msiexec /i Speech2Text.msi /quiet

# Silent installation with log
msiexec /i Speech2Text.msi /quiet /l*v install.log

# Uninstall silently
msiexec /x Speech2Text.msi /quiet
```

## 🔧 Customization

### Modify Installation Settings
Edit `build_msi_simple.py` to customize:

```python
# Change installation directory
<Directory Id="INSTALLFOLDER" Name="YourAppName" />

# Modify shortcuts
<Shortcut Id="ApplicationStartMenuShortcut"
          Name="Your App Name"
          Description="Your Description" />

# Update product information
<Product Id="{GUID}" 
         Name="Your Product Name" 
         Manufacturer="Your Company" />
```

### Add Icons
1. Create `.ico` file
2. Place in project root
3. Update scripts:
   ```python
   icon="path/to/your/icon.ico"
   ```

### Custom Install Features
- **Multiple Components**: Add optional features
- **Custom Actions**: Run scripts during install/uninstall
- **System Requirements**: Check Windows version, .NET, etc.
- **License Agreement**: Custom license text

## 🛡️ Code Signing (Optional)

For professional distribution, sign your MSI:

```bash
# Using signtool.exe (Windows SDK)
signtool sign /f certificate.pfx /p password /t http://timestamp.server Speech2Text.msi
```

Benefits:
- ✅ Removes "Unknown Publisher" warnings
- ✅ Builds user trust
- ✅ Required for some corporate environments

## 🔍 Troubleshooting

### Common Issues

**"WiX Toolset not found"**
- Install WiX Toolset from https://wixtoolset.org/
- Ensure `candle.exe` and `light.exe` are in PATH

**"Build failed with exit code 1"**
- Check that `dist/Speech2Text.exe` exists
- Verify all file paths in WiX configuration
- Check Windows Event Viewer for detailed errors

**"MSI installation fails"**
- Run as Administrator
- Check Windows Installer service is running
- Verify sufficient disk space

**"Application won't start after install"**
- Check installed files in Program Files
- Verify all dependencies are included
- Test with antivirus temporarily disabled

### Debug Build Issues

```bash
# Verbose cx_Freeze build
python setup_msi.py build --verbose

# WiX verbose output
candle speech2text.wxs -v
light speech2text.wixobj -v
```

## 📈 Version Management

### Update Version Numbers
1. Update `pyproject.toml`:
   ```toml
   version = "0.2.0"
   ```

2. Update build scripts:
   ```python
   version = "0.2.0"
   ```

3. Generate new upgrade GUID for major versions

### Release Process
1. **Test**: Verify application works
2. **Build**: Create new MSI
3. **Test Install**: Test on clean system
4. **Sign**: Code sign if needed
5. **Distribute**: Upload to release platform

## 🆘 Support

### Build Issues
- Check Python version compatibility
- Verify all dependencies installed
- Review build script error messages

### Installation Issues
- Test on multiple Windows versions
- Check antivirus software compatibility
- Verify system requirements met

### Runtime Issues
- Include all required DLLs
- Test with minimal Windows installation
- Check OpenAI API connectivity

## 📄 License

MSI installer inherits the MIT license from the main application.

---

**Next Steps**: After creating your MSI, test it on a clean Windows system to ensure proper installation and functionality.