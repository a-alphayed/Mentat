#!/usr/bin/env python3
"""
SuperClaude Hooks Installation Script

Automatically installs SuperClaude hooks system to Claude Code CLI.
Handles:
- Hook file deployment to ~/.claude/SuperClaude/Hooks/
- Claude Code settings integration
- Configuration validation
- Installation verification

Usage:
    python SuperClaude/Hooks/scripts/install.py [--force] [--dry-run] [--quiet]
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("SuperClaude.Hooks.Installer")


class HooksInstaller:
    """
    SuperClaude Hooks installation manager.
    
    Handles complete installation process:
    - File deployment
    - Configuration integration
    - Validation and verification
    """
    
    def __init__(self, force: bool = False, dry_run: bool = False, quiet: bool = False):
        """
        Initialize installer.
        
        Args:
            force: Overwrite existing installations
            dry_run: Show what would be done without making changes
            quiet: Minimal output mode
        """
        self.force = force
        self.dry_run = dry_run
        self.quiet = quiet
        
        # Setup paths
        self.claude_home = Path.home() / ".claude"
        self.superclaude_root = self._find_superclaude_root()
        self.hooks_source = self.superclaude_root / "Hooks"
        self.hooks_target = self.claude_home / "SuperClaude" / "Hooks"
        self.settings_file = self.claude_home / "settings.json"
        
        if not quiet:
            logger.info(f"Claude home: {self.claude_home}")
            logger.info(f"SuperClaude root: {self.superclaude_root}")
    
    def _find_superclaude_root(self) -> Path:
        """Find SuperClaude root directory."""
        # Start from script location
        script_path = Path(__file__).parent
        current_path = script_path
        
        while current_path != current_path.parent:
            # Look for SuperClaude directory
            if (current_path / "SuperClaude").exists():
                return current_path / "SuperClaude"
            current_path = current_path.parent
        
        # Check current working directory
        if (Path.cwd() / "SuperClaude").exists():
            return Path.cwd() / "SuperClaude"
            
        raise RuntimeError("Could not find SuperClaude root directory")
    
    def _log(self, message: str, level: str = "info") -> None:
        """Log message if not in quiet mode."""
        if not self.quiet:
            getattr(logger, level)(message)
    
    def _ensure_directory(self, path: Path) -> bool:
        """Ensure directory exists."""
        if self.dry_run:
            self._log(f"Would create directory: {path}")
            return True
            
        try:
            path.mkdir(parents=True, exist_ok=True)
            self._log(f"Created directory: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {e}")
            return False
    
    def _copy_file(self, source: Path, target: Path) -> bool:
        """Copy file with validation."""
        if not source.exists():
            logger.error(f"Source file not found: {source}")
            return False
            
        if target.exists() and not self.force:
            logger.error(f"Target file exists (use --force to overwrite): {target}")
            return False
        
        if self.dry_run:
            self._log(f"Would copy: {source} -> {target}")
            return True
            
        try:
            # Ensure target directory exists
            self._ensure_directory(target.parent)
            
            shutil.copy2(source, target)
            self._log(f"Copied: {source.name} -> {target}")
            return True
        except Exception as e:
            logger.error(f"Failed to copy {source} to {target}: {e}")
            return False
    
    def _copy_directory(self, source: Path, target: Path) -> bool:
        """Copy directory recursively."""
        if not source.exists():
            logger.error(f"Source directory not found: {source}")
            return False
        
        if target.exists() and not self.force:
            logger.error(f"Target directory exists (use --force to overwrite): {target}")
            return False
        
        if self.dry_run:
            self._log(f"Would copy directory: {source} -> {target}")
            return True
            
        try:
            if target.exists():
                shutil.rmtree(target)
            
            shutil.copytree(source, target)
            self._log(f"Copied directory: {source} -> {target}")
            return True
        except Exception as e:
            logger.error(f"Failed to copy directory {source} to {target}: {e}")
            return False
    
    def _load_claude_settings(self) -> Optional[Dict[str, Any]]:
        """Load existing Claude Code settings."""
        if not self.settings_file.exists():
            return {}
            
        try:
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load Claude settings: {e}")
            return None
    
    def _save_claude_settings(self, settings: Dict[str, Any]) -> bool:
        """Save Claude Code settings."""
        if self.dry_run:
            self._log("Would update Claude Code settings")
            return True
            
        try:
            # Backup existing settings
            if self.settings_file.exists():
                backup_file = self.settings_file.with_suffix('.json.backup')
                shutil.copy2(self.settings_file, backup_file)
                self._log(f"Backed up settings to: {backup_file}")
            
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            self._log("Updated Claude Code settings")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save Claude settings: {e}")
            return False
    
    def _merge_hook_settings(self, existing_settings: Dict[str, Any]) -> Dict[str, Any]:
        """Merge SuperClaude hook settings with existing settings."""
        # Load SuperClaude hook configuration from template
        # First try the Config directory
        hook_settings_file = self.superclaude_root / "Config" / "claude-code-settings-template.json"
        if not hook_settings_file.exists():
            # Fallback to hooks config directory
            hook_settings_file = self.hooks_source / "config" / "claude-code-settings-template.json"
        
        if not hook_settings_file.exists():
            logger.error(f"Hook settings template not found: {hook_settings_file}")
            return existing_settings
        
        try:
            with open(hook_settings_file, 'r') as f:
                hook_settings = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load hook settings: {e}")
            return existing_settings
        
        # Merge settings - new format uses object structure for hooks
        merged = existing_settings.copy()
        
        # Handle hooks in the new format (object with event names as keys)
        if 'hooks' not in merged or not isinstance(merged['hooks'], dict):
            merged['hooks'] = {}
        
        # Merge hook configuration from template
        if 'hooks' in hook_settings:
            for event_name, event_hooks in hook_settings['hooks'].items():
                if event_name not in merged['hooks']:
                    merged['hooks'][event_name] = []
                
                # Remove existing SuperClaude matchers to avoid duplicates
                existing_matchers = []
                for matcher_group in merged['hooks'][event_name]:
                    # Check if any hooks mention SuperClaude
                    has_superclaude = False
                    if 'hooks' in matcher_group:
                        for hook in matcher_group['hooks']:
                            if 'SuperClaude' in hook.get('command', ''):
                                has_superclaude = True
                                break
                    if not has_superclaude:
                        existing_matchers.append(matcher_group)
                
                # Add new matchers from template
                merged['hooks'][event_name] = existing_matchers + event_hooks
        
        # Remove 'superclaude' field as it's not supported by Claude Code
        if 'superclaude' in merged:
            del merged['superclaude']
        
        return merged
    
    def install_files(self) -> bool:
        """Install hook files to Claude home directory."""
        self._log("Installing SuperClaude Hooks files...")
        
        if not self.hooks_source.exists():
            logger.error(f"Hooks source directory not found: {self.hooks_source}")
            return False
        
        # Ensure target directory exists
        if not self._ensure_directory(self.hooks_target):
            return False
        
        # Copy hook directories
        hook_dirs = ['common', 'framework_coordinator', 'session_lifecycle', 'quality_gates', 'performance_monitor']
        
        for hook_dir in hook_dirs:
            source_dir = self.hooks_source / hook_dir
            target_dir = self.hooks_target / hook_dir
            
            if source_dir.exists():
                if not self._copy_directory(source_dir, target_dir):
                    return False
            else:
                logger.warning(f"Hook directory not found: {source_dir}")
        
        # Copy other important files
        files_to_copy = [
            '__init__.py',
            'README.md'
        ]
        
        for filename in files_to_copy:
            source_file = self.hooks_source / filename
            target_file = self.hooks_target / filename
            
            if source_file.exists():
                if not self._copy_file(source_file, target_file):
                    return False
        
        # Copy config and scripts directories
        for dir_name in ['config', 'scripts']:
            source_dir = self.hooks_source / dir_name
            target_dir = self.hooks_target / dir_name
            
            if source_dir.exists():
                if not self._copy_directory(source_dir, target_dir):
                    return False
        
        self._log("Successfully installed hook files")
        return True
    
    def install_settings(self) -> bool:
        """Install hook settings to Claude Code configuration."""
        self._log("Installing SuperClaude Hooks settings...")
        
        # Load existing settings
        existing_settings = self._load_claude_settings()
        if existing_settings is None:
            return False
        
        # Merge with hook settings
        merged_settings = self._merge_hook_settings(existing_settings)
        
        # Save updated settings
        if not self._save_claude_settings(merged_settings):
            return False
        
        # Also install SuperClaude configuration file
        superclaude_config_template = self.superclaude_root / "Config" / "superclaude-config-template.json"
        if not superclaude_config_template.exists():
            superclaude_config_template = self.hooks_source / "config" / "superclaude-config-template.json"
        
        if superclaude_config_template.exists():
            superclaude_config_target = self.claude_home / "superclaude-config.json"
            
            # Only copy if it doesn't exist or if force is set
            if not superclaude_config_target.exists() or self.force:
                if self.dry_run:
                    self._log(f"Would copy SuperClaude config: {superclaude_config_template} -> {superclaude_config_target}")
                else:
                    try:
                        shutil.copy2(superclaude_config_template, superclaude_config_target)
                        self._log(f"Installed SuperClaude configuration: {superclaude_config_target}")
                    except Exception as e:
                        logger.error(f"Failed to copy SuperClaude config: {e}")
                        return False
            else:
                self._log("SuperClaude config already exists (use --force to overwrite)")
        else:
            logger.warning("SuperClaude config template not found")
        
        return True
    
    def validate_installation(self) -> bool:
        """Validate that installation was successful."""
        self._log("Validating installation...")
        
        # Check that hook files exist
        required_files = [
            self.hooks_target / '__init__.py',
            self.hooks_target / 'common' / 'base_hook.py',
            self.hooks_target / 'common' / 'framework_parser.py'
        ]
        
        for file_path in required_files:
            if not file_path.exists():
                logger.error(f"Required file missing: {file_path}")
                return False
        
        # Check that settings were updated
        settings = self._load_claude_settings()
        if settings is None:
            return False
        
        # Check for SuperClaude hooks in new format
        hooks = settings.get('hooks', {})
        if not isinstance(hooks, dict):
            logger.error("Hooks configuration is not in the correct format (should be object, not array)")
            return False
        
        # Count SuperClaude hooks across all events
        superclaude_hook_count = 0
        for event_name, event_hooks in hooks.items():
            for matcher_group in event_hooks:
                if 'hooks' in matcher_group:
                    for hook in matcher_group['hooks']:
                        if 'SuperClaude' in hook.get('command', ''):
                            superclaude_hook_count += 1
        
        if superclaude_hook_count == 0:
            logger.error("No SuperClaude hooks found in Claude settings")
            return False
        
        # Check for SuperClaude configuration file
        superclaude_config_file = self.claude_home / "superclaude-config.json"
        if not superclaude_config_file.exists():
            logger.error("SuperClaude configuration file not found")
            return False
        
        self._log(f"Found {superclaude_hook_count} SuperClaude hooks in configuration")
        self._log("Installation validation successful")
        return True
    
    def install(self) -> bool:
        """Run complete installation process."""
        self._log("Starting SuperClaude Hooks installation...")
        
        if self.dry_run:
            self._log("DRY RUN MODE - No changes will be made")
        
        # Install files
        if not self.install_files():
            logger.error("Failed to install hook files")
            return False
        
        # Install settings
        if not self.install_settings():
            logger.error("Failed to install hook settings")
            return False
        
        # Validate installation
        if not self.dry_run and not self.validate_installation():
            logger.error("Installation validation failed")
            return False
        
        if self.dry_run:
            self._log("DRY RUN: Installation would complete successfully")
        else:
            self._log("SuperClaude Hooks installation completed successfully!")
            self._log("Restart Claude Code CLI to activate hooks")
        
        return True


def main():
    """Main installation function."""
    parser = argparse.ArgumentParser(
        description="Install SuperClaude Hooks system to Claude Code CLI"
    )
    parser.add_argument(
        "--force", 
        action="store_true", 
        help="Overwrite existing installations"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--quiet", 
        action="store_true", 
        help="Minimal output mode"
    )
    
    args = parser.parse_args()
    
    # Create installer
    try:
        installer = HooksInstaller(
            force=args.force,
            dry_run=args.dry_run,
            quiet=args.quiet
        )
    except Exception as e:
        logger.error(f"Failed to initialize installer: {e}")
        sys.exit(1)
    
    # Run installation
    success = installer.install()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()