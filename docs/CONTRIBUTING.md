# Contributing to Speech2Text

Thank you for your interest in contributing to Speech2Text! We welcome contributions from the community and are grateful for any help you can provide.

## 🤝 Ways to Contribute

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, please include:

- **Clear, descriptive title**
- **Steps to reproduce** the bug
- **Expected vs. actual behavior**
- **System information** (OS, Python version, etc.)
- **Error messages** or logs if applicable
- **Screenshots** if relevant

### 💡 Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Clear description** of the enhancement
- **Use case** - why would this be useful?
- **Possible implementation** approach (if you have ideas)
- **Examples** of similar features in other applications

### 🔧 Code Contributions

We appreciate code contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Test** your changes thoroughly
5. **Commit** your changes (`git commit -m 'Add amazing feature'`)
6. **Push** to your branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- uv package manager
- Git
- A working microphone for testing

### Local Development

1. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/speech2text.git
   cd speech2text
   ```

2. **Install dependencies**
   ```bash
   uv sync --dev
   ```

3. **Set up your API key**
   - Run the application once: `uv run python speech_to_text_app.py`
   - Go to Settings and add your OpenAI API key

4. **Run the application**
   ```bash
   uv run python speech_to_text_app.py
   ```

### Code Style

We follow these coding standards:

- **PEP 8** for Python code style
- **Black** for code formatting (line length: 88)
- **isort** for import sorting
- **Type hints** for all function parameters and return values
- **Docstrings** for all public functions and classes

### Running Code Quality Tools

```bash
# Format code
uv run black .
uv run isort .

# Lint code
uv run flake8 .

# Type checking
uv run mypy .

# Run tests
uv run pytest
```

## 📝 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
feat(ui): add dark mode toggle
fix(audio): resolve microphone permission issue
docs(readme): update installation instructions
```

## 🧪 Testing

### Manual Testing

Before submitting a PR, please test:

- **Basic functionality**: Recording and transcription
- **Settings**: All configuration options work
- **UI interactions**: Menu items, buttons, keyboard shortcuts
- **Error handling**: Invalid API keys, no microphone, etc.
- **Cross-platform**: Test on different OS if possible

### Automated Testing

We're working on expanding our test suite. Currently:

```bash
# Run existing tests
uv run pytest

# Run with coverage
uv run pytest --cov=speech2text
```

## 🔍 Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated as needed
- [ ] Documentation updated if needed
- [ ] No merge conflicts with main branch

### PR Description Template

```markdown
## Summary
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Manual testing completed
- [ ] Automated tests pass
- [ ] Cross-platform testing (if applicable)

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
```

### Review Process

1. **Automated checks** must pass (linting, tests)
2. **Code review** by maintainers
3. **Testing** on different platforms if needed
4. **Approval** and merge

## 🏗️ Architecture Overview

### Project Structure

```
speech2text/
├── speech_to_text_app.py   # Main application
├── settings.py             # Configuration management
├── settings_dialog.py      # Settings UI
├── pyproject.toml         # Project configuration
├── README.md              # Project documentation
├── CONTRIBUTING.md        # This file
├── CHANGELOG.md           # Version history
└── LICENSE                # MIT license
```

### Key Components

- **SpeechToTextApp**: Main application class with UI and audio handling
- **SettingsManager**: Encrypted configuration storage
- **SettingsDialog**: Tabbed settings interface
- **Audio Processing**: PyAudio for recording, OpenAI for transcription

## 🚀 Feature Guidelines

### UI/UX Principles

- **Simplicity**: Keep the interface clean and intuitive
- **Accessibility**: Consider keyboard navigation and screen readers
- **Performance**: Don't block the UI thread
- **Error Handling**: Provide clear, actionable error messages

### Security Considerations

- **API Keys**: Always encrypt sensitive data
- **File Permissions**: Use appropriate file permissions
- **Input Validation**: Validate all user inputs
- **Dependencies**: Keep dependencies updated

### Platform Support

- **Primary**: Windows 10/11
- **Secondary**: macOS, Linux (community supported)
- **Compatibility**: Test on Python 3.8+

## ❓ Getting Help

### Community

- **Discussions**: [GitHub Discussions](https://github.com/yourusername/speech2text/discussions)
- **Issues**: [GitHub Issues](https://github.com/yourusername/speech2text/issues)

### Maintainers

For questions about contributing, feel free to:

- Open a discussion on GitHub
- Comment on relevant issues
- Reach out via email (see pyproject.toml)

## 📜 License

By contributing to Speech2Text, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be:

- Listed in the project contributors
- Mentioned in release notes for significant contributions
- Added to the project's acknowledgments

---

Thank you for contributing to Speech2Text! 🎉