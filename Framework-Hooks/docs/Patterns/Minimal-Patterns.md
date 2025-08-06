# Minimal Patterns: Project Detection and Bootstrap

## Overview

Minimal patterns provide project type detection and initial Framework-Hooks configuration. These patterns are stored in `/patterns/minimal/` and automatically configure MCP server activation and auto-flags based on detected project characteristics.

## Purpose

Minimal patterns handle:

- **Project Detection**: Identify project type from file structure and dependencies
- **MCP Server Selection**: Configure primary and secondary MCP servers  
- **Auto-Flag Configuration**: Set automatic flags for immediate activation
- **Performance Targets**: Define bootstrap timing and context size goals

## Pattern Structure

All minimal patterns follow this YAML structure:

```yaml
project_type: "string"              # Unique project identifier
detection_patterns: []              # File/directory detection rules
auto_flags: []                      # Automatic flag activation
mcp_servers:
  primary: "string"                 # Primary MCP server
  secondary: []                     # Fallback servers
patterns:
  file_structure: []                # Expected project files/dirs
  common_tasks: []                  # Typical operations
intelligence:
  mode_triggers: []                 # Mode activation conditions
  validation_focus: []              # Quality validation priorities
performance_targets:
  bootstrap_ms: number              # Bootstrap time target
  context_size: "string"            # Context footprint target
  cache_duration: "string"          # Cache retention time
```

### Detection Rules

Detection patterns identify projects through:

- **File Extensions**: Look for specific file types (`.py`, `.jsx`, etc.)
- **Dependency Files**: Check for `package.json`, `requirements.txt`, `pyproject.toml`
- **Directory Structure**: Verify expected directories exist
- **Configuration Files**: Detect framework-specific config files

## Current Minimal Patterns

### Python Project Pattern (`python_project.yaml`)

This is the actual pattern file for Python projects:

```yaml
project_type: "python"
detection_patterns:
  - "*.py files present"
  - "requirements.txt or pyproject.toml"
  - "__pycache__/ directories"

auto_flags:
  - "--serena"    # Semantic analysis
  - "--context7"  # Python documentation

mcp_servers:
  primary: "serena"
  secondary: ["context7", "sequential", "morphllm"]

patterns:
  file_structure:
    - "src/ or lib/"
    - "tests/"
    - "docs/"
    - "requirements.txt"
  
  common_tasks:
    - "function refactoring"
    - "class extraction"
    - "import optimization"
    - "testing setup"

intelligence:
  mode_triggers:
    - "token_efficiency: context >75%"
    - "task_management: refactor|test|analyze"
  
  validation_focus:
    - "python_syntax"
    - "pep8_compliance"
    - "type_hints"
    - "testing_coverage"

performance_targets:
  bootstrap_ms: 40
  context_size: "4KB"
  cache_duration: "45min"
```

This pattern automatically activates Serena (for semantic analysis) and Context7 (for Python documentation) when Python projects are detected.

### React Project Pattern (`react_project.yaml`)

```yaml
project_type: "react"
detection_patterns:
  - "package.json with react dependency"
  - "src/ directory with .jsx/.tsx files"
  - "public/index.html"

auto_flags:
  - "--magic"     # UI component generation
  - "--context7"  # React documentation

mcp_servers:
  primary: "magic"
  secondary: ["context7", "morphllm"]

patterns:
  file_structure:
    - "src/components/"
    - "src/hooks/"
    - "src/pages/"
    - "src/utils/"
  
  common_tasks:
    - "component creation"
    - "state management"
    - "routing setup"
    - "performance optimization"

intelligence:
  mode_triggers:
    - "token_efficiency: context >75%"
    - "task_management: build|implement|create"
  
  validation_focus:
    - "jsx_syntax"
    - "react_patterns"
    - "accessibility"
    - "performance"

performance_targets:
  bootstrap_ms: 30
  context_size: "3KB"
  cache_duration: "60min"
```

This pattern activates Magic (for UI component generation) and Context7 (for React documentation) when React projects are detected.

## Creating New Minimal Patterns

### Pattern Creation Process

1. **Identify Project Type**: Determine unique characteristics of the project type
2. **Define Detection Rules**: Create file/directory patterns for identification
3. **Select MCP Servers**: Choose primary and secondary servers for the project type
4. **Configure Auto-Flags**: Set flags that should activate automatically
5. **Define Intelligence**: Specify mode triggers and validation focus
6. **Set Performance Targets**: Define bootstrap time and context size goals

### Pattern Template

```yaml
project_type: "your_project_type"
detection_patterns:
  - "unique file or directory patterns"
  - "dependency or configuration files"
  - "framework-specific indicators"

auto_flags:
  - "--primary_server"
  - "--supporting_server"

mcp_servers:
  primary: "most_relevant_server"
  secondary: ["fallback", "servers"]

patterns:
  file_structure:
    - "expected/directories/"
    - "important files"
  common_tasks:
    - "typical operations"
    - "common workflows"

intelligence:
  mode_triggers:
    - "mode_name: trigger_conditions"
  validation_focus:
    - "syntax_validation"
    - "best_practices"
    - "quality_checks"

performance_targets:
  bootstrap_ms: target_milliseconds
  context_size: "target_size"
  cache_duration: "cache_time"
```

## Best Practices

### Detection Pattern Guidelines

1. **Use Specific Identifiers**: Look for unique files or dependency patterns
2. **Multiple Signals**: Combine file extensions, directories, and config files
3. **Avoid Generic Patterns**: Don't rely on common files like `README.md`
4. **Test Edge Cases**: Handle missing files or permission errors gracefully

### MCP Server Selection

1. **Primary Server**: Choose the most relevant MCP server for the project type
2. **Secondary Servers**: Add complementary servers as fallbacks
3. **Auto-Flags**: Set flags that provide immediate value for the project type
4. **Performance Targets**: Set realistic bootstrap and context size goals

## Integration Notes

Minimal patterns integrate with Framework-Hooks through:

- **session_start hook**: Loads and applies patterns during initialization
- **Project detection**: Scans files and directories to identify project type
- **MCP activation**: Automatically starts relevant MCP servers
- **Flag processing**: Sets auto-flags for immediate feature activation

The pattern system provides a declarative way to configure Framework-Hooks behavior for different project types without requiring code changes.