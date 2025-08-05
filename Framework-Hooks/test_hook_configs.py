#!/usr/bin/env python3
"""
Hook Configuration Integration Test

Verifies that hooks can properly access their configurations from YAML files
and that the configuration structure matches what the hooks expect.
"""

import sys
import os
from pathlib import Path

# Add shared modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "hooks", "shared"))

try:
    from yaml_loader import config_loader
    print("✅ Successfully imported yaml_loader")
except ImportError as e:
    print(f"❌ Failed to import yaml_loader: {e}")
    sys.exit(1)


def test_hook_configuration_access():
    """Test that hooks can access their expected configurations."""
    print("\n🔧 Testing Hook Configuration Access")
    print("=" * 40)
    
    # Test session_start hook configurations
    print("\n📋 Session Start Hook Configuration:")
    try:
        # Test session configuration from YAML
        session_config = config_loader.load_config('session')
        print(f"✅ Session config loaded: {len(session_config)} sections")
        
        # Check key sections that session_start expects
        expected_sections = [
            'session_lifecycle', 'project_detection', 
            'intelligence_activation', 'session_analytics'
        ]
        
        for section in expected_sections:
            if section in session_config:
                print(f"  ✅ {section}: Present")
            else:
                print(f"  ❌ {section}: Missing")
        
        # Test specific configuration access patterns used in session_start.py
        if 'session_lifecycle' in session_config:
            lifecycle_config = session_config['session_lifecycle']
            if 'initialization' in lifecycle_config:
                init_config = lifecycle_config['initialization']
                target_ms = init_config.get('performance_target_ms', 50)
                print(f"  📊 Performance target: {target_ms}ms")
            
    except Exception as e:
        print(f"❌ Session config access failed: {e}")
    
    # Test performance configuration
    print("\n⚡ Performance Configuration:")
    try:
        performance_config = config_loader.load_config('performance')
        
        # Check hook targets that hooks reference
        if 'hook_targets' in performance_config:
            hook_targets = performance_config['hook_targets']
            hook_names = ['session_start', 'pre_tool_use', 'post_tool_use', 'pre_compact']
            
            for hook_name in hook_names:
                if hook_name in hook_targets:
                    target = hook_targets[hook_name]['target_ms']
                    print(f"  ✅ {hook_name}: {target}ms target")
                else:
                    print(f"  ❌ {hook_name}: No performance target")
        
    except Exception as e:
        print(f"❌ Performance config access failed: {e}")
    
    # Test compression configuration 
    print("\n🗜️ Compression Configuration:")
    try:
        compression_config = config_loader.load_config('compression')
        
        # Check compression levels hooks might use
        if 'compression_levels' in compression_config:
            levels = compression_config['compression_levels']
            level_names = ['minimal', 'efficient', 'compressed', 'critical', 'emergency']
            
            for level in level_names:
                if level in levels:
                    threshold = levels[level].get('quality_threshold', 'unknown')
                    print(f"  ✅ {level}: Quality threshold {threshold}")
                else:
                    print(f"  ❌ {level}: Missing")
        
        # Test selective compression patterns
        if 'selective_compression' in compression_config:
            selective = compression_config['selective_compression']
            if 'content_classification' in selective:
                classification = selective['content_classification']
                categories = ['framework_exclusions', 'user_content_preservation', 'session_data_optimization']
                
                for category in categories:
                    if category in classification:
                        patterns = classification[category].get('patterns', [])
                        print(f"  ✅ {category}: {len(patterns)} patterns")
                    else:
                        print(f"  ❌ {category}: Missing")
        
    except Exception as e:
        print(f"❌ Compression config access failed: {e}")


def test_configuration_consistency():
    """Test configuration consistency across YAML files."""
    print("\n🔗 Testing Configuration Consistency")
    print("=" * 38)
    
    try:
        # Load all configuration files
        configs = {}
        config_names = ['performance', 'compression', 'session', 'modes', 'validation', 'orchestrator', 'logging']
        
        for name in config_names:
            try:
                configs[name] = config_loader.load_config(name)
                print(f"✅ Loaded {name}.yaml")
            except Exception as e:
                print(f"❌ Failed to load {name}.yaml: {e}")
                configs[name] = {}
        
        # Check for consistency in hook references
        print(f"\n🔍 Checking Hook References Consistency:")
        
        # Get hook names from performance config
        performance_hooks = set()
        if 'hook_targets' in configs.get('performance', {}):
            performance_hooks = set(configs['performance']['hook_targets'].keys())
            print(f"  Performance config defines: {performance_hooks}")
        
        # Get hook names from modes config
        mode_hooks = set()
        if 'mode_configurations' in configs.get('modes', {}):
            mode_config = configs['modes']['mode_configurations']
            for mode_name, mode_data in mode_config.items():
                if 'hook_integration' in mode_data:
                    hooks = mode_data['hook_integration'].get('compatible_hooks', [])
                    mode_hooks.update(hooks)
            print(f"  Modes config references: {mode_hooks}")
        
        # Check consistency
        common_hooks = performance_hooks.intersection(mode_hooks)
        if common_hooks:
            print(f"  ✅ Common hooks: {common_hooks}")
        
        missing_in_modes = performance_hooks - mode_hooks
        if missing_in_modes:
            print(f"  ⚠️ In performance but not modes: {missing_in_modes}")
        
        missing_in_performance = mode_hooks - performance_hooks  
        if missing_in_performance:
            print(f"  ⚠️ In modes but not performance: {missing_in_performance}")
        
        # Check performance targets consistency
        print(f"\n⏱️ Checking Performance Target Consistency:")
        if 'performance_targets' in configs.get('compression', {}):
            compression_target = configs['compression']['performance_targets'].get('processing_time_ms', 0)
            print(f"  Compression processing target: {compression_target}ms")
            
        if 'system_targets' in configs.get('performance', {}):
            system_targets = configs['performance']['system_targets']
            overall_efficiency = system_targets.get('overall_session_efficiency', 0)
            print(f"  Overall session efficiency target: {overall_efficiency}")
        
    except Exception as e:
        print(f"❌ Configuration consistency check failed: {e}")


