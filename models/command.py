"""Data models for commands and responses."""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class CommandType(str, Enum):
    """Types of commands that can be generated."""
    FILE_OPERATION = "file_operation"
    GIT_COMMAND = "git_command"
    SYSTEM_INFO = "system_info"
    PROCESS_MANAGEMENT = "process_management"
    NETWORK_OPERATION = "network_operation"
    PACKAGE_MANAGEMENT = "package_management"
    CUSTOM = "custom"


class SafetyLevel(str, Enum):
    """Safety levels for commands."""
    SAFE = "safe"           # Completely safe, no confirmation needed
    CAUTIOUS = "cautious"   # Potentially risky, should confirm
    DANGEROUS = "dangerous" # High risk, require explicit confirmation
    FORBIDDEN = "forbidden" # Never execute


class Command(BaseModel):
    """Represents a shell command with metadata."""
    
    original_query: str = Field(..., description="Original natural language query")
    shell_command: str = Field(..., description="Generated shell command")
    explanation: str = Field(..., description="Human-readable explanation")
    command_type: CommandType = Field(..., description="Type of command")
    safety_level: SafetyLevel = Field(..., description="Safety assessment")
    confidence: float = Field(..., ge=0.0, le=1.0, description="AI confidence score")
    alternatives: List[str] = Field(default_factory=list, description="Alternative commands")
    warnings: List[str] = Field(default_factory=list, description="Potential warnings")
    context_used: Dict[str, Any] = Field(default_factory=dict, description="Context information used")
    timestamp: datetime = Field(default_factory=datetime.now)


class ExecutionResult(BaseModel):
    """Result of command execution."""
    
    command: Command
    executed: bool = Field(..., description="Whether command was executed")
    return_code: Optional[int] = Field(None, description="Command return code")
    stdout: Optional[str] = Field(None, description="Standard output")
    stderr: Optional[str] = Field(None, description="Standard error")
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now)


class UserPreference(BaseModel):
    """User preferences and learned patterns."""
    
    user_id: str = Field(..., description="User identifier")
    preferred_tools: Dict[str, str] = Field(default_factory=dict, description="Preferred tools for tasks")
    command_aliases: Dict[str, str] = Field(default_factory=dict, description="Custom aliases")
    safety_preferences: Dict[SafetyLevel, bool] = Field(
        default_factory=lambda: {
            SafetyLevel.SAFE: True,
            SafetyLevel.CAUTIOUS: True,
            SafetyLevel.DANGEROUS: False,
            SafetyLevel.FORBIDDEN: False,
        },
        description="Safety level preferences"
    )
    frequently_used_patterns: List[str] = Field(default_factory=list, description="Common command patterns")
    context_preferences: Dict[str, Any] = Field(default_factory=dict, description="Context-specific preferences")
    last_updated: datetime = Field(default_factory=datetime.now)


class SystemContext(BaseModel):
    """Current system context information."""
    
    current_directory: str = Field(..., description="Current working directory")
    operating_system: str = Field(..., description="Operating system")
    shell_type: str = Field(..., description="Type of shell (bash, zsh, etc.)")
    git_repository: Optional[str] = Field(None, description="Current git repository")
    git_branch: Optional[str] = Field(None, description="Current git branch")
    git_status: Optional[str] = Field(None, description="Git status summary")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Relevant env vars")
    available_tools: List[str] = Field(default_factory=list, description="Available command-line tools")
    recent_commands: List[str] = Field(default_factory=list, description="Recently executed commands")
    timestamp: datetime = Field(default_factory=datetime.now)