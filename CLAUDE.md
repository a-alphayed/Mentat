# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mentat (v1.0.0-mentat) is a custom fork of the SuperClaude Framework that extends it with intelligent dotfiles synchronization and automated environment management capabilities. The framework transforms Claude Code into a hyper-intelligent development environment with perfect synchronization across all machines.

**Note**: Package name changed from "SuperClaude" to "Mentat" to avoid conflicts with upstream.

## Key Architecture

### Framework Structure
- **Base Framework**: SuperClaude Framework v4.0.8 providing meta-programming capabilities
- **Mentat Extensions**: Custom agents and commands in `mentat-extensions/`
- **Dotfiles Management**: GitHub-based synchronization with `~/dotfiles/` as canonical source
- **Installation**: Python package installable via pipx

### Core Components

#### Custom Agents
- **@syncer** (`mentat-extensions/agents/agent-syncer.md`): Maintains perfect dotfiles synchronization across machines
- **@mentat-updater** (`mentat-extensions/agents/agent-mentat-updater.md`): Keeps framework updated with upstream SuperClaude while preserving customizations

#### Custom Commands
- `/mentat:setup` - Initialize new machine with complete environment
- `/mentat:sync` - Force dotfiles synchronization
- `/mentat:status` - Display comprehensive system status

#### Supporting Scripts
- `scripts/sync-orchestrator.sh` - Main synchronization engine with secure lock management
- `scripts/health-monitor.sh` - Repository health and integrity checks
- `scripts/conflict-resolver.sh` - Intelligent conflict resolution
- `scripts/version-bump.sh` - Semantic versioning management

## Development Commands

### Installation
```bash
# Install Mentat framework (package name: Mentat)
pipx install git+https://github.com/a-alphayed/Mentat.git
mentat install

# Development installation (editable mode)
cd /Users/afayed/Projects/mentat
pipx install -e .
mentat install

# Update from source
cd /Users/afayed/Projects/mentat
# Changes apply immediately in editable mode
```

### Testing
```bash
# Test sync functionality
bash ~/.claude/scripts/sync-orchestrator.sh sync

# Check health
bash ~/.claude/scripts/sync-orchestrator.sh health

# Run status check
/mentat:status
```

### Building and Publishing
```bash
# Clean build artifacts
bash scripts/cleanup.sh

# Build package
python -m build

# Publish to PyPI (when ready)
bash scripts/publish.sh
```

## Dotfiles Synchronization Workflow

The system maintains bidirectional sync between local machine and GitHub repository:

1. **GitHub as Source of Truth**: Repository at `https://github.com/a-alphayed/dotfiles.git`
2. **Local Directory**: `~/dotfiles/` with symlinks to actual locations
3. **Automatic Sync**: Every 30 minutes or on-demand via `/mentat:sync`
4. **Conflict Prevention**: Smart merge strategies and machine attribution

### Directory Structure
```
~/dotfiles/
├── home/           # Files symlinked from home directory
├── packages/       # Package lists (Brewfile, npm, Cursor extensions)
├── scripts/        # Utility scripts
└── special/        # App-specific configs (Cursor settings)
```

## Working with Mentat

### Adding New Dotfiles
1. Copy file to appropriate `~/dotfiles/` subdirectory
2. Create symlink from original location
3. Run sync: `bash ~/.claude/scripts/sync-orchestrator.sh sync`

### Updating Packages
```bash
# Update Brewfile
brew bundle dump --file=~/dotfiles/packages/Brewfile --force

# Update Cursor extensions
cursor --list-extensions > ~/dotfiles/packages/cursor-extensions.txt

# Sync changes
/mentat:sync
```

### Framework Updates
The Mentat Updater agent checks daily for upstream SuperClaude updates and can safely rebase while preserving customizations.

## Important Context

- **Never auto-commit**: User handles all git commits manually
- **Symlinks are critical**: Always verify symlinks when making changes
- **Machine Registry**: Tracks all machines in `.machine-registry`
- **Conflict Resolution**: Automatic for simple conflicts, creates branch for complex ones
- **Security**: Never sync sensitive files (.ssh/*, *.key, *.pem)

## Integration Points

### With SuperClaude Components
- All SuperClaude agents and commands remain available
- Mentat extensions are in separate `mentat-extensions/` directory
- Custom agents appear in "mentat" category

### With Claude Code
- Configuration stored in `~/.claude/`
- Agents require YAML frontmatter to be recognized
- Commands follow SuperClaude markdown format

## Common Tasks

### Check sync status
```bash
/mentat:status
```

### Force sync now
```bash
/mentat:sync
# or
bash ~/.claude/scripts/sync-orchestrator.sh sync
```

### Install on new machine
```bash
/mentat:setup
```

### Update framework from upstream
```bash
@mentat-updater
```

### Version management
```bash
# Check current version
cat VERSION

# Bump version
./scripts/version-bump.sh patch  # 1.0.0 → 1.0.1
./scripts/version-bump.sh minor  # 1.0.1 → 1.1.0
./scripts/version-bump.sh major  # 1.1.0 → 2.0.0
```

## Recent Changes (v1.0.0-mentat)

### Security Improvements
- **Lock file**: Moved from `/tmp/mentat-sync.lock` to `~/.mentat/sync.lock` with 700 permissions
- **Machine registry**: Uses generic IDs instead of hostnames for privacy
- **Configuration sanitization**: P10k and other configs sanitized before syncing

### Package Changes
- **Name**: Changed from "SuperClaude" to "Mentat" to avoid pipx conflicts
- **Version**: Now using semantic versioning with "-mentat" suffix
- **Branch**: Main development branch renamed from `mentat` to `main`

### New Features
- **Version management**: Added VERSION file and version-bump.sh script
- **Enhanced dotfiles support**: Added terminal configs (WezTerm, FZF, P10k, ccstatusline)