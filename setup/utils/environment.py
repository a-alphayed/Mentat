"""
Environment variable management for SuperClaude
Cross-platform utilities for setting up persistent environment variables
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, Optional
from .ui import display_info, display_success, display_warning, Colors
from .logger import get_logger


def detect_shell_config() -> Optional[Path]:
    """
    Detect user's shell configuration file
    
    Returns:
        Path to the shell configuration file, or None if not found
    """
    home = Path.home()
    
    # Check in order of preference
    configs = [
        home / ".zshrc",        # Zsh (Mac default)
        home / ".bashrc",       # Bash
        home / ".profile",      # Generic shell profile
        home / ".bash_profile"  # Mac Bash profile
    ]
    
    for config in configs:
        if config.exists():
            return config
    
    # Default to .bashrc if none exist (will be created)
    return home / ".bashrc"


def setup_environment_variables(api_keys: Dict[str, str]) -> bool:
    """
    Set up environment variables across platforms
    
    Args:
        api_keys: Dictionary of environment variable names to values
        
    Returns:
        True if all variables were set successfully, False otherwise
    """
    logger = get_logger()
    success = True
    
    if not api_keys:
        return True
    
    print(f"\n{Colors.BLUE}[INFO] Setting up environment variables...{Colors.RESET}")
    
    for env_var, value in api_keys.items():
        try:
            # Set for current session
            os.environ[env_var] = value
            
            if os.name == 'nt':  # Windows
                # Use setx for persistent user variable
                result = subprocess.run(
                    ['setx', env_var, value],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    display_warning(f"Could not set {env_var} persistently: {result.stderr.strip()}")
                    success = False
                else:
                    logger.info(f"Windows environment variable {env_var} set persistently")
            else:  # Unix-like systems
                shell_config = detect_shell_config()
                
                # Check if the export already exists
                export_line = f'export {env_var}="{value}"'
                
                try:
                    with open(shell_config, 'r') as f:
                        content = f.read()
                    
                    # Check if this environment variable is already set
                    if f'export {env_var}=' in content:
                        # Variable exists - don't duplicate
                        logger.info(f"Environment variable {env_var} already exists in {shell_config.name}")
                    else:
                        # Append export to shell config
                        with open(shell_config, 'a') as f:
                            f.write(f'\n# SuperClaude API Key\n{export_line}\n')
                        
                        display_info(f"Added {env_var} to {shell_config.name}")
                        logger.info(f"Added {env_var} to {shell_config}")
                        
                except Exception as e:
                    display_warning(f"Could not update {shell_config.name}: {e}")
                    success = False
            
            logger.info(f"Environment variable {env_var} configured for current session")
            
        except Exception as e:
            logger.error(f"Failed to set {env_var}: {e}")
            display_warning(f"Failed to set {env_var}: {e}")
            success = False
    
    if success:
        display_success("Environment variables configured successfully")
        if os.name != 'nt':
            display_info("Restart your terminal or run 'source ~/.bashrc' to apply changes")
        else:
            display_info("New environment variables will be available in new terminal sessions")
    else:
        display_warning("Some environment variables could not be set persistently")
        display_info("You can set them manually or check the logs for details")
    
    return success


def validate_environment_setup(env_vars: Dict[str, str]) -> bool:
    """
    Validate that environment variables are properly set
    
    Args:
        env_vars: Dictionary of environment variable names to expected values
        
    Returns:
        True if all variables are set correctly, False otherwise
    """
    logger = get_logger()
    all_valid = True
    
    for env_var, expected_value in env_vars.items():
        current_value = os.environ.get(env_var)
        
        if current_value is None:
            logger.warning(f"Environment variable {env_var} is not set")
            all_valid = False
        elif current_value != expected_value:
            logger.warning(f"Environment variable {env_var} has unexpected value")
            all_valid = False
        else:
            logger.info(f"Environment variable {env_var} is set correctly")
    
    return all_valid


def get_shell_name() -> str:
    """
    Get the name of the current shell
    
    Returns:
        Name of the shell (e.g., 'bash', 'zsh', 'fish')
    """
    shell_path = os.environ.get('SHELL', '')
    if shell_path:
        return Path(shell_path).name
    return 'unknown'


def create_env_file(api_keys: Dict[str, str], env_file_path: Optional[Path] = None) -> bool:
    """
    Create a .env file with the API keys (alternative to shell config)
    
    Args:
        api_keys: Dictionary of environment variable names to values
        env_file_path: Path to the .env file (defaults to home directory)
        
    Returns:
        True if .env file was created successfully, False otherwise
    """
    if env_file_path is None:
        env_file_path = Path.home() / ".env"
    
    logger = get_logger()
    
    try:
        # Read existing .env file if it exists
        existing_content = ""
        if env_file_path.exists():
            with open(env_file_path, 'r') as f:
                existing_content = f.read()
        
        # Prepare new content
        new_lines = []
        for env_var, value in api_keys.items():
            line = f'{env_var}="{value}"'
            
            # Check if this variable already exists
            if f'{env_var}=' in existing_content:
                logger.info(f"Variable {env_var} already exists in .env file")
            else:
                new_lines.append(line)
        
        # Append new lines if any
        if new_lines:
            with open(env_file_path, 'a') as f:
                if existing_content and not existing_content.endswith('\n'):
                    f.write('\n')
                f.write('# SuperClaude API Keys\n')
                for line in new_lines:
                    f.write(line + '\n')
            
            # Set file permissions (readable only by owner)
            env_file_path.chmod(0o600)
            
            display_success(f"Created .env file at {env_file_path}")
            logger.info(f"Created .env file with {len(new_lines)} new variables")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to create .env file: {e}")
        display_warning(f"Could not create .env file: {e}")
        return False