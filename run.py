#!/usr/bin/env python3
"""Simple launcher script for Speech2Text application."""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from speech2text.main import main

if __name__ == "__main__":
    main()