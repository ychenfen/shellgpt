#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小化CI测试脚本 - 最大兼容性版本
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_basic_imports():
    """测试基础导入"""
    print("Testing basic imports...")
    
    try:
        # 测试基础Python库
        import typing
        print("  [OK] typing module available")
        
        # 测试第三方库
        import rich
        print("  [OK] rich library available")
        
        import typer
        print("  [OK] typer library available")
        
        import pydantic
        print("  [OK] pydantic library available")
        
        return True
    except Exception as e:
        print("  [FAIL] Basic import failed: {}".format(e))
        return False

def test_model_imports():
    """测试模型导入"""
    print("Testing model imports...")
    
    try:
        from models.command import Command, CommandType, SafetyLevel
        print("  [OK] Command models imported")
        return True
    except Exception as e:
        print("  [FAIL] Model import failed: {}".format(e))
        return False

def test_core_imports():
    """测试核心模块导入"""
    print("Testing core module imports...")
    
    try:
        from core.safety_checker import SafetyChecker
        print("  [OK] SafetyChecker imported")
        
        from utils.patterns import COMMAND_PATTERNS
        print("  [OK] Command patterns imported ({} patterns)".format(len(COMMAND_PATTERNS)))
        
        return True
    except Exception as e:
        print("  [FAIL] Core import failed: {}".format(e))
        return False

def test_basic_functionality():
    """测试基础功能"""
    print("Testing basic functionality...")
    
    try:
        from models.command import Command, CommandType, SafetyLevel
        from core.safety_checker import SafetyChecker
        
        # 创建安全检查器
        checker = SafetyChecker()
        
        # 创建测试命令
        cmd = Command(
            original_query="test command",
            shell_command="ls -la",
            command_type=CommandType.FILE_OPERATION,
            explanation="List files",
            confidence=0.9,
            safety_level=SafetyLevel.SAFE
        )
        
        # 运行安全检查
        result = checker.check_command_safety(cmd)
        print("  [OK] Safety check works: {}".format(result.safety_level))
        
        return True
    except Exception as e:
        print("  [FAIL] Functionality test failed: {}".format(e))
        return False

def main():
    """运行所有测试"""
    print("Starting minimal CI tests...")
    print("Python version: {}.{}".format(sys.version_info.major, sys.version_info.minor))
    print("Platform: {}".format(sys.platform))
    print("=" * 50)
    
    tests = [
        ("Basic imports", test_basic_imports),
        ("Model imports", test_model_imports),
        ("Core imports", test_core_imports), 
        ("Basic functionality", test_basic_functionality),
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print("\n{}".format(test_name))
        print("-" * 30)
        if test_func():
            passed += 1
            print("Result: PASS")
        else:
            print("Result: FAIL")
    
    print("\n" + "=" * 50)
    print("Summary: {}/{} tests passed".format(passed, len(tests)))
    
    if passed == len(tests):
        print("All tests passed!")
        return 0
    else:
        print("Some tests failed!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)