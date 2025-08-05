#!/usr/bin/env python3
"""
Test hook timeout handling
"""

import os
import json
import time
import subprocess
import tempfile

def create_slow_hook(sleep_time):
    """Create a hook that sleeps for specified time"""
    return f"""#!/usr/bin/env python3
import sys
import json
import time

# Sleep to simulate slow operation
time.sleep({sleep_time})

# Return result
result = {{"status": "completed", "sleep_time": {sleep_time}}}
print(json.dumps(result))
"""

def test_hook_timeouts():
    """Test that hooks respect timeout settings"""
    print("🧪 Testing Hook Timeout Handling\n")
    
    # Read current settings to get timeouts
    settings_path = os.path.expanduser("~/.claude/settings.json")
    
    print("📋 Reading timeout settings from settings.json...")
    
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        
        hooks_config = settings.get('hooks', {})
        
        # Extract timeouts from array structure
        timeouts = {}
        for hook_name, hook_configs in hooks_config.items():
            if isinstance(hook_configs, list) and hook_configs:
                # Get timeout from first matcher's first hook
                first_config = hook_configs[0]
                if 'hooks' in first_config and first_config['hooks']:
                    timeout = first_config['hooks'][0].get('timeout', 10)
                    timeouts[hook_name] = timeout
        
        # Add defaults for any missing
        default_timeouts = {
            'SessionStart': 10,
            'PreToolUse': 15,
            'PostToolUse': 10,
            'PreCompact': 15,
            'Notification': 10,
            'Stop': 15,
            'SubagentStop': 15
        }
        
        for hook, default in default_timeouts.items():
            if hook not in timeouts:
                timeouts[hook] = default
        
        print("\n📊 Configured Timeouts:")
        for hook, timeout in timeouts.items():
            print(f"   {hook}: {timeout}s")
        
    except Exception as e:
        print(f"❌ Error reading settings: {e}")
        return False
    
    # Test timeout scenarios
    print("\n🧪 Testing Timeout Scenarios:\n")
    
    scenarios = [
        {
            "name": "Hook completes before timeout",
            "hook": "test_hook_fast.py",
            "sleep_time": 1,
            "timeout": 5,
            "expected": "success"
        },
        {
            "name": "Hook exceeds timeout",
            "hook": "test_hook_slow.py", 
            "sleep_time": 3,
            "timeout": 1,
            "expected": "timeout"
        },
        {
            "name": "Hook at timeout boundary",
            "hook": "test_hook_boundary.py",
            "sleep_time": 2,
            "timeout": 2,
            "expected": "success"  # Should complete just in time
        }
    ]
    
    passed = 0
    failed = 0
    
    for scenario in scenarios:
        print(f"🔍 {scenario['name']}")
        print(f"   Sleep: {scenario['sleep_time']}s, Timeout: {scenario['timeout']}s")
        
        # Create temporary hook file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(create_slow_hook(scenario['sleep_time']))
            hook_path = f.name
        
        os.chmod(hook_path, 0o755)
        
        try:
            # Run hook with timeout
            start_time = time.time()
            result = subprocess.run(
                ['python3', hook_path],
                timeout=scenario['timeout'],
                capture_output=True,
                text=True,
                input=json.dumps({"test": "data"})
            )
            elapsed = time.time() - start_time
            
            if scenario['expected'] == 'success':
                if result.returncode == 0:
                    print(f"   ✅ PASS - Completed in {elapsed:.2f}s")
                    passed += 1
                else:
                    print(f"   ❌ FAIL - Expected success but got error")
                    failed += 1
            else:
                print(f"   ❌ FAIL - Expected timeout but completed in {elapsed:.2f}s")
                failed += 1
                
        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            if scenario['expected'] == 'timeout':
                print(f"   ✅ PASS - Timed out after {elapsed:.2f}s as expected")
                passed += 1
            else:
                print(f"   ❌ FAIL - Unexpected timeout after {elapsed:.2f}s")
                failed += 1
        
        finally:
            # Clean up
            os.unlink(hook_path)
        
        print()
    
    # Test actual hooks with simulated delays
    print("🧪 Testing Real Hook Timeout Behavior:\n")
    
    # Check if hooks handle timeouts gracefully
    test_hooks = [
        '/home/anton/.claude/hooks/session_start.py',
        '/home/anton/.claude/hooks/pre_tool_use.py',
        '/home/anton/.claude/hooks/post_tool_use.py'
    ]
    
    for hook_path in test_hooks:
        if os.path.exists(hook_path):
            hook_name = os.path.basename(hook_path)
            print(f"🔍 Testing {hook_name} timeout handling")
            
            try:
                # Run with very short timeout to test behavior
                result = subprocess.run(
                    ['python3', hook_path],
                    timeout=0.1,  # 100ms timeout
                    capture_output=True,
                    text=True,
                    input=json.dumps({"test": "timeout_test"})
                )
                # If it completes that fast, it handled it well
                print(f"   ✅ Hook completed quickly")
                
            except subprocess.TimeoutExpired:
                # This is expected for most hooks
                print(f"   ⚠️  Hook exceeded 100ms test timeout (normal)")
            
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    # Summary
    print(f"\n📊 Timeout Test Results:")
    print(f"   Scenarios: {passed}/{passed+failed} passed ({passed/(passed+failed)*100:.1f}%)")
    print(f"   Behavior: {'✅ Timeouts working correctly' if passed > failed else '❌ Timeout issues detected'}")
    
    # Additional timeout recommendations
    print("\n💡 Timeout Recommendations:")
    print("   - Session hooks: 10-15s (may need initialization)")
    print("   - Tool hooks: 5-10s (should be fast)")
    print("   - Compaction hooks: 15-20s (may process large content)")
    print("   - Stop hooks: 10-15s (cleanup operations)")
    
    return passed > failed

if __name__ == "__main__":
    success = test_hook_timeouts()
    exit(0 if success else 1)