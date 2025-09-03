# CLAUDE.md

Mentat = Personal Claude Code customization framework built on SuperClaude v4.0.8
Package: `Mentat` | Version: `1.0.0-mentat` | Base: `SuperClaude Framework`

## Identity
- **Purpose**: Extensible personal customization layer for Claude Code
- **Architecture**: SuperClaude base + Mentat extensions (dotfiles sync is first feature)
- **Philosophy**: Add features as needed, following SuperClaude patterns

## Structure
```
/Users/ahmed/projects/Mentat/
├── mentat-extensions/       # Custom features
│   ├── agents/             # @syncer, @mentat-updater
│   └── commands/           # /mentat:* commands
├── setup/
│   ├── components/         # MentatExtensions, MentatDev
│   └── utils/              # ssh_auth, mentat_config
└── scripts/                # sync-orchestrator, test-ssh, etc.
```

## Quick Reference

### Commands
| Command | Purpose | Location |
|---------|---------|----------|
| `/mentat:setup` | Init new machine | `mentat-extensions/commands/setup.md` |
| `/mentat:sync` | Force dotfiles sync | `mentat-extensions/commands/sync.md` |
| `/mentat:config` | Configure repo (SSH/HTTPS) | `mentat-extensions/commands/config.md` |
| `/mentat:status` | Show sync status | `mentat-extensions/commands/status.md` |
| `/mentat:force-pull` | Safe destructive pull | `mentat-extensions/commands/force-pull.md` |
| `/mentat:update-claude-md` | Update ~/.claude/CLAUDE.md | `mentat-extensions/commands/update-claude-md.md` |
| `/mentat:packages` | Manage tracked packages | `mentat-extensions/commands/packages.md` |

### Agents
| Agent | Purpose | Category |
|-------|---------|----------|
| `@syncer` | Auto dotfiles sync | mentat |
| `@mentat-updater` | Framework updates (dev) | mentat |

### Key Scripts
| Script | Purpose | Path |
|--------|---------|------|
| `sync-orchestrator.sh` | Core sync engine | `scripts/` |
| `test-ssh.sh` | SSH diagnostics | `scripts/` |
| `health-monitor.sh` | Repo health check | `scripts/` |
| `version-bump.sh` | Semver mgmt | `scripts/` |

### Components
| Component | Type | Features Added |
|-----------|------|----------------|
| `ssh_auth.py` | Security | SSH key mgmt, GitHub auth, passphrase |
| `mentat_config.py` | Config | Interactive setup, validation |
| `MentatExtensionsComponent` | Install | User features (cmds, agents) |
| `MentatDevComponent` | Install | Dev tools (@mentat-updater) |

## Paths & Permissions
```
~/.mentat/config.json    # 0600 - repo URL, no creds
~/.mentat/sync.lock/     # 0700 - prevent concurrent
~/.mentat/sync.log       # logs, auto-rotate
~/dotfiles/              # canonical source, symlinked
~/.claude/               # SuperClaude + Mentat install
```

## Security Rules
- **Never auto-commit** - user handles git
- **Validate all inputs** - email, username, URLs
- **No credential storage** - use system SSH
- **Atomic permissions** - 0600 keys, 0700 dirs
- **Sanitize logs/commits** - no sensitive data
- **Force-pull = interactive only** - no automation

## Dev Workflow

### Install Dev Mode
```bash
cd /Users/ahmed/projects/Mentat
pipx install -e .
mentat install
```

### Add New Feature
1. Create in `mentat-extensions/` following patterns
2. Add component to `setup/components/` if needed
3. Update this CLAUDE.md & run `/mentat:update-claude-md`
4. Test: `bash scripts/test-*.sh`
5. Version: `./scripts/version-bump.sh [patch|minor|major]`

### Test Commands
```bash
/mentat:status                              # Check system
bash ~/.claude/scripts/sync-orchestrator.sh # Manual sync
bash scripts/test-ssh.sh                   # SSH diag
```

## Current Features

### 1. Dotfiles Sync
- **What**: Bidirectional GitHub sync every 30min
- **Repo**: Private GitHub, SSH auth recommended
- **Conflicts**: Auto-resolve simple, branch complex
- **Security**: Input validation, passphrase protect, sanitized commits

### 2. Package Management
- **What**: Track and sync all installed packages across machines
- **Tracks**: Homebrew (formulae/casks), npm global, pipx, Cursor extensions
- **Commands**: `/mentat:packages update|install|status|sync`
- **Scripts**: Auto-update package lists, batch installation

## Expansion Framework

### Planned Features
- [ ] will be added here


### Extension Hooks
- Pre/post sync hooks
- Custom conflict strategies
- Machine-specific configs
- Third-party integrations

### Adding Components
- **Commands**: Add `.md` to `mentat-extensions/commands/`
- **Agents**: Add `.md` with YAML to `mentat-extensions/agents/`
- **Utils**: Add `.py` to `setup/utils/`
- **Scripts**: Add `.sh` to `scripts/`

## Integration
- **With SuperClaude**: All base features available, Mentat adds on top
- **With Claude Code**: Config in `~/.claude/`, follows SC patterns
- **With Git**: Never auto-commit, user controls all commits

## Component Count
Commands: 7 | Agents: 2 | Scripts: 10 | Utils: 5 | Components: 2

---
*Token-optimized for Claude context. Update when adding features.*