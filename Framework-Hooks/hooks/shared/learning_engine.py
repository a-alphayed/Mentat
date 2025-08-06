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
from intelligence_engine import IntelligenceEngine


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
        
        # Initialize intelligence engine for YAML pattern integration
        self.intelligence_engine = IntelligenceEngine()
        
        self._load_learning_data()
        
    def _load_learning_data(self):
        """Load existing learning data from cache with robust error handling."""
        # Initialize empty data structures first
        self.learning_records = []
        self.adaptations = {}
        self.user_preferences = {}
        self.project_patterns = {}
        
        try:
            # Load learning records with corruption detection
            records_file = self.cache_dir / "learning_records.json"
            if records_file.exists():
                try:
                    with open(records_file, 'r') as f:
                        content = f.read().strip()
                        if not content:
                            # Empty file, initialize with empty array
                            self._initialize_empty_records_file(records_file)
                        elif content == '[]':
                            # Valid empty array
                            self.learning_records = []
                        else:
                            # Try to parse JSON
                            data = json.loads(content)
                            if isinstance(data, list):
                                self.learning_records = [
                                    LearningRecord(**record) for record in data
                                    if self._validate_learning_record(record)
                                ]
                            else:
                                # Invalid format, reinitialize
                                self._initialize_empty_records_file(records_file)
                except (json.JSONDecodeError, TypeError, ValueError) as e:
                    # JSON corruption detected, reinitialize
                    print(f"Learning records corrupted, reinitializing: {e}")
                    self._initialize_empty_records_file(records_file)
            else:
                # File doesn't exist, create it
                self._initialize_empty_records_file(records_file)
            
            # Load adaptations with error handling
            adaptations_file = self.cache_dir / "adaptations.json"
            if adaptations_file.exists():
                try:
                    with open(adaptations_file, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            self.adaptations = {
                                k: Adaptation(**v) for k, v in data.items()
                                if self._validate_adaptation_data(v)
                            }
                except (json.JSONDecodeError, TypeError, ValueError):
                    # Corrupted adaptations file, start fresh
                    self.adaptations = {}
            
            # Load user preferences with error handling
            preferences_file = self.cache_dir / "user_preferences.json"
            if preferences_file.exists():
                try:
                    with open(preferences_file, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            self.user_preferences = data
                except (json.JSONDecodeError, TypeError, ValueError):
                    self.user_preferences = {}
            
            # Load project patterns with error handling
            patterns_file = self.cache_dir / "project_patterns.json"
            if patterns_file.exists():
                try:
                    with open(patterns_file, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            self.project_patterns = data
                except (json.JSONDecodeError, TypeError, ValueError):
                    self.project_patterns = {}
                    
        except Exception as e:
            # Final fallback - ensure all data structures are initialized
            print(f"Error loading learning data, using defaults: {e}")
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
        
        # Validate effectiveness score bounds
        if not (0.0 <= effectiveness_score <= 1.0):
            raise ValueError(f"Effectiveness score must be between 0.0 and 1.0, got: {effectiveness_score}")
        
        # Validate confidence bounds  
        if not (0.0 <= confidence <= 1.0):
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got: {confidence}")
        
        # Flag suspicious perfect score sequences (potential overfitting)
        if effectiveness_score == 1.0:
            metadata['perfect_score_flag'] = True
        
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
        """Generate a unique signature for a pattern using YAML intelligence patterns."""
        # Get pattern dimensions from YAML intelligence patterns
        intelligence_patterns = self.intelligence_engine.evaluate_context(context, 'intelligence_patterns')
        pattern_dimensions = intelligence_patterns.get('recommendations', {}).get('pattern_dimensions', [])
        
        # If no YAML dimensions available, use fallback dimensions
        if not pattern_dimensions:
            pattern_dimensions = ['context_type', 'complexity_score', 'operation_type', 'performance_score']
        
        key_elements = []
        
        # Use YAML-defined dimensions for signature generation
        for dimension in pattern_dimensions:
            if dimension in context:
                value = context[dimension]
                # Bucket numeric values for better grouping
                if isinstance(value, (int, float)) and dimension in ['complexity_score', 'performance_score']:
                    bucketed_value = int(value * 10) / 10  # Round to 0.1
                    key_elements.append(f"{dimension}:{bucketed_value}")
                elif isinstance(value, (int, float)) and dimension in ['file_count', 'directory_count']:
                    bucketed_value = min(int(value), 10)  # Cap at 10 for grouping
                    key_elements.append(f"{dimension}:{bucketed_value}")
                else:
                    key_elements.append(f"{dimension}:{value}")
            elif dimension in pattern:
                key_elements.append(f"{dimension}:{pattern[dimension]}")
        
        # Add pattern-specific elements
        for key in ['mcp_server', 'mode', 'compression_level', 'delegation_strategy']:
            if key in pattern and key not in [d.split(':')[0] for d in key_elements]:
                key_elements.append(f"{key}:{pattern[key]}")
        
        signature = "_".join(sorted(key_elements))
        return signature if signature else "unknown_pattern"
    
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
        Apply learned adaptations enhanced with YAML intelligence patterns.
        
        Args:
            context: Current operation context
            base_recommendations: Base recommendations before adaptation
            
        Returns:
            Enhanced recommendations with learned adaptations and YAML intelligence applied
        """
        # Get YAML intelligence recommendations first
        mcp_intelligence = self.intelligence_engine.evaluate_context(context, 'mcp_orchestration')
        ux_intelligence = self.intelligence_engine.evaluate_context(context, 'user_experience')
        performance_intelligence = self.intelligence_engine.evaluate_context(context, 'performance_intelligence')
        
        # Start with base recommendations and add YAML intelligence
        enhanced_recommendations = base_recommendations.copy()
        
        # Integrate YAML-based MCP recommendations
        mcp_recs = mcp_intelligence.get('recommendations', {})
        if mcp_recs.get('primary_server'):
            if 'recommended_mcp_servers' not in enhanced_recommendations:
                enhanced_recommendations['recommended_mcp_servers'] = []
            servers = enhanced_recommendations['recommended_mcp_servers']
            if mcp_recs['primary_server'] not in servers:
                servers.insert(0, mcp_recs['primary_server'])
            
            # Add support servers
            for support_server in mcp_recs.get('support_servers', []):
                if support_server not in servers:
                    servers.append(support_server)
        
        # Integrate UX intelligence (project detection, smart defaults)
        ux_recs = ux_intelligence.get('recommendations', {})
        if ux_recs.get('suggested_servers'):
            if 'recommended_mcp_servers' not in enhanced_recommendations:
                enhanced_recommendations['recommended_mcp_servers'] = []
            for server in ux_recs['suggested_servers']:
                if server not in enhanced_recommendations['recommended_mcp_servers']:
                    enhanced_recommendations['recommended_mcp_servers'].append(server)
        
        # Integrate performance optimizations
        perf_recs = performance_intelligence.get('recommendations', {})
        if perf_recs.get('optimizations'):
            enhanced_recommendations['performance_optimizations'] = perf_recs['optimizations']
            enhanced_recommendations['resource_zone'] = perf_recs.get('resource_zone', 'green')
        
        # Apply learned adaptations on top of YAML intelligence
        relevant_adaptations = self.get_adaptations_for_context(context)
        
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
        """Save learning data to cache files with validation and atomic writes."""
        try:
            # Save learning records with validation
            records_file = self.cache_dir / "learning_records.json"
            records_data = []
            for record in self.learning_records:
                try:
                    # Convert record to dict and handle enums
                    record_dict = asdict(record)
                    
                    # Convert enum values to strings for JSON serialization
                    if isinstance(record_dict.get('learning_type'), LearningType):
                        record_dict['learning_type'] = record_dict['learning_type'].value
                    if isinstance(record_dict.get('scope'), AdaptationScope):
                        record_dict['scope'] = record_dict['scope'].value
                    
                    # Validate the record
                    if self._validate_learning_record_dict(record_dict):
                        records_data.append(record_dict)
                    else:
                        print(f"Warning: Invalid record skipped: {record_dict}")
                except Exception as e:
                    print(f"Warning: Error processing record: {e}")
                    continue  # Skip invalid records
            
            # Atomic write to prevent corruption during write
            temp_file = records_file.with_suffix('.tmp')
            with open(temp_file, 'w') as f:
                json.dump(records_data, f, indent=2)
            temp_file.replace(records_file)
            
            # Save adaptations with validation
            adaptations_file = self.cache_dir / "adaptations.json"
            adaptations_data = {}
            for k, v in self.adaptations.items():
                try:
                    adapt_dict = asdict(v)
                    if self._validate_adaptation_data(adapt_dict):
                        adaptations_data[k] = adapt_dict
                except Exception:
                    continue
            
            temp_file = adaptations_file.with_suffix('.tmp')
            with open(temp_file, 'w') as f:
                json.dump(adaptations_data, f, indent=2)
            temp_file.replace(adaptations_file)
            
            # Save user preferences
            preferences_file = self.cache_dir / "user_preferences.json"
            if isinstance(self.user_preferences, dict):
                temp_file = preferences_file.with_suffix('.tmp')
                with open(temp_file, 'w') as f:
                    json.dump(self.user_preferences, f, indent=2)
                temp_file.replace(preferences_file)
            
            # Save project patterns
            patterns_file = self.cache_dir / "project_patterns.json"
            if isinstance(self.project_patterns, dict):
                temp_file = patterns_file.with_suffix('.tmp')
                with open(temp_file, 'w') as f:
                    json.dump(self.project_patterns, f, indent=2)
                temp_file.replace(patterns_file)
                
        except Exception as e:
            print(f"Error saving learning data: {e}")
    
    def _initialize_empty_records_file(self, records_file: Path):
        """Initialize learning records file with empty array."""
        try:
            with open(records_file, 'w') as f:
                json.dump([], f)
        except Exception as e:
            print(f"Error initializing records file: {e}")
    
    def _validate_learning_record(self, record_data: dict) -> bool:
        """Validate learning record data structure."""
        required_fields = ['timestamp', 'learning_type', 'scope', 'context', 'pattern', 'effectiveness_score', 'confidence', 'metadata']
        try:
            return all(field in record_data for field in required_fields)
        except (TypeError, AttributeError):
            return False
    
    def _validate_learning_record_dict(self, record_dict: dict) -> bool:
        """Validate learning record dictionary before saving."""
        try:
            # Check required fields exist and have valid types
            if not isinstance(record_dict.get('timestamp'), (int, float)):
                return False
            
            # Handle both enum objects and string values for learning_type
            learning_type = record_dict.get('learning_type')
            if not (isinstance(learning_type, str) or isinstance(learning_type, LearningType)):
                return False
            
            # Handle both enum objects and string values for scope
            scope = record_dict.get('scope')
            if not (isinstance(scope, str) or isinstance(scope, AdaptationScope)):
                return False
                
            if not isinstance(record_dict.get('context'), dict):
                return False
            if not isinstance(record_dict.get('pattern'), dict):
                return False
            if not isinstance(record_dict.get('effectiveness_score'), (int, float)):
                return False
            if not isinstance(record_dict.get('confidence'), (int, float)):
                return False
            if not isinstance(record_dict.get('metadata'), dict):
                return False
            return True
        except (TypeError, AttributeError):
            return False
    
    def _validate_adaptation_data(self, adapt_data: dict) -> bool:
        """Validate adaptation data structure."""
        required_fields = ['adaptation_id', 'pattern_signature', 'trigger_conditions', 'modifications', 'effectiveness_history', 'usage_count', 'last_used', 'confidence_score']
        try:
            return all(field in adapt_data for field in required_fields)
        except (TypeError, AttributeError):
            return False
    
    def get_intelligent_recommendations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive intelligent recommendations combining YAML patterns and learned adaptations.
        
        Args:
            context: Current operation context
            
        Returns:
            Comprehensive recommendations with intelligence from multiple sources
        """
        # Get base recommendations from all YAML intelligence patterns
        base_recommendations = {}
        
        # Collect recommendations from all intelligence pattern types
        pattern_types = ['mcp_orchestration', 'hook_coordination', 'performance_intelligence', 
                        'validation_intelligence', 'user_experience', 'intelligence_patterns']
        
        intelligence_results = {}
        for pattern_type in pattern_types:
            try:
                result = self.intelligence_engine.evaluate_context(context, pattern_type)
                intelligence_results[pattern_type] = result
                
                # Merge recommendations
                recommendations = result.get('recommendations', {})
                for key, value in recommendations.items():
                    if key not in base_recommendations:
                        base_recommendations[key] = value
                    elif isinstance(base_recommendations[key], list) and isinstance(value, list):
                        # Merge lists without duplicates
                        base_recommendations[key] = list(set(base_recommendations[key] + value))
            except Exception as e:
                print(f"Warning: Could not evaluate {pattern_type} patterns: {e}")
        
        # Apply learned adaptations on top of YAML intelligence
        enhanced_recommendations = self.apply_adaptations(context, base_recommendations)
        
        # Add intelligence metadata
        enhanced_recommendations['intelligence_metadata'] = {
            'yaml_patterns_used': list(intelligence_results.keys()),
            'adaptations_applied': len(self.get_adaptations_for_context(context)),
            'confidence_scores': {k: v.get('confidence', 0.0) for k, v in intelligence_results.items()},
            'recommendations_source': 'yaml_intelligence_plus_learned_adaptations'
        }
        
        return enhanced_recommendations
    
    def cleanup_old_data(self, days_to_keep: int = 30):
        """Clean up old learning data to prevent cache bloat."""
        cutoff_time = time.time() - (days_to_keep * 24 * 60 * 60)
        
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
    
    def update_last_preference(self, preference_key: str, value: Any):
        """Simply store the last successful choice - no complex learning."""
        if not self.user_preferences:
            self.user_preferences = {}
        self.user_preferences[preference_key] = {
            "value": value,
            "timestamp": time.time()
        }
        self._save_learning_data()
    
    def get_last_preference(self, preference_key: str, default=None):
        """Get the last successful choice if available."""
        if not self.user_preferences:
            return default
        pref = self.user_preferences.get(preference_key, {})
        return pref.get("value", default)
    
    def update_project_info(self, project_path: str, info_type: str, value: Any):
        """Store basic project information."""
        if not self.project_patterns:
            self.project_patterns = {}
        if project_path not in self.project_patterns:
            self.project_patterns[project_path] = {}
        self.project_patterns[project_path][info_type] = value
        self.project_patterns[project_path]["last_updated"] = time.time()
        self._save_learning_data()