# Command: /mentat:setup

> "Awakening a new node in the Mentat network"

## Command Metadata

- **Trigger**: `/mentat:setup`
- **Description**: Initialize a new machine with complete development environment
- **Category**: Environment Management
- **Requires**: git, internet connection
- **Time Estimate**: 5-10 minutes

## Purpose

The `/mentat:setup` command transforms a fresh machine into a fully configured development environment by:
1. Cloning your dotfiles repository
2. Setting up all symlinks
3. Installing required packages and tools
4. Configuring development applications
5. Initializing the Syncer for continuous synchronization

## Workflow

### Phase 1: System Detection

```bash
# Detect operating system
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
fi

# Detect shell
SHELL_TYPE=$(basename "$SHELL")

# Detect package managers
PACKAGE_MANAGER="none"
if command -v brew &> /dev/null; then
    PACKAGE_MANAGER="brew"
elif command -v apt &> /dev/null; then
    PACKAGE_MANAGER="apt"
elif command -v yum &> /dev/null; then
    PACKAGE_MANAGER="yum"
fi
```

### Phase 2: Prerequisites Check

```bash
# Ensure git is installed
if ! command -v git &> /dev/null; then
    echo "📦 Installing git..."
    case $PACKAGE_MANAGER in
        brew) brew install git ;;
        apt) sudo apt update && sudo apt install -y git ;;
        yum) sudo yum install -y git ;;
        *) echo "❌ Please install git manually" && exit 1 ;;
    esac
fi

# Check GitHub authentication
if ! ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "🔑 Setting up GitHub authentication..."
    # Guide user through SSH key setup or token configuration
fi
```

### Phase 3: Dotfiles Repository Setup

```bash
# Read configuration
CONFIG_FILE="$HOME/.mentat/config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Mentat configuration not found!"
    echo "Please run /mentat:config to set up your dotfiles repository"
    exit 1
fi

# Extract repository URL from config
DOTFILES_REPO=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['dotfiles_repo'])" 2>/dev/null)
SYNC_BRANCH=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('sync_branch', 'main'))" 2>/dev/null)

if [ -z "$DOTFILES_REPO" ]; then
    echo "❌ No dotfiles repository configured!"
    echo "Please run /mentat:config to set up your repository"
    exit 1
fi

DOTFILES_DIR="$HOME/dotfiles"

# Check if repository is accessible
echo "🔍 Checking repository access..."
if ! git ls-remote "$DOTFILES_REPO" HEAD >/dev/null 2>&1; then
    echo "⚠️  Cannot access repository: $DOTFILES_REPO"
    
    # Provide SSH-specific troubleshooting
    if [[ "$DOTFILES_REPO" == git@* ]]; then
        echo ""
        echo "🔐 SSH Authentication Issue Detected"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # Run automated SSH test if available
        if [ -f "$HOME/.claude/scripts/test-ssh.sh" ]; then
            echo "Running SSH diagnostics..."
            echo ""
            bash "$HOME/.claude/scripts/test-ssh.sh"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        else
            # Manual troubleshooting steps
            echo "Quick SSH checks:"
            
            # Check for SSH keys
            if ls ~/.ssh/id_* 2>/dev/null | grep -q .; then
                echo "  ✅ SSH keys found"
            else
                echo "  ❌ No SSH keys found"
                echo "     → Generate one: ssh-keygen -t ed25519 -C 'your_email@example.com'"
            fi
            
            # Check SSH agent
            if ssh-add -l &>/dev/null; then
                echo "  ✅ SSH agent has keys loaded"
            else
                echo "  ❌ No keys in SSH agent"
                echo "     → Add your key: ssh-add ~/.ssh/id_ed25519"
            fi
            
            # Check GitHub connectivity
            if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
                echo "  ✅ GitHub SSH authentication works"
                echo ""
                echo "  Repository issue - possible causes:"
                echo "    • Repository doesn't exist yet"
                echo "    • Repository name is incorrect"
                echo "    • You don't have access to this repository"
            else
                echo "  ❌ GitHub SSH authentication failed"
                echo "     → Add your public key to GitHub: https://github.com/settings/keys"
                echo "     → Copy key: cat ~/.ssh/id_ed25519.pub"
            fi
        fi
        
        echo ""
        echo "To reconfigure: /mentat:config"
        echo "This will guide you through complete SSH setup"
        
    elif [[ "$DOTFILES_REPO" == https://* ]]; then
        echo ""
        echo "🔑 HTTPS Authentication Issue"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "For HTTPS authentication, you need:"
        echo "  1. Personal Access Token from: https://github.com/settings/tokens"
        echo "  2. Token scope: 'repo' (Full control of private repositories)"
        echo "  3. Configure git: git config --global credential.helper store"
        echo ""
        echo "Alternative: Switch to SSH (recommended)"
        echo "Run: /mentat:config and choose SSH option"
    fi
    
    exit 1
fi

if [ ! -d "$DOTFILES_DIR" ]; then
    echo "📥 Cloning dotfiles repository..."
    git clone "$DOTFILES_REPO" "$DOTFILES_DIR"
    
    # Check if clone was successful
    if [ $? -ne 0 ]; then
        echo "❌ Failed to clone repository"
        exit 1
    fi
    
    echo "✅ Repository cloned successfully"
else
    echo "✅ Dotfiles repository already exists"
    cd "$DOTFILES_DIR"
    
    # Fetch and pull latest changes
    echo "📥 Updating from remote..."
    git fetch origin "$SYNC_BRANCH"
    
    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        echo "⚠️  Uncommitted changes detected"
        echo "Stashing changes..."
        git stash push -m "Mentat setup: auto-stash $(date +%Y%m%d-%H%M%S)"
    fi
    
    git pull origin "$SYNC_BRANCH"
fi

# Setup symlinks using Mentat's symlink manager
echo "🔧 Setting up dotfile symlinks..."
SYMLINK_SCRIPT="$HOME/.claude/scripts/symlink-manager.sh"

if [ -f "$SYMLINK_SCRIPT" ]; then
    bash "$SYMLINK_SCRIPT" setup
else
    echo "⚠️ Symlink manager not found, attempting fallback..."
    # Fallback: Try to use the script from Mentat installation
    MENTAT_SYMLINK="/usr/local/bin/mentat-symlink-manager"
    if [ -f "$MENTAT_SYMLINK" ]; then
        bash "$MENTAT_SYMLINK" setup
    else
        echo "❌ Cannot setup symlinks - symlink manager not found"
        echo "Please reinstall Mentat or run: mentat install"
    fi
fi
```

