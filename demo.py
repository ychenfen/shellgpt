#!/usr/bin/env python3
"""ShellGPT 演示脚本 - 展示核心功能"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.prompt import Prompt

# 直接导入避免相对导入问题
from models.command import Command, CommandType, SafetyLevel
from core.safety_checker import SafetyChecker
from utils.patterns import COMMAND_PATTERNS

console = Console()

def show_welcome():
    """显示欢迎信息"""
    welcome_text = """
🤖 **ShellGPT** - AI驱动的智能命令行助手

特色功能：
• 🧠 自然语言转shell命令
• 🔍 上下文感知 (Git、目录、系统)
• 🛡️ 四级安全检查系统
• ⚡ 模式匹配快速响应
• 🎨 美观的终端界面
"""
    console.print(Panel(welcome_text, title="欢迎使用 ShellGPT", border_style="green"))

def demo_safety_system():
    """演示安全检查系统"""
    console.print("\n🛡️ **安全检查系统演示**\n")
    
    safety_checker = SafetyChecker()
    
    # 测试不同安全级别的命令
    test_commands = [
        ("ls -la", "列出目录文件"),
        ("rm file.txt", "删除单个文件"),
        ("rm -rf /", "删除根目录"),
        ("sudo dd if=/dev/zero of=/dev/sda", "危险的磁盘操作"),
    ]
    
    table = Table(title="安全级别检测")
    table.add_column("命令", style="cyan")
    table.add_column("说明", style="white")
    table.add_column("安全级别", style="bold")
    table.add_column("建议", style="yellow")
    
    for cmd, desc in test_commands:
        command = Command(
            shell_command=cmd,
            command_type=CommandType.SYSTEM_OPERATION,
            explanation=desc,
            confidence=0.9
        )
        
        checked = safety_checker.check_command_safety(command)
        
        # 安全级别样式
        level_style = {
            SafetyLevel.SAFE: "✅ 安全",
            SafetyLevel.CAUTIOUS: "⚠️ 谨慎", 
            SafetyLevel.DANGEROUS: "🚨 危险",
            SafetyLevel.FORBIDDEN: "❌ 禁止"
        }
        
        recommendation = "建议执行" if checked.safety_level == SafetyLevel.SAFE else \
                        "需要确认" if checked.safety_level == SafetyLevel.CAUTIOUS else \
                        "强烈警告" if checked.safety_level == SafetyLevel.DANGEROUS else \
                        "已阻止"
        
        table.add_row(cmd, desc, level_style[checked.safety_level], recommendation)
    
    console.print(table)

def demo_pattern_matching():
    """演示模式匹配系统"""
    console.print("\n⚡ **模式匹配系统演示**\n")
    
    table = Table(title="常用命令模式")
    table.add_column("自然语言", style="green")
    table.add_column("生成命令", style="cyan")
    table.add_column("类型", style="yellow")
    
    # 展示一些模式
    sample_patterns = [
        ("list files", "ls -la", "文件操作"),
        ("show processes", "ps aux", "系统信息"),
        ("git status", "git status", "Git操作"),
        ("disk usage", "df -h", "系统信息"),
        ("memory usage", "free -h", "系统信息"),
    ]
    
    for query, cmd, cmd_type in sample_patterns:
        table.add_row(query, cmd, cmd_type)
    
    console.print(table)
    console.print(f"\n📊 **总共支持 {len(COMMAND_PATTERNS)} 种常用命令模式**")

def demo_command_output():
    """演示命令输出格式"""
    console.print("\n🎨 **命令输出演示**\n")
    
    # 模拟一个生成的命令
    sample_command = """find . -name "*.py" -type f -exec grep -l "import os" {} \\;"""
    
    # 显示命令面板
    syntax = Syntax(sample_command, "bash", theme="monokai", line_numbers=False)
    panel = Panel(
        syntax,
        title="🚀 Generated Command",
        border_style="green",
        padding=(1, 2)
    )
    console.print(panel)
    
    # 显示详细信息
    info_table = Table(show_header=False, box=None, padding=(0, 2))
    info_table.add_row("📝 Explanation:", "Find all Python files that import os module")
    info_table.add_row("🔧 Type:", "File Search")
    info_table.add_row("🛡️  Safety:", "✅ Safe")
    info_table.add_row("🎯 Confidence:", "95.0%")
    console.print(info_table)

def interactive_demo():
    """交互式演示"""
    console.print("\n💬 **交互式演示**\n")
    
    console.print("尝试一些自然语言查询（输入 'quit' 退出）:")
    console.print("例如: 'list files', 'show git status', 'check disk space'\n")
    
    safety_checker = SafetyChecker()
    
    while True:
        try:
            query = Prompt.ask("🤖 ShellGPT")
            
            if query.lower() in ['quit', 'exit', 'q']:
                console.print("👋 再见！")
                break
                
            # 简单的模式匹配演示
            pattern_map = {
                "list files": "ls -la",
                "show git status": "git status", 
                "check disk space": "df -h",
                "show processes": "ps aux",
                "memory usage": "free -h",
            }
            
            if query.lower() in pattern_map:
                cmd = pattern_map[query.lower()]
                
                # 创建命令对象
                command = Command(
                    shell_command=cmd,
                    command_type=CommandType.SYSTEM_OPERATION,
                    explanation=f"Execute: {query}",
                    confidence=0.95
                )
                
                # 安全检查
                checked = safety_checker.check_command_safety(command)
                
                # 显示结果
                syntax = Syntax(cmd, "bash", theme="monokai")
                console.print(Panel(syntax, title="生成的命令", border_style="green"))
                console.print(f"🛡️ 安全级别: {checked.safety_level.value}")
                
            else:
                console.print("💡 这是一个演示版本，实际版本会使用AI生成命令")
                console.print("   尝试: 'list files', 'show git status', 'check disk space'")
                
        except KeyboardInterrupt:
            console.print("\n👋 再见！")
            break
        except Exception as e:
            console.print(f"❌ 错误: {e}")

def main():
    """主函数"""
    show_welcome()
    demo_safety_system()
    demo_pattern_matching()
    demo_command_output()
    
    console.print("\n" + "="*60)
    console.print("✨ **ShellGPT 核心功能演示完成!**")
    console.print("📝 要使用完整AI功能，请设置OpenAI API密钥")
    console.print("="*60)
    
    # 询问是否要进行交互式演示
    if Prompt.ask("\n🎮 是否要试用交互式演示？", choices=["y", "n"], default="n") == "y":
        interactive_demo()

if __name__ == "__main__":
    main()