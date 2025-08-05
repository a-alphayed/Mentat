"""
Core SuperClaude Framework Logic

Implements the core decision-making algorithms from the SuperClaude framework,
including RULES.md, PRINCIPLES.md, and ORCHESTRATOR.md patterns.
"""

import json
import time
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum

from yaml_loader import config_loader


class OperationType(Enum):
    """Types of operations SuperClaude can perform."""
    READ = "read"
    WRITE = "write" 
    EDIT = "edit"
    ANALYZE = "analyze"
    BUILD = "build"
    TEST = "test"
    DEPLOY = "deploy"
    REFACTOR = "refactor"


class RiskLevel(Enum):
    """Risk levels for operations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class OperationContext:
    """Context information for an operation."""
    operation_type: OperationType
    file_count: int
    directory_count: int
    has_tests: bool
    is_production: bool
    user_expertise: str  # beginner, intermediate, expert
    project_type: str   # web, api, cli, library, etc.
    complexity_score: float  # 0.0 to 1.0
    risk_level: RiskLevel


@dataclass
class ValidationResult:
    """Result of validation checks."""
    is_valid: bool
    issues: List[str]
    warnings: List[str]
    suggestions: List[str]
    quality_score: float  # 0.0 to 1.0


class FrameworkLogic:
    """
    Core SuperClaude framework logic implementation.
    
    Encapsulates decision-making algorithms from:
    - RULES.md: Operational rules and security patterns
    - PRINCIPLES.md: Development principles and quality standards
    - ORCHESTRATOR.md: Intelligent routing and coordination
    """
    
    def __init__(self):
        # Load performance targets from SuperClaude configuration
        self.performance_targets = {}
        
        # Get hook-specific performance targets
        self.performance_targets['session_start_ms'] = config_loader.get_hook_config(
            'session_start', 'performance_target_ms', 50
        )
        self.performance_targets['tool_routing_ms'] = config_loader.get_hook_config(
            'pre_tool_use', 'performance_target_ms', 200
        )
        self.performance_targets['validation_ms'] = config_loader.get_hook_config(
            'post_tool_use', 'performance_target_ms', 100
        )
        self.performance_targets['compression_ms'] = config_loader.get_hook_config(
            'pre_compact', 'performance_target_ms', 150
        )
        
        # Load additional performance settings from global configuration
        global_perf = config_loader.get_performance_targets()
        if global_perf:
            self.performance_targets.update(global_perf)
    
    def should_use_read_before_write(self, context: OperationContext) -> bool:
        """
        RULES.md: Always use Read tool before Write or Edit operations.
        """
        return context.operation_type in [OperationType.WRITE, OperationType.EDIT]
    
    def calculate_complexity_score(self, operation_data: Dict[str, Any]) -> float:
        """
        Calculate operation complexity score (0.0 to 1.0).
        
        Factors:
        - File count and types
        - Operation scope
        - Dependencies
        - Risk factors
        """
        score = 0.0
        
        # File count factor (0.0 to 0.3)
        file_count = operation_data.get('file_count', 1)
        if file_count <= 1:
            score += 0.0
        elif file_count <= 3:
            score += 0.1
        elif file_count <= 10:
            score += 0.2
        else:
            score += 0.3
        
        # Directory factor (0.0 to 0.2)
        dir_count = operation_data.get('directory_count', 1)
        if dir_count > 2:
            score += 0.2
        elif dir_count > 1:
            score += 0.1
        
        # Operation type factor (0.0 to 0.3)
        op_type = operation_data.get('operation_type', '')
        if op_type in ['refactor', 'architecture', 'system-wide']:
            score += 0.3
        elif op_type in ['build', 'implement', 'migrate']:
            score += 0.2
        elif op_type in ['fix', 'update', 'improve']:
            score += 0.1
        
        # Language/framework factor (0.0 to 0.2)
        if operation_data.get('multi_language', False):
            score += 0.2
        elif operation_data.get('framework_changes', False):
            score += 0.1
        
        return min(score, 1.0)
    
    def assess_risk_level(self, context: OperationContext) -> RiskLevel:
        """
        Assess risk level based on operation context.
        """
        if context.is_production:
            return RiskLevel.HIGH
        
        if context.complexity_score > 0.7:
            return RiskLevel.HIGH
        elif context.complexity_score > 0.4:
            return RiskLevel.MEDIUM
        elif context.file_count > 10:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def should_enable_validation(self, context: OperationContext) -> bool:
        """
        ORCHESTRATOR.md: Enable validation for production code or high-risk operations.
        """
        return (
            context.is_production or 
            context.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL] or
            context.operation_type in [OperationType.DEPLOY, OperationType.REFACTOR]
        )
    
    def should_enable_delegation(self, context: OperationContext) -> Tuple[bool, str]:
        """
        ORCHESTRATOR.md: Enable delegation for multi-file operations.
        
        Returns:
            (should_delegate, delegation_strategy)
        """
        if context.file_count > 3:
            return True, "files"
        elif context.directory_count > 2:
            return True, "folders"
        elif context.complexity_score > 0.4:
            return True, "auto"
        else:
            return False, "none"
    
    def validate_operation(self, operation_data: Dict[str, Any]) -> ValidationResult:
        """
        PRINCIPLES.md: Validate operation against core principles.
        """
        issues = []
        warnings = []
        suggestions = []
        quality_score = 1.0
        
        # Check for evidence-based decision making
        if 'evidence' not in operation_data:
            warnings.append("No evidence provided for decision")
            quality_score -= 0.1
        
        # Check for proper error handling
        if operation_data.get('operation_type') in ['write', 'edit', 'deploy']:
            if not operation_data.get('has_error_handling', False):
                issues.append("Error handling not implemented")
                quality_score -= 0.2
        
        # Check for test coverage
        if operation_data.get('affects_logic', False):
            if not operation_data.get('has_tests', False):
                warnings.append("No tests found for logic changes")
                quality_score -= 0.1
                suggestions.append("Add unit tests for new logic")
        
        # Check for documentation
        if operation_data.get('is_public_api', False):
            if not operation_data.get('has_documentation', False):
                warnings.append("Public API lacks documentation")
                quality_score -= 0.1
                suggestions.append("Add API documentation")
        
        # Security checks
        if operation_data.get('handles_user_input', False):
            if not operation_data.get('has_input_validation', False):
                issues.append("User input handling without validation")
                quality_score -= 0.3
        
        is_valid = len(issues) == 0 and quality_score >= 0.7
        
        return ValidationResult(
            is_valid=is_valid,
            issues=issues,
            warnings=warnings,
            suggestions=suggestions,
            quality_score=max(quality_score, 0.0)
        )
    
    def determine_thinking_mode(self, context: OperationContext) -> Optional[str]:
        """
        FLAGS.md: Determine appropriate thinking mode based on complexity.
        """
        if context.complexity_score >= 0.8:
            return "--ultrathink"
        elif context.complexity_score >= 0.6:
            return "--think-hard"
        elif context.complexity_score >= 0.3:
            return "--think"
        else:
            return None
    
    def should_enable_efficiency_mode(self, session_data: Dict[str, Any]) -> bool:
        """
        MODE_Token_Efficiency.md: Enable efficiency mode based on resource usage.
        """
        resource_usage = session_data.get('resource_usage_percent', 0)
        conversation_length = session_data.get('conversation_length', 0)
        
        return (
            resource_usage > 75 or
            conversation_length > 100 or
            session_data.get('user_requests_brevity', False)
        )
    
    def get_quality_gates(self, context: OperationContext) -> List[str]:
        """
        ORCHESTRATOR.md: Get appropriate quality gates for operation.
        """
        gates = ['syntax_validation']
        
        if context.operation_type in [OperationType.WRITE, OperationType.EDIT]:
            gates.extend(['type_analysis', 'code_quality'])
        
        if self.should_enable_validation(context):
            gates.extend(['security_assessment', 'performance_analysis'])
        
        if context.has_tests:
            gates.append('test_validation')
        
        if context.operation_type == OperationType.DEPLOY:
            gates.extend(['integration_testing', 'deployment_validation'])
        
        return gates
    
    def estimate_performance_impact(self, context: OperationContext) -> Dict[str, Any]:
        """
        Estimate performance impact and suggested optimizations.
        """
        base_time = 100  # ms
        
        # Calculate estimated time based on complexity
        estimated_time = base_time * (1 + context.complexity_score * 3)
        
        # Factor in file count
        if context.file_count > 5:
            estimated_time *= 1.5
        
        # Suggest optimizations
        optimizations = []
        if context.file_count > 3:
            optimizations.append("Consider parallel processing")
        if context.complexity_score > 0.6:
            optimizations.append("Enable delegation mode")
        if context.directory_count > 2:
            optimizations.append("Use folder-based delegation")
        
        return {
            'estimated_time_ms': int(estimated_time),
            'performance_risk': 'high' if estimated_time > 1000 else 'low',
            'suggested_optimizations': optimizations,
            'efficiency_gains_possible': len(optimizations) > 0
        }
    
    def apply_superclaude_principles(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply SuperClaude core principles to operation planning.
        
        Returns enhanced operation data with principle-based recommendations.
        """
        enhanced_data = operation_data.copy()
        
        # Evidence > assumptions
        if 'assumptions' in enhanced_data and not enhanced_data.get('evidence'):
            enhanced_data['recommendations'] = enhanced_data.get('recommendations', [])
            enhanced_data['recommendations'].append(
                "Gather evidence to validate assumptions"
            )
        
        # Code > documentation
        if enhanced_data.get('operation_type') == 'document' and not enhanced_data.get('has_working_code'):
            enhanced_data['warnings'] = enhanced_data.get('warnings', [])
            enhanced_data['warnings'].append(
                "Ensure working code exists before extensive documentation"
            )
        
        # Efficiency > verbosity
        if enhanced_data.get('output_length', 0) > 1000 and not enhanced_data.get('justification_for_length'):
            enhanced_data['efficiency_suggestions'] = enhanced_data.get('efficiency_suggestions', [])
            enhanced_data['efficiency_suggestions'].append(
                "Consider token efficiency techniques for long outputs"
            )
        
        return enhanced_data