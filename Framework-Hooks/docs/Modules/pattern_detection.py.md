# pattern_detection.py - Intelligent Pattern Recognition Engine

## Overview

The `pattern_detection.py` module provides intelligent pattern detection for automatic mode activation, MCP server selection, and operational optimization. It analyzes user input, context, and operation patterns to make smart recommendations about which SuperClaude modes should be activated, which MCP servers are needed, and what optimization flags to apply.

## Purpose and Responsibilities

### Primary Functions
- **Mode Trigger Detection**: Automatic identification of when SuperClaude modes should be activated
- **MCP Server Selection**: Context-aware recommendation of which MCP servers to enable
- **Complexity Analysis**: Pattern-based complexity assessment and scoring
- **Persona Recognition**: Detection of domain expertise hints in user requests
- **Performance Optimization**: Pattern-based performance optimization recommendations

### Intelligence Capabilities
- **Regex Pattern Matching**: Compiled patterns for efficient text analysis
- **Context-Aware Analysis**: Integration of user input, session context, and operation data
- **Confidence Scoring**: Probabilistic assessment of pattern matches
- **Multi-Factor Decision Making**: Combination of multiple pattern types for comprehensive analysis

## Core Classes and Data Structures

### Enumerations

#### PatternType
```python
class PatternType(Enum):
    MODE_TRIGGER = "mode_trigger"           # SuperClaude mode activation patterns
    MCP_SERVER = "mcp_server"               # MCP server selection patterns
    OPERATION_TYPE = "operation_type"       # Operation classification patterns
    COMPLEXITY_INDICATOR = "complexity_indicator"  # Complexity assessment patterns
    PERSONA_HINT = "persona_hint"           # Domain expertise detection patterns
    PERFORMANCE_HINT = "performance_hint"   # Performance optimization patterns
```

### Data Classes

#### PatternMatch
```python
@dataclass
class PatternMatch:
    pattern_type: PatternType      # Type of pattern detected
    pattern_name: str              # Specific pattern identifier
    confidence: float              # 0.0 to 1.0 confidence score
    matched_text: str              # Text that triggered the match
    suggestions: List[str]         # Actionable recommendations
    metadata: Dict[str, Any]       # Additional pattern-specific data
```

#### DetectionResult
```python
@dataclass
class DetectionResult:
    matches: List[PatternMatch]           # All detected pattern matches
    recommended_modes: List[str]          # SuperClaude modes to activate
    recommended_mcp_servers: List[str]    # MCP servers to enable
    suggested_flags: List[str]            # Command-line flags to apply
    complexity_score: float               # Overall complexity assessment
    confidence_score: float               # Overall confidence in detection
```

## Pattern Detection Engine

### Initialization and Configuration
```python
def __init__(self):
    self.patterns = config_loader.load_config('modes')
    self.mcp_patterns = config_loader.load_config('orchestrator')
    self._compile_patterns()
```

**Pattern Compilation Process**:
1. Load mode detection patterns from YAML configuration
2. Load MCP routing patterns from orchestrator configuration
3. Compile regex patterns for efficient matching
4. Cache compiled patterns for performance

### Core Detection Method

#### detect_patterns()
```python
def detect_patterns(self, 
                   user_input: str, 
                   context: Dict[str, Any], 
                   operation_data: Dict[str, Any]) -> DetectionResult:
```

**Detection Pipeline**:
1. **Mode Pattern Detection**: Identify SuperClaude mode triggers
2. **MCP Server Pattern Detection**: Determine required MCP servers
3. **Complexity Pattern Detection**: Assess operation complexity indicators
4. **Persona Pattern Detection**: Detect domain expertise hints
5. **Score Calculation**: Compute overall complexity and confidence scores
6. **Recommendation Generation**: Generate actionable recommendations

## Mode Detection Patterns

