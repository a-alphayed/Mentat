# Command: /mentat:force-pull

> "Complete override from the Mentat collective consciousness"

## Command Metadata

- **Trigger**: `/mentat:force-pull`
- **Description**: Force pull dotfiles from remote repository and override all local dotfiles
- **Category**: Synchronization
- **Requires**: Active internet connection, initialized dotfiles repository, **INTERACTIVE USER SESSION**
- **Time Estimate**: 10-60 seconds
- **Risk Level**: **CRITICAL** - Overwrites local changes, destroys local data
- **Execution**: **USER-ONLY** - Cannot be run by automation, scripts, or agents

## ⚠️ CRITICAL SAFETY NOTICE

**This command can ONLY be executed by a human user in an interactive terminal session.**

Safety mechanisms prevent execution by:
- The Syncer agent or any other agents
- Shell scripts or automation tools
- Cron jobs, systemd timers, or launchd
- CI/CD pipelines or deployment systems
- Non-interactive SSH sessions
- Piped or redirected input/output

Even with `--no-prompt` flag, human verification is required to ensure conscious user action.

## Purpose

The `/mentat:force-pull` command provides a way to completely reset local dotfiles to match the remote repository state. This is useful for:
- Recovering from local corruption or misconfiguration
- Resetting a machine to known-good state
- Onboarding a machine that has conflicting local dotfiles
- Discarding all local experiments and returning to baseline

## Workflow

### Phase 1: Pre-Pull Validation

```bash
# Verify dotfiles repository exists
if [ ! -d "$HOME/dotfiles" ]; then
    echo "❌ Dotfiles not initialized. Run /mentat:setup first."
    exit 1
fi

cd "$HOME/dotfiles"

# Check repository health
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Repository corrupted. Cannot proceed with force pull."
    exit 1
fi

# Check network connectivity
if ! git ls-remote origin > /dev/null 2>&1; then
    echo "❌ Cannot reach GitHub. Check your internet connection."
    exit 1
fi

# Warning prompt (unless --no-prompt flag)
if [ "$NO_PROMPT" != "true" ]; then
    echo "⚠️  WARNING: This will OVERRIDE all local dotfiles with remote versions"
    echo "   All local changes will be PERMANENTLY LOST"
    echo ""
    read -p "Are you sure? Type 'yes' to continue: " confirmation
    if [ "$confirmation" != "yes" ]; then
        echo "❌ Force pull cancelled"
        exit 0
    fi
fi
```

### Phase 2: Create Backup

```bash
# Create timestamped backup
BACKUP_DIR="$HOME/.mentat/backups/$(date +%Y%m%d-%H%M%S)"
echo "📦 Creating backup at $BACKUP_DIR..."

mkdir -p "$BACKUP_DIR"

# Backup current dotfiles state
cp -Ra "$HOME/dotfiles" "$BACKUP_DIR/dotfiles-backup" 2>/dev/null || true

# Backup current symlink targets
while IFS= read -r link; do
    if [ -L "$link" ]; then
        TARGET=$(readlink "$link")
        REL_PATH="${link#$HOME/}"
        mkdir -p "$BACKUP_DIR/symlinks/$(dirname "$REL_PATH")"
        echo "$TARGET" > "$BACKUP_DIR/symlinks/$REL_PATH.target"
        
        # Copy actual file if it exists
        if [ -f "$link" ]; then
            cp -a "$link" "$BACKUP_DIR/symlinks/$REL_PATH.backup"
        fi
    fi
done < <(find "$HOME" -maxdepth 3 -type l -lname "*dotfiles*" 2>/dev/null)

echo "✅ Backup created at $BACKUP_DIR"
```

### Phase 3: Force Pull from Remote

```bash
cd "$HOME/dotfiles"

echo "🔄 Fetching latest from remote..."
git fetch origin --all

echo "💥 Discarding all local changes..."
# Stash any uncommitted changes (for record keeping)
git stash push -m "force-pull-backup-$(date +%s)" --include-untracked || true

# Reset to remote state
git reset --hard origin/main

echo "✅ Local repository reset to match remote"

# Clean up any untracked files
git clean -fdx

echo "🧹 Cleaned untracked files"
```

### Phase 4: Remove Old Symlinks

```bash
echo "🔗 Removing old symlinks..."

# Find and remove all existing dotfile symlinks
REMOVED_COUNT=0
while IFS= read -r link; do
    if [ -L "$link" ]; then
        rm "$link"
        REMOVED_COUNT=$((REMOVED_COUNT + 1))
    fi
done < <(find "$HOME" -maxdepth 3 -type l -lname "*dotfiles*" 2>/dev/null)

echo "✅ Removed $REMOVED_COUNT old symlinks"
```

