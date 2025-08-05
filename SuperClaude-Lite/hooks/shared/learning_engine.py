"""
Learning Engine for SuperClaude-Lite

Cross-hook adaptation system that learns from user patterns, operation effectiveness,
and system performance to continuously improve SuperClaude intelligence.
"""

import json
import time
import statistics
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

from yaml_loader import config_loader


class LearningType(Enum):
    """Types of learning patterns."""
    USER_PREFERENCE = "user_preference"
    OPERATION_PATTERN = "operation_pattern"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    ERROR_RECOVERY = "error_recovery"
    EFFECTIVENESS_FEEDBACK = "effectiveness_feedback"


class AdaptationScope(Enum):
    """Scope of learning adaptations."""
    SESSION = "session"          # Apply only to current session
    PROJECT = "project"          # Apply to current project
    USER = "user"               # Apply across all user sessions
    GLOBAL = "global"           # Apply to all users (anonymized)


@dataclass
class LearningRecord:
    """Record of a learning event."""
    timestamp: float
    learning_type: LearningType
    scope: AdaptationScope
    context: Dict[str, Any]
    pattern: Dict[str, Any]
    effectiveness_score: float  # 0.0 to 1.0
    confidence: float          # 0.0 to 1.0
    metadata: Dict[str, Any]


@dataclass
class Adaptation:
    """An adaptation learned from patterns."""
    adaptation_id: str
    pattern_signature: str
    trigger_conditions: Dict[str, Any]
    modifications: Dict[str, Any]
    effectiveness_history: List[float]
    usage_count: int
    last_used: float
    confidence_score: float


@dataclass
class LearningInsight:
    """Insight derived from learning patterns."""
    insight_type: str
    description: str
    evidence: List[str]
    recommendations: List[str]
    confidence: float
    impact_score: float