### Brainstorming Mode Detection
**Trigger Indicators**:
```python
brainstorm_indicators = [
    r"(?:i want to|thinking about|not sure|maybe|could we)\s+(?:build|create|make)",
    r"(?:brainstorm|explore|figure out|discuss)",
    r"(?:new project|startup idea|feature concept)",
    r"(?:ambiguous|uncertain|unclear)\s+(?:requirements|needs)"
]
```

**Pattern Match Example**:
```python
PatternMatch(
    pattern_type=PatternType.MODE_TRIGGER,
    pattern_name="brainstorming",
    confidence=0.8,
    matched_text="thinking about building",
    suggestions=["Enable brainstorming mode for requirements discovery"],
    metadata={"mode": "brainstorming", "auto_activate": True}
)
```

### Task Management Mode Detection
**Trigger Indicators**:
```python
task_management_indicators = [
    r"(?:multiple|many|several)\s+(?:tasks|files|components)",
    r"(?:build|implement|create)\s+(?:system|feature|application)",
    r"(?:complex|comprehensive|large-scale)",
    r"(?:manage|coordinate|orchestrate)\s+(?:work|tasks|operations)"
]
```

### Token Efficiency Mode Detection
**Trigger Indicators**:
```python
efficiency_indicators = [
    r"(?:brief|concise|compressed|short)",
    r"(?:token|resource|memory)\s+(?:limit|constraint|optimization)",
    r"(?:efficient|optimized|minimal)\s+(?:output|response)"
]
```

**Automatic Resource-Based Activation**:
```python
resource_usage = context.get('resource_usage_percent', 0)
if resource_usage > 75:
    # Auto-enable token efficiency mode
    match = PatternMatch(
        pattern_type=PatternType.MODE_TRIGGER,
        pattern_name="token_efficiency",
        confidence=0.85,
        matched_text="high_resource_usage",
        suggestions=["Auto-enable token efficiency due to resource constraints"],
        metadata={"mode": "token_efficiency", "trigger": "resource_constraint"}
    )
```

## MCP Server Detection Patterns

### Context7 (Library Documentation)
**Trigger Patterns**:
```python
context7_patterns = [
    r"(?:library|framework|package)\s+(?:documentation|docs|patterns)",
    r"(?:react|vue|angular|express|django|flask)",
    r"(?:import|require|install|dependency)",
    r"(?:official|standard|best practice)\s+(?:way|pattern|approach)"
]
```

### Sequential (Complex Analysis)
**Trigger Patterns**:
```python
sequential_patterns = [
    r"(?:analyze|debug|troubleshoot|investigate)",
    r"(?:complex|complicated|multi-step|systematic)",
    r"(?:architecture|system|design)\s+(?:review|analysis)",
    r"(?:root cause|performance|bottleneck)"
]
```

### Magic (UI Components)
**Trigger Patterns**:
```python
magic_patterns = [
    r"(?:component|button|form|modal|dialog)",
    r"(?:ui|frontend|interface|design)",
    r"(?:react|vue|angular)\s+(?:component|element)",
    r"(?:responsive|mobile|accessibility)"
]
```

### Playwright (Testing)
**Trigger Patterns**:
```python
playwright_patterns = [
    r"(?:test|testing|e2e|end-to-end)",
    r"(?:browser|cross-browser|automation)",
    r"(?:performance|visual|regression)\s+(?:test|testing)",
    r"(?:validate|verify|check)\s+(?:functionality|behavior)"
]
```

