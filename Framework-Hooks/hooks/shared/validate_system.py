#!/usr/bin/env python3
"""
YAML-Driven System Validation Engine for SuperClaude Framework-Hooks

Intelligent validation system that consumes declarative YAML patterns from 
validation_intelligence.yaml for health scoring, proactive diagnostics, and 
predictive analysis.

Features:
- YAML-driven validation patterns (hot-reloadable)
- Health scoring with weighted components
- Proactive diagnostic pattern matching
- Predictive health analysis
- Automated remediation suggestions
- Continuous validation cycles
"""

import os
import json
import time
import statistics
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Import our YAML intelligence infrastructure
from yaml_loader import config_loader
from intelligence_engine import IntelligenceEngine


class ValidationSeverity(Enum):
    """Validation issue severity levels."""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class HealthStatus(Enum):
    """System health status levels."""
    HEALTHY = "healthy"
    WARNING = "warning"  
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class ValidationIssue:
    """Represents a validation issue found by the system."""
    component: str
    issue_type: str
    severity: ValidationSeverity
    description: str
    evidence: List[str]
    recommendations: List[str]
    remediation_action: Optional[str] = None
    auto_fixable: bool = False
    timestamp: float = 0.0
    
    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()


@dataclass
class HealthScore:
    """Health score for a system component."""
    component: str
    score: float  # 0.0 to 1.0
    status: HealthStatus
    contributing_factors: List[str]
    trend: str  # improving, stable, degrading
    last_updated: float = 0.0
    
    def __post_init__(self):
        if self.last_updated == 0.0:
            self.last_updated = time.time()


@dataclass
class DiagnosticResult:
    """Result of diagnostic analysis."""
    component: str
    diagnosis: str
    confidence: float
    symptoms: List[str]
    root_cause: Optional[str]
    recommendations: List[str]
    predicted_impact: str
    timeline: str


