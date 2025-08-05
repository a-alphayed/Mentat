"""
MCP Intelligence Engine for SuperClaude-Lite

Intelligent MCP server activation, coordination, and optimization based on
ORCHESTRATOR.md patterns and real-time context analysis.
"""

import json
import time
from typing import Dict, Any, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum

from yaml_loader import config_loader
from pattern_detection import PatternDetector, PatternMatch


class MCPServerState(Enum):
    """States of MCP server availability."""
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    LOADING = "loading"
    ERROR = "error"


@dataclass
class MCPServerCapability:
    """Capability definition for an MCP server."""
    server_name: str
    primary_functions: List[str]
    performance_profile: str  # lightweight, standard, intensive
    activation_cost_ms: int
    token_efficiency: float  # 0.0 to 1.0
    quality_impact: float   # 0.0 to 1.0


@dataclass
class MCPActivationPlan:
    """Plan for MCP server activation."""
    servers_to_activate: List[str]
    activation_order: List[str]
    estimated_cost_ms: int
    efficiency_gains: Dict[str, float]
    fallback_strategy: Dict[str, str]
    coordination_strategy: str


class MCPIntelligence:
    """
    Intelligent MCP server management and coordination.
    
    Implements ORCHESTRATOR.md patterns for:
    - Smart server selection based on context
    - Performance-optimized activation sequences
    - Fallback strategies for server failures
    - Cross-server coordination and caching
    - Real-time adaptation based on effectiveness
    """
    
    def __init__(self):
        self.pattern_detector = PatternDetector()
        self.server_capabilities = self._load_server_capabilities()
        self.server_states = self._initialize_server_states()
        self.activation_history = []
        self.performance_metrics = {}
        
    def _load_server_capabilities(self) -> Dict[str, MCPServerCapability]:
        """Load MCP server capabilities from configuration."""
        config = config_loader.load_config('orchestrator')
        capabilities = {}
        
        servers_config = config.get('mcp_servers', {})
        
        capabilities['context7'] = MCPServerCapability(
            server_name='context7',
            primary_functions=['library_docs', 'framework_patterns', 'best_practices'],
            performance_profile='standard',
            activation_cost_ms=150,
            token_efficiency=0.8,
            quality_impact=0.9
        )
        
        capabilities['sequential'] = MCPServerCapability(
            server_name='sequential',
            primary_functions=['complex_analysis', 'multi_step_reasoning', 'debugging'],
            performance_profile='intensive',
            activation_cost_ms=200,
            token_efficiency=0.6,
            quality_impact=0.95
        )
        
        capabilities['magic'] = MCPServerCapability(
            server_name='magic',
            primary_functions=['ui_components', 'design_systems', 'frontend_generation'],
            performance_profile='standard',
            activation_cost_ms=120,
            token_efficiency=0.85,
            quality_impact=0.9
        )
        
        capabilities['playwright'] = MCPServerCapability(
            server_name='playwright',
            primary_functions=['e2e_testing', 'browser_automation', 'performance_testing'],
            performance_profile='intensive',
            activation_cost_ms=300,
            token_efficiency=0.7,
            quality_impact=0.85
        )
        
        capabilities['morphllm'] = MCPServerCapability(
            server_name='morphllm',
            primary_functions=['intelligent_editing', 'pattern_application', 'fast_apply'],
            performance_profile='lightweight',
            activation_cost_ms=80,
            token_efficiency=0.9,
            quality_impact=0.8
        )
        
        capabilities['serena'] = MCPServerCapability(
            server_name='serena',
            primary_functions=['semantic_analysis', 'project_context', 'memory_management'],
            performance_profile='standard',
            activation_cost_ms=100,
            token_efficiency=0.75,
            quality_impact=0.95
        )
        
        return capabilities
    
    def _initialize_server_states(self) -> Dict[str, MCPServerState]:
        """Initialize server state tracking."""
        return {
            server: MCPServerState.AVAILABLE 
            for server in self.server_capabilities.keys()
        }
    
    def create_activation_plan(self, 
                             user_input: str, 
                             context: Dict[str, Any], 
                             operation_data: Dict[str, Any]) -> MCPActivationPlan:
        """
        Create intelligent MCP server activation plan.
        
        Args:
            user_input: User's request or command
            context: Session and environment context
            operation_data: Information about the planned operation
            
        Returns:
            MCPActivationPlan with optimized server selection and coordination
        """
        # Detect patterns to determine server needs
        detection_result = self.pattern_detector.detect_patterns(
            user_input, context, operation_data
        )
        
        # Extract recommended servers from pattern detection
        recommended_servers = detection_result.recommended_mcp_servers
        
        # Apply intelligent selection based on context
        optimized_servers = self._optimize_server_selection(
            recommended_servers, context, operation_data
        )
        
        # Determine activation order for optimal performance
        activation_order = self._calculate_activation_order(optimized_servers, context)
        
        # Calculate estimated costs and gains
        estimated_cost = self._calculate_activation_cost(optimized_servers)
        efficiency_gains = self._calculate_efficiency_gains(optimized_servers, operation_data)
        
        # Create fallback strategy
        fallback_strategy = self._create_fallback_strategy(optimized_servers)
        
        # Determine coordination strategy
        coordination_strategy = self._determine_coordination_strategy(
            optimized_servers, operation_data
        )
        
        return MCPActivationPlan(
            servers_to_activate=optimized_servers,
            activation_order=activation_order,
            estimated_cost_ms=estimated_cost,
            efficiency_gains=efficiency_gains,
            fallback_strategy=fallback_strategy,
            coordination_strategy=coordination_strategy
        )
    
    def _optimize_server_selection(self, 
                                 recommended_servers: List[str], 
                                 context: Dict[str, Any], 
                                 operation_data: Dict[str, Any]) -> List[str]:
        """Apply intelligent optimization to server selection."""
        optimized = set(recommended_servers)
        
        # Morphllm vs Serena intelligence selection
        file_count = operation_data.get('file_count', 1)
        complexity_score = operation_data.get('complexity_score', 0.0)
        
        if 'morphllm' in optimized and 'serena' in optimized:
            # Choose the more appropriate server based on complexity
            if file_count > 10 or complexity_score > 0.6:
                optimized.remove('morphllm')  # Use Serena for complex operations
            else:
                optimized.remove('serena')    # Use Morphllm for efficient operations
        elif file_count > 10 or complexity_score > 0.6:
            # Auto-add Serena for complex operations
            optimized.add('serena')
            optimized.discard('morphllm')
        elif file_count <= 10 and complexity_score <= 0.6:
            # Auto-add Morphllm for simple operations
            optimized.add('morphllm')
            optimized.discard('serena')
        
        # Resource constraint optimization
        resource_usage = context.get('resource_usage_percent', 0)
        if resource_usage > 85:
            # Remove intensive servers under resource constraints
            intensive_servers = {
                name for name, cap in self.server_capabilities.items()
                if cap.performance_profile == 'intensive'
            }
            optimized -= intensive_servers
        
        # Performance optimization based on operation type
        operation_type = operation_data.get('operation_type', '')
        if operation_type in ['read', 'analyze'] and 'sequential' not in optimized:
            # Add Sequential for analysis operations
            optimized.add('sequential')
        
        # Auto-add Context7 if external libraries detected
        if operation_data.get('has_external_dependencies', False):
            optimized.add('context7')
        
        return list(optimized)
    
    def _calculate_activation_order(self, servers: List[str], context: Dict[str, Any]) -> List[str]:
        """Calculate optimal activation order for performance."""
        if not servers:
            return []
        
        # Sort by activation cost (lightweight first)
        server_costs = [
            (server, self.server_capabilities[server].activation_cost_ms)
            for server in servers
        ]
        server_costs.sort(key=lambda x: x[1])
        
        # Special ordering rules
        ordered = []
        
        # 1. Serena first if present (provides context for others)
        if 'serena' in servers:
            ordered.append('serena')
            servers = [s for s in servers if s != 'serena']
        
        # 2. Context7 early for documentation context
        if 'context7' in servers:
            ordered.append('context7')
            servers = [s for s in servers if s != 'context7']
        
        # 3. Remaining servers by cost
        remaining_costs = [
            (server, self.server_capabilities[server].activation_cost_ms)
            for server in servers
        ]
        remaining_costs.sort(key=lambda x: x[1])
        ordered.extend([server for server, _ in remaining_costs])
        
        return ordered
    
    def _calculate_activation_cost(self, servers: List[str]) -> int:
        """Calculate total activation cost in milliseconds."""
        return sum(
            self.server_capabilities[server].activation_cost_ms
            for server in servers
            if server in self.server_capabilities
        )
    
    def _calculate_efficiency_gains(self, servers: List[str], operation_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate expected efficiency gains from server activation."""
        gains = {}
        
        for server in servers:
            if server not in self.server_capabilities:
                continue
                
            capability = self.server_capabilities[server]
            
            # Base efficiency gain
            base_gain = capability.token_efficiency * capability.quality_impact
            
            # Context-specific adjustments
            if server == 'morphllm' and operation_data.get('file_count', 1) <= 5:
                gains[server] = base_gain * 1.2  # Extra efficient for small operations
            elif server == 'serena' and operation_data.get('complexity_score', 0) > 0.6:
                gains[server] = base_gain * 1.3  # Extra valuable for complex operations
            elif server == 'sequential' and 'debug' in operation_data.get('operation_type', ''):
                gains[server] = base_gain * 1.4  # Extra valuable for debugging
            else:
                gains[server] = base_gain
        
        return gains
    
    def _create_fallback_strategy(self, servers: List[str]) -> Dict[str, str]:
        """Create fallback strategy for server failures."""
        fallbacks = {}
        
        # Define fallback mappings
        fallback_map = {
            'morphllm': 'serena',      # Serena can handle editing
            'serena': 'morphllm',      # Morphllm can handle simple edits
            'sequential': 'context7',   # Context7 for documentation-based analysis
            'context7': 'sequential',   # Sequential for complex analysis
            'magic': 'morphllm',       # Morphllm for component generation
            'playwright': 'sequential'  # Sequential for test planning
        }
        
        for server in servers:
            fallback = fallback_map.get(server)
            if fallback and fallback not in servers:
                fallbacks[server] = fallback
            else:
                fallbacks[server] = 'native_tools'  # Fall back to native Claude tools
        
        return fallbacks
    
    def _determine_coordination_strategy(self, servers: List[str], operation_data: Dict[str, Any]) -> str:
        """Determine how servers should coordinate."""
        if len(servers) <= 1:
            return 'single_server'
        
        # Sequential coordination for complex analysis
        if 'sequential' in servers and operation_data.get('complexity_score', 0) > 0.6:
            return 'sequential_lead'
        
        # Serena coordination for multi-file operations
        if 'serena' in servers and operation_data.get('file_count', 1) > 5:
            return 'serena_lead'
        
        # Parallel coordination for independent operations
        if len(servers) >= 3:
            return 'parallel_with_sync'
        
        return 'collaborative'
    
    def execute_activation_plan(self, plan: MCPActivationPlan, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute MCP server activation plan with error handling and performance tracking.
        
        Args:
            plan: MCPActivationPlan to execute
            context: Current session context
            
        Returns:
            Execution results with performance metrics and activated servers
        """
        start_time = time.time()
        activated_servers = []
        failed_servers = []
        fallback_activations = []
        
        for server in plan.activation_order:
            try:
                # Check server availability
                if self.server_states.get(server) == MCPServerState.UNAVAILABLE:
                    failed_servers.append(server)
                    self._handle_server_fallback(server, plan, fallback_activations)
                    continue
                
                # Activate server (simulated - real implementation would call MCP)
                self.server_states[server] = MCPServerState.LOADING
                activation_start = time.time()
                
                # Simulate activation time
                expected_cost = self.server_capabilities[server].activation_cost_ms
                actual_cost = expected_cost * (0.8 + 0.4 * hash(server) % 1000 / 1000)  # Simulated variance
                
                self.server_states[server] = MCPServerState.AVAILABLE
                activated_servers.append(server)
                
                # Track performance
                activation_time = (time.time() - activation_start) * 1000
                self.performance_metrics[server] = {
                    'last_activation_ms': activation_time,
                    'expected_ms': expected_cost,
                    'efficiency_ratio': expected_cost / max(activation_time, 1)
                }
                
            except Exception as e:
                failed_servers.append(server)
                self.server_states[server] = MCPServerState.ERROR
                self._handle_server_fallback(server, plan, fallback_activations)
        
        total_time = (time.time() - start_time) * 1000
        
        # Update activation history
        self.activation_history.append({
            'timestamp': time.time(),
            'plan': plan,
            'activated': activated_servers,
            'failed': failed_servers,
            'fallbacks': fallback_activations,
            'total_time_ms': total_time
        })
        
        return {
            'activated_servers': activated_servers,
            'failed_servers': failed_servers,
            'fallback_activations': fallback_activations,
            'total_activation_time_ms': total_time,
            'coordination_strategy': plan.coordination_strategy,
            'performance_metrics': self.performance_metrics
        }
    
    def _handle_server_fallback(self, failed_server: str, plan: MCPActivationPlan, fallback_activations: List[str]):
        """Handle server activation failure with fallback strategy."""
        fallback = plan.fallback_strategy.get(failed_server)
        
        if fallback and fallback != 'native_tools' and fallback not in plan.servers_to_activate:
            # Try to activate fallback server
            if self.server_states.get(fallback) == MCPServerState.AVAILABLE:
                fallback_activations.append(f"{failed_server}->{fallback}")
                # In real implementation, would activate fallback server
    
    def get_optimization_recommendations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get recommendations for optimizing MCP server usage."""
        recommendations = []
        
        # Analyze activation history for patterns
        if len(self.activation_history) >= 5:
            recent_activations = self.activation_history[-5:]
            
            # Check for frequently failing servers
            failed_counts = {}
            for activation in recent_activations:
                for failed in activation['failed']:
                    failed_counts[failed] = failed_counts.get(failed, 0) + 1
            
            for server, count in failed_counts.items():
                if count >= 3:
                    recommendations.append(f"Server {server} failing frequently - consider fallback strategy")
            
            # Check for performance issues
            avg_times = {}
            for activation in recent_activations:
                total_time = activation['total_time_ms']
                server_count = len(activation['activated'])
                if server_count > 0:
                    avg_time_per_server = total_time / server_count
                    avg_times[len(activation['activated'])] = avg_time_per_server
            
            if avg_times and max(avg_times.values()) > 500:
                recommendations.append("Consider reducing concurrent server activations for better performance")
        
        # Resource usage recommendations
        resource_usage = context.get('resource_usage_percent', 0)
        if resource_usage > 80:
            recommendations.append("High resource usage - consider lightweight servers only")
        
        return {
            'recommendations': recommendations,
            'performance_metrics': self.performance_metrics,
            'server_states': {k: v.value for k, v in self.server_states.items()},
            'efficiency_score': self._calculate_overall_efficiency()
        }
    
    def _calculate_overall_efficiency(self) -> float:
        """Calculate overall MCP system efficiency."""
        if not self.performance_metrics:
            return 1.0
        
        efficiency_scores = []
        for server, metrics in self.performance_metrics.items():
            efficiency_ratio = metrics.get('efficiency_ratio', 1.0)
            efficiency_scores.append(min(efficiency_ratio, 2.0))  # Cap at 200% efficiency
        
        return sum(efficiency_scores) / len(efficiency_scores) if efficiency_scores else 1.0
    
    def select_optimal_server(self, tool_name: str, context: Dict[str, Any]) -> str:
        """
        Select the most appropriate MCP server for a given tool and context.
        
        Args:
            tool_name: Name of the tool to be executed
            context: Context information for intelligent selection
            
        Returns:
            Name of the optimal server for the tool
        """
        # Map common tools to server capabilities
        tool_server_mapping = {
            'read_file': 'morphllm',
            'write_file': 'morphllm', 
            'edit_file': 'morphllm',
            'analyze_architecture': 'sequential',
            'complex_reasoning': 'sequential',
            'debug_analysis': 'sequential',
            'create_component': 'magic',
            'ui_component': 'magic',
            'design_system': 'magic',
            'browser_test': 'playwright',
            'e2e_test': 'playwright',
            'performance_test': 'playwright',
            'get_documentation': 'context7',
            'library_docs': 'context7',
            'framework_patterns': 'context7',
            'semantic_analysis': 'serena',
            'project_context': 'serena',
            'memory_management': 'serena'
        }
        
        # Primary server selection based on tool
        primary_server = tool_server_mapping.get(tool_name)
        
        if primary_server:
            return primary_server
            
        # Context-based selection for unknown tools
        if context.get('complexity', 'low') == 'high':
            return 'sequential'
        elif context.get('type') == 'ui':
            return 'magic' 
        elif context.get('type') == 'browser':
            return 'playwright'
        elif context.get('file_count', 1) > 10:
            return 'serena'
        else:
            return 'morphllm'  # Default fallback
    
    def get_fallback_server(self, tool_name: str, context: Dict[str, Any]) -> str:
        """
        Get fallback server when primary server fails.
        
        Args:
            tool_name: Name of the tool
            context: Context information
            
        Returns:
            Name of the fallback server
        """
        primary_server = self.select_optimal_server(tool_name, context)
        
        # Define fallback chains
        fallback_chains = {
            'sequential': 'serena',
            'serena': 'morphllm',
            'morphllm': 'context7',
            'magic': 'morphllm',
            'playwright': 'sequential',
            'context7': 'morphllm'
        }
        
        fallback = fallback_chains.get(primary_server, 'morphllm')
        
        # Avoid circular fallback
        if fallback == primary_server:
            return 'morphllm'
            
        return fallback