# Validation Configuration (`validation.yaml`)

## Overview

The `validation.yaml` file defines comprehensive quality validation rules and standards for the SuperClaude-Lite framework. This configuration implements RULES.md and PRINCIPLES.md enforcement through automated validation cycles, quality standards, and continuous improvement mechanisms.

## Purpose and Role

The validation configuration serves as:
- **Rules Enforcement Engine**: Implements SuperClaude RULES.md validation with automatic detection and correction
- **Principles Alignment Validator**: Ensures adherence to PRINCIPLES.md through systematic validation
- **Quality Standards Framework**: Establishes minimum quality thresholds across code, security, performance, and maintainability
- **Validation Workflow Orchestrator**: Manages pre-validation, post-validation, and continuous validation cycles
- **Learning Integration System**: Incorporates validation results into framework learning and adaptation

## Configuration Structure

### 1. Core SuperClaude Rules Validation (`rules_validation`)

#### File Operations Validation
```yaml
file_operations:
  read_before_write:
    enabled: true
    severity: "error"
    message: "RULES violation: No Read operation detected before Write/Edit"
    check_recent_tools: 3
    exceptions: ["new_file_creation"]
```

**Purpose**: Enforces mandatory Read operations before Write/Edit operations
**Severity**: Error level prevents execution without compliance
**Recent Tools Check**: Examines last 3 tool operations for Read operations
**Exceptions**: Allows new file creation without prior Read requirement

```yaml
absolute_paths_only:
  enabled: true
  severity: "error"
  message: "RULES violation: Relative path used"
  path_parameters: ["file_path", "path", "directory", "output_path"]
  allowed_prefixes: ["http://", "https://", "/"]
```

**Purpose**: Prevents security issues through relative path usage
**Parameter Validation**: Checks all path-related parameters
**Allowed Prefixes**: Permits absolute paths and URLs only

```yaml
validate_before_execution:
  enabled: true
  severity: "warning"
  message: "RULES recommendation: High-risk operation should include validation"
  high_risk_operations: ["delete", "refactor", "deploy", "migrate"]
  complexity_threshold: 0.7
```

**Purpose**: Recommends validation before high-risk operations
**Risk Assessment**: Identifies operations requiring additional validation
**Complexity Consideration**: Higher complexity operations require validation

#### Security Requirements Validation
```yaml
security_requirements:
  input_validation:
    enabled: true
    severity: "error"
    message: "RULES violation: User input handling without validation"
    check_patterns: ["user_input", "external_data", "api_input"]
  
  no_hardcoded_secrets:
    enabled: true
    severity: "critical"
    message: "RULES violation: Hardcoded sensitive information detected"
    patterns: ["password", "api_key", "secret", "token"]
  
  production_safety:
    enabled: true
    severity: "error"
    message: "RULES violation: Unsafe operation in production context"
    production_indicators: ["is_production", "prod_env", "production"]
```

**Input Validation**: Ensures user input is properly validated
**Secret Detection**: Prevents hardcoded sensitive information
**Production Safety**: Protects against unsafe production operations

### 2. SuperClaude Principles Validation (`principles_validation`)

#### Evidence Over Assumptions
```yaml
evidence_over_assumptions:
  enabled: true
  severity: "warning"
  message: "PRINCIPLES: Provide evidence to support assumptions"
  check_for_assumptions: true
  require_evidence: true
  confidence_threshold: 0.7
```

**Purpose**: Enforces evidence-based reasoning and decision-making
**Assumption Detection**: Identifies assumptions requiring evidence support
**Confidence Threshold**: 70% confidence required for assumption validation

#### Code Over Documentation
```yaml
code_over_documentation:
  enabled: true
  severity: "warning"
  message: "PRINCIPLES: Documentation should follow working code, not precede it"
  documentation_operations: ["document", "readme", "guide"]
  require_working_code: true
```

**Purpose**: Ensures documentation follows working code implementation
**Documentation Operations**: Identifies documentation-focused operations
**Working Code Requirement**: Validates existence of working code before documentation

