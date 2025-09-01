#!/bin/bash
# Mentat Health Monitor
# Continuous health monitoring for the dotfiles system

set -euo pipefail

# Configuration
DOTFILES_DIR="${DOTFILES_DIR:-$HOME/dotfiles}"
MENTAT_DIR="$HOME/.mentat"
HEALTH_LOG="$MENTAT_DIR/health.log"
HEALTH_STATUS="$MENTAT_DIR/health.status"
ALERT_THRESHOLD=3

# Health metrics
declare -A HEALTH_SCORES=(
    [repository]=100
    [symlinks]=100
    [network]=100
    [disk]=100
    [sync]=100
)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$HEALTH_LOG"
}

# Check repository health
check_repository() {
    local score=100
    local issues=()
    
    if [ ! -d "$DOTFILES_DIR" ]; then
        score=0
        issues+=("Repository not found")
    else
        cd "$DOTFILES_DIR"
        
        # Check if it's a git repo
        if ! git rev-parse --git-dir > /dev/null 2>&1; then
            score=0
            issues+=("Not a git repository")
        else
            # Check for corruption
            if ! git fsck --quiet 2>/dev/null; then
                score=$((score - 30))
                issues+=("Repository needs repair")
            fi
            
            # Check for lock files
            if [ -f ".git/index.lock" ]; then
                score=$((score - 20))
                issues+=("Lock file present")
            fi
            
            # Check for merge conflicts
            if git ls-files -u | grep -q .; then
                score=$((score - 25))
                issues+=("Unresolved conflicts")
            fi
            
            # Check uncommitted changes age
            if [ -n "$(git status --porcelain)" ]; then
                local last_commit=$(git log -1 --format="%at" 2>/dev/null || echo "0")
                local now=$(date +%s)
                local age=$((now - last_commit))
                
                if [ $age -gt 86400 ]; then  # 24 hours
                    score=$((score - 15))
                    issues+=("Uncommitted changes > 24h old")
                fi
            fi
        fi
    fi
    
    HEALTH_SCORES[repository]=$score
    
    if [ ${#issues[@]} -gt 0 ]; then
        log "Repository issues: ${issues[*]}"
    fi
    
    return $([ $score -ge 70 ] && echo 0 || echo 1)
}

# Check symlink health
check_symlinks() {
    local score=100
    local total=0
    local broken=0
    
    while IFS= read -r link; do
        total=$((total + 1))
        if [ ! -e "$link" ]; then
            broken=$((broken + 1))
            log "Broken symlink: $link"
        fi
    done < <(find "$HOME" -maxdepth 3 -type l -lname "*dotfiles*" 2>/dev/null)
    
    if [ $total -gt 0 ]; then
        local broken_percent=$((broken * 100 / total))
        score=$((100 - broken_percent * 2))
        score=$((score < 0 ? 0 : score))
    fi
    
    HEALTH_SCORES[symlinks]=$score
    
    if [ $broken -gt 0 ]; then
        log "Symlinks: $broken of $total broken"
    fi
    
    return $([ $score -ge 70 ] && echo 0 || echo 1)
}

# Check network connectivity
check_network() {
    local score=100
    local issues=()
    
    # Check internet connectivity
    if ! ping -c 1 -W 2 8.8.8.8 > /dev/null 2>&1; then
        score=$((score - 50))
        issues+=("No internet connection")
    fi
    
    # Check GitHub connectivity
    if ! ping -c 1 -W 2 github.com > /dev/null 2>&1; then
        score=$((score - 30))
        issues+=("Cannot reach GitHub")
    elif [ -d "$DOTFILES_DIR" ]; then
        cd "$DOTFILES_DIR"
        if ! git ls-remote origin > /dev/null 2>&1; then
            score=$((score - 20))
            issues+=("Cannot connect to repository")
        fi
    fi
    
    # Check SSH authentication
    if ! ssh -o ConnectTimeout=5 -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
        score=$((score - 20))
        issues+=("SSH authentication issues")
    fi
    
    HEALTH_SCORES[network]=$score
    
    if [ ${#issues[@]} -gt 0 ]; then
        log "Network issues: ${issues[*]}"
    fi
    
    return $([ $score -ge 50 ] && echo 0 || echo 1)
}

# Check disk space
check_disk() {
    local score=100
    local issues=()
    
    # Check home directory disk usage
    local usage=$(df "$HOME" | awk 'NR==2 {print int($5)}')
    
    if [ "$usage" -gt 95 ]; then
        score=0
        issues+=("Critical: Disk usage at ${usage}%")
    elif [ "$usage" -gt 90 ]; then
        score=30
        issues+=("Warning: Disk usage at ${usage}%")
    elif [ "$usage" -gt 80 ]; then
        score=70
        issues+=("Disk usage at ${usage}%")
    fi
    
    # Check dotfiles size
    if [ -d "$DOTFILES_DIR" ]; then
        local dotfiles_size=$(du -sm "$DOTFILES_DIR" | cut -f1)
        if [ "$dotfiles_size" -gt 100 ]; then
            score=$((score - 10))
            issues+=("Dotfiles using ${dotfiles_size}MB")
        fi
    fi
    
    HEALTH_SCORES[disk]=$score
    
    if [ ${#issues[@]} -gt 0 ]; then
        log "Disk issues: ${issues[*]}"
    fi
    
    return $([ $score -ge 30 ] && echo 0 || echo 1)
}

# Check sync status
check_sync() {
    local score=100
    local issues=()
    
    if [ ! -d "$DOTFILES_DIR" ]; then
        score=0
        issues+=("No dotfiles directory")
    else
        cd "$DOTFILES_DIR"
        
        # Fetch latest
        git fetch origin --quiet 2>/dev/null || true
        
        # Check if behind
        local behind=$(git rev-list HEAD..origin/main --count 2>/dev/null || echo "0")
        if [ "$behind" -gt 0 ]; then
            score=$((score - 20))
            issues+=("Behind remote by $behind commits")
        fi
        
        # Check if ahead
        local ahead=$(git rev-list origin/main..HEAD --count 2>/dev/null || echo "0")
        if [ "$ahead" -gt 0 ]; then
            score=$((score - 10))
            issues+=("Ahead of remote by $ahead commits")
        fi
        
        # Check last sync time
        if [ -f "$MENTAT_DIR/last_sync" ]; then
            local last_sync=$(cat "$MENTAT_DIR/last_sync")
            local now=$(date +%s)
            local age=$((now - last_sync))
            
            if [ $age -gt 172800 ]; then  # 48 hours
                score=$((score - 30))
                issues+=("No sync in 48+ hours")
            elif [ $age -gt 86400 ]; then  # 24 hours
                score=$((score - 15))
                issues+=("No sync in 24+ hours")
            fi
        fi
        
        # Check for divergence
        if [ "$ahead" -gt 0 ] && [ "$behind" -gt 0 ]; then
            score=$((score - 20))
            issues+=("Local and remote have diverged")
        fi
    fi
    
    HEALTH_SCORES[sync]=$score
    
    if [ ${#issues[@]} -gt 0 ]; then
        log "Sync issues: ${issues[*]}"
    fi
    
    return $([ $score -ge 50 ] && echo 0 || echo 1)
}

# Calculate overall health
calculate_overall_health() {
    local total=0
    local count=0
    
    for category in "${!HEALTH_SCORES[@]}"; do
        total=$((total + HEALTH_SCORES[$category]))
        count=$((count + 1))
    done
    
    local overall=$((total / count))
    echo "$overall"
}

# Generate status report
generate_report() {
    local overall=$(calculate_overall_health)
    local status="HEALTHY"
    local color="$GREEN"
    
    if [ "$overall" -lt 50 ]; then
        status="CRITICAL"
        color="$RED"
    elif [ "$overall" -lt 70 ]; then
        status="WARNING"
        color="$YELLOW"
    fi
    
    # Save to status file
    cat > "$HEALTH_STATUS" << EOF
{
    "timestamp": $(date +%s),
    "overall": $overall,
    "status": "$status",
    "scores": {
        "repository": ${HEALTH_SCORES[repository]},
        "symlinks": ${HEALTH_SCORES[symlinks]},
        "network": ${HEALTH_SCORES[network]},
        "disk": ${HEALTH_SCORES[disk]},
        "sync": ${HEALTH_SCORES[sync]}
    }
}
EOF
    
    # Print report
    echo -e "${color}═══════════════════════════════════════${NC}"
    echo -e "${color}    MENTAT HEALTH: $status ($overall%)${NC}"
    echo -e "${color}═══════════════════════════════════════${NC}"
    
    for category in repository symlinks network disk sync; do
        local score=${HEALTH_SCORES[$category]}
        local indicator="✅"
        
        if [ "$score" -lt 50 ]; then
            indicator="❌"
        elif [ "$score" -lt 70 ]; then
            indicator="⚠️"
        fi
        
        printf "  %-12s %s %3d%%\n" "$category:" "$indicator" "$score"
    done
    
    echo -e "${color}═══════════════════════════════════════${NC}"
}

# Auto-repair function
auto_repair() {
    local fixed=0
    
    # Fix repository issues
    if [ "${HEALTH_SCORES[repository]}" -lt 70 ]; then
        if [ -d "$DOTFILES_DIR" ]; then
            cd "$DOTFILES_DIR"
            
            # Remove lock files
            if [ -f ".git/index.lock" ]; then
                rm -f ".git/index.lock"
                log "Removed lock file"
                fixed=$((fixed + 1))
            fi
            
            # Run git gc
            git gc --auto 2>/dev/null || true
        fi
    fi
    
    # Fix broken symlinks
    if [ "${HEALTH_SCORES[symlinks]}" -lt 70 ]; then
        "$DOTFILES_DIR/scripts/repair-symlinks.sh" 2>/dev/null || true
        fixed=$((fixed + 1))
    fi
    
    if [ $fixed -gt 0 ]; then
        log "Auto-repair: Fixed $fixed issues"
    fi
}

# Alert function
send_alert() {
    local message="$1"
    local severity="${2:-WARNING}"
    
    # Log alert
    log "ALERT [$severity]: $message"
    
    # System notification (macOS)
    if command -v osascript > /dev/null; then
        osascript -e "display notification \"$message\" with title \"Mentat Health Alert\" subtitle \"$severity\""
    fi
    
    # Linux notification
    if command -v notify-send > /dev/null; then
        notify-send "Mentat Health Alert" "$message" -u critical
    fi
}

# Monitor function
monitor() {
    local interval="${1:-300}"  # Default 5 minutes
    local consecutive_failures=0
    
    log "Starting health monitor (interval: ${interval}s)"
    
    while true; do
        # Run all checks
        check_repository || true
        check_symlinks || true
        check_network || true
        check_disk || true
        check_sync || true
        
        # Calculate health
        local overall=$(calculate_overall_health)
        
        # Generate report
        generate_report
        
        # Auto-repair if needed
        if [ "$overall" -lt 70 ]; then
            auto_repair
        fi
        
        # Send alerts
        if [ "$overall" -lt 30 ]; then
            consecutive_failures=$((consecutive_failures + 1))
            if [ $consecutive_failures -ge $ALERT_THRESHOLD ]; then
                send_alert "Critical health issues detected (score: $overall%)" "CRITICAL"
            fi
        elif [ "$overall" -lt 50 ]; then
            send_alert "Health degraded (score: $overall%)" "WARNING"
        else
            consecutive_failures=0
        fi
        
        sleep "$interval"
    done
}

# Main execution
main() {
    local command="${1:-check}"
    
    # Ensure directories exist
    mkdir -p "$MENTAT_DIR"
    
    case "$command" in
        check)
            check_repository
            check_symlinks
            check_network
            check_disk
            check_sync
            generate_report
            ;;
        monitor)
            monitor "${2:-300}"
            ;;
        repair)
            auto_repair
            ;;
        *)
            echo "Usage: $0 {check|monitor|repair} [interval]"
            exit 1
            ;;
    esac
}

# Run if executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi