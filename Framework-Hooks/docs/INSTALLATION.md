# Installation Guide

Framework-Hooks provides intelligent session management for Claude Code through Python hooks that run at specific lifecycle events.

## Prerequisites

- Python 3.8+ (Python 3.x required by hook scripts)
- Claude Code application
- Write access to your system's hook installation directory

## Installation Steps

### 1. Verify Python Installation

```bash
python3 --version
# Should show Python 3.8 or higher
```

### 2. Clone or Extract Framework-Hooks

Place the Framework-Hooks directory in your SuperClaude installation:

```
YourProject/
├── SuperClaude/
│   └── Framework-Hooks/    # This repository
└── other-files...
```

### 3. Install Hook Scripts

Framework-Hooks includes pre-configured hook registration files:

- `settings.json` - Claude Code hook configuration
- `superclaude-config.json` - SuperClaude framework settings

These files configure 7 hooks to run at specific lifecycle events:
- `session_start.py` - Session initialization (<50ms target)
- `pre_tool_use.py` - Tool preparation (<200ms target)
- `post_tool_use.py` - Tool usage recording (<100ms target)
- `pre_compact.py` - Context compression (<150ms target)
- `notification.py` - Notification handling (<50ms target)
- `stop.py` - Session cleanup (<100ms target)
- `subagent_stop.py` - Subagent coordination (<100ms target)

### 4. Directory Structure Verification

After installation, verify this structure exists:

```
Framework-Hooks/
├── hooks/
│   ├── session_start.py
│   ├── pre_tool_use.py
│   ├── post_tool_use.py
│   ├── pre_compact.py
│   ├── notification.py
│   ├── stop.py
│   ├── subagent_stop.py
│   └── shared/                  # 9 shared modules
│       ├── framework_logic.py
│       ├── compression_engine.py
│       ├── learning_engine.py
│       ├── mcp_intelligence.py
│       ├── pattern_detection.py
│       ├── intelligence_engine.py
│       ├── logger.py
│       ├── yaml_loader.py
│       └── validate_system.py
├── config/                      # 12+ YAML configuration files
│   ├── session.yaml
│   ├── performance.yaml
│   ├── compression.yaml
│   ├── modes.yaml
│   ├── mcp_orchestration.yaml
│   ├── orchestrator.yaml
│   ├── logging.yaml
│   └── validation.yaml
├── patterns/                    # 3-tier pattern system
│   ├── minimal/                 # Basic patterns (3-5KB each)
│   ├── dynamic/                 # Feature-specific (8-12KB each)
│   └── learned/                 # User adaptations (10-20KB each)
├── cache/                       # Runtime cache directory
└── docs/                        # Documentation
```

### 5. Configuration Check

The system ships with conservative defaults:

- **Logging**: Disabled by default (`logging.yaml` has `enabled: false`)
- **Performance targets**: session_start <50ms, pre_tool_use <200ms
- **Timeouts**: 10-15 seconds per hook execution
- **All hooks enabled**: via settings.json configuration

### 6. Test Installation

Run the validation system to verify installation:

```bash
cd Framework-Hooks/hooks/shared
python3 validate_system.py --check-installation
```

This will verify:
- Python dependencies available
- All hook files are executable
- Configuration files are valid YAML
- Required directories exist
- Shared modules can be imported

## Verification

### Quick Test

Start a Claude Code session. You should see hook execution if logging is enabled (edit `config/logging.yaml` to enable logging).

### Check Hook Registration

The hooks register automatically through:
- `settings.json` - Defines 7 hooks with 10-15 second timeouts
- Commands like `python3 ~/.claude/hooks/session_start.py`
- Universal matcher `"*"` applies to all sessions

### Performance Verification

Hooks should execute within performance targets:
- Session start: <50ms
- Pre tool use: <200ms
- Post tool use: <100ms
- Other hooks: <100-150ms each

## Configuration

### Default Settings

All hooks start **enabled** with conservative defaults:
- Logging **disabled** (`config/logging.yaml`)
- Error-only log level
- 30-day log retention
- Privacy-safe logging (sanitizes user content)

### Enable Logging (Optional)

To see hook activity, edit `config/logging.yaml`:

```yaml
logging:
  enabled: true
  level: "INFO"  # or DEBUG for verbose output
```

### Pattern System

The 3-tier pattern system loads automatically:
- **minimal/**: Basic project detection (always loaded)
- **dynamic/**: Feature-specific patterns (loaded on demand)
- **learned/**: User-specific adaptations (evolve with usage)

## Next Steps

After installation:

1. **Normal Usage**: Start Claude Code sessions normally - hooks run automatically
2. **Monitor Performance**: Check that hooks execute within target times
3. **Review Logs**: Enable logging to see hook decisions and learning
4. **Customize Patterns**: Add project-specific patterns to `patterns/` directories

## What Framework-Hooks Does

Once installed, the system automatically:

1. **Detects project type** and loads appropriate patterns
2. **Activates relevant modes** and MCP servers based on context  
3. **Applies learned preferences** from previous sessions
4. **Optimizes performance** based on resource constraints
5. **Learns from usage patterns** to improve future sessions

The system operates transparently - no manual invocation required.

## Troubleshooting

If you encounter issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common problems and solutions.