#### Efficiency Over Verbosity
```yaml
efficiency_over_verbosity:
  enabled: true
  severity: "suggestion"
  message: "PRINCIPLES: Consider token efficiency techniques for large outputs"
  output_size_threshold: 5000
  verbosity_indicators: ["repetitive_content", "unnecessary_detail"]
```

**Purpose**: Promotes token efficiency and concise communication
**Size Threshold**: 5000 tokens triggers efficiency recommendations
**Verbosity Detection**: Identifies repetitive or unnecessarily detailed content

#### Test-Driven Development
```yaml
test_driven_development:
  enabled: true
  severity: "warning"
  message: "PRINCIPLES: Logic changes should include tests"
  logic_operations: ["write", "edit", "generate", "implement"]
  test_file_patterns: ["*test*", "*spec*", "test_*", "*_test.*"]
```

**Purpose**: Promotes test-driven development practices
**Logic Operations**: Identifies operations requiring test coverage
**Test Pattern Recognition**: Recognizes various test file naming conventions

#### Single Responsibility Principle
```yaml
single_responsibility:
  enabled: true
  severity: "suggestion"
  message: "PRINCIPLES: Functions/classes should have single responsibility"
  complexity_indicators: ["multiple_purposes", "large_function", "many_parameters"]
```

**Purpose**: Enforces single responsibility principle in code design
**Complexity Detection**: Identifies functions/classes violating single responsibility

#### Error Handling Requirement
```yaml
error_handling_required:
  enabled: true
  severity: "warning"
  message: "PRINCIPLES: Error handling not implemented"
  critical_operations: ["write", "edit", "deploy", "api_calls"]
```

**Purpose**: Ensures proper error handling in critical operations
**Critical Operations**: Identifies operations requiring error handling

### 3. Quality Standards (`quality_standards`)

#### Code Quality Standards
```yaml
code_quality:
  minimum_score: 0.7
  factors:
    - syntax_correctness
    - logical_consistency
    - error_handling_presence
    - documentation_adequacy
    - test_coverage
```

**Minimum Score**: 70% quality score required for code acceptance
**Multi-Factor Assessment**: Comprehensive quality evaluation across multiple dimensions

#### Security Compliance Standards
```yaml
security_compliance:
  minimum_score: 0.8
  checks:
    - input_validation
    - output_sanitization
    - authentication_checks
    - authorization_verification
    - secure_communication
```

**Security Score**: 80% security compliance required (higher than code quality)
**Comprehensive Security**: Covers all major security aspects

#### Performance Standards
```yaml
performance_standards:
  response_time_threshold_ms: 2000
  resource_efficiency_min: 0.6
  optimization_indicators:
    - algorithm_efficiency
    - memory_usage
    - processing_speed
```

**Response Time**: 2-second maximum response time threshold
**Resource Efficiency**: 60% minimum resource efficiency requirement
**Optimization Focus**: Algorithm efficiency, memory usage, and processing speed

#### Maintainability Standards
```yaml
maintainability:
  minimum_score: 0.6
  factors:
    - code_clarity
    - documentation_quality
    - modular_design
    - consistent_style
```

**Maintainability Score**: 60% minimum maintainability score
**Sustainability Focus**: Emphasizes long-term code maintainability

### 4. Validation Workflow (`validation_workflow`)

#### Pre-Validation
```yaml
pre_validation:
  enabled: true
  quick_checks:
    - syntax_validation
    - basic_security_scan
    - rule_compliance_check
```

**Purpose**: Fast validation before operation execution
**Quick Checks**: Essential validations that execute rapidly
**Blocking**: Can prevent operation execution based on results

#### Post-Validation
```yaml
post_validation:
  enabled: true
  comprehensive_checks:
    - quality_assessment
    - principle_alignment
    - effectiveness_measurement
    - learning_opportunity_detection
```

**Purpose**: Comprehensive validation after operation completion
**Thorough Analysis**: Complete quality and principle assessment
**Learning Integration**: Identifies opportunities for framework learning

#### Continuous Validation
```yaml
continuous_validation:
  enabled: true
  real_time_monitoring:
    - pattern_violation_detection
    - quality_degradation_alerts
    - performance_regression_detection
```

**Purpose**: Ongoing validation throughout operation lifecycle
**Real-Time Monitoring**: Immediate detection of issues as they arise
**Proactive Alerts**: Early warning system for quality issues

