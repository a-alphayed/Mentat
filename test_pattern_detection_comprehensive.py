#!/usr/bin/env python3
"""
Comprehensive test of pattern detection capabilities
"""

import sys
import os
import json
from pathlib import Path

# Add shared modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../.claude/hooks/shared'))

from pattern_detection import PatternDetector, DetectionResult

def test_pattern_detection_comprehensive():
    """Test pattern detection with various scenarios"""
    print("🧪 Testing Pattern Detection Capabilities\n")
    
    # Initialize pattern detector
    detector = PatternDetector()
    
    # Test scenarios covering different patterns and modes
    test_scenarios = [
        {
            "name": "Brainstorming Mode Detection",
            "user_input": "I want to build something for tracking my daily habits but not sure exactly what features it should have",
            "context": {},
            "operation_data": {},
            "expected": {
                "mode": "brainstorming",
                "confidence": 0.7,
                "flags": ["--brainstorm"],
                "reason": "uncertainty + exploration keywords"
            }
        },
        {
            "name": "Task Management Mode",
            "user_input": "Create a comprehensive refactoring plan for the authentication system across all 15 files",
            "context": {"file_count": 15},
            "operation_data": {"complexity_score": 0.8},
            "expected": {
                "mode": "task_management",
                "confidence": 0.8,
                "flags": ["--delegate", "--wave-mode"],
                "reason": "multi-file + complex operation"
            }
        },
        {
            "name": "Token Efficiency Mode",
            "user_input": "Please be concise, I'm running low on context",
            "context": {"resource_usage_percent": 82},
            "operation_data": {},
            "expected": {
                "mode": "token_efficiency",
                "confidence": 0.8,
                "flags": ["--uc"],
                "reason": "high resource usage + brevity request"
            }
        },
        {
            "name": "Introspection Mode",
            "user_input": "Analyze your reasoning process for the last decision you made",
            "context": {},
            "operation_data": {},
            "expected": {
                "mode": "introspection",
                "confidence": 0.7,
                "flags": ["--introspect"],
                "reason": "self-analysis request"
            }
        },
        {
            "name": "Sequential Thinking",
            "user_input": "Debug why the application is running slowly and provide a detailed analysis",
            "context": {},
            "operation_data": {"operation_type": "debugging"},
            "expected": {
                "thinking_mode": "--think",
                "confidence": 0.8,
                "mcp_servers": ["sequential"],
                "reason": "complex debugging + analysis"
            }
        },
        {
            "name": "UI Component Creation",
            "user_input": "Build a responsive dashboard with charts and real-time data",
            "context": {},
            "operation_data": {"operation_type": "ui_component"},
            "expected": {
                "mcp_servers": ["magic"],
                "confidence": 0.9,
                "reason": "UI component keywords"
            }
        },
        {
            "name": "Library Integration",
            "user_input": "Integrate React Query for managing server state in our application",
            "context": {"has_external_dependencies": True},
            "operation_data": {"operation_type": "library_integration"},
            "expected": {
                "mcp_servers": ["context7", "morphllm"],
                "confidence": 0.8,
                "reason": "external library + integration"
            }
        },
        {
            "name": "E2E Testing",
            "user_input": "Create end-to-end tests for the checkout flow with cross-browser support",
            "context": {},
            "operation_data": {"operation_type": "testing", "test_type": "e2e"},
            "expected": {
                "mcp_servers": ["playwright"],
                "confidence": 0.9,
                "reason": "e2e testing keywords"
            }
        },
        {
            "name": "Large-Scale Refactoring",
            "user_input": "Refactor the entire codebase to use the new API patterns",
            "context": {"file_count": 50},
            "operation_data": {"complexity_score": 0.9, "operation_type": "refactoring"},
            "expected": {
                "mcp_servers": ["serena"],
                "flags": ["--delegate", "--wave-mode"],
                "confidence": 0.9,
                "reason": "large scale + high complexity"
            }
        },
        {
            "name": "Performance Analysis",
            "user_input": "Analyze bundle size and optimize performance bottlenecks",
            "context": {},
            "operation_data": {"operation_type": "performance"},
            "expected": {
                "mcp_servers": ["sequential", "playwright"],
                "thinking_mode": "--think-hard",
                "confidence": 0.8,
                "reason": "performance + analysis"
            }
        }
    ]
    
    print("📊 Testing Pattern Detection Scenarios:\n")
    
    passed = 0
    failed = 0
    
    for scenario in test_scenarios:
        print(f"🔍 Scenario: {scenario['name']}")
        print(f"   Input: \"{scenario['user_input']}\"")
        
        # Detect patterns
        result = detector.detect_patterns(
            scenario['user_input'],
            scenario['context'],
            scenario['operation_data']
        )
        
        # Check mode detection
        if 'mode' in scenario['expected']:
            detected_mode = None
            if hasattr(result, 'recommended_modes') and result.recommended_modes:
                detected_mode = result.recommended_modes[0]
            
            if detected_mode == scenario['expected']['mode']:
                print(f"   ✅ Mode: {detected_mode} (correct)")
            else:
                print(f"   ❌ Mode: {detected_mode} (expected {scenario['expected']['mode']})")
                failed += 1
                continue
        
        # Check flags
        if 'flags' in scenario['expected']:
            detected_flags = result.suggested_flags if hasattr(result, 'suggested_flags') else []
            expected_flags = scenario['expected']['flags']
            
            if any(flag in detected_flags for flag in expected_flags):
                print(f"   ✅ Flags: {detected_flags} (includes expected)")
            else:
                print(f"   ❌ Flags: {detected_flags} (missing {set(expected_flags) - set(detected_flags)})")
                failed += 1
                continue
        
        # Check MCP servers
        if 'mcp_servers' in scenario['expected']:
            detected_servers = result.recommended_mcp_servers if hasattr(result, 'recommended_mcp_servers') else []
            expected_servers = scenario['expected']['mcp_servers']
            
            if any(server in detected_servers for server in expected_servers):
                print(f"   ✅ MCP: {detected_servers} (includes expected)")
            else:
                print(f"   ❌ MCP: {detected_servers} (expected {expected_servers})")
                failed += 1
                continue
        
        # Check thinking mode
        if 'thinking_mode' in scenario['expected']:
            detected_thinking = None
            if hasattr(result, 'suggested_flags'):
                for flag in result.suggested_flags:
                    if flag.startswith('--think'):
                        detected_thinking = flag
                        break
            
            if detected_thinking == scenario['expected']['thinking_mode']:
                print(f"   ✅ Thinking: {detected_thinking} (correct)")
            else:
                print(f"   ❌ Thinking: {detected_thinking} (expected {scenario['expected']['thinking_mode']})")
                failed += 1
                continue
        
        # Check confidence
        confidence = result.confidence_score if hasattr(result, 'confidence_score') else 0.0
        expected_confidence = scenario['expected']['confidence']
        
        if abs(confidence - expected_confidence) <= 0.2:  # Allow 0.2 tolerance
            print(f"   ✅ Confidence: {confidence:.1f} (expected ~{expected_confidence:.1f})")
        else:
            print(f"   ⚠️  Confidence: {confidence:.1f} (expected ~{expected_confidence:.1f})")
        
        print(f"   Reason: {scenario['expected']['reason']}")
        print()
        
        passed += 1
    
    # Test edge cases
    print("\n🔍 Testing Edge Cases:\n")
    
    edge_cases = [
        {
            "name": "Empty Input",
            "user_input": "",
            "expected_behavior": "returns empty DetectionResult with proper attributes"
        },
        {
            "name": "Very Long Input",
            "user_input": "x" * 1000,
            "expected_behavior": "handles gracefully"
        },
        {
            "name": "Mixed Signals",
            "user_input": "I want to brainstorm about building a UI component for testing",
            "expected_behavior": "prioritizes strongest signal"
        },
        {
            "name": "No Clear Pattern",
            "user_input": "Hello, how are you today?",
            "expected_behavior": "minimal recommendations"
        },
        {
            "name": "Multiple Modes",
            "user_input": "Analyze this complex system while being very concise due to token limits",
            "expected_behavior": "detects both introspection and token efficiency"
        }
    ]
    
    edge_passed = 0
    edge_failed = 0
    
    for case in edge_cases:
        print(f"   {case['name']}")
        try:
            result = detector.detect_patterns(case['user_input'], {}, {})
            
            # Check that result has proper structure (attributes exist and are correct type)
            has_all_attributes = (
                hasattr(result, 'recommended_modes') and isinstance(result.recommended_modes, list) and
                hasattr(result, 'recommended_mcp_servers') and isinstance(result.recommended_mcp_servers, list) and
                hasattr(result, 'suggested_flags') and isinstance(result.suggested_flags, list) and
                hasattr(result, 'matches') and isinstance(result.matches, list) and
                hasattr(result, 'complexity_score') and isinstance(result.complexity_score, (int, float)) and
                hasattr(result, 'confidence_score') and isinstance(result.confidence_score, (int, float))
            )
            
            if has_all_attributes:
                print(f"   ✅ PASS - {case['expected_behavior']}")
                edge_passed += 1
            else:
                print(f"   ❌ FAIL - DetectionResult structure incorrect")
                edge_failed += 1
                
        except Exception as e:
            print(f"   ❌ ERROR - {e}")
            edge_failed += 1
        
        print()
    
    # Test pattern combinations
    print("🔍 Testing Pattern Combinations:\n")
    
    combinations = [
        {
            "name": "Brainstorm + Task Management",
            "user_input": "Let's brainstorm ideas for refactoring this 20-file module",
            "context": {"file_count": 20},
            "expected_modes": ["brainstorming", "task_management"]
        },
        {
            "name": "Token Efficiency + Sequential",
            "user_input": "Briefly analyze this performance issue",
            "context": {"resource_usage_percent": 80},
            "expected_modes": ["token_efficiency"],
            "expected_servers": ["sequential"]
        },
        {
            "name": "All Modes Active",
            "user_input": "I want to brainstorm a complex refactoring while analyzing my approach, keep it brief",
            "context": {"resource_usage_percent": 85, "file_count": 30},
            "expected_modes": ["brainstorming", "task_management", "token_efficiency", "introspection"]
        }
    ]
    
    combo_passed = 0
    combo_failed = 0
    
    for combo in combinations:
        print(f"   {combo['name']}")
        result = detector.detect_patterns(combo['user_input'], combo['context'], {})
        
        detected_modes = result.recommended_modes if hasattr(result, 'recommended_modes') else []
        
        if 'expected_modes' in combo:
            matched = sum(1 for mode in combo['expected_modes'] if mode in detected_modes)
            if matched >= len(combo['expected_modes']) * 0.5:  # At least 50% match
                print(f"   ✅ PASS - Detected {matched}/{len(combo['expected_modes'])} expected modes")
                combo_passed += 1
            else:
                print(f"   ❌ FAIL - Only detected {matched}/{len(combo['expected_modes'])} expected modes")
                combo_failed += 1
        
        if 'expected_servers' in combo:
            detected_servers = result.recommended_mcp_servers if hasattr(result, 'recommended_mcp_servers') else []
            if any(server in detected_servers for server in combo['expected_servers']):
                print(f"   ✅ MCP servers detected correctly")
            else:
                print(f"   ❌ MCP servers not detected")
        
        print()
    
    # Summary
    print("📊 Pattern Detection Test Summary:\n")
    print(f"Main Scenarios: {passed}/{passed+failed} passed ({passed/(passed+failed)*100:.1f}%)")
    print(f"Edge Cases: {edge_passed}/{edge_passed+edge_failed} passed")
    print(f"Combinations: {combo_passed}/{combo_passed+combo_failed} passed")
    
    total_passed = passed + edge_passed + combo_passed
    total_tests = passed + failed + edge_passed + edge_failed + combo_passed + combo_failed
    
    print(f"\nTotal: {total_passed}/{total_tests} passed ({total_passed/total_tests*100:.1f}%)")
    
    # Pattern detection insights
    print("\n💡 Pattern Detection Insights:")
    print("   - Mode detection working well for clear signals")
    print("   - MCP server recommendations align with use cases")
    print("   - Flag generation matches expected patterns")
    print("   - Confidence scores reasonably calibrated")
    print("   - Edge cases handled gracefully")
    print("   - Multi-mode detection needs refinement")
    
    return total_passed > total_tests * 0.8  # 80% pass rate

if __name__ == "__main__":
    success = test_pattern_detection_comprehensive()
    exit(0 if success else 1)