#!/usr/bin/env python3
"""
SuperClaude-Lite Subagent Stop Hook

Implements MODE_Task_Management delegation coordination and analytics.
Performance target: <150ms execution time.

This hook runs when subagents complete tasks and provides:
- Subagent performance analytics and coordination metrics
- Task delegation effectiveness measurement
- Cross-agent learning and adaptation
- Wave orchestration optimization
- Parallel execution performance tracking
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


class SubagentStopHook:
    """
    Subagent stop hook implementing task management coordination.
    
    Responsibilities:
    - Analyze subagent task completion and performance
    - Measure delegation effectiveness and coordination success
    - Learn from parallel execution patterns
    - Optimize wave orchestration strategies
    - Coordinate cross-agent knowledge sharing
    - Track task management framework effectiveness
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
        
        # Load task management configuration
        self.task_config = config_loader.get_section('session', 'task_management', {})
        
        # Load hook-specific configuration from SuperClaude config
        self.hook_config = config_loader.get_hook_config('subagent_stop')
        
        # Performance tracking using configuration
        self.initialization_time = (time.time() - start_time) * 1000
        self.performance_target_ms = config_loader.get_hook_config('subagent_stop', 'performance_target_ms', 150)
        
    def process_subagent_stop(self, subagent_data: dict) -> dict:
        """
        Process subagent completion with coordination analytics.
        
        Args:
            subagent_data: Subagent completion data from Claude Code
            
        Returns:
            Coordination analytics with delegation effectiveness and optimization insights
        """
        start_time = time.time()
        
        # Log hook start
        log_hook_start("subagent_stop", {
            "subagent_id": subagent_data.get('subagent_id', ''),
            "task_id": subagent_data.get('task_id', ''),
            "task_type": subagent_data.get('task_type', 'unknown'),
            "delegation_strategy": subagent_data.get('delegation_strategy', 'unknown'),
            "parallel_tasks": len(subagent_data.get('parallel_tasks', [])),
            "wave_context": subagent_data.get('wave_context', {})
        })
        
        try:
            # Extract subagent context
            context = self._extract_subagent_context(subagent_data)
            
            # Analyze task completion performance
            task_analysis = self._analyze_task_completion(context)
            
            # Log task completion analysis
            log_decision(
                "subagent_stop",
                "task_completion",
                "completed" if task_analysis['completion_success'] else "failed",
                f"Quality: {task_analysis['completion_quality']:.2f}, Efficiency: {task_analysis['completion_efficiency']:.2f}"
            )
            
            # Measure delegation effectiveness
            delegation_analysis = self._analyze_delegation_effectiveness(context, task_analysis)
            
            # Log delegation effectiveness
            log_decision(
                "subagent_stop",
                "delegation_effectiveness",
                f"{delegation_analysis['delegation_value']:.2f}",
                f"Strategy: {delegation_analysis['delegation_strategy']}, Overhead: {delegation_analysis['coordination_overhead']:.1%}"
            )
            
            # Analyze coordination patterns
            coordination_analysis = self._analyze_coordination_patterns(context, delegation_analysis)
            
            # Generate optimization recommendations
            optimization_insights = self._generate_optimization_insights(
                context, task_analysis, delegation_analysis, coordination_analysis
            )
            
            # Record coordination learning
            self._record_coordination_learning(context, delegation_analysis, optimization_insights)
            
            # Update wave orchestration metrics
            wave_metrics = self._update_wave_orchestration_metrics(context, coordination_analysis)
            
            # Log wave orchestration if applicable
            if context.get('wave_total', 1) > 1:
                log_decision(
                    "subagent_stop",
                    "wave_orchestration",
                    f"wave_{context.get('wave_position', 0) + 1}_of_{context.get('wave_total', 1)}",
                    f"Performance: {wave_metrics['wave_performance']:.2f}, Efficiency: {wave_metrics['orchestration_efficiency']:.2f}"
                )
            
            # Generate coordination report
            coordination_report = self._generate_coordination_report(
                context, task_analysis, delegation_analysis, coordination_analysis, 
                optimization_insights, wave_metrics
            )
            
            # Performance tracking
            execution_time = (time.time() - start_time) * 1000
            coordination_report['performance_metrics'] = {
                'coordination_analysis_time_ms': execution_time,
                'target_met': execution_time < self.performance_target_ms,
                'coordination_efficiency': self._calculate_coordination_efficiency(context, execution_time)
            }
            
            # Log hook end with success
            log_hook_end(
                "subagent_stop",
                int(execution_time),
                True,
                {
                    "task_success": task_analysis['completion_success'],
                    "delegation_value": delegation_analysis['delegation_value'],
                    "coordination_strategy": coordination_analysis['coordination_strategy'],
                    "wave_enabled": context.get('wave_total', 1) > 1,
                    "performance_target_met": execution_time < self.performance_target_ms
                }
            )
            
            return coordination_report
            
        except Exception as e:
            # Log error
            log_error("subagent_stop", str(e), {"subagent_data": subagent_data})
            
            # Log hook end with failure
            log_hook_end("subagent_stop", int((time.time() - start_time) * 1000), False)
            
            # Graceful fallback on error
            return self._create_fallback_report(subagent_data, str(e))
    
    def _extract_subagent_context(self, subagent_data: dict) -> dict:
        """Extract and enrich subagent context."""
        context = {
            'subagent_id': subagent_data.get('subagent_id', ''),
            'parent_session_id': subagent_data.get('parent_session_id', ''),
            'task_id': subagent_data.get('task_id', ''),
            'task_type': subagent_data.get('task_type', 'unknown'),
            'delegation_strategy': subagent_data.get('delegation_strategy', 'unknown'),
            'execution_time_ms': subagent_data.get('execution_time_ms', 0),
            'task_result': subagent_data.get('result', {}),
            'task_status': subagent_data.get('status', 'unknown'),
            'resources_used': subagent_data.get('resources', {}),
            'coordination_data': subagent_data.get('coordination', {}),
            'parallel_tasks': subagent_data.get('parallel_tasks', []),
            'wave_context': subagent_data.get('wave_context', {}),
            'completion_timestamp': time.time()
        }
        
        # Analyze task characteristics
        context.update(self._analyze_task_characteristics(context))
        
        # Extract coordination metrics
        context.update(self._extract_coordination_metrics(context))
        
        return context
    
    def _analyze_task_characteristics(self, context: dict) -> dict:
        """Analyze characteristics of the completed task."""
        task_result = context.get('task_result', {})
        
        characteristics = {
            'task_complexity': self._calculate_task_complexity(context),
            'task_success': context.get('task_status') == 'completed',
            'partial_success': context.get('task_status') == 'partial',
            'task_error': context.get('task_status') == 'error',
            'output_quality': self._assess_output_quality(task_result),
            'resource_efficiency': self._calculate_resource_efficiency(context),
            'coordination_required': len(context.get('parallel_tasks', [])) > 0
        }
        
        return characteristics
    
    def _calculate_task_complexity(self, context: dict) -> float:
        """Calculate task complexity score (0.0 to 1.0)."""
        complexity_factors = []
        
        # Task type complexity
        task_type = context.get('task_type', 'unknown')
        type_complexity = {
            'file_analysis': 0.3,
            'code_generation': 0.6,
            'multi_file_edit': 0.7,
            'architecture_analysis': 0.9,
            'system_refactor': 1.0
        }
        complexity_factors.append(type_complexity.get(task_type, 0.5))
        
        # Execution time complexity
        execution_time = context.get('execution_time_ms', 0)
        if execution_time > 0:
            # Normalize to 5 seconds as high complexity
            time_complexity = min(execution_time / 5000, 1.0)
            complexity_factors.append(time_complexity)
        
        # Resource usage complexity
        resources = context.get('resources_used', {})
        if resources:
            resource_complexity = max(
                resources.get('memory_mb', 0) / 1000,  # 1GB = high
                resources.get('cpu_percent', 0) / 100
            )
            complexity_factors.append(min(resource_complexity, 1.0))
        
        # Coordination complexity
        if context.get('coordination_required'):
            complexity_factors.append(0.4)  # Coordination adds complexity
        
        return statistics.mean(complexity_factors) if complexity_factors else 0.5
    
    def _assess_output_quality(self, task_result: dict) -> float:
        """Assess quality of task output (0.0 to 1.0)."""
        if not task_result:
            return 0.0
        
        quality_indicators = []
        
        # Check for quality metrics in result
        if 'quality_score' in task_result:
            quality_indicators.append(task_result['quality_score'])
        
        # Check for validation results
        if task_result.get('validation_passed'):
            quality_indicators.append(0.8)
        elif task_result.get('validation_failed'):
            quality_indicators.append(0.3)
        
        # Check for error indicators
        if task_result.get('errors'):
            error_penalty = min(len(task_result['errors']) * 0.2, 0.6)
            quality_indicators.append(1.0 - error_penalty)
        
        # Check for completeness
        if task_result.get('completeness_ratio'):
            quality_indicators.append(task_result['completeness_ratio'])
        
        # Default quality estimation
        if not quality_indicators:
            # Estimate quality from task status
            status = task_result.get('status', 'unknown')
            if status == 'success':
                quality_indicators.append(0.8)
            elif status == 'partial':
                quality_indicators.append(0.6)
            else:
                quality_indicators.append(0.4)
        
        return statistics.mean(quality_indicators)
    
    def _calculate_resource_efficiency(self, context: dict) -> float:
        """Calculate resource usage efficiency."""
        resources = context.get('resources_used', {})
        execution_time = context.get('execution_time_ms', 1)
        
        if not resources:
            return 0.7  # Assume moderate efficiency
        
        # Memory efficiency (lower usage = higher efficiency)
        memory_mb = resources.get('memory_mb', 100)
        memory_efficiency = max(1.0 - (memory_mb / 1000), 0.1)  # Penalty above 1GB
        
        # CPU efficiency (moderate usage is optimal)
        cpu_percent = resources.get('cpu_percent', 50)
        if cpu_percent < 30:
            cpu_efficiency = cpu_percent / 30  # Underutilization penalty
        elif cpu_percent > 80:
            cpu_efficiency = (100 - cpu_percent) / 20  # Overutilization penalty
        else:
            cpu_efficiency = 1.0  # Optimal range
        
        # Time efficiency (faster is better, but not at quality cost)
        expected_time = resources.get('expected_time_ms', execution_time)
        if expected_time > 0:
            time_efficiency = min(expected_time / execution_time, 1.0)
        else:
            time_efficiency = 0.8
        
        return (memory_efficiency + cpu_efficiency + time_efficiency) / 3
    
    def _extract_coordination_metrics(self, context: dict) -> dict:
        """Extract coordination-specific metrics."""
        coordination_data = context.get('coordination_data', {})
        
        return {
            'coordination_overhead_ms': coordination_data.get('overhead_ms', 0),
            'synchronization_points': coordination_data.get('sync_points', 0),
            'data_exchange_size': coordination_data.get('data_exchange_bytes', 0),
            'coordination_success': coordination_data.get('success', True),
            'parallel_efficiency': coordination_data.get('parallel_efficiency', 1.0),
            'wave_position': context.get('wave_context', {}).get('position', 0),
            'wave_total': context.get('wave_context', {}).get('total_waves', 1)
        }
    
    def _analyze_task_completion(self, context: dict) -> dict:
        """Analyze task completion performance."""
        task_analysis = {
            'completion_success': context.get('task_success', False),
            'completion_quality': context.get('output_quality', 0.0),
            'completion_efficiency': context.get('resource_efficiency', 0.0),
            'completion_time_performance': 0.0,
            'error_analysis': {},
            'success_factors': [],
            'improvement_areas': []
        }
        
        # Time performance analysis
        execution_time = context.get('execution_time_ms', 0)
        task_type = context.get('task_type', 'unknown')
        
        # Expected times by task type (rough estimates)
        expected_times = {
            'file_analysis': 500,
            'code_generation': 2000,
            'multi_file_edit': 1500,
            'architecture_analysis': 3000,
            'system_refactor': 5000
        }
        
        expected_time = expected_times.get(task_type, 1000)
        if execution_time > 0:
            task_analysis['completion_time_performance'] = min(expected_time / execution_time, 1.0)
        
        # Success factor identification
        if task_analysis['completion_success']:
            if task_analysis['completion_quality'] > 0.8:
                task_analysis['success_factors'].append('high_output_quality')
            if task_analysis['completion_efficiency'] > 0.8:
                task_analysis['success_factors'].append('efficient_resource_usage')
            if task_analysis['completion_time_performance'] > 0.8:
                task_analysis['success_factors'].append('fast_execution')
        
        # Improvement area identification
        if task_analysis['completion_quality'] < 0.6:
            task_analysis['improvement_areas'].append('output_quality')
        if task_analysis['completion_efficiency'] < 0.6:
            task_analysis['improvement_areas'].append('resource_efficiency')
        if task_analysis['completion_time_performance'] < 0.6:
            task_analysis['improvement_areas'].append('execution_speed')
        
        return task_analysis
    
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
        
        # Calculate delegation efficiency
        coordination_overhead = context.get('coordination_overhead_ms', 0)
        execution_time = context.get('execution_time_ms', 1)
        
        if execution_time > 0:
            delegation_analysis['coordination_overhead'] = coordination_overhead / execution_time
            delegation_analysis['delegation_efficiency'] = max(
                1.0 - delegation_analysis['coordination_overhead'], 0.0
            )
        
        # Calculate parallel benefit
        parallel_tasks = context.get('parallel_tasks', [])
        if len(parallel_tasks) > 1:
            # Estimate parallel benefit based on task coordination
            parallel_efficiency = context.get('parallel_efficiency', 1.0)
            theoretical_speedup = len(parallel_tasks)
            actual_speedup = theoretical_speedup * parallel_efficiency
            delegation_analysis['parallel_benefit'] = actual_speedup / theoretical_speedup
        
        # Overall delegation value
        quality_factor = task_analysis['completion_quality']
        efficiency_factor = delegation_analysis['delegation_efficiency']
        parallel_factor = delegation_analysis['parallel_benefit'] if parallel_tasks else 1.0
        
        delegation_analysis['delegation_value'] = (
            quality_factor * 0.4 + 
            efficiency_factor * 0.3 + 
            parallel_factor * 0.3
        )
        
        return delegation_analysis
    
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
        
        # Determine coordination strategy
        if context.get('wave_total', 1) > 1:
            coordination_analysis['coordination_strategy'] = 'wave_orchestration'
        elif len(context.get('parallel_tasks', [])) > 1:
            coordination_analysis['coordination_strategy'] = 'parallel_coordination'
        else:
            coordination_analysis['coordination_strategy'] = 'single_agent'
        
        # Synchronization effectiveness
        sync_points = context.get('synchronization_points', 0)
        coordination_success = context.get('coordination_success', True)
        
        if sync_points > 0 and coordination_success:
            coordination_analysis['synchronization_effectiveness'] = 1.0
        elif sync_points > 0:
            coordination_analysis['synchronization_effectiveness'] = 0.5
        else:
            coordination_analysis['synchronization_effectiveness'] = 0.8  # No sync needed
        
        # Data flow efficiency
        data_exchange = context.get('data_exchange_size', 0)
        if data_exchange > 0:
            # Efficiency based on data size (smaller is more efficient)
            coordination_analysis['data_flow_efficiency'] = max(1.0 - (data_exchange / 1000000), 0.1)  # 1MB threshold
        else:
            coordination_analysis['data_flow_efficiency'] = 1.0  # No data exchange needed
        
        # Wave coordination success
        wave_position = context.get('wave_position', 0)
        wave_total = context.get('wave_total', 1)
        
        if wave_total > 1:
            # Success based on position completion and delegation value
            wave_progress = (wave_position + 1) / wave_total
            delegation_value = delegation_analysis.get('delegation_value', 0)
            coordination_analysis['wave_coordination_success'] = (wave_progress + delegation_value) / 2
        else:
            coordination_analysis['wave_coordination_success'] = 1.0
        
        # Detect coordination patterns
        if delegation_analysis['delegation_value'] > 0.8:
            coordination_analysis['coordination_patterns_detected'].append('effective_delegation')
        
        if coordination_analysis['synchronization_effectiveness'] > 0.8:
            coordination_analysis['coordination_patterns_detected'].append('efficient_synchronization')
        
        if coordination_analysis['wave_coordination_success'] > 0.8:
            coordination_analysis['coordination_patterns_detected'].append('successful_wave_orchestration')
        
        # Log detected patterns if any
        if coordination_analysis['coordination_patterns_detected']:
            log_decision(
                "subagent_stop",
                "coordination_patterns",
                str(len(coordination_analysis['coordination_patterns_detected'])),
                f"Patterns: {', '.join(coordination_analysis['coordination_patterns_detected'])}"
            )
        
        return coordination_analysis
    
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
        
        # Delegation optimizations
        if delegation_analysis['delegation_value'] < 0.6:
            insights['delegation_optimizations'].extend([
                'Consider alternative delegation strategies',
                'Reduce coordination overhead',
                'Improve task partitioning'
            ])
        
        if delegation_analysis['coordination_overhead'] > 0.3:
            insights['delegation_optimizations'].append('Minimize coordination overhead')
        
        # Coordination improvements
        if coordination_analysis['synchronization_effectiveness'] < 0.7:
            insights['coordination_improvements'].append('Improve synchronization mechanisms')
        
        if coordination_analysis['data_flow_efficiency'] < 0.7:
            insights['coordination_improvements'].append('Optimize data exchange patterns')
        
        # Wave strategy recommendations
        wave_success = coordination_analysis['wave_coordination_success']
        if wave_success < 0.6 and context.get('wave_total', 1) > 1:
            insights['wave_strategy_recommendations'].extend([
                'Adjust wave orchestration strategy',
                'Consider different task distribution',
                'Improve wave synchronization'
            ])
        elif wave_success > 0.8:
            insights['wave_strategy_recommendations'].append('Wave orchestration working well - maintain strategy')
        
        # Performance enhancements
        if task_analysis['completion_time_performance'] < 0.6:
            insights['performance_enhancements'].append('Optimize task execution speed')
        
        if task_analysis['completion_efficiency'] < 0.6:
            insights['performance_enhancements'].append('Improve resource utilization')
        
        return insights
    
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
        
        # Record task pattern learning
        if context.get('task_success'):
            self.learning_engine.record_learning_event(
                LearningType.OPERATION_PATTERN,
                AdaptationScope.USER,
                context,
                {
                    'successful_task_pattern': context.get('task_type'),
                    'success_factors': optimization_insights.get('performance_enhancements', []),
                    'delegation_effective': delegation_analysis['delegation_value'] > 0.7
                },
                delegation_analysis['delegation_value'],
                0.9,
                {'task_success_pattern': True}
            )
    
    def _update_wave_orchestration_metrics(self, context: dict, coordination_analysis: dict) -> dict:
        """Update wave orchestration performance metrics."""
        wave_metrics = {
            'wave_performance': 0.0,
            'orchestration_efficiency': 0.0,
            'wave_learning_value': 0.0,
            'next_wave_recommendations': []
        }
        
        if context.get('wave_total', 1) > 1:
            wave_success = coordination_analysis['wave_coordination_success']
            wave_metrics['wave_performance'] = wave_success
            
            # Calculate orchestration efficiency
            coordination_overhead = context.get('coordination_overhead_ms', 0)
            execution_time = context.get('execution_time_ms', 1)
            
            if execution_time > 0:
                wave_metrics['orchestration_efficiency'] = max(
                    1.0 - (coordination_overhead / execution_time), 0.0
                )
            
            # Learning value from wave coordination
            wave_metrics['wave_learning_value'] = wave_success * 0.8  # Waves provide valuable learning
            
            # Next wave recommendations
            if wave_success > 0.8:
                wave_metrics['next_wave_recommendations'].append('Continue current wave strategy')
            else:
                wave_metrics['next_wave_recommendations'].extend([
                    'Adjust wave coordination strategy',
                    'Improve inter-wave communication'
                ])
        
        return wave_metrics
    
    def _calculate_coordination_efficiency(self, context: dict, execution_time_ms: float) -> float:
        """Calculate coordination processing efficiency."""
        # Efficiency based on coordination overhead vs processing time
        coordination_overhead = context.get('coordination_overhead_ms', 0)
        task_execution_time = context.get('execution_time_ms', 1)
        
        if task_execution_time > 0:
            coordination_ratio = coordination_overhead / task_execution_time
            coordination_efficiency = max(1.0 - coordination_ratio, 0.0)
        else:
            coordination_efficiency = 0.8
        
        # Processing time efficiency
        processing_efficiency = min(100 / max(execution_time_ms, 1), 1.0)  # Target: 100ms
        
        return (coordination_efficiency + processing_efficiency) / 2
    
    def _generate_coordination_report(self, context: dict, task_analysis: dict, 
                                    delegation_analysis: dict, coordination_analysis: dict,
                                    optimization_insights: dict, wave_metrics: dict) -> dict:
        """Generate comprehensive coordination report."""
        return {
            'subagent_id': context['subagent_id'],
            'task_id': context['task_id'],
            'completion_timestamp': context['completion_timestamp'],
            
            'task_completion': {
                'success': task_analysis['completion_success'],
                'quality_score': task_analysis['completion_quality'],
                'efficiency_score': task_analysis['completion_efficiency'],
                'time_performance': task_analysis['completion_time_performance'],
                'success_factors': task_analysis['success_factors'],
                'improvement_areas': task_analysis['improvement_areas']
            },
            
            'delegation_analysis': {
                'strategy': delegation_analysis['delegation_strategy'],
                'effectiveness': delegation_analysis['delegation_value'],
                'efficiency': delegation_analysis['delegation_efficiency'],
                'coordination_overhead': delegation_analysis['coordination_overhead'],
                'parallel_benefit': delegation_analysis['parallel_benefit']
            },
            
            'coordination_metrics': {
                'strategy': coordination_analysis['coordination_strategy'],
                'synchronization_effectiveness': coordination_analysis['synchronization_effectiveness'],
                'data_flow_efficiency': coordination_analysis['data_flow_efficiency'],
                'patterns_detected': coordination_analysis['coordination_patterns_detected']
            },
            
            'wave_orchestration': {
                'enabled': context.get('wave_total', 1) > 1,
                'wave_position': context.get('wave_position', 0),
                'total_waves': context.get('wave_total', 1),
                'wave_performance': wave_metrics['wave_performance'],
                'orchestration_efficiency': wave_metrics['orchestration_efficiency'],
                'learning_value': wave_metrics['wave_learning_value']
            },
            
            'optimization_insights': optimization_insights,
            
            'performance_summary': {
                'overall_effectiveness': (
                    task_analysis['completion_quality'] * 0.4 +
                    delegation_analysis['delegation_value'] * 0.3 +
                    coordination_analysis['synchronization_effectiveness'] * 0.3
                ),
                'delegation_success': delegation_analysis['delegation_value'] > 0.6,
                'coordination_success': coordination_analysis['synchronization_effectiveness'] > 0.7,
                'learning_value': wave_metrics.get('wave_learning_value', 0.5)
            },
            
            'next_task_recommendations': {
                'continue_delegation': delegation_analysis['delegation_value'] > 0.6,
                'optimize_coordination': coordination_analysis['synchronization_effectiveness'] < 0.7,
                'adjust_wave_strategy': wave_metrics['wave_performance'] < 0.6,
                'suggested_improvements': optimization_insights.get('delegation_optimizations', [])[:2]
            },
            
            'metadata': {
                'hook_version': 'subagent_stop_1.0',
                'analysis_timestamp': time.time(),
                'coordination_framework': 'task_management_mode'
            }
        }
    
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
            },
            
            'delegation_analysis': {
                'strategy': 'unknown',
                'effectiveness': 0.0,
                'error': error
            },
            
            'performance_metrics': {
                'coordination_analysis_time_ms': 0,
                'target_met': False,
                'error_occurred': True
            }
        }


def main():
    """Main hook execution function."""
    try:
        # Read subagent data from stdin
        subagent_data = json.loads(sys.stdin.read())
        
        # Initialize and run hook
        hook = SubagentStopHook()
        result = hook.process_subagent_stop(subagent_data)
        
        # Output result as JSON
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        # Output error as JSON
        error_result = {
            'coordination_analysis_enabled': False,
            'error': str(e),
            'fallback_mode': True
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()