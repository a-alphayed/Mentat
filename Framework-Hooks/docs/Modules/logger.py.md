# logger.py - Structured Logging Utilities for SuperClaude Hooks

## Overview

The `logger.py` module provides structured logging of hook events for later analysis, focusing on capturing hook lifecycle, decisions, and errors in a structured JSON format. It implements simple, efficient logging without complex features, prioritizing performance and structured data collection for operational analysis and debugging.

## Purpose and Responsibilities

### Primary Functions
- **Hook Lifecycle Logging**: Structured capture of hook start/end events with timing
- **Decision Logging**: Record decision-making processes and rationale within hooks
- **Error Logging**: Comprehensive error capture with context and recovery information
- **Performance Monitoring**: Timing and performance metrics collection for optimization
- **Session Tracking**: Correlation of events across hook executions with session IDs

### Design Philosophy
- **Structured Data**: JSON-formatted logs for machine readability and analysis
- **Performance First**: Minimal overhead with efficient logging operations
- **Operational Focus**: Data collection for debugging and operational insights
- **Simple Interface**: Easy integration with hooks without complex configuration

## Core Architecture

### HookLogger Class
```python
class HookLogger:
    """Simple logger for SuperClaude-Lite hooks."""
    
    def __init__(self, log_dir: str = None, retention_days: int = None):
        """
        Initialize the logger.
        
        Args:
            log_dir: Directory to store log files. Defaults to cache/logs/
            retention_days: Number of days to keep log files. Defaults to 30.
        """
```

### Initialization and Configuration
```python
def __init__(self, log_dir: str = None, retention_days: int = None):
    # Load configuration
    self.config = self._load_config()
    
    # Check if logging is enabled
    if not self.config.get('logging', {}).get('enabled', True):
        self.enabled = False
        return
    
    self.enabled = True
    
    # Set up log directory
    if log_dir is None:
        root_dir = Path(__file__).parent.parent.parent
        log_dir_config = self.config.get('logging', {}).get('file_settings', {}).get('log_directory', 'cache/logs')
        log_dir = root_dir / log_dir_config
    
    self.log_dir = Path(log_dir)
    self.log_dir.mkdir(parents=True, exist_ok=True)
    
    # Session ID for correlating events
    self.session_id = str(uuid.uuid4())[:8]
```

**Initialization Features**:
- **Configurable Enablement**: Logging can be disabled via configuration
- **Flexible Directory**: Log directory configurable via parameter or configuration
- **Session Correlation**: Unique session ID for event correlation
- **Automatic Cleanup**: Old log file cleanup on initialization

## Configuration Management

### Configuration Loading
```python
def _load_config(self) -> Dict[str, Any]:
    """Load logging configuration from YAML file."""
    if UnifiedConfigLoader is None:
        # Return default configuration if loader not available
        return {
            'logging': {
                'enabled': True,
                'level': 'INFO',
                'file_settings': {
                    'log_directory': 'cache/logs',
                    'retention_days': 30
                }
            }
        }
    
    try:
        # Get project root
        root_dir = Path(__file__).parent.parent.parent
        loader = UnifiedConfigLoader(root_dir)
        
        # Load logging configuration
        config = loader.load_yaml('logging')
        return config or {}
    except Exception:
        # Return default configuration on error
        return {
            'logging': {
                'enabled': True,
                'level': 'INFO',
                'file_settings': {
                    'log_directory': 'cache/logs',
                    'retention_days': 30
                }
            }
        }
```

**Configuration Fallback Strategy**:
1. **Primary**: Load from logging.yaml via UnifiedConfigLoader
2. **Fallback**: Use hardcoded default configuration if loader unavailable
3. **Error Recovery**: Default configuration on any loading error
4. **Graceful Degradation**: Continue operation even with configuration issues

### Configuration Structure
```python
default_config = {
    'logging': {
        'enabled': True,              # Enable/disable logging
        'level': 'INFO',             # Log level (DEBUG, INFO, WARNING, ERROR)
        'file_settings': {
            'log_directory': 'cache/logs',    # Log file directory
            'retention_days': 30              # Days to keep log files
        }
    },
    'hook_configuration': {
        'hook_name': {
            'enabled': True           # Per-hook logging control
        }
    }
}
```

## Python Logger Integration

### Logger Setup
```python
def _setup_logger(self):
    """Set up the Python logger with JSON formatting."""
    self.logger = logging.getLogger("superclaude_lite_hooks")
    
    # Set log level from configuration
    log_level_str = self.config.get('logging', {}).get('level', 'INFO').upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    self.logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    self.logger.handlers.clear()
    
    # Create daily log file
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = self.log_dir / f"superclaude-lite-{today}.log"
    
    # File handler
    handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    handler.setLevel(logging.INFO)
    
    # Simple formatter - just output the message (which is already JSON)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    
    self.logger.addHandler(handler)
```

**Logger Features**:
- **Daily Log Files**: Separate log file per day for easy management
- **JSON Message Format**: Messages are pre-formatted JSON for structure
- **UTF-8 Encoding**: Support for international characters
- **Configurable Log Level**: Log level set from configuration
- **Handler Management**: Automatic cleanup of duplicate handlers

## Structured Event Logging

### Event Structure
```python
def _create_event(self, event_type: str, hook_name: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Create a structured event."""
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session": self.session_id,
        "hook": hook_name,
        "event": event_type
    }
    
    if data:
        event["data"] = data
        
    return event
```

**Event Structure Components**:
- **timestamp**: ISO 8601 UTC timestamp for precise timing
- **session**: 8-character session ID for event correlation
- **hook**: Hook name for operation identification
- **event**: Event type (start, end, decision, error)
- **data**: Optional additional data specific to event type

### Event Filtering
```python
def _should_log_event(self, hook_name: str, event_type: str) -> bool:
    """Check if this event should be logged based on configuration."""
    if not self.enabled:
        return False
        
    # Check hook-specific configuration
    hook_config = self.config.get('hook_configuration', {}).get(hook_name, {})
    if not hook_config.get('enabled', True):
        return False
        
    # Check event type configuration
    hook_logging = self.config.get('logging', {}).get('hook_logging', {})
    event_mapping = {
        'start': 'log_lifecycle',
        'end': 'log_lifecycle',
        'decision': 'log_decisions',
        'error': 'log_errors'
    }
    
    config_key = event_mapping.get(event_type, 'log_lifecycle')
    return hook_logging.get(config_key, True)
```

**Filtering Logic**:
1. **Global Enable Check**: Respect global logging enabled/disabled setting
2. **Hook-Specific Check**: Allow per-hook logging control
3. **Event Type Check**: Filter by event type (lifecycle, decisions, errors)
4. **Default Behavior**: Log all events if configuration not specified

## Core Logging Methods

### Hook Lifecycle Logging
```python
def log_hook_start(self, hook_name: str, context: Optional[Dict[str, Any]] = None):
    """Log the start of a hook execution."""
    if not self._should_log_event(hook_name, 'start'):
        return
        
    event = self._create_event("start", hook_name, context)
    self.logger.info(json.dumps(event))

def log_hook_end(self, hook_name: str, duration_ms: int, success: bool, result: Optional[Dict[str, Any]] = None):
    """Log the end of a hook execution."""
    if not self._should_log_event(hook_name, 'end'):
        return
        
    data = {
        "duration_ms": duration_ms,
        "success": success
    }
    if result:
        data["result"] = result
        
    event = self._create_event("end", hook_name, data)
    self.logger.info(json.dumps(event))
```

**Lifecycle Event Data**:
- **Start Events**: Hook name, optional context data, timestamp
- **End Events**: Duration in milliseconds, success/failure status, optional results
- **Session Correlation**: All events include session ID for correlation

### Decision Logging
```python
def log_decision(self, hook_name: str, decision_type: str, choice: str, reason: str):
    """Log a decision made by a hook."""
    if not self._should_log_event(hook_name, 'decision'):
        return
        
    data = {
        "type": decision_type,
        "choice": choice,
        "reason": reason
    }
    event = self._create_event("decision", hook_name, data)
    self.logger.info(json.dumps(event))
```

