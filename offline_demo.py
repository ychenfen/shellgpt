#!/usr/bin/env python3
"""
ShellGPT离线演示 - 不需要API key的功能展示
"""

import sys
import os
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.prompt import Prompt, Confirm

from models.command import Command, CommandType, SafetyLevel
from core.safety_checker import SafetyChecker
from utils.patterns import COMMAND_PATTERNS

console = Console()

class OfflineShellGPT:
    """离线版本的ShellGPT，使用模式匹配"""
    
    def __init__(self):
        self.safety_checker = SafetyChecker()
        self.command_patterns = {
            # 文件操作
            "list files": "ls -la",
            "list all files": "ls -la", 
            "show files": "ls -la",
            "list python files": "find . -name '*.py' -type f",
            "find python files": "find . -name '*.py' -type f",
            "list directories": "ls -d */",
            "show hidden files": "ls -la",
            
            # Git操作
            "git status": "git status",
            "show git status": "git status",
            "git log": "git log --oneline -10",
            "show commits": "git log --oneline -10",
            "git diff": "git diff",
            "show changes": "git diff",
            
            # 系统信息
            "show processes": "ps aux",
            "list processes": "ps aux",
            "check memory": "free -h",
            "memory usage": "free -h",
            "disk space": "df -h",
            "disk usage": "df -h", 
            "system info": "uname -a",
            
            # 网络
            "check network": "ping -c 4 google.com",
            "network status": "netstat -tuln",
            "show ports": "netstat -tuln",
            
            # 文件搜索
            "find large files": "find . -size +100M -type f",
            "find big files": "find . -size +100M -type f",
            "search text": "grep -r 'pattern' .",
            
            # 压缩解压
            "compress folder": "tar -czf archive.tar.gz folder/",
            "extract tar": "tar -xzf archive.tar.gz",
            "create zip": "zip -r archive.zip folder/",
        }
    
    def find_command(self, query: str) -> Command:
        """根据查询找到匹配的命令"""
        query_lower = query.lower().strip()
        
        # 精确匹配
        if query_lower in self.command_patterns:
            shell_cmd = self.command_patterns[query_lower]
            return Command(
                shell_command=shell_cmd,
                command_type=CommandType.SYSTEM_INFO,
                explanation=f"Execute: {query}",
                confidence=0.95,
                safety_level=SafetyLevel.SAFE,
                original_query=query
            )
        
        # 模糊匹配
        for pattern, cmd in self.command_patterns.items():
            if any(word in query_lower for word in pattern.split()):
                if len([w for w in pattern.split() if w in query_lower]) >= len(pattern.split()) // 2:
                    return Command(
                        shell_command=cmd,
                        command_type=CommandType.SYSTEM_INFO,
                        explanation=f"Best match for: {query}",
                        confidence=0.75,
                        safety_level=SafetyLevel.SAFE,
                        original_query=query
                    )
        
        # 未找到匹配
        return Command(
            shell_command=f"# No pattern found for: {query}",
            command_type=CommandType.CUSTOM,
            explanation=f"No matching pattern found for '{query}'. This offline version supports limited commands.",
            confidence=0.0,
            safety_level=SafetyLevel.SAFE,
            original_query=query,
            warnings=["This is an offline demo. Install with OpenAI API key for full functionality."]
        )
    
    def explain_command(self, cmd: str) -> str:
        """解释命令（离线版本）"""
        explanations = {
            "ls": "List directory contents",
            "ls -la": "List all files including hidden ones with detailed information",
            "find": "Search for files and directories",
            "grep": "Search text patterns in files",
            "ps": "Display running processes",
            "df": "Display filesystem disk space usage",
            "free": "Display memory usage",
            "tar": "Archive files", 
            "git": "Git version control commands",
            "ping": "Test network connectivity",
            "netstat": "Display network connections",
            "uname": "Display system information"
        }
        
        for keyword, explanation in explanations.items():
            if cmd.strip().startswith(keyword):
                return f"{explanation}\n\nCommand: {cmd}\n\nNote: This is a basic offline explanation. Full AI explanations require OpenAI API key."
        
        return f"Command: {cmd}\n\nThis command is not in the offline explanation database. Use full version with OpenAI API key for detailed explanations."

def show_welcome():
    """显示欢迎信息"""
    welcome = """
🤖 **ShellGPT 离线演示版**

此版本展示核心功能，无需OpenAI API密钥：
• 🔍 模式匹配命令生成
• 🛡️ 安全检查系统
• 📝 基础命令解释
• 🎨 美观的终端界面

💡 完整版本支持：
• 🧠 AI自然语言理解
• 🔍 智能上下文感知
• 💬 复杂查询处理
• 📚 学习用户习惯
"""
    console.print(Panel(welcome, title="欢迎使用 ShellGPT", border_style="green"))

