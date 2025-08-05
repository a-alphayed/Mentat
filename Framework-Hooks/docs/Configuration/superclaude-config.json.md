# SuperClaude Master Configuration (`superclaude-config.json`)

## Overview

The `superclaude-config.json` file serves as the master configuration file for the SuperClaude-Lite framework. This comprehensive JSON configuration controls all aspects of hook execution, MCP server integration, mode coordination, and quality gates within the framework.

## Purpose and Role

The master configuration file acts as the central control system for:
- **Hook Configuration Management**: Defines behavior and settings for all 7 framework hooks
- **MCP Server Integration**: Coordinates intelligent routing and fallback strategies across servers
- **Mode Orchestration**: Manages behavioral mode activation and coordination patterns
- **Quality Gate Enforcement**: Implements the 8-step validation cycle throughout operations
- **Performance Monitoring**: Establishes targets and thresholds for optimization
- **Learning System Integration**: Enables cross-hook learning and adaptation

## File Structure and Organization

### 1. Framework Metadata
```json
{
  "superclaude": {
    "description": "SuperClaude-Lite Framework Configuration",
    "version": "1.0.0",
    "framework": "superclaude-lite",
    "enabled": true
  }
}
```

**Purpose**: Identifies framework version and overall enablement status.

### 2. Hook Configurations (`hook_configurations`)

The master configuration defines settings for all 7 SuperClaude hooks:

#### Session Start Hook
- **Performance Target**: 50ms initialization
- **Features**: Smart project context loading, automatic mode detection, MCP intelligence routing
- **Configuration**: Auto-detection, framework exclusion, intelligence activation
- **Error Handling**: Graceful fallback with context preservation

#### Pre-Tool Use Hook  
- **Performance Target**: 200ms routing decision
- **Features**: Intelligent tool routing, MCP server selection, real-time adaptation
- **Integration**: All 6 MCP servers with quality gates and learning engine
- **Configuration**: Pattern detection, learning adaptations, fallback strategies

#### Post-Tool Use Hook
- **Performance Target**: 100ms validation
- **Features**: Quality validation, rules compliance, effectiveness measurement
- **Validation Levels**: Basic → Standard → Comprehensive → Production
- **Configuration**: Rules validation, principles alignment, learning integration

#### Pre-Compact Hook
- **Performance Target**: 150ms compression decision
- **Features**: Intelligent compression strategy selection, selective content preservation
- **Compression Levels**: Minimal (0-40%) → Emergency (95%+)
- **Configuration**: Framework protection, quality preservation target (95%)

#### Notification Hook
- **Performance Target**: 100ms processing
- **Features**: Just-in-time documentation loading, dynamic pattern updates
- **Caching**: Documentation (30min), patterns (60min), intelligence (15min)
- **Configuration**: Real-time learning, performance optimization through caching

#### Stop Hook
- **Performance Target**: 200ms analytics generation
- **Features**: Comprehensive session analytics, learning consolidation
- **Analytics**: Performance metrics, effectiveness measurement, optimization recommendations
- **Configuration**: Session persistence, performance tracking, recommendation generation

#### Subagent Stop Hook
- **Performance Target**: 150ms coordination analytics
- **Features**: Subagent performance analytics, delegation effectiveness measurement
- **Task Management**: Wave orchestration, parallel coordination, performance optimization
- **Configuration**: Delegation analytics, coordination measurement, learning integration

### 3. Global Configuration (`global_configuration`)

#### Framework Integration
- **SuperClaude Compliance**: Ensures adherence to framework standards
- **YAML-Driven Logic**: Hot-reload configuration capability
- **Cross-Hook Coordination**: Enables hooks to share context and learnings

#### Performance Monitoring
- **Real-Time Tracking**: Continuous performance measurement
- **Target Enforcement**: Automatic optimization when targets are missed
- **Analytics**: Performance trend analysis and optimization suggestions

#### Learning System
- **Cross-Hook Learning**: Shared knowledge across hook executions
- **Adaptation Application**: Real-time improvement based on effectiveness
- **Pattern Recognition**: Identifies successful operational patterns