### Hybrid Intelligence Selection (Morphllm vs Serena)
```python
def _detect_mcp_patterns(self, user_input: str, context: Dict[str, Any], operation_data: Dict[str, Any]):
    file_count = operation_data.get('file_count', 1)
    complexity = operation_data.get('complexity_score', 0.0)
    
    if file_count > 10 or complexity > 0.6:
        # Recommend Serena for complex operations
        return PatternMatch(
            pattern_type=PatternType.MCP_SERVER,
            pattern_name="serena",
            confidence=0.9,
            matched_text="high_complexity_operation",
            suggestions=["Use Serena for complex multi-file operations"],
            metadata={"mcp_server": "serena", "reason": "complexity_threshold"}
        )
    elif file_count <= 10 and complexity <= 0.6:
        # Recommend Morphllm for efficient operations
        return PatternMatch(
            pattern_type=PatternType.MCP_SERVER,
            pattern_name="morphllm",
            confidence=0.8,
            matched_text="moderate_complexity_operation",
            suggestions=["Use Morphllm for efficient editing operations"],
            metadata={"mcp_server": "morphllm", "reason": "efficiency_optimized"}
        )
```

## Complexity Detection Patterns

### High Complexity Indicators
```python
high_complexity_patterns = [
    r"(?:entire|whole|complete)\s+(?:codebase|system|application)",
    r"(?:refactor|migrate|restructure)\s+(?:all|everything|entire)",
    r"(?:architecture|system-wide|comprehensive)\s+(?:change|update|redesign)",
    r"(?:complex|complicated|sophisticated)\s+(?:logic|algorithm|system)"
]
```

**Pattern Processing**:
```python
for pattern in high_complexity_patterns:
    if re.search(pattern, user_input, re.IGNORECASE):
        matches.append(PatternMatch(
            pattern_type=PatternType.COMPLEXITY_INDICATOR,
            pattern_name="high_complexity",
            confidence=0.8,
            matched_text=re.search(pattern, user_input, re.IGNORECASE).group(),
            suggestions=["Consider delegation and thinking modes"],
            metadata={"complexity_level": "high", "score_boost": 0.3}
        ))
```

### File Count-Based Complexity
```python
file_count = operation_data.get('file_count', 1)
if file_count > 5:
    matches.append(PatternMatch(
        pattern_type=PatternType.COMPLEXITY_INDICATOR,
        pattern_name="multi_file_operation",
        confidence=0.9,
        matched_text=f"{file_count}_files",
        suggestions=["Enable delegation for multi-file operations"],
        metadata={"file_count": file_count, "delegation_recommended": True}
    ))
```

## Persona Detection Patterns

### Domain-Specific Patterns
```python
persona_patterns = {
    "architect": [r"(?:architecture|design|structure|system)\s+(?:review|analysis|planning)"],
    "performance": [r"(?:performance|optimization|speed|efficiency|bottleneck)"],
    "security": [r"(?:security|vulnerability|audit|secure|safety)"],
    "frontend": [r"(?:ui|frontend|interface|component|design|responsive)"],
    "backend": [r"(?:api|server|database|backend|service)"],
    "devops": [r"(?:deploy|deployment|ci|cd|infrastructure|docker|kubernetes)"],
    "testing": [r"(?:test|testing|qa|quality|coverage|validation)"]
}
```

**Pattern Matching Process**:
```python
for persona, patterns in persona_patterns.items():
    for pattern in patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            matches.append(PatternMatch(
                pattern_type=PatternType.PERSONA_HINT,
                pattern_name=persona,
                confidence=0.7,
                matched_text=re.search(pattern, user_input, re.IGNORECASE).group(),
                suggestions=[f"Consider {persona} persona for specialized expertise"],
                metadata={"persona": persona, "domain_specific": True}
            ))
```

## Scoring Algorithms

### Complexity Score Calculation
```python
def _calculate_complexity_score(self, matches: List[PatternMatch], operation_data: Dict[str, Any]) -> float:
    base_score = operation_data.get('complexity_score', 0.0)
    
    # Add complexity from pattern matches
    for match in matches:
        if match.pattern_type == PatternType.COMPLEXITY_INDICATOR:
            score_boost = match.metadata.get('score_boost', 0.1)
            base_score += score_boost
    
    return min(base_score, 1.0)
```

