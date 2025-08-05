# Post-Tool-Use Hook Documentation

## Purpose

The **post_tool_use hook** implements comprehensive validation and learning after every tool execution in Claude Code. It serves as the primary quality assurance and continuous improvement mechanism for the SuperClaude framework, ensuring operations comply with RULES.md and PRINCIPLES.md while learning from each execution to enhance future performance.

**Core Functions:**
- **Quality Validation**: Verifies tool execution against SuperClaude framework standards
- **Rules Compliance**: Enforces RULES.md operational requirements and safety protocols
- **Principles Alignment**: Validates adherence to PRINCIPLES.md development philosophy
- **Effectiveness Measurement**: Quantifies operation success and learning value
- **Error Pattern Detection**: Identifies and learns from recurring issues and failures
- **Learning Integration**: Records insights for continuous framework improvement

## Execution Context

The post_tool_use hook **runs after every tool use** in Claude Code, providing universal validation coverage across all operations.

**Execution Trigger Points:**
- **Universal Coverage**: Activated after every tool execution (Read, Write, Edit, Bash, etc.)
- **Automatic Activation**: No manual intervention required - built into Claude Code's execution pipeline
- **Real-Time Processing**: Immediate validation and feedback on tool results
- **Session Integration**: Maintains context across multiple tool executions within a session

**Input Processing:**
- Receives complete tool execution result via stdin as JSON
- Extracts execution context including parameters, results, errors, and performance data
- Analyzes operation characteristics and quality indicators
- Enriches context with framework-specific metadata

**Output Generation:**
- Comprehensive validation report with quality scores and compliance status
- Actionable recommendations for improvement and optimization
- Learning insights and pattern detection results
- Performance metrics and effectiveness measurements

## Performance Target

**Primary Target: <100ms execution time**

The hook is designed to provide comprehensive validation while maintaining minimal impact on overall system performance.

**Performance Breakdown:**
- **Initialization**: <20ms (component loading and configuration)
- **Context Extraction**: <15ms (analyzing tool results and parameters)
- **Validation Processing**: <35ms (RULES.md and PRINCIPLES.md compliance checking)
- **Learning Analysis**: <20ms (pattern detection and effectiveness measurement)
- **Report Generation**: <10ms (creating comprehensive validation report)

**Performance Monitoring:**
- Real-time execution time tracking with target enforcement
- Automatic performance degradation detection and alerts
- Resource usage monitoring (memory, CPU utilization)
- Fallback mechanisms for performance constraint scenarios

**Optimization Strategies:**
- Parallel validation processing for independent checks
- Cached validation results for repeated patterns
- Incremental validation for large operations
- Smart rule selection based on operation context

## Validation Levels

The hook implements four distinct validation levels, each providing increasing depth of analysis:

### Basic Level
**Focus**: Syntax and fundamental correctness
- **Syntax Validation**: Ensures generated code is syntactically correct
- **Basic Security Scan**: Detects obvious security vulnerabilities
- **Rule Compliance Check**: Validates core RULES.md requirements
- **Performance Target**: <50ms execution time
- **Use Cases**: Simple operations, low-risk contexts, performance-critical scenarios

### Standard Level (Default)
**Focus**: Comprehensive quality and type safety
- **All Basic Level checks**
- **Type Analysis**: Deep type compatibility checking and inference
- **Code Quality Assessment**: Maintainability, readability, and best practices
- **Principle Alignment**: Verification against PRINCIPLES.md guidelines
- **Performance Target**: <100ms execution time
- **Use Cases**: Regular development operations, standard complexity tasks

### Comprehensive Level
**Focus**: Security and performance optimization
- **All Standard Level checks**
- **Security Assessment**: Vulnerability analysis and threat modeling
- **Performance Analysis**: Bottleneck identification and optimization recommendations
- **Error Pattern Detection**: Advanced pattern recognition for failure modes
- **Learning Integration**: Enhanced effectiveness measurement and adaptation
- **Performance Target**: <150ms execution time
- **Use Cases**: High-risk operations, production deployments, security-sensitive contexts

### Production Level
**Focus**: Integration and deployment readiness
- **All Comprehensive Level checks**
- **Integration Testing**: Cross-component compatibility verification
- **Deployment Validation**: Production readiness assessment
- **Quality Gate Enforcement**: Complete 8-step validation cycle
- **Comprehensive Reporting**: Detailed compliance and quality documentation
- **Performance Target**: <200ms execution time
- **Use Cases**: Production deployments, critical system changes, release preparation

## RULES.md Compliance

The hook implements comprehensive enforcement of SuperClaude's core operational rules:

### File Operation Rules
**Read Before Write/Edit Enforcement:**
- Validates that Read operations precede Write/Edit operations
- Checks recent tool history (last 3 operations) for compliance
- Issues errors for violations with clear remediation guidance
- Provides exceptions for new file creation scenarios

**Absolute Path Validation:**
- Scans all path parameters (file_path, path, directory, output_path)
- Blocks relative path usage with specific violation reporting
- Allows approved prefixes (http://, https://, absolute paths)
- Prevents path traversal attacks and ensures operation security

**High-Risk Operation Validation:**
- Identifies high-risk operations (delete, refactor, deploy, migrate)
- Recommends validation for complex operations (complexity > 0.7)
- Provides warnings for operations lacking pre-validation
- Tracks validation compliance across operation types

### Security Requirements
**Input Validation Enforcement:**
- Detects user input handling patterns without validation
- Scans for external data processing vulnerabilities
- Validates API input sanitization and error handling
- Reports security violations with severity classification

**Secret Management Validation:**
- Scans for hardcoded sensitive information (passwords, API keys, tokens)
- Issues critical alerts for secret exposure risks
- Validates secure credential handling patterns
- Provides guidance for proper secret management

**Production Safety Checks:**
- Identifies production context indicators
- Validates safety measures for production operations
- Blocks unsafe operations in production environments
- Ensures proper rollback and recovery mechanisms

### Systematic Code Changes
**Project-Wide Discovery Validation:**
- Ensures comprehensive discovery before systematic changes
- Validates search completeness across all file types
- Confirms impact assessment documentation
- Verifies coordinated change execution planning

## PRINCIPLES.md Alignment

The hook validates adherence to SuperClaude's core development principles:

### Evidence-Based Decision Making
**Evidence Over Assumptions:**
- Detects assumption-based reasoning without supporting evidence
- Requires measurable data for significant decisions
- Validates hypothesis testing and empirical verification
- Promotes evidence-based development practices

**Decision Documentation:**
- Ensures decision rationale is recorded and accessible
- Validates trade-off analysis and alternative consideration
- Requires evidence for architectural and design choices
- Supports future decision review and learning

### Development Priority Validation
**Code Over Documentation:**
- Validates that documentation follows working code implementation
- Prevents documentation-first development anti-patterns
- Ensures documentation accuracy reflects actual implementation
- Promotes iterative development with validated outcomes

**Working Software Priority:**
- Verifies working implementations before extensive documentation
- Validates incremental development with functional milestones
- Ensures user value delivery through functional software
- Supports rapid prototyping and validation cycles

### Efficiency and Quality Balance
**Efficiency Over Verbosity:**
- Analyzes output size and complexity for unnecessary verbosity
- Recommends token efficiency techniques for large outputs
- Validates communication clarity without redundancy
- Promotes concise, actionable guidance and documentation

**Quality Without Compromise:**
- Ensures efficiency improvements don't sacrifice quality
- Validates testing and validation coverage during optimization
- Maintains code clarity and maintainability standards
- Balances development speed with long-term sustainability

## Learning Integration

The hook implements sophisticated learning mechanisms to continuously improve framework effectiveness:

### Effectiveness Measurement
**Multi-Dimensional Scoring:**
- **Overall Effectiveness**: Weighted combination of quality, performance, and satisfaction
- **Quality Score**: Code quality, security compliance, and principle alignment
- **Performance Score**: Execution time efficiency and resource utilization
- **User Satisfaction Estimate**: Success rate and error impact assessment
- **Learning Value**: Complexity, novelty, and insight generation potential

**Effectiveness Calculation:**
```yaml
effectiveness_weights:
  quality_score: 30%          # Code quality and compliance
  performance_score: 25%      # Execution efficiency
  user_satisfaction: 35%      # Perceived value and success
  learning_value: 10%         # Knowledge generation potential
```

### Pattern Recognition and Adaptation
**Success Pattern Detection:**
- Identifies effective tool usage patterns and MCP server coordination
- Recognizes high-quality output characteristics and optimal performance
- Records successful validation patterns and compliance strategies
- Builds pattern library for future operation optimization

**Failure Pattern Analysis:**
- Detects recurring error patterns and failure modes
- Analyzes root causes and contributing factors
- Identifies improvement opportunities and prevention strategies
- Generates targeted recommendations for specific failure types

**Adaptation Mechanisms:**
- **Real-Time Adjustment**: Dynamic threshold modification based on effectiveness
- **Rule Refinement**: Continuous improvement of validation rules and criteria
- **Principle Enhancement**: Evolution of principle interpretation and application
- **Validation Optimization**: Performance tuning based on usage patterns

### Learning Event Recording
**Operation Pattern Learning:**
- Records tool usage effectiveness with context and outcomes
- Tracks MCP server coordination patterns and success rates
- Documents user preference patterns and adaptation opportunities
- Builds comprehensive operation effectiveness database

**Error Recovery Learning:**
- Captures error context, recovery actions, and success rates
- Identifies effective error handling patterns and prevention strategies
- Records recovery time and resource requirements
- Builds error pattern knowledge base for future prevention

## Error Pattern Detection

The hook implements advanced error pattern detection to identify and prevent recurring issues:

### Error Classification System
**Severity-Based Classification:**
- **Critical Errors**: Security vulnerabilities, data corruption risks, system instability
- **Standard Errors**: Rule violations, quality failures, incomplete implementations
- **Warnings**: Principle deviations, optimization opportunities, best practice suggestions
- **Suggestions**: Code improvements, efficiency enhancements, learning recommendations

**Pattern Recognition Engine:**
- **Temporal Pattern Detection**: Identifies error trends over time and contexts
- **Contextual Pattern Analysis**: Recognizes error patterns specific to operation types
- **Cross-Operation Correlation**: Detects error patterns spanning multiple tool executions
- **User-Specific Pattern Learning**: Identifies individual user error tendencies

### Error Prevention Strategies
**Proactive Prevention:**
- **Pre-Validation Recommendations**: Suggests validation for similar high-risk operations
- **Security Check Integration**: Implements automated security validation checks
- **Performance Optimization**: Recommends parallel execution for large operations
- **Pattern-Based Warnings**: Provides early warnings for known problematic patterns

**Reactive Learning:**
- **Error Recovery Documentation**: Records successful recovery strategies
- **Pattern Knowledge Base**: Builds comprehensive error pattern database
- **Adaptation Recommendations**: Generates specific guidance for error prevention
- **User Education**: Provides learning opportunities from error analysis

## Configuration

The hook's behavior is controlled through multiple configuration layers providing flexibility and customization:

### Primary Configuration Source
**superclaude-config.json - post_tool_use section:**
```json
{
  "post_tool_use": {
    "enabled": true,
    "performance_target_ms": 100,
    "features": [
      "quality_validation",
      "rules_compliance_checking", 
      "principles_alignment_verification",
      "effectiveness_measurement",
      "error_pattern_detection",
      "learning_opportunity_identification"
    ],
    "configuration": {
      "rules_validation": true,
      "principles_validation": true,
      "quality_standards_enforcement": true,
      "effectiveness_tracking": true,
      "learning_integration": true
    },
    "validation_levels": {
      "basic": ["syntax_validation"],
      "standard": ["syntax_validation", "type_analysis", "code_quality"],
      "comprehensive": ["syntax_validation", "type_analysis", "code_quality", "security_assessment", "performance_analysis"],
      "production": ["syntax_validation", "type_analysis", "code_quality", "security_assessment", "performance_analysis", "integration_testing", "deployment_validation"]
    }
  }
}
```

### Detailed Validation Configuration
**config/validation.yaml** provides comprehensive validation rule definitions:

**Rules Validation Configuration:**
- File operation rules (read_before_write, absolute_paths_only, validate_before_execution)
- Security requirements (input_validation, no_hardcoded_secrets, production_safety)
- Error severity levels and blocking behavior
- Context-aware validation adjustments

**Principles Validation Configuration:**
- Evidence-based decision making requirements
- Code-over-documentation enforcement
- Efficiency-over-verbosity thresholds
- Test-driven development validation

**Quality Standards:**
- Minimum quality scores for different assessment areas
- Performance thresholds and optimization indicators
- Security compliance requirements and checks
- Maintainability factors and measurement criteria

### Performance and Resource Configuration
**Performance Targets:**
```yaml
performance_configuration:
  validation_targets:
    processing_time_ms: 100      # Primary performance target
    memory_usage_mb: 50          # Memory utilization limit
    cpu_utilization_percent: 30  # CPU usage threshold
  
  optimization_strategies:
    parallel_validation: true     # Enable parallel processing
    cached_results: true         # Cache validation results
    incremental_validation: true  # Optimize for repeated operations
    smart_rule_selection: true   # Context-aware rule application
```

**Resource Management:**
- Maximum validation time limits with fallback mechanisms
- Memory and CPU usage constraints with monitoring
- Automatic resource optimization and constraint handling
- Performance degradation detection and response

## Quality Gates Integration

The post_tool_use hook is integral to SuperClaude's 8-step validation cycle, contributing to multiple quality gates:

### Step 3: Code Quality Assessment
**Comprehensive Quality Analysis:**
- **Code Structure**: Evaluates organization, modularity, and architectural patterns
- **Maintainability**: Assesses readability, documentation, and modification ease
- **Best Practices**: Validates adherence to language and framework conventions
- **Technical Debt**: Identifies accumulation and provides reduction recommendations

**Quality Metrics:**
- Code quality score calculation (target: >0.7)
- Maintainability index with trend analysis
- Technical debt assessment and prioritization
- Best practice compliance percentage

### Step 4: Security Assessment
**Multi-Layer Security Validation:**
- **Vulnerability Analysis**: Scans for common security vulnerabilities (OWASP Top 10)
- **Input Validation**: Ensures proper sanitization and validation of external inputs
- **Authentication/Authorization**: Validates proper access control implementation
- **Data Protection**: Verifies secure data handling and storage practices

**Security Compliance:**
- Security score calculation (target: >0.8)
- Vulnerability severity assessment and prioritization
- Compliance reporting for security standards
- Threat modeling and risk assessment integration

### Step 5: Testing Validation
**Test Coverage and Quality:**
- **Test Presence**: Validates existence of appropriate tests for code changes
- **Coverage Analysis**: Measures test coverage depth and breadth
- **Test Quality**: Assesses test effectiveness and maintainability
- **Integration Testing**: Validates cross-component test coverage

**Testing Metrics:**
- Unit test coverage percentage (target: ≥80%)
- Integration test coverage (target: ≥70%)
- Test quality score and effectiveness measurement
- Testing best practice compliance validation

### Integration with Other Quality Gates
**Coordination with Pre-Tool-Use (Steps 1-2):**
- Receives syntax and type validation results for enhanced analysis
- Builds upon initial validation with deeper quality assessment
- Provides feedback for future pre-validation optimization

**Coordination with Session End (Steps 6-8):**
- Contributes validation results to performance analysis
- Provides quality metrics for documentation verification
- Supports integration testing with operation effectiveness data

### Quality Gate Reporting
**Comprehensive Quality Reports:**
- Step-by-step validation results with detailed findings
- Quality score breakdowns by category and importance
- Trend analysis and improvement recommendations
- Compliance status with actionable remediation steps

**Integration Metrics:**
- Overall quality gate passage rate
- Step-specific success rates and failure analysis
- Quality improvement trends over time
- Framework effectiveness measurement and optimization

## Advanced Features

### Context-Aware Validation
**Project Type Adaptations:**
- **Frontend Projects**: Additional accessibility, responsive design, and browser compatibility checks
- **Backend Projects**: Enhanced API security, data validation, and performance optimization focus  
- **Full-Stack Projects**: Integration testing, end-to-end validation, and deployment safety verification

**User Expertise Adjustments:**
- **Beginner Users**: High validation verbosity, educational suggestions, step-by-step guidance
- **Intermediate Users**: Medium verbosity, best practice suggestions, optimization recommendations
- **Expert Users**: Low verbosity, advanced optimization suggestions, architectural guidance

### Learning System Integration
**Cross-Hook Learning:**
- Shares effectiveness data with pre_tool_use hook for optimization
- Coordinates with session_start hook for user preference learning
- Integrates with stop hook for comprehensive session analysis

**Adaptive Behavior:**
- Adjusts validation thresholds based on user expertise and project context
- Learns from validation effectiveness and user feedback
- Optimizes rule selection and severity based on operation patterns

### Error Recovery and Resilience
**Graceful Degradation:**
- Maintains essential validation even during system constraints
- Provides fallback validation reports on processing errors
- Preserves user context and operation continuity during failures

**Learning from Failures:**
- Records validation hook errors for system improvement
- Analyzes failure patterns to prevent future issues
- Generates insights from error recovery experiences

## Integration Examples

### MCP Server Coordination
**Serena Integration:**
- Receives semantic validation support for code structure analysis
- Coordinates edit validation for complex refactoring operations
- Leverages project context for enhanced validation accuracy

**Morphllm Integration:**
- Validates intelligent editing operations and pattern applications
- Coordinates edit effectiveness measurement and optimization
- Provides feedback for fast-apply optimization

**Sequential Integration:**
- Leverages complex validation analysis for multi-step operations
- Coordinates systematic validation for architectural changes
- Integrates reasoning validation with decision documentation

### Hook Ecosystem Integration
**Pre-Tool-Use Coordination:**
- Receives validation preparation data for enhanced analysis
- Provides effectiveness feedback for future operation optimization
- Coordinates rule enforcement across the complete execution cycle

**Session Management Integration:**
- Contributes validation metrics to session analytics
- Provides quality insights for session summary generation
- Supports cross-session learning and pattern recognition

## Conclusion

The post_tool_use hook serves as the cornerstone of SuperClaude's quality assurance and continuous improvement system. By providing comprehensive validation, learning integration, and adaptive behavior, it ensures that every tool execution contributes to the framework's overall effectiveness while maintaining the highest standards of quality, security, and compliance.

Through its sophisticated validation levels, error pattern detection, and learning mechanisms, the hook enables SuperClaude to continuously evolve and improve, providing users with increasingly effective and reliable development assistance while maintaining strict adherence to the framework's core principles and operational rules.