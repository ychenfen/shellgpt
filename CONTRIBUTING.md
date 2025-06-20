# Contributing to ShellGPT

Thank you for your interest in contributing to ShellGPT! 🎉

## 🚀 Quick Start for Contributors

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/shellgpt.git
   cd shellgpt
   ```
3. **Set up development environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   pip install -e .
   ```
4. **Run tests to ensure everything works**
   ```bash
   python test_real_functionality.py
   ```

## 🎯 Ways to Contribute

### 🐛 Bug Reports
- Use the bug report template
- Include system information and steps to reproduce
- Test with the latest version

### ✨ Feature Requests
- Use the feature request template
- Explain the use case and expected behavior
- Consider backward compatibility

### 💻 Code Contributions
- Follow the existing code style
- Add tests for new functionality
- Update documentation if needed

## 🔧 Development Guidelines

### Code Style
- Use type hints for all functions
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings for classes and functions

### Testing
- Run the test suite before submitting
- Add tests for new features
- Ensure all platforms are supported

### Commit Messages
- Use clear, descriptive commit messages
- Include emoji for visual clarity
- Reference issues when applicable

Example:
```
🐛 Fix safety checker regex pattern for Windows paths

- Update regex to handle Windows drive letters
- Add test cases for Windows-specific paths
- Fixes #123
```

## 📁 Project Structure

```
shellgpt/
├── core/           # Core AI and processing engines
├── models/         # Data models and schemas
├── cli/           # Command-line interface
├── config/        # Configuration management
├── utils/         # Utilities and patterns
└── tests/         # Test files
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Core functionality tests
python test_real_functionality.py

# Demo and examples
python demo_with_fallback.py
python simple_demo.py

# CLI tests
python run_shellgpt.py --help
python run_shellgpt.py version
```

## 🎨 Adding New Command Patterns

To add new command patterns for offline mode:

1. Edit `utils/patterns.py`
2. Add your pattern to the `COMMAND_PATTERNS` list
3. Test with the offline demo
4. Update documentation

Example pattern:
```python
{
    "action": "my_action",
    "patterns": [
        r"my.*pattern",
        r"alternative.*pattern",
    ],
    "templates": {
        "unix": "my-command {target}",
        "windows": "my-command.exe {target}",
    }
}
```

## 🌟 Recognition

Contributors will be:
- Listed in the README
- Mentioned in release notes
- Given credit in commit messages

## 📞 Getting Help

- Open an issue for questions
- Check existing issues first
- Join discussions for feature planning

## 📜 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn and contribute

Thank you for making ShellGPT better! 🙏