**Decision Event Components**:
- **type**: Category of decision (e.g., "mcp_server_selection", "mode_activation")
- **choice**: The decision made (e.g., "sequential", "brainstorming_mode")
- **reason**: Explanation for the decision (e.g., "complexity_score > 0.6")

### Error Logging
```python
def log_error(self, hook_name: str, error: str, context: Optional[Dict[str, Any]] = None):
    """Log an error that occurred in a hook."""
    if not self._should_log_event(hook_name, 'error'):
        return
        
    data = {
        "error": error
    }
    if context:
        data["context"] = context
        
    event = self._create_event("error", hook_name, data)
    self.logger.info(json.dumps(event))
```

**Error Event Components**:
- **error**: Error message or description
- **context**: Optional additional context about error conditions
- **Timestamp**: Precise timing for error correlation

## Log File Management

### Automatic Cleanup
```python
def _cleanup_old_logs(self):
    """Remove log files older than retention_days."""
    if self.retention_days <= 0:
        return
        
    cutoff_date = datetime.now() - timedelta(days=self.retention_days)
    
    # Find all log files
    log_pattern = self.log_dir / "superclaude-lite-*.log"
    for log_file in glob.glob(str(log_pattern)):
        try:
            # Extract date from filename
            filename = os.path.basename(log_file)
            date_str = filename.replace("superclaude-lite-", "").replace(".log", "")
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            
            # Remove if older than cutoff
            if file_date < cutoff_date:
                os.remove(log_file)
                
        except (ValueError, OSError):
            # Skip files that don't match expected format or can't be removed
            continue
```

**Cleanup Features**:
- **Configurable Retention**: Retention period set via configuration
- **Date-Based**: Log files named with YYYY-MM-DD format for easy parsing
- **Error Resilience**: Skip problematic files rather than failing entire cleanup
- **Initialization Cleanup**: Cleanup performed during logger initialization

### Log File Naming Convention
```
superclaude-lite-2024-12-15.log
superclaude-lite-2024-12-16.log
superclaude-lite-2024-12-17.log
```

**Naming Benefits**:
- **Chronological Sorting**: Files sort naturally by name
- **Easy Filtering**: Date-based filtering for log analysis
- **Rotation-Friendly**: Daily rotation without complex log rotation tools

## Global Interface and Convenience Functions

### Global Logger Instance
```python
# Global logger instance
_logger = None

def get_logger() -> HookLogger:
    """Get the global logger instance."""
    global _logger
    if _logger is None:
        _logger = HookLogger()
    return _logger
```

### Convenience Functions
```python
def log_hook_start(hook_name: str, context: Optional[Dict[str, Any]] = None):
    """Log the start of a hook execution."""
    get_logger().log_hook_start(hook_name, context)

def log_hook_end(hook_name: str, duration_ms: int, success: bool, result: Optional[Dict[str, Any]] = None):
    """Log the end of a hook execution."""
    get_logger().log_hook_end(hook_name, duration_ms, success, result)

def log_decision(hook_name: str, decision_type: str, choice: str, reason: str):
    """Log a decision made by a hook."""
    get_logger().log_decision(hook_name, decision_type, choice, reason)

def log_error(hook_name: str, error: str, context: Optional[Dict[str, Any]] = None):
    """Log an error that occurred in a hook."""
    get_logger().log_error(hook_name, error, context)
```

**Global Interface Benefits**:
- **Simplified Import**: Single import for all logging functions
- **Consistent Configuration**: Shared configuration across all hooks
- **Lazy Initialization**: Logger created only when first used
- **Memory Efficiency**: Single logger instance for entire application

## Hook Integration Patterns

### Basic Hook Integration
```python
from shared.logger import log_hook_start, log_hook_end, log_decision, log_error
import time

def pre_tool_use_hook(context):
    start_time = time.time()
    
    # Log hook start
    log_hook_start("pre_tool_use", {"operation_type": context.get("operation_type")})
    
    try:
        # Hook logic
        if context.get("complexity_score", 0) > 0.6:
            # Log decision
            log_decision("pre_tool_use", "delegation_activation", "enabled", "complexity_score > 0.6")
            result = {"delegation_enabled": True}
        else:
            result = {"delegation_enabled": False}
        
        # Log successful completion
        duration_ms = int((time.time() - start_time) * 1000)
        log_hook_end("pre_tool_use", duration_ms, True, result)
        
        return result
        
    except Exception as e:
        # Log error
        log_error("pre_tool_use", str(e), {"context": context})
        
        # Log failed completion
        duration_ms = int((time.time() - start_time) * 1000)
        log_hook_end("pre_tool_use", duration_ms, False)
        
        raise
```

