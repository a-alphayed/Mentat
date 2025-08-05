# Session Configuration (`session.yaml`)

## Overview

The `session.yaml` file defines session lifecycle management and analytics configuration for the SuperClaude-Lite framework. This configuration controls session initialization, termination, project detection, intelligence activation, and comprehensive session analytics across the framework.

## Purpose and Role

The session configuration serves as:
- **Session Lifecycle Manager**: Controls initialization and termination patterns for optimal user experience
- **Project Intelligence Engine**: Automatically detects project types and activates appropriate framework features
- **Mode Activation Coordinator**: Manages intelligent activation of behavioral modes based on context
- **Analytics and Learning System**: Tracks session effectiveness and enables continuous framework improvement
- **Performance Optimizer**: Manages session-level performance targets and resource utilization

## Configuration Structure

### 1. Session Lifecycle Configuration (`session_lifecycle`)

#### Initialization Settings
```yaml
initialization:
  performance_target_ms: 50
  auto_project_detection: true
  context_loading_strategy: "selective"
  framework_exclusion_enabled: true
  
  default_modes:
    - "adaptive_intelligence"
    - "performance_monitoring"
  
  intelligence_activation:
    pattern_detection: true
    mcp_routing: true
    learning_integration: true
    compression_optimization: true
```

**Performance Target**: 50ms initialization for immediate user engagement
**Selective Loading**: Loads only necessary context for fast startup
**Framework Exclusion**: Protects framework content from modification
**Default Modes**: Activates adaptive intelligence and performance monitoring by default

#### Termination Settings
```yaml
termination:
  performance_target_ms: 200
  analytics_generation: true
  learning_consolidation: true
  session_persistence: true
  cleanup_optimization: true
```

**Analytics Generation**: Creates comprehensive session analytics on termination
**Learning Consolidation**: Consolidates session learnings for future improvement
**Session Persistence**: Saves session state for potential recovery
**Cleanup Optimization**: Optimizes resource cleanup for performance

### 2. Project Type Detection (`project_detection`)

#### File Indicators
```yaml
file_indicators:
  nodejs:
    - "package.json"
    - "node_modules/"
    - "yarn.lock"
    - "pnpm-lock.yaml"
  
  python:
    - "pyproject.toml"
    - "setup.py"
    - "requirements.txt"
    - "__pycache__/"
    - ".py"
  
  rust:
    - "Cargo.toml"
    - "Cargo.lock"
    - "src/main.rs"
    - "src/lib.rs"
  
  go:
    - "go.mod"
    - "go.sum"
    - "main.go"
  
  web_frontend:
    - "index.html"
    - "public/"
    - "dist/"
    - "build/"
    - "src/components/"
```

**Purpose**: Automatically detects project type based on characteristic files
**Multi-Language Support**: Supports major programming languages and frameworks
**Progressive Detection**: Multiple indicators increase detection confidence

#### Framework Detection
```yaml
framework_detection:
  react:
    - "react"
    - "next.js"
    - "@types/react"
  
  vue:
    - "vue"
    - "nuxt"
    - "@vue/cli"
  
  angular:
    - "@angular/core"
    - "angular.json"
  
  express:
    - "express"
    - "app.js"
    - "server.js"
```

**Framework Intelligence**: Detects specific frameworks within project types
**Package Analysis**: Analyzes package.json and similar files for framework indicators
**Enhanced Context**: Framework detection enables specialized optimizations

### 3. Intelligence Activation Rules (`intelligence_activation`)

#### Mode Detection Patterns
```yaml
mode_detection:
  brainstorming:
    triggers:
      - "new project"
      - "not sure"
      - "thinking about"
      - "explore"
      - "brainstorm"
    confidence_threshold: 0.7
    auto_activate: true
  
  task_management:
    triggers:
      - "multiple files"
      - "complex operation"
      - "system-wide"
      - "comprehensive"
    file_count_threshold: 3
    complexity_threshold: 0.4
    auto_activate: true
  
  token_efficiency:
    triggers:
      - "resource constraint"
      - "brevity"
      - "compressed"
      - "efficient"
    resource_threshold_percent: 75
    conversation_length_threshold: 100
    auto_activate: true
```

