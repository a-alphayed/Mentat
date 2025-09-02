# Command: /mentat:config

> "Adjusting the neural pathways of synchronization"

## Command Metadata

- **Trigger**: `/mentat:config`
- **Description**: Configure or reconfigure Mentat dotfiles repository settings
- **Category**: Configuration
- **Requires**: git
- **Time Estimate**: 2-3 minutes

## Purpose

The `/mentat:config` command allows you to:
1. Configure your dotfiles repository for the first time
2. Change your dotfiles repository URL
3. Update authentication settings
4. Modify sync preferences
5. View current configuration

## Configuration Workflow

### Interactive Configuration

```python
#!/usr/bin/env python3
import json
import subprocess
import os
from pathlib import Path

# Configuration file location
CONFIG_DIR = Path.home() / ".mentat"
CONFIG_FILE = CONFIG_DIR / "config.json"

def load_config():
    """Load existing configuration"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    """Save configuration with proper permissions"""
    CONFIG_DIR.mkdir(mode=0o700, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    CONFIG_FILE.chmod(0o600)
    print("✅ Configuration saved")

def test_repo_access(repo_url):
    """Test repository accessibility"""
    try:
        result = subprocess.run(
            ["git", "ls-remote", repo_url, "HEAD"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except:
        return False

def main():
    print("\n🧠 Mentat Dotfiles Configuration")
    print("=" * 50)
    
    # Load existing config
    config = load_config()
    
    # Show current configuration
    if config.get("configured"):
        print("\nCurrent Configuration:")
        print(f"  Repository: {config.get('dotfiles_repo', 'Not set')}")
        print(f"  Type: {config.get('repo_type', 'Not set')}")
        print(f"  Branch: {config.get('sync_branch', 'main')}")
        print(f"  Auto-sync: {config.get('auto_sync', True)}")
        
        choice = input("\nOptions: [c]hange, [v]iew, [t]est, [q]uit: ").lower()
        
        if choice == 'q':
            return
        elif choice == 'v':
            print(json.dumps(config, indent=2))
            return
        elif choice == 't':
            repo = config.get('dotfiles_repo')
            if repo:
                print(f"\nTesting access to {repo}...")
                if test_repo_access(repo):
                    print("✅ Repository is accessible")
                else:
                    print("❌ Cannot access repository")
            return
        elif choice != 'c':
            return
    
    # Configuration wizard
    print("\n📝 Dotfiles Repository Setup")
    print("\n⚠️  Important: Your dotfiles repository should be PRIVATE")
    print("as it may contain sensitive information.\n")
    
    # Repository URL
    print("Enter your dotfiles repository URL:")
    print("Examples:")
    print("  SSH:   git@github.com:yourusername/dotfiles.git")
    print("  HTTPS: https://github.com/yourusername/dotfiles.git")
    
    repo_url = input("\nRepository URL (or 'skip'): ").strip()
    
    if repo_url.lower() == 'skip':
        print("Configuration skipped")
        return
    
    # Validate URL format
    import re
    ssh_pattern = r'^git@[\w\.-]+:[\w\.-]+/[\w\.-]+\.git$'
    https_pattern = r'^https://[\w\.-]+/[\w\.-]+/[\w\.-]+\.git$'
    
    if not (re.match(ssh_pattern, repo_url) or re.match(https_pattern, repo_url)):
        print("❌ Invalid repository URL format")
        return
    
    config['dotfiles_repo'] = repo_url
    
    # Detect auth method
    if repo_url.startswith('git@'):
        config['auth_method'] = 'ssh'
        print("✓ Using SSH authentication")
    else:
        config['auth_method'] = 'https'
        print("✓ Using HTTPS authentication")
    
    # Repository type
    is_private = input("Is this a private repository? [Y/n]: ").lower() != 'n'
    config['repo_type'] = 'private' if is_private else 'public'
    
    # Test access
    print("\nTesting repository access...")
    if test_repo_access(repo_url):
        print("✅ Successfully connected!")
    else:
        print("⚠️  Could not connect to repository")
        print("\nPossible reasons:")
        print("  1. Repository doesn't exist yet")
        print("  2. Authentication not set up")
        print("  3. Network issues")
        
        if input("\nContinue anyway? [y/N]: ").lower() != 'y':
            return
    
    # Sync settings
    config['sync_branch'] = input("Branch to sync [main]: ").strip() or 'main'
    config['auto_sync'] = input("Enable auto-sync? [Y/n]: ").lower() != 'n'
    config['sync_interval'] = 1800  # 30 minutes
    config['configured'] = True
    
    # Save configuration
    save_config(config)
    print("\n✨ Configuration complete!")
    print(f"Config file: {CONFIG_FILE}")
    print("\nYou can now use:")
    print("  /mentat:setup  - Initialize this machine")
    print("  /mentat:sync   - Sync your dotfiles")

if __name__ == "__main__":
    main()
```

