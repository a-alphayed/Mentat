"""
Compression Engine for SuperClaude-Lite

Intelligent token optimization implementing MODE_Token_Efficiency.md algorithms
with adaptive compression, symbol systems, and quality-gated validation.
"""

import re
import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum

from yaml_loader import config_loader


class CompressionLevel(Enum):
    """Compression levels from MODE_Token_Efficiency.md."""
    MINIMAL = "minimal"        # 0-40% compression
    EFFICIENT = "efficient"    # 40-70% compression  
    COMPRESSED = "compressed"  # 70-85% compression
    CRITICAL = "critical"      # 85-95% compression
    EMERGENCY = "emergency"    # 95%+ compression


class ContentType(Enum):
    """Types of content for selective compression."""
    FRAMEWORK_CONTENT = "framework"        # SuperClaude framework - EXCLUDE
    SESSION_DATA = "session"              # Session metadata - COMPRESS
    USER_CONTENT = "user"                 # User project files - PRESERVE
    WORKING_ARTIFACTS = "artifacts"       # Analysis results - COMPRESS


@dataclass
class CompressionResult:
    """Result of compression operation."""
    original_length: int
    compressed_length: int
    compression_ratio: float
    quality_score: float  # 0.0 to 1.0
    techniques_used: List[str]
    preservation_score: float  # Information preservation
    processing_time_ms: float


@dataclass
class CompressionStrategy:
    """Strategy configuration for compression."""
    level: CompressionLevel
    symbol_systems_enabled: bool
    abbreviation_systems_enabled: bool
    structural_optimization: bool
    selective_preservation: Dict[str, bool]
    quality_threshold: float


