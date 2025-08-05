#!/usr/bin/env python3
"""
SuperClaude Hooks Validation Script

Validates SuperClaude hooks installation and configuration.
Checks:
- Hook file integrity and accessibility
- Claude Code settings configuration
- Hook configuration validity
- Performance requirements
- Dependencies availability

Usage:
    python SuperClaude/Hooks/scripts/validate.py [--verbose] [--fix] [--report]
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import logging
import importlib.util

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("SuperClaude.Hooks.Validator")


class ValidationResult:
    """Container for validation results."""
    
    def __init__(self, test_name: str, passed: bool, message: str, details: Optional[str] = None):
        self.test_name = test_name
        self.passed = passed
        self.message = message
        self.details = details
        self.timestamp = time.time()
    
    def __str__(self) -> str:
        status = "✅ PASS" if self.passed else "❌ FAIL"
        result = f"{status} {self.test_name}: {self.message}"
        if self.details:
            result += f"\n    Details: {self.details}"
        return result


class HooksValidator:
    """
    SuperClaude Hooks validation manager.
    
    Performs comprehensive validation of hooks installation:
    - File integrity checks
    - Configuration validation
    - Performance verification
    - Dependency checking
    """
    
    def __init__(self, verbose: bool = False, fix: bool = False):
        """
        Initialize validator.
        
        Args:
            verbose: Enable detailed output
            fix: Attempt to fix issues found
        """
        self.verbose = verbose
        self.fix = fix
        self.results: List[ValidationResult] = []
        
        # Setup paths
        self.claude_home = Path.home() / ".claude"
        self.hooks_path = self.claude_home / "SuperClaude" / "Hooks"
        self.settings_file = self.claude_home / "settings.json"
        
        # Performance targets
        self.performance_targets = {
            'hook_execution_ms': 100,
            'memory_operations_ms': 200,
            'session_load_ms': 500,
            'context_retention_percent': 90
        }
        
        if verbose:
            logger.info(f"Validating hooks at: {self.hooks_path}")
            logger.info(f"Claude settings at: {self.settings_file}")
    
    def _add_result(self, test_name: str, passed: bool, message: str, details: Optional[str] = None) -> None:
        """Add validation result."""
        result = ValidationResult(test_name, passed, message, details)
        self.results.append(result)
        
        if self.verbose or not passed:
            print(result)
    
    def _load_json_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Load and parse JSON file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError as e:
            self._add_result(
                f"JSON Parse ({file_path.name})",
                False,
                f"Invalid JSON syntax: {e}",
                f"File: {file_path}"
            )
            return None
        except Exception as e:
            self._add_result(
                f"File Access ({file_path.name})",
                False,
                f"Cannot read file: {e}",
                f"File: {file_path}"
            )
            return None
    
    def _test_python_import(self, module_path: Path, module_name: str) -> bool:
        """Test if Python module can be imported."""
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec is None:
                return False
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return True
            
        except Exception as e:
            self._add_result(
                f"Python Import ({module_name})",
                False,
                f"Import failed: {e}",
                f"Module: {module_path}"
            )
            return False
    
    def validate_file_structure(self) -> bool:
        """Validate hook file structure and accessibility."""
        logger.info("Validating file structure...")
        
        # Check main hooks directory
        if not self.hooks_path.exists():
            self._add_result(
                "Hooks Directory",
                False,
                "SuperClaude Hooks directory not found",
                f"Expected: {self.hooks_path}"
            )
            return False
        
        self._add_result("Hooks Directory", True, "Hooks directory exists")
        
        # Check required files and directories
        required_structure = {
            '__init__.py': 'file',
            'README.md': 'file',
            'common/__init__.py': 'file',
            'common/base_hook.py': 'file',
            'common/framework_parser.py': 'file',
            'common/utils.py': 'file',
            'framework_coordinator/__init__.py': 'file',
            'session_lifecycle/__init__.py': 'file',
            'quality_gates/__init__.py': 'file',
            'performance_monitor/__init__.py': 'file',
            'config/claude-code-settings.json': 'file',
            'scripts/install.py': 'file',
            'scripts/validate.py': 'file'
        }
        
        structure_valid = True
        
        for path_str, expected_type in required_structure.items():
            full_path = self.hooks_path / path_str
            
            if not full_path.exists():
                self._add_result(
                    f"Required {expected_type.title()}",
                    False,
                    f"Missing: {path_str}",
                    f"Path: {full_path}"
                )
                structure_valid = False
            else:
                if expected_type == 'file' and not full_path.is_file():
                    self._add_result(
                        f"File Type",
                        False,
                        f"Expected file, found directory: {path_str}"
                    )
                    structure_valid = False
                elif expected_type == 'directory' and not full_path.is_dir():
                    self._add_result(
                        f"Directory Type",
                        False,
                        f"Expected directory, found file: {path_str}"
                    )
                    structure_valid = False
        
        if structure_valid:
            self._add_result("File Structure", True, "All required files and directories present")
        
        return structure_valid
    
    def validate_python_modules(self) -> bool:
        """Validate Python modules can be imported."""
        logger.info("Validating Python modules...")
        
        modules_to_test = [
            ('common/base_hook.py', 'base_hook'),
            ('common/framework_parser.py', 'framework_parser'),
            ('common/utils.py', 'utils')
        ]
        
        all_valid = True
        
        for module_path_str, module_name in modules_to_test:
            module_path = self.hooks_path / module_path_str
            if module_path.exists():
                if not self._test_python_import(module_path, module_name):
                    all_valid = False
                else:
                    self._add_result(
                        f"Python Module ({module_name})",
                        True,
                        "Module imports successfully"
                    )
        
        return all_valid
    
    def validate_claude_settings(self) -> bool:
        """Validate Claude Code settings configuration."""
        logger.info("Validating Claude Code settings...")
        
        # Check settings file exists
        if not self.settings_file.exists():
            self._add_result(
                "Claude Settings File",
                False,
                "Claude Code settings.json not found",
                f"Expected: {self.settings_file}"
            )
            return False
        
        # Load settings
        settings = self._load_json_file(self.settings_file)
        if settings is None:
            return False
        
        self._add_result("Claude Settings File", True, "Settings file loaded successfully")
        
        # Check for hooks configuration
        if 'hooks' not in settings:
            self._add_result(
                "Hooks Configuration",
                False,
                "No hooks configuration found in settings"
            )
            return False
        
        hooks = settings['hooks']
        if not isinstance(hooks, list):
            self._add_result(
                "Hooks Configuration",
                False,
                "Hooks configuration is not a list"
            )
            return False
        
        # Check for SuperClaude hooks
        superclaude_hooks = [h for h in hooks if h.get('name', '').startswith('superclaude-')]
        
        if len(superclaude_hooks) == 0:
            self._add_result(
                "SuperClaude Hooks",
                False,
                "No SuperClaude hooks found in settings"
            )
            return False
        
        self._add_result(
            "SuperClaude Hooks",
            True,
            f"Found {len(superclaude_hooks)} SuperClaude hooks"
        )
        
        # Validate individual hook configurations
        hooks_valid = True
        expected_hooks = [
            'superclaude-framework-coordinator',
            'superclaude-framework-coordinator-post',
            'superclaude-session-lifecycle',
            'superclaude-session-lifecycle-post',
            'superclaude-quality-gates',
            'superclaude-performance-monitor-pre',
            'superclaude-performance-monitor-post'
        ]
        
        found_hooks = {h.get('name') for h in superclaude_hooks}
        missing_hooks = set(expected_hooks) - found_hooks
        
        if missing_hooks:
            self._add_result(
                "Hook Completeness",
                False,
                f"Missing hooks: {', '.join(missing_hooks)}"
            )
            hooks_valid = False
        else:
            self._add_result("Hook Completeness", True, "All expected hooks present")
        
        # Validate hook command paths
        for hook in superclaude_hooks:
            hook_name = hook.get('name', 'unknown')
            command = hook.get('command', '')
            
            if not command:
                self._add_result(
                    f"Hook Command ({hook_name})",
                    False,
                    "Missing command configuration"
                )
                hooks_valid = False
                continue
            
            # Extract Python file path from command
            if 'SuperClaude/Hooks/' in command:
                # This is a simple check - in practice, the path might use variables
                self._add_result(
                    f"Hook Command ({hook_name})",
                    True,
                    "Command path appears valid"
                )
            else:
                self._add_result(
                    f"Hook Command ({hook_name})",
                    False,
                    "Command path does not reference SuperClaude hooks"
                )
                hooks_valid = False
        
        # Check SuperClaude configuration
        if 'superclaude' not in settings:
            self._add_result(
                "SuperClaude Config",
                False,
                "SuperClaude configuration section missing"
            )
            hooks_valid = False
        else:
            superclaude_config = settings['superclaude']
            
            # Check for required configuration sections
            required_sections = [
                'hooks_system',
                'framework_coordination',
                'session_lifecycle',
                'quality_gates',
                'performance_monitoring'
            ]
            
            for section in required_sections:
                if section not in superclaude_config:
                    self._add_result(
                        f"Config Section ({section})",
                        False,
                        f"Missing configuration section: {section}"
                    )
                    hooks_valid = False
                else:
                    self._add_result(
                        f"Config Section ({section})",
                        True,
                        f"Configuration section present: {section}"
                    )
        
        return hooks_valid
    
    def validate_hook_configurations(self) -> bool:
        """Validate individual hook configuration files."""
        logger.info("Validating hook configurations...")
        
        config_file = self.hooks_path / "config" / "claude-code-settings.json"
        
        if not config_file.exists():
            self._add_result(
                "Hook Config File",
                False,
                "Hook configuration file not found",
                f"Expected: {config_file}"
            )
            return False
        
        config = self._load_json_file(config_file)
        if config is None:
            return False
        
        # Validate configuration structure
        if 'hooks' not in config or 'superclaude' not in config:
            self._add_result(
                "Hook Config Structure",
                False,
                "Invalid configuration structure - missing hooks or superclaude sections"
            )
            return False
        
        self._add_result("Hook Config File", True, "Hook configuration loaded successfully")
        
        # Validate performance targets
        superclaude_config = config.get('superclaude', {})
        perf_config = superclaude_config.get('performance_monitoring', {})
        targets = perf_config.get('targets', {})
        
        targets_valid = True
        for target_name, expected_value in self.performance_targets.items():
            if target_name not in targets:
                self._add_result(
                    f"Performance Target ({target_name})",
                    False,
                    f"Missing performance target: {target_name}"
                )
                targets_valid = False
            else:
                actual_value = targets[target_name]
                if target_name.endswith('_ms') and actual_value > expected_value * 2:
                    self._add_result(
                        f"Performance Target ({target_name})",
                        False,
                        f"Performance target too lenient: {actual_value}ms > {expected_value * 2}ms"
                    )
                    targets_valid = False
                else:
                    self._add_result(
                        f"Performance Target ({target_name})",
                        True,
                        f"Performance target appropriate: {actual_value}"
                    )
        
        return targets_valid
    
    def validate_dependencies(self) -> bool:
        """Validate required dependencies are available."""
        logger.info("Validating dependencies...")
        
        required_modules = [
            'json',
            'pathlib',
            'logging',
            'time',
            'os',
            'sys',
            're',
            'yaml'
        ]
        
        dependencies_valid = True
        
        for module_name in required_modules:
            try:
                __import__(module_name)
                self._add_result(
                    f"Dependency ({module_name})",
                    True,
                    f"Module {module_name} available"
                )
            except ImportError:
                self._add_result(
                    f"Dependency ({module_name})",
                    False,
                    f"Required module not available: {module_name}"
                )
                dependencies_valid = False
        
        return dependencies_valid
    
    def validate_performance_requirements(self) -> bool:
        """Validate performance requirements can be met."""
        logger.info("Validating performance requirements...")
        
        # Test basic hook execution time
        try:
            start_time = time.time()
            
            # Simulate basic hook operations
            base_hook_path = self.hooks_path / "common" / "base_hook.py"
            if base_hook_path.exists():
                # Basic import test
                spec = importlib.util.spec_from_file_location("base_hook", base_hook_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
            
            execution_time_ms = (time.time() - start_time) * 1000
            
            if execution_time_ms > self.performance_targets['hook_execution_ms']:
                self._add_result(
                    "Performance Test",
                    False,
                    f"Hook execution too slow: {execution_time_ms:.2f}ms > {self.performance_targets['hook_execution_ms']}ms"
                )
                return False
            else:
                self._add_result(
                    "Performance Test",
                    True,
                    f"Hook execution time acceptable: {execution_time_ms:.2f}ms"
                )
                return True
                
        except Exception as e:
            self._add_result(
                "Performance Test",
                False,
                f"Performance test failed: {e}"
            )
            return False
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report."""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.passed)
        failed_tests = total_tests - passed_tests
        
        report = {
            'timestamp': time.time(),
            'summary': {
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            'tests': [
                {
                    'name': r.test_name,
                    'passed': r.passed,
                    'message': r.message,
                    'details': r.details,
                    'timestamp': r.timestamp
                }
                for r in self.results
            ],
            'recommendations': self.get_recommendations()
        }
        
        return report
    
    def get_recommendations(self) -> List[str]:
        """Get recommendations based on validation results."""
        recommendations = []
        
        failed_results = [r for r in self.results if not r.passed]
        
        if any('File Structure' in r.test_name or 'Required' in r.test_name for r in failed_results):
            recommendations.append("Run the installation script: python SuperClaude/Hooks/scripts/install.py")
        
        if any('Claude Settings' in r.test_name for r in failed_results):
            recommendations.append("Update Claude Code settings with hook configurations")
        
        if any('Python' in r.test_name for r in failed_results):
            recommendations.append("Check Python environment and install missing dependencies")
        
        if any('Performance' in r.test_name for r in failed_results):
            recommendations.append("Check system performance and consider optimization")
        
        if any('Dependency' in r.test_name for r in failed_results):
            recommendations.append("Install missing Python dependencies: pip install pyyaml")
        
        return recommendations
    
    def validate_all(self) -> bool:
        """Run all validation tests."""
        logger.info("Starting SuperClaude Hooks validation...")
        
        validation_tests = [
            self.validate_file_structure,
            self.validate_python_modules,
            self.validate_claude_settings,
            self.validate_hook_configurations,
            self.validate_dependencies,
            self.validate_performance_requirements
        ]
        
        all_passed = True
        
        for test_func in validation_tests:
            try:
                result = test_func()
                if not result:
                    all_passed = False
            except Exception as e:
                logger.error(f"Validation test failed with exception: {e}")
                self._add_result(
                    test_func.__name__,
                    False,
                    f"Test failed with exception: {e}"
                )
                all_passed = False
        
        # Print summary
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.passed)
        failed_tests = total_tests - passed_tests
        
        print(f"\n{'='*60}")
        print(f"VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"Total tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success rate: {(passed_tests / total_tests * 100):.1f}%" if total_tests > 0 else "N/A")
        
        if failed_tests > 0:
            print(f"\nRECOMMENDATIONS:")
            for rec in self.get_recommendations():
                print(f"  • {rec}")
        
        return all_passed


def main():
    """Main validation function."""
    parser = argparse.ArgumentParser(
        description="Validate SuperClaude Hooks installation and configuration"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable detailed output"
    )
    parser.add_argument(
        "--fix", 
        action="store_true", 
        help="Attempt to fix issues found (not implemented)"
    )
    parser.add_argument(
        "--report", 
        action="store_true", 
        help="Generate JSON report file"
    )
    
    args = parser.parse_args()
    
    # Create validator
    validator = HooksValidator(verbose=args.verbose, fix=args.fix)
    
    # Run validation
    success = validator.validate_all()
    
    # Generate report if requested
    if args.report:
        report = validator.generate_report()
        report_file = Path.home() / ".claude" / "superclaude-hooks-validation-report.json"
        
        try:
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\nValidation report saved to: {report_file}")
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()