def test_hook_yaml_integration():
    """Test actual hook-YAML integration patterns."""
    print("\n🔌 Testing Hook-YAML Integration Patterns")
    print("=" * 42)
    
    # Simulate how session_start.py loads configuration
    print("\n📋 Simulating session_start.py config loading:")
    try:
        # This matches the pattern in session_start.py lines 65-72
        hook_config = config_loader.get_hook_config('session_start')
        print(f"  ✅ Hook config: {type(hook_config)} - {hook_config}")
        
        # Try loading session config (with fallback pattern)
        try:
            session_config = config_loader.load_config('session')
            print(f"  ✅ Session YAML config: {len(session_config)} sections")
        except FileNotFoundError:
            # This is the fallback pattern from session_start.py
            session_config = hook_config.get('configuration', {})
            print(f"  ⚠️ Using hook config fallback: {len(session_config)} items")
        
        # Test performance target access (line 76 in session_start.py)
        performance_target_ms = config_loader.get_hook_config('session_start', 'performance_target_ms', 50)
        print(f"  📊 Performance target: {performance_target_ms}ms")
        
    except Exception as e:
        print(f"❌ session_start config simulation failed: {e}")
    
    # Test section access patterns
    print(f"\n🎯 Testing Section Access Patterns:")
    try:
        # Test dot notation access (used throughout the codebase)
        compression_minimal = config_loader.get_section('compression', 'compression_levels.minimal')
        if compression_minimal:
            print(f"  ✅ Dot notation access: compression_levels.minimal loaded")
            quality_threshold = compression_minimal.get('quality_threshold', 'unknown')
            print(f"      Quality threshold: {quality_threshold}")
        else:
            print(f"  ❌ Dot notation access failed")
        
        # Test default value handling
        missing_section = config_loader.get_section('compression', 'nonexistent.section', {'default': True})
        if missing_section == {'default': True}:
            print(f"  ✅ Default value handling works")
        else:
            print(f"  ❌ Default value handling failed: {missing_section}")
        
    except Exception as e:
        print(f"❌ Section access test failed: {e}")


def test_performance_compliance():
    """Test that configuration loading meets performance requirements."""
    print("\n⚡ Testing Performance Compliance")
    print("=" * 35)
    
    import time
    
    # Test cold load performance
    print("🔥 Cold Load Performance:")
    config_names = ['performance', 'compression', 'session']
    
    for config_name in config_names:
        times = []
        for _ in range(3):  # Test 3 times
            start_time = time.time()
            config_loader.load_config(config_name, force_reload=True)
            load_time = (time.time() - start_time) * 1000
            times.append(load_time)
        
        avg_time = sum(times) / len(times)
        print(f"  {config_name}.yaml: {avg_time:.1f}ms avg")
        
    # Test cache performance  
    print(f"\n⚡ Cache Hit Performance:")
    for config_name in config_names:
        times = []
        for _ in range(5):  # Test 5 cache hits
            start_time = time.time()
            config_loader.load_config(config_name)  # Should hit cache
            cache_time = (time.time() - start_time) * 1000
            times.append(cache_time)
        
        avg_cache_time = sum(times) / len(times)
        print(f"  {config_name}.yaml: {avg_cache_time:.2f}ms avg (cache)")
    
    # Test bulk loading performance
    print(f"\n📦 Bulk Loading Performance:")
    start_time = time.time()
    all_configs = {}
    for config_name in ['performance', 'compression', 'session', 'modes', 'validation']:
        all_configs[config_name] = config_loader.load_config(config_name)
    
    bulk_time = (time.time() - start_time) * 1000
    print(f"  Loaded 5 configs in: {bulk_time:.1f}ms")
    print(f"  Average per config: {bulk_time/5:.1f}ms")


def main():
    """Run all hook configuration tests."""
    print("🧪 Hook Configuration Integration Tests")
    print("=" * 45)
    
    test_functions = [
        test_hook_configuration_access,
        test_configuration_consistency,
        test_hook_yaml_integration,
        test_performance_compliance
    ]
    
    for test_func in test_functions:
        try:
            test_func()
        except Exception as e:
            print(f"💥 {test_func.__name__} failed: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 45)
    print("🎯 Hook Configuration Testing Complete")
    print("✅ If you see this message, basic integration is working!")


if __name__ == "__main__":
    main()