### Phase 4: Package Installation

```bash
# Install packages based on OS
echo "📦 Installing packages..."

# Homebrew packages (macOS)
if [ "$OS" == "macos" ] && [ -f "$DOTFILES_DIR/packages/Brewfile" ]; then
    echo "🍺 Installing Homebrew packages..."
    brew bundle --file="$DOTFILES_DIR/packages/Brewfile"
fi

# APT packages (Linux)
if [ "$PACKAGE_MANAGER" == "apt" ] && [ -f "$DOTFILES_DIR/packages/apt-packages.txt" ]; then
    echo "📦 Installing APT packages..."
    xargs -a "$DOTFILES_DIR/packages/apt-packages.txt" sudo apt install -y
fi

# NPM global packages
if command -v npm &> /dev/null && [ -f "$DOTFILES_DIR/packages/npm-global.txt" ]; then
    echo "📦 Installing NPM packages..."
    xargs -a "$DOTFILES_DIR/packages/npm-global.txt" npm install -g
fi

# Python packages
if command -v pip &> /dev/null && [ -f "$DOTFILES_DIR/packages/pip-requirements.txt" ]; then
    echo "🐍 Installing Python packages..."
    pip install -r "$DOTFILES_DIR/packages/pip-requirements.txt"
fi
```

### Phase 5: Development Environment Setup

```bash
# Configure Cursor/VS Code
if [ -f "$DOTFILES_DIR/packages/cursor-extensions.txt" ]; then
    echo "🎨 Installing Cursor extensions..."
    while IFS= read -r extension; do
        cursor --install-extension "$extension"
    done < "$DOTFILES_DIR/packages/cursor-extensions.txt"
fi

# Copy Cursor settings
CURSOR_SETTINGS_DIR="$HOME/Library/Application Support/Cursor/User"
if [ "$OS" == "linux" ]; then
    CURSOR_SETTINGS_DIR="$HOME/.config/Code/User"
fi

if [ -f "$DOTFILES_DIR/special/cursor-settings.json" ]; then
    echo "⚙️ Configuring Cursor settings..."
    mkdir -p "$CURSOR_SETTINGS_DIR"
    ln -sf "$DOTFILES_DIR/special/cursor-settings.json" "$CURSOR_SETTINGS_DIR/settings.json"
fi
```

