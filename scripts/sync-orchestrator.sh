#!/bin/bash
# Mentat Sync Orchestrator
# Core synchronization logic for the Syncer agent

set -euo pipefail

# Configuration
DOTFILES_DIR="${DOTFILES_DIR:-$HOME/dotfiles}"
CONFIG_FILE="$HOME/.mentat/config.json"
SYNC_LOCK="$HOME/.mentat/sync.lock"
LOG_FILE="$HOME/.mentat/sync.log"
MAX_RETRIES=3
BATCH_DELAY=5

# Load configuration if available
if [ -f "$CONFIG_FILE" ]; then
    SYNC_BRANCH=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('sync_branch', 'main'))" 2>/dev/null || echo "main")
    AUTO_SYNC=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('auto_sync', True))" 2>/dev/null || echo "true")
else
    SYNC_BRANCH="main"
    AUTO_SYNC="true"
    log WARNING "Configuration file not found, using defaults"
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message" >> "$LOG_FILE"
    
    case "$level" in
        ERROR)   echo -e "${RED}❌ $message${NC}" >&2 ;;
        SUCCESS) echo -e "${GREEN}✅ $message${NC}" ;;
        WARNING) echo -e "${YELLOW}⚠️  $message${NC}" ;;
        INFO)    echo -e "${BLUE}ℹ️  $message${NC}" ;;
        *)       echo "$message" ;;
    esac
}

# Lock management
acquire_lock() {
    local timeout=${1:-30}
    local elapsed=0
    
    while [ $elapsed -lt $timeout ]; do
        if mkdir "$SYNC_LOCK" 2>/dev/null; then
            echo $$ > "$SYNC_LOCK/pid"
            return 0
        fi
        
        # Check if lock holder is still alive
        if [ -f "$SYNC_LOCK/pid" ]; then
            local lock_pid=$(cat "$SYNC_LOCK/pid" 2>/dev/null || echo "0")
            if ! kill -0 "$lock_pid" 2>/dev/null; then
                log WARNING "Removing stale lock from PID $lock_pid"
                rm -rf "$SYNC_LOCK"
                continue
            fi
        fi
        
        sleep 1
        elapsed=$((elapsed + 1))
    done
    
    return 1
}

release_lock() {
    rm -rf "$SYNC_LOCK"
}

# Cleanup on exit
cleanup() {
    local exit_code=$?
    release_lock
    if [ $exit_code -ne 0 ]; then
        log ERROR "Sync failed with exit code $exit_code"
    fi
}

trap cleanup EXIT

# Health check
verify_symlinks() {
    log INFO "Verifying dotfile symlinks..."
    
    # Use Mentat's symlink manager
    local symlink_script="$HOME/.claude/scripts/symlink-manager.sh"
    
    if [ -f "$symlink_script" ]; then
        bash "$symlink_script" verify
    else
        log WARNING "Symlink manager not found, skipping verification"
    fi
}

health_check() {
    log INFO "Running health check..."
    
    # Check repository exists
    if [ ! -d "$DOTFILES_DIR" ]; then
        log ERROR "Dotfiles directory not found: $DOTFILES_DIR"
        return 1
    fi
    
    cd "$DOTFILES_DIR"
    
    # Check git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log ERROR "Not a git repository: $DOTFILES_DIR"
        return 1
    fi
    
    # Check for corruption
    if ! git fsck --quiet 2>/dev/null; then
        log WARNING "Repository needs repair"
        git fsck --full
        git gc --aggressive
    fi
    
    # Check network and authentication
    if ! git ls-remote origin > /dev/null 2>&1; then
        log WARNING "Cannot reach remote repository"
        
        # Check if it's an SSH URL
        REMOTE_URL=$(git config --get remote.origin.url || echo "")
        if [[ "$REMOTE_URL" == git@* ]]; then
            log INFO "Testing SSH authentication..."
            
            # Test SSH to GitHub
            if ! ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
                log ERROR "SSH authentication to GitHub failed"
                log INFO "Run this command to troubleshoot: bash $HOME/.claude/scripts/test-ssh.sh"
                return 2
            fi
            
            log INFO "SSH authentication works, but cannot reach repository"
            log INFO "Possible causes:"
            log INFO "  • Repository doesn't exist yet"
            log INFO "  • Repository name is incorrect"
            log INFO "  • You don't have access to this repository"
        fi
        
        return 2
    fi
    
    log SUCCESS "Health check passed"
    return 0
}

