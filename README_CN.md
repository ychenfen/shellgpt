# 🤖 ShellGPT - AI驱动的智能Shell助手

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenAI](https://img.shields.io/badge/Powered%20by-OpenAI-green.svg)](https://openai.com)
[![GitHub stars](https://img.shields.io/github/stars/ychenfen/shellgpt?style=social)](https://github.com/ychenfen/shellgpt/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ychenfen/shellgpt?style=social)](https://github.com/ychenfen/shellgpt/network)

> **用自然语言描述，AI智能生成精确的Shell命令，内置安全检查和上下文感知**

ShellGPT是一款革命性的命令行助手，能够理解你的自然语言意图并将其转换为准确的Shell命令。内置安全检查、上下文感知和学习能力，是新手和专家的完美工具。

![ShellGPT演示](https://user-images.githubusercontent.com/placeholder/demo.gif)

<div align="center">

**[📖 完整文档](README.md) • [🚀 快速开始](#-快速开始) • [🎥 在线演示](#-立即试用) • [🤝 参与贡献](CONTRIBUTING.md) • [⭐ 给项目加星](https://github.com/ychenfen/shellgpt/stargazers)**

</div>

## ✨ 核心特性

- 🧠 **自然语言理解** - 用中文或英文描述你想做什么
- 🔍 **上下文感知** - 了解当前目录、Git状态和系统环境
- 🛡️ **安全优先** - 高级安全检查，防止危险操作
- ⚡ **极速响应** - 常用命令模式匹配，毫秒级响应
- 🎯 **高准确率** - AI驱动，复杂查询准确率90%+
- 📚 **智能学习** - 适应你的使用偏好和操作模式
- 🔧 **跨平台** - 支持Linux、macOS和Windows
- 🎨 **美观界面** - 丰富多彩的现代终端界面

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/ychenfen/shellgpt.git
cd shellgpt

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或者 venv\Scripts\activate  # Windows

# 安装依赖
pip install -e .
```

### ⚡ 立即试用！

```bash
# 测试基础功能（无需API密钥）
python run_shellgpt.py --help
python run_shellgpt.py version
python test_real_functionality.py

# 查看演示效果
python demo_with_fallback.py
```

### 配置

1. **获取OpenAI API密钥** - 访问 [OpenAI平台](https://platform.openai.com/api-keys)

2. **配置ShellGPT**：
   ```bash
   python run_shellgpt.py config --set-api-key
   # 输入你的API密钥
   ```

3. **开始使用**：
   ```bash
   python run_shellgpt.py ask "列出所有Python文件"
   python run_shellgpt.py ask "显示Git状态"
   python run_shellgpt.py ask "查找大于100MB的文件"
   ```

## 📖 使用示例

### 基础命令

```bash
# 文件操作
python run_shellgpt.py ask "创建一个名为project的新目录"
python run_shellgpt.py ask "复制所有txt文件到backup文件夹"
python run_shellgpt.py ask "查找上周修改的所有文件"

# Git操作  
python run_shellgpt.py ask "提交所有修改，消息为'修复bug'"
python run_shellgpt.py ask "推送到main分支"
python run_shellgpt.py ask "显示最近的提交记录"

# 系统信息
python run_shellgpt.py ask "显示磁盘使用情况"
python run_shellgpt.py ask "列出运行中的进程"
python run_shellgpt.py ask "检查内存使用率"
```

### 高级功能

```bash
# 安全检查下立即执行
python run_shellgpt.py ask "安装docker" --execute

# 显示多种解决方案
python run_shellgpt.py ask "压缩这个文件夹" --alternatives

# 解释现有命令
python run_shellgpt.py explain "find . -name '*.py' -exec grep -l 'import os' {} \\;"

# 交互模式
python run_shellgpt.py interactive
```

### 示例输出

```
🚀 生成的命令
┌─────────────────────────────────────────────────────────────┐
│ find . -name "*.py" -type f                                 │
└─────────────────────────────────────────────────────────────┘

📝 说明：    在当前目录及子目录中查找所有Python文件
🔧 类型：    文件操作  
🛡️  安全性：  ✅ 安全
🎯 置信度：  95.0%

是否执行此命令？ [Y/n]: 
```

## 🛡️ 安全特性

ShellGPT包含全面的安全机制：

- **🚨 危险检测** - 识别潜在的破坏性命令
- **⚠️ 警告系统** - 突出显示风险操作
- **🔒 确认提示** - 危险操作需要用户确认
- **❌ 禁用命令** - 阻止极其危险的操作
- **💡 安全替代** - 建议更安全的方法

### 安全级别

| 级别 | 描述 | 示例 |
|------|------|------|
| ✅ **安全** | 无风险检测 | `ls -la`, `git status` |
| ⚠️ **谨慎** | 潜在风险 | `rm file.txt`, `chmod 755` |
| 🚨 **危险** | 高风险操作 | `rm -rf /`, `sudo dd` |
| ❌ **禁止** | 安全阻止 | 恶意脚本 |

## 🧠 AI智能特性

### 自然语言处理

```bash
# 无需记住复杂语法：
python run_shellgpt.py ask "显示所有大于1GB且最近一个月修改过的文件"

# 生成：find . -type f -size +1G -mtime -30 -ls
```

### 上下文感知

ShellGPT了解你的环境：

- **📁 当前目录** - 根据位置调整命令
- **🔗 Git仓库** - 知道分支和状态  
- **💻 操作系统** - 使用适合平台的命令
- **🛠️ 可用工具** - 检查系统安装的工具

### 学习和适应

- **📊 使用模式** - 学习你偏好的工具和方法
- **🎯 个人偏好** - 记住你的配置选择
- **📈 持续改进** - 使用越多越智能

## ⚙️ 配置

### 配置文件

创建 `~/.config/shellgpt/config.yaml`：

```yaml
# OpenAI配置
openai_model: "gpt-3.5-turbo"
openai_max_tokens: 1000
openai_temperature: 0.1

# 安全配置
require_confirmation: true
enable_safety_checks: true
max_command_length: 1000

# 学习配置  
enable_learning: true
max_history_size: 1000

# 应用配置
debug: false
log_level: "INFO"
```

### 环境变量

```bash
export OPENAI_API_KEY="your-api-key-here"
export SHELLGPT_MODEL="gpt-4"
export SHELLGPT_ENABLE_SAFETY="true"
```

## 🔧 高级用法

### 命令别名

添加到shell配置文件：

```bash
# 简短别名
alias s="python run_shellgpt.py ask"
alias sx="python run_shellgpt.py ask --execute"  
alias se="python run_shellgpt.py explain"

# 快捷操作
alias sgi="python run_shellgpt.py ask '显示git状态'"
alias sgl="python run_shellgpt.py ask '显示git日志'"
```

### 与现有工具集成

```bash
# 将输出传递给shellgpt进行解释
history | tail -1 | python run_shellgpt.py explain

# 与其他工具配合使用
python run_shellgpt.py ask "查找大文件" | head -10
```

## 🛠️ 开发

### 前置要求

- Python 3.8+
- OpenAI API密钥
- Git（用于Git相关功能）

### 开发环境设置

```bash
git clone https://github.com/ychenfen/shellgpt.git
cd shellgpt

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\\Scripts\\activate  # Windows

# 开发模式安装
pip install -e ".[dev]"

# 运行测试
python test_real_functionality.py

# 代码格式化
black shellgpt/
isort shellgpt/
```

### 项目结构

```
shellgpt/
├── core/               # 核心AI和处理引擎
│   ├── nlp_engine.py       # 自然语言处理
│   ├── command_generator.py # 命令生成
│   ├── context_manager.py   # 系统上下文感知
│   └── safety_checker.py    # 安全验证
├── models/             # 数据模型和架构
├── utils/              # 工具函数和模式
├── config/             # 配置管理
├── cli/               # 命令行界面
└── tests/             # 测试套件
```

## 🤝 贡献

我们欢迎贡献！请查看我们的[贡献指南](CONTRIBUTING.md)了解详情。

1. Fork仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开Pull Request

## 📊 路线图

- [x] **核心AI引擎** - 自然语言到shell命令转换
- [x] **安全系统** - 全面的安全检查和警告
- [x] **上下文感知** - Git、目录和系统上下文
- [x] **多平台支持** - Linux、macOS、Windows兼容性
- [ ] **插件系统** - 可扩展的自定义命令架构
- [ ] **Shell集成** - 原生shell补全和历史记录
- [ ] **团队共享** - 跨团队共享学习模式
- [ ] **高级学习** - 个人AI模型微调
- [ ] **GUI界面** - 非终端用户的桌面应用
- [ ] **移动应用** - iOS/Android伴侣应用

## ⚠️ 安全提醒

虽然ShellGPT包含全面的安全检查，但在执行生成的命令之前，请始终审查标记为"谨慎"或"危险"的命令。AI很强大但并非绝对可靠。

## 📝 许可证

此项目基于MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。

## 🙏 致谢

- **OpenAI** 提供驱动ShellGPT的GPT模型
- **Rich** 提供美观的命令行界面
- **Typer** 提供优秀的CLI框架
- **开源社区** 提供灵感和反馈

## 📞 支持

- 📚 [文档](https://github.com/ychenfen/shellgpt/wiki)
- 🐛 [报告问题](https://github.com/ychenfen/shellgpt/issues)
- 💬 [讨论](https://github.com/ychenfen/shellgpt/discussions)
- 📧 邮箱: 2570601904@qq.com

## 🌟 支持我们

如果ShellGPT帮助你提高了效率，请考虑：

- ⭐ **[为此仓库加星](https://github.com/ychenfen/shellgpt/stargazers)** - 这对我们意义重大！
- 🐦 **在社交媒体分享** - 帮助其他人发现这个工具
- 📝 **写下你的体验** - 欢迎博客文章！
- 💝 **[参与项目贡献](CONTRIBUTING.md)** - 感谢所有贡献
- 🐛 **[报告bug](https://github.com/ychenfen/shellgpt/issues/new?template=bug_report.md)** - 帮助我们改进
- 💡 **[请求功能](https://github.com/ychenfen/shellgpt/issues/new?template=feature_request.md)** - 分享你的想法

### 🏆 为什么要为这个项目加星？

- ✅ **生产就绪** - 不是演示，而是真正的工具
- 🧠 **AI驱动** - 智能的自然语言理解  
- 🛡️ **安全优先** - 内置安全机制
- 🎨 **美观界面** - 现代终端体验
- 📈 **积极开发** - 定期更新和改进
- 🌍 **开源** - 永远免费，社区驱动

**[⭐ 点击这里为仓库加星 ⭐](https://github.com/ychenfen/shellgpt)**

---

<div align="center">

**[⭐ 在GitHub上为我们加星](https://github.com/ychenfen/shellgpt)，如果你觉得这个项目有用！**

由开发者为开发者制作，用 ❤️ 打造。

</div>