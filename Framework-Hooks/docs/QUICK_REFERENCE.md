# Quick Reference

Essential commands and information for Framework-Hooks developers and users.

## System Overview

- **7 hooks**: Execute at specific Claude Code lifecycle events
- **9 shared modules**: Common functionality across hooks
- **12+ config files**: YAML-based configuration system
- **3-tier patterns**: minimal/dynamic/learned pattern system
- **Performance targets**: <50ms to <200ms per hook

## Installation Quick Check

```bash
# Verify Python version
python3 --version  # Need 3.8+

# Check directory structure
ls Framework-Hooks/
# Should see: hooks/ config/ patterns/ cache/ docs/

# Test hook execution
python3 Framework-Hooks/hooks/session_start.py

# Validate system
cd Framework-Hooks/hooks/shared
python3 validate_system.py --check-installation
```

## Configuration Files

| File | Purpose | Key Settings |
|------|---------|-------------|
| `logging.yaml` | System logging | `enabled: false` (default) |
| `performance.yaml` | Timing targets | session_start: 50ms, pre_tool_use: 200ms |
| `session.yaml` | Session lifecycle | Context management, cleanup behavior |
| `compression.yaml` | Content compression | Selective compression rules |
| `mcp_orchestration.yaml` | MCP server routing | Server activation patterns |

## Performance Targets

| Hook | Target Time | Timeout |
|------|-------------|---------|
| session_start.py | <50ms | 10s |
| pre_tool_use.py | <200ms | 15s |
| post_tool_use.py | <100ms | 10s |
| pre_compact.py | <150ms | 15s |
| notification.py | <50ms | 10s |
| stop.py | <100ms | 15s |
| subagent_stop.py | <100ms | 15s |

## Common Operations

### Enable Logging
```yaml
# Edit config/logging.yaml
logging:
  enabled: true
  level: "INFO"  # or DEBUG
```

### Check System Health
```bash
cd Framework-Hooks/hooks/shared
python3 validate_system.py --health-check
```

### Test Individual Hook
```bash
cd Framework-Hooks/hooks
python3 session_start.py       # Test session initialization
python3 pre_tool_use.py        # Test tool preparation
```

### Clear Cache
```bash
# Reset learning data and cache
rm -rf Framework-Hooks/cache/*
# System will recreate on next run
```

### View Recent Logs
```bash
# Check latest logs (if logging enabled)
tail -f Framework-Hooks/cache/logs/hooks-$(date +%Y-%m-%d).log
```

## Hook Execution Flow

```
Session Start → Load Config → Detect Project → Apply Patterns →
Activate Features → [Work Session with Tool Use Hooks] → 
Record Learning → Save State → Session End
```

## Directory Structure

```
Framework-Hooks/
├── hooks/                    # 7 hook scripts
│   ├── session_start.py      # <50ms - Session init
│   ├── pre_tool_use.py       # <200ms - Tool prep
│   ├── post_tool_use.py      # <100ms - Usage recording
│   ├── pre_compact.py        # <150ms - Context compression
│   ├── notification.py       # <50ms - Notifications
│   ├── stop.py               # <100ms - Session cleanup
│   ├── subagent_stop.py      # <100ms - Subagent coordination
│   └── shared/               # 9 shared modules
├── config/                   # 12+ YAML config files
├── patterns/                 # 3-tier pattern system
│   ├── minimal/              # Always loaded (3-5KB each)
│   ├── dynamic/              # On-demand (8-12KB each)
│   └── learned/              # User adaptations (10-20KB each)
├── cache/                    # Runtime cache and logs
└── docs/                     # Documentation
```

## Shared Modules

| Module | Purpose |
|--------|---------|
| `framework_logic.py` | SuperClaude framework integration |
| `compression_engine.py` | Context compression and optimization |
| `learning_engine.py` | Adaptive learning from usage |
| `mcp_intelligence.py` | MCP server coordination |
| `pattern_detection.py` | Project and usage pattern detection |
| `intelligence_engine.py` | Central intelligence coordination |
| `logger.py` | Structured logging system |
| `yaml_loader.py` | Configuration loading utilities |
| `validate_system.py` | System validation and health checks |

## Troubleshooting Quick Fixes

### Hook Timeout
- Check performance targets in `config/performance.yaml`
- Clear cache: `rm -rf cache/*`
- Reduce pattern loading

### Import Errors
```bash
# Verify shared modules path
ls Framework-Hooks/hooks/shared/
# Should show all 9 .py files

# Check permissions
chmod +x Framework-Hooks/hooks/*.py
```

### YAML Errors
```bash
# Validate YAML files
python3 -c "
import yaml, glob
for f in glob.glob('config/*.yaml'):
    yaml.safe_load(open(f))
    print(f'{f}: OK')
"
```

### No Log Output
```yaml
# Enable in config/logging.yaml
logging:
  enabled: true
  level: "INFO"
  hook_logging:
    log_lifecycle: true
```

## Configuration Shortcuts

### Development Mode
```yaml
# config/logging.yaml
logging:
  enabled: true
  level: "DEBUG"
development:
  debug_mode: true
  verbose_errors: true
```

### Production Mode  
```yaml
# config/logging.yaml
logging:
  enabled: false
  level: "ERROR"
```

### Reset to Defaults
```bash
# Backup first, then:
git checkout config/*.yaml
rm -rf cache/
rm -rf patterns/learned/
```

## File Locations

- **Hook scripts**: `hooks/*.py`
- **Configuration**: `config/*.yaml`
- **Logs**: `cache/logs/hooks-YYYY-MM-DD.log`
- **Learning data**: `cache/learning/`
- **Pattern cache**: `cache/patterns/`
- **Installation config**: `settings.json`, `superclaude-config.json`

## Debug Commands

```bash
# Full system validation
python3 hooks/shared/validate_system.py --full-check

# Check configuration integrity
python3 hooks/shared/validate_system.py --check-config

# Test pattern loading
python3 hooks/shared/pattern_detection.py --test-patterns

# Verify learning engine
python3 hooks/shared/learning_engine.py --test-learning
```

## System Behavior

### Default State
- All hooks **enabled** via settings.json
- Logging **disabled** for performance
- Conservative timeouts (10-15 seconds)
- Selective compression preserves user content
- Learning engine adapts to usage patterns

### What Happens Automatically
1. **Project detection** - Identifies project type and loads patterns
2. **Mode activation** - Enables relevant SuperClaude modes
3. **MCP coordination** - Routes to appropriate servers
4. **Performance optimization** - Applies compression and caching
5. **Learning adaptation** - Records and learns from usage

Framework-Hooks operates transparently without requiring manual intervention.