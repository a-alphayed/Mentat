# Modes Configuration (`modes.yaml`)

## Overview

The `modes.yaml` file defines behavioral mode configurations for the SuperClaude-Lite framework. This configuration controls mode detection patterns, activation thresholds, coordination strategies, and integration patterns for all four SuperClaude behavioral modes.

## Purpose and Role

The modes configuration serves as:
- **Mode Detection Engine**: Defines trigger patterns and confidence thresholds for automatic mode activation
- **Behavioral Configuration**: Specifies mode-specific settings and coordination patterns
- **Integration Orchestration**: Manages mode coordination with hooks, MCP servers, and commands
- **Performance Optimization**: Configures performance profiles and resource management for each mode
- **Learning Integration**: Enables mode effectiveness tracking and adaptive optimization

## Configuration Structure

### 1. Mode Detection Patterns (`mode_detection`)

#### Brainstorming Mode
```yaml
brainstorming:
  description: "Interactive requirements discovery and exploration"
  activation_type: "automatic"
  confidence_threshold: 0.7
  
  trigger_patterns:
    vague_requests:
      - "i want to build"
      - "thinking about"
      - "not sure"
      - "maybe we could"
      - "what if we"
      - "considering"
    
    exploration_keywords:
      - "brainstorm"
      - "explore"
      - "discuss"
      - "figure out"
      - "work through"
      - "think through"
    
    uncertainty_indicators:
      - "maybe"
      - "possibly"
      - "perhaps"
      - "could we"
      - "would it be possible"
      - "wondering if"
    
    project_initiation:
      - "new project"
      - "startup idea"
      - "feature concept"
      - "app idea"
      - "building something"
```

**Purpose**: Detects exploratory and uncertain requests that benefit from interactive dialogue
**Activation**: Automatic with 70% confidence threshold
**Behavioral Settings**: Collaborative, non-presumptive dialogue with adaptive discovery depth

#### Task Management Mode
```yaml
task_management:
  description: "Multi-layer task orchestration with delegation and wave systems"
  activation_type: "automatic"
  confidence_threshold: 0.8
  
  trigger_patterns:
    multi_step_operations:
      - "build"
      - "implement"
      - "create"
      - "develop"
      - "set up"
      - "establish"
    
    scope_indicators:
      - "system"
      - "feature"
      - "comprehensive"
      - "complete"
      - "entire"
      - "full"
    
    complexity_indicators:
      - "complex"
      - "multiple"
      - "several"
      - "many"
      - "various"
      - "different"
  
  auto_activation_thresholds:
    file_count: 3
    directory_count: 2
    complexity_score: 0.4
    operation_types: 2
```

**Purpose**: Manages complex, multi-step operations requiring coordination and delegation
**Activation**: Automatic with 80% confidence threshold and quantitative thresholds
**Thresholds**: 3+ files, 2+ directories, 0.4+ complexity score, 2+ operation types

#### Token Efficiency Mode
```yaml
token_efficiency:
  description: "Intelligent token optimization with adaptive compression"
  activation_type: "automatic"
  confidence_threshold: 0.75
  
  trigger_patterns:
    resource_constraints:
      - "context usage >75%"
      - "large-scale operations"
      - "resource constraints"
      - "memory pressure"
    
    user_requests:
      - "brief"
      - "concise"
      - "compressed"
      - "short"
      - "efficient"
      - "minimal"
    
    efficiency_needs:
      - "token optimization"
      - "resource optimization"
      - "efficiency"
      - "performance"
```

**Purpose**: Optimizes token usage through intelligent compression and symbol systems
**Activation**: Automatic with 75% confidence threshold
**Compression Levels**: Minimal (0-40%) through Emergency (95%+)

#### Introspection Mode
```yaml
introspection:
  description: "Meta-cognitive analysis and framework troubleshooting"
  activation_type: "automatic"
  confidence_threshold: 0.6
  
  trigger_patterns:
    self_analysis:
      - "analyze reasoning"
      - "examine decision"
      - "reflect on"
      - "thinking process"
      - "decision logic"
    
    problem_solving:
      - "complex problem"
      - "multi-step"
      - "meta-cognitive"
      - "systematic thinking"
    
    error_recovery:
      - "outcomes don't match"
      - "errors occur"
      - "unexpected results"
      - "troubleshoot"
    
    framework_discussion:
      - "SuperClaude"
      - "framework"
      - "meta-conversation"
      - "system analysis"
```

