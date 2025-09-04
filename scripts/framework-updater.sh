#!/bin/bash
# Mentat Framework Updater
# Updates the Mentat framework to the latest version from GitHub

set -euo pipefail

# Configuration
REPO_URL="https://github.com/a-alphayed/Mentat"
RAW_URL="https://raw.githubusercontent.com/a-alphayed/Mentat"
BRANCH="${MENTAT_BRANCH:-main}"
VERSION_FILE="$HOME/.claude/.mentat-version"
CONFIG_FILE="$HOME/.mentat/config.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    
    case "$level" in
        ERROR)   echo -e "${RED}❌ $message${NC}" >&2 ;;
        SUCCESS) echo -e "${GREEN}✅ $message${NC}" ;;
        WARNING) echo -e "${YELLOW}⚠️  $message${NC}" ;;
        INFO)    echo -e "${BLUE}ℹ️  $message${NC}" ;;
        *)       echo "$message" ;;
    esac
}

# Check prerequisites
check_prerequisites() {
    log INFO "Checking prerequisites..."
    
    # Check for pipx
    if ! command -v pipx &> /dev/null; then
        log ERROR "pipx is not installed"
        log INFO "Install with: python3 -m pip install --user pipx"
        return 1
    fi
    
    # Check if Mentat is installed via pipx
    if ! pipx list 2>/dev/null | grep -q "package Mentat"; then
        log ERROR "Mentat is not installed via pipx"
        log INFO "Install with: pipx install git+${REPO_URL}.git"
        return 1
    fi
    
    # Check for internet connection
    if ! curl -s --head https://github.com > /dev/null; then
        log ERROR "No internet connection"
        return 1
    fi
    
    log SUCCESS "Prerequisites satisfied"
    return 0
}

# Get current version
get_current_version() {
    if [ -f "$VERSION_FILE" ]; then
        cat "$VERSION_FILE"
    else
        echo "unknown"
    fi
}

# Get latest version from GitHub
get_latest_version() {
    local url="${RAW_URL}/${BRANCH}/VERSION"
    curl -s "$url" 2>/dev/null || echo "unknown"
}

# Compare versions
version_compare() {
    local current="$1"
    local latest="$2"
    
    # Handle unknown versions
    if [ "$current" = "unknown" ] || [ "$latest" = "unknown" ]; then
        return 1  # Assume update needed if version unknown
    fi
    
    # Simple string comparison for now
    # TODO: Implement semantic versioning comparison
    if [ "$current" = "$latest" ]; then
        return 0  # Same version
    else
        return 1  # Different version
    fi
}

# Fetch changelog
show_changelog() {
    local current="$1"
    local latest="$2"
    
    log INFO "What's new in version $latest:"
    echo ""
    
    # Try to fetch changelog
    local changelog_url="${RAW_URL}/${BRANCH}/CHANGELOG.md"
    local changelog=$(curl -s "$changelog_url" 2>/dev/null || echo "")
    
    if [ -n "$changelog" ]; then
        # Extract relevant section (simple approach)
        echo "$changelog" | head -20
    else
        echo "  • Check ${REPO_URL}/releases for details"
    fi
    echo ""
}

# Backup configuration
backup_config() {
    local backup_dir="$HOME/.mentat-backup-$(date +%Y%m%d-%H%M%S)"
    
    log INFO "Backing up configuration..."
    
    mkdir -p "$backup_dir"
    
    # Backup config file
    if [ -f "$CONFIG_FILE" ]; then
        cp -a "$CONFIG_FILE" "$backup_dir/"
        log SUCCESS "Configuration backed up to: $backup_dir"
    fi
    
    # Backup version file
    if [ -f "$VERSION_FILE" ]; then
        cp -a "$VERSION_FILE" "$backup_dir/"
    fi
    
    # Save backup location for restore
    echo "$backup_dir" > /tmp/mentat_backup_dir
    
    return 0
}