**Automatic Mode Activation**: Intelligent detection and activation based on user patterns
**Confidence Thresholds**: Ensures accurate mode selection
**Context-Aware**: Considers project characteristics and resource constraints

#### MCP Server Activation
```yaml
mcp_server_activation:
  context7:
    triggers:
      - "library"
      - "documentation"
      - "framework"
      - "api reference"
    project_indicators:
      - "external_dependencies"
      - "framework_detected"
    auto_activate: true
  
  sequential:
    triggers:
      - "analyze"
      - "debug"
      - "complex"
      - "systematic"
    complexity_threshold: 0.6
    auto_activate: true
  
  magic:
    triggers:
      - "component"
      - "ui"
      - "frontend"
      - "design"
    project_type_match: ["web_frontend", "react", "vue", "angular"]
    auto_activate: true
  
  serena:
    triggers:
      - "navigate"
      - "find"
      - "search"
      - "analyze"
    file_count_min: 5
    complexity_min: 0.4
    auto_activate: true
```

**Intelligent Server Selection**: Automatic MCP server activation based on task requirements
**Project Context**: Server selection considers project type and characteristics
**Threshold Management**: Prevents unnecessary server activation through intelligent thresholds

### 4. Session Analytics Configuration (`session_analytics`)

#### Performance Tracking
```yaml
performance_tracking:
  enabled: true
  metrics:
    - "operation_count"
    - "tool_usage_patterns"
    - "mcp_server_effectiveness"
    - "error_rates"
    - "completion_times"
    - "resource_utilization"
```

**Comprehensive Metrics**: Tracks all key performance dimensions
**Usage Patterns**: Analyzes tool and server usage for optimization
**Error Tracking**: Monitors error rates for reliability improvement

#### Effectiveness Measurement
```yaml
effectiveness_measurement:
  enabled: true
  factors:
    productivity: "weight: 0.4"
    quality: "weight: 0.3"
    user_satisfaction: "weight: 0.2"
    learning_value: "weight: 0.1"
```

**Weighted Effectiveness**: Balanced assessment across multiple factors
**Productivity Focus**: Highest weight on productivity outcomes
**Quality Assurance**: Significant weight on quality maintenance
**User Experience**: Important consideration for user satisfaction
**Learning Value**: Tracks framework learning and improvement

#### Learning Consolidation
```yaml
learning_consolidation:
  enabled: true
  pattern_detection: true
  adaptation_creation: true
  effectiveness_feedback: true
  insight_generation: true
```

**Pattern Learning**: Identifies successful patterns for replication
**Adaptive Improvement**: Creates adaptations based on session outcomes
**Feedback Integration**: Incorporates effectiveness feedback into learning
**Insight Generation**: Generates actionable insights for framework improvement

### 5. Session Persistence (`session_persistence`)

#### Storage Strategy
```yaml
enabled: true
storage_strategy: "intelligent_compression"
retention_policy:
  session_data_days: 90
  analytics_data_days: 365
  learning_data_persistent: true

compression_settings:
  session_metadata: "efficient" # 40-70% compression
  analytics_data: "compressed" # 70-85% compression
  learning_data: "minimal" # Preserve learning quality
```

**Intelligent Compression**: Applies appropriate compression based on data type
**Retention Management**: Balances storage with analytical value
**Learning Preservation**: Maintains high fidelity for learning data

#### Cleanup Automation
```yaml
cleanup_automation:
  enabled: true
  old_session_cleanup: true
  max_sessions_retained: 50
  storage_optimization: true
```

**Automatic Cleanup**: Prevents storage bloat through automated cleanup
**Session Limits**: Maintains reasonable number of retained sessions
**Storage Optimization**: Continuously optimizes storage usage

### 6. Notification Processing (`notifications`)

#### Core Notification Settings
```yaml
enabled: true
just_in_time_loading: true
pattern_updates: true
intelligence_updates: true

priority_handling:
  critical: "immediate_processing"
  high: "fast_track_processing"
  medium: "standard_processing"
  low: "background_processing"
```