### Confidence Score Calculation
```python
def _calculate_confidence_score(self, matches: List[PatternMatch]) -> float:
    if not matches:
        return 0.0
    
    total_confidence = sum(match.confidence for match in matches)
    return min(total_confidence / len(matches), 1.0)
```

## Recommendation Generation

### Mode Recommendations
```python
def _get_recommended_modes(self, matches: List[PatternMatch], complexity_score: float) -> List[str]:
    modes = set()
    
    # Add modes from pattern matches
    for match in matches:
        if match.pattern_type == PatternType.MODE_TRIGGER:
            modes.add(match.pattern_name)
    
    # Auto-activate based on complexity
    if complexity_score > 0.6:
        modes.add("task_management")
    
    return list(modes)
```

### Flag Suggestions
```python
def _get_suggested_flags(self, matches: List[PatternMatch], complexity_score: float, context: Dict[str, Any]) -> List[str]:
    flags = []
    
    # Thinking flags based on complexity
    if complexity_score >= 0.8:
        flags.append("--ultrathink")
    elif complexity_score >= 0.6:
        flags.append("--think-hard")
    elif complexity_score >= 0.3:
        flags.append("--think")
    
    # Delegation flags
    for match in matches:
        if match.metadata.get("delegation_recommended"):
            flags.append("--delegate auto")
            break
    
    # Efficiency flags
    for match in matches:
        if match.metadata.get("compression_needed") or context.get('resource_usage_percent', 0) > 75:
            flags.append("--uc")
            break
    
    # Validation flags for high-risk operations
    if complexity_score > 0.7 or context.get('is_production', False):
        flags.append("--validate")
    
    return flags
```

## Performance Characteristics

### Pattern Compilation
- **Initialization Time**: <50ms for full pattern compilation
- **Memory Usage**: ~5-10KB for compiled pattern cache
- **Pattern Count**: ~50-100 patterns across all categories

### Detection Performance
- **Single Pattern Match**: <1ms average
- **Full Detection Pipeline**: <25ms for complex analysis
- **Regex Operations**: Optimized with compiled patterns
- **Context Processing**: <5ms for typical context sizes

### Cache Efficiency
- **Pattern Reuse**: 95%+ pattern reuse across requests
- **Compilation Avoidance**: Patterns compiled once per session
- **Memory Efficiency**: Patterns shared across all detection calls

## Integration with Hooks

### Hook Usage Pattern
```python
# Initialize pattern detector
pattern_detector = PatternDetector()

# Perform pattern detection
detection_result = pattern_detector.detect_patterns(
    user_input="I want to build a complex web application with multiple components",
    context={
        'resource_usage_percent': 45,
        'conversation_length': 25,
        'user_expertise': 'intermediate'
    },
    operation_data={
        'file_count': 12,
        'complexity_score': 0.0,  # Will be enhanced by detection
        'operation_type': 'build'
    }
)

# Apply recommendations
recommended_modes = detection_result.recommended_modes           # ['brainstorming', 'task_management']
recommended_servers = detection_result.recommended_mcp_servers   # ['serena', 'magic']
suggested_flags = detection_result.suggested_flags              # ['--think-hard', '--delegate auto']
complexity_score = detection_result.complexity_score            # 0.7
```

### Pattern Match Processing
```python
for match in detection_result.matches:
    if match.pattern_type == PatternType.MODE_TRIGGER:
        # Activate detected modes
        activate_mode(match.pattern_name)
    elif match.pattern_type == PatternType.MCP_SERVER:
        # Enable recommended MCP servers
        enable_mcp_server(match.pattern_name)
    elif match.pattern_type == PatternType.COMPLEXITY_INDICATOR:
        # Apply complexity-based optimizations
        apply_complexity_optimizations(match.metadata)
```

## Configuration Requirements

