#!/usr/bin/env python3
"""
Performance Monitor Hook for SuperClaude Claude Code Integration

Real-time performance tracking and optimization for SuperClaude session lifecycle,
MCP server coordination, and framework operations. Monitors all tool executions
against strict PRD performance targets and provides optimization suggestions.

Key Capabilities:
- Tool execution timing measurement (<2s target)
- Memory usage tracking during operations
- Resource utilization analysis
- Performance threshold violation detection  
- Optimization recommendations generation
- Historical performance trend tracking
"""

import json
import sys
import time
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.WARNING, format='[%(name)s] %(levelname)s: %(message)s')
logger = logging.getLogger('SuperClaude.Hooks.PerformanceMonitor')

# Try to import yaml for configuration loading
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    logger.warning("PyYAML not available - using fallback performance targets")

# Try to import psutil for resource monitoring, fall back gracefully
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# Import base hook with error handling
try:
    sys.path.append(str(Path(__file__).parent.parent / "common"))
    from base_hook import BaseHook
    BASE_HOOK_AVAILABLE = True
except ImportError:
    BASE_HOOK_AVAILABLE = False
    # Minimal base class fallback
    class BaseHook:
        def __init__(self, hook_name: str, input_data: Optional[Dict[str, Any]] = None):
            self.hook_name = hook_name
            self.start_time = time.time()
            self.claude_project_dir = os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())
            self.input_data = input_data if input_data is not None else self._load_json_input()
            
        def _load_json_input(self) -> Dict[str, Any]:
            try:
                if sys.stdin.isatty():
                    return {}
                input_text = sys.stdin.read().strip()
                return json.loads(input_text) if input_text else {}
            except:
                return {}
                
        def _log_error(self, message: str):
            print(f"[SuperClaude Hook Error] {self.hook_name}: {message}", file=sys.stderr)
            
        def get_tool_name(self) -> Optional[str]:
            return self.input_data.get("tool", {}).get("name")
            
        def get_tool_args(self) -> Dict[str, Any]:
            return self.input_data.get("tool", {}).get("args", {})
            
        def get_session_id(self) -> Optional[str]:
            return self.input_data.get("session_id")
            
        def get_cwd(self) -> Optional[str]:
            return self.input_data.get("cwd")
            
        def get_transcript_path(self) -> Optional[str]:
            return self.input_data.get("transcript_path")
            
        def run(self) -> int:
            try:
                result = self.execute()
                return 0 if result else 1
            except Exception as e:
                self._log_error(f"Execution failed: {e}")
                return 1

class PerformanceMonitorHook(BaseHook):
    """
    Real-time performance monitoring hook for SuperClaude operations
    
    Tracks:
    - Tool execution timing (PostToolUse trigger)
    - Memory usage during operations
    - Resource utilization patterns
    - Performance threshold violations
    - Historical trends and optimization opportunities
    """
    
    def __init__(self, input_data: Optional[Dict[str, Any]] = None):
        # Pass input_data to parent class if BaseHook accepts it
        try:
            super().__init__("PerformanceMonitor", input_data=input_data)
        except TypeError:
            # Fallback for BaseHook that doesn't accept input_data
            super().__init__("PerformanceMonitor")
            if input_data is not None:
                self.input_data = input_data
        
        # Add logger attribute for compatibility
        if not hasattr(self, 'logger'):
            import logging
            self.logger = logging.getLogger(f"SuperClaude.Hooks.{self.hook_name}")
        
        # Add helper methods if not inherited from fallback BaseHook
        if not hasattr(self, 'get_tool_name'):
            self.get_tool_name = lambda: self.input_data.get("tool", {}).get("name") if hasattr(self, 'input_data') else None
            self.get_tool_args = lambda: self.input_data.get("tool", {}).get("args", {}) if hasattr(self, 'input_data') else {}
            self.get_session_id = lambda: self.input_data.get("session_id") if hasattr(self, 'input_data') else None
            self.get_cwd = lambda: self.input_data.get("cwd") if hasattr(self, 'input_data') else None
            self.get_transcript_path = lambda: self.input_data.get("transcript_path") if hasattr(self, 'input_data') else None
        
        # Load performance targets from Resources
        self.performance_targets = {}
        self.warning_threshold = 0.8
        self.critical_threshold = 1.5
        self.resource_limits = {}
        
        # Define fallback values
        fallback_targets = {
            "memory_operations": 200,
            "project_loading": 500,
            "session_save": 2000,
            "tool_selection": 100,
            "checkpoint_creation": 1000,
            "context_loading": 500,
            "reflection_operations": 5000,
            "session_restore": 500,
            "general_operations": 2000
        }
        
        fallback_resource_limits = {
            "monitoring_overhead_cpu_percent": 2,
            "monitoring_memory_mb": 50
        }
        
        # Try to load from YAML if available
        if YAML_AVAILABLE:
            resources_path = Path(__file__).parent.parent / "Resources" / "performance_targets.yaml"
            try:
                if resources_path.exists():
                    with open(resources_path, 'r') as f:
                        config = yaml.safe_load(f)
                        
                        # Load and validate performance targets
                        loaded_targets = config.get('performance_targets', {})
                        self.performance_targets = self._validate_performance_targets(loaded_targets, fallback_targets)
                        logger.debug(f"Loaded {len(self.performance_targets)} performance targets from YAML")
                        
                        # Load and validate alert thresholds
                        thresholds = config.get('alert_thresholds', {})
                        self.warning_threshold = self._validate_threshold(thresholds.get('warning'), 0.8, 'warning')
                        self.critical_threshold = self._validate_threshold(thresholds.get('critical'), 1.5, 'critical')
                        
                        # Load and validate resource limits
                        loaded_limits = config.get('resource_limits', {})
                        self.resource_limits = self._validate_resource_limits(loaded_limits, fallback_resource_limits)
                        logger.debug(f"Loaded resource limits: {self.resource_limits}")
                else:
                    logger.warning(f"Performance targets YAML not found at {resources_path}")
                    self.performance_targets = fallback_targets
                    self.resource_limits = fallback_resource_limits
                    
            except yaml.YAMLError as e:
                logger.error(f"YAML parsing error in performance targets: {e}")
                self.performance_targets = fallback_targets
                self.resource_limits = fallback_resource_limits
                
            except FileNotFoundError as e:
                logger.error(f"File not found when loading performance targets: {e}")
                self.performance_targets = fallback_targets
                self.resource_limits = fallback_resource_limits
                
            except Exception as e:
                logger.error(f"Unexpected error loading performance targets: {type(e).__name__}: {e}")
                self.performance_targets = fallback_targets
                self.resource_limits = fallback_resource_limits
        else:
            # YAML not available, use fallback
            self.performance_targets = fallback_targets
            self.resource_limits = fallback_resource_limits
        
        # Performance metrics storage
        # Use the hook's own directory for metrics storage
        self.metrics_file = Path(__file__).parent / "metrics.jsonl"
        self.ensure_metrics_directory()
        
        # Process monitoring (if psutil available)
        if PSUTIL_AVAILABLE:
            try:
                self.process = psutil.Process()
                self.initial_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            except:
                self.process = None
                self.initial_memory = 0
        else:
            self.process = None
            self.initial_memory = 0
        
    def ensure_metrics_directory(self):
        """Ensure metrics directory exists"""
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _validate_performance_targets(self, targets: Dict[str, Any], fallback: Dict[str, int]) -> Dict[str, int]:
        """Validate performance targets are positive integers"""
        validated = {}
        
        for key, default_value in fallback.items():
            if key in targets:
                value = targets[key]
                if isinstance(value, (int, float)) and value > 0:
                    validated[key] = int(value)
                    if value != int(value):
                        logger.warning(f"Performance target '{key}' converted from float {value} to int {int(value)}")
                else:
                    logger.warning(f"Invalid performance target '{key}': {value} (must be positive number), using default: {default_value}")
                    validated[key] = default_value
            else:
                validated[key] = default_value
                
        # Log any extra keys that were ignored
        extra_keys = set(targets.keys()) - set(fallback.keys())
        if extra_keys:
            logger.warning(f"Ignoring unknown performance target keys: {extra_keys}")
            
        return validated
    
    def _validate_threshold(self, value: Any, default: float, name: str) -> float:
        """Validate threshold is a positive float"""
        if value is None:
            return default
            
        if isinstance(value, (int, float)) and 0 < value <= 10:  # Reasonable range for thresholds
            return float(value)
        else:
            logger.warning(f"Invalid {name} threshold: {value} (must be 0 < value <= 10), using default: {default}")
            return default
    
    def _validate_resource_limits(self, limits: Dict[str, Any], fallback: Dict[str, int]) -> Dict[str, int]:
        """Validate resource limits are positive numbers"""
        validated = {}
        
        # Validate CPU percentage
        cpu_key = "monitoring_overhead_cpu_percent"
        if cpu_key in limits:
            cpu_value = limits[cpu_key]
            if isinstance(cpu_value, (int, float)) and 0 < cpu_value <= 100:
                validated[cpu_key] = float(cpu_value)
            else:
                logger.warning(f"Invalid CPU limit: {cpu_value} (must be 0-100%), using default: {fallback[cpu_key]}")
                validated[cpu_key] = fallback[cpu_key]
        else:
            validated[cpu_key] = fallback[cpu_key]
            
        # Validate memory MB
        mem_key = "monitoring_memory_mb"
        if mem_key in limits:
            mem_value = limits[mem_key]
            if isinstance(mem_value, (int, float)) and mem_value > 0:
                validated[mem_key] = int(mem_value)
            else:
                logger.warning(f"Invalid memory limit: {mem_value} (must be positive), using default: {fallback[mem_key]}")
                validated[mem_key] = fallback[mem_key]
        else:
            validated[mem_key] = fallback[mem_key]
            
        return validated
        
    def execute(self) -> bool:
        """Main performance monitoring execution"""
        try:
            # Extract tool execution data
            tool_name = self.get_tool_name()
            if not tool_name:
                return True  # No tool to monitor
                
            # Get performance data from input
            performance_data = self.extract_performance_data()
            
            # Classify operation type for appropriate target
            operation_type = self.classify_operation(tool_name, performance_data)
            
            # Calculate metrics
            metrics = self.calculate_metrics(tool_name, operation_type, performance_data)
            
            # Evaluate performance against targets
            status = self.evaluate_performance(metrics, operation_type)
            
            # Generate output with color-coded status
            self.output_performance_report(metrics, status)
            
            # Store metrics for trend analysis
            self.store_metrics(metrics, status)
            
            # Generate optimization suggestions if needed
            if status["severity"] in ["warning", "critical"]:
                self.generate_optimization_suggestions(metrics, status)
                
            return True
            
        except Exception as e:
            self.logger.error(f"Performance monitoring failed: {e}")
            return False
    
    def extract_performance_data(self) -> Dict[str, Any]:
        """Extract performance data from input"""
        data = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": self.get_session_id(),
            "cwd": self.get_cwd(),
            "transcript_path": self.get_transcript_path()
        }
        
        # Extract timing information if available
        if "execution_time_ms" in self.input_data:
            data["execution_time_ms"] = self.input_data["execution_time_ms"]
        
        # Extract tool-specific data
        tool_data = self.input_data.get("tool", {})
        data["tool_args"] = tool_data.get("args", {})
        data["tool_result"] = self.input_data.get("result", {})
        
        return data
    
    def classify_operation(self, tool_name: str, performance_data: Dict[str, Any]) -> str:
        """Classify operation type for appropriate performance target"""
        
        # Session lifecycle operations
        if any(cmd in str(performance_data.get("tool_args", {})) for cmd in ["/sc:load", "sc:load"]):
            return "project_loading"
        elif any(cmd in str(performance_data.get("tool_args", {})) for cmd in ["/sc:save", "sc:save"]):
            return "session_save"  
        elif any(cmd in str(performance_data.get("tool_args", {})) for cmd in ["/sc:reflect", "sc:reflect"]):
            return "reflection_operations"
            
        # Memory operations (Serena MCP)
        elif "serena" in tool_name.lower() or "memory" in tool_name.lower():
            return "memory_operations"
            
        # Context and loading operations
        elif tool_name in ["Read", "Glob", "Grep"] and self.is_context_operation(performance_data):
            return "context_loading"
            
        # File operations that might be checkpoints
        elif tool_name in ["Write"] and self.is_checkpoint_operation(performance_data):
            return "checkpoint_creation"
            
        # Default to general operations
        else:
            return "general_operations"
    
    def is_context_operation(self, performance_data: Dict[str, Any]) -> bool:
        """Determine if operation is context loading"""
        args = performance_data.get("tool_args", {})
        
        # Check for patterns indicating context loading
        context_patterns = [
            ".claude", "superclaude", "context", "session", "memory",
            "*.md", "config", "settings"
        ]
        
        file_path = args.get("file_path", "")
        pattern = args.get("pattern", "")
        
        return any(pattern_str in (file_path + pattern).lower() for pattern_str in context_patterns)
    
    def is_checkpoint_operation(self, performance_data: Dict[str, Any]) -> bool:
        """Determine if operation is checkpoint creation"""
        args = performance_data.get("tool_args", {})
        file_path = args.get("file_path", "")
        
        checkpoint_patterns = ["checkpoint", "session", "save", "memory", "serena"]
        return any(pattern in file_path.lower() for pattern in checkpoint_patterns)
    
    def calculate_metrics(self, tool_name: str, operation_type: str, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive performance metrics"""
        
        # Get current resource usage (if available)
        current_memory = 0
        memory_delta = 0
        cpu_percent = 0
        
        if self.process:
            try:
                current_memory = self.process.memory_info().rss / 1024 / 1024  # MB
                memory_delta = current_memory - self.initial_memory
                cpu_percent = self.process.cpu_percent(interval=0.01)  # Reduced interval for speed
            except:
                pass
                
        # Calculate execution time (estimate if not provided)
        execution_time_ms = performance_data.get("execution_time_ms")
        if execution_time_ms is None:
            # Estimate based on tool type and args
            execution_time_ms = self.estimate_execution_time(tool_name, performance_data)
        
        metrics = {
            "timestamp": performance_data["timestamp"],
            "tool_name": tool_name,
            "operation_type": operation_type,
            "execution_time_ms": execution_time_ms,
            "memory_usage_mb": current_memory,
            "memory_delta_mb": memory_delta,
            "cpu_percent": cpu_percent,
            "session_id": performance_data.get("session_id"),
            "performance_target_ms": self.performance_targets.get(operation_type, 2000)
        }
        
        # Add file-specific metrics if applicable  
        tool_args = performance_data.get("tool_args", {})
        if "file_path" in tool_args:
            try:
                file_path = Path(tool_args["file_path"])
                if file_path.exists():
                    metrics["file_size_kb"] = file_path.stat().st_size / 1024
            except:
                pass
                
        return metrics
    
    def estimate_execution_time(self, tool_name: str, performance_data: Dict[str, Any]) -> float:
        """Estimate execution time based on tool type and arguments"""
        
        # Base execution time estimates by tool type (ms)
        base_times = {
            "Read": 10, "Write": 50, "Glob": 20, "Grep": 30,
            "Bash": 100, "Edit": 40, "MultiEdit": 80
        }
        
        base_time = base_times.get(tool_name, 50)
        
        # Adjust based on arguments
        args = performance_data.get("tool_args", {})
        
        # File size adjustments
        if "file_path" in args:
            try:
                file_path = Path(args["file_path"])
                if file_path.exists():
                    size_kb = file_path.stat().st_size / 1024
                    # Add 1ms per KB for large files
                    base_time += min(size_kb, 1000)
            except:
                pass
                
        # Pattern complexity for Grep
        if tool_name == "Grep" and "pattern" in args:
            pattern_complexity = len(args["pattern"])
            base_time += pattern_complexity * 2
            
        # Bash command complexity
        if tool_name == "Bash" and "command" in args:
            command_length = len(args["command"])
            base_time += command_length * 0.5
            
        return base_time
    
    def evaluate_performance(self, metrics: Dict[str, Any], operation_type: str) -> Dict[str, Any]:
        """Evaluate performance against targets and generate status"""
        
        target_ms = metrics["performance_target_ms"]
        actual_ms = metrics["execution_time_ms"]
        
        # Calculate performance ratio
        performance_ratio = actual_ms / target_ms if target_ms > 0 else 0
        
        # Determine severity
        if performance_ratio >= self.critical_threshold:
            severity = "critical"
            status_icon = "🔴"
        elif performance_ratio >= self.warning_threshold:
            severity = "warning" 
            status_icon = "🟡"
        else:
            severity = "good"
            status_icon = "🟢"
            
        # Memory evaluation
        memory_status = "good"
        if metrics["memory_delta_mb"] > 100:  # >100MB increase
            memory_status = "high"
        elif metrics["memory_delta_mb"] > 50:  # >50MB increase
            memory_status = "moderate"
            
        return {
            "severity": severity,
            "status_icon": status_icon,
            "performance_ratio": performance_ratio,
            "target_ms": target_ms,
            "actual_ms": actual_ms,
            "memory_status": memory_status,
            "within_target": actual_ms <= target_ms,
            "efficiency_score": min(1.0, target_ms / actual_ms) if actual_ms > 0 else 1.0
        }
    
    def check_monitoring_overhead(self) -> Optional[Dict[str, Any]]:
        """Check if monitoring is within resource limits"""
        if not PSUTIL_AVAILABLE or not self.process:
            return None
            
        try:
            # Get current resource usage
            cpu_percent = self.process.cpu_percent(interval=0.01)
            memory_mb = self.process.memory_info().rss / 1024 / 1024
            
            # Check against limits
            cpu_limit = self.resource_limits.get("monitoring_overhead_cpu_percent", 2.0)
            memory_limit = self.resource_limits.get("monitoring_memory_mb", 50)
            
            overhead_status = {
                "cpu_percent": cpu_percent,
                "memory_mb": memory_mb,
                "cpu_limit": cpu_limit,
                "memory_limit": memory_limit,
                "cpu_within_limit": cpu_percent <= cpu_limit,
                "memory_within_limit": memory_mb <= memory_limit
            }
            
            # Log if exceeding limits
            if not overhead_status["cpu_within_limit"]:
                logger.warning(f"Monitoring CPU overhead ({cpu_percent:.1f}%) exceeds limit ({cpu_limit}%)")
            if not overhead_status["memory_within_limit"]:
                logger.warning(f"Monitoring memory usage ({memory_mb:.1f}MB) exceeds limit ({memory_limit}MB)")
                
            return overhead_status
            
        except Exception as e:
            logger.error(f"Failed to check monitoring overhead: {e}")
            return None
    
    def output_performance_report(self, metrics: Dict[str, Any], status: Dict[str, Any]):
        """Output color-coded performance report to stderr"""
        
        tool_name = metrics["tool_name"]
        operation_type = metrics["operation_type"]
        status_icon = status["status_icon"]
        actual_ms = status["actual_ms"]
        target_ms = status["target_ms"]
        efficiency = status["efficiency_score"] * 100
        
        # Main performance line
        print(f"{status_icon} {tool_name} ({operation_type}): {actual_ms:.0f}ms "
              f"(target: {target_ms}ms, efficiency: {efficiency:.0f}%)", file=sys.stderr)
        
        # Memory info if significant
        if metrics["memory_delta_mb"] > 10:  # Only show if >10MB change
            print(f"   💾 Memory: {metrics['memory_usage_mb']:.1f}MB "
                  f"(Δ{metrics['memory_delta_mb']:+.1f}MB)", file=sys.stderr)
        
        # CPU info if significant
        if metrics["cpu_percent"] > 50:  # Only show if >50% CPU
            print(f"   ⚡ CPU: {metrics['cpu_percent']:.1f}%", file=sys.stderr)
            
        # Performance warnings
        if status["severity"] == "critical":
            print(f"   🚨 CRITICAL: {status['performance_ratio']:.1f}x target exceeded", file=sys.stderr)
        elif status["severity"] == "warning":
            print(f"   ⚠️  WARNING: {status['performance_ratio']:.1f}x target approached", file=sys.stderr)
            
        # Check monitoring overhead periodically (every 10th execution)
        if hasattr(self, '_execution_count'):
            self._execution_count += 1
        else:
            self._execution_count = 1
            
        if self._execution_count % 10 == 0:
            overhead = self.check_monitoring_overhead()
            if overhead and (not overhead["cpu_within_limit"] or not overhead["memory_within_limit"]):
                print(f"   🔍 Monitor overhead: CPU {overhead['cpu_percent']:.1f}% (limit: {overhead['cpu_limit']}%), "
                      f"Memory {overhead['memory_mb']:.1f}MB (limit: {overhead['memory_limit']}MB)", file=sys.stderr)
    
    def store_metrics(self, metrics: Dict[str, Any], status: Dict[str, Any]):
        """Store metrics for historical trend analysis"""
        try:
            # Combine metrics and status for storage
            record = {**metrics, **status}
            
            # Append to metrics file
            with open(self.metrics_file, "a") as f:
                f.write(json.dumps(record) + "\n")
                
        except Exception as e:
            self.logger.error(f"Failed to store metrics: {e}")
    
    def generate_optimization_suggestions(self, metrics: Dict[str, Any], status: Dict[str, Any]):
        """Generate actionable optimization suggestions"""
        
        tool_name = metrics["tool_name"]
        operation_type = metrics["operation_type"]
        actual_ms = status["actual_ms"]
        
        suggestions = []
        
        # Tool-specific optimizations
        if tool_name == "Read" and actual_ms > 100:
            suggestions.append("Consider using Glob for file discovery before Read")
            suggestions.append("Check file size - large files may need streaming")
            
        elif tool_name == "Grep" and actual_ms > 200:
            suggestions.append("Simplify regex pattern or use literal search")
            suggestions.append("Add file type filters to reduce search scope")
            
        elif tool_name == "Write" and actual_ms > 500:
            suggestions.append("Check disk I/O performance")
            suggestions.append("Consider batching multiple writes")
            
        elif tool_name == "Bash" and actual_ms > 1000:
            suggestions.append("Break complex commands into simpler steps")
            suggestions.append("Use built-in tools instead of external commands")
            
        # Operation-type optimizations
        if operation_type == "memory_operations" and actual_ms > 200:
            suggestions.append("Check Serena MCP server responsiveness")
            suggestions.append("Consider memory caching for frequently accessed data")
            
        elif operation_type == "context_loading" and actual_ms > 500:
            suggestions.append("Implement context preloading")
            suggestions.append("Use selective context loading")
            
        # Memory optimizations
        if metrics["memory_delta_mb"] > 100:
            suggestions.append("Monitor memory leaks in long-running operations")
            suggestions.append("Consider processing data in chunks")
            
        # Output suggestions
        if suggestions:
            print(f"   💡 Optimization suggestions:", file=sys.stderr)
            for suggestion in suggestions[:3]:  # Limit to top 3
                print(f"      • {suggestion}", file=sys.stderr)
    
    def get_performance_history(self, operation_type: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Get performance history for trend analysis"""
        try:
            if not self.metrics_file.exists():
                return []
                
            cutoff_time = datetime.utcnow().timestamp() - (hours * 3600)
            history = []
            
            with open(self.metrics_file, "r") as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        record_time = datetime.fromisoformat(record["timestamp"]).timestamp()
                        
                        if (record_time >= cutoff_time and 
                            record.get("operation_type") == operation_type):
                            history.append(record)
                    except:
                        continue
                        
            return history[-100:]  # Return last 100 records
            
        except Exception as e:
            self.logger.error(f"Failed to load performance history: {e}")
            return []
    
    def process_pre_tool_use(self, tool_name: str, tool_args: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        Process PreToolUse event for performance monitoring.
        
        Records the start time for tool execution timing.
        
        Args:
            tool_name: Name of the tool being invoked
            tool_args: Arguments passed to the tool
            session_id: Current session identifier
            
        Returns:
            Dict with status and any messages
        """
        try:
            # Record start time for timing calculations
            self.start_time = time.time()
            
            # Log the tool invocation (removed debug call for compatibility)
            
            return {
                "status": "success",
                "message": f"Performance monitoring started for {tool_name}"
            }
            
        except Exception as e:
            self.logger.error(f"PreToolUse processing failed: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def process_post_tool_use(self, tool_name: str, tool_result: Any, tool_args: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        Process PostToolUse event for performance monitoring.
        
        Calculates execution time and monitors performance metrics.
        
        Args:
            tool_name: Name of the tool that was invoked
            tool_result: Result returned by the tool
            tool_args: Arguments that were passed to the tool
            session_id: Current session identifier
            
        Returns:
            Dict with status and performance metrics
        """
        try:
            # Calculate execution time
            if hasattr(self, 'start_time') and self.start_time:
                execution_time_ms = (time.time() - self.start_time) * 1000
                self.start_time = None
            else:
                execution_time_ms = 0
            
            # Store execution data for the main execute method
            self.input_data = {
                "tool": {
                    "name": tool_name,
                    "args": tool_args
                },
                "result": tool_result,
                "session_id": session_id,
                "execution_time_ms": execution_time_ms
            }
            
            # Run the main performance monitoring logic
            success = self.execute()
            
            return {
                "status": "success" if success else "warning",
                "execution_time_ms": execution_time_ms,
                "message": f"Performance monitored for {tool_name}"
            }
            
        except Exception as e:
            self.logger.error(f"PostToolUse processing failed: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

def main():
    """Main entry point for hook execution"""
    try:
        # Parse command line arguments
        if len(sys.argv) < 2:
            print("Usage: python hook.py <event> <tool_name> <tool_args> [session_id]", file=sys.stderr)
            sys.exit(1)
        
        event = sys.argv[1]
        
        # Create hook instance
        hook = PerformanceMonitorHook(input_data={})
        
        # Process event
        if event == "pre":
            # For pre event, arguments should be: pre <tool_name> <tool_args> <session_id>
            if len(sys.argv) < 4:
                print("Usage for pre: python hook.py pre <tool_name> <tool_args> [session_id]", file=sys.stderr)
                sys.exit(1)
                
            tool_name = sys.argv[2]
            tool_args_str = sys.argv[3] if len(sys.argv) > 3 else "{}"
            session_id = sys.argv[4] if len(sys.argv) > 4 else "default"
            
            # Parse tool args
            try:
                tool_args = json.loads(tool_args_str)
            except json.JSONDecodeError:
                tool_args = {"raw": tool_args_str}
            
            result = hook.process_pre_tool_use(tool_name, tool_args, session_id)
            
        elif event == "post":
            # For post event, arguments should be: post <tool_name> <tool_args> <session_id>
            # Note: tool_result is not passed on command line for performance monitor
            if len(sys.argv) < 4:
                print("Usage for post: python hook.py post <tool_name> <tool_args> [session_id]", file=sys.stderr)
                sys.exit(1)
                
            tool_name = sys.argv[2]
            tool_args_str = sys.argv[3] if len(sys.argv) > 3 else "{}"
            session_id = sys.argv[4] if len(sys.argv) > 4 else "default"
            
            # Parse tool args
            try:
                tool_args = json.loads(tool_args_str)
            except json.JSONDecodeError:
                tool_args = {"raw": tool_args_str}
            
            # For post event, we need the tool result - it might be in stdin
            tool_result = None
            if not sys.stdin.isatty():
                try:
                    input_text = sys.stdin.read().strip()
                    if input_text:
                        tool_result = json.loads(input_text)
                except:
                    tool_result = None
            
            result = hook.process_post_tool_use(tool_name, tool_result, tool_args, session_id)
            
        else:
            result = {
                "status": "error",
                "message": f"Unknown event type: {event}"
            }
        
        # Output result as JSON
        print(json.dumps(result, indent=2))
        
        # Exit with appropriate code
        sys.exit(0 if result.get('status') == 'success' else 1)
        
    except Exception as e:
        error_result = {
            'status': 'error',
            'hook': 'performance_monitor',
            'error': str(e),
            'message': 'Performance monitor hook execution failed'
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()