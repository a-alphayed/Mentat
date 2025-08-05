#!/usr/bin/env python3
"""
Live test of MCP Intelligence module with real scenarios
"""

import sys
import os
import json
from pathlib import Path

# Add shared modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../.claude/hooks/shared'))

from mcp_intelligence import MCPIntelligence
from yaml_loader import UnifiedConfigLoader, config_loader

def test_mcp_intelligence_live():
    """Test MCP intelligence with real-world scenarios"""
    print("🧪 Testing MCP Intelligence Module - Live Scenarios\n")
    
    # Initialize MCP Intelligence
    mcp = MCPIntelligence()
    
    # Test scenarios
    scenarios = [
        {
            "name": "UI Component Creation",
            "context": {
                "tool_name": "build",
                "user_intent": "create a login form with validation",
                "operation_type": "ui_component"
            },
            "expected_servers": ["magic"]
        },
        {
            "name": "Complex Debugging",
            "context": {
                "tool_name": "analyze",
                "user_intent": "debug why the application is slow",
                "complexity_score": 0.8,
                "operation_type": "debugging"
            },
            "expected_servers": ["sequential", "morphllm"]
        },
        {
            "name": "Library Integration",
            "context": {
                "tool_name": "implement",
                "user_intent": "integrate React Query for data fetching",
                "has_external_dependencies": True,
                "operation_type": "library_integration"
            },
            "expected_servers": ["context7", "morphllm"]
        },
        {
            "name": "Large File Refactoring",
            "context": {
                "tool_name": "refactor",
                "file_count": 15,
                "operation_type": "refactoring",
                "complexity_score": 0.6
            },
            "expected_servers": ["serena", "morphllm"]
        },
        {
            "name": "E2E Testing",
            "context": {
                "tool_name": "test",
                "user_intent": "create end-to-end tests for checkout flow",
                "operation_type": "testing",
                "test_type": "e2e"
            },
            "expected_servers": ["playwright"]
        },
        {
            "name": "Performance Analysis",
            "context": {
                "tool_name": "analyze",
                "user_intent": "analyze bundle size and optimize performance",
                "operation_type": "performance",
                "complexity_score": 0.7
            },
            "expected_servers": ["sequential", "playwright"]
        },
        {
            "name": "Documentation Generation",
            "context": {
                "tool_name": "document",
                "user_intent": "generate API documentation",
                "operation_type": "documentation"
            },
            "expected_servers": ["context7"]
        },
        {
            "name": "Multi-file Pattern Update",
            "context": {
                "tool_name": "update",
                "file_count": 20,
                "pattern_type": "import_statements",
                "operation_type": "pattern_update"
            },
            "expected_servers": ["morphllm", "serena"]
        }
    ]
    
    print("📊 Testing MCP Server Selection Logic:\n")
    
    passed = 0
    failed = 0
    
    for scenario in scenarios:
        print(f"🔍 Scenario: {scenario['name']}")
        print(f"   Context: {json.dumps(scenario['context'], indent=6)}")
        
        # Get server recommendations
        server = mcp.select_optimal_server(
            scenario['context'].get('tool_name', 'unknown'),
            scenario['context']
        )
        servers = [server] if server else []
        
        # Also get optimization recommendations
        recommendations = mcp.get_optimization_recommendations(scenario['context'])
        if 'recommended_servers' in recommendations:
            servers.extend(recommendations['recommended_servers'])
        
        # Remove duplicates
        servers = list(set(servers))
        
        print(f"   Selected: {servers}")
        print(f"   Expected: {scenario['expected_servers']}")
        
        # Check if expected servers are selected
        success = any(server in servers for server in scenario['expected_servers'])
        
        if success:
            print("   ✅ PASS\n")
            passed += 1
        else:
            print("   ❌ FAIL\n")
            failed += 1
    
    # Test activation planning
    print("\n📊 Testing Activation Planning:\n")
    
    plan_scenarios = [
        {
            "name": "Simple File Edit",
            "context": {
                "tool_name": "edit",
                "file_count": 1,
                "complexity_score": 0.2
            }
        },
        {
            "name": "Complex Multi-Domain Task",
            "context": {
                "tool_name": "implement",
                "file_count": 10,
                "complexity_score": 0.8,
                "has_ui_components": True,
                "has_external_dependencies": True,
                "requires_testing": True
            }
        }
    ]
    
    for scenario in plan_scenarios:
        print(f"🔍 Scenario: {scenario['name']}")
        plan = mcp.create_activation_plan(
            [server for server in ['morphllm', 'sequential', 'serena'] if server],
            scenario['context'],
            scenario['context']
        )
        print(f"   Servers: {plan.servers_to_activate}")
        print(f"   Order: {plan.activation_order}")
        print(f"   Coordination: {plan.coordination_strategy}")
        print(f"   Estimated Time: {plan.estimated_cost_ms}ms")
        print(f"   Efficiency Gains: {plan.efficiency_gains}")
        print()
    
    # Test optimization recommendations
    print("\n📊 Testing Optimization Recommendations:\n")
    
    opt_scenarios = [
        {
            "name": "Symbol-level Refactoring",
            "context": {"tool_name": "refactor", "file_count": 8, "language": "python"}
        },
        {
            "name": "Pattern Application",
            "context": {"tool_name": "apply", "pattern_type": "repository", "file_count": 3}
        }
    ]
    
    for scenario in opt_scenarios:
        print(f"🔍 Scenario: {scenario['name']}")
        rec = mcp.get_optimization_recommendations(scenario['context'])
        print(f"   Servers: {rec.get('recommended_servers', [])}")
        print(f"   Efficiency: {rec.get('efficiency_gains', {})}")
        print(f"   Strategy: {rec.get('strategy', 'unknown')}")
        print()
    
    # Test cache effectiveness
    print("\n📊 Testing Cache Performance:\n")
    
    import time
    
    # First call (cold)
    start = time.time()
    _ = mcp.select_optimal_server("test", {"complexity_score": 0.5})
    cold_time = (time.time() - start) * 1000
    
    # Second call (warm)
    start = time.time()
    _ = mcp.select_optimal_server("test", {"complexity_score": 0.5})
    warm_time = (time.time() - start) * 1000
    
    print(f"   Cold call: {cold_time:.2f}ms")
    print(f"   Warm call: {warm_time:.2f}ms")
    print(f"   Speedup: {cold_time/warm_time:.1f}x")
    
    # Final summary
    print(f"\n📊 Final Results:")
    print(f"   Server Selection: {passed}/{passed+failed} passed ({passed/(passed+failed)*100:.1f}%)")
    print(f"   Performance: {'✅ PASS' if cold_time < 200 else '❌ FAIL'} (target <200ms)")
    print(f"   Cache: {'✅ WORKING' if warm_time < cold_time/2 else '❌ NOT WORKING'}")
    
    return passed == len(scenarios)

if __name__ == "__main__":
    success = test_mcp_intelligence_live()
    sys.exit(0 if success else 1)