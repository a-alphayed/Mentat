# Hook Settings Configuration (`settings.json`)

## Overview

The `settings.json` file defines the Claude Code hook configuration settings for the SuperClaude-Lite framework. This file registers all framework hooks with Claude Code and specifies their execution parameters.

## Purpose and Role

This configuration provides:
- **Hook Registration**: Registers all 7 SuperClaude hooks with Claude Code
- **Execution Configuration**: Defines command paths, timeouts, and execution patterns  
- **Universal Matching**: Applies hooks to all operations through `"matcher": "*"`
- **Timeout Management**: Establishes execution time limits for each hook

## Configuration Structure

### Basic Pattern
```json
{
  "hooks": {
    "HookName": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/script.py",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

### Hook Definitions

The actual configuration registers these hooks:

#### SessionStart Hook
```json
"SessionStart": [
  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command", 
        "command": "python3 ~/.claude/hooks/session_start.py",
        "timeout": 10
      }
    ]
  }
]
```

**Purpose**: Initialize sessions and detect project context
**Timeout**: 10 seconds for session initialization
**Execution**: Runs at the start of every Claude Code session

#### PreToolUse Hook
```json
"PreToolUse": [
  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command",
        "command": "python3 ~/.claude/hooks/pre_tool_use.py", 
        "timeout": 15
      }
    ]
  }
]
```

**Purpose**: Pre-process tool usage and provide intelligent routing
**Timeout**: 15 seconds for analysis and routing decisions
**Execution**: Runs before every tool use operation

#### PostToolUse Hook
```json
"PostToolUse": [
  {
    "matcher": "*", 
    "hooks": [
      {
        "type": "command",
        "command": "python3 ~/.claude/hooks/post_tool_use.py",
        "timeout": 10
      }
    ]
  }
]
```

**Purpose**: Post-process tool results and apply quality gates
**Timeout**: 10 seconds for result analysis and validation
**Execution**: Runs after every tool use operation

#### PreCompact Hook
```json
"PreCompact": [
  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command", 
        "command": "python3 ~/.claude/hooks/pre_compact.py",
        "timeout": 15
      }
    ]
  }
]
```

**Purpose**: Apply intelligent compression before context compaction
**Timeout**: 15 seconds for compression analysis and application
**Execution**: Runs before Claude Code compacts conversation context

#### Notification Hook
```json
"Notification": [
  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command",
        "command": "python3 ~/.claude/hooks/notification.py", 
        "timeout": 10
      }
    ]
  }
]
```

**Purpose**: Handle notifications and update learning patterns
**Timeout**: 10 seconds for notification processing
**Execution**: Runs when Claude Code sends notifications

#### Stop Hook
```json
"Stop": [
  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command",
        "command": "python3 ~/.claude/hooks/stop.py",
        "timeout": 15
      }
    ]
  }
]
```

**Purpose**: Session cleanup and analytics generation
**Timeout**: 15 seconds for cleanup and analysis
**Execution**: Runs when Claude Code session ends

#### SubagentStop Hook
```json
"SubagentStop": [
  {
    "matcher": "*",
    "hooks": [
      {
        "type": "command", 
        "command": "python3 ~/.claude/hooks/subagent_stop.py",
        "timeout": 15
      }
    ]
  }
]
```

**Purpose**: Subagent coordination and task management analytics
**Timeout**: 15 seconds for subagent cleanup
**Execution**: Runs when Claude Code subagent sessions end

## Key Configuration Elements

### Universal Matcher
- **Pattern**: `"matcher": "*"`
- **Effect**: All hooks apply to every operation
- **Purpose**: Ensures consistent framework behavior across all interactions

### Command Type
- **Type**: `"command"`
- **Execution**: Runs external Python scripts
- **Environment**: Uses system Python 3 installation

### File Paths
- **Location**: `~/.claude/hooks/`
- **Naming**: Matches hook names in snake_case (e.g., `session_start.py`)
- **Permissions**: Scripts must be executable

### Timeout Values
- **SessionStart**: 10 seconds (session initialization)
- **PreToolUse**: 15 seconds (analysis and routing)
- **PostToolUse**: 10 seconds (result processing)
- **PreCompact**: 15 seconds (compression)
- **Notification**: 10 seconds (notification handling)
- **Stop**: 15 seconds (cleanup and analytics)
- **SubagentStop**: 15 seconds (subagent coordination)

## Installation Requirements

### File Installation
The framework installation process must:
1. Copy Python hook scripts to `~/.claude/hooks/`
2. Set executable permissions on all hook scripts
3. Install this `settings.json` file for Claude Code to read
4. Verify Python 3 is available in the system PATH

### Dependencies
- Python 3.7+ installation
- Required Python packages (see hook implementations)
- Read/write access to `~/.claude/hooks/` directory
- Network access for MCP server communication (if used)

## Troubleshooting

### Hook Not Executing
- **Check file paths**: Verify scripts exist at specified locations
- **Check permissions**: Ensure scripts are executable
- **Check Python**: Verify Python 3 is available in PATH
- **Check timeouts**: Increase timeout if hooks are timing out

### Performance Issues
- **Timeout Tuning**: Adjust timeout values for your system performance
- **Hook Optimization**: Review hook configuration files for performance settings
- **Parallel Execution**: Some hooks can be optimized for parallel execution

### Path Issues
- **Absolute Paths**: Use absolute paths if relative paths cause issues
- **User Directory**: Ensure `~/.claude/hooks/` expands correctly in your environment
- **File Permissions**: Verify both read and execute permissions on hook files

## Related Documentation

- **Hook Implementation**: Individual hook Python files for specific behavior
- **Configuration Files**: YAML configuration files for hook behavior tuning
- **Installation Guide**: Framework installation and setup documentation