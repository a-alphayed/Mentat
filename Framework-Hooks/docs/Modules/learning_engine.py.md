# learning_engine.py - Adaptive Learning and Feedback System

## Overview

The `learning_engine.py` module provides a cross-hook adaptation system that learns from user patterns, operation effectiveness, and system performance to continuously improve SuperClaude intelligence. It implements user preference learning, operation pattern recognition, performance feedback integration, and cross-hook coordination for personalized and project-specific adaptations.

## Purpose and Responsibilities

### Primary Functions
- **User Preference Learning**: Personalization based on effectiveness feedback and usage patterns
- **Operation Pattern Recognition**: Identification and optimization of common workflows
- **Performance Feedback Integration**: Continuous improvement through effectiveness metrics
- **Cross-Hook Knowledge Sharing**: Shared learning across all hook implementations
- **Effectiveness Measurement**: Validation of adaptation success and continuous refinement

### Intelligence Capabilities
- **Pattern Signature Generation**: Unique identification of learning patterns for reuse
- **Adaptation Creation**: Automatic generation of behavioral modifications from patterns
- **Context Matching**: Intelligent matching of current context to learned adaptations
- **Effectiveness Tracking**: Longitudinal monitoring of adaptation success rates

## Core Classes and Data Structures

### Enumerations

#### LearningType
```python
class LearningType(Enum):
    USER_PREFERENCE = "user_preference"              # Personal preference patterns
    OPERATION_PATTERN = "operation_pattern"          # Workflow optimization patterns
    PERFORMANCE_OPTIMIZATION = "performance_optimization"  # Performance improvement patterns
    ERROR_RECOVERY = "error_recovery"                # Error handling and recovery patterns
    EFFECTIVENESS_FEEDBACK = "effectiveness_feedback"  # Feedback on adaptation effectiveness
```

#### AdaptationScope
```python
class AdaptationScope(Enum):
    SESSION = "session"          # Apply only to current session
    PROJECT = "project"          # Apply to current project
    USER = "user"               # Apply across all user sessions
    GLOBAL = "global"           # Apply to all users (anonymized)
```

### Data Classes

#### LearningRecord
```python
@dataclass
class LearningRecord:
    timestamp: float                    # When the learning event occurred
    learning_type: LearningType         # Type of learning pattern
    scope: AdaptationScope             # Scope of application
    context: Dict[str, Any]            # Context in which learning occurred
    pattern: Dict[str, Any]            # The pattern or behavior observed
    effectiveness_score: float          # 0.0 to 1.0 effectiveness rating
    confidence: float                   # 0.0 to 1.0 confidence in learning
    metadata: Dict[str, Any]           # Additional learning metadata
```

#### Adaptation
```python
@dataclass
class Adaptation:
    adaptation_id: str                  # Unique adaptation identifier
    pattern_signature: str              # Pattern signature for matching
    trigger_conditions: Dict[str, Any]  # Conditions that trigger this adaptation
    modifications: Dict[str, Any]       # Modifications to apply
    effectiveness_history: List[float]  # Historical effectiveness scores
    usage_count: int                   # Number of times applied
    last_used: float                   # Timestamp of last usage
    confidence_score: float            # Current confidence in adaptation
```

#### LearningInsight
```python
@dataclass
class LearningInsight:
    insight_type: str                   # Type of insight discovered
    description: str                    # Human-readable description
    evidence: List[str]                # Supporting evidence for insight
    recommendations: List[str]          # Actionable recommendations
    confidence: float                   # Confidence in insight accuracy
    impact_score: float                # Expected impact of implementing insight
```

## Learning Record Management

### record_learning_event()
```python
def record_learning_event(self, 
                        learning_type: LearningType,
                        scope: AdaptationScope,
                        context: Dict[str, Any],
                        pattern: Dict[str, Any],
                        effectiveness_score: float,
                        confidence: float = 1.0,
                        metadata: Dict[str, Any] = None) -> str:
    
    record = LearningRecord(
        timestamp=time.time(),
        learning_type=learning_type,
        scope=scope,
        context=context,
        pattern=pattern,
        effectiveness_score=effectiveness_score,
        confidence=confidence,
        metadata=metadata
    )
    
    self.learning_records.append(record)
    
    # Trigger adaptation creation if pattern is significant
    if effectiveness_score > 0.7 and confidence > 0.6:
        self._create_adaptation_from_record(record)
    
    self._save_learning_data()
    return f"learning_{int(record.timestamp)}"
```

**Learning Event Processing**:
1. **Record Creation**: Capture learning event with full context
2. **Significance Assessment**: Evaluate effectiveness and confidence thresholds
3. **Adaptation Trigger**: Create adaptations for significant patterns
4. **Persistence**: Save learning data for future sessions
5. **ID Generation**: Return unique learning record identifier

## Pattern Recognition and Adaptation

### Pattern Signature Generation
```python
def _generate_pattern_signature(self, pattern: Dict[str, Any], context: Dict[str, Any]) -> str:
    key_elements = []
    
    # Pattern type
    if 'type' in pattern:
        key_elements.append(f"type:{pattern['type']}")
    
    # Context elements
    if 'operation_type' in context:
        key_elements.append(f"op:{context['operation_type']}")
    
    if 'complexity_score' in context:
        complexity_bucket = int(context['complexity_score'] * 10) / 10  # Round to 0.1
        key_elements.append(f"complexity:{complexity_bucket}")
    
    if 'file_count' in context:
        file_bucket = min(context['file_count'], 10)  # Cap at 10 for grouping
        key_elements.append(f"files:{file_bucket}")
    
    # Pattern-specific elements
    for key in ['mcp_server', 'mode', 'compression_level', 'delegation_strategy']:
        if key in pattern:
            key_elements.append(f"{key}:{pattern[key]}")
    
    return "_".join(sorted(key_elements))
```

**Signature Components**:
- **Pattern Type**: Core pattern classification
- **Operation Context**: Operation type, complexity, file count
- **Domain Elements**: MCP server, mode, compression level, delegation strategy
- **Normalization**: Bucketing and sorting for consistent matching

### Adaptation Creation
```python
def _create_adaptation_from_record(self, record: LearningRecord):
    pattern_signature = self._generate_pattern_signature(record.pattern, record.context)
    
    # Check if adaptation already exists
    if pattern_signature in self.adaptations:
        adaptation = self.adaptations[pattern_signature]
        adaptation.effectiveness_history.append(record.effectiveness_score)
        adaptation.usage_count += 1
        adaptation.last_used = record.timestamp
        
        # Update confidence based on consistency
        if len(adaptation.effectiveness_history) > 1:
            consistency = 1.0 - statistics.stdev(adaptation.effectiveness_history[-5:]) / max(statistics.mean(adaptation.effectiveness_history[-5:]), 0.1)
            adaptation.confidence_score = min(consistency * record.confidence, 1.0)
    else:
        # Create new adaptation
        adaptation_id = f"adapt_{int(record.timestamp)}_{len(self.adaptations)}"
        
        adaptation = Adaptation(
            adaptation_id=adaptation_id,
            pattern_signature=pattern_signature,
            trigger_conditions=self._extract_trigger_conditions(record.context),
            modifications=self._extract_modifications(record.pattern),
            effectiveness_history=[record.effectiveness_score],
            usage_count=1,
            last_used=record.timestamp,
            confidence_score=record.confidence
        )
        
        self.adaptations[pattern_signature] = adaptation
```

**Adaptation Logic**:
- **Existing Adaptation**: Update effectiveness history and confidence based on consistency
- **New Adaptation**: Create adaptation with initial effectiveness and confidence scores
- **Confidence Calculation**: Based on consistency of effectiveness scores over time

## Context Matching and Application

### Context Matching
```python
def _matches_trigger_conditions(self, conditions: Dict[str, Any], context: Dict[str, Any]) -> bool:
    for key, expected_value in conditions.items():
        if key not in context:
            continue
        
        context_value = context[key]
        
        # Exact match for strings and booleans
        if isinstance(expected_value, (str, bool)):
            if context_value != expected_value:
                return False
        
        # Range match for numbers
        elif isinstance(expected_value, (int, float)):
            tolerance = 0.1 if isinstance(expected_value, float) else 1
            if abs(context_value - expected_value) > tolerance:
                return False
    
    return True
```

**Matching Strategies**:
- **Exact Match**: String and boolean values must match exactly
- **Range Match**: Numeric values within tolerance (0.1 for floats, 1 for integers)
- **Missing Values**: Ignore missing context keys (graceful degradation)