**Just-in-Time Loading**: Loads documentation and patterns as needed
**Priority Processing**: Handles notifications based on priority levels
**Intelligence Updates**: Updates framework intelligence based on new patterns

#### Caching Strategy
```yaml
caching_strategy:
  documentation_cache_minutes: 30
  pattern_cache_minutes: 60
  intelligence_cache_minutes: 15
```

**Documentation Caching**: 30-minute cache for documentation lookup
**Pattern Caching**: 60-minute cache for pattern recognition
**Intelligence Caching**: 15-minute cache for intelligence updates

### 7. Task Management Integration (`task_management`)

#### Delegation Strategies
```yaml
enabled: true
delegation_strategies:
  files: "file_based_delegation"
  folders: "directory_based_delegation"
  auto: "intelligent_auto_detection"

wave_orchestration:
  enabled: true
  complexity_threshold: 0.4
  file_count_threshold: 3
  operation_types_threshold: 2
```

**Multi-Strategy Support**: Supports file, folder, and auto-delegation strategies
**Wave Orchestration**: Enables complex multi-step operation coordination
**Intelligent Thresholds**: Activates advanced features based on operation complexity

#### Performance Optimization
```yaml
performance_optimization:
  parallel_execution: true
  resource_management: true
  coordination_efficiency: true
```

**Parallel Processing**: Enables parallel execution for performance
**Resource Management**: Optimizes resource allocation across tasks
**Coordination**: Efficient coordination of multiple operations

### 8. User Experience Configuration (`user_experience`)

#### Session Feedback
```yaml
session_feedback:
  enabled: true
  satisfaction_tracking: true
  improvement_suggestions: true
```

**Satisfaction Tracking**: Monitors user satisfaction throughout session
**Improvement Suggestions**: Provides suggestions for enhanced experience

#### Personalization
```yaml
personalization:
  enabled: true
  preference_learning: true
  adaptation_application: true
  context_awareness: true
```

**Preference Learning**: Learns user preferences over time
**Adaptive Application**: Applies learned preferences to improve experience
**Context Awareness**: Considers context in personalization decisions

#### Progressive Enhancement
```yaml
progressive_enhancement:
  enabled: true
  capability_discovery: true
  feature_introduction: true
  learning_curve_optimization: true
```

**Capability Discovery**: Gradually discovers and introduces new capabilities
**Feature Introduction**: Introduces features at appropriate times
**Learning Curve**: Optimizes learning curve for user adoption

### 9. Performance Targets (`performance_targets`)

#### Session Performance
```yaml
session_start_ms: 50
session_stop_ms: 200
context_loading_ms: 500
analytics_generation_ms: 1000
```

**Fast Startup**: 50ms session start for immediate engagement
**Efficient Termination**: 200ms session stop with analytics
**Context Loading**: 500ms context loading for comprehensive initialization
**Analytics**: 1000ms analytics generation for comprehensive insights

#### Efficiency Targets
```yaml
efficiency_targets:
  productivity_score: 0.7
  quality_score: 0.8
  satisfaction_score: 0.7
  learning_value: 0.6
```

**Productivity**: 70% productivity score target
**Quality**: 80% quality score maintenance
**Satisfaction**: 70% user satisfaction target
**Learning**: 60% learning value extraction

#### Resource Utilization
```yaml
resource_utilization:
  memory_efficient: true
  cpu_optimization: true
  token_management: true
  storage_optimization: true
```

**Comprehensive Optimization**: Optimizes all resource dimensions
**Token Management**: Intelligent token usage optimization
**Storage Efficiency**: Efficient storage utilization and cleanup

### 10. Error Handling and Recovery (`error_handling`)

#### Core Error Handling
```yaml
graceful_degradation: true
fallback_strategies: true
error_learning: true
recovery_optimization: true
```

**Graceful Degradation**: Maintains functionality during errors
**Fallback Strategies**: Multiple fallback options for resilience
**Error Learning**: Learns from errors to prevent recurrence