def demo_pattern_matching():
    """演示模式匹配"""
    console.print("\n⚡ **支持的命令模式演示**\n")
    
    shellgpt = OfflineShellGPT()
    
    sample_queries = [
        "list files",
        "show git status", 
        "check memory usage",
        "find python files",
        "compress folder",
        "show processes"
    ]
    
    table = Table(title="模式匹配结果")
    table.add_column("查询", style="green")
    table.add_column("生成命令", style="cyan")
    table.add_column("置信度", style="yellow")
    
    for query in sample_queries:
        command = shellgpt.find_command(query)
        confidence = f"{command.confidence:.1%}"
        table.add_row(query, command.shell_command, confidence)
    
    console.print(table)

def interactive_demo():
    """交互式演示"""
    console.print("\n💬 **交互式演示模式**\n")
    
    shellgpt = OfflineShellGPT()
    
    console.print("尝试以下查询类型：")
    console.print("• 文件操作: 'list files', 'find python files'")
    console.print("• Git操作: 'git status', 'show commits'") 
    console.print("• 系统信息: 'check memory', 'disk usage'")
    console.print("• 输入 'quit' 退出\n")
    
    while True:
        try:
            query = Prompt.ask("🤖 ShellGPT (offline)")
            
            if query.lower() in ['quit', 'exit', 'q']:
                console.print("👋 再见！")
                break
            
            if query.lower().startswith("explain "):
                cmd = query[8:].strip()
                explanation = shellgpt.explain_command(cmd)
                console.print(Panel(explanation, title="命令解释", border_style="blue"))
                continue
            
            # 生成命令
            command = shellgpt.find_command(query)
            
            # 安全检查
            checked_command = shellgpt.safety_checker.check_command_safety(command)
            
            # 显示结果
            if checked_command.confidence > 0:
                syntax = Syntax(checked_command.shell_command, "bash", theme="monokai", line_numbers=False)
                panel = Panel(syntax, title="🚀 生成的命令", border_style="green")
                console.print(panel)
                
                # 显示详细信息
                info_table = Table(show_header=False, box=None, padding=(0, 2))
                info_table.add_row("📝 说明:", checked_command.explanation)
                info_table.add_row("🛡️ 安全级别:", f"{_get_safety_emoji(checked_command.safety_level)} {checked_command.safety_level.value}")
                info_table.add_row("🎯 置信度:", f"{checked_command.confidence:.1%}")
                console.print(info_table)
                
                # 显示警告
                if checked_command.warnings:
                    for warning in checked_command.warnings:
                        console.print(f"⚠️ {warning}")
                
                # 询问是否执行
                if checked_command.confidence > 0.5 and checked_command.safety_level in [SafetyLevel.SAFE, SafetyLevel.CAUTIOUS]:
                    if Confirm.ask("是否执行此命令？", default=False):
                        console.print("💡 在真实环境中，命令将被执行")
                        console.print("  （此为演示模式，不会实际执行）")
                        
            else:
                console.print("❌ 未找到匹配的命令模式")
                console.print("💡 尝试: 'list files', 'git status', 'check memory'")
            
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n👋 再见！")
            break
        except Exception as e:
            console.print(f"❌ 错误: {e}")

def _get_safety_emoji(safety_level: SafetyLevel) -> str:
    """获取安全级别emoji"""
    return {
        SafetyLevel.SAFE: "✅",
        SafetyLevel.CAUTIOUS: "⚠️",
        SafetyLevel.DANGEROUS: "🚨", 
        SafetyLevel.FORBIDDEN: "❌"
    }.get(safety_level, "❓")

def show_upgrade_info():
    """显示升级信息"""
    upgrade_info = """
🚀 **升级到完整版本**

获得完整AI功能：

1. 获取OpenAI API密钥：
   • 访问 https://platform.openai.com/api-keys
   • 创建新的API密钥

2. 设置环境变量：
   export OPENAI_API_KEY="your-api-key"

3. 享受完整功能：
   • 🧠 智能自然语言理解
   • 🔍 复杂查询处理
   • 📚 学习和适应能力
   • 🌐 跨平台命令适配

现在就试试完整版本吧！
"""
    console.print(Panel(upgrade_info, title="升级指南", border_style="cyan"))

def main():
    """主函数"""
    console.clear()
    show_welcome()
    demo_pattern_matching()
    show_upgrade_info()
    
    if Prompt.ask("\n🎮 是否要试用交互式演示？", choices=["y", "n"], default="y") == "y":
        interactive_demo()

if __name__ == "__main__":
    main()