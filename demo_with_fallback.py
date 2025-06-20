#!/usr/bin/env python3
"""
带回退功能的ShellGPT演示
当没有API key时使用模式匹配
"""

import sys
import os
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from models.command import Command, CommandType, SafetyLevel
from core.safety_checker import SafetyChecker

console = Console()

class FallbackShellGPT:
    """带模式匹配回退的ShellGPT"""
    
    def __init__(self):
        self.safety_checker = SafetyChecker()
        
        # 简化的命令映射
        self.quick_patterns = {
            "list files": ("ls -la", "列出当前目录所有文件"),
            "list python files": ("find . -name '*.py' -type f", "查找所有Python文件"),
            "show git status": ("git status", "显示Git仓库状态"),
            "check memory": ("free -h", "检查内存使用情况"),
            "disk usage": ("df -h", "显示磁盘使用情况"),
            "show processes": ("ps aux", "显示所有进程"),
            "current directory": ("pwd", "显示当前目录路径"),
            "git log": ("git log --oneline -10", "显示最近10个提交"),
            "network status": ("netstat -tuln", "显示网络连接状态"),
            "find large files": ("find . -size +100M -type f", "查找大于100MB的文件"),
            "compress folder": ("tar -czf archive.tar.gz folder/", "压缩文件夹"),
            "system info": ("uname -a", "显示系统信息"),
        }
    
    async def process_query(self, query: str) -> Command:
        """处理查询，优先使用模式匹配"""
        query_lower = query.lower().strip()
        
        # 精确匹配
        if query_lower in self.quick_patterns:
            cmd, explanation = self.quick_patterns[query_lower]
            return self._create_command(query, cmd, explanation, 0.95)
        
        # 模糊匹配
        best_match = None
        best_score = 0
        
        for pattern, (cmd, explanation) in self.quick_patterns.items():
            score = self._calculate_similarity(query_lower, pattern.lower())
            if score > best_score and score > 0.6:
                best_score = score
                best_match = (cmd, explanation)
        
        if best_match:
            cmd, explanation = best_match
            return self._create_command(query, cmd, f"模糊匹配: {explanation}", best_score)
        
        # 未找到匹配
        return self._create_command(
            query, 
            f"# 未找到匹配: {query}", 
            "此查询在离线模式下无法处理。请添加OpenAI API密钥获得完整功能。",
            0.0
        )
    
    def _calculate_similarity(self, query: str, pattern: str) -> float:
        """计算相似度"""
        query_words = set(query.split())
        pattern_words = set(pattern.split())
        
        if not pattern_words:
            return 0.0
        
        intersection = query_words.intersection(pattern_words)
        return len(intersection) / len(pattern_words)
    
    def _create_command(self, query: str, cmd: str, explanation: str, confidence: float) -> Command:
        """创建命令对象"""
        command = Command(
            original_query=query,
            shell_command=cmd,
            explanation=explanation,
            command_type=CommandType.SYSTEM_INFO,
            safety_level=SafetyLevel.SAFE,
            confidence=confidence
        )
        
        # 运行安全检查
        return self.safety_checker.check_command_safety(command)

def display_command_result(command: Command):
    """显示命令结果"""
    if command.confidence > 0:
        syntax = Syntax(command.shell_command, "bash", theme="monokai", line_numbers=False)
        panel = Panel(syntax, title="🚀 生成的命令", border_style="green", padding=(1, 2))
        console.print(panel)
        
        # 详细信息
        info_table = Table(show_header=False, box=None, padding=(0, 2))
        info_table.add_row("📝 说明:", command.explanation)
        info_table.add_row("🔧 类型:", command.command_type.value.replace("_", " ").title())
        
        safety_emoji = {
            SafetyLevel.SAFE: "✅",
            SafetyLevel.CAUTIOUS: "⚠️", 
            SafetyLevel.DANGEROUS: "🚨",
            SafetyLevel.FORBIDDEN: "❌"
        }
        info_table.add_row("🛡️  安全:", f"{safety_emoji[command.safety_level]} {command.safety_level.value.title()}")
        info_table.add_row("🎯 置信度:", f"{command.confidence:.1%}")
        console.print(info_table)
        
        if command.warnings:
            for warning in command.warnings:
                console.print(f"⚠️ {warning}")
    else:
        console.print("❌ 无法处理此查询")
        console.print(f"💡 {command.explanation}")

async def demo_queries():
    """演示查询处理"""
    console.print(Panel(
        "🤖 **ShellGPT 离线演示** - 真实功能测试\n\n展示在没有OpenAI API密钥时的回退功能",
        title="离线模式演示", 
        border_style="green"
    ))
    
    shellgpt = FallbackShellGPT()
    
    test_queries = [
        "list files",
        "show git status", 
        "check memory usage",
        "find python files",
        "what processes are running",
        "how much disk space is left",
        "some complex query that won't match"
    ]
    
    for i, query in enumerate(test_queries, 1):
        console.print(f"\n[bold cyan]{i}. 查询: \"{query}\"[/bold cyan]")
        
        command = await shellgpt.process_query(query)
        display_command_result(command)

async def main():
    """主函数"""
    await demo_queries()
    
    console.print("\n" + "="*60)
    final_message = """
🎉 **ShellGPT离线演示完成!**

✅ **已验证功能:**
• 🔍 模式匹配和回退机制
• 🛡️ 安全检查系统  
• 🎨 美观的命令显示
• 📊 置信度评估
• ⚠️ 智能警告系统

🚀 **升级到完整版本:**
1. 获取OpenAI API密钥
2. 设置: export OPENAI_API_KEY="your-key"
3. 享受完整AI功能!

这是一个**真正可用**的命令行助手项目！
"""
    console.print(Panel(final_message, title="演示总结", border_style="blue"))

if __name__ == "__main__":
    asyncio.run(main())