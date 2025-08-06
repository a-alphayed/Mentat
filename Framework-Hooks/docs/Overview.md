# Framework-Hooks System Overview

## System Architecture

The Framework-Hooks system provides lifecycle hooks for Claude Code that implement SuperClaude framework patterns. The system consists of:

### Core Components

1. **Lifecycle Hooks** - 7 Python modules (session_start.py, pre_tool_use.py, post_tool_use.py, pre_compact.py, notification.py, stop.py, subagent_stop.py)
2. **Shared Modules** - 9 Python modules providing shared functionality (framework_logic.py, pattern_detection.py, mcp_intelligence.py, learning_engine.py, compression_engine.py, intelligence_engine.py, validate_system.py, yaml_loader.py, logger.py)
3. **Configuration System** - 19 YAML files defining behavior and settings
4. **Pattern System** - YAML pattern files in minimal/, dynamic/, and learned/ directories

### Architecture Layers

```
┌─────────────────────────────────────────┐
│           Claude Code Interface         │
├─────────────────────────────────────────┤
│            Lifecycle Hooks              │
│  ┌─────┬─────┬─────┬─────┬─────┬─────┐  │
│  │Start│Pre  │Post │Pre  │Notif│Stop │  │
│  │     │Tool │Tool │Comp │     │     │  │
│  └─────┴─────┴─────┴─────┴─────┴─────┘  │
├─────────────────────────────────────────┤
│         Shared Intelligence             │
│  ┌────────────┬─────────────┬─────────┐ │
│  │ Framework  │ Pattern     │Learning │ │
│  │ Logic      │ Detection   │Engine   │ │
│  └────────────┴─────────────┴─────────┘ │
├─────────────────────────────────────────┤
│         YAML Configuration              │
│  ┌─────────────┬────────────┬─────────┐ │
│  │Performance  │Modes       │Logging  │ │
│  │Targets      │Config      │Config   │ │
│  └─────────────┴────────────┴─────────┘ │
└─────────────────────────────────────────┘
```

## Purpose

The Framework-Hooks system implements the SuperClaude framework through lifecycle hooks that run during Claude Code execution.

### Implementation Features

1. **Session Management** - Implements session lifecycle patterns from SESSION_LIFECYCLE.md
2. **Mode Detection** - Activates SuperClaude modes (brainstorming, task management, token efficiency, introspection) based on user input patterns
3. **MCP Server Routing** - Routes operations to appropriate MCP servers (Context7, Sequential, Magic, Playwright, Morphllm, Serena)
4. **Configuration Management** - Loads settings from YAML files to customize behavior
5. **Pattern Recognition** - Detects project types and operation patterns to apply appropriate configurations

### Design Goals

- **Framework Compliance**: Implement SuperClaude patterns and principles
- **Configuration Flexibility**: YAML-driven behavior customization
- **Performance Targets**: 50ms session_start, 200ms pre_tool_use, etc. (as defined in performance.yaml)
- **Pattern-Based Operation**: Use project type and operation detection for intelligent behavior

## Pattern-Based Operation

The system uses pattern files to configure behavior based on detected project characteristics:

### Pattern Detection
```
User Request → Project Type Detection → Load Pattern Files → Apply Configuration → Execute
```

### Pattern System Components

1. **Minimal Patterns** - Essential patterns loaded during session initialization (e.g., python_project.yaml, react_project.yaml)
2. **Dynamic Patterns** - Runtime patterns for mode detection and MCP activation
3. **Learned Patterns** - User preference and project-specific optimizations (stored in learned/ directory)

### Core Modules

1. **Pattern Detection (pattern_detection.py)**
   - 45KB module detecting project types and operation patterns
   - Analyzes file structures, dependencies, and user input

2. **Learning Engine (learning_engine.py)** 
   - 40KB module for user preference tracking
   - Records effectiveness of different configurations

3. **MCP Intelligence (mcp_intelligence.py)**
   - 31KB module for MCP server routing decisions
   - Maps operations to appropriate servers based on capabilities

4. **Framework Logic (framework_logic.py)**
   - 12KB module implementing SuperClaude principles
   - Handles complexity scoring and risk assessment

## Configuration System

The system is configured through YAML files and settings:

### Configuration Files (19 total)

Configuration is defined in /config/ directory:
- **performance.yaml** (345 lines) - Performance targets and thresholds
- **modes.yaml** - Mode detection patterns and settings
- **session.yaml** - Session lifecycle configuration
- **logging.yaml** - Logging configuration and levels
- **compression.yaml** - Token efficiency settings
- Other specialized configuration files

### Settings Integration

Claude Code hooks are configured through settings.json:
- **Hook Timeouts**: session_start (10s), pre_tool_use (15s), etc.
- **Hook Commands**: Python execution paths for each lifecycle hook
- **Hook Matching**: All hooks configured with "*" matcher (apply to all sessions)

### Performance Targets (from performance.yaml)

| Component     | Target | Warning | Critical |
|---------------|--------|---------|----------|
| session_start | 50ms   | 75ms    | 100ms    |
| pre_tool_use  | 200ms  | 300ms   | 500ms    |
| post_tool_use | 100ms  | 150ms   | 250ms    |
| pre_compact   | 150ms  | 200ms   | 300ms    |
| notification  | 100ms  | 150ms   | 200ms    |
| stop          | 200ms  | 300ms   | 500ms    |
| subagent_stop | 150ms  | 200ms   | 300ms    |

