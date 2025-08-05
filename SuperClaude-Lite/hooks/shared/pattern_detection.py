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
        self.patterns = config_loader.load_config('modes')
        self.mcp_patterns = config_loader.load_config('orchestrator')
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for efficient matching."""
        self.compiled_patterns = {}
        
        # Mode detection patterns
        for mode_name, mode_config in self.patterns.get('mode_detection', {}).items():
            patterns = mode_config.get('trigger_patterns', [])
            self.compiled_patterns[f"mode_{mode_name}"] = [
                re.compile(pattern, re.IGNORECASE) for pattern in patterns
            ]
        
        # MCP server patterns
        for server_name, server_config in self.mcp_patterns.get('routing_patterns', {}).items():
            triggers = server_config.get('triggers', [])
            self.compiled_patterns[f"mcp_{server_name}"] = [
                re.compile(trigger, re.IGNORECASE) for trigger in triggers
            ]
    
    def detect_patterns(self, 
                       user_input: str, 
                       context: Dict[str, Any], 
                       operation_data: Dict[str, Any]) -> DetectionResult:
        """
        Perform comprehensive pattern detection.
        
        Args:
            user_input: User's request or command
            context: Session and environment context
            operation_data: Information about the planned operation
            
        Returns:
            DetectionResult with all detected patterns and recommendations
        """
        matches = []
        
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
    
    def _detect_mode_patterns(self, user_input: str, context: Dict[str, Any]) -> List[PatternMatch]:
        """Detect which SuperClaude modes should be activated."""
        matches = []
        
        # Brainstorming mode detection
        brainstorm_indicators = [
            r"(?:i want to|thinking about|not sure|maybe|could we)\s+(?:build|create|make)",
            r"(?:brainstorm|explore|figure out|discuss)",
            r"(?:new project|startup idea|feature concept)",
            r"(?:ambiguous|uncertain|unclear)\s+(?:requirements|needs)"
        ]
        
        for pattern in brainstorm_indicators:
            if re.search(pattern, user_input, re.IGNORECASE):
                matches.append(PatternMatch(
                    pattern_type=PatternType.MODE_TRIGGER,
                    pattern_name="brainstorming",
                    confidence=0.8,
                    matched_text=re.search(pattern, user_input, re.IGNORECASE).group(),
                    suggestions=["Enable brainstorming mode for requirements discovery"],
                    metadata={"mode": "brainstorming", "auto_activate": True}
                ))
                break
        
        # Task management mode detection
        task_management_indicators = [
            r"(?:multiple|many|several)\s+(?:tasks|files|components)",
            r"(?:build|implement|create)\s+(?:system|feature|application)",
            r"(?:complex|comprehensive|large-scale)",
            r"(?:manage|coordinate|orchestrate)\s+(?:work|tasks|operations)"
        ]
        
        for pattern in task_management_indicators:
            if re.search(pattern, user_input, re.IGNORECASE):
                matches.append(PatternMatch(
                    pattern_type=PatternType.MODE_TRIGGER,
                    pattern_name="task_management",
                    confidence=0.7,
                    matched_text=re.search(pattern, user_input, re.IGNORECASE).group(),
                    suggestions=["Enable task management for complex operations"],
                    metadata={"mode": "task_management", "delegation_likely": True}
                ))
                break
        
        # Token efficiency mode detection
        efficiency_indicators = [
            r"(?:brief|concise|compressed|short)",
            r"(?:token|resource|memory)\s+(?:limit|constraint|optimization)",
            r"(?:efficient|optimized|minimal)\s+(?:output|response)"
        ]
        
        for pattern in efficiency_indicators:
            if re.search(pattern, user_input, re.IGNORECASE):
                matches.append(PatternMatch(
                    pattern_type=PatternType.MODE_TRIGGER,
                    pattern_name="token_efficiency",
                    confidence=0.9,
                    matched_text=re.search(pattern, user_input, re.IGNORECASE).group(),
                    suggestions=["Enable token efficiency mode"],
                    metadata={"mode": "token_efficiency", "compression_needed": True}
                ))
                break
        
        # Check resource usage for automatic efficiency mode
        resource_usage = context.get('resource_usage_percent', 0)
        if resource_usage > 75:
            matches.append(PatternMatch(
                pattern_type=PatternType.MODE_TRIGGER,
                pattern_name="token_efficiency",
                confidence=0.85,
                matched_text="high_resource_usage",
                suggestions=["Auto-enable token efficiency due to resource constraints"],
                metadata={"mode": "token_efficiency", "trigger": "resource_constraint"}
            ))
        
        return matches
    
    def _detect_mcp_patterns(self, user_input: str, context: Dict[str, Any], operation_data: Dict[str, Any]) -> List[PatternMatch]:
        """Detect which MCP servers should be activated."""
        matches = []
        
        # Context7 (library documentation)
        context7_patterns = [
            r"(?:library|framework|package)\s+(?:documentation|docs|patterns)",
            r"(?:react|vue|angular|express|django|flask)",
            r"(?:import|require|install|dependency)",
            r"(?:official|standard|best practice)\s+(?:way|pattern|approach)"
        ]
        
        for pattern in context7_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                matches.append(PatternMatch(
                    pattern_type=PatternType.MCP_SERVER,
                    pattern_name="context7",
                    confidence=0.8,
                    matched_text=re.search(pattern, user_input, re.IGNORECASE).group(),
                    suggestions=["Enable Context7 for library documentation"],
                    metadata={"mcp_server": "context7", "focus": "documentation"}
                ))
                break
        
        # Sequential (complex analysis)
        sequential_patterns = [
            r"(?:analyze|debug|troubleshoot|investigate)",
            r"(?:complex|complicated|multi-step|systematic)",
            r"(?:architecture|system|design)\s+(?:review|analysis)",
            r"(?:root cause|performance|bottleneck)"
        ]
        
        for pattern in sequential_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                matches.append(PatternMatch(
                    pattern_type=PatternType.MCP_SERVER,
                    pattern_name="sequential",
                    confidence=0.75,
                    matched_text=re.search(pattern, user_input, re.IGNORECASE).group(),
                    suggestions=["Enable Sequential for multi-step analysis"],
                    metadata={"mcp_server": "sequential", "analysis_type": "complex"}
                ))
                break
        
        # Magic (UI components)
        magic_patterns = [
            r"(?:component|button|form|modal|dialog)",
            r"(?:ui|frontend|interface|design)",
            r"(?:react|vue|angular)\s+(?:component|element)",
            r"(?:responsive|mobile|accessibility)"
        ]
        
        for pattern in magic_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                matches.append(PatternMatch(
                    pattern_type=PatternType.MCP_SERVER,
                    pattern_name="magic",
                    confidence=0.85,
                    matched_text=re.search(pattern, user_input, re.IGNORECASE).group(),
                    suggestions=["Enable Magic for UI component generation"],
                    metadata={"mcp_server": "magic", "component_type": "ui"}
                ))
                break
        
        # Playwright (testing)
        playwright_patterns = [
            r"(?:test|testing|e2e|end-to-end)",
            r"(?:browser|cross-browser|automation)",
            r"(?:performance|visual|regression)\s+(?:test|testing)",
            r"(?:validate|verify|check)\s+(?:functionality|behavior)"
        ]
        
        for pattern in playwright_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                matches.append(PatternMatch(
                    pattern_type=PatternType.MCP_SERVER,
                    pattern_name="playwright",
                    confidence=0.8,
                    matched_text=re.search(pattern, user_input, re.IGNORECASE).group(),
                    suggestions=["Enable Playwright for testing operations"],
                    metadata={"mcp_server": "playwright", "test_type": "e2e"}
                ))
                break
        
        # Morphllm vs Serena intelligence selection
        file_count = operation_data.get('file_count', 1)
        complexity = operation_data.get('complexity_score', 0.0)
        
        if file_count > 10 or complexity > 0.6:
            matches.append(PatternMatch(
                pattern_type=PatternType.MCP_SERVER,
                pattern_name="serena",
                confidence=0.9,
                matched_text="high_complexity_operation",
                suggestions=["Use Serena for complex multi-file operations"],
                metadata={"mcp_server": "serena", "reason": "complexity_threshold"}
            ))
        elif file_count <= 10 and complexity <= 0.6:
            matches.append(PatternMatch(
                pattern_type=PatternType.MCP_SERVER,
                pattern_name="morphllm",
                confidence=0.8,
                matched_text="moderate_complexity_operation",
                suggestions=["Use Morphllm for efficient editing operations"],
                metadata={"mcp_server": "morphllm", "reason": "efficiency_optimized"}
            ))
        
        return matches
    
    def _detect_complexity_patterns(self, user_input: str, operation_data: Dict[str, Any]) -> List[PatternMatch]:
        """Detect complexity indicators in the request."""
        matches = []
        
        # High complexity indicators
        high_complexity_patterns = [
            r"(?:entire|whole|complete)\s+(?:codebase|system|application)",
            r"(?:refactor|migrate|restructure)\s+(?:all|everything|entire)",
            r"(?:architecture|system-wide|comprehensive)\s+(?:change|update|redesign)",
            r"(?:complex|complicated|sophisticated)\s+(?:logic|algorithm|system)"
        ]
        
        for pattern in high_complexity_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                matches.append(PatternMatch(
                    pattern_type=PatternType.COMPLEXITY_INDICATOR,
                    pattern_name="high_complexity",
                    confidence=0.8,
                    matched_text=re.search(pattern, user_input, re.IGNORECASE).group(),
                    suggestions=["Consider delegation and thinking modes"],
                    metadata={"complexity_level": "high", "score_boost": 0.3}
                ))
                break
        
        # File count indicators
        file_count = operation_data.get('file_count', 1)
        if file_count > 5:
            matches.append(PatternMatch(
                pattern_type=PatternType.COMPLEXITY_INDICATOR,
                pattern_name="multi_file_operation",
                confidence=0.9,
                matched_text=f"{file_count}_files",
                suggestions=["Enable delegation for multi-file operations"],
                metadata={"file_count": file_count, "delegation_recommended": True}
            ))
        
        return matches
    
    def _detect_persona_patterns(self, user_input: str, context: Dict[str, Any]) -> List[PatternMatch]:
        """Detect hints about which persona should be active."""
        matches = []
        
        persona_patterns = {
            "architect": [r"(?:architecture|design|structure|system)\s+(?:review|analysis|planning)"],
            "performance": [r"(?:performance|optimization|speed|efficiency|bottleneck)"],
            "security": [r"(?:security|vulnerability|audit|secure|safety)"],
            "frontend": [r"(?:ui|frontend|interface|component|design|responsive)"],
            "backend": [r"(?:api|server|database|backend|service)"],
            "devops": [r"(?:deploy|deployment|ci|cd|infrastructure|docker|kubernetes)"],
            "testing": [r"(?:test|testing|qa|quality|coverage|validation)"]
        }
        
        for persona, patterns in persona_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    matches.append(PatternMatch(
                        pattern_type=PatternType.PERSONA_HINT,
                        pattern_name=persona,
                        confidence=0.7,
                        matched_text=re.search(pattern, user_input, re.IGNORECASE).group(),
                        suggestions=[f"Consider {persona} persona for specialized expertise"],
                        metadata={"persona": persona, "domain_specific": True}
                    ))
                    break
        
        return matches
    
    def _calculate_complexity_score(self, matches: List[PatternMatch], operation_data: Dict[str, Any]) -> float:
        """Calculate overall complexity score from detected patterns."""
        base_score = operation_data.get('complexity_score', 0.0)
        
        # Add complexity from pattern matches
        for match in matches:
            if match.pattern_type == PatternType.COMPLEXITY_INDICATOR:
                score_boost = match.metadata.get('score_boost', 0.1)
                base_score += score_boost
        
        return min(base_score, 1.0)
    
    def _calculate_confidence_score(self, matches: List[PatternMatch]) -> float:
        """Calculate overall confidence in pattern detection."""
        if not matches:
            return 0.0
        
        total_confidence = sum(match.confidence for match in matches)
        return min(total_confidence / len(matches), 1.0)
    
    def _get_recommended_modes(self, matches: List[PatternMatch], complexity_score: float) -> List[str]:
        """Get recommended modes based on detected patterns."""
        modes = set()
        
        for match in matches:
            if match.pattern_type == PatternType.MODE_TRIGGER:
                modes.add(match.pattern_name)
        
        # Auto-activate based on complexity
        if complexity_score > 0.6:
            modes.add("task_management")
        
        return list(modes)
    
    def _get_recommended_mcp_servers(self, matches: List[PatternMatch], context: Dict[str, Any]) -> List[str]:
        """Get recommended MCP servers based on detected patterns."""
        servers = set()
        
        for match in matches:
            if match.pattern_type == PatternType.MCP_SERVER:
                servers.add(match.pattern_name)
        
        return list(servers)
    
    def _get_suggested_flags(self, matches: List[PatternMatch], complexity_score: float, context: Dict[str, Any]) -> List[str]:
        """Get suggested flags based on patterns and complexity."""
        flags = []
        
        # Thinking flags based on complexity
        if complexity_score >= 0.8:
            flags.append("--ultrathink")
        elif complexity_score >= 0.6:
            flags.append("--think-hard")
        elif complexity_score >= 0.3:
            flags.append("--think")
        
        # Delegation flags
        for match in matches:
            if match.metadata.get("delegation_recommended"):
                flags.append("--delegate auto")
                break
        
        # Efficiency flags
        for match in matches:
            if match.metadata.get("compression_needed") or context.get('resource_usage_percent', 0) > 75:
                flags.append("--uc")
                break
        
        # Validation flags for high-risk operations
        if complexity_score > 0.7 or context.get('is_production', False):
            flags.append("--validate")
        
        return flags