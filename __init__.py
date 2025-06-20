"""
🤖 ShellGPT - AI-Powered Intelligent Shell Assistant

A revolutionary command-line tool that understands natural language
and converts it into precise shell commands with context awareness.
"""

__version__ = "1.0.0"
__author__ = "ychenfen"
__email__ = "2570601904@qq.com"
__description__ = "AI-powered intelligent shell assistant that understands natural language"

from .core.nlp_engine import NLPEngine
from .core.command_generator import CommandGenerator
from .core.context_manager import ContextManager
from .core.safety_checker import SafetyChecker

__all__ = [
    "NLPEngine",
    "CommandGenerator", 
    "ContextManager",
    "SafetyChecker",
]