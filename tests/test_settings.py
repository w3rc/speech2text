"""Tests for settings module."""

import pytest
import tempfile
import os
from pathlib import Path
import sys

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from speech2text.settings import SettingsManager


def test_settings_creation():
    """Test settings manager creation."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Override config directory for testing
        original_get_config_dir = SettingsManager._get_config_directory
        
        def temp_config_dir(self):
            return Path(temp_dir) / "test_config"
        
        SettingsManager._get_config_directory = temp_config_dir
        
        try:
            settings = SettingsManager()
            assert settings is not None
            assert settings.get("audio.sample_rate") == 44100
        finally:
            SettingsManager._get_config_directory = original_get_config_dir


def test_api_key_validation():
    """Test API key validation."""
    settings = SettingsManager()
    
    # Valid API key format
    assert settings.validate_api_key("sk-1234567890abcdef")
    
    # Invalid formats
    assert not settings.validate_api_key("")
    assert not settings.validate_api_key("invalid-key")
    assert not settings.validate_api_key("pk-1234567890abcdef")


if __name__ == "__main__":
    pytest.main([__file__])