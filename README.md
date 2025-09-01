# Mentat Framework

> "It is by will alone I set my mind in motion"

Mentat is an advanced meta-programming framework that transforms Claude Code into a hyper-intelligent development environment with perfect synchronization across all machines.

## What is Mentat?

Mentat extends the SuperClaude Framework with powerful dotfiles synchronization and automated environment management capabilities. Like the Mentats of Dune, it provides:

- **Perfect Recall**: Your dotfiles are always synchronized across all machines
- **Computational Precision**: Automated workflows and intelligent conflict resolution
- **Predictive Analysis**: Prevents conflicts before they occur
- **Total Awareness**: Multi-machine consciousness and health monitoring

## Core Components

### The Syncer Agent (`@agent-syncer`)

The Syncer maintains perfect synchronization of your development environment across all machines. It monitors, predicts, and resolves configuration changes automatically.

### The Mentat Updater (`@agent-mentat-updater`)

Keeps your Mentat framework synchronized with upstream SuperClaude updates while preserving your customizations.

## Quick Start

```bash
# Install Mentat
pipx install git+https://github.com/YOUR-USERNAME/Mentat.git
mentat install

# Setup your environment on a new machine
/mentat:setup

# Check synchronization status
/mentat:status

# Force synchronization
/mentat:sync
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
- `/mentat:compute` - Analyze and optimize your environment
- `/mentat:recall` - Restore any previous configuration state

## Architecture

```
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
pipx install git+https://github.com/YOUR-USERNAME/Mentat.git
mentat install
```

### Development Installation

```bash
git clone https://github.com/YOUR-USERNAME/Mentat.git
cd Mentat
pip install -e .
mentat install --dev
```

## Configuration

Mentat stores its configuration in `~/.claude/` alongside SuperClaude settings. Your dotfiles are managed in a separate repository (default: `~/dotfiles/`).

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## License

MIT License - See [LICENSE](LICENSE) for details.

## Acknowledgments

- Built on top of [SuperClaude Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)
- Inspired by Frank Herbert's Dune universe

---

*"The highest function of ecology is understanding consequences" - Frank Herbert*