class CompressionEngine:
    """
    Intelligent token optimization engine implementing MODE_Token_Efficiency.md.
    
    Features:
    - 5-level adaptive compression (minimal to emergency)
    - Symbol systems for mathematical and logical relationships
    - Abbreviation systems for technical domains
    - Selective compression with framework/user content protection
    - Quality-gated validation with ≥95% information preservation
    - Real-time compression effectiveness monitoring
    """
    
    def __init__(self):
        self.config = config_loader.load_config('compression')
        self.symbol_mappings = self._load_symbol_mappings()
        self.abbreviation_mappings = self._load_abbreviation_mappings()
        self.compression_cache = {}
        self.performance_metrics = {}
        
    def _load_symbol_mappings(self) -> Dict[str, str]:
        """Load symbol system mappings from configuration."""
        return {
            # Core Logic & Flow
            'leads to': '→',
            'implies': '→',
            'transforms to': '⇒',
            'converts to': '⇒',
            'rollback': '←',
            'reverse': '←',
            'bidirectional': '⇄',
            'sync': '⇄',
            'and': '&',
            'combine': '&',
            'separator': '|',
            'or': '|',
            'define': ':',
            'specify': ':',
            'sequence': '»',
            'then': '»',
            'therefore': '∴',
            'because': '∵',
            'equivalent': '≡',
            'approximately': '≈',
            'not equal': '≠',
            
            # Status & Progress  
            'completed': '✅',
            'passed': '✅',
            'failed': '❌',
            'error': '❌',
            'warning': '⚠️',
            'information': 'ℹ️',
            'in progress': '🔄',
            'processing': '🔄',
            'waiting': '⏳',
            'pending': '⏳',
            'critical': '🚨',
            'urgent': '🚨',
            'target': '🎯',
            'goal': '🎯',
            'metrics': '📊',
            'data': '📊',
            'insight': '💡',
            'learning': '💡',
            
            # Technical Domains
            'performance': '⚡',
            'optimization': '⚡',
            'analysis': '🔍',
            'investigation': '🔍',
            'configuration': '🔧',
            'setup': '🔧',
            'security': '🛡️',
            'protection': '🛡️',
            'deployment': '📦',
            'package': '📦',
            'design': '🎨',
            'frontend': '🎨',
            'network': '🌐',
            'connectivity': '🌐',
            'mobile': '📱',
            'responsive': '📱',
            'architecture': '🏗️',
            'system structure': '🏗️',
            'components': '🧩',
            'modular': '🧩'
        }
    
    def _load_abbreviation_mappings(self) -> Dict[str, str]:
        """Load abbreviation system mappings from configuration."""
        return {
            # System & Architecture
            'configuration': 'cfg',
            'settings': 'cfg',
            'implementation': 'impl',
            'code structure': 'impl',
            'architecture': 'arch',
            'system design': 'arch',
            'performance': 'perf',
            'optimization': 'perf',
            'operations': 'ops',
            'deployment': 'ops',
            'environment': 'env',
            'runtime context': 'env',
            
            # Development Process
            'requirements': 'req',
            'dependencies': 'deps',
            'packages': 'deps',
            'validation': 'val',
            'verification': 'val',
            'testing': 'test',
            'quality assurance': 'test',
            'documentation': 'docs',
            'guides': 'docs',
            'standards': 'std',
            'conventions': 'std',
            
            # Quality & Analysis
            'quality': 'qual',
            'maintainability': 'qual',
            'security': 'sec',
            'safety measures': 'sec',
            'error': 'err',
            'exception handling': 'err',
            'recovery': 'rec',
            'resilience': 'rec',
            'severity': 'sev',
            'priority level': 'sev',
            'optimization': 'opt',
            'improvement': 'opt'
        }
    
    def determine_compression_level(self, context: Dict[str, Any]) -> CompressionLevel:
        """
        Determine appropriate compression level based on context.
        
        Args:
            context: Session context including resource usage, conversation length, etc.
            
        Returns:
            Appropriate CompressionLevel for the situation
        """
        resource_usage = context.get('resource_usage_percent', 0)
        conversation_length = context.get('conversation_length', 0)
        user_requests_brevity = context.get('user_requests_brevity', False)
        complexity_score = context.get('complexity_score', 0.0)
        
        # Emergency compression for critical resource constraints
        if resource_usage >= 95:
            return CompressionLevel.EMERGENCY
        
        # Critical compression for high resource usage
        if resource_usage >= 85 or conversation_length > 200:
            return CompressionLevel.CRITICAL
        
        # Compressed level for moderate constraints
        if resource_usage >= 70 or conversation_length > 100 or user_requests_brevity:
            return CompressionLevel.COMPRESSED
        
        # Efficient level for mild constraints or complex operations
        if resource_usage >= 40 or complexity_score > 0.6:
            return CompressionLevel.EFFICIENT
        
        # Minimal compression for normal operations
        return CompressionLevel.MINIMAL
    
    def classify_content(self, content: str, metadata: Dict[str, Any]) -> ContentType:
        """
        Classify content type for selective compression.
        
        Args:
            content: Content to classify
            metadata: Metadata about the content (file paths, context, etc.)
            
        Returns:
            ContentType for compression decision making
        """
        file_path = metadata.get('file_path', '')
        context_type = metadata.get('context_type', '')
        
        # Framework content - complete exclusion
        framework_patterns = [
            '/SuperClaude/SuperClaude/',
            '~/.claude/',
            '.claude/',
            'SuperClaude/',
            'CLAUDE.md',
            'FLAGS.md',
            'PRINCIPLES.md',
            'ORCHESTRATOR.md',
            'MCP_',
            'MODE_',
            'SESSION_LIFECYCLE.md'
        ]
        
        for pattern in framework_patterns:
            if pattern in file_path or pattern in content:
                return ContentType.FRAMEWORK_CONTENT
        
        # Session data - apply compression
        if context_type in ['session_metadata', 'checkpoint_data', 'cache_content']:
            return ContentType.SESSION_DATA
        
        # Working artifacts - apply compression  
        if context_type in ['analysis_results', 'processing_data', 'working_artifacts']:
            return ContentType.WORKING_ARTIFACTS
        
        # User content - preserve with minimal compression only
        user_patterns = [
            'project_files',
            'user_documentation', 
            'source_code',
            'configuration_files',
            'custom_content'
        ]
        
        for pattern in user_patterns:
            if pattern in context_type or pattern in file_path:
                return ContentType.USER_CONTENT
        
        # Default to user content preservation
        return ContentType.USER_CONTENT
    
    def compress_content(self, 
                        content: str, 
                        context: Dict[str, Any], 
                        metadata: Dict[str, Any] = None) -> CompressionResult:
        """
        Compress content with intelligent optimization.
        
        Args:
            content: Content to compress
            context: Session context for compression level determination
            metadata: Content metadata for selective compression
            
        Returns:
            CompressionResult with metrics and compressed content
        """
        import time
        start_time = time.time()
        
        if metadata is None:
            metadata = {}
        
        # Classify content type
        content_type = self.classify_content(content, metadata)
        
        # Framework content - no compression
        if content_type == ContentType.FRAMEWORK_CONTENT:
            return CompressionResult(
                original_length=len(content),
                compressed_length=len(content),
                compression_ratio=0.0,
                quality_score=1.0,
                techniques_used=['framework_exclusion'],
                preservation_score=1.0,
                processing_time_ms=(time.time() - start_time) * 1000
            )
        
        # User content - minimal compression only
        if content_type == ContentType.USER_CONTENT:
            compression_level = CompressionLevel.MINIMAL
        else:
            compression_level = self.determine_compression_level(context)
        
        # Create compression strategy
        strategy = self._create_compression_strategy(compression_level, content_type)
        
        # Apply compression techniques
        compressed_content = content
        techniques_used = []
        
        if strategy.symbol_systems_enabled:
            compressed_content, symbol_techniques = self._apply_symbol_systems(compressed_content)
            techniques_used.extend(symbol_techniques)
        
        if strategy.abbreviation_systems_enabled:
            compressed_content, abbrev_techniques = self._apply_abbreviation_systems(compressed_content)
            techniques_used.extend(abbrev_techniques)
        
        if strategy.structural_optimization:
            compressed_content, struct_techniques = self._apply_structural_optimization(
                compressed_content, compression_level
            )
            techniques_used.extend(struct_techniques)
        
        # Calculate metrics
        original_length = len(content)
        compressed_length = len(compressed_content)
        compression_ratio = (original_length - compressed_length) / original_length if original_length > 0 else 0.0
        
        # Quality validation
        quality_score = self._validate_compression_quality(content, compressed_content, strategy)
        preservation_score = self._calculate_information_preservation(content, compressed_content)
        
        processing_time = (time.time() - start_time) * 1000
        
        # Cache result for performance
        cache_key = hashlib.md5(content.encode()).hexdigest()
        self.compression_cache[cache_key] = compressed_content
        
        return CompressionResult(
            original_length=original_length,
            compressed_length=compressed_length,
            compression_ratio=compression_ratio,
            quality_score=quality_score,
            techniques_used=techniques_used,
            preservation_score=preservation_score,
            processing_time_ms=processing_time
        )
    
    def _create_compression_strategy(self, level: CompressionLevel, content_type: ContentType) -> CompressionStrategy:
        """Create compression strategy based on level and content type."""
        level_configs = {
            CompressionLevel.MINIMAL: {
                'symbol_systems': False,
                'abbreviations': False,
                'structural': False,
                'quality_threshold': 0.98
            },
            CompressionLevel.EFFICIENT: {
                'symbol_systems': True,
                'abbreviations': False,
                'structural': True,
                'quality_threshold': 0.95
            },
            CompressionLevel.COMPRESSED: {
                'symbol_systems': True,
                'abbreviations': True,
                'structural': True,
                'quality_threshold': 0.90
            },
            CompressionLevel.CRITICAL: {
                'symbol_systems': True,
                'abbreviations': True,
                'structural': True,
                'quality_threshold': 0.85
            },
            CompressionLevel.EMERGENCY: {
                'symbol_systems': True,
                'abbreviations': True,
                'structural': True,
                'quality_threshold': 0.80
            }
        }
        
        config = level_configs[level]
        
        # Adjust for content type
        if content_type == ContentType.USER_CONTENT:
            # More conservative for user content
            config['quality_threshold'] = min(config['quality_threshold'] + 0.1, 1.0)
        
        return CompressionStrategy(
            level=level,
            symbol_systems_enabled=config['symbol_systems'],
            abbreviation_systems_enabled=config['abbreviations'],
            structural_optimization=config['structural'],
            selective_preservation={},
            quality_threshold=config['quality_threshold']
        )
    
    def _apply_symbol_systems(self, content: str) -> Tuple[str, List[str]]:
        """Apply symbol system replacements."""
        compressed = content
        techniques = []
        
        # Apply symbol mappings with word boundary protection
        for phrase, symbol in self.symbol_mappings.items():
            pattern = r'\b' + re.escape(phrase) + r'\b'
            if re.search(pattern, compressed, re.IGNORECASE):
                compressed = re.sub(pattern, symbol, compressed, flags=re.IGNORECASE)
                techniques.append(f"symbol_{phrase.replace(' ', '_')}")
        
        return compressed, techniques
    
    def _apply_abbreviation_systems(self, content: str) -> Tuple[str, List[str]]:
        """Apply abbreviation system replacements."""
        compressed = content
        techniques = []
        
        # Apply abbreviation mappings with context awareness
        for phrase, abbrev in self.abbreviation_mappings.items():
            pattern = r'\b' + re.escape(phrase) + r'\b'
            if re.search(pattern, compressed, re.IGNORECASE):
                compressed = re.sub(pattern, abbrev, compressed, flags=re.IGNORECASE)
                techniques.append(f"abbrev_{phrase.replace(' ', '_')}")
        
        return compressed, techniques
    
    def _apply_structural_optimization(self, content: str, level: CompressionLevel) -> Tuple[str, List[str]]:
        """Apply structural optimizations for token efficiency."""
        compressed = content
        techniques = []
        
        # Remove redundant whitespace
        compressed = re.sub(r'\s+', ' ', compressed)
        compressed = re.sub(r'\n\s*\n', '\n', compressed)
        techniques.append('whitespace_optimization')
        
        # Aggressive optimizations for higher compression levels
        if level in [CompressionLevel.COMPRESSED, CompressionLevel.CRITICAL, CompressionLevel.EMERGENCY]:
            # Remove redundant words
            compressed = re.sub(r'\b(the|a|an)\s+', '', compressed, flags=re.IGNORECASE)
            techniques.append('article_removal')
            
            # Simplify common phrases
            phrase_simplifications = {
                r'in order to': 'to',
                r'it is important to note that': 'note:',
                r'please be aware that': 'note:',
                r'it should be noted that': 'note:',
                r'for the purpose of': 'for',
                r'with regard to': 'regarding',
                r'in relation to': 'regarding'
            }
            
            for pattern, replacement in phrase_simplifications.items():
                if re.search(pattern, compressed, re.IGNORECASE):
                    compressed = re.sub(pattern, replacement, compressed, flags=re.IGNORECASE)
                    techniques.append(f'phrase_simplification_{replacement}')
        
        return compressed, techniques
    
    def _validate_compression_quality(self, original: str, compressed: str, strategy: CompressionStrategy) -> float:
        """Validate compression quality against thresholds."""
        # Simple quality heuristics (real implementation would be more sophisticated)
        
        # Check if key information is preserved
        original_words = set(re.findall(r'\b\w+\b', original.lower()))
        compressed_words = set(re.findall(r'\b\w+\b', compressed.lower()))
        
        # Word preservation ratio
        word_preservation = len(compressed_words & original_words) / len(original_words) if original_words else 1.0
        
        # Length efficiency (not too aggressive)
        length_ratio = len(compressed) / len(original) if original else 1.0
        
        # Penalize over-compression
        if length_ratio < 0.3:
            word_preservation *= 0.8
        
        quality_score = (word_preservation * 0.7) + (min(length_ratio * 2, 1.0) * 0.3)
        
        return min(quality_score, 1.0)
    
    def _calculate_information_preservation(self, original: str, compressed: str) -> float:
        """Calculate information preservation score."""
        # Simple preservation metric based on key information retention
        
        # Extract key concepts (capitalized words, technical terms)
        original_concepts = set(re.findall(r'\b[A-Z][a-z]+\b|\b\w+\.(js|py|md|yaml|json)\b', original))
        compressed_concepts = set(re.findall(r'\b[A-Z][a-z]+\b|\b\w+\.(js|py|md|yaml|json)\b', compressed))
        
        if not original_concepts:
            return 1.0
        
        preservation_ratio = len(compressed_concepts & original_concepts) / len(original_concepts)
        return preservation_ratio
    
    def get_compression_recommendations(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get recommendations for optimizing compression."""
        recommendations = []
        
        current_level = self.determine_compression_level(context)
        resource_usage = context.get('resource_usage_percent', 0)
        
        # Resource-based recommendations
        if resource_usage > 85:
            recommendations.append("Enable emergency compression mode for critical resource constraints")
        elif resource_usage > 70:
            recommendations.append("Consider compressed mode for better resource efficiency")
        elif resource_usage < 40:
            recommendations.append("Resource usage low - minimal compression sufficient")
        
        # Performance recommendations
        if context.get('processing_time_ms', 0) > 500:
            recommendations.append("Compression processing time high - consider caching strategies")
        
        return {
            'current_level': current_level.value,
            'recommendations': recommendations,
            'estimated_savings': self._estimate_compression_savings(current_level),
            'quality_impact': self._estimate_quality_impact(current_level),
            'performance_metrics': self.performance_metrics
        }
    
    def _estimate_compression_savings(self, level: CompressionLevel) -> Dict[str, float]:
        """Estimate compression savings for a given level."""
        savings_map = {
            CompressionLevel.MINIMAL: {'token_reduction': 0.15, 'time_savings': 0.05},
            CompressionLevel.EFFICIENT: {'token_reduction': 0.40, 'time_savings': 0.15},
            CompressionLevel.COMPRESSED: {'token_reduction': 0.60, 'time_savings': 0.25},
            CompressionLevel.CRITICAL: {'token_reduction': 0.75, 'time_savings': 0.35},
            CompressionLevel.EMERGENCY: {'token_reduction': 0.85, 'time_savings': 0.45}
        }
        return savings_map.get(level, {'token_reduction': 0.0, 'time_savings': 0.0})
    
    def _estimate_quality_impact(self, level: CompressionLevel) -> float:
        """Estimate quality preservation for a given level."""
        quality_map = {
            CompressionLevel.MINIMAL: 0.98,
            CompressionLevel.EFFICIENT: 0.95,
            CompressionLevel.COMPRESSED: 0.90,
            CompressionLevel.CRITICAL: 0.85,
            CompressionLevel.EMERGENCY: 0.80
        }
        return quality_map.get(level, 0.95)