#!/usr/bin/env python3
"""
SuperClaude Framework Coordinator Hook

Critical priority hook providing central intelligence for SuperClaude framework coordination.
Enforces ORCHESTRATOR.md auto-activation rules and RULES.md compliance patterns automatically.

Events: PreToolUse, PostToolUse
Responsibilities:
- Parse ORCHESTRATOR.md auto-activation rules
- Analyze context and suggest MCP server activation
- Enforce RULES.md compliance patterns
- Route based on complexity indicators

Usage:
    python hook.py pre ${tool.name} "${tool.args}" ${session.id}
    python hook.py post ${tool.name} "${tool.result}" "${tool.args}" ${session.id}
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add the common directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "common"))

from base_hook import BaseHook
from framework_parser import FrameworkParser
from utils import (
    parse_tool_args, 
    extract_file_paths_from_args,
    count_files_in_directory,
    detect_project_type,
    is_git_repository
)


class FrameworkCoordinatorHook(BaseHook):
    """
    Framework Coordinator Hook implementation.
    
    Provides central intelligence for SuperClaude framework coordination:
    - Auto-activation rule enforcement
    - MCP server routing suggestions
    - Framework compliance validation
    - Complexity-based routing decisions
    """
    
    def __init__(self, config_path: Optional[str] = None, input_data: Optional[Dict[str, Any]] = None):
        """Initialize Framework Coordinator Hook."""
        super().__init__("FrameworkCoordinator", config_path)
        
        # Initialize framework parser
        try:
            self.parser = FrameworkParser()
            self.logger.info("Framework parser initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize framework parser: {e}")
            self.parser = None
        
        # Cache for session context
        self.session_context = {}
        
        # MCP server complexity thresholds
        self.mcp_thresholds = {
            'context7': 0.3,
            'sequential': 0.7,
            'magic': 0.3,
            'serena': 0.6,
            'morphllm': 0.4,
            'playwright': 0.6
        }
    
    def _analyze_context(self, tool_name: str, tool_args: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        Analyze context for framework coordination decisions.
        
        Returns:
            Dictionary with context analysis including complexity score,
            file counts, project type, and other routing factors.
        """
        context = {
            'tool_name': tool_name,
            'session_id': session_id,
            'complexity_score': 0.0,
            'file_count': 0,
            'project_types': [],
            'has_symbol_operations': False,
            'is_ui_related': False,
            'is_analysis_task': False,
            'is_testing_task': False,
            'file_paths': [],
            'working_directory': None
        }
        
        # Extract file paths from arguments
        context['file_paths'] = extract_file_paths_from_args(tool_args)
        
        # Determine working directory
        if context['file_paths']:
            first_path = Path(context['file_paths'][0])
            if first_path.is_absolute():
                context['working_directory'] = str(first_path.parent)
            else:
                context['working_directory'] = str(Path.cwd())
        else:
            context['working_directory'] = str(Path.cwd())
        
        # Analyze project type and file count
        if context['working_directory']:
            working_path = Path(context['working_directory'])
            context['project_types'] = detect_project_type(working_path)
            context['file_count'] = count_files_in_directory(working_path, "**/*")
        
        # Calculate base complexity score
        complexity_factors = []
        
        # Tool-based complexity
        complex_tools = [
            'Grep', 'Glob', 'Task', 'MultiEdit', 'NotebookEdit', 
            'find_symbol', 'replace_symbol_body'
        ]
        if tool_name in complex_tools:
            complexity_factors.append(0.3)
        
        # File count complexity
        if context['file_count'] > 50:
            complexity_factors.append(0.4)
        elif context['file_count'] > 10:
            complexity_factors.append(0.2)
        
        # Multi-language project complexity
        if len(context['project_types']) > 2:
            complexity_factors.append(0.2)
        
        # Symbol operations detection
        symbol_keywords = ['symbol', 'refactor', 'rename', 'extract', 'move']
        if any(keyword in tool_name.lower() or 
               keyword in str(tool_args).lower() for keyword in symbol_keywords):
            context['has_symbol_operations'] = True
            complexity_factors.append(0.3)
        
        # UI-related detection
        ui_keywords = ['component', 'ui', 'frontend', 'react', 'vue', 'angular', 'css', 'html']
        if any(keyword in tool_name.lower() or 
               keyword in str(tool_args).lower() for keyword in ui_keywords):
            context['is_ui_related'] = True
            complexity_factors.append(0.2)
        
        # Analysis task detection
        analysis_keywords = ['analyze', 'debug', 'troubleshoot', 'investigate', 'examine']
        if any(keyword in tool_name.lower() or 
               keyword in str(tool_args).lower() for keyword in analysis_keywords):
            context['is_analysis_task'] = True
            complexity_factors.append(0.3)
        
        # Testing task detection
        testing_keywords = ['test', 'spec', 'pytest', 'jest', 'browser', 'e2e']
        if any(keyword in tool_name.lower() or 
               keyword in str(tool_args).lower() for keyword in testing_keywords):
            context['is_testing_task'] = True
            complexity_factors.append(0.2)
        
        # Calculate final complexity score
        if complexity_factors:
            context['complexity_score'] = min(sum(complexity_factors), 1.0)
        
        return context
    
    def _get_mcp_suggestions(self, context: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate MCP server activation suggestions based on context.
        
        Returns:
            List of MCP server suggestions with reasoning.
        """
        suggestions = []
        
        if not self.parser:
            return suggestions
        
        # Check each MCP server for activation
        server_checks = {
            'serena': {
                'condition': (
                    context['file_count'] > 10 or 
                    context['has_symbol_operations'] or 
                    len(context['project_types']) > 1
                ),
                'reason': f"Large project ({context['file_count']} files) or symbol operations detected"
            },
            'sequential': {
                'condition': (
                    context['complexity_score'] > 0.7 or 
                    context['is_analysis_task']
                ),
                'reason': f"Complex analysis needed (complexity: {context['complexity_score']:.2f})"
            },
            'magic': {
                'condition': context['is_ui_related'],
                'reason': "UI component operations detected"
            },
            'morphllm': {
                'condition': (
                    context['complexity_score'] < 0.6 and 
                    context['file_count'] < 20 and 
                    not context['has_symbol_operations']
                ),
                'reason': f"Simple edit suitable for token optimization"
            },
            'context7': {
                'condition': (
                    any(proj_type in ['python', 'node', 'rust', 'go'] 
                        for proj_type in context['project_types'])
                ),
                'reason': f"Framework project detected: {', '.join(context['project_types'])}"
            },
            'playwright': {
                'condition': context['is_testing_task'],
                'reason': "Testing operations detected"
            }
        }
        
        for server_name, check in server_checks.items():
            if check['condition']:
                suggestions.append({
                    'type': 'mcp_server_activation',
                    'server': server_name,
                    'reason': check['reason'],
                    'confidence': min(context['complexity_score'] + 0.3, 1.0)
                })
        
        return suggestions
    
    def _check_compliance_violations(self, tool_name: str, tool_args: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Check for RULES.md compliance violations.
        
        Returns:
            List of compliance violations found.
        """
        violations = []
        
        if not self.parser:
            return violations
        
        # Get compliance violations from parser
        parser_violations = self.parser.get_compliance_violations(tool_name, tool_args)
        
        for violation in parser_violations:
            violations.append({
                'type': 'compliance_violation',
                'rule': 'RULES.md',
                'message': violation,
                'severity': 'warning'
            })
        
        # Additional context-based checks
        
        # Check for Read before Write/Edit pattern
        if tool_name in ['Write', 'Edit', 'MultiEdit']:
            file_path = tool_args.get('file_path', '')
            if file_path:
                # This would require session state tracking to properly validate
                # For now, just suggest the best practice
                violations.append({
                    'type': 'best_practice_suggestion',
                    'rule': 'RULES.md - File Operation Security',
                    'message': f"Ensure Read tool was used before {tool_name} on {file_path}",
                    'severity': 'info'
                })
        
        # Check for absolute path usage
        file_paths = context.get('file_paths', [])
        for file_path in file_paths:
            if file_path and not (file_path.startswith('/') or file_path.startswith('C:')):
                violations.append({
                    'type': 'compliance_violation',
                    'rule': 'RULES.md - File Operation Security',
                    'message': f"Relative path detected, use absolute paths: {file_path}",
                    'severity': 'warning'
                })
        
        # Check for batch operations opportunity
        if tool_name in ['Read', 'Write', 'Edit'] and len(file_paths) > 1:
            violations.append({
                'type': 'optimization_suggestion',
                'rule': 'RULES.md - Task Management Rules',
                'message': f"Consider using batch operations for {len(file_paths)} files",
                'severity': 'info'
            })
        
        return violations
    
    def _get_resource_zone_recommendations(self, context: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Get resource zone recommendations based on current context.
        
        Returns:
            List of resource management recommendations.
        """
        recommendations = []
        
        # Simulate resource usage analysis (in real implementation, would check actual usage)
        estimated_resource_usage = context['complexity_score']
        
        if estimated_resource_usage > 0.85:
            recommendations.append({
                'type': 'resource_management',
                'zone': 'red',
                'message': 'High complexity operation - consider splitting into smaller tasks',
                'suggestions': [
                    'Use Task tool for delegation',
                    'Enable token efficiency mode',
                    'Consider sequential processing'
                ]
            })
        elif estimated_resource_usage > 0.75:
            recommendations.append({
                'type': 'resource_management',
                'zone': 'yellow',
                'message': 'Moderate complexity - activate efficiency mode',
                'suggestions': [
                    'Reduce verbosity',
                    'Defer non-critical operations',
                    'Enable caching'
                ]
            })
        
        return recommendations
    
    def process_pre_tool_use(self, tool_name: str, tool_args: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Process PreToolUse event for framework coordination."""
        if not self._validate_tool_context(tool_name, tool_args):
            return self._handle_error(ValueError("Invalid tool context"), "pre_tool_use")
        
        try:
            # Analyze context
            context = self._analyze_context(tool_name, tool_args, session_id)
            
            # Store context for session
            self.session_context[session_id] = context
            
            # Generate suggestions
            suggestions = []
            
            # MCP server suggestions
            mcp_suggestions = self._get_mcp_suggestions(context)
            suggestions.extend(mcp_suggestions)
            
            # Compliance checks
            compliance_violations = self._check_compliance_violations(tool_name, tool_args, context)
            suggestions.extend(compliance_violations)
            
            # Resource zone recommendations
            resource_recommendations = self._get_resource_zone_recommendations(context)  
            suggestions.extend(resource_recommendations)
            
            # Format response
            response = {
                'status': 'success',
                'hook': 'framework_coordinator',
                'event': 'pre_tool_use',
                'context': {
                    'complexity_score': context['complexity_score'],
                    'file_count': context['file_count'],
                    'project_types': context['project_types']
                },
                'suggestions': suggestions,
                'metadata': {
                    'session_id': session_id,
                    'tool_name': tool_name,
                    'analysis_time_ms': 0  # Will be set by performance tracking
                }
            }
            
            # Log suggestions if verbose
            if suggestions:
                self.logger.info(f"Generated {len(suggestions)} framework coordination suggestions")
                for suggestion in suggestions[:3]:  # Log first 3 suggestions
                    self.logger.debug(f"Suggestion: {suggestion.get('type')} - {suggestion.get('message', suggestion.get('reason', 'N/A'))}")
            
            return response
            
        except Exception as e:
            return self._handle_error(e, "pre_tool_use analysis")
    
    def process_post_tool_use(self, tool_name: str, tool_result: Any, tool_args: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Process PostToolUse event for framework coordination."""
        try:
            # Get stored context from pre-execution
            context = self.session_context.get(session_id, {})
            
            suggestions = []
            
            # Analyze tool result for patterns
            if tool_result and isinstance(tool_result, str):
                # Check for error patterns that might suggest MCP server activation
                if 'error' in tool_result.lower() or 'failed' in tool_result.lower():
                    suggestions.append({
                        'type': 'error_recovery',
                        'message': 'Tool execution had issues - consider alternative approach',
                        'suggestions': [
                            'Try different MCP server',
                            'Simplify operation',
                            'Check file permissions'
                        ]
                    })
                
                # Check for performance indicators
                if 'timeout' in tool_result.lower() or 'slow' in tool_result.lower():
                    suggestions.append({
                        'type': 'performance_optimization',
                        'message': 'Performance issues detected',
                        'suggestions': [
                            'Enable caching',
                            'Use batch operations',
                            'Consider Morphllm for optimization'
                        ]
                    })
            
            # Check if automatic checkpoint should be triggered
            if self.parser:
                should_checkpoint = self.parser.should_create_checkpoint({
                    'time_elapsed_minutes': 0,  # Would need session tracking
                    'task_priority': 'normal',
                    'task_completed': tool_name in ['Write', 'Edit', 'MultiEdit'],
                    'risk_level': 'low' if context.get('complexity_score', 0) < 0.7 else 'high'
                })
                
                if should_checkpoint:
                    suggestions.append({
                        'type': 'session_management',
                        'message': 'Consider creating checkpoint',
                        'command': '/sc:save --checkpoint',
                        'reason': 'Automatic checkpoint trigger conditions met'
                    })
            
            # Update session context
            if session_id in self.session_context:
                self.session_context[session_id]['last_tool'] = tool_name
                self.session_context[session_id]['last_result'] = str(tool_result)[:100] if tool_result else None
            
            response = {
                'status': 'success',
                'hook': 'framework_coordinator', 
                'event': 'post_tool_use',
                'suggestions': suggestions,
                'metadata': {
                    'session_id': session_id,
                    'tool_name': tool_name,
                    'context_updated': session_id in self.session_context
                }
            }
            
            return response
            
        except Exception as e:
            return self._handle_error(e, "post_tool_use analysis")


def main():
    """Main entry point for framework coordinator hook."""
    if len(sys.argv) < 2:
        print("Usage: python hook.py <event> <tool_name> <tool_args> [session_id]", file=sys.stderr)
        sys.exit(1)
    
    event = sys.argv[1]
    
    # Create hook instance
    try:
        hook = FrameworkCoordinatorHook(input_data={})
    except Exception as e:
        print(f"Error initializing hook: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Execute hook based on event
    try:
        if event == "pre":
            # For pre event, arguments should be: pre <tool_name> <tool_args> <session_id>
            if len(sys.argv) < 4:
                print("Usage for pre: python hook.py pre <tool_name> <tool_args> [session_id]", file=sys.stderr)
                sys.exit(1)
            
            tool_name = sys.argv[2]
            tool_args_str = sys.argv[3] if len(sys.argv) > 3 else "{}"
            session_id = sys.argv[4] if len(sys.argv) > 4 else "default"
            
            # Parse tool arguments
            tool_args = parse_tool_args(tool_args_str)
            
            result = hook.execute("PreToolUse", tool_name=tool_name, tool_args=tool_args, session_id=session_id)
            
        elif event == "post":
            # For post event, arguments should be: post <tool_name> <tool_result> <tool_args> <session_id>
            if len(sys.argv) < 6:
                print("Usage for post: python hook.py post <tool_name> <tool_result> <tool_args> <session_id>", file=sys.stderr)
                sys.exit(1)
                
            tool_name = sys.argv[2]
            tool_result = sys.argv[3] if sys.argv[3] != "null" and sys.argv[3] != "''" else None
            tool_args_str = sys.argv[4]
            session_id = sys.argv[5] if len(sys.argv) > 5 else "default"
            
            # Parse tool arguments
            tool_args = parse_tool_args(tool_args_str)
            
            result = hook.execute("PostToolUse", tool_name=tool_name, tool_result=tool_result, tool_args=tool_args, session_id=session_id)
            
        else:
            print(f"Unknown event: {event}", file=sys.stderr)
            sys.exit(1)
        
        # Output result as JSON for Claude Code
        print(json.dumps(result, indent=2))
        
        # Exit with appropriate code
        sys.exit(0 if result.get('status') == 'success' else 1)
        
    except Exception as e:
        error_result = {
            'status': 'error',
            'hook': 'framework_coordinator',
            'error': str(e),
            'message': 'Framework coordinator hook execution failed'
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()