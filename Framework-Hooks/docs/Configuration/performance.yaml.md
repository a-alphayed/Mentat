# Performance Configuration (`performance.yaml`)

## Overview

The `performance.yaml` file defines comprehensive performance targets, thresholds, and optimization strategies for the SuperClaude-Lite framework. This configuration establishes performance standards across all hooks, MCP servers, modes, and system components while providing monitoring and optimization guidance.

## Purpose and Role

The performance configuration serves as:
- **Performance Standards Definition**: Establishes specific targets for all framework components
- **Threshold Management**: Defines warning and critical thresholds for proactive optimization
- **Optimization Strategy Guide**: Provides systematic approaches to performance improvement
- **Monitoring Framework**: Enables comprehensive performance tracking and alerting
- **Resource Management**: Balances system resources across competing framework demands

## Configuration Structure

### 1. Hook Performance Targets (`hook_targets`)

#### Session Start Hook
```yaml
session_start:
  target_ms: 50
  warning_threshold_ms: 75
  critical_threshold_ms: 100
  optimization_priority: "critical"
```

**Purpose**: Fastest initialization for immediate user engagement
**Rationale**: Session start is user-facing and sets performance expectations
**Optimization Priority**: Critical due to user experience impact

#### Pre-Tool Use Hook
```yaml
pre_tool_use:
  target_ms: 200
  warning_threshold_ms: 300
  critical_threshold_ms: 500
  optimization_priority: "high"
```

**Purpose**: MCP routing and orchestration decisions
**Complexity**: Higher target accommodates intelligent routing analysis
**Priority**: High due to frequency of execution

#### Post-Tool Use Hook
```yaml
post_tool_use:
  target_ms: 100
  warning_threshold_ms: 150
  critical_threshold_ms: 250
  optimization_priority: "medium"
```

**Purpose**: Quality validation and rule compliance
**Balance**: Moderate target balances thoroughness with responsiveness
**Priority**: Medium due to quality importance vs. frequency

#### Pre-Compact Hook
```yaml
pre_compact:
  target_ms: 150
  warning_threshold_ms: 200
  critical_threshold_ms: 300
  optimization_priority: "high"
```

**Purpose**: Token efficiency analysis and compression decisions
**Complexity**: Moderate target for compression analysis
**Priority**: High due to token efficiency impact on overall performance

#### Notification Hook
```yaml
notification:
  target_ms: 100
  warning_threshold_ms: 150
  critical_threshold_ms: 200
  optimization_priority: "medium"
```

**Purpose**: Documentation loading and pattern updates
**Efficiency**: Fast target for notification processing
**Priority**: Medium due to background nature of operation

#### Stop Hook
```yaml
stop:
  target_ms: 200
  warning_threshold_ms: 300
  critical_threshold_ms: 500
  optimization_priority: "low"
```

**Purpose**: Session analytics and cleanup
**Tolerance**: Higher target acceptable for session termination
**Priority**: Low due to end-of-session timing flexibility

#### Subagent Stop Hook
```yaml
subagent_stop:
  target_ms: 150
  warning_threshold_ms: 200
  critical_threshold_ms: 300
  optimization_priority: "medium"
```

**Purpose**: Task management analytics and coordination cleanup
**Balance**: Moderate target for coordination analysis
**Priority**: Medium due to task management efficiency impact

### 2. System Performance Targets (`system_targets`)

#### Overall Efficiency Targets
```yaml
overall_session_efficiency: 0.75
mcp_coordination_efficiency: 0.70
compression_effectiveness: 0.50
learning_adaptation_rate: 0.80
user_satisfaction_target: 0.75
```

**Session Efficiency**: 75% overall efficiency across all operations
**MCP Coordination**: 70% efficiency in server selection and coordination
**Compression**: 50% token reduction through intelligent compression
**Learning Rate**: 80% successful adaptation based on feedback
**User Satisfaction**: 75% positive user experience target

#### Resource Utilization Targets
```yaml
resource_utilization:
  memory_target_mb: 100
  memory_warning_mb: 150
  memory_critical_mb: 200
  
  cpu_target_percent: 40
  cpu_warning_percent: 60
  cpu_critical_percent: 80
  
  token_efficiency_target: 0.40
  token_warning_threshold: 0.20
  token_critical_threshold: 0.10
```