# Restore configuration
restore_config() {
    local backup_dir=$(cat /tmp/mentat_backup_dir 2>/dev/null || echo "")
    
    if [ -z "$backup_dir" ] || [ ! -d "$backup_dir" ]; then
        log WARNING "No backup found to restore"
        return 1
    fi
    
    log INFO "Restoring configuration..."
    
    # Restore config file
    if [ -f "$backup_dir/config.json" ]; then
        mkdir -p "$(dirname "$CONFIG_FILE")"
        cp "$backup_dir/config.json" "$CONFIG_FILE"
        log SUCCESS "Configuration restored"
    fi
    
    return 0
}

# Update Mentat via pipx
update_mentat() {
    local branch="${1:-main}"
    
    log INFO "Updating Mentat framework..."
    
    # Use pipx reinstall to get latest from GitHub
    if pipx reinstall Mentat --verbose; then
        log SUCCESS "Mentat framework updated successfully"
        return 0
    else
        log ERROR "Failed to update Mentat"
        return 1
    fi
}

# Update version file
update_version_file() {
    local version="$1"
    
    mkdir -p "$(dirname "$VERSION_FILE")"
    echo "$version" > "$VERSION_FILE"
    log SUCCESS "Version file updated: $version"
}

# Verify installation
verify_installation() {
    log INFO "Verifying installation..."
    
    local all_good=true
    
    # Check key scripts
    if [ ! -f "$HOME/.claude/scripts/sync-orchestrator.sh" ]; then
        log WARNING "Missing sync-orchestrator.sh"
        all_good=false
    fi
    
    # Check commands directory
    if [ ! -d "$HOME/.claude/commands/mentat" ]; then
        log WARNING "Missing mentat commands directory"
        all_good=false
    fi
    
    # Check agent
    if [ ! -f "$HOME/.claude/agents/agent-syncer.md" ]; then
        log WARNING "Missing agent-syncer.md"
        all_good=false
    fi
    
    if $all_good; then
        log SUCCESS "All components verified"
        return 0
    else
        log WARNING "Some components may be missing"
        log INFO "Run 'mentat install' to repair installation"
        return 1
    fi
}

# Main update process
main() {
    local force="${1:-false}"
    
    echo ""
    echo "╔════════════════════════════════════════╗"
    echo "║        MENTAT FRAMEWORK UPDATER        ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
    
    # Check prerequisites
    if ! check_prerequisites; then
        log ERROR "Prerequisites check failed"
        exit 1
    fi
    
    # Get versions
    local current_version=$(get_current_version)
    local latest_version=$(get_latest_version)
    
    log INFO "Current version: $current_version"
    log INFO "Latest version:  $latest_version"
    
    # Check if update needed
    if version_compare "$current_version" "$latest_version" && [ "$force" != "force" ]; then
        log SUCCESS "Already on the latest version!"
        exit 0
    fi
    
    # Show what's new
    if [ "$current_version" != "$latest_version" ]; then
        show_changelog "$current_version" "$latest_version"
    fi
    
    # Confirm update
    if [ "$force" != "force" ]; then
        echo -n "Update Mentat framework? (y/n): "
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            log INFO "Update cancelled"
            exit 0
        fi
    fi
    
    # Perform update
    echo ""
    backup_config
    
    if update_mentat "$BRANCH"; then
        restore_config
        update_version_file "$latest_version"
        verify_installation || true
        
        echo ""
        echo "╔════════════════════════════════════════╗"
        echo "║         UPDATE COMPLETE! 🎉            ║"
        echo "╠════════════════════════════════════════╣"
        echo "║ Version: $latest_version"
        echo "║                                        ║"
        echo "║ Next steps:                           ║"
        echo "║ • Run /mentat:status to verify        ║"
        echo "║ • Check new features with /help       ║"
        echo "╚════════════════════════════════════════╝"
        echo ""
    else
        log ERROR "Update failed!"
        log INFO "Attempting to restore configuration..."
        restore_config
        exit 1
    fi
}

# Handle script arguments
case "${1:-}" in
    --force)
        main "force"
        ;;
    --check)
        # Just check for updates
        current=$(get_current_version)
        latest=$(get_latest_version)
        if version_compare "$current" "$latest"; then
            log SUCCESS "No updates available (version: $current)"
        else
            log INFO "Update available: $current → $latest"
        fi
        ;;
    --version)
        get_current_version
        ;;
    *)
        main
        ;;
esac