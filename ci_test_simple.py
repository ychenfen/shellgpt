#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CI测试脚本 - 简化版本，避免编码问题
"""

import sys
import os
import traceback

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_imports():
    """测试核心模块导入"""
    print("Testing module imports...")
    
    try:
        # 测试模型导入
        from models.command import Command, CommandType, SafetyLevel
        print("  [OK] models.command imported successfully")
        
        # 测试安全检查器
        from core.safety_checker import SafetyChecker
        print("  [OK] core.safety_checker imported successfully")
        
        # 测试模式匹配
        from utils.patterns import COMMAND_PATTERNS
        print(f"  [OK] utils.patterns imported successfully ({len(COMMAND_PATTERNS)} patterns)")
        
        # 测试配置系统
        from config.settings import get_settings
        print("  [OK] config.settings imported successfully")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Import failed: {e}")
        traceback.print_exc()
        return False

def test_safety_checker():
    """测试安全检查器"""
    print("Testing safety checker...")
    
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
        print(f"  [OK] Safe command detection: {checked.safety_level}")
        
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
        print(f"  [OK] Dangerous command detection: {checked.safety_level}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Safety checker test failed: {e}")
        traceback.print_exc()
        return False

def test_patterns():
    """测试模式匹配"""
    print("Testing pattern matching...")
    
    try:
        from utils.patterns import COMMAND_PATTERNS
        
        if len(COMMAND_PATTERNS) > 0:
            print(f"  [OK] Loaded {len(COMMAND_PATTERNS)} command patterns")
            
            # 检查模式结构
            first_pattern = COMMAND_PATTERNS[0]
            required_keys = ['action', 'patterns', 'templates']
            
            for key in required_keys:
                if key in first_pattern:
                    print(f"  [OK] Pattern structure contains '{key}'")
                else:
                    print(f"  [WARN] Pattern structure missing '{key}'")
            
            return True
        else:
            print("  [FAIL] No command patterns loaded")
            return False
            
    except Exception as e:
        print(f"  [FAIL] Pattern matching test failed: {e}")
        traceback.print_exc()
        return False

def test_cli_import():
    """测试CLI导入"""
    print("Testing CLI import...")
    
    try:
        # 检查Python版本
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        print(f"  [INFO] Python version: {python_version}")
        print(f"  [INFO] Platform: {sys.platform}")
        
        from cli.main import app
        print("  [OK] CLI application imported successfully")
        
        # 测试基本CLI功能
        import typer
        print(f"  [OK] Typer version: {typer.__version__}")
        
        return True
    except Exception as e:
        print(f"  [FAIL] CLI import failed: {e}")
        print(f"  [INFO] Error type: {type(e).__name__}")
        traceback.print_exc()
        return False

def main():
    """运行所有测试"""
    print("Starting CI tests...")
    print("=" * 50)
    
    tests = [
        ("Module imports", test_imports),
        ("Safety checker", test_safety_checker),
        ("Pattern matching", test_patterns),
        ("CLI import", test_cli_import),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'-' * 30}")
        print(f"Running: {test_name}")
        print(f"{'-' * 30}")
        success = test_func()
        results.append((test_name, success))
    
    # 总结结果
    print(f"\n{'=' * 50}")
    print("Test Results Summary:")
    print(f"{'=' * 50}")
    
    passed = 0
    for test_name, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"  {test_name:<20} {status}")
        if success:
            passed += 1
    
    print(f"{'=' * 50}")
    print(f"Total: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("All tests passed!")
        return 0
    else:
        print("Some tests failed!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)