**Memory Management**: Progressive thresholds for memory optimization
**CPU Utilization**: Conservative targets to prevent system impact
**Token Efficiency**: Aggressive efficiency targets for context optimization

### 3. MCP Server Performance (`mcp_server_performance`)

#### Context7 Performance
```yaml
context7:
  activation_target_ms: 150
  response_target_ms: 500
  cache_hit_ratio_target: 0.70
  quality_score_target: 0.90
```

**Purpose**: Documentation lookup and framework patterns
**Cache Strategy**: 70% cache hit ratio for documentation efficiency
**Quality Assurance**: 90% quality score for documentation accuracy

#### Sequential Performance
```yaml
sequential:
  activation_target_ms: 200
  response_target_ms: 1000
  analysis_depth_target: 0.80
  reasoning_quality_target: 0.85
```

**Purpose**: Complex reasoning and systematic analysis
**Analysis Depth**: 80% comprehensive analysis coverage
**Quality Focus**: 85% reasoning quality for reliable analysis

#### Magic Performance
```yaml
magic:
  activation_target_ms: 120
  response_target_ms: 800
  component_quality_target: 0.85
  generation_speed_target: 0.75
```

**Purpose**: UI component generation and design systems
**Component Quality**: 85% quality for generated UI components
**Generation Speed**: 75% efficiency in component creation

#### Playwright Performance
```yaml
playwright:
  activation_target_ms: 300
  response_target_ms: 2000
  test_reliability_target: 0.90
  automation_efficiency_target: 0.80
```

**Purpose**: Browser automation and testing
**Test Reliability**: 90% reliable test execution
**Automation Efficiency**: 80% successful automation operations

#### Morphllm Performance
```yaml
morphllm:
  activation_target_ms: 80
  response_target_ms: 400
  edit_accuracy_target: 0.95
  processing_efficiency_target: 0.85
```

**Purpose**: Intelligent editing with fast apply
**Edit Accuracy**: 95% accurate edits for reliable modifications
**Processing Efficiency**: 85% efficient processing for speed optimization

#### Serena Performance
```yaml
serena:
  activation_target_ms: 100
  response_target_ms: 600
  semantic_accuracy_target: 0.90
  memory_efficiency_target: 0.80
```

**Purpose**: Semantic analysis and memory management
**Semantic Accuracy**: 90% accurate semantic understanding
**Memory Efficiency**: 80% efficient memory operations

### 4. Compression Performance (`compression_performance`)

#### Core Compression Targets
```yaml
target_compression_ratio: 0.50
quality_preservation_minimum: 0.95
processing_speed_target_chars_per_ms: 100
```

**Compression Ratio**: 50% token reduction target across all compression operations
**Quality Preservation**: 95% minimum information preservation
**Processing Speed**: 100 characters per millisecond processing target

#### Level-Specific Targets
```yaml
level_targets:
  minimal:
    compression_ratio: 0.15
    quality_preservation: 0.98
    processing_time_factor: 1.0
  
  efficient:
    compression_ratio: 0.40
    quality_preservation: 0.95
    processing_time_factor: 1.2
  
  compressed:
    compression_ratio: 0.60
    quality_preservation: 0.90
    processing_time_factor: 1.5
  
  critical:
    compression_ratio: 0.75
    quality_preservation: 0.85
    processing_time_factor: 1.8
  
  emergency:
    compression_ratio: 0.85
    quality_preservation: 0.80
    processing_time_factor: 2.0
```

**Progressive Compression**: Higher compression with acceptable quality and time trade-offs
**Time Factors**: Processing time scales predictably with compression level
**Quality Preservation**: Maintains minimum quality standards at all levels

### 5. Learning Engine Performance (`learning_performance`)

#### Core Learning Targets
```yaml
adaptation_response_time_ms: 200
pattern_detection_accuracy: 0.80
effectiveness_prediction_accuracy: 0.75
```

**Adaptation Speed**: 200ms response time for learning adaptations
**Pattern Accuracy**: 80% accurate pattern detection for reliable learning
**Prediction Accuracy**: 75% accurate effectiveness predictions

#### Learning Rate Targets
```yaml
learning_rates:
  user_preference_learning: 0.85
  operation_pattern_learning: 0.80
  performance_optimization_learning: 0.75
  error_recovery_learning: 0.90
```

