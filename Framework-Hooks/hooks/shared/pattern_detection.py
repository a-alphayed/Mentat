"""
Pattern Detection Engine for SuperClaude-Lite

Intelligent pattern detection for automatic mode activation,
MCP server selection, and operational optimization.
"""

import re
import json
from typing import Dict, Any, List, Set, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from yaml_loader import config_loader


class PatternType(Enum):
    """Types of patterns we can detect."""
    MODE_TRIGGER = "mode_trigger"
    MCP_SERVER = "mcp_server"
    OPERATION_TYPE = "operation_type"
    COMPLEXITY_INDICATOR = "complexity_indicator"
    PERSONA_HINT = "persona_hint"
    PERFORMANCE_HINT = "performance_hint"


@dataclass
class PatternMatch:
    """A detected pattern match."""
    pattern_type: PatternType
    pattern_name: str
    confidence: float  # 0.0 to 1.0
    matched_text: str
    suggestions: List[str]
    metadata: Dict[str, Any]


@dataclass
class DetectionResult:
    """Result of pattern detection analysis."""
    matches: List[PatternMatch]
    recommended_modes: List[str]
    recommended_mcp_servers: List[str]
    suggested_flags: List[str]
    complexity_score: float
    confidence_score: float


class PatternDetector:
    """
    Intelligent pattern detection system.
    
    Analyzes user input, context, and operation patterns to determine:
    - Which SuperClaude modes should be activated
    - Which MCP servers are needed
    - What optimization flags to apply
    - Complexity and performance considerations
    """
    
    def __init__(self):
        """Initialize pattern detector with configuration loading and error handling."""
        try:
            self.patterns = config_loader.load_config('modes') or {}
            self.mcp_patterns = config_loader.load_config('orchestrator') or {}
        except Exception as e:
            print(f"Warning: Failed to load configuration: {e}")
            self.patterns = {}
            self.mcp_patterns = {}
        
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for efficient matching with proper error handling."""
        self.compiled_patterns = {}
        self.mode_configs = {}
        self.mcp_configs = {}
        
        # Load mode detection patterns from the correct YAML structure
        mode_detection = self.patterns.get('mode_detection', {})
        for mode_name, mode_config in mode_detection.items():
            try:
                # Store mode configuration for threshold access
                self.mode_configs[mode_name] = mode_config
                
                # Compile all trigger patterns from different categories
                all_patterns = []
                trigger_patterns = mode_config.get('trigger_patterns', {})
                
                # Handle different YAML structures
                if isinstance(trigger_patterns, list):
                    # Simple list of patterns
                    all_patterns.extend(trigger_patterns)
                elif isinstance(trigger_patterns, dict):
                    # Nested categories of patterns
                    for category, patterns in trigger_patterns.items():
                        if isinstance(patterns, list):
                            all_patterns.extend(patterns)
                        elif isinstance(patterns, str):
                            all_patterns.append(patterns)
                elif isinstance(trigger_patterns, str):
                    # Single pattern string
                    all_patterns.append(trigger_patterns)
                
                # Compile patterns with error handling
                compiled = []
                for pattern in all_patterns:
                    try:
                        compiled.append(re.compile(pattern, re.IGNORECASE))
                    except re.error as e:
                        print(f"Warning: Invalid regex pattern '{pattern}' for mode {mode_name}: {e}")
                
                self.compiled_patterns[f"mode_{mode_name}"] = compiled
                
            except Exception as e:
                print(f"Warning: Error compiling patterns for mode {mode_name}: {e}")
                self.compiled_patterns[f"mode_{mode_name}"] = []
        
        # Load MCP server patterns from routing_patterns
        routing_patterns = self.mcp_patterns.get('routing_patterns', {})
        for server_name, server_config in routing_patterns.items():
            try:
                # Store server configuration
                self.mcp_configs[server_name] = server_config
                
                triggers = server_config.get('triggers', [])
                compiled = []
                for trigger in triggers:
                    try:
                        compiled.append(re.compile(trigger, re.IGNORECASE))
                    except re.error as e:
                        print(f"Warning: Invalid regex pattern '{trigger}' for server {server_name}: {e}")
                
                self.compiled_patterns[f"mcp_{server_name}"] = compiled
                
            except Exception as e:
                print(f"Warning: Error compiling patterns for MCP server {server_name}: {e}")
                self.compiled_patterns[f"mcp_{server_name}"] = []
    
    def detect_patterns(self, 
                       user_input: str, 
                       context: Dict[str, Any], 
                       operation_data: Dict[str, Any]) -> DetectionResult:
        """
        Perform comprehensive pattern detection with input validation and error handling.
        
        Args:
            user_input: User's request or command
            context: Session and environment context
            operation_data: Information about the planned operation
            
        Returns:
            DetectionResult with all detected patterns and recommendations
        """
        # Validate inputs
        is_valid, validation_message = self.validate_input(user_input, context, operation_data)
        if not is_valid:
            # Return empty result for invalid inputs
            return DetectionResult(
                matches=[],
                recommended_modes=[],
                recommended_mcp_servers=[],
                suggested_flags=[],
                complexity_score=0.0,
                confidence_score=0.0
            )
        
        matches = []
        
        try:
            # Detect mode triggers
            mode_matches = self._detect_mode_patterns(user_input, context)
            matches.extend(mode_matches)
            
            # Detect MCP server needs
            mcp_matches = self._detect_mcp_patterns(user_input, context, operation_data)
            matches.extend(mcp_matches)
            
            # Detect complexity indicators
            complexity_matches = self._detect_complexity_patterns(user_input, operation_data)
            matches.extend(complexity_matches)
            
            # Detect persona hints
            persona_matches = self._detect_persona_patterns(user_input, context)
            matches.extend(persona_matches)
            
            # Calculate overall scores
            complexity_score = self._calculate_complexity_score(matches, operation_data)
            confidence_score = self._calculate_confidence_score(matches)
            
            # Generate recommendations
            recommended_modes = self._get_recommended_modes(matches, complexity_score)
            recommended_mcp_servers = self._get_recommended_mcp_servers(matches, context)
            suggested_flags = self._get_suggested_flags(matches, complexity_score, context)
            
            return DetectionResult(
                matches=matches,
                recommended_modes=recommended_modes,
                recommended_mcp_servers=recommended_mcp_servers,
                suggested_flags=suggested_flags,
                complexity_score=complexity_score,
                confidence_score=confidence_score
            )
            
        except Exception as e:
            print(f"Error during pattern detection: {e}")
            # Return partial results if available
            return DetectionResult(
                matches=matches,  # Include any matches found before error
                recommended_modes=[],
                recommended_mcp_servers=[],
                suggested_flags=[],
                complexity_score=operation_data.get('complexity_score', 0.0),
                confidence_score=0.0
            )
    
    def _detect_mode_patterns(self, user_input: str, context: Dict[str, Any]) -> List[PatternMatch]:
        """Detect which SuperClaude modes should be activated using compiled patterns."""
        matches = []
        
        # Iterate through all compiled mode patterns
        for pattern_key, compiled_patterns in self.compiled_patterns.items():
            if not pattern_key.startswith("mode_"):
                continue
                
            mode_name = pattern_key[5:]  # Remove "mode_" prefix
            mode_config = self.mode_configs.get(mode_name, {})
            confidence_threshold = mode_config.get('confidence_threshold', 0.7)
            
            # Check if any pattern matches
            for pattern in compiled_patterns:
                try:
                    match = pattern.search(user_input)
                    if match:
                        # Calculate confidence based on pattern type and context
                        confidence = self._calculate_mode_confidence(mode_name, match, context)
                        
                        # Only include if above threshold
                        if confidence >= confidence_threshold:
                            matches.append(PatternMatch(
                                pattern_type=PatternType.MODE_TRIGGER,
                                pattern_name=mode_name,
                                confidence=confidence,
                                matched_text=match.group(),
                                suggestions=[f"Enable {mode_name} mode based on detected patterns"],
                                metadata={
                                    "mode": mode_name, 
                                    "auto_activate": mode_config.get('activation_type') == 'automatic',
                                    "threshold_met": confidence >= confidence_threshold
                                }
                            ))
                        break  # Stop after first match for this mode
                except Exception as e:
                    print(f"Warning: Error matching pattern for mode {mode_name}: {e}")
        
        # Check context-based triggers (resource usage, complexity, etc.)
        matches.extend(self._detect_context_mode_triggers(context))
        
        return matches
    
    def _calculate_mode_confidence(self, mode_name: str, match: re.Match, context: Dict[str, Any]) -> float:
        """Calculate confidence score for mode activation based on match and context."""
        base_confidence = 0.7
        
        # Mode-specific confidence adjustments
        mode_adjustments = {
            'brainstorming': {
                'uncertainty_words': ['maybe', 'not sure', 'thinking about', 'wondering'],
                'project_words': ['new project', 'startup', 'build something'],
                'exploration_words': ['brainstorm', 'explore', 'figure out']
            },
            'task_management': {
                'scope_words': ['multiple', 'many', 'complex', 'comprehensive'],
                'build_words': ['build', 'implement', 'create', 'develop']
            },
            'token_efficiency': {
                'efficiency_words': ['brief', 'concise', 'compressed', 'short'],
                'resource_words': ['token', 'resource', 'memory', 'optimization']
            }
        }
        
        adjustments = mode_adjustments.get(mode_name, {})
        matched_text = match.group().lower()
        
        # Boost confidence based on specific word categories
        confidence_boost = 0.0
        for category, words in adjustments.items():
            if any(word in matched_text for word in words):
                confidence_boost += 0.1
        
        # Context-based adjustments
        resource_usage = context.get('resource_usage_percent', 0)
        if mode_name == 'token_efficiency' and resource_usage > 75:
            confidence_boost += 0.2
        
        file_count = context.get('file_count', 1)
        complexity_score = context.get('complexity_score', 0.0)
        if mode_name == 'task_management' and (file_count > 3 or complexity_score > 0.4):
            confidence_boost += 0.15
        
        return min(base_confidence + confidence_boost, 1.0)
    
    def _detect_context_mode_triggers(self, context: Dict[str, Any]) -> List[PatternMatch]:
        """Detect mode triggers based on context alone (not user input)."""
        matches = []
        
        # Resource-based token efficiency trigger
        resource_usage = context.get('resource_usage_percent', 0)
        if resource_usage > 75:
            token_efficiency_config = self.mode_configs.get('token_efficiency', {})
            confidence_threshold = token_efficiency_config.get('confidence_threshold', 0.75)
            
            matches.append(PatternMatch(
                pattern_type=PatternType.MODE_TRIGGER,
                pattern_name="token_efficiency",
                confidence=0.85,
                matched_text="high_resource_usage",
                suggestions=["Auto-enable token efficiency due to resource constraints"],
                metadata={
                    "mode": "token_efficiency", 
                    "trigger": "resource_constraint",
                    "resource_usage": resource_usage
                }
            ))
        
        # Complexity-based task management trigger
        file_count = context.get('file_count', 1)
        complexity_score = context.get('complexity_score', 0.0)
        task_mgmt_config = self.mode_configs.get('task_management', {})
        auto_thresholds = task_mgmt_config.get('auto_activation_thresholds', {})
        
        file_threshold = auto_thresholds.get('file_count', 3)
        complexity_threshold = auto_thresholds.get('complexity_score', 0.4)
        
        if file_count >= file_threshold or complexity_score >= complexity_threshold:
            matches.append(PatternMatch(
                pattern_type=PatternType.MODE_TRIGGER,
                pattern_name="task_management",
                confidence=0.8,
                matched_text="complexity_threshold_met",
                suggestions=["Auto-enable task management for complex operations"],
                metadata={
                    "mode": "task_management",
                    "trigger": "complexity_threshold",
                    "file_count": file_count,
                    "complexity_score": complexity_score
                }
            ))
        
        return matches
    
    def _detect_mcp_patterns(self, user_input: str, context: Dict[str, Any], operation_data: Dict[str, Any]) -> List[PatternMatch]:
        """Detect which MCP servers should be activated using compiled patterns."""
        matches = []
        
        # Iterate through all compiled MCP server patterns
        for pattern_key, compiled_patterns in self.compiled_patterns.items():
            if not pattern_key.startswith("mcp_"):
                continue
                
            server_name = pattern_key[4:]  # Remove "mcp_" prefix
            server_config = self.mcp_configs.get(server_name, {})
            confidence_threshold = server_config.get('confidence_threshold', 0.7)
            
            # Check if any pattern matches
            for pattern in compiled_patterns:
                try:
                    match = pattern.search(user_input)
                    if match:
                        # Calculate confidence based on server type and context
                        confidence = self._calculate_mcp_confidence(server_name, match, context, operation_data)
                        
                        # Only include if above threshold
                        if confidence >= confidence_threshold:
                            matches.append(PatternMatch(
                                pattern_type=PatternType.MCP_SERVER,
                                pattern_name=server_name,
                                confidence=confidence,
                                matched_text=match.group(),
                                suggestions=[f"Enable {server_name} server for {server_config.get('capabilities', ['general'])[0]} capabilities"],
                                metadata={
                                    "mcp_server": server_name,
                                    "confidence_threshold": confidence_threshold,
                                    "server_config": server_config,
                                    "capabilities": server_config.get('capabilities', [])
                                }
                            ))
                        break  # Stop after first match for this server
                except Exception as e:
                    print(f"Warning: Error matching pattern for MCP server {server_name}: {e}")
        
        # Add hybrid intelligence selection (Morphllm vs Serena)
        matches.extend(self._detect_hybrid_intelligence_selection(operation_data))
        
        return matches
    
    def _calculate_mcp_confidence(self, server_name: str, match: re.Match, context: Dict[str, Any], operation_data: Dict[str, Any]) -> float:
        """Calculate confidence score for MCP server activation."""
        server_config = self.mcp_configs.get(server_name, {})
        base_confidence = server_config.get('confidence_threshold', 0.7)
        
        # Server-specific confidence adjustments
        matched_text = match.group().lower()
        confidence_boost = 0.0
        
        # Boost confidence based on operation context
        file_count = operation_data.get('file_count', 1)
        complexity_score = operation_data.get('complexity_score', 0.0)
        
        # Context-specific boosts
        if server_name == 'sequential' and (complexity_score > 0.6 or 'complex' in matched_text):
            confidence_boost += 0.15
        elif server_name == 'magic' and ('ui' in matched_text or 'component' in matched_text):
            confidence_boost += 0.1
        elif server_name == 'context7' and ('library' in matched_text or 'framework' in matched_text):
            confidence_boost += 0.1
        elif server_name == 'playwright' and ('test' in matched_text or 'automation' in matched_text):
            confidence_boost += 0.1
        
        # Performance profile adjustments
        performance_profile = server_config.get('performance_profile', 'standard')
        if performance_profile == 'intensive' and complexity_score > 0.5:
            confidence_boost += 0.05
        elif performance_profile == 'lightweight' and file_count <= 3:
            confidence_boost += 0.05
        
        return min(base_confidence + confidence_boost, 1.0)
    
    def _detect_hybrid_intelligence_selection(self, operation_data: Dict[str, Any]) -> List[PatternMatch]:
        """Detect whether to use Morphllm or Serena based on operation characteristics."""
        matches = []
        
        file_count = operation_data.get('file_count', 1)
        complexity_score = operation_data.get('complexity_score', 0.0)
        operation_types = operation_data.get('operation_types', [])
        
        # Get hybrid intelligence configuration
        hybrid_config = self.mcp_patterns.get('hybrid_intelligence', {}).get('morphllm_vs_serena', {})
        
        # Morphllm criteria
        morphllm_criteria = hybrid_config.get('morphllm_criteria', {})
        morphllm_file_max = morphllm_criteria.get('file_count_max', 10)
        morphllm_complexity_max = morphllm_criteria.get('complexity_max', 0.6)
        morphllm_ops = morphllm_criteria.get('preferred_operations', [])
        
        # Serena criteria
        serena_criteria = hybrid_config.get('serena_criteria', {})
        serena_file_min = serena_criteria.get('file_count_min', 5)
        serena_complexity_min = serena_criteria.get('complexity_min', 0.4)
        serena_ops = serena_criteria.get('preferred_operations', [])
        
        # Determine which system to use
        morphllm_score = 0
        serena_score = 0
        
        # File count scoring
        if file_count <= morphllm_file_max:
            morphllm_score += 1
        if file_count >= serena_file_min:
            serena_score += 1
        
        # Complexity scoring
        if complexity_score <= morphllm_complexity_max:
            morphllm_score += 1
        if complexity_score >= serena_complexity_min:
            serena_score += 1
        
        # Operation type scoring
        for op_type in operation_types:
            if op_type in morphllm_ops:
                morphllm_score += 1
            if op_type in serena_ops:
                serena_score += 1
        
        # Make selection based on scores
        if serena_score > morphllm_score:
            matches.append(PatternMatch(
                pattern_type=PatternType.MCP_SERVER,
                pattern_name="serena",
                confidence=0.8 + (serena_score * 0.05),
                matched_text="hybrid_intelligence_selection",
                suggestions=["Use Serena for complex multi-file operations with semantic understanding"],
                metadata={
                    "mcp_server": "serena",
                    "selection_reason": "hybrid_intelligence",
                    "file_count": file_count,
                    "complexity_score": complexity_score,
                    "score": serena_score
                }
            ))
        elif morphllm_score > 0:  # Only suggest Morphllm if it has some score
            matches.append(PatternMatch(
                pattern_type=PatternType.MCP_SERVER,
                pattern_name="morphllm",
                confidence=0.7 + (morphllm_score * 0.05),
                matched_text="hybrid_intelligence_selection",
                suggestions=["Use Morphllm for efficient editing operations with pattern optimization"],
                metadata={
                    "mcp_server": "morphllm",
                    "selection_reason": "hybrid_intelligence",
                    "file_count": file_count,
                    "complexity_score": complexity_score,
                    "score": morphllm_score
                }
            ))
        
        return matches
    
    def _detect_complexity_patterns(self, user_input: str, operation_data: Dict[str, Any]) -> List[PatternMatch]:
        """Detect complexity indicators in the request with configurable thresholds."""
        matches = []
        
        # Get complexity thresholds from configuration
        auto_activation = self.mcp_patterns.get('auto_activation', {})
        complexity_thresholds = auto_activation.get('complexity_thresholds', {})
        
        # High complexity indicators from text patterns
        high_complexity_patterns = [
            (r"(?:entire|whole|complete)\s+(?:codebase|system|application)", 0.4),
            (r"(?:refactor|migrate|restructure)\s+(?:all|everything|entire)", 0.35),
            (r"(?:architecture|system-wide|comprehensive)\s+(?:change|update|redesign)", 0.3),
            (r"(?:complex|complicated|sophisticated)\s+(?:logic|algorithm|system)", 0.25)
        ]
        
        for pattern, score_boost in high_complexity_patterns:
            try:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    matches.append(PatternMatch(
                        pattern_type=PatternType.COMPLEXITY_INDICATOR,
                        pattern_name="high_complexity",
                        confidence=0.8,
                        matched_text=match.group(),
                        suggestions=["Consider delegation and thinking modes"],
                        metadata={"complexity_level": "high", "score_boost": score_boost}
                    ))
                    break
            except re.error as e:
                print(f"Warning: Invalid complexity pattern: {e}")
        
        # File count and operation complexity indicators
        file_count = operation_data.get('file_count', 1)
        complexity_score = operation_data.get('complexity_score', 0.0)
        directory_count = operation_data.get('directory_count', 1)
        
        # Multi-file operation detection with configurable thresholds
        delegation_threshold = complexity_thresholds.get('enable_delegation', {})
        file_threshold = delegation_threshold.get('file_count', 3)
        dir_threshold = delegation_threshold.get('directory_count', 2)
        complexity_threshold = delegation_threshold.get('complexity_score', 0.4)
        
        if file_count >= file_threshold:
            matches.append(PatternMatch(
                pattern_type=PatternType.COMPLEXITY_INDICATOR,
                pattern_name="multi_file_operation",
                confidence=0.9,
                matched_text=f"{file_count}_files",
                suggestions=[f"Enable delegation for {file_count}-file operations"],
                metadata={
                    "file_count": file_count, 
                    "delegation_recommended": True,
                    "threshold_met": "file_count"
                }
            ))
        
        if directory_count >= dir_threshold:
            matches.append(PatternMatch(
                pattern_type=PatternType.COMPLEXITY_INDICATOR,
                pattern_name="multi_directory_operation",
                confidence=0.85,
                matched_text=f"{directory_count}_directories",
                suggestions=[f"Enable delegation for {directory_count}-directory operations"],
                metadata={
                    "directory_count": directory_count,
                    "delegation_recommended": True,
                    "threshold_met": "directory_count"
                }
            ))
        
        if complexity_score >= complexity_threshold:
            matches.append(PatternMatch(
                pattern_type=PatternType.COMPLEXITY_INDICATOR,
                pattern_name="high_complexity_score",
                confidence=0.8 + min(complexity_score * 0.2, 0.2),  # Cap boost at 0.2
                matched_text=f"complexity_{complexity_score:.2f}",
                suggestions=[f"Enable advanced processing for complexity score {complexity_score:.2f}"],
                metadata={
                    "complexity_score": complexity_score,
                    "sequential_recommended": complexity_score > 0.6,
                    "threshold_met": "complexity_score"
                }
            ))
        
        return matches
    
    def _detect_persona_patterns(self, user_input: str, context: Dict[str, Any]) -> List[PatternMatch]:
        """Detect hints about which persona should be active with improved confidence calculation."""
        matches = []
        
        # Enhanced persona patterns with confidence weighting
        persona_patterns = {
            "architect": {
                "patterns": [r"(?:architecture|design|structure|system)\s+(?:review|analysis|planning)"],
                "base_confidence": 0.75,
                "boost_words": ["architecture", "design", "structure", "system", "planning"]
            },
            "performance": {
                "patterns": [r"(?:performance|optimization|speed|efficiency|bottleneck)"],
                "base_confidence": 0.8,
                "boost_words": ["performance", "optimization", "speed", "efficiency", "bottleneck"]
            },
            "security": {
                "patterns": [r"(?:security|vulnerability|audit|secure|safety)"],
                "base_confidence": 0.85,
                "boost_words": ["security", "vulnerability", "audit", "secure", "safety"]
            },
            "frontend": {
                "patterns": [r"(?:ui|frontend|interface|component|design|responsive)"],
                "base_confidence": 0.75,
                "boost_words": ["ui", "frontend", "interface", "component", "responsive"]
            },
            "backend": {
                "patterns": [r"(?:api|server|database|backend|service)"],
                "base_confidence": 0.75,
                "boost_words": ["api", "server", "database", "backend", "service"]
            },
            "devops": {
                "patterns": [r"(?:deploy|deployment|ci|cd|infrastructure|docker|kubernetes)"],
                "base_confidence": 0.8,
                "boost_words": ["deploy", "deployment", "infrastructure", "docker", "kubernetes"]
            },
            "testing": {
                "patterns": [r"(?:test|testing|qa|quality|coverage|validation)"],
                "base_confidence": 0.75,
                "boost_words": ["test", "testing", "qa", "quality", "coverage", "validation"]
            }
        }
        
        for persona, persona_config in persona_patterns.items():
            patterns = persona_config["patterns"]
            base_confidence = persona_config["base_confidence"]
            boost_words = persona_config["boost_words"]
            
            for pattern in patterns:
                try:
                    match = re.search(pattern, user_input, re.IGNORECASE)
                    if match:
                        # Calculate confidence with word-based boosting
                        confidence = self._calculate_persona_confidence(
                            base_confidence, match, boost_words, user_input
                        )
                        
                        matches.append(PatternMatch(
                            pattern_type=PatternType.PERSONA_HINT,
                            pattern_name=persona,
                            confidence=confidence,
                            matched_text=match.group(),
                            suggestions=[f"Consider {persona} persona for specialized expertise"],
                            metadata={
                                "persona": persona, 
                                "domain_specific": True,
                                "base_confidence": base_confidence,
                                "calculated_confidence": confidence
                            }
                        ))
                        break  # Stop after first match for this persona
                except re.error as e:
                    print(f"Warning: Invalid persona pattern for {persona}: {e}")
        
        return matches
    
    def _calculate_persona_confidence(self, base_confidence: float, match: re.Match, boost_words: List[str], full_text: str) -> float:
        """Calculate persona confidence with word-based boosting."""
        confidence = base_confidence
        matched_text = match.group().lower()
        full_text_lower = full_text.lower()
        
        # Boost confidence based on additional domain words in the full text
        word_count = 0
        for word in boost_words:
            if word in full_text_lower:
                word_count += 1
        
        # Add confidence boost based on domain word density
        confidence_boost = min(word_count * 0.05, 0.15)  # Cap at 0.15
        
        return min(confidence + confidence_boost, 1.0)
    
    def _calculate_complexity_score(self, matches: List[PatternMatch], operation_data: Dict[str, Any]) -> float:
        """Calculate overall complexity score from detected patterns with proper weighting."""
        try:
            base_score = operation_data.get('complexity_score', 0.0)
            
            # Add complexity from pattern matches with proper validation
            complexity_boost = 0.0
            for match in matches:
                if match.pattern_type == PatternType.COMPLEXITY_INDICATOR:
                    score_boost = match.metadata.get('score_boost', 0.1)
                    if isinstance(score_boost, (int, float)) and 0 <= score_boost <= 1:
                        complexity_boost += score_boost
            
            # Weight the pattern-based boost to prevent over-scoring
            weighted_boost = complexity_boost * 0.7  # Reduce impact of pattern matches
            final_score = base_score + weighted_boost
            
            return min(max(final_score, 0.0), 1.0)  # Ensure score is between 0 and 1
            
        except Exception as e:
            print(f"Warning: Error calculating complexity score: {e}")
            return operation_data.get('complexity_score', 0.0)
    
    def _calculate_confidence_score(self, matches: List[PatternMatch]) -> float:
        """Calculate overall confidence in pattern detection with improved weighting."""
        try:
            if not matches:
                return 0.0
            
            # Weight different match types differently
            type_weights = {
                PatternType.MODE_TRIGGER: 0.3,
                PatternType.MCP_SERVER: 0.25,
                PatternType.COMPLEXITY_INDICATOR: 0.2,
                PatternType.PERSONA_HINT: 0.15,
                PatternType.PERFORMANCE_HINT: 0.1
            }
            
            weighted_confidence = 0.0
            total_weight = 0.0
            
            for match in matches:
                weight = type_weights.get(match.pattern_type, 0.1)
                weighted_confidence += match.confidence * weight
                total_weight += weight
            
            if total_weight == 0:
                return 0.0
            
            return min(weighted_confidence / total_weight, 1.0)
            
        except Exception as e:
            print(f"Warning: Error calculating confidence score: {e}")
            return 0.0
    
    def _get_recommended_modes(self, matches: List[PatternMatch], complexity_score: float) -> List[str]:
        """Get recommended modes based on detected patterns with configuration support."""
        modes = set()
        
        try:
            # Add modes from pattern matches
            for match in matches:
                if match.pattern_type == PatternType.MODE_TRIGGER:
                    # Only add if confidence threshold is met
                    mode_config = self.mode_configs.get(match.pattern_name, {})
                    threshold = mode_config.get('confidence_threshold', 0.7)
                    if match.confidence >= threshold:
                        modes.add(match.pattern_name)
            
            # Auto-activate modes based on complexity with configurable thresholds
            auto_activation = self.mcp_patterns.get('auto_activation', {})
            complexity_thresholds = auto_activation.get('complexity_thresholds', {})
            
            # Task management auto-activation
            task_mgmt_threshold = complexity_thresholds.get('enable_delegation', {}).get('complexity_score', 0.4)
            if complexity_score >= task_mgmt_threshold:
                modes.add("task_management")
            
            # Sequential analysis auto-activation
            sequential_threshold = complexity_thresholds.get('enable_sequential', {}).get('complexity_score', 0.6)
            if complexity_score >= sequential_threshold:
                # Don't add sequential as a mode, but note it for MCP server selection
                pass
            
        except Exception as e:
            print(f"Warning: Error getting recommended modes: {e}")
        
        return list(modes)
    
    def _get_recommended_mcp_servers(self, matches: List[PatternMatch], context: Dict[str, Any]) -> List[str]:
        """Get recommended MCP servers based on detected patterns with priority handling."""
        servers = {}  # Use dict to track server priorities
        
        try:
            for match in matches:
                if match.pattern_type == PatternType.MCP_SERVER:
                    server_config = match.metadata.get('server_config', {})
                    priority = server_config.get('priority', 'medium')
                    
                    # Assign numeric priority for sorting
                    priority_value = {'high': 3, 'medium': 2, 'low': 1}.get(priority, 2)
                    
                    if match.pattern_name not in servers or servers[match.pattern_name]['priority'] < priority_value:
                        servers[match.pattern_name] = {
                            'priority': priority_value,
                            'confidence': match.confidence
                        }
            
            # Sort servers by priority, then by confidence
            sorted_servers = sorted(
                servers.items(),
                key=lambda x: (x[1]['priority'], x[1]['confidence']),
                reverse=True
            )
            
            return [server[0] for server in sorted_servers]
            
        except Exception as e:
            print(f"Warning: Error getting recommended MCP servers: {e}")
            return []
    
    def _get_suggested_flags(self, matches: List[PatternMatch], complexity_score: float, context: Dict[str, Any]) -> List[str]:
        """Get suggested flags based on patterns and complexity with configuration support."""
        flags = []
        
        try:
            # Get auto-activation configuration
            auto_activation = self.mcp_patterns.get('auto_activation', {})
            complexity_thresholds = auto_activation.get('complexity_thresholds', {})
            
            # Mode-specific flags
            mode_flags = {
                'brainstorming': ['--brainstorm'],
                'task_management': ['--delegate', '--wave-mode'],
                'token_efficiency': ['--uc'],
                'introspection': ['--introspect']
            }
            
            # Add flags based on detected modes
            for match in matches:
                if match.pattern_type == PatternType.MODE_TRIGGER:
                    mode_name = match.pattern_name
                    if mode_name in mode_flags:
                        flags.extend(mode_flags[mode_name])
            
            # MCP server-specific flags (thinking flags based on server matches)
            mcp_thinking_flags = {
                'sequential': '--think',
                'serena': '--think-hard'
            }
            
            # Add thinking flags based on MCP server matches
            for match in matches:
                if match.pattern_type == PatternType.MCP_SERVER:
                    server_name = match.pattern_name
                    if server_name in mcp_thinking_flags:
                        thinking_flag = mcp_thinking_flags[server_name]
                        if thinking_flag not in flags:
                            flags.append(thinking_flag)
            
            # Check for performance analysis patterns (special case for think-hard)
            for match in matches:
                if match.pattern_type == PatternType.MCP_SERVER and match.pattern_name == 'sequential':
                    matched_text = match.matched_text.lower()
                    if 'performance' in matched_text or 'bottleneck' in matched_text or 'bundle' in matched_text:
                        # Replace --think with --think-hard for performance analysis
                        if '--think' in flags:
                            flags.remove('--think')
                        if '--think-hard' not in flags:
                            flags.append('--think-hard')
            
            # Thinking flags based on complexity with configurable thresholds
            sequential_config = complexity_thresholds.get('enable_sequential', {})
            sequential_threshold = sequential_config.get('complexity_score', 0.6)
            
            # Only add complexity-based thinking flags if no MCP-based flags were added
            if not any(flag.startswith('--think') for flag in flags):
                if complexity_score >= 0.8:
                    flags.append("--ultrathink")
                elif complexity_score >= sequential_threshold:
                    flags.append("--think-hard")
                elif complexity_score >= 0.3:
                    flags.append("--think")
            
            # Delegation flags from pattern matches
            delegation_recommended = False
            for match in matches:
                if match.metadata.get("delegation_recommended"):
                    delegation_recommended = True
                    break
            
            if delegation_recommended and "--delegate" not in flags:
                flags.append("--delegate")
            
            # Efficiency flags based on patterns and context
            efficiency_needed = False
            resource_usage = context.get('resource_usage_percent', 0)
            
            for match in matches:
                if match.metadata.get("compression_needed"):
                    efficiency_needed = True
                    break
            
            # Check resource thresholds from configuration
            resource_mgmt = self.mcp_patterns.get('performance_optimization', {}).get('resource_management', {})
            token_threshold = resource_mgmt.get('token_threshold_percent', 75)
            
            if (efficiency_needed or resource_usage > token_threshold) and "--uc" not in flags:
                flags.append("--uc")
            
            # Validation flags for high-risk operations
            validation_config = complexity_thresholds.get('enable_validation', {})
            is_production = context.get('is_production', False)
            risk_level = context.get('risk_level', 'low')
            
            validation_needed = (
                complexity_score > 0.7 or 
                is_production or 
                risk_level in validation_config.get('risk_level', ['high', 'critical'])
            )
            
            if validation_needed:
                flags.append("--validate")
            
        except Exception as e:
            print(f"Warning: Error getting suggested flags: {e}")
        
        return flags
    
    def validate_input(self, user_input: str, context: Dict[str, Any], operation_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate input parameters for pattern detection."""
        try:
            # Validate user_input
            if not isinstance(user_input, str):
                return False, "user_input must be a string"
            
            if len(user_input.strip()) == 0:
                return False, "user_input cannot be empty"
            
            # Validate context
            if not isinstance(context, dict):
                return False, "context must be a dictionary"
            
            # Validate operation_data
            if not isinstance(operation_data, dict):
                return False, "operation_data must be a dictionary" 
            
            # Validate numeric values in context
            resource_usage = context.get('resource_usage_percent', 0)
            if not isinstance(resource_usage, (int, float)) or not (0 <= resource_usage <= 100):
                context['resource_usage_percent'] = 0
            
            # Validate numeric values in operation_data
            file_count = operation_data.get('file_count', 1)
            if not isinstance(file_count, int) or file_count < 0:
                operation_data['file_count'] = 1
            
            complexity_score = operation_data.get('complexity_score', 0.0)
            if not isinstance(complexity_score, (int, float)) or not (0 <= complexity_score <= 1):
                operation_data['complexity_score'] = 0.0
            
            return True, "Input validation passed"
            
        except Exception as e:
            return False, f"Input validation error: {e}"
    
    def get_pattern_statistics(self) -> Dict[str, Any]:
        """Get statistics about compiled patterns for debugging."""
        try:
            stats = {
                'total_patterns': len(self.compiled_patterns),
                'mode_patterns': len([k for k in self.compiled_patterns.keys() if k.startswith('mode_')]),
                'mcp_patterns': len([k for k in self.compiled_patterns.keys() if k.startswith('mcp_')]),
                'mode_configs_loaded': len(self.mode_configs),
                'mcp_configs_loaded': len(self.mcp_configs),
                'pattern_details': {}
            }
            
            # Detailed pattern statistics
            for pattern_key, compiled_patterns in self.compiled_patterns.items():
                stats['pattern_details'][pattern_key] = {
                    'pattern_count': len(compiled_patterns),
                    'patterns': [p.pattern for p in compiled_patterns]
                }
            
            return stats
            
        except Exception as e:
            return {'error': f"Failed to generate pattern statistics: {e}"}
    
    def reset_patterns(self):
        """Reset and reload all patterns from configuration."""
        try:
            self.__init__()
            return True
        except Exception as e:
            print(f"Warning: Failed to reset patterns: {e}")
            return False