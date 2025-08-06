#!/usr/bin/env python3
"""
Comprehensive tests for mcp_intelligence.py

Tests all core functionality including:
- MCP server selection logic and optimization
- Activation plan creation and execution
- Hybrid intelligence coordination (Morphllm vs Serena)
- Performance estimation and fallback strategies
- Real-time adaptation and effectiveness tracking
"""

import unittest
import sys
import time
from pathlib import Path

# Add the shared directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_intelligence import (
    MCPIntelligence, MCPServerState, MCPServerCapability, 
    MCPActivationPlan
)


class TestMCPIntelligence(unittest.TestCase):
    """Comprehensive tests for MCPIntelligence."""
    
    def setUp(self):
        """Set up test environment."""
        self.mcp = MCPIntelligence()
        
        # Test contexts
        self.simple_context = {
            'resource_usage_percent': 30,
            'conversation_length': 20,
            'user_expertise': 'intermediate'
        }
        
        self.complex_context = {
            'resource_usage_percent': 70,
            'conversation_length': 100,
            'user_expertise': 'expert'
        }
        
        # Test operation data
        self.simple_operation = {
            'operation_type': 'read',
            'file_count': 2,
            'complexity_score': 0.3,
            'has_external_dependencies': False
        }
        
        self.complex_operation = {
            'operation_type': 'refactor',
            'file_count': 15,
            'complexity_score': 0.8,
            'has_external_dependencies': True
        }
    
    def test_server_capabilities_loading(self):
        """Test that server capabilities are loaded correctly."""
        # Should have all expected servers
        expected_servers = ['context7', 'sequential', 'magic', 'playwright', 'morphllm', 'serena']
        
        for server in expected_servers:
            self.assertIn(server, self.mcp.server_capabilities)
            capability = self.mcp.server_capabilities[server]
            self.assertIsInstance(capability, MCPServerCapability)
            
            # Should have valid properties
            self.assertIsInstance(capability.primary_functions, list)
            self.assertGreater(len(capability.primary_functions), 0)
            self.assertIsInstance(capability.activation_cost_ms, int)
            self.assertGreater(capability.activation_cost_ms, 0)
            self.assertIsInstance(capability.token_efficiency, float)
            self.assertGreaterEqual(capability.token_efficiency, 0.0)
            self.assertLessEqual(capability.token_efficiency, 1.0)
    
    def test_server_state_initialization(self):
        """Test server state initialization."""
        # All servers should start as available
        for server in self.mcp.server_capabilities:
            self.assertEqual(self.mcp.server_states[server], MCPServerState.AVAILABLE)
    
    def test_activation_plan_creation_simple(self):
        """Test activation plan creation for simple operations."""
        user_input = "Read this file and analyze its structure"
        
        plan = self.mcp.create_activation_plan(
            user_input, self.simple_context, self.simple_operation
        )
        
        self.assertIsInstance(plan, MCPActivationPlan)
        self.assertIsInstance(plan.servers_to_activate, list)
        self.assertIsInstance(plan.activation_order, list)
        self.assertIsInstance(plan.estimated_cost_ms, int)
        self.assertIsInstance(plan.efficiency_gains, dict)
        self.assertIsInstance(plan.fallback_strategy, dict)
        self.assertIsInstance(plan.coordination_strategy, str)
        
        # Simple operations should prefer lightweight servers
        self.assertGreater(len(plan.servers_to_activate), 0)
        self.assertGreater(plan.estimated_cost_ms, 0)
    
    def test_activation_plan_creation_complex(self):
        """Test activation plan creation for complex operations."""
        user_input = "Refactor this entire codebase architecture and update all components"
        
        plan = self.mcp.create_activation_plan(
            user_input, self.complex_context, self.complex_operation
        )
        
        # Complex operations should activate more servers
        self.assertGreaterEqual(len(plan.servers_to_activate), 2)
        
        # Should include appropriate servers for complex operations
        servers = plan.servers_to_activate
        # Either Serena or Sequential should be included for complex analysis
        self.assertTrue('serena' in servers or 'sequential' in servers)
        
        # Should have higher estimated cost
        self.assertGreater(plan.estimated_cost_ms, 100)
    
    def test_morphllm_vs_serena_intelligence(self):
        """Test hybrid intelligence selection between Morphllm and Serena."""
        # Simple operation should prefer Morphllm
        simple_operation = {
            'operation_type': 'edit',
            'file_count': 3,
            'complexity_score': 0.4
        }
        
        simple_servers = self.mcp._optimize_server_selection(
            ['morphllm', 'serena'], self.simple_context, simple_operation
        )
        
        # Should prefer Morphllm for simple operations
        self.assertIn('morphllm', simple_servers)
        self.assertNotIn('serena', simple_servers)
        
        # Complex operation should prefer Serena
        complex_operation = {
            'operation_type': 'refactor',
            'file_count': 15,
            'complexity_score': 0.7
        }
        
        complex_servers = self.mcp._optimize_server_selection(
            ['morphllm', 'serena'], self.complex_context, complex_operation
        )
        
        # Should prefer Serena for complex operations
        self.assertIn('serena', complex_servers)
        self.assertNotIn('morphllm', complex_servers)
    
    def test_resource_constraint_optimization(self):
        """Test server selection under resource constraints."""
        high_resource_context = {
            'resource_usage_percent': 90,
            'conversation_length': 200
        }
        
        # Should remove intensive servers under constraints
        recommended_servers = ['sequential', 'playwright', 'magic', 'morphllm']
        optimized_servers = self.mcp._optimize_server_selection(
            recommended_servers, high_resource_context, self.simple_operation
        )
        
        # Should remove intensive servers (sequential, playwright)
        intensive_servers = ['sequential', 'playwright']
        for server in intensive_servers:
            capability = self.mcp.server_capabilities[server]
            if capability.performance_profile == 'intensive':
                self.assertNotIn(server, optimized_servers)
    
    def test_external_dependencies_detection(self):
        """Test auto-activation of Context7 for external dependencies."""
        operation_with_deps = {
            'operation_type': 'implement',
            'file_count': 5,
            'complexity_score': 0.5,
            'has_external_dependencies': True
        }
        
        optimized_servers = self.mcp._optimize_server_selection(
            ['morphllm'], self.simple_context, operation_with_deps
        )
        
        # Should auto-add Context7 for external dependencies
        self.assertIn('context7', optimized_servers)
    
    def test_activation_order_calculation(self):
        """Test optimal activation order calculation."""
        servers = ['serena', 'context7', 'sequential', 'morphllm']
        
        order = self.mcp._calculate_activation_order(servers, self.simple_context)
        
        # Serena should be first (provides context)
        self.assertEqual(order[0], 'serena')
        
        # Context7 should be second (provides documentation context)
        if 'context7' in order:
            serena_index = order.index('serena')
            context7_index = order.index('context7')
            self.assertLess(serena_index, context7_index)
        
        # Should maintain all servers
        self.assertEqual(set(order), set(servers))
    
    def test_activation_cost_calculation(self):
        """Test activation cost calculation."""
        servers = ['morphllm', 'magic', 'context7']
        
        cost = self.mcp._calculate_activation_cost(servers)
        
        # Should sum individual server costs
        expected_cost = sum(
            self.mcp.server_capabilities[server].activation_cost_ms
            for server in servers
        )
        
        self.assertEqual(cost, expected_cost)
        self.assertGreater(cost, 0)
    
    def test_efficiency_gains_calculation(self):
        """Test efficiency gains calculation."""
        servers = ['morphllm', 'serena', 'sequential']
        
        gains = self.mcp._calculate_efficiency_gains(servers, self.simple_operation)
        
        # Should return gains for each server
        for server in servers:
            self.assertIn(server, gains)
            self.assertIsInstance(gains[server], float)
            self.assertGreater(gains[server], 0.0)
            self.assertLessEqual(gains[server], 2.0)  # Reasonable upper bound
        
        # Morphllm should have higher efficiency for simple operations
        if 'morphllm' in gains and len([s for s in servers if s in gains]) > 1:
            morphllm_gain = gains['morphllm']
            other_gains = [gains[s] for s in gains if s != 'morphllm']
            if other_gains:
                avg_other_gain = sum(other_gains) / len(other_gains)
                # Morphllm should be competitive for simple operations
                self.assertGreaterEqual(morphllm_gain, avg_other_gain * 0.8)
    
    def test_fallback_strategy_creation(self):
        """Test fallback strategy creation."""
        servers = ['sequential', 'morphllm', 'magic']
        
        fallbacks = self.mcp._create_fallback_strategy(servers)
        
        # Should have fallback for each server
        for server in servers:
            self.assertIn(server, fallbacks)
            fallback = fallbacks[server]
            
            # Fallback should be different from original server
            self.assertNotEqual(fallback, server)
            
            # Should be either a valid server or native_tools
            if fallback != 'native_tools':
                self.assertIn(fallback, self.mcp.server_capabilities)
    
    def test_coordination_strategy_determination(self):
        """Test coordination strategy determination."""
        # Single server should use single_server strategy
        single_strategy = self.mcp._determine_coordination_strategy(['morphllm'], self.simple_operation)
        self.assertEqual(single_strategy, 'single_server')
        
        # Sequential with high complexity should lead
        sequential_servers = ['sequential', 'context7']
        sequential_strategy = self.mcp._determine_coordination_strategy(
            sequential_servers, self.complex_operation
        )
        self.assertEqual(sequential_strategy, 'sequential_lead')
        
        # Serena with many files should lead
        serena_servers = ['serena', 'morphllm']
        multi_file_operation = {
            'operation_type': 'refactor',
            'file_count': 10,
            'complexity_score': 0.6
        }
        serena_strategy = self.mcp._determine_coordination_strategy(
            serena_servers, multi_file_operation
        )
        self.assertEqual(serena_strategy, 'serena_lead')
        
        # Many servers should use parallel coordination
        many_servers = ['sequential', 'context7', 'morphllm', 'magic']
        parallel_strategy = self.mcp._determine_coordination_strategy(
            many_servers, self.simple_operation
        )
        self.assertEqual(parallel_strategy, 'parallel_with_sync')
    
    def test_activation_plan_execution(self):
        """Test activation plan execution with performance tracking."""
        plan = self.mcp.create_activation_plan(
            "Test user input", self.simple_context, self.simple_operation
        )
        
        result = self.mcp.execute_activation_plan(plan, self.simple_context)
        
        # Should return execution results
        self.assertIn('activated_servers', result)
        self.assertIn('failed_servers', result)
        self.assertIn('fallback_activations', result)
        self.assertIn('total_activation_time_ms', result)
        self.assertIn('coordination_strategy', result)
        self.assertIn('performance_metrics', result)
        
        # Should have activated some servers (simulated)
        self.assertIsInstance(result['activated_servers'], list)
        self.assertIsInstance(result['failed_servers'], list)
        self.assertIsInstance(result['total_activation_time_ms'], float)
        
        # Should track performance metrics
        self.assertIsInstance(result['performance_metrics'], dict)
    
    def test_server_failure_handling(self):
        """Test handling of server activation failures."""
        # Manually set a server as unavailable
        self.mcp.server_states['sequential'] = MCPServerState.UNAVAILABLE
        
        plan = MCPActivationPlan(
            servers_to_activate=['sequential', 'morphllm'],
            activation_order=['sequential', 'morphllm'],
            estimated_cost_ms=300,
            efficiency_gains={'sequential': 0.8, 'morphllm': 0.7},
            fallback_strategy={'sequential': 'context7', 'morphllm': 'serena'},
            coordination_strategy='collaborative'
        )
        
        result = self.mcp.execute_activation_plan(plan, self.simple_context)
        
        # Sequential should be in failed servers
        self.assertIn('sequential', result['failed_servers'])
        
        # Should have attempted fallback activation
        if len(result['fallback_activations']) > 0:
            fallback_text = ' '.join(result['fallback_activations'])
            self.assertIn('sequential', fallback_text)
    
    def test_optimization_recommendations(self):
        """Test optimization recommendations generation."""
        # Create some activation history first
        for i in range(6):
            plan = self.mcp.create_activation_plan(
                f"Test operation {i}", self.simple_context, self.simple_operation
            )
            self.mcp.execute_activation_plan(plan, self.simple_context)
        
        recommendations = self.mcp.get_optimization_recommendations(self.simple_context)
        
        self.assertIn('recommendations', recommendations)
        self.assertIn('performance_metrics', recommendations)
        self.assertIn('server_states', recommendations)
        self.assertIn('efficiency_score', recommendations)
        
        self.assertIsInstance(recommendations['recommendations'], list)
        self.assertIsInstance(recommendations['efficiency_score'], float)
        self.assertGreaterEqual(recommendations['efficiency_score'], 0.0)
    
    def test_tool_to_server_mapping(self):
        """Test tool-to-server mapping functionality."""
        # Test common tool mappings
        test_cases = [
            ('read_file', 'morphllm'),
            ('write_file', 'morphllm'),
            ('analyze_architecture', 'sequential'),
            ('create_component', 'magic'),
            ('browser_test', 'playwright'),
            ('get_documentation', 'context7'),
            ('semantic_analysis', 'serena')
        ]
        
        for tool_name, expected_server in test_cases:
            server = self.mcp.select_optimal_server(tool_name, self.simple_context)
            self.assertEqual(server, expected_server)
        
        # Test context-based selection for unknown tools
        high_complexity_context = {'complexity': 'high'}
        server = self.mcp.select_optimal_server('unknown_tool', high_complexity_context)
        self.assertEqual(server, 'sequential')
        
        ui_context = {'type': 'ui'}
        server = self.mcp.select_optimal_server('unknown_ui_tool', ui_context)
        self.assertEqual(server, 'magic')
    
    def test_fallback_server_selection(self):
        """Test fallback server selection."""
        test_cases = [
            ('read_file', 'morphllm', 'context7'),  # morphllm -> context7 -> morphllm (avoid circular)
            ('analyze_architecture', 'sequential', 'serena'),
            ('create_component', 'magic', 'morphllm'),
            ('browser_test', 'playwright', 'sequential')
        ]
        
        for tool_name, expected_primary, expected_fallback in test_cases:
            primary = self.mcp.select_optimal_server(tool_name, self.simple_context)
            fallback = self.mcp.get_fallback_server(tool_name, self.simple_context)
            
            self.assertEqual(primary, expected_primary)
            self.assertEqual(fallback, expected_fallback)
            
            # Fallback should be different from primary
            self.assertNotEqual(primary, fallback)
    
    def test_performance_targets(self):
        """Test that operations meet performance targets."""
        start_time = time.time()
        
        # Create and execute multiple plans quickly
        for i in range(10):
            plan = self.mcp.create_activation_plan(
                f"Performance test {i}", self.simple_context, self.simple_operation
            )
            
            result = self.mcp.execute_activation_plan(plan, self.simple_context)
            
            # Each operation should complete reasonably quickly
            self.assertLess(result['total_activation_time_ms'], 1000)  # < 1 second
        
        total_time = time.time() - start_time
        
        # All 10 operations should complete in reasonable time
        self.assertLess(total_time, 5.0)  # < 5 seconds total
    
    def test_efficiency_score_calculation(self):
        """Test overall efficiency score calculation."""
        # Initially should have reasonable efficiency
        initial_efficiency = self.mcp._calculate_overall_efficiency()
        self.assertGreaterEqual(initial_efficiency, 0.0)
        self.assertLessEqual(initial_efficiency, 2.0)
        
        # Add some performance metrics
        self.mcp.performance_metrics['test_server'] = {
            'efficiency_ratio': 1.5,
            'last_activation_ms': 100,
            'expected_ms': 150
        }
        
        efficiency_with_data = self.mcp._calculate_overall_efficiency()
        self.assertGreater(efficiency_with_data, 0.0)
        self.assertLessEqual(efficiency_with_data, 2.0)
    
    def test_edge_cases_and_error_handling(self):
        """Test edge cases and error handling."""
        # Empty server list
        empty_plan = MCPActivationPlan(
            servers_to_activate=[],
            activation_order=[],
            estimated_cost_ms=0,
            efficiency_gains={},
            fallback_strategy={},
            coordination_strategy='single_server'
        )
        
        result = self.mcp.execute_activation_plan(empty_plan, self.simple_context)
        self.assertEqual(len(result['activated_servers']), 0)
        self.assertEqual(result['total_activation_time_ms'], 0.0)
        
        # Unknown server
        cost = self.mcp._calculate_activation_cost(['unknown_server'])
        self.assertEqual(cost, 0)
        
        # Empty context
        plan = self.mcp.create_activation_plan("", {}, {})
        self.assertIsInstance(plan, MCPActivationPlan)
        
        # Very large file count
        extreme_operation = {
            'operation_type': 'process',
            'file_count': 10000,
            'complexity_score': 1.0
        }
        
        plan = self.mcp.create_activation_plan(
            "Process everything", self.simple_context, extreme_operation
        )
        self.assertIsInstance(plan, MCPActivationPlan)
        
        # Should handle gracefully
        self.assertGreater(len(plan.servers_to_activate), 0)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)