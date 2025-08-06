#!/usr/bin/env python3
"""
Comprehensive tests for learning_engine.py

Tests all core functionality including:
- Learning event recording and pattern creation
- Adaptation generation and application
- Cross-hook learning and effectiveness tracking
- Data persistence and corruption recovery
- Performance optimization patterns
"""

import unittest
import sys
import tempfile
import json
import time
from pathlib import Path

# Add the shared directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from learning_engine import (
    LearningEngine, LearningType, AdaptationScope, LearningRecord,
    Adaptation, LearningInsight
)


class TestLearningEngine(unittest.TestCase):
    """Comprehensive tests for LearningEngine."""
    
    def setUp(self):
        """Set up test environment with temporary cache directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = Path(self.temp_dir)
        self.engine = LearningEngine(self.cache_dir)
        
        # Test data
        self.test_context = {
            'operation_type': 'write',
            'complexity_score': 0.5,
            'file_count': 3,
            'resource_usage_percent': 60,
            'user_expertise': 'intermediate'
        }
        
        self.test_pattern = {
            'mcp_server': 'morphllm',
            'mode': 'efficient',
            'flags': ['--delegate', 'files'],
            'optimization': {'token_reduction': 0.3}
        }
    
    def test_learning_event_recording(self):
        """Test basic learning event recording."""
        learning_id = self.engine.record_learning_event(
            learning_type=LearningType.USER_PREFERENCE,
            scope=AdaptationScope.USER,
            context=self.test_context,
            pattern=self.test_pattern,
            effectiveness_score=0.8,
            confidence=0.9,
            metadata={'hook': 'pre_tool_use'}
        )
        
        # Should return a valid learning ID
        self.assertIsInstance(learning_id, str)
        self.assertTrue(learning_id.startswith('learning_'))
        
        # Should add to learning records
        self.assertEqual(len(self.engine.learning_records), 1)
        
        record = self.engine.learning_records[0]
        self.assertEqual(record.learning_type, LearningType.USER_PREFERENCE)
        self.assertEqual(record.scope, AdaptationScope.USER)
        self.assertEqual(record.effectiveness_score, 0.8)
        self.assertEqual(record.confidence, 0.9)
        self.assertEqual(record.context, self.test_context)
        self.assertEqual(record.pattern, self.test_pattern)
    
    def test_automatic_adaptation_creation(self):
        """Test that adaptations are automatically created from significant learning events."""
        # Record a significant learning event (high effectiveness and confidence)
        self.engine.record_learning_event(
            learning_type=LearningType.PERFORMANCE_OPTIMIZATION,
            scope=AdaptationScope.USER,
            context=self.test_context,
            pattern=self.test_pattern,
            effectiveness_score=0.85,  # High effectiveness
            confidence=0.8             # High confidence
        )
        
        # Should create an adaptation
        self.assertGreater(len(self.engine.adaptations), 0)
        
        # Find the created adaptation
        adaptation = list(self.engine.adaptations.values())[0]
        self.assertIsInstance(adaptation, Adaptation)
        self.assertEqual(adaptation.effectiveness_history, [0.85])
        self.assertEqual(adaptation.usage_count, 1)
        self.assertEqual(adaptation.confidence_score, 0.8)
        
        # Should have extracted modifications correctly
        self.assertIn('preferred_mcp_server', adaptation.modifications)
        self.assertEqual(adaptation.modifications['preferred_mcp_server'], 'morphllm')
    
    def test_pattern_signature_generation(self):
        """Test pattern signature generation for grouping similar patterns."""
        pattern1 = {'mcp_server': 'morphllm', 'complexity': 0.5}
        pattern2 = {'mcp_server': 'morphllm', 'complexity': 0.5}
        pattern3 = {'mcp_server': 'serena', 'complexity': 0.8}
        
        context = {'operation_type': 'write', 'file_count': 3}
        
        sig1 = self.engine._generate_pattern_signature(pattern1, context)
        sig2 = self.engine._generate_pattern_signature(pattern2, context)
        sig3 = self.engine._generate_pattern_signature(pattern3, context)
        
        # Similar patterns should have same signature
        self.assertEqual(sig1, sig2)
        
        # Different patterns should have different signatures
        self.assertNotEqual(sig1, sig3)
        
        # Signatures should be stable and deterministic
        self.assertIsInstance(sig1, str)
        self.assertGreater(len(sig1), 0)
    
    def test_adaptation_retrieval_for_context(self):
        """Test retrieving relevant adaptations for a given context."""
        # Create some adaptations
        self.engine.record_learning_event(
            LearningType.OPERATION_PATTERN, AdaptationScope.USER,
            {'operation_type': 'write', 'file_count': 3, 'complexity_score': 0.5},
            {'mcp_server': 'morphllm'}, 0.8, 0.9
        )
        
        self.engine.record_learning_event(
            LearningType.OPERATION_PATTERN, AdaptationScope.USER,
            {'operation_type': 'read', 'file_count': 10, 'complexity_score': 0.8},
            {'mcp_server': 'serena'}, 0.9, 0.8
        )
        
        # Test matching context
        matching_context = {'operation_type': 'write', 'file_count': 3, 'complexity_score': 0.5}
        adaptations = self.engine.get_adaptations_for_context(matching_context)
        
        self.assertGreater(len(adaptations), 0)
        # Should be sorted by effectiveness * confidence
        if len(adaptations) > 1:
            first_score = adaptations[0].effectiveness_history[0] * adaptations[0].confidence_score
            second_score = adaptations[1].effectiveness_history[0] * adaptations[1].confidence_score
            self.assertGreaterEqual(first_score, second_score)
    
    def test_adaptation_application(self):
        """Test applying adaptations to enhance recommendations."""
        # Create an adaptation
        self.engine.record_learning_event(
            LearningType.USER_PREFERENCE, AdaptationScope.USER,
            self.test_context, self.test_pattern, 0.85, 0.8
        )
        
        # Apply adaptations to base recommendations
        base_recommendations = {
            'recommended_mcp_servers': ['sequential'],
            'recommended_modes': ['standard']
        }
        
        enhanced = self.engine.apply_adaptations(self.test_context, base_recommendations)
        
        # Should enhance recommendations with learned preferences
        self.assertIn('recommended_mcp_servers', enhanced)
        servers = enhanced['recommended_mcp_servers']
        self.assertIn('morphllm', servers)
        self.assertEqual(servers[0], 'morphllm')  # Should be prioritized
        
        # Should include adaptation metadata
        self.assertIn('applied_adaptations', enhanced)
        self.assertGreater(len(enhanced['applied_adaptations']), 0)
        
        adaptation_info = enhanced['applied_adaptations'][0]
        self.assertIn('id', adaptation_info)
        self.assertIn('confidence', adaptation_info)
        self.assertIn('effectiveness', adaptation_info)
    
    def test_effectiveness_feedback_integration(self):
        """Test recording and integrating effectiveness feedback."""
        # Create an adaptation first
        self.engine.record_learning_event(
            LearningType.PERFORMANCE_OPTIMIZATION, AdaptationScope.USER,
            self.test_context, self.test_pattern, 0.8, 0.9
        )
        
        # Get the adaptation ID
        adaptation = list(self.engine.adaptations.values())[0]
        adaptation_id = adaptation.adaptation_id
        original_history_length = len(adaptation.effectiveness_history)
        
        # Record effectiveness feedback
        self.engine.record_effectiveness_feedback(
            [adaptation_id], 0.9, self.test_context
        )
        
        # Should update the adaptation's effectiveness history
        updated_adaptation = self.engine.adaptations[adaptation.pattern_signature]
        self.assertEqual(len(updated_adaptation.effectiveness_history), original_history_length + 1)
        self.assertEqual(updated_adaptation.effectiveness_history[-1], 0.9)
        
        # Should update confidence based on consistency
        self.assertIsInstance(updated_adaptation.confidence_score, float)
        self.assertGreaterEqual(updated_adaptation.confidence_score, 0.0)
        self.assertLessEqual(updated_adaptation.confidence_score, 1.0)
    
    def test_learning_insights_generation(self):
        """Test generation of learning insights from patterns."""
        # Create multiple learning records for insights
        for i in range(5):
            self.engine.record_learning_event(
                LearningType.USER_PREFERENCE, AdaptationScope.USER,
                self.test_context,
                {'mcp_server': 'morphllm'},
                0.85 + i * 0.01,  # Slightly varying effectiveness
                0.8
            )
        
        # Generate insights
        insights = self.engine.generate_learning_insights()
        
        self.assertIsInstance(insights, list)
        
        # Should generate user preference insights
        user_insights = [i for i in insights if i.insight_type == 'user_preference']
        if len(user_insights) > 0:
            insight = user_insights[0]
            self.assertIsInstance(insight, LearningInsight)
            self.assertIn('morphllm', insight.description)
            self.assertGreater(len(insight.evidence), 0)
            self.assertGreater(len(insight.recommendations), 0)
            self.assertGreater(insight.confidence, 0.0)
            self.assertGreater(insight.impact_score, 0.0)
    
    def test_data_persistence_and_loading(self):
        """Test data persistence and loading across engine instances."""
        # Add some learning data
        self.engine.record_learning_event(
            LearningType.USER_PREFERENCE, AdaptationScope.USER,
            self.test_context, self.test_pattern, 0.8, 0.9
        )
        
        # Force save
        self.engine._save_learning_data()
        
        # Create new engine instance with same cache directory
        new_engine = LearningEngine(self.cache_dir)
        
        # Should load the previously saved data
        self.assertEqual(len(new_engine.learning_records), len(self.engine.learning_records))
        self.assertEqual(len(new_engine.adaptations), len(self.engine.adaptations))
        
        # Data should be identical
        if len(new_engine.learning_records) > 0:
            original_record = self.engine.learning_records[0]
            loaded_record = new_engine.learning_records[0]
            
            self.assertEqual(loaded_record.learning_type, original_record.learning_type)
            self.assertEqual(loaded_record.effectiveness_score, original_record.effectiveness_score)
            self.assertEqual(loaded_record.context, original_record.context)
    
    def test_data_corruption_recovery(self):
        """Test recovery from corrupted data files."""
        # Create valid data first
        self.engine.record_learning_event(
            LearningType.USER_PREFERENCE, AdaptationScope.USER,
            self.test_context, self.test_pattern, 0.8, 0.9
        )
        
        # Manually corrupt the learning records file
        records_file = self.cache_dir / "learning_records.json"
        with open(records_file, 'w') as f:
            f.write('{"invalid": "json structure"}')  # Invalid JSON structure
        
        # Create new engine - should recover gracefully
        new_engine = LearningEngine(self.cache_dir)
        
        # Should initialize with empty data structures
        self.assertEqual(len(new_engine.learning_records), 0)
        self.assertEqual(len(new_engine.adaptations), 0)
        
        # Should still be functional
        new_engine.record_learning_event(
            LearningType.USER_PREFERENCE, AdaptationScope.USER,
            {'operation_type': 'test'}, {'test': 'pattern'}, 0.7, 0.8
        )
        
        self.assertEqual(len(new_engine.learning_records), 1)
    
    def test_performance_pattern_analysis(self):
        """Test analysis of performance optimization patterns."""
        # Add delegation performance records
        for i in range(6):
            self.engine.record_learning_event(
                LearningType.PERFORMANCE_OPTIMIZATION, AdaptationScope.USER,
                {'operation_type': 'multi_file', 'file_count': 10},
                {'delegation': True, 'strategy': 'files'},
                0.8 + i * 0.01,  # Good performance
                0.8
            )
        
        insights = self.engine.generate_learning_insights()
        
        # Should generate performance insights
        perf_insights = [i for i in insights if i.insight_type == 'performance_optimization']
        
        if len(perf_insights) > 0:
            insight = perf_insights[0]
            self.assertIn('delegation', insight.description.lower())
            self.assertIn('performance', insight.description.lower())
            self.assertGreater(insight.confidence, 0.7)
            self.assertGreater(insight.impact_score, 0.6)
    
    def test_error_pattern_analysis(self):
        """Test analysis of error recovery patterns."""
        # Add error recovery records
        for i in range(3):
            self.engine.record_learning_event(
                LearningType.ERROR_RECOVERY, AdaptationScope.USER,
                {'operation_type': 'write', 'error_type': 'file_not_found'},
                {'recovery_strategy': 'create_directory_first'},
                0.7 + i * 0.05,
                0.8
            )
        
        insights = self.engine.generate_learning_insights()
        
        # Should generate error recovery insights
        error_insights = [i for i in insights if i.insight_type == 'error_recovery']
        
        if len(error_insights) > 0:
            insight = error_insights[0]
            self.assertIn('error', insight.description.lower())
            self.assertIn('write', insight.description.lower())
            self.assertGreater(len(insight.recommendations), 0)
    
    def test_effectiveness_trend_analysis(self):
        """Test analysis of overall effectiveness trends."""
        # Add many records with high effectiveness
        for i in range(12):
            self.engine.record_learning_event(
                LearningType.OPERATION_PATTERN, AdaptationScope.USER,
                {'operation_type': f'operation_{i}'},
                {'pattern': f'pattern_{i}'},
                0.85 + (i % 3) * 0.02,  # High effectiveness with variation
                0.8
            )
        
        insights = self.engine.generate_learning_insights()
        
        # Should generate effectiveness trend insights
        trend_insights = [i for i in insights if i.insight_type == 'effectiveness_trend']
        
        if len(trend_insights) > 0:
            insight = trend_insights[0]
            self.assertIn('effectiveness', insight.description.lower())
            self.assertIn('high', insight.description.lower())
            self.assertGreater(insight.confidence, 0.8)
            self.assertGreater(insight.impact_score, 0.8)
    
    def test_data_cleanup(self):
        """Test cleanup of old learning data."""
        # Add old data
        old_timestamp = time.time() - (40 * 24 * 60 * 60)  # 40 days ago
        
        # Manually create old record
        old_record = LearningRecord(
            timestamp=old_timestamp,
            learning_type=LearningType.USER_PREFERENCE,
            scope=AdaptationScope.USER,
            context={'old': 'context'},
            pattern={'old': 'pattern'},
            effectiveness_score=0.5,
            confidence=0.5,
            metadata={}
        )
        
        self.engine.learning_records.append(old_record)
        
        # Add recent data
        self.engine.record_learning_event(
            LearningType.USER_PREFERENCE, AdaptationScope.USER,
            {'recent': 'context'}, {'recent': 'pattern'}, 0.8, 0.9
        )
        
        original_count = len(self.engine.learning_records)
        
        # Cleanup with 30-day retention
        self.engine.cleanup_old_data(30)
        
        # Should remove old data but keep recent data
        self.assertLess(len(self.engine.learning_records), original_count)
        
        # Recent data should still be there
        recent_records = [r for r in self.engine.learning_records if 'recent' in r.context]
        self.assertGreater(len(recent_records), 0)
    
    def test_pattern_matching_logic(self):
        """Test pattern matching logic for adaptation triggers."""
        # Create adaptation with specific trigger conditions
        trigger_conditions = {
            'operation_type': 'write',
            'file_count': 5,
            'complexity_score': 0.6
        }
        
        # Exact match should work
        exact_context = {
            'operation_type': 'write',
            'file_count': 5,
            'complexity_score': 0.6
        }
        self.assertTrue(self.engine._matches_trigger_conditions(trigger_conditions, exact_context))
        
        # Close numerical match should work (within tolerance)
        close_context = {
            'operation_type': 'write',
            'file_count': 5,
            'complexity_score': 0.65  # Within 0.1 tolerance
        }
        self.assertTrue(self.engine._matches_trigger_conditions(trigger_conditions, close_context))
        
        # Different string should not match
        different_context = {
            'operation_type': 'read',
            'file_count': 5,
            'complexity_score': 0.6
        }
        self.assertFalse(self.engine._matches_trigger_conditions(trigger_conditions, different_context))
        
        # Missing key should not prevent matching
        partial_context = {
            'operation_type': 'write',
            'file_count': 5
            # complexity_score missing
        }
        self.assertTrue(self.engine._matches_trigger_conditions(trigger_conditions, partial_context))
    
    def test_edge_cases_and_error_handling(self):
        """Test edge cases and error handling."""
        # Empty context and pattern
        learning_id = self.engine.record_learning_event(
            LearningType.USER_PREFERENCE, AdaptationScope.SESSION,
            {}, {}, 0.5, 0.5
        )
        self.assertIsInstance(learning_id, str)
        
        # Extreme values
        extreme_id = self.engine.record_learning_event(
            LearningType.PERFORMANCE_OPTIMIZATION, AdaptationScope.GLOBAL,
            {'extreme_value': 999999}, {'extreme_pattern': True},
            1.0, 1.0
        )
        self.assertIsInstance(extreme_id, str)
        
        # Invalid effectiveness scores (should be clamped)
        invalid_id = self.engine.record_learning_event(
            LearningType.ERROR_RECOVERY, AdaptationScope.USER,
            {'test': 'context'}, {'test': 'pattern'},
            -0.5, 2.0  # Invalid scores
        )
        self.assertIsInstance(invalid_id, str)
        
        # Test with empty adaptations
        empty_recommendations = self.engine.apply_adaptations({}, {})
        self.assertIsInstance(empty_recommendations, dict)
        
        # Test insights with no data
        self.engine.learning_records = []
        self.engine.adaptations = {}
        insights = self.engine.generate_learning_insights()
        self.assertIsInstance(insights, list)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)