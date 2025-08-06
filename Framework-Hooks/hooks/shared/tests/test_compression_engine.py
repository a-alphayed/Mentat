#!/usr/bin/env python3
"""
Comprehensive tests for compression_engine.py

Tests all core functionality including:
- Token compression with symbol systems
- Content classification and selective compression
- Quality validation and preservation metrics
- Performance testing
- Edge cases and error handling
"""

import unittest
import sys
import os
import time
from pathlib import Path

# Add the shared directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from compression_engine import (
    CompressionEngine, CompressionLevel, ContentType, 
    CompressionResult, CompressionStrategy
)


class TestCompressionEngine(unittest.TestCase):
    """Comprehensive tests for CompressionEngine."""
    
    def setUp(self):
        """Set up test environment."""
        self.engine = CompressionEngine()
        self.test_content = """
        This is a test document that leads to better performance and optimization.
        The configuration settings need to be analyzed for security vulnerabilities.
        We need to implement error handling and recovery mechanisms.
        The user interface components require testing and validation.
        """
        
    def test_compression_levels(self):
        """Test all compression levels work correctly."""
        context_levels = [
            {'resource_usage_percent': 30},  # MINIMAL
            {'resource_usage_percent': 50},  # EFFICIENT
            {'resource_usage_percent': 75},  # COMPRESSED
            {'resource_usage_percent': 90},  # CRITICAL
            {'resource_usage_percent': 96}   # EMERGENCY
        ]
        
        expected_levels = [
            CompressionLevel.MINIMAL,
            CompressionLevel.EFFICIENT,
            CompressionLevel.COMPRESSED,
            CompressionLevel.CRITICAL,
            CompressionLevel.EMERGENCY
        ]
        
        for context, expected in zip(context_levels, expected_levels):
            with self.subTest(context=context):
                level = self.engine.determine_compression_level(context)
                self.assertEqual(level, expected)
    
    def test_content_classification(self):
        """Test content type classification."""
        test_cases = [
            # Framework Content - should be excluded
            ("SuperClaude framework content", {'file_path': '~/.claude/test'}, ContentType.FRAMEWORK_CONTENT),
            ("ORCHESTRATOR.md content", {'file_path': 'ORCHESTRATOR.md'}, ContentType.FRAMEWORK_CONTENT),
            ("MCP_Sequential.md content", {'file_path': 'MCP_Sequential.md'}, ContentType.FRAMEWORK_CONTENT),
            
            # Session Data - should be compressed
            ("Session metadata", {'context_type': 'session_metadata'}, ContentType.SESSION_DATA),
            ("Cache content", {'context_type': 'cache_content'}, ContentType.SESSION_DATA),
            
            # User Content - should be preserved
            ("User project code", {'context_type': 'source_code'}, ContentType.USER_CONTENT),
            ("User documentation", {'context_type': 'user_documentation'}, ContentType.USER_CONTENT),
            
            # Working Artifacts - should be compressed
            ("Analysis results", {'context_type': 'analysis_results'}, ContentType.WORKING_ARTIFACTS)
        ]
        
        for content, metadata, expected_type in test_cases:
            with self.subTest(content=content[:30]):
                content_type = self.engine.classify_content(content, metadata)
                self.assertEqual(content_type, expected_type)
    
    def test_symbol_system_compression(self):
        """Test symbol system replacements."""
        test_content = "This leads to better performance and security protection"
        result, techniques = self.engine._apply_symbol_systems(test_content)
        
        # Should replace "leads to" with "→" and other patterns
        self.assertIn("→", result)
        self.assertIn("⚡", result)  # performance
        self.assertIn("🛡️", result)  # security
        self.assertTrue(len(techniques) > 0)
        self.assertIn("symbol_leads_to", techniques)
    
    def test_abbreviation_system_compression(self):
        """Test abbreviation system replacements."""
        test_content = "The configuration settings and documentation standards need optimization"
        result, techniques = self.engine._apply_abbreviation_systems(test_content)
        
        # Should replace long terms with abbreviations
        self.assertIn("cfg", result)     # configuration
        self.assertIn("docs", result)    # documentation
        self.assertIn("std", result)     # standards
        self.assertIn("opt", result)     # optimization
        self.assertTrue(len(techniques) > 0)
    
    def test_structural_optimization(self):
        """Test structural optimization techniques."""
        test_content = """
        
        This is   a   test    with    extra    whitespace.
        
        
        It is important to note that we need to analyze this.
        
        
        """
        
        result, techniques = self.engine._apply_structural_optimization(
            test_content, CompressionLevel.COMPRESSED
        )
        
        # Should remove extra whitespace
        self.assertNotIn("   ", result)
        self.assertNotIn("\n\n\n", result)
        self.assertIn("whitespace_optimization", techniques)
        
        # At compressed level, should also remove articles and simplify phrases
        self.assertNotIn("It is important to note that", result)
        self.assertIn("phrase_simplification", techniques[1] if len(techniques) > 1 else "")
    
    def test_compression_with_different_levels(self):
        """Test compression with different levels produces different results."""
        context_minimal = {'resource_usage_percent': 30}
        context_critical = {'resource_usage_percent': 90}
        
        result_minimal = self.engine.compress_content(
            self.test_content, context_minimal, {'context_type': 'analysis_results'}
        )
        result_critical = self.engine.compress_content(
            self.test_content, context_critical, {'context_type': 'analysis_results'}
        )
        
        # Critical compression should achieve higher compression ratio
        self.assertGreater(result_critical.compression_ratio, result_minimal.compression_ratio)
        self.assertGreater(len(result_minimal.techniques_used), 0)
        self.assertGreater(len(result_critical.techniques_used), len(result_minimal.techniques_used))
    
    def test_framework_content_exclusion(self):
        """Test that framework content is never compressed."""
        framework_content = "This is SuperClaude framework content with complex analysis"
        metadata = {'file_path': '~/.claude/ORCHESTRATOR.md'}
        
        result = self.engine.compress_content(
            framework_content, 
            {'resource_usage_percent': 95},  # Should trigger emergency compression
            metadata
        )
        
        # Framework content should not be compressed regardless of context
        self.assertEqual(result.compression_ratio, 0.0)
        self.assertEqual(result.original_length, result.compressed_length)
        self.assertIn("framework_exclusion", result.techniques_used)
        self.assertEqual(result.quality_score, 1.0)
        self.assertEqual(result.preservation_score, 1.0)
    
    def test_quality_validation(self):
        """Test compression quality validation."""
        test_content = "Important technical terms: React components, API endpoints, database queries"
        strategy = CompressionStrategy(
            level=CompressionLevel.EFFICIENT,
            symbol_systems_enabled=True,
            abbreviation_systems_enabled=True,
            structural_optimization=True,
            selective_preservation={},
            quality_threshold=0.95
        )
        
        quality_score = self.engine._validate_compression_quality(
            test_content, test_content, strategy
        )
        
        # Same content should have perfect quality score
        self.assertEqual(quality_score, 1.0)
        
        # Test with over-compressed content
        over_compressed = "React API database"
        quality_score_low = self.engine._validate_compression_quality(
            test_content, over_compressed, strategy
        )
        
        # Over-compressed content should have lower quality score
        self.assertLess(quality_score_low, 0.8)
    
    def test_information_preservation_calculation(self):
        """Test information preservation scoring."""
        original = "The React component handles API calls to UserService.js endpoints."
        compressed = "React component handles API calls UserService.js endpoints."
        
        preservation_score = self.engine._calculate_information_preservation(original, compressed)
        
        # Key concepts (React, UserService.js) should be preserved
        self.assertGreater(preservation_score, 0.8)
        
        # Test with lost concepts
        over_compressed = "Component handles calls."
        low_preservation = self.engine._calculate_information_preservation(original, over_compressed)
        
        self.assertLess(low_preservation, 0.5)
    
    def test_performance_targets(self):
        """Test that compression meets performance targets."""
        large_content = self.test_content * 100  # Make content larger
        
        start_time = time.time()
        result = self.engine.compress_content(
            large_content,
            {'resource_usage_percent': 75},
            {'context_type': 'analysis_results'}
        )
        end_time = time.time()
        
        # Should complete within reasonable time
        processing_time_ms = (end_time - start_time) * 1000
        self.assertLess(processing_time_ms, 500)  # Less than 500ms
        
        # Result should include timing
        self.assertGreater(result.processing_time_ms, 0)
        self.assertLess(result.processing_time_ms, 200)  # Target <100ms but allow some margin
    
    def test_caching_functionality(self):
        """Test that compression results are cached."""
        test_content = "This content will be cached for performance testing"
        context = {'resource_usage_percent': 50}
        metadata = {'context_type': 'analysis_results'}
        
        # First compression
        result1 = self.engine.compress_content(test_content, context, metadata)
        cache_size_after_first = len(self.engine.compression_cache)
        
        # Second compression of same content
        result2 = self.engine.compress_content(test_content, context, metadata)
        cache_size_after_second = len(self.engine.compression_cache)
        
        # Cache should contain the result
        self.assertGreater(cache_size_after_first, 0)
        self.assertEqual(cache_size_after_first, cache_size_after_second)
        
        # Results should be identical
        self.assertEqual(result1.compression_ratio, result2.compression_ratio)
    
    def test_compression_recommendations(self):
        """Test compression recommendations generation."""
        # High resource usage scenario
        high_usage_context = {'resource_usage_percent': 88, 'processing_time_ms': 600}
        recommendations = self.engine.get_compression_recommendations(high_usage_context)
        
        self.assertIn('current_level', recommendations)
        self.assertIn('recommendations', recommendations)
        self.assertIn('estimated_savings', recommendations)
        self.assertIn('quality_impact', recommendations)
        
        # Should recommend emergency compression for high usage
        self.assertEqual(recommendations['current_level'], 'critical')
        self.assertGreater(len(recommendations['recommendations']), 0)
        
        # Should suggest emergency mode
        rec_text = ' '.join(recommendations['recommendations']).lower()
        self.assertIn('emergency', rec_text)
    
    def test_compression_effectiveness_estimation(self):
        """Test compression savings and quality impact estimation."""
        levels_to_test = [
            CompressionLevel.MINIMAL,
            CompressionLevel.EFFICIENT,
            CompressionLevel.COMPRESSED,
            CompressionLevel.CRITICAL,
            CompressionLevel.EMERGENCY
        ]
        
        for level in levels_to_test:
            with self.subTest(level=level):
                savings = self.engine._estimate_compression_savings(level)
                quality_impact = self.engine._estimate_quality_impact(level)
                
                self.assertIn('token_reduction', savings)
                self.assertIn('time_savings', savings)
                self.assertIsInstance(quality_impact, float)
                self.assertGreaterEqual(quality_impact, 0.0)
                self.assertLessEqual(quality_impact, 1.0)
        
        # Higher compression levels should have higher savings but lower quality
        minimal_savings = self.engine._estimate_compression_savings(CompressionLevel.MINIMAL)
        emergency_savings = self.engine._estimate_compression_savings(CompressionLevel.EMERGENCY)
        
        self.assertLess(minimal_savings['token_reduction'], emergency_savings['token_reduction'])
        
        minimal_quality = self.engine._estimate_quality_impact(CompressionLevel.MINIMAL)
        emergency_quality = self.engine._estimate_quality_impact(CompressionLevel.EMERGENCY)
        
        self.assertGreater(minimal_quality, emergency_quality)
    
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        # Empty content
        result_empty = self.engine.compress_content("", {}, {})
        self.assertEqual(result_empty.compression_ratio, 0.0)
        self.assertEqual(result_empty.original_length, 0)
        self.assertEqual(result_empty.compressed_length, 0)
        
        # Very short content
        result_short = self.engine.compress_content("Hi", {}, {})
        self.assertLessEqual(result_short.compression_ratio, 0.5)
        
        # Content with only symbols that shouldn't be compressed
        symbol_content = "→ ⇒ ← ⇄ & | : » ∴ ∵ ≡ ≈ ≠"
        result_symbols = self.engine.compress_content(symbol_content, {}, {})
        # Should not compress much since it's already symbols
        self.assertLessEqual(result_symbols.compression_ratio, 0.2)
        
        # None metadata handling
        result_none_meta = self.engine.compress_content("test content", {}, None)
        self.assertIsInstance(result_none_meta, CompressionResult)
    
if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)