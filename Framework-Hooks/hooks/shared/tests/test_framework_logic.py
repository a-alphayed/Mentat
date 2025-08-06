#!/usr/bin/env python3
"""
Comprehensive tests for framework_logic.py

Tests all core functionality including:
- RULES.md compliance validation
- PRINCIPLES.md application
- ORCHESTRATOR.md decision logic
- Risk assessment and complexity scoring
- Performance estimation and optimization
"""

import unittest
import sys
from pathlib import Path

# Add the shared directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from framework_logic import (
    FrameworkLogic, OperationType, RiskLevel, OperationContext,
    ValidationResult
)


class TestFrameworkLogic(unittest.TestCase):
    """Comprehensive tests for FrameworkLogic."""
    
    def setUp(self):
        """Set up test environment."""
        self.framework = FrameworkLogic()
        
        # Create test contexts
        self.simple_context = OperationContext(
            operation_type=OperationType.READ,
            file_count=1,
            directory_count=1,
            has_tests=False,
            is_production=False,
            user_expertise='intermediate',
            project_type='web',
            complexity_score=0.2,
            risk_level=RiskLevel.LOW
        )
        
        self.complex_context = OperationContext(
            operation_type=OperationType.REFACTOR,
            file_count=15,
            directory_count=5,
            has_tests=True,
            is_production=True,
            user_expertise='expert',
            project_type='api',
            complexity_score=0.8,
            risk_level=RiskLevel.HIGH
        )
    
    def test_read_before_write_rule(self):
        """Test RULES.md: Always use Read tool before Write or Edit operations."""
        # Write and Edit operations should require read
        write_context = OperationContext(
            operation_type=OperationType.WRITE,
            file_count=1, directory_count=1, has_tests=False,
            is_production=False, user_expertise='beginner',
            project_type='web', complexity_score=0.3, risk_level=RiskLevel.LOW
        )
        edit_context = OperationContext(
            operation_type=OperationType.EDIT,
            file_count=1, directory_count=1, has_tests=False,
            is_production=False, user_expertise='beginner',
            project_type='web', complexity_score=0.3, risk_level=RiskLevel.LOW
        )
        
        self.assertTrue(self.framework.should_use_read_before_write(write_context))
        self.assertTrue(self.framework.should_use_read_before_write(edit_context))
        
        # Read operations should not require read
        self.assertFalse(self.framework.should_use_read_before_write(self.simple_context))
    
    def test_complexity_score_calculation(self):
        """Test complexity score calculation algorithm."""
        # Simple operation
        simple_data = {
            'file_count': 1,
            'directory_count': 1,
            'operation_type': 'read',
            'multi_language': False,
            'framework_changes': False
        }
        simple_score = self.framework.calculate_complexity_score(simple_data)
        self.assertLess(simple_score, 0.3)
        
        # Complex operation
        complex_data = {
            'file_count': 20,
            'directory_count': 5,
            'operation_type': 'refactor',
            'multi_language': True,
            'framework_changes': True
        }
        complex_score = self.framework.calculate_complexity_score(complex_data)
        self.assertGreater(complex_score, 0.7)
        
        # Score should be capped at 1.0
        extreme_data = {
            'file_count': 1000,
            'directory_count': 100,
            'operation_type': 'system-wide',
            'multi_language': True,
            'framework_changes': True
        }
        extreme_score = self.framework.calculate_complexity_score(extreme_data)
        self.assertEqual(extreme_score, 1.0)
    
    def test_risk_assessment(self):
        """Test risk level assessment logic."""
        # Production context should be high risk
        prod_context = OperationContext(
            operation_type=OperationType.DEPLOY,
            file_count=5, directory_count=2, has_tests=True,
            is_production=True, user_expertise='expert',
            project_type='api', complexity_score=0.5, risk_level=RiskLevel.MEDIUM
        )
        risk = self.framework.assess_risk_level(prod_context)
        self.assertEqual(risk, RiskLevel.HIGH)
        
        # High complexity should be high risk
        high_complexity_context = OperationContext(
            operation_type=OperationType.BUILD,
            file_count=5, directory_count=2, has_tests=False,
            is_production=False, user_expertise='intermediate',
            project_type='web', complexity_score=0.8, risk_level=RiskLevel.LOW
        )
        risk = self.framework.assess_risk_level(high_complexity_context)
        self.assertEqual(risk, RiskLevel.HIGH)
        
        # Many files should be medium risk
        many_files_context = OperationContext(
            operation_type=OperationType.EDIT,
            file_count=15, directory_count=2, has_tests=False,
            is_production=False, user_expertise='intermediate',
            project_type='web', complexity_score=0.3, risk_level=RiskLevel.LOW
        )
        risk = self.framework.assess_risk_level(many_files_context)
        self.assertEqual(risk, RiskLevel.MEDIUM)
        
        # Simple operations should be low risk
        risk = self.framework.assess_risk_level(self.simple_context)
        self.assertEqual(risk, RiskLevel.LOW)
    
    def test_validation_enablement(self):
        """Test when validation should be enabled."""
        # High risk operations should enable validation
        self.assertTrue(self.framework.should_enable_validation(self.complex_context))
        
        # Production operations should enable validation
        prod_context = OperationContext(
            operation_type=OperationType.WRITE,
            file_count=1, directory_count=1, has_tests=False,
            is_production=True, user_expertise='beginner',
            project_type='web', complexity_score=0.2, risk_level=RiskLevel.LOW
        )
        self.assertTrue(self.framework.should_enable_validation(prod_context))
        
        # Deploy operations should enable validation
        deploy_context = OperationContext(
            operation_type=OperationType.DEPLOY,
            file_count=1, directory_count=1, has_tests=False,
            is_production=False, user_expertise='expert',
            project_type='web', complexity_score=0.2, risk_level=RiskLevel.LOW
        )
        self.assertTrue(self.framework.should_enable_validation(deploy_context))
        
        # Simple operations should not require validation
        self.assertFalse(self.framework.should_enable_validation(self.simple_context))
    
    def test_delegation_logic(self):
        """Test delegation decision logic."""
        # Multiple files should trigger delegation
        should_delegate, strategy = self.framework.should_enable_delegation(self.complex_context)
        self.assertTrue(should_delegate)
        self.assertEqual(strategy, "files")
        
        # Multiple directories should trigger delegation
        multi_dir_context = OperationContext(
            operation_type=OperationType.ANALYZE,
            file_count=2, directory_count=4, has_tests=False,
            is_production=False, user_expertise='intermediate',
            project_type='web', complexity_score=0.3, risk_level=RiskLevel.LOW
        )
        should_delegate, strategy = self.framework.should_enable_delegation(multi_dir_context)
        self.assertTrue(should_delegate)
        self.assertEqual(strategy, "folders")
        
        # High complexity should trigger auto delegation
        high_complexity_context = OperationContext(
            operation_type=OperationType.BUILD,
            file_count=2, directory_count=1, has_tests=False,
            is_production=False, user_expertise='intermediate',
            project_type='web', complexity_score=0.7, risk_level=RiskLevel.MEDIUM
        )
        should_delegate, strategy = self.framework.should_enable_delegation(high_complexity_context)
        self.assertTrue(should_delegate)
        self.assertEqual(strategy, "auto")
        
        # Simple operations should not require delegation
        should_delegate, strategy = self.framework.should_enable_delegation(self.simple_context)
        self.assertFalse(should_delegate)
        self.assertEqual(strategy, "none")
    
    def test_operation_validation(self):
        """Test operation validation against PRINCIPLES.md."""
        # Valid operation with all requirements
        valid_operation = {
            'operation_type': 'write',
            'evidence': 'User explicitly requested file creation',
            'has_error_handling': True,
            'affects_logic': True,
            'has_tests': True,
            'is_public_api': False,
            'handles_user_input': False
        }
        result = self.framework.validate_operation(valid_operation)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.issues), 0)
        self.assertGreaterEqual(result.quality_score, 0.7)
        
        # Invalid operation missing error handling
        invalid_operation = {
            'operation_type': 'write',
            'evidence': 'User requested',
            'has_error_handling': False,
            'affects_logic': True,
            'has_tests': False,
            'is_public_api': True,
            'has_documentation': False,
            'handles_user_input': True,
            'has_input_validation': False
        }
        result = self.framework.validate_operation(invalid_operation)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.issues), 0)
        self.assertLess(result.quality_score, 0.7)
        
        # Check specific validation issues
        issue_texts = ' '.join(result.issues).lower()
        self.assertIn('error handling', issue_texts)
        self.assertIn('input', issue_texts)
        
        warning_texts = ' '.join(result.warnings).lower()
        self.assertIn('tests', warning_texts)
        self.assertIn('documentation', warning_texts)
    
    def test_thinking_mode_determination(self):
        """Test thinking mode determination based on complexity."""
        # Very high complexity should trigger ultrathink
        ultra_context = OperationContext(
            operation_type=OperationType.REFACTOR,
            file_count=20, directory_count=5, has_tests=True,
            is_production=True, user_expertise='expert',
            project_type='system', complexity_score=0.85, risk_level=RiskLevel.HIGH
        )
        mode = self.framework.determine_thinking_mode(ultra_context)
        self.assertEqual(mode, "--ultrathink")
        
        # High complexity should trigger think-hard
        hard_context = OperationContext(
            operation_type=OperationType.BUILD,
            file_count=10, directory_count=3, has_tests=True,
            is_production=False, user_expertise='intermediate',
            project_type='web', complexity_score=0.65, risk_level=RiskLevel.MEDIUM
        )
        mode = self.framework.determine_thinking_mode(hard_context)
        self.assertEqual(mode, "--think-hard")
        
        # Medium complexity should trigger think
        medium_context = OperationContext(
            operation_type=OperationType.ANALYZE,
            file_count=5, directory_count=2, has_tests=False,
            is_production=False, user_expertise='intermediate',
            project_type='web', complexity_score=0.4, risk_level=RiskLevel.LOW
        )
        mode = self.framework.determine_thinking_mode(medium_context)
        self.assertEqual(mode, "--think")
        
        # Low complexity should not trigger thinking mode
        mode = self.framework.determine_thinking_mode(self.simple_context)
        self.assertIsNone(mode)
    
    def test_efficiency_mode_enablement(self):
        """Test token efficiency mode enablement logic."""
        # High resource usage should enable efficiency mode
        high_resource_session = {
            'resource_usage_percent': 80,
            'conversation_length': 50,
            'user_requests_brevity': False
        }
        self.assertTrue(self.framework.should_enable_efficiency_mode(high_resource_session))
        
        # Long conversation should enable efficiency mode
        long_conversation_session = {
            'resource_usage_percent': 60,
            'conversation_length': 150,
            'user_requests_brevity': False
        }
        self.assertTrue(self.framework.should_enable_efficiency_mode(long_conversation_session))
        
        # User requesting brevity should enable efficiency mode
        brevity_request_session = {
            'resource_usage_percent': 50,
            'conversation_length': 30,
            'user_requests_brevity': True
        }
        self.assertTrue(self.framework.should_enable_efficiency_mode(brevity_request_session))
        
        # Normal session should not enable efficiency mode
        normal_session = {
            'resource_usage_percent': 40,
            'conversation_length': 20,
            'user_requests_brevity': False
        }
        self.assertFalse(self.framework.should_enable_efficiency_mode(normal_session))
    
    def test_quality_gates_selection(self):
        """Test quality gate selection for different operations."""
        # All operations should have syntax validation
        gates = self.framework.get_quality_gates(self.simple_context)
        self.assertIn('syntax_validation', gates)
        
        # Write/Edit operations should have additional gates
        write_context = OperationContext(
            operation_type=OperationType.WRITE,
            file_count=1, directory_count=1, has_tests=False,
            is_production=False, user_expertise='intermediate',
            project_type='web', complexity_score=0.3, risk_level=RiskLevel.LOW
        )
        gates = self.framework.get_quality_gates(write_context)
        self.assertIn('syntax_validation', gates)
        self.assertIn('type_analysis', gates)
        self.assertIn('code_quality', gates)
        
        # High-risk operations should have security and performance gates
        gates = self.framework.get_quality_gates(self.complex_context)
        self.assertIn('security_assessment', gates)
        self.assertIn('performance_analysis', gates)
        
        # Operations with tests should include test validation
        test_context = OperationContext(
            operation_type=OperationType.BUILD,
            file_count=5, directory_count=2, has_tests=True,
            is_production=False, user_expertise='expert',
            project_type='api', complexity_score=0.5, risk_level=RiskLevel.MEDIUM
        )
        gates = self.framework.get_quality_gates(test_context)
        self.assertIn('test_validation', gates)
        
        # Deploy operations should have integration testing
        deploy_context = OperationContext(
            operation_type=OperationType.DEPLOY,
            file_count=3, directory_count=1, has_tests=True,
            is_production=True, user_expertise='expert',
            project_type='web', complexity_score=0.4, risk_level=RiskLevel.HIGH
        )
        gates = self.framework.get_quality_gates(deploy_context)
        self.assertIn('integration_testing', gates)
        self.assertIn('deployment_validation', gates)
    
    def test_performance_impact_estimation(self):
        """Test performance impact estimation."""
        # Simple operation should have low estimated time
        simple_estimate = self.framework.estimate_performance_impact(self.simple_context)
        self.assertLess(simple_estimate['estimated_time_ms'], 300)
        self.assertEqual(simple_estimate['performance_risk'], 'low')
        self.assertEqual(len(simple_estimate['suggested_optimizations']), 0)
        
        # Complex operation should have higher estimated time and optimizations
        complex_estimate = self.framework.estimate_performance_impact(self.complex_context)
        self.assertGreater(complex_estimate['estimated_time_ms'], 400)
        self.assertGreater(len(complex_estimate['suggested_optimizations']), 2)
        
        # Should suggest appropriate optimizations
        optimizations = complex_estimate['suggested_optimizations']
        opt_text = ' '.join(optimizations).lower()
        self.assertIn('parallel', opt_text)
        self.assertIn('delegation', opt_text)
        
        # Very high estimated time should be high risk
        if complex_estimate['estimated_time_ms'] > 1000:
            self.assertEqual(complex_estimate['performance_risk'], 'high')
    
    def test_superclaude_principles_application(self):
        """Test application of SuperClaude core principles."""
        # Test Evidence > assumptions principle
        assumption_heavy_data = {
            'operation_type': 'analyze',
            'assumptions': ['This should work', 'Users will like it'],
            'evidence': None
        }
        enhanced = self.framework.apply_superclaude_principles(assumption_heavy_data)
        self.assertIn('recommendations', enhanced)
        rec_text = ' '.join(enhanced['recommendations']).lower()
        self.assertIn('evidence', rec_text)
        
        # Test Code > documentation principle
        doc_heavy_data = {
            'operation_type': 'document',
            'has_working_code': False
        }
        enhanced = self.framework.apply_superclaude_principles(doc_heavy_data)
        self.assertIn('warnings', enhanced)
        warning_text = ' '.join(enhanced['warnings']).lower()
        self.assertIn('working code', warning_text)
        
        # Test Efficiency > verbosity principle
        verbose_data = {
            'operation_type': 'generate',
            'output_length': 2000,
            'justification_for_length': None
        }
        enhanced = self.framework.apply_superclaude_principles(verbose_data)
        self.assertIn('efficiency_suggestions', enhanced)
        eff_text = ' '.join(enhanced['efficiency_suggestions']).lower()
        self.assertIn('token efficiency', eff_text)
    
    def test_performance_targets_loading(self):
        """Test that performance targets are loaded correctly."""
        # Should have performance targets loaded
        self.assertIsInstance(self.framework.performance_targets, dict)
        
        # Should have hook-specific targets (with defaults if config not available)
        expected_targets = [
            'session_start_ms',
            'tool_routing_ms', 
            'validation_ms',
            'compression_ms'
        ]
        
        for target in expected_targets:
            self.assertIn(target, self.framework.performance_targets)
            self.assertIsInstance(self.framework.performance_targets[target], (int, float))
            self.assertGreater(self.framework.performance_targets[target], 0)
    
    def test_edge_cases_and_error_handling(self):
        """Test edge cases and error handling."""
        # Empty operation data
        empty_score = self.framework.calculate_complexity_score({})
        self.assertGreaterEqual(empty_score, 0.0)
        self.assertLessEqual(empty_score, 1.0)
        
        # Negative file counts (shouldn't happen but should be handled)
        negative_data = {
            'file_count': -1,
            'directory_count': -1,
            'operation_type': 'unknown'
        }
        negative_score = self.framework.calculate_complexity_score(negative_data)
        self.assertGreaterEqual(negative_score, 0.0)
        
        # Very large file counts
        large_data = {
            'file_count': 1000000,
            'directory_count': 10000,
            'operation_type': 'system-wide'
        }
        large_score = self.framework.calculate_complexity_score(large_data)
        self.assertEqual(large_score, 1.0)  # Should be capped
        
        # Empty validation operation
        empty_validation = self.framework.validate_operation({})
        self.assertIsInstance(empty_validation, ValidationResult)
        self.assertIsInstance(empty_validation.quality_score, float)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)