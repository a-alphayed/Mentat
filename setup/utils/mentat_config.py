"""
Mentat Configuration Management
Handles dotfiles repository configuration and authentication settings
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, Optional, Any
from ..utils.logger import get_logger
from ..utils.ui import Colors, confirm
from ..utils.ssh_auth import SSHAuthHelper


class MentatConfig:
    """Manages Mentat configuration for dotfiles synchronization"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".mentat"
        self.config_file = self.config_dir / "config.json"
        self.logger = get_logger()
        self.ssh_helper = SSHAuthHelper()
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load existing configuration or return defaults"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Could not load config: {e}")
        
        # Default configuration
        return {
            "dotfiles_repo": "",
            "repo_type": "private",
            "auth_method": "ssh",
            "sync_branch": "main",
            "auto_sync": True,
            "sync_interval": 1800,  # 30 minutes
            "configured": False
        }
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            # Ensure config directory exists with proper permissions
            self.config_dir.mkdir(mode=0o700, exist_ok=True)
            
            # Write config file with restricted permissions
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            # Set restrictive permissions on config file
            self.config_file.chmod(0o600)
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
            return False
    
    def configure_interactive(self) -> bool:
        """Interactive configuration wizard for dotfiles repository"""
        print(f"\n{Colors.CYAN}{Colors.BRIGHT}Mentat Dotfiles Configuration{Colors.RESET}")
        print(f"{Colors.CYAN}{'=' * 50}{Colors.RESET}")
        
        # Explain what dotfiles are
        if not self.config.get("configured", False):
            print(f"\n{Colors.BLUE}ℹ️  What are dotfiles?{Colors.RESET}")
            print("Dotfiles are configuration files for your development environment.")
            print("Mentat syncs them across all your machines using a Git repository.")
            print(f"\n{Colors.YELLOW}⚠️  Important: Your dotfiles repository should be PRIVATE{Colors.RESET}")
            print("as it may contain sensitive information like API keys and personal configs.\n")
        
        # Ask for repository URL
        current_repo = self.config.get("dotfiles_repo", "")
        if current_repo:
            print(f"Current repository: {Colors.GREEN}{current_repo}{Colors.RESET}")
            if not confirm("Do you want to change the repository?"):
                return True
        
        print(f"\n{Colors.BLUE}Repository Setup Options:{Colors.RESET}")
        print("1. Use SSH authentication (recommended - most secure)")
        print("2. Use HTTPS with token (alternative)")
        print("3. Enter custom repository URL")
        print("4. Get help creating a new repository")
        print("5. Skip configuration for now")
        
        choice = input(f"{Colors.CYAN}Select option [1-5]: {Colors.RESET}").strip()
        
        if choice == "1":
            # SSH setup flow
            print(f"\n{Colors.BLUE}Setting up SSH authentication...{Colors.RESET}")
            
            # Check and setup SSH
            ssh_status = self.ssh_helper.check_ssh_setup()
            if not ssh_status['github_verified']:
                print(f"{Colors.YELLOW}SSH authentication not configured. Let's set it up!{Colors.RESET}")
                if not self.ssh_helper.setup_ssh_interactive():
                    print(f"{Colors.RED}SSH setup failed or was cancelled{Colors.RESET}")
                    return self.configure_interactive()  # Restart configuration
            else:
                print(f"{Colors.GREEN}✅ SSH authentication is already configured!{Colors.RESET}")
            
            # Get GitHub username for repo URL with validation
            username = input(f"\n{Colors.CYAN}Enter your GitHub username: {Colors.RESET}").strip()
            if not self._validate_github_username(username):
                print(f"{Colors.RED}Invalid GitHub username format{Colors.RESET}")
                print("Username must be alphanumeric with hyphens, max 39 characters")
                return self.configure_interactive()
            
            # Suggest repository name
            repo_name = input(f"{Colors.CYAN}Repository name [dotfiles]: {Colors.RESET}").strip() or "dotfiles"
            
            repo_url = f"git@github.com:{username}/{repo_name}.git"
            print(f"\n{Colors.BLUE}Repository URL: {Colors.GREEN}{repo_url}{Colors.RESET}")
            
        elif choice == "2":
            # HTTPS setup flow
            print(f"\n{Colors.YELLOW}⚠️  HTTPS requires a Personal Access Token{Colors.RESET}")
            print("You'll need to create one at: https://github.com/settings/tokens")
            print("Required scope: 'repo' (Full control of private repositories)")
            
            username = input(f"\n{Colors.CYAN}Enter your GitHub username: {Colors.RESET}").strip()
            if not self._validate_github_username(username):
                print(f"{Colors.RED}Invalid GitHub username format{Colors.RESET}")
                print("Username must be alphanumeric with hyphens, max 39 characters")
                return self.configure_interactive()
            
            repo_name = input(f"{Colors.CYAN}Repository name [dotfiles]: {Colors.RESET}").strip() or "dotfiles"
            
            repo_url = f"https://github.com/{username}/{repo_name}.git"
            print(f"\n{Colors.BLUE}Repository URL: {Colors.GREEN}{repo_url}{Colors.RESET}")
            
        elif choice == "3":
            # Custom URL
            print(f"\n{Colors.BLUE}Enter your dotfiles repository URL:{Colors.RESET}")
            print("Examples:")
            print("  • SSH:   git@github.com:yourusername/dotfiles.git")
            print("  • HTTPS: https://github.com/yourusername/dotfiles.git")
            
            repo_url = input(f"{Colors.CYAN}Repository URL: {Colors.RESET}").strip()
            
        elif choice == "4":
            self._show_repo_creation_guide()
            return self.configure_interactive()  # Restart configuration
            
        elif choice == "5":
            repo_url = "skip"
            
        else:
            print(f"{Colors.RED}Invalid option{Colors.RESET}")
            return self.configure_interactive()
        
        if repo_url.lower() == 'skip':
            print(f"{Colors.YELLOW}Skipping configuration. Use /mentat:config to set up later.{Colors.RESET}")
            return True
        
        if repo_url.lower() == 'create':
            self._show_repo_creation_guide()
            return self.configure_interactive()  # Restart configuration
        
        # Validate repository URL
        if not self._validate_repo_url(repo_url):
            print(f"{Colors.RED}Invalid repository URL format{Colors.RESET}")
            return False
        
        self.config["dotfiles_repo"] = repo_url
        
        # Detect authentication method
        if repo_url.startswith("git@"):
            self.config["auth_method"] = "ssh"
            print(f"{Colors.GREEN}✓ Using SSH authentication{Colors.RESET}")
        elif repo_url.startswith("https://"):
            self.config["auth_method"] = "https"
            print(f"{Colors.BLUE}Using HTTPS authentication{Colors.RESET}")
            print(f"{Colors.YELLOW}Note: You may need to set up a Personal Access Token{Colors.RESET}")
        
        # Ask about repository privacy
        self.config["repo_type"] = "private" if confirm(
            "Is this a private repository? (recommended)",
            default=True
        ) else "public"
        
        # Test repository access
        print(f"\n{Colors.BLUE}Testing repository access...{Colors.RESET}")
        if self._test_repo_access(repo_url):
            print(f"{Colors.GREEN}✅ Successfully connected to repository!{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠️  Could not connect to repository{Colors.RESET}")
            
            # Provide specific troubleshooting based on URL type
            if repo_url.startswith("git@"):
                print("\nTroubleshooting SSH connection:")
                
                # Check SSH status
                ssh_status = self.ssh_helper.check_ssh_setup()
                
                if not ssh_status['has_keys']:
                    print(f"  {Colors.RED}❌ No SSH keys found{Colors.RESET}")
                    print("     Run this command to generate: ssh-keygen -t ed25519")
                elif not ssh_status['agent_running']:
                    print(f"  {Colors.YELLOW}⚠️  SSH agent not running{Colors.RESET}")
                    print("     Run: eval '$(ssh-agent -s)'")
                elif not ssh_status['keys_loaded']:
                    print(f"  {Colors.YELLOW}⚠️  No keys loaded in SSH agent{Colors.RESET}")
                    print("     Run: ssh-add ~/.ssh/id_ed25519")
                elif not ssh_status['github_verified']:
                    print(f"  {Colors.YELLOW}⚠️  GitHub authentication not verified{Colors.RESET}")
                    print("     Your SSH key may not be added to GitHub")
                    print("     Check: https://github.com/settings/keys")
                
                print("\nOther possible issues:")
                print("  • Repository doesn't exist yet (create it on GitHub)")
                print("  • Repository name or username is incorrect")
                print("  • Network connectivity issues")
                
                if confirm("\nWould you like to set up SSH authentication now?"):
                    if self.ssh_helper.setup_ssh_interactive():
                        # Retry connection test
                        if self._test_repo_access(repo_url):
                            print(f"{Colors.GREEN}✅ Now successfully connected!{Colors.RESET}")
                        else:
                            print(f"{Colors.YELLOW}Still can't connect. The repository may not exist.{Colors.RESET}")
            
            elif repo_url.startswith("https://"):
                print("\nTroubleshooting HTTPS connection:")
                print("  • Make sure you have a Personal Access Token")
                print("  • Token needs 'repo' scope for private repositories")
                print("  • Configure git credentials: git config --global credential.helper store")
                print("  • Repository may not exist yet")
            
            if not confirm("\nContinue with this repository URL anyway?"):
                return False
        
        # Ask about sync preferences
        self.config["auto_sync"] = confirm(
            "Enable automatic synchronization every 30 minutes?",
            default=True
        )
        
        # Ask about branch
        branch = input(f"Which branch to sync? [{Colors.GREEN}main{Colors.RESET}]: ").strip()
        self.config["sync_branch"] = branch if branch else "main"
        
        # Mark as configured
        self.config["configured"] = True
        
        # Save configuration
        if self.save_config():
            print(f"\n{Colors.GREEN}✅ Configuration saved successfully!{Colors.RESET}")
            print(f"Configuration file: {self.config_file}")
            return True
        else:
            print(f"{Colors.RED}Failed to save configuration{Colors.RESET}")
            return False
    
    def _validate_github_username(self, username: str) -> bool:
        """Validate GitHub username format"""
        import re
        # GitHub username rules: alphanumeric, hyphens, max 39 chars
        # Cannot start/end with hyphen, no consecutive hyphens
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?$'
        
        # Security checks
        if not username or len(username) > 39:
            return False
        
        # Check for shell metacharacters
        dangerous_chars = [';', '|', '&', '$', '`', '\\', '"', "'", '\n', '\r', '<', '>', '/', '..']
        if any(char in username for char in dangerous_chars):
            return False
            
        return bool(re.match(pattern, username))
    
    def _validate_repo_url(self, url: str) -> bool:
        """Enhanced repository URL validation with security checks"""
        import re
        
        # Comprehensive validation patterns for GitHub
        ssh_pattern = r'^git@github\.com:[a-zA-Z0-9][a-zA-Z0-9-]{0,38}/[a-zA-Z0-9][a-zA-Z0-9._-]{0,100}\.git$'
        https_pattern = r'^https://github\.com/[a-zA-Z0-9][a-zA-Z0-9-]{0,38}/[a-zA-Z0-9][a-zA-Z0-9._-]{0,100}\.git$'
        
        if not (re.match(ssh_pattern, url) or re.match(https_pattern, url)):
            return False
        
        # Additional security checks
        if '..' in url or '//' in url.replace('https://', '').replace('git@', ''):
            return False
        
        return True
    
    def _test_repo_access(self, repo_url: str) -> bool:
        """Test if we can access the repository"""
        try:
            # Use git ls-remote to test access without cloning
            result = subprocess.run(
                ["git", "ls-remote", repo_url, "HEAD"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            self.logger.debug(f"Repository access test failed: {e}")
            return False
    
    def _show_repo_creation_guide(self):
        """Show guide for creating a new dotfiles repository"""
        print(f"\n{Colors.CYAN}{Colors.BRIGHT}Creating a Private Dotfiles Repository{Colors.RESET}")
        print(f"{Colors.CYAN}{'=' * 50}{Colors.RESET}")
        
        print(f"\n{Colors.RED}{Colors.BRIGHT}⚠️  IMPORTANT: Make your repository PRIVATE!{Colors.RESET}")
        print("Dotfiles contain sensitive information like:")
        print("  • API keys and tokens")
        print("  • SSH configurations")
        print("  • Personal paths and settings")
        
        print(f"\n{Colors.BLUE}Step 1: Create the repository{Colors.RESET}")
        print("1. Go to: https://github.com/new")
        print("2. Repository name: 'dotfiles'")
        print(f"3. {Colors.RED}Visibility: 🔒 Private (CRITICAL!){Colors.RESET}")
        print("4. Do NOT initialize with README")
        print("5. Click 'Create repository'")
        
        print(f"\n{Colors.BLUE}Step 2: Set up SSH authentication{Colors.RESET}")
        
        # Check current SSH status
        ssh_status = self.ssh_helper.check_ssh_setup()
        if ssh_status['github_verified']:
            print(f"{Colors.GREEN}✅ SSH is already set up!{Colors.RESET}")
        else:
            print("We'll help you set up SSH after creating the repository.")
        
        print(f"\n{Colors.BLUE}Step 3: Return here{Colors.RESET}")
        print("After creating your PRIVATE repository, we'll configure Mentat to use it.")
        
        print(f"\n{Colors.YELLOW}Ready to create your repository?{Colors.RESET}")
        print("1. Open https://github.com/new in your browser")
        print("2. Create a PRIVATE repository named 'dotfiles'")
        print("3. Come back here to continue setup")
        
        print(f"\n{Colors.BLUE}Press Enter when you've created the repository...{Colors.RESET}")
        input()
    
    def get_repo_url(self) -> Optional[str]:
        """Get configured repository URL"""
        return self.config.get("dotfiles_repo") if self.config.get("configured") else None
    
    def is_configured(self) -> bool:
        """Check if Mentat has been configured"""
        return self.config.get("configured", False)
    
    def get_config(self) -> Dict[str, Any]:
        """Get full configuration"""
        return self.config.copy()
    
    def update_config(self, key: str, value: Any) -> bool:
        """Update a specific configuration value"""
        self.config[key] = value
        return self.save_config()