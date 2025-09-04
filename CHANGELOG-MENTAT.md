# Mentat Framework Changelog

All notable changes to the Mentat framework extensions will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2025-01-04

### Added
- **Framework Update System**
  - `/mentat:update` command for self-updating the framework
  - `framework-updater.sh` script for handling updates via pipx
  - Version tracking with `.mentat-version` file
  - Automatic backup and restore of configuration during updates
  - Update checking against GitHub repository

- **Symlink Management Consolidation**
  - `symlink-manager.sh` for centralized symlink management
  - Removed dependency on external dotfiles scripts
  - Integrated symlink verification into sync workflow

### Changed
- Consolidated all symlink management under Mentat control
- Updated `/mentat:setup` to use internal symlink manager
- Removed duplicate scripts from dotfiles repository
- Branch structure simplified (main + develop only)

### Fixed
- Circular dependency between Mentat and dotfiles scripts
- Duplicate functionality across repositories
- ELOOP error in symlink management

## [1.0.0-mentat] - 2025-01-02

### Added
- **Core Framework**
  - Initial release of Mentat framework extensions for SuperClaude
  - Built on SuperClaude v4.0.8 foundation
  - Extensible architecture for personal customizations

- **Dotfiles Synchronization**
  - Bidirectional sync with GitHub repository
  - Automatic 30-minute sync cycles
  - Conflict resolution system
  - Machine registry for multi-machine tracking

- **Commands**
  - `/mentat:setup` - Initialize new machine environment
  - `/mentat:sync` - Manual synchronization trigger
  - `/mentat:status` - Comprehensive system status
  - `/mentat:config` - Repository configuration (SSH/HTTPS)
  - `/mentat:force-pull` - Safe destructive pull with two-step verification
  - `/mentat:packages` - Package management (update/install/status/sync)
  - `/mentat:update-claude-md` - Documentation updates

- **Agents**
  - `@syncer` - Automatic dotfiles synchronization agent
  - `@mentat-updater` - Framework update agent (developer mode)

- **Package Management**
  - Homebrew tracking (formulae, casks, taps via Brewfile)
  - NPM global packages tracking
  - Pipx packages tracking
  - Cursor/VS Code extensions tracking
  - One-command restoration on new machines

- **Security Features**
  - SSH key generation with passphrase protection
  - Input validation for all user inputs
  - Atomic file permissions (0600 keys, 0700 directories)
  - No credential storage in configuration
  - Sanitized git commits
  - Force-pull safety checks (interactive only)

- **Scripts**
  - `sync-orchestrator.sh` - Core synchronization engine
  - `health-monitor.sh` - Repository health checks
  - `conflict-resolver.sh` - Intelligent merge conflict resolution
  - `test-ssh.sh` - SSH connectivity diagnostics
  - `force-pull.sh` - Two-step destructive pull process
  - `version-bump.sh` - Semantic versioning management

### Technical Details
- Python package installable via pipx
- Configuration stored in `~/.mentat/config.json`
- Lock files in `~/.mentat/sync.lock`
- Logs in `~/.mentat/sync.log`
- Components installed to `~/.claude/`

## [0.9.0-beta] - 2024-12-15

### Added
- Beta release for testing
- Core synchronization concept
- Basic command structure
- Initial agent implementation
- Proof of concept for dotfiles management

---

## Version History

Mentat uses semantic versioning with a special suffix:
- Format: `major.minor.patch-mentat`
- Example: `1.0.0-mentat`

The `-mentat` suffix distinguishes Mentat versions from the underlying SuperClaude framework.

## Updating Mentat

### For Users (After Implementation)
```bash
# Check for updates and update if available
/mentat:update

# Or force update
/mentat:update --force
```

### Current Workaround (Until /mentat:update is Released)
```bash
# Option 1: Reinstall via pipx (recommended)
pipx reinstall Mentat

# Option 2: Uninstall and reinstall
pipx uninstall Mentat
pipx install git+https://github.com/a-alphayed/Mentat.git
```

## Links

- [Mentat Repository](https://github.com/a-alphayed/Mentat)
- [SuperClaude Framework](https://github.com/SuperClaude-Org/SuperClaude_Framework)
- [Issue Tracker](https://github.com/a-alphayed/Mentat/issues)