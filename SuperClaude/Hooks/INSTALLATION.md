# SuperClaude Hooks Installation Guide

**Complete guide for installing and configuring SuperClaude hooks with Claude Code compliance.**

## 🚀 Quick Installation

### Automated Installation (Recommended)

```bash
# Navigate to SuperClaude project
cd /path/to/SuperClaude

# Install dependencies (optional but recommended)
pip install -r Hooks/requirements.txt

# Run automated installer
python3 Hooks/scripts/install_hooks.py
```

**Expected Output**:
```
🚀 SuperClaude Hooks Installation
==================================================
🔍 Checking prerequisites...
✅ Python 3.12 detected
✅ SuperClaude project structure validated
✅ All hook files validated
📁 Creating settings directory: /home/user/.claude
✅ Settings directory ready
⚙️ Installing hooks configuration...
✅ Configuration installed: /home/user/.claude/settings.json
✅ Validating installation...
✅ Installation validation passed
⚡ Running performance tests...
✅ Performance tests passed

✅ SuperClaude Hooks installation completed successfully!
```

### Prerequisites

The SuperClaude Hooks system has minimal dependencies:

**Required:**
- Python 3.8 or higher
- PyYAML 6.0+ (for configuration loading)

**Optional but Recommended:**
- psutil 5.9+ (for resource monitoring)

```bash
# Install all dependencies
pip install -r SuperClaude/Hooks/requirements.txt

# Or install individually
pip install PyYAML>=6.0.1  # Required for performance target configuration
pip install psutil>=5.9.0   # Optional for CPU/memory monitoring
```

### Manual Installation

If automated installation fails, follow these manual steps:

#### 1. Prerequisites Check

```bash
# Verify Python version (3.8+ required)
python3 --version

# Verify dependencies
python3 -c "import yaml; print('PyYAML installed:', yaml.__version__)"
python3 -c "import psutil; print('psutil installed:', psutil.__version__)" 2>/dev/null || echo "psutil not installed (optional)"

# Verify SuperClaude structure
ls SuperClaude/Hooks/framework_coordinator/hook.py
ls SuperClaude/Hooks/session_lifecycle/hook.py
ls SuperClaude/Hooks/performance_monitor/hook.py
ls SuperClaude/Hooks/quality_gates/hook.py
```

#### 2. Create Settings Directory

```bash
# Create Claude Code settings directory
mkdir -p ~/.claude
```

#### 3. Install Configuration

```bash
# Copy template and customize
cp SuperClaude/Hooks/config/settings-template.json ~/.claude/settings.json

# Update paths in settings.json (replace /path/to/SuperClaude with actual path)
sed -i 's|$CLAUDE_PROJECT_DIR|/absolute/path/to/SuperClaude|g' ~/.claude/settings.json
```

#### 4. Validate Installation

```bash
# Test all hooks
python3 SuperClaude/Hooks/scripts/test_hooks.py

# Should output: 🎯 Overall Result: ✅ PASS
```

## 🔧 Configuration Details

### Settings File Location

The hooks configuration is stored in Claude Code's standard location:
- **Linux/macOS**: `~/.claude/settings.json`
- **Windows**: `%USERPROFILE%\.claude\settings.json`

### Configuration Structure

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /absolute/path/to/SuperClaude/Hooks/framework_coordinator/hook.py",
            "timeout": 5,
            "description": "Framework Coordinator - MCP suggestions and compliance"
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
            "command": "python3 /absolute/path/to/SuperClaude/Hooks/session_lifecycle/hook.py", 
            "timeout": 3,
            "description": "Session Lifecycle - Checkpoint triggers and session management"
          },
          {
            "type": "command",
            "command": "python3 /absolute/path/to/SuperClaude/Hooks/performance_monitor/hook.py",
            "timeout": 2,
            "description": "Performance Monitor - Real-time performance tracking"
          }
        ]
      },
      {
        "matcher": "Edit|Write|MultiEdit|edit_file|write_file",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /absolute/path/to/SuperClaude/Hooks/quality_gates/hook.py",
            "timeout": 8,
            "description": "Quality Gates - 8-step validation system"
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
            "command": "python3 /absolute/path/to/SuperClaude/Hooks/session_lifecycle/hook.py",
            "timeout": 5,
            "description": "Session Lifecycle - Initialize session tracking"
          }
        ]
      }
    ]
  }
}
```

### Hook-Specific Configuration

Create `SuperClaude/Hooks/config/superclaude-config.json` for advanced settings:

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
    "block_on_syntax": true,
    "performance_validation": true,
    "documentation_validation": true
  },
  "performance_monitor": {
    "real_time_tracking": true,
    "optimization_suggestions": true,
    "history_retention_days": 30
  },
  "session_lifecycle": {
    "auto_checkpoint_intervals": 30,
    "high_risk_operations": ["rm ", "git reset", "DROP"],
    "project_detection": true
  }
}
```