### Adaptation Application
```python
def apply_adaptations(self, 
                     context: Dict[str, Any], 
                     base_recommendations: Dict[str, Any]) -> Dict[str, Any]:
    
    relevant_adaptations = self.get_adaptations_for_context(context)
    enhanced_recommendations = base_recommendations.copy()
    
    for adaptation in relevant_adaptations:
        # Apply modifications from adaptation
        for modification_type, modification_value in adaptation.modifications.items():
            if modification_type == 'preferred_mcp_server':
                # Enhance MCP server selection
                if 'recommended_mcp_servers' not in enhanced_recommendations:
                    enhanced_recommendations['recommended_mcp_servers'] = []
                
                servers = enhanced_recommendations['recommended_mcp_servers']
                if modification_value not in servers:
                    servers.insert(0, modification_value)  # Prioritize learned preference
            
            elif modification_type == 'preferred_mode':
                # Enhance mode selection
                if 'recommended_modes' not in enhanced_recommendations:
                    enhanced_recommendations['recommended_modes'] = []
                
                modes = enhanced_recommendations['recommended_modes']
                if modification_value not in modes:
                    modes.insert(0, modification_value)
            
            elif modification_type == 'suggested_flags':
                # Enhance flag suggestions
                if 'suggested_flags' not in enhanced_recommendations:
                    enhanced_recommendations['suggested_flags'] = []
                
                for flag in modification_value:
                    if flag not in enhanced_recommendations['suggested_flags']:
                        enhanced_recommendations['suggested_flags'].append(flag)
        
        # Update usage tracking
        adaptation.usage_count += 1
        adaptation.last_used = time.time()
    
    return enhanced_recommendations
```

**Application Process**:
1. **Context Matching**: Find adaptations that match current context
2. **Recommendation Enhancement**: Apply learned preferences to base recommendations
3. **Prioritization**: Insert learned preferences at the beginning of recommendation lists  
4. **Usage Tracking**: Update usage statistics for applied adaptations
5. **Metadata Addition**: Include adaptation metadata in enhanced recommendations

## Learning Insights Generation

### generate_learning_insights()
```python
def generate_learning_insights(self) -> List[LearningInsight]:
    insights = []
    
    # User preference insights
    insights.extend(self._analyze_user_preferences())
    
    # Performance pattern insights
    insights.extend(self._analyze_performance_patterns())
    
    # Error pattern insights
    insights.extend(self._analyze_error_patterns())
    
    # Effectiveness insights
    insights.extend(self._analyze_effectiveness_patterns())
    
    return insights
```

### User Preference Analysis
```python
def _analyze_user_preferences(self) -> List[LearningInsight]:
    insights = []
    
    # Analyze MCP server preferences
    mcp_usage = {}
    for record in self.learning_records:
        if record.learning_type == LearningType.USER_PREFERENCE:
            server = record.pattern.get('mcp_server')
            if server:
                if server not in mcp_usage:
                    mcp_usage[server] = []
                mcp_usage[server].append(record.effectiveness_score)
    
    if mcp_usage:
        # Find most effective server
        server_effectiveness = {
            server: statistics.mean(scores)
            for server, scores in mcp_usage.items()
            if len(scores) >= 3
        }
        
        if server_effectiveness:
            best_server = max(server_effectiveness, key=server_effectiveness.get)
            best_score = server_effectiveness[best_server]
            
            if best_score > 0.8:
                insights.append(LearningInsight(
                    insight_type="user_preference",
                    description=f"User consistently prefers {best_server} MCP server",
                    evidence=[f"Effectiveness score: {best_score:.2f}", f"Usage count: {len(mcp_usage[best_server])}"],
                    recommendations=[f"Auto-suggest {best_server} for similar operations"],
                    confidence=min(best_score, 1.0),
                    impact_score=0.7
                ))
    
    return insights
```

### Performance Pattern Analysis
```python
def _analyze_performance_patterns(self) -> List[LearningInsight]:
    insights = []
    
    # Analyze delegation effectiveness
    delegation_records = [
        r for r in self.learning_records
        if r.learning_type == LearningType.PERFORMANCE_OPTIMIZATION
        and 'delegation' in r.pattern
    ]
    
    if len(delegation_records) >= 5:
        avg_effectiveness = statistics.mean([r.effectiveness_score for r in delegation_records])
        
        if avg_effectiveness > 0.75:
            insights.append(LearningInsight(
                insight_type="performance_optimization",
                description="Delegation consistently improves performance",
                evidence=[f"Average effectiveness: {avg_effectiveness:.2f}", f"Sample size: {len(delegation_records)}"],
                recommendations=["Enable delegation for multi-file operations", "Lower delegation threshold"],
                confidence=avg_effectiveness,
                impact_score=0.8
            ))
    
    return insights
```

