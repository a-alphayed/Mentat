# Logging Configuration (`logging.yaml`)

## Overview

The `logging.yaml` file defines the logging configuration for the SuperClaude-Lite framework hooks. This configuration provides comprehensive logging capabilities while maintaining performance and privacy standards for production environments.

## Purpose and Role

The logging configuration serves as:
- **Execution Monitoring**: Tracks hook lifecycle events and execution patterns
- **Performance Analysis**: Logs timing information for optimization analysis
- **Error Tracking**: Captures and logs error events with appropriate detail
- **Privacy Protection**: Sanitizes user content while preserving debugging capability
- **Development Support**: Provides configurable verbosity for development and troubleshooting

## Configuration Structure

### 1. Core Logging Settings (`logging`)

#### Basic Configuration
```yaml
logging:
  enabled: true
  level: "INFO"  # ERROR, WARNING, INFO, DEBUG
```

**Purpose**: Controls overall logging enablement and verbosity level
**Levels**: ERROR (critical only) → WARNING (issues) → INFO (operations) → DEBUG (detailed)
**Default**: INFO provides optimal balance of information and performance

#### File Settings
```yaml
file_settings:
  log_directory: "cache/logs"
  retention_days: 30
  rotation_strategy: "daily"
```

**Log Directory**: Stores logs in cache directory for easy cleanup
**Retention Policy**: 30-day retention balances storage with debugging needs
**Rotation Strategy**: Daily rotation prevents large log files

#### Hook Logging Settings
```yaml
hook_logging:
  log_lifecycle: true      # Log hook start/end events
  log_decisions: true      # Log decision points
  log_errors: true         # Log error events
  log_timing: true         # Include timing information
```

**Lifecycle Logging**: Tracks hook execution start/end for performance analysis
**Decision Logging**: Records key decision points for debugging and learning
**Error Logging**: Comprehensive error capture with context preservation
**Timing Logging**: Performance metrics for optimization and monitoring

#### Performance Settings
```yaml
performance:
  max_overhead_ms: 1       # Maximum acceptable logging overhead
  async_logging: false     # Keep simple for now
```

**Overhead Limit**: 1ms maximum overhead ensures logging doesn't impact performance
**Synchronous Logging**: Simple synchronous approach for reliability and consistency

#### Privacy Settings
```yaml
privacy:
  sanitize_user_content: true
  exclude_sensitive_data: true
  anonymize_session_ids: false  # Keep for correlation
```

**Content Sanitization**: Removes or masks user content from logs
**Sensitive Data Protection**: Excludes passwords, tokens, and personal information
**Session Correlation**: Preserves session IDs for debugging while protecting user identity

### 2. Hook-Specific Configuration (`hook_configuration`)

#### Pre-Tool Use Hook
```yaml
pre_tool_use:
  enabled: true
  log_tool_selection: true
  log_input_validation: true
```

**Tool Selection Logging**: Records MCP server routing decisions
**Input Validation Logging**: Tracks validation results and failures
**Purpose**: Debug routing logic and validate input processing

#### Post-Tool Use Hook
```yaml
post_tool_use:
  enabled: true
  log_output_processing: true
  log_integration_success: true
```

**Output Processing**: Logs quality validation and rule compliance checks
**Integration Success**: Records successful framework integration outcomes
**Purpose**: Monitor quality gates and integration effectiveness

#### Session Start Hook
```yaml
session_start:
  enabled: true
  log_initialization: true
  log_configuration_loading: true
```

**Initialization Logging**: Tracks project detection and mode activation
**Configuration Loading**: Records YAML configuration loading and validation
**Purpose**: Debug session startup issues and configuration problems

#### Pre-Compact Hook
```yaml
pre_compact:
  enabled: true
  log_compression_decisions: true
```

**Compression Decisions**: Records compression level selection and strategy choices
**Purpose**: Optimize compression effectiveness and debug quality issues

#### Notification Hook
```yaml
notification:
  enabled: true
  log_notification_handling: true
```

**Notification Handling**: Tracks notification processing and pattern updates
**Purpose**: Debug notification system and monitor pattern update effectiveness

#### Stop Hook
```yaml
stop:
  enabled: true
  log_cleanup_operations: true
```

**Cleanup Operations**: Records session analytics generation and cleanup processes
**Purpose**: Monitor session termination and ensure proper cleanup

#### Subagent Stop Hook
```yaml
subagent_stop:
  enabled: true
  log_subagent_cleanup: true
```

**Subagent Cleanup**: Tracks task management analytics and coordination cleanup
**Purpose**: Debug task management delegation and monitor coordination effectiveness

### 3. Development Settings (`development`)

```yaml
development:
  verbose_errors: true
  include_stack_traces: false  # Keep logs clean
  debug_mode: false
```

**Verbose Errors**: Provides detailed error messages for troubleshooting
**Stack Traces**: Disabled by default to keep logs clean and readable
**Debug Mode**: Disabled for production performance, can be enabled for deep debugging

## Default Values and Meanings

### Log Levels
- **ERROR**: Only critical errors that prevent operation (default for production)
- **WARNING**: Issues that don't prevent operation but should be addressed
- **INFO**: Normal operational information and key decision points (recommended default)
- **DEBUG**: Detailed execution information for deep troubleshooting

### Retention Policy
- **30 Days**: Balances debugging capability with storage requirements
- **Daily Rotation**: Prevents large log files, enables efficient log management
- **Automatic Cleanup**: Prevents log directory bloat over time

### Privacy Defaults
- **Sanitize User Content**: Always enabled to protect user privacy
- **Exclude Sensitive Data**: Always enabled to prevent credential exposure
- **Session ID Preservation**: Enabled for debugging correlation while protecting user identity

## Integration with Hooks

### 1. Hook Execution Logging

Each hook logs key execution events:
```
[INFO] [SessionStart] Hook execution started - session_id: abc123
[INFO] [SessionStart] Project type detected: nodejs
[INFO] [SessionStart] Mode activated: task_management
[INFO] [SessionStart] Hook execution completed - duration: 125ms
```

### 2. Decision Point Logging

Critical decisions are logged for analysis:
```
[INFO] [PreToolUse] MCP server selected: serena - confidence: 0.85
[INFO] [PreToolUse] Routing decision: multi_file_operation detected
[WARNING] [PreToolUse] Fallback activated: serena unavailable
```

### 3. Performance Logging

Timing information for optimization:
```
[INFO] [PostToolUse] Quality validation completed - duration: 45ms
[WARNING] [PreCompact] Compression exceeded target - duration: 200ms (target: 150ms)
```

### 4. Error Logging

Comprehensive error capture:
```
[ERROR] [Stop] Analytics generation failed - error: connection_timeout
[ERROR] [Stop] Fallback: basic session cleanup activated
```

## Performance Implications

### 1. Logging Overhead

#### Synchronous Logging Impact
- **Per Log Entry**: <1ms overhead (within target)
- **File I/O**: Batched writes for efficiency
- **String Processing**: Minimal formatting overhead

#### Performance Monitoring
- **Overhead Tracking**: Monitors logging performance impact
- **Threshold Alerts**: Warns when overhead exceeds 1ms target
- **Auto-Adjustment**: Can reduce logging verbosity if performance degrades

### 2. Storage Impact

#### Log File Sizes
- **Typical Session**: 50-200KB log data
- **Daily Logs**: 1-10MB depending on activity
- **Storage Growth**: ~300MB per month with 30-day retention

#### Disk I/O Impact
- **Write Operations**: Minimal impact through batching
- **Log Rotation**: Daily rotation minimizes individual file sizes
- **Cleanup**: Automatic cleanup prevents storage bloat

### 3. Memory Impact

#### Log Buffer Management
- **Buffer Size**: 10KB typical buffer size
- **Flush Strategy**: Regular flushes prevent memory buildup
- **Memory Usage**: <5MB memory overhead for logging system

## Configuration Best Practices

### 1. Production Configuration
```yaml
logging:
  enabled: true
  level: "INFO"
privacy:
  sanitize_user_content: true
  exclude_sensitive_data: true
performance:
  max_overhead_ms: 1
```

**Recommendations**:
- Use INFO level for production (balances information with performance)
- Always enable privacy protection in production
- Maintain 1ms overhead limit for performance

### 2. Development Configuration
```yaml
logging:
  level: "DEBUG"
development:
  verbose_errors: true
  debug_mode: true
privacy:
  sanitize_user_content: false  # Only for development
```

**Development Settings**:
- DEBUG level for detailed troubleshooting
- Verbose errors for comprehensive debugging
- Reduced privacy restrictions (development only)

### 3. Performance-Critical Configuration
```yaml
logging:
  level: "ERROR"
hook_logging:
  log_timing: false
performance:
  max_overhead_ms: 0.5
```

**Optimization Settings**:
- ERROR level only for minimal overhead
- Disable timing logs for performance
- Stricter overhead limits

### 4. Debugging Configuration
```yaml
logging:
  level: "DEBUG"
hook_logging:
  log_lifecycle: true
  log_decisions: true
  log_timing: true
development:
  verbose_errors: true
  include_stack_traces: true
```

**Debug Settings**:
- Maximum verbosity for troubleshooting
- All logging features enabled
- Stack traces for deep debugging

## Log File Structure

### 1. Log Entry Format
```
[TIMESTAMP] [LEVEL] [HOOK_NAME] Message - context_key: value
```

**Example**:
```
[2024-12-15T14:30:22Z] [INFO] [PreToolUse] MCP routing completed - server: serena, confidence: 0.85, duration: 125ms
```

### 2. Log Directory Structure
```
cache/logs/
├── superclaude-hooks-2024-12-15.log
├── superclaude-hooks-2024-12-14.log
├── superclaude-hooks-2024-12-13.log
└── archived/
    └── older-logs...
```

### 3. Log Rotation Management
- **Daily Files**: New log file each day
- **Automatic Cleanup**: Removes files older than retention period
- **Archive Option**: Can archive old logs instead of deletion

## Troubleshooting

### Common Logging Issues

#### No Logs Generated
- **Check**: Logging enabled in configuration
- **Verify**: Log directory permissions and existence
- **Test**: Hook execution and error handling
- **Debug**: Basic logging functionality

#### Performance Impact
- **Symptoms**: Slow hook execution, high overhead
- **Solutions**: Reduce log level, disable timing logs
- **Monitoring**: Track logging overhead metrics
- **Optimization**: Adjust performance settings

#### Log File Issues
- **Symptoms**: Missing logs, rotation problems
- **Solutions**: Check file permissions, disk space
- **Prevention**: Monitor log directory size
- **Maintenance**: Regular log cleanup

#### Privacy Concerns
- **Symptoms**: User data in logs, sensitive information exposure
- **Solutions**: Enable sanitization, review privacy settings
- **Validation**: Audit log content for sensitive data
- **Compliance**: Ensure privacy settings meet requirements

### Log Analysis

#### Performance Analysis
```bash
# Analyze hook execution times
grep "duration:" superclaude-hooks-*.log | sort -k5 -n

# Find performance outliers
grep "exceeded target" superclaude-hooks-*.log
```

#### Error Analysis
```bash
# Review error patterns
grep "ERROR" superclaude-hooks-*.log

# Analyze fallback activation frequency
grep "Fallback activated" superclaude-hooks-*.log
```

#### Effectiveness Analysis
```bash
# Monitor MCP server selection patterns
grep "MCP server selected" superclaude-hooks-*.log

# Track mode activation patterns
grep "Mode activated" superclaude-hooks-*.log
```

## Related Documentation

- **Hook Implementation**: See individual hook documentation for specific logging patterns
- **Performance Configuration**: Reference `performance.yaml.md` for performance monitoring integration
- **Privacy Guidelines**: Review framework privacy standards for logging compliance
- **Development Support**: See development configuration for debugging techniques

## Version History

- **v1.0.0**: Initial logging configuration
- Simple, performance-focused logging system
- Comprehensive privacy protection
- Hook-specific logging customization
- Development and production configuration support