### Phase 5: Create Fresh Symlinks

```bash
echo "🔗 Creating fresh symlinks from remote state..."

CREATED_COUNT=0

# Symlink files from home/
if [ -d "$HOME/dotfiles/home" ]; then
    for file in "$HOME/dotfiles/home"/.*; do
        [ -f "$file" ] || continue
        basename=$(basename "$file")
        
        # Skip . and ..
        [[ "$basename" == "." || "$basename" == ".." ]] && continue
        
        # Remove existing file/directory if present
        if [ -e "$HOME/$basename" ] && [ ! -L "$HOME/$basename" ]; then
            echo "  ⚠️ Backing up existing $HOME/$basename"
            mv "$HOME/$basename" "$HOME/$basename.pre-force-pull"
        fi
        
        # Create symlink
        ln -sf "$file" "$HOME/$basename"
        CREATED_COUNT=$((CREATED_COUNT + 1))
        echo "  ✅ Linked $basename"
    done
fi

# Symlink Cursor settings
if [ -d "$HOME/dotfiles/special/cursor" ]; then
    CURSOR_DIR="$HOME/Library/Application Support/Cursor/User"
    mkdir -p "$CURSOR_DIR"
    
    for file in "$HOME/dotfiles/special/cursor"/*; do
        [ -f "$file" ] || continue
        basename=$(basename "$file")
        
        # Backup existing
        if [ -f "$CURSOR_DIR/$basename" ] && [ ! -L "$CURSOR_DIR/$basename" ]; then
            mv "$CURSOR_DIR/$basename" "$CURSOR_DIR/$basename.pre-force-pull"
        fi
        
        ln -sf "$file" "$CURSOR_DIR/$basename"
        CREATED_COUNT=$((CREATED_COUNT + 1))
        echo "  ✅ Linked Cursor $basename"
    done
fi

# Symlink .config files
if [ -d "$HOME/dotfiles/config" ]; then
    mkdir -p "$HOME/.config"
    
    for dir in "$HOME/dotfiles/config"/*; do
        [ -d "$dir" ] || continue
        basename=$(basename "$dir")
        
        # Backup existing
        if [ -d "$HOME/.config/$basename" ] && [ ! -L "$HOME/.config/$basename" ]; then
            mv "$HOME/.config/$basename" "$HOME/.config/$basename.pre-force-pull"
        fi
        
        ln -sf "$dir" "$HOME/.config/$basename"
        CREATED_COUNT=$((CREATED_COUNT + 1))
        echo "  ✅ Linked .config/$basename"
    done
fi

echo "✅ Created $CREATED_COUNT fresh symlinks"
```

### Phase 6: Install Packages

```bash
# Reinstall packages from remote lists
if [ "$INSTALL_PACKAGES" = "true" ]; then
    echo "📦 Installing packages from remote lists..."
    
    # Homebrew packages
    if [ -f "$HOME/dotfiles/packages/Brewfile" ] && command -v brew >/dev/null; then
        echo "  🍺 Installing Homebrew packages..."
        brew bundle --file="$HOME/dotfiles/packages/Brewfile"
    fi
    
    # NPM global packages
    if [ -f "$HOME/dotfiles/packages/npm-global.txt" ] && command -v npm >/dev/null; then
        echo "  📦 Installing NPM packages..."
        cat "$HOME/dotfiles/packages/npm-global.txt" | xargs npm install -g
    fi
    
    # Cursor extensions
    if [ -f "$HOME/dotfiles/packages/cursor-extensions.txt" ] && command -v cursor >/dev/null; then
        echo "  🎨 Installing Cursor extensions..."
        cat "$HOME/dotfiles/packages/cursor-extensions.txt" | xargs -L 1 cursor --install-extension
    fi
fi
```

### Phase 7: Post-Pull Actions

```bash
# Run post-pull hooks if they exist
if [ -f "$HOME/dotfiles/hooks/post-pull.sh" ]; then
    echo "🎣 Running post-pull hooks..."
    bash "$HOME/dotfiles/hooks/post-pull.sh"
fi

# Update machine registry
echo "📝 Updating machine registry..."
cd "$HOME/dotfiles"
echo "$(hostname):force-pull:$(date +%s)" >> ".sync-log"
git add ".sync-log"
git commit -m "Force pull on $(hostname)" --quiet || true
git push origin main --quiet || true

# Reload shell configuration
echo "🔄 Reloading shell configuration..."
if [ -n "$ZSH_VERSION" ]; then
    source "$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    source "$HOME/.bashrc"
fi
```