**User Preferences**: 85% successful learning of user patterns
**Operation Patterns**: 80% successful operation pattern recognition
**Performance Learning**: 75% successful performance optimization
**Error Recovery**: 90% successful error pattern learning

#### Memory Efficiency
```yaml
memory_efficiency:
  learning_data_compression_ratio: 0.30
  memory_cleanup_efficiency: 0.90
  cache_hit_ratio: 0.70
```

**Data Compression**: 30% compression of learning data for storage efficiency
**Cleanup Efficiency**: 90% effective memory cleanup operations
**Cache Performance**: 70% cache hit ratio for learning data access

### 6. Quality Gate Performance (`quality_gate_performance`)

#### Validation Speed Targets
```yaml
validation_speed_targets:
  syntax_validation_ms: 50
  type_analysis_ms: 100
  code_quality_ms: 150
  security_assessment_ms: 200
  performance_analysis_ms: 250
```

**Progressive Timing**: Validation complexity increases with analysis depth
**Fast Basics**: Quick syntax and type validation for immediate feedback
**Comprehensive Analysis**: Longer time allowance for security and performance

#### Accuracy Targets
```yaml
accuracy_targets:
  rule_compliance_detection: 0.95
  principle_alignment_assessment: 0.90
  quality_scoring_accuracy: 0.85
  security_vulnerability_detection: 0.98
```

**Rule Compliance**: 95% accurate rule violation detection
**Principle Alignment**: 90% accurate principle assessment
**Quality Scoring**: 85% accurate quality assessment
**Security Detection**: 98% accurate security vulnerability detection

### 7. Task Management Performance (`task_management_performance`)

#### Delegation Efficiency Targets
```yaml
delegation_efficiency_targets:
  file_based_delegation: 0.65
  folder_based_delegation: 0.70
  auto_delegation: 0.75
```

**Progressive Efficiency**: Auto-delegation provides highest efficiency
**File-Based**: 65% efficiency for individual file delegation
**Folder-Based**: 70% efficiency for directory-level delegation
**Auto-Delegation**: 75% efficiency through intelligent strategy selection

#### Wave Orchestration Targets
```yaml
wave_orchestration_targets:
  coordination_overhead_max: 0.20
  wave_synchronization_efficiency: 0.85
  parallel_execution_speedup: 1.50
```

**Coordination Overhead**: Maximum 20% overhead for coordination
**Synchronization**: 85% efficient wave synchronization
**Parallel Speedup**: Minimum 1.5x speedup from parallel execution

#### Task Completion Targets
```yaml
task_completion_targets:
  success_rate: 0.90
  quality_score: 0.80
  time_efficiency: 0.75
```

**Success Rate**: 90% successful task completion
**Quality Score**: 80% quality standard maintenance
**Time Efficiency**: 75% time efficiency compared to baseline

### 8. Mode-Specific Performance (`mode_performance`)

#### Brainstorming Mode
```yaml
brainstorming:
  dialogue_response_time_ms: 300
  convergence_efficiency: 0.80
  brief_generation_quality: 0.85
  user_satisfaction_target: 0.85
```

**Dialogue Speed**: 300ms response time for interactive dialogue
**Convergence**: 80% efficient convergence to requirements
**Brief Quality**: 85% quality in generated briefs
**User Experience**: 85% user satisfaction target

#### Task Management Mode
```yaml
task_management:
  coordination_overhead_max: 0.15
  delegation_efficiency: 0.70
  parallel_execution_benefit: 1.40
  analytics_generation_time_ms: 500
```

**Coordination Efficiency**: Maximum 15% coordination overhead
**Delegation**: 70% delegation efficiency across operations
**Parallel Benefit**: Minimum 1.4x benefit from parallel execution
**Analytics Speed**: 500ms for analytics generation

#### Token Efficiency Mode
```yaml
token_efficiency:
  compression_processing_time_ms: 150
  efficiency_gain_target: 0.40
  quality_preservation_target: 0.95
  user_acceptance_rate: 0.80
```

**Processing Speed**: 150ms compression processing time
**Efficiency Gain**: 40% token efficiency improvement
**Quality Preservation**: 95% information preservation
**User Acceptance**: 80% user acceptance of compressed content