**Purpose**: Enables meta-cognitive analysis and framework troubleshooting
**Activation**: Automatic with 60% confidence threshold (lower threshold for broader detection)
**Analysis Depth**: Meta-cognitive with high transparency and continuous pattern recognition

### 2. Mode Coordination Patterns (`mode_coordination`)

#### Concurrent Mode Support
```yaml
concurrent_modes:
  allowed_combinations:
    - ["brainstorming", "token_efficiency"]
    - ["task_management", "token_efficiency"]
    - ["introspection", "token_efficiency"]
    - ["task_management", "introspection"]
  
  coordination_strategies:
    brainstorming_efficiency: "compress_non_dialogue_content"
    task_management_efficiency: "compress_session_metadata"
    introspection_efficiency: "selective_analysis_compression"
```

**Purpose**: Enables multiple modes to work together efficiently
**Token Efficiency Integration**: Can combine with any other mode for resource optimization
**Coordination Strategies**: Mode-specific compression and optimization patterns

#### Mode Transitions
```yaml
mode_transitions:
  brainstorming_to_task_management:
    trigger: "requirements_clarified"
    handoff_data: ["brief", "requirements", "constraints"]
  
  task_management_to_introspection:
    trigger: "complex_issues_encountered"
    handoff_data: ["task_context", "performance_metrics", "issues"]
  
  any_to_token_efficiency:
    trigger: "resource_pressure"
    activation_priority: "immediate"
```

**Purpose**: Manages smooth transitions between modes with context preservation
**Automatic Handoffs**: Seamless transitions based on contextual triggers
**Data Preservation**: Critical context maintained during transitions

### 3. Performance Profiles (`performance_profiles`)

#### Lightweight Profile
```yaml
lightweight:
  target_response_time_ms: 100
  memory_usage_mb: 25
  cpu_utilization_percent: 20
  token_optimization: "standard"
```

**Usage**: Token Efficiency Mode, simple operations
**Characteristics**: Fast response, minimal resource usage, standard optimization

#### Standard Profile
```yaml
standard:
  target_response_time_ms: 200
  memory_usage_mb: 50
  cpu_utilization_percent: 40
  token_optimization: "balanced"
```

**Usage**: Brainstorming Mode, typical operations
**Characteristics**: Balanced performance and functionality

#### Intensive Profile
```yaml
intensive:
  target_response_time_ms: 500
  memory_usage_mb: 100
  cpu_utilization_percent: 70
  token_optimization: "aggressive"
```

**Usage**: Task Management Mode, complex operations
**Characteristics**: Higher resource usage for complex analysis and coordination

### 4. Mode-Specific Configurations (`mode_configurations`)

#### Brainstorming Configuration
```yaml
brainstorming:
  dialogue:
    max_rounds: 15
    convergence_threshold: 0.85
    context_preservation: "full"
  
  brief_generation:
    min_requirements: 3
    include_context: true
    validation_criteria: ["clarity", "completeness", "actionability"]
  
  integration:
    auto_handoff: true
    prd_agent: "brainstorm-PRD"
    command_coordination: "/sc:brainstorm"
```

**Dialogue Management**: Up to 15 dialogue rounds with 85% convergence threshold
**Brief Quality**: Minimum 3 requirements with comprehensive validation
**Integration**: Automatic handoff to PRD agent with command coordination

#### Task Management Configuration
```yaml
task_management:
  delegation:
    default_strategy: "auto"
    concurrency_limit: 7
    performance_monitoring: true
  
  wave_orchestration:
    auto_activation: true
    complexity_threshold: 0.4
    coordination_strategy: "adaptive"
  
  analytics:
    real_time_tracking: true
    performance_metrics: true
    optimization_suggestions: true
```

**Delegation**: Auto-strategy with 7 concurrent operations and performance monitoring
**Wave Orchestration**: Auto-activation at 0.4 complexity with adaptive coordination
**Analytics**: Real-time tracking with comprehensive performance metrics

#### Token Efficiency Configuration
```yaml
token_efficiency:
  compression:
    adaptive_levels: true
    quality_thresholds: [0.98, 0.95, 0.90, 0.85, 0.80]
    symbol_systems: true
    abbreviation_systems: true
  
  selective_compression:
    framework_exclusion: true
    user_content_preservation: true
    session_data_optimization: true
  
  performance:
    processing_target_ms: 150
    efficiency_target: 0.50
    quality_preservation: 0.95
```