# Push local changes
push_changes() {
    log INFO "Checking for local changes..."
    
    cd "$DOTFILES_DIR"
    
    # Check for changes
    if git diff --quiet && git diff --cached --quiet; then
        log INFO "No local changes to push"
        return 0
    fi
    
    # Stage all changes
    git add -A
    
    # Generate commit message with sanitized hostname
    local changed_count=$(git diff --cached --numstat | wc -l)
    # Sanitize hostname to prevent injection
    local machine=$(hostname | sed 's/[^a-zA-Z0-9._-]//g' | cut -c1-30)
    local timestamp=$(date '+%Y%m%d-%H%M%S')
    local commit_msg="Sync from $machine at $timestamp ($changed_count files)"
    
    # Get list of changed files for detailed message
    local changed_files=$(git diff --cached --name-only | head -5 | xargs -I {} basename {} | tr '\n' ', ')
    if [ -n "$changed_files" ]; then
        commit_msg="Sync from $machine: ${changed_files%, }"
    fi
    
    # Commit
    if git commit -m "$commit_msg"; then
        log SUCCESS "Committed $changed_count changes"
    else
        log WARNING "No changes to commit"
        return 0
    fi
    
    # Push with retry
    local retry=0
    while [ $retry -lt $MAX_RETRIES ]; do
        if git push origin main; then
            log SUCCESS "Pushed changes to remote"
            return 0
        fi
        
        retry=$((retry + 1))
        log WARNING "Push failed, attempt $retry of $MAX_RETRIES"
        sleep 2
    done
    
    log ERROR "Failed to push after $MAX_RETRIES attempts"
    return 1
}

# Pull remote changes
pull_changes() {
    log INFO "Checking for remote changes..."
    
    cd "$DOTFILES_DIR"
    
    # Fetch latest
    git fetch origin --quiet
    
    # Check if we're behind
    local local_commit=$(git rev-parse HEAD)
    local remote_commit=$(git rev-parse origin/main)
    
    if [ "$local_commit" = "$remote_commit" ]; then
        log INFO "Already up to date"
        return 0
    fi
    
    # Calculate commits behind
    local behind=$(git rev-list HEAD..origin/main --count)
    log INFO "Local is $behind commits behind remote"
    
    # Try fast-forward merge
    if git merge origin/main --ff-only 2>/dev/null; then
        log SUCCESS "Fast-forward merge successful"
        return 0
    fi
    
    # Try rebase
    log INFO "Attempting rebase..."
    if git rebase origin/main; then
        log SUCCESS "Rebase successful"
        return 0
    fi
    
    # Handle conflicts
    log WARNING "Conflicts detected during rebase"
    
    # Try to auto-resolve simple conflicts
    local conflicts=$(git diff --name-only --diff-filter=U)
    for file in $conflicts; do
        log INFO "Attempting to auto-resolve: $file"
        
        # For config files, prefer remote
        if [[ "$file" == *.conf ]] || [[ "$file" == *.config ]]; then
            git checkout --theirs "$file"
            git add "$file"
        # For shell rc files, try to merge
        elif [[ "$file" == *rc ]] || [[ "$file" == *.bash* ]] || [[ "$file" == *.zsh* ]]; then
            # This is simplified - in production, use a proper merge tool
            git checkout --ours "$file"
            git add "$file"
        fi
    done
    
    # Continue rebase if possible
    if git rebase --continue 2>/dev/null; then
        log SUCCESS "Conflicts resolved automatically"
        return 0
    fi
    
    # Abort and report
    git rebase --abort
    log ERROR "Manual conflict resolution required"
    return 1
}

# Verify symlinks
verify_symlinks() {
    log INFO "Verifying symlinks..."
    
    local broken_count=0
    local repaired_count=0
    
    # Find all symlinks pointing to dotfiles
    while IFS= read -r link; do
        if [ ! -e "$link" ]; then
            log WARNING "Broken symlink: $link"
            broken_count=$((broken_count + 1))
            
            # Try to repair
            local target=$(readlink "$link")
            if [ -f "$DOTFILES_DIR/home/${target#$HOME/}" ]; then
                rm "$link"
                ln -s "$DOTFILES_DIR/home/${target#$HOME/}" "$link"
                if [ -e "$link" ]; then
                    log SUCCESS "Repaired: $link"
                    repaired_count=$((repaired_count + 1))
                fi
            fi
        fi
    done < <(find "$HOME" -maxdepth 3 -type l -lname "*dotfiles*" 2>/dev/null)
    
    if [ $broken_count -eq 0 ]; then
        log SUCCESS "All symlinks valid"
    else
        log WARNING "Found $broken_count broken symlinks, repaired $repaired_count"
    fi
}

