"""Command generation engine that orchestrates all components."""

from typing import Dict, Any, Optional
from ..models.command import Command, CommandType, SafetyLevel
from ..utils.patterns import get_pattern_by_action, get_template_for_os
from .nlp_engine import NLPEngine
from .context_manager import ContextManager
from .safety_checker import SafetyChecker


class CommandGenerator:
    """Main command generation engine."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize command generator with all components."""
        self.nlp_engine = NLPEngine(api_key=api_key)
        self.context_manager = ContextManager()
        self.safety_checker = SafetyChecker()
    
    async def generate_command(self, query: str, use_context: bool = True) -> Command:
        """Generate a command from natural language query."""
        
        # Get system context if requested
        context = {}
        if use_context:
            system_context = await self.context_manager.get_current_context()
            context = {
                "current_directory": system_context.current_directory,
                "operating_system": system_context.operating_system,
                "shell_type": system_context.shell_type,
                "git_repository": system_context.git_repository,
                "git_branch": system_context.git_branch,
                "git_status": system_context.git_status,
                "available_tools": system_context.available_tools,
            }
        
        # Parse the natural language query
        intent = await self.nlp_engine.parse_query(query, context)
        
        # Try pattern-based generation first (faster)
        command = self._try_pattern_based_generation(intent, context, query)
        
        if not command:
            # Fall back to AI-based generation
            command = await self.nlp_engine.generate_command(intent, context)
            command.original_query = query
        
        # Safety check
        command = self.safety_checker.check_command_safety(command)
        
        return command
    
    def _try_pattern_based_generation(
        self, 
        intent, 
        context: Dict[str, Any], 
        query: str
    ) -> Optional[Command]:
        """Try to generate command using pattern matching."""
        
        pattern_config = get_pattern_by_action(intent.action)
        if not pattern_config:
            return None
        
        # Get appropriate template for OS
        os_type = context.get("operating_system", "Linux")
        template = get_template_for_os(pattern_config, os_type)
        
        if not template:
            return None
        
        # Fill in template parameters
        try:
            shell_command = self._fill_template(template, intent, context)
            
            # Determine command type based on action
            command_type = self._determine_command_type(intent.action)
            
            # Create command object
            command = Command(
                original_query=query,
                shell_command=shell_command,
                explanation=self._generate_explanation(intent, shell_command),
                command_type=command_type,
                safety_level=SafetyLevel.SAFE,  # Will be updated by safety checker
                confidence=0.9,  # High confidence for pattern matches
                alternatives=[],
                warnings=[],
                context_used=context
            )
            
            return command
            
        except Exception:
            # If template filling fails, return None to fall back to AI
            return None
    
    def _fill_template(self, template: str, intent, context: Dict[str, Any]) -> str:
        """Fill template with appropriate values."""
        
        # Default substitutions
        substitutions = {
            "target": intent.target or ".",
            "source": intent.parameters.get("source", ""),
            "message": intent.parameters.get("message", "Update"),
            "branch": context.get("git_branch", "main"),
            "package": intent.target or "",
            "pattern": intent.target or "",
            "file": intent.target or "",
            "path": intent.target or ".",
            "url": intent.target or "",
            "pid": intent.target or "",
        }
        
        # Try to substitute all placeholders
        result = template
        for key, value in substitutions.items():
            placeholder = "{" + key + "}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        
        return result
    
    def _determine_command_type(self, action: str) -> CommandType:
        """Determine command type based on action."""
        
        if action.startswith("git_"):
            return CommandType.GIT_COMMAND
        elif action in ["list", "create_directory", "remove_file", "copy_file", "move_file"]:
            return CommandType.FILE_OPERATION
        elif action in ["system_info", "disk_usage", "memory_usage"]:
            return CommandType.SYSTEM_INFO
        elif action in ["list_processes", "kill_process"]:
            return CommandType.PROCESS_MANAGEMENT
        elif action in ["ping", "curl_get"]:
            return CommandType.NETWORK_OPERATION
        elif action in ["install_package", "uninstall_package"]:
            return CommandType.PACKAGE_MANAGEMENT
        else:
            return CommandType.CUSTOM
    
    def _generate_explanation(self, intent, command: str) -> str:
        """Generate human-readable explanation for the command."""
        
        action_explanations = {
            "list": f"List files and directories",
            "list_python": "Find all Python files in the current directory and subdirectories",
            "create_directory": f"Create a new directory",
            "remove_file": f"Delete a file",
            "copy_file": f"Copy a file to another location",
            "move_file": f"Move or rename a file",
            "git_status": "Show the current status of the Git repository",
            "git_add_all": "Stage all changes for the next commit",
            "git_commit": "Create a new commit with staged changes",
            "git_push": "Upload local commits to the remote repository",
            "git_pull": "Download and merge changes from the remote repository",
            "git_log": "Show recent commit history",
            "system_info": "Display system information",
            "disk_usage": "Show disk space usage",
            "memory_usage": "Display memory usage information",
            "list_processes": "List all running processes",
            "kill_process": "Terminate a running process",
            "ping": "Test network connectivity to a host",
            "curl_get": "Download or fetch content from a URL",
            "install_package": "Install a software package",
            "uninstall_package": "Remove a software package",
            "search_text": "Search for text patterns in files",
            "count_lines": "Count the number of lines in a file",
        }
        
        base_explanation = action_explanations.get(intent.action, f"Execute {intent.action}")
        
        if intent.target:
            return f"{base_explanation}: {intent.target}"
        else:
            return base_explanation
    
    async def generate_multiple_alternatives(self, query: str, count: int = 3) -> list[Command]:
        """Generate multiple alternative commands for the same query."""
        
        alternatives = []
        
        # Generate primary command
        primary = await self.generate_command(query)
        alternatives.append(primary)
        
        # Generate variations by tweaking the prompt
        variations = [
            f"Alternative way to: {query}",
            f"Another method to: {query}",
            f"Different approach for: {query}",
        ]
        
        for i, variation in enumerate(variations[:count-1]):
            try:
                alt_command = await self.generate_command(variation)
                # Make sure it's actually different
                if alt_command.shell_command != primary.shell_command:
                    alternatives.append(alt_command)
                if len(alternatives) >= count:
                    break
            except Exception:
                continue
        
        return alternatives
    
    async def explain_command(self, command: str) -> str:
        """Explain what an existing command does."""
        
        context = await self.context_manager.get_current_context()
        
        system_prompt = """You are an expert system administrator. Explain what the given shell command does in clear, simple terms.
        
        Provide:
        1. What the command does
        2. What each part/flag means
        3. Potential risks or side effects
        4. Expected output or result
        
        Keep it concise but informative."""
        
        user_prompt = f"""Explain this command: {command}
        
        Operating System: {context.operating_system}
        Current Directory: {context.current_directory}"""
        
        try:
            response = await self.nlp_engine.client.chat.completions.acreate(
                model=self.nlp_engine.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Unable to explain command: {str(e)}"
    
    async def suggest_improvements(self, command: str) -> list[str]:
        """Suggest improvements or alternatives for a command."""
        
        context = await self.context_manager.get_current_context()
        
        system_prompt = """You are an expert system administrator. Analyze the given command and suggest improvements.
        
        Consider:
        1. More efficient alternatives
        2. Safer options
        3. Better practices
        4. Additional useful flags
        
        Return suggestions as a list of strings, each describing one improvement."""
        
        user_prompt = f"""Improve this command: {command}
        
        Context:
        - OS: {context.operating_system}
        - Shell: {context.shell_type}
        - Directory: {context.current_directory}"""
        
        try:
            response = await self.nlp_engine.client.chat.completions.acreate(
                model=self.nlp_engine.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=600
            )
            
            # Parse response into list
            suggestions = response.choices[0].message.content.strip().split('\n')
            return [s.strip('- ').strip() for s in suggestions if s.strip()]
            
        except Exception:
            return ["Unable to generate suggestions"]