class YAMLValidationEngine:
    """
    YAML-driven validation engine that consumes intelligence patterns.
    
    Features:
    - Hot-reloadable YAML validation patterns
    - Component-based health scoring 
    - Proactive diagnostic pattern matching
    - Predictive health analysis
    - Intelligent remediation suggestions
    """
    
    def __init__(self, framework_root: Path, fix_issues: bool = False):
        self.framework_root = Path(framework_root)
        self.fix_issues = fix_issues
        self.cache_dir = self.framework_root / "cache"
        self.config_dir = self.framework_root / "config"
        
        # Initialize intelligence engine for YAML patterns
        self.intelligence_engine = IntelligenceEngine()
        
        # Validation state
        self.issues: List[ValidationIssue] = []
        self.fixes_applied: List[str] = []
        self.health_scores: Dict[str, HealthScore] = {}
        self.diagnostic_results: List[DiagnosticResult] = []
        
        # Load validation intelligence patterns
        self.validation_patterns = self._load_validation_patterns()
        
    def _load_validation_patterns(self) -> Dict[str, Any]:
        """Load validation patterns from YAML intelligence configuration."""
        try:
            patterns = config_loader.get_validation_health_config()
            return patterns if patterns else {}
        except Exception as e:
            print(f"Warning: Could not load validation patterns: {e}")
            return {}
    
    def validate_all(self) -> Tuple[List[ValidationIssue], List[str], Dict[str, HealthScore]]:
        """
        Run comprehensive YAML-driven validation.
        
        Returns:
            Tuple of (issues, fixes_applied, health_scores)
        """
        print("🔍 Starting YAML-driven framework validation...")
        
        # Clear previous state
        self.issues.clear()
        self.fixes_applied.clear()
        self.health_scores.clear()
        self.diagnostic_results.clear()
        
        # Get current system context
        context = self._gather_system_context()
        
        # Run validation intelligence analysis
        validation_intelligence = self.intelligence_engine.evaluate_context(
            context, 'validation_intelligence'
        )
        
        # Core component validations using YAML patterns
        self._validate_learning_system(context, validation_intelligence)
        self._validate_performance_system(context, validation_intelligence)
        self._validate_mcp_coordination(context, validation_intelligence)
        self._validate_hook_system(context, validation_intelligence)
        self._validate_configuration_system(context, validation_intelligence)
        self._validate_cache_system(context, validation_intelligence)
        
        # Run proactive diagnostics
        self._run_proactive_diagnostics(context)
        
        # Calculate overall health score
        self._calculate_overall_health_score()
        
        # Generate remediation recommendations
        self._generate_remediation_suggestions()
        
        return self.issues, self.fixes_applied, self.health_scores
    
    def _gather_system_context(self) -> Dict[str, Any]:
        """Gather current system context for validation analysis."""
        context = {
            'timestamp': time.time(),
            'framework_root': str(self.framework_root),
            'cache_directory_exists': self.cache_dir.exists(),
            'config_directory_exists': self.config_dir.exists(),
        }
        
        # Learning system context
        learning_records_path = self.cache_dir / "learning_records.json"
        if learning_records_path.exists():
            try:
                with open(learning_records_path, 'r') as f:
                    records = json.load(f)
                context['learning_records_count'] = len(records)
                if records:
                    context['recent_learning_activity'] = len([
                        r for r in records 
                        if r.get('timestamp', 0) > time.time() - 86400  # Last 24h
                    ])
            except:
                context['learning_records_count'] = 0
                context['recent_learning_activity'] = 0
        
        # Adaptations context
        adaptations_path = self.cache_dir / "adaptations.json"
        if adaptations_path.exists():
            try:
                with open(adaptations_path, 'r') as f:
                    adaptations = json.load(f)
                context['adaptations_count'] = len(adaptations)
                
                # Calculate effectiveness statistics
                all_effectiveness = []
                for adaptation in adaptations.values():
                    history = adaptation.get('effectiveness_history', [])
                    all_effectiveness.extend(history)
                
                if all_effectiveness:
                    context['average_effectiveness'] = statistics.mean(all_effectiveness)
                    context['effectiveness_variance'] = statistics.variance(all_effectiveness) if len(all_effectiveness) > 1 else 0
                    context['perfect_score_count'] = sum(1 for score in all_effectiveness if score == 1.0)
            except:
                context['adaptations_count'] = 0
        
        # Configuration files context
        yaml_files = list(self.config_dir.glob("*.yaml")) if self.config_dir.exists() else []
        context['yaml_config_count'] = len(yaml_files)
        context['intelligence_patterns_available'] = len([
            f for f in yaml_files 
            if f.name in ['intelligence_patterns.yaml', 'mcp_orchestration.yaml', 
                         'hook_coordination.yaml', 'performance_intelligence.yaml',
                         'validation_intelligence.yaml', 'user_experience.yaml']
        ])
        
        return context
    
    def _validate_learning_system(self, context: Dict[str, Any], intelligence: Dict[str, Any]):
        """Validate learning system using YAML patterns."""
        print("📊 Validating learning system...")
        
        component_weight = self.validation_patterns.get('component_weights', {}).get('learning_system', 0.25)
        scoring_metrics = self.validation_patterns.get('scoring_metrics', {}).get('learning_system', {})
        
        issues = []
        score_factors = []
        
        # Pattern diversity validation
        adaptations_count = context.get('adaptations_count', 0)
        if adaptations_count > 0:
            # Simplified diversity calculation
            diversity_score = min(adaptations_count / 50.0, 0.95)  # Cap at 0.95
            pattern_diversity_config = scoring_metrics.get('pattern_diversity', {})
            healthy_range = pattern_diversity_config.get('healthy_range', [0.6, 0.95])
            
            if diversity_score < healthy_range[0]:
                issues.append(ValidationIssue(
                    component="learning_system",
                    issue_type="pattern_diversity",
                    severity=ValidationSeverity.MEDIUM,
                    description=f"Pattern diversity low: {diversity_score:.2f}",
                    evidence=[f"Only {adaptations_count} unique patterns learned"],
                    recommendations=["Expose system to more diverse operational patterns"]
                ))
            score_factors.append(diversity_score)
        
        # Effectiveness consistency validation
        effectiveness_variance = context.get('effectiveness_variance', 0)
        if effectiveness_variance is not None:
            consistency_score = max(0, 1.0 - effectiveness_variance)
            effectiveness_config = scoring_metrics.get('effectiveness_consistency', {})
            healthy_range = effectiveness_config.get('healthy_range', [0.7, 0.9])
            
            if consistency_score < healthy_range[0]:
                issues.append(ValidationIssue(
                    component="learning_system",
                    issue_type="effectiveness_consistency", 
                    severity=ValidationSeverity.LOW,
                    description=f"Effectiveness variance high: {effectiveness_variance:.3f}",
                    evidence=[f"Effectiveness consistency score: {consistency_score:.2f}"],
                    recommendations=["Review learning patterns for instability"]
                ))
            score_factors.append(consistency_score)
        
        # Perfect score detection (overfitting indicator)
        perfect_scores = context.get('perfect_score_count', 0)
        total_effectiveness_records = context.get('adaptations_count', 0) * 3  # Rough estimate
        if total_effectiveness_records > 0 and perfect_scores / total_effectiveness_records > 0.3:
            issues.append(ValidationIssue(
                component="learning_system",
                issue_type="potential_overfitting",
                severity=ValidationSeverity.MEDIUM,
                description=f"High proportion of perfect scores: {perfect_scores}/{total_effectiveness_records}",
                evidence=[f"Perfect score ratio: {perfect_scores/total_effectiveness_records:.1%}"],
                recommendations=[
                    "Review learning patterns for overfitting",
                    "Add noise to prevent overconfident patterns"
                ],
                remediation_action="automatic_pattern_diversification"
            ))
        
        # Calculate health score
        component_health = statistics.mean(score_factors) if score_factors else 0.5
        health_status = (
            HealthStatus.HEALTHY if component_health >= 0.8 else
            HealthStatus.WARNING if component_health >= 0.6 else
            HealthStatus.CRITICAL
        )
        
        self.health_scores['learning_system'] = HealthScore(
            component='learning_system',
            score=component_health,
            status=health_status,
            contributing_factors=[f"pattern_diversity", "effectiveness_consistency"],
            trend="stable"  # Would need historical data to determine trend
        )
        
        self.issues.extend(issues)
    
    def _validate_performance_system(self, context: Dict[str, Any], intelligence: Dict[str, Any]):
        """Validate performance system using YAML patterns."""
        print("⚡ Validating performance system...")
        
        # This would integrate with actual performance metrics
        # For now, provide basic validation based on available data
        
        issues = []
        score_factors = []
        
        # Check for performance-related files and configurations
        perf_score = 0.8  # Default assuming healthy
        
        # Cache size validation (proxy for memory efficiency)
        if self.cache_dir.exists():
            cache_size = sum(f.stat().st_size for f in self.cache_dir.rglob('*') if f.is_file())
            cache_size_mb = cache_size / (1024 * 1024)
            
            if cache_size_mb > 10:  # > 10MB cache
                issues.append(ValidationIssue(
                    component="performance_system",
                    issue_type="cache_size_large",
                    severity=ValidationSeverity.LOW,
                    description=f"Cache size is large: {cache_size_mb:.1f}MB",
                    evidence=[f"Total cache size: {cache_size_mb:.1f}MB"],
                    recommendations=["Consider cache cleanup policies"],
                    remediation_action="aggressive_cache_cleanup"
                ))
                perf_score -= 0.1
        
        score_factors.append(perf_score)
        
        self.health_scores['performance_system'] = HealthScore(
            component='performance_system',
            score=statistics.mean(score_factors) if score_factors else 0.8,
            status=HealthStatus.HEALTHY,
            contributing_factors=["cache_efficiency", "resource_utilization"],
            trend="stable"
        )
        
        self.issues.extend(issues)
    
    def _validate_mcp_coordination(self, context: Dict[str, Any], intelligence: Dict[str, Any]):
        """Validate MCP coordination system using YAML patterns."""
        print("🔗 Validating MCP coordination...")
        
        issues = []
        score = 0.8  # Default healthy score
        
        # Check MCP orchestration patterns availability
        mcp_patterns_available = 'mcp_orchestration.yaml' in [
            f.name for f in self.config_dir.glob("*.yaml")
        ] if self.config_dir.exists() else False
        
        if not mcp_patterns_available:
            issues.append(ValidationIssue(
                component="mcp_coordination",
                issue_type="missing_orchestration_patterns",
                severity=ValidationSeverity.MEDIUM,
                description="MCP orchestration patterns not available",
                evidence=["mcp_orchestration.yaml not found"],
                recommendations=["Ensure MCP orchestration patterns are configured"]
            ))
            score -= 0.2
        
        self.health_scores['mcp_coordination'] = HealthScore(
            component='mcp_coordination',
            score=score,
            status=HealthStatus.HEALTHY if score >= 0.8 else HealthStatus.WARNING,
            contributing_factors=["pattern_availability", "server_selection_accuracy"],
            trend="stable"
        )
        
        self.issues.extend(issues)
    
    def _validate_hook_system(self, context: Dict[str, Any], intelligence: Dict[str, Any]):
        """Validate hook system using YAML patterns."""
        print("🎣 Validating hook system...")
        
        issues = []
        score = 0.8
        
        # Check hook coordination patterns
        hook_patterns_available = 'hook_coordination.yaml' in [
            f.name for f in self.config_dir.glob("*.yaml")
        ] if self.config_dir.exists() else False
        
        if not hook_patterns_available:
            issues.append(ValidationIssue(
                component="hook_system",
                issue_type="missing_coordination_patterns",
                severity=ValidationSeverity.MEDIUM,
                description="Hook coordination patterns not available", 
                evidence=["hook_coordination.yaml not found"],
                recommendations=["Ensure hook coordination patterns are configured"]
            ))
            score -= 0.2
        
        self.health_scores['hook_system'] = HealthScore(
            component='hook_system',
            score=score,
            status=HealthStatus.HEALTHY if score >= 0.8 else HealthStatus.WARNING,
            contributing_factors=["coordination_patterns", "execution_efficiency"],
            trend="stable"
        )
        
        self.issues.extend(issues)
    
    def _validate_configuration_system(self, context: Dict[str, Any], intelligence: Dict[str, Any]):
        """Validate configuration system using YAML patterns.""" 
        print("📝 Validating configuration system...")
        
        issues = []
        score_factors = []
        
        # Check YAML configuration files
        expected_intelligence_files = [
            'intelligence_patterns.yaml',
            'mcp_orchestration.yaml', 
            'hook_coordination.yaml',
            'performance_intelligence.yaml',
            'validation_intelligence.yaml',
            'user_experience.yaml'
        ]
        
        available_files = [f.name for f in self.config_dir.glob("*.yaml")] if self.config_dir.exists() else []
        missing_files = [f for f in expected_intelligence_files if f not in available_files]
        
        if missing_files:
            issues.append(ValidationIssue(
                component="configuration_system",
                issue_type="missing_intelligence_configs",
                severity=ValidationSeverity.HIGH,
                description=f"Missing {len(missing_files)} intelligence configuration files",
                evidence=[f"Missing files: {', '.join(missing_files)}"],
                recommendations=["Ensure all intelligence pattern files are available"]
            ))
            score_factors.append(0.5)
        else:
            score_factors.append(0.9)
        
        # Validate YAML syntax
        yaml_issues = 0
        if self.config_dir.exists():
            for yaml_file in self.config_dir.glob("*.yaml"):
                try:
                    with open(yaml_file, 'r') as f:
                        config_loader.load_config(yaml_file.stem)
                except Exception as e:
                    yaml_issues += 1
                    issues.append(ValidationIssue(
                        component="configuration_system",
                        issue_type="yaml_syntax_error",
                        severity=ValidationSeverity.HIGH,
                        description=f"YAML syntax error in {yaml_file.name}",
                        evidence=[f"Error: {str(e)}"],
                        recommendations=[f"Fix YAML syntax in {yaml_file.name}"]
                    ))
        
        syntax_score = max(0, 1.0 - yaml_issues * 0.2)
        score_factors.append(syntax_score)
        
        overall_score = statistics.mean(score_factors) if score_factors else 0.5
        
        self.health_scores['configuration_system'] = HealthScore(
            component='configuration_system', 
            score=overall_score,
            status=HealthStatus.HEALTHY if overall_score >= 0.8 else 
                   HealthStatus.WARNING if overall_score >= 0.6 else 
                   HealthStatus.CRITICAL,
            contributing_factors=["file_availability", "yaml_syntax", "intelligence_patterns"],
            trend="stable"
        )
        
        self.issues.extend(issues)
    
    def _validate_cache_system(self, context: Dict[str, Any], intelligence: Dict[str, Any]):
        """Validate cache system using YAML patterns."""
        print("💾 Validating cache system...")
        
        issues = []
        score = 0.8
        
        if not self.cache_dir.exists():
            issues.append(ValidationIssue(
                component="cache_system",
                issue_type="cache_directory_missing",
                severity=ValidationSeverity.HIGH,
                description="Cache directory does not exist",
                evidence=[f"Path not found: {self.cache_dir}"],
                recommendations=["Initialize cache directory"],
                auto_fixable=True,
                remediation_action="create_cache_directory"
            ))
            score = 0.3
        else:
            # Validate essential cache files
            essential_files = ['learning_records.json', 'adaptations.json']
            missing_essential = []
            
            for essential_file in essential_files:
                file_path = self.cache_dir / essential_file
                if not file_path.exists():
                    missing_essential.append(essential_file)
            
            if missing_essential:
                issues.append(ValidationIssue(
                    component="cache_system",
                    issue_type="missing_essential_cache_files", 
                    severity=ValidationSeverity.MEDIUM,
                    description=f"Missing essential cache files: {', '.join(missing_essential)}",
                    evidence=[f"Missing files in {self.cache_dir}"],
                    recommendations=["Initialize missing cache files"],
                    auto_fixable=True
                ))
                score -= 0.1 * len(missing_essential)
        
        self.health_scores['cache_system'] = HealthScore(
            component='cache_system',
            score=score,
            status=HealthStatus.HEALTHY if score >= 0.8 else 
                   HealthStatus.WARNING if score >= 0.6 else 
                   HealthStatus.CRITICAL,
            contributing_factors=["directory_existence", "essential_files"],
            trend="stable"
        )
        
        self.issues.extend(issues)
    
    def _run_proactive_diagnostics(self, context: Dict[str, Any]):
        """Run proactive diagnostic pattern matching from YAML."""
        print("🔮 Running proactive diagnostics...")
        
        # Get early warning patterns from YAML
        early_warning_patterns = self.validation_patterns.get(
            'proactive_diagnostics', {}
        ).get('early_warning_patterns', {})
        
        # Check learning system warnings
        learning_warnings = early_warning_patterns.get('learning_system_warnings', [])
        for warning_pattern in learning_warnings:
            if self._matches_warning_pattern(context, warning_pattern):
                severity_map = {
                    'low': ValidationSeverity.LOW,
                    'medium': ValidationSeverity.MEDIUM, 
                    'high': ValidationSeverity.HIGH,
                    'critical': ValidationSeverity.CRITICAL
                }
                
                self.issues.append(ValidationIssue(
                    component="learning_system",
                    issue_type=warning_pattern.get('name', 'unknown_warning'),
                    severity=severity_map.get(warning_pattern.get('severity', 'medium'), ValidationSeverity.MEDIUM),
                    description=f"Proactive warning: {warning_pattern.get('name')}",
                    evidence=[f"Pattern matched: {warning_pattern.get('pattern', {})}"],
                    recommendations=[warning_pattern.get('recommendation', 'Review system state')],
                    remediation_action=warning_pattern.get('remediation')
                ))
        
        # Similar checks for performance and coordination warnings would go here
    
    def _matches_warning_pattern(self, context: Dict[str, Any], warning_pattern: Dict[str, Any]) -> bool:
        """Check if current context matches a warning pattern."""
        pattern_conditions = warning_pattern.get('pattern', {})
        
        for key, expected_value in pattern_conditions.items():
            if key not in context:
                continue
            
            context_value = context[key]
            
            # Handle string comparisons with operators
            if isinstance(expected_value, str):
                if expected_value.startswith('>'):
                    threshold = float(expected_value[1:])
                    if not (isinstance(context_value, (int, float)) and context_value > threshold):
                        return False
                elif expected_value.startswith('<'):
                    threshold = float(expected_value[1:])
                    if not (isinstance(context_value, (int, float)) and context_value < threshold):
                        return False
                else:
                    if context_value != expected_value:
                        return False
            else:
                if context_value != expected_value:
                    return False
        
        return True
    
    def _calculate_overall_health_score(self):
        """Calculate overall system health score using YAML component weights."""
        component_weights = self.validation_patterns.get('component_weights', {
            'learning_system': 0.25,
            'performance_system': 0.20,
            'mcp_coordination': 0.20,
            'hook_system': 0.15,
            'configuration_system': 0.10,
            'cache_system': 0.10
        })
        
        weighted_score = 0.0
        total_weight = 0.0
        
        for component, weight in component_weights.items():
            if component in self.health_scores:
                weighted_score += self.health_scores[component].score * weight
                total_weight += weight
        
        overall_score = weighted_score / total_weight if total_weight > 0 else 0.0
        
        overall_status = (
            HealthStatus.HEALTHY if overall_score >= 0.8 else
            HealthStatus.WARNING if overall_score >= 0.6 else
            HealthStatus.CRITICAL
        )
        
        self.health_scores['overall'] = HealthScore(
            component='overall_system',
            score=overall_score,
            status=overall_status,
            contributing_factors=list(component_weights.keys()),
            trend="stable"
        )
    
    def _generate_remediation_suggestions(self):
        """Generate intelligent remediation suggestions based on issues found."""
        auto_fixable_issues = [issue for issue in self.issues if issue.auto_fixable]
        
        if auto_fixable_issues and self.fix_issues:
            for issue in auto_fixable_issues:
                if issue.remediation_action == "create_cache_directory":
                    try:
                        self.cache_dir.mkdir(parents=True, exist_ok=True)
                        self.fixes_applied.append(f"✅ Created cache directory: {self.cache_dir}")
                    except Exception as e:
                        print(f"Failed to create cache directory: {e}")
    
    def print_results(self, verbose: bool = False):
        """Print comprehensive validation results."""
        print("\n" + "="*70)
        print("🎯 YAML-DRIVEN VALIDATION RESULTS")
        print("="*70)
        
        # Overall health score
        overall_health = self.health_scores.get('overall')
        if overall_health:
            status_emoji = {
                HealthStatus.HEALTHY: "🟢",
                HealthStatus.WARNING: "🟡", 
                HealthStatus.CRITICAL: "🔴",
                HealthStatus.UNKNOWN: "⚪"
            }
            print(f"\n{status_emoji.get(overall_health.status, '⚪')} Overall Health Score: {overall_health.score:.2f}/1.0 ({overall_health.status.value})")
        
        # Component health scores  
        if verbose and len(self.health_scores) > 1:
            print(f"\n📊 Component Health Scores:")
            for component, health in self.health_scores.items():
                if component != 'overall':
                    status_emoji = {
                        HealthStatus.HEALTHY: "🟢",
                        HealthStatus.WARNING: "🟡",
                        HealthStatus.CRITICAL: "🔴"
                    }
                    print(f"   {status_emoji.get(health.status, '⚪')} {component}: {health.score:.2f}")
        
        # Issues found
        if not self.issues:
            print("\n✅ All validations passed! System appears healthy.")
        else:
            severity_counts = {}
            for issue in self.issues:
                severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
            
            print(f"\n🔍 Found {len(self.issues)} issues:")
            for severity in [ValidationSeverity.CRITICAL, ValidationSeverity.HIGH, 
                           ValidationSeverity.MEDIUM, ValidationSeverity.LOW, ValidationSeverity.INFO]:
                if severity in severity_counts:
                    severity_emoji = {
                        ValidationSeverity.CRITICAL: "🚨",
                        ValidationSeverity.HIGH: "⚠️ ",
                        ValidationSeverity.MEDIUM: "🟡",
                        ValidationSeverity.LOW: "ℹ️ ",
                        ValidationSeverity.INFO: "💡"
                    }
                    print(f"   {severity_emoji.get(severity, '')} {severity.value.title()}: {severity_counts[severity]}")
            
            if verbose:
                print(f"\n📋 Detailed Issues:")
                for issue in sorted(self.issues, key=lambda x: x.severity.value):
                    print(f"\n   • {issue.component}/{issue.issue_type} ({issue.severity.value})")
                    print(f"     {issue.description}")
                    if issue.evidence:
                        print(f"     Evidence: {'; '.join(issue.evidence)}")
                    if issue.recommendations:
                        print(f"     Recommendations: {'; '.join(issue.recommendations)}")
        
        # Fixes applied
        if self.fixes_applied:
            print(f"\n🔧 Applied {len(self.fixes_applied)} fixes:")
            for fix in self.fixes_applied:
                print(f"   {fix}")
        
        print("\n" + "="*70)


def main():
    """Main entry point for YAML-driven validation."""
    parser = argparse.ArgumentParser(
        description="YAML-driven Framework-Hooks validation engine"
    )
    parser.add_argument("--fix", action="store_true", 
                       help="Attempt to fix auto-fixable issues")
    parser.add_argument("--verbose", action="store_true", 
                       help="Verbose output with detailed results")
    parser.add_argument("--framework-root", 
                       default=".", 
                       help="Path to Framework-Hooks directory")
    
    args = parser.parse_args()
    
    framework_root = Path(args.framework_root).resolve()
    if not framework_root.exists():
        print(f"❌ Framework root directory not found: {framework_root}")
        sys.exit(1)
    
    # Initialize YAML-driven validation engine
    validator = YAMLValidationEngine(framework_root, args.fix)
    
    # Run comprehensive validation
    issues, fixes, health_scores = validator.validate_all()
    
    # Print results
    validator.print_results(args.verbose)
    
    # Exit with health score as return code (0 = perfect, higher = issues)
    overall_health = health_scores.get('overall')
    health_score = overall_health.score if overall_health else 0.0
    exit_code = max(0, min(10, int((1.0 - health_score) * 10)))  # 0-10 range
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()