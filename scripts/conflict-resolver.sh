#!/bin/bash
# Mentat Conflict Resolver
# Intelligent conflict resolution for dotfiles synchronization

set -euo pipefail

# Configuration
DOTFILES_DIR="${DOTFILES_DIR:-$HOME/dotfiles}"
MENTAT_DIR="$HOME/.mentat"
CONFLICT_LOG="$MENTAT_DIR/conflicts.log"
BACKUP_DIR="$MENTAT_DIR/conflict-backups"

# Conflict resolution strategies
declare -A RESOLUTION_RULES=(
    [".bashrc"]="merge_append"
    [".zshrc"]="merge_append"
    [".gitconfig"]="merge_sections"
    [".vimrc"]="merge_append"
    ["*.conf"]="prefer_remote"
    ["*.json"]="prefer_local"
    ["*"]="prompt_user"
)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$CONFLICT_LOG"
    echo -e "$*"
}

# Detect conflicts
detect_conflicts() {
    cd "$DOTFILES_DIR"
    
    local conflicts=()
    
    # Check for merge conflicts
    if git ls-files -u | grep -q .; then
        while IFS= read -r file; do
            conflicts+=("$file")
        done < <(git diff --name-only --diff-filter=U)
    fi
    
    # Check for rebase conflicts
    if [ -d ".git/rebase-merge" ] || [ -d ".git/rebase-apply" ]; then
        while IFS= read -r file; do
            if grep -q "<<<<<<< " "$file" 2>/dev/null; then
                conflicts+=("$file")
            fi
        done < <(git diff --name-only)
    fi
    
    printf '%s\n' "${conflicts[@]}"
}

# Get resolution strategy for file
get_strategy() {
    local file="$1"
    local basename=$(basename "$file")
    
    # Check specific rules first
    for pattern in "${!RESOLUTION_RULES[@]}"; do
        if [[ "$basename" == $pattern ]]; then
            echo "${RESOLUTION_RULES[$pattern]}"
            return
        fi
    done
    
    # Default strategy
    echo "${RESOLUTION_RULES[*]}"
}

# Backup conflicted file
backup_file() {
    local file="$1"
    local timestamp=$(date +%Y%m%d-%H%M%S)
    local backup_path="$BACKUP_DIR/$timestamp"
    
    mkdir -p "$backup_path"
    
    # Save all versions
    git show :1:"$file" > "$backup_path/${file}.base" 2>/dev/null || true
    git show :2:"$file" > "$backup_path/${file}.ours" 2>/dev/null || true
    git show :3:"$file" > "$backup_path/${file}.theirs" 2>/dev/null || true
    cp "$file" "$backup_path/${file}.conflict" 2>/dev/null || true
    
    log "Backed up $file to $backup_path"
}

# Merge by appending unique lines
merge_append() {
    local file="$1"
    local merged="$file.merged"
    
    log "Merging $file using append strategy..."
    
    # Get all three versions
    local base=$(mktemp)
    local ours=$(mktemp)
    local theirs=$(mktemp)
    
    git show :1:"$file" > "$base" 2>/dev/null || touch "$base"
    git show :2:"$file" > "$ours" 2>/dev/null || cp "$file" "$ours"
    git show :3:"$file" > "$theirs" 2>/dev/null || true
    
    # Start with base
    cp "$base" "$merged"
    
    # Add unique lines from ours
    while IFS= read -r line; do
        if ! grep -Fxq "$line" "$merged"; then
            echo "$line" >> "$merged"
        fi
    done < <(comm -13 <(sort "$base") <(sort "$ours"))
    
    # Add unique lines from theirs
    while IFS= read -r line; do
        if ! grep -Fxq "$line" "$merged"; then
            echo "$line" >> "$merged"
        fi
    done < <(comm -13 <(sort "$base") <(sort "$theirs"))
    
    # Replace original
    mv "$merged" "$file"
    
    # Cleanup
    rm -f "$base" "$ours" "$theirs"
    
    log "✅ Merged $file successfully"
}