### 5. Error Classification and Handling (`error_classification`)

#### Critical Errors
```yaml
critical_errors:
  severity_level: "critical"
  block_execution: true
  examples:
    - security_vulnerabilities
    - data_corruption_risk
    - system_instability
```

**Execution Blocking**: Critical errors prevent operation execution
**System Protection**: Prevents system-level damage or security breaches

#### Standard Errors
```yaml
standard_errors:
  severity_level: "error"
  block_execution: false
  require_acknowledgment: true
  examples:
    - rule_violations
    - quality_failures
    - incomplete_implementation
```

**Acknowledgment Required**: User must acknowledge errors before proceeding
**Non-Blocking**: Allows execution with user awareness of issues

#### Warnings and Suggestions
```yaml
warnings:
  severity_level: "warning"
  block_execution: false
  examples:
    - principle_deviations
    - optimization_opportunities
    - best_practice_suggestions

suggestions:
  severity_level: "suggestion"
  informational: true
  examples:
    - code_improvements
    - efficiency_enhancements
    - learning_recommendations
```

**Non-Blocking**: Warnings and suggestions don't prevent execution
**Educational Value**: Provides learning opportunities and improvement suggestions

### 6. Effectiveness Measurement (`effectiveness_measurement`)

#### Success Indicators
```yaml
success_indicators:
  task_completion: "weight: 0.4"
  quality_achievement: "weight: 0.3"
  user_satisfaction: "weight: 0.2"
  learning_value: "weight: 0.1"
```

**Weighted Assessment**: Balanced evaluation across multiple success dimensions
**Task Completion**: Highest weight on successful task completion
**Quality Focus**: Significant weight on quality achievement
**User Experience**: Important consideration for user satisfaction
**Learning Value**: Framework learning and improvement value

#### Performance Metrics
```yaml
performance_metrics:
  execution_time: "target: <2000ms"
  resource_efficiency: "target: >0.6"
  error_rate: "target: <0.1"
  validation_accuracy: "target: >0.9"
```

**Performance Targets**: Specific measurable targets for performance assessment
**Error Rate**: Low error rate target for system reliability
**Validation Accuracy**: High accuracy target for validation effectiveness

#### Quality Metrics
```yaml
quality_metrics:
  code_quality_score: "target: >0.7"
  security_compliance: "target: >0.8"
  principle_alignment: "target: >0.7"
  rule_compliance: "target: >0.9"
```

**Quality Targets**: Specific targets for different quality dimensions
**High Compliance**: Very high rule compliance target (90%)
**Strong Security**: High security compliance target (80%)

### 7. Learning Integration (`learning_integration`)

#### Pattern Detection
```yaml
pattern_detection:
  success_patterns: true
  failure_patterns: true
  optimization_patterns: true
  user_preference_patterns: true
```

**Comprehensive Pattern Learning**: Learns from all types of patterns
**Success and Failure**: Learns from both positive and negative outcomes
**User Preferences**: Adapts to individual user patterns and preferences

#### Effectiveness Feedback
```yaml
effectiveness_feedback:
  real_time_collection: true
  user_satisfaction_tracking: true
  quality_trend_analysis: true
  adaptation_triggers: true
```

**Real-Time Learning**: Immediate learning from validation outcomes
**User Satisfaction**: Incorporates user satisfaction into learning
**Trend Analysis**: Identifies quality trends over time
**Adaptive Triggers**: Triggers adaptations based on learning insights

#### Continuous Improvement
```yaml
continuous_improvement:
  threshold_adjustment: true
  rule_refinement: true
  principle_enhancement: true
  validation_optimization: true
```

**Dynamic Optimization**: Continuously improves validation effectiveness
**Rule Evolution**: Refines rules based on effectiveness data
**Validation Enhancement**: Optimizes validation processes over time

### 8. Context-Aware Validation (`context_awareness`)

#### Project Type Adaptations
```yaml
project_type_adaptations:
  frontend_projects:
    additional_checks: ["accessibility", "responsive_design", "browser_compatibility"]
  
  backend_projects:
    additional_checks: ["api_security", "data_validation", "performance_optimization"]
  
  full_stack_projects:
    additional_checks: ["integration_testing", "end_to_end_validation", "deployment_safety"]
```

**Project-Specific Validation**: Adapts validation to project characteristics
**Domain-Specific Checks**: Includes relevant checks for each project type
**Comprehensive Coverage**: Ensures all relevant aspects are validated

#### User Expertise Adjustments
```yaml
user_expertise_adjustments:
  beginner:
    validation_verbosity: "high"
    educational_suggestions: true
    step_by_step_guidance: true
  
  intermediate:
    validation_verbosity: "medium"
    best_practice_suggestions: true
    optimization_recommendations: true
  
  expert:
    validation_verbosity: "low"
    advanced_optimization_suggestions: true
    architectural_guidance: true
```

**Expertise-Aware Validation**: Adapts validation approach to user expertise level
**Educational Value**: Provides appropriate learning opportunities
**Efficiency Optimization**: Reduces noise for expert users while maintaining quality

### 9. Performance Configuration (`performance_configuration`)

#### Validation Targets
```yaml
validation_targets:
  processing_time_ms: 100
  memory_usage_mb: 50
  cpu_utilization_percent: 30
```

**Performance Limits**: Ensures validation doesn't impact system performance
**Resource Constraints**: Reasonable resource usage for validation processes

#### Optimization Strategies
```yaml
optimization_strategies:
  parallel_validation: true
  cached_results: true
  incremental_validation: true
  smart_rule_selection: true
```

**Performance Optimization**: Multiple strategies to optimize validation speed
**Intelligent Caching**: Caches validation results for repeated operations
**Smart Selection**: Applies only relevant rules based on context

#### Resource Management
```yaml
resource_management:
  max_validation_time_ms: 500
  memory_limit_mb: 100
  cpu_limit_percent: 50
  fallback_on_resource_limit: true
```

**Resource Protection**: Prevents validation from consuming excessive resources
**Graceful Fallback**: Falls back to basic validation if resource limits exceeded

### 10. Integration Points (`integration_points`)

#### MCP Server Integration
```yaml
mcp_servers:
  serena: "semantic_validation_support"
  morphllm: "edit_validation_coordination"
  sequential: "complex_validation_analysis"
```

**Server-Specific Integration**: Leverages MCP server capabilities for validation
**Semantic Validation**: Uses Serena for semantic analysis validation
**Edit Coordination**: Coordinates with Morphllm for edit validation

#### Learning Engine Integration
```yaml
learning_engine:
  effectiveness_tracking: true
  pattern_learning: true
  adaptation_feedback: true
```

**Learning Coordination**: Integrates validation results with learning system
**Pattern Learning**: Learns patterns from validation outcomes
**Adaptive Feedback**: Provides feedback for learning adaptation

#### Other Hook Integration
```yaml
other_hooks:
  pre_tool_use: "validation_preparation"
  session_start: "validation_configuration"
  stop: "validation_summary_generation"
```

**Hook Coordination**: Integrates validation across hook lifecycle
**Preparation**: Prepares validation context before tool use
**Summary**: Generates validation summaries at session end

## Performance Implications

### 1. Validation Processing Performance

#### Rule Validation Performance
- **File Operation Rules**: 5-20ms per rule validation
- **Security Rules**: 10-50ms per security check
- **Principle Validation**: 20-100ms per principle assessment
- **Total Rule Validation**: 50-200ms for complete rule validation

#### Quality Assessment Performance
- **Code Quality**: 100-500ms for comprehensive quality assessment
- **Security Compliance**: 200ms-1s for security analysis
- **Performance Analysis**: 150-750ms for performance validation
- **Maintainability**: 50-300ms for maintainability assessment

### 2. Learning Integration Performance

#### Pattern Learning Impact
- **Pattern Detection**: 50-200ms for pattern recognition
- **Learning Updates**: 100-500ms for learning data updates
- **Adaptation Application**: 200ms-1s for adaptation implementation

#### Effectiveness Tracking
- **Metrics Collection**: 10-50ms per validation operation
- **Trend Analysis**: 100-500ms for trend calculation
- **User Satisfaction**: 20-100ms for satisfaction tracking

### 3. Resource Usage

