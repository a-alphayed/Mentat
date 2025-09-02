# Command: /mentat:force-pull

> "Complete override from the Mentat collective consciousness"

## Command Metadata

- **Trigger**: `/mentat:force-pull`
- **Description**: Prepares a force pull of dotfiles from remote repository to override all local dotfiles
- **Category**: Synchronization
- **Requires**: Active internet connection, initialized dotfiles repository
- **Time Estimate**: 10-60 seconds total (preparation + execution)
- **Risk Level**: **CRITICAL** - Overwrites local changes, destroys local data
- **Execution Model**: **TWO-STEP PROCESS** - Claude prepares, user executes in terminal

## ⚠️ CRITICAL SAFETY NOTICE

**This is a two-step process for safety:**

1. **Step 1 (Claude Code)**: The `/mentat:force-pull` command validates your environment, analyzes impact, and prepares a temporary execution script
2. **Step 2 (Your Terminal)**: You manually run the generated script in your terminal with full interactive control

This design ensures:
- No accidental automation can trigger destructive operations
- You have full visibility into what will happen before execution
- You maintain complete control with ability to cancel at any point
- A backup is always created before any changes

The temporary execution script self-deletes after use or expires in 10 minutes for security.

## Purpose

The `/mentat:force-pull` command provides a way to completely reset local dotfiles to match the remote repository state. This is useful for:
- Recovering from local corruption or misconfiguration
- Resetting a machine to known-good state
- Onboarding a machine that has conflicting local dotfiles
- Discarding all local experiments and returning to baseline

## How It Works

### Step 1: Claude Code Preparation Phase

When you run `/mentat:force-pull`, Claude Code will:

1. **Validate Environment**
   - Check dotfiles repository exists and is healthy
   - Verify remote repository connectivity
   - Ensure git configuration is correct

2. **Analyze Impact**
   - Count uncommitted changes that will be lost
   - Identify symlinks that will be recreated
   - Calculate backup size requirements

3. **Generate Execution Script**
   - Create a temporary script at `~/.mentat/temp-force-pull.sh`
   - Include all safety checks and confirmation prompts
   - Set 10-minute expiration for security

4. **Provide Clear Instructions**
   - Display exactly what will happen
   - Show the command to run in your terminal
   - Explain recovery options if needed

### Step 2: Terminal Execution Phase

After Claude Code prepares everything, you:

1. **Open your terminal** (not through Claude Code)
2. **Run the generated command** shown by Claude
3. **Confirm the operation** when prompted (type 'YES')
4. **Wait for completion** (usually 10-60 seconds)

The execution script will:
- Create a full backup before any changes
- Reset your repository to match remote
- Recreate all symlinks
- Update the machine registry
- Self-delete when complete

## Detailed Workflow

### Phase 1: Preparation (Handled by Claude Code)

```bash
# The force-pull-prepare.sh script runs these checks:
# 1. Validates dotfiles repository exists
# 2. Checks git repository health  
# 3. Verifies remote connectivity
# 4. Analyzes uncommitted changes
# 5. Counts affected symlinks
# 6. Generates execution script

# 7. Creates temporary execution script at ~/.mentat/temp-force-pull.sh
```

### Phase 2: Execution (In Your Terminal)

The generated script performs these operations:

1. **Final Safety Confirmation** - Requires typing 'YES' in capitals
2. **Full Backup Creation** - Saves current state to `~/.mentat/backups/`
3. **Repository Reset** - Forces local to match remote exactly
4. **Symlink Recreation** - Removes old and creates fresh symlinks
5. **Registry Update** - Records the force-pull operation
6. **Self-Cleanup** - Deletes the temporary script when done
```

## Usage Examples

### Basic Force Pull
```bash
# Step 1: In Claude Code
/mentat:force-pull

# Step 2: In your terminal (command shown by Claude)
~/.mentat/temp-force-pull.sh
```

### Analyze Without Executing
```bash
# Just see what would happen without generating script
/mentat:force-pull --dry-run
```

## Expected Output

### After Step 1 (Claude Code):
```
╔════════════════════════════════════════╗
║         READY FOR FORCE-PULL           ║
╚════════════════════════════════════════╝

To complete the force-pull, run this command in your terminal:

   ~/.mentat/temp-force-pull.sh

This command will:
  1. Ask for final confirmation
  2. Create a backup of current state
  3. Reset to remote repository state
  4. Recreate all symlinks
  5. Self-delete the temporary script

The script will expire and self-delete in 10 minutes for security.
```

### After Step 2 (Terminal Execution):
```
╔════════════════════════════════════════╗
║       FORCE PULL COMPLETE              ║
╠════════════════════════════════════════╣
║ 📦 Backup:     ~/.mentat/backups/...   ║
║ 🔄 Reset to:   origin/main @ abc123    ║
║ 🔗 Symlinks:   25 created              ║
║                                        ║
║ Status: ✅ Local matches remote        ║
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