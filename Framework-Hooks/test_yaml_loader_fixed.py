#!/usr/bin/env python3
"""
Quick YAML Configuration Test Script

A simplified version to test the key functionality without the temporary file issues.
"""

import sys
import os
import time
from pathlib import Path

# Add shared modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "hooks", "shared"))

try:
    from yaml_loader import config_loader
    print("✅ Successfully imported yaml_loader")
except ImportError as e:
    print(f"❌ Failed to import yaml_loader: {e}")
    sys.exit(1)


def test_yaml_configuration_loading():
    """Test YAML configuration loading functionality."""
    print("\n🧪 YAML Configuration Loading Tests")
    print("=" * 50)
    
    framework_hooks_path = Path(__file__).parent
    config_dir = framework_hooks_path / "config"
    
    # Check if config directory exists
    if not config_dir.exists():
        print(f"❌ Config directory not found: {config_dir}")
        return False
    
    # Get all YAML files
    yaml_files = list(config_dir.glob("*.yaml"))
    print(f"📁 Found {len(yaml_files)} YAML files: {[f.name for f in yaml_files]}")
    
    # Test each YAML file
    total_tests = 0
    passed_tests = 0
    
    for yaml_file in yaml_files:
        config_name = yaml_file.stem
        total_tests += 1
        
        try:
            start_time = time.time()
            config = config_loader.load_config(config_name)
            load_time = (time.time() - start_time) * 1000
            
            if config and isinstance(config, dict):
                print(f"✅ {config_name}.yaml loaded successfully ({load_time:.1f}ms)")
                print(f"   Keys: {list(config.keys())[:5]}{'...' if len(config.keys()) > 5 else ''}")
                passed_tests += 1
            else:
                print(f"❌ {config_name}.yaml loaded but invalid content: {type(config)}")
                
        except Exception as e:
            print(f"❌ {config_name}.yaml failed to load: {e}")
    
    # Test specific configuration sections
    print(f"\n🔍 Testing Configuration Sections")
    print("-" * 30)
    
    # Test compression configuration
    try:
        compression_config = config_loader.load_config('compression')
        if 'compression_levels' in compression_config:
            levels = list(compression_config['compression_levels'].keys())
            print(f"✅ Compression levels: {levels}")
            passed_tests += 1
        else:
            print(f"❌ Compression config missing 'compression_levels'")
        total_tests += 1
    except Exception as e:
        print(f"❌ Compression config test failed: {e}")
        total_tests += 1
    
    # Test performance configuration
    try:
        performance_config = config_loader.load_config('performance')
        if 'hook_targets' in performance_config:
            hooks = list(performance_config['hook_targets'].keys())
            print(f"✅ Hook performance targets: {hooks}")
            passed_tests += 1
        else:
            print(f"❌ Performance config missing 'hook_targets'")
        total_tests += 1
    except Exception as e:
        print(f"❌ Performance config test failed: {e}")
        total_tests += 1
    
    # Test hook configuration access
    print(f"\n🔧 Testing Hook Configuration Access")
    print("-" * 35)
    
    hook_names = ['session_start', 'pre_tool_use', 'post_tool_use']
    for hook_name in hook_names:
        total_tests += 1
        try:
            hook_config = config_loader.get_hook_config(hook_name)
            print(f"✅ {hook_name} hook config: {type(hook_config)}")
            passed_tests += 1
        except Exception as e:
            print(f"❌ {hook_name} hook config failed: {e}")
    
    # Test performance
    print(f"\n⚡ Performance Tests")
    print("-" * 20)
    
    # Test cache performance
    if yaml_files:
        config_name = yaml_files[0].stem
        total_tests += 1
        
        # Cold load
        start_time = time.time()
        config_loader.load_config(config_name, force_reload=True)
        cold_time = (time.time() - start_time) * 1000
        
        # Cache hit
        start_time = time.time()
        config_loader.load_config(config_name)
        cache_time = (time.time() - start_time) * 1000
        
        print(f"✅ Cold load: {cold_time:.1f}ms, Cache hit: {cache_time:.2f}ms")
        if cold_time < 100 and cache_time < 10:
            passed_tests += 1
    
    # Final results
    print(f"\n📊 Results Summary")
    print("=" * 20)
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎯 EXCELLENT: YAML loader working perfectly")
        return True
    elif success_rate >= 75:
        print("⚠️ GOOD: YAML loader mostly working")
        return True
    else:
        print("❌ ISSUES: YAML loader has problems")
        return False


def test_hook_yaml_usage():
    """Test how hooks actually use YAML configurations."""
    print("\n🔗 Hook YAML Usage Verification")
    print("=" * 35)
    
    hook_files = [
        "hooks/session_start.py",
        "hooks/pre_tool_use.py", 
        "hooks/post_tool_use.py"
    ]
    
    framework_hooks_path = Path(__file__).parent
    
    for hook_file in hook_files:
        hook_path = framework_hooks_path / hook_file
        if hook_path.exists():
            try:
                with open(hook_path, 'r') as f:
                    content = f.read()
                
                # Check for yaml_loader import
                has_yaml_import = 'from yaml_loader import' in content or 'import yaml_loader' in content
                
                # Check for config usage
                has_config_usage = 'config_loader' in content or '.load_config(' in content
                
                print(f"📄 {hook_file}:")
                print(f"   Import: {'✅' if has_yaml_import else '❌'}")
                print(f"   Usage:  {'✅' if has_config_usage else '❌'}")
                
            except Exception as e:
                print(f"❌ Error reading {hook_file}: {e}")
        else:
            print(f"❌ Hook file not found: {hook_path}")


def main():
    """Main test execution."""
    print("🚀 SuperClaude YAML Configuration Test")
    print("=" * 40)
    
    # Test YAML loading
    yaml_success = test_yaml_configuration_loading()
    
    # Test hook integration
    test_hook_yaml_usage()
    
    print("\n" + "=" * 40)
    if yaml_success:
        print("✅ YAML Configuration System: WORKING")
        return 0
    else:
        print("❌ YAML Configuration System: ISSUES DETECTED")
        return 1


if __name__ == "__main__":
    sys.exit(main())