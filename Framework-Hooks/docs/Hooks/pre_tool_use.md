# Pre-Tool-Use Hook Technical Documentation

## Purpose

The `pre_tool_use` hook analyzes tool requests and provides intelligent routing decisions before tool execution in Claude Code. It determines optimal MCP server coordination, performance optimizations, and execution strategies based on tool characteristics and context.

**Core Implementation**: A 648-line Python implementation that processes tool requests, analyzes operation characteristics, routes to appropriate MCP servers, and provides enhanced tool configurations with a target execution time of <200ms.

---

## Execution Context

The pre_tool_use hook runs before every tool execution in Claude Code. According to `settings.json`, it has a 15-second timeout and executes via: `python3 ~/.claude/hooks/pre_tool_use.py`

**Actual Execution Flow:**
1. Receives tool request from Claude Code via stdin (JSON)
2. Initializes PreToolUseHook class with shared module components
3. Processes tool request through `process_tool_use()` method
4. Analyzes operation characteristics and routing patterns
5. Outputs enhanced tool configuration via stdout (JSON)
6. Falls back gracefully on errors with basic tool configuration

**Input Processing:**
- Extracts tool context including tool name, parameters, user intent
- Analyzes operation characteristics (file count, complexity, parallelizability)  
- Identifies tool chain patterns (read-edit, multi-file, analysis chains)

**Output Configuration:**
- Enhanced mode flag and MCP server coordination
- Performance optimization settings (parallel execution, caching)
- Quality enhancement settings (validation, error recovery)
- Execution metadata (estimated time, complexity score, intelligence level)

---

## Performance Target

### Primary Target: <200ms Execution Time
- **Requirement**: Complete routing analysis and configuration within 200ms
- **Measurement**: End-to-end hook execution time from input to enhanced configuration
- **Validation**: Real-time performance tracking with target compliance reporting
- **Optimization**: Cached pattern recognition, pre-computed routing tables, intelligent fallbacks

### Performance Architecture
```yaml
Performance Zones:
  green_zone: 0-150ms     # Optimal performance with full intelligence
  yellow_zone: 150-200ms  # Target compliance with efficiency mode
  red_zone: 200ms+        # Performance fallback with reduced intelligence
```

### Efficiency Calculation
```python
efficiency_score = (
    time_efficiency * 0.4 +      # Execution speed relative to target
    complexity_efficiency * 0.3 + # Handling complexity appropriately  
    resource_efficiency * 0.3     # Resource utilization optimization
)
```

---

## Core Features

### 1. Intelligent Tool Routing
**Pattern-Based Tool Analysis**:
- Analyzes tool name, parameters, and context to determine optimal execution strategy
- Detects operation complexity (0.0-1.0 scale) based on file count, operation type, and requirements
- Identifies parallelization opportunities for multi-file operations
- Determines intelligence requirements for analysis and generation tasks

**Operation Categorization**:
```python
Operation Types:
- READ: File reading, search, navigation
- WRITE: File creation, editing, updates  
- BUILD: Implementation, generation, creation
- TEST: Validation, testing, verification
- ANALYZE: Analysis, debugging, investigation
```

**Complexity Scoring Algorithm**:
```python
base_complexity = {
    'READ': 0.0,
    'WRITE': 0.2, 
    'BUILD': 0.4,
    'TEST': 0.1,
    'ANALYZE': 0.3
}

file_multiplier = (file_count - 1) * 0.1
directory_multiplier = (directory_count - 1) * 0.05
intelligence_bonus = 0.2 if requires_intelligence else 0.0

complexity_score = base_complexity + file_multiplier + directory_multiplier + intelligence_bonus
```

### 2. Context-Aware Configuration
**Session Context Integration**:
- Tracks tool usage patterns across session for optimization opportunities
- Analyzes tool chain patterns (Read→Edit, Multi-file operations, Analysis chains)
- Applies session-specific optimizations based on detected patterns
- Maintains resource state awareness for performance tuning

**Operation Chain Analysis**:
```python
Pattern Detection:
- read_edit_pattern: Read followed by Edit operations
- multi_file_pattern: Multiple file operations in sequence
- analysis_chain: Sequential analysis operations with caching opportunities
```

### 3. Real-Time Adaptation
**Learning Engine Integration**:
- Records tool usage effectiveness for routing optimization
- Adapts routing decisions based on historical performance
- Applies user-specific and project-specific routing preferences
- Continuous improvement through effectiveness measurement

