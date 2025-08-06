# User Experience Configuration (`user_experience.yaml`)

## Overview

The `user_experience.yaml` file configures UX optimization, project detection, and user-centric intelligence patterns for the SuperClaude-Lite framework. This configuration enables intelligent user experience through smart defaults, proactive assistance, and adaptive interfaces.

## Purpose and Role

This configuration provides:
- **Project Detection**: Automatically detect project types and optimize accordingly
- **User Preference Learning**: Learn and adapt to user behavior patterns
- **Proactive Assistance**: Provide intelligent suggestions and contextual help
- **Smart Defaults**: Generate context-aware default configurations
- **Error Recovery**: Intelligent error handling with user-focused recovery

## Configuration Structure

### 1. Project Type Detection

#### Frontend Frameworks
```yaml
react_project:
  file_indicators:
    - "package.json"
    - "*.tsx"
    - "*.jsx"
    - "react"      # in package.json dependencies
  directory_indicators:
    - "src/components"
    - "public"
    - "node_modules"
  confidence_threshold: 0.8
  recommendations:
    mcp_servers: ["magic", "context7", "playwright"]
    compression_level: "minimal"
    performance_focus: "ui_responsiveness"
```

**Detection Logic**: File and directory pattern matching with confidence scoring
**Recommendations**: Automatic MCP server selection and optimization settings
**Thresholds**: Confidence levels for reliable project type detection

#### Backend Frameworks
```yaml
python_project:
  file_indicators:
    - "requirements.txt"
    - "pyproject.toml"
    - "*.py"
  recommendations:
    mcp_servers: ["serena", "sequential", "context7"]
    compression_level: "standard"
    validation_level: "enhanced"
```

**Language Detection**: Python, Node.js, and other backend frameworks
**Tool Selection**: Appropriate MCP servers for backend development
**Configuration**: Optimized settings for backend workflows

### 2. User Preference Intelligence

#### Preference Learning
```yaml
preference_learning:
  interaction_patterns:
    command_preferences:
      track_command_usage: true
      track_flag_preferences: true
      track_workflow_patterns: true
      learning_window: 100      # operations
```

**Pattern Tracking**: Monitor user command and workflow preferences
**Learning Window**: Number of operations used for preference analysis
**Behavioral Analysis**: Speed vs quality preferences, detail level preferences

#### Adaptation Strategies
```yaml
adaptation_strategies:
  speed_focused_user:
    optimizations: ["aggressive_caching", "parallel_execution", "reduced_analysis"]
    ui_changes: ["shorter_responses", "quick_suggestions", "minimal_explanations"]
  quality_focused_user:
    optimizations: ["comprehensive_analysis", "detailed_validation", "thorough_documentation"]
    ui_changes: ["detailed_responses", "comprehensive_suggestions", "full_explanations"]
```

**User Profiles**: Speed-focused, quality-focused, and efficiency-focused adaptations
**Optimization**: Performance tuning based on user preferences
**Interface Adaptation**: UI changes to match user preferences

### 3. Proactive User Assistance

#### Intelligent Suggestions
```yaml
optimization_suggestions:
  - trigger: {repeated_operations: ">5", same_pattern: true}
    suggestion: "Consider creating a script or alias for this repeated operation"
    confidence: 0.8
    category: "workflow_optimization"
  - trigger: {performance_issues: "detected", duration: ">3_sessions"}
    suggestion: "Performance optimization recommendations available"
    action: "show_performance_guide"
    confidence: 0.9
```

**Pattern Recognition**: Detect repeated operations and inefficiencies
**Contextual Suggestions**: Provide relevant optimization recommendations
**Confidence Scoring**: Reliability ratings for suggestions

#### Contextual Help
```yaml
help_triggers:
  - context: {new_user: true, session_count: "<5"}
    help_type: "onboarding_guidance"
    content: "Getting started tips and best practices"
  - context: {error_rate: ">10%", recent_errors: ">3"}
    help_type: "troubleshooting_assistance"
    content: "Common error solutions and debugging tips"
```

