#!/bin/bash
# Mentat Force Pull Script
# Completely override local dotfiles with remote repository state

set -euo pipefail

# Configuration
DOTFILES_DIR="${DOTFILES_DIR:-$HOME/dotfiles}"
BACKUP_BASE_DIR="$HOME/.mentat/backups"
LOG_FILE="$HOME/.mentat/force-pull.log"
REMOTE_BRANCH="${REMOTE_BRANCH:-main}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Options (can be overridden by command line args)
NO_PROMPT=false
CREATE_BACKUP=true
INSTALL_PACKAGES=false
DRY_RUN=false
ONLY_PATH=""
RESTORE_DIR=""

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

# Ensure this is being run by an interactive user, not automation
ensure_interactive_user() {
    # Skip checks for dry-run (safe to preview)
    if [ "$DRY_RUN" = true ]; then
        return 0
    fi
    
    # Check if running in interactive terminal
    if ! [[ -t 0 && -t 1 ]]; then
        log ERROR "SECURITY: Force-pull can ONLY be run interactively by a human user"
        log ERROR "This command cannot be run by scripts, automation, or the syncer agent"
        exit 1
    fi
    
    # Check parent process name to detect automation
    local parent_cmd=$(ps -o comm= $PPID 2>/dev/null | tr -d ' ')
    if echo "$parent_cmd" | grep -qE "(cron|systemd|launchd|sync-orchestrator|syncer|agent)"; then
        log ERROR "SECURITY: Force-pull detected automation parent process: $parent_cmd"
        log ERROR "This command must be run directly by a user, not by automation"
        exit 1
    fi
    
    # Check for automation environment variables
    if [[ -n "${CI:-}" || -n "${GITHUB_ACTIONS:-}" || -n "${JENKINS_HOME:-}" || -n "${AUTOMATION:-}" ]]; then
        log ERROR "SECURITY: Force-pull detected automation environment"
        log ERROR "This command cannot be run in CI/CD or automated environments"
        exit 1
    fi
    
    # Check if being piped or redirected (additional safety)
    if [[ ! -t 0 ]] || [[ ! -t 1 ]]; then
        log ERROR "SECURITY: Input/output is redirected or piped"
        log ERROR "Force-pull must be run directly in a terminal"
        exit 1
    fi
    
    # Check SSH session to ensure it's an interactive session
    if [[ -n "${SSH_CLIENT:-}" || -n "${SSH_TTY:-}" ]]; then
        # SSH is okay only if it's an interactive session
        if [[ ! -t 0 ]]; then
            log ERROR "SECURITY: Non-interactive SSH session detected"
            log ERROR "Force-pull requires an interactive terminal session"
            exit 1
        fi
    fi
    
    log INFO "Interactive user verification passed"
}

# Human verification challenge (even with --no-prompt)
require_human_verification() {
    # Skip for dry-run
    if [ "$DRY_RUN" = true ]; then
        return 0
    fi
    
    # For --no-prompt, still require a simple human verification
    if [ "$NO_PROMPT" = true ]; then
        log WARNING "Force-pull with --no-prompt still requires human verification"
        
        # Generate a simple math problem
        local num1=$((RANDOM % 10 + 1))
        local num2=$((RANDOM % 10 + 1))
        local answer=$((num1 + num2))
        
        echo ""
        echo "HUMAN VERIFICATION REQUIRED"
        echo "This ensures force-pull is not run by automation"
        echo ""
        printf "Please solve: %d + %d = " "$num1" "$num2"
        
        # Read with timeout to prevent hanging automation
        local user_answer
        if read -r -t 30 user_answer; then
            if [ "$user_answer" = "$answer" ]; then
                log SUCCESS "Human verification passed"
                return 0
            else
                log ERROR "Incorrect answer. Force-pull cancelled."
                exit 1
            fi
        else
            log ERROR "Verification timeout. Force-pull cancelled."
            exit 1
        fi
    fi
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --no-prompt)
                NO_PROMPT=true
                shift
                ;;
            --backup)
                CREATE_BACKUP=true
                shift
                ;;
            --no-backup)
                CREATE_BACKUP=false
                shift
                ;;
            --install-packages)
                INSTALL_PACKAGES=true
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --only)
                ONLY_PATH="$2"
                shift 2
                ;;
            --restore)
                RESTORE_DIR="$2"
                shift 2
                ;;
            *)
                log ERROR "Unknown option: $1"
                exit 1
                ;;
        esac
    done
}