# Update machine registry
update_registry() {
    # Sanitize hostname to prevent injection
    local machine=$(hostname | sed 's/[^a-zA-Z0-9._-]//g' | cut -c1-30)
    local timestamp=$(date +%s)
    local registry="$DOTFILES_DIR/.machine-registry"
    
    # Create or update entry
    if [ -f "$registry" ]; then
        grep -v "^$machine:" "$registry" > "$registry.tmp" || true
    else
        touch "$registry.tmp"
    fi
    
    echo "$machine:$timestamp" >> "$registry.tmp"
    mv "$registry.tmp" "$registry"
    
    cd "$DOTFILES_DIR"
    git add ".machine-registry"
    git commit -m "Update machine registry: $machine" --quiet || true
    git push origin main --quiet || true
}

# Main sync function
sync() {
    local mode="${1:-full}"
    
    log INFO "Starting sync (mode: $mode)"
    
    # Acquire lock
    if ! acquire_lock; then
        log ERROR "Another sync is already running"
        return 1
    fi
    
    # Run health check
    if ! health_check; then
        log ERROR "Health check failed"
        return 1
    fi
    
    # Perform sync based on mode
    case "$mode" in
        full)
            push_changes || true
            pull_changes || true
            verify_symlinks
            update_registry
            ;;
        push)
            push_changes
            ;;
        pull)
            pull_changes
            verify_symlinks
            ;;
        force-pull)
            # SECURITY: Force-pull must only be run interactively by user
            if ! [[ -t 0 && -t 1 ]]; then
                log ERROR "SECURITY: Force-pull can only be run interactively"
                log ERROR "Use the dedicated force-pull.sh script or /mentat:force-pull command"
                return 1
            fi
            
            # Check if being called by automation
            local parent_cmd=$(ps -o comm= $PPID 2>/dev/null | tr -d ' ')
            if echo "$parent_cmd" | grep -qE "(cron|systemd|launchd|agent)"; then
                log ERROR "SECURITY: Force-pull cannot be run by automation"
                return 1
            fi
            
            log WARNING "Force-pull should use the dedicated script for safety"
            log INFO "Running: bash $HOME/.claude/scripts/force-pull.sh"
            
            # Delegate to the dedicated force-pull script with all safety checks
            bash "$HOME/.claude/scripts/force-pull.sh" "$@"
            return $?
            ;;
        check)
            # Just health check (already done)
            ;;
        *)
            log ERROR "Unknown sync mode: $mode"
            return 1
            ;;
    esac
    
    log SUCCESS "Sync completed successfully"
    return 0
}

# Auto-sync daemon
daemon() {
    local interval="${1:-1800}"  # Default 30 minutes
    
    log INFO "Starting sync daemon (interval: ${interval}s)"
    
    while true; do
        sync full
        log INFO "Next sync in $interval seconds"
        sleep "$interval"
    done
}

# Main execution
main() {
    local command="${1:-sync}"
    shift || true
    
    # Ensure log directory exists
    mkdir -p "$(dirname "$LOG_FILE")"
    
    case "$command" in
        sync)
            sync "$@"
            ;;
        daemon)
            daemon "$@"
            ;;
        health)
            health_check
            ;;
        push)
            push_changes
            ;;
        pull)
            pull_changes
            verify_symlinks
            ;;
        force-pull)
            # Force-pull requires interactive terminal
            if ! [[ -t 0 && -t 1 ]]; then
                echo "ERROR: Force-pull requires an interactive terminal session"
                echo "This command cannot be run by scripts or automation"
                exit 1
            fi
            sync "force-pull" "$@"
            ;;
        verify)
            verify_symlinks
            ;;
        *)
            echo "Usage: $0 {sync|daemon|health|push|pull|force-pull|verify} [options]"
            exit 1
            ;;
    esac
}

# Run if executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi