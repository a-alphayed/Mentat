"""
Mentat Extensions Component
Installs Mentat-specific agents and commands for dotfiles synchronization
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import shutil
from ..core.base import Component
from ..utils.logger import get_logger
from ..utils.mentat_config import MentatConfig
from ..utils.claude_config import ClaudeConfigManager


class MentatExtensionsComponent(Component):
    """Component for installing Mentat user-facing extensions"""
    
    def __init__(self, install_dir: Path = None):
        # Find the mentat-extensions directory relative to the setup module
        self.extensions_dir = Path(__file__).parent.parent.parent / "mentat-extensions"
        super().__init__(install_dir)
        self.logger = get_logger()
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get component metadata"""
        return {
            "name": "mentat",
            "description": "Mentat dotfiles synchronization system (agents, commands, and scripts)",
            "version": "1.0.0",
            "category": "extensions",
            "author": "Mentat Framework",
            "size": self._calculate_size()
        }
    
    def get_dependencies(self) -> List[str]:
        """Mentat extensions depend on core being installed"""
        return ["core"]
    
    def validate_prerequisites(self) -> bool:
        """Check if mentat-extensions directory exists"""
        if not self.extensions_dir.exists():
            self.logger.error(f"mentat-extensions directory not found at {self.extensions_dir}")
            return False
        return True
    
    def _get_source_dir(self) -> Path:
        """Get source directory for Mentat extensions"""
        # Return the mentat-extensions directory
        return self.extensions_dir
    
    def _install(self, config: Dict[str, Any]) -> bool:
        """Perform Mentat extensions installation"""
        try:
            # Ensure target directories exist
            commands_dir = self.install_dir / "commands" / "mentat"
            agents_dir = self.install_dir / "agents"
            scripts_dir = self.install_dir / "scripts"
            
            commands_dir.mkdir(parents=True, exist_ok=True)
            agents_dir.mkdir(parents=True, exist_ok=True)
            scripts_dir.mkdir(parents=True, exist_ok=True)
            
            installed_items = []
            
            # Install commands
            commands_source = self.extensions_dir / "commands"
            if commands_source.exists():
                for cmd_file in commands_source.glob("*.md"):
                    target = commands_dir / cmd_file.name
                    shutil.copy2(cmd_file, target)
                    installed_items.append(f"Command: /mentat:{cmd_file.stem}")
                    self.logger.debug(f"Installed command: {cmd_file.name}")
            
            # Install agents (excluding mentat-updater which is developer-only)
            agents_source = self.extensions_dir / "agents"
            if agents_source.exists():
                for agent_file in agents_source.glob("*.md"):
                    # Skip the mentat-updater agent (it's in mentat_dev component)
                    if agent_file.name == "agent-mentat-updater.md":
                        continue
                    
                    target = agents_dir / agent_file.name
                    shutil.copy2(agent_file, target)
                    installed_items.append(f"Agent: @{agent_file.stem}")
                    self.logger.debug(f"Installed agent: {agent_file.name}")
            
            # Install supporting scripts
            scripts_source = Path(__file__).parent.parent.parent / "scripts"
            if scripts_source.exists():
                important_scripts = [
                    "sync-orchestrator.sh",
                    "health-monitor.sh",
                    "conflict-resolver.sh",
                    "framework-updater.sh",
                    "symlink-manager.sh"
                ]
                
                for script_name in important_scripts:
                    script_path = scripts_source / script_name
                    if script_path.exists():
                        target = scripts_dir / script_name
                        shutil.copy2(script_path, target)
                        # Make executable
                        target.chmod(0o755)
                        installed_items.append(f"Script: {script_name}")
                        self.logger.debug(f"Installed script: {script_name}")
            
            # Create .mentat directory for lock files and state
            mentat_dir = Path.home() / ".mentat"
            mentat_dir.mkdir(mode=0o700, exist_ok=True)
            self.logger.debug(f"Created .mentat directory at {mentat_dir}")
            
            # Store version information
            version_file_source = Path(__file__).parent.parent.parent / "VERSION"
            if version_file_source.exists():
                version_content = version_file_source.read_text().strip()
                version_file_target = self.install_dir / ".mentat-version"
                version_file_target.write_text(version_content)
                self.logger.debug(f"Stored version: {version_content}")
            
            if installed_items:
                self.logger.info(f"Installed {len(installed_items)} Mentat components")
                for item in installed_items:
                    self.logger.debug(f"  • {item}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to install Mentat extensions: {e}")
            return False
    
    def _post_install(self) -> bool:
        """Post-installation tasks - configure dotfiles repository and update CLAUDE.md"""
        try:
            # Update ~/.claude/CLAUDE.md with Mentat section
            self.logger.info("Updating CLAUDE.md with Mentat components...")
            claude_config = ClaudeConfigManager()
            if claude_config.update_claude_md():
                self.logger.success("Updated CLAUDE.md with Mentat section")
            else:
                self.logger.warning("Could not update CLAUDE.md - may need manual update")
            
            # Configure dotfiles repository
            config = MentatConfig()
            
            if not config.is_configured():
                self.logger.info("Configuring Mentat dotfiles repository...")
                
                # Run interactive configuration
                if config.configure_interactive():
                    self.logger.success("Dotfiles repository configured successfully")
                else:
                    self.logger.warning("Dotfiles repository configuration skipped")
                    self.logger.info("You can configure it later using /mentat:config")
            else:
                self.logger.info("Mentat dotfiles repository already configured")
                repo_url = config.get_repo_url()
                if repo_url:
                    self.logger.info(f"Using repository: {repo_url}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed during post-installation: {e}")
            # Don't fail the entire installation if config fails
            self.logger.warning("Installation completed but configuration failed")
            self.logger.info("Use /mentat:config to configure dotfiles repository")
            return True
    
    def uninstall(self) -> bool:
        """Uninstall Mentat extensions"""
        try:
            # Remove commands directory
            commands_dir = self.install_dir / "commands" / "mentat"
            if commands_dir.exists():
                shutil.rmtree(commands_dir)
                self.logger.debug("Removed Mentat commands")
            
            # Remove agents (only Mentat-specific ones)
            agents_dir = self.install_dir / "agents"
            if agents_dir.exists():
                # Only remove the syncer agent (mentat-updater is in dev component)
                syncer_path = agents_dir / "agent-syncer.md"
                if syncer_path.exists():
                    syncer_path.unlink()
                    self.logger.debug("Removed agent-syncer.md")
            
            # Remove scripts
            scripts_dir = self.install_dir / "scripts"
            if scripts_dir.exists():
                scripts_to_remove = [
                    "sync-orchestrator.sh",
                    "health-monitor.sh",
                    "conflict-resolver.sh"
                ]
                for script in scripts_to_remove:
                    script_path = scripts_dir / script
                    if script_path.exists():
                        script_path.unlink()
                        self.logger.debug(f"Removed script: {script}")
            
            # Remove Mentat section from CLAUDE.md
            self.logger.info("Removing Mentat section from CLAUDE.md...")
            claude_config = ClaudeConfigManager()
            if claude_config.remove_mentat_section():
                self.logger.debug("Removed Mentat section from CLAUDE.md")
            
            self.logger.info("Uninstalled Mentat extensions")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to uninstall Mentat extensions: {e}")
            return False
    
    def verify_installation(self) -> bool:
        """Verify that Mentat extensions are properly installed"""
        try:
            # Check for key commands
            commands_dir = self.install_dir / "commands" / "mentat"
            required_commands = ["setup.md", "sync.md", "status.md"]
            
            for cmd in required_commands:
                if not (commands_dir / cmd).exists():
                    self.logger.warning(f"Missing command: {cmd}")
                    return False
            
            # Check for syncer agent
            agents_dir = self.install_dir / "agents"
            syncer_agent = agents_dir / "agent-syncer.md"
            if not syncer_agent.exists():
                self.logger.warning("Missing agent-syncer.md")
                return False
            
            # Check for sync orchestrator script
            sync_script = self.install_dir / "scripts" / "sync-orchestrator.sh"
            if not sync_script.exists():
                self.logger.warning("Missing sync-orchestrator.sh script")
                return False
            
            # Check for .mentat directory
            mentat_dir = Path.home() / ".mentat"
            if not mentat_dir.exists():
                self.logger.warning("Missing .mentat directory")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to verify installation: {e}")
            return False
    
    def _calculate_size(self) -> int:
        """Calculate total size of Mentat extensions"""
        total_size = 0
        
        if self.extensions_dir.exists():
            # Calculate size of commands and agents (excluding mentat-updater)
            for item in self.extensions_dir.rglob("*"):
                if item.is_file() and item.name != "agent-mentat-updater.md":
                    total_size += item.stat().st_size
        
        # Add size of scripts
        scripts_dir = Path(__file__).parent.parent.parent / "scripts"
        if scripts_dir.exists():
            for script in ["sync-orchestrator.sh", "health-monitor.sh", "conflict-resolver.sh"]:
                script_path = scripts_dir / script
                if script_path.exists():
                    total_size += script_path.stat().st_size
        
        return total_size