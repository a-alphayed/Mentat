#!/usr/bin/env python3
"""
Comprehensive tests for pattern_detection.py

Tests all core functionality including:
- Mode activation pattern detection
- MCP server selection patterns
- Complexity and performance pattern recognition
- Persona hint detection
- Real-world scenario pattern matching
"""

import unittest
import sys
from pathlib import Path

# Add the shared directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from pattern_detection import (
    PatternDetector, PatternType, PatternMatch, DetectionResult
)


class TestPatternDetection(unittest.TestCase):
    """Comprehensive tests for PatternDetector."""
    
    def setUp(self):
        """Set up test environment."""
        self.detector = PatternDetector()
        
        # Test contexts
        self.simple_context = {
            'resource_usage_percent': 30,
            'conversation_length': 20,
            'user_expertise': 'intermediate'
        }
        
        self.high_resource_context = {
            'resource_usage_percent': 80,
            'conversation_length': 150,
            'user_expertise': 'expert'
        }
        
        # Test operation data
        self.simple_operation = {
            'file_count': 2,
            'complexity_score': 0.3,
            'operation_type': 'read'
        }
        
        self.complex_operation = {
            'file_count': 20,
            'complexity_score': 0.8,
            'operation_type': 'refactor'
        }
    
    def test_brainstorming_mode_detection(self):
        """Test detection of brainstorming mode triggers."""
        brainstorm_inputs = [
            "I want to build something for task management",
            "Thinking about creating a new web application",
            "Not sure what kind of API to build",
            "Maybe we could implement a chat system",
            "Could we brainstorm some ideas for the frontend?",
            "I have unclear requirements for this project"
        ]
        
        for user_input in brainstorm_inputs:
            with self.subTest(input=user_input):
                result = self.detector.detect_patterns(
                    user_input, self.simple_context, self.simple_operation
                )
                
                # Should detect brainstorming mode
                brainstorm_modes = [mode for mode in result.recommended_modes if mode == 'brainstorming']
                self.assertGreater(len(brainstorm_modes), 0, f"Failed to detect brainstorming in: {user_input}")
                
                # Should have brainstorming matches
                brainstorm_matches = [m for m in result.matches if m.pattern_name == 'brainstorming']
                self.assertGreater(len(brainstorm_matches), 0)
                
                if brainstorm_matches:
                    match = brainstorm_matches[0]
                    self.assertEqual(match.pattern_type, PatternType.MODE_TRIGGER)
                    self.assertGreater(match.confidence, 0.7)
    
    def test_task_management_mode_detection(self):
        """Test detection of task management mode triggers."""
        task_management_inputs = [
            "Build a complex system with multiple components",
            "Implement a comprehensive web application",
            "Create a large-scale microservice architecture",
            "We need to coordinate multiple tasks across the project",
            "This is a complex operation requiring multiple files"
        ]
        
        for user_input in task_management_inputs:
            with self.subTest(input=user_input):
                result = self.detector.detect_patterns(
                    user_input, self.simple_context, self.simple_operation
                )
                
                # Should detect task management mode
                task_modes = [mode for mode in result.recommended_modes if mode == 'task_management']
                self.assertGreater(len(task_modes), 0, f"Failed to detect task management in: {user_input}")
    
    def test_token_efficiency_mode_detection(self):
        """Test detection of token efficiency mode triggers."""
        efficiency_inputs = [
            "Please give me a brief summary",
            "I need a concise response",
            "Can you compress this output?",
            "Keep it short and efficient",
            "I'm running low on tokens"
        ]
        
        for user_input in efficiency_inputs:
            with self.subTest(input=user_input):
                result = self.detector.detect_patterns(
                    user_input, self.simple_context, self.simple_operation
                )
                
                # Should detect efficiency mode
                efficiency_modes = [mode for mode in result.recommended_modes if mode == 'token_efficiency']
                self.assertGreater(len(efficiency_modes), 0, f"Failed to detect efficiency mode in: {user_input}")
        
        # Test automatic efficiency mode for high resource usage
        result = self.detector.detect_patterns(
            "Analyze this code", self.high_resource_context, self.simple_operation
        )
        efficiency_modes = [mode for mode in result.recommended_modes if mode == 'token_efficiency']
        self.assertGreater(len(efficiency_modes), 0, "Should auto-detect efficiency mode for high resource usage")
    
    def test_context7_mcp_detection(self):
        """Test detection of Context7 MCP server needs."""
        context7_inputs = [
            "I need React documentation for this component",
            "What's the official way to use Vue Router?",
            "Can you help me with Django best practices?",
            "I need to import a new library",
            "Show me the standard pattern for Express middleware"
        ]
        
        for user_input in context7_inputs:
            with self.subTest(input=user_input):
                result = self.detector.detect_patterns(
                    user_input, self.simple_context, self.simple_operation
                )
                
                # Should recommend Context7
                self.assertIn('context7', result.recommended_mcp_servers, 
                             f"Failed to detect Context7 need in: {user_input}")
                
                # Should have Context7 matches
                context7_matches = [m for m in result.matches if m.pattern_name == 'context7']
                self.assertGreater(len(context7_matches), 0)
    
    def test_sequential_mcp_detection(self):
        """Test detection of Sequential MCP server needs."""
        sequential_inputs = [
            "Analyze this complex architecture problem",
            "Debug this multi-step issue systematically",
            "I need to troubleshoot this performance bottleneck",
            "Let's investigate the root cause of this error",
            "Can you help me with complex system design?"
        ]
        
        for user_input in sequential_inputs:
            with self.subTest(input=user_input):
                result = self.detector.detect_patterns(
                    user_input, self.simple_context, self.simple_operation
                )
                
                # Should recommend Sequential
                self.assertIn('sequential', result.recommended_mcp_servers,
                             f"Failed to detect Sequential need in: {user_input}")
    
    def test_magic_mcp_detection(self):
        """Test detection of Magic MCP server needs."""
        magic_inputs = [
            "Create a React component for user login",
            "Build a responsive modal dialog",
            "I need a navigation component",
            "Design a mobile-friendly form",
            "Create an accessible button component"
        ]
        
        for user_input in magic_inputs:
            with self.subTest(input=user_input):
                result = self.detector.detect_patterns(
                    user_input, self.simple_context, self.simple_operation
                )
                
                # Should recommend Magic
                self.assertIn('magic', result.recommended_mcp_servers,
                             f"Failed to detect Magic need in: {user_input}")
    
    def test_playwright_mcp_detection(self):
        """Test detection of Playwright MCP server needs."""
        playwright_inputs = [
            "I need to test this user workflow end-to-end",
            "Create browser automation for this feature",
            "Can you help me with cross-browser testing?",
            "I need performance testing for this page",
            "Write visual regression tests"
        ]
        
        for user_input in playwright_inputs:
            with self.subTest(input=user_input):
                result = self.detector.detect_patterns(
                    user_input, self.simple_context, self.simple_operation
                )
                
                # Should recommend Playwright
                self.assertIn('playwright', result.recommended_mcp_servers,
                             f"Failed to detect Playwright need in: {user_input}")
    
    def test_morphllm_vs_serena_intelligence_selection(self):
        """Test intelligent selection between Morphllm and Serena."""
        # Simple operation should prefer Morphllm
        simple_result = self.detector.detect_patterns(
            "Edit this file", self.simple_context, self.simple_operation
        )
        
        morphllm_matches = [m for m in simple_result.matches if m.pattern_name == 'morphllm']
        serena_matches = [m for m in simple_result.matches if m.pattern_name == 'serena']
        
        # For simple operations, should prefer Morphllm
        if morphllm_matches or serena_matches:
            self.assertGreater(len(morphllm_matches), len(serena_matches))
        
        # Complex operation should prefer Serena
        complex_result = self.detector.detect_patterns(
            "Refactor the entire codebase", self.simple_context, self.complex_operation
        )
        
        complex_morphllm_matches = [m for m in complex_result.matches if m.pattern_name == 'morphllm']
        complex_serena_matches = [m for m in complex_result.matches if m.pattern_name == 'serena']
        
        # For complex operations, should prefer Serena
        if complex_morphllm_matches or complex_serena_matches:
            self.assertGreater(len(complex_serena_matches), len(complex_morphllm_matches))
    
    def test_complexity_pattern_detection(self):
        """Test detection of complexity indicators."""
        high_complexity_inputs = [
            "Refactor the entire codebase architecture",
            "Migrate all components to the new system", 
            "Restructure the complete application",
            "This is a very complex algorithmic problem"
        ]
        
        for user_input in high_complexity_inputs:
            with self.subTest(input=user_input):
                result = self.detector.detect_patterns(
                    user_input, self.simple_context, self.simple_operation
                )
                
                # Should detect high complexity
                complexity_matches = [m for m in result.matches 
                                    if m.pattern_type == PatternType.COMPLEXITY_INDICATOR]
                self.assertGreater(len(complexity_matches), 0,
                                 f"Failed to detect complexity in: {user_input}")
                
                # Should increase complexity score
                base_score = self.simple_operation.get('complexity_score', 0.0)
                self.assertGreater(result.complexity_score, base_score)
        
        # Test file count complexity
        many_files_result = self.detector.detect_patterns(
            "Process these files", self.simple_context, 
            {'file_count': 10, 'complexity_score': 0.2}
        )
        
        file_complexity_matches = [m for m in many_files_result.matches 
                                 if 'multi_file' in m.pattern_name]
        self.assertGreater(len(file_complexity_matches), 0)
    
    def test_persona_pattern_detection(self):
        """Test detection of persona hints."""
        persona_test_cases = [
            ("Review the system architecture design", "architect"),
            ("Optimize this for better performance", "performance"),
            ("Check this code for security vulnerabilities", "security"),
            ("Create a beautiful user interface", "frontend"),
            ("Design the API endpoints", "backend"),
            ("Set up the deployment pipeline", "devops"),
            ("Write comprehensive tests for this", "testing")
        ]
        
        for user_input, expected_persona in persona_test_cases:
            with self.subTest(input=user_input, persona=expected_persona):
                result = self.detector.detect_patterns(
                    user_input, self.simple_context, self.simple_operation
                )
                
                # Should detect the persona hint
                persona_matches = [m for m in result.matches 
                                 if m.pattern_type == PatternType.PERSONA_HINT
                                 and m.pattern_name == expected_persona]
                self.assertGreater(len(persona_matches), 0,
                                 f"Failed to detect {expected_persona} persona in: {user_input}")
    
    def test_thinking_mode_flag_suggestions(self):
        """Test thinking mode flag suggestions based on complexity."""
        # Ultra-high complexity should suggest --ultrathink
        ultra_complex_operation = {'complexity_score': 0.85, 'file_count': 25}
        result = self.detector.detect_patterns(
            "Complex system analysis", self.simple_context, ultra_complex_operation
        )
        self.assertIn("--ultrathink", result.suggested_flags, 
                     "Should suggest --ultrathink for ultra-complex operations")
        
        # High complexity should suggest --think-hard
        high_complex_operation = {'complexity_score': 0.65, 'file_count': 10}
        result = self.detector.detect_patterns(
            "System analysis", self.simple_context, high_complex_operation
        )
        self.assertIn("--think-hard", result.suggested_flags,
                     "Should suggest --think-hard for high complexity")
        
        # Medium complexity should suggest --think
        medium_complex_operation = {'complexity_score': 0.4, 'file_count': 5}
        result = self.detector.detect_patterns(
            "Code analysis", self.simple_context, medium_complex_operation
        )
        self.assertIn("--think", result.suggested_flags,
                     "Should suggest --think for medium complexity")
    
    def test_delegation_flag_suggestions(self):
        """Test delegation flag suggestions."""
        # Many files should suggest delegation
        many_files_operation = {'file_count': 8, 'complexity_score': 0.4}
        result = self.detector.detect_patterns(
            "Process multiple files", self.simple_context, many_files_operation
        )
        
        # Should suggest delegation
        delegation_flags = [flag for flag in result.suggested_flags if 'delegate' in flag]
        self.assertGreater(len(delegation_flags), 0, "Should suggest delegation for multi-file operations")
    
    def test_efficiency_flag_suggestions(self):
        """Test efficiency flag suggestions."""
        # High resource usage should suggest efficiency flags
        result = self.detector.detect_patterns(
            "Analyze this code", self.high_resource_context, self.simple_operation
        )
        
        self.assertIn("--uc", result.suggested_flags,
                     "Should suggest --uc for high resource usage")
        
        # User requesting brevity should suggest efficiency
        brevity_result = self.detector.detect_patterns(
            "Please be brief and concise", self.simple_context, self.simple_operation
        )
        
        self.assertIn("--uc", brevity_result.suggested_flags,
                     "Should suggest --uc when user requests brevity")
    
    def test_validation_flag_suggestions(self):
        """Test validation flag suggestions."""
        # High complexity should suggest validation
        high_complexity_operation = {'complexity_score': 0.8, 'file_count': 15}
        result = self.detector.detect_patterns(
            "Major refactoring", self.simple_context, high_complexity_operation
        )
        
        self.assertIn("--validate", result.suggested_flags,
                     "Should suggest --validate for high complexity operations")
        
        # Production context should suggest validation
        production_context = {'is_production': True, 'resource_usage_percent': 40}
        result = self.detector.detect_patterns(
            "Deploy changes", production_context, self.simple_operation
        )
        
        self.assertIn("--validate", result.suggested_flags,
                     "Should suggest --validate for production operations")
    
    def test_confidence_score_calculation(self):
        """Test confidence score calculation."""
        # Clear patterns should have high confidence
        clear_result = self.detector.detect_patterns(
            "Create a React component with responsive design",
            self.simple_context, self.simple_operation
        )
        
        self.assertGreater(clear_result.confidence_score, 0.7,
                          "Clear patterns should have high confidence")
        
        # Ambiguous input should have lower confidence
        ambiguous_result = self.detector.detect_patterns(
            "Do something", self.simple_context, self.simple_operation
        )
        
        # Should still have some confidence but lower
        self.assertLessEqual(ambiguous_result.confidence_score, clear_result.confidence_score)
    
    def test_comprehensive_pattern_integration(self):
        """Test comprehensive pattern detection integration."""
        complex_user_input = """
        I want to build a comprehensive React application with multiple components.
        It needs to be responsive, accessible, and well-tested across browsers.
        The architecture should be scalable and the code should be optimized for performance.
        I also need documentation and want to follow best practices.
        """
        
        complex_context = {
            'resource_usage_percent': 60,
            'conversation_length': 80,
            'user_expertise': 'expert',
            'is_production': True
        }
        
        complex_operation_data = {
            'file_count': 12,
            'complexity_score': 0.7,
            'operation_type': 'build',
            'has_external_dependencies': True
        }
        
        result = self.detector.detect_patterns(
            complex_user_input, complex_context, complex_operation_data
        )
        
        # Should detect multiple modes
        self.assertIn('task_management', result.recommended_modes,
                     "Should detect task management for complex build")
        
        # Should recommend multiple MCP servers
        expected_servers = ['magic', 'context7', 'playwright']
        for server in expected_servers:
            self.assertIn(server, result.recommended_mcp_servers,
                         f"Should recommend {server} server")
        
        # Should suggest appropriate flags
        self.assertIn('--think-hard', result.suggested_flags,
                     "Should suggest thinking mode for complex operation")
        self.assertIn('--delegate auto', result.suggested_flags,
                     "Should suggest delegation for multi-file operation")
        self.assertIn('--validate', result.suggested_flags,
                     "Should suggest validation for production/complex operation")
        
        # Should have high complexity score
        self.assertGreater(result.complexity_score, 0.7,
                          "Should calculate high complexity score")
        
        # Should have reasonable confidence
        self.assertGreater(result.confidence_score, 0.6,
                          "Should have good confidence in comprehensive detection")
    
    def test_edge_cases_and_error_handling(self):
        """Test edge cases and error handling."""
        # Empty input
        empty_result = self.detector.detect_patterns("", {}, {})
        self.assertIsInstance(empty_result, DetectionResult)
        self.assertIsInstance(empty_result.matches, list)
        self.assertIsInstance(empty_result.recommended_modes, list)
        self.assertIsInstance(empty_result.recommended_mcp_servers, list)
        
        # Very long input
        long_input = "test " * 1000
        long_result = self.detector.detect_patterns(long_input, self.simple_context, self.simple_operation)
        self.assertIsInstance(long_result, DetectionResult)
        
        # Special characters
        special_input = "Test with special chars: @#$%^&*()[]{}|\\:;\"'<>,.?/~`"
        special_result = self.detector.detect_patterns(special_input, self.simple_context, self.simple_operation)
        self.assertIsInstance(special_result, DetectionResult)
        
        # Unicode characters
        unicode_input = "测试 Unicode 字符 🚀 and émojis"
        unicode_result = self.detector.detect_patterns(unicode_input, self.simple_context, self.simple_operation)
        self.assertIsInstance(unicode_result, DetectionResult)
        
        # Missing operation data fields
        minimal_operation = {}
        minimal_result = self.detector.detect_patterns(
            "Test input", self.simple_context, minimal_operation
        )
        self.assertIsInstance(minimal_result, DetectionResult)
        
        # Extreme values
        extreme_operation = {
            'file_count': -1,
            'complexity_score': 999.0,
            'operation_type': None
        }
        extreme_result = self.detector.detect_patterns(
            "Test input", self.simple_context, extreme_operation
        )
        self.assertIsInstance(extreme_result, DetectionResult)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)