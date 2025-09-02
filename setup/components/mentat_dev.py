"""
Mentat Developer Component
Installs developer-only tools for maintaining the Mentat fork
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import shutil
from ..core.base import Component
from ..utils.logger import get_logger


class MentatDevComponent(Component):
    """Component for installing Mentat developer tools"""
    
    def __init__(self, install_dir: Path = None):
        # Find the mentat-extensions directory relative to the setup module
        self.extensions_dir = Path(__file__).parent.parent.parent / "mentat-extensions"
        super().__init__(install_dir)
        self.logger = get_logger()
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get component metadata"""
        return {
            "name": "mentat_dev",
            "description": "Developer tools for maintaining the Mentat fork (includes @mentat-updater)",
            "version": "1.0.0",
            "category": "developer",
            "author": "Mentat Framework",
            "size": self._calculate_size()
        }
    
    def get_dependencies(self) -> List[str]:
        """Developer tools depend on core and mentat being installed"""
        return ["core", "mentat"]
    
    def validate_prerequisites(self) -> bool:
        """Check if this is a development environment"""
        # Check if we're in a git repository
        git_dir = Path.cwd() / ".git"
        mentat_repo_git = Path(__file__).parent.parent.parent / ".git"
        
        if not (git_dir.exists() or mentat_repo_git.exists()):
            self.logger.warning("mentat_dev component is intended for development environments with git repository")
            # Still allow installation but warn the user
        
        if not self.extensions_dir.exists():
            self.logger.error(f"mentat-extensions directory not found at {self.extensions_dir}")
            return False
        
        return True
    
    def _get_source_dir(self) -> Optional[Path]:
        """Get source directory for developer tools"""
        # Return the mentat-extensions directory
        return self.extensions_dir
    
    def _install(self, config: Dict[str, Any]) -> bool:
        """Perform developer tools installation"""
        try:
            agents_dir = self.install_dir / "agents"
            scripts_dir = self.install_dir / "scripts"
            
            agents_dir.mkdir(parents=True, exist_ok=True)
            scripts_dir.mkdir(parents=True, exist_ok=True)
            
            installed_items = []
            
            # Install the mentat-updater agent
            updater_source = self.extensions_dir / "agents" / "agent-mentat-updater.md"
            if updater_source.exists():
                target = agents_dir / "agent-mentat-updater.md"
                shutil.copy2(updater_source, target)
                installed_items.append("Agent: @mentat-updater")
                self.logger.debug("Installed agent-mentat-updater.md")
            else:
                self.logger.warning("agent-mentat-updater.md not found")
            
            # Install developer scripts
            scripts_source = Path(__file__).parent.parent.parent / "scripts"
            if scripts_source.exists():
                dev_scripts = [
                    "version-bump.sh",
                    "test-mentat-integration.sh",
                    "cleanup.sh",
                    "publish.sh"
                ]
                
                for script_name in dev_scripts:
                    script_path = scripts_source / script_name
                    if script_path.exists():
                        target = scripts_dir / script_name
                        shutil.copy2(script_path, target)
                        # Make executable
                        target.chmod(0o755)
                        installed_items.append(f"Script: {script_name}")
                        self.logger.debug(f"Installed script: {script_name}")
            
            if installed_items:
                self.logger.info(f"Installed {len(installed_items)} Mentat developer components")
                for item in installed_items:
                    self.logger.debug(f"  • {item}")
                
                # Show developer-specific message
                self.logger.info("Developer tools installed. Use @mentat-updater to sync with upstream SuperClaude.")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to install Mentat developer tools: {e}")
            return False
    
    def _post_install(self) -> bool:
        """Post-installation tasks"""
        # No post-install tasks needed for developer tools
        return True
    
    def uninstall(self) -> bool:
        """Uninstall Mentat developer tools"""
        try:
            # Remove mentat-updater agent
            agents_dir = self.install_dir / "agents"
            if agents_dir.exists():
                updater_path = agents_dir / "agent-mentat-updater.md"
                if updater_path.exists():
                    updater_path.unlink()
                    self.logger.debug("Removed agent-mentat-updater.md")
            
            # Remove developer scripts
            scripts_dir = self.install_dir / "scripts"
            if scripts_dir.exists():
                dev_scripts = [
                    "version-bump.sh",
                    "test-mentat-integration.sh",
                    "cleanup.sh",
                    "publish.sh"
                ]
                for script in dev_scripts:
                    script_path = scripts_dir / script
                    if script_path.exists():
                        script_path.unlink()
                        self.logger.debug(f"Removed script: {script}")
            
            self.logger.info("Uninstalled Mentat developer tools")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to uninstall Mentat developer tools: {e}")
            return False
    
    def verify_installation(self) -> bool:
        """Verify that Mentat developer tools are properly installed"""
        try:
            # Check for mentat-updater agent
            agents_dir = self.install_dir / "agents"
            updater_agent = agents_dir / "agent-mentat-updater.md"
            if not updater_agent.exists():
                self.logger.warning("Missing agent-mentat-updater.md")
                return False
            
            # Check for at least one developer script
            scripts_dir = self.install_dir / "scripts"
            version_script = scripts_dir / "version-bump.sh"
            if not version_script.exists():
                self.logger.warning("Missing version-bump.sh script")
                # Not critical, but worth noting
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to verify installation: {e}")
            return False
    
    def _calculate_size(self) -> int:
        """Calculate total size of developer tools"""
        total_size = 0
        
        # Size of mentat-updater agent
        if self.extensions_dir.exists():
            updater_path = self.extensions_dir / "agents" / "agent-mentat-updater.md"
            if updater_path.exists():
                total_size += updater_path.stat().st_size
        
        # Add size of developer scripts
        scripts_dir = Path(__file__).parent.parent.parent / "scripts"
        if scripts_dir.exists():
            for script in ["version-bump.sh", "test-mentat-integration.sh", "cleanup.sh", "publish.sh"]:
                script_path = scripts_dir / script
                if script_path.exists():
                    total_size += script_path.stat().st_size
        
        return total_size