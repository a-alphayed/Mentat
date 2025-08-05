# Checkpoint Triggers Configuration Schema

This document describes the schema for `checkpoint_triggers.yaml` used by the SuperClaude Session Lifecycle hook.

## File Location

```
SuperClaude/Hooks/Resources/checkpoint_triggers.yaml
```

## Schema Structure

```yaml
# Checkpoint trigger configurations
checkpoint_triggers:
  # Time-based automatic checkpoints
  time_based:
    enabled: <boolean>              # Whether time-based checkpoints are enabled
    interval_minutes: <number>      # Minutes between automatic checkpoints
    
  # Task completion based checkpoints  
  task_based:
    enabled: <boolean>              # Whether task-based checkpoints are enabled
    high_priority_only: <boolean>   # Only trigger on high priority tasks
    
  # Risk-based checkpoints for major operations
  risk_based:
    enabled: <boolean>              # Whether risk-based checkpoints are enabled
    major_operations: <list>        # List of operations that trigger checkpoints
    file_threshold: <integer>       # Number of files for major refactoring
    
  # Error recovery checkpoints
  error_recovery:
    enabled: <boolean>              # Whether error recovery checkpoints are enabled
    auto_checkpoint: <boolean>      # Automatically checkpoint after errors

# Memory key patterns for checkpoint storage
memory_key_patterns:
  time_based: <string>             # Pattern for time-based checkpoint keys
  task_based: <string>             # Pattern for task-based checkpoint keys
  risk_based: <string>             # Pattern for risk-based checkpoint keys
  error_recovery: <string>         # Pattern for error recovery checkpoint keys
  manual: <string>                 # Pattern for manual checkpoint keys
```

## Field Descriptions

### checkpoint_triggers

Configuration for automatic checkpoint triggers based on SESSION_LIFECYCLE.md specifications.

#### time_based

Triggers checkpoints at regular time intervals during active work sessions.

| Field | Description | Default | Valid Range |
|-------|-------------|---------|-------------|
| `enabled` | Enable time-based checkpoints | true | true/false |
| `interval_minutes` | Minutes between checkpoints | 30 | 1-1440 (1 min to 24 hours) |

#### task_based

Triggers checkpoints when tasks are completed, particularly high-priority tasks.

| Field | Description | Default | Valid Range |
|-------|-------------|---------|-------------|
| `enabled` | Enable task-based checkpoints | true | true/false |
| `high_priority_only` | Only checkpoint on high priority tasks | true | true/false |

#### risk_based

Triggers checkpoints before high-risk operations to enable recovery if needed.

| Field | Description | Default | Valid Range |
|-------|-------------|---------|-------------|
| `enabled` | Enable risk-based checkpoints | true | true/false |
| `major_operations` | Operations that trigger checkpoints | ["Write", "Edit", "MultiEdit", "Delete"] | List of tool names |
| `file_threshold` | File count for major refactoring | 50 | 1-1000 |

#### error_recovery

Triggers checkpoints after errors to preserve error context and recovery steps.

| Field | Description | Default | Valid Range |
|-------|-------------|---------|-------------|
| `enabled` | Enable error recovery checkpoints | true | true/false |
| `auto_checkpoint` | Auto-checkpoint after errors | true | true/false |

### memory_key_patterns

Patterns for generating memory keys when storing checkpoints. Uses placeholders:
- `{timestamp}`: ISO format timestamp
- `{task_id}`: Task identifier
- `{operation}`: Operation name
- `{session_id}`: Session identifier

| Field | Description | Default Pattern |
|-------|-------------|-----------------|
| `time_based` | Time-based checkpoint keys | `checkpoints/auto-{timestamp}` |
| `task_based` | Task completion checkpoint keys | `checkpoints/task-{task_id}-{timestamp}` |
| `risk_based` | Risk operation checkpoint keys | `checkpoints/risk-{operation}-{timestamp}` |
| `error_recovery` | Error recovery checkpoint keys | `checkpoints/recovery-{timestamp}` |
| `manual` | Manual checkpoint keys | `checkpoints/manual-{timestamp}` |

## Validation Rules

1. **Boolean Fields**: Converted to boolean type
2. **Numeric Fields**: 
   - `interval_minutes`: Must be 1-1440 (validated as float)
   - `file_threshold`: Must be 1-1000 (validated as integer)
3. **List Fields**:
   - `major_operations`: Filtered to valid string entries only
4. **Invalid Values**: Fall back to defaults with warning logs

## Example Configurations

### Default Configuration
```yaml
checkpoint_triggers:
  time_based:
    enabled: true
    interval_minutes: 30
    
  task_based:
    enabled: true
    high_priority_only: true
    
  risk_based:
    enabled: true
    major_operations:
      - Write
      - Edit
      - MultiEdit
      - Delete
    file_threshold: 50
    
  error_recovery:
    enabled: true
    auto_checkpoint: true
```

### Aggressive Checkpointing
```yaml
checkpoint_triggers:
  time_based:
    enabled: true
    interval_minutes: 15    # More frequent time-based checkpoints
    
  task_based:
    enabled: true
    high_priority_only: false  # Checkpoint on all task completions
    
  risk_based:
    enabled: true
    major_operations:
      - Write
      - Edit
      - MultiEdit
      - Delete
      - Bash          # Add shell commands as risky
    file_threshold: 20  # Lower threshold for major operations
```

### Minimal Checkpointing
```yaml
checkpoint_triggers:
  time_based:
    enabled: true
    interval_minutes: 60    # Less frequent checkpoints
    
  task_based:
    enabled: false          # Disable task-based checkpoints
    
  risk_based:
    enabled: true
    major_operations:
      - Delete              # Only most dangerous operations
    file_threshold: 100     # Higher threshold
    
  error_recovery:
    enabled: true
    auto_checkpoint: true
```

## Integration with Session Lifecycle

The Session Lifecycle hook uses this configuration to:

1. **Monitor Sessions**: Track active work sessions and time elapsed
2. **Detect Triggers**: Check configured conditions during PostToolUse events
3. **Generate Suggestions**: Create checkpoint recommendations to stderr
4. **Execute Checkpoints**: User can run suggested `/sc:save --checkpoint` commands
5. **Track State**: Update checkpoint counters and timestamps

## Loading Behavior

1. **File Missing**: Uses hardcoded defaults based on SESSION_LIFECYCLE.md
2. **YAML Parse Error**: Uses defaults with error log
3. **Invalid Values**: Uses defaults for invalid fields with warning log
4. **PyYAML Missing**: Uses all hardcoded defaults with warning

## Best Practices

1. **Balance Frequency**: Too many checkpoints create overhead, too few risk data loss
2. **Monitor Performance**: Check checkpoint creation time (<1s target)
3. **Review Triggers**: Adjust based on your workflow and risk tolerance
4. **Test Recovery**: Verify checkpoints can be restored successfully
5. **Clean Old Checkpoints**: Implement retention policy (default: 90 days)

## Related Documentation

- **SESSION_LIFECYCLE.md**: Architectural documentation for session management
- **performance_targets.yaml**: Performance targets for checkpoint operations
- **performance_targets_schema.md**: Schema for performance configuration