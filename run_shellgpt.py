#!/usr/bin/env python3
"""
ShellGPT启动脚本 - 独立的可执行文件
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 导入CLI应用
from cli.main import app

if __name__ == "__main__":
    app()