### Advanced Integration with Context
```python
def session_start_hook(context):
    # Start with rich context
    log_hook_start("session_start", {
        "project_path": context.get("project_path"),
        "user_expertise": context.get("user_expertise", "intermediate"),
        "session_type": context.get("session_type", "interactive")
    })
    
    # Log multiple decisions
    log_decision("session_start", "configuration_load", "superclaude-config.json", "project configuration detected")
    log_decision("session_start", "learning_engine", "enabled", "user preference learning available")
    
    # Complex result logging
    result = {
        "configuration_loaded": True,
        "hooks_initialized": 7,
        "performance_targets": {
            "session_start_ms": 50,
            "pre_tool_use_ms": 200
        }
    }
    
    log_hook_end("session_start", 45, True, result)
```

## Log Analysis and Monitoring

### Log Entry Format
```json
{
  "timestamp": "2024-12-15T14:30:22.123456Z",
  "session": "abc12345",
  "hook": "pre_tool_use",
  "event": "start",
  "data": {
    "operation_type": "build",
    "complexity_score": 0.7
  }
}
```

### Example Log Sequence
```json
{"timestamp": "2024-12-15T14:30:22.123Z", "session": "abc12345", "hook": "pre_tool_use", "event": "start", "data": {"operation_type": "build"}}
{"timestamp": "2024-12-15T14:30:22.125Z", "session": "abc12345", "hook": "pre_tool_use", "event": "decision", "data": {"type": "mcp_server_selection", "choice": "sequential", "reason": "complex analysis required"}}
{"timestamp": "2024-12-15T14:30:22.148Z", "session": "abc12345", "hook": "pre_tool_use", "event": "end", "data": {"duration_ms": 25, "success": true, "result": {"mcp_servers": ["sequential"]}}}
```

### Analysis Queries
```bash
# Find all errors in the last day
jq 'select(.event == "error")' superclaude-lite-2024-12-15.log

# Calculate average hook execution times
jq 'select(.event == "end") | .data.duration_ms' superclaude-lite-2024-12-15.log | awk '{sum+=$1; count++} END {print sum/count}'

# Find all decisions made by specific hook
jq 'select(.hook == "pre_tool_use" and .event == "decision")' superclaude-lite-2024-12-15.log

# Track session completion rates
jq 'select(.hook == "session_start" and .event == "end") | .data.success' superclaude-lite-2024-12-15.log
```

## Performance Characteristics

### Logging Performance
- **Event Creation**: <1ms for structured event creation
- **File Writing**: <5ms for typical log entry with JSON serialization
- **Configuration Loading**: <10ms during initialization
- **Cleanup Operations**: <50ms for cleanup of old log files (depends on file count)

### Memory Efficiency
- **Logger Instance**: ~1-2KB for logger instance with configuration
- **Session Tracking**: ~100B for session ID and correlation data
- **Event Buffer**: Direct write-through, no event buffering for reliability
- **Configuration Cache**: ~500B for logging configuration

### File System Impact
- **Daily Log Files**: Automatic daily rotation with configurable retention
- **Log File Size**: Typical ~10-50KB per day depending on hook activity
- **Directory Structure**: Simple flat file structure in configurable directory
- **Cleanup Efficiency**: O(n) cleanup where n is number of log files

## Error Handling and Reliability

### Logging Error Handling
```python
def log_hook_start(self, hook_name: str, context: Optional[Dict[str, Any]] = None):
    """Log the start of a hook execution."""
    try:
        if not self._should_log_event(hook_name, 'start'):
            return
            
        event = self._create_event("start", hook_name, context)
        self.logger.info(json.dumps(event))
    except Exception:
        # Silent failure - logging should never break hook execution
        pass
```

