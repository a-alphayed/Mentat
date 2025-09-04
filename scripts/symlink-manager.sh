#!/bin/bash
# Mentat Symlink Manager
# Handles creation and verification of dotfile symlinks

set -euo pipefail

# Configuration
DOTFILES_DIR="${DOTFILES_DIR:-$HOME/dotfiles}"
BACKUP_DIR="$HOME/.dotfiles-backup/$(date +%Y%m%d-%H%M%S)"

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

# Function to create symlink
create_symlink() {
    local source="$1"
    local target="$2"
    
    # Create parent directory if needed
    local target_dir=$(dirname "$target")
    if [ ! -d "$target_dir" ]; then
        mkdir -p "$target_dir"
        log INFO "Created directory: $target_dir"
    fi
    
    # Check if target exists
    if [ -e "$target" ] || [ -L "$target" ]; then
        if [ -L "$target" ] && [ "$(readlink "$target")" = "$source" ]; then
            log SUCCESS "$target already linked correctly"
            return 0
        fi
        
        # Backup existing file/symlink
        if [ ! -d "$BACKUP_DIR" ]; then
            mkdir -p "$BACKUP_DIR"
        fi
        
        local backup_path="$BACKUP_DIR/$(basename "$target")"
        cp -a "$target" "$backup_path" 2>/dev/null || true
        rm -rf "$target"
        log WARNING "Backed up existing $target"
    fi
    
    # Create symlink
    ln -s "$source" "$target"
    log SUCCESS "Linked $target → $source"
}

# Setup all dotfile symlinks
setup_symlinks() {
    log INFO "Setting up dotfile symlinks..."
    
    if [ ! -d "$DOTFILES_DIR" ]; then
        log ERROR "Dotfiles directory not found: $DOTFILES_DIR"
        return 1
    fi
    
    # Process files in home directory
    if [ -d "$DOTFILES_DIR/home" ]; then
        log INFO "Processing home directory files..."
        
        # Find all files in home directory (not directories)
        find "$DOTFILES_DIR/home" -type f | while read -r file; do
            # Get relative path from home directory
            local relative_path="${file#$DOTFILES_DIR/home/}"
            local target="$HOME/$relative_path"
            
            # Skip if in .dotfiles-ignore
            if [ -f "$DOTFILES_DIR/.dotfiles-ignore" ]; then
                if grep -q "$(basename "$file")" "$DOTFILES_DIR/.dotfiles-ignore" 2>/dev/null; then
                    log WARNING "Skipping $target (in .dotfiles-ignore)"
                    continue
                fi
            fi
            
            create_symlink "$file" "$target"
        done
    fi
    
    log SUCCESS "Symlink setup complete!"
    [ -d "$BACKUP_DIR" ] && log INFO "Backups saved to: $BACKUP_DIR"
}

# Verify and repair symlinks
verify_symlinks() {
    log INFO "Verifying symlinks..."
    
    local broken_count=0
    local repaired_count=0
    
    # Find all symlinks pointing to dotfiles
    while IFS= read -r link; do
        if [ ! -e "$link" ]; then
            log WARNING "Broken symlink: $link"
            
            # Try to repair
            local target=$(readlink "$link")
            if [ -f "$target" ]; then
                rm "$link"
                ln -s "$target" "$link"
                if [ -e "$link" ]; then
                    log SUCCESS "Repaired: $link"
                    ((repaired_count++))
                else
                    ((broken_count++))
                fi
            else
                ((broken_count++))
            fi
        fi
    done < <(find ~ -maxdepth 4 -type l -lname "*dotfiles*" 2>/dev/null)
    
    if [ $broken_count -eq 0 ]; then
        log SUCCESS "All symlinks valid"
    else
        log WARNING "$broken_count symlinks need manual repair"
    fi
    
    [ $repaired_count -gt 0 ] && log SUCCESS "Repaired $repaired_count symlinks"
}

# Main execution
main() {
    local action="${1:-setup}"
    
    case "$action" in
        setup)
            setup_symlinks
            ;;
        verify)
            verify_symlinks
            ;;
        repair)
            verify_symlinks
            setup_symlinks
            ;;
        *)
            log ERROR "Unknown action: $action"
            echo "Usage: $0 [setup|verify|repair]"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"