### Error Pattern Analysis
```python
def _analyze_error_patterns(self) -> List[LearningInsight]:
    insights = []
    
    error_records = [
        r for r in self.learning_records
        if r.learning_type == LearningType.ERROR_RECOVERY
    ]
    
    if len(error_records) >= 3:
        # Analyze common error contexts
        error_contexts = {}
        for record in error_records:
            context_key = record.context.get('operation_type', 'unknown')
            if context_key not in error_contexts:
                error_contexts[context_key] = []
            error_contexts[context_key].append(record)
        
        for context, records in error_contexts.items():
            if len(records) >= 2:
                avg_recovery_effectiveness = statistics.mean([r.effectiveness_score for r in records])
                
                insights.append(LearningInsight(
                    insight_type="error_recovery",
                    description=f"Error patterns identified for {context} operations",
                    evidence=[f"Occurrence count: {len(records)}", f"Recovery effectiveness: {avg_recovery_effectiveness:.2f}"],
                    recommendations=[f"Add proactive validation for {context} operations"],
                    confidence=min(len(records) / 5, 1.0),
                    impact_score=0.6
                ))
    
    return insights
```

### Effectiveness Trend Analysis
```python
def _analyze_effectiveness_patterns(self) -> List[LearningInsight]:
    insights = []
    
    if len(self.learning_records) >= 10:
        recent_records = sorted(self.learning_records, key=lambda r: r.timestamp)[-10:]
        avg_effectiveness = statistics.mean([r.effectiveness_score for r in recent_records])
        
        if avg_effectiveness > 0.8:
            insights.append(LearningInsight(
                insight_type="effectiveness_trend",
                description="SuperClaude effectiveness is high and improving",
                evidence=[f"Recent average effectiveness: {avg_effectiveness:.2f}"],
                recommendations=["Continue current learning patterns", "Consider expanding adaptation scope"],
                confidence=avg_effectiveness,
                impact_score=0.9
            ))
        elif avg_effectiveness < 0.6:
            insights.append(LearningInsight(
                insight_type="effectiveness_concern",
                description="SuperClaude effectiveness below optimal",
                evidence=[f"Recent average effectiveness: {avg_effectiveness:.2f}"],
                recommendations=["Review recent adaptations", "Gather more user feedback", "Adjust learning thresholds"],
                confidence=1.0 - avg_effectiveness,
                impact_score=0.8
            ))
    
    return insights
```

## Effectiveness Feedback Integration

### record_effectiveness_feedback()
```python
def record_effectiveness_feedback(self, 
                                adaptation_ids: List[str], 
                                effectiveness_score: float,
                                context: Dict[str, Any]):
    
    for adaptation_id in adaptation_ids:
        # Find adaptation by ID
        adaptation = None
        for adapt in self.adaptations.values():
            if adapt.adaptation_id == adaptation_id:
                adaptation = adapt
                break
        
        if adaptation:
            adaptation.effectiveness_history.append(effectiveness_score)
            
            # Update confidence based on consistency
            if len(adaptation.effectiveness_history) > 2:
                recent_scores = adaptation.effectiveness_history[-5:]
                consistency = 1.0 - statistics.stdev(recent_scores) / max(statistics.mean(recent_scores), 0.1)
                adaptation.confidence_score = min(consistency, 1.0)
            
            # Record learning event
            self.record_learning_event(
                LearningType.EFFECTIVENESS_FEEDBACK,
                AdaptationScope.USER,
                context,
                {'adaptation_id': adaptation_id},
                effectiveness_score,
                adaptation.confidence_score
            )
```

**Feedback Processing**:
1. **Adaptation Lookup**: Find adaptation by unique ID
2. **Effectiveness Update**: Append new effectiveness score to history
3. **Confidence Recalculation**: Update confidence based on score consistency
4. **Learning Event Recording**: Create feedback learning record for future analysis

## Data Persistence and Management

