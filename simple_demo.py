#!/usr/bin/env python3
"""ShellGPT 简单演示 - 展示项目结构和理念"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.tree import Tree
import os

console = Console()

def show_project_overview():
    """显示项目概览"""
    overview = """
🤖 **ShellGPT** - AI驱动的智能命令行助手

🎯 **核心理念**
将自然语言转换为精确的Shell命令，让命令行操作更加直观和安全

🚀 **主要特性**
• 🧠 AI驱动的自然语言理解
• 🔍 智能上下文感知 (Git状态、目录结构、系统信息)
• 🛡️ 四级安全检查系统 (安全/谨慎/危险/禁止)
• ⚡ 模式匹配加速常用操作
• 🎨 美观的Rich终端界面
• 🔧 灵活的配置管理系统
"""
    console.print(Panel(overview, title="🌟 ShellGPT 项目概览", border_style="green"))

def show_architecture():
    """显示项目架构"""
    console.print("\n🏗️ **项目架构**\n")
    
    tree = Tree("📁 shellgpt/")
    tree.add("📁 [cyan]core/[/cyan] - 核心AI引擎")
    tree.add("  └── 🧠 nlp_engine.py - 自然语言处理")
    tree.add("  └── 🔧 command_generator.py - 命令生成器")
    tree.add("  └── 🔍 context_manager.py - 上下文管理")
    tree.add("  └── 🛡️ safety_checker.py - 安全检查")
    
    tree.add("📁 [yellow]models/[/yellow] - 数据模型")
    tree.add("  └── 📋 command.py - 命令数据结构")
    
    tree.add("📁 [green]cli/[/green] - 命令行界面")
    tree.add("  └── 💻 main.py - 主CLI应用")
    
    tree.add("📁 [blue]config/[/blue] - 配置管理")
    tree.add("  └── ⚙️ settings.py - 配置系统")
    
    tree.add("📁 [magenta]utils/[/magenta] - 工具函数")
    tree.add("  └── 🔍 patterns.py - 命令模式匹配")
    
    console.print(tree)

def show_safety_levels():
    """展示安全级别系统"""
    console.print("\n🛡️ **安全检查系统**\n")
    
    table = Table(title="四级安全检查机制")
    table.add_column("级别", style="bold")
    table.add_column("图标", style="bold")
    table.add_column("描述", style="white")
    table.add_column("示例命令", style="cyan")
    table.add_column("行为", style="yellow")
    
    safety_data = [
        ("Safe", "✅", "无风险操作", "ls, pwd, git status", "直接执行"),
        ("Cautious", "⚠️", "需要注意的操作", "rm file.txt, chmod 755", "询问确认"),
        ("Dangerous", "🚨", "高风险操作", "rm -rf *, sudo commands", "强烈警告"),
        ("Forbidden", "❌", "禁止的操作", "格式化磁盘，恶意脚本", "完全阻止")
    ]
    
    for level, icon, desc, example, behavior in safety_data:
        table.add_row(level, icon, desc, example, behavior)
    
    console.print(table)

def show_usage_examples():
    """显示使用示例"""
    console.print("\n📖 **使用示例**\n")
    
    examples = [
        ("列出Python文件", "shellgpt ask \"list all python files\"", "find . -name '*.py' -type f"),
        ("查看Git状态", "shellgpt ask \"show git status\"", "git status"),
        ("查找大文件", "shellgpt ask \"find files larger than 100MB\"", "find . -size +100M -type f"),
        ("压缩文件夹", "shellgpt ask \"compress project folder\"", "tar -czf project.tar.gz project/"),
        ("查看系统信息", "shellgpt ask \"show system information\"", "uname -a && lscpu && free -h")
    ]
    
    for i, (desc, query, result) in enumerate(examples, 1):
        console.print(f"[bold cyan]{i}. {desc}[/bold cyan]")
        console.print(f"   [dim]输入:[/dim] {query}")
        
        syntax = Syntax(result, "bash", theme="monokai", line_numbers=False)
        console.print("   [dim]生成:[/dim]", end=" ")
        console.print(syntax)
        console.print()

def show_ai_features():
    """展示AI功能特性"""
    console.print("🧠 **AI智能特性**\n")
    
    features = [
        "🎯 **上下文感知**: 了解当前目录、Git仓库状态、操作系统类型",
        "🔍 **智能解析**: 支持复杂的自然语言查询和多步骤操作",
        "💡 **学习能力**: 记住用户偏好和常用操作模式",
        "🔄 **多方案生成**: 为同一需求提供多种实现方案",
        "📊 **置信度评估**: 每个生成的命令都有置信度评分",
        "🌐 **跨平台适配**: 自动适配Linux、macOS、Windows命令差异"
    ]
    
    for feature in features:
        console.print(f"  {feature}")
    
    console.print()

def show_installation_guide():
    """显示安装指南"""
    console.print("📦 **安装和使用指南**\n")
    
    install_steps = """
# 1. 克隆仓库
git clone https://github.com/ychenfen/shellgpt.git
cd shellgpt

# 2. 安装依赖
pip install -e .

# 3. 配置API密钥
export OPENAI_API_KEY="your-openai-api-key"

# 4. 开始使用
shellgpt ask "list all python files"
shellgpt ask "show git status" --execute
shellgpt interactive
"""
    
    syntax = Syntax(install_steps, "bash", theme="monokai")
    console.print(Panel(syntax, title="安装步骤", border_style="blue"))

def show_tech_stack():
    """显示技术栈"""
    console.print("🛠️ **技术栈**\n")
    
    table = Table(title="核心技术组件")
    table.add_column("组件", style="cyan")
    table.add_column("技术", style="green")
    table.add_column("用途", style="white")
    
    tech_data = [
        ("AI引擎", "OpenAI GPT-3.5/4", "自然语言理解和命令生成"),
        ("CLI框架", "Typer + Rich", "美观的命令行界面"),
        ("数据验证", "Pydantic", "类型安全的数据模型"),
        ("异步处理", "AsyncIO", "高性能的异步操作"),
        ("系统集成", "PSUtil + GitPython", "系统信息和Git集成"),
        ("配置管理", "PyYAML", "灵活的配置文件支持")
    ]
    
    for component, tech, purpose in tech_data:
        table.add_row(component, tech, purpose)
    
    console.print(table)

def main():
    """主演示函数"""
    console.clear()
    
    show_project_overview()
    show_architecture()
    show_safety_levels()
    show_ai_features()
    show_usage_examples()
    show_tech_stack()
    show_installation_guide()
    
    console.print("\n" + "="*80)
    final_message = """
🎉 **ShellGPT演示完成！**

这是一个完整的AI驱动命令行助手项目，具备：
✅ 完整的项目架构和代码实现
✅ 四级安全检查系统
✅ 智能上下文感知能力
✅ 美观的终端用户界面
✅ 跨平台兼容性支持

🚀 **下一步**: 获取OpenAI API密钥即可开始使用完整功能！
📚 **文档**: 查看README.md了解详细使用方法
🐛 **反馈**: 在GitHub上提交issues和建议
"""
    
    console.print(Panel(final_message, title="演示总结", border_style="green"))

if __name__ == "__main__":
    main()