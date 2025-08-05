"""
Base Hook Class for SuperClaude Hooks System

Provides common functionality for all hook implementations including:
- Performance monitoring with <100ms target
- Error handling and logging with graceful degradation
- Claude Code CLI integration helpers
- Configuration parsing utilities
- Framework compliance validation
"""

import json
import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import sys
import os

# Setup logging for hooks - configured later based on verbosity
# Default minimal configuration - ONLY to file, never to stdout
log_file = os.path.expanduser('~/.claude/superclaude-hooks.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file)
    ],
    force=True  # Override any existing configuration
)

class BaseHook(ABC):
    """
    Base class for all SuperClaude hooks.
    
    Provides common functionality:
    - Performance monitoring (<100ms target)
    - Error handling with graceful degradation
    - Configuration parsing
    - Framework compliance validation
    """
    
    def __init__(self, hook_name: str, config_path: Optional[str] = None, input_data: Optional[Dict[str, Any]] = None):
        """
        Initialize base hook.
        
        Args:
            hook_name: Name of the hook for logging and identification
            config_path: Optional path to hook configuration file
            input_data: Optional pre-loaded input data (to avoid stdin double-read)
        """
        self.hook_name = hook_name
        self.start_time = None
        self.config = self._load_config(config_path)
        self.performance_target_ms = 100  # <100ms execution target
        
        # Configure logging based on verbosity
        self._configure_logging()
        
        # Create logger after configuring logging
        self.logger = logging.getLogger(f"SuperClaude.Hooks.{hook_name}")
        
        # Track hook metrics
        self.metrics = {
            "executions": 0,
            "successes": 0,
            "failures": 0,
            "avg_execution_time_ms": 0,
            "total_execution_time_ms": 0
        }
        
        # Only log initialization in verbose mode
        if self.get_verbosity() in ['verbose', 'debug']:
            self.logger.info(f"Initialized {hook_name} hook")
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load hook configuration from SuperClaude config file or defaults."""
        config = {}
        
        # Try to load from provided path or look for superclaude-config.json
        if config_path and Path(config_path).exists():
            config_file = Path(config_path)
        else:
            # Look for superclaude-config.json in various locations
            claude_home = os.environ.get('CLAUDE_HOME', os.path.expanduser('~/.claude'))
            project_dir = os.environ.get('CLAUDE_PROJECT_DIR')
            
            # Try project-specific config first
            if project_dir:
                project_config = Path(project_dir) / '.claude' / 'superclaude-config.json'
                if project_config.exists():
                    config_file = project_config
                else:
                    config_file = Path(claude_home) / 'superclaude-config.json'
            else:
                config_file = Path(claude_home) / 'superclaude-config.json'
        
        # Load the config file if it exists
        if 'config_file' in locals() and config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    full_config = json.load(f)
                    # Extract SuperClaude config
                    if 'superclaude' in full_config:
                        config = full_config['superclaude']
            except Exception as e:
                self.logger.warning(f"Failed to load config from {config_file}: {e}")
        
        # Merge with defaults
        defaults = {
            "enabled": True,
            "performance_target_ms": 100,
            "retry_attempts": 3,
            "timeout_ms": 5000,
            "graceful_degradation": True,
            "log_level": "INFO"
        }
        
        # Update performance target if specified in config
        if 'hooks_system' in config and 'performance_target_ms' in config['hooks_system']:
            defaults['performance_target_ms'] = config['hooks_system']['performance_target_ms']
        
        # Update graceful degradation if specified
        if 'hooks_system' in config and 'graceful_degradation' in config['hooks_system']:
            defaults['graceful_degradation'] = config['hooks_system']['graceful_degradation']
            
        return defaults
    
    def get_verbosity(self) -> str:
        """
        Get the configured verbosity level.
        
        Returns:
            Verbosity level: 'minimal', 'normal', 'verbose', or 'debug'
        """
        # Try to get from hooks-config.json
        hooks_config_path = Path(__file__).parent.parent.parent / "Config" / "hooks-config.json"
        if hooks_config_path.exists():
            try:
                with open(hooks_config_path, 'r') as f:
                    hooks_config = json.load(f)
                    return hooks_config.get('general', {}).get('verbosity', 'minimal')
            except Exception:
                pass
        
        # Fallback to config or default
        return self.config.get('verbosity', 'minimal')
    
    def _configure_logging(self) -> None:
        """Configure logging based on verbosity level."""
        verbosity = self.get_verbosity()
        
        # Get root logger
        root_logger = logging.getLogger()
        
        # Clear existing handlers
        root_logger.handlers = []
        
        # Always add file handler
        file_handler = logging.FileHandler(os.path.expanduser('~/.claude/superclaude-hooks.log'))
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        root_logger.addHandler(file_handler)
        
        # Configure based on verbosity - but NEVER log to stdout for hooks
        # Stdout is reserved for JSON responses to Claude Code
        if verbosity == 'minimal':
            root_logger.setLevel(logging.WARNING)
        elif verbosity == 'normal':
            root_logger.setLevel(logging.WARNING)
        elif verbosity == 'verbose':
            root_logger.setLevel(logging.INFO)
        elif verbosity == 'debug':
            root_logger.setLevel(logging.DEBUG)
        
        # For Claude Code hooks, we must NEVER write logs to stdout
        # as it interferes with JSON communication
    
    def _start_performance_tracking(self) -> None:
        """Start performance tracking for hook execution."""
        self.start_time = time.time() * 1000  # Convert to milliseconds
        self.metrics["executions"] += 1
    
    def _end_performance_tracking(self, success: bool = True) -> float:
        """
        End performance tracking and log results.
        
        Args:
            success: Whether the hook execution was successful
            
        Returns:
            Execution time in milliseconds
        """
        if self.start_time is None:
            return 0.0
            
        execution_time_ms = (time.time() * 1000) - self.start_time
        
        # Update metrics
        self.metrics["total_execution_time_ms"] += execution_time_ms
        if success:
            self.metrics["successes"] += 1
        else:
            self.metrics["failures"] += 1
            
        # Calculate average execution time
        if self.metrics["executions"] > 0:
            self.metrics["avg_execution_time_ms"] = (
                self.metrics["total_execution_time_ms"] / self.metrics["executions"]
            )
        
        # Log performance warning if exceeding target
        if execution_time_ms > self.performance_target_ms:
            self.logger.warning(
                f"{self.hook_name} execution took {execution_time_ms:.2f}ms "
                f"(target: {self.performance_target_ms}ms)"
            )
        else:
            self.logger.debug(
                f"{self.hook_name} execution took {execution_time_ms:.2f}ms"
            )
            
        return execution_time_ms
    
    def _handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Handle errors with graceful degradation.
        
        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred
            
        Returns:
            Error response with graceful degradation
        """
        error_msg = f"{self.hook_name} error{' in ' + context if context else ''}: {str(error)}"
        self.logger.error(error_msg, exc_info=True)
        
        if self.config.get("graceful_degradation", True):
            return {
                "status": "degraded",
                "message": f"Hook {self.hook_name} failed gracefully - continuing without hook functionality",
                "error": str(error),
                "suggestions": []
            }
        else:
            return {
                "status": "error", 
                "message": error_msg,
                "error": str(error)
            }
    
    def _validate_tool_context(self, tool_name: str, tool_args: Dict[str, Any]) -> bool:
        """
        Validate that we have sufficient context to process the tool.
        
        Args:
            tool_name: Name of the tool being used
            tool_args: Arguments passed to the tool
            
        Returns:
            True if context is valid, False otherwise
        """
        if not tool_name:
            self.logger.warning("No tool name provided")
            return False
            
        if not isinstance(tool_args, dict):
            self.logger.warning(f"Invalid tool_args type: {type(tool_args)}")
            return False
            
        return True
    
    def _format_suggestion(self, suggestion_type: str, message: str, command: Optional[str] = None) -> Dict[str, Any]:
        """
        Format a suggestion for Claude Code.
        
        Args:
            suggestion_type: Type of suggestion (command, mcp_server, validation, etc.)
            message: Human-readable message
            command: Optional command to suggest
            
        Returns:
            Formatted suggestion dictionary
        """
        suggestion = {
            "type": suggestion_type,
            "message": message,
            "hook": self.hook_name
        }
        
        if command:
            suggestion["command"] = command
            
        return suggestion
    
    def _get_superclaude_root(self) -> Optional[Path]:
        """Get the SuperClaude framework root directory."""
        # Try to find SuperClaude directory from hook location
        current_path = Path(__file__).parent
        while current_path != current_path.parent:
            if (current_path / "SuperClaude").exists():
                return current_path / "SuperClaude"
            current_path = current_path.parent
        
        # Fallback to common locations
        possible_paths = [
            Path.home() / ".claude" / "SuperClaude",
            Path("/usr/local/share/SuperClaude"),
            Path.cwd() / "SuperClaude"
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
                
        self.logger.warning("Could not find SuperClaude root directory")
        return None
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for this hook."""
        return self.metrics.copy()
    
    # Abstract methods for hook implementations
    
    @abstractmethod
    def process_pre_tool_use(self, tool_name: str, tool_args: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        Process PreToolUse event.
        
        Args:
            tool_name: Name of the tool about to be used
            tool_args: Arguments for the tool
            session_id: Current session identifier
            
        Returns:
            Response with suggestions/validations for Claude Code
        """
        pass
    
    @abstractmethod  
    def process_post_tool_use(self, tool_name: str, tool_result: Any, tool_args: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        Process PostToolUse event.
        
        Args:
            tool_name: Name of the tool that was used
            tool_result: Result returned by the tool
            tool_args: Arguments that were passed to the tool
            session_id: Current session identifier
            
        Returns:
            Response with suggestions/validations for Claude Code
        """
        pass
    
    def process_session_start(self, session_id: str) -> Dict[str, Any]:
        """
        Process SessionStart event (optional for hooks that need it).
        
        Args:
            session_id: New session identifier
            
        Returns:
            Response with suggestions for Claude Code
        """
        return {"status": "success", "suggestions": []}
    
    # Main execution wrapper
    
    def execute(self, event: str, **kwargs) -> Dict[str, Any]:
        """
        Main execution wrapper with performance tracking and error handling.
        
        Args:
            event: Hook event (SessionStart, PreToolUse, PostToolUse)
            **kwargs: Event-specific arguments
            
        Returns:
            Hook response with suggestions and status
        """
        if not self.config.get("enabled", True):
            return {"status": "disabled", "suggestions": []}
            
        self._start_performance_tracking()
        
        try:
            # Route to appropriate handler
            if event == "SessionStart":
                result = self.process_session_start(kwargs.get("session_id", ""))
            elif event == "PreToolUse":
                result = self.process_pre_tool_use(
                    kwargs.get("tool_name", ""),
                    kwargs.get("tool_args", {}),
                    kwargs.get("session_id", "")
                )
            elif event == "PostToolUse":
                result = self.process_post_tool_use(
                    kwargs.get("tool_name", ""),
                    kwargs.get("tool_result", None),
                    kwargs.get("tool_args", {}),
                    kwargs.get("session_id", "")
                )
            else:
                raise ValueError(f"Unknown event type: {event}")
            
            self._end_performance_tracking(success=True)
            return result
            
        except Exception as e:
            self._end_performance_tracking(success=False)
            return self._handle_error(e, f"processing {event}")


# Utility functions for all hooks

def get_claude_home() -> Path:
    """Get Claude Code home directory."""
    return Path.home() / ".claude"

def load_superclaude_config(filename: str) -> Optional[Dict[str, Any]]:
    """
    Load SuperClaude framework configuration from .md file.
    
    Args:
        filename: Name of the configuration file (e.g., "ORCHESTRATOR.md")
        
    Returns:
        Parsed configuration or None if not found
    """
    superclaude_root = Path(__file__).parent.parent.parent
    config_path = superclaude_root / "Core" / filename
    
    if not config_path.exists():
        return None
        
    try:
        with open(config_path, 'r') as f:
            content = f.read()
            # TODO: Implement .md parsing logic based on framework_parser.py
            return {"raw_content": content}
    except Exception as e:
        logging.getLogger("SuperClaude.Hooks").error(f"Failed to load {filename}: {e}")
        return None