# Pre-pull validation
validate_environment() {
    log INFO "Validating environment..."
    
    # Check if dotfiles directory exists
    if [ ! -d "$DOTFILES_DIR" ]; then
        log ERROR "Dotfiles directory not found: $DOTFILES_DIR"
        log ERROR "Run /mentat:setup first to initialize dotfiles"
        exit 1
    fi
    
    cd "$DOTFILES_DIR"
    
    # Check if it's a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log ERROR "Not a git repository: $DOTFILES_DIR"
        exit 1
    fi
    
    # Check network connectivity
    if ! git ls-remote origin > /dev/null 2>&1; then
        log ERROR "Cannot reach remote repository. Check your internet connection."
        exit 1
    fi
    
    log SUCCESS "Environment validation passed"
}

# Confirmation prompt
confirm_action() {
    if [ "$NO_PROMPT" = true ] || [ "$DRY_RUN" = true ]; then
        return 0
    fi
    
    echo -e "${YELLOW}════════════════════════════════════════${NC}"
    echo -e "${YELLOW}⚠️  WARNING: DESTRUCTIVE OPERATION ⚠️${NC}"
    echo -e "${YELLOW}════════════════════════════════════════${NC}"
    echo ""
    echo "This will:"
    echo "  • DELETE all local changes in $DOTFILES_DIR"
    echo "  • OVERRIDE all symlinked dotfiles"
    echo "  • REMOVE any local-only configurations"
    echo ""
    echo "Your local dotfiles will be replaced with the remote versions."
    echo ""
    
    if [ "$CREATE_BACKUP" = true ]; then
        echo "A backup will be created before proceeding."
    else
        echo -e "${RED}NO BACKUP will be created (--no-backup flag set)${NC}"
    fi
    
    echo ""
    read -p "Are you SURE? Type 'yes' to continue: " confirmation
    
    if [ "$confirmation" != "yes" ]; then
        log INFO "Force pull cancelled by user"
        exit 0
    fi
}

# Create backup of current state
create_backup() {
    if [ "$CREATE_BACKUP" = false ]; then
        log WARNING "Skipping backup (--no-backup flag set)"
        return 0
    fi
    
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local backup_dir="$BACKUP_BASE_DIR/$timestamp"
    
    log INFO "Creating backup at $backup_dir..."
    mkdir -p "$backup_dir"
    
    # Backup current dotfiles repository
    if [ "$DRY_RUN" = false ]; then
        cp -Ra "$DOTFILES_DIR" "$backup_dir/dotfiles-backup" 2>/dev/null || true
    fi
    
    # Backup current symlinks and their targets
    local symlink_backup_dir="$backup_dir/symlinks"
    mkdir -p "$symlink_backup_dir"
    
    while IFS= read -r link; do
        if [ -L "$link" ]; then
            local target=$(readlink "$link")
            local rel_path="${link#$HOME/}"
            local backup_info_dir="$symlink_backup_dir/$(dirname "$rel_path")"
            
            mkdir -p "$backup_info_dir"
            echo "$target" > "$backup_info_dir/$(basename "$rel_path").target"
            
            # Copy the actual file if it exists and isn't a directory
            if [ -f "$link" ] && [ "$DRY_RUN" = false ]; then
                cp -a "$link" "$backup_info_dir/$(basename "$rel_path").backup"
            fi
        fi
    done < <(find "$HOME" -maxdepth 3 -type l -lname "*dotfiles*" 2>/dev/null)
    
    # Store backup location for potential restore
    echo "$backup_dir" > "$BACKUP_BASE_DIR/latest"
    
    log SUCCESS "Backup created at $backup_dir"
    echo "$backup_dir"  # Return backup directory path
}

