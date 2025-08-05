# SuperClaude Hooks System Guide

**Complete guide to understanding, implementing, and extending the SuperClaude hooks system for Claude Code integration.**

## 🎯 Overview

The SuperClaude Hooks System provides intelligent framework coordination, session management, performance monitoring, and quality validation through Claude Code's hooks feature. This guide covers everything from basic usage to advanced customization.

## 📚 Table of Contents

- [Quick Reference](#quick-reference)
- [Architecture Deep Dive](#architecture-deep-dive)
- [Hook Implementation Details](#hook-implementation-details)
- [Framework Integration](#framework-integration) 
- [Performance Optimization](#performance-optimization)
- [Troubleshooting Guide](#troubleshooting-guide)
- [Advanced Customization](#advanced-customization)
- [Development Guide](#development-guide)

## 🚀 Quick Reference

### Installation & Setup
```bash
# Automated installation
python3 SuperClaude/Hooks/scripts/install_hooks.py

# Manual verification
python3 SuperClaude/Hooks/scripts/test_hooks.py

# System diagnostic
python3 SuperClaude/Hooks/scripts/hooks_diagnostic.py
```

### Hook Activation
| Event | Hook | Trigger | Output |
|-------|------|---------|--------|
| `PreToolUse` | Framework Coordinator | All tools | MCP suggestions, compliance checks |
| `PreToolUse` | Token Efficiency | `mcp__serena__write_memory` | Adds --uc flag for compression |
| `PostToolUse` | Session Lifecycle | All tools | Checkpoint triggers, session tracking |
| `PostToolUse` | Performance Monitor | All tools | Performance metrics, optimization tips |
| `PostToolUse` | Quality Gates | File operations | 8-step validation results |
| `SessionStart` | Session Lifecycle | Session init | Project detection, /sc:load suggestions |

### Performance Targets
- **Framework Coordinator**: <100ms (avg ~35ms)
- **Session Lifecycle**: <100ms (avg ~32ms)
- **Performance Monitor**: <100ms (avg ~47ms)
- **Quality Gates**: <8000ms (avg ~2500ms)
- **Token Efficiency**: <100ms (avg ~15ms)

## 🏗️ Architecture Deep Dive

### System Architecture

```
Claude Code CLI
      ↓
   Hook Events (PreToolUse, PostToolUse, SessionStart)
      ↓
SuperClaude Hooks System
      ↓
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Framework       │ Session         │ Performance     │ Quality         │
│ Coordinator     │ Lifecycle       │ Monitor         │ Gates           │
│                 │                 │                 │                 │
│ • MCP suggestions│ • Checkpoints  │ • Real-time     │ • 8-step        │
│ • Compliance    │ • /sc:load hints│   metrics       │   validation    │
│ • Tool routing  │ • State tracking│ • Optimization  │ • Security      │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
      ↓
SuperClaude Framework Integration
      ↓
Enhanced Development Experience
```

### Data Flow

1. **Claude Code** executes a tool
2. **Hook Event** triggered (PreToolUse/PostToolUse/SessionStart)
3. **JSON Input** passed via stdin to appropriate hooks
4. **Hooks Process** the input concurrently
5. **Framework Analysis** provides suggestions and validation
6. **Output** returned via stderr to Claude Code
7. **User Experience** enhanced with intelligent suggestions

### Component Interaction

```yaml
Framework_Coordinator:
  reads: ORCHESTRATOR.md, MCP server patterns
  provides: Tool routing suggestions, MCP activation hints
  integrates_with: All other hooks for coordination

Session_Lifecycle:
  reads: SESSION_LIFECYCLE.md, project structure  
  provides: Checkpoint triggers, session state tracking
  integrates_with: Performance Monitor for session metrics

Performance_Monitor:
  reads: Resources/performance_targets.yaml
  provides: Real-time metrics, optimization suggestions
  integrates_with: All hooks for performance validation

Quality_Gates:
  reads: Project files, validation rules
  provides: 8-step validation, security assessment
  integrates_with: Framework Coordinator for compliance
```

## 🔧 Hook Implementation Details

### Framework Coordinator Hook

**Purpose**: Central intelligence for framework coordination and MCP server suggestions.

**Key Features**:
- Analyzes tool usage patterns for MCP server recommendations
- Enforces ORCHESTRATOR.md auto-activation rules
- Provides intelligent tool routing suggestions
- Validates framework compliance patterns

**Implementation Highlights**:
```python
def _generate_framework_suggestions(self, tool_name: str, tool_args: Dict) -> List[Dict]:
    suggestions = []
    
    # Sequential MCP for complex analysis
    if self._should_suggest_sequential(tool_name, tool_args):
        suggestions.append({
            "type": "mcp_activation",
            "server": "sequential", 
            "reason": "Complex analysis detected - Sequential MCP recommended",
            "command": "--seq or --sequential flag"
        })
    
    return suggestions
```

**Output Examples**:
```
💡 MCP Suggestion: Complex analysis detected - Sequential MCP recommended → --seq flag
🎯 Framework Pattern: I/O operation detected - Consider performance monitoring → --perf flag
```

### Session Lifecycle Hook

**Purpose**: Automatic session management and checkpoint coordination based on SESSION_LIFECYCLE.md patterns.

**Key Features**:
- SuperClaude project detection and /sc:load suggestions
- Automatic checkpoint triggers (time-based, task-based, risk-based)
- Session state tracking and context preservation
- Integration with Serena MCP for memory operations

**Checkpoint Triggers**:
```python
def _should_trigger_checkpoint(self, tool_name: str) -> bool:
    # Time-based (every 30 minutes)
    if (current_time - self.last_checkpoint_time) > 1800:
        return True
    
    # High-priority task completion
    if tool_name == "TodoWrite" and high_priority_completed:
        return True
    
    # High-risk operations
    if self._is_high_risk_operation(tool_name, tool_args):
        return True
    
    return False
```

**Output Examples**:
```
🚀 Session started - checking for project initialization
💡 SuperClaude project detected - consider running /sc:load for enhanced context
💾 Checkpoint suggested: High-risk operation detected
   Run /sc:save --checkpoint to preserve current progress
```

### Performance Monitor Hook

**Purpose**: Real-time performance tracking against strict PRD targets with optimization suggestions.

**Key Features**:
- Monitors all tool execution timing against operation-specific targets
- Classifies operations (memory, loading, general) for appropriate benchmarks
- Tracks resource usage (CPU, memory) when available
- Generates actionable optimization suggestions
- Maintains performance history for trend analysis

**Performance Classification**:
```python
def classify_operation(self, tool_name: str, performance_data: Dict[str, Any]) -> str:
    tool_args_str = str(performance_data.get("tool_args", {})).lower()
    
    if any(cmd in tool_args_str for cmd in ["/sc:load", "activate_project"]):
        return "project_loading"  # <500ms target
    elif "serena" in tool_name.lower() or "memory" in tool_name.lower():
        return "memory_operations"  # <200ms target
    else:
        return "general_operations"  # <2000ms target
```

**Output Examples**:
```
🟢 Read (context_loading): 45ms (target: 500ms, efficiency: 91%)
🟡 Edit (general_operations): 1600ms (target: 2000ms, efficiency: 80%)
   💡 Optimization suggestions:
      • Check disk I/O performance
      • Consider batching multiple writes
```

### Quality Gates Hook

**Purpose**: 8-step validation system ensuring comprehensive code quality and security.

**Validation Steps**:
1. **Syntax Validation**: AST parsing for Python, node for JavaScript/TypeScript
2. **Type Analysis**: mypy for Python, tsc for TypeScript, basic type hint coverage
3. **Lint Rules Compliance**: flake8, eslint integration with fallback to basic checks
4. **Security Assessment**: Pattern-based vulnerability detection (hardcoded secrets, injection risks)
5. **E2E Testing Readiness**: Testability analysis, test coverage assessment
6. **Performance Analysis**: Anti-pattern detection, file size checks
7. **Documentation Completeness**: Docstring coverage, comment analysis
8. **Integration Testing Validation**: Import analysis, error handling assessment

**Validation Implementation**:
```python
def _validate_file(self, file_path: str) -> bool:
    validation_success = True
    
    # Execute all 8 validation steps
    for step in [
        self._validate_syntax,
        self._validate_types, 
        self._validate_lint_rules,
        self._validate_security,
        self._validate_testing_readiness,
        self._validate_performance,
        self._validate_documentation,
        self._validate_integration
    ]:
        if not step(file_path, file_ext):
            validation_success = False
    
    return validation_success
```

**Output Examples**:
```
🔍 Quality Gates Validation Summary:
  ✅ 1. Syntax Validation: 3/3 passed
  ✅ 2. Type Analysis: 3/3 passed  
  ⚠️ 3. Lint Rules Compliance: 2/3 passed
    ❌ main.py: Line 45: Line too long (125 > 120)
  ✅ 4. Security Assessment: 3/3 passed
🚨 2 blocking issues found:
  • SECURITY: main.py - Hardcoded password detected
```

## 🔗 Framework Integration

### SuperClaude Framework Compliance

The hooks system integrates deeply with SuperClaude's framework components:

**ORCHESTRATOR.md Integration**:
- Auto-activation rules parsed and enforced by Framework Coordinator
- MCP server suggestions based on tool patterns and complexity analysis
- Framework compliance validation throughout operation lifecycle

**SESSION_LIFECYCLE.md Integration**:
- Checkpoint patterns implemented in Session Lifecycle hook
- Session state management with memory operation integration
- Performance targets enforced across session boundaries

**Performance Monitoring Integration**:
- Strict performance targets from Resources/performance_targets.yaml
- Operation classification for appropriate benchmarking
- Historical performance tracking and trend analysis

**Quality Gates Integration**:
- 8-step validation cycle aligned with framework quality standards
- Security pattern validation against SuperClaude security requirements
- Documentation completeness verification

### Cross-Component Coordination

```yaml
Framework_Flow:
  1. PreToolUse → Framework Coordinator analyzes and suggests
  2. Tool Execution → Claude Code executes with enhanced context
  3. PostToolUse → Multiple hooks validate and track
  4. Session Management → Lifecycle hook maintains state
  5. Performance Tracking → Monitor validates against targets
  6. Quality Validation → Gates ensure comprehensive quality

Integration_Points:
  - Shared configuration via superclaude-config.json
  - Common base classes for consistent behavior
  - Framework parser for .md file integration
  - Cross-hook communication via shared state
```

## ⚡ Performance Optimization

### Performance Targets & Monitoring

All hooks are designed to meet strict performance requirements:

| Hook | Target | Typical | 95th Percentile | Optimization Focus |
|------|--------|---------|-----------------|-------------------|
| Framework Coordinator | <100ms | ~35ms | ~45ms | Pattern matching efficiency |
| Session Lifecycle | <100ms | ~32ms | ~40ms | File system access optimization |
| Performance Monitor | <100ms | ~47ms | ~55ms | Resource monitoring overhead |
| Quality Gates | <8000ms | ~2500ms | ~4000ms | Validation tool integration |

### Optimization Strategies

**Parallel Execution**:
- Hooks run concurrently for different events
- Independent tool validation processes
- Shared resource caching across hooks

**Intelligent Caching**:
- Framework configuration parsed once per session
- Performance metrics cached for trend analysis
- MCP server suggestion patterns cached

**Resource Management**:
- Optional psutil integration for detailed monitoring
- Graceful degradation when tools unavailable
- Minimal memory footprint through efficient data structures

**Performance Profiling**:
```python
# Built-in performance tracking
def _check_performance(self) -> bool:
    elapsed_ms = (time.time() - self.start_time) * 1000
    if elapsed_ms > self.performance_target_ms:
        self._log_error(f"Performance target exceeded: {elapsed_ms:.1f}ms")
        return False
    return True
```

## 🔍 Troubleshooting Guide

### Common Issues & Solutions

#### Hook Execution Failures

**Symptom**: Hooks not executing or failing silently
```bash
# Diagnostic commands
python3 SuperClaude/Hooks/scripts/hooks_diagnostic.py
python3 SuperClaude/Hooks/scripts/test_hooks.py

# Check individual hook
echo '{"test": true}' | python3 SuperClaude/Hooks/framework_coordinator/hook.py
```

**Common Causes**:
- Missing Python dependencies (Base: json, sys, pathlib)
- Incorrect file permissions (`chmod +x *.py`)
- Python path issues (check `sys.path.insert` in hooks)
- Configuration file corruption

#### Performance Issues

**Symptom**: Hooks exceeding performance targets
```bash
# Performance analysis
python3 SuperClaude/Hooks/scripts/comprehensive_test.py
time echo '{}' | python3 SuperClaude/Hooks/quality_gates/hook.py
```

**Optimization Steps**:
1. **Reduce Validation Scope**: Disable expensive validations in development
2. **Optimize Tool Availability**: Install flake8, mypy, eslint for faster validation
3. **Cache Configuration**: Avoid re-parsing framework files
4. **Parallel Processing**: Use concurrent execution where possible

#### Configuration Problems  

**Symptom**: Hooks not triggering or incorrect behavior
```bash
# Validate configuration
python3 -m json.tool ~/.claude/settings.json
grep -n "SuperClaude" ~/.claude/settings.json
```

**Configuration Fixes**:
```bash
# Reinstall configuration
python3 SuperClaude/Hooks/scripts/install_hooks.py

# Migrate old configuration
python3 SuperClaude/Hooks/scripts/migrate_config.py

# Validate settings
python3 SuperClaude/Hooks/scripts/hooks_diagnostic.py
```

#### Framework Integration Issues

**Symptom**: No MCP suggestions or framework compliance errors
```bash
# Test framework integration
python3 SuperClaude/Hooks/scripts/integration_test.py

# Check framework files
ls SuperClaude/Core/ORCHESTRATOR.md
ls SuperClaude/Core/SESSION_LIFECYCLE.md
```

**Integration Fixes**:
1. Ensure SuperClaude framework files exist
2. Verify project directory detection
3. Test with explicit SuperClaude project context
4. Check framework parser functionality

### Debug Mode

Enable detailed logging for troubleshooting:

```json
// SuperClaude/Hooks/config/superclaude-config.json
{
  "performance_target_ms": 1000,
  "error_handling": "verbose",
  "logging_enabled": true,
  "debug_mode": true
}
```

### Log Analysis

```bash
# Capture hook logs during Claude Code usage
claude-code "test command" 2>debug.log

# Analyze logs
grep "SuperClaude Hook" debug.log
grep "Error\|Exception" debug.log
grep "Performance\|ms" debug.log
```

## 🚀 Advanced Customization

### Custom Hook Development

Create new hooks following the established pattern:

```python
#!/usr/bin/env python3
"""
Custom Hook Template

Description of hook functionality and purpose.
Event: PreToolUse|PostToolUse|SessionStart
Priority: Critical|High|Medium|Low
Performance Target: <Xms
"""

import sys
from pathlib import Path

# Add common directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "common"))

from base_hook import BaseHook

class CustomHook(BaseHook):
    """Custom hook implementation"""
    
    def __init__(self):
        super().__init__("CustomHookName")
        # Custom initialization
        
    def execute(self) -> bool:
        """Hook-specific execution logic"""
        try:
            # Implement custom logic here
            return True
        except Exception as e:
            self._log_error(f"Custom hook failed: {e}")
            return False

def main():
    """Main entry point for Claude Code hook execution"""
    hook = CustomHook()
    exit_code = hook.run()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
```

### Configuration Customization

Advanced configuration options:

```json
{
  "performance_target_ms": 100,
  "error_handling": "graceful|verbose|strict",
  "logging_enabled": true,
  "framework_coordination": true,
  
  "quality_gates": {
    "enabled": true,
    "validation_steps": 8,
    "block_on_security": true,
    "block_on_syntax": true,
    "skip_large_files": true,
    "max_file_size_kb": 1000,
    "custom_patterns": {
      "security": ["custom_pattern_1", "custom_pattern_2"],
      "performance": ["avoid_pattern_1"]
    }
  },
  
  "performance_monitor": {
    "targets": {
      "custom_operation": 500,
      "batch_operations": 5000
    },
    "alerts": {
      "warning_threshold": 0.8,
      "critical_threshold": 1.5
    }
  },
  
  "session_lifecycle": {
    "checkpoint_intervals": 30,
    "risk_operations": ["rm ", "DROP", "DELETE"],
    "auto_suggestions": true
  }
}
```

### Matcher Customization

Customize which tools trigger specific hooks:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "serena_*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/custom_serena_hook.py"
          }
        ]
      },
      {
        "matcher": "Read|Write|Edit|Glob|Grep",
        "hooks": [
          {
            "type": "command", 
            "command": "python3 /path/to/file_operations_hook.py"
          }
        ]
      }
    ]
  }
}
```

## 🛠️ Development Guide

### Setting Up Development Environment

```bash
# Clone SuperClaude
git clone https://github.com/YourOrg/SuperClaude.git
cd SuperClaude

# Install development dependencies
pip install flake8 mypy pytest psutil

# Set up hooks for development
python3 Hooks/scripts/install_hooks.py

# Run development tests
python3 Hooks/scripts/comprehensive_test.py
```

### Testing New Features

```bash
# Unit tests
python3 Hooks/scripts/test_hooks.py

# Integration tests  
python3 Hooks/scripts/integration_test.py

# Performance validation
python3 Hooks/scripts/comprehensive_test.py

# Manual testing
echo '{"tool": {"name": "TestTool"}}' | python3 Hooks/custom_hook/hook.py
```

### Code Quality Standards

- **Performance**: All hooks must meet strict timing targets
- **Error Handling**: Graceful degradation on all failure modes
- **Security**: No execution of untrusted input, secure file handling
- **Documentation**: Comprehensive docstrings and inline comments
- **Testing**: >95% test coverage for all hook functionality

### Contributing Guidelines

1. **Fork the Repository**: Create your own fork for development
2. **Create Feature Branch**: `git checkout -b feature/new-hook`
3. **Implement with Tests**: Include comprehensive test coverage
4. **Validate Performance**: Ensure performance targets are met
5. **Update Documentation**: Update relevant .md files
6. **Submit Pull Request**: Include description of changes and test results

### Release Process

1. **Version Bump**: Update VERSION file
2. **Run Full Test Suite**: Ensure all tests pass
3. **Performance Validation**: Verify performance targets
4. **Documentation Update**: Update all relevant documentation
5. **Integration Testing**: Test with actual Claude Code installation
6. **Release Notes**: Document changes and improvements

---

*The SuperClaude Hooks System provides a powerful foundation for enhancing Claude Code with intelligent framework coordination, proactive session management, and comprehensive quality validation. This guide should help you understand, customize, and extend the system to meet your specific development needs.*