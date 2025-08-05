#!/usr/bin/env python3
"""
Comprehensive YAML Configuration Loader Test Suite

Tests all aspects of the yaml_loader module functionality including:
1. YAML file discovery and loading
2. Configuration parsing and validation
3. Error handling for missing files, malformed YAML
4. Hook configuration integration
5. Performance testing
6. Edge cases and boundary conditions
"""

import sys
import os
import time
import json
import tempfile
import yaml
from pathlib import Path
from typing import Dict, List, Any

# Add shared modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "hooks", "shared"))

try:
    from yaml_loader import config_loader, UnifiedConfigLoader
except ImportError as e:
    print(f"❌ Failed to import yaml_loader: {e}")
    sys.exit(1)


class YAMLLoaderTestSuite:
    """Comprehensive test suite for YAML configuration loading."""
    
    def __init__(self):
        self.test_results = []
        self.framework_hooks_path = Path(__file__).parent
        self.config_dir = self.framework_hooks_path / "config"
        self.all_yaml_files = list(self.config_dir.glob("*.yaml"))
        
    def run_all_tests(self):
        """Run all test categories."""
        print("🧪 SuperClaude YAML Configuration Loader Test Suite")
        print("=" * 60)
        
        # Test categories
        test_categories = [
            ("File Discovery", self.test_file_discovery),
            ("Basic YAML Loading", self.test_basic_yaml_loading),
            ("Configuration Parsing", self.test_configuration_parsing),
            ("Hook Integration", self.test_hook_integration),
            ("Error Handling", self.test_error_handling),
            ("Edge Cases", self.test_edge_cases),
            ("Performance Testing", self.test_performance),
            ("Cache Functionality", self.test_cache_functionality),
            ("Environment Variables", self.test_environment_variables),
            ("Include Functionality", self.test_include_functionality)
        ]
        
        for category_name, test_method in test_categories:
            print(f"\n📋 {category_name}")
            print("-" * 40)
            try:
                test_method()
            except Exception as e:
                self.record_test("SYSTEM_ERROR", f"{category_name} failed", False, str(e))
                print(f"❌ SYSTEM ERROR in {category_name}: {e}")
        
        # Generate final report
        self.generate_report()
    
    def record_test(self, test_name: str, description: str, passed: bool, details: str = ""):
        """Record test result."""
        self.test_results.append({
            'test_name': test_name,
            'description': description,
            'passed': passed,
            'details': details,
            'timestamp': time.time()
        })
        
        status = "✅" if passed else "❌"
        print(f"{status} {test_name}: {description}")
        if details and not passed:
            print(f"   Details: {details}")
    
    def test_file_discovery(self):
        """Test YAML file discovery and accessibility."""
        # Test 1: Framework-Hooks directory exists
        self.record_test(
            "DIR_EXISTS",
            "Framework-Hooks directory exists",
            self.framework_hooks_path.exists(),
            str(self.framework_hooks_path)
        )
        
        # Test 2: Config directory exists
        self.record_test(
            "CONFIG_DIR_EXISTS", 
            "Config directory exists",
            self.config_dir.exists(),
            str(self.config_dir)
        )
        
        # Test 3: YAML files found
        self.record_test(
            "YAML_FILES_FOUND",
            f"Found {len(self.all_yaml_files)} YAML files",
            len(self.all_yaml_files) > 0,
            f"Files: {[f.name for f in self.all_yaml_files]}"
        )
        
        # Test 4: Expected configuration files exist
        expected_configs = [
            'compression.yaml', 'performance.yaml', 'logging.yaml', 
            'session.yaml', 'modes.yaml', 'validation.yaml', 'orchestrator.yaml'
        ]
        
        for config_name in expected_configs:
            config_path = self.config_dir / config_name
            self.record_test(
                f"CONFIG_{config_name.upper().replace('.', '_')}",
                f"{config_name} exists and readable",
                config_path.exists() and config_path.is_file(),
                str(config_path)
            )
    
    def test_basic_yaml_loading(self):
        """Test basic YAML file loading functionality."""
        for yaml_file in self.all_yaml_files:
            config_name = yaml_file.stem
            
            # Test loading each YAML file
            try:
                start_time = time.time()
                config = config_loader.load_config(config_name)
                load_time = (time.time() - start_time) * 1000
                
                self.record_test(
                    f"LOAD_{config_name.upper()}",
                    f"Load {config_name}.yaml ({load_time:.1f}ms)",
                    isinstance(config, dict) and len(config) > 0,
                    f"Keys: {list(config.keys())[:5] if config else 'None'}"
                )
                
                # Test performance target (should be < 100ms for any config)
                self.record_test(
                    f"PERF_{config_name.upper()}",
                    f"{config_name}.yaml load performance",
                    load_time < 100,
                    f"Load time: {load_time:.1f}ms (target: <100ms)"
                )
                
            except Exception as e:
                self.record_test(
                    f"LOAD_{config_name.upper()}",
                    f"Load {config_name}.yaml",
                    False,
                    str(e)
                )
    
    def test_configuration_parsing(self):
        """Test configuration parsing and structure validation."""
        # Test compression.yaml structure
        try:
            compression_config = config_loader.load_config('compression')
            expected_sections = [
                'compression_levels', 'selective_compression', 'symbol_systems',
                'abbreviation_systems', 'performance_targets'
            ]
            
            for section in expected_sections:
                self.record_test(
                    f"COMPRESSION_SECTION_{section.upper()}",
                    f"Compression config has {section}",
                    section in compression_config,
                    f"Available sections: {list(compression_config.keys())}"
                )
                
            # Test compression levels
            if 'compression_levels' in compression_config:
                levels = compression_config['compression_levels']
                expected_levels = ['minimal', 'efficient', 'compressed', 'critical', 'emergency']
                
                for level in expected_levels:
                    self.record_test(
                        f"COMPRESSION_LEVEL_{level.upper()}",
                        f"Compression level {level} exists",
                        level in levels,
                        f"Available levels: {list(levels.keys()) if levels else 'None'}"
                    )
                    
        except Exception as e:
            self.record_test(
                "COMPRESSION_STRUCTURE",
                "Compression config structure test",
                False,
                str(e)
            )
        
        # Test performance.yaml structure
        try:
            performance_config = config_loader.load_config('performance')
            expected_sections = [
                'hook_targets', 'system_targets', 'mcp_server_performance',
                'performance_monitoring'
            ]
            
            for section in expected_sections:
                self.record_test(
                    f"PERFORMANCE_SECTION_{section.upper()}",
                    f"Performance config has {section}",
                    section in performance_config,
                    f"Available sections: {list(performance_config.keys())}"
                )
                
        except Exception as e:
            self.record_test(
                "PERFORMANCE_STRUCTURE",
                "Performance config structure test",
                False,
                str(e)
            )
    
    def test_hook_integration(self):
        """Test hook configuration integration."""
        # Test getting hook-specific configurations
        hook_names = [
            'session_start', 'pre_tool_use', 'post_tool_use', 
            'pre_compact', 'notification', 'stop'
        ]
        
        for hook_name in hook_names:
            try:
                # This will try superclaude_config first, then fallback
                hook_config = config_loader.get_hook_config(hook_name)
                
                self.record_test(
                    f"HOOK_CONFIG_{hook_name.upper()}",
                    f"Get {hook_name} hook config",
                    hook_config is not None,
                    f"Config type: {type(hook_config)}, Value: {hook_config}"
                )
                
            except Exception as e:
                self.record_test(
                    f"HOOK_CONFIG_{hook_name.upper()}",
                    f"Get {hook_name} hook config",
                    False,
                    str(e)
                )
        
        # Test hook enablement check
        try:
            enabled_result = config_loader.is_hook_enabled('session_start')
            self.record_test(
                "HOOK_ENABLED_CHECK",
                "Hook enablement check",
                isinstance(enabled_result, bool),
                f"session_start enabled: {enabled_result}"
            )
        except Exception as e:
            self.record_test(
                "HOOK_ENABLED_CHECK",
                "Hook enablement check",
                False,
                str(e)
            )
    
    def test_error_handling(self):
        """Test error handling for various failure conditions."""
        # Test 1: Non-existent YAML file
        try:
            config_loader.load_config('nonexistent_config')
            self.record_test(
                "ERROR_NONEXISTENT_FILE",
                "Non-existent file handling",
                False,
                "Should have raised FileNotFoundError"
            )
        except FileNotFoundError:
            self.record_test(
                "ERROR_NONEXISTENT_FILE",
                "Non-existent file handling",
                True,
                "Correctly raised FileNotFoundError"
            )
        except Exception as e:
            self.record_test(
                "ERROR_NONEXISTENT_FILE",
                "Non-existent file handling",
                False,
                f"Wrong exception type: {type(e).__name__}: {e}"
            )
        
        # Test 2: Malformed YAML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content:\n  - malformed\n    - structure")
            malformed_file = f.name
        
        try:
            # Create a temporary config loader for this test
            temp_config_dir = Path(malformed_file).parent
            temp_loader = UnifiedConfigLoader(temp_config_dir)
            
            # Try to load the malformed file
            config_name = Path(malformed_file).stem
            temp_loader.load_config(config_name)
            
            self.record_test(
                "ERROR_MALFORMED_YAML",
                "Malformed YAML handling",
                False,
                "Should have raised ValueError for YAML parsing error"
            )
        except ValueError as e:
            self.record_test(
                "ERROR_MALFORMED_YAML",
                "Malformed YAML handling",
                "YAML parsing error" in str(e),
                f"Correctly raised ValueError: {e}"
            )
        except Exception as e:
            self.record_test(
                "ERROR_MALFORMED_YAML",
                "Malformed YAML handling",
                False,
                f"Wrong exception type: {type(e).__name__}: {e}"
            )
        finally:
            # Clean up temp file
            try:
                os.unlink(malformed_file)
            except:
                pass
        
        # Test 3: Empty YAML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("")  # Empty file
            empty_file = f.name
        
        try:
            temp_config_dir = Path(empty_file).parent
            temp_loader = UnifiedConfigLoader(temp_config_dir)
            config_name = Path(empty_file).stem
            
            config = temp_loader.load_config(config_name)
            
            self.record_test(
                "ERROR_EMPTY_YAML",
                "Empty YAML file handling",
                config is None,
                f"Empty file returned: {config}"
            )
        except Exception as e:
            self.record_test(
                "ERROR_EMPTY_YAML",
                "Empty YAML file handling",
                False,
                f"Exception on empty file: {type(e).__name__}: {e}"
            )
        finally:
            try:
                os.unlink(empty_file)
            except:
                pass
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test 1: Very large configuration file
        try:
            # Create a large config programmatically and test load time
            large_config = {
                'large_section': {
                    f'item_{i}': {
                        'value': f'data_{i}',
                        'nested': {'deep': f'nested_value_{i}'}
                    } for i in range(1000)
                }
            }
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
                yaml.dump(large_config, f)
                large_file = f.name
            
            temp_config_dir = Path(large_file).parent
            temp_loader = UnifiedConfigLoader(temp_config_dir)
            config_name = Path(large_file).stem
            
            start_time = time.time()
            loaded_config = temp_loader.load_config(config_name)
            load_time = (time.time() - start_time) * 1000
            
            self.record_test(
                "EDGE_LARGE_CONFIG",
                "Large configuration file loading",
                loaded_config is not None and load_time < 1000,  # Should load within 1 second
                f"Load time: {load_time:.1f}ms, Items: {len(loaded_config.get('large_section', {}))}"
            )
            
        except Exception as e:
            self.record_test(
                "EDGE_LARGE_CONFIG",
                "Large configuration file loading",
                False,
                str(e)
            )
        finally:
            try:
                os.unlink(large_file)
            except:
                pass
        
        # Test 2: Deep nesting
        try:
            deep_config = {'level1': {'level2': {'level3': {'level4': {'level5': 'deep_value'}}}}}
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
                yaml.dump(deep_config, f)
                deep_file = f.name
            
            temp_config_dir = Path(deep_file).parent
            temp_loader = UnifiedConfigLoader(temp_config_dir)
            config_name = Path(deep_file).stem
            
            loaded_config = temp_loader.load_config(config_name)
            deep_value = temp_loader.get_section(config_name, 'level1.level2.level3.level4.level5')
            
            self.record_test(
                "EDGE_DEEP_NESTING",
                "Deep nested configuration access",
                deep_value == 'deep_value',
                f"Retrieved value: {deep_value}"
            )
            
        except Exception as e:
            self.record_test(
                "EDGE_DEEP_NESTING",
                "Deep nested configuration access",
                False,
                str(e)
            )
        finally:
            try:
                os.unlink(deep_file)
            except:
                pass
        
        # Test 3: Unicode content
        try:
            unicode_config = {
                'unicode_section': {
                    'chinese': '中文配置',
                    'emoji': '🚀✨💡',
                    'special_chars': 'àáâãäåæç'
                }
            }
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as f:
                yaml.dump(unicode_config, f, allow_unicode=True)
                unicode_file = f.name
            
            temp_config_dir = Path(unicode_file).parent
            temp_loader = UnifiedConfigLoader(temp_config_dir)
            config_name = Path(unicode_file).stem
            
            loaded_config = temp_loader.load_config(config_name)
            
            self.record_test(
                "EDGE_UNICODE_CONTENT",
                "Unicode content handling",
                loaded_config is not None and 'unicode_section' in loaded_config,
                f"Unicode data: {loaded_config.get('unicode_section', {})}"
            )
            
        except Exception as e:
            self.record_test(
                "EDGE_UNICODE_CONTENT",
                "Unicode content handling",
                False,
                str(e)
            )
        finally:
            try:
                os.unlink(unicode_file)
            except:
                pass
    
    def test_performance(self):
        """Test performance characteristics."""
        # Test 1: Cold load performance
        cold_load_times = []
        for yaml_file in self.all_yaml_files[:3]:  # Test first 3 files
            config_name = yaml_file.stem
            
            # Force reload to ensure cold load
            start_time = time.time()
            config_loader.load_config(config_name, force_reload=True)
            load_time = (time.time() - start_time) * 1000
            cold_load_times.append(load_time)
        
        avg_cold_load = sum(cold_load_times) / len(cold_load_times) if cold_load_times else 0
        self.record_test(
            "PERF_COLD_LOAD",
            "Cold load performance",
            avg_cold_load < 100,  # Target: < 100ms average
            f"Average cold load time: {avg_cold_load:.1f}ms"
        )
        
        # Test 2: Cache hit performance
        if self.all_yaml_files:
            config_name = self.all_yaml_files[0].stem
            
            # Load once to cache
            config_loader.load_config(config_name)
            
            # Test cache hit
            cache_hit_times = []
            for _ in range(5):
                start_time = time.time()
                config_loader.load_config(config_name)
                cache_time = (time.time() - start_time) * 1000
                cache_hit_times.append(cache_time)
            
            avg_cache_time = sum(cache_hit_times) / len(cache_hit_times)
            self.record_test(
                "PERF_CACHE_HIT",
                "Cache hit performance",
                avg_cache_time < 10,  # Target: < 10ms for cache hits
                f"Average cache hit time: {avg_cache_time:.2f}ms"
            )
    
    def test_cache_functionality(self):
        """Test caching mechanism."""
        if not self.all_yaml_files:
            self.record_test("CACHE_NO_FILES", "No YAML files for cache test", False, "")
            return
        
        config_name = self.all_yaml_files[0].stem
        
        # Test 1: Cache population
        config1 = config_loader.load_config(config_name)
        config2 = config_loader.load_config(config_name)  # Should hit cache
        
        self.record_test(
            "CACHE_POPULATION",
            "Cache population and hit",
            config1 == config2,
            "Cached config matches original"
        )
        
        # Test 2: Force reload bypasses cache
        config3 = config_loader.load_config(config_name, force_reload=True)
        
        self.record_test(
            "CACHE_FORCE_RELOAD",
            "Force reload bypasses cache",
            config3 == config1,  # Content should still match
            "Force reload content matches"
        )
    
    def test_environment_variables(self):
        """Test environment variable interpolation."""
        # Set a test environment variable
        os.environ['TEST_YAML_VAR'] = 'test_value_123'
        
        try:
            test_config = {
                'env_test': {
                    'simple_var': '${TEST_YAML_VAR}',
                    'var_with_default': '${NONEXISTENT_VAR:default_value}',
                    'regular_value': 'no_substitution'
                }
            }
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
                yaml.dump(test_config, f)
                env_file = f.name
            
            temp_config_dir = Path(env_file).parent
            temp_loader = UnifiedConfigLoader(temp_config_dir)
            config_name = Path(env_file).stem
            
            loaded_config = temp_loader.load_config(config_name)
            env_section = loaded_config.get('env_test', {})
            
            # Test environment variable substitution
            self.record_test(
                "ENV_VAR_SUBSTITUTION",
                "Environment variable substitution",
                env_section.get('simple_var') == 'test_value_123',
                f"Substituted value: {env_section.get('simple_var')}"
            )
            
            # Test default value substitution
            self.record_test(
                "ENV_VAR_DEFAULT",
                "Environment variable default value",
                env_section.get('var_with_default') == 'default_value',
                f"Default value: {env_section.get('var_with_default')}"
            )
            
            # Test non-substituted values remain unchanged
            self.record_test(
                "ENV_VAR_NO_SUBSTITUTION",
                "Non-environment values unchanged",
                env_section.get('regular_value') == 'no_substitution',
                f"Regular value: {env_section.get('regular_value')}"
            )
            
        except Exception as e:
            self.record_test(
                "ENV_VAR_INTERPOLATION",
                "Environment variable interpolation",
                False,
                str(e)
            )
        finally:
            # Clean up
            try:
                os.unlink(env_file)
                del os.environ['TEST_YAML_VAR']
            except:
                pass
    
    def test_include_functionality(self):
        """Test include/merge functionality."""
        try:
            # Create base config
            base_config = {
                'base_section': {
                    'base_value': 'from_base'
                },
                '__include__': ['included_config.yaml']
            }
            
            # Create included config
            included_config = {
                'included_section': {
                    'included_value': 'from_included'
                },
                'base_section': {
                    'override_value': 'from_included'
                }
            }
            
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir_path = Path(temp_dir)
                
                # Write base config
                with open(temp_dir_path / 'base_config.yaml', 'w') as f:
                    yaml.dump(base_config, f)
                
                # Write included config
                with open(temp_dir_path / 'included_config.yaml', 'w') as f:
                    yaml.dump(included_config, f)
                
                # Test include functionality
                temp_loader = UnifiedConfigLoader(temp_dir_path)
                loaded_config = temp_loader.load_config('base_config')
                
                # Test that included section is present
                self.record_test(
                    "INCLUDE_SECTION_PRESENT",
                    "Included section is present",
                    'included_section' in loaded_config,
                    f"Config sections: {list(loaded_config.keys())}"
                )
                
                # Test that base sections are preserved
                self.record_test(
                    "INCLUDE_BASE_PRESERVED",
                    "Base configuration preserved",
                    'base_section' in loaded_config,
                    f"Base section: {loaded_config.get('base_section', {})}"
                )
                
        except Exception as e:
            self.record_test(
                "INCLUDE_FUNCTIONALITY",
                "Include functionality test",
                False,
                str(e)
            )
    
    def generate_report(self):
        """Generate comprehensive test report."""
        print("\n" + "=" * 60)
        print("🔍 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        # Calculate statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['passed'])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed:      {passed_tests} ✅")
        print(f"Failed:      {failed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Group results by category
        categories = {}
        for result in self.test_results:
            category = result['test_name'].split('_')[0]
            if category not in categories:
                categories[category] = {'passed': 0, 'failed': 0, 'total': 0}
            categories[category]['total'] += 1
            if result['passed']:
                categories[category]['passed'] += 1
            else:
                categories[category]['failed'] += 1
        
        print(f"\n📊 Results by Category:")
        for category, stats in categories.items():
            rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"  {category:20} {stats['passed']:2d}/{stats['total']:2d} ({rate:5.1f}%)")
        
        # Show failed tests
        failed_tests_list = [r for r in self.test_results if not r['passed']]
        if failed_tests_list:
            print(f"\n❌ Failed Tests ({len(failed_tests_list)}):")
            for failure in failed_tests_list:
                print(f"  • {failure['test_name']}: {failure['description']}")
                if failure['details']:
                    print(f"    {failure['details']}")
        
        # Configuration files summary
        print(f"\n📁 Configuration Files Discovered:")
        if self.all_yaml_files:
            for yaml_file in self.all_yaml_files:
                size = yaml_file.stat().st_size
                print(f"  • {yaml_file.name:25} ({size:,} bytes)")
        else:
            print("  No YAML files found")
        
        # Performance summary
        performance_tests = [r for r in self.test_results if 'PERF_' in r['test_name']]
        if performance_tests:
            print(f"\n⚡ Performance Summary:")
            for perf_test in performance_tests:
                status = "✅" if perf_test['passed'] else "❌"
                print(f"  {status} {perf_test['description']}")
                if perf_test['details']:
                    print(f"      {perf_test['details']}")
        
        # Overall assessment
        print(f"\n🎯 Overall Assessment:")
        if success_rate >= 90:
            print("   ✅ EXCELLENT - YAML loader is functioning properly")
        elif success_rate >= 75:
            print("   ⚠️  GOOD - YAML loader mostly working, minor issues detected")
        elif success_rate >= 50:
            print("   ⚠️  FAIR - YAML loader has some significant issues")
        else:
            print("   ❌ POOR - YAML loader has major problems requiring attention")
        
        print("\n" + "=" * 60)
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': success_rate,
            'categories': categories,
            'failed_tests_details': failed_tests_list,
            'yaml_files_found': len(self.all_yaml_files)
        }


def main():
    """Main test execution."""
    test_suite = YAMLLoaderTestSuite()
    
    try:
        results = test_suite.run_all_tests()
        
        # Exit with appropriate code
        if results['success_rate'] >= 90:
            sys.exit(0)  # All good
        elif results['success_rate'] >= 50:
            sys.exit(1)  # Some issues
        else:
            sys.exit(2)  # Major issues
            
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR during test execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(3)


if __name__ == "__main__":
    main()