**Adaptation Scopes**:
- **User Level**: Personal routing preferences and patterns
- **Project Level**: Project-specific tool effectiveness patterns
- **Session Level**: Real-time adaptation within current session

---

## MCP Server Routing Logic

### Server Capability Matching
The hook implements sophisticated capability matching to select optimal MCP servers:

```python
Server Capabilities Map:
context7:    [documentation_access, framework_patterns, best_practices]
sequential:  [complex_reasoning, systematic_analysis, hypothesis_testing]
magic:       [ui_generation, design_systems, component_patterns]
playwright:  [browser_automation, testing_frameworks, performance_testing]
morphllm:    [pattern_application, fast_apply, intelligent_editing]
serena:      [semantic_understanding, project_context, memory_management]
```

### Routing Decision Matrix

#### Single Server Selection
```yaml
Context7 Triggers:
  - Library/framework keywords in user intent
  - Documentation-related operations
  - API reference needs
  - Best practices queries

Sequential Triggers:
  - Complexity score > 0.6
  - Multi-step analysis required
  - Debugging complex issues
  - System architecture analysis

Magic Triggers:
  - UI/component keywords
  - Frontend development operations
  - Design system integration
  - Component generation requests

Playwright Triggers:
  - Testing operations
  - Browser automation needs
  - Performance testing requirements
  - E2E validation requests

Morphllm Triggers:
  - Pattern-based editing
  - Fast apply suitable operations
  - Token optimization critical
  - Simple to moderate complexity

Serena Triggers:
  - File count > 5
  - Symbol-level operations
  - Project-wide analysis
  - Memory operations
```

#### Multi-Server Coordination
```python
Coordination Strategies:
- single_server: One MCP server handles the operation
- collaborative: Multiple servers work together
- sequential_handoff: Primary server → Secondary server
- parallel_coordination: Servers work on different aspects simultaneously
```

### Server Selection Algorithm
```python
def select_mcp_servers(context, requirements):
    servers = []
    
    # Primary capability matching
    for server, capabilities in server_capabilities.items():
        if any(cap in requirements['capabilities_needed'] for cap in capabilities):
            servers.append(server)
    
    # Context-specific routing
    if context['complexity_score'] > 0.6:
        servers.append('sequential')
    
    if context['file_count'] > 5:
        servers.append('serena')
    
    # User intent analysis
    intent_lower = context.get('user_intent', '').lower()
    if any(word in intent_lower for word in ['component', 'ui', 'frontend']):
        servers.append('magic')
    
    # Deduplication and prioritization
    return list(dict.fromkeys(servers))  # Preserve order, remove duplicates
```

---

## Fallback Strategies

### Hierarchy of Fallback Options

#### Level 1: Preferred MCP Server Unavailable
```python
Strategy: Alternative Server Selection
- Sequential unavailable → Use Morphllm for analysis
- Serena unavailable → Use native tools with manual coordination
- Magic unavailable → Generate basic components with Context7 patterns
```

#### Level 2: Multiple MCP Servers Unavailable
```python
Strategy: Capability Degradation
- Disable enhanced intelligence features
- Fall back to native Claude Code tools
- Maintain basic functionality with warnings
- Preserve user context and intent
```

#### Level 3: All MCP Servers Unavailable
```python
Strategy: Native Tool Execution
- Execute original tool request without enhancement
- Log degradation for performance analysis
- Provide clear feedback about reduced capabilities
- Maintain operational continuity
```

### Fallback Configuration Generation
```python
def create_fallback_tool_config(tool_request, error):
    return {
        'tool_name': tool_request.get('tool_name'),
        'enhanced_mode': False,
        'fallback_mode': True,
        'error': error,
        'mcp_integration': {
            'enabled': False,
            'servers': [],
            'coordination_strategy': 'none'
        },
        'performance_optimization': {
            'parallel_execution': False,
            'caching_enabled': False,
            'optimizations': []
        },
        'performance_metrics': {
            'routing_time_ms': 0,
            'target_met': False,
            'error_occurred': True
        }
    }
```

### Error Recovery Mechanisms
- **Graceful Degradation**: Reduce capability rather than failing completely
- **Context Preservation**: Maintain user intent and session context during fallback
- **Performance Continuity**: Ensure operations continue with acceptable performance
- **Learning Integration**: Record fallback events for routing improvement

---

## Configuration

