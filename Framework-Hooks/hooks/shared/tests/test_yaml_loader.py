#!/usr/bin/env python3
"""
Comprehensive tests for yaml_loader.py

Tests all core functionality including:
- YAML and JSON configuration loading
- Caching and hot-reload capabilities
- Environment variable interpolation
- Hook configuration management
- Error handling and validation
"""

import unittest
import sys
import tempfile
import json
import yaml
import os
import time
from pathlib import Path

# Add the shared directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from yaml_loader import UnifiedConfigLoader


class TestUnifiedConfigLoader(unittest.TestCase):
    """Comprehensive tests for UnifiedConfigLoader."""
    
    def setUp(self):
        """Set up test environment with temporary directories and files."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_root = Path(self.temp_dir)
        self.config_dir = self.project_root / "config"
        self.config_dir.mkdir(exist_ok=True)
        
        # Create test configuration files
        self._create_test_configs()
        
        # Create loader instance
        self.loader = UnifiedConfigLoader(self.project_root)
    
    def _create_test_configs(self):
        """Create test configuration files."""
        # Claude settings.json
        claude_settings = {
            "hooks": {
                "session_start": {
                    "enabled": True,
                    "script": "session_start.py"
                },
                "pre_tool_use": {
                    "enabled": True,
                    "script": "pre_tool_use.py"
                }
            },
            "general": {
                "timeout": 30,
                "max_retries": 3
            }
        }
        
        settings_file = self.project_root / "settings.json"
        with open(settings_file, 'w') as f:
            json.dump(claude_settings, f, indent=2)
        
        # SuperClaude config
        superclaude_config = {
            "global_configuration": {
                "performance_monitoring": {
                    "enabled": True,
                    "target_response_time_ms": 200,
                    "memory_usage_limit": 512
                }
            },
            "hook_configurations": {
                "session_start": {
                    "enabled": True,
                    "performance_target_ms": 50,
                    "logging_level": "INFO"
                },
                "pre_tool_use": {
                    "enabled": True,
                    "performance_target_ms": 200,
                    "intelligent_routing": True
                }
            },
            "mcp_server_integration": {
                "servers": {
                    "morphllm": {
                        "enabled": True,
                        "priority": 1,
                        "capabilities": ["editing", "fast_apply"]
                    },
                    "serena": {
                        "enabled": True,
                        "priority": 2,
                        "capabilities": ["semantic_analysis", "project_context"]
                    }
                }
            }
        }
        
        superclaude_file = self.project_root / "superclaude-config.json"
        with open(superclaude_file, 'w') as f:
            json.dump(superclaude_config, f, indent=2)
        
        # YAML configuration files
        compression_config = {
            "compression": {
                "enabled": True,
                "default_level": "efficient",
                "quality_threshold": 0.95,
                "selective_compression": {
                    "framework_content": False,
                    "user_content": True,
                    "session_data": True
                }
            }
        }
        
        compression_file = self.config_dir / "compression.yaml"
        with open(compression_file, 'w') as f:
            yaml.dump(compression_config, f, default_flow_style=False)
        
        # Configuration with environment variables
        env_config = {
            "database": {
                "host": "${DB_HOST:localhost}",
                "port": "${DB_PORT:5432}",
                "name": "${DB_NAME}",
                "debug": "${DEBUG:false}"
            },
            "api": {
                "base_url": "${API_URL:http://localhost:8000}",
                "timeout": "${API_TIMEOUT:30}"
            }
        }
        
        env_file = self.config_dir / "environment.yaml"
        with open(env_file, 'w') as f:
            yaml.dump(env_config, f, default_flow_style=False)
        
        # Configuration with includes
        base_config = {
            "__include__": ["included.yaml"],
            "base": {
                "name": "base_config",
                "version": "1.0"
            }
        }
        
        included_config = {
            "included": {
                "feature": "included_feature",
                "enabled": True
            }
        }
        
        base_file = self.config_dir / "base.yaml"
        with open(base_file, 'w') as f:
            yaml.dump(base_config, f, default_flow_style=False)
        
        included_file = self.config_dir / "included.yaml"
        with open(included_file, 'w') as f:
            yaml.dump(included_config, f, default_flow_style=False)
    
    def test_json_config_loading(self):
        """Test loading JSON configuration files."""
        # Test Claude settings loading
        claude_config = self.loader.load_config('claude_settings')
        
        self.assertIsInstance(claude_config, dict)
        self.assertIn('hooks', claude_config)
        self.assertIn('general', claude_config)
        self.assertEqual(claude_config['general']['timeout'], 30)
        
        # Test SuperClaude config loading
        superclaude_config = self.loader.load_config('superclaude_config')
        
        self.assertIsInstance(superclaude_config, dict)
        self.assertIn('global_configuration', superclaude_config)
        self.assertIn('hook_configurations', superclaude_config)
        self.assertTrue(superclaude_config['global_configuration']['performance_monitoring']['enabled'])
    
    def test_yaml_config_loading(self):
        """Test loading YAML configuration files."""
        compression_config = self.loader.load_config('compression')
        
        self.assertIsInstance(compression_config, dict)
        self.assertIn('compression', compression_config)
        self.assertTrue(compression_config['compression']['enabled'])
        self.assertEqual(compression_config['compression']['default_level'], 'efficient')
        self.assertEqual(compression_config['compression']['quality_threshold'], 0.95)
    
    def test_section_retrieval(self):
        """Test retrieving specific configuration sections."""
        # Test dot notation access
        timeout = self.loader.get_section('claude_settings', 'general.timeout')
        self.assertEqual(timeout, 30)
        
        # Test nested access
        perf_enabled = self.loader.get_section(
            'superclaude_config', 
            'global_configuration.performance_monitoring.enabled'
        )
        self.assertTrue(perf_enabled)
        
        # Test with default value
        missing_value = self.loader.get_section('compression', 'missing.path', 'default')
        self.assertEqual(missing_value, 'default')
        
        # Test invalid path
        invalid = self.loader.get_section('compression', 'invalid.path')
        self.assertIsNone(invalid)
    
    def test_hook_configuration_access(self):
        """Test hook-specific configuration access."""
        # Test hook config retrieval
        session_config = self.loader.get_hook_config('session_start')
        self.assertIsInstance(session_config, dict)
        self.assertTrue(session_config['enabled'])
        self.assertEqual(session_config['performance_target_ms'], 50)
        
        # Test specific hook config section
        perf_target = self.loader.get_hook_config('pre_tool_use', 'performance_target_ms')
        self.assertEqual(perf_target, 200)
        
        # Test with default
        missing_hook = self.loader.get_hook_config('missing_hook', 'some_setting', 'default')
        self.assertEqual(missing_hook, 'default')
        
        # Test hook enabled check
        self.assertTrue(self.loader.is_hook_enabled('session_start'))
        self.assertFalse(self.loader.is_hook_enabled('missing_hook'))
    
    def test_claude_hooks_retrieval(self):
        """Test Claude Code hook definitions retrieval."""
        hooks = self.loader.get_claude_hooks()
        
        self.assertIsInstance(hooks, dict)
        self.assertIn('session_start', hooks)
        self.assertIn('pre_tool_use', hooks)
        self.assertTrue(hooks['session_start']['enabled'])
        self.assertEqual(hooks['session_start']['script'], 'session_start.py')
    
    def test_superclaude_config_access(self):
        """Test SuperClaude configuration access methods."""
        # Test full config
        full_config = self.loader.get_superclaude_config()
        self.assertIsInstance(full_config, dict)
        self.assertIn('global_configuration', full_config)
        
        # Test specific section
        perf_config = self.loader.get_superclaude_config('global_configuration.performance_monitoring')
        self.assertIsInstance(perf_config, dict)
        self.assertTrue(perf_config['enabled'])
        self.assertEqual(perf_config['target_response_time_ms'], 200)
    
    def test_mcp_server_configuration(self):
        """Test MCP server configuration access."""
        # Test all MCP config
        mcp_config = self.loader.get_mcp_server_config()
        self.assertIsInstance(mcp_config, dict)
        self.assertIn('servers', mcp_config)
        
        # Test specific server config
        morphllm_config = self.loader.get_mcp_server_config('morphllm')
        self.assertIsInstance(morphllm_config, dict)
        self.assertTrue(morphllm_config['enabled'])
        self.assertEqual(morphllm_config['priority'], 1)
        self.assertIn('editing', morphllm_config['capabilities'])
    
    def test_performance_targets_access(self):
        """Test performance targets access."""
        perf_targets = self.loader.get_performance_targets()
        
        self.assertIsInstance(perf_targets, dict)
        self.assertTrue(perf_targets['enabled'])
        self.assertEqual(perf_targets['target_response_time_ms'], 200)
        self.assertEqual(perf_targets['memory_usage_limit'], 512)
    
    def test_environment_variable_interpolation(self):
        """Test environment variable interpolation."""
        # Set test environment variables
        os.environ['DB_HOST'] = 'test-db-server'
        os.environ['DB_NAME'] = 'test_database'
        os.environ['API_URL'] = 'https://api.example.com'
        
        try:
            env_config = self.loader.load_config('environment')
            
            # Should interpolate environment variables
            self.assertEqual(env_config['database']['host'], 'test-db-server')
            self.assertEqual(env_config['database']['name'], 'test_database')
            self.assertEqual(env_config['api']['base_url'], 'https://api.example.com')
            
            # Should use defaults when env var not set
            self.assertEqual(env_config['database']['port'], '5432')  # Default
            self.assertEqual(env_config['database']['debug'], 'false')  # Default
            self.assertEqual(env_config['api']['timeout'], '30')  # Default
            
        finally:
            # Clean up environment variables
            for var in ['DB_HOST', 'DB_NAME', 'API_URL']:
                if var in os.environ:
                    del os.environ[var]
    
    def test_include_processing(self):
        """Test configuration include/merge functionality."""
        base_config = self.loader.load_config('base')
        
        # Should have base configuration
        self.assertIn('base', base_config)
        self.assertEqual(base_config['base']['name'], 'base_config')
        
        # Should have included configuration
        self.assertIn('included', base_config)
        self.assertEqual(base_config['included']['feature'], 'included_feature')
        self.assertTrue(base_config['included']['enabled'])
    
    def test_caching_functionality(self):
        """Test configuration caching and hot-reload."""
        # Load config multiple times
        config1 = self.loader.load_config('compression')
        config2 = self.loader.load_config('compression')
        
        # Should be the same object (cached)
        self.assertIs(config1, config2)
        
        # Check cache state
        self.assertIn('compression', self.loader._cache)
        self.assertIn('compression', self.loader._file_hashes)
        
        # Force reload
        config3 = self.loader.load_config('compression', force_reload=True)
        self.assertIsNot(config1, config3)
        self.assertEqual(config1, config3)  # Content should be same
    
    def test_file_modification_detection(self):
        """Test file modification detection for cache invalidation."""
        # Load initial config
        initial_config = self.loader.load_config('compression')
        initial_level = initial_config['compression']['default_level']
        
        # Wait a bit to ensure different modification time
        time.sleep(0.1)
        
        # Modify the file
        compression_file = self.config_dir / "compression.yaml"
        modified_config = {
            "compression": {
                "enabled": True,
                "default_level": "critical",  # Changed value
                "quality_threshold": 0.95
            }
        }
        
        with open(compression_file, 'w') as f:
            yaml.dump(modified_config, f, default_flow_style=False)
        
        # Load again - should detect modification and reload
        updated_config = self.loader.load_config('compression')
        updated_level = updated_config['compression']['default_level']
        
        # Should have new value
        self.assertNotEqual(initial_level, updated_level)
        self.assertEqual(updated_level, 'critical')
    
    def test_reload_all_functionality(self):
        """Test reloading all cached configurations."""
        # Load multiple configs
        self.loader.load_config('compression')
        self.loader.load_config('claude_settings')
        self.loader.load_config('superclaude_config')
        
        # Should have multiple cached configs
        self.assertGreaterEqual(len(self.loader._cache), 3)
        
        # Reload all
        self.loader.reload_all()
        
        # Cache should still exist but content may be refreshed
        self.assertGreaterEqual(len(self.loader._cache), 3)
    
    def test_performance_requirements(self):
        """Test that configuration loading meets performance requirements."""
        # First load (cold)
        start_time = time.time()
        config1 = self.loader.load_config('compression')
        cold_load_time = time.time() - start_time
        
        # Second load (cached)
        start_time = time.time()
        config2 = self.loader.load_config('compression')
        cached_load_time = time.time() - start_time
        
        # Cached load should be much faster (< 10ms)
        self.assertLess(cached_load_time * 1000, 10, "Cached load should be < 10ms")
        
        # Should be same object (cached)
        self.assertIs(config1, config2)
        
        # Cold load should still be reasonable (< 100ms)
        self.assertLess(cold_load_time * 1000, 100, "Cold load should be < 100ms")
    
    def test_error_handling(self):
        """Test error handling for various failure scenarios."""
        # Test missing file
        with self.assertRaises(FileNotFoundError):
            self.loader.load_config('nonexistent')
        
        # Test invalid YAML
        invalid_yaml_file = self.config_dir / "invalid.yaml"
        with open(invalid_yaml_file, 'w') as f:
            f.write("invalid: yaml: content: [unclosed")
        
        with self.assertRaises(ValueError):
            self.loader.load_config('invalid')
        
        # Test invalid JSON
        invalid_json_file = self.project_root / "invalid.json"
        with open(invalid_json_file, 'w') as f:
            f.write('{"invalid": json content}')
        
        # Add to config sources for testing
        self.loader._config_sources['invalid_json'] = invalid_json_file
        
        with self.assertRaises(ValueError):
            self.loader.load_config('invalid_json')
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Empty YAML file
        empty_yaml_file = self.config_dir / "empty.yaml"
        with open(empty_yaml_file, 'w') as f:
            f.write("")
        
        empty_config = self.loader.load_config('empty')
        self.assertIsNone(empty_config)
        
        # YAML file with only comments
        comment_yaml_file = self.config_dir / "comments.yaml"
        with open(comment_yaml_file, 'w') as f:
            f.write("# This is a comment\n# Another comment\n")
        
        comment_config = self.loader.load_config('comments')
        self.assertIsNone(comment_config)
        
        # Very deep nesting
        deep_config = {"level1": {"level2": {"level3": {"level4": {"value": "deep"}}}}}
        deep_yaml_file = self.config_dir / "deep.yaml"
        with open(deep_yaml_file, 'w') as f:
            yaml.dump(deep_config, f)
        
        loaded_deep = self.loader.load_config('deep')
        deep_value = self.loader.get_section('deep', 'level1.level2.level3.level4.value')
        self.assertEqual(deep_value, 'deep')
        
        # Large configuration file
        large_config = {f"section_{i}": {f"key_{j}": f"value_{i}_{j}" 
                       for j in range(10)} for i in range(100)}
        large_yaml_file = self.config_dir / "large.yaml"
        with open(large_yaml_file, 'w') as f:
            yaml.dump(large_config, f)
        
        start_time = time.time()
        large_loaded = self.loader.load_config('large')
        load_time = time.time() - start_time
        
        # Should load large config efficiently
        self.assertLess(load_time, 1.0)  # < 1 second
        self.assertEqual(len(large_loaded), 100)
    
    def test_concurrent_access(self):
        """Test concurrent configuration access."""
        import threading
        
        results = []
        exceptions = []
        
        def load_config_worker():
            try:
                config = self.loader.load_config('compression')
                results.append(config)
            except Exception as e:
                exceptions.append(e)
        
        # Create multiple threads
        threads = [threading.Thread(target=load_config_worker) for _ in range(10)]
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Should have no exceptions
        self.assertEqual(len(exceptions), 0, f"Concurrent access caused exceptions: {exceptions}")
        
        # All results should be identical (cached)
        self.assertEqual(len(results), 10)
        for result in results[1:]:
            self.assertIs(result, results[0])


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)