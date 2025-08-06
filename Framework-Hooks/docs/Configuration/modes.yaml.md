# Modes Configuration (`modes.yaml`)

## Overview

The `modes.yaml` file defines mode detection patterns for the SuperClaude-Lite framework. This configuration controls trigger patterns and activation thresholds for behavioral mode detection.

## Purpose and Role

The modes configuration provides:
- **Pattern-Based Detection**: Regex and keyword patterns for automatic mode activation
- **Confidence Thresholds**: Minimum confidence levels required for mode activation
- **Auto-Activation Control**: Enable/disable automatic mode detection
- **Performance Tuning**: File count and complexity thresholds for task management mode

## Configuration Structure

### Basic Structure

```yaml
mode_detection:
  [mode_name]:
    enabled: true/false
    trigger_patterns: [list of patterns]
    confidence_threshold: 0.0-1.0
    auto_activate: true/false
```

### 1. Brainstorming Mode

```yaml
brainstorming:
  enabled: true
  trigger_patterns:
    - "I want to build"
    - "thinking about"
    - "not sure"
    - "maybe.*could"
    - "brainstorm"
    - "explore"
    - "figure out"
    - "unclear.*requirements"
    - "ambiguous.*needs"
  confidence_threshold: 0.7
  auto_activate: true
```

**Purpose**: Detects exploration and requirement discovery needs
**Patterns**: Matches uncertain language and exploration keywords
**Threshold**: 70% confidence required for activation

### 2. Task Management Mode

```yaml
task_management:
  enabled: true  
  trigger_patterns:
    - "multiple.*tasks"
    - "complex.*system"
    - "build.*comprehensive"
    - "coordinate.*work"
    - "large-scale.*operation"
    - "manage.*operations"
    - "comprehensive.*refactoring"
    - "authentication.*system"
  confidence_threshold: 0.7
  auto_activate: true
  auto_activation_thresholds:
    file_count: 3
    complexity_score: 0.4
```

**Purpose**: Detects complex, multi-step operations requiring coordination
**Patterns**: Matches system-level and coordination keywords
**Thresholds**: 70% confidence, 3+ files, 0.4+ complexity score

### 3. Token Efficiency Mode

```yaml
token_efficiency:
  enabled: true
  trigger_patterns:
    - "brief"
    - "concise"
    - "compressed"
    - "efficient.*output"
    - "token.*optimization"
    - "short.*response"
    - "running.*low.*context"
  confidence_threshold: 0.75
  auto_activate: true
```

**Purpose**: Detects requests for compressed or efficient output
**Patterns**: Matches brevity and efficiency requests
**Threshold**: 75% confidence required for activation

### 4. Introspection Mode

```yaml
introspection:
  enabled: true
  trigger_patterns:
    - "analyze.*reasoning"
    - "examine.*decision"
    - "reflect.*on"
    - "meta.*cognitive"
    - "thinking.*process"
    - "reasoning.*process"
    - "decision.*made"
  confidence_threshold: 0.6
  auto_activate: true
```

**Purpose**: Detects requests for meta-cognitive analysis
**Patterns**: Matches reasoning and analysis language
**Threshold**: 60% confidence (lower threshold for broader detection)

## Configuration Guidelines

### Pattern Design
- Use regex patterns for flexible matching
- Include variations of key concepts
- Balance specificity with coverage
- Test patterns against common user inputs

### Threshold Tuning
- **Higher thresholds** (0.8+): Reduce false positives, increase precision
- **Lower thresholds** (0.5-0.6): Increase detection, may include false positives
- **Balanced thresholds** (0.7): Good default for most use cases

### Performance Considerations
- Pattern matching adds ~10-50ms per mode evaluation
- More complex regex patterns increase processing time
- Consider disabling unused modes to improve performance

## Integration Points

### Hook Integration
- **Session Start**: Mode detection runs during session initialization
- **Pre-Tool Use**: Mode coordination affects tool selection
- **Post-Tool Use**: Mode effectiveness tracking and validation

### MCP Server Coordination
- Detected modes influence MCP server routing
- Mode-specific optimization strategies applied
- Performance profiles adapted based on active modes

## Troubleshooting

### Mode Not Activating
- **Check pattern matching**: Test patterns against actual user input
- **Lower threshold**: Reduce confidence threshold for broader detection
- **Add patterns**: Include additional trigger patterns for edge cases

### Wrong Mode Activating  
- **Increase threshold**: Raise confidence threshold for more selective activation
- **Refine patterns**: Make patterns more specific to reduce false matches
- **Pattern conflicts**: Check for overlapping patterns between modes

### Performance Issues
- **Disable unused modes**: Set `enabled: false` for unused modes
- **Simplify patterns**: Use simpler regex patterns for better performance
- **Monitor timing**: Track mode detection overhead in logs

## Related Documentation

- **Mode Implementation**: See individual mode documentation (MODE_*.md files)
- **Hook Integration**: Reference `session_start.py` for mode initialization
- **Performance Configuration**: See `performance.yaml.md` for performance monitoring