### Hook-Specific Configuration (superclaude-config.json)
```json
{
  "pre_tool_use": {
    "enabled": true,
    "description": "ORCHESTRATOR + MCP routing intelligence for optimal tool selection",
    "performance_target_ms": 200,
    "features": [
      "intelligent_tool_routing",
      "mcp_server_selection", 
      "performance_optimization",
      "context_aware_configuration",
      "fallback_strategy_implementation",
      "real_time_adaptation"
    ],
    "configuration": {
      "mcp_intelligence": true,
      "pattern_detection": true,
      "learning_adaptations": true,
      "performance_optimization": true,
      "fallback_strategies": true
    },
    "integration": {
      "mcp_servers": ["context7", "sequential", "magic", "playwright", "morphllm", "serena"],
      "quality_gates": true,
      "learning_engine": true
    }
  }
}
```

### MCP Server Integration Configuration
```json
{
  "mcp_server_integration": {
    "enabled": true,
    "servers": {
      "context7": {
        "description": "Library documentation and framework patterns",
        "capabilities": ["documentation_access", "framework_patterns", "best_practices"],
        "performance_profile": "standard"
      },
      "sequential": {
        "description": "Multi-step reasoning and complex analysis", 
        "capabilities": ["complex_reasoning", "systematic_analysis", "hypothesis_testing"],
        "performance_profile": "intensive"
      },
      "serena": {
        "description": "Semantic analysis and memory management",
        "capabilities": ["semantic_understanding", "project_context", "memory_management"],
        "performance_profile": "standard"
      }
    },
    "coordination": {
      "intelligent_routing": true,
      "fallback_strategies": true,
      "performance_optimization": true,
      "learning_adaptation": true
    }
  }
}
```

### Runtime Configuration Loading
```python
class PreToolUseHook:
    def __init__(self):
        # Load hook-specific configuration
        self.hook_config = config_loader.get_hook_config('pre_tool_use')
        
        # Load orchestrator configuration (YAML or fallback)
        try:
            self.orchestrator_config = config_loader.load_config('orchestrator')
        except FileNotFoundError:
            self.orchestrator_config = self.hook_config.get('configuration', {})
        
        # Performance targets from configuration
        self.performance_target_ms = config_loader.get_hook_config(
            'pre_tool_use', 'performance_target_ms', 200
        )
```

---

## Learning Integration

### Learning Data Collection
**Operation Pattern Recording**:
```python
def record_tool_learning(context, tool_config):
    self.learning_engine.record_learning_event(
        LearningType.OPERATION_PATTERN,
        AdaptationScope.USER,
        context,
        {
            'tool_name': context['tool_name'],
            'mcp_servers_used': tool_config.get('mcp_integration', {}).get('servers', []),
            'execution_strategy': tool_config.get('execution_metadata', {}).get('intelligence_level'),
            'optimizations_applied': tool_config.get('performance_optimization', {}).get('optimizations', [])
        },
        effectiveness_score=0.8,  # Updated after execution
        confidence_score=0.7,
        metadata={'hook': 'pre_tool_use', 'version': '1.0'}
    )
```

### Adaptive Routing Enhancement
**Learning-Based Routing Improvements**:
- **User Preferences**: Learn individual user's tool and server preferences
- **Project Patterns**: Adapt to project-specific optimal routing strategies
- **Performance Optimization**: Route based on historical performance data
- **Error Pattern Recognition**: Avoid routing strategies that historically failed

### Learning Scope Hierarchy
```python
Learning Scopes:
1. Session Level: Real-time adaptation within current session
2. User Level: Personal routing preferences across sessions
3. Project Level: Project-specific optimization patterns
4. Global Level: Framework-wide routing intelligence
```

### Effectiveness Measurement
```python
Effectiveness Metrics:
- execution_time: Actual vs estimated execution time
- success_rate: Successful operation completion rate
- quality_score: Output quality assessment
- user_satisfaction: Implicit feedback from continued usage
- resource_efficiency: Resource utilization optimization
```

---

## Performance Optimization

### Caching Strategies

#### Pattern Recognition Cache
```python
Cache Structure:
- Key: hash(user_intent + tool_name + context_hash)
- Value: routing_decision + confidence_score
- TTL: 60 minutes for pattern stability
- Size: 1000 entries with LRU eviction
```

#### MCP Server Response Cache
```python
Cache Strategy:
- Documentation lookups: 30 minutes TTL
- Analysis results: Session-scoped cache
- Pattern templates: 1 hour TTL
- Server availability: 5 minutes TTL
```

