# Troubleshooting Guide

Common issues and solutions for Framework-Hooks based on actual implementation patterns.

## Installation Issues

### Python Import Errors

**Problem**: Hook fails with `ModuleNotFoundError` for shared modules

**Cause**: Python path not finding shared modules in `hooks/shared/`

**Solution**: 
```python
# Each hook script includes this path setup:
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "shared"))
```

Verify the `shared/` directory exists and contains all 9 modules:
- `framework_logic.py`
- `compression_engine.py` 
- `learning_engine.py`
- `mcp_intelligence.py`
- `pattern_detection.py`
- `intelligence_engine.py`
- `logger.py`
- `yaml_loader.py` 
- `validate_system.py`

### Hook Execution Permissions

**Problem**: Hooks fail to execute with permission errors

**Solution**:
```bash
cd Framework-Hooks/hooks
chmod +x *.py
chmod +x shared/*.py
```

The following hooks need execute permissions:
- `pre_compact.py`
- `stop.py` 
- `subagent_stop.py`

### YAML Configuration Errors

**Problem**: Hook fails with YAML parsing errors

**Cause**: Invalid YAML syntax in config files

**Solution**:
```bash
# Test YAML validity
python3 -c "import yaml; yaml.safe_load(open('config/session.yaml'))"
```

Check these configuration files for syntax issues:
- `config/logging.yaml`
- `config/session.yaml`
- `config/performance.yaml`
- `config/compression.yaml`
- All other `.yaml` files in `config/`

## Performance Issues

### Hook Timeout Errors

**Problem**: Hooks timing out (default 10-15 seconds from settings.json)

**Cause**: Performance targets not met:
- session_start.py: >50ms target
- pre_tool_use.py: >200ms target  
- Other hooks: >100-150ms targets

**Diagnosis**:
```bash
# Enable timing logs in config/logging.yaml
logging:
  enabled: true
  level: "INFO"
  hook_logging:
    log_timing: true
```

**Solutions**:
1. **Reduce pattern loading**: Remove unnecessary patterns from `patterns/` directories
2. **Check disk I/O**: Ensure `cache/` directory is writable and has space
3. **Disable verbose features**: Set `logging.level: "ERROR"` 
4. **Check Python performance**: Use faster Python interpreter if available

### Memory Usage Issues

**Problem**: High memory usage during hook execution

**Cause**: Large pattern files or cache accumulation

**Solutions**:
1. **Clear cache**: Remove files from `cache/` directory
2. **Reduce pattern size**: Check for oversized files in `patterns/learned/`
3. **Limit learning data**: Review learning_engine.py cache size limits

### Pattern Loading Slow

**Problem**: Session start delays due to pattern loading

**Cause**: Pattern system loading large files from:
- `patterns/minimal/`: Should be 3-5KB each
- `patterns/dynamic/`: Should be 8-12KB each  
- `patterns/learned/`: Should be 10-20KB each

**Solutions**:
1. **Check pattern sizes**: Identify oversized pattern files
2. **Remove unused patterns**: Delete patterns not relevant to your projects
3. **Reset learned patterns**: Clear `patterns/learned/` to start fresh

## Configuration Issues

### Logging Not Working  

**Problem**: No log output despite enabling logging

**Cause**: Default logging configuration in `config/logging.yaml`:
```yaml
logging:
  enabled: false  # Default is disabled
  level: "ERROR"  # Only shows errors by default
```

**Solution**: Enable logging properly:
```yaml
logging:
  enabled: true
  level: "INFO"    # or "DEBUG" for verbose output
  hook_logging:
    log_lifecycle: true
    log_decisions: true
    log_timing: true
```

### Cache Directory Issues

**Problem**: Hooks fail with cache write errors

**Cause**: Missing or permission issues with `cache/` directory

**Solution**:
```bash
mkdir -p Framework-Hooks/cache/logs
chmod 755 Framework-Hooks/cache
chmod 755 Framework-Hooks/cache/logs
```

Required cache structure:
```
cache/
├── logs/          # Log files (30-day retention)
├── patterns/      # Cached pattern data
├── learning/      # Learning engine data
└── session/       # Session state
```

### MCP Intelligence Failures

**Problem**: MCP server coordination not working

