# SuperClaude Hooks System

**Claude Code compliant hooks system providing intelligent framework coordination, session management, performance monitoring, and quality validation.**

## 🎯 Overview

The SuperClaude Hooks System integrates seamlessly with Claude Code to provide:

- **Framework Coordinator**: MCP server suggestions and framework compliance validation
- **Session Lifecycle**: Automatic checkpoint triggers and session state management  
- **Performance Monitor**: Real-time performance tracking against strict targets (<100ms)
- **Quality Gates**: 8-step validation system for code quality and security

## 🚀 Quick Start

### Installation

```bash
# Clone or navigate to SuperClaude project
cd SuperClaude

# Run automated installation
python3 Hooks/scripts/install_hooks.py
```

### Verification

```bash
# Test all hooks for compliance
python3 Hooks/scripts/test_hooks.py

# Manual hook test
echo '{"tool":{"name":"Read","args":{}}}' | python3 Hooks/framework_coordinator/hook.py
```

## 🏗️ Architecture

### Hook Events & Triggers

| Event | Hook | Trigger | Performance Target |
|-------|------|---------|-------------------|
| `PreToolUse` | Framework Coordinator | All tools (`*`) | <100ms |
| `PreToolUse` | Token Efficiency | `mcp__serena__write_memory` | <100ms |
| `PostToolUse` | Session Lifecycle | All tools (`*`) | <100ms |
| `PostToolUse` | Performance Monitor | All tools (`*`) | <100ms |
| `PostToolUse` | Quality Gates | File operations | <8000ms |
| `SessionStart` | Session Lifecycle | Session initialization | <100ms |

### Component Overview

```
SuperClaude/Hooks/
├── framework_coordinator/    # MCP suggestions & framework compliance
├── session_lifecycle/        # Checkpoint triggers & session management
├── performance_monitor/      # Real-time performance tracking
├── quality_gates/           # 8-step validation system
├── token_efficiency/        # Automatic --uc flag injection for memory operations
├── common/                  # Shared utilities and base classes
├── config/                  # Configuration templates and settings
└── scripts/                 # Installation and testing scripts
```

## 🔧 Configuration

### Settings File Structure

