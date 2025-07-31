"""Create a Windows installer using available tools."""

import sys
import os
import subprocess
from pathlib import Path
import shutil
import zipfile

def check_available_tools():
    """Check what installer creation tools are available."""
    tools = {}
    
    # Check for WiX Toolset
    try:
        subprocess.run(['candle', '-?'], capture_output=True, timeout=5)
        tools['wix'] = True
        print("[OK] WiX Toolset is available")
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        tools['wix'] = False
        print("[INFO] WiX Toolset not found")
    
    # Check for NSIS
    try:
        subprocess.run(['makensis', '/VERSION'], capture_output=True, timeout=5)
        tools['nsis'] = True
        print("[OK] NSIS is available")
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        tools['nsis'] = False
        print("[INFO] NSIS not found")
    
    # Check for cx_Freeze (even though MSI doesn't work on Python 3.13)
    try:
        import cx_Freeze
        tools['cx_freeze'] = True
        print(f"[OK] cx_Freeze {cx_Freeze.__version__} is available (MSI limited on Python 3.13)")
    except ImportError:
        tools['cx_freeze'] = False
        print("[INFO] cx_Freeze not found")
    
    return tools

def build_exe_first():
    """Build the EXE first using PyInstaller."""
    print("[STEP 1] Building executable with PyInstaller...")
    
    try:
        result = subprocess.run([
            sys.executable, 'build_exe.py'
        ], check=True, capture_output=True, text=True)
        
        exe_path = Path('dist/Speech2Text.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"[OK] Executable built: {exe_path} ({size_mb:.1f} MB)")
            return True
        else:
            print("[ERROR] Executable not found after build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] EXE build failed: {e}")
        return False

def create_portable_installer():
    """Create a simple portable installer package."""
    print("[STEP 2] Creating portable installer package...")
    
    # Create installer directory
    installer_dir = Path('installer_package')
    if installer_dir.exists():
        shutil.rmtree(installer_dir)
    installer_dir.mkdir()
    
    # Copy executable
    exe_src = Path('dist/Speech2Text.exe')
    exe_dst = installer_dir / 'Speech2Text.exe'
    shutil.copy2(exe_src, exe_dst)
    
    # Create install script
    install_script = installer_dir / 'install.bat'
    install_content = '''@echo off
echo ================================
echo   Speech2Text Installer
echo ================================
echo.

REM Create installation directory
set INSTALL_DIR=%ProgramFiles%\\Speech2Text
echo Creating installation directory: %INSTALL_DIR%
mkdir "%INSTALL_DIR%" 2>nul

REM Copy executable
echo Copying Speech2Text.exe...
copy "Speech2Text.exe" "%INSTALL_DIR%\\" >nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to copy files. Try running as Administrator.
    pause
    exit /b 1
)

REM Create desktop shortcut
echo Creating desktop shortcut...
set DESKTOP=%USERPROFILE%\\Desktop
echo Set WshShell = CreateObject("WScript.Shell") > create_shortcut.vbs
echo Set Shortcut = WshShell.CreateShortcut("%DESKTOP%\\Speech2Text.lnk") >> create_shortcut.vbs
echo Shortcut.TargetPath = "%INSTALL_DIR%\\Speech2Text.exe" >> create_shortcut.vbs
echo Shortcut.WorkingDirectory = "%INSTALL_DIR%" >> create_shortcut.vbs
echo Shortcut.Description = "Modern Speech-to-Text Application" >> create_shortcut.vbs
echo Shortcut.Save >> create_shortcut.vbs
cscript create_shortcut.vbs >nul
del create_shortcut.vbs

REM Create start menu shortcut
echo Creating start menu shortcut...
set STARTMENU=%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs
mkdir "%STARTMENU%\\Speech2Text" 2>nul
echo Set WshShell = CreateObject("WScript.Shell") > create_startmenu.vbs
echo Set Shortcut = WshShell.CreateShortcut("%STARTMENU%\\Speech2Text\\Speech2Text.lnk") >> create_startmenu.vbs
echo Shortcut.TargetPath = "%INSTALL_DIR%\\Speech2Text.exe" >> create_startmenu.vbs
echo Shortcut.WorkingDirectory = "%INSTALL_DIR%" >> create_startmenu.vbs
echo Shortcut.Description = "Modern Speech-to-Text Application" >> create_startmenu.vbs
echo Shortcut.Save >> create_startmenu.vbs
cscript create_startmenu.vbs >nul
del create_startmenu.vbs

REM Add to Windows registry for Add/Remove Programs
echo Adding to Windows registry...
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Speech2Text" /v "DisplayName" /t REG_SZ /d "Speech2Text" /f >nul 2>&1
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Speech2Text" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\\uninstall.bat" /f >nul 2>&1
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Speech2Text" /v "DisplayVersion" /t REG_SZ /d "0.1.0" /f >nul 2>&1
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Speech2Text" /v "Publisher" /t REG_SZ /d "Speech2Text Contributors" /f >nul 2>&1
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Speech2Text" /v "InstallLocation" /t REG_SZ /d "%INSTALL_DIR%" /f >nul 2>&1

REM Create uninstaller
echo Creating uninstaller...
echo @echo off > "%INSTALL_DIR%\\uninstall.bat"
echo echo Uninstalling Speech2Text... >> "%INSTALL_DIR%\\uninstall.bat"
echo del "%USERPROFILE%\\Desktop\\Speech2Text.lnk" 2^>nul >> "%INSTALL_DIR%\\uninstall.bat"
echo rmdir /s /q "%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\Speech2Text" 2^>nul >> "%INSTALL_DIR%\\uninstall.bat"
echo reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Speech2Text" /f ^>nul 2^>^&1 >> "%INSTALL_DIR%\\uninstall.bat"
echo cd /d "%TEMP%" >> "%INSTALL_DIR%\\uninstall.bat"
echo rmdir /s /q "%INSTALL_DIR%" >> "%INSTALL_DIR%\\uninstall.bat"
echo echo Speech2Text has been uninstalled. >> "%INSTALL_DIR%\\uninstall.bat"
echo pause >> "%INSTALL_DIR%\\uninstall.bat"

echo.
echo ================================
echo   Installation completed!
echo ================================
echo.
echo Speech2Text has been installed to: %INSTALL_DIR%
echo Desktop shortcut created
echo Start menu shortcut created
echo.
echo You can now:
echo - Launch from desktop shortcut
echo - Launch from Start Menu ^> Speech2Text
echo - Uninstall via Add/Remove Programs
echo.
pause
'''
    
    with open(install_script, 'w', encoding='utf-8') as f:
        f.write(install_content)
    
    # Create README
    readme_path = installer_dir / 'README.txt'
    readme_content = '''Speech2Text Installer Package
=============================

INSTALLATION INSTRUCTIONS:
1. Right-click "install.bat" and select "Run as administrator"
2. Follow the installation prompts
3. The app will be installed to Program Files
4. Desktop and Start Menu shortcuts will be created

WHAT YOU GET:
- Professional installation to Program Files
- Desktop shortcut
- Start Menu entry
- Add/Remove Programs integration
- Clean uninstall support

REQUIREMENTS:
- Windows 10 or 11 (64-bit)
- Administrator privileges for installation
- Internet connection (for OpenAI API)
- Microphone for speech input

FIRST RUN:
1. Launch Speech2Text from desktop or Start Menu
2. Click the Settings button
3. Enter your OpenAI API key
4. Start using speech-to-text!

SUPPORT:
If you encounter issues, try:
- Running the installer as Administrator
- Temporarily disabling antivirus
- Checking Windows Event Viewer for errors

This installer package provides the same functionality as an MSI
installer but works on all Python versions and Windows systems.
'''
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"[OK] Portable installer created in: {installer_dir.absolute()}")
    return True