**Cause**: `mcp_intelligence.py` configuration issues

**Diagnosis**: Check `config/mcp_orchestration.yaml` for valid server configurations

**Solution**: Verify MCP server availability and configuration in:
- Context7, Sequential, Magic, Playwright, Morphllm, Serena

## Runtime Issues

### Hook Script Failures

**Problem**: Individual hook scripts crash or fail

**Diagnosis Steps**:

1. **Test hook directly**:
```bash
cd Framework-Hooks/hooks
python3 session_start.py
```

2. **Check imports**: Verify all shared modules import correctly:
```python
from framework_logic import FrameworkLogic
from pattern_detection import PatternDetector  
from mcp_intelligence import MCPIntelligence
from compression_engine import CompressionEngine
from learning_engine import LearningEngine
```

3. **Check YAML loading**:
```python
from yaml_loader import config_loader
config = config_loader.load_config('session')
```

### Learning System Issues

**Problem**: Learning engine not adapting to usage patterns

**Cause**: Learning data not persisting or invalid

**Solutions**:
1. **Check cache permissions**: Ensure `cache/learning/` is writable
2. **Reset learning data**: Remove `cache/learning/*` files to start fresh
3. **Verify pattern detection**: Check that `pattern_detection.py` identifies your project type

### Validation Failures

**Problem**: System validation reports errors

**Run validation manually**:
```bash
cd Framework-Hooks/hooks/shared
python3 validate_system.py --full-check
```

Common validation issues:
- Missing configuration files
- Invalid YAML syntax
- Permission problems
- Missing directories

## Debug Mode

### Enable Comprehensive Debugging

Edit `config/logging.yaml`:
```yaml
logging:
  enabled: true
  level: "DEBUG"
  
development:
  verbose_errors: true
  include_stack_traces: true
  debug_mode: true
```

This provides detailed information about:
- Hook execution flow
- Pattern loading decisions  
- MCP server coordination
- Learning system adaptations
- Performance timing data

### Manual Hook Testing

Test individual hooks outside Claude Code:

```bash
# Test session start
python3 hooks/session_start.py

# Test tool use hooks  
python3 hooks/pre_tool_use.py
python3 hooks/post_tool_use.py

# Test cleanup hooks
python3 hooks/stop.py
```

## System Health Checks

### Automated Validation

Run the comprehensive system check:
```bash
cd Framework-Hooks/hooks/shared  
python3 validate_system.py --health-check
```

This checks:
- File permissions and structure
- YAML configuration validity
- Python module imports
- Cache directory accessibility
- Pattern file integrity

### Performance Monitoring

Enable performance logging:
```yaml
# In config/performance.yaml
performance_monitoring:
  enabled: true
  track_execution_time: true
  alert_on_slow_hooks: true
  target_times:
    session_start: 50    # ms
    pre_tool_use: 200    # ms  
    post_tool_use: 100   # ms
    other_hooks: 100     # ms
```

## Common Error Messages

### "Hook timeout exceeded"
- **Cause**: Hook execution taking longer than 10-15 seconds (settings.json timeout)
- **Solution**: Check performance issues section above

### "YAML load failed"  
- **Cause**: Invalid YAML syntax in configuration files
- **Solution**: Validate YAML files using Python or online validator

### "Pattern detection failed"
- **Cause**: Issues with pattern files or pattern_detection.py
- **Solution**: Check pattern file sizes and YAML validity

### "Learning engine initialization failed"
- **Cause**: Cache directory issues or learning data corruption  
- **Solution**: Clear cache and reset learning data

### "MCP intelligence routing failed"
- **Cause**: MCP server configuration or availability issues
- **Solution**: Check MCP server status and configuration

## Getting Help

### Log Analysis

Logs are written to `cache/logs/` with daily rotation (30-day retention). Check recent logs for detailed error information.

### Clean Installation

To reset to clean state:
```bash
# Backup any custom patterns first
rm -rf cache/
rm -rf patterns/learned/
# Restart Claude Code session
```

### Configuration Reset

To reset all configurations to defaults:
```bash  
git checkout config/*.yaml
# Or restore from backup if modified
```

The system is designed to be resilient with conservative defaults. Most issues resolve with basic file permission fixes and configuration validation.