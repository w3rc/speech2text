"""Test the full application with a timeout."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import tkinter as tk
from src.speech2text.modern_speech_app import ModernSpeechToTextApp

# Create root window
root = tk.Tk()

# Create app
app = ModernSpeechToTextApp(root)

# Auto-close after 8 seconds for testing  
def auto_close():
    print("Auto-closing application...")
    app.on_closing()

root.after(8000, auto_close)  # Close after 8 seconds

print("Starting application with clean interface (no menu bar)...")
print("Features to test:")
print("- Dark title bar")
print("- Settings button (gear icon)")
print("- Help button (question mark) with shortcuts/about")
print("- Ctrl+Win global hotkey")
print("Application will auto-close in 8 seconds...")
root.mainloop()
print("Application closed.")