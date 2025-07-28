"""
Settings management for Speech2Text application.

Handles configuration storage, encryption, and retrieval of user preferences
including API keys, audio parameters, and application settings.
"""

import json
import os
import base64
from pathlib import Path
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SettingsManager:
    """Manages application settings with secure storage for sensitive data."""
    
    def __init__(self):
        self.config_dir = self._get_config_directory()
        self.config_file = self.config_dir / "config.json"
        self.key_file = self.config_dir / ".key"
        
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Default settings
        self.defaults = {
            "api_key": "",
            "audio": {
                "sample_rate": 44100,
                "channels": 1,
                "chunk_size": 1024,
                "format": "paInt16"
            },
            "transcription": {
                "language": "en",  # English by default
                "model": "whisper-1",
                "temperature": 0.0,  # More deterministic
                "prompt": ""  # Optional context prompt
            },
            "ui": {
                "window_geometry": "600x500",
                "theme": "default"
            },
            "output": {
                "auto_save": False,
                "save_directory": str(Path.home() / "Documents"),
                "file_format": "txt"
            }
        }
        
        self.settings = self._load_settings()
        self._encryption_key = self._get_encryption_key()
    
    def _get_config_directory(self) -> Path:
        """Get the configuration directory path based on OS."""
        if os.name == 'nt':  # Windows
            config_dir = Path(os.environ.get('APPDATA', '')) / "Speech2Text"
        else:  # macOS/Linux
            config_dir = Path.home() / ".config" / "speech2text"
        
        return config_dir
    
    def _get_encryption_key(self) -> bytes:
        """Get or create encryption key for sensitive data."""
        if self.key_file.exists():
            try:
                key_data = json.loads(self.key_file.read_text())
                return base64.urlsafe_b64decode(key_data["key"].encode())
            except (json.JSONDecodeError, KeyError):
                # If key file is corrupted, regenerate it
                pass
        
        # Generate new key
        password = b"speech2text_default_key"  # In production, this could be more secure
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        
        # Save key and salt
        key_data = {
            "key": key.decode(),
            "salt": base64.urlsafe_b64encode(salt).decode()
        }
        self.key_file.write_text(json.dumps(key_data))
        return key
    
    def _encrypt_value(self, value: str) -> str:
        """Encrypt sensitive string values."""
        if not value:
            return ""
        
        fernet = Fernet(self._encryption_key)
        encrypted = fernet.encrypt(value.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def _decrypt_value(self, encrypted_value: str) -> str:
        """Decrypt sensitive string values."""
        if not encrypted_value:
            return ""
        
        try:
            fernet = Fernet(self._encryption_key)
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_value.encode())
            decrypted = fernet.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception:
            return ""  # Return empty string if decryption fails
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from config file."""
        if not self.config_file.exists():
            return self.defaults.copy()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                loaded_settings = json.load(f)
            
            # Merge with defaults to ensure all keys exist
            settings = self.defaults.copy()
            self._deep_update(settings, loaded_settings)
            return settings
            
        except (json.JSONDecodeError, IOError):
            return self.defaults.copy()
    
    def _deep_update(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """Deep update dictionary while preserving nested structure."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
    
    def save_settings(self) -> bool:
        """Save current settings to config file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value using dot notation (e.g., 'audio.sample_rate')."""
        keys = key.split('.')
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set setting value using dot notation."""
        keys = key.split('.')
        target = self.settings
        
        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        
        # Set the final value
        target[keys[-1]] = value
    
    def get_api_key(self) -> str:
        """Get decrypted API key."""
        encrypted_key = self.get("api_key", "")
        return self._decrypt_value(encrypted_key)
    
    def set_api_key(self, api_key: str) -> None:
        """Set encrypted API key."""
        encrypted_key = self._encrypt_value(api_key)
        self.set("api_key", encrypted_key)
    
    def validate_api_key(self, api_key: str) -> bool:
        """Validate OpenAI API key format."""
        return api_key.startswith("sk-") and len(api_key) > 20
    
    def get_audio_settings(self) -> Dict[str, Any]:
        """Get audio configuration settings."""
        return self.get("audio", self.defaults["audio"])
    
    def get_ui_settings(self) -> Dict[str, Any]:
        """Get UI configuration settings."""
        return self.get("ui", self.defaults["ui"])
    
    def get_transcription_settings(self) -> Dict[str, Any]:
        """Get transcription configuration settings."""
        return self.get("transcription", self.defaults["transcription"])
    
    def get_output_settings(self) -> Dict[str, Any]:
        """Get output configuration settings."""
        return self.get("output", self.defaults["output"])
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        self.settings = self.defaults.copy()
    
    def export_settings(self, file_path: str) -> bool:
        """Export settings to file (excluding sensitive data)."""
        try:
            export_data = self.settings.copy()
            # Remove sensitive data from export
            export_data["api_key"] = ""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def import_settings(self, file_path: str) -> bool:
        """Import settings from file (excluding sensitive data)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
            
            # Don't import sensitive data
            if "api_key" in imported_settings:
                del imported_settings["api_key"]
            
            self._deep_update(self.settings, imported_settings)
            return True
        except (json.JSONDecodeError, IOError):
            return False


# Global settings instance
settings = SettingsManager()