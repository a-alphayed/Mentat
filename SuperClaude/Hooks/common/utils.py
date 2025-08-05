"""
General utilities for SuperClaude hooks system.

Provides helper functions for common operations like:
- File operations and path handling
- JSON parsing and validation
- String manipulation and pattern matching
- System information and environment detection
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import os
import platform
import subprocess


def safe_json_load(file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
    """
    Safely load JSON file with error handling.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON data or None if failed
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
        return None


def safe_json_save(data: Dict[str, Any], file_path: Union[str, Path]) -> bool:
    """
    Safely save data to JSON file.
    
    Args:
        data: Data to save
        file_path: Target file path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        return False


def extract_yaml_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """
    Extract YAML frontmatter from markdown content.
    
    Args:
        content: Markdown content with potential YAML frontmatter
        
    Returns:
        Parsed YAML data or None if not found
    """
    # Look for YAML frontmatter pattern: ---\n...yaml...\n---
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return None
        
    yaml_content = match.group(1)
    
    # Simple YAML parsing for common patterns
    # Note: This is a simplified parser for SuperClaude's specific YAML format
    result = {}
    
    for line in yaml_content.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Handle different value types
            if value.lower() in ['true', 'false']:
                result[key] = value.lower() == 'true'
            elif value.isdigit():
                result[key] = int(value)
            elif value.replace('.', '').isdigit():
                result[key] = float(value)
            elif value.startswith('[') and value.endswith(']'):
                # Simple list parsing
                list_content = value[1:-1]
                if list_content:
                    result[key] = [item.strip().strip('"\'') for item in list_content.split(',')]
                else:
                    result[key] = []
            else:
                # String value, remove quotes if present
                result[key] = value.strip('"\'')
    
    return result


def find_superclaude_root() -> Optional[Path]:
    """
    Find SuperClaude framework root directory.
    
    Returns:
        Path to SuperClaude root or None if not found
    """
    # Start from current file location and work up
    current_path = Path(__file__).parent
    while current_path != current_path.parent:
        # Look for SuperClaude directory
        superclaude_path = current_path / "SuperClaude"
        if superclaude_path.exists() and (superclaude_path / "Core").exists():
            return superclaude_path
        current_path = current_path.parent
    
    # Check common installation locations
    possible_paths = [
        Path.home() / ".claude" / "SuperClaude",
        Path("/usr/local/share/SuperClaude"),
        Path.cwd() / "SuperClaude"
    ]
    
    for path in possible_paths:
        if path.exists() and (path / "Core").exists():
            return path
    
    return None


def get_system_info() -> Dict[str, Any]:
    """
    Get system information for context.
    
    Returns:
        Dictionary with system information
    """
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": platform.python_version(),
        "architecture": platform.machine(),
        "node": platform.node()
    }


def is_git_repository(path: Union[str, Path]) -> bool:
    """
    Check if path is within a git repository.
    
    Args:
        path: Path to check
        
    Returns:
        True if in git repository, False otherwise
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            cwd=str(path),
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except Exception:
        return False


def count_files_in_directory(path: Union[str, Path], pattern: str = "*") -> int:
    """
    Count files matching pattern in directory.
    
    Args:
        path: Directory path
        pattern: Glob pattern for file matching
        
    Returns:
        Number of matching files
    """
    try:
        path = Path(path)
        if not path.is_dir():
            return 0
        return len(list(path.glob(pattern)))
    except Exception:
        return 0


def detect_project_type(path: Union[str, Path]) -> List[str]:
    """
    Detect project type based on files present.
    
    Args:
        path: Project directory path
        
    Returns:
        List of detected project types
    """
    path = Path(path)
    project_types = []
    
    # Check for common project files
    indicators = {
        "python": ["pyproject.toml", "setup.py", "requirements.txt", "Pipfile"],
        "node": ["package.json", "yarn.lock", "npm-shrinkwrap.json"],
        "rust": ["Cargo.toml", "Cargo.lock"],
        "go": ["go.mod", "go.sum"],
        "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
        "docker": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
        "git": [".git"],
        "vscode": [".vscode"],
        "superclaude": ["SuperClaude", ".superclaude"]
    }
    
    for project_type, files in indicators.items():
        for file in files:
            if (path / file).exists():
                project_types.append(project_type)
                break
    
    return project_types


def parse_tool_args(args_str: str) -> Dict[str, Any]:
    """
    Parse tool arguments from string format.
    
    Args:
        args_str: String representation of tool arguments
        
    Returns:
        Parsed arguments dictionary
    """
    if not args_str:
        return {}
        
    try:
        # Try JSON parsing first
        return json.loads(args_str)
    except json.JSONDecodeError:
        # Fall back to simple key=value parsing
        result = {}
        for pair in args_str.split():
            if '=' in pair:
                key, value = pair.split('=', 1)
                result[key] = value
        return result


def format_execution_time(ms: float) -> str:
    """
    Format execution time for human reading.
    
    Args:
        ms: Time in milliseconds
        
    Returns:
        Formatted time string
    """
    if ms < 1:
        return f"{ms:.2f}ms"
    elif ms < 1000:
        return f"{ms:.0f}ms"
    else:
        return f"{ms/1000:.1f}s"


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate string to max length with suffix.
    
    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to add when truncating
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_file_paths_from_args(args: Dict[str, Any]) -> List[str]:
    """
    Extract file paths from tool arguments.
    
    Args:
        args: Tool arguments dictionary
        
    Returns:
        List of file paths found in arguments
    """
    file_paths = []
    
    # Common argument names that contain file paths
    path_keys = ['file_path', 'path', 'relative_path', 'notebook_path', 'source', 'destination']
    
    for key in path_keys:
        if key in args and isinstance(args[key], str):
            file_paths.append(args[key])
    
    # Check for paths in lists
    for value in args.values():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str) and ('/' in item or '\\' in item):
                    file_paths.append(item)
                    
    return file_paths