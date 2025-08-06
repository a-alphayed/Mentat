# Learned Patterns: Adaptive Behavior Learning

## Overview

Learned patterns store adaptive behaviors that evolve based on project usage and user preferences. These patterns are stored in `/patterns/learned/` and track effectiveness, optimizations, and personalization data to improve Framework-Hooks behavior over time.

## Purpose

Learned patterns handle:

- **Project Optimizations**: Track effective workflows and performance improvements for specific projects
- **User Preferences**: Learn individual user behavior patterns and communication styles
- **Performance Metrics**: Monitor effectiveness of different MCP servers and coordination strategies
- **Error Prevention**: Learn from past issues to prevent recurring problems

## Current Learned Patterns

### User Preferences Pattern (`user_preferences.yaml`)

This pattern tracks individual user behavior and preferences:

```yaml
user_profile:
  id: "example_user"
  created: "2025-01-31"
  last_updated: "2025-01-31"
  sessions_analyzed: 0
  
learned_preferences:
  communication_style:
    verbosity_preference: "balanced"  # minimal, balanced, detailed
    technical_depth: "high"  # low, medium, high
    symbol_usage_comfort: "high"  # low, medium, high
    abbreviation_tolerance: "medium"  # low, medium, high
    
  workflow_patterns:
    preferred_thinking_mode: "--think-hard"
    mcp_server_preferences:
      - "serena"  # Most frequently beneficial
      - "sequential"  # High success rate
      - "context7"  # Frequently requested
    mode_activation_frequency:
      task_management: 0.8  # High usage
      token_efficiency: 0.6  # Medium usage
      brainstorming: 0.3  # Low usage
      introspection: 0.4  # Medium usage
      
  project_type_expertise:
    python: 0.9  # High proficiency
    react: 0.7  # Good proficiency
    javascript: 0.8  # High proficiency
    documentation: 0.6  # Medium proficiency
    
  performance_preferences:
    speed_vs_quality: "quality_focused"  # speed_focused, balanced, quality_focused
    compression_tolerance: 0.7  # How much compression user accepts
    context_size_preference: "medium"  # small, medium, large

learning_insights:
  effective_patterns:
    - pattern: "serena + morphllm hybrid"
      success_rate: 0.92
      context: "large refactoring tasks"
      
    - pattern: "sequential + context7"
      success_rate: 0.88
      context: "complex debugging"
      
    - pattern: "magic + context7"
      success_rate: 0.85
      context: "UI component creation"

adaptive_thresholds:
  mode_activation:
    brainstorming: 0.6  # Lowered from 0.7 due to user preference
    task_management: 0.9  # Raised from 0.8 due to frequent use
    token_efficiency: 0.65  # Adjusted based on tolerance
    introspection: 0.5  # Lowered due to user comfort with meta-analysis
### Project Optimizations Pattern (`project_optimizations.yaml`)

This pattern tracks project-specific performance and optimization data:

```yaml
project_profile:
  id: "superclaude_framework"
  type: "python_framework"
  created: "2025-01-31"
  last_analyzed: "2025-01-31"
  optimization_cycles: 0

learned_optimizations:
  file_patterns:
    high_frequency_files:
      patterns:
        - "commands/*.md" 
        - "Core/*.md"
        - "Modes/*.md"
        - "MCP/*.md"
      frequency_weight: 0.9
      cache_priority: "high"
      
    structural_patterns:
      patterns:
        - "markdown documentation with YAML frontmatter"
        - "python scripts with comprehensive docstrings"
        - "modular architecture with clear separation"
      optimization: "maintain full context for these patterns"
      
  workflow_optimizations:
    effective_sequences:
      - sequence: ["Read", "Edit", "Validate"]
        success_rate: 0.95
        context: "documentation updates"
        
      - sequence: ["Glob", "Read", "MultiEdit"]
        success_rate: 0.88
        context: "multi-file refactoring"
        
      - sequence: ["Serena analyze", "Morphllm execute"]
        success_rate: 0.92
        context: "large codebase changes"
        
  mcp_server_effectiveness:
    serena:
      effectiveness: 0.9
      optimal_contexts:
        - "framework documentation analysis"
        - "cross-file relationship mapping"
        - "memory-driven development"
      performance_notes: "excellent for project context"
      
    sequential:
      effectiveness: 0.85
      optimal_contexts:
        - "complex architectural decisions"
        - "multi-step problem solving"
        - "systematic analysis"
      performance_notes: "valuable for thinking-intensive tasks"
      
    morphllm:
      effectiveness: 0.8
      optimal_contexts:
        - "pattern-based editing"
        - "documentation updates"
        - "style consistency"
      performance_notes: "efficient for text transformations"

performance_insights:
  bottleneck_identification:
    - area: "large markdown file processing"
      impact: "medium"
      optimization: "selective reading with targeted edits"
      
    - area: "cross-file reference validation"
      impact: "low"
      optimization: "cached reference mapping"
      
  acceleration_opportunities:
    - opportunity: "pattern-based file detection"
      potential_improvement: "40% faster file processing"
      implementation: "regex pre-filtering"
      
    - opportunity: "intelligent caching"
      potential_improvement: "60% faster repeated operations"
      implementation: "content-aware cache keys"
## Learning Process

Learned patterns evolve through:

1. **Data Collection**: Track user interactions, tool effectiveness, and performance metrics
2. **Pattern Analysis**: Identify successful workflows and optimization opportunities  
3. **Threshold Adjustment**: Adapt confidence thresholds based on user behavior
4. **Performance Tracking**: Monitor the effectiveness of different strategies
5. **Cross-Session Persistence**: Maintain learning across multiple work sessions

## Integration Notes

Learned patterns integrate with Framework-Hooks through:

- **Adaptive Thresholds**: Modify activation thresholds based on learned preferences
- **Server Selection**: Prioritize MCP servers based on measured effectiveness
- **Workflow Optimization**: Apply learned effective sequences to new tasks
- **Performance Monitoring**: Track and optimize based on measured performance

The learned patterns provide a feedback mechanism that allows Framework-Hooks to improve its behavior based on actual usage patterns and results.