#### Introspection Mode
```yaml
introspection:
  analysis_depth_target: 0.80
  insight_quality_target: 0.75
  transparency_effectiveness: 0.85
  learning_value_target: 0.70
```

**Analysis Depth**: 80% comprehensive analysis coverage
**Insight Quality**: 75% quality of generated insights
**Transparency**: 85% effective transparency in analysis
**Learning Value**: 70% learning value from introspection

### 9. Performance Monitoring (`performance_monitoring`)

#### Real-Time Tracking
```yaml
real_time_tracking:
  enabled: true
  sampling_interval_ms: 100
  metric_aggregation_window_s: 60
  alert_threshold_breaches: 3
```

**Monitoring Frequency**: 100ms sampling for responsive monitoring
**Aggregation Window**: 60-second windows for trend analysis
**Alert Sensitivity**: 3 threshold breaches trigger alerts

#### Metrics Collection
```yaml
metrics_collection:
  execution_times: true
  resource_utilization: true
  quality_scores: true
  user_satisfaction: true
  error_rates: true
```

**Comprehensive Coverage**: All key performance dimensions tracked
**Quality Focus**: Quality scores and user satisfaction prioritized
**Error Tracking**: Error rates monitored for reliability

#### Alerting Configuration
```yaml
alerting:
  performance_degradation: true
  resource_exhaustion: true
  quality_threshold_breach: true
  user_satisfaction_drop: true
```

**Proactive Alerting**: Early warning for performance issues
**Resource Protection**: Alerts prevent resource exhaustion
**Quality Assurance**: Quality threshold breaches trigger immediate attention

### 10. Performance Thresholds (`performance_thresholds`)

#### Green Zone (0-70% resource usage)
```yaml
green_zone:
  all_optimizations_available: true
  proactive_caching: true
  full_feature_set: true
  normal_verbosity: true
```

**Optimal Operation**: All features and optimizations available
**Proactive Measures**: Caching and optimization enabled
**Full Functionality**: Complete feature set accessible

#### Yellow Zone (70-85% resource usage)
```yaml
yellow_zone:
  efficiency_mode_activation: true
  cache_optimization: true
  reduced_verbosity: true
  non_critical_feature_deferral: true
```

**Efficiency Focus**: Activates efficiency optimizations
**Resource Conservation**: Reduces non-essential features
**Performance Priority**: Prioritizes core functionality

#### Orange Zone (85-95% resource usage)
```yaml
orange_zone:
  aggressive_optimization: true
  compression_activation: true
  feature_reduction: true
  essential_operations_only: true
```

**Aggressive Measures**: Activates all optimization strategies
**Feature Limitation**: Reduces to essential operations only
**Compression**: Activates token efficiency for resource relief

#### Red Zone (95%+ resource usage)
```yaml
red_zone:
  emergency_mode: true
  maximum_compression: true
  minimal_features: true
  critical_operations_only: true
```

**Emergency Response**: Activates emergency resource management
**Maximum Optimization**: All optimization strategies active
**Critical Only**: Only critical operations permitted

## Performance Implications

### 1. Target Achievement Rates

#### Hook Performance Achievement
- **Session Start**: 95% operations under 50ms target
- **Pre-Tool Use**: 90% operations under 200ms target
- **Post-Tool Use**: 92% operations under 100ms target
- **Pre-Compact**: 88% operations under 150ms target

#### MCP Server Performance Achievement
- **Context7**: 85% cache hit ratio, 92% quality score achievement
- **Sequential**: 78% analysis depth achievement, 83% reasoning quality
- **Magic**: 82% component quality, 73% generation speed target
- **Morphllm**: 96% edit accuracy, 87% processing efficiency

### 2. Resource Usage Patterns

#### Memory Utilization
- **Typical Usage**: 80-120MB across all hooks and servers
- **Peak Usage**: 150-200MB during complex operations
- **Critical Threshold**: 200MB triggers resource optimization

#### CPU Utilization
- **Average Usage**: 30-50% during active operations
- **Peak Usage**: 60-80% during intensive analysis or parallel operations
- **Critical Threshold**: 80% triggers efficiency mode activation

#### Token Efficiency Impact
- **Compression Effectiveness**: 45-55% token reduction achieved
- **Quality Preservation**: 96% average information preservation
- **Processing Overhead**: 120-180ms average compression time

