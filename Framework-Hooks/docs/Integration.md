# Framework-Hooks Integration with SuperClaude

## Overview

The Framework-Hooks system implements SuperClaude framework patterns through Claude Code lifecycle hooks. The system executes 7 Python hooks during session lifecycle events to provide mode detection, MCP server routing, and configuration management.

## 1. Hook Implementation Architecture

### Lifecycle Hook Integration

The Framework-Hooks system implements SuperClaude patterns through 7 Python hooks:

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code Runtime                      │
├─────────────────────────────────────────────────────────────┤
│  SessionStart → PreTool → PostTool → PreCompact → Notify   │
│       ↓            ↓         ↓           ↓          ↓       │
│   Mode/MCP     Server      Learning    Token        Pattern │
│   Detection    Selection   Tracking    Compression  Updates │
└─────────────────────────────────────────────────────────────┘
```

### SuperClaude Framework Implementation

Each hook implements specific SuperClaude framework aspects:

- **session_start.py**: MODE detection patterns from MODE_*.md files
- **pre_tool_use.py**: MCP server routing from ORCHESTRATOR.md patterns  
- **post_tool_use.py**: Learning and effectiveness tracking
- **pre_compact.py**: Token efficiency patterns from MODE_Token_Efficiency.md
- **stop.py/subagent_stop.py**: Session analytics and coordination tracking

### Configuration Integration

Hook behavior is configured through:

- **settings.json**: Hook timeouts and execution commands
- **performance.yaml**: Performance targets (50ms session_start, 200ms pre_tool_use, etc.)
- **modes.yaml**: Mode detection patterns and triggers
- **pattern files**: Project-specific behavior in minimal/, dynamic/, learned/ directories

## 2. Hook Lifecycle Integration

### Hook Execution Flow

The hooks execute during specific Claude Code lifecycle events:

```yaml
Hook Execution Sequence:
  1. SessionStart (10s timeout)
     - Detects project type (Python, React, etc.)
     - Loads appropriate pattern files
     - Activates SuperClaude modes based on user input
     - Routes to MCP servers

  2. PreToolUse (15s timeout)
     - Analyzes operation type and complexity
     - Selects optimal MCP servers
     - Applies performance optimizations

  3. PostToolUse (10s timeout)
     - Validates operation results
     - Records learning data and effectiveness metrics
     - Updates user preferences

  4. PreCompact (15s timeout)
     - Applies token compression strategies
     - Preserves framework content (0% compression)
     - Uses symbols and abbreviations for efficiency

  5. Notification (10s timeout)
     - Updates pattern caches
     - Refreshes configurations
     - Handles runtime notifications

  6. Stop (15s timeout)
     - Generates session analytics
     - Saves learning data to files
     - Creates performance metrics

  7. SubagentStop (15s timeout)
     - Tracks delegation performance
     - Records coordination effectiveness
```

### Integration Points

- **Pattern Loading**: Minimal patterns loaded during session_start for project-specific behavior
- **Learning Persistence**: User preferences and effectiveness data saved to learned/ directory
- **Performance Monitoring**: Hook execution times tracked against targets in performance.yaml
- **Configuration Updates**: YAML configuration changes applied during runtime

## 3. MCP Server Coordination

### Server Routing Logic

The pre_tool_use hook routes operations to MCP servers based on detected patterns:

```yaml
MCP Server Selection:
  Magic: 
    - Triggers: UI keywords (component, button, form, modal)
    - Use case: UI component generation and design

  Sequential:
    - Triggers: Analysis keywords (analyze, debug, complex)
    - Use case: Multi-step reasoning and systematic analysis

  Context7:
    - Triggers: Documentation keywords (library, framework, api)
    - Use case: Library documentation and best practices

  Playwright:
    - Triggers: Testing keywords (test, e2e, browser)
    - Use case: Browser automation and testing

  Morphllm vs Serena:
    - Morphllm: Simple edits (<10 files, token optimization)
    - Serena: Complex operations (>5 files, semantic analysis)

  Auto-activation:
    - Project patterns trigger appropriate server combinations
    - User preferences influence server selection
    - Fallback strategies for unavailable servers
```

### Server Configuration

Server routing is configured through:

- **mcp_intelligence.py** (31KB) - Core routing logic and server capability matching
- **mcp_activation.yaml** - Dynamic patterns for server activation
- **Project patterns** - Server preferences by project type (e.g., python_project.yaml specifies Serena + Context7)
- **Learning data** - User preferences for server selection stored in learned/ directory

## 4. SuperClaude Mode Integration

### Mode Detection

The session_start hook detects user intent and activates SuperClaude modes:

```yaml
Mode Detection Patterns:
  Brainstorming Mode:
    - Triggers: "not sure", "thinking about", "explore", ambiguous requests
    - Implementation: Activates interactive requirements discovery

  Task Management Mode:
    - Triggers: Multi-file operations, "build", "implement", complexity >0.4
    - Implementation: Enables delegation and wave orchestration

  Token Efficiency Mode:
    - Triggers: Resource constraints >75%, "--uc", "brief"
    - Implementation: Activates compression in pre_compact hook

  Introspection Mode:
    - Triggers: "analyze reasoning", meta-cognitive requests
    - Implementation: Enables framework compliance analysis
