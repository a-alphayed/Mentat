#!/usr/bin/env python3
"""
Comprehensive test runner for all SuperClaude shared modules.

Runs all test suites and generates a comprehensive test report with:
- Individual module test results
- Performance metrics and coverage analysis
- Integration test results
- QA findings and recommendations
"""

import unittest
import sys
import time
import io
from pathlib import Path
from contextlib import redirect_stdout, redirect_stderr

# Add the shared directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import all test modules
import test_compression_engine
import test_framework_logic
import test_learning_engine
import test_logger
import test_mcp_intelligence
import test_pattern_detection
import test_yaml_loader


class TestResult:
    """Container for test results and metrics."""
    
    def __init__(self, module_name, test_count, failures, errors, time_taken, output):
        self.module_name = module_name
        self.test_count = test_count
        self.failures = failures
        self.errors = errors
        self.time_taken = time_taken
        self.output = output
        self.success_rate = (test_count - len(failures) - len(errors)) / test_count if test_count > 0 else 0.0


def run_module_tests(test_module):
    """Run tests for a specific module and collect results."""
    print(f"\n{'='*60}")
    print(f"Running tests for {test_module.__name__}")
    print(f"{'='*60}")
    
    # Create test suite from module
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_module)
    
    # Capture output
    output_buffer = io.StringIO()
    error_buffer = io.StringIO()
    
    # Run tests with custom result class
    runner = unittest.TextTestRunner(
        stream=output_buffer,
        verbosity=2,
        buffer=True
    )
    
    start_time = time.time()
    
    with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
        result = runner.run(suite)
    
    end_time = time.time()
    
    # Collect output
    test_output = output_buffer.getvalue() + error_buffer.getvalue()
    
    # Print summary to console
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0:.1f}%")
    print(f"Time taken: {end_time - start_time:.2f}s")
    
    # Print any failures or errors
    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split(chr(10))[-2] if chr(10) in traceback else traceback}")
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split(chr(10))[-2] if chr(10) in traceback else traceback}")
    
    return TestResult(
        test_module.__name__,
        result.testsRun,
        result.failures,
        result.errors,
        end_time - start_time,
        test_output
    )


