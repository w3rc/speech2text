"""Simple launcher for Speech2Text to handle PyInstaller imports."""

import sys
import os
import tkinter as tk

# Add the src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
speech2text_dir = os.path.join(src_dir, 'speech2text')

# Add both directories to Python path
sys.path.insert(0, src_dir)
sys.path.insert(0, speech2text_dir)

# Now import all our modules
from speech2text.modern_speech_app import ModernSpeechToTextApp

def main():
    """Main entry point for the Speech2Text application."""
    try:
        root = tk.Tk()
        app = ModernSpeechToTextApp(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()