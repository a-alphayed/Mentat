# Subagent Stop Hook Documentation

## Purpose

The `subagent_stop` hook analyzes subagent task completion and provides delegation effectiveness measurement after subagent operations. It implements MODE_Task_Management delegation coordination analytics for multi-agent collaboration optimization.

**Core Implementation**: Measures delegation effectiveness, analyzes cross-agent coordination patterns, and optimizes wave orchestration strategies with a target execution time of <150ms.

## Execution Context

The subagent_stop hook runs after subagent operations complete in Claude Code. According to `settings.json`, it has a 15-second timeout and executes via: `python3 ~/.claude/hooks/subagent_stop.py`

**Execution Triggers:**
- Individual subagent task completion
- Multi-agent coordination end
- Wave orchestration completion  
- Delegation strategy assessment

**Actual Processing:**
1. Receives subagent completion data via stdin (JSON)
2. Analyzes delegation effectiveness and coordination patterns
3. Measures multi-agent collaboration success
4. Records learning events for delegation optimization
5. Outputs coordination analytics via stdout (JSON)

## Performance Target

**Target Execution Time: <150ms**

The hook maintains strict performance requirements to ensure minimal overhead during delegation analytics:

```python
# Performance configuration
self.performance_target_ms = config_loader.get_hook_config('subagent_stop', 'performance_target_ms', 150)

# Performance tracking
execution_time = (time.time() - start_time) * 1000
coordination_report['performance_metrics'] = {
    'coordination_analysis_time_ms': execution_time,
    'target_met': execution_time < self.performance_target_ms,
    'coordination_efficiency': self._calculate_coordination_efficiency(context, execution_time)
}
```

**Performance Optimization Features:**
- **Fast Context Extraction**: Efficient subagent data parsing and context enrichment
- **Streamlined Analytics**: Optimized delegation effectiveness calculations
- **Batched Operations**: Grouped analysis operations for efficiency
- **Cached Learning**: Reuse of previous coordination patterns for faster analysis

## Delegation Analytics

The hook provides comprehensive **delegation effectiveness measurement** through multiple analytical dimensions:

### Task Completion Analysis

```python
def _analyze_task_completion(self, context: dict) -> dict:
    """Analyze task completion performance."""
    task_analysis = {
        'completion_success': context.get('task_success', False),
        'completion_quality': context.get('output_quality', 0.0),
        'completion_efficiency': context.get('resource_efficiency', 0.0),
        'completion_time_performance': 0.0,
        'success_factors': [],
        'improvement_areas': []
    }
```

**Key Metrics:**
- **Completion Success Rate**: Binary success/failure tracking for delegated tasks
- **Output Quality Assessment**: Quality scoring (0.0-1.0) based on validation results and error indicators
- **Resource Efficiency**: Memory, CPU, and time utilization effectiveness measurement
- **Time Performance**: Actual vs. expected execution time analysis
- **Success Factor Identification**: Patterns that lead to successful delegation outcomes
- **Improvement Area Detection**: Areas requiring optimization in future delegations

### Delegation Effectiveness Measurement

```python
def _analyze_delegation_effectiveness(self, context: dict, task_analysis: dict) -> dict:
    """Analyze effectiveness of task delegation."""
    delegation_analysis = {
        'delegation_strategy': context.get('delegation_strategy', 'unknown'),
        'delegation_success': context.get('task_success', False),
        'delegation_efficiency': 0.0,
        'coordination_overhead': 0.0,
        'parallel_benefit': 0.0,
        'delegation_value': 0.0
    }
```

**Delegation Strategies Analyzed:**
- **Files Strategy**: Individual file-based delegation effectiveness
- **Folders Strategy**: Directory-level delegation performance
- **Auto Strategy**: Intelligent delegation strategy effectiveness
- **Custom Strategies**: User-defined delegation pattern analysis

**Effectiveness Dimensions:**
- **Delegation Efficiency**: Ratio of productive work to coordination overhead
- **Coordination Overhead**: Time and resource cost of agent coordination
- **Parallel Benefit**: Actual speedup achieved through parallel execution
- **Overall Delegation Value**: Composite score weighing quality, efficiency, and parallel benefits

## Wave Orchestration

