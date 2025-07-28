"""Build script to create a standalone .exe file for Speech2Text application."""
import subprocess
import sys
import os
from pathlib import Path

def create_spec_file():
    """Create PyInstaller spec file with proper configuration."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=['.', 'src', 'src/speech2text'],
    binaries=[],
    datas=[
        ('src/speech2text/*.py', 'speech2text'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk', 
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'openai',
        'pyaudio',
        'cryptography',
        'cryptography.fernet',
        'numpy',
        'pynput',
        'pynput.keyboard',
        'pynput.mouse',
        'threading',
        'tempfile',
        'wave',
        'json',
        'base64',
        'hashlib',
        'pathlib',
        'ctypes',
        'ctypes.wintypes',
        'platform',
        'time',
        'datetime',
        'math',
        'os',
        'sys',
        'speech2text',
        'speech2text.modern_speech_app',
        'speech2text.settings',
        'speech2text.theme',
        'speech2text.audio_monitor', 
        'speech2text.global_hotkey',
        'speech2text.animations',
        'speech2text.modern_settings_dialog'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Speech2Text',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app (no console window)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add path to .ico file if you have one
    version_info={
        'version': '0.1.0',
        'description': 'Modern Speech-to-Text Application',
        'product_name': 'Speech2Text',
        'file_description': 'Speech2Text - Modern Desktop Application',
        'company_name': 'Speech2Text Contributors',
        'copyright': '(C) 2025 Speech2Text Contributors'
    }
)
'''
    
    with open('speech2text.spec', 'w') as f:
        f.write(spec_content)
    print("[OK] Created speech2text.spec file")

def build_exe():
    """Build the executable using PyInstaller."""
    print("[BUILD] Building executable with PyInstaller...")
    
    # Create spec file
    create_spec_file()
    
    # Run PyInstaller
    try:
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller', 
            '--clean',
            'speech2text.spec'
        ], check=True, capture_output=True, text=True)
        
        print("[SUCCESS] Build completed successfully!")
        print(f"[LOCATION] Executable created at: {Path.cwd() / 'dist' / 'Speech2Text.exe'}")
        
        # Show file size
        exe_path = Path('dist/Speech2Text.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"[SIZE] File size: {size_mb:.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main build function."""
    print("[START] Building Speech2Text executable...")
    print(f"[DIR] Working directory: {Path.cwd()}")
    
    # Check if we're in the right directory
    if not Path('src/speech2text/main.py').exists():
        print("[ERROR] main.py not found. Make sure you're in the project root directory.")
        return
    
    # Build the executable
    success = build_exe()
    
    if success:
        print("\n[COMPLETE] Build completed successfully!")
        print("\n[STEPS] Next steps:")
        print("1. Navigate to the 'dist' folder")
        print("2. Run Speech2Text.exe")
        print("3. The first run might be slower as it extracts files")
        print("\n[TIPS] Distribution tips:")
        print("- You can distribute the Speech2Text.exe file to other Windows computers")
        print("- Make sure users have their OpenAI API key ready")
        print("- The exe includes all dependencies, no Python installation needed")
    else:
        print("\n[FAILED] Build failed. Check the error messages above.")

if __name__ == "__main__":
    main()