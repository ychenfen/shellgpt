"""Main CLI application for ShellGPT."""

from __future__ import annotations

import asyncio
import sys
import subprocess
from typing import Optional
import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich import print as rprint

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.command_generator import CommandGenerator
from config.settings import get_config_manager, get_settings
from models.command import SafetyLevel

app = typer.Typer(
    name="shellgpt",
    help="🤖 AI-powered intelligent shell assistant",
    no_args_is_help=True,
)
console = Console()


@app.command("ask")
def ask_command(
    query: str = typer.Argument(..., help="Natural language query"),
    execute: bool = typer.Option(False, "--execute", "-e", help="Execute command immediately"),
    explain: bool = typer.Option(False, "--explain", "-x", help="Show detailed explanation"),
    alternatives: bool = typer.Option(False, "--alternatives", "-a", help="Show alternative commands"),
    no_safety: bool = typer.Option(False, "--no-safety", help="Skip safety checks"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Show command without executing"),
):
    """Ask ShellGPT to generate a shell command from natural language."""
    asyncio.run(_ask_command_async(query, execute, explain, alternatives, no_safety, dry_run))


async def _ask_command_async(
    query: str, 
    execute: bool, 
    explain: bool, 
    alternatives: bool, 
    no_safety: bool, 
    dry_run: bool
):
    """Async implementation of ask command."""
    
    settings = get_settings()
    config_manager = get_config_manager()
    
    # Check for API key
    api_key = config_manager.get_api_key()
    if not api_key:
        rprint("[red]❌ OpenAI API key not found![/red]")
        rprint("Set it using: [cyan]shellgpt config --set-api-key[/cyan]")
        return
    
    # Initialize command generator
    generator = CommandGenerator(api_key=api_key)
    
    try:
        with console.status("🤖 Thinking..."):
            if alternatives:
                commands = await generator.generate_multiple_alternatives(query, count=3)
                command = commands[0]  # Primary command
            else:
                command = await generator.generate_command(query)
        
        # Display the result
        _display_command_result(command, explain)
        
        # Show alternatives if requested
        if alternatives and len(commands) > 1:
            _display_alternatives(commands[1:])
        
        # Safety check
        if not no_safety and settings.enable_safety_checks:
            if command.safety_level in [SafetyLevel.DANGEROUS, SafetyLevel.FORBIDDEN]:
                safety_msg = generator.safety_checker.get_safety_recommendation(command)
                rprint(f"\n{safety_msg}")
                
                if command.safety_level == SafetyLevel.FORBIDDEN:
                    rprint("[red]Command execution blocked for safety.[/red]")
                    return
        
        # Execute command if requested
        if execute or (not dry_run and _should_execute(command, no_safety)):
            await _execute_command(command)
    
    except Exception as e:
        rprint(f"[red]❌ Error: {str(e)}[/red]")


def _display_command_result(command, show_explanation: bool = False):
    """Display the generated command in a nice format."""
    
    # Command panel
    syntax = Syntax(command.shell_command, "bash", theme="monokai", line_numbers=False)
    panel = Panel(
        syntax,
        title="🚀 Generated Command",
        border_style="green",
        padding=(1, 2)
    )
    console.print(panel)
    
    # Basic info
    info_table = Table(show_header=False, box=None, padding=(0, 2))
    info_table.add_row("📝 Explanation:", command.explanation)
    info_table.add_row("🔧 Type:", command.command_type.value.replace("_", " ").title())
    info_table.add_row("🛡️  Safety:", _get_safety_emoji(command.safety_level) + " " + command.safety_level.value.title())
    info_table.add_row("🎯 Confidence:", f"{command.confidence:.1%}")
    console.print(info_table)
    
    # Show warnings if any
    if command.warnings:
        rprint("\n⚠️  [yellow]Warnings:[/yellow]")
        for warning in command.warnings:
            rprint(f"  • {warning}")
    
    # Show detailed explanation if requested
    if show_explanation and command.alternatives:
        rprint("\n💡 [cyan]Alternative commands:[/cyan]")
        for i, alt in enumerate(command.alternatives, 1):
            rprint(f"  {i}. [dim]{alt}[/dim]")


def _display_alternatives(alternatives):
    """Display alternative commands."""
    rprint("\n🔄 [cyan]Alternative approaches:[/cyan]")
    
    for i, cmd in enumerate(alternatives, 1):
        rprint(f"\n[dim]{i}.[/dim] {cmd.explanation}")
        syntax = Syntax(cmd.shell_command, "bash", theme="monokai", line_numbers=False)
        console.print("  ", syntax)


def _get_safety_emoji(safety_level: SafetyLevel) -> str:
    """Get emoji for safety level."""
    return {
        SafetyLevel.SAFE: "✅",
        SafetyLevel.CAUTIOUS: "⚠️",
        SafetyLevel.DANGEROUS: "🚨",
        SafetyLevel.FORBIDDEN: "❌"
    }.get(safety_level, "❓")


def _should_execute(command, no_safety: bool) -> bool:
    """Ask user if they want to execute the command."""
    
    if no_safety:
        return Confirm.ask("Execute this command?")
    
    # Check safety level
    if command.safety_level == SafetyLevel.SAFE:
        return Confirm.ask("Execute this command?", default=True)
    elif command.safety_level == SafetyLevel.CAUTIOUS:
        return Confirm.ask("⚠️  This command requires caution. Execute anyway?", default=False)
    elif command.safety_level == SafetyLevel.DANGEROUS:
        return Confirm.ask("🚨 DANGEROUS command detected! Are you absolutely sure?", default=False)
    else:  # FORBIDDEN
        rprint("[red]❌ Command execution blocked for safety.[/red]")
        return False


async def _execute_command(command):
    """Execute the shell command."""
    rprint("\n🚀 [green]Executing command...[/green]")
    
    try:
        # Execute command
        result = subprocess.run(
            command.shell_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60  # 1 minute timeout
        )
        
        # Display output
        if result.stdout:
            rprint("\n📤 [green]Output:[/green]")
            console.print(result.stdout)
        
        if result.stderr:
            rprint("\n❌ [red]Error:[/red]")
            console.print(result.stderr)
        
        # Show return code
        if result.returncode == 0:
            rprint("✅ [green]Command completed successfully[/green]")
        else:
            rprint(f"❌ [red]Command failed with exit code {result.returncode}[/red]")
    
    except subprocess.TimeoutExpired:
        rprint("⏰ [yellow]Command timed out after 60 seconds[/yellow]")
    except Exception as e:
        rprint(f"❌ [red]Execution error: {str(e)}[/red]")


@app.command("explain")
def explain_command(
    command: str = typer.Argument(..., help="Shell command to explain")
):
    """Explain what a shell command does."""
    asyncio.run(_explain_command_async(command))


async def _explain_command_async(command: str):
    """Async implementation of explain command."""
    
    settings = get_settings()
    config_manager = get_config_manager()
    
    api_key = config_manager.get_api_key()
    if not api_key:
        rprint("[red]❌ OpenAI API key not found![/red]")
        return
    
    generator = CommandGenerator(api_key=api_key)
    
    try:
        with console.status("🔍 Analyzing command..."):
            explanation = await generator.explain_command(command)
        
        # Display explanation
        panel = Panel(
            explanation,
            title=f"📖 Explanation: {command}",
            border_style="blue",
            padding=(1, 2)
        )
        console.print(panel)
    
    except Exception as e:
        rprint(f"[red]❌ Error: {str(e)}[/red]")


@app.command("config")
def config_command(
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
    set_api_key: bool = typer.Option(False, "--set-api-key", help="Set OpenAI API key"),
    model: Optional[str] = typer.Option(None, "--model", help="Set OpenAI model"),
    init: bool = typer.Option(False, "--init", help="Initialize default configuration"),
):
    """Manage ShellGPT configuration."""
    
    config_manager = get_config_manager()
    settings = get_settings()
    
    if init:
        config_manager.create_default_config()
        rprint("✅ [green]Default configuration created[/green]")
        return
    
    if set_api_key:
        api_key = Prompt.ask("Enter your OpenAI API key", password=True)
        config_manager.set_api_key(api_key)
        rprint("✅ [green]API key saved securely[/green]")
        return
    
    if model:
        settings.openai_model = model
        config_manager.save_config()
        rprint(f"✅ [green]Model set to: {model}[/green]")
        return
    
    if show:
        # Display current configuration
        config_table = Table(title="🔧 ShellGPT Configuration")
        config_table.add_column("Setting", style="cyan")
        config_table.add_column("Value", style="green")
        
        config_table.add_row("OpenAI Model", settings.openai_model)
        config_table.add_row("Max Tokens", str(settings.openai_max_tokens))
        config_table.add_row("Temperature", str(settings.openai_temperature))
        config_table.add_row("Safety Checks", "✅" if settings.enable_safety_checks else "❌")
        config_table.add_row("Learning", "✅" if settings.enable_learning else "❌")
        config_table.add_row("API Key", "✅ Set" if config_manager.get_api_key() else "❌ Not set")
        config_table.add_row("Config Dir", str(settings.config_dir))
        
        console.print(config_table)
    else:
        rprint("Use [cyan]--show[/cyan] to see current configuration")


@app.command("version")
def version_command():
    """Show ShellGPT version information."""
    __version__ = "1.0.0"
    __description__ = "AI-powered intelligent shell assistant that understands natural language"
    
    version_panel = Panel(
        f"🤖 [bold cyan]ShellGPT[/bold cyan] v{__version__}\n\n{__description__}",
        title="Version Information",
        border_style="blue",
        padding=(1, 2)
    )
    console.print(version_panel)


@app.command("interactive")
def interactive_mode():
    """Start interactive mode for continuous conversation."""
    rprint("🤖 [bold cyan]ShellGPT Interactive Mode[/bold cyan]")
    rprint("Type your queries in natural language. Type 'exit' to quit.\n")
    
    while True:
        try:
            query = Prompt.ask("💬")
            
            if query.lower() in ['exit', 'quit', 'q']:
                rprint("👋 [yellow]Goodbye![/yellow]")
                break
            
            if query.strip():
                asyncio.run(_ask_command_async(
                    query=query,
                    execute=False,
                    explain=False,
                    alternatives=False,
                    no_safety=False,
                    dry_run=False
                ))
                print()  # Empty line for better readability
        
        except KeyboardInterrupt:
            rprint("\n👋 [yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            rprint(f"[red]❌ Error: {str(e)}[/red]")


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()