"""
SuperClaude-Lite Shared Infrastructure

Core components for the executable SuperClaude intelligence framework.
Provides shared functionality across all 7 Claude Code hooks.
"""

__version__ = "1.0.0"
__author__ = "SuperClaude Framework"

from .yaml_loader import UnifiedConfigLoader
from .framework_logic import FrameworkLogic
from .pattern_detection import PatternDetector
from .mcp_intelligence import MCPIntelligence
from .compression_engine import CompressionEngine
from .learning_engine import LearningEngine

__all__ = [
    'UnifiedConfigLoader',
    'FrameworkLogic', 
    'PatternDetector',
    'MCPIntelligence',
    'CompressionEngine',
    'LearningEngine'
]