The hook provides advanced **multi-agent coordination analysis** for wave-based task orchestration:

### Wave Coordination Success

```python
def _analyze_coordination_patterns(self, context: dict, delegation_analysis: dict) -> dict:
    """Analyze coordination patterns and effectiveness."""
    coordination_analysis = {
        'coordination_strategy': 'unknown',
        'synchronization_effectiveness': 0.0,
        'data_flow_efficiency': 0.0,
        'wave_coordination_success': 0.0,
        'cross_agent_learning': 0.0,
        'coordination_patterns_detected': []
    }
```

**Wave Orchestration Features:**
- **Progressive Enhancement**: Iterative improvement through multiple coordination waves
- **Systematic Analysis**: Comprehensive methodical analysis across wave cycles
- **Adaptive Coordination**: Dynamic strategy adjustment based on wave performance
- **Enterprise Orchestration**: Large-scale coordination for complex multi-agent operations

### Wave Performance Metrics

```python
def _update_wave_orchestration_metrics(self, context: dict, coordination_analysis: dict) -> dict:
    """Update wave orchestration performance metrics."""
    wave_metrics = {
        'wave_performance': 0.0,
        'orchestration_efficiency': 0.0,
        'wave_learning_value': 0.0,
        'next_wave_recommendations': []
    }
```

**Wave Strategy Analysis:**
- **Wave Position Tracking**: Current position within multi-wave coordination
- **Inter-Wave Communication**: Data flow and synchronization between waves
- **Wave Success Metrics**: Performance measurement across wave cycles
- **Orchestration Efficiency**: Resource utilization effectiveness in wave coordination

## Cross-Agent Learning

The hook implements **sophisticated learning mechanisms** for continuous delegation improvement:

### Learning Event Recording

```python
def _record_coordination_learning(self, context: dict, delegation_analysis: dict, 
                               optimization_insights: dict):
    """Record coordination learning for future optimization."""
    # Record delegation effectiveness
    self.learning_engine.record_learning_event(
        LearningType.PERFORMANCE_OPTIMIZATION,
        AdaptationScope.PROJECT,
        context,
        {
            'delegation_strategy': context.get('delegation_strategy'),
            'task_type': context.get('task_type'),
            'delegation_value': delegation_analysis['delegation_value'],
            'coordination_overhead': delegation_analysis['coordination_overhead'],
            'parallel_benefit': delegation_analysis['parallel_benefit']
        },
        delegation_analysis['delegation_value'],
        0.8,
        {'hook': 'subagent_stop', 'coordination_learning': True}
    )
```

**Learning Categories:**
- **Performance Optimization**: Delegation strategy effectiveness patterns
- **Operation Patterns**: Successful task completion patterns
- **Coordination Patterns**: Effective multi-agent coordination strategies
- **Error Recovery**: Learning from delegation failures and recovery strategies

**Learning Scopes:**
- **Project-Level Learning**: Delegation patterns specific to current project
- **User-Level Learning**: Cross-project delegation preferences and patterns
- **System-Level Learning**: Framework-wide coordination optimization patterns

## Parallel Execution Tracking

The hook provides comprehensive **parallel operation performance analysis**:

### Parallel Benefit Calculation

```python
# Calculate parallel benefit
parallel_tasks = context.get('parallel_tasks', [])
if len(parallel_tasks) > 1:
    # Estimate parallel benefit based on task coordination
    parallel_efficiency = context.get('parallel_efficiency', 1.0)
    theoretical_speedup = len(parallel_tasks)
    actual_speedup = theoretical_speedup * parallel_efficiency
    delegation_analysis['parallel_benefit'] = actual_speedup / theoretical_speedup
```

**Parallel Performance Metrics:**
- **Theoretical vs. Actual Speedup**: Comparison of expected and achieved parallel performance
- **Parallel Efficiency**: Effectiveness of parallel task coordination
- **Synchronization Overhead**: Cost of coordinating parallel operations
- **Resource Contention Analysis**: Impact of resource sharing on parallel performance

### Coordination Pattern Detection

