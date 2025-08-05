# Orchestrator Configuration (`orchestrator.yaml`)

## Overview

The `orchestrator.yaml` file defines intelligent routing patterns and coordination strategies for the SuperClaude-Lite framework. This configuration implements the ORCHESTRATOR.md patterns through automated MCP server selection, hybrid intelligence coordination, and performance optimization strategies.

## Purpose and Role

The orchestrator configuration serves as:
- **Intelligent Routing Engine**: Automatically selects optimal MCP servers based on task characteristics
- **Hybrid Intelligence Coordinator**: Manages coordination between Morphllm and Serena for optimal editing strategies
- **Performance Optimizer**: Implements caching, parallel processing, and resource management strategies
- **Fallback Manager**: Provides graceful degradation when preferred servers are unavailable
- **Learning Coordinator**: Tracks routing effectiveness and adapts selection strategies

## Configuration Structure

### 1. MCP Server Routing Patterns (`routing_patterns`)

#### UI Components Routing
```yaml
ui_components:
  triggers: ["component", "button", "form", "modal", "dialog", "card", "input", "design", "frontend", "ui", "interface"]
  mcp_server: "magic"
  persona: "frontend-specialist"
  confidence_threshold: 0.8
  priority: "high"
  performance_profile: "standard"
  capabilities: ["ui_generation", "design_systems", "component_patterns"]
```

**Purpose**: Routes UI-related requests to Magic MCP server with frontend persona activation
**Triggers**: Comprehensive UI terminology detection
**Performance**: Standard performance profile with high priority routing

#### Deep Analysis Routing
```yaml
deep_analysis:
  triggers: ["analyze", "complex", "system-wide", "architecture", "debug", "troubleshoot", "investigate", "root cause"]
  mcp_server: "sequential"
  thinking_mode: "--think-hard"
  confidence_threshold: 0.75
  priority: "high"
  performance_profile: "intensive"
  capabilities: ["complex_reasoning", "systematic_analysis", "hypothesis_testing"]
  context_expansion: true
```

**Purpose**: Routes complex analysis requests to Sequential with enhanced thinking modes
**Thinking Integration**: Automatically activates `--think-hard` for systematic analysis
**Context Expansion**: Enables broader context analysis for complex problems

#### Library Documentation Routing
```yaml
library_documentation:
  triggers: ["library", "framework", "package", "import", "dependency", "documentation", "docs", "api", "reference"]
  mcp_server: "context7"
  persona: "architect"
  confidence_threshold: 0.85
  priority: "medium"
  performance_profile: "standard"
  capabilities: ["documentation_access", "framework_patterns", "best_practices"]
```

**Purpose**: Routes documentation requests to Context7 with architect persona
**High Confidence**: 85% threshold ensures precise documentation routing
**Best Practices**: Integrates framework patterns and best practices into responses

#### Testing Automation Routing
```yaml
testing_automation:
  triggers: ["test", "testing", "e2e", "end-to-end", "browser", "automation", "validation", "verify"]
  mcp_server: "playwright"
  confidence_threshold: 0.8
  priority: "medium"
  performance_profile: "intensive"
  capabilities: ["browser_automation", "testing_frameworks", "performance_testing"]
```

**Purpose**: Routes testing requests to Playwright for browser automation
**Manual Preference**: No auto-activation, prefers manual confirmation for testing operations
**Intensive Profile**: Uses intensive performance profile for testing workloads

#### Intelligent Editing Routing
```yaml
intelligent_editing:
  triggers: ["edit", "modify", "refactor", "update", "change", "fix", "improve"]
  mcp_server: "morphllm"
  confidence_threshold: 0.7
  priority: "medium"
  performance_profile: "lightweight"
  capabilities: ["pattern_application", "fast_apply", "intelligent_editing"]
  complexity_threshold: 0.6
  file_count_threshold: 10
```

**Purpose**: Routes editing requests to Morphllm for fast, intelligent modifications
**Thresholds**: Complexity ≤0.6 and file count ≤10 for optimal Morphllm performance
**Lightweight Profile**: Optimized for speed and efficiency

#### Semantic Analysis Routing
```yaml
semantic_analysis:
  triggers: ["semantic", "symbol", "reference", "find", "search", "navigate", "explore"]
  mcp_server: "serena"
  confidence_threshold: 0.8
  priority: "high"
  performance_profile: "standard"
  capabilities: ["semantic_understanding", "project_context", "memory_management"]
```

**Purpose**: Routes semantic analysis to Serena for deep project understanding
**High Priority**: Essential for project navigation and context management
**Symbol Operations**: Optimal for symbol-level operations and refactoring

