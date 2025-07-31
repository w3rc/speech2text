"""Setup script for creating MSI installer with cx_Freeze."""

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
    "initial_target_dir": r"[ProgramFilesFolder]\Speech2Text",
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