### Mode Configuration (modes.yaml)
```yaml
mode_detection:
  brainstorming:
    trigger_patterns:
      - "(?:i want to|thinking about|not sure)\\s+(?:build|create)"
      - "(?:brainstorm|explore|figure out)"
      - "(?:new project|startup idea)"
    confidence_threshold: 0.7
    
  task_management:
    trigger_patterns:
      - "(?:multiple|many)\\s+(?:files|components)"
      - "(?:complex|comprehensive)"
      - "(?:build|implement)\\s+(?:system|feature)"
    confidence_threshold: 0.6
```

### MCP Routing Configuration (orchestrator.yaml)
```yaml
routing_patterns:
  context7:
    triggers:
      - "(?:library|framework)\\s+(?:docs|patterns)"
      - "(?:react|vue|angular)"
      - "(?:official|standard)\\s+(?:way|approach)"
    activation_threshold: 0.8
    
  sequential:
    triggers:
      - "(?:analyze|debug|troubleshoot)"
      - "(?:complex|multi-step)"
      - "(?:architecture|system)\\s+(?:analysis|review)"
    activation_threshold: 0.75
```

## Error Handling Strategies

### Pattern Compilation Errors
```python
def _compile_patterns(self):
    """Compile regex patterns for efficient matching."""
    self.compiled_patterns = {}
    
    try:
        # Compile patterns with error handling
        for mode_name, mode_config in self.patterns.get('mode_detection', {}).items():
            patterns = mode_config.get('trigger_patterns', [])
            self.compiled_patterns[f"mode_{mode_name}"] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
    except re.error as e:
        # Log pattern compilation error and continue with empty patterns
        logger.log_error("pattern_detection", f"Pattern compilation error: {e}")
        self.compiled_patterns[f"mode_{mode_name}"] = []
```

### Detection Failures
- **Regex Errors**: Skip problematic patterns, continue with others
- **Context Errors**: Use default values for missing context keys
- **Scoring Errors**: Return safe default scores (0.5 complexity, 0.0 confidence)

### Graceful Degradation
- **Configuration Missing**: Use hardcoded fallback patterns
- **Pattern Compilation Failed**: Continue with available patterns
- **Performance Issues**: Implement timeout mechanisms for complex patterns

## Usage Examples

### Basic Pattern Detection
```python
detector = PatternDetector()

result = detector.detect_patterns(
    user_input="I need to analyze the performance bottlenecks in this complex React application",
    context={'resource_usage_percent': 60, 'user_expertise': 'expert'},
    operation_data={'file_count': 25, 'operation_type': 'analyze'}
)

print(f"Detected modes: {result.recommended_modes}")        # ['task_management']
print(f"MCP servers: {result.recommended_mcp_servers}")     # ['sequential', 'context7']
print(f"Suggested flags: {result.suggested_flags}")        # ['--think-hard', '--delegate auto']
print(f"Complexity score: {result.complexity_score}")      # 0.7
```

### Pattern Match Analysis
```python
for match in result.matches:
    print(f"Pattern: {match.pattern_name}")
    print(f"Type: {match.pattern_type.value}")
    print(f"Confidence: {match.confidence}")
    print(f"Matched text: {match.matched_text}")
    print(f"Suggestions: {match.suggestions}")
    print(f"Metadata: {match.metadata}")
    print("---")
```

## Dependencies and Relationships

### Internal Dependencies
- **yaml_loader**: Configuration loading for pattern definitions
- **Standard Libraries**: re, json, typing, dataclasses, enum

### Framework Integration
- **MODE Detection**: Triggers for SuperClaude behavioral modes
- **MCP Coordination**: Server selection for intelligent tool routing
- **Performance Optimization**: Flag suggestions for efficiency improvements

### Hook Coordination
- Used by all hooks for consistent pattern-based decision making
- Provides standardized detection interface and result formats
- Enables cross-hook pattern learning and optimization

---

*This module serves as the intelligent pattern recognition system that transforms user input and context into actionable recommendations, enabling SuperClaude to automatically adapt its behavior based on detected patterns and requirements.*