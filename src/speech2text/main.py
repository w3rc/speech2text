"""Main entry point for Speech2Text application."""

import sys
import tkinter as tk
from .speech_to_text_app import SpeechToTextApp


def main() -> None:
    """Main entry point for the Speech2Text application."""
    try:
        root = tk.Tk()
        app = SpeechToTextApp(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()