# SuperClaude Pattern System Overview

## Overview

The SuperClaude Pattern System provides a three-tier architecture for project detection, mode activation, and adaptive learning within the Framework-Hooks system. The system uses YAML-based patterns to configure automatic behavior, MCP server activation, and performance optimization.

## System Architecture

### Core Structure

The pattern system consists of three directories with distinct purposes:

```
patterns/
├── minimal/     # Project detection and bootstrap configuration
├── dynamic/     # Mode detection and MCP server activation 
└── learned/     # Project-specific adaptations and user preferences
```

### Pattern Types

**Minimal Patterns**: Project type detection and initial MCP server selection
- File detection patterns for project types (Python, React, etc.)
- Auto-flag configuration for immediate MCP server activation
- Basic project structure recognition

**Dynamic Patterns**: Runtime activation based on context analysis
- Mode detection patterns (brainstorming, task management, etc.)
- MCP server activation based on user requests
- Cross-mode coordination rules

**Learned Patterns**: Adaptation based on usage patterns
- Project-specific optimizations that evolve over time
- User preference learning and adaptation
- Performance metrics and effectiveness tracking

## Pattern Structure

### 1. Minimal Patterns
**Purpose**: Project detection and bootstrap configuration
- **Location**: `/patterns/minimal/`
- **Files**: `python_project.yaml`, `react_project.yaml`
- **Content**: Detection patterns, auto-flags, MCP server configuration

### 2. Dynamic Patterns  
**Purpose**: Runtime mode detection and MCP server activation
- **Location**: `/patterns/dynamic/`
- **Files**: `mcp_activation.yaml`, `mode_detection.yaml`  
- **Content**: Activation patterns, confidence thresholds, coordination rules

### 3. Learned Patterns
**Purpose**: Adaptive behavior based on usage patterns
- **Location**: `/patterns/learned/`
- **Files**: `project_optimizations.yaml`, `user_preferences.yaml`
- **Content**: Performance metrics, user preferences, optimization tracking

## Pattern Schema

### Minimal Pattern Structure

Based on actual files like `python_project.yaml`:

```yaml
project_type: "python"
detection_patterns:
  - "*.py files present"
  - "requirements.txt or pyproject.toml"
  - "__pycache__/ directories"

auto_flags:
  - "--serena"    # Semantic analysis
  - "--context7"  # Python documentation

mcp_servers:
  primary: "serena"
  secondary: ["context7", "sequential", "morphllm"]

patterns:
  file_structure:
    - "src/ or lib/"
    - "tests/"
    - "docs/"
    - "requirements.txt"
  common_tasks:
    - "function refactoring"
    - "class extraction"
    - "import optimization"
    - "testing setup"

intelligence:
  mode_triggers:
    - "token_efficiency: context >75%"
    - "task_management: refactor|test|analyze"
  validation_focus:
    - "python_syntax"
    - "pep8_compliance"
    - "type_hints"
    - "testing_coverage"

performance_targets:
  bootstrap_ms: 40
  context_size: "4KB"
  cache_duration: "45min"
```

### Dynamic Pattern Structure

Based on `mcp_activation.yaml`:

```yaml
activation_patterns:
  context7:
    triggers:
      - "import statements from external libraries"
      - "framework-specific questions"
      - "documentation requests"
    context_keywords:
      - "documentation"
      - "examples"
      - "patterns"
    activation_confidence: 0.8

coordination_patterns:
  hybrid_intelligence:
    serena_morphllm:
      condition: "complex editing with semantic understanding"
      strategy: "serena analyzes, morphllm executes"
      confidence_threshold: 0.8

performance_optimization:
  cache_activation_decisions: true
  cache_duration_minutes: 15
  batch_similar_requests: true
  lazy_loading: true
```

## Hook Integration

### Hook Points

The pattern system integrates with Framework-Hooks at these points:

**session_start**: Load minimal patterns for project detection
**pre_tool_use**: Apply dynamic patterns for mode detection
**post_tool_use**: Update learned patterns with usage data
**stop**: Persist learned optimizations and preferences

### MCP Server Activation

Patterns control MCP server activation through:

1. **Auto-flags**: Immediate activation based on project type
2. **Dynamic activation**: Context-based activation during operation
3. **Coordination patterns**: Rules for multi-server interactions

### Mode Detection

Mode activation is controlled by patterns in `mode_detection.yaml`:

- **Brainstorming**: Triggered by vague project requests, exploration keywords
- **Task Management**: Multi-step operations, system-wide scope
- **Token Efficiency**: Context usage >75%, resource constraints
- **Introspection**: Self-analysis requests, framework discussions

## Current Pattern Files

### Minimal Patterns

**python_project.yaml** (45 lines):
- Detects Python projects by `.py` files, `requirements.txt`, `pyproject.toml`
- Auto-activates `--serena` and `--context7` flags
- Targets 40ms bootstrap, 4KB context size
- Primary server: serena, with context7/sequential/morphllm fallback

**react_project.yaml**:
- Detects React projects by `package.json` with react dependency
- Auto-activates `--magic` and `--context7` flags  
- Targets 30ms bootstrap, 3KB context size
- Primary server: magic, with context7/morphllm fallback

### Dynamic Patterns

**mcp_activation.yaml** (114 lines):
- Defines activation patterns for all 6 MCP servers
- Includes context keywords and confidence thresholds
- Hybrid intelligence coordination (serena + morphllm)
- Performance optimization settings (caching, lazy loading)

**mode_detection.yaml**:
- Mode detection for brainstorming, task management, token efficiency, introspection
- Confidence thresholds from 0.6-0.8 depending on mode
- Cross-mode coordination and transition rules
- Adaptive learning configuration

### Learned Patterns

**project_optimizations.yaml**:
- Project-specific learning for SuperClaude framework
- File pattern analysis and workflow optimization tracking
- MCP server effectiveness measurements
- Performance bottleneck identification and solutions

**user_preferences.yaml**:
- User behavior adaptation patterns
- Communication style preferences
- Workflow pattern effectiveness tracking
- Personalized thresholds and server preferences

## Usage

### Creating New Patterns

1. **Minimal Patterns**: Create project detection patterns in `/patterns/minimal/`
2. **Dynamic Patterns**: Define activation rules in `/patterns/dynamic/`
3. **Learned Patterns**: Configure adaptation tracking in `/patterns/learned/`

### Pattern Development

Patterns are YAML files that follow specific schema formats. They control:

- Project type detection based on file patterns
- Automatic MCP server activation
- Mode detection and activation thresholds
- Performance optimization preferences
- User behavior adaptation

The pattern system provides a declarative way to configure Framework-Hooks behavior without modifying code, enabling customization and optimization based on project types and usage patterns.