# Configuration Guide

Framework-Hooks uses YAML configuration files to control hook behavior, performance targets, and system features. This guide covers the essential configuration options for customizing the system.

## Configuration Files Overview

The `config/` directory contains 12+ YAML files that control different aspects of the hook system:

```
config/
├── session.yaml           # Session lifecycle settings
├── performance.yaml       # Performance targets and limits
├── compression.yaml       # Context compression settings
├── modes.yaml            # Mode activation thresholds
├── mcp_orchestration.yaml # MCP server coordination
├── orchestrator.yaml     # General orchestration settings
├── logging.yaml          # Logging configuration
├── validation.yaml       # System validation rules
└── [other specialized configs]
```

## Essential Configuration Files

### logging.yaml - System Logging

Controls logging behavior and output:

```yaml
# Core Logging Settings
logging:
  enabled: false           # Default: disabled for performance
  level: "ERROR"          # ERROR, WARNING, INFO, DEBUG
  
  file_settings:
    log_directory: "cache/logs"
    retention_days: 30
    rotation_strategy: "daily"
    
  hook_logging:
    log_lifecycle: false    # Log hook start/end events
    log_decisions: false    # Log decision points  
    log_errors: false       # Log error events
    log_timing: false       # Include timing information
    
  performance:
    max_overhead_ms: 1      # Maximum logging overhead
    async_logging: false    # Keep simple for now
    
  privacy:
    sanitize_user_content: true
    exclude_sensitive_data: true
    anonymize_session_ids: false
```

**Common customizations:**
```yaml
# Enable basic logging
logging:
  enabled: true
  level: "INFO"

# Enable debugging  
logging:
  enabled: true
  level: "DEBUG"
  hook_logging:
    log_lifecycle: true
    log_decisions: true
    log_timing: true
    
development:
  verbose_errors: true
  include_stack_traces: true
  debug_mode: true
```

### performance.yaml - Performance Targets

Defines execution time targets for each hook:

```yaml
performance_targets:
  session_start: 50        # ms - Session initialization
  pre_tool_use: 200       # ms - Tool preparation  
  post_tool_use: 100      # ms - Tool usage recording
  pre_compact: 150        # ms - Context compression
  notification: 50        # ms - Notification handling
  stop: 100              # ms - Session cleanup
  subagent_stop: 100     # ms - Subagent coordination

# Pattern loading performance
pattern_loading:
  minimal_patterns: 100   # ms - Basic patterns (3-5KB each)
  dynamic_patterns: 200   # ms - Feature patterns (8-12KB each)
  learned_patterns: 300   # ms - User patterns (10-20KB each)
  
# Cache operation limits  
cache_operations:
  read_timeout: 10        # ms
  write_timeout: 50       # ms
  
# Timeouts (from settings.json)
hook_timeouts:
  default: 10             # seconds
  extended: 15            # seconds (pre_tool_use, pre_compact, etc.)
```

### session.yaml - Session Management

Controls session lifecycle behavior:

```yaml
session_lifecycle:
  initialization:
    load_minimal_patterns: true
    enable_project_detection: true
    activate_learning_engine: true
    
  context_management:
    preserve_user_content: true
    compress_framework_content: false    # Keep framework content uncompressed
    apply_selective_compression: true
    
  cleanup:
    save_learning_data: true
    persist_adaptations: true
    cleanup_temp_files: true
```

### compression.yaml - Context Compression

Controls how the compression engine handles content:

```yaml
compression_settings:
  enabled: true
  
  # Content classification for selective compression
  content_types:
    framework_content: 
      compression_level: 0              # No compression for SuperClaude framework
      exclusion_patterns:
        - "/SuperClaude/"
        - "~/.claude/"
        - ".claude/"
        - "framework_*"
        
    session_data:
      compression_level: 0.4            # 40% compression for session operational data
      apply_to:
        - "session_metadata"
        - "checkpoint_data"  
        - "cache_content"
        
    user_content:
      compression_level: 0              # No compression for user content
      preserve_patterns:
        - "project_files"
        - "user_documentation"
        - "source_code"
        - "configuration_*"
        
  compression_levels:
    minimal: 0.40      # 40% compression
    efficient: 0.70    # 70% compression
    compressed: 0.85   # 85% compression
    critical: 0.95     # 95% compression
    
  quality_targets:
    preservation_minimum: 0.95          # 95% information preservation required
    processing_time_limit: 100          # ms
```

## Hook-Specific Configuration

Each hook can be configured individually. The general pattern is:

### Hook Enable/Disable

