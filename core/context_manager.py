"""Context management for intelligent command generation."""

import os
import platform
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
import psutil
import git

from ..models.command import SystemContext


class ContextManager:
    """Manages system context and environment information."""
    
    def __init__(self):
        """Initialize context manager."""
        self._cached_context: Optional[SystemContext] = None
        self._cache_valid_duration = 30  # seconds
        
    async def get_current_context(self, force_refresh: bool = False) -> SystemContext:
        """Get current system context with caching."""
        if not force_refresh and self._is_cache_valid():
            return self._cached_context
            
        context = await self._collect_context()
        self._cached_context = context
        return context
    
    def _is_cache_valid(self) -> bool:
        """Check if cached context is still valid."""
        if not self._cached_context:
            return False
        # Simple time-based cache validation
        return True  # For simplicity, always refresh for now
    
    async def _collect_context(self) -> SystemContext:
        """Collect comprehensive system context."""
        
        # Basic system information
        current_dir = os.getcwd()
        os_name = platform.system()
        shell_type = self._detect_shell()
        
        # Git information
        git_info = await self._get_git_context(current_dir)
        
        # Environment variables
        env_vars = self._get_relevant_env_vars()
        
        # Available tools
        tools = self._detect_available_tools()
        
        # Recent commands (from history if available)
        recent_commands = self._get_recent_commands()
        
        return SystemContext(
            current_directory=current_dir,
            operating_system=os_name,
            shell_type=shell_type,
            git_repository=git_info.get("repository"),
            git_branch=git_info.get("branch"),
            git_status=git_info.get("status"),
            environment_variables=env_vars,
            available_tools=tools,
            recent_commands=recent_commands
        )
    
    def _detect_shell(self) -> str:
        """Detect the current shell type."""
        shell = os.environ.get("SHELL", "")
        if "bash" in shell:
            return "bash"
        elif "zsh" in shell:
            return "zsh"
        elif "fish" in shell:
            return "fish"
        elif "powershell" in shell.lower() or "pwsh" in shell.lower():
            return "powershell"
        elif "cmd" in shell.lower():
            return "cmd"
        else:
            return "unknown"
    
    async def _get_git_context(self, directory: str) -> Dict[str, Optional[str]]:
        """Get Git repository context information."""
        try:
            repo = git.Repo(directory, search_parent_directories=True)
            
            # Get current branch
            current_branch = repo.active_branch.name if repo.active_branch else None
            
            # Get repository name
            repo_name = os.path.basename(repo.working_dir)
            
            # Get status summary
            status_summary = self._get_git_status_summary(repo)
            
            return {
                "repository": repo_name,
                "branch": current_branch,
                "status": status_summary
            }
            
        except (git.InvalidGitRepositoryError, git.GitCommandError):
            return {
                "repository": None,
                "branch": None,
                "status": None
            }
    
    def _get_git_status_summary(self, repo: git.Repo) -> str:
        """Get a summary of git status."""
        try:
            status = repo.git.status("--porcelain")
            if not status:
                return "clean"
            
            lines = status.strip().split("\n")
            modified = len([l for l in lines if l.startswith(" M")])
            added = len([l for l in lines if l.startswith("A")])
            deleted = len([l for l in lines if l.startswith(" D")])
            untracked = len([l for l in lines if l.startswith("??")])
            
            parts = []
            if modified > 0:
                parts.append(f"{modified} modified")
            if added > 0:
                parts.append(f"{added} added")
            if deleted > 0:
                parts.append(f"{deleted} deleted")
            if untracked > 0:
                parts.append(f"{untracked} untracked")
                
            return ", ".join(parts) if parts else "clean"
            
        except git.GitCommandError:
            return "unknown"
    
    def _get_relevant_env_vars(self) -> Dict[str, str]:
        """Get relevant environment variables."""
        relevant_vars = [
            "PATH", "HOME", "USER", "PWD", "SHELL",
            "EDITOR", "LANG", "TERM", "VIRTUAL_ENV",
            "NODE_ENV", "PYTHON_PATH", "JAVA_HOME"
        ]
        
        return {
            var: os.environ.get(var, "")
            for var in relevant_vars
            if os.environ.get(var)
        }
    
    def _detect_available_tools(self) -> List[str]:
        """Detect available command-line tools."""
        common_tools = [
            # Basic tools
            "ls", "cd", "mkdir", "rm", "cp", "mv", "find", "grep",
            # Git
            "git",
            # Package managers
            "npm", "yarn", "pip", "pip3", "brew", "apt", "yum", "dnf",
            # Editors
            "vim", "nano", "emacs", "code",
            # Development tools
            "node", "python", "python3", "java", "gcc", "make",
            # System tools
            "ps", "top", "htop", "kill", "curl", "wget", "ssh", "scp",
            # Docker/containers
            "docker", "docker-compose", "kubectl",
        ]
        
        available = []
        for tool in common_tools:
            if shutil.which(tool):
                available.append(tool)
                
        return available
    
    def _get_recent_commands(self) -> List[str]:
        """Get recent commands from shell history."""
        try:
            shell = self._detect_shell()
            history_file = None
            
            if shell == "bash":
                history_file = os.path.expanduser("~/.bash_history")
            elif shell == "zsh":
                history_file = os.path.expanduser("~/.zsh_history")
            elif shell == "fish":
                history_file = os.path.expanduser("~/.local/share/fish/fish_history")
            
            if history_file and os.path.exists(history_file):
                with open(history_file, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    # Get last 10 commands
                    recent = [line.strip() for line in lines[-10:] if line.strip()]
                    return recent
                    
        except Exception:
            pass
            
        return []
    
    async def get_directory_context(self, path: str = None) -> Dict[str, Any]:
        """Get context specific to a directory."""
        target_path = path or os.getcwd()
        
        try:
            path_obj = Path(target_path)
            
            # Basic directory info
            files = list(path_obj.iterdir()) if path_obj.exists() else []
            file_count = len([f for f in files if f.is_file()])
            dir_count = len([f for f in files if f.is_dir()])
            
            # Look for special files
            special_files = []
            for special in ["package.json", "requirements.txt", "Dockerfile", "Makefile", "README.md"]:
                if (path_obj / special).exists():
                    special_files.append(special)
            
            return {
                "path": str(path_obj.absolute()),
                "exists": path_obj.exists(),
                "is_directory": path_obj.is_dir(),
                "file_count": file_count,
                "directory_count": dir_count,
                "special_files": special_files,
                "total_size": self._get_directory_size(path_obj) if path_obj.exists() else 0
            }
            
        except Exception as e:
            return {
                "path": target_path,
                "error": str(e)
            }
    
    def _get_directory_size(self, path: Path) -> int:
        """Get total size of directory in bytes."""
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
            return total_size
        except Exception:
            return 0
    
    async def get_process_context(self) -> Dict[str, Any]:
        """Get information about running processes."""
        try:
            # Get basic system info
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Get running processes (limit to user processes)
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    if proc_info['cpu_percent'] > 0 or proc_info['memory_percent'] > 1:
                        processes.append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'cpu': proc_info['cpu_percent'],
                            'memory': proc_info['memory_percent']
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu'], reverse=True)
            
            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "available_memory_gb": memory.available / (1024**3),
                "top_processes": processes[:10]  # Top 10 processes
            }
            
        except Exception as e:
            return {"error": str(e)}