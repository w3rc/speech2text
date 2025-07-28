# Tests

This directory contains all test files for the Speech2Text application.

## Running Tests

To run the tests, use pytest from the project root:

```bash
# Install development dependencies
uv sync --dev

# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/speech2text

# Run specific test file
uv run pytest tests/test_settings.py
```

## Test Structure

- `test_settings.py` - Tests for the settings management system
- More test files will be added as the project grows

## Writing Tests

When adding new tests:
1. Create test files with the `test_` prefix
2. Use pytest fixtures for setup/teardown
3. Test both positive and negative cases
4. Include docstrings explaining what each test does