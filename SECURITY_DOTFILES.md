# Mentat Dotfiles Security Guide

## Why Dotfiles Security Matters

Dotfiles contain your personal development environment configuration. They often include:

- **API Keys & Tokens**: Service authentication credentials
- **SSH Configurations**: Server access settings
- **Database Credentials**: Connection strings and passwords
- **Personal Information**: Email addresses, usernames, paths
- **Work-Related Configs**: Company-specific settings
- **Cloud Credentials**: AWS, GCP, Azure access keys

**⚠️ CRITICAL: Always use a PRIVATE repository for your dotfiles!**

## Security Best Practices

### 1. Private Repository (Required)

```bash
# When creating your dotfiles repository:
# 1. Go to https://github.com/new
# 2. Repository name: dotfiles
# 3. Visibility: 🔒 Private (NEVER Public)
# 4. Initialize: No README (we'll add files later)
```

### 2. Authentication Methods

#### SSH Authentication (Recommended)

Most secure method for accessing your private repository:

```bash
# Generate a new SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub
# Add to GitHub: Settings > SSH and GPG keys > New SSH key

# Test connection
ssh -T git@github.com
```

#### Personal Access Token (Alternative)

For HTTPS authentication:

```bash
# Create token at: https://github.com/settings/tokens
# Required scopes: repo (full control of private repositories)
# Store securely - treat like a password!

# Configure git to use token
git config --global credential.helper store
# First push/pull will prompt for username and token
```

### 3. Sensitive File Protection

#### Essential .gitignore

Create `~/dotfiles/.gitignore` with:

```gitignore
# CRITICAL: Never commit these files
# Secrets and credentials
.env
.env.*
*.key
*.pem
*.p12
*.pfx
*.crt
*.cer

# SSH keys (NEVER commit these!)
id_rsa*
id_ed25519*
id_ecdsa*
id_dsa*
known_hosts
authorized_keys

# API tokens and credentials
.npmrc
.pypirc
.gem/credentials
.docker/config.json
.netrc
.authinfo

# Cloud provider credentials
.aws/credentials
.aws/config
.gcloud/
.azure/
.kube/config
kubeconfig*

# Database files
*.sqlite
*.sqlite3
*.db
*.sql

# Password stores
.password-store/
.gnupg/
*.gpg
*.asc

# Application secrets
.wakatime.cfg
.gh_token
.github_token
.gitlab_token

# History files (may contain sensitive commands)
.*_history
.bash_history
.zsh_history
.python_history
.mysql_history
.psql_history
.rediscli_history

# macOS
.DS_Store
.Trash/

# Temporary files
*.tmp
*.bak
*.swp
*.swo
*~
.cache/
tmp/
temp/

# IDE
.idea/
.vscode/settings.json
*.code-workspace
```

### 4. Secret Management

#### Use Environment Variables

Instead of hardcoding secrets in config files:

```bash
# .zshrc or .bashrc (this file CAN be committed)
export API_KEY_NAME="${API_KEY_NAME}"  # Placeholder

# .env.local (NEVER commit this file)
export API_KEY_NAME="actual-secret-key-value"

# Source the local env file in your shell config
[ -f ~/.env.local ] && source ~/.env.local
```

#### Use Secret Management Tools

Consider using dedicated tools for sensitive data:

- **1Password CLI**: `op` command for accessing vaults
- **pass**: Unix password manager
- **Keychain (macOS)**: System keychain integration
- **Secret files**: Keep in `~/.secrets/` (not in dotfiles repo)

### 5. Audit Your Dotfiles

Before committing, always check for secrets:

```bash
# Search for potential secrets
grep -r "password\|token\|key\|secret\|api" ~/dotfiles/

# Check git status before committing
git status
git diff --staged

# Use tools to scan for secrets
# Install: pip install detect-secrets
detect-secrets scan ~/dotfiles/

# GitHub secret scanning (automatic for private repos)
```

### 6. Repository Access Control

#### Limit Access

- Keep repository private
- Don't add collaborators unless necessary
- Review access permissions regularly
- Use deploy keys for CI/CD instead of personal tokens

#### Enable Security Features

On GitHub:
1. Settings > Security & analysis
2. Enable:
   - Dependency alerts
   - Secret scanning
   - Security advisories

### 7. Sync Security

#### Secure Synchronization

The Mentat sync system:
- Only syncs with YOUR configured repository
- Uses your existing Git authentication
- Creates secure lock files in `~/.mentat/` (mode 700)
- Config file has restricted permissions (mode 600)

#### Verify Repository

Always verify you're syncing with the correct repository:

```bash
# Check current configuration
cat ~/.mentat/config.json

# Verify remote
cd ~/dotfiles
git remote -v
```

## What to Include vs Exclude

### ✅ Safe to Include

- Shell configurations (without secrets)
- Editor settings
- Git config (without tokens)
- Application preferences
- Aliases and functions
- PATH modifications
- Theme configurations

### ❌ Never Include

- Private SSH keys
- API tokens/keys
- Passwords
- Database credentials
- SSL certificates
- Personal identification
- Work proprietary info
- Browser cookies/sessions

## Emergency Response

### If You Accidentally Commit Secrets

1. **Immediately revoke** the exposed credential
2. **Remove from repository**:
   ```bash
   # Remove file from history (requires force push)
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch PATH_TO_FILE" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push (this rewrites history!)
   git push origin --force --all
   ```
3. **Generate new credentials**
4. **Audit access logs** for any unauthorized use
5. **Consider the secret permanently compromised**

### Prevention Tools

```bash
# Pre-commit hook to prevent secret commits
# Install: pip install pre-commit
# Add to .pre-commit-config.yaml:
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
```

## Mentat-Specific Security

### Configuration File

Location: `~/.mentat/config.json`
- Permissions: 600 (read/write owner only)
- Contains: Repository URL, no credentials
- Safe to backup

### Lock Files

Location: `~/.mentat/sync.lock`
- Permissions: 700 directory
- Purpose: Prevent concurrent syncs
- Auto-cleaned on exit

### Logs

Location: `~/.mentat/sync.log`
- May contain: File paths, timestamps
- Should not contain: Credentials
- Rotate regularly

## Regular Security Checklist

- [ ] Repository is private
- [ ] .gitignore includes all sensitive patterns
- [ ] No secrets in committed files
- [ ] SSH keys have passphrase
- [ ] Repository access is limited
- [ ] Security scanning is enabled
- [ ] Local config files have correct permissions
- [ ] Credentials are in environment variables or secret manager
- [ ] Regular audit of repository contents
- [ ] Backup of essential configs (without secrets)

## Getting Help

If you have security concerns:

1. **GitHub Security**: https://docs.github.com/en/code-security
2. **SSH Setup**: https://docs.github.com/en/authentication
3. **Secret Scanning**: https://docs.github.com/en/code-security/secret-scanning
4. **Report Issues**: Create issue at https://github.com/a-alphayed/Mentat (don't include sensitive info!)

Remember: **Security is not optional when dealing with dotfiles!**