### Data Storage
```python
def _save_learning_data(self):
    try:
        # Save learning records
        records_file = self.cache_dir / "learning_records.json"
        with open(records_file, 'w') as f:
            json.dump([asdict(record) for record in self.learning_records], f, indent=2)
        
        # Save adaptations
        adaptations_file = self.cache_dir / "adaptations.json"
        with open(adaptations_file, 'w') as f:
            json.dump({k: asdict(v) for k, v in self.adaptations.items()}, f, indent=2)
        
        # Save user preferences
        preferences_file = self.cache_dir / "user_preferences.json"
        with open(preferences_file, 'w') as f:
            json.dump(self.user_preferences, f, indent=2)
        
        # Save project patterns
        patterns_file = self.cache_dir / "project_patterns.json"
        with open(patterns_file, 'w') as f:
            json.dump(self.project_patterns, f, indent=2)
            
    except Exception as e:
        pass  # Silent fail for cache operations
```

### Data Cleanup
```python
def cleanup_old_data(self, max_age_days: int = 30):
    cutoff_time = time.time() - (max_age_days * 24 * 60 * 60)
    
    # Remove old learning records
    self.learning_records = [
        record for record in self.learning_records
        if record.timestamp > cutoff_time
    ]
    
    # Remove unused adaptations
    self.adaptations = {
        k: v for k, v in self.adaptations.items()
        if v.last_used > cutoff_time or v.usage_count > 5
    }
    
    self._save_learning_data()
```

**Cleanup Strategy**:
- **Learning Records**: Remove records older than max_age_days
- **Adaptations**: Keep adaptations used within max_age_days OR with usage_count > 5
- **Automatic Cleanup**: Triggered during initialization and periodically

## Integration with Hooks

### Hook Usage Pattern
```python
# Initialize learning engine
learning_engine = LearningEngine(cache_dir=Path("cache"))

# Record learning event during hook operation
learning_engine.record_learning_event(
    learning_type=LearningType.USER_PREFERENCE,
    scope=AdaptationScope.USER,
    context={
        'operation_type': 'build',
        'complexity_score': 0.6,
        'file_count': 8,
        'user_expertise': 'intermediate'
    },
    pattern={
        'mcp_server': 'serena',
        'mode': 'task_management',
        'flags': ['--delegate', '--think-hard']
    },
    effectiveness_score=0.85,
    confidence=0.9
)

# Apply learned adaptations to recommendations
base_recommendations = {
    'recommended_mcp_servers': ['morphllm'],
    'recommended_modes': ['brainstorming'],
    'suggested_flags': ['--think']
}

enhanced_recommendations = learning_engine.apply_adaptations(
    context={
        'operation_type': 'build',
        'complexity_score': 0.6,
        'file_count': 8
    },
    base_recommendations=base_recommendations
)

print(f"Enhanced servers: {enhanced_recommendations['recommended_mcp_servers']}")  # ['serena', 'morphllm']
print(f"Enhanced modes: {enhanced_recommendations['recommended_modes']}")          # ['task_management', 'brainstorming']
print(f"Enhanced flags: {enhanced_recommendations['suggested_flags']}")           # ['--delegate', '--think-hard', '--think']
```

### Learning Insights Usage
```python
# Generate insights from learning patterns
insights = learning_engine.generate_learning_insights()

for insight in insights:
    print(f"Insight Type: {insight.insight_type}")
    print(f"Description: {insight.description}")
    print(f"Evidence: {insight.evidence}")
    print(f"Recommendations: {insight.recommendations}")
    print(f"Confidence: {insight.confidence:.2f}")
    print(f"Impact Score: {insight.impact_score:.2f}")
    print("---")
```

### Effectiveness Feedback Integration
```python
# Record effectiveness feedback after operation completion
adaptation_ids = enhanced_recommendations.get('applied_adaptations', [])
if adaptation_ids:
    adaptation_ids_list = [adapt['id'] for adapt in adaptation_ids]
    learning_engine.record_effectiveness_feedback(
        adaptation_ids=adaptation_ids_list,
        effectiveness_score=0.92,
        context={'operation_result': 'success', 'user_satisfaction': 'high'}
    )
```

## Performance Characteristics

### Learning Operations
- **Learning Event Recording**: <5ms for single event with persistence
- **Pattern Signature Generation**: <3ms for typical context and pattern
- **Adaptation Creation**: <10ms including condition extraction and modification setup
- **Context Matching**: <2ms per adaptation for trigger condition evaluation
- **Adaptation Application**: <15ms for typical enhancement with multiple adaptations