class LearningEngine:
    """
    Cross-hook adaptation system for continuous improvement.
    
    Features:
    - User preference learning and adaptation
    - Operation pattern recognition and optimization
    - Performance feedback integration
    - Cross-hook coordination and knowledge sharing
    - Effectiveness measurement and validation
    - Personalization and project-specific adaptations
    """
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        self.learning_records: List[LearningRecord] = []
        self.adaptations: Dict[str, Adaptation] = {}
        self.user_preferences: Dict[str, Any] = {}
        self.project_patterns: Dict[str, Dict[str, Any]] = {}
        
        self._load_learning_data()
        
    def _load_learning_data(self):
        """Load existing learning data from cache."""
        try:
            # Load learning records
            records_file = self.cache_dir / "learning_records.json"
            if records_file.exists():
                with open(records_file, 'r') as f:
                    data = json.load(f)
                    self.learning_records = [
                        LearningRecord(**record) for record in data
                    ]
            
            # Load adaptations
            adaptations_file = self.cache_dir / "adaptations.json"
            if adaptations_file.exists():
                with open(adaptations_file, 'r') as f:
                    data = json.load(f)
                    self.adaptations = {
                        k: Adaptation(**v) for k, v in data.items()
                    }
            
            # Load user preferences
            preferences_file = self.cache_dir / "user_preferences.json"
            if preferences_file.exists():
                with open(preferences_file, 'r') as f:
                    self.user_preferences = json.load(f)
            
            # Load project patterns
            patterns_file = self.cache_dir / "project_patterns.json"
            if patterns_file.exists():
                with open(patterns_file, 'r') as f:
                    self.project_patterns = json.load(f)
                    
        except Exception as e:
            # Initialize empty data on error
            self.learning_records = []
            self.adaptations = {}
            self.user_preferences = {}
            self.project_patterns = {}
    
    def record_learning_event(self, 
                            learning_type: LearningType,
                            scope: AdaptationScope,
                            context: Dict[str, Any],
                            pattern: Dict[str, Any],
                            effectiveness_score: float,
                            confidence: float = 1.0,
                            metadata: Dict[str, Any] = None) -> str:
        """
        Record a learning event for future adaptation.
        
        Args:
            learning_type: Type of learning event
            scope: Scope of the learning (session, project, user, global)
            context: Context in which the learning occurred
            pattern: Pattern or behavior that was observed
            effectiveness_score: How effective the pattern was (0.0 to 1.0)
            confidence: Confidence in the learning (0.0 to 1.0)
            metadata: Additional metadata about the learning event
            
        Returns:
            Learning record ID
        """
        if metadata is None:
            metadata = {}
        
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
        
        # Save to cache
        self._save_learning_data()
        
        return f"learning_{int(record.timestamp)}"
    
    def _create_adaptation_from_record(self, record: LearningRecord):
        """Create an adaptation from a significant learning record."""
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
    
    def _generate_pattern_signature(self, pattern: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate a unique signature for a pattern."""
        # Create a simplified signature based on key pattern elements
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
    
    def _extract_trigger_conditions(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract trigger conditions from context."""
        conditions = {}
        
        # Operational conditions
        for key in ['operation_type', 'complexity_score', 'file_count', 'directory_count']:
            if key in context:
                conditions[key] = context[key]
        
        # Environmental conditions
        for key in ['resource_usage_percent', 'conversation_length', 'user_expertise']:
            if key in context:
                conditions[key] = context[key]
        
        # Project conditions
        for key in ['project_type', 'has_tests', 'is_production']:
            if key in context:
                conditions[key] = context[key]
        
        return conditions
    
    def _extract_modifications(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Extract modifications to apply from pattern."""
        modifications = {}
        
        # MCP server preferences
        if 'mcp_server' in pattern:
            modifications['preferred_mcp_server'] = pattern['mcp_server']
        
        # Mode preferences
        if 'mode' in pattern:
            modifications['preferred_mode'] = pattern['mode']
        
        # Flag preferences
        if 'flags' in pattern:
            modifications['suggested_flags'] = pattern['flags']
        
        # Performance optimizations
        if 'optimization' in pattern:
            modifications['optimization'] = pattern['optimization']
        
        return modifications
    
    def get_adaptations_for_context(self, context: Dict[str, Any]) -> List[Adaptation]:
        """Get relevant adaptations for the current context."""
        relevant_adaptations = []
        
        for adaptation in self.adaptations.values():
            if self._matches_trigger_conditions(adaptation.trigger_conditions, context):
                # Check effectiveness threshold
                if adaptation.confidence_score > 0.5 and len(adaptation.effectiveness_history) > 0:
                    avg_effectiveness = statistics.mean(adaptation.effectiveness_history)
                    if avg_effectiveness > 0.6:
                        relevant_adaptations.append(adaptation)
        
        # Sort by effectiveness and confidence
        relevant_adaptations.sort(
            key=lambda a: statistics.mean(a.effectiveness_history) * a.confidence_score,
            reverse=True
        )
        
        return relevant_adaptations
    
    def _matches_trigger_conditions(self, conditions: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if context matches adaptation trigger conditions."""
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
    
    def apply_adaptations(self, 
                         context: Dict[str, Any], 
                         base_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply learned adaptations to enhance recommendations.
        
        Args:
            context: Current operation context
            base_recommendations: Base recommendations before adaptation
            
        Returns:
            Enhanced recommendations with learned adaptations applied
        """
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
                
                elif modification_type == 'optimization':
                    # Apply performance optimizations
                    if 'optimizations' not in enhanced_recommendations:
                        enhanced_recommendations['optimizations'] = []
                    enhanced_recommendations['optimizations'].append(modification_value)
            
            # Update usage tracking
            adaptation.usage_count += 1
            adaptation.last_used = time.time()
        
        # Add learning metadata
        enhanced_recommendations['applied_adaptations'] = [
            {
                'id': adaptation.adaptation_id,
                'confidence': adaptation.confidence_score,
                'effectiveness': statistics.mean(adaptation.effectiveness_history)
            }
            for adaptation in relevant_adaptations
        ]
        
        return enhanced_recommendations
    
    def record_effectiveness_feedback(self, 
                                    adaptation_ids: List[str], 
                                    effectiveness_score: float,
                                    context: Dict[str, Any]):
        """Record feedback on adaptation effectiveness."""
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
    
    def generate_learning_insights(self) -> List[LearningInsight]:
        """Generate insights from learning patterns."""
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
    
    def _analyze_user_preferences(self) -> List[LearningInsight]:
        """Analyze user preference patterns."""
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
    
    def _analyze_performance_patterns(self) -> List[LearningInsight]:
        """Analyze performance optimization patterns."""
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
    
    def _analyze_error_patterns(self) -> List[LearningInsight]:
        """Analyze error recovery patterns."""
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
    
    def _analyze_effectiveness_patterns(self) -> List[LearningInsight]:
        """Analyze overall effectiveness patterns."""
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
    
    def _save_learning_data(self):
        """Save learning data to cache files."""
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
    
    def cleanup_old_data(self, max_age_days: int = 30):
        """Clean up old learning data to prevent cache bloat."""
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