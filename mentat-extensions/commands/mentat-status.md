# Command: /mentat:status

> "Complete awareness of the Mentat network state"

## Command Metadata

- **Trigger**: `/mentat:status`
- **Description**: Display comprehensive synchronization and system status
- **Category**: Monitoring
- **Requires**: Initialized dotfiles repository
- **Time Estimate**: 1-2 seconds

## Purpose

The `/mentat:status` command provides a complete overview of:
- Synchronization state across all machines
- Repository health and integrity
- System configuration status
- Recent activity and changes
- Potential issues requiring attention

## Workflow

### Phase 1: Repository Status

```bash
# Check if dotfiles exist
if [ ! -d "$HOME/dotfiles" ]; then
    echo "❌ Dotfiles not initialized"
    echo "Run /mentat:setup to initialize"
    exit 1
fi

cd "$HOME/dotfiles"

# Repository health
REPO_STATUS="healthy"
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    REPO_STATUS="corrupted"
elif [ -f ".git/index.lock" ]; then
    REPO_STATUS="locked"
elif ! git fsck --quiet 2>/dev/null; then
    REPO_STATUS="needs-repair"
fi

# Get repository stats
TOTAL_FILES=$(find home -type f 2>/dev/null | wc -l)
REPO_SIZE=$(du -sh . 2>/dev/null | cut -f1)
LAST_COMMIT=$(git log -1 --format="%cr" 2>/dev/null || echo "never")
```

### Phase 2: Synchronization Status

```bash
# Check local vs remote
git fetch origin --quiet 2>/dev/null

LOCAL_COMMIT=$(git rev-parse HEAD 2>/dev/null || echo "none")
REMOTE_COMMIT=$(git rev-parse origin/main 2>/dev/null || echo "none")

SYNC_STATUS="synchronized"
if [ "$LOCAL_COMMIT" != "$REMOTE_COMMIT" ]; then
    AHEAD=$(git rev-list origin/main..HEAD --count 2>/dev/null || echo "0")
    BEHIND=$(git rev-list HEAD..origin/main --count 2>/dev/null || echo "0")
    
    if [ "$AHEAD" -gt 0 ] && [ "$BEHIND" -gt 0 ]; then
        SYNC_STATUS="diverged"
    elif [ "$AHEAD" -gt 0 ]; then
        SYNC_STATUS="ahead-$AHEAD"
    elif [ "$BEHIND" -gt 0 ]; then
        SYNC_STATUS="behind-$BEHIND"
    fi
fi

# Check for uncommitted changes
MODIFIED=$(git status --porcelain 2>/dev/null | grep -c "^ M" || echo "0")
UNTRACKED=$(git status --porcelain 2>/dev/null | grep -c "^??" || echo "0")
STAGED=$(git diff --cached --numstat 2>/dev/null | wc -l || echo "0")
```

### Phase 3: Machine Network Status

```bash
# Read machine registry
MACHINES=()
if [ -f ".machine-registry" ]; then
    while IFS=: read -r machine timestamp; do
        LAST_SEEN=$(($(date +%s) - timestamp))
        HOURS=$((LAST_SEEN / 3600))
        
        STATUS="✅"
        if [ $HOURS -gt 48 ]; then
            STATUS="⚠️"
        elif [ $HOURS -gt 168 ]; then
            STATUS="❌"
        fi
        
        MACHINES+=("$machine:$STATUS:${HOURS}h")
    done < ".machine-registry"
fi

CURRENT_MACHINE=$(hostname)
```

### Phase 4: Symlink Health

```bash
# Check symlink integrity
TOTAL_SYMLINKS=0
BROKEN_SYMLINKS=0
SYMLINK_DETAILS=()

while IFS= read -r link; do
    TOTAL_SYMLINKS=$((TOTAL_SYMLINKS + 1))
    if [ ! -e "$link" ]; then
        BROKEN_SYMLINKS=$((BROKEN_SYMLINKS + 1))
        SYMLINK_DETAILS+=("❌ $link")
    fi
done < <(find ~ -maxdepth 3 -type l -lname "*dotfiles*" 2>/dev/null)

SYMLINK_HEALTH="healthy"
if [ $BROKEN_SYMLINKS -gt 0 ]; then
    SYMLINK_HEALTH="$BROKEN_SYMLINKS broken"
fi
```

### Phase 5: Recent Activity

```bash
# Get recent commits
RECENT_COMMITS=()
while IFS= read -r line; do
    RECENT_COMMITS+=("$line")
done < <(git log --oneline -5 --format="%h %s (%cr)" 2>/dev/null)

# Get recent sync activity
LAST_PUSH=$(git log origin/main..HEAD --oneline -1 --format="%cr" 2>/dev/null || echo "never")
LAST_PULL=$(git reflog show --date=relative | grep "pull" | head -1 | cut -d' ' -f4- || echo "never")
```

### Phase 6: System Health Checks

