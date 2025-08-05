# Performance Targets Configuration Schema

This document describes the schema for `performance_targets.yaml` used by the SuperClaude Performance Monitor hook.

## File Location

```
SuperClaude/Hooks/Resources/performance_targets.yaml
```

## Schema Structure

```yaml
# Performance targets in milliseconds for various operations
performance_targets:
  memory_operations: <integer>        # Target for Serena MCP operations
  project_loading: <integer>          # Target for /sc:load command
  session_save: <integer>             # Target for /sc:save command
  session_restore: <integer>          # Target for session restoration
  tool_selection: <integer>           # Target for tool selection logic
  checkpoint_creation: <integer>      # Target for checkpoint creation
  context_loading: <integer>          # Target for context loading operations
  reflection_operations: <integer>    # Target for /sc:reflect command
  general_operations: <integer>       # Default target for unclassified operations

# Alert thresholds as multipliers of target values
alert_thresholds:
  warning: <float>    # Multiplier for warning threshold (e.g., 0.8 = 80% of target)
  critical: <float>   # Multiplier for critical threshold (e.g., 1.5 = 150% of target)

# Resource usage limits for the monitoring system itself
resource_limits:
  monitoring_overhead_cpu_percent: <float>  # Max CPU % for monitoring
  monitoring_memory_mb: <integer>           # Max memory MB for monitoring
```

## Field Descriptions

### performance_targets

All values are positive integers representing milliseconds.

| Field | Description | Default | Valid Range |
|-------|-------------|---------|-------------|
| `memory_operations` | Serena MCP read/write/list operations | 200ms | 1-10000 |
| `project_loading` | `/sc:load` project activation | 500ms | 1-30000 |
| `session_save` | `/sc:save` session persistence | 2000ms | 1-60000 |
| `session_restore` | Session state restoration | 500ms | 1-30000 |
| `tool_selection` | Intelligent tool selection | 100ms | 1-5000 |
| `checkpoint_creation` | Checkpoint creation | 1000ms | 1-30000 |
| `context_loading` | Context restoration | 500ms | 1-30000 |
| `reflection_operations` | `/sc:reflect` analysis | 5000ms | 1-120000 |
| `general_operations` | Default for unclassified ops | 2000ms | 1-60000 |

### alert_thresholds

Float values representing multipliers of the target values.

| Field | Description | Default | Valid Range |
|-------|-------------|---------|-------------|
| `warning` | Threshold for warning alerts | 0.8 | 0.1-10.0 |
| `critical` | Threshold for critical alerts | 1.5 | 0.1-10.0 |

Example: If `memory_operations` target is 200ms and `warning` is 0.8:
- Warning triggered at: 200ms × 0.8 = 160ms
- Critical triggered at: 200ms × 1.5 = 300ms

### resource_limits

Limits for the monitoring system's own resource usage.

| Field | Description | Default | Valid Range |
|-------|-------------|---------|-------------|
| `monitoring_overhead_cpu_percent` | Max CPU usage for monitoring | 2.0 | 0.1-100.0 |
| `monitoring_memory_mb` | Max memory for monitoring data | 50 | 1-1000 |

## Validation Rules

1. **Required Sections**: None - all sections are optional with defaults
2. **Type Validation**:
   - `performance_targets`: All values must be positive integers
   - `alert_thresholds`: All values must be positive floats ≤ 10.0
   - `resource_limits`: 
     - CPU: Float between 0.1-100.0
     - Memory: Positive integer
3. **Unknown Keys**: Logged as warnings but ignored
4. **Invalid Values**: Fall back to defaults with warning logs

## Example Configuration

```yaml
# Optimized for fast local development
performance_targets:
  memory_operations: 150
  project_loading: 400
  session_save: 1500
  tool_selection: 80
  general_operations: 1500

alert_thresholds:
  warning: 0.7   # More aggressive warning at 70%
  critical: 1.3  # Critical at 130%

resource_limits:
  monitoring_overhead_cpu_percent: 1.5
  monitoring_memory_mb: 40
```

## Loading Behavior

1. **File Missing**: Uses hardcoded defaults with warning log
2. **YAML Parse Error**: Uses hardcoded defaults with error log
3. **Invalid Values**: Uses defaults for invalid fields with warning log
4. **PyYAML Missing**: Uses all hardcoded defaults with warning

## Integration with Performance Monitor

The Performance Monitor hook loads this configuration during initialization:

```python
# Loads from: SuperClaude/Hooks/Resources/performance_targets.yaml
# Validates all values
# Applies defaults for missing/invalid entries
# Logs any issues to stderr
```

## Monitoring Usage

The loaded targets are used to:
- Classify operation performance (good/warning/critical)
- Generate optimization suggestions
- Track performance trends
- Trigger alerts when thresholds exceeded

Resource limits are used to:
- Monitor the monitoring system's own overhead
- Ensure monitoring doesn't impact system performance
- Provide self-regulation capabilities

## Best Practices

1. **Tune for Your Environment**: Adjust targets based on your hardware
2. **Monitor Trends**: Use metrics.jsonl to analyze patterns before adjusting
3. **Start Conservative**: Begin with higher targets and lower gradually
4. **Document Changes**: Comment your YAML with reasons for custom values
5. **Test Changes**: Verify new targets don't cause excessive warnings