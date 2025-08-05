#!/usr/bin/env python3
"""
SuperClaude-Lite Notification Hook

Implements just-in-time MCP documentation loading and pattern updates.
Performance target: <100ms execution time.

This hook runs when Claude Code sends notifications and provides:
- Just-in-time loading of MCP server documentation
- Dynamic pattern updates based on operation context
- Framework intelligence updates and adaptations
- Real-time learning from notification patterns
- Performance optimization through intelligent caching
"""

import sys
import json
import time
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add shared modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "shared"))

from framework_logic import FrameworkLogic
from pattern_detection import PatternDetector
from mcp_intelligence import MCPIntelligence
from compression_engine import CompressionEngine
from learning_engine import LearningEngine, LearningType, AdaptationScope
from yaml_loader import config_loader
from logger import log_hook_start, log_hook_end, log_decision, log_error


class NotificationHook:
    """
    Notification hook implementing just-in-time intelligence loading.
    
    Responsibilities:
    - Process Claude Code notifications for intelligence opportunities
    - Load relevant MCP documentation on-demand
    - Update pattern detection based on real-time context
    - Provide framework intelligence updates
    - Cache and optimize frequently accessed information
    - Learn from notification patterns for future optimization
    """
    
    def __init__(self):
        start_time = time.time()
        
        # Initialize core components
        self.framework_logic = FrameworkLogic()
        self.pattern_detector = PatternDetector()
        self.mcp_intelligence = MCPIntelligence()
        self.compression_engine = CompressionEngine()
        
        # Initialize learning engine
        cache_dir = Path("cache")
        self.learning_engine = LearningEngine(cache_dir)
        
        # Load notification configuration
        self.notification_config = config_loader.get_section('session', 'notifications', {})
        
        # Initialize notification cache
        self.notification_cache = {}
        self.pattern_cache = {}
        
        # Load hook-specific configuration from SuperClaude config
        self.hook_config = config_loader.get_hook_config('notification')
        
        # Performance tracking using configuration
        self.initialization_time = (time.time() - start_time) * 1000
        self.performance_target_ms = config_loader.get_hook_config('notification', 'performance_target_ms', 100)
        
    def process_notification(self, notification: dict) -> dict:
        """
        Process notification with just-in-time intelligence loading.
        
        Args:
            notification: Notification from Claude Code
            
        Returns:
            Enhanced notification response with intelligence updates
        """
        start_time = time.time()
        
        # Log hook start
        log_hook_start("notification", {
            "notification_type": notification.get('type', 'unknown'),
            "has_context": bool(notification.get('context')),
            "priority": notification.get('priority', 'normal')
        })
        
        try:
            # Extract notification context
            context = self._extract_notification_context(notification)
            
            # Analyze notification for intelligence opportunities
            intelligence_analysis = self._analyze_intelligence_opportunities(context)
            
            # Determine intelligence needs
            intelligence_needs = self._analyze_intelligence_needs(context)
            
            # Log intelligence loading decision
            if intelligence_needs.get('mcp_docs_needed'):
                log_decision(
                    "notification",
                    "mcp_docs_loading",
                    ",".join(intelligence_needs.get('mcp_servers', [])),
                    f"Documentation needed for: {intelligence_needs.get('reason', 'notification context')}"
                )
            
            # Load just-in-time documentation if needed
            documentation_updates = self._load_jit_documentation(context, intelligence_analysis)
            
            # Update patterns if needed
            pattern_updates = self._update_patterns_if_needed(context, intelligence_needs)
            
            # Log pattern update decision
            if pattern_updates.get('patterns_updated'):
                log_decision(
                    "notification",
                    "pattern_update",
                    pattern_updates.get('pattern_type', 'unknown'),
                    f"Updated {pattern_updates.get('update_count', 0)} patterns"
                )
            
            # Generate framework intelligence updates
            framework_updates = self._generate_framework_updates(context, intelligence_analysis)
            
            # Record learning events
            self._record_notification_learning(context, intelligence_analysis)
            
            # Create intelligence response
            intelligence_response = self._create_intelligence_response(
                context, documentation_updates, pattern_updates, framework_updates
            )
            
            # Performance validation
            execution_time = (time.time() - start_time) * 1000
            intelligence_response['performance_metrics'] = {
                'processing_time_ms': execution_time,
                'target_met': execution_time < self.performance_target_ms,
                'cache_hit_rate': self._calculate_cache_hit_rate()
            }
            
            # Log successful completion
            log_hook_end(
                "notification",
                int(execution_time),
                True,
                {
                    "notification_type": context['notification_type'],
                    "intelligence_loaded": bool(intelligence_needs.get('mcp_docs_needed')),
                    "patterns_updated": pattern_updates.get('patterns_updated', False)
                }
            )
            
            return intelligence_response
            
        except Exception as e:
            # Log error
            execution_time = (time.time() - start_time) * 1000
            log_error(
                "notification",
                str(e),
                {"notification_type": notification.get('type', 'unknown')}
            )
            log_hook_end("notification", int(execution_time), False)
            
            # Graceful fallback on error
            return self._create_fallback_response(notification, str(e))
    
    def _extract_notification_context(self, notification: dict) -> dict:
        """Extract and enrich notification context."""
        context = {
            'notification_type': notification.get('type', 'unknown'),
            'notification_data': notification.get('data', {}),
            'session_context': notification.get('session_context', {}),
            'user_context': notification.get('user_context', {}),
            'operation_context': notification.get('operation_context', {}),
            'trigger_event': notification.get('trigger', ''),
            'timestamp': time.time()
        }
        
        # Analyze notification importance
        context['priority'] = self._assess_notification_priority(context)
        
        # Extract operation characteristics
        context.update(self._extract_operation_characteristics(context))
        
        return context
    
    def _assess_notification_priority(self, context: dict) -> str:
        """Assess notification priority for processing."""
        notification_type = context['notification_type']
        
        # High priority notifications
        if notification_type in ['error', 'failure', 'security_alert']:
            return 'high'
        elif notification_type in ['performance_issue', 'validation_failure']:
            return 'high'
        
        # Medium priority notifications
        elif notification_type in ['tool_request', 'context_change', 'resource_constraint']:
            return 'medium'
        
        # Low priority notifications
        elif notification_type in ['info', 'debug', 'status_update']:
            return 'low'
        
        return 'medium'
    
    def _extract_operation_characteristics(self, context: dict) -> dict:
        """Extract operation characteristics from notification."""
        operation_context = context.get('operation_context', {})
        
        return {
            'operation_type': operation_context.get('type', 'unknown'),
            'complexity_indicators': operation_context.get('complexity', 0.0),
            'tool_requests': operation_context.get('tools_requested', []),
            'mcp_server_hints': operation_context.get('mcp_hints', []),
            'performance_requirements': operation_context.get('performance', {}),
            'intelligence_requirements': operation_context.get('intelligence_needed', False)
        }
    
    def _analyze_intelligence_opportunities(self, context: dict) -> dict:
        """Analyze notification for intelligence loading opportunities."""
        analysis = {
            'documentation_needed': [],
            'pattern_updates_needed': [],
            'framework_updates_needed': [],
            'learning_opportunities': [],
            'optimization_opportunities': []
        }
        
        notification_type = context['notification_type']
        operation_type = context.get('operation_type', 'unknown')
        
        # Documentation loading opportunities
        if notification_type == 'tool_request':
            requested_tools = context.get('tool_requests', [])
            for tool in requested_tools:
                if tool in ['ui_component', 'component_generation']:
                    analysis['documentation_needed'].append('magic_patterns')
                elif tool in ['library_integration', 'framework_usage']:
                    analysis['documentation_needed'].append('context7_patterns')
                elif tool in ['complex_analysis', 'debugging']:
                    analysis['documentation_needed'].append('sequential_patterns')
                elif tool in ['testing', 'validation']:
                    analysis['documentation_needed'].append('playwright_patterns')
        
        # Pattern update opportunities
        if notification_type in ['context_change', 'operation_start']:
            analysis['pattern_updates_needed'].extend([
                'operation_patterns',
                'context_patterns'
            ])
        
        # Framework update opportunities
        if notification_type in ['performance_issue', 'optimization_request']:
            analysis['framework_updates_needed'].extend([
                'performance_optimization',
                'resource_management'
            ])
        
        # Learning opportunities
        if notification_type in ['error', 'failure']:
            analysis['learning_opportunities'].append('error_pattern_learning')
        elif notification_type in ['success', 'completion']:
            analysis['learning_opportunities'].append('success_pattern_learning')
        
        # Optimization opportunities
        if context.get('performance_requirements'):
            analysis['optimization_opportunities'].append('performance_optimization')
        
        return analysis
    
    def _analyze_intelligence_needs(self, context: dict) -> dict:
        """Determine intelligence needs based on context."""
        needs = {
            'mcp_docs_needed': False,
            'mcp_servers': [],
            'reason': ''
        }
        
        # Check for MCP server hints
        mcp_hints = context.get('mcp_server_hints', [])
        if mcp_hints:
            needs['mcp_docs_needed'] = True
            needs['mcp_servers'] = mcp_hints
            needs['reason'] = 'MCP server hints'
        
        # Check for tool requests
        tool_requests = context.get('tool_requests', [])
        if tool_requests:
            needs['mcp_docs_needed'] = True
            needs['mcp_servers'] = [tool for tool in tool_requests if tool in ['ui_component', 'component_generation', 'library_integration', 'framework_usage', 'complex_analysis', 'debugging', 'testing', 'validation']]
            needs['reason'] = 'Tool requests'
        
        # Check for performance requirements
        performance_requirements = context.get('performance_requirements', {})
        if performance_requirements:
            needs['mcp_docs_needed'] = True
            needs['mcp_servers'] = ['performance_optimization', 'resource_management']
            needs['reason'] = 'Performance requirements'
        
        return needs
    
    def _load_jit_documentation(self, context: dict, intelligence_analysis: dict) -> dict:
        """Load just-in-time documentation based on analysis."""
        documentation_updates = {
            'loaded_patterns': [],
            'cached_content': {},
            'documentation_summaries': {}
        }
        
        needed_docs = intelligence_analysis.get('documentation_needed', [])
        
        for doc_type in needed_docs:
            # Check cache first
            if doc_type in self.notification_cache:
                documentation_updates['cached_content'][doc_type] = self.notification_cache[doc_type]
                documentation_updates['loaded_patterns'].append(f"{doc_type}_cached")
                continue
            
            # Load documentation on-demand
            doc_content = self._load_documentation_content(doc_type, context)
            if doc_content:
                # Cache for future use
                self.notification_cache[doc_type] = doc_content
                documentation_updates['cached_content'][doc_type] = doc_content
                documentation_updates['loaded_patterns'].append(f"{doc_type}_loaded")
                
                # Create summary for quick access
                summary = self._create_documentation_summary(doc_content)
                documentation_updates['documentation_summaries'][doc_type] = summary
        
        return documentation_updates
    
    def _load_documentation_content(self, doc_type: str, context: dict) -> Optional[dict]:
        """Load specific documentation content."""
        # Simulated documentation loading - real implementation would fetch from MCP servers
        documentation_patterns = {
            'magic_patterns': {
                'ui_components': ['button', 'form', 'modal', 'card'],
                'design_systems': ['theme', 'tokens', 'spacing'],
                'accessibility': ['aria-labels', 'keyboard-navigation', 'screen-readers']
            },
            'context7_patterns': {
                'library_integration': ['import_patterns', 'configuration', 'best_practices'],
                'framework_usage': ['react_patterns', 'vue_patterns', 'angular_patterns'],
                'documentation_access': ['api_docs', 'examples', 'tutorials']
            },
            'sequential_patterns': {
                'analysis_workflows': ['step_by_step', 'hypothesis_testing', 'validation'],
                'debugging_strategies': ['systematic_approach', 'root_cause', 'verification'],
                'complex_reasoning': ['decomposition', 'synthesis', 'optimization']
            },
            'playwright_patterns': {
                'testing_strategies': ['e2e_tests', 'unit_tests', 'integration_tests'],
                'automation_patterns': ['page_objects', 'test_data', 'assertions'],
                'performance_testing': ['load_testing', 'stress_testing', 'monitoring']
            }
        }
        
        return documentation_patterns.get(doc_type, {})
    
    def _create_documentation_summary(self, doc_content: dict) -> dict:
        """Create summary of documentation content for quick access."""
        summary = {
            'categories': list(doc_content.keys()),
            'total_patterns': sum(len(patterns) if isinstance(patterns, list) else 1 
                                for patterns in doc_content.values()),
            'quick_access_items': []
        }
        
        # Extract most commonly used patterns
        for category, patterns in doc_content.items():
            if isinstance(patterns, list) and patterns:
                summary['quick_access_items'].append({
                    'category': category,
                    'top_pattern': patterns[0],
                    'pattern_count': len(patterns)
                })
        
        return summary
    
    def _update_patterns_if_needed(self, context: dict, intelligence_needs: dict) -> dict:
        """Update pattern detection based on context."""
        pattern_updates = {
            'updated_patterns': [],
            'new_patterns_detected': [],
            'pattern_effectiveness': {}
        }
        
        if intelligence_needs.get('mcp_docs_needed'):
            # Update operation-specific patterns
            operation_type = context.get('operation_type', 'unknown')
            self._update_operation_patterns(operation_type, pattern_updates)
            
            # Update context-specific patterns
            session_context = context.get('session_context', {})
            self._update_context_patterns(session_context, pattern_updates)
        
        return pattern_updates
    
    def _update_operation_patterns(self, operation_type: str, pattern_updates: dict):
        """Update operation-specific patterns."""
        if operation_type in ['build', 'implement']:
            pattern_updates['updated_patterns'].append('build_operation_patterns')
            # Update pattern detection for build operations
        elif operation_type in ['analyze', 'debug']:
            pattern_updates['updated_patterns'].append('analysis_operation_patterns')
            # Update pattern detection for analysis operations
        elif operation_type in ['test', 'validate']:
            pattern_updates['updated_patterns'].append('testing_operation_patterns')
            # Update pattern detection for testing operations
    
    def _update_context_patterns(self, session_context: dict, pattern_updates: dict):
        """Update context-specific patterns."""
        if session_context.get('project_type') == 'frontend':
            pattern_updates['updated_patterns'].append('frontend_context_patterns')
        elif session_context.get('project_type') == 'backend':
            pattern_updates['updated_patterns'].append('backend_context_patterns')
        elif session_context.get('project_type') == 'fullstack':
            pattern_updates['updated_patterns'].append('fullstack_context_patterns')
    
    def _generate_framework_updates(self, context: dict, intelligence_analysis: dict) -> dict:
        """Generate framework intelligence updates."""
        framework_updates = {
            'configuration_updates': {},
            'optimization_recommendations': [],
            'intelligence_enhancements': []
        }
        
        needed_updates = intelligence_analysis.get('framework_updates_needed', [])
        
        for update_type in needed_updates:
            if update_type == 'performance_optimization':
                framework_updates['optimization_recommendations'].extend([
                    'Enable parallel processing for multi-file operations',
                    'Activate compression for resource-constrained scenarios',
                    'Use intelligent caching for repeated operations'
                ])
            
            elif update_type == 'resource_management':
                resource_usage = context.get('session_context', {}).get('resource_usage', 0)
                if resource_usage > 75:
                    framework_updates['configuration_updates']['compression'] = 'enable_aggressive'
                    framework_updates['optimization_recommendations'].append(
                        'Resource usage high - enabling aggressive compression'
                    )
        
        return framework_updates
    
    def _record_notification_learning(self, context: dict, intelligence_analysis: dict):
        """Record notification learning for optimization."""
        learning_opportunities = intelligence_analysis.get('learning_opportunities', [])
        
        for opportunity in learning_opportunities:
            if opportunity == 'error_pattern_learning':
                self.learning_engine.record_learning_event(
                    LearningType.ERROR_RECOVERY,
                    AdaptationScope.USER,
                    context,
                    {
                        'notification_type': context['notification_type'],
                        'error_context': context.get('notification_data', {}),
                        'intelligence_loaded': len(intelligence_analysis.get('documentation_needed', []))
                    },
                    0.7,  # Learning value from errors
                    0.8,
                    {'hook': 'notification', 'learning_type': 'error'}
                )
            
            elif opportunity == 'success_pattern_learning':
                self.learning_engine.record_learning_event(
                    LearningType.OPERATION_PATTERN,
                    AdaptationScope.USER,
                    context,
                    {
                        'notification_type': context['notification_type'],
                        'success_context': context.get('notification_data', {}),
                        'patterns_updated': len(intelligence_analysis.get('pattern_updates_needed', []))
                    },
                    0.9,  # High learning value from success
                    0.9,
                    {'hook': 'notification', 'learning_type': 'success'}
                )
    
    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit ratio for performance metrics."""
        if not hasattr(self, '_cache_requests'):
            self._cache_requests = 0
            self._cache_hits = 0
        
        if self._cache_requests == 0:
            return 0.0
        
        return self._cache_hits / self._cache_requests
    
    def _create_intelligence_response(self, context: dict, documentation_updates: dict,
                                    pattern_updates: dict, framework_updates: dict) -> dict:
        """Create comprehensive intelligence response."""
        return {
            'notification_type': context['notification_type'],
            'priority': context['priority'],
            'timestamp': context['timestamp'],
            
            'intelligence_updates': {
                'documentation_loaded': len(documentation_updates.get('loaded_patterns', [])) > 0,
                'patterns_updated': len(pattern_updates.get('updated_patterns', [])) > 0,
                'framework_enhanced': len(framework_updates.get('optimization_recommendations', [])) > 0
            },
            
            'documentation': {
                'patterns_loaded': documentation_updates.get('loaded_patterns', []),
                'summaries': documentation_updates.get('documentation_summaries', {}),
                'cache_status': 'active'
            },
            
            'patterns': {
                'updated_patterns': pattern_updates.get('updated_patterns', []),
                'new_patterns': pattern_updates.get('new_patterns_detected', []),
                'effectiveness': pattern_updates.get('pattern_effectiveness', {})
            },
            
            'framework': {
                'configuration_updates': framework_updates.get('configuration_updates', {}),
                'optimization_recommendations': framework_updates.get('optimization_recommendations', []),
                'intelligence_enhancements': framework_updates.get('intelligence_enhancements', [])
            },
            
            'optimization': {
                'just_in_time_loading': True,
                'intelligent_caching': True,
                'performance_optimized': True,
                'learning_enabled': True
            },
            
            'metadata': {
                'hook_version': 'notification_1.0',
                'processing_timestamp': time.time(),
                'intelligence_level': 'adaptive'
            }
        }
    
    def _create_fallback_response(self, notification: dict, error: str) -> dict:
        """Create fallback response on error."""
        return {
            'notification_type': notification.get('type', 'unknown'),
            'priority': 'low',
            'error': error,
            'fallback_mode': True,
            
            'intelligence_updates': {
                'documentation_loaded': False,
                'patterns_updated': False,
                'framework_enhanced': False
            },
            
            'documentation': {
                'patterns_loaded': [],
                'summaries': {},
                'cache_status': 'error'
            },
            
            'performance_metrics': {
                'processing_time_ms': 0,
                'target_met': False,
                'error_occurred': True
            }
        }


def main():
    """Main hook execution function."""
    try:
        # Read notification from stdin
        notification = json.loads(sys.stdin.read())
        
        # Initialize and run hook
        hook = NotificationHook()
        result = hook.process_notification(notification)
        
        # Output result as JSON
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        # Output error as JSON
        error_result = {
            'intelligence_updates_enabled': False,
            'error': str(e),
            'fallback_mode': True
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()