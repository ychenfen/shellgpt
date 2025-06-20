"""Natural Language Processing Engine for command interpretation."""

import json
import re
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

import openai
from openai import OpenAI

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.command import Command, CommandType, SafetyLevel
from utils.patterns import COMMAND_PATTERNS
from config.settings import get_settings


@dataclass
class ParsedIntent:
    """Parsed user intent from natural language."""
    action: str
    target: Optional[str]
    parameters: Dict[str, Any]
    context_needed: List[str]


class NLPEngine:
    """AI-powered natural language processing engine."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the NLP engine with OpenAI client."""
        self.settings = get_settings()
        self.client = OpenAI(api_key=api_key or self.settings.openai_api_key)
        self.model = self.settings.openai_model
        
    async def parse_query(self, query: str, context: Dict[str, Any] = None) -> ParsedIntent:
        """Parse natural language query into structured intent."""
        
        # First, try pattern matching for common queries
        pattern_result = self._try_pattern_matching(query)
        if pattern_result:
            return pattern_result
            
        # Use AI for complex queries
        return await self._ai_parse_query(query, context or {})
    
    def _try_pattern_matching(self, query: str) -> Optional[ParsedIntent]:
        """Try to match query against known patterns."""
        query_lower = query.lower().strip()
        
        for pattern_data in COMMAND_PATTERNS:
            for pattern in pattern_data["patterns"]:
                if re.search(pattern, query_lower):
                    return ParsedIntent(
                        action=pattern_data["action"],
                        target=self._extract_target(query_lower, pattern),
                        parameters=pattern_data.get("default_params", {}),
                        context_needed=pattern_data.get("context_needed", [])
                    )
        return None
    
    def _extract_target(self, query: str, pattern: str) -> Optional[str]:
        """Extract target from query using pattern."""
        # Simple extraction logic - can be enhanced
        words = query.split()
        for i, word in enumerate(words):
            if word in ["file", "directory", "folder", "repo", "branch"]:
                if i + 1 < len(words):
                    return words[i + 1]
        return None
    
    async def _ai_parse_query(self, query: str, context: Dict[str, Any]) -> ParsedIntent:
        """Use AI to parse complex queries."""
        
        system_prompt = """You are an AI assistant that converts natural language into structured command intents.
        
        Parse the user's query and return a JSON object with:
        - action: the main action to perform
        - target: the target of the action (file, directory, etc.)
        - parameters: additional parameters
        - context_needed: list of context information needed
        
        Available actions: list, create, delete, move, copy, search, git_add, git_commit, git_push, git_pull, git_status, install, uninstall, run, kill, find_process, system_info, network_info
        
        Examples:
        "list all python files" -> {"action": "list", "target": "*.py", "parameters": {"type": "files"}, "context_needed": ["current_directory"]}
        "commit changes with message fix bug" -> {"action": "git_commit", "target": null, "parameters": {"message": "fix bug"}, "context_needed": ["git_status"]}
        """
        
        user_prompt = f"""Query: "{query}"
        Current context: {json.dumps(context, indent=2)}
        
        Return only valid JSON."""
        
        try:
            response = await self.client.chat.completions.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            result = json.loads(response.choices[0].message.content)
            return ParsedIntent(
                action=result.get("action", "unknown"),
                target=result.get("target"),
                parameters=result.get("parameters", {}),
                context_needed=result.get("context_needed", [])
            )
            
        except Exception as e:
            # Fallback to basic parsing
            return ParsedIntent(
                action="unknown",
                target=None,
                parameters={"raw_query": query},
                context_needed=["current_directory"]
            )
    
    async def generate_command(
        self, 
        intent: ParsedIntent, 
        context: Dict[str, Any]
    ) -> Command:
        """Generate shell command from parsed intent and context."""
        
        system_prompt = f"""You are an expert system administrator who generates shell commands.
        
        Generate a shell command for the given intent and context.
        Consider the user's operating system: {context.get('operating_system', 'unknown')}
        Current directory: {context.get('current_directory', '.')}
        Shell type: {context.get('shell_type', 'bash')}
        
        Return a JSON object with:
        - shell_command: the exact command to run
        - explanation: clear explanation of what the command does
        - command_type: one of {[t.value for t in CommandType]}
        - safety_level: one of {[s.value for s in SafetyLevel]}
        - confidence: confidence score 0.0-1.0
        - alternatives: list of alternative commands
        - warnings: list of potential warnings
        
        Be precise and consider safety. Mark dangerous commands appropriately.
        """
        
        user_prompt = f"""Intent: {intent}
        Context: {json.dumps(context, indent=2)}
        
        Generate the appropriate shell command."""
        
        try:
            response = await self.client.chat.completions.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=800
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return Command(
                original_query="",  # Will be set by caller
                shell_command=result["shell_command"],
                explanation=result["explanation"],
                command_type=CommandType(result["command_type"]),
                safety_level=SafetyLevel(result["safety_level"]),
                confidence=result["confidence"],
                alternatives=result.get("alternatives", []),
                warnings=result.get("warnings", []),
                context_used=context
            )
            
        except Exception as e:
            # Fallback command
            return Command(
                original_query="",
                shell_command=f"echo 'Error processing query: {str(e)}'",
                explanation="Error occurred during command generation",
                command_type=CommandType.CUSTOM,
                safety_level=SafetyLevel.SAFE,
                confidence=0.0,
                alternatives=[],
                warnings=["Command generation failed"],
                context_used=context
            )