## 🧪 Verification & Testing

### Basic Verification

```bash
# Test hook execution
echo '{"tool":{"name":"Read","args":{}}}' | python3 SuperClaude/Hooks/framework_coordinator/hook.py
echo $?  # Should be 0 or 1

# Test JSON input processing
echo '{"session_id":"test","tool":{"name":"Edit","args":{"file_path":"/tmp/test.py"}}}' | \
  python3 SuperClaude/Hooks/quality_gates/hook.py
```

### Comprehensive Testing

```bash
# Run full test suite
python3 SuperClaude/Hooks/scripts/test_hooks.py

# Expected results:
# ✅ framework_coordinator: 4/4 passed (100%)
# ✅ session_lifecycle: 4/4 passed (100%)
# ✅ performance_monitor: 4/4 passed (100%)
# ✅ quality_gates: 4/4 passed (100%)
# 🎯 Overall Result: ✅ PASS
```

### Performance Validation

```bash
# Check performance against targets
time echo '{}' | python3 SuperClaude/Hooks/performance_monitor/hook.py
# Should complete in <100ms

# Benchmark all hooks
for hook in framework_coordinator session_lifecycle performance_monitor quality_gates; do
  echo "Testing $hook..."
  time echo '{"tool":{"name":"Test"}}' | python3 SuperClaude/Hooks/$hook/hook.py
done
```

### Integration Testing with Claude Code

```bash
# Test with actual Claude Code (if installed)
claude-code --help 2>&1 | grep -i "SuperClaude Hook"

# Run a simple command to trigger hooks
echo "print('hello')" > test.py
claude-code "edit this file" 2>hooks.log
grep "SuperClaude Hook" hooks.log
```

## 🔍 Troubleshooting

### Common Installation Issues

#### Issue: "Python 3.8+ required"
```bash
# Check Python version
python3 --version
# If < 3.8, install newer Python

# Ubuntu/Debian
sudo apt update && sudo apt install python3.9

# macOS with Homebrew
brew install python@3.9

# Update symlink if needed
which python3
```

#### Issue: "No module named 'yaml'"
```bash
# Install PyYAML
pip install PyYAML>=6.0.1

# Or with pip3
pip3 install PyYAML>=6.0.1

# If permission denied
pip install --user PyYAML>=6.0.1
```

#### Issue: "Performance targets using fallback values"
```bash
# Check if PyYAML is installed
python3 -c "import yaml; print(yaml.__version__)"

# Verify performance_targets.yaml exists
ls SuperClaude/Hooks/Resources/performance_targets.yaml

# Test YAML loading
python3 -c "import yaml; print(yaml.safe_load(open('SuperClaude/Hooks/Resources/performance_targets.yaml')))"
```

#### Issue: "Missing required directory"
```bash
# Verify SuperClaude structure
find SuperClaude -name "*.py" -path "*/Hooks/*" | head -10

# If structure is incorrect, re-clone SuperClaude
git clone https://github.com/YourOrg/SuperClaude.git
```

#### Issue: "Hook execution failed"
```bash
# Check individual hook
python3 SuperClaude/Hooks/framework_coordinator/hook.py
# Look for import errors or syntax issues

# Check Python path
export PYTHONPATH="$PYTHONPATH:$(pwd)/SuperClaude/Hooks/common"
```

#### Issue: "Configuration not found"
```bash
# Verify settings file exists
ls -la ~/.claude/settings.json

# Check JSON syntax
python3 -m json.tool ~/.claude/settings.json

# Recreate if corrupted
cp SuperClaude/Hooks/config/settings-template.json ~/.claude/settings.json
```

### Runtime Issues

#### "Bad substitution" errors
```bash
# Check variable format in settings
grep "CLAUDE_PROJECT_DIR" ~/.claude/settings.json
# Should use $VAR format, not ${VAR}

# Fix if needed
sed -i 's/${CLAUDE_PROJECT_DIR}/$CLAUDE_PROJECT_DIR/g' ~/.claude/settings.json
```