```python
# Detect coordination patterns
if delegation_analysis['delegation_value'] > 0.8:
    coordination_analysis['coordination_patterns_detected'].append('effective_delegation')

if coordination_analysis['synchronization_effectiveness'] > 0.8:
    coordination_analysis['coordination_patterns_detected'].append('efficient_synchronization')

if coordination_analysis['wave_coordination_success'] > 0.8:
    coordination_analysis['coordination_patterns_detected'].append('successful_wave_orchestration')
```

**Pattern Categories:**
- **Effective Delegation**: High-value delegation strategies
- **Efficient Synchronization**: Optimal coordination mechanisms
- **Successful Wave Orchestration**: High-performing wave coordination patterns
- **Resource Optimization**: Efficient resource utilization patterns

## Configuration

The hook is configured through `superclaude-config.json` with comprehensive settings for delegation analytics:

### Core Configuration

```json
{
  "hooks": {
    "subagent_stop": {
      "enabled": true,
      "priority": 7,
      "performance_target_ms": 150,
      "delegation_analytics": {
        "enabled": true,
        "strategy_analysis": ["files", "folders", "auto"],
        "effectiveness_threshold": 0.6,
        "coordination_overhead_threshold": 0.3
      },
      "wave_orchestration": {
        "enabled": true,
        "wave_strategies": ["progressive", "systematic", "adaptive", "enterprise"],
        "success_threshold": 0.7,
        "learning_enabled": true
      },
      "parallel_tracking": {
        "efficiency_threshold": 0.7,
        "synchronization_tracking": true,
        "resource_contention_analysis": true
      },
      "learning_configuration": {
        "coordination_learning": true,
        "pattern_detection": true,
        "cross_agent_learning": true,
        "performance_learning": true
      }
    }
  }
}
```

### Task Management Configuration

```json
{
  "session": {
    "task_management": {
      "delegation_strategies": ["files", "folders", "auto"],
      "wave_orchestration": {
        "enabled": true,
        "strategies": ["progressive", "systematic", "adaptive", "enterprise"],
        "complexity_threshold": 0.4,
        "min_wave_tasks": 3
      },
      "parallel_coordination": {
        "max_parallel_agents": 7,
        "synchronization_timeout_ms": 5000,
        "resource_sharing_enabled": true
      },
      "learning_integration": {
        "delegation_learning": true,
        "wave_learning": true,
        "cross_session_learning": true
      }
    }
  }
}
```

## MODE_Task_Management Integration

The hook implements **MODE_Task_Management** through comprehensive integration with the task management framework:

### Task Management Layer Integration

```python
# Load task management configuration
self.task_config = config_loader.get_section('session', 'task_management', {})

# Integration with task management layers
# Layer 1: TodoRead/TodoWrite (Session Tasks) - Real-time state management
# Layer 2: /task Command (Project Management) - Cross-session persistence
# Layer 3: /spawn Command (Meta-Orchestration) - Complex multi-domain operations
# Layer 4: /loop Command (Iterative Enhancement) - Progressive refinement workflows
```

**Framework Integration Points:**
- **Session Task Tracking**: Integration with TodoWrite for task completion analytics
- **Project Task Coordination**: Cross-session task management integration
- **Meta-Orchestration**: Complex multi-domain operation coordination
- **Iterative Enhancement**: Progressive refinement and quality improvement cycles

### Auto-Activation Patterns

The hook supports MODE_Task_Management auto-activation patterns:

```python
# Auto-activation triggers from MODE_Task_Management:
# - Sub-Agent Delegation: >2 directories OR >3 files OR complexity >0.4
# - Wave Mode: complexity ≥0.4 AND files >3 AND operation_types >2
# - Loop Mode: polish, refine, enhance, improve keywords detected
```

**Detection Patterns:**
- **Multi-Step Operations**: 3+ step sequences with dependency analysis
- **Complexity Thresholds**: Operations exceeding 0.4 complexity score
- **File Count Triggers**: 3+ files for delegation, 2+ directories for coordination
- **Performance Opportunities**: Auto-detect parallelizable operations with time estimates

## Coordination Effectiveness

The hook provides comprehensive **success metrics for delegation** through multiple measurement dimensions:

### Overall Effectiveness Calculation