#### Multi-File Operations Routing
```yaml
multi_file_operations:
  triggers: ["multiple files", "batch", "bulk", "project-wide", "codebase", "entire"]
  mcp_server: "serena"
  confidence_threshold: 0.9
  priority: "high"
  performance_profile: "intensive"
  capabilities: ["multi_file_coordination", "project_analysis"]
```

**Purpose**: Routes large-scale operations to Serena for comprehensive project handling
**High Confidence**: 90% threshold ensures accurate detection of multi-file operations
**Intensive Profile**: Resources allocated for complex project-wide operations

### 2. Hybrid Intelligence Selection (`hybrid_intelligence`)

#### Morphllm vs Serena Decision Matrix
```yaml
morphllm_vs_serena:
  decision_factors:
    - file_count
    - complexity_score
    - operation_type
    - symbol_operations_required
    - project_size
  
  morphllm_criteria:
    file_count_max: 10
    complexity_max: 0.6
    preferred_operations: ["edit", "modify", "update", "pattern_application"]
    optimization_focus: "token_efficiency"
  
  serena_criteria:
    file_count_min: 5
    complexity_min: 0.4
    preferred_operations: ["analyze", "refactor", "navigate", "symbol_operations"]
    optimization_focus: "semantic_understanding"
  
  fallback_strategy:
    - try_primary_choice
    - fallback_to_alternative
    - use_native_tools
```

**Decision Logic**: Multi-factor analysis determines optimal server selection
**Clear Boundaries**: Morphllm for simple edits, Serena for complex analysis
**Fallback Chain**: Graceful degradation through alternative servers to native tools

### 3. Auto-Activation Rules (`auto_activation`)

#### Complexity Thresholds
```yaml
complexity_thresholds:
  enable_sequential:
    complexity_score: 0.6
    file_count: 5
    operation_types: ["analyze", "debug", "complex"]
  
  enable_delegation:
    file_count: 3
    directory_count: 2
    complexity_score: 0.4
  
  enable_validation:
    is_production: true
    risk_level: ["high", "critical"]
    operation_types: ["deploy", "refactor", "delete"]
```

**Sequential Activation**: Complex operations with 0.6+ complexity or 5+ files
**Delegation Triggers**: Multi-file operations exceeding thresholds
**Validation Requirements**: Production and high-risk operations

### 4. Performance Optimization (`performance_optimization`)

#### Parallel Execution Strategy
```yaml
parallel_execution:
  file_threshold: 3
  estimated_speedup_min: 1.4
  max_concurrency: 7
```

**Threshold Management**: 3+ files required for parallel processing
**Performance Guarantee**: Minimum 1.4x speedup required for activation
**Concurrency Limits**: Maximum 7 concurrent operations for resource management

#### Caching Strategy
```yaml
caching_strategy:
  enable_for_operations: ["documentation_lookup", "analysis_results", "pattern_matching"]
  cache_duration_minutes: 30
  max_cache_size_mb: 100
```

**Selective Caching**: Focuses on high-benefit operations
**Duration Management**: 30-minute cache lifetime balances freshness with performance
**Size Limits**: 100MB cache prevents excessive memory usage

#### Resource Management
```yaml
resource_management:
  memory_threshold_percent: 85
  token_threshold_percent: 75
  fallback_to_lightweight: true
```

**Memory Protection**: 85% memory threshold triggers resource optimization
**Token Management**: 75% token usage threshold activates efficiency mode
**Automatic Fallback**: Switches to lightweight alternatives under pressure

### 5. Quality Gates Integration (`quality_gates`)

#### Validation Levels
```yaml
validation_levels:
  basic: ["syntax_validation"]
  standard: ["syntax_validation", "type_analysis", "code_quality"]
  comprehensive: ["syntax_validation", "type_analysis", "code_quality", "security_assessment", "performance_analysis"]
  production: ["syntax_validation", "type_analysis", "code_quality", "security_assessment", "performance_analysis", "integration_testing", "deployment_validation"]
```

**Progressive Validation**: Escalating validation complexity based on operation risk
**Production Standards**: Comprehensive 7-step validation for production operations

#### Trigger Conditions
```yaml
trigger_conditions:
  comprehensive:
    - is_production: true
    - complexity_score: ">0.7"
    - operation_types: ["refactor", "architecture"]
  
  production:
    - is_production: true
    - operation_types: ["deploy", "release"]
```

**Comprehensive Triggers**: Production context or high complexity operations
**Production Triggers**: Deploy and release operations receive maximum validation

### 6. Fallback Strategies (`fallback_strategies`)

