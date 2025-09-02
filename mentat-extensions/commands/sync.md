# Command: /mentat:sync

> "Synchronizing memories across the Mentat network"

## Command Metadata

- **Trigger**: `/mentat:sync`
- **Description**: Force immediate synchronization of dotfiles across all machines
- **Category**: Synchronization
- **Requires**: Active internet connection, initialized dotfiles
- **Time Estimate**: 5-30 seconds

## Purpose

The `/mentat:sync` command provides manual control over the synchronization process, allowing users to:
- Force immediate sync when needed
- Resolve conflicts interactively
- Verify sync status
- Recover from sync issues

## Workflow

### Phase 1: Pre-Sync Validation

```bash
# Verify dotfiles repository exists
if [ ! -d "$HOME/dotfiles" ]; then
    echo "❌ Dotfiles not initialized. Run /mentat:setup first."
    exit 1
fi

cd "$HOME/dotfiles"

# Check repository health
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Repository corrupted. Initiating recovery..."
    @agent-syncer --recover
    exit 1
fi

# Check network connectivity
if ! git ls-remote origin > /dev/null 2>&1; then
    echo "⚠️ Cannot reach GitHub. Check your internet connection."
    echo "Local changes will be queued for later sync."
fi
```

### Phase 2: Status Assessment

```bash
# Check for local changes
LOCAL_CHANGES=$(git status --porcelain | wc -l)
if [ $LOCAL_CHANGES -gt 0 ]; then
    echo "📝 Found $LOCAL_CHANGES local changes"
    git status --short
fi

# Check for remote changes
git fetch origin --quiet
LOCAL_COMMIT=$(git rev-parse HEAD)
REMOTE_COMMIT=$(git rev-parse origin/main)

if [ "$LOCAL_COMMIT" != "$REMOTE_COMMIT" ]; then
    BEHIND=$(git rev-list HEAD..origin/main --count)
    AHEAD=$(git rev-list origin/main..HEAD --count)
    echo "📊 Local is $AHEAD commits ahead, $BEHIND commits behind remote"
fi
```

### Phase 3: Push Local Changes

```bash
# Stage and commit local changes
if [ $LOCAL_CHANGES -gt 0 ]; then
    echo "📤 Pushing local changes..."
    
    # Smart commit message
    CHANGED_FILES=$(git diff --name-only | head -3 | xargs basename | tr '\n' ', ')
    COMMIT_MSG="Manual sync from $(hostname): ${CHANGED_FILES%, }"
    
    git add -A
    git commit -m "$COMMIT_MSG" || {
        echo "⚠️ No changes to commit"
    }
    
    # Push with retry logic
    RETRY=0
    MAX_RETRIES=3
    while [ $RETRY -lt $MAX_RETRIES ]; do
        if git push origin main; then
            echo "✅ Successfully pushed local changes"
            break
        else
            RETRY=$((RETRY + 1))
            echo "⚠️ Push failed, attempt $RETRY of $MAX_RETRIES"
            sleep 2
        fi
    done
fi
```

### Phase 4: Pull Remote Changes

```bash
# Pull remote changes with conflict handling
if [ "$LOCAL_COMMIT" != "$REMOTE_COMMIT" ]; then
    echo "📥 Pulling remote changes..."
    
    # Try fast-forward merge first
    if git merge origin/main --ff-only 2>/dev/null; then
        echo "✅ Fast-forward merge successful"
    else
        echo "⚠️ Merge conflicts detected"
        
        # Try rebase
        if git rebase origin/main; then
            echo "✅ Rebase successful"
        else
            # Handle conflicts
            echo "🔀 Conflicts require manual resolution:"
            git status --short | grep "^UU"
            
            # Offer resolution options
            echo ""
            echo "Options:"
            echo "1. Accept remote changes (theirs)"
            echo "2. Keep local changes (ours)"
            echo "3. Manual merge"
            echo "4. Abort sync"
            
            read -p "Choose option [1-4]: " choice
            
            case $choice in
                1)
                    git checkout --theirs .
                    git add -A
                    git rebase --continue
                    ;;
                2)
                    git checkout --ours .
                    git add -A
                    git rebase --continue
                    ;;
                3)
                    echo "Please resolve conflicts manually, then run:"
                    echo "  git add -A && git rebase --continue"
                    exit 0
                    ;;
                4)
                    git rebase --abort
                    echo "❌ Sync aborted"
                    exit 1
                    ;;
            esac
        fi
    fi
fi
```

### Phase 5: Symlink Verification