#### Security
- **Input Validation**: Protects against malicious input
- **Path Traversal Protection**: Prevents unauthorized file access
- **Resource Limits**: Prevents resource exhaustion attacks

### 4. MCP Server Integration (`mcp_server_integration`)

Defines integration patterns for all 6 MCP servers:

#### Server Definitions
- **Context7**: Library documentation and framework patterns (standard profile)
- **Sequential**: Multi-step reasoning and complex analysis (intensive profile)
- **Magic**: UI component generation and design systems (standard profile)
- **Playwright**: Browser automation and testing (intensive profile)
- **Morphllm**: Intelligent editing with fast apply (lightweight profile)
- **Serena**: Semantic analysis and memory management (standard profile)

#### Coordination Settings
- **Intelligent Routing**: Automatic server selection based on task requirements
- **Fallback Strategies**: Graceful degradation when servers are unavailable
- **Performance Optimization**: Load balancing and resource management
- **Learning Adaptation**: Real-time improvement of routing decisions

### 5. Mode Integration (`mode_integration`)

#### Supported Modes
- **Brainstorming**: Interactive requirements discovery (sequential, context7)
- **Task Management**: Multi-layer task orchestration (serena, morphllm)
- **Token Efficiency**: Intelligent token optimization (morphllm)
- **Introspection**: Meta-cognitive analysis (sequential)

#### Mode-Hook Coordination
Each mode specifies which hooks it integrates with and which MCP servers it prefers.

### 6. Quality Gates (`quality_gates`)

Implements the 8-step validation cycle:
1. **Syntax Validation**: Language-specific syntax checking
2. **Type Analysis**: Type compatibility and inference
3. **Code Quality**: Linting rules and quality standards
4. **Security Assessment**: Vulnerability scanning and OWASP compliance
5. **Testing Validation**: Test coverage and quality assurance
6. **Performance Analysis**: Performance benchmarking and optimization
7. **Documentation Verification**: Documentation completeness and accuracy
8. **Integration Testing**: End-to-end validation and deployment readiness

#### Hook Integration
- **Pre-Tool Use**: Steps 1-2 (validation preparation)
- **Post-Tool Use**: Steps 3-5 (comprehensive validation)
- **Stop**: Steps 6-8 (final validation and analytics)

### 7. Cache Configuration (`cache_configuration`)

#### Cache Settings
- **Cache Directory**: `./cache` for all cached data
- **Retention Policies**: Learning data (90 days), session data (30 days), performance data (365 days)
- **Automatic Cleanup**: Prevents cache bloat through scheduled cleanup

### 8. Logging Configuration (`logging_configuration`)

#### Logging Levels
- **Log Level**: INFO (configurable: ERROR, WARNING, INFO, DEBUG)
- **Specialized Logging**: Performance, error, learning, and hook execution logging
- **Privacy**: Sanitizes user content while preserving correlation data

### 9. Development Support (`development_support`)

#### Development Features
- **Debugging**: Optional debugging mode (disabled by default)
- **Performance Profiling**: Optional profiling capabilities
- **Verbose Logging**: Enhanced logging for development
- **Test Mode**: Specialized testing configuration

## Key Configuration Sections

### Performance Targets
Each hook has specific performance targets:
- **Session Start**: 50ms (critical priority)
- **Pre-Tool Use**: 200ms (high priority)
- **Post-Tool Use**: 100ms (medium priority)
- **Pre-Compact**: 150ms (high priority)
- **Notification**: 100ms (medium priority)
- **Stop**: 200ms (low priority)
- **Subagent Stop**: 150ms (medium priority)

### Default Values and Meanings

#### Hook Enablement
All hooks are enabled by default (`"enabled": true`) to provide full framework functionality.

#### Performance Monitoring
Real-time tracking is enabled with target enforcement and optimization suggestions.

#### Learning System
Cross-hook learning is enabled to continuously improve framework effectiveness.

#### Security Settings
All security features are enabled by default for production-ready security.

## Integration with Hooks

### Configuration Loading
Hooks load configuration through the shared YAML loader system, enabling:
- **Hot Reload**: Configuration changes without restart
- **Environment-Specific**: Different configs for development/production
- **Validation**: Configuration validation before application