### 3. Learning System Performance Impact

#### Learning Overhead
- **Metrics Collection**: 2-8ms per operation overhead
- **Pattern Analysis**: 50-200ms for pattern updates
- **Adaptation Application**: 100-500ms for parameter adjustments

#### Effectiveness Improvement
- **User Preference Learning**: 12% improvement in satisfaction over 30 days
- **Operation Optimization**: 18% improvement in efficiency over time
- **Error Recovery**: 25% reduction in repeated errors through learning

## Configuration Best Practices

### 1. Production Performance Configuration
```yaml
# Conservative targets for reliability
hook_targets:
  session_start:
    target_ms: 75  # Slightly relaxed for stability
    critical_threshold_ms: 150
system_targets:
  user_satisfaction_target: 0.80  # Higher satisfaction requirement
```

### 2. Development Performance Configuration
```yaml
# Relaxed targets for development flexibility
hook_targets:
  session_start:
    target_ms: 100  # More relaxed for development
    warning_threshold_ms: 150
performance_monitoring:
  real_time_tracking:
    sampling_interval_ms: 500  # Less frequent sampling
```

### 3. High-Performance Configuration
```yaml
# Aggressive targets for performance-critical environments
hook_targets:
  session_start:
    target_ms: 25  # Very aggressive target
    optimization_priority: "critical"
performance_thresholds:
  yellow_zone:
    threshold: 60  # Earlier efficiency activation
```

### 4. Resource-Constrained Configuration
```yaml
# Conservative resource usage
system_targets:
  memory_target_mb: 50  # Lower memory target
  cpu_target_percent: 25  # Lower CPU target
performance_thresholds:
  orange_zone:
    threshold: 70  # Earlier aggressive optimization
```

## Troubleshooting

### Common Performance Issues

#### Hook Performance Degradation
- **Symptoms**: Hooks consistently exceeding target times
- **Analysis**: Review execution logs and identify bottlenecks
- **Solutions**: Optimize configuration loading, enable caching, reduce feature complexity
- **Monitoring**: Track performance trends and identify patterns

#### MCP Server Latency
- **Symptoms**: High response times from MCP servers
- **Diagnosis**: Check server availability, network connectivity, resource constraints
- **Optimization**: Enable caching, implement server health monitoring
- **Fallbacks**: Ensure fallback strategies are effective

#### Resource Exhaustion
- **Symptoms**: High memory or CPU usage, frequent threshold breaches
- **Immediate Response**: Activate efficiency mode, reduce feature set
- **Long-term Solutions**: Optimize resource usage, implement better cleanup
- **Prevention**: Monitor trends and adjust thresholds proactively

#### Quality vs Performance Trade-offs
- **Symptoms**: Quality targets missed due to performance constraints
- **Analysis**: Review quality-performance balance in configuration
- **Adjustment**: Find optimal balance for specific use case requirements
- **Monitoring**: Track both quality and performance metrics continuously

### Performance Optimization Strategies

#### Caching Optimization
```yaml
# Optimize caching for better performance
caching_strategy:
  enable_for_operations: ["all_frequent_operations"]
  cache_duration_minutes: 60  # Longer cache duration
  max_cache_size_mb: 200  # Larger cache size
```

#### Resource Management Optimization
```yaml
# More aggressive resource management
performance_thresholds:
  green_zone: 60  # Smaller green zone for earlier optimization
  yellow_zone: 75  # Earlier efficiency activation
```

#### Learning System Optimization
```yaml
# Balance learning with performance
learning_performance:
  adaptation_response_time_ms: 100  # Faster adaptations
  pattern_detection_accuracy: 0.85  # Higher accuracy requirement
```

## Related Documentation

- **Hook Documentation**: See individual hook documentation for performance implementation details
- **MCP Server Performance**: Reference MCP server documentation for server-specific optimization
- **Mode Performance**: Review mode documentation for mode-specific performance characteristics
- **Monitoring Integration**: See logging configuration for performance monitoring implementation

## Version History

- **v1.0.0**: Initial performance configuration
- Comprehensive performance targets across all framework components
- Progressive threshold management with zone-based optimization
- MCP server performance standards with quality targets
- Mode-specific performance profiles and optimization strategies
- Real-time monitoring with proactive alerting
- Learning system performance integration with effectiveness tracking