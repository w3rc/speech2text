"""Main entry point for Speech2Text application."""

import sys
import os
import tkinter as tk

# Add current directory to path for PyInstaller
if getattr(sys, 'frozen', False):
    # Running as PyInstaller executable
    current_dir = os.path.dirname(sys.executable)
    sys.path.insert(0, current_dir)

# Try multiple import strategies
try:
    # Try relative import first (normal development)
    from .modern_speech_app import ModernSpeechToTextApp
except ImportError:
    try:
        # Try direct import (PyInstaller)
        import modern_speech_app
        ModernSpeechToTextApp = modern_speech_app.ModernSpeechToTextApp
    except ImportError:
        try:
            # Try with speech2text prefix
            from speech2text.modern_speech_app import ModernSpeechToTextApp
        except ImportError:
            # Last resort - set up path manually
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sys.path.insert(0, current_dir)
            import modern_speech_app
            ModernSpeechToTextApp = modern_speech_app.ModernSpeechToTextApp


def main() -> None:
    """Main entry point for the modern Speech2Text application."""
    try:
        root = tk.Tk()
        app = ModernSpeechToTextApp(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()