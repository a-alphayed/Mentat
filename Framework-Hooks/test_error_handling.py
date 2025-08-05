#!/usr/bin/env python3
"""
YAML Error Handling Test Script

Tests specific error conditions and edge cases for the yaml_loader module.
"""

import sys
import os
import tempfile
import yaml
from pathlib import Path

# Add shared modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "hooks", "shared"))

try:
    from yaml_loader import config_loader, UnifiedConfigLoader
    print("✅ Successfully imported yaml_loader")
except ImportError as e:
    print(f"❌ Failed to import yaml_loader: {e}")
    sys.exit(1)


def test_malformed_yaml():
    """Test handling of malformed YAML files."""
    print("\n🔥 Testing Malformed YAML Handling")
    print("-" * 40)
    
    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config_subdir = temp_path / "config"
        config_subdir.mkdir()
        
        # Create custom loader for temp directory
        temp_loader = UnifiedConfigLoader(temp_path)
        
        # Test 1: Malformed YAML structure
        malformed_content = """
invalid: yaml: content:
  - malformed
    - structure
  [missing bracket
"""
        malformed_file = config_subdir / "malformed.yaml"
        with open(malformed_file, 'w') as f:
            f.write(malformed_content)
        
        try:
            config = temp_loader.load_config('malformed')
            print("❌ Malformed YAML: Should have raised exception")
            return False
        except ValueError as e:
            if "YAML parsing error" in str(e):
                print(f"✅ Malformed YAML: Correctly caught ValueError - {e}")
            else:
                print(f"❌ Malformed YAML: Wrong ValueError message - {e}")
                return False
        except Exception as e:
            print(f"❌ Malformed YAML: Wrong exception type {type(e).__name__}: {e}")
            return False
        
        # Test 2: Empty YAML file
        empty_file = config_subdir / "empty.yaml"
        with open(empty_file, 'w') as f:
            f.write("")  # Empty file
        
        try:
            config = temp_loader.load_config('empty')
            if config is None:
                print("✅ Empty YAML: Returns None as expected")
            else:
                print(f"❌ Empty YAML: Should return None, got {type(config)}: {config}")
                return False
        except Exception as e:
            print(f"❌ Empty YAML: Unexpected exception - {type(e).__name__}: {e}")
            return False
        
        # Test 3: YAML with syntax errors
        syntax_error_content = """
valid_start: true
  invalid_indentation: bad
missing_colon value
"""
        syntax_file = config_subdir / "syntax_error.yaml"
        with open(syntax_file, 'w') as f:
            f.write(syntax_error_content)
        
        try:
            config = temp_loader.load_config('syntax_error')
            print("❌ Syntax Error YAML: Should have raised exception")
            return False
        except ValueError as e:
            print(f"✅ Syntax Error YAML: Correctly caught ValueError")
        except Exception as e:
            print(f"❌ Syntax Error YAML: Wrong exception type {type(e).__name__}: {e}")
            return False
    
    return True


def test_missing_files():
    """Test handling of missing configuration files."""
    print("\n📂 Testing Missing File Handling")
    print("-" * 35)
    
    # Test 1: Non-existent YAML file
    try:
        config = config_loader.load_config('definitely_does_not_exist')
        print("❌ Missing file: Should have raised FileNotFoundError")
        return False
    except FileNotFoundError:
        print("✅ Missing file: Correctly raised FileNotFoundError")
    except Exception as e:
        print(f"❌ Missing file: Wrong exception type {type(e).__name__}: {e}")
        return False
    
    # Test 2: Hook config for non-existent hook (should return default)
    try:
        hook_config = config_loader.get_hook_config('non_existent_hook', default={'enabled': False})
        if hook_config == {'enabled': False}:
            print("✅ Missing hook config: Returns default value")
        else:
            print(f"❌ Missing hook config: Should return default, got {hook_config}")
            return False
    except Exception as e:
        print(f"❌ Missing hook config: Unexpected exception - {type(e).__name__}: {e}")
        return False
    
    return True