```

### Mode Implementation

Modes are implemented across multiple hooks:

- **session_start.py**: Detects mode triggers and sets activation flags
- **pre_compact.py**: Implements token efficiency compression strategies  
- **post_tool_use.py**: Validates mode-specific behaviors and tracks effectiveness
- **stop.py**: Records mode usage analytics and learning data

## 5. Configuration and Validation

### Configuration Management

The system uses 19 YAML configuration files to define behavior:

- **performance.yaml** (345 lines): Performance targets and monitoring thresholds
- **modes.yaml**: Mode detection patterns and activation triggers  
- **validation.yaml**: Quality gate definitions and validation rules
- **compression.yaml**: Token efficiency settings and compression levels
- **session.yaml**: Session lifecycle and analytics configuration

### Validation Implementation

Validation is distributed across hooks:

- **pre_tool_use.py**: Basic validation before tool execution
- **post_tool_use.py**: Results validation and quality assessment  
- **validate_system.py** (32KB): System health checks and validation utilities
- **stop.py**: Final session validation and analytics generation

### Learning and Analytics

The system tracks effectiveness and adapts behavior:

- **learning_engine.py** (40KB): Records user preferences and operation effectiveness
- **Learned patterns**: Stored in patterns/learned/ directory
- **Performance tracking**: Hook execution times and success rates
- **User preferences**: Saved across sessions for personalized behavior

## 6. Session Management

### Session Integration

Framework-Hooks integrates with Claude Code session lifecycle:

- **Session Start**: session_start hook runs when Claude Code sessions begin
- **Tool Execution**: pre/post_tool_use hooks run for each tool operation
- **Token Optimization**: pre_compact hook runs during token compression
- **Session End**: stop hook runs when sessions complete

### Data Persistence

Session data is persisted through:

- **Learning Records**: User preferences saved to patterns/learned/ directory
- **Performance Metrics**: Hook execution times and success rates logged
- **Session Analytics**: Summary data generated by stop hook
- **Pattern Updates**: Dynamic patterns updated based on usage

### Performance Monitoring

The system tracks performance against configuration targets:

- **Hook Timing**: Each hook execution timed and compared to performance.yaml targets
- **Resource Usage**: Memory and CPU monitoring during hook execution
- **Success Rates**: Operation effectiveness tracked by learning_engine.py
- **User Satisfaction**: Implicit feedback through continued usage patterns

## 7. Pattern System

### Pattern Directory Structure

The system uses a three-tier pattern organization:

```yaml
patterns/
  minimal/        # Essential patterns loaded during session start
    - python_project.yaml: Python project detection and configuration
    - react_project.yaml: React project patterns and MCP routing
    
  dynamic/        # Runtime patterns for adaptive behavior  
    - mode_detection.yaml: SuperClaude mode triggers and activation
    - mcp_activation.yaml: MCP server routing patterns
    
  learned/        # User preference and effectiveness data
    - user_preferences.yaml: Personal configuration adaptations
    - project_optimizations.yaml: Project-specific learned patterns
```

### Pattern Processing

Pattern loading and application:

- **pattern_detection.py** (45KB): Core pattern recognition and matching logic
- **Session startup**: Minimal patterns loaded based on detected project type
- **Runtime updates**: Dynamic patterns applied during hook execution
- **Learning updates**: Successful patterns saved to learned/ directory for future use

### Pattern Configuration

Patterns define:

- **Project detection**: File patterns and dependency analysis for project type identification
- **MCP server routing**: Which servers to activate for different operation types
- **Mode triggers**: Keywords and contexts that activate SuperClaude modes
- **Performance targets**: Project-specific timing and resource goals

## 8. Implementation Summary

### System Implementation

The Framework-Hooks system implements SuperClaude framework patterns through:

**Core Components:**
- 7 Python lifecycle hooks (17 Python files total)
- 19 YAML configuration files  
- 3-tier pattern system (minimal/dynamic/learned)
- 9 shared modules providing common functionality

**Key Features:**
- Project type detection and pattern-based configuration
- SuperClaude mode activation based on user input patterns  
- MCP server routing with fallback strategies
- Token compression with selective framework protection
- Learning system that adapts to user preferences
- Performance monitoring against configured targets

**Integration Points:**
- Claude Code lifecycle hooks via settings.json
- SuperClaude framework mode implementations
- MCP server coordination and routing
- Pattern-based project and operation detection
- Cross-session learning and preference persistence

The system provides a Python-based implementation of SuperClaude framework concepts, enabling intelligent behavior through configuration-driven lifecycle hooks that execute during Claude Code sessions.