#### MCP Server Unavailable
```yaml
mcp_server_unavailable:
  context7: ["web_search", "cached_documentation", "native_analysis"]
  sequential: ["native_step_by_step", "basic_analysis"]
  magic: ["manual_component_generation", "template_suggestions"]
  playwright: ["manual_testing_suggestions", "test_case_generation"]
  morphllm: ["native_edit_tools", "manual_editing"]
  serena: ["basic_file_operations", "simple_search"]
```

**Graceful Degradation**: Each server has specific fallback alternatives
**Functionality Preservation**: Maintains core functionality even with server failures
**User Guidance**: Provides manual alternatives when automation unavailable

#### Performance Degradation
```yaml
performance_degradation:
  high_latency: ["reduce_analysis_depth", "enable_caching", "parallel_processing"]
  resource_constraints: ["lightweight_alternatives", "compression_mode", "minimal_features"]
```

**Latency Management**: Reduces analysis depth and increases caching
**Resource Protection**: Switches to lightweight alternatives and compression

#### Quality Issues
```yaml
quality_issues:
  validation_failures: ["increase_validation_depth", "manual_review", "rollback_capability"]
  error_rates_high: ["enable_pre_validation", "reduce_complexity", "step_by_step_execution"]
```

**Quality Recovery**: Increases validation and enables manual review
**Error Prevention**: Pre-validation and complexity reduction strategies

### 7. Learning Integration (`learning_integration`)

#### Effectiveness Tracking
```yaml
effectiveness_tracking:
  track_server_performance: true
  track_routing_decisions: true
  track_user_satisfaction: true
```

**Performance Monitoring**: Tracks server performance and routing accuracy
**User Feedback**: Incorporates user satisfaction into learning algorithms
**Decision Analysis**: Analyzes routing decision effectiveness over time

#### Adaptation Triggers
```yaml
adaptation_triggers:
  effectiveness_threshold: 0.6
  confidence_threshold: 0.7
  usage_count_min: 3
```

**Effectiveness Gates**: 60% effectiveness threshold triggers adaptation
**Confidence Requirements**: 70% confidence required for routing changes
**Statistical Significance**: Minimum 3 usage instances for pattern recognition

#### Optimization Feedback
```yaml
optimization_feedback:
  performance_degradation: "adjust_routing_weights"
  user_preference_detected: "update_server_priorities"
  error_patterns_found: "enhance_fallback_strategies"
```

**Dynamic Optimization**: Adjusts routing weights based on performance
**Personalization**: Updates priorities based on user preferences
**Error Learning**: Enhances fallback strategies based on error patterns

### 8. Mode Integration (`mode_integration`)

#### Brainstorming Mode
```yaml
brainstorming:
  preferred_servers: ["sequential", "context7"]
  thinking_modes: ["--think", "--think-hard"]
```

**Server Preference**: Sequential for reasoning, Context7 for documentation
**Enhanced Thinking**: Activates thinking modes for deeper analysis

#### Task Management Mode
```yaml
task_management:
  coordination_servers: ["serena", "morphllm"]
  delegation_strategies: ["files", "folders", "auto"]
```

**Coordination Focus**: Serena for analysis, Morphllm for execution
**Delegation Options**: Multiple strategies for different operation types

#### Token Efficiency Mode
```yaml
token_efficiency:
  optimization_servers: ["morphllm"]
  compression_strategies: ["symbol_systems", "abbreviations"]
```

**Efficiency Focus**: Morphllm for token-optimized operations
**Compression Integration**: Symbol systems and abbreviation strategies

## Performance Implications

### 1. Routing Decision Overhead

#### Decision Time Analysis
- **Pattern Matching**: 10-50ms per routing pattern evaluation
- **Confidence Calculation**: 5-20ms per server option
- **Total Routing Decision**: 50-200ms for complete routing analysis

#### Memory Usage
- **Pattern Storage**: 20-50KB for all routing patterns
- **Decision State**: 10-20KB during routing evaluation
- **Cache Storage**: Up to 100MB for cached results

### 2. MCP Server Coordination

#### Server Communication
- **Activation Time**: 100-500ms per MCP server activation
- **Coordination Overhead**: 50-200ms for multi-server operations
- **Fallback Detection**: 100-300ms to detect and switch to fallback

#### Resource Allocation
- **Memory Per Server**: 50-200MB depending on server type
- **CPU Usage**: 20-60% during intensive server operations
- **Network Usage**: Varies by server, cached where possible

### 3. Learning System Impact

#### Learning Overhead
- **Effectiveness Tracking**: 5-20ms per operation for metrics collection
- **Pattern Analysis**: 100-500ms for pattern recognition updates
- **Adaptation Application**: 200ms-2s for routing weight adjustments