def test_environment_variables():
    """Test environment variable substitution."""
    print("\n🌍 Testing Environment Variable Substitution")
    print("-" * 45)
    
    # Set test environment variables
    os.environ['TEST_YAML_VAR'] = 'test_value_123'
    os.environ['TEST_YAML_NUM'] = '42'
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config_subdir = temp_path / "config"
            config_subdir.mkdir()
            
            temp_loader = UnifiedConfigLoader(temp_path)
            
            # Create YAML with environment variables
            env_content = """
environment_test:
  simple_var: "${TEST_YAML_VAR}"
  numeric_var: "${TEST_YAML_NUM}"
  with_default: "${NONEXISTENT_VAR:default_value}"
  no_substitution: "regular_value"
  complex: "prefix_${TEST_YAML_VAR}_suffix"
"""
            env_file = config_subdir / "env_test.yaml"
            with open(env_file, 'w') as f:
                f.write(env_content)
            
            config = temp_loader.load_config('env_test')
            env_section = config.get('environment_test', {})
            
            # Test simple variable substitution
            if env_section.get('simple_var') == 'test_value_123':
                print("✅ Simple environment variable substitution")
            else:
                print(f"❌ Simple env var: Expected 'test_value_123', got '{env_section.get('simple_var')}'")
                return False
            
            # Test numeric variable substitution
            if env_section.get('numeric_var') == '42':
                print("✅ Numeric environment variable substitution")
            else:
                print(f"❌ Numeric env var: Expected '42', got '{env_section.get('numeric_var')}'")
                return False
            
            # Test default value substitution
            if env_section.get('with_default') == 'default_value':
                print("✅ Environment variable with default value")
            else:
                print(f"❌ Env var with default: Expected 'default_value', got '{env_section.get('with_default')}'")
                return False
            
            # Test no substitution for regular values
            if env_section.get('no_substitution') == 'regular_value':
                print("✅ Regular values remain unchanged")
            else:
                print(f"❌ Regular value: Expected 'regular_value', got '{env_section.get('no_substitution')}'")
                return False
            
            # Test complex substitution
            if env_section.get('complex') == 'prefix_test_value_123_suffix':
                print("✅ Complex environment variable substitution")
            else:
                print(f"❌ Complex env var: Expected 'prefix_test_value_123_suffix', got '{env_section.get('complex')}'")
                return False
            
    finally:
        # Clean up environment variables
        try:
            del os.environ['TEST_YAML_VAR']
            del os.environ['TEST_YAML_NUM']
        except KeyError:
            pass
    
    return True


def test_unicode_handling():
    """Test Unicode content handling."""
    print("\n🌐 Testing Unicode Content Handling")
    print("-" * 35)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config_subdir = temp_path / "config"
        config_subdir.mkdir()
        
        temp_loader = UnifiedConfigLoader(temp_path)
        
        # Create YAML with Unicode content
        unicode_content = """
unicode_test:
  chinese: "中文配置"
  emoji: "🚀✨💡"
  special_chars: "àáâãäåæç"
  mixed: "English中文🚀"
"""
        unicode_file = config_subdir / "unicode_test.yaml"
        with open(unicode_file, 'w', encoding='utf-8') as f:
            f.write(unicode_content)
        
        try:
            config = temp_loader.load_config('unicode_test')
            unicode_section = config.get('unicode_test', {})
            
            if unicode_section.get('chinese') == '中文配置':
                print("✅ Chinese characters handled correctly")
            else:
                print(f"❌ Chinese chars: Expected '中文配置', got '{unicode_section.get('chinese')}'")
                return False
            
            if unicode_section.get('emoji') == '🚀✨💡':
                print("✅ Emoji characters handled correctly")
            else:
                print(f"❌ Emoji: Expected '🚀✨💡', got '{unicode_section.get('emoji')}'")
                return False
            
            if unicode_section.get('special_chars') == 'àáâãäåæç':
                print("✅ Special characters handled correctly")
            else:
                print(f"❌ Special chars: Expected 'àáâãäåæç', got '{unicode_section.get('special_chars')}'")
                return False
            
        except Exception as e:
            print(f"❌ Unicode handling failed: {type(e).__name__}: {e}")
            return False
    
    return True


def test_deep_nesting():
    """Test deep nested configuration access."""
    print("\n🔗 Testing Deep Nested Configuration")
    print("-" * 37)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config_subdir = temp_path / "config"
        config_subdir.mkdir()
        
        temp_loader = UnifiedConfigLoader(temp_path)
        
        # Create deeply nested YAML
        deep_content = """
level1:
  level2:
    level3:
      level4:
        level5:
          deep_value: "found_it"
          deep_number: 42
          deep_list: [1, 2, 3]
"""
        deep_file = config_subdir / "deep_test.yaml"
        with open(deep_file, 'w') as f:
            f.write(deep_content)
        
        try:
            config = temp_loader.load_config('deep_test')
            
            # Test accessing deep nested values
            deep_value = temp_loader.get_section('deep_test', 'level1.level2.level3.level4.level5.deep_value')
            if deep_value == 'found_it':
                print("✅ Deep nested string value access")
            else:
                print(f"❌ Deep nested access: Expected 'found_it', got '{deep_value}'")
                return False
            
            # Test non-existent path with default
            missing_value = temp_loader.get_section('deep_test', 'level1.missing.path', 'default')
            if missing_value == 'default':
                print("✅ Missing deep path returns default")
            else:
                print(f"❌ Missing path: Expected 'default', got '{missing_value}'")
                return False
            
        except Exception as e:
            print(f"❌ Deep nesting test failed: {type(e).__name__}: {e}")
            return False
    
    return True


def main():
    """Run all error handling tests."""
    print("🧪 YAML Configuration Error Handling Tests")
    print("=" * 50)
    
    tests = [
        ("Malformed YAML", test_malformed_yaml),
        ("Missing Files", test_missing_files),
        ("Environment Variables", test_environment_variables),
        ("Unicode Handling", test_unicode_handling),
        ("Deep Nesting", test_deep_nesting)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"💥 {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 50)
    success_rate = (passed / total) * 100
    print(f"Results: {passed}/{total} tests passed ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("🎯 Error handling is working well!")
        return 0
    else:
        print("⚠️ Error handling needs improvement")
        return 1


if __name__ == "__main__":
    sys.exit(main())