#### "Hook timeout" warnings
```bash
# Check hook performance
python3 SuperClaude/Hooks/scripts/test_hooks.py | grep "ms"

# Increase timeout in settings.json if needed
# Default timeouts: Framework(5s), Session(3s), Performance(2s), Quality(8s)
```

#### "Permission denied" errors
```bash
# Check file permissions
ls -la SuperClaude/Hooks/*/hook.py

# Fix permissions if needed
chmod +x SuperClaude/Hooks/*/hook.py
```

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
# Create debug config
cat > SuperClaude/Hooks/config/superclaude-config.json << EOF
{
  "performance_target_ms": 1000,
  "error_handling": "verbose",
  "logging_enabled": true,
  "debug_mode": true
}
EOF

# Run with debug output
echo '{"tool":{"name":"Debug"}}' | python3 SuperClaude/Hooks/framework_coordinator/hook.py 2>&1
```

### Log Analysis

```bash
# Capture hook logs during Claude Code usage
claude-code "some command" 2>debug.log

# Analyze logs
grep "SuperClaude Hook" debug.log
grep "Error" debug.log
grep "Performance" debug.log
```

## 🔄 Migration from Previous Versions

### From Array-Format Configuration

If you have old SuperClaude hooks using array format:

```bash
# Backup old configuration
cp ~/.claude/settings.json ~/.claude/settings.json.backup

# Use migration script
python3 SuperClaude/Hooks/scripts/migrate_config.py
```

### From Command-Line Hook Arguments

Old hooks using `sys.argv` are automatically compatible with the new JSON stdin format. No migration needed.

## ⚙️ Advanced Configuration

### Custom Hook Matchers

Customize which tools trigger specific hooks:

```json
{
  "matcher": "Read|Write|Edit",
  "hooks": [...]
}
```

**Available Matchers**:
- `*`: All tools
- `Read|Write|Edit`: Specific tools
- `serena_*`: Serena MCP tools
- `Bash`: Command execution
- `MultiEdit`: Batch file operations

### Performance Tuning

Adjust performance targets per environment:

```json
{
  "performance_target_ms": 200,
  "quality_gates": {
    "timeout_override": 10000,
    "skip_slow_validations": true
  }
}
```

### Selective Hook Activation

Disable specific hooks without removing configuration:

```json
{
  "hooks": {
    "PreToolUse": [],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command", 
            "command": "python3 /path/to/performance_monitor/hook.py",
            "timeout": 2
          }
        ]
      }
    ]
  }
}
```

## 📊 Monitoring & Maintenance

### Performance Monitoring

```bash
# Check performance trends
tail -f SuperClaude/Hooks/performance_monitor/metrics.jsonl

# Generate performance report
python3 SuperClaude/Hooks/scripts/performance_report.py
```

### Log Rotation

```bash
# Clean old performance logs (if accumulated)
find SuperClaude/Hooks -name "*.jsonl" -mtime +30 -delete

# Archive logs
tar -czf hooks-logs-$(date +%Y%m%d).tar.gz SuperClaude/Hooks/*/logs/
```

### Health Checks

```bash
# Regular health check
python3 SuperClaude/Hooks/scripts/health_check.py

# Schedule periodic checks (cron example)
# 0 */6 * * * /path/to/SuperClaude/Hooks/scripts/health_check.py
```

## 🚀 Next Steps

After successful installation:

1. **Test Integration**: Run a few Claude Code commands to see hooks in action
2. **Review Logs**: Monitor stderr output for hook suggestions and validations
3. **Customize Configuration**: Adjust settings based on your workflow
4. **Enable Advanced Features**: Explore SESSION_LIFECYCLE.md integration
5. **Monitor Performance**: Use the performance monitor to optimize your development process

## 📞 Support

If you encounter issues:

1. **Check Prerequisites**: Ensure Python 3.8+ and proper SuperClaude structure
2. **Run Diagnostics**: `python3 SuperClaude/Hooks/scripts/test_hooks.py`
3. **Review Logs**: Check hook output in Claude Code stderr
4. **Consult Documentation**: See README.md for detailed hook information
5. **Report Issues**: Submit issues to SuperClaude repository

---

*The SuperClaude Hooks System enhances your Claude Code experience with intelligent framework coordination and comprehensive quality validation.*