#!/usr/bin/env python3
"""
Claude Code Hook Wrapper

Universal wrapper that adapts Claude Code's stdin JSON format to the
SuperClaude hook system's expected inputs.

Claude Code sends JSON via stdin with format:
{
  "tool": {
    "name": "ToolName",
    "args": {...}
  },
  "session_id": "session-id",
  "event": "PreToolUse|PostToolUse|SessionStart"
}
"""

import sys
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


def read_claude_input() -> Dict[str, Any]:
    """
    Read JSON input from stdin as provided by Claude Code.
    
    Returns:
        Parsed JSON data from stdin
    """
    try:
        # Read all stdin
        input_data = sys.stdin.read()
        
        # Parse JSON
        if input_data:
            return json.loads(input_data)
        else:
            return {}
    except json.JSONDecodeError as e:
        return {
            "error": f"Invalid JSON input: {e}",
            "raw_input": input_data[:100] if 'input_data' in locals() else "No input"
        }
    except Exception as e:
        return {"error": f"Failed to read input: {e}"}


def extract_hook_params(claude_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract hook parameters from Claude Code's JSON format.
    
    Args:
        claude_data: JSON data from Claude Code
        
    Returns:
        Dictionary with extracted parameters for hooks
    """
    params = {
        "event": claude_data.get("event", "unknown"),
        "session_id": claude_data.get("session_id", "default"),
        "tool_name": None,
        "tool_args": {},
        "tool_result": None
    }
    
    # Extract tool information
    if "tool" in claude_data:
        tool_info = claude_data["tool"]
        params["tool_name"] = tool_info.get("name", "unknown")
        params["tool_args"] = tool_info.get("args", {})
        params["tool_result"] = tool_info.get("result")
    
    return params


def format_hook_response(hook_result: Any) -> str:
    """
    Format hook response for Claude Code.
    
    Args:
        hook_result: Result from hook execution
        
    Returns:
        JSON string formatted for Claude Code
    """
    # If hook_result is already a dict, use it
    if isinstance(hook_result, dict):
        return json.dumps(hook_result, indent=2)
    
    # If it's a string, try to parse it as JSON
    if isinstance(hook_result, str):
        try:
            parsed = json.loads(hook_result)
            return json.dumps(parsed, indent=2)
        except:
            # If not JSON, wrap in a response
            return json.dumps({
                "status": "success",
                "message": str(hook_result)
            }, indent=2)
    
    # For any other type, convert to string and wrap
    return json.dumps({
        "status": "success",
        "result": str(hook_result)
    }, indent=2)


def create_hook_wrapper(hook_name: str, hook_module: str):
    """
    Factory function to create hook wrappers.
    
    Args:
        hook_name: Name of the hook (e.g., "token_efficiency")
        hook_module: Module name containing the hook class
        
    Returns:
        Wrapper function for the specific hook
    """
    def wrapper():
        try:
            # Read Claude Code input
            claude_data = read_claude_input()
            
            if "error" in claude_data:
                print(json.dumps({
                    "status": "error",
                    "hook": hook_name,
                    "message": claude_data["error"]
                }))
                return 1
            
            # Extract parameters
            params = extract_hook_params(claude_data)
            
            # Import the hook module dynamically
            hook_path = Path(__file__).parent.parent / hook_name
            sys.path.insert(0, str(hook_path))
            
            hook_module_obj = __import__(hook_module)
            
            # Get the hook class (assumes it follows naming convention)
            hook_class_name = ''.join(word.capitalize() for word in hook_name.split('_')) + 'Hook'
            hook_class = getattr(hook_module_obj, hook_class_name)
            
            # Create hook instance
            hook = hook_class(input_data=claude_data)
            
            # Execute appropriate method based on event
            if params["event"] == "PreToolUse":
                result = hook.process_pre_tool_use(
                    params["tool_name"],
                    params["tool_args"],
                    params["session_id"]
                )
            elif params["event"] == "PostToolUse":
                result = hook.process_post_tool_use(
                    params["tool_name"],
                    params["tool_result"],
                    params["tool_args"],
                    params["session_id"]
                )
            elif params["event"] == "SessionStart":
                if hasattr(hook, 'process_session_start'):
                    result = hook.process_session_start(params["session_id"])
                else:
                    result = {
                        "status": "ignored",
                        "message": f"{hook_name} does not handle SessionStart events"
                    }
            else:
                result = {
                    "status": "error",
                    "message": f"Unknown event type: {params['event']}"
                }
            
            # Format and output response
            print(format_hook_response(result))
            return 0
            
        except Exception as e:
            print(json.dumps({
                "status": "error",
                "hook": hook_name,
                "message": f"Hook execution failed: {str(e)}",
                "type": type(e).__name__
            }, indent=2))
            return 1
    
    return wrapper


# Export wrapper creator for use by individual hooks
__all__ = ['create_hook_wrapper', 'read_claude_input', 'extract_hook_params', 'format_hook_response']