#### Session Recovery
```yaml
session_recovery:
  auto_recovery: true
  state_preservation: true
  context_restoration: true
  learning_retention: true
```

**Automatic Recovery**: Attempts automatic recovery from errors
**State Preservation**: Preserves session state during recovery
**Context Restoration**: Restores context after recovery
**Learning Retention**: Maintains learning data through recovery

#### Error Pattern Detection
```yaml
error_patterns:
  detection: true
  prevention: true
  learning_integration: true
  adaptation_triggers: true
```

**Pattern Detection**: Identifies recurring error patterns
**Prevention**: Implements prevention strategies for known patterns
**Learning Integration**: Integrates error learning with overall framework learning

## Integration Points

### 1. Hook Integration (`integration`)

#### MCP Server Coordination
```yaml
mcp_servers:
  coordination: "seamless"
  fallback_handling: "automatic"
  performance_monitoring: "continuous"
```

**Seamless Coordination**: Smooth integration across all MCP servers
**Automatic Fallbacks**: Automatic fallback handling for server issues
**Continuous Monitoring**: Real-time performance monitoring

#### Learning Engine Integration
```yaml
learning_engine:
  session_learning: true
  pattern_recognition: true
  effectiveness_tracking: true
  adaptation_application: true
```

**Session Learning**: Comprehensive learning from session patterns
**Pattern Recognition**: Identifies successful session patterns
**Effectiveness Tracking**: Tracks session effectiveness over time
**Adaptation**: Applies learned patterns to improve future sessions

#### Quality Gates Integration
```yaml
quality_gates:
  session_validation: true
  analytics_verification: true
  learning_quality_assurance: true
```

**Session Validation**: Validates session outcomes against quality standards
**Analytics Verification**: Ensures analytics accuracy and completeness
**Learning QA**: Quality assurance for learning data and insights

### 2. Development Support (`development_support`)

```yaml
session_debugging: true
performance_profiling: true
analytics_validation: true
learning_verification: true

metrics_collection:
  detailed_timing: true
  resource_tracking: true
  effectiveness_measurement: true
  quality_assessment: true
```

**Debugging Support**: Enhanced debugging capabilities for development
**Performance Profiling**: Detailed performance analysis tools
**Metrics Collection**: Comprehensive metrics for analysis and optimization

## Performance Implications

### 1. Session Lifecycle Performance

#### Initialization Impact
- **Startup Time**: 45-55ms typical session initialization
- **Context Loading**: 400-600ms for selective context loading
- **Memory Usage**: 50-100MB initial memory allocation
- **CPU Usage**: 20-40% CPU during initialization

#### Termination Impact
- **Analytics Generation**: 800ms-1.2s for comprehensive analytics
- **Learning Consolidation**: 200-500ms for learning data processing
- **Cleanup Operations**: 100-300ms for resource cleanup
- **Storage Operations**: 50-200ms for session persistence

### 2. Project Detection Performance

#### Detection Speed
- **File System Scanning**: 10-50ms for project type detection
- **Framework Analysis**: 20-100ms for framework detection
- **Dependency Analysis**: 50-200ms for dependency graph analysis
- **Total Detection**: 100-400ms for complete project analysis

#### Memory Impact
- **Detection Data**: 10-50KB for project detection information
- **Framework Metadata**: 20-100KB for framework-specific data
- **Dependency Cache**: 100KB-1MB for dependency information

### 3. Analytics and Learning Performance

#### Analytics Generation
- **Metrics Collection**: 50-200ms for comprehensive metrics gathering
- **Effectiveness Calculation**: 100-500ms for effectiveness analysis
- **Pattern Analysis**: 200ms-1s for pattern recognition
- **Insight Generation**: 300ms-2s for actionable insights

#### Learning System Impact
- **Pattern Learning**: 100-500ms for pattern updates
- **Adaptation Creation**: 200ms-1s for adaptation generation
- **Effectiveness Feedback**: 50-200ms for feedback integration
- **Storage Updates**: 100-400ms for learning data persistence

## Configuration Best Practices