**Compression**: 5-level adaptive compression with quality thresholds
**Selective Application**: Framework protection with user content preservation
**Performance**: 150ms processing target with 50% efficiency gain and 95% quality preservation

#### Introspection Configuration
```yaml
introspection:
  analysis:
    reasoning_depth: "comprehensive"
    pattern_detection: "continuous"
    bias_recognition: "active"
  
  transparency:
    thinking_process_exposure: true
    decision_logic_analysis: true
    assumption_validation: true
  
  learning:
    pattern_recognition: "continuous"
    effectiveness_tracking: true
    adaptation_suggestions: true
```

**Analysis Depth**: Comprehensive reasoning analysis with continuous pattern detection
**Transparency**: Full exposure of thinking processes and decision logic
**Learning**: Continuous pattern recognition with effectiveness tracking

### 5. Learning Integration (`learning_integration`)

#### Effectiveness Tracking
```yaml
learning_integration:
  mode_effectiveness_tracking:
    enabled: true
    metrics:
      - "activation_accuracy"
      - "user_satisfaction"
      - "task_completion_rates"
      - "performance_improvements"
```

**Metrics Collection**: Comprehensive effectiveness measurement across multiple dimensions
**Continuous Monitoring**: Real-time tracking of mode performance and user satisfaction

#### Adaptation Triggers
```yaml
adaptation_triggers:
  effectiveness_threshold: 0.7
  user_preference_weight: 0.8
  performance_impact_weight: 0.6
```

**Threshold Management**: 70% effectiveness threshold triggers adaptation
**Preference Learning**: High weight on user preferences (80%)
**Performance Balance**: Moderate weight on performance impact (60%)

#### Pattern Learning
```yaml
pattern_learning:
  user_specific: true
  project_specific: true
  context_aware: true
  cross_session: true
```

**Learning Scope**: Multi-dimensional learning across user, project, context, and time
**Continuous Improvement**: Persistent learning across sessions for long-term optimization

### 6. Quality Gates Integration (`quality_gates`)

```yaml
quality_gates:
  mode_activation:
    pattern_confidence: 0.6
    context_appropriateness: 0.7
    performance_readiness: true
  
  mode_coordination:
    conflict_resolution: "automatic"
    resource_allocation: "intelligent"
    performance_monitoring: "continuous"
  
  mode_effectiveness:
    real_time_monitoring: true
    adaptation_triggers: true
    quality_preservation: true
```

**Activation Quality**: Pattern confidence and context appropriateness thresholds
**Coordination Quality**: Automatic conflict resolution with intelligent resource allocation
**Effectiveness Quality**: Real-time monitoring with adaptation triggers

## Integration Points

### 1. Hook Integration (`integration_points.hooks`)

```yaml
hooks:
  session_start: "mode_initialization"
  pre_tool_use: "mode_coordination"
  post_tool_use: "mode_effectiveness_tracking"
  stop: "mode_analytics_consolidation"
```

**Session Start**: Mode initialization and activation
**Pre-Tool Use**: Mode coordination and optimization
**Post-Tool Use**: Effectiveness tracking and validation
**Stop**: Analytics consolidation and learning

### 2. MCP Server Integration (`integration_points.mcp_servers`)

```yaml
mcp_servers:
  brainstorming: ["sequential", "context7"]
  task_management: ["serena", "morphllm"]
  token_efficiency: ["morphllm"]
  introspection: ["sequential"]
```

**Brainstorming**: Sequential reasoning with documentation access
**Task Management**: Semantic analysis with intelligent editing
**Token Efficiency**: Optimized editing for compression
**Introspection**: Deep analysis for meta-cognitive examination

### 3. Command Integration (`integration_points.commands`)

```yaml
commands:
  brainstorming: "/sc:brainstorm"
  task_management: ["/task", "/spawn", "/loop"]
  reflection: "/sc:reflect"
```

**Brainstorming**: Dedicated brainstorming command
**Task Management**: Multi-command orchestration
**Reflection**: Introspection and analysis command

## Performance Implications

### 1. Mode Detection Overhead

#### Pattern Matching Performance
- **Detection Time**: 10-50ms per mode evaluation
- **Confidence Calculation**: 5-20ms per trigger pattern set
- **Total Detection**: 50-200ms for all mode evaluations

