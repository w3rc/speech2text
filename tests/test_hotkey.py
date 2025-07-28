"""Test script for global hotkey functionality."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import time
from src.speech2text.global_hotkey import GlobalHotkeyManager

def test_callback():
    print("Ctrl+Win pressed!")

# Create hotkey manager
manager = GlobalHotkeyManager()
manager.register_toggle_hotkey(test_callback)

# Start listening
if manager.start():
    print("Hotkey manager started. Press Ctrl+Win to test...")
    print("Testing for 15 seconds, then exiting...")
    
    # Test for 15 seconds
    for i in range(15):
        print(f"Second {i+1}...")
        time.sleep(1)
    
    print("Test complete, stopping manager...")
    manager.stop()
else:
    print("Failed to start hotkey manager")