```bash
# Verify all symlinks are intact
echo "🔗 Verifying symlinks..."

BROKEN_LINKS=0
while IFS= read -r link; do
    if [ ! -e "$link" ]; then
        echo "  ⚠️ Broken: $link"
        # Attempt to repair
        TARGET=$(readlink "$link")
        rm "$link"
        ln -s "$TARGET" "$link"
        if [ -e "$link" ]; then
            echo "  ✅ Repaired: $link"
        else
            BROKEN_LINKS=$((BROKEN_LINKS + 1))
        fi
    fi
done < <(find ~ -maxdepth 3 -type l -lname "*dotfiles*" 2>/dev/null)

if [ $BROKEN_LINKS -eq 0 ]; then
    echo "✅ All symlinks valid"
else
    echo "⚠️ $BROKEN_LINKS symlinks need manual repair"
fi
```

### Phase 6: Post-Sync Actions

```bash
# Run post-sync hooks if they exist
if [ -f "$HOME/dotfiles/hooks/post-sync.sh" ]; then
    echo "🎣 Running post-sync hooks..."
    bash "$HOME/dotfiles/hooks/post-sync.sh"
fi

# Update machine registry
echo "$(hostname):$(date +%s)" >> "$HOME/dotfiles/.sync-log"
git add .sync-log
git commit -m "Update sync log" --quiet
git push origin main --quiet
```

## Options

The command supports these options:

- `--force`: Force push/pull without prompting
- `--dry-run`: Show what would be synced without doing it
- `--verbose`: Show detailed sync information
- `--pull-only`: Only pull remote changes
- `--push-only`: Only push local changes
- `--check`: Check sync status without syncing

### Examples

```bash
# Force sync, accepting remote changes for conflicts
/mentat:sync --force

# Check what would be synced
/mentat:sync --dry-run

# Only pull updates from other machines
/mentat:sync --pull-only

# Verbose output for debugging
/mentat:sync --verbose
```

## Success Output

```
╔════════════════════════════════════════╗
║         SYNC COMPLETE                  ║
╠════════════════════════════════════════╣
║ 📤 Pushed:     3 files                 ║
║ 📥 Pulled:     2 files                 ║
║ 🔀 Merged:     1 conflict              ║
║ 🔗 Repaired:   0 symlinks              ║
║                                        ║
║ Status: ✅ Fully synchronized           ║
║                                        ║
║ Last sync from:                        ║
║   work-laptop: 2 hours ago            ║
║   home-desktop: 5 hours ago           ║
╚════════════════════════════════════════╝
```

## Error Recovery

### Corrupted Repository

```bash
if [ -f "$HOME/dotfiles/.git/index.lock" ]; then
    echo "🔓 Removing stale lock file..."
    rm "$HOME/dotfiles/.git/index.lock"
fi

# If corruption detected
if ! git fsck --quiet; then
    echo "🔧 Repairing repository..."
    git fsck --full
    git gc --aggressive
fi
```

### Network Issues

```bash
# Queue changes for later if offline
if ! ping -c 1 github.com > /dev/null 2>&1; then
    echo "📝 Offline mode - changes queued"
    git stash push -m "offline-queue-$(date +%s)"
    echo "Changes will sync when connection restored"
fi
```

### Authentication Problems

```bash
# Check authentication based on repository URL
CONFIG_FILE="$HOME/.mentat/config.json"
if [ -f "$CONFIG_FILE" ]; then
    REPO_URL=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('dotfiles_repo', ''))" 2>/dev/null)
    
    if [[ "$REPO_URL" == git@* ]]; then
        # SSH authentication check
        echo "🔐 Checking SSH authentication..."
        
        # Run comprehensive SSH test
        if [ -f "$HOME/.claude/scripts/test-ssh.sh" ]; then
            bash "$HOME/.claude/scripts/test-ssh.sh"
        else
            # Basic SSH checks
            if ! ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
                echo "❌ SSH authentication failed"
                echo ""
                echo "Quick fixes:"
                echo "1. Generate SSH key: ssh-keygen -t ed25519 -C 'your_email@example.com'"
                echo "2. Add to GitHub: https://github.com/settings/keys"
                echo "3. Add to agent: ssh-add ~/.ssh/id_ed25519"
                echo ""
                echo "Or reconfigure: /mentat:config"
            else
                echo "✅ SSH authentication working"
                echo "Repository may not exist or you may lack access"
            fi
        fi
    elif [[ "$REPO_URL" == https://* ]]; then
        echo "🔑 Using HTTPS authentication"
        echo "If authentication fails, you may need a Personal Access Token"
        echo "Create one at: https://github.com/settings/tokens"
    fi
fi
```

## Integration with Syncer

This command works with @agent-syncer:
- Uses same sync logic for consistency
- Updates Syncer's last-sync timestamp
- Triggers Syncer's health check after sync
- Respects Syncer's configuration

## Conflict Prevention

To minimize conflicts:
1. Sync frequently (Syncer does this automatically)
2. Commit small, atomic changes
3. Use machine-specific files when appropriate
4. Coordinate major changes across machines

## Performance Metrics

Track sync performance:
- Time taken
- Data transferred
- Conflicts encountered
- Success rate

These metrics help optimize the sync process.