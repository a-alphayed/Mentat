# Mentat Framework Guide

## What is Mentat?

Mentat is a personal customization framework built on top of the SuperClaude Framework. While SuperClaude provides the core Claude Code automation capabilities, Mentat adds:

- **Dotfiles Synchronization**: Automatic cross-machine configuration sync
- **Package Management**: Track and install development tools consistently
- **Shell Enhancements**: Modern ZSH setup with productivity tools
- **Environment Consistency**: Ensure identical development setup everywhere

## Mentat vs SuperClaude

| Feature | SuperClaude | Mentat |
|---------|------------|--------|
| Base Framework | ✅ Core | ✅ Inherits all |
| Claude Code Integration | ✅ | ✅ Enhanced |
| Commands | `/sc:*` | `/mentat:*` |
| Dotfiles Management | ❌ | ✅ Full sync |
| Package Tracking | ❌ | ✅ Multi-manager |
| Shell Configuration | ❌ | ✅ Complete setup |
| Cross-Machine Sync | ❌ | ✅ Automatic |

## Quick Start

### First Time Setup

```bash
# 1. Install Mentat
pipx install git+https://github.com/a-alphayed/Mentat.git

# 2. Run interactive installer
mentat install

# 3. Setup your environment
/mentat:setup

# 4. Install tracked packages
/mentat:packages install
```

### Daily Usage

```bash
# Check system status
/mentat:status

# Sync dotfiles
/mentat:sync

# Update package tracking after installations
/mentat:packages update
```

## Core Features

### 1. Dotfiles Synchronization

Mentat maintains a GitHub repository of your configuration files:

- **Automatic Sync**: Every 30 minutes via cron/launchd
- **Bidirectional**: Changes from any machine propagate
- **Conflict Resolution**: Intelligent merge strategies
- **Machine Registry**: Track all connected devices

### 2. Package Management

Track and reproduce your exact development environment:

- **Homebrew**: Formulae, casks, and taps via Brewfile
- **npm**: Global packages in npm-global.txt
- **pipx**: Python tools in pipx-packages.txt
- **Cursor/VSCode**: Extensions in cursor-extensions.txt

### 3. Shell Configuration

Modern ZSH setup with productivity enhancements:

- **Powerlevel10k**: Beautiful and fast theme
- **zoxide**: Smarter `cd` that learns
- **eza**: Modern `ls` with icons
- **Syntax Highlighting**: Real-time validation
- **Custom Aliases**: Git shortcuts and utilities

### 4. Security

Built with security as a priority:

- **SSH Authentication**: Passphrase-protected keys
- **No Credential Storage**: API keys in local config only
- **Input Validation**: All user data sanitized
- **Atomic Operations**: Proper file permissions

## Commands Reference

| Command | Purpose |
|---------|---------|
| `/mentat:setup` | Initialize new machine |
| `/mentat:sync` | Force dotfiles sync |
| `/mentat:status` | System status check |
| `/mentat:packages` | Package management |
| `/mentat:config` | Configure repository |
| `/mentat:force-pull` | Override local files |
| `/mentat:update-claude-md` | Update documentation |

## Directory Structure

### Mentat Repository
```
Mentat/
├── mentat-extensions/     # Custom features
│   ├── agents/           # Sync agents
│   └── commands/         # Mentat commands
├── scripts/              # Core scripts
├── setup/                # Installation
└── Docs/                 # Documentation
```

### Dotfiles Repository
```
~/dotfiles/
├── home/                 # Config files
│   ├── .zprofile        # Login shell
│   ├── .zshrc           # Interactive shell
│   └── .zsh_functions   # Aliases
├── packages/            # Package lists
│   ├── Brewfile
│   ├── npm-global.txt
│   └── pipx-packages.txt
└── scripts/             # Management
```

## Workflow Examples

### Setting Up a New Machine

```bash
# 1. Install Mentat framework
pipx install git+https://github.com/a-alphayed/Mentat.git
mentat install

# 2. Configure dotfiles repo
/mentat:config

# 3. Initial setup
/mentat:setup

# 4. Install all packages
/mentat:packages install

# 5. Restart shell for changes
exec $SHELL
```

### After Installing New Software

```bash
# Install something new
brew install httpie
npm install -g typescript

# Update tracking
/mentat:packages update

# Sync to GitHub
/mentat:sync
```

### Troubleshooting Sync Issues

```bash
# Check health
bash ~/.claude/scripts/sync-orchestrator.sh health

# View logs
tail -f ~/.mentat/sync.log

# Force pull if needed
/mentat:force-pull
```

## Integration Points

### With Claude Code
- Commands available via `/mentat:` prefix
- Configuration in `~/.claude/` directory
- Seamless workflow integration

### With GitHub
- Private dotfiles repository
- SSH authentication recommended
- Automatic conflict resolution

### With SuperClaude
- All SuperClaude features available
- Mentat adds on top, doesn't replace
- Compatible command structure

## Best Practices

1. **Regular Syncing**: Let automatic sync run, manual sync when needed
2. **Package Updates**: Run `/mentat:packages update` after installations
3. **Commit Messages**: Use descriptive messages for dotfile changes
4. **Security**: Never commit secrets or API keys to dotfiles
5. **Testing**: Test configuration changes before syncing

## Common Issues

### Sync Lock Stuck
```bash
rm -rf ~/.mentat/sync.lock
```

### Package Installation Fails
```bash
# Verify package file
cat ~/dotfiles/packages/Brewfile

# Check individual manager
brew bundle check --file=~/dotfiles/packages/Brewfile
```

### SSH Authentication Issues
```bash
bash scripts/test-ssh.sh
```

## Advanced Usage

### Machine-Specific Configurations
Create `.local` files that won't sync:
- `.zsh_functions.local` - Machine-specific aliases
- `Brewfile.local` - Machine-specific packages

### Custom Sync Hooks
Add pre/post sync scripts in `~/dotfiles/scripts/`:
- `pre-sync.sh` - Run before sync
- `post-sync.sh` - Run after sync

### Manual Package Management
```bash
# Update specific package list
bash ~/dotfiles/scripts/update-package-lists.sh

# Install from specific list
brew bundle install --file=~/dotfiles/packages/Brewfile
```

## Contributing

Mentat is a personal framework, but contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

- **Issues**: [GitHub Issues](https://github.com/a-alphayed/Mentat/issues)
- **Documentation**: This guide and README.md
- **Commands**: Use `/mentat:status` for diagnostics

## License

MIT License - See LICENSE file for details.