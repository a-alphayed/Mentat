"""
Intelligence Engine for SuperClaude Framework-Hooks

Generic YAML pattern interpreter that provides intelligent services by consuming
declarative YAML patterns. Enables hot-reloadable intelligence without code changes.
"""

import time
import hashlib
from typing import Dict, Any, List, Optional, Tuple, Union
from pathlib import Path
from yaml_loader import config_loader


class IntelligenceEngine:
    """
    Generic YAML pattern interpreter for declarative intelligence.
    
    Features:
    - Hot-reload YAML intelligence patterns
    - Context-aware pattern matching
    - Decision tree execution
    - Recommendation generation
    - Performance optimization
    - Multi-pattern coordination
    """
    
    def __init__(self):
        self.patterns: Dict[str, Dict[str, Any]] = {}
        self.pattern_cache: Dict[str, Any] = {}
        self.pattern_timestamps: Dict[str, float] = {}
        self.evaluation_cache: Dict[str, Tuple[Any, float]] = {}
        self.cache_duration = 300  # 5 minutes
        
        self._load_all_patterns()
    
    def _load_all_patterns(self):
        """Load all intelligence pattern configurations."""
        pattern_files = [
            'intelligence_patterns',
            'mcp_orchestration', 
            'hook_coordination',
            'performance_intelligence',
            'validation_intelligence',
            'user_experience'
        ]
        
        for pattern_file in pattern_files:
            try:
                patterns = config_loader.load_config(pattern_file)
                self.patterns[pattern_file] = patterns
                self.pattern_timestamps[pattern_file] = time.time()
            except Exception as e:
                print(f"Warning: Could not load {pattern_file} patterns: {e}")
                self.patterns[pattern_file] = {}
    
    def reload_patterns(self, force: bool = False) -> bool:
        """
        Reload patterns if they have changed.
        
        Args:
            force: Force reload even if no changes detected
            
        Returns:
            True if patterns were reloaded
        """
        reloaded = False
        
        for pattern_file in self.patterns.keys():
            try:
                # Force reload or check for changes
                if force:
                    patterns = config_loader.load_config(pattern_file, force_reload=True)
                    self.patterns[pattern_file] = patterns
                    self.pattern_timestamps[pattern_file] = time.time()
                    reloaded = True
                else:
                    # Check if pattern file has been updated
                    current_patterns = config_loader.load_config(pattern_file)
                    pattern_hash = self._compute_pattern_hash(current_patterns)
                    cached_hash = self.pattern_cache.get(f"{pattern_file}_hash")
                    
                    if pattern_hash != cached_hash:
                        self.patterns[pattern_file] = current_patterns
                        self.pattern_cache[f"{pattern_file}_hash"] = pattern_hash
                        self.pattern_timestamps[pattern_file] = time.time()
                        reloaded = True
                        
            except Exception as e:
                print(f"Warning: Could not reload {pattern_file} patterns: {e}")
        
        if reloaded:
            # Clear evaluation cache when patterns change
            self.evaluation_cache.clear()
        
        return reloaded
    
    def _compute_pattern_hash(self, patterns: Dict[str, Any]) -> str:
        """Compute hash of pattern configuration for change detection."""
        pattern_str = str(sorted(patterns.items()))
        return hashlib.md5(pattern_str.encode()).hexdigest()
    
    def evaluate_context(self, context: Dict[str, Any], pattern_type: str) -> Dict[str, Any]:
        """
        Evaluate context against patterns to generate recommendations.
        
        Args:
            context: Current operation context
            pattern_type: Type of patterns to evaluate (e.g., 'mcp_orchestration')
            
        Returns:
            Dictionary with recommendations and metadata
        """
        # Check cache first
        cache_key = f"{pattern_type}_{self._compute_context_hash(context)}"
        if cache_key in self.evaluation_cache:
            result, timestamp = self.evaluation_cache[cache_key]
            if time.time() - timestamp < self.cache_duration:
                return result
        
        # Hot-reload patterns if needed
        self.reload_patterns()
        
        # Get patterns for this type
        patterns = self.patterns.get(pattern_type, {})
        if not patterns:
            return {'recommendations': {}, 'confidence': 0.0, 'source': 'no_patterns'}
        
        # Evaluate patterns
        recommendations = {}
        confidence_scores = []
        
        if pattern_type == 'mcp_orchestration':
            recommendations = self._evaluate_mcp_patterns(context, patterns)
        elif pattern_type == 'hook_coordination':
            recommendations = self._evaluate_hook_patterns(context, patterns)
        elif pattern_type == 'performance_intelligence':
            recommendations = self._evaluate_performance_patterns(context, patterns)
        elif pattern_type == 'validation_intelligence':
            recommendations = self._evaluate_validation_patterns(context, patterns)
        elif pattern_type == 'user_experience':
            recommendations = self._evaluate_ux_patterns(context, patterns)
        elif pattern_type == 'intelligence_patterns':
            recommendations = self._evaluate_learning_patterns(context, patterns)
        
        # Calculate overall confidence
        overall_confidence = max(confidence_scores) if confidence_scores else 0.0
        
        result = {
            'recommendations': recommendations,
            'confidence': overall_confidence,
            'source': pattern_type,
            'timestamp': time.time()
        }
        
        # Cache result
        self.evaluation_cache[cache_key] = (result, time.time())
        
        return result
    
    def _compute_context_hash(self, context: Dict[str, Any]) -> str:
        """Compute hash of context for caching."""
        context_str = str(sorted(context.items()))
        return hashlib.md5(context_str.encode()).hexdigest()[:8]
    
    def _evaluate_mcp_patterns(self, context: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate MCP orchestration patterns."""
        server_selection = patterns.get('server_selection', {})
        decision_tree = server_selection.get('decision_tree', [])
        
        recommendations = {
            'primary_server': None,
            'support_servers': [],
            'coordination_mode': 'sequential',
            'confidence': 0.0
        }
        
        # Evaluate decision tree
        for rule in decision_tree:
            if self._matches_conditions(context, rule.get('conditions', {})):
                recommendations['primary_server'] = rule.get('primary_server')
                recommendations['support_servers'] = rule.get('support_servers', [])
                recommendations['coordination_mode'] = rule.get('coordination_mode', 'sequential')
                recommendations['confidence'] = rule.get('confidence', 0.5)
                break
        
        # Apply fallback if no match
        if not recommendations['primary_server']:
            fallback = server_selection.get('fallback_chain', {})
            recommendations['primary_server'] = fallback.get('default_primary', 'sequential')
            recommendations['confidence'] = 0.3
        
        return recommendations
    
    def _evaluate_hook_patterns(self, context: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate hook coordination patterns."""
        execution_patterns = patterns.get('execution_patterns', {})
        
        recommendations = {
            'execution_strategy': 'sequential',
            'parallel_groups': [],
            'conditional_hooks': [],
            'performance_optimizations': []
        }
        
        # Check for parallel execution opportunities
        parallel_groups = execution_patterns.get('parallel_execution', {}).get('groups', [])
        for group in parallel_groups:
            if self._should_enable_parallel_group(context, group):
                recommendations['parallel_groups'].append(group)
        
        # Check conditional execution rules
        conditional_rules = execution_patterns.get('conditional_execution', {}).get('rules', [])
        for rule in conditional_rules:
            if self._matches_conditions(context, rule.get('conditions', [])):
                recommendations['conditional_hooks'].append({
                    'hook': rule.get('hook'),
                    'priority': rule.get('priority', 'medium')
                })
        
        return recommendations
    
    def _evaluate_performance_patterns(self, context: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate performance intelligence patterns."""
        auto_optimization = patterns.get('auto_optimization', {})
        optimization_triggers = auto_optimization.get('optimization_triggers', [])
        
        recommendations = {
            'optimizations': [],
            'resource_zone': 'green',
            'performance_actions': []
        }
        
        # Check optimization triggers
        for trigger in optimization_triggers:
            if self._matches_conditions(context, trigger.get('condition', {})):
                recommendations['optimizations'].extend(trigger.get('actions', []))
                recommendations['performance_actions'].append({
                    'trigger': trigger.get('name'),
                    'urgency': trigger.get('urgency', 'medium')
                })
        
        # Determine resource zone
        resource_usage = context.get('resource_usage', 0.5)
        resource_zones = patterns.get('resource_management', {}).get('resource_zones', {})
        
        for zone_name, zone_config in resource_zones.items():
            threshold = zone_config.get('threshold', 1.0)
            if resource_usage <= threshold:
                recommendations['resource_zone'] = zone_name
                break
        
        return recommendations
    
    def _evaluate_validation_patterns(self, context: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate validation intelligence patterns."""
        proactive_diagnostics = patterns.get('proactive_diagnostics', {})
        early_warnings = proactive_diagnostics.get('early_warning_patterns', {})
        
        recommendations = {
            'health_score': 1.0,
            'warnings': [],
            'diagnostics': [],
            'remediation_suggestions': []
        }
        
        # Check early warning patterns
        for category, warnings in early_warnings.items():
            for warning in warnings:
                if self._matches_conditions(context, warning.get('pattern', {})):
                    recommendations['warnings'].append({
                        'name': warning.get('name'),
                        'severity': warning.get('severity', 'medium'),
                        'recommendation': warning.get('recommendation'),
                        'category': category
                    })
        
        # Calculate health score (simplified)
        base_health = 1.0
        for warning in recommendations['warnings']:
            severity_impact = {'low': 0.05, 'medium': 0.1, 'high': 0.2, 'critical': 0.4}
            base_health -= severity_impact.get(warning['severity'], 0.1)
        
        recommendations['health_score'] = max(0.0, base_health)
        
        return recommendations
    
    def _evaluate_ux_patterns(self, context: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate user experience patterns."""
        project_detection = patterns.get('project_detection', {})
        detection_patterns = project_detection.get('detection_patterns', {})
        
        recommendations = {
            'project_type': 'unknown',
            'suggested_servers': [],
            'smart_defaults': {},
            'user_suggestions': []
        }
        
        # Detect project type
        file_indicators = context.get('file_indicators', [])
        directory_indicators = context.get('directory_indicators', [])
        
        for category, projects in detection_patterns.items():
            for project_type, project_config in projects.items():
                if self._matches_project_indicators(file_indicators, directory_indicators, project_config):
                    recommendations['project_type'] = project_type
                    project_recs = project_config.get('recommendations', {})
                    recommendations['suggested_servers'] = project_recs.get('mcp_servers', [])
                    recommendations['smart_defaults'] = project_recs
                    break
        
        return recommendations
    
    def _evaluate_learning_patterns(self, context: Dict[str, Any], patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate learning intelligence patterns."""
        learning_intelligence = patterns.get('learning_intelligence', {})
        pattern_recognition = learning_intelligence.get('pattern_recognition', {})
        
        recommendations = {
            'pattern_dimensions': [],
            'learning_strategy': 'standard',
            'confidence_threshold': 0.7
        }
        
        # Get pattern dimensions
        dimensions = pattern_recognition.get('dimensions', {})
        recommendations['pattern_dimensions'] = dimensions.get('primary', []) + dimensions.get('secondary', [])
        
        # Determine learning strategy based on context
        complexity = context.get('complexity_score', 0.5)
        if complexity > 0.8:
            recommendations['learning_strategy'] = 'comprehensive'
        elif complexity < 0.3:
            recommendations['learning_strategy'] = 'lightweight'
        
        return recommendations
    
    def _matches_conditions(self, context: Dict[str, Any], conditions: Union[Dict, List]) -> bool:
        """Check if context matches pattern conditions."""
        if isinstance(conditions, list):
            # List of conditions (AND logic)
            return all(self._matches_single_condition(context, cond) for cond in conditions)
        elif isinstance(conditions, dict):
            if 'AND' in conditions:
                return all(self._matches_single_condition(context, cond) for cond in conditions['AND'])
            elif 'OR' in conditions:
                return any(self._matches_single_condition(context, cond) for cond in conditions['OR'])
            else:
                return self._matches_single_condition(context, conditions)
        return False
    
    def _matches_single_condition(self, context: Dict[str, Any], condition: Dict[str, Any]) -> bool:
        """Check if context matches a single condition."""
        for key, expected_value in condition.items():
            context_value = context.get(key)
            
            if context_value is None:
                return False
            
            # Handle string operations
            if isinstance(expected_value, str):
                if expected_value.startswith('>'):
                    threshold = float(expected_value[1:])
                    return float(context_value) > threshold
                elif expected_value.startswith('<'):
                    threshold = float(expected_value[1:])
                    return float(context_value) < threshold
                elif isinstance(expected_value, list):
                    return context_value in expected_value
                else:
                    return context_value == expected_value
            elif isinstance(expected_value, list):
                return context_value in expected_value
            else:
                return context_value == expected_value
        
        return True
    
    def _should_enable_parallel_group(self, context: Dict[str, Any], group: Dict[str, Any]) -> bool:
        """Determine if a parallel group should be enabled."""
        # Simple heuristic: enable if not in resource-constrained environment
        resource_usage = context.get('resource_usage', 0.5)
        return resource_usage < 0.8 and context.get('complexity_score', 0.5) > 0.3
    
    def _matches_project_indicators(self, files: List[str], dirs: List[str], 
                                  project_config: Dict[str, Any]) -> bool:
        """Check if file/directory indicators match project pattern."""
        file_indicators = project_config.get('file_indicators', [])
        dir_indicators = project_config.get('directory_indicators', [])
        
        file_matches = sum(1 for indicator in file_indicators if any(indicator in f for f in files))
        dir_matches = sum(1 for indicator in dir_indicators if any(indicator in d for d in dirs))
        
        confidence_threshold = project_config.get('confidence_threshold', 0.8)
        total_indicators = len(file_indicators) + len(dir_indicators)
        
        if total_indicators == 0:
            return False
        
        match_ratio = (file_matches + dir_matches) / total_indicators
        return match_ratio >= confidence_threshold
    
    def get_intelligence_summary(self) -> Dict[str, Any]:
        """Get summary of current intelligence state."""
        return {
            'loaded_patterns': list(self.patterns.keys()),
            'cache_entries': len(self.evaluation_cache),
            'last_reload': max(self.pattern_timestamps.values()) if self.pattern_timestamps else 0,
            'pattern_status': {name: 'loaded' for name in self.patterns.keys()}
        }