# Force pull from remote
force_pull_repository() {
    log INFO "Force pulling from remote repository..."
    
    cd "$DOTFILES_DIR"
    
    # Fetch all updates from remote
    log INFO "Fetching latest from remote..."
    if [ "$DRY_RUN" = false ]; then
        git fetch origin --all
    else
        log INFO "[DRY RUN] Would fetch from origin"
    fi
    
    # Show what will be changed
    if [ "$DRY_RUN" = true ]; then
        log INFO "[DRY RUN] Changes that would be applied:"
        git diff HEAD..origin/$REMOTE_BRANCH --stat
        return 0
    fi
    
    # Stash any local changes (for record keeping)
    local stash_msg="force-pull-backup-$(date +%s)"
    git stash push -m "$stash_msg" --include-untracked || true
    
    # Reset to remote state
    log INFO "Resetting to origin/$REMOTE_BRANCH..."
    git reset --hard origin/$REMOTE_BRANCH
    
    # Clean untracked files
    log INFO "Cleaning untracked files..."
    git clean -fdx
    
    log SUCCESS "Repository reset to match remote"
}

# Remove old symlinks
remove_old_symlinks() {
    log INFO "Removing old symlinks..."
    
    local removed_count=0
    
    while IFS= read -r link; do
        if [ -L "$link" ]; then
            if [ "$DRY_RUN" = false ]; then
                rm "$link"
                removed_count=$((removed_count + 1))
            else
                log INFO "[DRY RUN] Would remove: $link"
                removed_count=$((removed_count + 1))
            fi
        fi
    done < <(find "$HOME" -maxdepth 3 -type l -lname "*dotfiles*" 2>/dev/null)
    
    log SUCCESS "Removed $removed_count old symlinks"
}