**Trigger-Based Help**: Automatic help based on user context and behavior
**Adaptive Content**: Different help types for different situations
**User Journey**: Onboarding, troubleshooting, and advanced guidance

### 4. Smart Defaults Intelligence

#### Project-Based Defaults
```yaml
project_based_defaults:
  react_project:
    default_mcp_servers: ["magic", "context7"]
    default_compression: "minimal"
    default_analysis_depth: "ui_focused"
    default_validation: "component_focused"
  python_project:
    default_mcp_servers: ["serena", "sequential"]
    default_compression: "standard"
    default_analysis_depth: "comprehensive"
    default_validation: "enhanced"
```

**Context-Aware Configuration**: Automatic configuration based on detected project type
**Framework Optimization**: Defaults optimized for specific development frameworks
**Workflow Enhancement**: Pre-configured settings for common development patterns

#### Dynamic Configuration
```yaml
configuration_adaptation:
  performance_based:
    - condition: {system_performance: "high"}
      adjustments: {analysis_depth: "comprehensive", features: "all_enabled"}
    - condition: {system_performance: "low"}
      adjustments: {analysis_depth: "essential", features: "performance_focused"}
```

**Performance Adaptation**: Adjust configuration based on system performance
**Expertise-Based**: Different defaults for beginner vs expert users
**Resource Management**: Optimize based on available system resources

### 5. Error Recovery Intelligence

#### Error Classification
```yaml
error_classification:
  user_errors:
    - type: "syntax_error"
      recovery: "suggest_correction"
      user_guidance: "detailed"
    - type: "configuration_error"
      recovery: "auto_fix_with_approval"
      user_guidance: "educational"
  system_errors:
    - type: "performance_degradation"
      recovery: "automatic_optimization"
      user_notification: "informational"
```

**Error Types**: Classification of user vs system errors
**Recovery Strategies**: Appropriate recovery actions for each error type
**User Guidance**: Educational vs informational responses

#### Recovery Learning
```yaml
recovery_effectiveness:
  track_recovery_success: true
  learn_recovery_patterns: true
  improve_recovery_strategies: true
user_recovery_preferences:
  learn_preferred_recovery: true
  adapt_recovery_approach: true
  personalize_error_handling: true
```

**Pattern Learning**: Learn from successful error recovery patterns
**Personalization**: Adapt error handling to user preferences
**Continuous Improvement**: Improve recovery strategies over time

### 6. User Expertise Detection

#### Behavioral Indicators
```yaml
expertise_indicators:
  command_proficiency:
    indicators: ["advanced_flags", "complex_operations", "custom_configurations"]
    weight: 0.4
  error_recovery_ability:
    indicators: ["self_correction", "minimal_help_needed", "independent_problem_solving"]
    weight: 0.3
  workflow_sophistication:
    indicators: ["efficient_workflows", "automation_usage", "advanced_patterns"]
    weight: 0.3
```

**Multi-Factor Detection**: Command proficiency, error recovery, workflow sophistication
**Weighted Scoring**: Balanced assessment of different expertise indicators
**Dynamic Assessment**: Continuous evaluation of user expertise level

#### Expertise Adaptation
```yaml
beginner_adaptations:
  interface: ["detailed_explanations", "step_by_step_guidance", "comprehensive_warnings"]
  defaults: ["safe_options", "guided_workflows", "educational_mode"]
expert_adaptations:
  interface: ["minimal_explanations", "advanced_options", "efficiency_focused"]
  defaults: ["maximum_automation", "performance_optimization", "minimal_interruptions"]
```

**Progressive Interface**: Interface complexity matches user expertise
**Default Optimization**: Appropriate defaults for each expertise level
**Learning Curve**: Smooth progression from beginner to expert experience

### 7. Satisfaction Intelligence