def create_zip_distribution():
    """Create a ZIP file with the installer package."""
    print("[STEP 3] Creating ZIP distribution...")
    
    zip_path = Path('dist/Speech2Text_Installer.zip')
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        installer_dir = Path('installer_package')
        for file in installer_dir.rglob('*'):
            if file.is_file():
                arcname = file.relative_to(installer_dir)
                zipf.write(file, arcname)
    
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"[OK] ZIP installer created: {zip_path} ({size_mb:.1f} MB)")
    return True

def cleanup():
    """Clean up temporary files."""
    try:
        installer_dir = Path('installer_package')
        if installer_dir.exists():
            shutil.rmtree(installer_dir)
            print("[CLEAN] Removed temporary installer directory")
    except Exception as e:
        print(f"[WARNING] Could not clean up: {e}")

def provide_manual_instructions():
    """Provide instructions for manual installer creation."""
    print("\\n" + "="*50)
    print("   ALTERNATIVE INSTALLER OPTIONS")
    print("="*50)
    print("\\nSince MSI creation is limited on Python 3.13, here are alternatives:")
    print("\\n1. PORTABLE INSTALLER (Created)")
    print("   - Located in: dist/Speech2Text_Installer.zip")
    print("   - Extract and run install.bat as Administrator")
    print("   - Provides full Windows integration")
    print("\\n2. MANUAL MSI with WiX Toolset:")
    print("   - Install WiX Toolset: https://wixtoolset.org/")
    print("   - Or: winget install Microsoft.WiX")
    print("   - Then run: python build_msi_simple.py")
    print("\\n3. NSIS Installer (if available):")
    print("   - Install NSIS: https://nsis.sourceforge.io/")
    print("   - Create .nsi script for professional installer")
    print("\\n4. SIMPLE DISTRIBUTION:")
    print("   - Just distribute Speech2Text.exe from dist folder")
    print("   - Users run it directly (no installation needed)")

def main():
    """Main installer creation function."""
    print("[START] Creating Windows installer for Speech2Text...")
    print(f"[DIR] Working directory: {Path.cwd()}")
    
    # Check what tools are available
    tools = check_available_tools()
    
    # Build EXE first
    if not build_exe_first():
        print("[ERROR] Cannot create installer without executable")
        return
    
    # Create portable installer (always works)
    if create_portable_installer():
        create_zip_distribution()
        cleanup()
    
    # Provide additional options
    provide_manual_instructions()
    
    print("\\n[COMPLETE] Installer creation completed!")
    print("\\nYour distribution options:")
    print("- Speech2Text_Installer.zip (Portable installer)")
    print("- Speech2Text.exe (Standalone executable)")

if __name__ == "__main__":
    main()