#### Performance Optimizations
```python
Optimization Techniques:
1. Pre-computed Routing Tables: Common patterns pre-calculated
2. Lazy Loading: Load components only when needed
3. Parallel Analysis: Run pattern detection and MCP planning concurrently
4. Result Reuse: Cache and reuse analysis results within session
5. Intelligent Fallbacks: Fast fallback paths for common failure modes
```

### Resource Management
```python
Resource Optimization:
- Memory: Bounded caches with intelligent eviction
- CPU: Parallel processing for independent operations
- I/O: Batch operations where possible
- Network: Connection pooling for MCP servers
```

### Execution Time Optimization
```python
Time Budget Allocation:
- Pattern Detection: 50ms (25%)
- MCP Server Selection: 30ms (15%)
- Configuration Generation: 40ms (20%)
- Learning Integration: 20ms (10%)
- Buffer/Safety Margin: 60ms (30%)
Total Target: 200ms
```

---

## Integration with ORCHESTRATOR.md

### Pattern Matching Implementation
The hook implements the ORCHESTRATOR.md pattern matching system:

```python
# Quick Pattern Matching from ORCHESTRATOR.md
pattern_mappings = {
    'ui_component': {
        'keywords': ['component', 'design', 'frontend', 'UI'],
        'mcp_server': 'magic',
        'persona': 'frontend'
    },
    'deep_analysis': {
        'keywords': ['architecture', 'complex', 'system-wide'],
        'mcp_server': 'sequential',
        'thinking_mode': 'think_hard'
    },
    'large_scope': {
        'keywords': ['many files', 'entire codebase'],
        'mcp_server': 'serena',
        'delegation': True
    },
    'symbol_operations': {
        'keywords': ['rename', 'refactor', 'extract', 'move'],
        'mcp_server': 'serena',
        'precision': 'lsp'
    },
    'pattern_edits': {
        'keywords': ['framework', 'style', 'cleanup'],
        'mcp_server': 'morphllm',
        'optimization': 'token'
    }
}
```

### Resource Zone Implementation
```python
def get_resource_zone(resource_usage):
    if resource_usage <= 0.75:
        return 'green_zone'    # Full capabilities
    elif resource_usage <= 0.85:
        return 'yellow_zone'   # Efficiency mode
    else:
        return 'red_zone'      # Essential operations only
```

### Tool Selection Guide Integration
The hook implements the ORCHESTRATOR.md tool selection guide:

```python
def apply_orchestrator_routing(context, user_intent):
    """Apply ORCHESTRATOR.md routing patterns"""
    
    # MCP Server selection based on ORCHESTRATOR.md
    if any(word in user_intent.lower() for word in ['library', 'docs', 'framework']):
        return ['context7']
    
    if any(word in user_intent.lower() for word in ['complex', 'analysis', 'debug']):
        return ['sequential']
    
    if any(word in user_intent.lower() for word in ['component', 'ui', 'design']):
        return ['magic']
    
    if context.get('file_count', 1) > 5:
        return ['serena']
    
    # Default to native tools for simple operations
    return []
```

### Quality Gate Integration
```python
Quality Gates Applied:
- Step 1 (Syntax Validation): Tool parameter validation
- Step 2 (Type Analysis): Context type checking and compatibility
- Performance Monitoring: Real-time execution time tracking
- Fallback Validation: Ensure fallback strategies maintain functionality
```

### Auto-Activation Rules Implementation
The hook implements ORCHESTRATOR.md auto-activation rules:

```python
def apply_auto_activation_rules(context):
    """Apply ORCHESTRATOR.md auto-activation patterns"""
    
    activations = []
    
    # Enable Sequential for complex operations
    if (context.get('complexity_score', 0) > 0.6 or 
        context.get('requires_intelligence')):
        activations.append('sequential')
    
    # Enable Serena for multi-file operations
    if (context.get('file_count', 1) > 5 or 
        any(op in context.get('operation_sequence', []) for op in ['rename', 'extract'])):
        activations.append('serena')
    
    # Enable delegation for large operations
    if (context.get('file_count', 1) > 3 or 
        context.get('directory_count', 1) > 2):
        activations.append('delegation')
    
    return activations
```

---

## Technical Implementation Details

### Core Architecture Components

#### 1. Framework Logic Integration
```python
from framework_logic import FrameworkLogic, OperationContext, OperationType, RiskLevel

# Provides SuperClaude framework intelligence
self.framework_logic = FrameworkLogic()
```

