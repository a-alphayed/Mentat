#!/usr/bin/env python3
"""
SuperClaude Quality Gates Hook

High priority hook for systematic enforcement of 8-step validation cycle.
Provides automatic quality validation after Write/Edit operations.

Events: PostToolUse (after Write/Edit operations)
Responsibilities:
- Trigger 8-step validation cycle automatically
- Monitor quality metrics and thresholds
- Provide evidence collection and documentation
- Integration with SuperClaude quality standards

Usage:
    python hook.py post ${tool.name} "${tool.result}" "${tool.args}" ${session.id}
"""

import sys
import os
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Add the common directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "common"))

from base_hook import BaseHook
from framework_parser import FrameworkParser
from utils import (
    parse_tool_args,
    extract_file_paths_from_args,
    detect_project_type
)


class QualityGatesHook(BaseHook):
    """
    Quality Gates Hook implementation.
    
    Provides systematic enforcement of 8-step validation cycle:
    1. Syntax validation
    2. Type analysis
    3. Lint rules
    4. Security assessment
    5. Testing
    6. Performance analysis
    7. Documentation
    8. Integration testing
    """
    
    def __init__(self, config_path: Optional[str] = None, input_data: Optional[Dict[str, Any]] = None):
        """Initialize Quality Gates Hook."""
        super().__init__("QualityGates", config_path)
        
        # Initialize framework parser
        try:
            self.parser = FrameworkParser()
            self.logger.info("Framework parser initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize framework parser: {e}")
            self.parser = None
        
        # Quality thresholds
        self.quality_thresholds = {
            'minimum_score': 0.8,
            'warning_threshold': 0.7,
            'auto_fix_threshold': 0.9
        }
        
        # 8-step validation configuration
        self.validation_steps = {
            'syntax_validation': {
                'enabled': True,
                'weight': 0.15,
                'description': 'Syntax and structural validation'
            },
            'type_analysis': {
                'enabled': True,
                'weight': 0.15,
                'description': 'Type compatibility and inference'
            },
            'lint_rules': {
                'enabled': True,
                'weight': 0.15,
                'description': 'Code style and linting rules'
            },
            'security_assessment': {
                'enabled': True,
                'weight': 0.15,
                'description': 'Security vulnerability assessment'
            },
            'testing': {
                'enabled': True,
                'weight': 0.15,
                'description': 'Test coverage and validation'
            },
            'performance_analysis': {
                'enabled': True,
                'weight': 0.10,
                'description': 'Performance impact analysis'
            },
            'documentation': {
                'enabled': True,
                'weight': 0.10,
                'description': 'Documentation completeness'
            },
            'integration_testing': {
                'enabled': True,
                'weight': 0.05,
                'description': 'Integration and compatibility testing'
            }
        }
    
    def _determine_file_language(self, file_path: str) -> str:
        """Determine programming language of file."""
        path = Path(file_path)
        extension = path.suffix.lower()
        
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.rs': 'rust',
            '.go': 'go',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.less': 'less',
            '.json': 'json',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.sql': 'sql'
        }
        
        return language_map.get(extension, 'unknown')
    
    def _validate_syntax(self, file_path: str, content: str, language: str) -> Dict[str, Any]:
        """Perform syntax validation for the file."""
        validation_result = {
            'step': 'syntax_validation',
            'passed': True,
            'score': 1.0,
            'issues': [],
            'suggestions': []
        }
        
        try:
            if language == 'python':
                # Basic Python syntax validation
                try:
                    compile(content, file_path, 'exec')
                    validation_result['suggestions'].append("Python syntax is valid")
                except SyntaxError as e:
                    validation_result['passed'] = False
                    validation_result['score'] = 0.0
                    validation_result['issues'].append(f"Python syntax error: {e}")
                    validation_result['suggestions'].append("Fix Python syntax errors before proceeding")
            
            elif language in ['javascript', 'typescript']:
                # Basic JS/TS validation - check for common syntax issues
                common_issues = [
                    (r'console\.log\(', "Consider removing console.log statements"),
                    (r'debugger;', "Remove debugger statements"),
                    (r'var\s+\w+', "Consider using 'let' or 'const' instead of 'var'"),
                    (r'==\s*(?!==)', "Consider using '===' for strict equality")
                ]
                
                for pattern, suggestion in common_issues:
                    if re.search(pattern, content):
                        validation_result['suggestions'].append(suggestion)
                        validation_result['score'] -= 0.1
            
            elif language == 'json':
                # JSON validation
                try:
                    json.loads(content)
                    validation_result['suggestions'].append("JSON syntax is valid")
                except json.JSONDecodeError as e:
                    validation_result['passed'] = False
                    validation_result['score'] = 0.0
                    validation_result['issues'].append(f"JSON syntax error: {e}")
                    validation_result['suggestions'].append("Fix JSON syntax errors")
            
            # General syntax checks
            if not content.strip():
                validation_result['issues'].append("File is empty")
                validation_result['score'] = 0.5
            
            # Check for very long lines
            long_lines = [i+1 for i, line in enumerate(content.split('\n')) if len(line) > 120]
            if long_lines:
                validation_result['suggestions'].append(f"Consider breaking long lines: {long_lines[:5]}")
                validation_result['score'] -= 0.05
            
            # Ensure score doesn't go below 0
            validation_result['score'] = max(0.0, validation_result['score'])
            
        except Exception as e:
            validation_result['passed'] = False
            validation_result['score'] = 0.0
            validation_result['issues'].append(f"Syntax validation failed: {e}")
        
        return validation_result
    
    def _validate_type_analysis(self, file_path: str, content: str, language: str) -> Dict[str, Any]:
        """Perform type analysis validation."""
        validation_result = {
            'step': 'type_analysis',
            'passed': True,
            'score': 1.0,
            'issues': [],
            'suggestions': []
        }
        
        try:
            if language == 'python':
                # Check for type hints
                has_type_hints = bool(re.search(r':\s*\w+|-> \w+', content))
                if not has_type_hints and len(content.split('\n')) > 20:
                    validation_result['suggestions'].append("Consider adding type hints for better code clarity")
                    validation_result['score'] -= 0.2
                
                # Check for common type issues
                if 'Any' in content and 'typing' in content:
                    validation_result['suggestions'].append("Consider using more specific types instead of Any")
                    validation_result['score'] -= 0.1
            
            elif language == 'typescript':
                # Check for 'any' usage
                any_usage = len(re.findall(r'\bany\b', content))
                if any_usage > 0:
                    validation_result['suggestions'].append(f"Found {any_usage} uses of 'any' - consider more specific types")
                    validation_result['score'] -= min(0.3, any_usage * 0.05)
                
                # Check for type assertions
                type_assertions = len(re.findall(r'as\s+\w+|<\w+>', content))
                if type_assertions > 3:
                    validation_result['suggestions'].append("High number of type assertions - review type safety")
                    validation_result['score'] -= 0.1
            
            elif language == 'javascript':
                # Suggest TypeScript for larger files
                if len(content.split('\n')) > 50:
                    validation_result['suggestions'].append("Consider migrating to TypeScript for better type safety")
                    validation_result['score'] -= 0.1
            
        except Exception as e:
            validation_result['issues'].append(f"Type analysis failed: {e}")
            validation_result['score'] = 0.8
        
        return validation_result
    
    def _validate_lint_rules(self, file_path: str, content: str, language: str) -> Dict[str, Any]:
        """Validate against linting rules."""
        validation_result = {
            'step': 'lint_rules',
            'passed': True,
            'score': 1.0,
            'issues': [],
            'suggestions': []
        }
        
        try:
            # General linting checks
            lines = content.split('\n')
            
            # Check indentation consistency
            indentation_types = set()
            for line in lines:
                if line.startswith(' '):
                    indentation_types.add('spaces')
                elif line.startswith('\t'):
                    indentation_types.add('tabs')
            
            if len(indentation_types) > 1:
                validation_result['issues'].append("Inconsistent indentation (mixed tabs and spaces)")
                validation_result['score'] -= 0.2
            
            # Check for trailing whitespace
            trailing_whitespace_lines = [i+1 for i, line in enumerate(lines) if line.endswith(' ') or line.endswith('\t')]
            if trailing_whitespace_lines:
                validation_result['suggestions'].append(f"Remove trailing whitespace on lines: {trailing_whitespace_lines[:5]}")
                validation_result['score'] -= 0.05
            
            # Language-specific linting
            if language == 'python':
                # PEP 8 checks
                if any(len(line) > 79 for line in lines):
                    validation_result['suggestions'].append("Some lines exceed PEP 8 line length (79 chars)")
                    validation_result['score'] -= 0.1
                
                # Check for unused imports (basic)
                import_pattern = r'^import\s+(\w+)|^from\s+\w+\s+import\s+(\w+)'
                imports = re.findall(import_pattern, content, re.MULTILINE)
                flat_imports = [imp for sublist in imports for imp in sublist if imp]
                
                for imp in flat_imports:
                    if imp not in content.replace(f"import {imp}", ""):
                        validation_result['suggestions'].append(f"Potentially unused import: {imp}")
                        validation_result['score'] -= 0.05
            
            elif language in ['javascript', 'typescript']:
                # Check for missing semicolons (if project uses them)
                semicolon_lines = [line for line in lines if line.strip().endswith(';')]
                non_semicolon_lines = [line for line in lines if line.strip() and not line.strip().endswith(';') and not line.strip().endswith('{') and not line.strip().endswith('}')]
                
                if len(semicolon_lines) > len(non_semicolon_lines) * 2:
                    # Project likely uses semicolons
                    validation_result['suggestions'].append("Consider consistent semicolon usage")
                    validation_result['score'] -= 0.05
            
        except Exception as e:
            validation_result['issues'].append(f"Lint validation failed: {e}")
            validation_result['score'] = 0.8
        
        return validation_result
    
    def _validate_security(self, file_path: str, content: str, language: str) -> Dict[str, Any]:
        """Perform security assessment."""
        validation_result = {
            'step': 'security_assessment',
            'passed': True,
            'score': 1.0,
            'issues': [],
            'suggestions': []
        }
        
        try:
            # General security checks
            security_patterns = [
                (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password detected", 0.5),
                (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key detected", 0.5),
                (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret detected", 0.5),
                (r'token\s*=\s*["\'][^"\']+["\']', "Hardcoded token detected", 0.3),
                (r'eval\s*\(', "Use of eval() function - security risk", 0.3),
                (r'exec\s*\(', "Use of exec() function - security risk", 0.3),
                (r'os\.system\s*\(', "Use of os.system() - security risk", 0.4),
                (r'subprocess\.call\s*\([^)]*shell\s*=\s*True', "subprocess with shell=True - security risk", 0.3),
                (r'innerHTML\s*=', "Direct innerHTML assignment - XSS risk", 0.2),
                (r'document\.write\s*\(', "Use of document.write - security risk", 0.2)
            ]
            
            for pattern, message, severity in security_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    if severity > 0.3:
                        validation_result['issues'].append(message)
                        validation_result['passed'] = False
                    else:
                        validation_result['suggestions'].append(message)
                    validation_result['score'] -= severity
            
            # Language-specific security checks
            if language == 'python':
                # Check for SQL injection risks
                sql_patterns = [
                    r'execute\s*\(\s*["\'][^"\']*%[^"\']*["\']',
                    r'cursor\.execute\s*\(\s*["\'][^"\']*\+[^"\']*["\']'
                ]
                for pattern in sql_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        validation_result['issues'].append("Potential SQL injection vulnerability")
                        validation_result['score'] -= 0.4
                        validation_result['passed'] = False
            
            elif language in ['javascript', 'typescript']:
                # Check for XSS risks
                if re.search(r'\.innerHTML\s*=\s*.*\+', content):
                    validation_result['issues'].append("Potential XSS vulnerability with innerHTML")
                    validation_result['score'] -= 0.3
            
            # Ensure score doesn't go below 0
            validation_result['score'] = max(0.0, validation_result['score'])
            
        except Exception as e:
            validation_result['issues'].append(f"Security validation failed: {e}")
            validation_result['score'] = 0.7
        
        return validation_result
    
    def _validate_testing(self, file_path: str, content: str, language: str, project_dir: str) -> Dict[str, Any]:
        """Validate testing aspects."""
        validation_result = {
            'step': 'testing',
            'passed': True,
            'score': 1.0,
            'issues': [],
            'suggestions': []
        }
        
        try:
            project_path = Path(project_dir)
            
            # Check for test files in project
            test_patterns = ['*test*', '*spec*', 'tests/*', '__tests__/*']
            test_files = []
            for pattern in test_patterns:
                test_files.extend(project_path.glob(pattern))
            
            if not test_files:
                validation_result['suggestions'].append("No test files found in project - consider adding tests")
                validation_result['score'] -= 0.3
            
            # Check if current file is a test file
            file_name = Path(file_path).name.lower()
            is_test_file = any(keyword in file_name for keyword in ['test', 'spec'])
            
            if is_test_file:
                # Validate test file structure
                test_keywords = ['test', 'it', 'describe', 'assert', 'expect', 'should']
                found_keywords = [kw for kw in test_keywords if kw in content.lower()]
                
                if not found_keywords:
                    validation_result['suggestions'].append("Test file lacks common testing keywords")
                    validation_result['score'] -= 0.2
                else:
                    validation_result['suggestions'].append(f"Test file contains: {', '.join(found_keywords)}")
            else:
                # For non-test files, check if they have corresponding tests
                base_name = Path(file_path).stem
                potential_test_files = [
                    f"{base_name}.test.{Path(file_path).suffix[1:]}",
                    f"{base_name}_test.{Path(file_path).suffix[1:]}",
                    f"test_{base_name}.{Path(file_path).suffix[1:]}"
                ]
                
                has_corresponding_test = any(
                    (project_path / test_file).exists() or
                    (project_path / "tests" / test_file).exists() or
                    (project_path / "__tests__" / test_file).exists()
                    for test_file in potential_test_files
                )
                
                if not has_corresponding_test:
                    validation_result['suggestions'].append(f"Consider creating tests for {base_name}")
                    validation_result['score'] -= 0.2
            
        except Exception as e:
            validation_result['suggestions'].append(f"Testing validation had issues: {e}")
            validation_result['score'] = 0.8
        
        return validation_result
    
    def _validate_performance(self, file_path: str, content: str, language: str) -> Dict[str, Any]:
        """Validate performance aspects."""
        validation_result = {
            'step': 'performance_analysis',
            'passed': True,
            'score': 1.0,
            'issues': [],
            'suggestions': []
        }
        
        try:
            # General performance checks
            lines = content.split('\n')
            line_count = len(lines)
            
            # Check file size
            if line_count > 500:
                validation_result['suggestions'].append(f"Large file ({line_count} lines) - consider splitting")
                validation_result['score'] -= 0.1
            
            # Language-specific performance checks
            if language == 'python':
                # Check for performance anti-patterns
                perf_issues = [
                    (r'\.append\s*\([^)]*\)\s*for\s+', "List comprehension may be faster than append in loop", 0.1),
                    (r'range\s*\(\s*len\s*\(', "Consider enumerate() instead of range(len())", 0.05),
                    (r'\.keys\s*\(\s*\).*in\s+', "Direct dict iteration is faster than .keys()", 0.05)
                ]
                
                for pattern, suggestion, impact in perf_issues:
                    if re.search(pattern, content):
                        validation_result['suggestions'].append(suggestion)
                        validation_result['score'] -= impact
            
            elif language in ['javascript', 'typescript']:
                # JS/TS performance checks
                perf_issues = [
                    (r'document\.getElementById.*for\s*\(', "Cache DOM queries outside loops", 0.1),
                    (r'innerHTML\s*\+=', "Consider using DocumentFragment for multiple DOM updates", 0.1),
                    (r'\.forEach\s*\(.*=>.*\.push\s*\(', "Consider using map() instead of forEach with push", 0.05)
                ]
                
                for pattern, suggestion, impact in perf_issues:
                    if re.search(pattern, content):
                        validation_result['suggestions'].append(suggestion)
                        validation_result['score'] -= impact
            
        except Exception as e:
            validation_result['suggestions'].append(f"Performance validation had issues: {e}")
            validation_result['score'] = 0.9
        
        return validation_result
    
    def _validate_documentation(self, file_path: str, content: str, language: str) -> Dict[str, Any]:
        """Validate documentation aspects."""
        validation_result = {
            'step': 'documentation',
            'passed': True,
            'score': 1.0,
            'issues': [],
            'suggestions': []
        }
        
        try:
            lines = content.split('\n')
            comment_lines = 0
            docstring_lines = 0
            
            # Count comments and docstrings
            if language == 'python':
                comment_lines = len([line for line in lines if line.strip().startswith('#')])
                docstring_matches = re.findall(r'""".*?"""', content, re.DOTALL)
                docstring_lines = sum(doc.count('\n') + 1 for doc in docstring_matches)
            
            elif language in ['javascript', 'typescript']:
                comment_lines = len([line for line in lines if line.strip().startswith('//')])
                block_comments = re.findall(r'/\*.*?\*/', content, re.DOTALL)
                comment_lines += sum(comment.count('\n') + 1 for comment in block_comments)
            
            elif language in ['java', 'cpp', 'c', 'csharp']:
                comment_lines = len([line for line in lines if line.strip().startswith('//')])
                block_comments = re.findall(r'/\*.*?\*/', content, re.DOTALL)
                comment_lines += sum(comment.count('\n') + 1 for comment in block_comments)
            
            # Calculate documentation ratio
            total_lines = len([line for line in lines if line.strip()])
            doc_ratio = (comment_lines + docstring_lines) / max(total_lines, 1)
            
            if doc_ratio < 0.1:
                validation_result['suggestions'].append(f"Low documentation ratio ({doc_ratio:.1%}) - consider adding more comments")
                validation_result['score'] -= 0.2
            elif doc_ratio < 0.05:
                validation_result['issues'].append("Very low documentation - add comments for maintainability")
                validation_result['score'] -= 0.3
            
            # Check for TODO/FIXME comments
            todo_pattern = r'(?i)(TODO|FIXME|HACK|XXX):'
            todos = re.findall(todo_pattern, content)
            if todos:
                validation_result['suggestions'].append(f"Found {len(todos)} TODO/FIXME comments to address")
                validation_result['score'] -= min(0.1, len(todos) * 0.02)
            
            # Check for function/class documentation
            if language == 'python':
                functions = re.findall(r'def\s+\w+\s*\(', content)
                classes = re.findall(r'class\s+\w+', content)
                
                if (functions or classes) and docstring_lines == 0:
                    validation_result['suggestions'].append("Add docstrings to functions and classes")
                    validation_result['score'] -= 0.2
            
        except Exception as e:
            validation_result['suggestions'].append(f"Documentation validation had issues: {e}")
            validation_result['score'] = 0.9
        
        return validation_result
    
    def _validate_integration(self, file_path: str, content: str, language: str, project_dir: str) -> Dict[str, Any]:
        """Validate integration aspects."""
        validation_result = {
            'step': 'integration_testing',
            'passed': True,
            'score': 1.0,
            'issues': [],
            'suggestions': []
        }
        
        try:
            # Check imports/dependencies
            if language == 'python':
                imports = re.findall(r'^(?:from\s+\S+\s+)?import\s+(\S+)', content, re.MULTILINE)
                external_imports = [imp for imp in imports if not imp.startswith('.') and imp not in ['os', 'sys', 'json', 'time', 'datetime']]
                
                if external_imports:
                    validation_result['suggestions'].append(f"External dependencies: {', '.join(external_imports[:5])}")
            
            elif language in ['javascript', 'typescript']:
                imports = re.findall(r'(?:import.*from\s+["\']([^"\']+)["\']|require\s*\(\s*["\']([^"\']+)["\'])', content)
                flat_imports = [imp for sublist in imports for imp in sublist if imp and not imp.startswith('.')]
                
                if flat_imports:
                    validation_result['suggestions'].append(f"External dependencies: {', '.join(flat_imports[:5])}")
            
            # Check for configuration files
            project_path = Path(project_dir)
            config_files = ['package.json', 'pyproject.toml', 'requirements.txt', 'Cargo.toml', 'go.mod']
            found_config = [cf for cf in config_files if (project_path / cf).exists()]
            
            if not found_config:
                validation_result['suggestions'].append("No package configuration files found - consider adding dependency management")
                validation_result['score'] -= 0.1
            
        except Exception as e:
            validation_result['suggestions'].append(f"Integration validation had issues: {e}")
            validation_result['score'] = 0.9
        
        return validation_result
    
    def _run_quality_validation(self, file_path: str, content: str, project_dir: str) -> Dict[str, Any]:
        """Run complete 8-step quality validation."""
        language = self._determine_file_language(file_path)
        results = []
        
        # Run all 8 validation steps
        validation_functions = [
            self._validate_syntax,
            self._validate_type_analysis,
            self._validate_lint_rules,
            self._validate_security,
            lambda fp, c, l: self._validate_testing(fp, c, l, project_dir),
            self._validate_performance,
            self._validate_documentation,
            lambda fp, c, l: self._validate_integration(fp, c, l, project_dir)
        ]
        
        for validate_func in validation_functions:
            try:
                if validate_func.__name__.endswith('testing') or validate_func.__name__.endswith('integration'):
                    result = validate_func(file_path, content, language)
                else:
                    result = validate_func(file_path, content, language)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Validation step failed: {e}")
                results.append({
                    'step': 'unknown',
                    'passed': False,
                    'score': 0.0,
                    'issues': [f"Validation failed: {e}"],
                    'suggestions': []
                })
        
        # Calculate overall quality score
        total_weight = sum(step['weight'] for step in self.validation_steps.values())
        weighted_score = 0.0
        
        for i, (step_name, step_config) in enumerate(self.validation_steps.items()):
            if i < len(results):
                weighted_score += results[i]['score'] * step_config['weight']
        
        overall_score = weighted_score / max(total_weight, 1.0)
        
        # Determine overall status
        overall_passed = overall_score >= self.quality_thresholds['minimum_score']
        
        return {
            'overall_score': overall_score,
            'overall_passed': overall_passed,
            'language': language,
            'validation_results': results,
            'thresholds': self.quality_thresholds
        }
    
    def process_pre_tool_use(self, tool_name: str, tool_args: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        Process PreToolUse event for quality gates.
        
        Quality validation only occurs post-tool use, so this returns success.
        
        Args:
            tool_name: Name of the tool about to be used
            tool_args: Arguments for the tool
            session_id: Current session identifier
            
        Returns:
            Response with status for Claude Code
        """
        # Quality gates only performs validation after tool use
        return {
            "status": "success",
            "hook": "quality_gates",
            "event": "pre_tool_use",
            "message": "Quality gates monitoring started"
        }
    
    def process_post_tool_use(self, tool_name: str, tool_result: Any, tool_args: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Process PostToolUse event for quality validation."""
        try:
            # Only trigger on write/edit operations
            if tool_name not in ['Write', 'Edit', 'MultiEdit', 'NotebookEdit']:
                return {
                    'status': 'success',
                    'hook': 'quality_gates', 
                    'event': 'post_tool_use',
                    'message': 'Quality gates not applicable for this tool',
                    'suggestions': []
                }
            
            # Extract file path
            file_paths = extract_file_paths_from_args(tool_args)
            if not file_paths:
                return {
                    'status': 'success',
                    'hook': 'quality_gates',
                    'event': 'post_tool_use', 
                    'message': 'No file paths found for quality validation',
                    'suggestions': []
                }
            
            suggestions = []
            validation_summaries = []
            
            for file_path in file_paths[:3]:  # Limit to first 3 files
                try:
                    # Read file content for validation
                    path = Path(file_path)
                    if not path.exists():
                        continue
                    
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Determine project directory
                    project_dir = str(path.parent)
                    if path.is_absolute():
                        # Walk up to find project root
                        current = path.parent
                        while current != current.parent:
                            if any((current / indicator).exists() for indicator in ['.git', 'package.json', 'pyproject.toml']):
                                project_dir = str(current)
                                break
                            current = current.parent
                    
                    # Run quality validation
                    validation_result = self._run_quality_validation(str(path), content, project_dir)
                    
                    # Create summary
                    summary = {
                        'file_path': str(path),
                        'language': validation_result['language'],
                        'overall_score': validation_result['overall_score'],
                        'passed': validation_result['overall_passed'],
                        'issues_count': sum(len(r.get('issues', [])) for r in validation_result['validation_results']),
                        'suggestions_count': sum(len(r.get('suggestions', [])) for r in validation_result['validation_results'])
                    }
                    validation_summaries.append(summary)
                    
                    # Generate suggestions based on results
                    if validation_result['overall_score'] < self.quality_thresholds['warning_threshold']:
                        suggestions.append({
                            'type': 'quality_warning',
                            'file': str(path),
                            'message': f"Quality score below threshold: {validation_result['overall_score']:.2f}",
                            'priority': 'high' if validation_result['overall_score'] < self.quality_thresholds['minimum_score'] else 'medium'
                        })
                    
                    # Add top suggestions from validation
                    all_suggestions = []
                    for result in validation_result['validation_results']:
                        all_suggestions.extend(result.get('suggestions', []))
                    
                    for suggestion in all_suggestions[:3]:  # Top 3 suggestions
                        suggestions.append({
                            'type': 'quality_improvement',
                            'file': str(path),
                            'message': suggestion,
                            'priority': 'info'
                        })
                    
                    # Add issues as high priority suggestions
                    all_issues = []
                    for result in validation_result['validation_results']:
                        all_issues.extend(result.get('issues', []))
                    
                    for issue in all_issues[:2]:  # Top 2 issues
                        suggestions.append({
                            'type': 'quality_issue',
                            'file': str(path),
                            'message': issue,
                            'priority': 'high'
                        })
                    
                except Exception as e:
                    self.logger.error(f"Quality validation failed for {file_path}: {e}")
                    suggestions.append({
                        'type': 'validation_error',
                        'file': file_path,
                        'message': f"Quality validation failed: {e}",
                        'priority': 'medium'
                    })
            
            # Calculate average quality score
            avg_score = sum(s['overall_score'] for s in validation_summaries) / max(len(validation_summaries), 1)
            
            response = {
                'status': 'success',
                'hook': 'quality_gates',
                'event': 'post_tool_use',
                'quality_summary': {
                    'files_validated': len(validation_summaries),
                    'average_score': avg_score,
                    'files_passed': sum(1 for s in validation_summaries if s['passed']),
                    'total_issues': sum(s['issues_count'] for s in validation_summaries),
                    'total_suggestions': sum(s['suggestions_count'] for s in validation_summaries)
                },
                'validation_summaries': validation_summaries,
                'suggestions': suggestions,
                'metadata': {
                    'session_id': session_id,
                    'tool_name': tool_name,
                    'quality_threshold_met': avg_score >= self.quality_thresholds['minimum_score']
                }
            }
            
            # Log quality results
            if validation_summaries:
                self.logger.info(f"Quality validation completed: {len(validation_summaries)} files, avg score: {avg_score:.2f}")
                high_priority_suggestions = [s for s in suggestions if s.get('priority') == 'high']
                if high_priority_suggestions:
                    self.logger.warning(f"Found {len(high_priority_suggestions)} high-priority quality issues")
            
            return response
            
        except Exception as e:
            return self._handle_error(e, "quality_gates_validation")


def main():
    """Main entry point for quality gates hook."""
    if len(sys.argv) < 2:
        print("Usage: python hook.py post <tool_name> <tool_result> <tool_args> <session_id>", file=sys.stderr)
        sys.exit(1)
    
    event = sys.argv[1]
    
    # Create hook instance
    try:
        hook = QualityGatesHook(input_data={})
    except Exception as e:
        print(f"Error initializing hook: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Execute hook
    try:
        if event == "post":
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
            print(f"Unknown event: {event}. Quality gates only supports 'post' event.", file=sys.stderr)
            sys.exit(1)
        
        # Output result as JSON for Claude Code
        print(json.dumps(result, indent=2))
        
        # Exit with appropriate code
        sys.exit(0 if result.get('status') == 'success' else 1)
        
    except Exception as e:
        error_result = {
            'status': 'error',
            'hook': 'quality_gates',
            'error': str(e),
            'message': 'Quality gates hook execution failed'
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()