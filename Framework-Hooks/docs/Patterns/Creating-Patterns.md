# Creating Patterns: Developer Guide

## Overview

This guide explains how to create new patterns for the Framework-Hooks pattern system. Patterns are YAML files that define automatic behavior, MCP server activation, and optimization rules for different contexts.

## Pattern Development Process

1. **Identify the Need**: Determine what behavior should be automated
2. **Choose Pattern Type**: Select minimal, dynamic, or learned pattern
3. **Define Structure**: Create YAML structure following the schema
4. **Test Pattern**: Verify the pattern works correctly
5. **Document Pattern**: Add appropriate documentation

## Creating Minimal Patterns

Minimal patterns detect project types and configure initial MCP server activation.

### Minimal Pattern Template

```yaml
# File: /patterns/minimal/{project_type}_project.yaml

project_type: "unique_identifier"          # e.g., "python", "react", "vue"
detection_patterns:                        # File/directory existence patterns
  - "*.{ext} files present"               # File extension patterns
  - "{manifest_file} dependency"          # Dependency manifest detection
  - "{directory}/ directories"            # Directory structure patterns

auto_flags:                               # Automatic flag activation
  - "--{primary_server}"                  # Primary server flag
  - "--{secondary_server}"                # Secondary server flag

mcp_servers:
  primary: "{server_name}"                # Primary MCP server
  secondary: ["{server1}", "{server2}"]   # Fallback servers

patterns:
  file_structure:                         # Expected project structure
    - "{directory}/"                      # Key directories
    - "{file_pattern}"                    # Important files
  common_tasks:                           # Typical operations
    - "{task_description}"                # Task patterns

intelligence:
  mode_triggers:                          # Mode activation patterns
    - "{mode_name}: {trigger_condition}"
  validation_focus:                       # Quality validation priorities
    - "{validation_type}"

performance_targets:
  bootstrap_ms: {target_milliseconds}     # Bootstrap time target
  context_size: "{size}KB"               # Context footprint
  cache_duration: "{duration}min"        # Cache retention time
```

### Example: Vue.js Project Pattern

```yaml
project_type: "vue"
detection_patterns:
  - "package.json with vue dependency"
  - "src/ directory with .vue files"
  - "vue.config.js or vite.config.js"

auto_flags:
  - "--magic"     # Vue component generation
  - "--context7"  # Vue documentation

mcp_servers:
  primary: "magic"
  secondary: ["context7", "morphllm"]

patterns:
  file_structure:
    - "src/components/"
    - "src/views/"
    - "src/composables/"
    - "src/stores/"
  common_tasks:
    - "component development"
    - "composable creation"
    - "store management"
    - "routing configuration"

intelligence:
  mode_triggers:
    - "task_management: component|view|composable"
    - "token_efficiency: context >75%"
  validation_focus:
    - "vue_syntax"
    - "composition_api"
    - "reactivity_patterns"
    - "performance"

performance_targets:
  bootstrap_ms: 32
  context_size: "3.2KB"
  cache_duration: "55min"
## Creating Dynamic Patterns

Dynamic patterns define runtime activation rules for modes and MCP servers.

### Dynamic Pattern Structure

```yaml
# For mode detection patterns
mode_detection:
  {mode_name}:
    triggers:
      - "trigger description"
    patterns:
      - "keyword or phrase"
    confidence_threshold: 0.7
    activation_hooks: ["session_start", "pre_tool_use"]
    coordination:
      command: "/sc:command"
      mcp_servers: ["server1", "server2"]

# For MCP activation patterns  
activation_patterns:
  {server_name}:
    triggers:
      - "activation trigger"
    context_keywords:
      - "keyword"
    activation_confidence: 0.8

coordination_patterns:
  hybrid_intelligence:
    {server1}_{server2}:
      condition: "coordination condition"
      strategy: "coordination strategy"
      confidence_threshold: 0.8

performance_optimization:
  cache_activation_decisions: true
  cache_duration_minutes: 15
  batch_similar_requests: true
  lazy_loading: true
```

## Creating Learned Patterns

Learned patterns track usage data and adapt behavior over time.

### Learned Pattern Structure

```yaml
# For user preferences
user_profile:
  id: "user_identifier"
  created: "2025-01-31"
  last_updated: "2025-01-31" 
  sessions_analyzed: 0

learned_preferences:
  communication_style:
    verbosity_preference: "balanced"
    technical_depth: "high"
    symbol_usage_comfort: "high"
    
  workflow_patterns:
    preferred_thinking_mode: "--think-hard"
    mcp_server_preferences:
      - "serena"
      - "sequential"
    mode_activation_frequency:
      task_management: 0.8
      token_efficiency: 0.6

# For project optimizations  
project_profile:
  id: "project_identifier"
  type: "project_type"
  created: "2025-01-31"
  optimization_cycles: 0

learned_optimizations:
  workflow_optimizations:
    effective_sequences:
      - sequence: ["Read", "Edit", "Validate"]
        success_rate: 0.95
        context: "documentation updates"
  
  mcp_server_effectiveness:
    serena:
      effectiveness: 0.9
      optimal_contexts:
        - "framework analysis"
      performance_notes: "excellent for project context"
```

## Best Practices

### Pattern Design Guidelines

1. **Be Specific**: Use unique identifiers and clear detection criteria
2. **Set Appropriate Thresholds**: Match confidence thresholds to resource impact
3. **Include Fallbacks**: Define secondary servers and graceful degradation
4. **Document Rationale**: Explain why specific servers or settings were chosen
5. **Test Thoroughly**: Verify patterns work in different scenarios

### Performance Considerations

1. **Keep Minimal Patterns Small**: Aim for fast loading and low memory usage
2. **Set Realistic Targets**: Bootstrap times should be achievable
3. **Cache Wisely**: Set appropriate cache durations for stability
4. **Monitor Effectiveness**: Track pattern performance over time

### Integration Testing

1. **Hook Integration**: Verify patterns work with Framework-Hooks lifecycle
2. **MCP Coordination**: Test server activation and coordination rules
3. **Mode Transitions**: Ensure smooth transitions between modes
4. **Error Handling**: Test graceful degradation when servers unavailable

Pattern creation requires understanding the specific use case, careful design of activation rules, and thorough testing to ensure reliable operation within the Framework-Hooks system.