# Create fresh symlinks from remote state
create_fresh_symlinks() {
    log INFO "Creating fresh symlinks from remote state..."
    
    local created_count=0
    
    # Symlink files from home/
    if [ -d "$DOTFILES_DIR/home" ]; then
        for file in "$DOTFILES_DIR/home"/.*; do
            [ -f "$file" ] || continue
            local basename=$(basename "$file")
            
            # Skip . and ..
            [[ "$basename" == "." || "$basename" == ".." ]] && continue
            
            # Skip if --only is set and doesn't match
            if [ -n "$ONLY_PATH" ] && [[ ! "$file" == *"$ONLY_PATH"* ]]; then
                continue
            fi
            
            local target_path="$HOME/$basename"
            
            # Backup existing non-symlink file
            if [ -e "$target_path" ] && [ ! -L "$target_path" ]; then
                if [ "$DRY_RUN" = false ]; then
                    mv "$target_path" "$target_path.pre-force-pull"
                    log WARNING "Backed up existing $target_path"
                else
                    log INFO "[DRY RUN] Would backup: $target_path"
                fi
            fi
            
            # Create symlink
            if [ "$DRY_RUN" = false ]; then
                ln -sf "$file" "$target_path"
                created_count=$((created_count + 1))
                log SUCCESS "Linked $basename"
            else
                log INFO "[DRY RUN] Would link: $basename"
                created_count=$((created_count + 1))
            fi
        done
    fi
    
    # Symlink Cursor settings (macOS specific)
    if [ -d "$DOTFILES_DIR/special/cursor" ] && [ "$(uname)" = "Darwin" ]; then
        local cursor_dir="$HOME/Library/Application Support/Cursor/User"
        mkdir -p "$cursor_dir"
        
        for file in "$DOTFILES_DIR/special/cursor"/*; do
            [ -f "$file" ] || continue
            local basename=$(basename "$file")
            
            if [ -n "$ONLY_PATH" ] && [[ ! "$file" == *"$ONLY_PATH"* ]]; then
                continue
            fi
            
            local target_path="$cursor_dir/$basename"
            
            if [ -f "$target_path" ] && [ ! -L "$target_path" ]; then
                if [ "$DRY_RUN" = false ]; then
                    mv "$target_path" "$target_path.pre-force-pull"
                else
                    log INFO "[DRY RUN] Would backup Cursor: $basename"
                fi
            fi
            
            if [ "$DRY_RUN" = false ]; then
                ln -sf "$file" "$target_path"
                created_count=$((created_count + 1))
                log SUCCESS "Linked Cursor $basename"
            else
                log INFO "[DRY RUN] Would link Cursor: $basename"
                created_count=$((created_count + 1))
            fi
        done
    fi
    
    # Symlink .config directory contents
    if [ -d "$DOTFILES_DIR/config" ]; then
        mkdir -p "$HOME/.config"
        
        for dir in "$DOTFILES_DIR/config"/*; do
            [ -d "$dir" ] || continue
            local basename=$(basename "$dir")
            
            if [ -n "$ONLY_PATH" ] && [[ ! "$dir" == *"$ONLY_PATH"* ]]; then
                continue
            fi
            
            local target_path="$HOME/.config/$basename"
            
            if [ -d "$target_path" ] && [ ! -L "$target_path" ]; then
                if [ "$DRY_RUN" = false ]; then
                    mv "$target_path" "$target_path.pre-force-pull"
                else
                    log INFO "[DRY RUN] Would backup .config: $basename"
                fi
            fi
            
            if [ "$DRY_RUN" = false ]; then
                ln -sf "$dir" "$target_path"
                created_count=$((created_count + 1))
                log SUCCESS "Linked .config/$basename"
            else
                log INFO "[DRY RUN] Would link .config: $basename"
                created_count=$((created_count + 1))
            fi
        done
    fi
    
    log SUCCESS "Created $created_count fresh symlinks"
}

# Install packages from remote lists
install_packages() {
    if [ "$INSTALL_PACKAGES" = false ] || [ "$DRY_RUN" = true ]; then
        return 0
    fi
    
    log INFO "Installing packages from remote lists..."
    
    # Homebrew packages
    if [ -f "$DOTFILES_DIR/packages/Brewfile" ] && command -v brew >/dev/null 2>&1; then
        log INFO "Installing Homebrew packages..."
        brew bundle --file="$DOTFILES_DIR/packages/Brewfile"
    fi
    
    # NPM global packages
    if [ -f "$DOTFILES_DIR/packages/npm-global.txt" ] && command -v npm >/dev/null 2>&1; then
        log INFO "Installing NPM packages..."
        cat "$DOTFILES_DIR/packages/npm-global.txt" | xargs npm install -g
    fi
    
    # Cursor extensions
    if [ -f "$DOTFILES_DIR/packages/cursor-extensions.txt" ] && command -v cursor >/dev/null 2>&1; then
        log INFO "Installing Cursor extensions..."
        cat "$DOTFILES_DIR/packages/cursor-extensions.txt" | xargs -L 1 cursor --install-extension
    fi
    
    log SUCCESS "Package installation complete"
}

# Restore from backup
restore_from_backup() {
    local backup_dir="$1"
    
    if [ ! -d "$backup_dir" ]; then
        log ERROR "Backup directory not found: $backup_dir"
        exit 1
    fi
    
    log INFO "Restoring from backup: $backup_dir"
    
    # Restore dotfiles repository
    if [ -d "$backup_dir/dotfiles-backup" ]; then
        rm -rf "$DOTFILES_DIR"
        cp -Ra "$backup_dir/dotfiles-backup" "$DOTFILES_DIR"
        log SUCCESS "Restored dotfiles repository"
    fi
    
    # Restore symlinks
    if [ -d "$backup_dir/symlinks" ]; then
        find "$backup_dir/symlinks" -name "*.target" | while read -r target_file; do
            local rel_path="${target_file#$backup_dir/symlinks/}"
            rel_path="${rel_path%.target}"
            local link_path="$HOME/$rel_path"
            local target=$(cat "$target_file")
            
            mkdir -p "$(dirname "$link_path")"
            ln -sf "$target" "$link_path"
        done
        log SUCCESS "Restored symlinks"
    fi
    
    log SUCCESS "Restore complete"
}

# Post-pull actions
post_pull_actions() {
    if [ "$DRY_RUN" = true ]; then
        return 0
    fi
    
    # Run post-pull hooks if they exist
    if [ -f "$DOTFILES_DIR/hooks/post-pull.sh" ]; then
        log INFO "Running post-pull hooks..."
        bash "$DOTFILES_DIR/hooks/post-pull.sh"
    fi
    
    # Update machine registry
    log INFO "Updating machine registry..."
    cd "$DOTFILES_DIR"
    echo "$(hostname):force-pull:$(date +%s)" >> ".sync-log"
    git add ".sync-log" 2>/dev/null || true
    git commit -m "Force pull on $(hostname)" --quiet 2>/dev/null || true
    git push origin $REMOTE_BRANCH --quiet 2>/dev/null || true
    
    log SUCCESS "Post-pull actions complete"
}

# Print summary
print_summary() {
    local backup_dir="$1"
    local current_commit=$(cd "$DOTFILES_DIR" && git rev-parse --short HEAD)
    
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║       FORCE PULL COMPLETE              ║${NC}"
    echo -e "${GREEN}╠════════════════════════════════════════╣${NC}"
    
    if [ -n "$backup_dir" ] && [ "$CREATE_BACKUP" = true ]; then
        echo -e "${GREEN}║${NC} 📦 Backup:     ${backup_dir#$HOME/}"
    fi
    
    echo -e "${GREEN}║${NC} 🔄 Reset to:   origin/$REMOTE_BRANCH @ $current_commit"
    echo -e "${GREEN}║${NC} 🔗 Status:     Symlinks recreated"
    
    if [ "$INSTALL_PACKAGES" = true ]; then
        echo -e "${GREEN}║${NC} 📦 Packages:   Installed"
    else
        echo -e "${GREEN}║${NC} 📦 Packages:   Not installed"
    fi
    
    echo -e "${GREEN}║${NC}"
    echo -e "${GREEN}║${NC} Status: ✅ Local matches remote"
    echo -e "${GREEN}║${NC}"
    
    if [ "$CREATE_BACKUP" = true ]; then
        echo -e "${GREEN}║${NC} ⚠️  Previous state backed up"
        echo -e "${GREEN}║${NC} Run with --restore to undo"
    fi
    
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
}

# Main function
main() {
    # Ensure log directory exists
    mkdir -p "$(dirname "$LOG_FILE")"
    mkdir -p "$BACKUP_BASE_DIR"
    
    log INFO "Starting force pull operation"
    
    # Parse command line arguments
    parse_args "$@"
    
    # SECURITY: Ensure this is being run by an interactive user
    ensure_interactive_user
    
    # Handle restore operation
    if [ -n "$RESTORE_DIR" ]; then
        restore_from_backup "$RESTORE_DIR"
        exit 0
    fi
    
    # Validate environment
    validate_environment
    
    # SECURITY: Require human verification for --no-prompt
    require_human_verification
    
    # Get confirmation
    confirm_action
    
    # Create backup
    local backup_dir=""
    if [ "$CREATE_BACKUP" = true ]; then
        backup_dir=$(create_backup)
    fi
    
    # Perform force pull
    force_pull_repository
    
    if [ "$DRY_RUN" = false ]; then
        # Remove old symlinks
        remove_old_symlinks
        
        # Create fresh symlinks
        create_fresh_symlinks
        
        # Install packages if requested
        install_packages
        
        # Post-pull actions
        post_pull_actions
    fi
    
    # Print summary
    if [ "$DRY_RUN" = false ]; then
        print_summary "$backup_dir"
    else
        log INFO "[DRY RUN] No changes were made"
    fi
    
    log SUCCESS "Force pull operation completed"
}

# Run if executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi