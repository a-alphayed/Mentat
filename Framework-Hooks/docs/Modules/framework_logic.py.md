# framework_logic.py - Core SuperClaude Framework Decision Engine

## Overview

The `framework_logic.py` module implements the core decision-making algorithms from the SuperClaude framework, translating RULES.md, PRINCIPLES.md, and ORCHESTRATOR.md patterns into executable intelligence. This module serves as the central nervous system for all hook operations, providing evidence-based decision making, complexity assessment, risk evaluation, and quality validation.

## Purpose and Responsibilities

### Primary Functions
- **Decision Algorithm Implementation**: Executable versions of SuperClaude framework rules
- **Complexity Assessment**: Multi-factor scoring system for operation routing decisions
- **Risk Evaluation**: Context-aware risk assessment with mitigation strategies
- **Quality Validation**: Multi-step validation cycles with measurable quality scores
- **Performance Estimation**: Resource impact prediction and optimization recommendations

### Framework Pattern Implementation
- **RULES.md Compliance**: Read-before-write validation, systematic codebase changes, session lifecycle rules
- **PRINCIPLES.md Integration**: Evidence-based decisions, quality standards, error handling patterns
- **ORCHESTRATOR.md Logic**: Intelligent routing, resource management, quality gate enforcement

## Core Classes and Data Structures

### Enumerations

#### OperationType
```python
class OperationType(Enum):
    READ = "read"           # File reading operations
    WRITE = "write"         # File creation operations
    EDIT = "edit"           # File modification operations
    ANALYZE = "analyze"     # Code analysis operations
    BUILD = "build"         # Build/compilation operations
    TEST = "test"           # Testing operations
    DEPLOY = "deploy"       # Deployment operations
    REFACTOR = "refactor"   # Code restructuring operations
```

#### RiskLevel
```python
class RiskLevel(Enum):
    LOW = "low"           # Minimal impact, safe operations
    MEDIUM = "medium"     # Moderate impact, requires validation
    HIGH = "high"         # Significant impact, requires approval
    CRITICAL = "critical" # System-wide impact, maximum validation
```

### Data Classes

#### OperationContext
```python
@dataclass
class OperationContext:
    operation_type: OperationType        # Type of operation being performed
    file_count: int                     # Number of files involved
    directory_count: int                # Number of directories involved
    has_tests: bool                     # Whether tests are available
    is_production: bool                 # Production environment flag
    user_expertise: str                 # beginner|intermediate|expert
    project_type: str                   # web|api|cli|library|etc
    complexity_score: float             # 0.0 to 1.0 complexity rating
    risk_level: RiskLevel              # Assessed risk level
```

#### ValidationResult
```python
@dataclass
class ValidationResult:
    is_valid: bool                      # Overall validation status
    issues: List[str]                   # Critical issues found
    warnings: List[str]                 # Non-critical warnings
    suggestions: List[str]              # Improvement recommendations
    quality_score: float                # 0.0 to 1.0 quality rating
```

## Core Methods and Algorithms

### Framework Rule Implementation

#### should_use_read_before_write()
```python
def should_use_read_before_write(self, context: OperationContext) -> bool:
    """RULES.md: Always use Read tool before Write or Edit operations."""
    return context.operation_type in [OperationType.WRITE, OperationType.EDIT]
```

**Implementation Details**:
- Direct mapping from RULES.md operational security requirements
- Returns True for any operation that modifies existing files
- Used by hooks to enforce read-before-write validation

#### should_enable_validation()
```python
def should_enable_validation(self, context: OperationContext) -> bool:
    """ORCHESTRATOR.md: Enable validation for production code or high-risk operations."""
    return (
        context.is_production or 
        context.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL] or
        context.operation_type in [OperationType.DEPLOY, OperationType.REFACTOR]
    )
```

### Complexity Assessment Algorithm

#### calculate_complexity_score()
Multi-factor complexity scoring with weighted components:

**File Count Factor (0.0 to 0.3)**:
- 1 file: 0.0
- 2-3 files: 0.1
- 4-10 files: 0.2
- 10+ files: 0.3

**Directory Factor (0.0 to 0.2)**:
- 1 directory: 0.0
- 2 directories: 0.1
- 3+ directories: 0.2

**Operation Type Factor (0.0 to 0.3)**:
- Refactor/Architecture: 0.3
- Build/Implement/Migrate: 0.2
- Fix/Update/Improve: 0.1
- Read/Analyze: 0.0

**Language/Framework Factor (0.0 to 0.2)**:
- Multi-language projects: 0.2
- Framework changes: 0.1
- Single language/no framework: 0.0

**Total Score**: Sum of all factors, capped at 1.0

### Risk Assessment Algorithm

#### assess_risk_level()
Context-based risk evaluation with escalation rules:

