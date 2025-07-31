"""Build script to create an MSI installer for Speech2Text application."""

import sys
import os
import subprocess
from pathlib import Path

def install_cx_freeze():
    """Install cx_Freeze if not already installed."""
    try:
        import cx_Freeze
        print("[OK] cx_Freeze is already installed")
        return True
    except ImportError:
        print("[INSTALL] Installing cx_Freeze...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'cx_Freeze'], check=True)
            print("[OK] cx_Freeze installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install cx_Freeze: {e}")
            return False

def create_setup_py():
    """Create setup.py file for cx_Freeze MSI build."""
    setup_content = '''"""Setup script for creating MSI installer with cx_Freeze."""

import sys
from cx_Freeze import setup, Executable
from pathlib import Path

# Read version from pyproject.toml or set default
version = "0.1.0"

# Include files and directories
include_files = [
    # Include Python source files
    ("src/speech2text/", "lib/speech2text/"),
]

# Build options
build_exe_options = {
    "packages": [
        "tkinter", "tkinter.ttk", "tkinter.messagebox", "tkinter.filedialog",
        "openai", "pyaudio", "cryptography", "numpy", "pynput",
        "threading", "tempfile", "wave", "json", "base64", "hashlib",
        "pathlib", "ctypes", "ctypes.wintypes", "platform", "time",
        "datetime", "math", "os", "sys", "typing"
    ],
    "excludes": [
        "matplotlib", "scipy", "pandas", "IPython", "jupyter",
        "test", "unittest", "email", "html", "http", "urllib",
        "xml", "xmlrpc", "distutils", "lib2to3"
    ],
    "include_files": include_files,
    "optimize": 2,
    "build_exe": "build/exe.win-amd64-3.13"
}

# MSI build options
bdist_msi_options = {
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\\Speech2Text",
    "install_icon": None,  # Add icon path if available
    "upgrade_code": "{12345678-1234-1234-1234-123456789012}",  # Generate unique GUID
    "summary_data": {
        "author": "Speech2Text Contributors",
        "comments": "Modern Speech-to-Text Desktop Application",
        "keywords": "speech-to-text, transcription, openai, whisper, voice"
    }
}

# Define executable
executables = [
    Executable(
        script="launcher.py",
        base="Win32GUI",  # Hide console window
        target_name="Speech2Text.exe",
        icon=None,  # Add icon path if available
        shortcut_name="Speech2Text",
        shortcut_dir="DesktopFolder",
    )
]

# Setup configuration
setup(
    name="Speech2Text",
    version=version,
    description="Modern Speech-to-Text Desktop Application",
    long_description="A modern desktop application for real-time speech-to-text transcription using OpenAI Whisper API.",
    author="Speech2Text Contributors",
    author_email="contributors@speech2text.dev",
    url="https://github.com/yourusername/speech2text",
    license="MIT",
    executables=executables,
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    }
)
'''
    
    with open('setup_msi.py', 'w') as f:
        f.write(setup_content)
    print("[OK] Created setup_msi.py file")

def build_msi():
    """Build the MSI installer using cx_Freeze."""
    print("[BUILD] Building MSI installer with cx_Freeze...")
    
    # Create setup.py file
    create_setup_py()
    
    # Clean previous builds
    import shutil
    if Path('build').exists():
        shutil.rmtree('build')
        print("[CLEAN] Removed previous build directory")
    
    if Path('dist').exists():
        shutil.rmtree('dist')
        print("[CLEAN] Removed previous dist directory")
    
    # Run cx_Freeze to build MSI
    try:
        # First build the exe
        print("[STEP 1/2] Building executable...")
        result = subprocess.run([
            sys.executable, 'setup_msi.py', 
            'build'
        ], check=True, capture_output=True, text=True)
        
        print("[OK] Executable build completed")
        
        # Then build the MSI
        print("[STEP 2/2] Building MSI installer...")
        result = subprocess.run([
            sys.executable, 'setup_msi.py', 
            'bdist_msi'
        ], check=True, capture_output=True, text=True)
        
        print("[SUCCESS] MSI build completed successfully!")
        
        # Find and report MSI file
        msi_files = list(Path('dist').glob('*.msi'))
        if msi_files:
            msi_path = msi_files[0]
            size_mb = msi_path.stat().st_size / (1024 * 1024)
            print(f"[LOCATION] MSI installer created at: {msi_path.absolute()}")
            print(f"[SIZE] File size: {size_mb:.1f} MB")
        else:
            print("[WARNING] MSI file not found in dist directory")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] MSI build failed!")
        print(f"Error output: {e.stderr}")
        if e.stdout:
            print(f"Standard output: {e.stdout}")
        return False

def main():
    """Main build function."""
    print("[START] Building Speech2Text MSI installer...")
    print(f"[DIR] Working directory: {Path.cwd()}")
    
    # Check if we're in the right directory
    if not Path('src/speech2text/main.py').exists():
        print("[ERROR] main.py not found. Make sure you're in the project root directory.")
        return
    
    if not Path('launcher.py').exists():
        print("[ERROR] launcher.py not found. Make sure launcher.py exists in the project root.")
        return
    
    # Install cx_Freeze if needed
    if not install_cx_freeze():
        print("[ERROR] Failed to install cx_Freeze. Cannot continue.")
        return
    
    # Build the MSI
    success = build_msi()
    
    if success:
        print("\\n[COMPLETE] MSI installer build completed successfully!")
        print("\\n[INSTALLATION] To install:")
        print("1. Right-click the .msi file → 'Install'")
        print("2. Follow the installation wizard")
        print("3. The app will be installed to Program Files")
        print("4. A desktop shortcut will be created")
        print("\\n[DISTRIBUTION] Distribution tips:")
        print("- The MSI file can be distributed to other Windows computers")
        print("- Users can install/uninstall through Windows Programs & Features")
        print("- The installer handles all dependencies automatically")
        print("- Includes proper Windows integration (Start Menu, Add/Remove Programs)")
    else:
        print("\\n[FAILED] MSI build failed. Check the error messages above.")
        print("\\n[ALTERNATIVE] You can still use the EXE version:")
        print("Run: python build_exe.py")

if __name__ == "__main__":
    main()