### Reliability Features
- **Silent Failure**: Logging errors never interrupt hook execution
- **Graceful Degradation**: Continue operation even if logging fails
- **Configuration Fallback**: Default configuration if loading fails
- **File System Resilience**: Handle permission errors and disk space issues

### Recovery Mechanisms
- **Logger Recreation**: Recreate logger if file handle issues occur
- **Directory Creation**: Automatically create log directory if missing
- **Permission Handling**: Graceful fallback if log directory not writable
- **Disk Space**: Continue operation even if disk space limited

## Configuration Examples

### Basic Configuration (logging.yaml)
```yaml
logging:
  enabled: true
  level: INFO
  
  file_settings:
    log_directory: cache/logs
    retention_days: 30
  
  hook_logging:
    log_lifecycle: true
    log_decisions: true
    log_errors: true
```

### Advanced Configuration
```yaml
logging:
  enabled: true
  level: DEBUG
  
  file_settings:
    log_directory: ${LOG_DIR:./logs}
    retention_days: ${LOG_RETENTION:7}
    max_file_size_mb: 10
  
  hook_logging:
    log_lifecycle: true
    log_decisions: true
    log_errors: true
    log_performance: true

hook_configuration:
  session_start:
    enabled: true
  pre_tool_use:
    enabled: true
  post_tool_use:
    enabled: false    # Disable logging for this hook
  pre_compact:
    enabled: true
```

### Production Configuration
```yaml
logging:
  enabled: true
  level: WARNING      # Reduce verbosity in production
  
  file_settings:
    log_directory: /var/log/superclaude
    retention_days: 90
  
  hook_logging:
    log_lifecycle: false    # Disable lifecycle logging
    log_decisions: true     # Keep decision logging
    log_errors: true        # Always log errors
```

## Usage Examples

### Basic Logging
```python
from shared.logger import log_hook_start, log_hook_end, log_decision, log_error

# Simple hook with logging
def my_hook(context):
    log_hook_start("my_hook")
    
    try:
        # Do work
        result = perform_operation()
        log_hook_end("my_hook", 150, True, {"result": result})
        return result
    except Exception as e:
        log_error("my_hook", str(e))
        log_hook_end("my_hook", 150, False)
        raise
```

### Decision Logging
```python
def intelligent_hook(context):
    log_hook_start("intelligent_hook", {"complexity": context.get("complexity_score")})
    
    # Log decision-making process
    if context.get("complexity_score", 0) > 0.6:
        log_decision("intelligent_hook", "server_selection", "sequential", "high complexity detected")
        server = "sequential"
    else:
        log_decision("intelligent_hook", "server_selection", "morphllm", "low complexity operation")
        server = "morphllm"
    
    log_hook_end("intelligent_hook", 85, True, {"selected_server": server})
```

### Error Context Logging
```python
def error_prone_hook(context):
    log_hook_start("error_prone_hook")
    
    try:
        risky_operation()
    except SpecificError as e:
        log_error("error_prone_hook", f"Specific error: {e}", {
            "context": context,
            "error_type": "SpecificError",
            "recovery_attempted": True
        })
        # Attempt recovery
        recovery_operation()
    except Exception as e:
        log_error("error_prone_hook", f"Unexpected error: {e}", {
            "context": context,
            "error_type": type(e).__name__
        })
        raise
```

## Dependencies and Relationships

### Internal Dependencies
- **yaml_loader**: Configuration loading (optional, fallback available)
- **Standard Libraries**: json, logging, os, time, datetime, pathlib, glob, uuid

### Framework Integration
- **Hook Lifecycle**: Integrated into all 7 SuperClaude hooks for consistent logging
- **Global Interface**: Shared logger instance across all hooks and modules
- **Configuration Management**: Unified configuration via yaml_loader integration

### External Analysis
- **JSON Format**: Structured logs for analysis with jq, logstash, elasticsearch
- **Daily Rotation**: Compatible with log analysis tools expecting daily files
- **Session Correlation**: Event correlation for debugging and monitoring

---

*This module provides the essential logging infrastructure for the SuperClaude framework, enabling comprehensive operational monitoring, debugging, and analysis through structured, high-performance event logging with reliable error handling and flexible configuration.*