#!/usr/bin/env python3
"""
SuperClaude-Lite Pre-Compact Hook

Implements MODE_Token_Efficiency.md compression algorithms for intelligent context optimization.
Performance target: <150ms execution time.

This hook runs before context compaction and provides:
- Intelligent compression strategy selection
- Selective content preservation with framework exclusion
- Symbol systems and abbreviation optimization
- Quality-gated compression with ≥95% information preservation
- Adaptive compression based on resource constraints
"""

import sys
import json
import time
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Add shared modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "shared"))

from framework_logic import FrameworkLogic
from pattern_detection import PatternDetector
from mcp_intelligence import MCPIntelligence
from compression_engine import (
    CompressionEngine, CompressionLevel, ContentType, CompressionResult, CompressionStrategy
)
from learning_engine import LearningEngine, LearningType, AdaptationScope
from yaml_loader import config_loader
from logger import log_hook_start, log_hook_end, log_decision, log_error


class PreCompactHook:
    """
    Pre-compact hook implementing SuperClaude token efficiency intelligence.
    
    Responsibilities:
    - Analyze context for compression opportunities
    - Apply selective compression with framework protection
    - Implement symbol systems and abbreviation optimization
    - Maintain ≥95% information preservation quality
    - Adapt compression strategy based on resource constraints
    - Learn from compression effectiveness and user preferences
    """
    
    def __init__(self):
        start_time = time.time()
        
        # Initialize core components
        self.framework_logic = FrameworkLogic()
        self.pattern_detector = PatternDetector()
        self.mcp_intelligence = MCPIntelligence()
        self.compression_engine = CompressionEngine()
        
        # Initialize learning engine
        cache_dir = Path("cache")
        self.learning_engine = LearningEngine(cache_dir)
        
        # Load hook-specific configuration from SuperClaude config
        self.hook_config = config_loader.get_hook_config('pre_compact')
        
        # Load compression configuration (from YAML if exists, otherwise use hook config)
        try:
            self.compression_config = config_loader.load_config('compression')
        except FileNotFoundError:
            # Fall back to hook configuration if YAML file not found
            self.compression_config = self.hook_config.get('configuration', {})
        
        # Performance tracking using configuration
        self.initialization_time = (time.time() - start_time) * 1000
        self.performance_target_ms = config_loader.get_hook_config('pre_compact', 'performance_target_ms', 150)
        
    def process_pre_compact(self, compact_request: dict) -> dict:
        """
        Process pre-compact request with intelligent compression.
        
        Args:
            compact_request: Context compaction request from Claude Code
            
        Returns:
            Compression configuration and optimized content strategy
        """
        start_time = time.time()
        
        # Log hook start
        log_hook_start("pre_compact", {
            "session_id": compact_request.get('session_id', ''),
            "content_size": len(compact_request.get('content', '')),
            "resource_state": compact_request.get('resource_state', {}),
            "triggers": compact_request.get('triggers', [])
        })
        
        try:
            # Extract compression context
            context = self._extract_compression_context(compact_request)
            
            # Analyze content for compression strategy
            content_analysis = self._analyze_content_for_compression(context)
            
            # Determine optimal compression strategy
            compression_strategy = self._determine_compression_strategy(context, content_analysis)
            
            # Log compression strategy decision
            log_decision(
                "pre_compact",
                "compression_strategy",
                compression_strategy.level.value,
                f"Based on resource usage: {context.get('token_usage_percent', 0)}%, content type: {content_analysis['content_type'].value}"
            )
            
            # Apply selective compression with framework protection
            compression_results = self._apply_selective_compression(
                context, compression_strategy, content_analysis
            )
            
            # Validate compression quality
            quality_validation = self._validate_compression_quality(
                compression_results, compression_strategy
            )
            
            # Log quality validation results
            if not quality_validation['overall_quality_met']:
                log_decision(
                    "pre_compact",
                    "quality_validation",
                    "failed",
                    f"Preservation score: {quality_validation['preservation_score']:.2f}, Issues: {', '.join(quality_validation['quality_issues'])}"
                )
            
            # Record learning events
            self._record_compression_learning(context, compression_results, quality_validation)
            
            # Generate compression configuration
            compression_config = self._generate_compression_config(
                context, compression_strategy, compression_results, quality_validation
            )
            
            # Performance tracking
            execution_time = (time.time() - start_time) * 1000
            compression_config['performance_metrics'] = {
                'compression_time_ms': execution_time,
                'target_met': execution_time < self.performance_target_ms,
                'efficiency_score': self._calculate_compression_efficiency(context, execution_time)
            }
            
            # Log compression results
            log_decision(
                "pre_compact",
                "compression_results",
                f"{compression_config['results']['compression_ratio']:.1%}",
                f"Saved {compression_config['optimization']['estimated_token_savings']} tokens"
            )
            
            # Log hook end
            log_hook_end(
                "pre_compact",
                int(execution_time),
                True,
                {
                    "compression_ratio": compression_config['results']['compression_ratio'],
                    "preservation_score": compression_config['quality']['preservation_score'],
                    "token_savings": compression_config['optimization']['estimated_token_savings'],
                    "performance_target_met": execution_time < self.performance_target_ms
                }
            )
            
            return compression_config
            
        except Exception as e:
            # Log error
            log_error("pre_compact", str(e), {"request": compact_request})
            
            # Log hook end with failure
            log_hook_end("pre_compact", int((time.time() - start_time) * 1000), False)
            
            # Graceful fallback on error
            return self._create_fallback_compression_config(compact_request, str(e))
    
    def _extract_compression_context(self, compact_request: dict) -> dict:
        """Extract and enrich compression context."""
        context = {
            'session_id': compact_request.get('session_id', ''),
            'content_to_compress': compact_request.get('content', ''),
            'content_metadata': compact_request.get('metadata', {}),
            'resource_constraints': compact_request.get('resource_state', {}),
            'user_preferences': compact_request.get('user_preferences', {}),
            'compression_triggers': compact_request.get('triggers', []),
            'previous_compressions': compact_request.get('compression_history', []),
            'session_context': compact_request.get('session_context', {}),
            'timestamp': time.time()
        }
        
        # Analyze content characteristics
        context.update(self._analyze_content_characteristics(context))
        
        # Extract resource state
        context.update(self._extract_resource_state(context))
        
        return context
    
    def _analyze_content_characteristics(self, context: dict) -> dict:
        """Analyze content characteristics for compression decisions."""
        content = context.get('content_to_compress', '')
        metadata = context.get('content_metadata', {})
        
        characteristics = {
            'content_length': len(content),
            'content_complexity': 0.0,
            'repetition_factor': 0.0,
            'technical_density': 0.0,
            'framework_content_ratio': 0.0,
            'user_content_ratio': 0.0,
            'compressibility_score': 0.0
        }
        
        if not content:
            return characteristics
        
        # Content complexity analysis
        lines = content.split('\n')
        characteristics['content_complexity'] = self._calculate_content_complexity(content, lines)
        
        # Repetition analysis
        characteristics['repetition_factor'] = self._calculate_repetition_factor(content, lines)
        
        # Technical density
        characteristics['technical_density'] = self._calculate_technical_density(content)
        
        # Framework vs user content ratio
        framework_ratio, user_ratio = self._analyze_content_sources(content, metadata)
        characteristics['framework_content_ratio'] = framework_ratio
        characteristics['user_content_ratio'] = user_ratio
        
        # Overall compressibility score
        characteristics['compressibility_score'] = self._calculate_compressibility_score(characteristics)
        
        return characteristics
    
    def _calculate_content_complexity(self, content: str, lines: List[str]) -> float:
        """Calculate content complexity score (0.0 to 1.0)."""
        complexity_indicators = [
            len([line for line in lines if len(line) > 100]) / max(len(lines), 1),  # Long lines
            len([char for char in content if char in '{}[]()']) / max(len(content), 1),  # Structural chars
            len(set(content.split())) / max(len(content.split()), 1),  # Vocabulary richness
        ]
        
        return min(sum(complexity_indicators) / len(complexity_indicators), 1.0)
    
    def _calculate_repetition_factor(self, content: str, lines: List[str]) -> float:
        """Calculate repetition factor for compression potential."""
        if not lines:
            return 0.0
        
        # Line repetition
        unique_lines = len(set(lines))
        line_repetition = 1.0 - (unique_lines / len(lines))
        
        # Word repetition
        words = content.split()
        if words:
            unique_words = len(set(words))
            word_repetition = 1.0 - (unique_words / len(words))
        else:
            word_repetition = 0.0
        
        return (line_repetition + word_repetition) / 2
    
    def _calculate_technical_density(self, content: str) -> float:
        """Calculate technical density for compression strategy."""
        technical_patterns = [
            r'\b[A-Z][a-zA-Z]*\b',  # CamelCase
            r'\b\w+\.\w+\b',        # Dotted notation
            r'\b\d+\.\d+\.\d+\b',   # Version numbers
            r'\b[a-z]+_[a-z]+\b',   # Snake_case
            r'\b[A-Z]{2,}\b',       # CONSTANTS
        ]
        
        import re
        technical_matches = 0
        for pattern in technical_patterns:
            technical_matches += len(re.findall(pattern, content))
        
        total_words = len(content.split())
        return min(technical_matches / max(total_words, 1), 1.0)
    
    def _analyze_content_sources(self, content: str, metadata: dict) -> Tuple[float, float]:
        """Analyze ratio of framework vs user content."""
        # Framework content indicators
        framework_indicators = [
            'SuperClaude', 'CLAUDE.md', 'FLAGS.md', 'PRINCIPLES.md',
            'ORCHESTRATOR.md', 'MCP_', 'MODE_', 'SESSION_LIFECYCLE'
        ]
        
        # User content indicators
        user_indicators = [
            'project_files', 'user_documentation', 'source_code',
            'configuration_files', 'custom_content'
        ]
        
        framework_score = 0
        user_score = 0
        
        # Check content text
        content_lower = content.lower()
        for indicator in framework_indicators:
            if indicator.lower() in content_lower:
                framework_score += 1
        
        for indicator in user_indicators:
            if indicator.lower() in content_lower:
                user_score += 1
        
        # Check metadata
        content_type = metadata.get('content_type', '')
        file_path = metadata.get('file_path', '')
        
        if any(pattern in file_path for pattern in ['/SuperClaude/', '/.claude/', 'framework']):
            framework_score += 3
        
        if any(pattern in content_type for pattern in user_indicators):
            user_score += 3
        
        total_score = framework_score + user_score
        if total_score == 0:
            return 0.5, 0.5  # Unknown, assume mixed
        
        return framework_score / total_score, user_score / total_score
    
    def _calculate_compressibility_score(self, characteristics: dict) -> float:
        """Calculate overall compressibility score."""
        # Higher repetition = higher compressibility
        repetition_contribution = characteristics['repetition_factor'] * 0.4
        
        # Higher technical density = better compression with abbreviations
        technical_contribution = characteristics['technical_density'] * 0.3
        
        # Framework content is not compressed (exclusion)
        framework_penalty = characteristics['framework_content_ratio'] * 0.5
        
        # Content complexity affects compression effectiveness
        complexity_factor = 1.0 - (characteristics['content_complexity'] * 0.2)
        
        score = (repetition_contribution + technical_contribution) * complexity_factor - framework_penalty
        
        return max(min(score, 1.0), 0.0)
    
    def _extract_resource_state(self, context: dict) -> dict:
        """Extract resource state for compression decisions."""
        resource_constraints = context.get('resource_constraints', {})
        
        return {
            'memory_usage_percent': resource_constraints.get('memory_usage', 0),
            'token_usage_percent': resource_constraints.get('token_usage', 0),
            'conversation_length': resource_constraints.get('conversation_length', 0),
            'resource_pressure': resource_constraints.get('pressure_level', 'normal'),
            'user_requests_compression': resource_constraints.get('user_compression_request', False)
        }
    
    def _analyze_content_for_compression(self, context: dict) -> dict:
        """Analyze content to determine compression approach."""
        content = context.get('content_to_compress', '')
        metadata = context.get('content_metadata', {})
        
        # Classify content type
        content_type = self.compression_engine.classify_content(content, metadata)
        
        # Analyze compression opportunities
        analysis = {
            'content_type': content_type,
            'compression_opportunities': [],
            'preservation_requirements': [],
            'optimization_techniques': []
        }
        
        # Framework content - complete exclusion
        if content_type == ContentType.FRAMEWORK_CONTENT:
            analysis['preservation_requirements'].append('complete_exclusion')
            analysis['compression_opportunities'] = []
            log_decision(
                "pre_compact",
                "content_classification",
                "framework_content",
                "Complete exclusion from compression - framework protection"
            )
            return analysis
        
        # User content - minimal compression only
        if content_type == ContentType.USER_CONTENT:
            analysis['preservation_requirements'].extend([
                'high_fidelity_preservation',
                'minimal_compression_only'
            ])
            analysis['compression_opportunities'].append('whitespace_optimization')
            log_decision(
                "pre_compact",
                "content_classification",
                "user_content",
                "Minimal compression only - user content preservation"
            )
            return analysis
        
        # Session/working data - full compression applicable
        compressibility = context.get('compressibility_score', 0.0)
        
        if compressibility > 0.7:
            analysis['compression_opportunities'].extend([
                'symbol_systems',
                'abbreviation_systems',
                'structural_optimization',
                'redundancy_removal'
            ])
        elif compressibility > 0.4:
            analysis['compression_opportunities'].extend([
                'symbol_systems',
                'structural_optimization'
            ])
        else:
            analysis['compression_opportunities'].append('minimal_optimization')
        
        # Technical content optimization
        if context.get('technical_density', 0) > 0.6:
            analysis['optimization_techniques'].append('technical_abbreviations')
        
        # Repetitive content optimization
        if context.get('repetition_factor', 0) > 0.5:
            analysis['optimization_techniques'].append('pattern_compression')
        
        return analysis
    
    def _determine_compression_strategy(self, context: dict, content_analysis: dict) -> CompressionStrategy:
        """Determine optimal compression strategy."""
        # Determine compression level based on resource state
        compression_level = self.compression_engine.determine_compression_level({
            'resource_usage_percent': context.get('token_usage_percent', 0),
            'conversation_length': context.get('conversation_length', 0),
            'user_requests_brevity': context.get('user_requests_compression', False),
            'complexity_score': context.get('content_complexity', 0.0)
        })
        
        # Adjust for content type
        content_type = content_analysis['content_type']
        if content_type == ContentType.FRAMEWORK_CONTENT:
            compression_level = CompressionLevel.MINIMAL  # Actually no compression
        elif content_type == ContentType.USER_CONTENT:
            compression_level = CompressionLevel.MINIMAL
        
        # Create strategy
        strategy = self.compression_engine._create_compression_strategy(compression_level, content_type)
        
        # Customize based on content analysis
        opportunities = content_analysis.get('compression_opportunities', [])
        
        if 'symbol_systems' not in opportunities:
            strategy.symbol_systems_enabled = False
        if 'abbreviation_systems' not in opportunities:
            strategy.abbreviation_systems_enabled = False
        if 'structural_optimization' not in opportunities:
            strategy.structural_optimization = False
        
        return strategy
    
    def _apply_selective_compression(self, context: dict, strategy: CompressionStrategy, 
                                   content_analysis: dict) -> Dict[str, CompressionResult]:
        """Apply selective compression with framework protection."""
        content = context.get('content_to_compress', '')
        metadata = context.get('content_metadata', {})
        
        # Split content into sections for selective processing
        content_sections = self._split_content_into_sections(content, metadata)
        
        compression_results = {}
        
        for section_name, section_data in content_sections.items():
            section_content = section_data['content']
            section_metadata = section_data['metadata']
            
            # Apply compression to each section
            result = self.compression_engine.compress_content(
                section_content,
                context,
                section_metadata
            )
            
            compression_results[section_name] = result
        
        return compression_results
    
    def _split_content_into_sections(self, content: str, metadata: dict) -> dict:
        """Split content into sections for selective compression."""
        sections = {}
        
        # Simple splitting strategy - can be enhanced
        lines = content.split('\n')
        
        # Detect different content types within the text
        current_section = 'default'
        current_content = []
        
        for line in lines:
            # Framework content detection
            if any(indicator in line for indicator in ['SuperClaude', 'CLAUDE.md', 'FLAGS.md']):
                if current_content and current_section != 'framework':
                    sections[current_section] = {
                        'content': '\n'.join(current_content),
                        'metadata': {**metadata, 'content_type': current_section}
                    }
                    current_content = []
                current_section = 'framework'
            
            # User code detection
            elif any(indicator in line for indicator in ['def ', 'class ', 'function', 'import ']):
                if current_content and current_section != 'user_code':
                    sections[current_section] = {
                        'content': '\n'.join(current_content),
                        'metadata': {**metadata, 'content_type': current_section}
                    }
                    current_content = []
                current_section = 'user_code'
            
            # Session data detection
            elif any(indicator in line for indicator in ['session_', 'checkpoint_', 'cache_']):
                if current_content and current_section != 'session_data':
                    sections[current_section] = {
                        'content': '\n'.join(current_content),
                        'metadata': {**metadata, 'content_type': current_section}
                    }
                    current_content = []
                current_section = 'session_data'
            
            current_content.append(line)
        
        # Add final section
        if current_content:
            sections[current_section] = {
                'content': '\n'.join(current_content),
                'metadata': {**metadata, 'content_type': current_section}
            }
        
        # If no sections detected, treat as single section
        if not sections:
            sections['default'] = {
                'content': content,
                'metadata': metadata
            }
        
        return sections
    
    def _validate_compression_quality(self, compression_results: Dict[str, CompressionResult], 
                                    strategy: CompressionStrategy) -> dict:
        """Validate compression quality against standards."""
        validation = {
            'overall_quality_met': True,
            'preservation_score': 0.0,
            'compression_efficiency': 0.0,
            'quality_issues': [],
            'quality_warnings': []
        }
        
        if not compression_results:
            return validation
        
        # Calculate overall metrics
        total_original = sum(result.original_length for result in compression_results.values())
        total_compressed = sum(result.compressed_length for result in compression_results.values())
        total_preservation = sum(result.preservation_score for result in compression_results.values())
        
        if total_original > 0:
            validation['compression_efficiency'] = (total_original - total_compressed) / total_original
        
        validation['preservation_score'] = total_preservation / len(compression_results)
        
        # Quality threshold validation
        if validation['preservation_score'] < strategy.quality_threshold:
            validation['overall_quality_met'] = False
            validation['quality_issues'].append(
                f"Preservation score {validation['preservation_score']:.2f} below threshold {strategy.quality_threshold}"
            )
        
        # Individual section validation
        for section_name, result in compression_results.items():
            if result.quality_score < 0.8:
                validation['quality_warnings'].append(
                    f"Section '{section_name}' quality score low: {result.quality_score:.2f}"
                )
            
            if result.compression_ratio > 0.9:  # Over 90% compression might be too aggressive
                validation['quality_warnings'].append(
                    f"Section '{section_name}' compression ratio very high: {result.compression_ratio:.2f}"
                )
        
        return validation
    
    def _record_compression_learning(self, context: dict, compression_results: Dict[str, CompressionResult], 
                                   quality_validation: dict):
        """Record compression learning for future optimization."""
        overall_effectiveness = quality_validation['preservation_score'] * quality_validation['compression_efficiency']
        
        # Record compression effectiveness
        self.learning_engine.record_learning_event(
            LearningType.PERFORMANCE_OPTIMIZATION,
            AdaptationScope.USER,
            context,
            {
                'compression_level': self.compression_engine.determine_compression_level(context).value,
                'techniques_used': list(set().union(*[result.techniques_used for result in compression_results.values()])),
                'preservation_score': quality_validation['preservation_score'],
                'compression_efficiency': quality_validation['compression_efficiency']
            },
            overall_effectiveness,
            0.9,  # High confidence in compression metrics
            {'hook': 'pre_compact', 'compression_learning': True}
        )
        
        # Record user preference if compression was requested
        if context.get('user_requests_compression'):
            self.learning_engine.record_learning_event(
                LearningType.USER_PREFERENCE,
                AdaptationScope.USER,
                context,
                {'compression_preference': 'enabled', 'user_satisfaction': overall_effectiveness},
                overall_effectiveness,
                0.8,
                {'user_initiated_compression': True}
            )
    
    def _calculate_compression_efficiency(self, context: dict, execution_time_ms: float) -> float:
        """Calculate compression processing efficiency."""
        content_length = context.get('content_length', 1)
        
        # Efficiency based on processing speed per character
        chars_per_ms = content_length / max(execution_time_ms, 1)
        
        # Target: 100 chars per ms for good efficiency
        target_chars_per_ms = 100
        efficiency = min(chars_per_ms / target_chars_per_ms, 1.0)
        
        return efficiency
    
    def _generate_compression_config(self, context: dict, strategy: CompressionStrategy, 
                                   compression_results: Dict[str, CompressionResult], 
                                   quality_validation: dict) -> dict:
        """Generate comprehensive compression configuration."""
        total_original = sum(result.original_length for result in compression_results.values())
        total_compressed = sum(result.compressed_length for result in compression_results.values())
        
        config = {
            'compression_enabled': True,
            'compression_level': strategy.level.value,
            'selective_compression': True,
            
            'strategy': {
                'symbol_systems_enabled': strategy.symbol_systems_enabled,
                'abbreviation_systems_enabled': strategy.abbreviation_systems_enabled,
                'structural_optimization': strategy.structural_optimization,
                'quality_threshold': strategy.quality_threshold
            },
            
            'results': {
                'original_length': total_original,
                'compressed_length': total_compressed,
                'compression_ratio': (total_original - total_compressed) / max(total_original, 1),
                'sections_processed': len(compression_results),
                'techniques_used': list(set().union(*[result.techniques_used for result in compression_results.values()]))
            },
            
            'quality': {
                'preservation_score': quality_validation['preservation_score'],
                'quality_met': quality_validation['overall_quality_met'],
                'issues': quality_validation['quality_issues'],
                'warnings': quality_validation['quality_warnings']
            },
            
            'framework_protection': {
                'framework_content_excluded': True,
                'user_content_preserved': True,
                'selective_processing_enabled': True
            },
            
            'optimization': {
                'estimated_token_savings': int((total_original - total_compressed) * 0.7),  # Rough estimate
                'processing_efficiency': quality_validation['compression_efficiency'],
                'recommendation': self._get_compression_recommendation(context, quality_validation)
            },
            
            'metadata': {
                'hook_version': 'pre_compact_1.0',
                'compression_timestamp': context['timestamp'],
                'content_classification': 'selective_compression_applied'
            }
        }
        
        return config
    
    def _get_compression_recommendation(self, context: dict, quality_validation: dict) -> str:
        """Get compression recommendation based on results."""
        if not quality_validation['overall_quality_met']:
            return "Reduce compression level to maintain quality"
        elif quality_validation['compression_efficiency'] > 0.7:
            return "Excellent compression efficiency achieved"
        elif quality_validation['compression_efficiency'] > 0.4:
            return "Good compression efficiency, consider slight optimization"
        else:
            return "Low compression efficiency, consider alternative strategies"
    
    def _create_fallback_compression_config(self, compact_request: dict, error: str) -> dict:
        """Create fallback compression configuration on error."""
        return {
            'compression_enabled': False,
            'fallback_mode': True,
            'error': error,
            
            'strategy': {
                'symbol_systems_enabled': False,
                'abbreviation_systems_enabled': False,
                'structural_optimization': False,
                'quality_threshold': 1.0
            },
            
            'results': {
                'original_length': len(compact_request.get('content', '')),
                'compressed_length': len(compact_request.get('content', '')),
                'compression_ratio': 0.0,
                'sections_processed': 0,
                'techniques_used': []
            },
            
            'quality': {
                'preservation_score': 1.0,
                'quality_met': False,
                'issues': [f"Compression hook error: {error}"],
                'warnings': []
            },
            
            'performance_metrics': {
                'compression_time_ms': 0,
                'target_met': False,
                'error_occurred': True
            }
        }


def main():
    """Main hook execution function."""
    try:
        # Read compact request from stdin
        compact_request = json.loads(sys.stdin.read())
        
        # Initialize and run hook
        hook = PreCompactHook()
        result = hook.process_pre_compact(compact_request)
        
        # Output result as JSON
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        # Output error as JSON
        error_result = {
            'compression_enabled': False,
            'error': str(e),
            'fallback_mode': True
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()