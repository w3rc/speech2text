"""Speech2Text - Desktop speech-to-text application using OpenAI Whisper API.

A modern desktop application for real-time speech-to-text transcription.
"""

__version__ = "0.1.0"
__author__ = "Speech2Text Contributors"
__email__ = "contributors@speech2text.dev"
__license__ = "MIT"

from .settings import settings, SettingsManager
from .settings_dialog import SettingsDialog
from .speech_to_text_app import SpeechToTextApp
from .main import main

__all__ = [
    "settings",
    "SettingsManager", 
    "SettingsDialog",
    "SpeechToTextApp",
    "main",
]