### 1. Production Session Configuration
```yaml
# Optimize for reliability and performance
session_lifecycle:
  initialization:
    performance_target_ms: 75  # Slightly relaxed for stability
    framework_exclusion_enabled: true  # Always protect framework
  
session_analytics:
  performance_tracking:
    enabled: true  # Essential for production monitoring
  
session_persistence:
  retention_policy:
    session_data_days: 30  # Shorter retention for production
    analytics_data_days: 180  # Sufficient for trend analysis
```

### 2. Development Session Configuration
```yaml
# Enhanced debugging and learning
development_support:
  session_debugging: true
  performance_profiling: true
  detailed_timing: true

session_analytics:
  learning_consolidation:
    effectiveness_feedback: true
    adaptation_creation: true  # Enable aggressive learning
```

### 3. Performance-Optimized Configuration
```yaml
# Minimize overhead for performance-critical environments
session_lifecycle:
  initialization:
    performance_target_ms: 25  # Aggressive target
    context_loading_strategy: "minimal"  # Minimal context loading

session_analytics:
  performance_tracking:
    metrics: ["operation_count", "completion_times"]  # Essential metrics only
```

### 4. Learning-Optimized Configuration
```yaml
# Maximum learning and adaptation
session_analytics:
  learning_consolidation:
    enabled: true
    pattern_detection: true
    adaptation_creation: true
    insight_generation: true

user_experience:
  personalization:
    preference_learning: true
    adaptation_application: true
```

## Troubleshooting

### Common Session Issues

#### Slow Session Initialization
- **Symptoms**: Session startup exceeds 50ms target consistently
- **Analysis**: Check project detection performance, context loading strategy
- **Solutions**: Optimize project detection patterns, reduce initial context loading
- **Monitoring**: Track initialization components and identify bottlenecks

#### Project Detection Failures
- **Symptoms**: Incorrect project type detection or missing framework detection
- **Diagnosis**: Review project indicators and framework patterns
- **Resolution**: Add missing patterns, adjust detection confidence thresholds
- **Validation**: Test detection with various project structures

#### Analytics Generation Issues
- **Symptoms**: Slow or incomplete analytics generation at session end
- **Investigation**: Check metrics collection performance and data completeness
- **Optimization**: Reduce analytics complexity, optimize metrics calculation
- **Quality**: Ensure analytics accuracy while maintaining performance

#### Learning System Problems
- **Symptoms**: No learning observed, ineffective adaptations
- **Analysis**: Review learning data collection and pattern recognition
- **Enhancement**: Adjust learning thresholds, improve pattern detection
- **Validation**: Test learning effectiveness with controlled scenarios

### Performance Troubleshooting

#### Memory Usage Issues
- **Monitoring**: Track session memory usage patterns and growth
- **Optimization**: Optimize context loading, implement better cleanup
- **Limits**: Set appropriate memory limits and cleanup triggers
- **Analysis**: Profile memory usage during different session phases

#### CPU Usage Problems
- **Identification**: Monitor CPU usage during session operations
- **Optimization**: Optimize project detection, reduce analytics complexity
- **Balancing**: Balance functionality with CPU usage requirements
- **Profiling**: Use profiling tools to identify CPU bottlenecks

#### Storage and Persistence Issues
- **Management**: Monitor storage usage and cleanup effectiveness
- **Optimization**: Optimize compression settings, adjust retention policies
- **Maintenance**: Implement regular cleanup and optimization routines
- **Analysis**: Track storage growth patterns and optimize accordingly

## Related Documentation

- **Session Lifecycle**: See SESSION_LIFECYCLE.md for comprehensive session management patterns
- **Hook Integration**: Reference hook documentation for session-hook coordination
- **Analytics and Learning**: Review learning system documentation for detailed analytics
- **Performance Monitoring**: See performance.yaml.md for performance targets and monitoring

## Version History

- **v1.0.0**: Initial session configuration
- Comprehensive session lifecycle management with 50ms initialization target
- Multi-language project detection with framework intelligence
- Automatic mode and MCP server activation based on context
- Session analytics with effectiveness measurement and learning consolidation
- User experience optimization with personalization and progressive enhancement
- Error handling and recovery with pattern detection and prevention