## Configuration Options

### Repository Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `dotfiles_repo` | Git repository URL | Required |
| `repo_type` | private or public | private |
| `auth_method` | ssh or https | Auto-detected |
| `sync_branch` | Branch to sync | main |

### Sync Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `auto_sync` | Enable automatic sync | true |
| `sync_interval` | Seconds between syncs | 1800 |

## Security Considerations

### Private Repository (Recommended)

```bash
# Create a private repository on GitHub
# 1. Go to https://github.com/new
# 2. Name: dotfiles
# 3. Visibility: Private ✅
# 4. Don't initialize with README
```

### SSH Authentication (Recommended)

```bash
# Generate SSH key if needed
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub
# Add to GitHub: Settings > SSH Keys
```

### HTTPS Authentication

```bash
# Create Personal Access Token
# 1. Go to https://github.com/settings/tokens
# 2. Generate new token (classic)
# 3. Select 'repo' scope
# 4. Save token securely

# Configure git to store credentials
git config --global credential.helper store
```

## Sensitive Files Protection

### Default .gitignore

The system automatically creates a `.gitignore` for sensitive files:

```gitignore
# Secrets and credentials
.env
.env.*
*.key
*.pem
*.p12
*.pfx
id_rsa*
id_ed25519*
*.secret

# API tokens
.npmrc
.pypirc
.gem/credentials
.docker/config.json

# Cloud credentials
.aws/credentials
.gcloud/
.azure/

# Database
*.sqlite
*.db

# System
.DS_Store
Thumbs.db
.Trash/

# Temporary
*.tmp
*.bak
*.swp
*~
```

## Troubleshooting

### Cannot Access Repository

```bash
# Check SSH connection
ssh -T git@github.com

# Check git remote
cd ~/dotfiles
git remote -v

# Test repository access
git ls-remote <your-repo-url> HEAD
```

### Authentication Issues

```bash
# SSH: Check if key is loaded
ssh-add -l

# HTTPS: Clear stored credentials
git config --global --unset credential.helper

# Re-authenticate
git push origin main
```

### Configuration File Issues

```bash
# Check configuration
cat ~/.mentat/config.json

# Reset configuration
rm ~/.mentat/config.json
/mentat:config  # Reconfigure
```

## Examples

### First-Time Setup

```
🧠 Mentat Dotfiles Configuration
==================================================

📝 Dotfiles Repository Setup

Enter your dotfiles repository URL:
> git@github.com:alice/dotfiles.git

✓ Using SSH authentication
Is this a private repository? [Y/n]: y

Testing repository access...
✅ Successfully connected!

Branch to sync [main]: main
Enable auto-sync? [Y/n]: y

✅ Configuration saved
✨ Configuration complete!
```

### Changing Repository

```
/mentat:config

Current Configuration:
  Repository: git@github.com:alice/old-dotfiles.git
  Type: private
  Branch: main
  Auto-sync: true

Options: [c]hange, [v]iew, [t]est, [q]uit: c

Enter your dotfiles repository URL:
> git@github.com:alice/new-dotfiles.git
...
```

### Testing Connection

```
/mentat:config

Options: [c]hange, [v]iew, [t]est, [q]uit: t

Testing access to git@github.com:alice/dotfiles.git...
✅ Repository is accessible
```