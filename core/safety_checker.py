"""Safety checking system for command validation."""

import re
from typing import List, Dict, Set, Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.command import Command, SafetyLevel


class SafetyChecker:
    """Analyzes commands for potential safety risks."""
    
    def __init__(self):
        """Initialize safety checker with predefined rules."""
        self.dangerous_patterns = self._load_dangerous_patterns()
        self.system_critical_paths = self._load_critical_paths()
        self.risky_flags = self._load_risky_flags()
        
    def _load_dangerous_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for dangerous commands."""
        return {
            "destructive": [
                r"\brm\s+-rf\s+/",
                r"\brm\s+-rf\s+\*",
                r"\bdd\s+if=.*of=/dev/",
                r"\bmkfs\.",
                r"\bformat\s+",
                r">\s*/dev/sd[a-z]",
                r"\bshred\s+",
                r"\bwipe\s+",
            ],
            "privilege_escalation": [
                r"\bsudo\s+rm\s+-rf",
                r"\bsudo\s+dd\s+",
                r"\bsudo\s+chmod\s+777",
                r"\bsu\s+-\s+",
                r"\bsudo\s+su\s+",
            ],
            "network_dangerous": [
                r"\bnc\s+.*-e\s+",
                r"\bnetcat\s+.*-e\s+",
                r"\bbash\s+-i\s+>&\s+/dev/tcp/",
                r"\bwget\s+.*\|\s*bash",
                r"\bcurl\s+.*\|\s*bash",
                r"\bcurl\s+.*\|\s*sh",
            ],
            "system_modification": [
                r"\bchmod\s+777\s+/",
                r"\bchown\s+.*:/",
                r">\s*/etc/",
                r"\bmount\s+",
                r"\bumount\s+",
                r"\bfdisk\s+",
                r"\bparted\s+",
            ],
            "credential_exposure": [
                r"\becho\s+.*password",
                r"\becho\s+.*token",
                r"\becho\s+.*secret",
                r"\bcat\s+.*\.pem",
                r"\bcat\s+.*\.key",
                r"\bcat\s+.*password",
            ]
        }
    
    def _load_critical_paths(self) -> Set[str]:
        """Load system critical paths that should be protected."""
        return {
            "/", "/bin", "/sbin", "/usr", "/etc", "/boot", "/sys", "/proc",
            "/dev", "/var/log", "/usr/bin", "/usr/sbin", "/lib", "/lib64",
            "C:\\Windows", "C:\\Program Files", "C:\\System32"
        }
    
    def _load_risky_flags(self) -> Dict[str, List[str]]:
        """Load risky command flags."""
        return {
            "rm": ["-rf", "-r", "-f", "--recursive", "--force"],
            "chmod": ["777", "666", "755"],
            "dd": ["of=/dev/", "if=/dev/"],
            "curl": ["|bash", "|sh", "|python"],
            "wget": ["|bash", "|sh", "|python"],
            "find": ["-delete", "-exec rm"],
        }
    
    def check_command_safety(self, command: Command) -> Command:
        """Analyze command for safety and update safety level."""
        shell_command = command.shell_command.lower()
        
        # Check for dangerous patterns
        danger_level, warnings = self._analyze_patterns(shell_command)
        
        # Check for critical path access
        path_warnings = self._check_critical_paths(shell_command)
        warnings.extend(path_warnings)
        
        # Check for risky flags
        flag_warnings = self._check_risky_flags(shell_command)
        warnings.extend(flag_warnings)
        
        # Additional context-based checks
        context_warnings = self._check_context_safety(command)
        warnings.extend(context_warnings)
        
        # Update command with safety assessment
        command.safety_level = danger_level
        command.warnings.extend(warnings)
        
        return command
    
    def _analyze_patterns(self, command: str) -> Tuple[SafetyLevel, List[str]]:
        """Analyze command against dangerous patterns."""
        warnings = []
        max_danger = SafetyLevel.SAFE
        
        for category, patterns in self.dangerous_patterns.items():
            for pattern in patterns:
                if re.search(pattern, command):
                    warnings.append(f"Detected {category} pattern: {pattern}")
                    if category == "destructive":
                        max_danger = SafetyLevel.DANGEROUS
                    elif category in ["privilege_escalation", "system_modification"]:
                        if max_danger != SafetyLevel.DANGEROUS:
                            max_danger = SafetyLevel.CAUTIOUS
                    elif category in ["network_dangerous", "credential_exposure"]:
                        if max_danger == SafetyLevel.SAFE:
                            max_danger = SafetyLevel.CAUTIOUS
        
        return max_danger, warnings
    
    def _check_critical_paths(self, command: str) -> List[str]:
        """Check if command targets critical system paths."""
        warnings = []
        
        for path in self.system_critical_paths:
            if path in command:
                warnings.append(f"Command targets critical system path: {path}")
        
        return warnings
    
    def _check_risky_flags(self, command: str) -> List[str]:
        """Check for risky command flags."""
        warnings = []
        
        for cmd, flags in self.risky_flags.items():
            if cmd in command:
                for flag in flags:
                    if flag in command:
                        warnings.append(f"Risky flag detected: {cmd} {flag}")
        
        return warnings
    
    def _check_context_safety(self, command: Command) -> List[str]:
        """Check safety based on command context."""
        warnings = []
        
        # Check if running as root/admin
        if command.context_used.get("user") == "root":
            warnings.append("Running as root user - extra caution advised")
        
        # Check if in important directory
        current_dir = command.context_used.get("current_directory", "")
        if any(important in current_dir.lower() for important in ["home", "documents", "desktop"]):
            if "rm" in command.shell_command.lower():
                warnings.append("Deletion command in user directory")
        
        # Check git context
        if command.context_used.get("git_repository"):
            git_commands = ["git reset --hard", "git clean -fd", "git push --force"]
            for git_cmd in git_commands:
                if git_cmd in command.shell_command.lower():
                    warnings.append(f"Potentially destructive git command: {git_cmd}")
        
        return warnings
    
    def get_safety_recommendation(self, command: Command) -> str:
        """Get safety recommendation for a command."""
        if command.safety_level == SafetyLevel.SAFE:
            return "✅ Command appears safe to execute"
        elif command.safety_level == SafetyLevel.CAUTIOUS:
            return "⚠️  Command requires caution - please review before executing"
        elif command.safety_level == SafetyLevel.DANGEROUS:
            return "🚨 DANGEROUS command detected - are you absolutely sure?"
        else:  # FORBIDDEN
            return "❌ Command is forbidden and will not be executed"
    
    def should_require_confirmation(self, command: Command) -> bool:
        """Determine if command should require user confirmation."""
        return command.safety_level in [SafetyLevel.CAUTIOUS, SafetyLevel.DANGEROUS]
    
    def is_command_forbidden(self, command: Command) -> bool:
        """Check if command is completely forbidden."""
        return command.safety_level == SafetyLevel.FORBIDDEN
    
    def sanitize_command(self, command: str) -> str:
        """Sanitize command by removing potentially dangerous elements."""
        # Remove obvious dangerous patterns
        sanitized = command
        
        # Remove pipe to bash/sh
        sanitized = re.sub(r'\|\s*(bash|sh|python)', '', sanitized)
        
        # Remove force flags in dangerous contexts
        if "rm" in sanitized and any(path in sanitized for path in self.system_critical_paths):
            sanitized = sanitized.replace("-rf", "-r").replace("-f", "")
        
        return sanitized.strip()
    
    def get_safer_alternative(self, command: Command) -> str:
        """Suggest a safer alternative to a dangerous command."""
        shell_cmd = command.shell_command.lower()
        
        if "rm -rf" in shell_cmd:
            return shell_cmd.replace("rm -rf", "rm -ri")  # Interactive mode
        
        if "chmod 777" in shell_cmd:
            return shell_cmd.replace("chmod 777", "chmod 755")  # More restrictive
        
        if "|bash" in shell_cmd or "|sh" in shell_cmd:
            # Suggest downloading first, then reviewing
            base_cmd = shell_cmd.split("|")[0]
            return f"{base_cmd} > /tmp/script.sh && cat /tmp/script.sh  # Review before: bash /tmp/script.sh"
        
        return "# No safer alternative available - manual review required"