#### Satisfaction Metrics
```yaml
satisfaction_metrics:
  task_completion_rate:
    weight: 0.3
    target_threshold: 0.85
  error_resolution_speed:
    weight: 0.25
    target_threshold: "fast"
  feature_adoption_rate:
    weight: 0.2
    target_threshold: 0.6
```

**Multi-Dimensional Tracking**: Completion rates, error resolution, feature adoption
**Weighted Scoring**: Balanced assessment of satisfaction factors
**Target Thresholds**: Performance targets for satisfaction metrics

#### Optimization Strategies
```yaml
optimization_strategies:
  low_satisfaction_triggers:
    - trigger: {completion_rate: "<0.7"}
      action: "simplify_workflows"
      priority: "high"
    - trigger: {error_rate: ">15%"}
      action: "improve_error_prevention"
      priority: "critical"
```

**Trigger-Based Optimization**: Automatic improvements based on satisfaction metrics
**Priority Management**: Critical vs high vs medium priority improvements
**Continuous Optimization**: Ongoing satisfaction improvement processes

### 8. Personalization Engine

#### Interface Personalization
```yaml
interface_personalization:
  layout_preferences:
    learn_preferred_layouts: true
    adapt_information_density: true
    customize_interaction_patterns: true
  content_personalization:
    learn_content_preferences: true
    adapt_explanation_depth: true
    customize_suggestion_types: true
```

**Adaptive Interface**: Layout and content adapted to user preferences
**Information Density**: Adjust detail level based on user preferences
**Interaction Patterns**: Customize based on user behavior patterns

#### Workflow Optimization
```yaml
personal_workflow_learning:
  common_task_patterns: true
  workflow_efficiency_analysis: true
  personalized_shortcuts: true
workflow_recommendations:
  suggest_workflow_improvements: true
  recommend_automation_opportunities: true
  provide_efficiency_insights: true
```

**Pattern Learning**: Learn individual user workflow patterns
**Efficiency Analysis**: Identify optimization opportunities
**Personalized Recommendations**: Workflow improvements tailored to user

## Configuration Guidelines

### Project Detection Tuning
- **Confidence Thresholds**: Higher thresholds reduce false positives
- **File Indicators**: Add project-specific files for better detection
- **Directory Structure**: Include common directory patterns
- **Recommendations**: Align MCP server selection with project needs

### Preference Learning
- **Learning Window**: Adjust based on user activity level
- **Adaptation Speed**: Balance responsiveness with stability
- **Pattern Recognition**: Include relevant behavioral indicators
- **Privacy**: Ensure user preference data remains private

### Proactive Assistance
- **Suggestion Timing**: Avoid interrupting user flow
- **Relevance**: Ensure suggestions are contextually appropriate
- **Frequency**: Balance helpfulness with intrusiveness
- **User Control**: Allow users to adjust assistance level

## Integration Points

### Hook Integration
- **Session Start**: Project detection and user preference loading
- **Pre-Tool Use**: Context-aware defaults and proactive suggestions
- **Post-Tool Use**: Satisfaction tracking and pattern learning

### MCP Server Coordination
- **Server Selection**: Project-based and preference-based routing
- **Configuration**: Context-aware MCP server configuration
- **Performance**: User preference-based optimization

## Troubleshooting

### Project Detection Issues
- **False Positives**: Increase confidence thresholds
- **False Negatives**: Add more file/directory indicators
- **Conflicting Types**: Review indicator specificity

### Preference Learning Problems
- **Slow Adaptation**: Reduce learning window size
- **Wrong Preferences**: Review behavioral indicators
- **Privacy Concerns**: Ensure data anonymization

### Satisfaction Issues
- **Low Completion Rates**: Review workflow complexity
- **High Error Rates**: Improve error prevention
- **Poor Feature Adoption**: Enhance feature discoverability

## Related Documentation

- **Project Detection**: Framework project type detection patterns
- **User Analytics**: User behavior analysis and learning systems
- **Error Recovery**: Comprehensive error handling and recovery strategies