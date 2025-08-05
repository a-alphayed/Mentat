#!/usr/bin/env python3
"""
SuperClaude Session Lifecycle Hook

High priority hook for automatic session management per SESSION_LIFECYCLE.md.
Handles session state transitions and automatic checkpoint creation.

Events: SessionStart, PostToolUse (time-based)
Responsibilities:
- Trigger /sc:load for new projects automatically
- Monitor for automatic checkpoint conditions
- Handle session state transitions
- Performance monitoring integration

Usage:
    python hook.py session_start ${session.id}
    python hook.py post ${tool.name} "${tool.result}" "${tool.args}" ${session.id}
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.WARNING, format='[%(name)s] %(levelname)s: %(message)s')
logger = logging.getLogger('SuperClaude.Hooks.SessionLifecycle')

# Try to import yaml for configuration loading
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    logger.warning("PyYAML not available - using fallback configuration")

# Add the common directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "common"))

from base_hook import BaseHook
from framework_parser import FrameworkParser
from utils import (
    parse_tool_args,
    detect_project_type,
    is_git_repository,
    get_system_info
)


class SessionLifecycleHook(BaseHook):
    """
    Session Lifecycle Hook implementation.
    
    Provides automatic session management per SESSION_LIFECYCLE.md:
    - Auto /sc:load for new projects
    - Automatic checkpoint triggers
    - Session state tracking
    - Performance monitoring integration
    """
    
    def __init__(self, config_path: Optional[str] = None, input_data: Optional[Dict[str, Any]] = None):
        """Initialize Session Lifecycle Hook."""
        super().__init__("SessionLifecycle", config_path)
        
        # Initialize framework parser
        try:
            self.parser = FrameworkParser()
            self.logger.info("Framework parser initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize framework parser: {e}")
            self.parser = None
        
        # Session tracking
        self.sessions = {}
        self.session_start_times = {}
        
        # Load configurations from YAML files
        self.checkpoint_config = self._load_checkpoint_config()
        self.performance_targets = self._load_performance_targets()
        self.memory_key_patterns = self.checkpoint_config.get('memory_key_patterns', {})
    
    def _load_checkpoint_config(self) -> Dict[str, Any]:
        """Load checkpoint triggers configuration from YAML or use defaults."""
        # Define fallback configuration
        fallback_config = {
            'time_based': {
                'enabled': True,
                'interval_minutes': 30
            },
            'task_based': {
                'enabled': True,
                'high_priority_only': True
            },
            'risk_based': {
                'enabled': True,
                'major_operations': ['Write', 'Edit', 'MultiEdit', 'Delete'],
                'file_threshold': 50
            },
            'error_recovery': {
                'enabled': True,
                'auto_checkpoint': True
            },
            'memory_key_patterns': {
                'time_based': 'checkpoints/auto-{timestamp}',
                'task_based': 'checkpoints/task-{task_id}-{timestamp}',
                'risk_based': 'checkpoints/risk-{operation}-{timestamp}',
                'error_recovery': 'checkpoints/recovery-{timestamp}',
                'manual': 'checkpoints/manual-{timestamp}'
            }
        }
        
        # Try to load from YAML if available
        if YAML_AVAILABLE:
            config_path = Path(__file__).parent.parent / "Resources" / "checkpoint_triggers.yaml"
            try:
                if config_path.exists():
                    with open(config_path, 'r') as f:
                        loaded_config = yaml.safe_load(f)
                        
                        # Merge checkpoint_triggers section
                        if 'checkpoint_triggers' in loaded_config:
                            triggers = loaded_config['checkpoint_triggers']
                            
                            # Validate and merge each trigger type
                            if 'time_based' in triggers:
                                validated = self._validate_time_based_config(triggers['time_based'])
                                fallback_config['time_based'].update(validated)
                                
                            if 'task_based' in triggers:
                                validated = self._validate_task_based_config(triggers['task_based'])
                                fallback_config['task_based'].update(validated)
                                
                            if 'risk_based' in triggers:
                                validated = self._validate_risk_based_config(triggers['risk_based'])
                                fallback_config['risk_based'].update(validated)
                                
                            if 'error_recovery' in triggers:
                                validated = self._validate_error_recovery_config(triggers['error_recovery'])
                                fallback_config['error_recovery'].update(validated)
                        
                        # Add memory key patterns if present
                        if 'memory_key_patterns' in loaded_config:
                            fallback_config['memory_key_patterns'] = loaded_config['memory_key_patterns']
                            
                        logger.debug("Loaded checkpoint configuration from YAML")
                else:
                    logger.warning(f"Checkpoint configuration not found at {config_path}")
                    
            except yaml.YAMLError as e:
                logger.error(f"YAML parsing error in checkpoint configuration: {e}")
            except Exception as e:
                logger.error(f"Error loading checkpoint configuration: {type(e).__name__}: {e}")
        
        return fallback_config
    
    def _load_performance_targets(self) -> Dict[str, Any]:
        """Load performance targets from YAML or use defaults."""
        # Define fallback targets
        fallback_targets = {
            'session_initialization': 500,     # SESSION_LIFECYCLE.md: <500ms
            'checkpoint_creation': 1000,       # SESSION_LIFECYCLE.md: <1s
            'checkpoint_restoration': 500,     # SESSION_LIFECYCLE.md: <500ms
            'summary_generation': 2000,        # SESSION_LIFECYCLE.md: <2s
            'memory_operations': 200           # SESSION_LIFECYCLE.md: <200ms each
        }
        
        # Try to load from YAML if available
        if YAML_AVAILABLE:
            targets_path = Path(__file__).parent.parent / "Resources" / "performance_targets.yaml"
            try:
                if targets_path.exists():
                    with open(targets_path, 'r') as f:
                        config = yaml.safe_load(f)
                        
                        if 'performance_targets' in config:
                            targets = config['performance_targets']
                            # Map from performance_targets.yaml keys to our keys
                            key_mapping = {
                                'project_loading': 'session_initialization',
                                'checkpoint_creation': 'checkpoint_creation',
                                'session_restore': 'checkpoint_restoration',
                                'session_save': 'summary_generation',
                                'memory_operations': 'memory_operations'
                            }
                            
                            for yaml_key, our_key in key_mapping.items():
                                if yaml_key in targets:
                                    fallback_targets[our_key] = targets[yaml_key]
                                    
                        logger.debug("Loaded performance targets from YAML")
                else:
                    logger.warning(f"Performance targets not found at {targets_path}")
                    
            except yaml.YAMLError as e:
                logger.error(f"YAML parsing error in performance targets: {e}")
            except Exception as e:
                logger.error(f"Error loading performance targets: {type(e).__name__}: {e}")
                
        return fallback_targets
    
    def _validate_time_based_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate time-based checkpoint configuration."""
        validated = {}
        
        # Validate enabled flag
        if 'enabled' in config:
            validated['enabled'] = bool(config['enabled'])
            
        # Validate interval_minutes
        if 'interval_minutes' in config:
            try:
                interval = float(config['interval_minutes'])
                if 1 <= interval <= 1440:  # 1 minute to 24 hours
                    validated['interval_minutes'] = interval
                else:
                    logger.warning(f"Invalid interval_minutes: {interval} (must be 1-1440), using default")
            except (ValueError, TypeError):
                logger.warning(f"Invalid interval_minutes: {config['interval_minutes']}, using default")
                
        return validated
    
    def _validate_task_based_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate task-based checkpoint configuration."""
        validated = {}
        
        # Validate enabled flag
        if 'enabled' in config:
            validated['enabled'] = bool(config['enabled'])
            
        # Validate high_priority_only flag
        if 'high_priority_only' in config:
            validated['high_priority_only'] = bool(config['high_priority_only'])
            
        return validated
    
    def _validate_risk_based_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate risk-based checkpoint configuration."""
        validated = {}
        
        # Validate enabled flag
        if 'enabled' in config:
            validated['enabled'] = bool(config['enabled'])
            
        # Validate major_operations list
        if 'major_operations' in config and isinstance(config['major_operations'], list):
            # Filter to valid tool names only
            valid_operations = [op for op in config['major_operations'] if isinstance(op, str)]
            if valid_operations:
                validated['major_operations'] = valid_operations
            else:
                logger.warning("No valid operations in major_operations list")
                
        # Validate file_threshold
        if 'file_threshold' in config:
            try:
                threshold = int(config['file_threshold'])
                if 1 <= threshold <= 1000:
                    validated['file_threshold'] = threshold
                else:
                    logger.warning(f"Invalid file_threshold: {threshold} (must be 1-1000), using default")
            except (ValueError, TypeError):
                logger.warning(f"Invalid file_threshold: {config['file_threshold']}, using default")
                
        return validated
    
    def _validate_error_recovery_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate error recovery checkpoint configuration."""
        validated = {}
        
        # Validate enabled flag
        if 'enabled' in config:
            validated['enabled'] = bool(config['enabled'])
            
        # Validate auto_checkpoint flag
        if 'auto_checkpoint' in config:
            validated['auto_checkpoint'] = bool(config['auto_checkpoint'])
            
        return validated
    
    def _get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Get or create session information."""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'id': session_id,
                'start_time': time.time(),
                'last_activity': time.time(),
                'operation_count': 0,
                'checkpoint_count': 0,
                'project_activated': False,
                'working_directory': str(Path.cwd()),
                'project_types': [],
                'high_priority_operations': 0,
                'last_checkpoint_time': time.time(),
                'risk_operations': []
            }
            self.session_start_times[session_id] = time.time()
        
        return self.sessions[session_id]
    
    def _update_session_activity(self, session_id: str, tool_name: str, operation_data: Optional[Dict[str, Any]] = None) -> None:
        """Update session activity tracking."""
        session_info = self._get_session_info(session_id)
        
        session_info['last_activity'] = time.time()
        session_info['operation_count'] += 1
        
        # Track high-priority operations
        high_priority_tools = ['Write', 'Edit', 'MultiEdit', 'Delete', 'Bash', 'Task']
        if tool_name in high_priority_tools:
            session_info['high_priority_operations'] += 1
        
        # Track risk operations
        risk_operations = ['Delete', 'Bash', 'MultiEdit']
        if tool_name in risk_operations:
            session_info['risk_operations'].append({
                'tool': tool_name,
                'timestamp': time.time(),
                'data': operation_data
            })
        
        self.sessions[session_id] = session_info
    
    def _should_suggest_project_load(self, session_id: str, working_directory: str) -> bool:
        """Check if /sc:load should be suggested for the session."""
        session_info = self._get_session_info(session_id)
        
        # Don't suggest if already activated
        if session_info.get('project_activated', False):
            return False
        
        # Check if working directory looks like a project
        working_path = Path(working_directory)
        
        # Look for project indicators
        project_indicators = [
            'pyproject.toml', 'package.json', 'Cargo.toml', 'go.mod', 'pom.xml', 
            'build.gradle', 'Dockerfile', 'README.md', '.git', 'SuperClaude'
        ]
        
        has_project_files = any((working_path / indicator).exists() for indicator in project_indicators)
        
        # Check if it's a git repository
        is_git_repo = is_git_repository(working_path)
        
        # Suggest load if project indicators found
        return has_project_files or is_git_repo
    
    def _check_checkpoint_triggers(self, session_id: str, tool_name: str, tool_result: Any) -> List[Dict[str, str]]:
        """Check if automatic checkpoint should be triggered."""
        session_info = self._get_session_info(session_id)
        suggestions = []
        
        current_time = time.time()
        time_since_last_checkpoint = current_time - session_info.get('last_checkpoint_time', current_time)
        time_since_session_start = current_time - session_info.get('start_time', current_time)
        
        # Time-based checkpoint trigger
        if (self.checkpoint_config['time_based']['enabled'] and 
            time_since_last_checkpoint > (self.checkpoint_config['time_based']['interval_minutes'] * 60)):
            
            suggestions.append({
                'type': 'session_checkpoint',
                'trigger': 'time_based',
                'message': f"Automatic checkpoint recommended (≥{self.checkpoint_config['time_based']['interval_minutes']} minutes elapsed)",
                'command': '/sc:save --checkpoint',
                'priority': 'medium'
            })
        
        # Task-based checkpoint trigger
        if (self.checkpoint_config['task_based']['enabled'] and 
            tool_name in ['Write', 'Edit', 'MultiEdit'] and 
            session_info.get('high_priority_operations', 0) % 5 == 0):
            
            suggestions.append({
                'type': 'session_checkpoint',
                'trigger': 'task_based',
                'message': f"Checkpoint recommended after {session_info.get('high_priority_operations', 0)} high-priority operations",
                'command': '/sc:save --checkpoint',
                'priority': 'high'
            })
        
        # Risk-based checkpoint trigger
        if (self.checkpoint_config['risk_based']['enabled'] and 
            tool_name in self.checkpoint_config['risk_based']['major_operations']):
            
            suggestions.append({
                'type': 'session_checkpoint',
                'trigger': 'risk_based',
                'message': f"Checkpoint recommended before/after major operation: {tool_name}",
                'command': '/sc:save --checkpoint',
                'priority': 'high'
            })
        
        # Error recovery checkpoint
        if tool_result and isinstance(tool_result, str) and ('error' in tool_result.lower() or 'failed' in tool_result.lower()):
            suggestions.append({
                'type': 'session_checkpoint',
                'trigger': 'error_recovery',
                'message': "Checkpoint recommended after error for recovery purposes",
                'command': '/sc:save --checkpoint --recovery',
                'priority': 'high'
            })
        
        return suggestions
    
    def _check_session_end_conditions(self, session_id: str) -> List[Dict[str, str]]:
        """Check if session should be ended/saved."""
        session_info = self._get_session_info(session_id)
        suggestions = []
        
        current_time = time.time()
        session_duration = current_time - session_info.get('start_time', current_time)
        inactive_time = current_time - session_info.get('last_activity', current_time)
        
        # Long session warning
        if session_duration > (2 * 3600):  # 2 hours
            suggestions.append({
                'type': 'session_management',
                'message': f"Long session detected ({session_duration/3600:.1f} hours) - consider /sc:save",
                'command': '/sc:save --summarize',
                'priority': 'medium'
            })
        
        # Extended inactivity
        if inactive_time > (30 * 60):  # 30 minutes
            suggestions.append({
                'type': 'session_management',
                'message': f"Extended inactivity ({inactive_time/60:.0f} minutes) - consider /sc:save",
                'command': '/sc:save',
                'priority': 'low'
            })
        
        return suggestions
    
    def _get_session_performance_metrics(self, session_id: str) -> Dict[str, Any]:
        """Get session performance metrics."""
        session_info = self._get_session_info(session_id)
        current_time = time.time()
        
        session_duration = current_time - session_info.get('start_time', current_time)
        operations_per_minute = (session_info.get('operation_count', 0) / max(session_duration / 60, 1))
        
        return {
            'session_duration_minutes': session_duration / 60,
            'total_operations': session_info.get('operation_count', 0),
            'operations_per_minute': operations_per_minute,
            'high_priority_operations': session_info.get('high_priority_operations', 0),
            'checkpoint_count': session_info.get('checkpoint_count', 0),
            'risk_operations_count': len(session_info.get('risk_operations', [])),
            'performance_rating': 'good' if operations_per_minute > 2 else 'normal' if operations_per_minute > 1 else 'slow'
        }
    
    def process_session_start(self, session_id: str) -> Dict[str, Any]:
        """Process SessionStart event for session lifecycle management."""
        try:
            # Initialize session tracking
            session_info = self._get_session_info(session_id)
            working_directory = str(Path.cwd())
            
            # Update session info
            session_info['working_directory'] = working_directory
            session_info['project_types'] = detect_project_type(working_directory)
            session_info['system_info'] = get_system_info()
            
            suggestions = []
            
            # Check if /sc:load should be suggested
            if self._should_suggest_project_load(session_id, working_directory):
                suggestions.append({
                    'type': 'session_initialization',
                    'message': f"Project detected in {working_directory} - recommend loading project context",
                    'command': '/sc:load',
                    'priority': 'high',
                    'reason': f"Detected project types: {', '.join(session_info['project_types'])}"
                })
            
            # System information suggestions
            if session_info.get('system_info', {}).get('platform') == 'Windows':
                suggestions.append({
                    'type': 'system_optimization',
                    'message': "Windows detected - consider using absolute paths",
                    'priority': 'info'
                })
            
            # Performance baseline
            performance_metrics = self._get_session_performance_metrics(session_id)
            
            response = {
                'status': 'success',
                'hook': 'session_lifecycle',
                'event': 'session_start',
                'session_info': {
                    'id': session_id,
                    'working_directory': working_directory,
                    'project_types': session_info['project_types'],
                    'start_time': session_info['start_time']
                },
                'suggestions': suggestions,
                'performance_metrics': performance_metrics,
                'metadata': {
                    'session_id': session_id,
                    'initialization_time_ms': 0  # Will be set by performance tracking
                }
            }
            
            self.logger.info(f"Session {session_id} started in {working_directory}")
            if suggestions:
                self.logger.info(f"Generated {len(suggestions)} session initialization suggestions")
            
            return response
            
        except Exception as e:
            return self._handle_error(e, "session_start")
    
    def process_pre_tool_use(self, tool_name: str, tool_args: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        Process PreToolUse event for session lifecycle management.
        
        This method is required by the BaseHook abstract class.
        
        Args:
            tool_name: Name of the tool being invoked
            tool_args: Arguments passed to the tool
            session_id: Current session identifier
            
        Returns:
            Dict with status and any messages
        """
        try:
            # Update session activity
            self._update_session_activity(session_id, tool_name, {'args': tool_args})
            
            # Log the tool invocation
            self.logger.debug(f"PreToolUse: {tool_name} starting for session {session_id}")
            
            return {
                "status": "success",
                "hook": "session_lifecycle",
                "event": "pre_tool_use",
                "message": f"Session lifecycle monitoring started for {tool_name}"
            }
            
        except Exception as e:
            return self._handle_error(e, "pre_tool_use")
    
    def process_post_tool_use(self, tool_name: str, tool_result: Any, tool_args: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Process PostToolUse event for session lifecycle monitoring."""
        try:
            # Update session activity
            self._update_session_activity(session_id, tool_name, {'args': tool_args, 'result': str(tool_result)[:100] if tool_result else None})
            
            suggestions = []
            
            # Check checkpoint triggers
            checkpoint_suggestions = self._check_checkpoint_triggers(session_id, tool_name, tool_result)
            suggestions.extend(checkpoint_suggestions)
            
            # Check session end conditions
            session_end_suggestions = self._check_session_end_conditions(session_id)
            suggestions.extend(session_end_suggestions)
            
            # Special handling for /sc:load and /sc:save commands
            if tool_name == 'Bash' and tool_args:
                command = tool_args.get('command', '')
                if '/sc:load' in command:
                    session_info = self._get_session_info(session_id)
                    session_info['project_activated'] = True
                    self.logger.info(f"Project activation detected for session {session_id}")
                elif '/sc:save' in command:
                    session_info = self._get_session_info(session_id) 
                    session_info['checkpoint_count'] += 1
                    session_info['last_checkpoint_time'] = time.time()
                    self.logger.info(f"Checkpoint created for session {session_id}")
            
            # Performance monitoring
            performance_metrics = self._get_session_performance_metrics(session_id)
            
            # Performance recommendations
            if performance_metrics['operations_per_minute'] < 1:
                suggestions.append({
                    'type': 'performance_optimization',
                    'message': f"Low operation rate ({performance_metrics['operations_per_minute']:.1f}/min) - consider optimization",
                    'suggestions': [
                        'Use batch operations when possible',
                        'Enable MCP server caching',
                        'Consider task delegation for large operations'
                    ],
                    'priority': 'info'
                })
            
            response = {
                'status': 'success',
                'hook': 'session_lifecycle',
                'event': 'post_tool_use',
                'suggestions': suggestions,
                'performance_metrics': performance_metrics,
                'metadata': {
                    'session_id': session_id,
                    'tool_name': tool_name,
                    'session_duration_minutes': performance_metrics['session_duration_minutes'],
                    'total_operations': performance_metrics['total_operations']
                }
            }
            
            # Log important suggestions
            high_priority_suggestions = [s for s in suggestions if s.get('priority') == 'high']
            if high_priority_suggestions:
                self.logger.info(f"Generated {len(high_priority_suggestions)} high-priority session suggestions")
            
            return response
            
        except Exception as e:
            return self._handle_error(e, "post_tool_use")


def main():
    """Main entry point for session lifecycle hook."""
    if len(sys.argv) < 2:
        print("Usage: python hook.py <event> [session_id] [tool_name] [tool_result] [tool_args]", file=sys.stderr)
        sys.exit(1)
    
    event = sys.argv[1]
    
    # Create hook instance
    try:
        hook = SessionLifecycleHook(input_data={})
    except Exception as e:
        print(f"Error initializing hook: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Execute hook based on event
    try:
        if event == "session_start":
            # Session ID is optional, use default if not provided
            session_id = sys.argv[2] if len(sys.argv) > 2 else "default"
            result = hook.execute("SessionStart", session_id=session_id)
            
        elif event == "post":
            # For post event, arguments should be: post <tool_name> <tool_result> <tool_args> <session_id>
            if len(sys.argv) < 6:
                print("Usage for post: python hook.py post <tool_name> <tool_result> <tool_args> <session_id>", file=sys.stderr)
                sys.exit(1)
                
            tool_name = sys.argv[2]
            tool_result = sys.argv[3] if sys.argv[3] != "null" and sys.argv[3] != "''" else None
            tool_args_str = sys.argv[4]
            session_id = sys.argv[5] if len(sys.argv) > 5 else "default"
            
            # Parse tool arguments
            tool_args = parse_tool_args(tool_args_str)
            
            result = hook.execute("PostToolUse", tool_name=tool_name, tool_result=tool_result, tool_args=tool_args, session_id=session_id)
            
        else:
            print(f"Unknown event: {event}", file=sys.stderr)
            sys.exit(1)
        
        # Output result as JSON for Claude Code
        print(json.dumps(result, indent=2))
        
        # Exit with appropriate code
        sys.exit(0 if result.get('status') == 'success' else 1)
        
    except Exception as e:
        error_result = {
            'status': 'error',
            'hook': 'session_lifecycle',
            'error': str(e),
            'message': 'Session lifecycle hook execution failed'
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()