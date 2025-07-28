"""Global hotkey management for Speech2Text application."""

import threading
from typing import Callable, Optional
from pynput import keyboard
import time


class GlobalHotkeyManager:
    """Manager for global keyboard shortcuts."""
    
    def __init__(self):
        self.listener: Optional[keyboard.Listener] = None
        self.toggle_callback: Optional[Callable] = None
        self.running = False
        self.ctrl_pressed = False
        self.win_pressed = False
        self.last_trigger_time = 0
        self.debounce_delay = 0.8  # 800ms debounce
        
    def register_toggle_hotkey(self, callback: Callable) -> None:
        """Register the Ctrl+Win toggle hotkey.
        
        Args:
            callback: Function to call when Ctrl+Win is pressed
        """
        self.toggle_callback = callback
        
    def start(self) -> bool:
        """Start listening for global hotkeys.
        
        Returns:
            True if started successfully, False otherwise
        """
        if self.running:
            return True
            
        try:
            # Start the listener
            self.listener = keyboard.Listener(
                on_press=self._on_key_press,
                on_release=self._on_key_release
            )
            
            self.listener.start()
            self.running = True
            print("Global hotkey listener started - Ctrl+Win to toggle recording")
            return True
            
        except Exception as e:
            print(f"Failed to start global hotkey listener: {e}")
            return False
    
    def stop(self) -> None:
        """Stop listening for global hotkeys."""
        if self.listener:
            self.listener.stop()
            self.listener = None
        self.running = False
        
    def _on_key_press(self, key):
        """Handle key press events."""
        try:
            # Track Ctrl key
            if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
                self.ctrl_pressed = True
                
            # Track Windows key  
            if key in [keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r]:
                self.win_pressed = True
                
            # Check if both Ctrl and Win are pressed
            if self.ctrl_pressed and self.win_pressed:
                current_time = time.time()
                if current_time - self.last_trigger_time > self.debounce_delay:
                    self.last_trigger_time = current_time
                    if self.toggle_callback:
                        print("Hotkey Ctrl+Win detected!")
                        # Execute callback in separate thread
                        thread = threading.Thread(target=self.toggle_callback, daemon=True)
                        thread.start()
                    
        except Exception as e:
            print(f"Error in key press handler: {e}")
    
    def _on_key_release(self, key):
        """Handle key release events."""
        try:
            # Track Ctrl key release
            if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
                self.ctrl_pressed = False
                
            # Track Windows key release
            if key in [keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r]:
                self.win_pressed = False
                
        except Exception as e:
            print(f"Error in key release handler: {e}")
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.stop()