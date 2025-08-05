"""Sound notification system for recording and transcription events."""

import platform
import threading
from typing import Optional


class SoundNotifications:
    """Handles sound notifications for different application events."""
    
    def __init__(self):
        """Initialize the sound notification system."""
        self.enabled = True
        self.system = platform.system()
        
    def play_recording_start(self) -> None:
        """Play sound when recording starts."""
        if not self.enabled:
            return
        threading.Thread(target=self._play_start_sound, daemon=True).start()
    
    def play_recording_stop(self) -> None:
        """Play sound when recording stops."""
        if not self.enabled:
            return
        threading.Thread(target=self._play_stop_sound, daemon=True).start()
    
    def play_transcription_processing(self) -> None:
        """Play sound when transcription processing begins."""
        if not self.enabled:
            return
        threading.Thread(target=self._play_processing_sound, daemon=True).start()
    
    def play_transcription_complete(self) -> None:
        """Play sound when transcription is complete."""
        if not self.enabled:
            return
        threading.Thread(target=self._play_complete_sound, daemon=True).start()
    
    def _play_start_sound(self) -> None:
        """Play the recording start sound."""
        try:
            if self.system == "Windows":
                import winsound
                # Short ascending beep for start
                winsound.Beep(800, 150)  # 800Hz for 150ms
            elif self.system == "Darwin":  # macOS
                import os
                os.system("afplay /System/Library/Sounds/Glass.aiff")
            elif self.system == "Linux":
                import os
                os.system("paplay /usr/share/sounds/alsa/Front_Left.wav 2>/dev/null || echo -e '\a'")
        except Exception:
            # Fallback to system bell
            print('\a', end='', flush=True)
    
    def _play_stop_sound(self) -> None:
        """Play the recording stop sound."""
        try:
            if self.system == "Windows":
                import winsound
                # Short descending beep for stop
                winsound.Beep(600, 150)  # 600Hz for 150ms
            elif self.system == "Darwin":  # macOS
                import os
                os.system("afplay /System/Library/Sounds/Tink.aiff")
            elif self.system == "Linux":
                import os
                os.system("paplay /usr/share/sounds/alsa/Front_Right.wav 2>/dev/null || echo -e '\a'")
        except Exception:
            # Fallback to system bell
            print('\a', end='', flush=True)
    
    def _play_processing_sound(self) -> None:
        """Play the transcription processing sound."""
        try:
            if self.system == "Windows":
                import winsound
                # Double beep for processing
                winsound.Beep(700, 100)
                winsound.Sleep(50)
                winsound.Beep(700, 100)
            elif self.system == "Darwin":  # macOS
                import os
                os.system("afplay /System/Library/Sounds/Submarine.aiff")
            elif self.system == "Linux":
                import os
                os.system("paplay /usr/share/sounds/alsa/Rear_Left.wav 2>/dev/null || echo -e '\a'")
        except Exception:
            # Fallback to system bell
            print('\a\a', end='', flush=True)
    
    def _play_complete_sound(self) -> None:
        """Play the transcription complete sound."""
        try:
            if self.system == "Windows":
                import winsound
                # Pleasant ascending sequence for completion
                winsound.Beep(600, 100)
                winsound.Sleep(50)
                winsound.Beep(800, 100)
                winsound.Sleep(50)
                winsound.Beep(1000, 150)
            elif self.system == "Darwin":  # macOS
                import os
                os.system("afplay /System/Library/Sounds/Hero.aiff")
            elif self.system == "Linux":
                import os
                os.system("paplay /usr/share/sounds/alsa/Rear_Right.wav 2>/dev/null || echo -e '\a'")
        except Exception:
            # Fallback to system bell
            print('\a\a\a', end='', flush=True)
    
    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable sound notifications."""
        self.enabled = enabled
    
    def is_enabled(self) -> bool:
        """Check if sound notifications are enabled."""
        return self.enabled