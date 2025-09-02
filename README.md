# Mentat Framework

[![Version](https://img.shields.io/badge/version-1.0.0--mentat-blue)](https://github.com/a-alphayed/Mentat/releases)
[![Based on SuperClaude](https://img.shields.io/badge/based%20on-SuperClaude%20v4.0.8-purple)](https://github.com/SuperClaude-Org/SuperClaude_Framework)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> "It is by will alone I set my mind in motion"

Mentat is my personal compute/programming framework that transforms Claude Code into a hyper-intelligent agentic development environment.
## What is Mentat?

Mentat extends the SuperClaude Framework with customized capabilities, so far it provides:

- **Perfect Recall**: Your dotfiles are always synchronized across all machines
- **Automation**: Automated workflows and intelligent conflict resolution
- **Predictive Analysis**: Prevents conflicts before they occur
- **Total Awareness**: Multi-machine consciousness and health monitoring

## Core Components

### Agents

#### The Syncer Agent (`@agent-syncer`)

The Syncer maintains perfect synchronization of your development environment across all machines. It:
- **Auto-syncs** every 30 minutes and on startup/shutdown
- **Monitors** file changes in your dotfiles directory
- **Resolves** conflicts intelligently using merge strategies
- **Repairs** broken symlinks automatically
- **Tracks** all machines in your network

#### The Mentat Updater (`@agent-mentat-updater`)

Keeps your Mentat framework synchronized with upstream SuperClaude updates while preserving your customizations. It:
- **Checks** daily for SuperClaude Framework updates
- **Preserves** your custom agents, commands, and scripts
- **Rebases** your changes on top of new framework versions
- **Tests** compatibility after updates
- **Rollback** capability if updates cause issues

## Installation

### Step 1: Install the Package
```bash
# Install Mentat framework via pipx (recommended)
pipx install git+https://github.com/a-alphayed/Mentat.git

# Or via pip
pip install git+https://github.com/a-alphayed/Mentat.git
```

### Step 2: Run the Installer (Required!)
```bash
# Run the interactive installer to complete setup
mentat install
```

**Important**: The `mentat install` command is required after package installation. It will:
- Configure MCP servers for Claude Code
- Install Mentat agents and commands
- Set up dotfiles synchronization
- Configure API keys for services

## Quick Start

After installation is complete:

```bash
# Setup your environment on a new machine
/mentat:setup

# Check synchronization status
/mentat:status

# Force synchronization
/mentat:sync

# Force pull from remote (destructive - requires user confirmation)
/mentat:force-pull
```

## Key Features

- 🔄 **Automatic Synchronization**: Changes sync across machines without manual intervention
- 🏥 **Self-Healing**: Automatically repairs broken symlinks and resolves conflicts
- 📊 **Health Monitoring**: Continuous system health checks and status reporting
- 🔮 **Predictive Sync**: Prevents conflicts through intelligent timing
- 🖥️ **Multi-Machine Aware**: Tracks and syncs across all your development machines
- 🚀 **Zero-Config**: Works immediately after installation

## Commands

- `/mentat:setup` - Initialize a new machine with your complete environment
- `/mentat:sync` - Force synchronization across all machines
- `/mentat:status` - Display comprehensive system status
- `/mentat:force-pull` - Override local dotfiles with remote state (user-only, destructive)
- `/mentat:compute` - Analyze and optimize your environment (planned)
- `/mentat:recall` - Restore any previous configuration state (planned)

## Architecture

```text
Mentat/
├── mentat-core/           # Core SuperClaude components
├── mentat-extensions/     # Custom Mentat additions
│   ├── agents/           # Syncer and updater agents
│   ├── commands/         # Mentat-specific commands
│   └── modules/          # Supporting modules
└── scripts/              # Utility scripts
```

## The Mentat Philosophy

1. **Synchronized Mind**: All machines share the same configuration
2. **Preservation**: Every change is captured and preserved
3. **Prediction**: Conflicts are prevented, not resolved
4. **Self-Maintenance**: Auto-update, self-heal, self-optimize
5. **Invisible Service**: Operates seamlessly in the background

## Requirements

- Python 3.9+
- Git
- Claude Code
- GitHub account (for dotfiles repository)

## Installation

### From GitHub (Recommended)

```bash
pipx install git+https://github.com/a-alphayed/Mentat.git
mentat install
```

### Development Installation

```bash
git clone https://github.com/a-alphayed/Mentat.git
cd Mentat
pip install -e .
mentat install --dev
```

## Configuration

Mentat stores its configuration in `~/.claude/` alongside SuperClaude settings. Your dotfiles are managed in a separate repository (default: `~/dotfiles/`).

## Versioning

Mentat follows [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH-mentat** format
- **MAJOR**: Breaking changes to core functionality
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes and minor improvements

### Version Management

```bash
# Check current version
cat VERSION

# Bump version (patch/minor/major)
./scripts/version-bump.sh patch    # 1.0.0 → 1.0.1
./scripts/version-bump.sh minor    # 1.0.1 → 1.1.0
./scripts/version-bump.sh major    # 1.1.0 → 2.0.0
```

## License

MIT License - See [LICENSE](LICENSE) for details.

## Acknowledgments

- Built on top of [SuperClaude Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework) v4.0.8
