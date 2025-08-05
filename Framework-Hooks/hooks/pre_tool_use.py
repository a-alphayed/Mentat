#!/usr/bin/env python3
"""
SuperClaude-Lite Pre-Tool-Use Hook

Implements ORCHESTRATOR.md + MCP routing intelligence for optimal tool selection.
Performance target: <200ms execution time.

This hook runs before every tool usage and provides:
- Intelligent tool routing and MCP server selection
- Performance optimization and parallel execution planning
- Context-aware tool configuration
- Fallback strategy implementation
- Real-time adaptation based on effectiveness
"""

import sys
import json
import time
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add shared modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "shared"))

from framework_logic import FrameworkLogic, OperationContext, OperationType, RiskLevel
from pattern_detection import PatternDetector, PatternMatch
from mcp_intelligence import MCPIntelligence, MCPActivationPlan
from compression_engine import CompressionEngine
from learning_engine import LearningEngine, LearningType, AdaptationScope
from yaml_loader import config_loader
from logger import log_hook_start, log_hook_end, log_decision, log_error


class PreToolUseHook:
    """
    Pre-tool-use hook implementing SuperClaude orchestration intelligence.
    
    Responsibilities:
    - Analyze tool usage context and requirements
    - Route to optimal MCP servers based on capability matching
    - Configure parallel execution and performance optimization
    - Apply learned adaptations for tool selection
    - Implement fallback strategies for server failures
    - Track tool effectiveness and performance metrics
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
        self.hook_config = config_loader.get_hook_config('pre_tool_use')
        
        # Load orchestrator configuration (from YAML if exists, otherwise use hook config)
        try:
            self.orchestrator_config = config_loader.load_config('orchestrator')
        except FileNotFoundError:
            # Fall back to hook configuration if YAML file not found
            self.orchestrator_config = self.hook_config.get('configuration', {})
        
        # Load performance configuration (from YAML if exists, otherwise use hook config)
        try:
            self.performance_config = config_loader.load_config('performance')
        except FileNotFoundError:
            # Fall back to performance targets from global configuration
            self.performance_config = config_loader.get_performance_targets()
        
        # Performance tracking using configuration
        self.initialization_time = (time.time() - start_time) * 1000
        self.performance_target_ms = config_loader.get_hook_config('pre_tool_use', 'performance_target_ms', 200)
        
    def process_tool_use(self, tool_request: dict) -> dict:
        """
        Process tool use request with intelligent routing.
        
        Args:
            tool_request: Tool usage request from Claude Code
            
        Returns:
            Enhanced tool configuration with SuperClaude intelligence
        """
        start_time = time.time()
        
        # Log hook start
        log_hook_start("pre_tool_use", {
            "tool_name": tool_request.get('tool_name', 'unknown'),
            "has_parameters": bool(tool_request.get('parameters'))
        })
        
        try:
            # Extract tool context
            context = self._extract_tool_context(tool_request)
            
            # Analyze tool requirements and capabilities
            requirements = self._analyze_tool_requirements(context)
            
            # Log routing decision
            if requirements.get('mcp_server_hints'):
                log_decision(
                    "pre_tool_use",
                    "mcp_server_selection", 
                    ",".join(requirements['mcp_server_hints']),
                    f"Tool '{context['tool_name']}' requires capabilities: {', '.join(requirements.get('capabilities_needed', []))}"
                )
            
            # Detect patterns for intelligent routing
            routing_analysis = self._analyze_routing_patterns(context, requirements)
            
            # Apply learned adaptations
            enhanced_routing = self._apply_routing_adaptations(context, routing_analysis)
            
            # Create optimal execution plan
            execution_plan = self._create_execution_plan(context, enhanced_routing)
            
            # Log execution strategy decision
            log_decision(
                "pre_tool_use",
                "execution_strategy",
                execution_plan['execution_strategy'],
                f"Complexity: {context.get('complexity_score', 0):.2f}, Files: {context.get('file_count', 1)}"
            )
            
            # Configure tool enhancement
            tool_config = self._configure_tool_enhancement(context, execution_plan)
            
            # Record learning event
            self._record_tool_learning(context, tool_config)
            
            # Performance validation
            execution_time = (time.time() - start_time) * 1000
            tool_config['performance_metrics'] = {
                'routing_time_ms': execution_time,
                'target_met': execution_time < self.performance_target_ms,
                'efficiency_score': self._calculate_efficiency_score(context, execution_time)
            }
            
            # Log successful completion
            log_hook_end(
                "pre_tool_use",
                int(execution_time),
                True,
                {
                    "tool_name": context['tool_name'],
                    "mcp_servers": tool_config.get('mcp_integration', {}).get('servers', []),
                    "enhanced_mode": tool_config.get('enhanced_mode', False)
                }
            )
            
            return tool_config
            
        except Exception as e:
            # Log error
            execution_time = (time.time() - start_time) * 1000
            log_error(
                "pre_tool_use",
                str(e),
                {"tool_name": tool_request.get('tool_name', 'unknown')}
            )
            log_hook_end("pre_tool_use", int(execution_time), False)
            
            # Graceful fallback on error
            return self._create_fallback_tool_config(tool_request, str(e))
    
    def _extract_tool_context(self, tool_request: dict) -> dict:
        """Extract and enrich tool usage context."""
        context = {
            'tool_name': tool_request.get('tool_name', ''),
            'tool_parameters': tool_request.get('parameters', {}),
            'user_intent': tool_request.get('user_intent', ''),
            'session_context': tool_request.get('session_context', {}),
            'previous_tools': tool_request.get('previous_tools', []),
            'operation_sequence': tool_request.get('operation_sequence', []),
            'resource_state': tool_request.get('resource_state', {}),
            'timestamp': time.time()
        }
        
        # Extract operation characteristics
        context.update(self._analyze_operation_characteristics(context))
        
        # Analyze tool chain context
        context.update(self._analyze_tool_chain_context(context))
        
        return context
    
    def _analyze_operation_characteristics(self, context: dict) -> dict:
        """Analyze operation characteristics for routing decisions."""
        characteristics = {
            'operation_type': OperationType.READ,
            'complexity_score': 0.0,
            'file_count': 1,
            'directory_count': 1,
            'parallelizable': False,
            'resource_intensive': False,
            'requires_intelligence': False
        }
        
        tool_name = context['tool_name']
        tool_params = context['tool_parameters']
        
        # Determine operation type from tool
        if tool_name in ['Write', 'Edit', 'MultiEdit']:
            characteristics['operation_type'] = OperationType.WRITE
            characteristics['complexity_score'] += 0.2
        elif tool_name in ['Build', 'Implement']:
            characteristics['operation_type'] = OperationType.BUILD
            characteristics['complexity_score'] += 0.4
        elif tool_name in ['Test', 'Validate']:
            characteristics['operation_type'] = OperationType.TEST
            characteristics['complexity_score'] += 0.1
        elif tool_name in ['Analyze', 'Debug']:
            characteristics['operation_type'] = OperationType.ANALYZE
            characteristics['complexity_score'] += 0.3
            characteristics['requires_intelligence'] = True
        
        # Analyze file/directory scope
        if 'file_path' in tool_params:
            characteristics['file_count'] = 1
        elif 'files' in tool_params:
            file_list = tool_params['files']
            characteristics['file_count'] = len(file_list) if isinstance(file_list, list) else 1
            if characteristics['file_count'] > 3:
                characteristics['parallelizable'] = True
                characteristics['complexity_score'] += 0.3
        
        if 'directory' in tool_params or 'path' in tool_params:
            path_param = tool_params.get('directory') or tool_params.get('path', '')
            if '*' in str(path_param) or '**' in str(path_param):
                characteristics['directory_count'] = 5  # Estimate for glob patterns
                characteristics['complexity_score'] += 0.2
                characteristics['parallelizable'] = True
        
        # Resource intensity analysis
        if characteristics['file_count'] > 10 or characteristics['complexity_score'] > 0.6:
            characteristics['resource_intensive'] = True
        
        # Intelligence requirements
        intelligence_tools = ['Analyze', 'Debug', 'Optimize', 'Refactor', 'Generate']
        if any(tool in tool_name for tool in intelligence_tools):
            characteristics['requires_intelligence'] = True
        
        return characteristics
    
    def _analyze_tool_chain_context(self, context: dict) -> dict:
        """Analyze tool chain context for optimization opportunities."""
        chain_analysis = {
            'chain_length': len(context['previous_tools']),
            'pattern_detected': None,
            'optimization_opportunity': False,
            'cache_opportunity': False
        }
        
        previous_tools = context['previous_tools']
        
        if len(previous_tools) >= 2:
            # Detect common patterns
            tool_names = [tool.get('name', '') for tool in previous_tools[-3:]]
            
            # Read-Edit pattern
            if any('Read' in name for name in tool_names) and any('Edit' in name for name in tool_names):
                chain_analysis['pattern_detected'] = 'read_edit_pattern'
                chain_analysis['optimization_opportunity'] = True
            
            # Multiple file operations
            if sum(1 for name in tool_names if 'file' in name.lower()) >= 2:
                chain_analysis['pattern_detected'] = 'multi_file_pattern'
                chain_analysis['optimization_opportunity'] = True
            
            # Analysis chain
            if sum(1 for name in tool_names if any(word in name for word in ['Analyze', 'Search', 'Find'])) >= 2:
                chain_analysis['pattern_detected'] = 'analysis_chain'
                chain_analysis['cache_opportunity'] = True
        
        return chain_analysis
    
    def _analyze_tool_requirements(self, context: dict) -> dict:
        """Analyze tool requirements for capability matching."""
        requirements = {
            'capabilities_needed': [],
            'performance_requirements': {},
            'quality_requirements': {},
            'mcp_server_hints': [],
            'native_tool_sufficient': True
        }
        
        tool_name = context['tool_name']
        characteristics = context
        
        # Determine required capabilities
        if characteristics.get('requires_intelligence'):
            requirements['capabilities_needed'].extend(['analysis', 'reasoning', 'context_understanding'])
            requirements['native_tool_sufficient'] = False
        
        if characteristics.get('complexity_score', 0) > 0.6:
            requirements['capabilities_needed'].extend(['complex_reasoning', 'systematic_analysis'])
            requirements['mcp_server_hints'].append('sequential')
        
        if characteristics.get('file_count', 1) > 5:
            requirements['capabilities_needed'].extend(['multi_file_coordination', 'semantic_understanding'])
            requirements['mcp_server_hints'].append('serena')
        
        # UI/component operations
        if any(word in context.get('user_intent', '').lower() for word in ['component', 'ui', 'frontend', 'design']):
            requirements['capabilities_needed'].append('ui_generation')
            requirements['mcp_server_hints'].append('magic')
        
        # Documentation/library operations
        if any(word in context.get('user_intent', '').lower() for word in ['library', 'documentation', 'framework', 'api']):
            requirements['capabilities_needed'].append('documentation_access')
            requirements['mcp_server_hints'].append('context7')
        
        # Testing operations
        if tool_name in ['Test'] or 'test' in context.get('user_intent', '').lower():
            requirements['capabilities_needed'].append('testing_automation')
            requirements['mcp_server_hints'].append('playwright')
        
        # Performance requirements
        if characteristics.get('resource_intensive'):
            requirements['performance_requirements'] = {
                'max_execution_time_ms': 5000,
                'memory_efficiency_required': True,
                'parallel_execution_preferred': True
            }
        else:
            requirements['performance_requirements'] = {
                'max_execution_time_ms': 2000,
                'response_time_critical': True
            }
        
        # Quality requirements
        if context.get('session_context', {}).get('is_production', False):
            requirements['quality_requirements'] = {
                'validation_required': True,
                'error_handling_critical': True,
                'rollback_capability_needed': True
            }
        
        return requirements
    
    def _analyze_routing_patterns(self, context: dict, requirements: dict) -> dict:
        """Analyze patterns for intelligent routing decisions."""
        # Create operation data for pattern detection
        operation_data = {
            'operation_type': context.get('operation_type', OperationType.READ).value,
            'file_count': context.get('file_count', 1),
            'complexity_score': context.get('complexity_score', 0.0),
            'tool_name': context['tool_name']
        }
        
        # Run pattern detection
        detection_result = self.pattern_detector.detect_patterns(
            context.get('user_intent', ''),
            context,
            operation_data
        )
        
        # Create MCP activation plan
        mcp_plan = self.mcp_intelligence.create_activation_plan(
            context.get('user_intent', ''),
            context,
            operation_data
        )
        
        return {
            'pattern_matches': detection_result.matches,
            'recommended_mcp_servers': detection_result.recommended_mcp_servers,
            'mcp_activation_plan': mcp_plan,
            'routing_confidence': detection_result.confidence_score,
            'optimization_opportunities': self._identify_optimization_opportunities(context, requirements)
        }
    
    def _identify_optimization_opportunities(self, context: dict, requirements: dict) -> list:
        """Identify optimization opportunities for tool execution."""
        opportunities = []
        
        # Parallel execution opportunity
        if context.get('parallelizable') and context.get('file_count', 1) > 3:
            opportunities.append({
                'type': 'parallel_execution',
                'description': 'Multi-file operation suitable for parallel processing',
                'estimated_speedup': min(context.get('file_count', 1) * 0.3, 2.0)
            })
        
        # Caching opportunity
        if context.get('cache_opportunity'):
            opportunities.append({
                'type': 'result_caching',
                'description': 'Analysis results can be cached for reuse',
                'estimated_speedup': 1.5
            })
        
        # MCP server coordination
        if len(requirements.get('mcp_server_hints', [])) > 1:
            opportunities.append({
                'type': 'mcp_coordination',
                'description': 'Multiple MCP servers can work together',
                'quality_improvement': 0.2
            })
        
        # Intelligence routing
        if not requirements.get('native_tool_sufficient'):
            opportunities.append({
                'type': 'intelligence_routing',
                'description': 'Operation benefits from MCP server intelligence',
                'quality_improvement': 0.3
            })
        
        return opportunities
    
    def _apply_routing_adaptations(self, context: dict, routing_analysis: dict) -> dict:
        """Apply learned adaptations to routing decisions."""
        base_routing = {
            'recommended_mcp_servers': routing_analysis['recommended_mcp_servers'],
            'mcp_activation_plan': routing_analysis['mcp_activation_plan'],
            'optimization_opportunities': routing_analysis['optimization_opportunities']
        }
        
        # Apply learning engine adaptations
        enhanced_routing = self.learning_engine.apply_adaptations(context, base_routing)
        
        return enhanced_routing
    
    def _create_execution_plan(self, context: dict, enhanced_routing: dict) -> dict:
        """Create optimal execution plan for tool usage."""
        plan = {
            'execution_strategy': 'direct',
            'mcp_servers_required': enhanced_routing.get('recommended_mcp_servers', []),
            'parallel_execution': False,
            'caching_enabled': False,
            'fallback_strategy': 'native_tools',
            'performance_optimizations': [],
            'estimated_execution_time_ms': 500
        }
        
        # Determine execution strategy
        if context.get('complexity_score', 0) > 0.6:
            plan['execution_strategy'] = 'intelligent_routing'
        elif context.get('file_count', 1) > 5:
            plan['execution_strategy'] = 'parallel_coordination'
        
        # Configure parallel execution
        if context.get('parallelizable') and context.get('file_count', 1) > 3:
            plan['parallel_execution'] = True
            plan['performance_optimizations'].append('parallel_file_processing')
            plan['estimated_execution_time_ms'] = int(plan['estimated_execution_time_ms'] * 0.6)
        
        # Configure caching
        if context.get('cache_opportunity'):
            plan['caching_enabled'] = True
            plan['performance_optimizations'].append('result_caching')
        
        # Configure MCP coordination
        mcp_servers = plan['mcp_servers_required']
        if len(mcp_servers) > 1:
            plan['coordination_strategy'] = enhanced_routing.get('mcp_activation_plan', {}).get('coordination_strategy', 'collaborative')
        
        # Estimate execution time based on complexity
        base_time = 200
        complexity_multiplier = 1 + context.get('complexity_score', 0.0)
        file_multiplier = 1 + (context.get('file_count', 1) - 1) * 0.1
        
        plan['estimated_execution_time_ms'] = int(base_time * complexity_multiplier * file_multiplier)
        
        return plan
    
    def _configure_tool_enhancement(self, context: dict, execution_plan: dict) -> dict:
        """Configure tool enhancement based on execution plan."""
        tool_config = {
            'tool_name': context['tool_name'],
            'enhanced_mode': execution_plan['execution_strategy'] != 'direct',
            'mcp_integration': {
                'enabled': len(execution_plan['mcp_servers_required']) > 0,
                'servers': execution_plan['mcp_servers_required'],
                'coordination_strategy': execution_plan.get('coordination_strategy', 'single_server')
            },
            'performance_optimization': {
                'parallel_execution': execution_plan['parallel_execution'],
                'caching_enabled': execution_plan['caching_enabled'],
                'optimizations': execution_plan['performance_optimizations']
            },
            'quality_enhancement': {
                'validation_enabled': context.get('session_context', {}).get('is_production', False),
                'error_recovery': True,
                'context_preservation': True
            },
            'execution_metadata': {
                'estimated_time_ms': execution_plan['estimated_execution_time_ms'],
                'complexity_score': context.get('complexity_score', 0.0),
                'intelligence_level': self._determine_intelligence_level(context)
            }
        }
        
        # Add tool-specific enhancements
        tool_config.update(self._get_tool_specific_enhancements(context, execution_plan))
        
        return tool_config
    
    def _determine_intelligence_level(self, context: dict) -> str:
        """Determine required intelligence level for operation."""
        complexity = context.get('complexity_score', 0.0)
        
        if complexity >= 0.8:
            return 'high'
        elif complexity >= 0.5:
            return 'medium'
        elif context.get('requires_intelligence'):
            return 'medium'
        else:
            return 'low'
    
    def _get_tool_specific_enhancements(self, context: dict, execution_plan: dict) -> dict:
        """Get tool-specific enhancement configurations."""
        tool_name = context['tool_name']
        enhancements = {}
        
        # File operation enhancements
        if tool_name in ['Read', 'Write', 'Edit']:
            enhancements['file_operations'] = {
                'integrity_check': True,
                'backup_on_write': context.get('session_context', {}).get('is_production', False),
                'encoding_detection': True
            }
        
        # Multi-file operation enhancements
        if tool_name in ['MultiEdit', 'Batch'] or context.get('file_count', 1) > 3:
            enhancements['multi_file_operations'] = {
                'transaction_mode': True,
                'rollback_capability': True,
                'progress_tracking': True
            }
        
        # Analysis operation enhancements
        if tool_name in ['Analyze', 'Debug', 'Search']:
            enhancements['analysis_operations'] = {
                'deep_context_analysis': context.get('complexity_score', 0.0) > 0.5,
                'semantic_understanding': 'serena' in execution_plan['mcp_servers_required'],
                'pattern_recognition': True
            }
        
        # Build/Implementation enhancements
        if tool_name in ['Build', 'Implement', 'Generate']:
            enhancements['build_operations'] = {
                'framework_integration': 'context7' in execution_plan['mcp_servers_required'],
                'component_generation': 'magic' in execution_plan['mcp_servers_required'],
                'quality_validation': True
            }
        
        return enhancements
    
    def _calculate_efficiency_score(self, context: dict, execution_time_ms: float) -> float:
        """Calculate efficiency score for the routing decision."""
        # Base efficiency is inverse of execution time relative to target
        time_efficiency = min(self.performance_target_ms / max(execution_time_ms, 1), 1.0)
        
        # Complexity handling efficiency
        complexity = context.get('complexity_score', 0.0)
        complexity_efficiency = 1.0 - (complexity * 0.3)  # Some complexity is expected
        
        # Resource utilization efficiency
        resource_usage = context.get('resource_state', {}).get('usage_percent', 0)
        resource_efficiency = 1.0 - max(resource_usage - 70, 0) / 100.0
        
        # Weighted efficiency score
        efficiency_score = (time_efficiency * 0.4 + 
                          complexity_efficiency * 0.3 + 
                          resource_efficiency * 0.3)
        
        return max(min(efficiency_score, 1.0), 0.0)
    
    def _record_tool_learning(self, context: dict, tool_config: dict):
        """Record tool usage for learning purposes."""
        self.learning_engine.record_learning_event(
            LearningType.OPERATION_PATTERN,
            AdaptationScope.USER,
            context,
            {
                'tool_name': context['tool_name'],
                'mcp_servers_used': tool_config.get('mcp_integration', {}).get('servers', []),
                'execution_strategy': tool_config.get('execution_metadata', {}).get('intelligence_level', 'low'),
                'optimizations_applied': tool_config.get('performance_optimization', {}).get('optimizations', [])
            },
            0.8,  # Assume good effectiveness (will be updated later)
            0.7,  # Medium confidence until validated
            {'hook': 'pre_tool_use', 'version': '1.0'}
        )
    
    def _create_fallback_tool_config(self, tool_request: dict, error: str) -> dict:
        """Create fallback tool configuration on error."""
        return {
            'tool_name': tool_request.get('tool_name', 'unknown'),
            'enhanced_mode': False,
            'fallback_mode': True,
            'error': error,
            'mcp_integration': {
                'enabled': False,
                'servers': [],
                'coordination_strategy': 'none'
            },
            'performance_optimization': {
                'parallel_execution': False,
                'caching_enabled': False,
                'optimizations': []
            },
            'performance_metrics': {
                'routing_time_ms': 0,
                'target_met': False,
                'error_occurred': True
            }
        }


def main():
    """Main hook execution function."""
    try:
        # Read tool request from stdin
        tool_request = json.loads(sys.stdin.read())
        
        # Initialize and run hook
        hook = PreToolUseHook()
        result = hook.process_tool_use(tool_request)
        
        # Output result as JSON
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        # Output error as JSON
        error_result = {
            'enhanced_mode': False,
            'error': str(e),
            'fallback_mode': True
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()