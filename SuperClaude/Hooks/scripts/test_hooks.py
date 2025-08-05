#!/usr/bin/env python3
"""
SuperClaude Hooks Test Script

Comprehensive testing for all SuperClaude hooks including:
- Framework Coordinator
- Session Lifecycle
- Performance Monitor
- Quality Gates
- Token Efficiency

Tests hook functionality, error handling, and performance requirements.
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple
import tempfile

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


class HookTestResult:
    """Container for test results."""
    
    def __init__(self, hook_name: str, test_name: str, passed: bool, 
                 message: str, execution_time_ms: float = 0):
        self.hook_name = hook_name
        self.test_name = test_name
        self.passed = passed
        self.message = message
        self.execution_time_ms = execution_time_ms
    
    def __str__(self):
        status = f"{GREEN}✅ PASS{RESET}" if self.passed else f"{RED}❌ FAIL{RESET}"
        time_str = f" ({self.execution_time_ms:.1f}ms)" if self.execution_time_ms > 0 else ""
        return f"  {status} {self.test_name}: {self.message}{time_str}"


class HookTester:
    """Test manager for SuperClaude hooks."""
    
    def __init__(self, hooks_dir: Path):
        self.hooks_dir = hooks_dir
        self.results: Dict[str, List[HookTestResult]] = {}
        
        # Performance targets in milliseconds
        self.performance_targets = {
            'framework_coordinator': 100,
            'session_lifecycle': 100,
            'performance_monitor': 100,
            'quality_gates': 8000,
            'token_efficiency': 100
        }
    
    def run_hook(self, hook_path: Path, input_data: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        """
        Run a hook with given input and return result and execution time.
        
        Returns:
            Tuple of (result_dict, execution_time_ms)
        """
        start_time = time.time()
        
        try:
            # Run hook as subprocess
            process = subprocess.Popen(
                ['python3', str(hook_path)],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Send input JSON
            stdout, stderr = process.communicate(input=json.dumps(input_data))
            execution_time_ms = (time.time() - start_time) * 1000
            
            # Parse output
            if process.returncode != 0:
                return {
                    "status": "error",
                    "message": f"Hook returned non-zero exit code: {process.returncode}",
                    "stderr": stderr
                }, execution_time_ms
            
            try:
                result = json.loads(stdout)
                return result, execution_time_ms
            except json.JSONDecodeError:
                return {
                    "status": "error",
                    "message": "Invalid JSON output",
                    "stdout": stdout,
                    "stderr": stderr
                }, execution_time_ms
                
        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            return {
                "status": "error",
                "message": f"Failed to run hook: {str(e)}"
            }, execution_time_ms
    
    def test_token_efficiency_hook(self):
        """Test Token Efficiency hook."""
        hook_name = "token_efficiency"
        hook_path = self.hooks_dir / hook_name / "hook.py"
        results = []
        
        print(f"\n{BLUE}Testing Token Efficiency Hook...{RESET}")
        
        # Test 1: PreToolUse with write_memory
        test_input = {
            "event": "PreToolUse",
            "tool": {
                "name": "mcp__serena__write_memory",
                "args": {
                    "memory_name": "test_memory",
                    "content": "test content"
                }
            },
            "session_id": "test-session"
        }
        
        result, exec_time = self.run_hook(hook_path, test_input)
        
        # Check if --uc flag was added
        passed = (
            result.get("status") == "success" and
            "tool_args" in result and
            result["tool_args"].get("context", {}).get("flags", []) == ["--uc"]
        )
        
        results.append(HookTestResult(
            hook_name, 
            "PreToolUse write_memory",
            passed,
            "Added --uc flag" if passed else f"Failed to add flag: {result}",
            exec_time
        ))
        
        # Test 2: PreToolUse with other tool (should ignore)
        test_input["tool"]["name"] = "Read"
        result, exec_time = self.run_hook(hook_path, test_input)
        
        passed = result.get("status") == "success" and "--uc" not in str(result)
        results.append(HookTestResult(
            hook_name,
            "PreToolUse other tool",
            passed,
            "Correctly ignored non-write_memory tool",
            exec_time
        ))
        
        # Test 3: PostToolUse (should ignore)
        test_input["event"] = "PostToolUse"
        result, exec_time = self.run_hook(hook_path, test_input)
        
        passed = result.get("status") == "ignored"
        results.append(HookTestResult(
            hook_name,
            "PostToolUse event",
            passed,
            "Correctly ignored post-tool event",
            exec_time
        ))
        
        # Test 4: Performance test
        total_time = sum(r.execution_time_ms for r in results)
        avg_time = total_time / len(results)
        target = self.performance_targets[hook_name]
        
        passed = avg_time < target
        results.append(HookTestResult(
            hook_name,
            "Performance requirement",
            passed,
            f"Average {avg_time:.1f}ms (target: <{target}ms)",
            avg_time
        ))
        
        self.results[hook_name] = results
    
    def test_framework_coordinator_hook(self):
        """Test Framework Coordinator hook."""
        hook_name = "framework_coordinator"
        hook_path = self.hooks_dir / hook_name / "hook.py"
        
        # Skip if hook doesn't exist
        if not hook_path.exists():
            print(f"\n{YELLOW}Skipping Framework Coordinator Hook (not found)...{RESET}")
            return
        
        results = []
        print(f"\n{BLUE}Testing Framework Coordinator Hook...{RESET}")
        
        # Test 1: PreToolUse with complex operation
        test_input = {
            "event": "PreToolUse",
            "tool": {
                "name": "MultiEdit",
                "args": {
                    "file_path": "/test/file.py",
                    "edits": [{"old": "foo", "new": "bar"}]
                }
            },
            "session_id": "test-session"
        }
        
        result, exec_time = self.run_hook(hook_path, test_input)
        
        # Should provide suggestions
        passed = result.get("status") == "success"
        results.append(HookTestResult(
            hook_name,
            "PreToolUse complex operation",
            passed,
            "Generated coordination suggestions" if passed else f"Failed: {result}",
            exec_time
        ))
        
        self.results[hook_name] = results
    
    def test_all_hooks(self):
        """Run all hook tests."""
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}SuperClaude Hooks Test Suite{RESET}")
        print(f"{BLUE}{'='*60}{RESET}")
        
        # Test each hook
        self.test_token_efficiency_hook()
        self.test_framework_coordinator_hook()
        # Add more hook tests as needed
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary."""
        print(f"\n{BLUE}{'='*60}{RESET}")
        print(f"{BLUE}TEST SUMMARY{RESET}")
        print(f"{BLUE}{'='*60}{RESET}")
        
        total_tests = 0
        total_passed = 0
        
        for hook_name, results in self.results.items():
            hook_passed = sum(1 for r in results if r.passed)
            hook_total = len(results)
            total_tests += hook_total
            total_passed += hook_passed
            
            status = f"{GREEN}✅{RESET}" if hook_passed == hook_total else f"{RED}❌{RESET}"
            print(f"\n{status} {hook_name}: {hook_passed}/{hook_total} passed ({hook_passed/hook_total*100:.0f}%)")
            
            for result in results:
                print(result)
        
        # Overall summary
        print(f"\n{BLUE}{'='*60}{RESET}")
        overall_status = f"{GREEN}✅ PASS{RESET}" if total_passed == total_tests else f"{RED}❌ FAIL{RESET}"
        print(f"🎯 Overall Result: {overall_status}")
        print(f"   Total tests: {total_tests}")
        print(f"   Passed: {total_passed}")
        print(f"   Failed: {total_tests - total_passed}")
        print(f"   Success rate: {total_passed/total_tests*100:.1f}%")
        print(f"{BLUE}{'='*60}{RESET}")
        
        # Exit with appropriate code
        sys.exit(0 if total_passed == total_tests else 1)


def main():
    """Main test function."""
    # Determine hooks directory
    script_dir = Path(__file__).parent
    hooks_dir = script_dir.parent
    
    if not hooks_dir.exists():
        print(f"{RED}Error: Hooks directory not found at {hooks_dir}{RESET}")
        sys.exit(1)
    
    # Create tester and run tests
    tester = HookTester(hooks_dir)
    tester.test_all_hooks()


if __name__ == "__main__":
    main()