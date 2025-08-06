# Framework-Hooks Performance Documentation

## Performance Targets

The Framework-Hooks system defines performance targets in performance.yaml for each hook:

**Core Performance Requirements:**

- Hook execution should complete within configured timeouts to avoid blocking Claude Code
- Performance targets provide goals for optimization but do not guarantee actual execution times
- Resource usage should remain reasonable during normal operation
- Performance monitoring tracks actual execution against configured targets

**Performance Target Rationale:**
```
Fast Hook Performance → Reduced Session Latency → Better User Experience
```

**Configured Thresholds:**
- **Target times**: Optimal performance goals from performance.yaml
- **Warning thresholds**: ~1.5x target (monitoring threshold)
- **Critical thresholds**: ~2x target (performance alert threshold)  
- **Timeout limits**: Configured in settings.json (10-15 seconds per hook)

## Hook Performance Targets

### Performance Targets from performance.yaml

The system defines performance targets for each lifecycle hook:

#### session_start: 50ms target
**Current Implementation**: 703 lines of Python code
**Timeout**: 10 seconds (from settings.json)
**Thresholds**: 50ms target, 75ms warning, 100ms critical
**Primary Tasks**:
- Project type detection (file analysis)
- Pattern loading from minimal/ directory
- Mode activation based on user input
- MCP server routing decisions

#### pre_tool_use: 200ms target  
**Timeout**: 15 seconds
**Thresholds**: 200ms target, 300ms warning, 500ms critical
**Primary Tasks**:
- Operation pattern analysis
- MCP server selection logic
- Performance optimization planning

#### post_tool_use: 100ms target
**Timeout**: 10 seconds  
**Thresholds**: 100ms target, 150ms warning, 250ms critical
**Primary Tasks**:
- Operation result validation
- Learning data recording  
- Effectiveness tracking

#### pre_compact: 150ms target
**Timeout**: 15 seconds
**Thresholds**: 150ms target, 200ms warning, 300ms critical  
**Primary Tasks**:
- Content type classification
- Compression strategy selection
- Token optimization application

#### notification: 100ms target
**Timeout**: 10 seconds
**Thresholds**: 100ms target, 150ms warning, 200ms critical
**Primary Tasks**:
- Pattern cache updates
- Configuration refreshes
- Notification processing

#### stop: 200ms target
**Timeout**: 15 seconds
**Thresholds**: 200ms target, 300ms warning, 500ms critical
**Primary Tasks**:
- Session analytics generation
- Learning data persistence
- Performance metrics collection

#### subagent_stop: 150ms target  
**Timeout**: 15 seconds
**Thresholds**: 150ms target, 200ms warning, 300ms critical
**Primary Tasks**:
- Delegation performance tracking
- Coordination effectiveness measurement
- Task management analytics

## Implementation Architecture  

### Core Implementation Components

The Framework-Hooks system consists of:

**Python Modules:**
- 7 main hook files (session_start.py: 703 lines, others vary)
- 9 shared modules totaling ~250KB of Python code
- pattern_detection.py (45KB) handles project type and pattern recognition
- learning_engine.py (40KB) manages user preferences and effectiveness tracking

**Configuration System:**
- 19 YAML configuration files
- performance.yaml (345 lines) defines all timing targets and thresholds  
- Pattern files organized in minimal/, dynamic/, learned/ directories
- settings.json configures hook execution and timeouts

**Pattern Loading Strategy:**
```yaml
Minimal Patterns (loaded at startup):
  - python_project.yaml: Python-specific configuration
  - react_project.yaml: React project patterns
  - Basic mode detection triggers
  
Dynamic Patterns (loaded as needed):
  - mcp_activation.yaml: Server routing patterns
  - mode_detection.yaml: SuperClaude mode triggers
  
Learned Patterns (updated during use):
  - user_preferences.yaml: Personal configuration adaptations
  - project_optimizations.yaml: Project-specific learned patterns
```

### Compression Implementation

The pre_compact hook implements token compression through compression_engine.py (27KB):

