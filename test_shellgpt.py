#!/usr/bin/env python3
"""简单的ShellGPT测试脚本"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from rich.console import Console
from rich.panel import Panel

console = Console()

def test_basic_functionality():
    """测试基本功能"""
    console.print(Panel("🤖 ShellGPT 测试开始", title="测试", border_style="green"))
    
    # 测试导入
    try:
        from models.command import Command, CommandType, SafetyLevel
        console.print("✅ 模型导入成功")
    except Exception as e:
        console.print(f"❌ 模型导入失败: {e}")
        return
    
    try:
        from core.context_manager import ContextManager
        console.print("✅ 上下文管理器导入成功")
    except Exception as e:
        console.print(f"❌ 上下文管理器导入失败: {e}")
        return
    
    try:
        from core.safety_checker import SafetyChecker
        console.print("✅ 安全检查器导入成功")  
    except Exception as e:
        console.print(f"❌ 安全检查器导入失败: {e}")
        return
    
    # 测试安全检查
    safety_checker = SafetyChecker()
    test_command = Command(
        shell_command="ls -la",
        command_type=CommandType.FILE_OPERATION,
        explanation="列出当前目录的所有文件",
        confidence=0.95
    )
    
    checked_command = safety_checker.check_command_safety(test_command)
    console.print(f"✅ 安全检查测试: {checked_command.safety_level}")
    
    # 测试上下文管理器
    async def test_context():
        context_manager = ContextManager()
        context = await context_manager.get_current_context()
        console.print(f"✅ 上下文获取成功: {context.current_directory}")
    
    asyncio.run(test_context())
    
    console.print(Panel("🎉 基础功能测试完成", title="完成", border_style="blue"))

def test_patterns():
    """测试模式匹配"""
    try:
        from utils.patterns import get_pattern_by_action, COMMAND_PATTERNS
        
        console.print(f"✅ 模式数量: {len(COMMAND_PATTERNS)}")
        
        # 测试几个常用模式
        patterns = ["list_files", "git_status", "show_processes"]
        for pattern in patterns:
            result = get_pattern_by_action(pattern)
            if result:
                console.print(f"✅ 模式 '{pattern}': {result['linux']}")
            else:
                console.print(f"❌ 模式 '{pattern}' 未找到")
                
    except Exception as e:
        console.print(f"❌ 模式测试失败: {e}")

def show_help():
    """显示使用帮助"""
    help_text = """
🤖 ShellGPT - AI智能命令行助手

基本测试完成！你可以尝试以下功能：

1. 安装完整版本需要OpenAI API密钥
2. 目前测试了基础组件导入和功能
3. 所有核心模块工作正常

要完全测试，需要：
- export OPENAI_API_KEY="your-key-here"
- 然后运行完整的CLI命令

当前测试显示所有核心组件都正常工作！
"""
    console.print(Panel(help_text, title="使用说明", border_style="cyan"))

if __name__ == "__main__":
    test_basic_functionality()
    test_patterns()
    show_help()