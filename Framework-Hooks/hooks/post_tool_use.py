#!/usr/bin/env python3
"""
SuperClaude-Lite Post-Tool-Use Hook

Implements RULES.md + PRINCIPLES.md validation and learning system.
Performance target: <100ms execution time.

This hook runs after every tool usage and provides:
- Quality validation against SuperClaude principles
- Effectiveness measurement and learning
- Error pattern detection and prevention
- Performance optimization feedback
- Adaptation and improvement recommendations
"""

import sys
import json
import time
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Add shared modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "shared"))

from framework_logic import FrameworkLogic, ValidationResult, OperationContext, OperationType, RiskLevel
from pattern_detection import PatternDetector
from mcp_intelligence import MCPIntelligence
from compression_engine import CompressionEngine
from learning_engine import LearningEngine, LearningType, AdaptationScope
from yaml_loader import config_loader
from logger import log_hook_start, log_hook_end, log_decision, log_error


class PostToolUseHook:
    """
    Post-tool-use hook implementing SuperClaude validation and learning.
    
    Responsibilities:
    - Validate tool execution against RULES.md and PRINCIPLES.md
    - Measure operation effectiveness and quality
    - Learn from successful and failed patterns
    - Detect error patterns and suggest improvements
    - Record performance metrics for optimization
    - Generate adaptation recommendations
    """
    
    def __init__(self):
        start_time = time.time()
        
        # Initialize core components
        self.framework_logic = FrameworkLogic()
        self.pattern_detector = PatternDetector()
        self.mcp_intelligence = MCPIntelligence()
        self.compression_engine = CompressionEngine()
        
        # Initialize learning engine with installation directory cache
        import os
        cache_dir = Path(os.path.expanduser("~/.claude/cache"))
        cache_dir.mkdir(parents=True, exist_ok=True)
        self.learning_engine = LearningEngine(cache_dir)
        
        # Load hook-specific configuration from SuperClaude config
        self.hook_config = config_loader.get_hook_config('post_tool_use')
        
        # Load validation configuration (from YAML if exists, otherwise use hook config)
        try:
            self.validation_config = config_loader.load_config('validation')
        except FileNotFoundError:
            # Fall back to hook configuration if YAML file not found
            self.validation_config = self.hook_config.get('configuration', {})
        
        # Load quality standards (from YAML if exists, otherwise use hook config)
        try:
            self.quality_standards = config_loader.load_config('performance')
        except FileNotFoundError:
            # Fall back to performance targets from global configuration
            self.quality_standards = config_loader.get_performance_targets()
        
        # Performance tracking using configuration
        self.initialization_time = (time.time() - start_time) * 1000
        self.performance_target_ms = config_loader.get_hook_config('post_tool_use', 'performance_target_ms', 100)
        
    def process_tool_result(self, tool_result: dict) -> dict:
        """
        Process tool execution result with validation and learning.
        
        Args:
            tool_result: Tool execution result from Claude Code
            
        Returns:
            Enhanced result with SuperClaude validation and insights
        """
        start_time = time.time()
        
        # Log hook start
        log_hook_start("post_tool_use", {
            "tool_name": tool_result.get('tool_name', 'unknown'),
            "success": tool_result.get('success', False),
            "has_error": bool(tool_result.get('error'))
        })
        
        try:
            # Extract execution context
            context = self._extract_execution_context(tool_result)
            
            # Validate against SuperClaude principles
            validation_result = self._validate_tool_result(context)
            
            # Log validation decision
            if not validation_result.is_valid:
                log_decision(
                    "post_tool_use",
                    "validation_failure",
                    validation_result.failed_checks[0] if validation_result.failed_checks else "unknown",
                    f"Tool '{context['tool_name']}' failed validation: {validation_result.message}"
                )
            
            # Measure effectiveness and quality
            effectiveness_metrics = self._measure_effectiveness(context, validation_result)
            
            # Detect patterns and learning opportunities
            learning_analysis = self._analyze_learning_opportunities(context, effectiveness_metrics)
            
            # Record learning events
            self._record_learning_events(context, effectiveness_metrics, learning_analysis)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(context, validation_result, learning_analysis)
            
            # Create validation report
            validation_report = self._create_validation_report(
                context, validation_result, effectiveness_metrics, 
                learning_analysis, recommendations
            )
            
            # Detect patterns in tool execution
            pattern_analysis = self._analyze_execution_patterns(context, validation_result)
            
            # Log pattern detection
            if pattern_analysis.get('error_pattern_detected'):
                log_decision(
                    "post_tool_use",
                    "error_pattern_detected",
                    pattern_analysis.get('pattern_type', 'unknown'),
                    pattern_analysis.get('description', 'Error pattern identified')
                )
            
            # Performance tracking
            execution_time = (time.time() - start_time) * 1000
            validation_report['performance_metrics'] = {
                'processing_time_ms': execution_time,
                'target_met': execution_time < self.performance_target_ms,
                'quality_score': self._calculate_quality_score(context, validation_result)
            }
            
            # Log successful completion
            log_hook_end(
                "post_tool_use",
                int(execution_time),
                True,
                {
                    "tool_name": context['tool_name'],
                    "validation_passed": validation_result.is_valid,
                    "quality_score": validation_report['performance_metrics']['quality_score']
                }
            )
            
            return validation_report
            
        except Exception as e:
            # Log error
            execution_time = (time.time() - start_time) * 1000
            log_error(
                "post_tool_use",
                str(e),
                {"tool_name": tool_result.get('tool_name', 'unknown')}
            )
            log_hook_end("post_tool_use", int(execution_time), False)
            
            # Graceful fallback on error
            return self._create_fallback_result(tool_result, str(e))
    
    def _extract_execution_context(self, tool_result: dict) -> dict:
        """Extract and enrich tool execution context."""
        context = {
            'tool_name': tool_result.get('tool_name', ''),
            'execution_status': tool_result.get('status', 'unknown'),
            'execution_time_ms': tool_result.get('execution_time_ms', 0),
            'parameters_used': tool_result.get('parameters', {}),
            'result_data': tool_result.get('result', {}),
            'error_info': tool_result.get('error', {}),
            'mcp_servers_used': tool_result.get('mcp_servers', []),
            'performance_data': tool_result.get('performance', {}),
            'user_intent': tool_result.get('user_intent', ''),
            'session_context': tool_result.get('session_context', {}),
            'timestamp': time.time()
        }
        
        # Analyze operation characteristics
        context.update(self._analyze_operation_outcome(context))
        
        # Extract quality indicators
        context.update(self._extract_quality_indicators(context))
        
        return context
    
    def _analyze_operation_outcome(self, context: dict) -> dict:
        """Analyze the outcome of the tool operation."""
        outcome_analysis = {
            'success': context['execution_status'] == 'success',
            'partial_success': False,
            'error_occurred': context['execution_status'] == 'error',
            'performance_acceptable': True,
            'quality_indicators': [],
            'risk_factors': []
        }
        
        # Analyze execution status
        if context['execution_status'] in ['partial', 'warning']:
            outcome_analysis['partial_success'] = True
        
        # Performance analysis
        execution_time = context.get('execution_time_ms', 0)
        if execution_time > 5000:  # 5 second threshold
            outcome_analysis['performance_acceptable'] = False
            outcome_analysis['risk_factors'].append('slow_execution')
        
        # Error analysis
        if context.get('error_info'):
            error_type = context['error_info'].get('type', 'unknown')
            outcome_analysis['error_type'] = error_type
            outcome_analysis['error_recoverable'] = error_type not in ['fatal', 'security', 'corruption']
        
        # Quality indicators from result data
        result_data = context.get('result_data', {})
        if result_data:
            if result_data.get('validation_passed'):
                outcome_analysis['quality_indicators'].append('validation_passed')
            if result_data.get('tests_passed'):
                outcome_analysis['quality_indicators'].append('tests_passed')
            if result_data.get('linting_clean'):
                outcome_analysis['quality_indicators'].append('linting_clean')
        
        return outcome_analysis
    
    def _extract_quality_indicators(self, context: dict) -> dict:
        """Extract quality indicators from execution context."""
        quality_indicators = {
            'code_quality_score': 0.0,
            'security_compliance': True,
            'performance_efficiency': 1.0,
            'error_handling_present': False,
            'documentation_adequate': False,
            'test_coverage_acceptable': False
        }
        
        # Analyze tool output for quality indicators
        tool_name = context['tool_name']
        result_data = context.get('result_data', {})
        
        # Code quality analysis
        if tool_name in ['Write', 'Edit', 'Generate']:
            # Check for quality indicators in the result
            if 'quality_score' in result_data:
                quality_indicators['code_quality_score'] = result_data['quality_score']
            
            # Infer quality from operation success and performance
            if context.get('success') and context.get('performance_acceptable'):
                quality_indicators['code_quality_score'] = max(
                    quality_indicators['code_quality_score'], 0.7
                )
        
        # Security compliance
        if context.get('error_type') in ['security', 'vulnerability']:
            quality_indicators['security_compliance'] = False
        
        # Performance efficiency
        execution_time = context.get('execution_time_ms', 0)
        expected_time = context.get('performance_data', {}).get('expected_time_ms', 1000)
        if execution_time > 0 and expected_time > 0:
            quality_indicators['performance_efficiency'] = min(expected_time / execution_time, 2.0)
        
        # Error handling detection
        if tool_name in ['Write', 'Edit'] and 'try' in str(result_data).lower():
            quality_indicators['error_handling_present'] = True
        
        # Documentation assessment
        if tool_name in ['Document', 'Generate'] or 'doc' in context.get('user_intent', '').lower():
            quality_indicators['documentation_adequate'] = context.get('success', False)
        
        return quality_indicators
    
    def _validate_tool_result(self, context: dict) -> ValidationResult:
        """Validate execution against SuperClaude principles."""
        # Create operation data for validation
        operation_data = {
            'operation_type': context['tool_name'],
            'has_error_handling': context.get('error_handling_present', False),
            'affects_logic': context['tool_name'] in ['Write', 'Edit', 'Generate'],
            'has_tests': context.get('test_coverage_acceptable', False),
            'is_public_api': 'api' in context.get('user_intent', '').lower(),
            'has_documentation': context.get('documentation_adequate', False),
            'handles_user_input': 'input' in context.get('user_intent', '').lower(),
            'has_input_validation': context.get('security_compliance', True),
            'evidence': context.get('success', False)
        }
        
        # Run framework validation
        validation_result = self.framework_logic.validate_operation(operation_data)
        
        # Enhance with SuperClaude-specific validations
        validation_result = self._enhance_validation_with_superclaude_rules(
            validation_result, context
        )
        
        return validation_result
    
    def _enhance_validation_with_superclaude_rules(self, 
                                                 base_validation: ValidationResult, 
                                                 context: dict) -> ValidationResult:
        """Enhance validation with SuperClaude-specific rules."""
        enhanced_validation = ValidationResult(
            is_valid=base_validation.is_valid,
            issues=base_validation.issues.copy(),
            warnings=base_validation.warnings.copy(),
            suggestions=base_validation.suggestions.copy(),
            quality_score=base_validation.quality_score
        )
        
        # RULES.md validation
        
        # Rule: Always use Read tool before Write or Edit operations
        if context['tool_name'] in ['Write', 'Edit']:
            session_context = context.get('session_context', {})
            recent_tools = session_context.get('recent_tools', [])
            if not any('Read' in tool for tool in recent_tools[-3:]):
                enhanced_validation.warnings.append(
                    "RULES violation: No Read operation detected before Write/Edit"
                )
                enhanced_validation.quality_score -= 0.1
        
        # Rule: Use absolute paths only
        params = context.get('parameters_used', {})
        for param_name, param_value in params.items():
            if 'path' in param_name.lower() and isinstance(param_value, str):
                if not os.path.isabs(param_value) and not param_value.startswith(('http', 'https')):
                    enhanced_validation.issues.append(
                        f"RULES violation: Relative path used in {param_name}: {param_value}"
                    )
                    enhanced_validation.quality_score -= 0.2
        
        # Rule: Validate before execution for high-risk operations
        if context.get('risk_factors'):
            if not context.get('validation_performed', False):
                enhanced_validation.warnings.append(
                    "RULES recommendation: High-risk operation should include validation"
                )
        
        # PRINCIPLES.md validation
        
        # Principle: Evidence > assumptions
        if not context.get('evidence_provided', False) and context.get('assumptions_made', False):
            enhanced_validation.suggestions.append(
                "PRINCIPLES: Provide evidence to support assumptions"
            )
        
        # Principle: Code > documentation
        if context['tool_name'] == 'Document' and not context.get('working_code_exists', True):
            enhanced_validation.warnings.append(
                "PRINCIPLES: Documentation should follow working code, not precede it"
            )
        
        # Principle: Efficiency > verbosity
        result_size = len(str(context.get('result_data', '')))
        if result_size > 5000 and not context.get('complexity_justifies_length', False):
            enhanced_validation.suggestions.append(
                "PRINCIPLES: Consider token efficiency techniques for large outputs"
            )
        
        # Recalculate overall validity
        enhanced_validation.is_valid = (
            len(enhanced_validation.issues) == 0 and 
            enhanced_validation.quality_score >= 0.7
        )
        
        return enhanced_validation
    
    def _measure_effectiveness(self, context: dict, validation_result: ValidationResult) -> dict:
        """Measure operation effectiveness and quality."""
        effectiveness_metrics = {
            'overall_effectiveness': 0.0,
            'quality_score': validation_result.quality_score,
            'performance_score': 0.0,
            'user_satisfaction_estimate': 0.0,
            'learning_value': 0.0,
            'improvement_potential': 0.0
        }
        
        # Performance scoring
        execution_time = context.get('execution_time_ms', 0)
        expected_time = context.get('performance_data', {}).get('expected_time_ms', 1000)
        if execution_time > 0:
            time_ratio = expected_time / max(execution_time, 1)
            effectiveness_metrics['performance_score'] = min(time_ratio, 1.0)
        else:
            effectiveness_metrics['performance_score'] = 1.0
        
        # User satisfaction estimation
        if context.get('success'):
            base_satisfaction = 0.8
            if validation_result.quality_score > 0.8:
                base_satisfaction += 0.15
            if effectiveness_metrics['performance_score'] > 0.8:
                base_satisfaction += 0.05
            effectiveness_metrics['user_satisfaction_estimate'] = min(base_satisfaction, 1.0)
        else:
            # Reduce satisfaction based on error severity
            error_severity = self._assess_error_severity(context)
            effectiveness_metrics['user_satisfaction_estimate'] = max(0.3 - error_severity * 0.3, 0.0)
        
        # Learning value assessment
        if context.get('mcp_servers_used'):
            effectiveness_metrics['learning_value'] += 0.2  # MCP usage provides learning
        if context.get('error_occurred'):
            effectiveness_metrics['learning_value'] += 0.3  # Errors provide valuable learning
        if context.get('complexity_score', 0) > 0.6:
            effectiveness_metrics['learning_value'] += 0.2  # Complex operations provide insights
        
        effectiveness_metrics['learning_value'] = min(effectiveness_metrics['learning_value'], 1.0)
        
        # Improvement potential
        if len(validation_result.suggestions) > 0:
            effectiveness_metrics['improvement_potential'] = min(len(validation_result.suggestions) * 0.2, 1.0)
        
        # Overall effectiveness calculation
        weights = {
            'quality': 0.3,
            'performance': 0.25,
            'satisfaction': 0.35,
            'learning': 0.1
        }
        
        effectiveness_metrics['overall_effectiveness'] = (
            effectiveness_metrics['quality_score'] * weights['quality'] +
            effectiveness_metrics['performance_score'] * weights['performance'] +
            effectiveness_metrics['user_satisfaction_estimate'] * weights['satisfaction'] +
            effectiveness_metrics['learning_value'] * weights['learning']
        )
        
        return effectiveness_metrics
    
    def _assess_error_severity(self, context: dict) -> float:
        """Assess error severity on a scale of 0.0 to 1.0."""
        if not context.get('error_occurred'):
            return 0.0
        
        error_type = context.get('error_type', 'unknown')
        
        severity_map = {
            'fatal': 1.0,
            'security': 0.9,
            'corruption': 0.8,
            'timeout': 0.6,
            'validation': 0.4,
            'warning': 0.2,
            'unknown': 0.5
        }
        
        return severity_map.get(error_type, 0.5)
    
    def _analyze_learning_opportunities(self, context: dict, effectiveness_metrics: dict) -> dict:
        """Analyze learning opportunities from the execution."""
        learning_analysis = {
            'patterns_detected': [],
            'success_factors': [],
            'failure_factors': [],
            'optimization_opportunities': [],
            'adaptation_recommendations': []
        }
        
        # Pattern detection
        if context.get('mcp_servers_used'):
            for server in context['mcp_servers_used']:
                if effectiveness_metrics['overall_effectiveness'] > 0.8:
                    learning_analysis['patterns_detected'].append(f"effective_{server}_usage")
                elif effectiveness_metrics['overall_effectiveness'] < 0.5:
                    learning_analysis['patterns_detected'].append(f"ineffective_{server}_usage")
        
        # Success factor analysis
        if effectiveness_metrics['overall_effectiveness'] > 0.8:
            if effectiveness_metrics['performance_score'] > 0.8:
                learning_analysis['success_factors'].append('optimal_performance')
            if effectiveness_metrics['quality_score'] > 0.8:
                learning_analysis['success_factors'].append('high_quality_output')
            if context.get('mcp_servers_used'):
                learning_analysis['success_factors'].append('effective_mcp_coordination')
        
        # Failure factor analysis
        if effectiveness_metrics['overall_effectiveness'] < 0.5:
            if effectiveness_metrics['performance_score'] < 0.5:
                learning_analysis['failure_factors'].append('poor_performance')
            if effectiveness_metrics['quality_score'] < 0.5:
                learning_analysis['failure_factors'].append('quality_issues')
            if context.get('error_occurred'):
                learning_analysis['failure_factors'].append(f"error_{context.get('error_type', 'unknown')}")
        
        # Optimization opportunities
        if effectiveness_metrics['improvement_potential'] > 0.3:
            learning_analysis['optimization_opportunities'].append('validation_improvements_available')
        
        if context.get('execution_time_ms', 0) > 2000:
            learning_analysis['optimization_opportunities'].append('performance_optimization_needed')
        
        # Adaptation recommendations
        if len(learning_analysis['success_factors']) > 0:
            learning_analysis['adaptation_recommendations'].append(
                f"Reinforce patterns: {', '.join(learning_analysis['success_factors'])}"
            )
        
        if len(learning_analysis['failure_factors']) > 0:
            learning_analysis['adaptation_recommendations'].append(
                f"Address failure patterns: {', '.join(learning_analysis['failure_factors'])}"
            )
        
        return learning_analysis
    
    def _record_learning_events(self, context: dict, effectiveness_metrics: dict, learning_analysis: dict):
        """Record learning events for future adaptation."""
        overall_effectiveness = effectiveness_metrics['overall_effectiveness']
        
        # Record general operation learning
        self.learning_engine.record_learning_event(
            LearningType.OPERATION_PATTERN,
            AdaptationScope.USER,
            context,
            {
                'tool_name': context['tool_name'],
                'mcp_servers': context.get('mcp_servers_used', []),
                'success_factors': learning_analysis['success_factors'],
                'failure_factors': learning_analysis['failure_factors']
            },
            overall_effectiveness,
            0.8,  # High confidence in post-execution analysis
            {'hook': 'post_tool_use', 'effectiveness': overall_effectiveness}
        )
        
        # Track tool preference if execution was successful
        if context.get('success') and overall_effectiveness > 0.7:
            operation_type = self._categorize_operation(context['tool_name'])
            if operation_type:
                self.learning_engine.update_last_preference(
                    f"tool_{operation_type}",
                    context['tool_name']
                )
        
        # Record MCP server effectiveness
        for server in context.get('mcp_servers_used', []):
            self.learning_engine.record_learning_event(
                LearningType.EFFECTIVENESS_FEEDBACK,
                AdaptationScope.USER,
                context,
                {'mcp_server': server},
                overall_effectiveness,
                0.9,  # Very high confidence in direct feedback
                {'server_performance': effectiveness_metrics['performance_score']}
            )
        
        # Record error patterns if applicable
        if context.get('error_occurred'):
            self.learning_engine.record_learning_event(
                LearningType.ERROR_RECOVERY,
                AdaptationScope.PROJECT,
                context,
                {
                    'error_type': context.get('error_type'),
                    'recovery_successful': context.get('error_recoverable', False),
                    'context_factors': learning_analysis['failure_factors']
                },
                1.0 - self._assess_error_severity(context),  # Inverse of severity
                1.0,  # Full confidence in error data
                {'error_learning': True}
            )
    
    def _generate_recommendations(self, context: dict, validation_result: ValidationResult, 
                                learning_analysis: dict) -> dict:
        """Generate recommendations for improvement."""
        recommendations = {
            'immediate_actions': [],
            'optimization_suggestions': [],
            'learning_adaptations': [],
            'prevention_measures': []
        }
        
        # Immediate actions from validation issues
        for issue in validation_result.issues:
            recommendations['immediate_actions'].append(f"Fix: {issue}")
        
        for warning in validation_result.warnings:
            recommendations['immediate_actions'].append(f"Address: {warning}")
        
        # Optimization suggestions
        for suggestion in validation_result.suggestions:
            recommendations['optimization_suggestions'].append(suggestion)
        
        for opportunity in learning_analysis['optimization_opportunities']:
            recommendations['optimization_suggestions'].append(f"Optimize: {opportunity}")
        
        # Learning adaptations
        for adaptation in learning_analysis['adaptation_recommendations']:
            recommendations['learning_adaptations'].append(adaptation)
        
        # Prevention measures for errors
        if context.get('error_occurred'):
            error_type = context.get('error_type', 'unknown')
            if error_type == 'timeout':
                recommendations['prevention_measures'].append("Consider parallel execution for large operations")
            elif error_type == 'validation':
                recommendations['prevention_measures'].append("Enable pre-validation for similar operations")
            elif error_type == 'security':
                recommendations['prevention_measures'].append("Implement security validation checks")
        
        return recommendations
    
    def _calculate_quality_score(self, context: dict, validation_result: ValidationResult) -> float:
        """Calculate quality score based on validation and execution."""
        base_score = validation_result.quality_score
        
        # Adjust for execution time
        execution_time = context.get('execution_time_ms', 0)
        time_ratio = execution_time / max(self.performance_target_ms, 1)
        time_penalty = min(time_ratio, 1.0)
        
        # Initialize error penalty (no penalty when no error occurs)
        error_penalty = 1.0
        
        # Adjust for error occurrence
        if context.get('error_occurred'):
            error_severity = self._assess_error_severity(context)
            error_penalty = 1.0 - error_severity
        
        # Combine adjustments
        quality_score = base_score * time_penalty * error_penalty
        
        return quality_score
    
    def _create_validation_report(self, context: dict, validation_result: ValidationResult,
                                effectiveness_metrics: dict, learning_analysis: dict, 
                                recommendations: dict) -> dict:
        """Create comprehensive validation report."""
        return {
            'tool_name': context['tool_name'],
            'execution_status': context['execution_status'],
            'timestamp': context['timestamp'],
            
            'validation': {
                'is_valid': validation_result.is_valid,
                'quality_score': validation_result.quality_score,
                'issues': validation_result.issues,
                'warnings': validation_result.warnings,
                'suggestions': validation_result.suggestions
            },
            
            'effectiveness': effectiveness_metrics,
            
            'learning': {
                'patterns_detected': learning_analysis['patterns_detected'],
                'success_factors': learning_analysis['success_factors'],
                'failure_factors': learning_analysis['failure_factors'],
                'learning_value': effectiveness_metrics['learning_value']
            },
            
            'recommendations': recommendations,
            
            'compliance': {
                'rules_compliance': len([i for i in validation_result.issues if 'RULES' in i]) == 0,
                'principles_alignment': len([w for w in validation_result.warnings if 'PRINCIPLES' in w]) == 0,
                'superclaude_score': self._calculate_superclaude_compliance_score(validation_result)
            },
            
            'metadata': {
                'hook_version': 'post_tool_use_1.0',
                'validation_timestamp': time.time(),
                'learning_events_recorded': len(learning_analysis['patterns_detected']) + 1
            }
        }
    
    def _calculate_superclaude_compliance_score(self, validation_result: ValidationResult) -> float:
        """Calculate overall SuperClaude compliance score."""
        base_score = validation_result.quality_score
        
        # Penalties for specific violations
        rules_violations = len([i for i in validation_result.issues if 'RULES' in i])
        principles_violations = len([w for w in validation_result.warnings if 'PRINCIPLES' in w])
        
        penalty = (rules_violations * 0.2) + (principles_violations * 0.1)
        
        return max(base_score - penalty, 0.0)
    
    def _create_fallback_result(self, tool_result: dict, error: str) -> dict:
        """Create fallback validation report on error."""
        return {
            'tool_name': tool_result.get('tool_name', 'unknown'),
            'execution_status': 'validation_error',
            'timestamp': time.time(),
            'error': error,
            'fallback_mode': True,
            
            'validation': {
                'is_valid': False,
                'quality_score': 0.0,
                'issues': [f"Validation hook error: {error}"],
                'warnings': [],
                'suggestions': ['Fix validation hook error']
            },
            
            'effectiveness': {
                'overall_effectiveness': 0.0,
                'quality_score': 0.0,
                'performance_score': 0.0,
                'user_satisfaction_estimate': 0.0,
                'learning_value': 0.0
            },
            
            'performance_metrics': {
                'processing_time_ms': 0,
                'target_met': False,
                'error_occurred': True
            }
        }
    
    def _analyze_execution_patterns(self, context: dict, validation_result: ValidationResult) -> dict:
        """Analyze patterns in tool execution."""
        pattern_analysis = {
            'error_pattern_detected': False,
            'pattern_type': 'unknown',
            'description': 'No error pattern detected'
        }
        
        # Check for error occurrence
        if context.get('error_occurred'):
            error_type = context.get('error_type', 'unknown')
            
            # Check for specific error types
            if error_type in ['fatal', 'security', 'corruption']:
                pattern_analysis['error_pattern_detected'] = True
                pattern_analysis['pattern_type'] = error_type
                pattern_analysis['description'] = f"Error pattern detected: {error_type}"
        
        return pattern_analysis
    
    def _categorize_operation(self, tool_name: str) -> Optional[str]:
        """Categorize tool into operation type for preference tracking."""
        operation_map = {
            'read': ['Read', 'Get', 'List', 'Search', 'Find'],
            'write': ['Write', 'Create', 'Generate'],
            'edit': ['Edit', 'Update', 'Modify', 'Replace'],
            'analyze': ['Analyze', 'Validate', 'Check', 'Test'],
            'mcp': ['Context7', 'Sequential', 'Magic', 'Playwright', 'Morphllm', 'Serena']
        }
        
        for operation_type, tools in operation_map.items():
            if any(tool in tool_name for tool in tools):
                return operation_type
        
        return None


def main():
    """Main hook execution function."""
    try:
        # Read tool result from stdin
        tool_result = json.loads(sys.stdin.read())
        
        # Initialize and run hook
        hook = PostToolUseHook()
        result = hook.process_tool_result(tool_result)
        
        # Output result as JSON
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        # Output error as JSON
        error_result = {
            'validation_error': True,
            'error': str(e),
            'fallback_mode': True
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()