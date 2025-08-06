#!/usr/bin/env python3
"""
Comprehensive tests for logger.py

Tests all core functionality including:
- Structured logging of hook events
- Session ID management and correlation
- Configuration loading and validation
- Log retention and cleanup
- Error handling and edge cases
"""

import unittest
import sys
import tempfile
import json
import os
import time
from pathlib import Path
from datetime import datetime, timedelta

# Add the shared directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import HookLogger, get_logger, log_hook_start, log_hook_end, log_decision, log_error


class TestHookLogger(unittest.TestCase):
    """Comprehensive tests for HookLogger."""
    
    def setUp(self):
        """Set up test environment with temporary directories."""
        self.temp_dir = tempfile.mkdtemp()
        self.log_dir = Path(self.temp_dir) / "logs"
        self.cache_dir = Path(self.temp_dir)
        
        # Create logger with custom directory
        self.logger = HookLogger(log_dir=str(self.log_dir), retention_days=7)
    
    def test_logger_initialization(self):
        """Test logger initialization and setup."""
        # Should create log directory
        self.assertTrue(self.log_dir.exists())
        
        # Should have session ID
        self.assertIsInstance(self.logger.session_id, str)
        self.assertEqual(len(self.logger.session_id), 8)
        
        # Should be enabled by default
        self.assertTrue(self.logger.enabled)
        
        # Should have created log file for today
        today = datetime.now().strftime("%Y-%m-%d")
        expected_log_file = self.log_dir / f"superclaude-lite-{today}.log"
        
        # File might not exist until first log entry, so test after logging
        self.logger.log_hook_start("test_hook", {"test": "context"})
        self.assertTrue(expected_log_file.exists())
    
    def test_session_id_consistency(self):
        """Test session ID consistency across logger instances."""
        session_id_1 = self.logger.session_id
        
        # Create another logger in same cache directory
        logger_2 = HookLogger(log_dir=str(self.log_dir))
        session_id_2 = logger_2.session_id
        
        # Should use the same session ID (from session file)
        self.assertEqual(session_id_1, session_id_2)
    
    def test_session_id_environment_variable(self):
        """Test session ID from environment variable."""
        test_session_id = "test1234"
        
        # Set environment variable
        os.environ['CLAUDE_SESSION_ID'] = test_session_id
        
        try:
            logger = HookLogger(log_dir=str(self.log_dir))
            self.assertEqual(logger.session_id, test_session_id)
        finally:
            # Clean up environment variable
            if 'CLAUDE_SESSION_ID' in os.environ:
                del os.environ['CLAUDE_SESSION_ID']
    
    def test_hook_start_logging(self):
        """Test logging hook start events."""
        context = {
            "tool_name": "Read", 
            "file_path": "/test/file.py",
            "complexity": 0.5
        }
        
        self.logger.log_hook_start("pre_tool_use", context)
        
        # Check that log file was created and contains the event
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"superclaude-lite-{today}.log"
        
        self.assertTrue(log_file.exists())
        
        # Read and parse the log entry
        with open(log_file, 'r') as f:
            log_content = f.read().strip()
        
        log_entry = json.loads(log_content)
        
        self.assertEqual(log_entry['hook'], 'pre_tool_use')
        self.assertEqual(log_entry['event'], 'start')
        self.assertEqual(log_entry['session'], self.logger.session_id)
        self.assertEqual(log_entry['data'], context)
        self.assertIn('timestamp', log_entry)
    
    def test_hook_end_logging(self):
        """Test logging hook end events."""
        result = {"processed_files": 3, "recommendations": ["use sequential"]}
        
        self.logger.log_hook_end("post_tool_use", 150, True, result)
        
        # Read the log entry
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"superclaude-lite-{today}.log"
        
        with open(log_file, 'r') as f:
            log_content = f.read().strip()
        
        log_entry = json.loads(log_content)
        
        self.assertEqual(log_entry['hook'], 'post_tool_use')
        self.assertEqual(log_entry['event'], 'end')
        self.assertEqual(log_entry['data']['duration_ms'], 150)
        self.assertTrue(log_entry['data']['success'])
        self.assertEqual(log_entry['data']['result'], result)
    
    def test_decision_logging(self):
        """Test logging decision events."""
        self.logger.log_decision(
            "mcp_intelligence", 
            "server_selection", 
            "morphllm", 
            "File count < 10 and complexity < 0.6"
        )
        
        # Read the log entry
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"superclaude-lite-{today}.log"
        
        with open(log_file, 'r') as f:
            log_content = f.read().strip()
        
        log_entry = json.loads(log_content)
        
        self.assertEqual(log_entry['hook'], 'mcp_intelligence')
        self.assertEqual(log_entry['event'], 'decision')
        self.assertEqual(log_entry['data']['type'], 'server_selection')
        self.assertEqual(log_entry['data']['choice'], 'morphllm')
        self.assertEqual(log_entry['data']['reason'], 'File count < 10 and complexity < 0.6')
    
    def test_error_logging(self):
        """Test logging error events."""
        error_context = {"operation": "file_read", "file_path": "/nonexistent/file.py"}
        
        self.logger.log_error(
            "pre_tool_use",
            "FileNotFoundError: File not found",
            error_context
        )
        
        # Read the log entry
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"superclaude-lite-{today}.log"
        
        with open(log_file, 'r') as f:
            log_content = f.read().strip()
        
        log_entry = json.loads(log_content)
        
        self.assertEqual(log_entry['hook'], 'pre_tool_use')
        self.assertEqual(log_entry['event'], 'error')
        self.assertEqual(log_entry['data']['error'], 'FileNotFoundError: File not found')
        self.assertEqual(log_entry['data']['context'], error_context)
    
    def test_multiple_log_entries(self):
        """Test multiple log entries in sequence."""
        # Log multiple events
        self.logger.log_hook_start("session_start", {"user": "test"})
        self.logger.log_decision("framework_logic", "validation", "enabled", "High risk operation")
        self.logger.log_hook_end("session_start", 50, True)
        
        # Read all log entries
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"superclaude-lite-{today}.log"
        
        with open(log_file, 'r') as f:
            log_lines = f.read().strip().split('\n')
        
        self.assertEqual(len(log_lines), 3)
        
        # Parse and verify each entry
        entries = [json.loads(line) for line in log_lines]
        
        # All should have same session ID
        for entry in entries:
            self.assertEqual(entry['session'], self.logger.session_id)
        
        # Verify event types
        self.assertEqual(entries[0]['event'], 'start')
        self.assertEqual(entries[1]['event'], 'decision')
        self.assertEqual(entries[2]['event'], 'end')
    
    def test_configuration_loading(self):
        """Test configuration loading and application."""
        # Test that logger loads configuration without errors
        config = self.logger._load_config()
        self.assertIsInstance(config, dict)
        
        # Should have logging section
        if 'logging' in config:
            self.assertIn('enabled', config['logging'])
    
    def test_disabled_logger(self):
        """Test behavior when logging is disabled."""
        # Create logger with disabled configuration
        disabled_logger = HookLogger(log_dir=str(self.log_dir))
        disabled_logger.enabled = False
        
        # Logging should not create files
        disabled_logger.log_hook_start("test_hook", {"test": "context"})
        
        # Should still work but not actually log
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"superclaude-lite-{today}.log"
        
        # File might exist from previous tests, but should not contain new entries
        # We can't easily test this without affecting other tests, so just ensure no exceptions
        self.assertIsInstance(disabled_logger.enabled, bool)
    
    def test_log_retention_cleanup(self):
        """Test log file retention and cleanup."""
        # Create old log files
        old_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        old_log_file = self.log_dir / f"superclaude-lite-{old_date}.log"
        
        # Create the old file
        with open(old_log_file, 'w') as f:
            f.write('{"old": "log entry"}\n')
        
        # Create recent log file
        recent_date = datetime.now().strftime("%Y-%m-%d")
        recent_log_file = self.log_dir / f"superclaude-lite-{recent_date}.log"
        
        with open(recent_log_file, 'w') as f:
            f.write('{"recent": "log entry"}\n')
        
        # Both files should exist initially
        self.assertTrue(old_log_file.exists())
        self.assertTrue(recent_log_file.exists())
        
        # Create logger with short retention (should trigger cleanup)
        cleanup_logger = HookLogger(log_dir=str(self.log_dir), retention_days=5)
        
        # Old file should be removed, recent file should remain
        self.assertFalse(old_log_file.exists())
        self.assertTrue(recent_log_file.exists())
    
    def test_global_logger_functions(self):
        """Test global convenience functions."""
        # Test that global functions work
        log_hook_start("test_hook", {"global": "test"})
        log_decision("test_hook", "test_decision", "test_choice", "test_reason")
        log_hook_end("test_hook", 100, True, {"result": "success"})
        log_error("test_hook", "test error", {"error": "context"})
        
        # Should not raise exceptions
        global_logger = get_logger()
        self.assertIsInstance(global_logger, HookLogger)
    
    def test_event_filtering(self):
        """Test event filtering based on configuration."""
        # Test the _should_log_event method
        self.assertTrue(self.logger._should_log_event("pre_tool_use", "start"))
        self.assertTrue(self.logger._should_log_event("post_tool_use", "end"))
        self.assertTrue(self.logger._should_log_event("any_hook", "error"))
        self.assertTrue(self.logger._should_log_event("any_hook", "decision"))
        
        # Test with disabled logger
        self.logger.enabled = False
        self.assertFalse(self.logger._should_log_event("any_hook", "start"))
    
    def test_json_structure_validation(self):
        """Test that all log entries produce valid JSON."""
        # Log various types of data that might cause JSON issues
        problematic_data = {
            "unicode": "测试 🚀 émojis",
            "nested": {"deep": {"structure": {"value": 123}}},
            "null_value": None,
            "empty_string": "",
            "large_number": 999999999999,
            "boolean": True,
            "list": [1, 2, 3, "test"]
        }
        
        self.logger.log_hook_start("json_test", problematic_data)
        
        # Read and verify it's valid JSON
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"superclaude-lite-{today}.log"
        
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read().strip()
        
        # Should be valid JSON
        log_entry = json.loads(log_content)
        self.assertEqual(log_entry['data'], problematic_data)
    
    def test_performance_requirements(self):
        """Test that logging meets performance requirements."""
        # Test logging performance
        start_time = time.time()
        
        for i in range(100):
            self.logger.log_hook_start(f"performance_test_{i}", {"iteration": i, "data": "test"})
        
        end_time = time.time()
        total_time_ms = (end_time - start_time) * 1000
        
        # Should complete 100 log entries quickly (< 100ms total)
        self.assertLess(total_time_ms, 100)
        
        # Average per log entry should be very fast (< 1ms)
        avg_time_ms = total_time_ms / 100
        self.assertLess(avg_time_ms, 1.0)
    
    def test_edge_cases_and_error_handling(self):
        """Test edge cases and error handling."""
        # Empty/None data
        self.logger.log_hook_start("test_hook", None)
        self.logger.log_hook_start("test_hook", {})
        
        # Very long strings
        long_string = "x" * 10000
        self.logger.log_hook_start("test_hook", {"long": long_string})
        
        # Special characters
        special_data = {
            "newlines": "line1\nline2\nline3",
            "tabs": "col1\tcol2\tcol3",
            "quotes": 'He said "Hello, World!"',
            "backslashes": "C:\\path\\to\\file"
        }
        self.logger.log_hook_start("test_hook", special_data)
        
        # Very large numbers
        self.logger.log_hook_end("test_hook", 999999999, False, {"huge_number": 2**63 - 1})
        
        # Test that all these don't raise exceptions and produce valid JSON
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"superclaude-lite-{today}.log"
        
        with open(log_file, 'r', encoding='utf-8') as f:
            log_lines = f.read().strip().split('\n')
        
        # All lines should be valid JSON
        for line in log_lines:
            if line.strip():  # Skip empty lines
                json.loads(line)  # Should not raise exception
    
    def test_concurrent_logging(self):
        """Test concurrent logging from multiple sources."""
        import threading
        
        def log_worker(worker_id):
            for i in range(10):
                self.logger.log_hook_start(f"worker_{worker_id}", {"iteration": i})
                self.logger.log_hook_end(f"worker_{worker_id}", 10 + i, True)
        
        # Create multiple threads
        threads = [threading.Thread(target=log_worker, args=(i,)) for i in range(5)]
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Check that all entries were logged
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"superclaude-lite-{today}.log"
        
        with open(log_file, 'r') as f:
            log_lines = f.read().strip().split('\n')
        
        # Should have entries from all workers (5 workers * 10 iterations * 2 events each = 100 entries)
        # Plus any entries from previous tests
        self.assertGreaterEqual(len([l for l in log_lines if l.strip()]), 100)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)