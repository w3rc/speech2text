"""Fixed MSI builder using cx_Freeze with correct options."""

import sys
import os
import subprocess
from pathlib import Path
import shutil

def create_fixed_setup_py():
    """Create a working setup.py file for cx_Freeze MSI build."""
    setup_content = '''"""Working setup script for creating MSI installer with cx_Freeze."""

import sys
from cx_Freeze import setup, Executable
from pathlib import Path

# Version
version = "0.1.0"

# Include files - just the essential ones
include_files = []

# Build options - simplified and compatible
build_exe_options = {
    "packages": [
        "tkinter", "tkinter.ttk", "tkinter.messagebox", "tkinter.filedialog",
        "openai", "pyaudio", "cryptography", "numpy", "pynput",
        "threading", "tempfile", "wave", "json", "base64", "hashlib",
        "pathlib", "ctypes", "platform", "time", "datetime", "math", "os", "sys"
    ],
    "excludes": [
        "matplotlib", "scipy", "pandas", "IPython", "jupyter",
        "test", "unittest", "email", "html", "http", "urllib",
        "xml", "xmlrpc", "distutils", "lib2to3", "pydoc"
    ],
    "include_files": include_files,
    "optimize": 1,  # Use level 1 optimization instead of 2
}

# MSI build options - simplified
bdist_msi_options = {
    "add_to_path": False,
    "initial_target_dir": "[ProgramFilesFolder]\\\\Speech2Text",
    "upgrade_code": "{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}",
}

# Define executable
executables = [
    Executable(
        script="launcher.py",
        base="Win32GUI",
        target_name="Speech2Text.exe",
    )
]

# Setup configuration
setup(
    name="Speech2Text",
    version=version,
    description="Modern Speech-to-Text Desktop Application",
    author="Speech2Text Contributors",
    executables=executables,
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    }
)
'''
    
    with open('setup_msi_fixed.py', 'w') as f:
        f.write(setup_content)
    print("[OK] Created setup_msi_fixed.py file")

def build_msi_fixed():
    """Build MSI using the fixed cx_Freeze setup."""
    print("[BUILD] Building MSI installer with fixed cx_Freeze...")
    
    # Create fixed setup file
    create_fixed_setup_py()
    
    # Clean previous builds
    if Path('build').exists():
        shutil.rmtree('build')
        print("[CLEAN] Removed previous build directory")
    
    if Path('dist').exists():
        shutil.rmtree('dist')
        print("[CLEAN] Removed previous dist directory")
    
    try:
        # Build the MSI directly
        print("[BUILDING] Creating MSI installer...")
        result = subprocess.run([
            sys.executable, 'setup_msi_fixed.py', 
            'bdist_msi'
        ], check=True, capture_output=True, text=True, cwd=Path.cwd())
        
        print("[SUCCESS] MSI build completed successfully!")
        
        # Find and report MSI file
        msi_files = list(Path('dist').glob('*.msi'))
        if msi_files:
            msi_path = msi_files[0]
            size_mb = msi_path.stat().st_size / (1024 * 1024)
            print(f"[LOCATION] MSI installer created at: {msi_path.absolute()}")
            print(f"[SIZE] File size: {size_mb:.1f} MB")
            return True
        else:
            print("[WARNING] MSI file not found in dist directory")
            return False
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] MSI build failed!")
        print(f"Return code: {e.returncode}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        if e.stdout:
            print(f"Standard output: {e.stdout}")
        return False

def cleanup_temp_files():
    """Clean up temporary build files."""
    temp_files = ['setup_msi_fixed.py']
    for file in temp_files:
        try:
            if Path(file).exists():
                os.remove(file)
                print(f"[CLEAN] Removed {file}")
        except Exception as e:
            print(f"[WARNING] Could not remove {file}: {e}")

def main():
    """Main build function."""
    print("[START] Building Speech2Text MSI installer (Fixed Version)...")
    print(f"[DIR] Working directory: {Path.cwd()}")
    
    # Check prerequisites
    if not Path('src/speech2text/main.py').exists():
        print("[ERROR] main.py not found. Make sure you're in the project root directory.")
        return
    
    if not Path('launcher.py').exists():
        print("[ERROR] launcher.py not found. Make sure launcher.py exists in the project root.")
        return
    
    # Check cx_Freeze
    try:
        import cx_Freeze
        print("[OK] cx_Freeze is available")
    except ImportError:
        print("[ERROR] cx_Freeze not found. Installing...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'cx_Freeze'], check=True)
            print("[OK] cx_Freeze installed successfully")
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to install cx_Freeze")
            return
    
    # Build the MSI
    success = build_msi_fixed()
    
    # Cleanup
    cleanup_temp_files()
    
    if success:
        print("\\n[COMPLETE] MSI installer build completed successfully!")
        print("\\n[FEATURES] The MSI installer includes:")
        print("- ✅ Professional Windows installer")
        print("- ✅ Program Files installation")
        print("- ✅ Add/Remove Programs integration")
        print("- ✅ All dependencies bundled")
        print("\\n[INSTALLATION] To install:")
        print("1. Double-click the .msi file")
        print("2. Follow the installation wizard")
        print("3. The app will be installed to Program Files")
        print("\\n[DISTRIBUTION] Ready for distribution:")
        print("- Professional MSI installer format")
        print("- No additional dependencies required")
        print("- Standard Windows installation experience")
    else:
        print("\\n[FAILED] MSI build failed. Check the error messages above.")
        print("\\n[ALTERNATIVE] Try the WiX Toolset approach:")
        print("Run: python build_msi_simple.py")

if __name__ == "__main__":
    main()