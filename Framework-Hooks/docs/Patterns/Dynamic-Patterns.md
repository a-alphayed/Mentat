# Dynamic Patterns: Runtime Mode Detection and MCP Activation

## Overview

Dynamic patterns provide runtime mode detection and MCP server activation based on user context and requests. These patterns are stored in `/patterns/dynamic/` and use confidence thresholds to determine when to activate specific modes or MCP servers during operation.

## Purpose

Dynamic patterns handle:

- **Mode Detection**: Detect when to activate behavioral modes (brainstorming, task management, etc.)
- **MCP Server Activation**: Determine which MCP servers to activate based on context
- **Confidence Thresholds**: Use probability scores to make activation decisions
- **Coordination Rules**: Define how multiple servers or modes work together

## Pattern Structure

Dynamic patterns use confidence-based activation with trigger patterns and context analysis.

## Current Dynamic Patterns

### Mode Detection Pattern (`mode_detection.yaml`)

This pattern defines how different behavioral modes are detected and activated:

```yaml
mode_detection:
  brainstorming:
    triggers:
      - "vague project requests"
      - "exploration keywords" 
      - "uncertainty indicators"
      - "new project discussions"
    patterns:
      - "I want to build"
      - "thinking about"
      - "not sure"
      - "explore"
      - "brainstorm"
      - "figure out"
    confidence_threshold: 0.7
    activation_hooks: ["session_start", "pre_tool_use"]
    coordination:
      command: "/sc:brainstorm"
      mcp_servers: ["sequential", "context7"]
      
  task_management:
    triggers:
      - "multi-step operations"
      - "build/implement keywords"
      - "system-wide scope"
      - "delegation indicators"
    patterns:
      - "build"
      - "implement"
      - "create"
      - "system"
      - "comprehensive"
      - "multiple files"
    confidence_threshold: 0.8
    activation_hooks: ["pre_tool_use", "subagent_stop"]
    coordination:
      wave_orchestration: true
      delegation_patterns: true
```

The pattern includes similar configurations for `token_efficiency` (threshold 0.75) and `introspection` (threshold 0.6) modes.

### MCP Activation Pattern (`mcp_activation.yaml`)

This pattern defines how MCP servers are activated based on context and user requests:

```yaml
activation_patterns:
  context7:
    triggers:
      - "import statements from external libraries"
      - "framework-specific questions"
      - "documentation requests"
      - "best practices queries"
    context_keywords:
      - "how to use"
      - "documentation"
      - "examples"
      - "patterns"
    activation_confidence: 0.8
    
  sequential:
    triggers:
      - "complex debugging scenarios"
      - "multi-step analysis requests"
      - "--think flags detected"
      - "system design questions"
    context_keywords:
      - "analyze"
      - "debug"
      - "complex"
      - "system"
      - "architecture"
    activation_confidence: 0.85
    
  magic:
    triggers:
      - "UI component requests"
      - "design system queries"
      - "frontend development"
      - "component keywords"
    context_keywords:
      - "component"
      - "UI"
      - "frontend"
      - "design"
      - "interface"
    activation_confidence: 0.9
    
  serena:
    triggers:
      - "semantic analysis"
      - "project-wide operations"
      - "symbol navigation"
      - "memory management"
    context_keywords:
      - "analyze"
      - "project"
      - "semantic"
      - "memory"
      - "context"
    activation_confidence: 0.75

coordination_patterns:
  hybrid_intelligence:
    serena_morphllm:
      condition: "complex editing with semantic understanding"
      strategy: "serena analyzes, morphllm executes"
      confidence_threshold: 0.8
      
  multi_server_activation:
    max_concurrent: 3
    priority_order:
      - "serena"
      - "sequential" 
      - "context7"
      - "magic"
      - "morphllm"
      - "playwright"

performance_optimization:
  cache_activation_decisions: true
  cache_duration_minutes: 15
  batch_similar_requests: true
  lazy_loading: true
```

## Confidence Thresholds

Dynamic patterns use confidence scores to determine activation:

- **Higher Thresholds (0.8-0.9)**: Used for resource-intensive operations (task management, magic)
- **Medium Thresholds (0.7-0.8)**: Used for standard operations (brainstorming, context7)
- **Lower Thresholds (0.6-0.75)**: Used for lightweight operations (introspection, serena)

## Coordination Patterns

The `mcp_activation.yaml` pattern includes coordination rules for:

- **Hybrid Intelligence**: Coordinated server usage (e.g., serena analyzes, morphllm executes)
- **Multi-Server Limits**: Maximum 3 concurrent servers to manage resources
- **Priority Ordering**: Server activation priority when multiple servers are relevant
- **Performance Optimization**: Caching, batching, and lazy loading strategies

## Hook Integration

Dynamic patterns integrate with Framework-Hooks at these points:

- **pre_tool_use**: Analyze user input for mode and server activation
- **session_start**: Apply initial context-based activations
- **post_tool_use**: Update activation patterns based on results
- **subagent_stop**: Re-evaluate activation patterns after sub-agent operations

## Creating Dynamic Patterns

To create new dynamic patterns:

1. **Define Triggers**: Identify the conditions that should activate the pattern
2. **Set Keywords**: Define specific words or phrases that indicate activation
3. **Choose Thresholds**: Set confidence thresholds appropriate for the operation's resource cost
4. **Specify Coordination**: Define how the pattern works with other systems
5. **Add Performance Rules**: Configure caching and optimization strategies

Dynamic patterns provide flexible, context-aware activation of Framework-Hooks features without requiring code changes.

