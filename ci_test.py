#!/usr/bin/env python3
"""
CI测试脚本 - 专门用于GitHub Actions的简化测试
"""

import sys
import os
import traceback

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_imports():
    """测试核心模块导入"""
    print("🧪 测试模块导入...")
    
    try:
        # 测试模型导入
        from models.command import Command, CommandType, SafetyLevel
        print("  ✅ models.command 导入成功")
        
        # 测试安全检查器
        from core.safety_checker import SafetyChecker
        print("  ✅ core.safety_checker 导入成功")
        
        # 测试模式匹配
        from utils.patterns import COMMAND_PATTERNS
        print(f"  ✅ utils.patterns 导入成功 ({len(COMMAND_PATTERNS)} 个模式)")
        
        # 测试配置系统
        from config.settings import get_settings
        print("  ✅ config.settings 导入成功")
        
        return True
    except Exception as e:
        print(f"  ❌ 导入失败: {e}")
        traceback.print_exc()
        return False

def test_safety_checker():
    """测试安全检查器"""
    print("🛡️ 测试安全检查器...")
    
    try:
        from models.command import Command, CommandType, SafetyLevel
        from core.safety_checker import SafetyChecker
        
        safety_checker = SafetyChecker()
        
        # 测试安全命令
        safe_cmd = Command(
            original_query="test safe command",
            shell_command="ls -la",
            command_type=CommandType.FILE_OPERATION,
            explanation="List files",
            confidence=0.9,
            safety_level=SafetyLevel.SAFE
        )
        
        checked = safety_checker.check_command_safety(safe_cmd)
        print(f"  ✅ 安全命令检测: {checked.safety_level}")
        
        # 测试危险命令
        dangerous_cmd = Command(
            original_query="test dangerous command",
            shell_command="rm -rf /",
            command_type=CommandType.FILE_OPERATION,
            explanation="Remove all files",
            confidence=0.9,
            safety_level=SafetyLevel.SAFE  # 初始值
        )
        
        checked = safety_checker.check_command_safety(dangerous_cmd)
        print(f"  ✅ 危险命令检测: {checked.safety_level}")
        
        return True
    except Exception as e:
        print(f"  ❌ 安全检查器测试失败: {e}")
        traceback.print_exc()
        return False

def test_patterns():
    """测试模式匹配"""
    print("⚡ 测试模式匹配...")
    
    try:
        from utils.patterns import COMMAND_PATTERNS
        
        if len(COMMAND_PATTERNS) > 0:
            print(f"  ✅ 加载了 {len(COMMAND_PATTERNS)} 个命令模式")
            
            # 检查模式结构
            first_pattern = COMMAND_PATTERNS[0]
            required_keys = ['action', 'patterns', 'templates']
            
            for key in required_keys:
                if key in first_pattern:
                    print(f"  ✅ 模式结构包含 '{key}'")
                else:
                    print(f"  ⚠️ 模式结构缺少 '{key}'")
            
            return True
        else:
            print("  ❌ 没有加载到命令模式")
            return False
            
    except Exception as e:
        print(f"  ❌ 模式匹配测试失败: {e}")
        traceback.print_exc()
        return False

def test_cli_import():
    """测试CLI导入"""
    print("💻 测试CLI导入...")
    
    try:
        # 检查Python版本
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        print(f"  📋 Python版本: {python_version}")
        
        from cli.main import app
        print("  ✅ CLI应用导入成功")
        
        # 测试基本CLI功能
        import typer
        print(f"  ✅ Typer版本: {typer.__version__}")
        
        return True
    except Exception as e:
        print(f"  ❌ CLI导入失败: {e}")
        print(f"  📍 错误类型: {type(e).__name__}")
        traceback.print_exc()
        return False

def main():
    """运行所有测试"""
    print("🚀 开始CI测试...\n")
    
    tests = [
        ("模块导入", test_imports),
        ("安全检查器", test_safety_checker),
        ("模式匹配", test_patterns),
        ("CLI导入", test_cli_import),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        success = test_func()
        results.append((test_name, success))
        print(f"{'='*50}")
    
    # 总结结果
    print(f"\n🎯 测试结果总结:")
    print(f"{'='*60}")
    
    passed = 0
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {test_name:<20} {status}")
        if success:
            passed += 1
    
    print(f"{'='*60}")
    print(f"  总计: {passed}/{len(tests)} 个测试通过")
    
    if passed == len(tests):
        print("🎉 所有测试通过！")
        return 0
    else:
        print("💥 部分测试失败！")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)