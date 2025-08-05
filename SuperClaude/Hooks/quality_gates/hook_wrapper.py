#!/usr/bin/env python3
"""
Hook Wrapper for Quality Gates
Bridges new Claude Code stdin JSON format to existing command-line argument format
"""
import sys
import json
import subprocess
import os

def main():
    # Get event type from command line
    if len(sys.argv) < 2:
        print("Usage: hook_wrapper.py <event_type>", file=sys.stderr)
        sys.exit(1)
    
    event_type = sys.argv[1]
    
    try:
        # Read JSON from stdin
        input_data = json.load(sys.stdin)
        
        # Extract common fields
        session_id = input_data.get('session_id', 'default')
        tool_name = input_data.get('tool_name', '')
        
        # Get the actual hook script path
        hook_dir = os.path.dirname(os.path.abspath(__file__))
        hook_script = os.path.join(hook_dir, 'hook.py')
        
        # Build command based on event type
        if event_type == 'post':
            tool_input = input_data.get('tool_input', {})
            # Quality gates expects: post <tool_name> <tool_result> <tool_args> <session_id>
            cmd = ['python3', hook_script, 'post', tool_name, '{}', json.dumps(tool_input), session_id]
        
        else:
            print(f"Unknown event type: {event_type}", file=sys.stderr)
            sys.exit(1)
        
        # Execute the original hook
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Pass through the output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        sys.exit(result.returncode)
        
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()