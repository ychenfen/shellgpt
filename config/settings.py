"""Configuration management for ShellGPT."""

import os
from typing import Optional, Dict, Any
from pathlib import Path
import yaml
from pydantic import BaseSettings, Field
from platformdirs import user_config_dir, user_data_dir


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Configuration
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-3.5-turbo", env="SHELLGPT_MODEL")
    openai_max_tokens: int = Field(1000, env="SHELLGPT_MAX_TOKENS")
    openai_temperature: float = Field(0.1, env="SHELLGPT_TEMPERATURE")
    
    # Application Configuration
    app_name: str = Field("shellgpt", env="SHELLGPT_APP_NAME")
    debug: bool = Field(False, env="SHELLGPT_DEBUG")
    log_level: str = Field("INFO", env="SHELLGPT_LOG_LEVEL")
    
    # Safety Configuration
    require_confirmation: bool = Field(True, env="SHELLGPT_REQUIRE_CONFIRMATION")
    enable_safety_checks: bool = Field(True, env="SHELLGPT_ENABLE_SAFETY")
    max_command_length: int = Field(1000, env="SHELLGPT_MAX_COMMAND_LENGTH")
    
    # Learning Configuration
    enable_learning: bool = Field(True, env="SHELLGPT_ENABLE_LEARNING")
    max_history_size: int = Field(1000, env="SHELLGPT_MAX_HISTORY")
    
    # Directory Configuration
    config_dir: Path = Field(default_factory=lambda: Path(user_config_dir("shellgpt")))
    data_dir: Path = Field(default_factory=lambda: Path(user_data_dir("shellgpt")))
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class ConfigManager:
    """Manages configuration loading and saving."""
    
    def __init__(self):
        self.settings = Settings()
        self.config_file = self.settings.config_dir / "config.yaml"
        self.user_preferences_file = self.settings.data_dir / "preferences.yaml"
        
        # Ensure directories exist
        self.settings.config_dir.mkdir(parents=True, exist_ok=True)
        self.settings.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Load user configuration if it exists
        self._load_user_config()
    
    def _load_user_config(self) -> None:
        """Load user configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config_data = yaml.safe_load(f)
                    
                # Update settings with loaded config
                for key, value in config_data.items():
                    if hasattr(self.settings, key):
                        setattr(self.settings, key, value)
                        
            except Exception as e:
                print(f"Warning: Failed to load config file: {e}")
    
    def save_config(self) -> None:
        """Save current configuration to file."""
        config_data = {
            "openai_model": self.settings.openai_model,
            "openai_max_tokens": self.settings.openai_max_tokens,
            "openai_temperature": self.settings.openai_temperature,
            "require_confirmation": self.settings.require_confirmation,
            "enable_safety_checks": self.settings.enable_safety_checks,
            "enable_learning": self.settings.enable_learning,
            "debug": self.settings.debug,
            "log_level": self.settings.log_level,
        }
        
        try:
            with open(self.config_file, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False)
        except Exception as e:
            print(f"Warning: Failed to save config file: {e}")
    
    def load_user_preferences(self) -> Dict[str, Any]:
        """Load user preferences and learned patterns."""
        if self.user_preferences_file.exists():
            try:
                with open(self.user_preferences_file, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                pass
        return {}
    
    def save_user_preferences(self, preferences: Dict[str, Any]) -> None:
        """Save user preferences and learned patterns."""
        try:
            with open(self.user_preferences_file, 'w') as f:
                yaml.dump(preferences, f, default_flow_style=False)
        except Exception as e:
            print(f"Warning: Failed to save preferences: {e}")
    
    def get_api_key(self) -> Optional[str]:
        """Get OpenAI API key from various sources."""
        # Check environment variable first
        if self.settings.openai_api_key:
            return self.settings.openai_api_key
        
        # Check config file
        api_key_file = self.settings.config_dir / "api_key"
        if api_key_file.exists():
            try:
                return api_key_file.read_text().strip()
            except Exception:
                pass
        
        return None
    
    def set_api_key(self, api_key: str) -> None:
        """Save API key securely."""
        api_key_file = self.settings.config_dir / "api_key"
        try:
            api_key_file.write_text(api_key)
            api_key_file.chmod(0o600)  # Restrict permissions
            self.settings.openai_api_key = api_key
        except Exception as e:
            print(f"Warning: Failed to save API key: {e}")
    
    def create_default_config(self) -> None:
        """Create default configuration file."""
        default_config = {
            "# OpenAI Configuration": None,
            "openai_model": "gpt-3.5-turbo",
            "openai_max_tokens": 1000,
            "openai_temperature": 0.1,
            "": None,  # Empty line
            "# Safety Configuration": None,
            "require_confirmation": True,
            "enable_safety_checks": True,
            "max_command_length": 1000,
            " ": None,  # Another empty line
            "# Learning Configuration": None,
            "enable_learning": True,
            "max_history_size": 1000,
            "  ": None,  # Another empty line
            "# Application Configuration": None,
            "debug": False,
            "log_level": "INFO",
        }
        
        # Create a properly formatted YAML
        yaml_content = """# ShellGPT Configuration File
# Edit this file to customize your ShellGPT experience

# OpenAI Configuration
openai_model: "gpt-3.5-turbo"
openai_max_tokens: 1000
openai_temperature: 0.1

# Safety Configuration
require_confirmation: true
enable_safety_checks: true
max_command_length: 1000

# Learning Configuration
enable_learning: true
max_history_size: 1000

# Application Configuration  
debug: false
log_level: "INFO"
"""
        
        try:
            with open(self.config_file, 'w') as f:
                f.write(yaml_content)
            print(f"Created default configuration at: {self.config_file}")
        except Exception as e:
            print(f"Warning: Failed to create default config: {e}")


# Global configuration instance
_config_manager = None

def get_settings() -> Settings:
    """Get global settings instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager.settings

def get_config_manager() -> ConfigManager:
    """Get global config manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager