# Mentat Framework

[![Version](https://img.shields.io/badge/version-1.1.0--mentat-blue)](https://github.com/a-alphayed/Mentat/releases)
[![Based on SuperClaude](https://img.shields.io/badge/based%20on-SuperClaude%20v4.0.8-purple)](https://github.com/SuperClaude-Org/SuperClaude_Framework)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> "It is by will alone I set my mind in motion"

**Mentat** is a customization framework for Claude Code that extends the SuperClaude Framework with intelligent dotfiles synchronization, automated environment management, and extensible agent/command system.

## Features

### Core Capabilities

- **Dotfiles Synchronization**: Automatic bidirectional sync across all machines via GitHub
- **Package Management**: Track and sync Homebrew, npm, pipx, and editor extensions
- **Environment Management**: Complete development environment setup and maintenance
- **Extensible Framework**: Custom agents and commands for Claude Code automation
- **Security First**: Protected SSH key generation, input validation, and atomic operations

### Intelligent Agents

- **@syncer**: Maintains perfect dotfiles synchronization with conflict resolution
- **@mentat-updater**: Keeps framework updated with upstream SuperClaude changes

## Quick Start

### Installation

```bash
# Install via pipx (recommended)
pipx install git+https://github.com/a-alphayed/Mentat.git

# Run the interactive installer (required)
mentat install
```

### Updating

```bash
# Update to latest version (after v1.1.0)
/mentat:update

# Or manually via pipx
pipx reinstall Mentat
```

### Basic Usage

```bash
# Setup new machine environment
/mentat:setup

# Check sync status
/mentat:status

# Force synchronization
/mentat:sync

# Package management
/mentat:packages update  # Update package tracking
/mentat:packages install # Install all tracked packages

# Update documentation
/mentat:update-claude-md
```

## Commands

| Command | Purpose |
|---------|---------|
| `/mentat:setup` | Initialize new machine with complete environment |
| `/mentat:sync` | Force dotfiles synchronization |
| `/mentat:status` | Display comprehensive system status |
| `/mentat:packages` | Manage tracked packages (update/install/status/sync) |
| `/mentat:update` | Update Mentat framework to latest version |
| `/mentat:force-pull` | Override local dotfiles with remote (destructive) |
| `/mentat:update-claude-md` | Refresh CLAUDE.md documentation |

## Recent Updates (v1.0.0-mentat)

### Package Management System
- **Automatic Tracking**: Captures all installed packages across package managers
- **Homebrew Integration**: Tracks formulae, casks, and taps via Brewfile
- **Development Tools**: Tracks npm globals, pipx packages, and editor extensions
- **One-Command Setup**: Install all packages on new machines with `/mentat:packages install`
- **Shell Enhancements**: Modern shell with Powerlevel10k, zoxide, eza, and syntax highlighting


## Security

For detailed security guidelines on protecting your dotfiles and credentials, see [SECURITY.md](SECURITY.md).

## Architecture

```text
Mentat/
├── mentat-core/              # SuperClaude Framework base
├── mentat-extensions/        # Mentat customizations
│   ├── agents/              # Custom agents (@syncer, @mentat-updater)
│   ├── commands/            # Mentat commands (/mentat:*)
│   └── modules/             # Supporting Python modules
├── scripts/                 # Shell utilities
│   ├── sync-orchestrator.sh # Main sync engine
│   ├── health-monitor.sh    # System health checks
│   └── conflict-resolver.sh # Intelligent conflict resolution
└── src/mentat/             # Python package source
```

## Configuration

- **Framework Config**: `~/.claude/` (SuperClaude settings)
- **Dotfiles Repository**: `~/dotfiles/` (GitHub-synced configurations)
- **Machine Registry**: `.machine-registry` (tracks all machines)
- **Sync Lock**: `~/.mentat/sync.lock` (prevents concurrent operations)

## Development

### Installation

```bash
git clone https://github.com/a-alphayed/Mentat.git
cd Mentat
pip install -e .
mentat install --dev
```

### Version Management

```bash
# Check version
cat VERSION

# Bump version
./scripts/version-bump.sh patch|minor|major
```

### Testing

```bash
# Test sync functionality
bash ~/.claude/scripts/sync-orchestrator.sh health

# Manual sync test
/mentat:sync
```

## Requirements

- Python 3.9+
- Git with GitHub access
- Claude Code
- pipx (recommended) or pip

## License

MIT License - See [LICENSE](LICENSE) for details.

Built on [SuperClaude Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework) v4.0.8
