"""
SSH Authentication Helper for Mentat
Handles SSH key setup, verification, and GitHub integration
"""

import os
import subprocess
import platform
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from ..utils.logger import get_logger
from ..utils.ui import Colors, confirm


class SSHAuthHelper:
    """Manages SSH authentication for private repository access"""
    
    def __init__(self):
        self.logger = get_logger()
        self.ssh_dir = Path.home() / ".ssh"
        self.known_hosts = self.ssh_dir / "known_hosts"
        self.ssh_key_types = [
            ("ed25519", "~/.ssh/id_ed25519", "Recommended - most secure"),
            ("rsa", "~/.ssh/id_rsa", "Legacy - widely compatible"),
            ("ecdsa", "~/.ssh/id_ecdsa", "Alternative - good security")
        ]
    
    def check_ssh_setup(self) -> Dict[str, Any]:
        """Check current SSH setup status"""
        status = {
            "has_ssh_dir": self.ssh_dir.exists(),
            "has_keys": False,
            "key_files": [],
            "agent_running": False,
            "keys_loaded": [],
            "github_verified": False
        }
        
        # Check for SSH keys
        for key_type, key_path, _ in self.ssh_key_types:
            key_file = Path(os.path.expanduser(key_path))
            if key_file.exists():
                status["has_keys"] = True
                status["key_files"].append(str(key_file))
        
        # Check SSH agent
        status["agent_running"] = self._check_ssh_agent()
        
        # Check loaded keys
        if status["agent_running"]:
            status["keys_loaded"] = self._get_loaded_keys()
        
        # Check GitHub authentication
        status["github_verified"] = self._verify_github_auth()
        
        return status
    
    def setup_ssh_interactive(self) -> bool:
        """Interactive SSH setup wizard"""
        print(f"\n{Colors.CYAN}{Colors.BRIGHT}SSH Authentication Setup{Colors.RESET}")
        print(f"{Colors.CYAN}{'=' * 50}{Colors.RESET}")
        
        # Check current status
        status = self.check_ssh_setup()
        
        # Show current status
        print(f"\n{Colors.BLUE}Current SSH Status:{Colors.RESET}")
        print(f"  SSH directory exists: {'✅' if status['has_ssh_dir'] else '❌'}")
        print(f"  SSH keys found: {'✅' if status['has_keys'] else '❌'}")
        if status['key_files']:
            for key in status['key_files']:
                print(f"    • {key}")
        print(f"  SSH agent running: {'✅' if status['agent_running'] else '❌'}")
        print(f"  GitHub access: {'✅' if status['github_verified'] else '❌'}")
        
        # If everything is working, offer to continue
        if status['github_verified']:
            print(f"\n{Colors.GREEN}✅ SSH authentication is already configured and working!{Colors.RESET}")
            if not confirm("Do you want to reconfigure?", default=False):
                return True
        
        # Offer setup options
        print(f"\n{Colors.BLUE}SSH Setup Options:{Colors.RESET}")
        print("1. Generate new SSH key (recommended for new setup)")
        print("2. Use existing SSH key")
        print("3. Skip SSH setup (not recommended for private repos)")
        
        choice = input(f"{Colors.CYAN}Select option [1-3] (default: 1): {Colors.RESET}").strip() or "1"
        
        if choice == "1":
            return self._generate_new_key()
        elif choice == "2":
            return self._use_existing_key()
        elif choice == "3":
            print(f"{Colors.YELLOW}⚠️  Skipping SSH setup. You may have issues accessing private repositories.{Colors.RESET}")
            return False
        else:
            print(f"{Colors.RED}Invalid option{Colors.RESET}")
            return False
    
    def _validate_email(self, email: str) -> bool:
        """Validate email address for SSH key generation"""
        import re
        # RFC 5322 compliant email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Security checks
        if not email or len(email) > 254:
            return False
        
        # Check for shell metacharacters that could cause injection
        dangerous_chars = [';', '|', '&', '$', '`', '\\', '"', "'", '\n', '\r', '<', '>']
        if any(char in email for char in dangerous_chars):
            return False
            
        return bool(re.match(email_pattern, email))
    
    def _generate_new_key(self) -> bool:
        """Generate a new SSH key"""
        print(f"\n{Colors.BLUE}Generating new SSH key...{Colors.RESET}")
        
        # Get email for key with validation
        email = input(f"{Colors.CYAN}Enter your GitHub email address: {Colors.RESET}").strip()
        if not self._validate_email(email):
            print(f"{Colors.RED}Invalid email address format{Colors.RESET}")
            print("Email must be a valid address without special characters")
            return False
        
        # Select key type
        print(f"\n{Colors.BLUE}Select SSH key type:{Colors.RESET}")
        for i, (key_type, path, desc) in enumerate(self.ssh_key_types, 1):
            print(f"{i}. {key_type} - {desc}")
        
        key_choice = input(f"{Colors.CYAN}Select key type [1] (default: 1): {Colors.RESET}").strip() or "1"
        
        try:
            idx = int(key_choice) - 1
            if idx < 0 or idx >= len(self.ssh_key_types):
                idx = 0
        except:
            idx = 0
        
        key_type, key_path, _ = self.ssh_key_types[idx]
        key_file = Path(os.path.expanduser(key_path))
        
        # Check if key already exists
        if key_file.exists():
            print(f"{Colors.YELLOW}⚠️  Key already exists at {key_file}{Colors.RESET}")
            if not confirm("Overwrite existing key?", default=False):
                return self._use_existing_key()
        
        # Ask for passphrase protection
        print(f"\n{Colors.BLUE}SSH Key Protection:{Colors.RESET}")
        print("A passphrase adds an extra layer of security to your SSH key.")
        print("Even if someone gains access to your key file, they can't use it without the passphrase.")
        
        use_passphrase = confirm("Protect your SSH key with a passphrase?", default=True)
        
        # Generate the key
        print(f"\n{Colors.BLUE}Generating {key_type} key...{Colors.RESET}")
        
        # Create SSH directory if it doesn't exist with secure permissions
        old_umask = os.umask(0o077)  # Temporarily restrict permissions
        try:
            self.ssh_dir.mkdir(mode=0o700, exist_ok=True)
            
            # Pre-create the key file with correct permissions (atomic)
            key_file.touch(mode=0o600)
            public_key_file = Path(str(key_file) + ".pub")
            
            # Generate key
            cmd = [
                "ssh-keygen",
                "-t", key_type,
                "-C", email,
                "-f", str(key_file)
            ]
            
            if key_type == "ed25519":
                cmd.extend(["-a", "100"])  # More secure key derivation
            elif key_type == "rsa":
                cmd.extend(["-b", "4096"])  # 4096 bit RSA
            
            if not use_passphrase:
                cmd.extend(["-N", ""])  # Empty passphrase if user declined
            
            # Run ssh-keygen
            result = subprocess.run(cmd, capture_output=False, text=True)
            
            if result.returncode != 0:
                print(f"{Colors.RED}Failed to generate SSH key{Colors.RESET}")
                # Clean up failed key files
                key_file.unlink(missing_ok=True)
                public_key_file.unlink(missing_ok=True)
                return False
            
            print(f"{Colors.GREEN}✅ SSH key generated successfully!{Colors.RESET}")
            
            # Verify and fix permissions (defensive)
            if key_file.stat().st_mode & 0o077 != 0:
                key_file.chmod(0o600)
            if public_key_file.exists() and public_key_file.stat().st_mode & 0o133 != 0:
                public_key_file.chmod(0o644)
        finally:
            os.umask(old_umask)  # Restore original umask
            
            # Add to SSH agent
            if self._add_key_to_agent(key_file):
                print(f"{Colors.GREEN}✅ Key added to SSH agent{Colors.RESET}")
            
            # Show public key and guide GitHub setup
            return self._setup_github_key(public_key_file)
            
        except Exception as e:
            self.logger.error(f"Failed to generate SSH key: {e}")
            print(f"{Colors.RED}Error generating SSH key: {e}{Colors.RESET}")
            return False
    
    def _use_existing_key(self) -> bool:
        """Use an existing SSH key"""
        print(f"\n{Colors.BLUE}Using existing SSH key...{Colors.RESET}")
        
        # Find existing keys
        existing_keys = []
        for key_type, key_path, _ in self.ssh_key_types:
            key_file = Path(os.path.expanduser(key_path))
            if key_file.exists():
                existing_keys.append(key_file)
        
        if not existing_keys:
            print(f"{Colors.RED}No existing SSH keys found{Colors.RESET}")
            return self._generate_new_key()
        
        # Select key
        if len(existing_keys) == 1:
            selected_key = existing_keys[0]
            print(f"Using key: {selected_key}")
        else:
            print(f"\n{Colors.BLUE}Select SSH key to use:{Colors.RESET}")
            for i, key in enumerate(existing_keys, 1):
                print(f"{i}. {key}")
            
            choice = input(f"{Colors.CYAN}Select key [1-{len(existing_keys)}] (default: 1): {Colors.RESET}").strip() or "1"
            try:
                idx = int(choice) - 1
                if idx < 0 or idx >= len(existing_keys):
                    idx = 0
            except:
                idx = 0
            
            selected_key = existing_keys[idx]
        
        # Add to SSH agent
        if self._add_key_to_agent(selected_key):
            print(f"{Colors.GREEN}✅ Key added to SSH agent{Colors.RESET}")
        
        # Check if key is already on GitHub
        if self._verify_github_auth():
            print(f"{Colors.GREEN}✅ SSH key is already configured with GitHub!{Colors.RESET}")
            return True
        
        # Guide GitHub setup
        public_key_file = Path(str(selected_key) + ".pub")
        if public_key_file.exists():
            return self._setup_github_key(public_key_file)
        else:
            print(f"{Colors.RED}Public key not found: {public_key_file}{Colors.RESET}")
            return False
    
    def _setup_github_key(self, public_key_file: Path) -> bool:
        """Guide user through adding SSH key to GitHub"""
        print(f"\n{Colors.CYAN}{Colors.BRIGHT}Add SSH Key to GitHub{Colors.RESET}")
        print(f"{Colors.CYAN}{'=' * 50}{Colors.RESET}")
        
        # Read public key
        try:
            with open(public_key_file, 'r') as f:
                public_key = f.read().strip()
        except Exception as e:
            print(f"{Colors.RED}Could not read public key: {e}{Colors.RESET}")
            return False
        
        # Display key
        print(f"\n{Colors.BLUE}Your public SSH key:{Colors.RESET}")
        print(f"{Colors.YELLOW}{public_key}{Colors.RESET}")
        
        # Copy to clipboard if possible
        if self._copy_to_clipboard(public_key):
            print(f"\n{Colors.GREEN}✅ Public key copied to clipboard!{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}⚠️  Could not copy to clipboard. Please copy the key above.{Colors.RESET}")
        
        # Guide through GitHub setup
        print(f"\n{Colors.BLUE}Steps to add key to GitHub:{Colors.RESET}")
        print("1. Go to: https://github.com/settings/keys")
        print("2. Click 'New SSH key'")
        print("3. Title: Give it a name (e.g., 'Mentat - Your Computer Name')")
        print("4. Key type: Authentication key")
        print("5. Key: Paste the public key (already copied to clipboard)")
        print("6. Click 'Add SSH key'")
        
        print(f"\n{Colors.YELLOW}Press Enter after you've added the key to GitHub...{Colors.RESET}")
        input()
        
        # Verify GitHub authentication
        print(f"\n{Colors.BLUE}Testing GitHub authentication...{Colors.RESET}")
        if self._verify_github_auth():
            print(f"{Colors.GREEN}✅ Successfully authenticated with GitHub!{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}❌ Could not verify GitHub authentication{Colors.RESET}")
            print("Please ensure you've added the key correctly to GitHub")
            
            if confirm("Try again?", default=True):
                return self._setup_github_key(public_key_file)
            
            return False
    
    def _check_ssh_agent(self) -> bool:
        """Check if SSH agent is running"""
        try:
            result = subprocess.run(
                ["ssh-add", "-l"],
                capture_output=True,
                text=True,
                timeout=5
            )
            # Return code 0 or 1 means agent is running (1 = no keys loaded)
            return result.returncode in [0, 1]
        except:
            return False
    
    def _start_ssh_agent(self) -> bool:
        """Start SSH agent if not running"""
        if self._check_ssh_agent():
            return True
        
        try:
            # Start ssh-agent
            result = subprocess.run(
                ["ssh-agent", "-s"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Parse output and set environment variables
                for line in result.stdout.split('\n'):
                    if line.startswith('SSH_'):
                        parts = line.split(';')[0].split('=')
                        if len(parts) == 2:
                            os.environ[parts[0]] = parts[1]
                
                return True
        except Exception as e:
            self.logger.error(f"Failed to start SSH agent: {e}")
        
        return False
    
    def _add_key_to_agent(self, key_file: Path) -> bool:
        """Add SSH key to agent"""
        # Ensure agent is running
        if not self._start_ssh_agent():
            print(f"{Colors.YELLOW}⚠️  Could not start SSH agent{Colors.RESET}")
            return False
        
        try:
            # Add key to agent
            result = subprocess.run(
                ["ssh-add", str(key_file)],
                capture_output=True,
                text=True
            )
            
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Failed to add key to agent: {e}")
            return False
    
    def _get_loaded_keys(self) -> list:
        """Get list of keys loaded in SSH agent"""
        try:
            result = subprocess.run(
                ["ssh-add", "-l"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return result.stdout.strip().split('\n')
            
        except:
            pass
        
        return []
    
    def _verify_github_auth(self) -> bool:
        """Verify GitHub SSH authentication"""
        try:
            # Test SSH connection to GitHub
            result = subprocess.run(
                ["ssh", "-T", "git@github.com"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # GitHub returns exit code 1 but with success message
            if "successfully authenticated" in result.stderr:
                return True
            
        except Exception as e:
            self.logger.debug(f"GitHub verification failed: {e}")
        
        return False
    
    def _copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard (platform-specific)"""
        system = platform.system()
        
        try:
            if system == "Darwin":  # macOS
                subprocess.run(["pbcopy"], input=text, text=True, check=True)
                return True
            elif system == "Linux":
                # Try xclip first, then xsel
                for cmd in [["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]]:
                    try:
                        subprocess.run(cmd, input=text, text=True, check=True)
                        return True
                    except:
                        continue
            elif system == "Windows":
                subprocess.run(["clip"], input=text, text=True, check=True)
                return True
        except:
            pass
        
        return False
    
    def ensure_github_in_known_hosts(self) -> bool:
        """Ensure GitHub's SSH key is in known_hosts"""
        try:
            # Create SSH directory if it doesn't exist
            self.ssh_dir.mkdir(mode=0o700, exist_ok=True)
            
            # Check if GitHub is already in known_hosts
            if self.known_hosts.exists():
                with open(self.known_hosts, 'r') as f:
                    if "github.com" in f.read():
                        return True
            
            # Add GitHub's SSH key
            print(f"{Colors.BLUE}Adding GitHub to known hosts...{Colors.RESET}")
            
            # Get GitHub's SSH key
            result = subprocess.run(
                ["ssh-keyscan", "-t", "rsa", "github.com"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout:
                with open(self.known_hosts, 'a') as f:
                    f.write(result.stdout)
                
                self.known_hosts.chmod(0o644)
                return True
            
        except Exception as e:
            self.logger.error(f"Failed to add GitHub to known_hosts: {e}")
        
        return False