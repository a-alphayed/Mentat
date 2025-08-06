"""
Unified Configuration Loader for SuperClaude-Lite

High-performance configuration loading with support for both JSON and YAML formats,
caching, hot-reload capabilities, and comprehensive error handling.

Supports:
- Claude Code settings.json (JSON format)
- SuperClaude superclaude-config.json (JSON format) 
- YAML configuration files
- Unified configuration interface for hooks
"""

import os
import json
import yaml
import time
import hashlib
from typing import Dict, Any, Optional, Union
from pathlib import Path


class UnifiedConfigLoader:
    """
    Intelligent configuration loader with support for JSON and YAML formats.
    
    Features:
    - Dual-configuration support (Claude Code + SuperClaude)
    - File modification detection for hot-reload
    - In-memory caching for performance (<10ms access)
    - Comprehensive error handling and validation
    - Environment variable interpolation
    - Include/merge support for modular configs
    - Unified configuration interface
    """
    
    def __init__(self, project_root: Union[str, Path]):
        self.project_root = Path(project_root)
        self.config_dir = self.project_root / "config"
        
        # Configuration file paths
        self.claude_settings_path = self.project_root / "settings.json"
        self.superclaude_config_path = self.project_root / "superclaude-config.json"
        
        # Cache for all configuration sources
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._file_hashes: Dict[str, str] = {}
        self._last_check: Dict[str, float] = {}
        self.check_interval = 1.0  # Check files every 1 second max
        
        # Configuration source registry
        self._config_sources = {
            'claude_settings': self.claude_settings_path,
            'superclaude_config': self.superclaude_config_path
        }
        
    def load_config(self, config_name: str, force_reload: bool = False) -> Dict[str, Any]:
        """
        Load configuration with intelligent caching (supports JSON and YAML).
        
        Args:
            config_name: Name of config file or special config identifier
                        - For YAML: config file name without .yaml extension
                        - For JSON: 'claude_settings' or 'superclaude_config'
            force_reload: Force reload even if cached
            
        Returns:
            Parsed configuration dictionary
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config parsing fails
        """
        # Handle special configuration sources
        if config_name in self._config_sources:
            return self._load_json_config(config_name, force_reload)
        
        # Handle YAML configuration files
        config_path = self.config_dir / f"{config_name}.yaml"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        # Check if we need to reload
        if not force_reload and self._should_use_cache(config_name, config_path):
            return self._cache[config_name]
        
        # Load and parse the YAML configuration
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Environment variable interpolation
            content = self._interpolate_env_vars(content)
            
            # Parse YAML
            config = yaml.safe_load(content)
            
            # Handle includes/merges
            config = self._process_includes(config, config_path.parent)
            
            # Update cache
            self._cache[config_name] = config
            self._file_hashes[config_name] = self._compute_hash(config_path)
            self._last_check[config_name] = time.time()
            
            return config
            
        except yaml.YAMLError as e:
            raise ValueError(f"YAML parsing error in {config_path}: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading config {config_name}: {e}")
    
    def _load_json_config(self, config_name: str, force_reload: bool = False) -> Dict[str, Any]:
        """Load JSON configuration file."""
        config_path = self._config_sources[config_name]
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        # Check if we need to reload
        if not force_reload and self._should_use_cache(config_name, config_path):
            return self._cache[config_name]
        
        # Load and parse the JSON configuration
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Environment variable interpolation
            content = self._interpolate_env_vars(content)
            
            # Parse JSON
            config = json.loads(content)
            
            # Update cache
            self._cache[config_name] = config
            self._file_hashes[config_name] = self._compute_hash(config_path)
            self._last_check[config_name] = time.time()
            
            return config
            
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON parsing error in {config_path}: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading JSON config {config_name}: {e}")
    
    def get_section(self, config_name: str, section_path: str, default: Any = None) -> Any:
        """
        Get specific section from configuration using dot notation.
        
        Args:
            config_name: Configuration file name or identifier
            section_path: Dot-separated path (e.g., 'routing.ui_components')
            default: Default value if section not found
            
        Returns:
            Configuration section value or default
        """
        config = self.load_config(config_name)
        
        try:
            result = config
            for key in section_path.split('.'):
                result = result[key]
            return result
        except (KeyError, TypeError):
            return default
    
    def get_hook_config(self, hook_name: str, section_path: str = None, default: Any = None) -> Any:
        """
        Get hook-specific configuration from SuperClaude config.
        
        Args:
            hook_name: Hook name (e.g., 'session_start', 'pre_tool_use')
            section_path: Optional dot-separated path within hook config
            default: Default value if not found
            
        Returns:
            Hook configuration or specific section
        """
        base_path = f"hook_configurations.{hook_name}"
        if section_path:
            full_path = f"{base_path}.{section_path}"
        else:
            full_path = base_path
            
        return self.get_section('superclaude_config', full_path, default)
    
    def get_claude_hooks(self) -> Dict[str, Any]:
        """Get Claude Code hook definitions from settings.json."""
        return self.get_section('claude_settings', 'hooks', {})
    
    def get_superclaude_config(self, section_path: str = None, default: Any = None) -> Any:
        """
        Get SuperClaude framework configuration.
        
        Args:
            section_path: Optional dot-separated path (e.g., 'global_configuration.performance_monitoring')
            default: Default value if not found
            
        Returns:
            Configuration section or full config if no path specified
        """
        if section_path:
            return self.get_section('superclaude_config', section_path, default)
        else:
            return self.load_config('superclaude_config')
    
    def get_mcp_server_config(self, server_name: str = None) -> Dict[str, Any]:
        """
        Get MCP server configuration.
        
        Args:
            server_name: Optional specific server name
            
        Returns:
            MCP server configuration
        """
        if server_name:
            return self.get_section('superclaude_config', f'mcp_server_integration.servers.{server_name}', {})
        else:
            return self.get_section('superclaude_config', 'mcp_server_integration', {})
    
    def get_performance_targets(self) -> Dict[str, Any]:
        """Get performance targets for all components."""
        return self.get_section('superclaude_config', 'global_configuration.performance_monitoring', {})
    
    def is_hook_enabled(self, hook_name: str) -> bool:
        """Check if a specific hook is enabled."""
        return self.get_hook_config(hook_name, 'enabled', False)
    
    def reload_all(self) -> None:
        """Force reload of all cached configurations."""
        for config_name in list(self._cache.keys()):
            self.load_config(config_name, force_reload=True)
    
    def _should_use_cache(self, config_name: str, config_path: Path) -> bool:
        """Check if cached version is still valid."""
        if config_name not in self._cache:
            return False
        
        # Rate limit file checks
        now = time.time()
        if now - self._last_check.get(config_name, 0) < self.check_interval:
            return True
        
        # Check if file changed
        current_hash = self._compute_hash(config_path)
        return current_hash == self._file_hashes.get(config_name)
    
    def _compute_hash(self, file_path: Path) -> str:
        """Compute file hash for change detection."""
        stat = file_path.stat()
        return hashlib.md5(f"{stat.st_mtime}:{stat.st_size}".encode()).hexdigest()
    
    def _interpolate_env_vars(self, content: str) -> str:
        """Replace environment variables in YAML content."""
        import re
        
        def replace_env_var(match):
            var_name = match.group(1)
            default_value = match.group(2) if match.group(2) else ""
            return os.getenv(var_name, default_value)
        
        # Support ${VAR} and ${VAR:default} syntax
        pattern = r'\$\{([^}:]+)(?::([^}]*))?\}'
        return re.sub(pattern, replace_env_var, content)
    
    def _process_includes(self, config: Dict[str, Any], base_dir: Path) -> Dict[str, Any]:
        """Process include directives in configuration."""
        if not isinstance(config, dict):
            return config
        
        # Handle special include key
        if '__include__' in config:
            includes = config.pop('__include__')
            if isinstance(includes, str):
                includes = [includes]
            
            for include_file in includes:
                include_path = base_dir / include_file
                if include_path.exists():
                    with open(include_path, 'r', encoding='utf-8') as f:
                        included_config = yaml.safe_load(f.read())
                    if isinstance(included_config, dict):
                        # Merge included config (current config takes precedence)
                        included_config.update(config)
                        config = included_config
        
        return config
    
    def get_intelligence_config(self, intelligence_type: str, section_path: str = None, default: Any = None) -> Any:
        """
        Get intelligence configuration from YAML patterns.
        
        Args:
            intelligence_type: Type of intelligence config (e.g., 'intelligence_patterns', 'mcp_orchestration')
            section_path: Optional dot-separated path within intelligence config
            default: Default value if not found
            
        Returns:
            Intelligence configuration or specific section
        """
        try:
            config = self.load_config(intelligence_type)
            
            if section_path:
                result = config
                for key in section_path.split('.'):
                    result = result[key]
                return result
            else:
                return config
                
        except (FileNotFoundError, KeyError, TypeError):
            return default
    
    def get_pattern_dimensions(self) -> Dict[str, Any]:
        """Get pattern recognition dimensions from intelligence patterns."""
        return self.get_intelligence_config(
            'intelligence_patterns', 
            'learning_intelligence.pattern_recognition.dimensions', 
            {'primary': ['context_type', 'complexity_score', 'operation_type'], 'secondary': []}
        )
    
    def get_mcp_orchestration_rules(self) -> Dict[str, Any]:
        """Get MCP server orchestration rules."""
        return self.get_intelligence_config(
            'mcp_orchestration', 
            'server_selection.decision_tree', 
            []
        )
    
    def get_hook_coordination_patterns(self) -> Dict[str, Any]:
        """Get hook coordination execution patterns."""
        return self.get_intelligence_config(
            'hook_coordination', 
            'execution_patterns', 
            {}
        )
    
    def get_performance_zones(self) -> Dict[str, Any]:
        """Get performance management resource zones."""
        return self.get_intelligence_config(
            'performance_intelligence',
            'resource_management.resource_zones',
            {}
        )
    
    def get_validation_health_config(self) -> Dict[str, Any]:
        """Get validation and health scoring configuration."""
        return self.get_intelligence_config(
            'validation_intelligence',
            'health_scoring',
            {}
        )
    
    def get_ux_project_patterns(self) -> Dict[str, Any]:
        """Get user experience project detection patterns."""
        return self.get_intelligence_config(
            'user_experience',
            'project_detection.detection_patterns',
            {}
        )
    
    def get_intelligence_summary(self) -> Dict[str, Any]:
        """Get summary of all available intelligence configurations."""
        intelligence_types = [
            'intelligence_patterns',
            'mcp_orchestration', 
            'hook_coordination',
            'performance_intelligence',
            'validation_intelligence',
            'user_experience'
        ]
        
        summary = {}
        for intelligence_type in intelligence_types:
            try:
                config = self.load_config(intelligence_type)
                summary[intelligence_type] = {
                    'loaded': True,
                    'version': config.get('version', 'unknown'),
                    'last_updated': config.get('last_updated', 'unknown'),
                    'sections': list(config.keys()) if isinstance(config, dict) else []
                }
            except Exception:
                summary[intelligence_type] = {
                    'loaded': False,
                    'error': 'Failed to load configuration'
                }
        
        return summary
    
    def reload_intelligence_configs(self) -> Dict[str, bool]:
        """Force reload all intelligence configurations and return status."""
        intelligence_types = [
            'intelligence_patterns',
            'mcp_orchestration', 
            'hook_coordination',
            'performance_intelligence',
            'validation_intelligence',
            'user_experience'
        ]
        
        reload_status = {}
        for intelligence_type in intelligence_types:
            try:
                self.load_config(intelligence_type, force_reload=True)
                reload_status[intelligence_type] = True
            except Exception as e:
                reload_status[intelligence_type] = False
                print(f"Warning: Could not reload {intelligence_type}: {e}")
        
        return reload_status


# Global instance for shared use across hooks
# Use Claude installation directory instead of current working directory
import os
config_loader = UnifiedConfigLoader(os.path.expanduser("~/.claude"))