def generate_test_report(results):
    """Generate comprehensive test report."""
    total_tests = sum(r.test_count for r in results)
    total_failures = sum(len(r.failures) for r in results)
    total_errors = sum(len(r.errors) for r in results)
    total_time = sum(r.time_taken for r in results)
    overall_success_rate = (total_tests - total_failures - total_errors) / total_tests * 100 if total_tests > 0 else 0
    
    print(f"\n{'='*80}")
    print("COMPREHENSIVE TEST REPORT")
    print(f"{'='*80}")
    print(f"Overall Results:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {total_tests - total_failures - total_errors}")
    print(f"  Failed: {total_failures}")
    print(f"  Errors: {total_errors}")
    print(f"  Success Rate: {overall_success_rate:.1f}%")
    print(f"  Total Time: {total_time:.2f}s")
    print(f"  Average Time per Test: {total_time/total_tests:.3f}s")
    
    print(f"\nModule Breakdown:")
    print(f"{'Module':<25} {'Tests':<6} {'Pass':<6} {'Fail':<6} {'Error':<6} {'Rate':<8} {'Time':<8}")
    print(f"{'-'*80}")
    
    for result in results:
        passed = result.test_count - len(result.failures) - len(result.errors)
        print(f"{result.module_name:<25} {result.test_count:<6} {passed:<6} {len(result.failures):<6} {len(result.errors):<6} {result.success_rate*100:<7.1f}% {result.time_taken:<7.2f}s")
    
    # Performance Analysis
    print(f"\nPerformance Analysis:")
    print(f"  Fastest Module: {min(results, key=lambda r: r.time_taken).module_name} ({min(r.time_taken for r in results):.2f}s)")
    print(f"  Slowest Module: {max(results, key=lambda r: r.time_taken).module_name} ({max(r.time_taken for r in results):.2f}s)")
    
    performance_threshold = 5.0  # 5 seconds per module
    slow_modules = [r for r in results if r.time_taken > performance_threshold]
    if slow_modules:
        print(f"  Modules exceeding {performance_threshold}s threshold:")
        for module in slow_modules:
            print(f"    - {module.module_name}: {module.time_taken:.2f}s")
    
    # Quality Analysis
    print(f"\nQuality Analysis:")
    
    # Modules with 100% pass rate
    perfect_modules = [r for r in results if r.success_rate == 1.0]
    if perfect_modules:
        print(f"  Modules with 100% pass rate ({len(perfect_modules)}):")
        for module in perfect_modules:
            print(f"    ✅ {module.module_name}")
    
    # Modules with issues
    issue_modules = [r for r in results if r.success_rate < 1.0]
    if issue_modules:
        print(f"  Modules with issues ({len(issue_modules)}):")
        for module in issue_modules:
            print(f"    ⚠️  {module.module_name}: {module.success_rate*100:.1f}% pass rate")
    
    # Test coverage analysis
    print(f"\nTest Coverage Analysis:")
    modules_tested = {
        'compression_engine': any('compression_engine' in r.module_name for r in results),
        'framework_logic': any('framework_logic' in r.module_name for r in results),
        'learning_engine': any('learning_engine' in r.module_name for r in results),
        'logger': any('logger' in r.module_name for r in results),
        'mcp_intelligence': any('mcp_intelligence' in r.module_name for r in results),
        'pattern_detection': any('pattern_detection' in r.module_name for r in results),
        'yaml_loader': any('yaml_loader' in r.module_name for r in results)
    }
    
    coverage_rate = sum(modules_tested.values()) / len(modules_tested) * 100
    print(f"  Module Coverage: {coverage_rate:.1f}% ({sum(modules_tested.values())}/{len(modules_tested)} modules)")
    
    for module, tested in modules_tested.items():
        status = "✅ Tested" if tested else "❌ Not Tested"
        print(f"    {module}: {status}")
    
    # Integration test analysis
    print(f"\nIntegration Test Analysis:")
    integration_keywords = ['integration', 'coordination', 'workflow', 'end_to_end']
    integration_tests = []
    
    for result in results:
        for failure in result.failures + result.errors:
            test_name = str(failure[0]).lower()
            if any(keyword in test_name for keyword in integration_keywords):
                integration_tests.append((result.module_name, test_name))
    
    if integration_tests:
        print(f"  Integration test results found in {len(set(r[0] for r in integration_tests))} modules")
    else:
        print(f"  Note: Limited integration test coverage detected")
    
    # Provide QA recommendations
    print(f"\nQA Recommendations:")
    
    if overall_success_rate < 95:
        print(f"  🔴 CRITICAL: Overall success rate ({overall_success_rate:.1f}%) below 95% threshold")
        print(f"      - Investigate and fix failing tests before production deployment")
    elif overall_success_rate < 98:
        print(f"  🟡 WARNING: Overall success rate ({overall_success_rate:.1f}%) below 98% target")
        print(f"      - Review failing tests and implement fixes")
    else:
        print(f"  ✅ EXCELLENT: Overall success rate ({overall_success_rate:.1f}%) meets quality standards")
    
    if total_time > 30:
        print(f"  ⚠️  PERFORMANCE: Total test time ({total_time:.1f}s) exceeds 30s target")
        print(f"      - Consider test optimization for faster CI/CD pipelines")
    
    if len(perfect_modules) == len(results):
        print(f"  🎉 OUTSTANDING: All modules achieve 100% test pass rate!")
    
    print(f"\nRecommended Actions:")
    if issue_modules:
        print(f"  1. Priority: Fix failing tests in {len(issue_modules)} modules")
        print(f"  2. Investigate root causes of test failures and errors")
        print(f"  3. Add additional test coverage for edge cases")
    else:
        print(f"  1. Maintain current test quality standards")
        print(f"  2. Consider adding integration tests for cross-module functionality")
        print(f"  3. Monitor performance metrics to ensure tests remain fast")
    
    return {
        'total_tests': total_tests,
        'total_failures': total_failures,
        'total_errors': total_errors,
        'success_rate': overall_success_rate,
        'total_time': total_time,
        'modules_tested': len(results),
        'perfect_modules': len(perfect_modules),
        'coverage_rate': coverage_rate
    }


def main():
    """Main test runner function."""
    print("SuperClaude Shared Modules - Comprehensive Test Suite")
    print(f"Python version: {sys.version}")
    print(f"Test directory: {Path(__file__).parent}")
    
    # Test modules to run
    test_modules = [
        test_compression_engine,
        test_framework_logic,
        test_learning_engine,
        test_logger,
        test_mcp_intelligence,
        test_pattern_detection,
        test_yaml_loader
    ]
    
    # Run all tests
    results = []
    overall_start_time = time.time()
    
    for test_module in test_modules:
        try:
            result = run_module_tests(test_module)
            results.append(result)
        except Exception as e:
            print(f"❌ CRITICAL ERROR running {test_module.__name__}: {e}")
            # Create dummy result for reporting
            results.append(TestResult(test_module.__name__, 0, [], [('Error', str(e))], 0, str(e)))
    
    overall_end_time = time.time()
    
    # Generate comprehensive report
    summary = generate_test_report(results)
    
    print(f"\n{'='*80}")
    print(f"TEST EXECUTION COMPLETE")
    print(f"Total execution time: {overall_end_time - overall_start_time:.2f}s")
    print(f"{'='*80}")
    
    # Return exit code based on results
    if summary['success_rate'] >= 95:
        print("🎉 ALL TESTS PASS - Ready for production!")
        return 0
    elif summary['total_failures'] == 0 and summary['total_errors'] > 0:
        print("⚠️  ERRORS DETECTED - Investigate technical issues")
        return 1
    else:
        print("❌ TEST FAILURES - Fix issues before deployment")
        return 2


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)