In `logging.yaml`:
```yaml
hook_configuration:
  pre_tool_use:
    enabled: true                        # Hook enabled/disabled
    log_tool_selection: true
    log_input_validation: true
    
  post_tool_use:
    enabled: true
    log_output_processing: true
    log_integration_success: true
    
  # Similar blocks for other hooks
```

### MCP Server Coordination

In `mcp_orchestration.yaml`:
```yaml
mcp_servers:
  context7:
    enabled: true
    auto_activation_patterns:
      - "external library imports"
      - "framework-specific questions" 
      
  sequential:
    enabled: true
    auto_activation_patterns:
      - "complex debugging scenarios"
      - "system design questions"
      
  magic:
    enabled: true  
    auto_activation_patterns:
      - "UI component requests"
      - "design system queries"
      
  # Configuration for other MCP servers
```

## Pattern System Configuration

The 3-tier pattern system can be customized:

### Pattern Loading

```yaml
# In session.yaml or dedicated pattern config
pattern_system:
  minimal_patterns:
    always_load: true
    size_limit_kb: 5
    
  dynamic_patterns:  
    load_on_demand: true
    size_limit_kb: 12
    
  learned_patterns:
    adaptation_enabled: true
    size_limit_kb: 20
    evolution_threshold: 0.8
```

### Project Detection Patterns

Add custom patterns in `patterns/minimal/` directories following existing YAML structure:

```yaml
# Example: patterns/minimal/custom-project.yaml
pattern_type: "project_detection"
name: "custom_project"
triggers:
  - "specific-file-pattern"
  - "directory-structure"
features_to_activate:
  - "custom_mode"
  - "specific_mcp_servers"
```

## Advanced Configuration

### Learning Engine Tuning

```yaml
# In learning configuration
learning_engine:
  adaptation_settings:
    learning_rate: 0.1
    adaptation_threshold: 0.75
    persistence_enabled: true
    
  data_retention:
    session_history_days: 90
    pattern_evolution_days: 30
    cache_cleanup_interval: 7
```

### Validation Rules

```yaml  
# In validation.yaml
validation_rules:
  hook_performance:
    enforce_timing_targets: true
    alert_on_timeout: true
    
  configuration_integrity:
    yaml_syntax_check: true
    required_fields_check: true
    
  system_health:
    file_permissions_check: true
    directory_structure_check: true
```

## Environment-Specific Configuration

### Development Environment

```yaml
# Enable verbose logging and debugging
logging:
  enabled: true
  level: "DEBUG"
  
development:
  verbose_errors: true
  include_stack_traces: true
  debug_mode: true
  
performance_targets:
  # Relaxed targets for development
  session_start: 100
  pre_tool_use: 500
```

### Production Environment  

```yaml
# Minimal logging, strict performance
logging:
  enabled: false
  level: "ERROR"
  
performance_targets:
  # Strict targets for production
  session_start: 30
  pre_tool_use: 150
  
compression_settings:
  # Aggressive optimization
  enabled: true
  default_level: "efficient"
```

## Configuration Validation

### Manual Validation

Test configuration changes:

```bash
cd Framework-Hooks/hooks/shared
python3 validate_system.py --check-config
```

### YAML Syntax Check

```bash
python3 -c "
import yaml
import glob
for file in glob.glob('config/*.yaml'):
    try:
        yaml.safe_load(open(file))
        print(f'{file}: OK')
    except Exception as e:
        print(f'{file}: ERROR - {e}')
"
```

## Configuration Best Practices

### Performance Optimization
1. **Keep logging disabled** in production for best performance
2. **Set realistic timing targets** based on your hardware
3. **Enable selective compression** to balance performance and quality
4. **Tune pattern loading** based on project complexity

### Debugging and Development
1. **Enable comprehensive logging** during development
2. **Use debug mode** for detailed error information  
3. **Test configuration changes** with validation tools
4. **Monitor hook performance** against targets

### Customization Guidelines
1. **Back up configurations** before making changes
2. **Test changes incrementally** rather than bulk modifications
3. **Use validation tools** to verify configuration integrity
4. **Document custom patterns** for team collaboration

## Configuration Troubleshooting

### Common Issues

**YAML Syntax Errors**: Use Python YAML validation or online checkers
**Performance Degradation**: Review enabled features and logging verbosity  
**Hook Failures**: Check required configuration fields are present
**Pattern Loading Issues**: Verify pattern file sizes and structure

### Reset to Defaults

```bash
# Reset all configurations (backup first!)
git checkout config/*.yaml
# Or restore from installation backup
```

The configuration system provides extensive customization while maintaining sensible defaults for immediate usability.