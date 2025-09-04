# Command: /mentat:update

> "Evolving the Mentat framework to its latest form"

## Command Metadata

- **Trigger**: `/mentat:update`
- **Description**: Update Mentat framework to the latest version
- **Category**: Framework Management
- **Requires**: git, pipx, internet connection
- **Time Estimate**: 2-3 minutes

## Purpose

The `/mentat:update` command updates the Mentat framework itself to the latest version from GitHub, ensuring you have access to:
- New commands and agents
- Bug fixes and improvements  
- Enhanced features and capabilities
- Latest scripts and utilities

## Important Notes

- **This updates Mentat framework**, not your dotfiles
- **Your configuration is preserved** during updates
- **Requires pipx installation** (not dev mode)
- **Internet connection required** to fetch from GitHub

## Workflow

### Phase 1: Version Check

```bash
# Check current version
CURRENT_VERSION=$(cat ~/.claude/.mentat-version 2>/dev/null || echo "unknown")

# Fetch latest version from GitHub
LATEST_VERSION=$(curl -s https://raw.githubusercontent.com/a-alphayed/Mentat/main/VERSION)

# Compare versions
if [ "$CURRENT_VERSION" = "$LATEST_VERSION" ]; then
    echo "✅ Already on latest version: $CURRENT_VERSION"
    exit 0
fi

echo "📦 Update available!"
echo "Current: $CURRENT_VERSION"
echo "Latest:  $LATEST_VERSION"
```

### Phase 2: Backup Configuration

```bash
# Backup critical files
BACKUP_DIR="$HOME/.mentat-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Save configuration
cp -a ~/.mentat/config.json "$BACKUP_DIR/" 2>/dev/null || true
cp -a ~/.claude/.mentat-version "$BACKUP_DIR/" 2>/dev/null || true

echo "💾 Configuration backed up to: $BACKUP_DIR"
```

### Phase 3: Update via pipx

```bash
# Check if installed via pipx
if ! pipx list | grep -q "package Mentat"; then
    echo "❌ Mentat not installed via pipx"
    echo "Please use: pipx install git+https://github.com/a-alphayed/Mentat.git"
    exit 1
fi

# Reinstall from GitHub (gets latest)
echo "🔄 Updating Mentat framework..."
pipx reinstall Mentat --verbose

# Alternative for specific branch:
# pipx reinstall Mentat --spec git+https://github.com/a-alphayed/Mentat.git@develop
```

### Phase 4: Restore Configuration

```bash
# Restore configuration files
if [ -f "$BACKUP_DIR/config.json" ]; then
    cp "$BACKUP_DIR/config.json" ~/.mentat/
    echo "✅ Configuration restored"
fi

# Update version file
echo "$LATEST_VERSION" > ~/.claude/.mentat-version
```

### Phase 5: Verify Update

```bash
# Run verification
echo "🔍 Verifying installation..."

# Check key components exist
if [ -f ~/.claude/scripts/sync-orchestrator.sh ] && \
   [ -f ~/.claude/commands/mentat/update.md ] && \
   [ -f ~/.claude/agents/agent-syncer.md ]; then
    echo "✅ Core components verified"
else
    echo "⚠️ Some components may be missing"
fi

# Update CLAUDE.md
/mentat:update-claude-md

echo "🎉 Update complete! Version: $LATEST_VERSION"
echo "Run /mentat:status to verify everything is working"
```

## Alternative Update Methods

### Method 1: Force Reinstall (Simple)
```bash
pipx reinstall Mentat
```

### Method 2: Manual Update (Advanced)
```bash
# For development installations
cd ~/projects/Mentat  # Or your Mentat directory
git pull origin main
mentat install
```

### Method 3: Specific Version
```bash
# Install specific branch or tag
pipx reinstall Mentat --spec git+https://github.com/a-alphayed/Mentat.git@v1.1.0
```

## What Gets Updated

- **Commands**: New `/mentat:*` commands
- **Agents**: New `@agent` definitions  
- **Scripts**: Updated shell scripts in `~/.claude/scripts/`
- **Core Logic**: Python modules and components
- **Documentation**: Updated command help and descriptions

## What's Preserved

- **Your dotfiles repository**: No changes to `~/dotfiles/`
- **Configuration**: `~/.mentat/config.json` preserved
- **SSH keys**: No changes to authentication
- **Sync state**: Lock files and logs preserved
- **Custom settings**: Any personal modifications

## Changelog Viewing

To see what's new in each version:

```bash
# View changelog online
open https://github.com/a-alphayed/Mentat/blob/main/CHANGELOG.md

# Or fetch locally
curl -s https://raw.githubusercontent.com/a-alphayed/Mentat/main/CHANGELOG.md | head -30
```

## Troubleshooting

### Update Fails
```bash
# Clear pipx cache
pipx uninstall Mentat
pipx install git+https://github.com/a-alphayed/Mentat.git
```

### Configuration Lost
```bash
# Restore from backup
cp ~/.mentat-backup-*/config.json ~/.mentat/
```

### Components Missing
```bash
# Reinstall specific component
mentat install
```

## Success Output

```
╔════════════════════════════════════════╗
║       MENTAT UPDATE COMPLETE           ║
╠════════════════════════════════════════╣
║ Previous:  1.0.0-mentat                ║
║ Current:   1.1.0-mentat                ║
║                                        ║
║ What's New:                           ║
║ • Framework update command             ║  
║ • Improved symlink management          ║
║ • Enhanced error handling              ║
║                                        ║
║ Configuration: ✅ Preserved             ║
║ Components:    ✅ Updated               ║
║ Status:        ✅ Ready                 ║
╚════════════════════════════════════════╝
```

## Developer Notes

- Version stored in `/VERSION` file in repo
- Semantic versioning: `major.minor.patch-mentat`
- Updates pull from `main` branch by default
- Use `develop` branch for testing updates

## Security Considerations

- Only updates from official repository
- Backs up configuration before update
- No credentials or secrets modified
- Uses pipx isolation for safety