# Merge configuration sections
merge_sections() {
    local file="$1"
    local merged="$file.merged"
    
    log "Merging $file using section strategy..."
    
    # This is a simplified version - in production, use proper INI/TOML parser
    local ours=$(mktemp)
    local theirs=$(mktemp)
    
    git show :2:"$file" > "$ours" 2>/dev/null || cp "$file" "$ours"
    git show :3:"$file" > "$theirs" 2>/dev/null || true
    
    # For .gitconfig, merge sections
    if [[ "$file" == *.gitconfig ]] || [[ "$file" == *gitconfig ]]; then
        # Start with ours
        cp "$ours" "$merged"
        
        # Extract sections from theirs and append if not present
        local current_section=""
        while IFS= read -r line; do
            if [[ "$line" =~ ^\[.*\]$ ]]; then
                current_section="$line"
                if ! grep -Fq "$current_section" "$merged"; then
                    echo "" >> "$merged"
                    echo "$current_section" >> "$merged"
                fi
            elif [ -n "$current_section" ] && [ -n "$line" ]; then
                # Add line if section exists and line doesn't
                if grep -Fq "$current_section" "$merged" && ! grep -Fq "$line" "$merged"; then
                    echo "$line" >> "$merged"
                fi
            fi
        done < "$theirs"
    else
        # Generic section merge
        merge_append "$file"
        return
    fi
    
    mv "$merged" "$file"
    rm -f "$ours" "$theirs"
    
    log "✅ Merged sections in $file"
}

# Prefer remote version
prefer_remote() {
    local file="$1"
    
    log "Taking remote version of $file..."
    
    git checkout --theirs "$file"
    git add "$file"
    
    log "✅ Accepted remote version of $file"
}

# Prefer local version
prefer_local() {
    local file="$1"
    
    log "Keeping local version of $file..."
    
    git checkout --ours "$file"
    git add "$file"
    
    log "✅ Kept local version of $file"
}

# Interactive resolution
prompt_user() {
    local file="$1"
    
    echo -e "${YELLOW}Conflict in: $file${NC}"
    echo "Options:"
    echo "  1) Keep local version (ours)"
    echo "  2) Accept remote version (theirs)"
    echo "  3) View diff"
    echo "  4) Edit manually"
    echo "  5) Try automatic merge"
    echo "  6) Skip this file"
    
    while true; do
        read -p "Choose [1-6]: " choice
        
        case "$choice" in
            1)
                prefer_local "$file"
                break
                ;;
            2)
                prefer_remote "$file"
                break
                ;;
            3)
                echo -e "${BLUE}=== Local vs Remote ===${NC}"
                git diff --color :2:"$file" :3:"$file" || true
                ;;
            4)
                ${EDITOR:-vi} "$file"
                echo "File edited. Mark as resolved? [y/n]"
                read -r mark
                if [[ "$mark" == "y" ]]; then
                    git add "$file"
                    log "✅ Manually resolved $file"
                    break
                fi
                ;;
            5)
                merge_append "$file"
                git add "$file"
                break
                ;;
            6)
                log "⏭️  Skipped $file"
                break
                ;;
            *)
                echo "Invalid choice"
                ;;
        esac
    done
}

# Resolve single conflict
resolve_conflict() {
    local file="$1"
    local strategy="${2:-auto}"
    
    log "Resolving conflict in $file (strategy: $strategy)"
    
    # Backup first
    backup_file "$file"
    
    # Apply resolution strategy
    if [ "$strategy" = "auto" ]; then
        strategy=$(get_strategy "$file")
    fi
    
    case "$strategy" in
        merge_append)
            merge_append "$file"
            ;;
        merge_sections)
            merge_sections "$file"
            ;;
        prefer_remote)
            prefer_remote "$file"
            ;;
        prefer_local)
            prefer_local "$file"
            ;;
        prompt_user|*)
            prompt_user "$file"
            ;;
    esac
    
    # Mark as resolved
    git add "$file"
}

# Resolve all conflicts
resolve_all() {
    local strategy="${1:-auto}"
    local conflicts=($(detect_conflicts))
    
    if [ ${#conflicts[@]} -eq 0 ]; then
        log "✅ No conflicts detected"
        return 0
    fi
    
    log "Found ${#conflicts[@]} conflicts to resolve"
    
    for file in "${conflicts[@]}"; do
        resolve_conflict "$file" "$strategy"
    done
    
    # Continue rebase/merge if in progress
    if [ -d ".git/rebase-merge" ] || [ -d ".git/rebase-apply" ]; then
        if git rebase --continue 2>/dev/null; then
            log "✅ Rebase continued successfully"
        else
            log "⚠️  Additional conflicts may exist"
        fi
    elif [ -f ".git/MERGE_HEAD" ]; then
        if git commit --no-edit; then
            log "✅ Merge completed successfully"
        else
            log "⚠️  Merge not complete"
        fi
    fi
}

# Analyze conflict patterns
analyze_conflicts() {
    local days="${1:-30}"
    
    echo -e "${BLUE}=== Conflict Analysis (last $days days) ===${NC}"
    
    if [ ! -f "$CONFLICT_LOG" ]; then
        echo "No conflict history available"
        return
    fi
    
    # Count conflicts by file
    echo -e "\n${YELLOW}Most conflicted files:${NC}"
    grep "Resolving conflict in" "$CONFLICT_LOG" | \
        awk '{print $5}' | \
        sort | uniq -c | sort -rn | head -10
    
    # Count by resolution strategy
    echo -e "\n${YELLOW}Resolution strategies used:${NC}"
    grep "strategy:" "$CONFLICT_LOG" | \
        sed 's/.*strategy: //' | sed 's/).*//' | \
        sort | uniq -c | sort -rn
    
    # Time analysis
    echo -e "\n${YELLOW}Conflicts by hour of day:${NC}"
    grep "^\[" "$CONFLICT_LOG" | \
        awk '{print substr($2,1,2)}' | \
        sort | uniq -c | sort -k2
}

# Prevent conflicts
prevent_conflicts() {
    cd "$DOTFILES_DIR"
    
    log "Running conflict prevention..."
    
    # Fetch latest
    git fetch origin --quiet
    
    # Check for potential conflicts
    local ahead=$(git rev-list origin/main..HEAD --count)
    local behind=$(git rev-list HEAD..origin/main --count)
    
    if [ "$ahead" -gt 0 ] && [ "$behind" -gt 0 ]; then
        log "⚠️  Warning: Local and remote have diverged"
        log "  Ahead: $ahead commits, Behind: $behind commits"
        
        # Check which files might conflict
        local local_files=$(git diff --name-only origin/main...HEAD)
        local remote_files=$(git diff --name-only HEAD...origin/main)
        
        local potential_conflicts=$(comm -12 <(echo "$local_files" | sort) <(echo "$remote_files" | sort))
        
        if [ -n "$potential_conflicts" ]; then
            echo -e "${YELLOW}Potential conflicts in:${NC}"
            echo "$potential_conflicts"
            
            echo -e "\n${YELLOW}Recommended action:${NC}"
            echo "Sync now to prevent conflicts: /mentat:sync"
        fi
    else
        log "✅ No conflict risk detected"
    fi
}

# Main execution
main() {
    local command="${1:-help}"
    shift || true
    
    # Ensure directories exist
    mkdir -p "$MENTAT_DIR" "$BACKUP_DIR"
    
    case "$command" in
        resolve)
            resolve_all "$@"
            ;;
        detect)
            detect_conflicts
            ;;
        analyze)
            analyze_conflicts "$@"
            ;;
        prevent)
            prevent_conflicts
            ;;
        clean)
            # Clean old backups
            find "$BACKUP_DIR" -type d -mtime +30 -exec rm -rf {} + 2>/dev/null || true
            log "Cleaned old conflict backups"
            ;;
        *)
            echo "Usage: $0 {resolve|detect|analyze|prevent|clean} [options]"
            echo ""
            echo "Commands:"
            echo "  resolve [strategy]  - Resolve all conflicts"
            echo "  detect             - List conflicted files"
            echo "  analyze [days]     - Analyze conflict patterns"
            echo "  prevent            - Check for potential conflicts"
            echo "  clean              - Remove old backup files"
            echo ""
            echo "Strategies:"
            echo "  auto          - Use automatic rules (default)"
            echo "  local         - Always keep local version"
            echo "  remote        - Always accept remote version"
            echo "  interactive   - Prompt for each file"
            exit 1
            ;;
    esac
}

# Run if executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi