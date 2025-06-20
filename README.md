# 🤖 ShellGPT - AI-Powered Intelligent Shell Assistant

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAI](https://img.shields.io/badge/Powered%20by-OpenAI-green.svg)](https://openai.com)

> **Transform natural language into precise shell commands with AI-powered intelligence and safety**

ShellGPT is a revolutionary command-line assistant that understands your intentions in natural language and converts them into accurate shell commands. With built-in safety checks, context awareness, and learning capabilities, it's the perfect tool for both beginners and experts.

![ShellGPT Demo](https://via.placeholder.com/800x400/1a1a1a/ffffff?text=ShellGPT+Demo)

## ✨ Features

- 🧠 **Natural Language Understanding** - Type what you want in plain English
- 🔍 **Context Awareness** - Knows your current directory, git status, and environment
- 🛡️ **Safety First** - Advanced safety checks prevent dangerous operations
- ⚡ **Lightning Fast** - Quick pattern matching for common commands
- 🎯 **High Accuracy** - AI-powered with 90%+ accuracy for complex queries
- 📚 **Learning Capability** - Adapts to your preferences and usage patterns
- 🔧 **Multi-Platform** - Works on Linux, macOS, and Windows
- 🎨 **Beautiful Interface** - Rich, colorful output with clear explanations

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (coming soon)
pip install shellgpt

# Or install from source
git clone https://github.com/ychenfen/shellgpt.git
cd shellgpt
pip install -e .
```

### Setup

1. **Get your OpenAI API key** from [OpenAI Platform](https://platform.openai.com/api-keys)

2. **Configure ShellGPT**:
   ```bash
   shellgpt config --set-api-key
   # Enter your API key when prompted
   ```

3. **Start using**:
   ```bash
   shellgpt ask "list all python files"
   shellgpt ask "show git status"
   shellgpt ask "find large files over 100MB"
   ```

## 📖 Usage Examples

### Basic Commands

```bash
# File operations
shellgpt ask "create a new directory called project"
shellgpt ask "copy all .txt files to backup folder" 
shellgpt ask "find all files modified in the last week"

# Git operations  
shellgpt ask "commit all changes with message 'fix bug'"
shellgpt ask "push to main branch"
shellgpt ask "show recent commits"

# System information
shellgpt ask "show disk usage"
shellgpt ask "list running processes"
shellgpt ask "check memory usage"
```

### Advanced Features

```bash
# Execute immediately with safety checks
shellgpt ask "install docker" --execute

# Show alternative approaches
shellgpt ask "compress this folder" --alternatives

# Explain existing commands
shellgpt explain "find . -name '*.py' -exec grep -l 'import os' {} \;"

# Interactive mode
shellgpt interactive
```

### Sample Output

```
🚀 Generated Command
┌─────────────────────────────────────────────────────────────┐
│ find . -name "*.py" -type f                                 │
└─────────────────────────────────────────────────────────────┘

📝 Explanation:  Find all Python files in current directory and subdirectories
🔧 Type:         File Operation  
🛡️  Safety:      ✅ Safe
🎯 Confidence:   95.0%

Execute this command? [Y/n]: 
```

## 🛡️ Safety Features

ShellGPT includes comprehensive safety mechanisms:

- **🚨 Danger Detection** - Identifies potentially destructive commands
- **⚠️ Warning System** - Highlights risky operations
- **🔒 Confirmation Prompts** - Requires approval for dangerous actions
- **❌ Forbidden Commands** - Blocks extremely dangerous operations
- **💡 Safe Alternatives** - Suggests safer approaches

### Safety Levels

| Level | Description | Example |
|-------|-------------|---------|
| ✅ **Safe** | No risks detected | `ls -la`, `git status` |
| ⚠️ **Cautious** | Potential risks | `rm file.txt`, `chmod 755` |
| 🚨 **Dangerous** | High risk operations | `rm -rf /`, `sudo dd` |
| ❌ **Forbidden** | Blocked for safety | Malicious scripts |

## 🧠 AI-Powered Intelligence

### Natural Language Processing

```bash
# Instead of remembering complex syntax:
shellgpt ask "show me all files larger than 1GB modified in the last month"

# Generates: find . -type f -size +1G -mtime -30 -ls
```

### Context Awareness

ShellGPT understands your environment:

- **📁 Current Directory** - Adapts commands to your location
- **🔗 Git Repository** - Knows your branch and status  
- **💻 Operating System** - Uses appropriate commands for your platform
- **🛠️ Available Tools** - Checks what's installed on your system

### Learning & Adaptation

- **📊 Usage Patterns** - Learns your preferred tools and approaches
- **🎯 Personal Preferences** - Remembers your configuration choices
- **📈 Improvement Over Time** - Gets better with usage

## ⚙️ Configuration

### Configuration File

Create `~/.config/shellgpt/config.yaml`:

```yaml
# OpenAI Configuration
openai_model: "gpt-3.5-turbo"
openai_max_tokens: 1000
openai_temperature: 0.1

# Safety Configuration
require_confirmation: true
enable_safety_checks: true
max_command_length: 1000

# Learning Configuration  
enable_learning: true
max_history_size: 1000

# Application Configuration
debug: false
log_level: "INFO"
```

### Environment Variables

```bash
export OPENAI_API_KEY="your-api-key-here"
export SHELLGPT_MODEL="gpt-4"
export SHELLGPT_ENABLE_SAFETY="true"
```

## 🔧 Advanced Usage

### Command Aliases

Add to your shell profile:

```bash
# Short aliases
alias s="shellgpt ask"
alias sx="shellgpt ask --execute"  
alias se="shellgpt explain"

# Quick actions
alias sgi="shellgpt ask 'show git status'"
alias sgl="shellgpt ask 'show git log'"
```

### Integration with Existing Tools

```bash
# Pipe output to shellgpt for explanation
history | tail -1 | shellgpt explain

# Use with other tools
shellgpt ask "find large files" | head -10
```

## 🛠️ Development

### Prerequisites

- Python 3.8+
- OpenAI API key
- Git (for git-related features)

### Setup Development Environment

```bash
git clone https://github.com/ychenfen/shellgpt.git
cd shellgpt

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black shellgpt/
isort shellgpt/
```

### Project Structure

```
shellgpt/
├── core/               # Core AI and processing engines
│   ├── nlp_engine.py       # Natural language processing
│   ├── command_generator.py # Command generation
│   ├── context_manager.py   # System context awareness
│   └── safety_checker.py    # Safety validation
├── models/             # Data models and schemas
├── utils/              # Utilities and patterns
├── config/             # Configuration management
├── cli/               # Command-line interface
└── tests/             # Test suite
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📊 Roadmap

- [x] **Core AI Engine** - Natural language to shell command conversion
- [x] **Safety System** - Comprehensive safety checks and warnings
- [x] **Context Awareness** - Git, directory, and system context
- [x] **Multi-Platform Support** - Linux, macOS, Windows compatibility
- [ ] **Plugin System** - Extensible architecture for custom commands
- [ ] **Shell Integration** - Native shell completion and history
- [ ] **Team Sharing** - Share learned patterns across teams
- [ ] **Advanced Learning** - Personal AI model fine-tuning
- [ ] **GUI Interface** - Desktop application for non-terminal users
- [ ] **Mobile App** - iOS/Android companion app

## ⚠️ Safety Notice

While ShellGPT includes comprehensive safety checks, always review generated commands before execution, especially those marked as "Cautious" or "Dangerous." The AI is powerful but not infallible.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT models that power ShellGPT
- **Rich** for the beautiful command-line interface
- **Typer** for the excellent CLI framework
- **The Open Source Community** for inspiration and feedback

## 📞 Support

- 📚 [Documentation](https://github.com/ychenfen/shellgpt/wiki)
- 🐛 [Report Issues](https://github.com/ychenfen/shellgpt/issues)
- 💬 [Discussions](https://github.com/ychenfen/shellgpt/discussions)
- 📧 Email: 2570601904@qq.com

## 🌟 Show Your Support

If ShellGPT helps you be more productive, please consider:

- ⭐ **Starring this repository**
- 🐦 **Sharing on social media**
- 📝 **Writing a blog post about your experience**
- 💝 **Contributing to the project**

---

<div align="center">

**[⭐ Star us on GitHub](https://github.com/ychenfen/shellgpt) if you find this project useful!**

Made with ❤️ by developers, for developers.

</div>