#### Storage Requirements
- **Learning Data**: 500KB-2MB per session for effectiveness tracking
- **Pattern Storage**: 100KB-1MB for persistent patterns
- **Cache Data**: Up to 100MB for performance optimization

## Configuration Best Practices

### 1. Production Orchestrator Configuration
```yaml
# Optimize for reliability and performance
routing_patterns:
  ui_components:
    confidence_threshold: 0.9  # Higher confidence for production
auto_activation:
  enable_validation:
    is_production: true
    risk_level: ["medium", "high", "critical"]  # More conservative
```

### 2. Development Orchestrator Configuration
```yaml
# Enable more experimentation and learning
learning_integration:
  adaptation_triggers:
    effectiveness_threshold: 0.4  # More aggressive learning
    usage_count_min: 1  # Learn from fewer samples
```

### 3. Performance-Optimized Configuration
```yaml
# Minimize overhead for performance-critical environments
performance_optimization:
  parallel_execution:
    file_threshold: 5  # Higher threshold to reduce overhead
  caching_strategy:
    cache_duration_minutes: 60  # Longer cache for better performance
```

### 4. Learning-Optimized Configuration
```yaml
# Maximum learning and adaptation
learning_integration:
  effectiveness_tracking:
    detailed_analytics: true
    user_interaction_tracking: true
  optimization_feedback:
    continuous_adaptation: true
```

## Troubleshooting

### Common Orchestration Issues

#### Wrong Server Selected
- **Symptoms**: Suboptimal server choice for task type
- **Analysis**: Review trigger patterns and confidence thresholds
- **Solution**: Adjust routing patterns or increase confidence thresholds
- **Testing**: Test routing with sample inputs and monitor effectiveness

#### Server Unavailable Issues
- **Symptoms**: Frequent fallback activation, degraded functionality
- **Diagnosis**: Check MCP server availability and network connectivity
- **Resolution**: Verify server configurations and fallback strategies
- **Prevention**: Implement server health monitoring

#### Performance Degradation
- **Symptoms**: Slow routing decisions, high overhead
- **Analysis**: Profile routing decision time and resource usage
- **Optimization**: Adjust confidence thresholds, enable caching
- **Monitoring**: Track routing performance metrics

#### Fallback Chain Failures
- **Symptoms**: Complete functionality loss when primary server fails
- **Investigation**: Review fallback strategy completeness
- **Enhancement**: Add more fallback options and manual alternatives
- **Testing**: Test fallback chains under various failure scenarios

### Learning System Troubleshooting

#### No Learning Observed
- **Check**: Learning integration enabled and collecting data
- **Verify**: Effectiveness metrics being calculated and stored
- **Debug**: Review adaptation trigger thresholds
- **Fix**: Ensure learning data persistence and pattern recognition

#### Poor Routing Decisions
- **Analysis**: Review routing effectiveness metrics and user feedback
- **Adjustment**: Modify confidence thresholds and trigger patterns
- **Validation**: Test routing decisions with controlled scenarios
- **Monitoring**: Track long-term routing accuracy trends

#### Resource Usage Issues
- **Monitoring**: Track memory and CPU usage during orchestration
- **Optimization**: Adjust cache sizes and parallel processing limits
- **Tuning**: Optimize resource thresholds and fallback triggers
- **Balancing**: Balance learning sophistication with resource constraints

## Integration with Other Configurations

### 1. MCP Server Coordination
The orchestrator configuration works closely with:
- **superclaude-config.json**: MCP server definitions and capabilities
- **performance.yaml**: Performance targets and optimization strategies
- **modes.yaml**: Mode-specific server preferences and coordination

### 2. Hook Integration
Orchestrator patterns are implemented through:
- **Pre-Tool Use Hook**: Server selection and routing decisions
- **Post-Tool Use Hook**: Effectiveness tracking and learning
- **Session Start Hook**: Initial server availability assessment

### 3. Quality Gates Coordination
Quality validation levels integrate with:
- **validation.yaml**: Specific validation rules and standards
- **Trigger conditions for comprehensive and production validation
- **Performance monitoring for validation effectiveness

## Related Documentation

- **ORCHESTRATOR.md**: Framework orchestration patterns and principles
- **MCP Server Documentation**: Individual server capabilities and integration
- **Hook Documentation**: Implementation details for orchestration hooks
- **Performance Configuration**: Performance targets and optimization strategies

## Version History

- **v1.0.0**: Initial orchestrator configuration
- Comprehensive MCP server routing with 6 server types
- Hybrid intelligence coordination between Morphllm and Serena
- Multi-level quality gates integration with production safeguards
- Learning system integration with effectiveness tracking
- Performance optimization with caching and parallel processing
- Robust fallback strategies for graceful degradation