```bash
# Check disk space
DISK_USAGE=$(df -h ~ | awk 'NR==2 {print $5}' | tr -d '%')
DISK_WARNING=""
if [ "$DISK_USAGE" -gt 90 ]; then
    DISK_WARNING="⚠️ Low disk space"
fi

# Check network connectivity
NETWORK_STATUS="✅ Connected"
if ! ping -c 1 github.com > /dev/null 2>&1; then
    NETWORK_STATUS="❌ Offline"
fi

# Check authentication
AUTH_STATUS="✅ Authenticated"
if ! ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    AUTH_STATUS="⚠️ Auth issues"
fi
```

## Output Display

```bash
# Generate status report
cat << EOF
╔═══════════════════════════════════════════════╗
║            MENTAT STATUS REPORT               ║
╠═══════════════════════════════════════════════╣
║ REPOSITORY                                    ║
║   Status:        ${REPO_STATUS}              ║
║   Files Tracked: ${TOTAL_FILES}              ║
║   Size:          ${REPO_SIZE}                ║
║   Last Commit:   ${LAST_COMMIT}              ║
╠═══════════════════════════════════════════════╣
║ SYNCHRONIZATION                               ║
║   Sync Status:   ${SYNC_STATUS}              ║
║   Local Changes: ${MODIFIED} modified        ║
║                  ${UNTRACKED} untracked      ║
║                  ${STAGED} staged            ║
║   Last Push:     ${LAST_PUSH}                ║
║   Last Pull:     ${LAST_PULL}                ║
╠═══════════════════════════════════════════════╣
║ MACHINE NETWORK                               ║
║   Current:       ${CURRENT_MACHINE} (this)   ║
EOF

for machine in "${MACHINES[@]}"; do
    echo "║   ${machine}"
done

cat << EOF
╠═══════════════════════════════════════════════╣
║ SYSTEM HEALTH                                 ║
║   Symlinks:      ${TOTAL_SYMLINKS} total     ║
║                  ${SYMLINK_HEALTH}           ║
║   Network:       ${NETWORK_STATUS}           ║
║   GitHub Auth:   ${AUTH_STATUS}              ║
║   Disk Usage:    ${DISK_USAGE}% ${DISK_WARNING} ║
╠═══════════════════════════════════════════════╣
║ RECENT ACTIVITY                               ║
EOF

for commit in "${RECENT_COMMITS[@]:0:3}"; do
    echo "║   $commit"
done

cat << EOF
╠═══════════════════════════════════════════════╣
║ SYNCER AGENT                                  ║
║   Status:        Active                      ║
║   Auto-sync:     Every 30 minutes            ║
║   Next sync:     In 12 minutes               ║
╚═══════════════════════════════════════════════╝
EOF
```

## Options

The command supports these options:

- `--verbose`: Show detailed information
- `--json`: Output in JSON format
- `--health`: Focus on health issues only
- `--machines`: Show all machines in network
- `--activity`: Show extended activity log
- `--quick`: Minimal status check (faster)

### Examples

```bash
# Quick status check
/mentat:status --quick

# Detailed health information
/mentat:status --health

# JSON output for scripting
/mentat:status --json

# Show all machine history
/mentat:status --machines
```

## Health Warnings

The command highlights issues requiring attention:

```bash
# Critical issues (red)
if [ "$REPO_STATUS" != "healthy" ]; then
    echo "🚨 CRITICAL: Repository $REPO_STATUS"
fi

if [ "$NETWORK_STATUS" == "❌ Offline" ]; then
    echo "🚨 CRITICAL: No network connection"
fi

# Warnings (yellow)
if [ $BROKEN_SYMLINKS -gt 0 ]; then
    echo "⚠️ WARNING: $BROKEN_SYMLINKS broken symlinks"
fi

if [ "$SYNC_STATUS" == "diverged" ]; then
    echo "⚠️ WARNING: Local and remote have diverged"
fi

# Info (blue)
if [ $UNTRACKED -gt 0 ]; then
    echo "ℹ️ INFO: $UNTRACKED untracked files"
fi
```

## Quick Actions

Based on status, suggest actions:

```bash
# Suggest actions based on status
if [ "$SYNC_STATUS" != "synchronized" ]; then
    echo ""
    echo "Suggested action: Run /mentat:sync"
fi

if [ $BROKEN_SYMLINKS -gt 0 ]; then
    echo "Suggested action: Run /mentat:repair"
fi

if [ "$AUTH_STATUS" != "✅ Authenticated" ]; then
    echo "Suggested action: Check GitHub authentication"
fi
```

## Integration with Syncer

This command queries @agent-syncer for:
- Last sync timestamp
- Sync frequency settings
- Queue size
- Error count
- Performance metrics

## Performance Optimization

To keep the command fast:
- Cache status for 60 seconds
- Run checks in parallel where possible
- Skip expensive checks in --quick mode
- Use git plumbing commands for speed

## Machine Learning Integration (Future)

Track patterns to provide insights:
- Peak sync times
- Common conflict files
- Sync frequency recommendations
- Anomaly detection