1. **Production Environment**: Automatic HIGH risk
2. **Complexity > 0.7**: HIGH risk
3. **Complexity > 0.4**: MEDIUM risk
4. **File Count > 10**: MEDIUM risk
5. **Default**: LOW risk

### Quality Validation Framework

#### validate_operation()
Multi-criteria validation with quality scoring:

**Evidence-Based Validation**:
- Evidence provided: Quality maintained
- No evidence: -0.1 quality score, warning generated

**Error Handling Validation**:
- Write/Edit/Deploy operations require error handling
- Missing error handling: -0.2 quality score, issue generated

**Test Coverage Validation**:
- Logic changes should have tests
- Missing tests: -0.1 quality score, suggestion generated

**Documentation Validation**:
- Public APIs require documentation
- Missing docs: -0.1 quality score, suggestion generated

**Security Validation**:
- User input handling requires validation
- Missing input validation: -0.3 quality score, critical issue

**Quality Thresholds**:
- Valid operation: No issues AND quality_score ≥ 0.7
- Final quality_score: max(calculated_score, 0.0)

### Thinking Mode Selection

#### determine_thinking_mode()
Complexity-based thinking mode selection:

- **Complexity ≥ 0.8**: `--ultrathink` (32K token analysis)
- **Complexity ≥ 0.6**: `--think-hard` (10K token analysis)
- **Complexity ≥ 0.3**: `--think` (4K token analysis)
- **Complexity < 0.3**: No thinking mode required

### Delegation Decision Logic

#### should_enable_delegation()
Multi-factor delegation assessment:

```python
def should_enable_delegation(self, context: OperationContext) -> Tuple[bool, str]:
    if context.file_count > 3:
        return True, "files"          # File-based delegation
    elif context.directory_count > 2:
        return True, "folders"        # Folder-based delegation
    elif context.complexity_score > 0.4:
        return True, "auto"           # Automatic strategy selection
    else:
        return False, "none"          # No delegation needed
```

## Performance Target Management

### Configuration Integration
```python
def __init__(self):
    # Load performance targets from SuperClaude configuration
    self.performance_targets = {}
    
    # Hook-specific targets
    self.performance_targets['session_start_ms'] = config_loader.get_hook_config(
        'session_start', 'performance_target_ms', 50
    )
    self.performance_targets['tool_routing_ms'] = config_loader.get_hook_config(
        'pre_tool_use', 'performance_target_ms', 200
    )
    # ... additional targets
```

### Performance Impact Estimation
```python
def estimate_performance_impact(self, context: OperationContext) -> Dict[str, Any]:
    base_time = 100  # ms
    estimated_time = base_time * (1 + context.complexity_score * 3)
    
    # Factor in file count impact
    if context.file_count > 5:
        estimated_time *= 1.5
    
    # Generate optimization suggestions
    optimizations = []
    if context.file_count > 3:
        optimizations.append("Consider parallel processing")
    if context.complexity_score > 0.6:
        optimizations.append("Enable delegation mode")
    
    return {
        'estimated_time_ms': int(estimated_time),
        'performance_risk': 'high' if estimated_time > 1000 else 'low',
        'suggested_optimizations': optimizations,
        'efficiency_gains_possible': len(optimizations) > 0
    }
```

## Quality Gates Integration

### get_quality_gates()
Dynamic quality gate selection based on operation context:

**Base Gates** (All Operations):
- `syntax_validation`: Language-specific syntax checking

**Write/Edit Operations**:
- `type_analysis`: Type compatibility validation
- `code_quality`: Linting and style checking

**High-Risk Operations**:
- `security_assessment`: Vulnerability scanning
- `performance_analysis`: Performance impact analysis

**Test-Available Operations**:
- `test_validation`: Test execution and coverage

**Deployment Operations**:
- `integration_testing`: End-to-end validation
- `deployment_validation`: Environment compatibility

## SuperClaude Principles Application

### apply_superclaude_principles()
Automatic principle enforcement with recommendations:

**Evidence > Assumptions**:
```python
if 'assumptions' in enhanced_data and not enhanced_data.get('evidence'):
    enhanced_data['recommendations'].append(
        "Gather evidence to validate assumptions"
    )
```

**Code > Documentation**:
```python
if enhanced_data.get('operation_type') == 'document' and not enhanced_data.get('has_working_code'):
    enhanced_data['warnings'].append(
        "Ensure working code exists before extensive documentation"
    )
```

**Efficiency > Verbosity**:
```python
if enhanced_data.get('output_length', 0) > 1000 and not enhanced_data.get('justification_for_length'):
    enhanced_data['efficiency_suggestions'].append(
        "Consider token efficiency techniques for long outputs"
    )
```

## Integration with Hooks

### Hook Implementation Pattern
```python
# Hook initialization
framework_logic = FrameworkLogic()

# Operation context creation
context = OperationContext(
    operation_type=OperationType.EDIT,
    file_count=file_count,
    directory_count=dir_count,
    has_tests=has_tests,
    is_production=is_production,
    user_expertise="intermediate",
    project_type="web",
    complexity_score=0.0,  # Will be calculated
    risk_level=RiskLevel.LOW  # Will be assessed
)

# Calculate complexity and assess risk
context.complexity_score = framework_logic.calculate_complexity_score(operation_data)
context.risk_level = framework_logic.assess_risk_level(context)

# Make framework-compliant decisions
should_validate = framework_logic.should_enable_validation(context)
should_delegate, delegation_strategy = framework_logic.should_enable_delegation(context)
thinking_mode = framework_logic.determine_thinking_mode(context)

# Validate operation
validation_result = framework_logic.validate_operation(operation_data)
if not validation_result.is_valid:
    # Handle validation issues
    handle_validation_issues(validation_result)
```

## Error Handling Strategies

### Graceful Degradation
- **Configuration Errors**: Use default performance targets
- **Calculation Errors**: Return safe default values
- **Validation Failures**: Provide detailed error context

### Fallback Mechanisms
- **Complexity Calculation**: Default to 0.5 if calculation fails
- **Risk Assessment**: Default to MEDIUM risk if assessment fails
- **Quality Validation**: Default to valid with warnings if validation fails

## Performance Characteristics

### Operation Timings
- **Complexity Calculation**: <5ms for typical operations
- **Risk Assessment**: <3ms for context evaluation
- **Quality Validation**: <10ms for comprehensive validation
- **Performance Estimation**: <2ms for impact calculation

### Memory Efficiency
- **Context Objects**: ~200-400 bytes per context
- **Validation Results**: ~500-1000 bytes with full details
- **Configuration Cache**: ~1-2KB for performance targets

## Configuration Requirements

### Required Configuration Sections
```yaml
# Performance targets for each hook
hook_configurations:
  session_start:
    performance_target_ms: 50
  pre_tool_use:
    performance_target_ms: 200
  post_tool_use:
    performance_target_ms: 100
  pre_compact:
    performance_target_ms: 150

# Global performance settings
global_configuration:
  performance_monitoring:
    enabled: true
    target_percentile: 95
    alert_threshold_ms: 500
```

## Usage Examples

### Basic Decision Making
```python
framework_logic = FrameworkLogic()

# Create operation context
context = OperationContext(
    operation_type=OperationType.REFACTOR,
    file_count=15,
    directory_count=3,
    has_tests=True,
    is_production=False,
    user_expertise="expert",
    project_type="web",
    complexity_score=0.0,
    risk_level=RiskLevel.LOW
)

# Calculate complexity and assess risk
context.complexity_score = framework_logic.calculate_complexity_score({
    'file_count': 15,
    'directory_count': 3,
    'operation_type': 'refactor',
    'multi_language': False,
    'framework_changes': True
})

context.risk_level = framework_logic.assess_risk_level(context)

# Make decisions
should_read_first = framework_logic.should_use_read_before_write(context)  # False (refactor)
should_validate = framework_logic.should_enable_validation(context)        # True (refactor)
should_delegate, strategy = framework_logic.should_enable_delegation(context)  # True, "files"
thinking_mode = framework_logic.determine_thinking_mode(context)           # "--think-hard"
```

### Quality Validation
```python
operation_data = {
    'operation_type': 'write',
    'affects_logic': True,
    'has_tests': False,
    'is_public_api': True,
    'has_documentation': False,
    'handles_user_input': True,
    'has_input_validation': False,
    'has_error_handling': True
}

validation_result = framework_logic.validate_operation(operation_data)

print(f"Valid: {validation_result.is_valid}")                    # False
print(f"Quality Score: {validation_result.quality_score}")       # 0.4
print(f"Issues: {validation_result.issues}")                     # ['User input handling without validation']
print(f"Warnings: {validation_result.warnings}")                # ['No tests found for logic changes', 'Public API lacks documentation']
print(f"Suggestions: {validation_result.suggestions}")          # ['Add unit tests for new logic', 'Add API documentation']
```

## Dependencies and Relationships

### Internal Dependencies
- **yaml_loader**: Configuration loading and management
- **Standard Libraries**: json, time, dataclasses, enum, typing

### Framework Integration
- **RULES.md**: Direct implementation of operational rules
- **PRINCIPLES.md**: Quality standards and decision-making principles
- **ORCHESTRATOR.md**: Intelligent routing and resource management patterns

### Hook Coordination
- Used by all 7 hooks for consistent decision-making
- Provides standardized context and validation interfaces
- Enables cross-hook performance monitoring and optimization

---

*This module serves as the foundational intelligence layer for the entire SuperClaude framework, ensuring that all hook operations are evidence-based, quality-validated, and optimally routed according to established patterns and principles.*