#### Memory Usage
- **Pattern Storage**: 10-20KB per mode configuration
- **Detection State**: 5-10KB during evaluation
- **Total Memory**: 50-100KB for mode detection system

### 2. Mode Coordination Impact

#### Concurrent Mode Overhead
- **Coordination Logic**: 20-100ms for multi-mode coordination
- **Resource Allocation**: 10-50ms for intelligent resource management
- **Transition Handling**: 50-200ms for mode transitions with data preservation

#### Resource Distribution
- **CPU Allocation**: Dynamic based on mode performance profiles
- **Memory Management**: Intelligent allocation based on mode requirements
- **Token Optimization**: Coordinated across all active modes

### 3. Learning System Performance

#### Effectiveness Tracking
- **Metrics Collection**: 5-20ms per mode operation
- **Pattern Analysis**: 50-200ms for pattern recognition updates
- **Adaptation Application**: 100-500ms for mode parameter adjustments

#### Storage Impact
- **Learning Data**: 100-500KB per mode per session
- **Pattern Storage**: 50-200KB persistent patterns per mode
- **Total Learning**: 1-5MB learning data with compression

## Configuration Best Practices

### 1. Production Mode Configuration
```yaml
# Optimize for reliability and performance
mode_detection:
  brainstorming:
    confidence_threshold: 0.8  # Higher threshold for production
  task_management:
    auto_activation_thresholds:
      file_count: 5  # Higher threshold to prevent unnecessary activation
```

### 2. Development Mode Configuration
```yaml
# Lower thresholds for testing and experimentation
mode_detection:
  introspection:
    confidence_threshold: 0.4  # Lower threshold for more introspection
learning_integration:
  adaptation_triggers:
    effectiveness_threshold: 0.5  # More aggressive adaptation
```

### 3. Performance-Optimized Configuration
```yaml
# Minimal mode activation for performance-critical environments
performance_profiles:
  lightweight:
    target_response_time_ms: 50  # Stricter performance targets
mode_coordination:
  concurrent_modes:
    allowed_combinations: []  # Disable concurrent modes
```

### 4. Learning-Optimized Configuration
```yaml
# Maximum learning and adaptation
learning_integration:
  pattern_learning:
    cross_session: true
    adaptation_frequency: "high"
mode_effectiveness_tracking:
  detailed_analytics: true
```

## Troubleshooting

### Common Mode Issues

#### Mode Not Activating
- **Check**: Trigger patterns match user input
- **Verify**: Confidence threshold appropriate for use case
- **Debug**: Log pattern matching results
- **Adjust**: Lower confidence threshold or add trigger patterns

#### Wrong Mode Activated
- **Analysis**: Review trigger pattern specificity
- **Solution**: Increase confidence thresholds or refine patterns
- **Testing**: Test pattern matching with sample inputs
- **Validation**: Monitor mode activation accuracy metrics

#### Mode Coordination Conflicts
- **Symptoms**: Multiple modes competing for resources
- **Resolution**: Check allowed combinations and coordination strategies
- **Optimization**: Adjust resource allocation and priority settings
- **Monitoring**: Track coordination effectiveness metrics

#### Performance Degradation
- **Identification**: Monitor mode detection and coordination overhead
- **Optimization**: Adjust performance profiles and thresholds
- **Resource Management**: Review concurrent mode limitations
- **Profiling**: Analyze mode-specific performance impact

### Learning System Troubleshooting

#### No Learning Observed
- **Check**: Learning integration enabled for relevant modes
- **Verify**: Effectiveness tracking collecting data
- **Debug**: Review adaptation trigger thresholds
- **Fix**: Ensure learning data persistence and pattern storage

#### Ineffective Adaptations
- **Analysis**: Review effectiveness metrics and adaptation triggers
- **Adjustment**: Modify effectiveness thresholds and learning weights
- **Validation**: Test adaptation effectiveness with controlled scenarios
- **Monitoring**: Track long-term learning trends and user satisfaction

## Related Documentation

- **Mode Implementation**: See individual mode documentation (MODE_*.md files)
- **Hook Integration**: Reference hook documentation for mode coordination
- **MCP Server Coordination**: Review MCP server documentation for mode-specific optimization
- **Command Integration**: See command documentation for mode-command coordination

## Version History

- **v1.0.0**: Initial modes configuration
- 4-mode behavioral system with comprehensive detection patterns
- Mode coordination and transition management
- Performance profiles and resource management
- Learning integration with effectiveness tracking
- Quality gates integration for mode validation