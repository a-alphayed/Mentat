"""
Framework Parser for SuperClaude Hooks System

Parses SuperClaude .md configuration files to extract:
- Auto-activation rules from ORCHESTRATOR.md
- Compliance patterns from RULES.md  
- Session lifecycle triggers from SESSION_LIFECYCLE.md
- Performance targets and quality gates
- MCP server coordination patterns

Provides structured access to framework configuration for hooks.
"""

import re
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import logging
from utils import extract_yaml_frontmatter, find_superclaude_root

logger = logging.getLogger("SuperClaude.Hooks.FrameworkParser")


class FrameworkParser:
    """
    Parser for SuperClaude framework configuration files.
    
    Extracts structured data from .md files for use by hooks:
    - Auto-activation rules and routing patterns
    - Framework compliance rules
    - Performance targets and quality gates
    - Session lifecycle triggers
    - MCP server coordination patterns
    """
    
    def __init__(self, superclaude_root: Optional[Path] = None):
        """
        Initialize framework parser.
        
        Args:
            superclaude_root: Path to SuperClaude root directory
        """
        self.root = superclaude_root or find_superclaude_root()
        if not self.root:
            raise RuntimeError("Could not find SuperClaude root directory")
            
        self.core_path = self.root / "Core"
        if not self.core_path.exists():
            raise RuntimeError(f"SuperClaude Core directory not found: {self.core_path}")
            
        # Cache for parsed configurations
        self._cache = {}
        
        logger.info(f"Initialized FrameworkParser with root: {self.root}")
    
    def _load_file(self, filename: str) -> Optional[str]:
        """Load content from framework file."""
        file_path = self.core_path / filename
        if not file_path.exists():
            logger.warning(f"Framework file not found: {filename}")
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to load {filename}: {e}")
            return None
    
    def _extract_yaml_blocks(self, content: str) -> List[Dict[str, Any]]:
        """Extract YAML code blocks from markdown content."""
        yaml_blocks = []
        
        # Find all ```yaml ... ``` blocks
        pattern = r'```yaml\s*\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            try:
                # Clean up the YAML content
                yaml_content = match.strip()
                if yaml_content:
                    parsed = yaml.safe_load(yaml_content)
                    if parsed:
                        yaml_blocks.append(parsed)
            except yaml.YAMLError as e:
                logger.warning(f"Failed to parse YAML block: {e}")
                continue
                
        return yaml_blocks
    
    def _extract_rules_from_section(self, content: str, section_title: str) -> List[str]:
        """Extract rules from a specific section."""
        rules = []
        
        # Find the section
        section_pattern = rf'### {re.escape(section_title)}.*?\n(.*?)(?=### |\n## |\Z)'
        section_match = re.search(section_pattern, content, re.DOTALL)
        
        if not section_match:
            return rules
            
        section_content = section_match.group(1)
        
        # Extract bullet points and numbered items
        rule_patterns = [
            r'^- (.+)$',  # Bullet points
            r'^\d+\. (.+)$',  # Numbered lists
            r'^  - (.+)$',  # Sub-bullet points
        ]
        
        for line in section_content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                for pattern in rule_patterns:
                    match = re.match(pattern, line)
                    if match:
                        rule = match.group(1).strip()
                        if rule:
                            rules.append(rule)
                        break
        
        return rules
    
    def _extract_performance_targets(self, content: str) -> Dict[str, Any]:
        """Extract performance targets from content."""
        targets = {}
        
        # Look for patterns like "<100ms", "≥90%", etc.
        patterns = {
            'timing_ms': r'<(\d+)ms',
            'percentage': r'[≥>](\d+)%',
            'memory_ms': r'<(\d+)ms memory',
            'load_ms': r'<(\d+)ms load',
        }
        
        for target_type, pattern in patterns.items():
            matches = re.findall(pattern, content)
            if matches:
                targets[target_type] = [int(match) for match in matches]
        
        return targets
    
    def get_orchestrator_config(self) -> Dict[str, Any]:
        """
        Parse ORCHESTRATOR.md to extract routing and auto-activation rules.
        
        Returns:
            Dictionary with orchestrator configuration
        """
        if 'orchestrator' in self._cache:
            return self._cache['orchestrator']
            
        content = self._load_file("ORCHESTRATOR.md")
        if not content:
            return {}
            
        config = {
            'pattern_matching': {},
            'resource_zones': {},
            'mcp_servers': {},
            'auto_activation_rules': {},
            'yaml_blocks': []
        }
        
        # Extract YAML blocks
        config['yaml_blocks'] = self._extract_yaml_blocks(content)
        
        # Extract pattern matching rules
        pattern_section = re.search(r'## 🎯 Quick Pattern Matching.*?\n```yaml\s*\n(.*?)\n```', content, re.DOTALL)
        if pattern_section:
            try:
                pattern_yaml = yaml.safe_load(pattern_section.group(1))
                config['pattern_matching'] = pattern_yaml or {}
            except yaml.YAMLError:
                pass
        
        # Extract resource zones
        resource_section = re.search(r'## 🚦 Resource Management.*?\n```yaml\s*\n(.*?)\n```', content, re.DOTALL)
        if resource_section:
            try:
                resource_yaml = yaml.safe_load(resource_section.group(1))
                config['resource_zones'] = resource_yaml or {}
            except yaml.YAMLError:
                pass
        
        # Extract auto-activation rules
        auto_activation_section = re.search(r'## ⚡ Auto-Activation Rules.*?\n```yaml\s*\n(.*?)\n```', content, re.DOTALL)
        if auto_activation_section:
            try:
                auto_yaml = yaml.safe_load(auto_activation_section.group(1))
                config['auto_activation_rules'] = auto_yaml or {}
            except yaml.YAMLError:
                pass
        
        self._cache['orchestrator'] = config
        return config
    
    def get_rules_config(self) -> Dict[str, Any]:
        """
        Parse RULES.md to extract framework compliance rules.
        
        Returns:
            Dictionary with rules configuration
        """
        if 'rules' in self._cache:
            return self._cache['rules']
            
        content = self._load_file("RULES.md")
        if not content:
            return {}
            
        config = {
            'task_management_rules': [],
            'file_operation_rules': [],
            'framework_compliance_rules': [],
            'session_lifecycle_rules': [],
            'quality_rules': [],
            'performance_targets': {}
        }
        
        # Extract rules from different sections
        sections = {
            'task_management_rules': 'Task Management Rules',
            'file_operation_rules': 'File Operation Security',
            'framework_compliance_rules': 'Framework Compliance',
            'session_lifecycle_rules': 'Session Lifecycle Rules',
        }
        
        for config_key, section_title in sections.items():
            config[config_key] = self._extract_rules_from_section(content, section_title)
        
        # Extract performance targets
        config['performance_targets'] = self._extract_performance_targets(content)
        
        self._cache['rules'] = config
        return config
    
    def get_session_lifecycle_config(self) -> Dict[str, Any]:
        """
        Parse SESSION_LIFECYCLE.md to extract session management patterns.
        
        Returns:
            Dictionary with session lifecycle configuration
        """
        if 'session_lifecycle' in self._cache:
            return self._cache['session_lifecycle']
            
        content = self._load_file("SESSION_LIFECYCLE.md")
        if not content:
            return {}
            
        config = {
            'session_states': [],
            'checkpoint_triggers': [],
            'performance_targets': {},
            'memory_organization': {},
            'yaml_blocks': []
        }
        
        # Extract YAML blocks
        config['yaml_blocks'] = self._extract_yaml_blocks(content)
        
        # Extract session states
        states_section = re.search(r'## Session States.*?\n(.*?)(?=## |\Z)', content, re.DOTALL)
        if states_section:
            # Look for state definitions like "### 1. INITIALIZING"
            state_pattern = r'### \d+\. (\w+)'
            states = re.findall(state_pattern, states_section.group(1))
            config['session_states'] = states
        
        # Extract checkpoint triggers
        checkpoint_section = re.search(r'### Automatic Checkpoint Triggers.*?\n(.*?)(?=### |\n## |\Z)', content, re.DOTALL)
        if checkpoint_section:
            config['checkpoint_triggers'] = self._extract_rules_from_section(checkpoint_section.group(1), '')
        
        # Extract performance targets
        config['performance_targets'] = self._extract_performance_targets(content)
        
        self._cache['session_lifecycle'] = config
        return config
    
    def get_quality_gates_config(self) -> Dict[str, Any]:
        """
        Extract quality gates configuration from various framework files.
        
        Returns:
            Dictionary with quality gates configuration
        """
        if 'quality_gates' in self._cache:
            return self._cache['quality_gates']
            
        config = {
            'validation_steps': [],
            'quality_targets': {},
            'validation_triggers': []
        }
        
        # Look for quality gates in multiple files
        files_to_check = ["ORCHESTRATOR.md", "RULES.md", "PRINCIPLES.md"]
        
        for filename in files_to_check:
            content = self._load_file(filename)
            if not content:
                continue
                
            # Look for quality gate sections
            quality_sections = re.findall(r'quality.gate.*?\n(.*?)(?=\n\n|\n#|\Z)', content, re.DOTALL | re.IGNORECASE)
            for section in quality_sections:
                steps = self._extract_rules_from_section(section, '')
                config['validation_steps'].extend(steps)
        
        # Extract quality targets
        for filename in files_to_check:
            content = self._load_file(filename)
            if content:
                targets = self._extract_performance_targets(content)
                config['quality_targets'].update(targets)
        
        self._cache['quality_gates'] = config
        return config
    
    def get_mcp_server_patterns(self) -> Dict[str, Any]:
        """
        Extract MCP server usage patterns from framework configuration.
        
        Returns:
            Dictionary with MCP server patterns
        """
        if 'mcp_patterns' in self._cache:
            return self._cache['mcp_patterns']
            
        orchestrator_config = self.get_orchestrator_config()
        
        config = {
            'server_selection_rules': {},
            'activation_patterns': {},
            'coordination_patterns': {}
        }
        
        # Extract from orchestrator pattern matching
        if 'pattern_matching' in orchestrator_config:
            for pattern, action in orchestrator_config['pattern_matching'].items():
                if '→' in str(action):
                    parts = str(action).split('→')
                    if len(parts) == 2:
                        keywords = parts[0].strip()
                        servers_and_actions = parts[1].strip()
                        config['server_selection_rules'][pattern] = {
                            'keywords': keywords,
                            'action': servers_and_actions
                        }
        
        self._cache['mcp_patterns'] = config
        return config
    
    def should_activate_mcp_server(self, server_name: str, context: Dict[str, Any]) -> bool:
        """
        Check if MCP server should be activated based on context.
        
        Args:
            server_name: Name of MCP server (e.g., 'serena', 'sequential')
            context: Context dictionary with tool info, file counts, etc.
            
        Returns:
            True if server should be activated
        """
        orchestrator_config = self.get_orchestrator_config()
        
        # Check auto-activation rules
        auto_rules = orchestrator_config.get('auto_activation_rules', {})
        
        server_rules = {
            'serena': ['file count >10', 'symbol operations', 'multi-language projects'],
            'sequential': ['complex analysis', 'system design', 'multi-step problems'],
            'magic': ['ui components', 'design systems', 'frontend'],
            'morphllm': ['pattern edits', 'token optimization', 'simple edits'],
            'context7': ['library docs', 'framework patterns', 'best practices'],
            'playwright': ['browser testing', 'e2e validation', 'visual testing']
        }
        
        if server_name.lower() not in server_rules:
            return False
            
        rules = server_rules[server_name.lower()]
        
        # Check context against rules
        for rule in rules:
            if 'file count' in rule and context.get('file_count', 0) > 10:
                return True
            if 'symbol operations' in rule and context.get('has_symbol_operations', False):
                return True
            if 'ui components' in rule and context.get('is_ui_related', False):
                return True
            if 'complex analysis' in rule and context.get('complexity_score', 0) > 0.7:
                return True
                
        return False
    
    def get_compliance_violations(self, tool_name: str, tool_args: Dict[str, Any]) -> List[str]:
        """
        Check for framework compliance violations.
        
        Args:
            tool_name: Name of tool being used
            tool_args: Arguments passed to tool
            
        Returns:
            List of compliance violations found
        """
        violations = []
        rules_config = self.get_rules_config()
        
        # Check file operation rules
        file_rules = rules_config.get('file_operation_rules', [])
        
        for rule in file_rules:
            if 'Read tool before Write or Edit' in rule:
                if tool_name in ['Write', 'Edit', 'MultiEdit']:
                    # This would require state tracking to properly validate
                    # For now, just log the rule that should be checked
                    violations.append(f"Should validate Read before {tool_name}")
                    
            if 'absolute paths only' in rule:
                file_path = tool_args.get('file_path', '')
                if file_path and not (file_path.startswith('/') or file_path.startswith('C:')):
                    violations.append(f"Relative path detected: {file_path}")
        
        return violations
    
    def get_checkpoint_triggers(self) -> List[str]:
        """
        Get list of automatic checkpoint triggers.
        
        Returns:
            List of checkpoint trigger conditions
        """
        session_config = self.get_session_lifecycle_config()
        return session_config.get('checkpoint_triggers', [])
    
    def should_create_checkpoint(self, context: Dict[str, Any]) -> bool:
        """
        Check if automatic checkpoint should be created.
        
        Args:
            context: Context with session info, time elapsed, task status, etc.
            
        Returns:
            True if checkpoint should be created
        """
        triggers = self.get_checkpoint_triggers()
        
        for trigger in triggers:
            if '30 minutes' in trigger and context.get('time_elapsed_minutes', 0) >= 30:
                return True
            if 'high priority task' in trigger and context.get('task_priority') == 'high' and context.get('task_completed'):
                return True
            if 'risk level' in trigger and context.get('risk_level', 'low') in ['high', 'critical']:
                return True
                
        return False
    
    def get_performance_targets(self) -> Dict[str, Any]:
        """
        Get consolidated performance targets from all framework files.
        
        Returns:
            Dictionary with all performance targets
        """
        targets = {}
        
        # Collect from all configs
        for config_name in ['rules', 'session_lifecycle', 'orchestrator']:
            config = getattr(self, f'get_{config_name}_config')()
            config_targets = config.get('performance_targets', {})
            targets.update(config_targets)
        
        # Add known targets from framework
        default_targets = {
            'hook_execution_ms': [100],
            'memory_operations_ms': [200],
            'session_load_ms': [500],
            'context_retention_percent': [90],
            'framework_compliance_percent': [95]
        }
        
        for key, value in default_targets.items():
            if key not in targets:
                targets[key] = value
                
        return targets
    
    def refresh_cache(self) -> None:
        """Clear cached configurations to force re-parsing."""
        self._cache.clear()
        logger.info("Framework parser cache cleared")