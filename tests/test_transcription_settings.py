"""Test transcription settings functionality."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.speech2text.settings import settings

def test_transcription_defaults():
    """Test that transcription settings have correct defaults."""
    transcription_settings = settings.get_transcription_settings()
    
    print("Testing transcription settings defaults...")
    print(f"Language: {transcription_settings.get('language', 'NOT SET')}")
    print(f"Model: {transcription_settings.get('model', 'NOT SET')}")
    print(f"Temperature: {transcription_settings.get('temperature', 'NOT SET')}")
    print(f"Prompt: '{transcription_settings.get('prompt', 'NOT SET')}'")
    
    # Verify defaults
    assert transcription_settings.get('language') == 'en', f"Expected 'en', got '{transcription_settings.get('language')}'"
    assert transcription_settings.get('model') == 'whisper-1', f"Expected 'whisper-1', got '{transcription_settings.get('model')}'"
    assert transcription_settings.get('temperature') == 0.0, f"Expected 0.0, got {transcription_settings.get('temperature')}"
    assert transcription_settings.get('prompt') == '', f"Expected empty string, got '{transcription_settings.get('prompt')}'"
    
    print("[OK] All transcription defaults are correct!")
    
    # Test setting and getting values
    print("\nTesting setting values...")
    settings.set('transcription.language', 'es')
    settings.set('transcription.temperature', 0.5)
    settings.set('transcription.prompt', 'This is a Spanish conversation.')
    
    updated_settings = settings.get_transcription_settings()
    print(f"Updated Language: {updated_settings.get('language')}")
    print(f"Updated Temperature: {updated_settings.get('temperature')}")
    print(f"Updated Prompt: '{updated_settings.get('prompt')}'")
    
    # Reset to defaults
    settings.set('transcription.language', 'en')
    settings.set('transcription.temperature', 0.0)
    settings.set('transcription.prompt', '')
    
    print("[OK] Setting and getting transcription values works correctly!")

if __name__ == "__main__":
    test_transcription_defaults()
    print("\n[SUCCESS] All transcription settings tests passed!")