### Phase 6: Shell Configuration

```bash
# Configure shell based on type
case $SHELL_TYPE in
    bash)
        if [ ! -f "$HOME/.bashrc" ] || ! grep -q "dotfiles" "$HOME/.bashrc"; then
            echo "source $DOTFILES_DIR/home/.bashrc" >> "$HOME/.bashrc"
        fi
        ;;
    zsh)
        if [ ! -f "$HOME/.zshrc" ] || ! grep -q "dotfiles" "$HOME/.zshrc"; then
            echo "source $DOTFILES_DIR/home/.zshrc" >> "$HOME/.zshrc"
        fi
        ;;
esac

echo "🐚 Shell configuration updated"
```

### Phase 7: Syncer Initialization

```bash
# Initialize the Syncer agent
echo "🔄 Initializing Syncer..."

# Register this machine
MACHINE_ID=$(hostname)-$(date +%s)
echo "$MACHINE_ID" > "$DOTFILES_DIR/.machine-id"

# Perform initial sync
cd "$DOTFILES_DIR"
git add .machine-id
git commit -m "Register new machine: $MACHINE_ID"
git push origin main

# Activate Syncer
echo "✅ Syncer activated for continuous synchronization"
```

### Phase 8: Verification

```bash
# Run health check
echo "🏥 Running system health check..."

# Check symlinks
BROKEN_LINKS=$(find ~ -maxdepth 3 -type l ! -exec test -e {} \; -print 2>/dev/null | wc -l)
if [ "$BROKEN_LINKS" -eq 0 ]; then
    echo "✅ All symlinks valid"
else
    echo "⚠️ Found $BROKEN_LINKS broken symlinks"
fi

# Check git status
cd "$DOTFILES_DIR"
if git diff --quiet && git diff --cached --quiet; then
    echo "✅ Repository clean"
else
    echo "⚠️ Uncommitted changes detected"
fi

# Check key tools
for tool in git node python cursor; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool installed"
    else
        echo "⚠️ $tool not found"
    fi
done
```

## Success Output

```
╔════════════════════════════════════════╗
║       MENTAT SETUP COMPLETE            ║
╠════════════════════════════════════════╣
║ Machine ID:    mac-studio-1735789234   ║
║ Dotfiles:      ✅ Synchronized          ║
║ Packages:      ✅ 47 installed          ║
║ Extensions:    ✅ 12 installed          ║
║ Syncer:        ✅ Active                ║
║                                        ║
║ Your development environment is ready! ║
║                                        ║
║ Next steps:                           ║
║ • Restart your terminal               ║
║ • Run /mentat:status to verify        ║
║ • Edit files - changes auto-sync      ║
╚════════════════════════════════════════╝
```

## Error Handling

### Common Issues and Solutions

1. **GitHub Authentication Failed**
   - Guide through SSH key generation
   - Offer HTTPS with token as alternative

2. **Dotfiles Repository Not Found**
   - Prompt for repository URL
   - Offer to create new repository

3. **Permission Denied**
   - Request sudo access for system packages
   - Offer user-space alternatives

4. **Network Issues**
   - Retry with exponential backoff
   - Offer offline setup mode

5. **Conflicting Files**
   - Backup existing files
   - Prompt for overwrite confirmation

## Options

The command supports these options:

- `--force`: Overwrite existing configurations
- `--minimal`: Skip package installation
- `--verbose`: Show detailed output
- `--dry-run`: Preview changes without applying

## Machine-Specific Configuration

If machine-specific configurations exist:

```bash
# Check for machine-specific overrides
MACHINE_TYPE=$(prompt "Select machine type: personal/work/server")
if [ -d "$DOTFILES_DIR/machines/$MACHINE_TYPE" ]; then
    echo "Applying $MACHINE_TYPE-specific configurations..."
    # Apply machine-specific settings
fi
```

## Post-Setup Hooks

Run any post-setup scripts:

```bash
if [ -f "$DOTFILES_DIR/hooks/post-setup.sh" ]; then
    echo "Running post-setup hooks..."
    bash "$DOTFILES_DIR/hooks/post-setup.sh"
fi
```

## Integration with Syncer

After successful setup, the Syncer agent is automatically activated to:
- Monitor file changes
- Sync with other machines
- Maintain configuration consistency

## Telemetry

Track setup metrics (optional, privacy-respecting):
- Setup duration
- Packages installed
- Errors encountered
- Success rate

This helps improve the setup process over time.