#### Memory Usage
- **Rule Storage**: 100-500KB for validation rules
- **Pattern Data**: 500KB-2MB for learned patterns
- **Validation State**: 50-200KB during validation execution

#### CPU Usage
- **Validation Processing**: 20-60% CPU during comprehensive validation
- **Learning Processing**: 10-40% CPU for pattern learning
- **Background Monitoring**: <5% CPU for continuous validation

## Configuration Best Practices

### 1. Production Validation Configuration
```yaml
# Strict validation for production reliability
rules_validation:
  file_operations:
    read_before_write:
      severity: "critical"  # Stricter enforcement
  security_requirements:
    production_safety:
      enabled: true
      severity: "critical"

quality_standards:
  security_compliance:
    minimum_score: 0.9  # Higher security requirement
```

### 2. Development Validation Configuration
```yaml
# Educational and learning-focused validation
user_expertise_adjustments:
  default_level: "beginner"
  educational_suggestions: true
  verbose_explanations: true

learning_integration:
  continuous_improvement:
    adaptation_triggers: "aggressive"  # More learning
```

### 3. Performance-Optimized Configuration
```yaml
# Minimal validation for performance-critical environments
performance_configuration:
  optimization_strategies:
    parallel_validation: true
    cached_results: true
    smart_rule_selection: true
  
  resource_management:
    max_validation_time_ms: 200  # Stricter time limits
```

### 4. Learning-Optimized Configuration
```yaml
# Maximum learning and adaptation
learning_integration:
  pattern_detection:
    detailed_analysis: true
    cross_session_learning: true
  
  effectiveness_feedback:
    real_time_collection: true
    detailed_metrics: true
```

## Troubleshooting

### Common Validation Issues

#### False Positive Rule Violations
- **Symptoms**: Valid operations flagged as rule violations
- **Analysis**: Review rule patterns and exception handling
- **Solutions**: Refine rule patterns, add appropriate exceptions
- **Testing**: Test rules with edge cases and valid scenarios

#### Performance Impact
- **Symptoms**: Validation causing significant delays
- **Diagnosis**: Profile validation performance and identify bottlenecks
- **Optimization**: Enable caching, parallel processing, smart rule selection
- **Monitoring**: Track validation performance metrics continuously

#### Learning System Issues
- **Symptoms**: Validation not improving over time, poor adaptations
- **Investigation**: Review learning data collection and pattern recognition
- **Enhancement**: Adjust learning parameters, improve pattern detection
- **Validation**: Test learning effectiveness with controlled scenarios

#### Quality Standards Conflicts
- **Symptoms**: Conflicting quality requirements or unrealistic standards
- **Analysis**: Review quality standard interactions and dependencies
- **Resolution**: Adjust standards based on project requirements and constraints
- **Balancing**: Balance quality with practical implementation constraints

### Validation System Optimization

#### Rule Optimization
```yaml
# Optimize rule execution for performance
rules_validation:
  smart_rule_selection:
    context_aware: true
    performance_optimized: true
    minimal_redundancy: true
```

#### Quality Standard Tuning
```yaml
# Adjust quality standards based on project needs
quality_standards:
  adaptive_thresholds: true
  project_specific_adjustments: true
  user_expertise_consideration: true
```

#### Learning System Tuning
```yaml
# Optimize learning for specific environments
learning_integration:
  learning_rate_adjustment: "environment_specific"
  pattern_recognition_sensitivity: "adaptive"
  effectiveness_measurement_accuracy: "high"
```

## Related Documentation

- **RULES.md**: Core SuperClaude rules being enforced through validation
- **PRINCIPLES.md**: SuperClaude principles being validated for alignment
- **Quality Gates**: Integration with 8-step quality validation cycle
- **Hook Integration**: Post-tool use hook implementation for validation execution

## Version History

- **v1.0.0**: Initial validation configuration
- Comprehensive RULES.md enforcement with automatic detection
- PRINCIPLES.md alignment validation with evidence-based requirements
- Multi-dimensional quality standards (code, security, performance, maintainability)
- Context-aware validation with project type and user expertise adaptations
- Learning integration with pattern detection and continuous improvement
- Performance optimization with parallel processing and intelligent caching