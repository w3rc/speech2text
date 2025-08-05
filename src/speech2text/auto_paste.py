"""Auto-paste functionality for transcribed text."""

import platform
import time
import threading
from typing import Optional
import tkinter as tk


class AutoPaste:
    """Handles automatic pasting of transcribed text to active text fields."""
    
    def __init__(self):
        """Initialize the auto-paste system."""
        self.enabled = False
        self.system = platform.system()
        self._last_focused_window = None
        
    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable auto-paste functionality."""
        self.enabled = enabled
    
    def is_enabled(self) -> bool:
        """Check if auto-paste is enabled."""
        return self.enabled
    
    def paste_text(self, text: str, delay_ms: int = 100) -> None:
        """Paste text to the currently active text field if auto-paste is enabled."""
        if not self.enabled or not text.strip():
            return
        
        # Run in separate thread to avoid blocking UI
        threading.Thread(
            target=self._paste_text_async, 
            args=(text, delay_ms), 
            daemon=True
        ).start()
    
    def _paste_text_async(self, text: str, delay_ms: int) -> None:
        """Perform the actual paste operation asynchronously."""
        try:
            # Small delay to ensure the UI has time to process
            time.sleep(delay_ms / 1000.0)
            
            if self._is_text_field_active():
                self._perform_paste(text)
        except Exception as e:
            print(f"Auto-paste failed: {e}")
    
    def _is_text_field_active(self) -> bool:
        """Check if a text field is currently active."""
        try:
            if self.system == "Windows":
                return self._is_windows_text_field_active()
            elif self.system == "Darwin":  # macOS
                return self._is_macos_text_field_active()
            elif self.system == "Linux":
                return self._is_linux_text_field_active()
        except Exception:
            pass
        return False
    
    def _is_windows_text_field_active(self) -> bool:
        """Check if a text field is active on Windows."""
        try:
            import ctypes
            from ctypes import wintypes
            
            # Get the currently focused window
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            if not hwnd:
                return False
            
            # Get the focused control within the window
            focused_hwnd = ctypes.windll.user32.GetFocus()
            if not focused_hwnd:
                return False
            
            # Get window class name to determine if it's a text field
            class_name = ctypes.create_unicode_buffer(256)
            ctypes.windll.user32.GetClassNameW(focused_hwnd, class_name, 256)
            class_name_str = class_name.value.lower()
            
            # Common text field class names
            text_field_classes = [
                'edit',           # Standard text box
                'richedit',       # Rich text box
                'richedit20a',    # Rich edit control
                'richedit20w',    # Rich edit control (Unicode)
                'richedit50w',    # Rich edit 5.0
                'textarea',       # HTML textarea
                'input',          # HTML input
                'scintilla',      # Code editors (Notepad++, etc.)
                'consolewindowclass',  # Command prompt
            ]
            
            # Check if the focused control is a text field
            for text_class in text_field_classes:
                if text_class in class_name_str:
                    return True
            
            # Additional check for web browsers and other apps
            # Get window title to make educated guesses
            title_length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            if title_length > 0:
                title = ctypes.create_unicode_buffer(title_length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, title, title_length + 1)
                title_str = title.value.lower()
                
                # Check for common applications where text input is likely
                text_apps = [
                    'notepad',
                    'wordpad',
                    'microsoft word',
                    'google docs',
                    'chrome',
                    'firefox',
                    'edge',
                    'code',
                    'visual studio',
                    'slack',
                    'discord',
                    'telegram',
                    'whatsapp',
                    'outlook',
                    'thunderbird'
                ]
                
                for app in text_apps:
                    if app in title_str:
                        return True
            
            return False
            
        except Exception:
            return False
    
    def _is_macos_text_field_active(self) -> bool:
        """Check if a text field is active on macOS."""
        try:
            import subprocess
            
            # Use AppleScript to check if a text field is focused
            script = '''
            tell application "System Events"
                set frontApp to name of first application process whose frontmost is true
                try
                    set focusedElement to focused UI element of application process frontApp
                    set elementRole to role of focusedElement
                    if elementRole is "AXTextField" or elementRole is "AXTextArea" then
                        return true
                    end if
                end try
                return false
            end tell
            '''
            
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            return result.stdout.strip().lower() == 'true'
            
        except Exception:
            return False
    
    def _is_linux_text_field_active(self) -> bool:
        """Check if a text field is active on Linux."""
        try:
            import subprocess
            
            # Try to use xdotool to get focused window info
            try:
                # Get the currently focused window
                result = subprocess.run(
                    ['xdotool', 'getwindowfocus', 'getwindowname'],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                
                if result.returncode == 0:
                    window_name = result.stdout.strip().lower()
                    
                    # Check for common text editors and applications
                    text_apps = [
                        'text',
                        'editor',
                        'gedit',
                        'kate',
                        'vim',
                        'emacs',
                        'code',
                        'atom',
                        'sublime',
                        'firefox',
                        'chrome',
                        'terminal',
                        'konsole',
                        'gnome-terminal'
                    ]
                    
                    for app in text_apps:
                        if app in window_name:
                            return True
            except FileNotFoundError:
                # xdotool not available, try alternative methods
                pass
            
            return False
            
        except Exception:
            return False
    
    def _perform_paste(self, text: str) -> None:
        """Perform the actual paste operation."""
        try:
            if self.system == "Windows":
                self._paste_windows(text)
            elif self.system == "Darwin":  # macOS
                self._paste_macos(text)
            elif self.system == "Linux":
                self._paste_linux(text)
        except Exception as e:
            print(f"Paste operation failed: {e}")
    
    def _paste_windows(self, text: str) -> None:
        """Paste text on Windows using clipboard and Ctrl+V."""
        import pyperclip
        import ctypes
        from ctypes import wintypes
        
        # Save current clipboard content
        try:
            original_clipboard = pyperclip.paste()
        except Exception:
            original_clipboard = ""
        
        try:
            # Set text to clipboard
            pyperclip.copy(text)
            time.sleep(0.05)  # Small delay for clipboard to update
            
            # Send Ctrl+V
            # VK_CONTROL = 0x11, VK_V = 0x56
            ctypes.windll.user32.keybd_event(0x11, 0, 0, 0)  # Ctrl down
            time.sleep(0.01)
            ctypes.windll.user32.keybd_event(0x56, 0, 0, 0)  # V down
            time.sleep(0.01)
            ctypes.windll.user32.keybd_event(0x56, 0, 2, 0)  # V up
            ctypes.windll.user32.keybd_event(0x11, 0, 2, 0)  # Ctrl up
            
            # Small delay before restoring clipboard
            time.sleep(0.1)
            
        finally:
            # Restore original clipboard content
            try:
                pyperclip.copy(original_clipboard)
            except Exception:
                pass
    
    def _paste_macos(self, text: str) -> None:
        """Paste text on macOS using clipboard and Cmd+V."""
        import pyperclip
        import subprocess
        
        # Save current clipboard content
        try:
            original_clipboard = pyperclip.paste()
        except Exception:
            original_clipboard = ""
        
        try:
            # Set text to clipboard
            pyperclip.copy(text)
            time.sleep(0.05)  # Small delay for clipboard to update
            
            # Send Cmd+V using AppleScript
            script = '''
            tell application "System Events"
                keystroke "v" using command down
            end tell
            '''
            
            subprocess.run(['osascript', '-e', script], timeout=2)
            
            # Small delay before restoring clipboard
            time.sleep(0.1)
            
        finally:
            # Restore original clipboard content
            try:
                pyperclip.copy(original_clipboard)
            except Exception:
                pass
    
    def _paste_linux(self, text: str) -> None:
        """Paste text on Linux using clipboard and Ctrl+V."""
        import pyperclip
        import subprocess
        
        # Save current clipboard content
        try:
            original_clipboard = pyperclip.paste()
        except Exception:
            original_clipboard = ""
        
        try:
            # Set text to clipboard
            pyperclip.copy(text)
            time.sleep(0.05)  # Small delay for clipboard to update
            
            # Send Ctrl+V using xdotool
            try:
                subprocess.run(['xdotool', 'key', 'ctrl+v'], timeout=2)
            except FileNotFoundError:
                # Fallback to other methods if xdotool is not available
                print("xdotool not found, auto-paste unavailable on this Linux system")
            
            # Small delay before restoring clipboard
            time.sleep(0.1)
            
        finally:
            # Restore original clipboard content
            try:
                pyperclip.copy(original_clipboard)
            except Exception:
                pass