The hooks use Claude Code's standard settings format at `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/SuperClaude/Hooks/framework_coordinator/hook.py",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*", 
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/SuperClaude/Hooks/session_lifecycle/hook.py",
            "timeout": 3
          },
          {
            "type": "command",
            "command": "python3 /path/to/SuperClaude/Hooks/performance_monitor/hook.py",
            "timeout": 2
          }
        ]
      },
      {
        "matcher": "Edit|Write|MultiEdit|edit_file",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/SuperClaude/Hooks/quality_gates/hook.py",
            "timeout": 8
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command", 
            "command": "python3 /path/to/SuperClaude/Hooks/session_lifecycle/hook.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Advanced Configuration

Individual hooks can be configured via `SuperClaude/Hooks/config/superclaude-config.json`:

```json
{
  "performance_target_ms": 100,
  "error_handling": "graceful",
  "logging_enabled": true,
  "framework_coordination": true,
  "quality_gates": {
    "enabled": true,
    "validation_steps": 8,
    "block_on_security": true,
    "block_on_syntax": true
  }
}
```

## 📊 Hook Details

### Framework Coordinator Hook

**Purpose**: Provides intelligent MCP server suggestions and framework compliance validation.

**Capabilities**:
- Auto-detects when Sequential MCP should be activated (complex analysis)
- Suggests Context7 for library/framework usage
- Recommends Magic for UI component work
- Suggests Serena for large-scale operations
- Validates framework compliance patterns

**Example Output**:
```
💡 MCP Suggestion: Complex analysis detected - Sequential MCP recommended → --seq flag
🎯 Framework Pattern: I/O operation detected - Consider performance monitoring → --perf flag
```

### Session Lifecycle Hook

**Purpose**: Manages session state and automatic checkpoint coordination.

**Capabilities**:
- Detects SuperClaude projects and suggests `/sc:load`
- Triggers automatic checkpoints based on:
  - Time intervals (every 30 minutes)
  - High-priority task completion
  - High-risk operations (deletions, config changes)
  - Error recovery scenarios
- Maintains session tracking and context preservation

**Example Output**:
```
🚀 Session started - checking for project initialization
💡 SuperClaude project detected - consider running /sc:load for enhanced context
💾 Checkpoint suggested: High-risk operation detected
```

### Performance Monitor Hook

**Purpose**: Real-time performance tracking against strict PRD targets.

**Capabilities**:
- Monitors all tool execution timing
- Classifies operations by type for appropriate targets:
  - Memory operations: <200ms
  - Project loading: <500ms
  - Session save: <2000ms
  - General operations: <2000ms
- Tracks resource usage (CPU, memory)
- Generates optimization suggestions
- Maintains performance history

**Example Output**:
```
🟢 Read (context_loading): 45ms (target: 500ms, efficiency: 91%)
🟡 Edit (general_operations): 1600ms (target: 2000ms, efficiency: 80%)
⚠️  WARNING: 1.2x target approached
   💡 Optimization suggestions:
      • Check disk I/O performance
      • Consider batching multiple writes
```

### Quality Gates Hook

**Purpose**: 8-step validation system ensuring code quality and security.

**Validation Steps**:
1. **Syntax Validation**: AST parsing for Python, node for JavaScript
2. **Type Analysis**: mypy for Python, tsc for TypeScript
3. **Lint Rules Compliance**: flake8, eslint integration
4. **Security Assessment**: Pattern-based security vulnerability detection
5. **E2E Testing Readiness**: Testability analysis and test coverage
6. **Performance Analysis**: Performance anti-pattern detection
7. **Documentation Completeness**: Docstring and comment analysis
8. **Integration Testing Validation**: Integration readiness assessment

**Example Output**:
```
🔍 Quality Gates Validation Summary:
  ✅ 1. Syntax Validation: 3/3 passed
  ✅ 2. Type Analysis: 3/3 passed  
  ⚠️ 3. Lint Rules Compliance: 2/3 passed
    ❌ main.py: Line 45: Line too long (125 > 120)
  ✅ 4. Security Assessment: 3/3 passed
```

### Token Efficiency Hook

**Purpose**: Automatically applies `--uc` flag to `mcp__serena__write_memory` operations to enable Token Efficiency mode compression.

**Features**:
- Intercepts all memory write operations
- Adds `--uc` flag to enable 30-50% token reduction
- Applies symbol systems and abbreviations per MODE_Token_Efficiency.md
- Maintains ≥95% information preservation quality
- Zero performance impact (<100ms execution time)

**Trigger**: `PreToolUse` event for `mcp__serena__write_memory` tool

**Configuration**:
- Automatically activated for all memory write operations
- No user configuration required
- Transparent operation with no user-visible changes

**Example Operation**:
```
# Original memory write
mcp__serena__write_memory("project_purpose", content)

# Hook automatically adds --uc flag
mcp__serena__write_memory("project_purpose", content, {"flags": ["--uc"]})
```

**Performance**: Target <100ms execution time to maintain framework standards.

## 🎛️ Performance Targets

All hooks are designed to meet strict performance requirements:

| Hook | Target | Typical Performance |
|------|--------|-------------------|
| Framework Coordinator | <100ms | ~35ms |
| Session Lifecycle | <100ms | ~32ms |
| Performance Monitor | <100ms | ~47ms |
| Quality Gates | <8000ms | ~2500ms |
| Token Efficiency | <100ms | ~15ms |

Performance is continuously monitored and optimized. The Performance Monitor hook tracks actual vs. target performance in real-time.

## 🧪 Testing

### Automated Testing

```bash
# Run comprehensive test suite
python3 SuperClaude/Hooks/scripts/test_hooks.py

# Expected output:
# ✅ framework_coordinator: 4/4 passed (100%)
# ✅ session_lifecycle: 4/4 passed (100%) 
# ✅ performance_monitor: 4/4 passed (100%)
# ✅ quality_gates: 4/4 passed (100%)
# ✅ token_efficiency: 4/4 passed (100%)
# 🎯 Overall Result: ✅ PASS
```

### Manual Testing

```bash
# Test individual hook
echo '{"tool":{"name":"Edit","args":{"file_path":"/tmp/test.py"}}}' | \
  python3 SuperClaude/Hooks/quality_gates/hook.py

# Test with invalid JSON (should handle gracefully)
echo 'invalid json{' | python3 SuperClaude/Hooks/framework_coordinator/hook.py
```

### Performance Benchmarking

```bash
# Time hook execution
time echo '{}' | python3 SuperClaude/Hooks/performance_monitor/hook.py

# Should complete in <100ms
```

## 🔍 Troubleshooting

### Common Issues

#### "No module named 'base_hook'"
```bash
# Ensure common directory is accessible
ls SuperClaude/Hooks/common/base_hook.py

# Check Python path in hook files
grep -n "sys.path.insert" SuperClaude/Hooks/*/hook.py
```

#### "Hook execution timeout"
```bash
# Check hook performance
python3 SuperClaude/Hooks/scripts/test_hooks.py

# Verify no blocking operations
strace -e trace=file python3 SuperClaude/Hooks/quality_gates/hook.py
```

#### "Bad substitution" errors
```bash
# Verify settings.json uses correct variable format
grep -n "CLAUDE_PROJECT_DIR" ~/.claude/settings.json

# Should use $CLAUDE_PROJECT_DIR (not ${CLAUDE_PROJECT_DIR})
```

### Debug Mode

Enable detailed logging by modifying `SuperClaude/Hooks/config/superclaude-config.json`:

```json
{
  "logging_enabled": true,
  "performance_target_ms": 1000,
  "error_handling": "verbose"
}
```

### Log Analysis

Hook output appears in Claude Code's stderr stream:

```bash
# Run Claude Code and capture hook output
claude-code --some-command 2>hooks.log

# Analyze hook logs
grep "SuperClaude Hook" hooks.log
```

## 🚀 Integration with SuperClaude Framework

### Framework Compliance

The hooks system integrates deeply with SuperClaude's framework:

- **ORCHESTRATOR.md**: Auto-activation rules parsed and enforced
- **SESSION_LIFECYCLE.md**: Checkpoint patterns implemented
- **Performance Monitoring**: Targets from Resources/performance_targets.yaml enforced
- **RULES.md**: Framework rules validated
- **Quality Gates**: 8-step validation cycle implemented

### MCP Server Coordination

Hooks provide intelligent suggestions for MCP server activation:

```
🎯 Context detected → Appropriate MCP server suggested → Enhanced capabilities
```

### Session Management Integration

Seamless integration with SuperClaude session commands:

```
SessionStart → /sc:load suggestion → Work session → Checkpoint triggers → /sc:save
```

## 📈 Performance Metrics

### Real-time Monitoring

The Performance Monitor hook tracks:

- **Execution Time**: Against operation-specific targets
- **Memory Usage**: Delta tracking during operations  
- **CPU Utilization**: High-usage detection and alerting
- **Resource Efficiency**: Optimization opportunity identification

### Historical Analysis

Performance data is stored in `SuperClaude/Hooks/performance_monitor/metrics.jsonl` for trend analysis and optimization.

## 🔒 Security

### Security Validation

The Quality Gates hook includes security pattern detection:

- Hardcoded credentials detection
- Code injection vulnerability scanning
- Shell command injection analysis  
- XSS vulnerability identification

### Secure Execution

All hooks follow secure execution practices:

- No shell command injection vulnerabilities
- Input validation on all JSON data
- Graceful error handling without information leakage
- Minimal privilege execution model

## 🤝 Contributing

### Development Setup

```bash
# Install development dependencies
pip install -r SuperClaude/Hooks/requirements-dev.txt

# Run linting
flake8 SuperClaude/Hooks/

# Run type checking  
mypy SuperClaude/Hooks/
```

### Adding New Hooks

1. Create hook directory: `SuperClaude/Hooks/new_hook/`
2. Implement `hook.py` extending `BaseHook`
3. Add configuration to `settings-template.json`
4. Add tests to `test_hooks.py`
5. Update documentation

### Testing Changes

```bash
# Run full test suite
python3 SuperClaude/Hooks/scripts/test_hooks.py

# Validate performance
python3 SuperClaude/Hooks/scripts/benchmark_hooks.py
```

## 📝 License

Part of the SuperClaude Framework - MIT License

## 🆘 Support

- **Issues**: Report at SuperClaude GitHub repository
- **Documentation**: See SuperClaude/Docs/ for framework documentation
- **Performance**: Run diagnostic: `python3 SuperClaude/Hooks/scripts/diagnose.py`

---

*The SuperClaude Hooks System brings intelligent framework coordination, proactive session management, and comprehensive quality validation to your Claude Code development workflow.*