```python
'performance_summary': {
    'overall_effectiveness': (
        task_analysis['completion_quality'] * 0.4 +
        delegation_analysis['delegation_value'] * 0.3 +
        coordination_analysis['synchronization_effectiveness'] * 0.3
    ),
    'delegation_success': delegation_analysis['delegation_value'] > 0.6,
    'coordination_success': coordination_analysis['synchronization_effectiveness'] > 0.7,
    'learning_value': wave_metrics.get('wave_learning_value', 0.5)
}
```

**Effectiveness Dimensions:**
- **Task Quality (40%)**: Output quality and completion success
- **Delegation Value (30%)**: Effectiveness of delegation strategy and execution
- **Coordination Success (30%)**: Synchronization and coordination effectiveness

### Success Thresholds

```python
# Success criteria
delegation_success = delegation_analysis['delegation_value'] > 0.6
coordination_success = coordination_analysis['synchronization_effectiveness'] > 0.7
wave_success = wave_metrics['wave_performance'] > 0.8
```

**Performance Benchmarks:**
- **Delegation Success**: >60% delegation value threshold
- **Coordination Success**: >70% synchronization effectiveness threshold  
- **Wave Success**: >80% wave performance threshold
- **Overall Effectiveness**: Composite score incorporating all dimensions

### Optimization Recommendations

```python
def _generate_optimization_insights(self, context: dict, task_analysis: dict, 
                                  delegation_analysis: dict, coordination_analysis: dict) -> dict:
    """Generate optimization insights for future delegations."""
    insights = {
        'delegation_optimizations': [],
        'coordination_improvements': [],
        'wave_strategy_recommendations': [],
        'performance_enhancements': [],
        'learning_opportunities': []
    }
```

**Recommendation Categories:**
- **Delegation Optimizations**: Alternative strategies, overhead reduction, task partitioning improvements
- **Coordination Improvements**: Synchronization mechanism optimization, data exchange pattern improvements
- **Wave Strategy Recommendations**: Orchestration strategy adjustments, task distribution optimization
- **Performance Enhancements**: Execution speed optimization, resource utilization improvements
- **Learning Opportunities**: Pattern recognition, cross-agent learning, continuous improvement areas

## Error Handling and Resilience

The hook implements robust error handling with graceful degradation:

```python
def _create_fallback_report(self, subagent_data: dict, error: str) -> dict:
    """Create fallback coordination report on error."""
    return {
        'subagent_id': subagent_data.get('subagent_id', 'unknown'),
        'task_id': subagent_data.get('task_id', 'unknown'),
        'completion_timestamp': time.time(),
        'error': error,
        'fallback_mode': True,
        
        'task_completion': {
            'success': False,
            'quality_score': 0.0,
            'efficiency_score': 0.0,
            'error_occurred': True
        }
    }
```

**Error Recovery Strategies:**
- **Graceful Degradation**: Fallback coordination reports when analysis fails
- **Context Preservation**: Maintain essential coordination data even during errors
- **Error Logging**: Comprehensive error tracking for debugging and improvement
- **Performance Monitoring**: Continue performance tracking even in error conditions

## Integration with SuperClaude Framework

The hook integrates seamlessly with the broader SuperClaude framework:

### Framework Components

- **Learning Engine Integration**: Records coordination patterns for continuous improvement
- **Pattern Detection**: Identifies successful delegation and coordination patterns
- **MCP Intelligence**: Coordinates with MCP servers for enhanced analysis
- **Compression Engine**: Optimizes data storage and transfer for coordination analytics
- **Framework Logic**: Implements SuperClaude operational principles and patterns

### Quality Gates Integration

The hook contributes to SuperClaude's 8-step quality validation cycle:
- **Step 2.5**: Task management validation during orchestration operations
- **Step 7.5**: Session completion verification and summary documentation
- **Continuous**: Real-time metrics collection and performance monitoring
- **Post-Session**: Comprehensive session analytics and completion reporting

### Future Enhancements

Planned improvements for enhanced delegation coordination:
- **Predictive Delegation**: ML-based delegation strategy recommendation
- **Cross-Project Learning**: Delegation pattern sharing across projects
- **Real-Time Optimization**: Dynamic delegation adjustment during execution
- **Advanced Wave Strategies**: More sophisticated wave orchestration patterns
- **Resource Prediction**: Predictive resource allocation for delegated tasks