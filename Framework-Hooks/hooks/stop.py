#!/usr/bin/env python3
"""
SuperClaude-Lite Stop Hook

Implements session analytics + /sc:save logic with performance tracking.
Performance target: <200ms execution time.

This hook runs at session end and provides:
- Comprehensive session analytics and performance metrics
- Learning consolidation and adaptation updates
- Session persistence with intelligent compression
- Performance optimization recommendations
- Quality assessment and improvement suggestions
"""

import sys
import json
import time
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import statistics

# Add shared modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "shared"))

from framework_logic import FrameworkLogic
from pattern_detection import PatternDetector
from mcp_intelligence import MCPIntelligence
from compression_engine import CompressionEngine
from learning_engine import LearningEngine, LearningType, AdaptationScope
from yaml_loader import config_loader
from logger import log_hook_start, log_hook_end, log_decision, log_error


class StopHook:
    """
    Stop hook implementing session analytics and persistence.
    
    Responsibilities:
    - Analyze session performance and effectiveness
    - Consolidate learning events and adaptations
    - Generate comprehensive session analytics
    - Implement intelligent session persistence
    - Provide optimization recommendations for future sessions
    - Track SuperClaude framework effectiveness metrics
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
        self.hook_config = config_loader.get_hook_config('stop')
        
        # Load session configuration (from YAML if exists, otherwise use hook config)
        try:
            self.session_config = config_loader.load_config('session')
        except FileNotFoundError:
            # Fall back to hook configuration if YAML file not found
            self.session_config = self.hook_config.get('configuration', {})
        
        # Performance tracking using configuration
        self.initialization_time = (time.time() - start_time) * 1000
        self.performance_target_ms = config_loader.get_hook_config('stop', 'performance_target_ms', 200)
        
    def process_session_stop(self, session_data: dict) -> dict:
        """
        Process session stop with analytics and persistence.
        
        Args:
            session_data: Session termination data from Claude Code
            
        Returns:
            Session analytics report with learning insights and persistence status
        """
        start_time = time.time()
        
        # Log hook start
        log_hook_start("stop", {
            "session_id": session_data.get('session_id', ''),
            "session_duration_ms": session_data.get('duration_ms', 0),
            "operations_count": len(session_data.get('operations', [])),
            "errors_count": len(session_data.get('errors', [])),
            "superclaude_enabled": session_data.get('superclaude_enabled', False)
        })
        
        try:
            # Extract session context
            context = self._extract_session_context(session_data)
            
            # Analyze session performance
            performance_analysis = self._analyze_session_performance(context)
            
            # Log performance analysis results
            log_decision(
                "stop",
                "performance_analysis",
                f"{performance_analysis['overall_score']:.2f}",
                f"Productivity: {context.get('session_productivity', 0):.2f}, Errors: {context.get('error_rate', 0):.2f}, Bottlenecks: {', '.join(performance_analysis['bottlenecks_identified'])}"
            )
            
            # Consolidate learning events
            learning_consolidation = self._consolidate_learning_events(context)
            
            # Generate session analytics
            session_analytics = self._generate_session_analytics(
                context, performance_analysis, learning_consolidation
            )
            
            # Perform session persistence
            persistence_result = self._perform_session_persistence(context, session_analytics)
            
            # Log persistence results
            if persistence_result['persistence_enabled']:
                log_decision(
                    "stop",
                    "session_persistence",
                    "saved",
                    f"Analytics saved: {persistence_result['analytics_saved']}, Compression: {persistence_result['compression_applied']}"
                )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                context, performance_analysis, learning_consolidation
            )
            
            # Log recommendations generated
            total_recommendations = sum(len(recs) for recs in recommendations.values())
            if total_recommendations > 0:
                log_decision(
                    "stop",
                    "recommendations_generated",
                    str(total_recommendations),
                    f"Categories: {', '.join(k for k, v in recommendations.items() if v)}"
                )
            
            # Create final learning events
            self._create_final_learning_events(context, session_analytics)
            
            # Generate session report
            session_report = self._generate_session_report(
                context, session_analytics, persistence_result, recommendations
            )
            
            # Performance tracking
            execution_time = (time.time() - start_time) * 1000
            session_report['performance_metrics'] = {
                'stop_processing_time_ms': execution_time,
                'target_met': execution_time < self.performance_target_ms,
                'total_session_efficiency': self._calculate_session_efficiency(session_analytics)
            }
            
            # Log hook end with success
            log_hook_end(
                "stop",
                int(execution_time),
                True,
                {
                    "session_score": session_analytics['performance_metrics']['overall_score'],
                    "superclaude_effectiveness": session_analytics['superclaude_effectiveness']['effectiveness_score'],
                    "learning_insights": session_analytics['learning_summary']['insights_generated'],
                    "recommendations": total_recommendations,
                    "performance_target_met": execution_time < self.performance_target_ms
                }
            )
            
            return session_report
            
        except Exception as e:
            # Log error
            log_error("stop", str(e), {"session_data": session_data})
            
            # Log hook end with failure
            log_hook_end("stop", int((time.time() - start_time) * 1000), False)
            
            # Graceful fallback on error
            return self._create_fallback_report(session_data, str(e))
    
    def _extract_session_context(self, session_data: dict) -> dict:
        """Extract and enrich session context."""
        context = {
            'session_id': session_data.get('session_id', ''),
            'session_duration_ms': session_data.get('duration_ms', 0),
            'session_start_time': session_data.get('start_time', 0),
            'session_end_time': time.time(),
            'operations_performed': session_data.get('operations', []),
            'tools_used': session_data.get('tools_used', []),
            'mcp_servers_activated': session_data.get('mcp_servers', []),
            'errors_encountered': session_data.get('errors', []),
            'user_interactions': session_data.get('user_interactions', []),
            'resource_usage': session_data.get('resource_usage', {}),
            'quality_metrics': session_data.get('quality_metrics', {}),
            'superclaude_enabled': session_data.get('superclaude_enabled', False)
        }
        
        # Calculate derived metrics
        context.update(self._calculate_derived_metrics(context))
        
        return context
    
    def _calculate_derived_metrics(self, context: dict) -> dict:
        """Calculate derived session metrics."""
        operations = context.get('operations_performed', [])
        tools = context.get('tools_used', [])
        
        return {
            'operation_count': len(operations),
            'unique_tools_count': len(set(tools)),
            'error_rate': len(context.get('errors_encountered', [])) / max(len(operations), 1),
            'mcp_usage_ratio': len(context.get('mcp_servers_activated', [])) / max(len(operations), 1),
            'session_productivity': self._calculate_productivity_score(context),
            'superclaude_effectiveness': self._calculate_superclaude_effectiveness(context)
        }
    
    def _calculate_productivity_score(self, context: dict) -> float:
        """Calculate session productivity score (0.0 to 1.0)."""
        operations = context.get('operations_performed', [])
        errors = context.get('errors_encountered', [])
        duration_ms = context.get('session_duration_ms', 1)
        
        if not operations:
            return 0.0
        
        # Base productivity from operation completion
        completion_rate = (len(operations) - len(errors)) / len(operations)
        
        # Time efficiency (operations per minute)
        duration_minutes = duration_ms / (1000 * 60)
        operations_per_minute = len(operations) / max(duration_minutes, 0.1)
        
        # Normalize operations per minute (assume 5 ops/min is very productive)
        time_efficiency = min(operations_per_minute / 5.0, 1.0)
        
        # Combined productivity score
        productivity = (completion_rate * 0.7) + (time_efficiency * 0.3)
        
        return min(productivity, 1.0)
    
    def _calculate_superclaude_effectiveness(self, context: dict) -> float:
        """Calculate SuperClaude framework effectiveness score."""
        if not context.get('superclaude_enabled'):
            return 0.0
        
        # Factors that indicate SuperClaude effectiveness
        factors = []
        
        # MCP server utilization
        mcp_ratio = context.get('mcp_usage_ratio', 0)
        factors.append(min(mcp_ratio * 2, 1.0))  # More MCP usage = better intelligence
        
        # Error reduction (assume SuperClaude reduces errors)
        error_rate = context.get('error_rate', 0)
        error_effectiveness = max(1.0 - (error_rate * 2), 0.0)
        factors.append(error_effectiveness)
        
        # Productivity enhancement
        productivity = context.get('session_productivity', 0)
        factors.append(productivity)
        
        # Quality metrics if available
        quality_metrics = context.get('quality_metrics', {})
        if quality_metrics:
            avg_quality = statistics.mean(quality_metrics.values()) if quality_metrics.values() else 0.5
            factors.append(avg_quality)
        
        return statistics.mean(factors) if factors else 0.5
    
    def _analyze_session_performance(self, context: dict) -> dict:
        """Analyze overall session performance."""
        performance_analysis = {
            'overall_score': 0.0,
            'performance_categories': {},
            'bottlenecks_identified': [],
            'optimization_opportunities': [],
            'performance_trends': {}
        }
        
        # Overall performance scoring
        productivity = context.get('session_productivity', 0)
        effectiveness = context.get('superclaude_effectiveness', 0)
        error_rate = context.get('error_rate', 0)
        
        performance_analysis['overall_score'] = (
            productivity * 0.4 + 
            effectiveness * 0.4 + 
            (1.0 - error_rate) * 0.2
        )
        
        # Category-specific performance
        performance_analysis['performance_categories'] = {
            'productivity': productivity,
            'quality': 1.0 - error_rate,
            'intelligence_utilization': context.get('mcp_usage_ratio', 0),
            'resource_efficiency': self._calculate_resource_efficiency(context),
            'user_satisfaction_estimate': self._estimate_user_satisfaction(context)
        }
        
        # Identify bottlenecks
        if error_rate > 0.2:
            performance_analysis['bottlenecks_identified'].append('high_error_rate')
        
        if productivity < 0.5:
            performance_analysis['bottlenecks_identified'].append('low_productivity')
        
        if context.get('mcp_usage_ratio', 0) < 0.3 and context.get('superclaude_enabled'):
            performance_analysis['bottlenecks_identified'].append('underutilized_intelligence')
            log_decision(
                "stop",
                "intelligence_utilization",
                "low",
                f"MCP usage ratio: {context.get('mcp_usage_ratio', 0):.2f}, SuperClaude enabled but underutilized"
            )
        
        # Optimization opportunities
        if context.get('unique_tools_count', 0) > 10:
            performance_analysis['optimization_opportunities'].append('tool_usage_optimization')
        
        if len(context.get('mcp_servers_activated', [])) < 2 and context.get('operation_count', 0) > 5:
            performance_analysis['optimization_opportunities'].append('mcp_server_coordination')
        
        return performance_analysis
    
    def _calculate_resource_efficiency(self, context: dict) -> float:
        """Calculate resource usage efficiency."""
        resource_usage = context.get('resource_usage', {})
        
        if not resource_usage:
            return 0.8  # Assume good efficiency if no data
        
        # Extract resource metrics
        memory_usage = resource_usage.get('memory_percent', 50)
        cpu_usage = resource_usage.get('cpu_percent', 50)
        token_usage = resource_usage.get('token_percent', 50)
        
        # Efficiency is inversely related to usage (but some usage is good)
        memory_efficiency = 1.0 - max((memory_usage - 60) / 40, 0)  # Penalty above 60%
        cpu_efficiency = 1.0 - max((cpu_usage - 70) / 30, 0)        # Penalty above 70%
        token_efficiency = 1.0 - max((token_usage - 75) / 25, 0)    # Penalty above 75%
        
        return (memory_efficiency + cpu_efficiency + token_efficiency) / 3
    
    def _estimate_user_satisfaction(self, context: dict) -> float:
        """Estimate user satisfaction based on session metrics."""
        satisfaction_factors = []
        
        # Low error rate increases satisfaction
        error_rate = context.get('error_rate', 0)
        satisfaction_factors.append(1.0 - error_rate)
        
        # High productivity increases satisfaction
        productivity = context.get('session_productivity', 0)
        satisfaction_factors.append(productivity)
        
        # SuperClaude effectiveness increases satisfaction
        if context.get('superclaude_enabled'):
            effectiveness = context.get('superclaude_effectiveness', 0)
            satisfaction_factors.append(effectiveness)
        
        # Session duration factor (not too short, not too long)
        duration_minutes = context.get('session_duration_ms', 0) / (1000 * 60)
        if duration_minutes > 0:
            # Optimal session length is 15-60 minutes
            if 15 <= duration_minutes <= 60:
                duration_satisfaction = 1.0
            elif duration_minutes < 15:
                duration_satisfaction = duration_minutes / 15
            else:
                duration_satisfaction = max(1.0 - (duration_minutes - 60) / 120, 0.3)
            satisfaction_factors.append(duration_satisfaction)
        
        return statistics.mean(satisfaction_factors) if satisfaction_factors else 0.5
    
    def _consolidate_learning_events(self, context: dict) -> dict:
        """Consolidate learning events from the session."""
        learning_consolidation = {
            'total_learning_events': 0,
            'learning_categories': {},
            'adaptations_created': 0,
            'effectiveness_feedback': [],
            'learning_insights': []
        }
        
        # Generate learning insights from session
        insights = self.learning_engine.generate_learning_insights()
        learning_consolidation['learning_insights'] = [
            {
                'insight_type': insight.insight_type,
                'description': insight.description,
                'confidence': insight.confidence,
                'impact_score': insight.impact_score
            }
            for insight in insights
        ]
        
        # Session-specific learning
        session_learning = {
            'session_effectiveness': context.get('superclaude_effectiveness', 0),
            'performance_score': context.get('session_productivity', 0),
            'mcp_coordination_effectiveness': min(context.get('mcp_usage_ratio', 0) * 2, 1.0),
            'error_recovery_success': 1.0 - context.get('error_rate', 0)
        }
        
        # Record session learning
        self.learning_engine.record_learning_event(
            LearningType.EFFECTIVENESS_FEEDBACK,
            AdaptationScope.SESSION,
            context,
            session_learning,
            context.get('superclaude_effectiveness', 0),
            0.9,
            {'hook': 'stop', 'session_end': True}
        )
        
        learning_consolidation['total_learning_events'] = 1 + len(insights)
        
        return learning_consolidation
    
    def _generate_session_analytics(self, context: dict, performance_analysis: dict, 
                                  learning_consolidation: dict) -> dict:
        """Generate comprehensive session analytics."""
        analytics = {
            'session_summary': {
                'session_id': context['session_id'],
                'duration_minutes': context.get('session_duration_ms', 0) / (1000 * 60),
                'operations_completed': context.get('operation_count', 0),
                'tools_utilized': context.get('unique_tools_count', 0),
                'mcp_servers_used': len(context.get('mcp_servers_activated', [])),
                'superclaude_enabled': context.get('superclaude_enabled', False)
            },
            
            'performance_metrics': {
                'overall_score': performance_analysis['overall_score'],
                'productivity_score': context.get('session_productivity', 0),
                'quality_score': 1.0 - context.get('error_rate', 0),
                'efficiency_score': performance_analysis['performance_categories'].get('resource_efficiency', 0),
                'satisfaction_estimate': performance_analysis['performance_categories'].get('user_satisfaction_estimate', 0)
            },
            
            'superclaude_effectiveness': {
                'framework_enabled': context.get('superclaude_enabled', False),
                'effectiveness_score': context.get('superclaude_effectiveness', 0),
                'intelligence_utilization': context.get('mcp_usage_ratio', 0),
                'learning_events_generated': learning_consolidation['total_learning_events'],
                'adaptations_created': learning_consolidation['adaptations_created']
            },
            
            'quality_analysis': {
                'error_rate': context.get('error_rate', 0),
                'operation_success_rate': 1.0 - context.get('error_rate', 0),
                'bottlenecks': performance_analysis['bottlenecks_identified'],
                'optimization_opportunities': performance_analysis['optimization_opportunities']
            },
            
            'learning_summary': {
                'insights_generated': len(learning_consolidation['learning_insights']),
                'key_insights': learning_consolidation['learning_insights'][:3],  # Top 3 insights
                'learning_effectiveness': statistics.mean([
                    insight['confidence'] * insight['impact_score'] 
                    for insight in learning_consolidation['learning_insights']
                ]) if learning_consolidation['learning_insights'] else 0.0
            },
            
            'resource_utilization': context.get('resource_usage', {}),
            
            'session_metadata': {
                'start_time': context.get('session_start_time', 0),
                'end_time': context.get('session_end_time', 0),
                'framework_version': '1.0.0',
                'analytics_version': 'stop_1.0'
            }
        }
        
        return analytics
    
    def _perform_session_persistence(self, context: dict, session_analytics: dict) -> dict:
        """Perform intelligent session persistence."""
        persistence_result = {
            'persistence_enabled': True,
            'session_data_saved': False,
            'analytics_saved': False,
            'learning_data_saved': False,
            'compression_applied': False,
            'storage_optimized': False
        }
        
        try:
            # Save session analytics
            analytics_data = json.dumps(session_analytics, indent=2)
            
            # Apply compression if session data is large
            if len(analytics_data) > 10000:  # 10KB threshold
                compression_result = self.compression_engine.compress_content(
                    analytics_data,
                    context,
                    {'content_type': 'session_data'}
                )
                persistence_result['compression_applied'] = True
                persistence_result['compression_ratio'] = compression_result.compression_ratio
            
            # Simulate saving (real implementation would use actual storage)
            cache_dir = Path(os.path.expanduser("~/.claude/cache"))
            cache_dir.mkdir(parents=True, exist_ok=True)
            session_file = cache_dir / f"session_{context['session_id']}.json"
            
            with open(session_file, 'w') as f:
                f.write(analytics_data)
            
            persistence_result['session_data_saved'] = True
            persistence_result['analytics_saved'] = True
            
            # Learning data is automatically saved by learning engine
            persistence_result['learning_data_saved'] = True
            
            # Optimize storage by cleaning old sessions
            self._cleanup_old_sessions(cache_dir)
            persistence_result['storage_optimized'] = True
            
        except Exception as e:
            persistence_result['error'] = str(e)
            persistence_result['persistence_enabled'] = False
        
        return persistence_result
    
    def _cleanup_old_sessions(self, cache_dir: Path):
        """Clean up old session files to optimize storage."""
        session_files = list(cache_dir.glob("session_*.json"))
        
        # Keep only the most recent 50 sessions
        if len(session_files) > 50:
            session_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            for old_file in session_files[50:]:
                try:
                    old_file.unlink()
                except:
                    pass  # Ignore cleanup errors
    
    def _generate_recommendations(self, context: dict, performance_analysis: dict, 
                                learning_consolidation: dict) -> dict:
        """Generate recommendations for future sessions."""
        recommendations = {
            'performance_improvements': [],
            'superclaude_optimizations': [],
            'learning_suggestions': [],
            'workflow_enhancements': []
        }
        
        # Performance recommendations
        if performance_analysis['overall_score'] < 0.7:
            recommendations['performance_improvements'].extend([
                'Focus on reducing error rate through validation',
                'Consider enabling more SuperClaude intelligence features',
                'Optimize tool selection and usage patterns'
            ])
        
        # SuperClaude optimization recommendations
        if context.get('superclaude_enabled') and context.get('superclaude_effectiveness', 0) < 0.6:
            recommendations['superclaude_optimizations'].extend([
                'Enable more MCP servers for better intelligence',
                'Use delegation features for complex operations',
                'Activate compression for resource optimization'
            ])
        elif not context.get('superclaude_enabled'):
            recommendations['superclaude_optimizations'].append(
                'Consider enabling SuperClaude framework for enhanced productivity'
            )
        
        # Learning suggestions
        if learning_consolidation['total_learning_events'] < 3:
            recommendations['learning_suggestions'].append(
                'Engage with more complex operations to improve system learning'
            )
        
        # Workflow enhancements
        if context.get('error_rate', 0) > 0.1:
            recommendations['workflow_enhancements'].extend([
                'Use validation hooks to catch errors early',
                'Enable pre-tool-use intelligence for better routing'
            ])
        
        return recommendations
    
    def _create_final_learning_events(self, context: dict, session_analytics: dict):
        """Create final learning events for the session."""
        # Record overall session effectiveness
        self.learning_engine.record_learning_event(
            LearningType.USER_PREFERENCE,
            AdaptationScope.USER,
            context,
            {
                'session_pattern': 'completion',
                'satisfaction_score': session_analytics['performance_metrics']['satisfaction_estimate'],
                'productivity_achieved': session_analytics['performance_metrics']['productivity_score'],
                'superclaude_usage': context.get('superclaude_enabled', False)
            },
            session_analytics['performance_metrics']['overall_score'],
            1.0,  # High confidence in final session metrics
            {'hook': 'stop', 'final_learning': True}
        )
    
    def _calculate_session_efficiency(self, session_analytics: dict) -> float:
        """Calculate overall session efficiency score."""
        performance_metrics = session_analytics.get('performance_metrics', {})
        
        efficiency_components = [
            performance_metrics.get('productivity_score', 0),
            performance_metrics.get('quality_score', 0),
            performance_metrics.get('efficiency_score', 0),
            session_analytics.get('superclaude_effectiveness', {}).get('effectiveness_score', 0)
        ]
        
        return statistics.mean([comp for comp in efficiency_components if comp > 0])
    
    def _generate_session_report(self, context: dict, session_analytics: dict, 
                                persistence_result: dict, recommendations: dict) -> dict:
        """Generate final session report."""
        return {
            'session_id': context['session_id'],
            'session_completed': True,
            'completion_timestamp': context.get('session_end_time', time.time()),
            
            'analytics': session_analytics,
            'persistence': persistence_result,
            'recommendations': recommendations,
            
            'summary': {
                'session_success': session_analytics['performance_metrics']['overall_score'] > 0.6,
                'superclaude_effective': session_analytics['superclaude_effectiveness']['effectiveness_score'] > 0.6,
                'learning_achieved': session_analytics['learning_summary']['insights_generated'] > 0,
                'recommendations_generated': sum(len(recs) for recs in recommendations.values()) > 0
            },
            
            'next_session_preparation': {
                'enable_superclaude': True,
                'suggested_optimizations': recommendations.get('superclaude_optimizations', [])[:2],
                'learning_focus_areas': [insight['insight_type'] for insight in 
                                       session_analytics['learning_summary']['key_insights']]
            },
            
            'metadata': {
                'hook_version': 'stop_1.0',
                'report_timestamp': time.time(),
                'analytics_comprehensive': True
            }
        }
    
    def _create_fallback_report(self, session_data: dict, error: str) -> dict:
        """Create fallback session report on error."""
        return {
            'session_id': session_data.get('session_id', 'unknown'),
            'session_completed': False,
            'error': error,
            'fallback_mode': True,
            
            'analytics': {
                'session_summary': {
                    'session_id': session_data.get('session_id', 'unknown'),
                    'error_occurred': True
                },
                'performance_metrics': {
                    'overall_score': 0.0
                }
            },
            
            'persistence': {
                'persistence_enabled': False,
                'error': error
            },
            
            'performance_metrics': {
                'stop_processing_time_ms': 0,
                'target_met': False,
                'error_occurred': True
            }
        }


def main():
    """Main hook execution function."""
    try:
        # Read session data from stdin
        session_data = json.loads(sys.stdin.read())
        
        # Initialize and run hook
        hook = StopHook()
        result = hook.process_session_stop(session_data)
        
        # Output result as JSON
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        # Output error as JSON
        error_result = {
            'session_completed': False,
            'error': str(e),
            'fallback_mode': True
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()