**Compression Strategies:**
```python
Compression Levels (from compression.yaml):
  MINIMAL:     Framework content excluded, user content preserved
  EFFICIENT:   Selective compression with quality validation
  COMPRESSED:  Symbol systems and abbreviations applied
  CRITICAL:    Aggressive optimization when needed
  EMERGENCY:   Maximum compression for resource constraints
```

**Symbol Systems Implementation:**
- Mathematical operators: 'leads to' → '→' 
- Status indicators: 'completed' → '✅'
- Technical domains: 'performance' → '⚡'
- Applied selectively based on content type and compression level

**Content Classification:**
```python
Compression Strategy by Content Type:
  FRAMEWORK_CONTENT:   0% compression (complete preservation)
  SESSION_DATA:        Variable compression (based on compression level)
  USER_CONTENT:        Minimal compression (quality preservation priority)
  WORKING_ARTIFACTS:   Higher compression allowed (temporary data)
```

## Session Startup Implementation

### session_start Hook Operation

The session_start.py hook (703 lines) implements session initialization:

**Primary Operations:**
1. **Project Detection**: Analyzes file structure to determine project type (Python, React, etc.)
2. **Pattern Loading**: Loads appropriate minimal pattern files based on detected project type
3. **Mode Activation**: Parses user input to detect SuperClaude mode triggers
4. **MCP Routing**: Determines which MCP servers to activate based on patterns and project type

**Implementation Approach:**
```python
Session Startup Process:
  1. Initialize shared modules (framework_logic, pattern_detection, etc.)
  2. Load YAML configurations (performance.yaml, modes.yaml, etc.)  
  3. Analyze current directory for project type indicators
  4. Load appropriate minimal pattern files
  5. Process user input for mode detection
  6. Generate MCP server activation recommendations
  7. Record startup metrics for performance monitoring
```

**Performance Considerations:**
- Hook has 10-second timeout limit (configured in settings.json)
- Target execution time: 50ms (from performance.yaml)  
- Actual performance depends on system resources and project complexity
- Pattern loading optimized by only loading relevant minimal patterns initially

## Performance Monitoring Implementation

### Performance Tracking System

The Framework-Hooks system includes performance monitoring through:

**Performance Configuration:**
- **performance.yaml** (345 lines): Defines targets, warning, and critical thresholds for each hook
- **logger.py** (11KB): Provides logging utilities for performance tracking and debugging
- **Hook timing**: Each hook execution is measured and compared against configured targets

**Monitoring Components:**
```yaml
Performance Tracking:
  Target Times: Defined in performance.yaml for each hook
  Warning Thresholds: ~1.5x target time (monitoring alerts)
  Critical Thresholds: ~2x target time (performance degradation alerts)
  Timeout Limits: Configured in settings.json (10-15 seconds per hook)
```

**Learning Integration:**
- **learning_engine.py** (40KB): Tracks operation effectiveness and user preferences
- **Learned patterns**: Performance data influences future pattern selection
- **User preferences**: Successful configurations saved for future sessions
- **Analytics**: stop.py hook generates session performance summaries

## Implementation Summary

### Framework-Hooks Performance Characteristics

The Framework-Hooks system implements performance monitoring and optimization through:

**Performance Configuration:**
- Performance targets defined in performance.yaml for each of 7 lifecycle hooks
- Timeout limits configured in settings.json (10-15 seconds per hook)
- Warning and critical thresholds for performance degradation detection

**Implementation Approach:**
- Python hooks execute during Claude Code lifecycle events
- Shared modules provide common functionality (pattern detection, learning, compression)
- YAML configuration files customize behavior without code changes
- Pattern system enables project-specific optimizations

**Performance Considerations:**
- Hook performance depends on system resources, project complexity, and configuration
- Targets provide optimization goals but do not guarantee actual execution times
- Learning system adapts behavior based on measured effectiveness
- Compression system balances token efficiency with content quality preservation

The system aims to provide SuperClaude framework functionality through efficient lifecycle hooks while maintaining reasonable resource usage and execution times.