### Cross-Hook Communication
The configuration enables hooks to:
- **Share Context**: Pass relevant information between hooks
- **Coordinate Actions**: Avoid conflicts through intelligent coordination
- **Learn Together**: Share effectiveness insights across hook executions

## Performance Implications

### Memory Usage
- **Configuration Size**: ~50KB typical configuration
- **Cache Impact**: Up to 100MB cache with automatic cleanup
- **Learning Data**: Persistent learning data with compression

### Processing Overhead
- **Configuration Loading**: <10ms initial load
- **Validation**: <5ms per configuration access
- **Hot Reload**: <50ms configuration refresh

### Network Impact
- **MCP Coordination**: Intelligent caching reduces network calls
- **Documentation Loading**: Just-in-time loading minimizes bandwidth usage

## Configuration Best Practices

### 1. Performance Tuning
```json
{
  "hook_configurations": {
    "session_start": {
      "performance_target_ms": 50,
      "configuration": {
        "auto_project_detection": true,
        "performance_monitoring": true
      }
    }
  }
}
```

**Recommendation**: Keep performance targets aggressive but achievable for your environment.

### 2. Security Hardening
```json
{
  "global_configuration": {
    "security": {
      "input_validation": true,
      "path_traversal_protection": true,
      "timeout_protection": true,
      "resource_limits": true
    }
  }
}
```

**Recommendation**: Never disable security features in production environments.

### 3. Learning Optimization
```json
{
  "global_configuration": {
    "learning_system": {
      "enabled": true,
      "cross_hook_learning": true,
      "effectiveness_tracking": true,
      "pattern_recognition": true
    }
  }
}
```

**Recommendation**: Enable learning system for continuous improvement, but monitor resource usage.

### 4. Mode Configuration
```json
{
  "mode_integration": {
    "enabled": true,
    "modes": {
      "token_efficiency": {
        "hooks": ["pre_compact", "session_start"],
        "mcp_servers": ["morphllm"]
      }
    }
  }
}
```

**Recommendation**: Configure modes based on your primary use cases and available MCP servers.

### 5. Cache Management
```json
{
  "cache_configuration": {
    "learning_data_retention_days": 90,
    "session_data_retention_days": 30,
    "automatic_cleanup": true
  }
}
```

**Recommendation**: Balance retention periods with storage requirements and privacy needs.

## Troubleshooting

### Common Configuration Issues

#### Performance Degradation
- **Symptoms**: Hooks exceeding performance targets
- **Solutions**: Adjust performance targets, enable caching, reduce feature complexity
- **Monitoring**: Check `performance_monitoring` settings

#### MCP Server Failures
- **Symptoms**: Routing failures, fallback activation
- **Solutions**: Verify MCP server availability, check fallback strategies
- **Configuration**: Review `mcp_server_integration` settings

#### Learning System Issues
- **Symptoms**: No adaptation observed, effectiveness not improving
- **Solutions**: Check learning data retention, verify effectiveness tracking
- **Debug**: Enable verbose learning logging

#### Memory Usage Issues
- **Symptoms**: High memory consumption, cache bloat
- **Solutions**: Reduce cache retention periods, enable automatic cleanup
- **Monitoring**: Review cache configuration and usage patterns

### Configuration Validation

The framework validates configuration on startup:
- **Schema Validation**: Ensures proper JSON structure
- **Value Validation**: Checks ranges and dependencies
- **Integration Validation**: Verifies hook and MCP server consistency
- **Security Validation**: Ensures security settings are appropriate

## Related Documentation

- **Hook Implementation**: See individual hook documentation in `/docs/Hooks/`
- **MCP Integration**: Reference MCP server documentation for specific server configurations
- **Mode Documentation**: Review mode-specific documentation for behavioral patterns
- **Performance Monitoring**: See performance configuration documentation for optimization strategies

## Version History

- **v1.0.0**: Initial SuperClaude-Lite configuration with all 7 hooks and 6 MCP servers
- Full hook lifecycle support with learning and performance monitoring
- Comprehensive quality gates implementation
- Mode integration with behavioral pattern support