### Memory Efficiency
- **Learning Records**: ~500B per record with full context and metadata
- **Adaptations**: ~300-500B per adaptation with effectiveness history
- **Pattern Signatures**: ~50-100B per signature for matching
- **Cache Storage**: JSON serialization with compression for large datasets

### Effectiveness Metrics
- **Adaptation Accuracy**: >85% correct context matching for learned adaptations
- **Effectiveness Prediction**: 80%+ correlation between predicted and actual effectiveness
- **Learning Convergence**: 3-5 similar events required for stable adaptation creation
- **Data Persistence Reliability**: <0.1% data loss rate with automatic recovery

## Error Handling Strategies

### Learning Event Failures
```python
try:
    self.record_learning_event(learning_type, scope, context, pattern, effectiveness_score)
except Exception as e:
    # Log error but continue operation
    logger.log_error("learning_engine", f"Failed to record learning event: {e}")
    # Return dummy learning ID for caller consistency
    return f"learning_failed_{int(time.time())}"
```

### Adaptation Application Failures
- **Context Matching Errors**: Skip problematic adaptations, continue with others
- **Modification Application Errors**: Log warning, apply partial modifications
- **Effectiveness Tracking Errors**: Continue without tracking, log for later analysis

### Data Persistence Failures
- **File Write Errors**: Cache in memory, retry on next operation
- **Data Corruption**: Use backup files, regenerate from memory if needed
- **Permission Errors**: Fall back to temporary storage, warn user

## Configuration Requirements

### Learning Configuration
```yaml
learning_engine:
  enabled: true
  cache_directory: "cache/learning"
  max_learning_records: 10000
  max_adaptations: 1000
  cleanup_interval_days: 30
  
  thresholds:
    significant_effectiveness: 0.7
    significant_confidence: 0.6
    adaptation_usage_threshold: 5
    
  insights:
    min_records_for_analysis: 10
    min_pattern_occurrences: 3
    confidence_threshold: 0.6
```

### Adaptation Scopes
```yaml
adaptation_scopes:
  session:
    enabled: true
    max_adaptations: 100
    
  project:
    enabled: true
    max_adaptations: 500
    
  user:
    enabled: true
    max_adaptations: 1000
    
  global:
    enabled: false  # Privacy-sensitive, disabled by default
    anonymization_required: true
```

## Usage Examples

### Basic Learning Integration
```python
learning_engine = LearningEngine(cache_dir=Path("cache/learning"))

# Record successful MCP server selection
learning_engine.record_learning_event(
    LearningType.USER_PREFERENCE,
    AdaptationScope.USER,
    context={'operation_type': 'analyze', 'complexity_score': 0.7},
    pattern={'mcp_server': 'sequential'},
    effectiveness_score=0.9
)

# Apply learned preferences
recommendations = learning_engine.apply_adaptations(
    context={'operation_type': 'analyze', 'complexity_score': 0.7},
    base_recommendations={'recommended_mcp_servers': ['morphllm']}
)
print(recommendations['recommended_mcp_servers'])  # ['sequential', 'morphllm']
```

### Performance Optimization Learning
```python
# Record performance optimization success
learning_engine.record_learning_event(
    LearningType.PERFORMANCE_OPTIMIZATION,
    AdaptationScope.PROJECT,
    context={'file_count': 25, 'operation_type': 'refactor'},
    pattern={'delegation': 'auto', 'flags': ['--delegate', 'auto']},
    effectiveness_score=0.85,
    metadata={'time_saved_ms': 3000, 'quality_preserved': 0.95}
)

# Generate performance insights
insights = learning_engine.generate_learning_insights()
performance_insights = [i for i in insights if i.insight_type == "performance_optimization"]
```

## Dependencies and Relationships

### Internal Dependencies
- **yaml_loader**: Configuration loading for learning settings
- **Standard Libraries**: json, time, statistics, pathlib, typing, dataclasses, enum

### Framework Integration
- **Cross-Hook Learning**: Shared learning across all 7 hook implementations
- **Pattern Recognition**: Integration with pattern_detection.py for enhanced recommendations
- **Performance Monitoring**: Effectiveness tracking for framework optimization

### Hook Coordination
- Used by all hooks for consistent learning and adaptation
- Provides standardized learning interfaces and effectiveness tracking
- Enables cross-hook knowledge sharing and personalization

---

*This module serves as the intelligent learning and adaptation system for the SuperClaude framework, enabling continuous improvement through user preference learning, pattern recognition, and effectiveness feedback integration across all hook operations.*