## Directory Structure

```
Framework-Hooks/
├── hooks/                         # Lifecycle hook implementations (7 Python files)
│   ├── session_start.py           # 703 lines - Session initialization
│   ├── pre_tool_use.py            # MCP server selection and optimization
│   ├── post_tool_use.py           # Validation and learning integration
│   ├── pre_compact.py             # Token efficiency and compression
│   ├── notification.py            # Pattern updates and notifications
│   ├── stop.py                    # Session analytics and persistence
│   ├── subagent_stop.py           # Task management coordination
│   └── shared/                    # Shared modules (9 Python files)
│       ├── framework_logic.py     # 12KB - SuperClaude principles
│       ├── pattern_detection.py   # 45KB - Pattern recognition
│       ├── mcp_intelligence.py    # 31KB - MCP server routing
│       ├── learning_engine.py     # 40KB - User preference learning
│       ├── compression_engine.py  # 27KB - Token optimization
│       ├── intelligence_engine.py # 18KB - Core intelligence
│       ├── validate_system.py     # 32KB - System validation
│       ├── yaml_loader.py         # 16KB - Configuration loading
│       └── logger.py              # 11KB - Logging utilities
├── config/                        # Configuration files (19 YAML files)
│   ├── performance.yaml           # 345 lines - Performance targets
│   ├── modes.yaml                 # Mode detection patterns
│   ├── session.yaml               # Session management settings
│   ├── logging.yaml               # Logging configuration
│   ├── compression.yaml           # Token efficiency settings
│   └── ...                        # Additional configuration files
├── patterns/                      # Pattern storage
│   ├── dynamic/                   # Runtime pattern detection (mode_detection.yaml, mcp_activation.yaml)
│   ├── learned/                   # User preferences (user_preferences.yaml, project_optimizations.yaml)
│   └── minimal/                   # Project patterns (python_project.yaml, react_project.yaml)
├── docs/                          # Documentation
└── settings.json                  # Claude Code hook configuration
```

## Key Components

### Lifecycle Hooks

1. **session_start.py** (703 lines)
   - Runs at session start with 10-second timeout
   - Detects project type and loads appropriate patterns
   - Activates modes based on user input (brainstorming, task management, etc.)
   - Routes to appropriate MCP servers

2. **pre_tool_use.py**
   - Runs before each tool use with 15-second timeout
   - Selects MCP servers based on operation type
   - Applies performance optimizations

3. **post_tool_use.py** 
   - Runs after tool execution with 10-second timeout
   - Validates results and logs learning data
   - Updates effectiveness tracking

4. **pre_compact.py**
   - Runs before token compression with 15-second timeout
   - Applies compression strategies based on content type
   - Preserves important content while optimizing tokens

5. **notification.py**
   - Handles notifications with 10-second timeout
   - Updates pattern caches and configurations

6. **stop.py**
   - Runs at session end with 15-second timeout
   - Generates session analytics and saves learning data

7. **subagent_stop.py**
   - Handles subagent coordination with 15-second timeout
   - Tracks delegation performance

### Shared Modules

Core functionality shared across hooks:

- **pattern_detection.py** (45KB) - Project and operation pattern recognition
- **learning_engine.py** (40KB) - User preference and effectiveness tracking  
- **validate_system.py** (32KB) - System validation and health checks
- **mcp_intelligence.py** (31KB) - MCP server routing logic
- **compression_engine.py** (27KB) - Token optimization algorithms
- **intelligence_engine.py** (18KB) - Core intelligence coordination
- **yaml_loader.py** (16KB) - Configuration file loading
- **framework_logic.py** (12KB) - SuperClaude framework implementation
- **logger.py** (11KB) - Logging and debugging utilities

## Integration with SuperClaude

The Framework-Hooks system implements SuperClaude framework patterns through lifecycle hooks:

### Mode Detection and Activation

The session_start hook detects user intent and activates appropriate SuperClaude modes:

1. **Brainstorming Mode** - Activated for ambiguous requests ("not sure", "thinking about")
2. **Task Management Mode** - Activated for multi-step operations and complex builds
3. **Token Efficiency Mode** - Activated during resource constraints or when brevity requested
4. **Introspection Mode** - Activated for meta-analysis requests

### MCP Server Routing

The hooks route operations to appropriate MCP servers based on detected patterns:

- **Context7** - Library documentation and framework patterns
- **Sequential** - Multi-step reasoning and complex analysis  
- **Magic** - UI component generation and design systems
- **Playwright** - Browser automation and testing
- **Morphllm** - File editing with pattern optimization
- **Serena** - Semantic analysis and memory management

### Framework Implementation

The hooks implement core SuperClaude concepts:

- **Rules Compliance** - File operation validation and security protocols
- **Principles Enforcement** - Evidence-based decisions and code quality standards
- **Performance Targets** - Sub-200ms operation targets with monitoring
- **Configuration Management** - YAML-driven behavior customization

The system provides SuperClaude framework functionality through Python hooks that run during Claude Code execution, enabling intelligent behavior based on project patterns and user preferences while maintaining performance targets defined in the configuration files.