"""Command patterns for quick matching and generation."""

# Common command patterns that can be matched quickly without AI
COMMAND_PATTERNS = [
    # File and Directory Operations
    {
        "action": "list",
        "patterns": [
            r"list.*files?",
            r"show.*files?",
            r"what.*files?.*here",
            r"ls\s",
            r"dir\s",
        ],
        "default_params": {"type": "files"},
        "context_needed": ["current_directory"],
        "templates": {
            "unix": "ls -la {target}",
            "windows": "dir {target}",
        }
    },
    {
        "action": "list_python",
        "patterns": [
            r"list.*python.*files?",
            r"show.*\.py.*files?",
            r"find.*python.*files?",
        ],
        "default_params": {"extension": ".py"},
        "context_needed": ["current_directory"],
        "templates": {
            "unix": "find . -name '*.py' -type f",
            "windows": "dir /s *.py",
        }
    },
    {
        "action": "create_directory", 
        "patterns": [
            r"create.*director(y|ies)",
            r"make.*director(y|ies)",
            r"mkdir\s",
        ],
        "default_params": {},
        "context_needed": ["current_directory"],
        "templates": {
            "unix": "mkdir -p {target}",
            "windows": "mkdir {target}",
        }
    },
    {
        "action": "remove_file",
        "patterns": [
            r"delete.*file",
            r"remove.*file",
            r"rm\s",
        ],
        "default_params": {},
        "context_needed": ["current_directory"],
        "templates": {
            "unix": "rm {target}",
            "windows": "del {target}",
        }
    },
    {
        "action": "copy_file",
        "patterns": [
            r"copy.*file",
            r"cp\s",
        ],
        "default_params": {},
        "context_needed": ["current_directory"],
        "templates": {
            "unix": "cp {source} {target}",
            "windows": "copy {source} {target}",
        }
    },
    {
        "action": "move_file",
        "patterns": [
            r"move.*file",
            r"mv\s",
        ],
        "default_params": {},
        "context_needed": ["current_directory"],
        "templates": {
            "unix": "mv {source} {target}",
            "windows": "move {source} {target}",
        }
    },
    
    # Git Operations
    {
        "action": "git_status",
        "patterns": [
            r"git.*status",
            r"check.*git.*status",
            r"what.*git.*status",
            r"show.*git.*status",
        ],
        "default_params": {},
        "context_needed": ["git_repository"],
        "templates": {
            "unix": "git status",
            "windows": "git status",
        }
    },
    {
        "action": "git_add_all",
        "patterns": [
            r"git.*add.*all",
            r"stage.*all.*changes",
            r"add.*all.*files",
        ],
        "default_params": {},
        "context_needed": ["git_repository"],
        "templates": {
            "unix": "git add .",
            "windows": "git add .",
        }
    },
    {
        "action": "git_commit",
        "patterns": [
            r"git.*commit",
            r"commit.*changes",
            r"make.*commit",
        ],
        "default_params": {},
        "context_needed": ["git_repository", "git_status"],
        "templates": {
            "unix": "git commit -m \"{message}\"",
            "windows": "git commit -m \"{message}\"",
        }
    },
    {
        "action": "git_push",
        "patterns": [
            r"git.*push",
            r"push.*changes",
            r"upload.*changes",
        ],
        "default_params": {},
        "context_needed": ["git_repository", "git_branch"],
        "templates": {
            "unix": "git push origin {branch}",
            "windows": "git push origin {branch}",
        }
    },
    {
        "action": "git_pull",
        "patterns": [
            r"git.*pull",
            r"pull.*changes",
            r"update.*from.*remote",
        ],
        "default_params": {},
        "context_needed": ["git_repository", "git_branch"],
        "templates": {
            "unix": "git pull origin {branch}",
            "windows": "git pull origin {branch}",
        }
    },
    {
        "action": "git_log",
        "patterns": [
            r"git.*log",
            r"show.*git.*history",
            r"git.*history",
        ],
        "default_params": {},
        "context_needed": ["git_repository"],
        "templates": {
            "unix": "git log --oneline -10",
            "windows": "git log --oneline -10",
        }
    },
    
    # System Information
    {
        "action": "system_info",
        "patterns": [
            r"system.*info",
            r"show.*system",
            r"what.*system",
            r"uname",
        ],
        "default_params": {},
        "context_needed": ["operating_system"],
        "templates": {
            "unix": "uname -a",
            "windows": "systeminfo",
        }
    },
    {
        "action": "disk_usage",
        "patterns": [
            r"disk.*usage",
            r"disk.*space",
            r"show.*disk",
            r"df\s",
        ],
        "default_params": {},
        "context_needed": ["operating_system"],
        "templates": {
            "unix": "df -h",
            "windows": "dir",
        }
    },
    {
        "action": "memory_usage",
        "patterns": [
            r"memory.*usage",
            r"show.*memory",
            r"ram.*usage",
            r"free\s",
        ],
        "default_params": {},
        "context_needed": ["operating_system"],
        "templates": {
            "unix": "free -h",
            "windows": "wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /format:table",
        }
    },
    
    # Process Management
    {
        "action": "list_processes",
        "patterns": [
            r"list.*processes",
            r"show.*processes",
            r"ps\s",
            r"running.*processes",
        ],
        "default_params": {},
        "context_needed": ["operating_system"],
        "templates": {
            "unix": "ps aux",
            "windows": "tasklist",
        }
    },
    {
        "action": "kill_process",
        "patterns": [
            r"kill.*process",
            r"stop.*process",
            r"terminate.*process",
        ],
        "default_params": {},
        "context_needed": ["operating_system"],
        "templates": {
            "unix": "kill {pid}",
            "windows": "taskkill /PID {pid}",
        }
    },
    
    # Network Operations
    {
        "action": "ping",
        "patterns": [
            r"ping\s",
            r"test.*connection",
            r"check.*connectivity",
        ],
        "default_params": {},
        "context_needed": [],
        "templates": {
            "unix": "ping -c 4 {target}",
            "windows": "ping {target}",
        }
    },
    {
        "action": "curl_get",
        "patterns": [
            r"curl\s",
            r"download.*from",
            r"fetch.*from",
            r"get.*from.*url",
        ],
        "default_params": {},
        "context_needed": [],
        "templates": {
            "unix": "curl -L {url}",
            "windows": "curl -L {url}",
        }
    },
    
    # Package Management
    {
        "action": "install_package",
        "patterns": [
            r"install.*package",
            r"npm.*install",
            r"pip.*install",
            r"apt.*install",
            r"brew.*install",
        ],
        "default_params": {},
        "context_needed": ["available_tools"],
        "templates": {
            "npm": "npm install {package}",
            "pip": "pip install {package}",
            "apt": "sudo apt install {package}",
            "brew": "brew install {package}",
        }
    },
    {
        "action": "uninstall_package",
        "patterns": [
            r"uninstall.*package",
            r"remove.*package",
            r"npm.*uninstall",
            r"pip.*uninstall",
        ],
        "default_params": {},
        "context_needed": ["available_tools"],
        "templates": {
            "npm": "npm uninstall {package}",
            "pip": "pip uninstall {package}",
            "apt": "sudo apt remove {package}",
            "brew": "brew uninstall {package}",
        }
    },
    
    # Docker Operations
    {
        "action": "docker_list",
        "patterns": [
            r"docker.*list",
            r"list.*containers",
            r"show.*containers",
            r"docker.*ps",
        ],
        "default_params": {},
        "context_needed": ["available_tools"],
        "templates": {
            "unix": "docker ps -a",
            "windows": "docker ps -a",
        }
    },
    {
        "action": "docker_images",
        "patterns": [
            r"docker.*images",
            r"list.*images",
            r"show.*images",
        ],
        "default_params": {},
        "context_needed": ["available_tools"],
        "templates": {
            "unix": "docker images",
            "windows": "docker images",
        }
    },
    
    # Text Processing
    {
        "action": "search_text",
        "patterns": [
            r"search.*for",
            r"find.*text",
            r"grep\s",
            r"look.*for",
        ],
        "default_params": {},
        "context_needed": ["current_directory"],
        "templates": {
            "unix": "grep -r \"{pattern}\" {path}",
            "windows": "findstr /s \"{pattern}\" {path}",
        }
    },
    {
        "action": "count_lines",
        "patterns": [
            r"count.*lines",
            r"how.*many.*lines",
            r"wc.*-l",
        ],
        "default_params": {},
        "context_needed": ["current_directory"],
        "templates": {
            "unix": "wc -l {file}",
            "windows": "find /c /v \"\" {file}",
        }
    },
]


def get_pattern_by_action(action: str) -> dict:
    """Get pattern configuration by action name."""
    for pattern in COMMAND_PATTERNS:
        if pattern["action"] == action:
            return pattern
    return {}


def get_template_for_os(pattern: dict, os_type: str) -> str:
    """Get command template for specific operating system."""
    templates = pattern.get("templates", {})
    
    if os_type.lower() in ["linux", "darwin"]:  # Unix-like
        return templates.get("unix", "")
    elif os_type.lower() == "windows":
        return templates.get("windows", "")
    else:
        # Default to unix template
        return templates.get("unix", templates.get("windows", ""))


def get_all_actions() -> list:
    """Get list of all available actions."""
    return [pattern["action"] for pattern in COMMAND_PATTERNS]