# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-06-20

### Added
- 🎉 Initial release of ShellGPT
- 🧠 AI-powered natural language to shell command conversion
- 🛡️ Four-level safety checking system (Safe/Cautious/Dangerous/Forbidden)
- 🔍 Intelligent context awareness (Git, directory, system info)
- ⚡ Pattern matching for fast common operations
- 🎨 Beautiful Rich-powered terminal interface
- 🔧 Comprehensive configuration management
- 💻 Cross-platform support (Linux/macOS/Windows)
- 📦 Complete CLI application with multiple commands
- 🚀 Interactive mode for continuous conversation
- 🎯 Offline mode with pattern matching fallback
- 📚 Comprehensive documentation and examples

### Features
- **CLI Commands:**
  - `ask` - Generate commands from natural language
  - `explain` - Explain what shell commands do
  - `config` - Manage configuration settings
  - `version` - Show version information
  - `interactive` - Start interactive mode

- **Core Components:**
  - NLP Engine with OpenAI integration
  - Safety Checker with regex patterns
  - Context Manager for environment awareness
  - Command Generator with AI and pattern fallback
  - Configuration system with YAML support

- **Safety Features:**
  - Intelligent command risk assessment
  - User confirmation for dangerous operations
  - Safe alternative suggestions
  - Forbidden command blocking

- **Developer Experience:**
  - Type hints throughout codebase
  - Async/await patterns for performance
  - Modular architecture for extensibility
  - Comprehensive test suite
  - Multiple demo programs

### Technical Details
- Python 3.8+ support
- Pydantic v2 for data validation
- Rich library for terminal UI
- Typer for CLI framework
- AsyncIO for async operations
- GitPython for Git integration
- PSUtil for system information

### Documentation
- Complete README with usage examples
- Detailed USAGE.md guide
- Contributing guidelines
- Issue templates for bug reports and features
- Changelog for version tracking