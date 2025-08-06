# Framework-Hooks

Framework-Hooks is a hook system for Claude Code that provides intelligent session management and context adaptation. It runs Python hooks at different points in Claude Code's lifecycle to optimize performance and adapt behavior based on usage patterns.

## What it does

The system runs 7 hooks that execute at specific lifecycle events:

- `session_start.py` - Initializes session context and activates appropriate features
- `pre_tool_use.py` - Prepares for tool execution and applies optimizations  
- `post_tool_use.py` - Records tool usage patterns and updates learning data
- `pre_compact.py` - Applies compression before context compaction
- `notification.py` - Handles system notifications and adaptive responses
- `stop.py` - Performs cleanup and saves session data at shutdown
- `subagent_stop.py` - Manages subagent cleanup and coordination

## Components

### Hooks
Each hook is a Python script that runs at a specific lifecycle point. Hooks share common functionality through shared modules and can access configuration through YAML files.

### Shared Modules
- `framework_logic.py` - Core logic for SuperClaude framework integration
- `compression_engine.py` - Context compression and optimization
- `learning_engine.py` - Adaptive learning from usage patterns
- `mcp_intelligence.py` - MCP server coordination and routing
- `pattern_detection.py` - Project and usage pattern detection
- `logger.py` - Structured logging for hook operations
- `yaml_loader.py` - Configuration loading utilities
- `validate_system.py` - System validation and health checks

### Configuration
12 YAML configuration files control different aspects:
- `session.yaml` - Session lifecycle settings
- `performance.yaml` - Performance targets and limits  
- `compression.yaml` - Context compression settings
- `modes.yaml` - Mode activation thresholds
- `mcp_orchestration.yaml` - MCP server coordination
- `orchestrator.yaml` - General orchestration settings
- `logging.yaml` - Logging configuration
- `validation.yaml` - System validation rules
- Others for specialized features

### Patterns
3-tier pattern system for adaptability:
- `minimal/` - Basic project detection patterns (3-5KB each)
- `dynamic/` - Feature-specific patterns loaded on demand (8-12KB each)  
- `learned/` - User-specific adaptations that evolve with usage (10-20KB each)

### Cache
The system maintains JSON cache files for:
- User preferences and adaptations
- Project-specific patterns
- Learning records and effectiveness data
- Session state and metrics

## Installation

1. Ensure Python 3.8+ is available
2. Place Framework-Hooks directory in your SuperClaude installation
3. Claude Code will automatically discover and use the hooks

## Usage

Framework-Hooks runs automatically when Claude Code starts a session. You don't need to invoke it manually.

The system will:
1. Detect your project type and load appropriate patterns
2. Activate relevant modes and MCP servers based on context
3. Apply learned preferences from previous sessions
4. Optimize performance based on resource constraints
5. Learn from your usage patterns to improve future sessions

## How it works

### Session Flow
```
Session Start → Load Config → Detect Project → Apply Patterns → 
Activate Features → Work Session → Record Learning → Save State
```

### Hook Coordination
Hooks coordinate through shared state and configuration. Earlier hooks prepare context for later ones, and the system maintains consistency across the entire session lifecycle.

### Learning System
The system tracks what works well for your specific projects and usage patterns. Over time, it adapts thresholds, preferences, and feature activation to match your workflow.

### Performance Targets
- Session initialization: <50ms
- Pattern loading: <100ms per pattern
- Hook execution: <30ms per hook
- Cache operations: <10ms

## Architecture

Framework-Hooks operates as a lightweight layer between Claude Code and the SuperClaude framework. It provides just-in-time intelligence loading instead of loading comprehensive framework documentation upfront.

The hook system allows Claude Code sessions to:
- Start faster by loading only necessary context
- Adapt to project-specific needs automatically  
- Learn from usage patterns over time
- Coordinate MCP servers intelligently
- Apply compression and optimization transparently

## Development

### Adding Hooks
Create new hooks by:
1. Adding a Python file in `hooks/` directory
2. Following existing hook patterns for initialization
3. Using shared modules for common functionality
4. Adding corresponding configuration if needed

### Modifying Configuration  
YAML files in `config/` control hook behavior. Changes take effect on next session start.

### Pattern Development
Add new patterns in appropriate `patterns/` subdirectories following existing YAML structure.

## Troubleshooting

Logs are written to `cache/logs/` directory. Check these files if hooks aren't behaving as expected.

The system includes validation utilities in `validate_system.py` for checking configuration and installation integrity.