## Options

The command supports these options:

- `--no-prompt`: Skip confirmation prompt (dangerous!)
- `--backup`: Create backup (default: true)
- `--no-backup`: Skip backup creation (dangerous!)
- `--install-packages`: Reinstall packages from remote lists
- `--dry-run`: Show what would be changed without doing it
- `--only [path]`: Only force-pull specific subdirectory
- `--restore [backup-dir]`: Restore from a previous backup

### Examples

```bash
# Force pull with confirmation prompt
/mentat:force-pull

# Force pull without prompt (CI/automation)
/mentat:force-pull --no-prompt

# Force pull and reinstall all packages
/mentat:force-pull --install-packages

# See what would be changed
/mentat:force-pull --dry-run

# Force pull only home directory files
/mentat:force-pull --only home/

# Restore from backup if something goes wrong
/mentat:force-pull --restore ~/.mentat/backups/20240115-143022
```

## Success Output

```
╔════════════════════════════════════════╗
║       FORCE PULL COMPLETE              ║
╠════════════════════════════════════════╣
║ 📦 Backup:     ~/.mentat/backups/...   ║
║ 🔄 Reset to:   origin/main @ abc123    ║
║ 🔗 Symlinks:   25 created              ║
║ 📦 Packages:   Not installed           ║
║                                        ║
║ Status: ✅ Local matches remote        ║
║                                        ║
║ ⚠️  Previous local state backed up     ║
║ Run with --restore to undo            ║
╚════════════════════════════════════════╝
```

## Error Recovery

### Restore from Backup

```bash
# If force-pull causes issues, restore previous state
BACKUP_DIR="$1"  # Pass backup directory path

if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Backup directory not found: $BACKUP_DIR"
    exit 1
fi

echo "🔄 Restoring from backup: $BACKUP_DIR"

# Restore dotfiles repository
if [ -d "$BACKUP_DIR/dotfiles-backup" ]; then
    rm -rf "$HOME/dotfiles"
    cp -Ra "$BACKUP_DIR/dotfiles-backup" "$HOME/dotfiles"
    echo "✅ Restored dotfiles repository"
fi

# Restore symlinks
if [ -d "$BACKUP_DIR/symlinks" ]; then
    find "$BACKUP_DIR/symlinks" -name "*.target" | while read -r target_file; do
        REL_PATH="${target_file#$BACKUP_DIR/symlinks/}"
        REL_PATH="${REL_PATH%.target}"
        LINK_PATH="$HOME/$REL_PATH"
        TARGET=$(cat "$target_file")
        
        mkdir -p "$(dirname "$LINK_PATH")"
        ln -sf "$TARGET" "$LINK_PATH"
    done
    echo "✅ Restored symlinks"
fi

echo "✅ Restore complete"
```

### Network Issues

```bash
# If network fails during pull
if ! git fetch origin; then
    echo "❌ Network error during force pull"
    echo "🔄 Attempting to restore from backup..."
    # Trigger restore logic
fi
```

### Repository Corruption

```bash
# If repository becomes corrupted
if ! git fsck --quiet; then
    echo "🔧 Repository corrupted, attempting repair..."
    git fsck --full --no-dangling
    git gc --aggressive --prune=now
    
    # If still broken, re-clone
    if ! git fsck --quiet; then
        echo "🔄 Re-cloning repository..."
        mv "$HOME/dotfiles" "$HOME/dotfiles.corrupted"
        git clone git@github.com:USERNAME/dotfiles.git "$HOME/dotfiles"
    fi
fi
```

## Integration with Syncer

This command complements the Syncer agent:
- Uses same repository and structure
- Updates Syncer's tracking files
- Can be triggered by Syncer when conflicts are unresolvable
- Respects Syncer's configuration for paths and exclusions

## Safety Considerations

**⚠️ WARNING**: This command is destructive and will:
1. **Delete all local changes** in the dotfiles repository
2. **Override all symlinked files** with remote versions
3. **Remove any local-only dotfiles** not in the repository

Always ensure you have important local changes pushed to remote before using this command.

## Performance Metrics

Track force-pull operations:
- Time taken
- Files changed
- Symlinks recreated
- Backup size
- Success rate

These metrics help identify patterns in when force-pulls are needed.