#### 2. Pattern Detection Engine  
```python
from pattern_detection import PatternDetector, PatternMatch

# Analyzes patterns for routing decisions
detection_result = self.pattern_detector.detect_patterns(
    user_intent, context, operation_data
)
```

#### 3. MCP Intelligence Coordination
```python
from mcp_intelligence import MCPIntelligence, MCPActivationPlan

# Creates optimal MCP server activation plans
mcp_plan = self.mcp_intelligence.create_activation_plan(
    user_intent, context, operation_data
)
```

#### 4. Learning Engine Integration
```python
from learning_engine import LearningEngine

# Applies learned adaptations and records new patterns
enhanced_routing = self.learning_engine.apply_adaptations(context, base_routing)
```

### Error Handling Architecture
```python
Exception Handling Strategy:
1. Catch all exceptions during routing analysis
2. Log error with context for debugging
3. Generate fallback configuration
4. Preserve user intent and operation continuity
5. Record error for learning and improvement
```

### Performance Monitoring
```python
Performance Tracking:
- Initialization time measurement
- Per-operation execution time tracking
- Target compliance validation (<200ms)
- Efficiency score calculation
- Resource utilization monitoring
```

---

## Usage Examples

### Example 1: Simple File Read
```json
Input Request:
{
  "tool_name": "Read",
  "parameters": {"file_path": "/src/components/Button.tsx"},
  "user_intent": "read button component"
}

Hook Enhancement:
{
  "tool_name": "Read",
  "enhanced_mode": false,
  "mcp_integration": {"enabled": false},
  "execution_metadata": {
    "complexity_score": 0.0,
    "intelligence_level": "low"
  }
}
```

### Example 2: Complex Multi-File Analysis
```json
Input Request:
{
  "tool_name": "Analyze", 
  "parameters": {"directory": "/src/**/*.ts"},
  "user_intent": "analyze typescript architecture patterns"
}

Hook Enhancement:
{
  "tool_name": "Analyze",
  "enhanced_mode": true,
  "mcp_integration": {
    "enabled": true,
    "servers": ["sequential", "serena"],
    "coordination_strategy": "collaborative"
  },
  "performance_optimization": {
    "parallel_execution": true,
    "optimizations": ["parallel_file_processing"]
  },
  "execution_metadata": {
    "complexity_score": 0.75,
    "intelligence_level": "high"
  }
}
```

### Example 3: UI Component Generation
```json
Input Request:
{
  "tool_name": "Generate",
  "parameters": {"component_type": "form"},
  "user_intent": "create login form component"
}

Hook Enhancement:
{
  "tool_name": "Generate",
  "enhanced_mode": true,
  "mcp_integration": {
    "enabled": true,
    "servers": ["magic", "context7"],
    "coordination_strategy": "sequential_handoff"
  },
  "build_operations": {
    "framework_integration": true,
    "component_generation": true,
    "quality_validation": true
  }
}
```

---

## Monitoring and Debugging

### Performance Metrics
```python
Tracked Metrics:
- routing_time_ms: Time spent in routing analysis
- target_met: Boolean indicating <200ms compliance
- efficiency_score: Overall routing effectiveness (0.0-1.0)
- mcp_servers_activated: Count of MCP servers coordinated
- optimizations_applied: List of performance optimizations
- fallback_triggered: Boolean indicating fallback usage
```

### Logging Integration
```python
Log Events:
- Hook start: Tool name and parameters
- Routing decisions: MCP server selection rationale
- Execution strategy: Chosen execution approach
- Performance metrics: Timing and efficiency data
- Error events: Failures and fallback triggers
- Hook completion: Success/failure status
```

### Debug Information
```python
Debug Output:
- Pattern detection results with confidence scores
- MCP server capability matching analysis
- Optimization opportunity identification
- Learning adaptation application
- Configuration generation process
- Performance target validation
```

---

## Related Documentation

- **ORCHESTRATOR.md**: Core routing patterns and coordination strategies
- **Framework Integration**: Quality gates and mode coordination
- **MCP Server Documentation**: Individual server capabilities and integration
- **Learning Engine**: Adaptive intelligence and pattern recognition
- **Performance Monitoring**: System-wide performance tracking and optimization

---

*The pre_tool_use hook serves as the intelligent routing engine for the SuperClaude framework, ensuring optimal tool selection, MCP server coordination, and performance optimization for every operation within Claude Code.*