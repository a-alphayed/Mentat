#!/bin/bash
# Mentat SSH Authentication Test Script
# Tests and troubleshoots SSH authentication for GitHub

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║        Mentat SSH Authentication Test            ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════╝${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for SSH
echo -e "${BLUE}1. Checking SSH installation...${NC}"
if command_exists ssh; then
    echo -e "   ${GREEN}✅ SSH is installed${NC}"
    ssh -V 2>&1 | head -1 | sed 's/^/   /'
else
    echo -e "   ${RED}❌ SSH is not installed${NC}"
    echo "   Please install SSH first"
    exit 1
fi

# Check for SSH directory
echo -e "\n${BLUE}2. Checking SSH directory...${NC}"
if [ -d ~/.ssh ]; then
    echo -e "   ${GREEN}✅ SSH directory exists${NC}"
    
    # Check permissions
    perms=$(stat -f "%OLp" ~/.ssh 2>/dev/null || stat -c "%a" ~/.ssh 2>/dev/null || echo "unknown")
    if [ "$perms" = "700" ]; then
        echo -e "   ${GREEN}✅ Correct permissions (700)${NC}"
    else
        echo -e "   ${YELLOW}⚠️  Incorrect permissions: $perms (should be 700)${NC}"
        echo "   Fix with: chmod 700 ~/.ssh"
    fi
else
    echo -e "   ${YELLOW}⚠️  SSH directory doesn't exist${NC}"
    echo "   Creating ~/.ssh directory..."
    mkdir -p ~/.ssh
    chmod 700 ~/.ssh
    echo -e "   ${GREEN}✅ Created ~/.ssh with correct permissions${NC}"
fi

# Check for SSH keys
echo -e "\n${BLUE}3. Checking for SSH keys...${NC}"
KEY_FOUND=false
KEY_FILES=""

for key_type in "ed25519" "rsa" "ecdsa" "dsa"; do
    key_file="$HOME/.ssh/id_$key_type"
    if [ -f "$key_file" ]; then
        echo -e "   ${GREEN}✅ Found $key_type key: $key_file${NC}"
        KEY_FOUND=true
        KEY_FILES="$KEY_FILES $key_file"
    fi
done

if [ "$KEY_FOUND" = false ]; then
    echo -e "   ${YELLOW}⚠️  No SSH keys found${NC}"
    echo ""
    echo -e "   ${BLUE}To generate a new SSH key:${NC}"
    echo "   ssh-keygen -t ed25519 -C \"your_email@example.com\""
    echo ""
fi

# Check SSH agent
echo -e "\n${BLUE}4. Checking SSH agent...${NC}"
if ssh-add -l &>/dev/null; then
    echo -e "   ${GREEN}✅ SSH agent is running with keys loaded${NC}"
    echo "   Loaded keys:"
    ssh-add -l | sed 's/^/   /'
elif [ $? -eq 1 ]; then
    echo -e "   ${YELLOW}⚠️  SSH agent is running but no keys loaded${NC}"
    echo ""
    echo -e "   ${BLUE}To add your key to the agent:${NC}"
    if [ -n "$KEY_FILES" ]; then
        for key in $KEY_FILES; do
            echo "   ssh-add $key"
        done
    else
        echo "   ssh-add ~/.ssh/id_ed25519"
    fi
    echo ""
else
    echo -e "   ${YELLOW}⚠️  SSH agent is not running${NC}"
    echo ""
    echo -e "   ${BLUE}To start SSH agent:${NC}"
    echo "   eval \"\$(ssh-agent -s)\""
    echo "   ssh-add ~/.ssh/id_ed25519"
    echo ""
fi

# Check GitHub connectivity
echo -e "\n${BLUE}5. Testing GitHub SSH authentication...${NC}"
echo -e "   Connecting to git@github.com..."

# Test SSH connection to GitHub
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo -e "   ${GREEN}✅ Successfully authenticated with GitHub!${NC}"
    
    # Show which key is being used
    echo ""
    echo -e "   ${BLUE}Authentication details:${NC}"
    ssh -T git@github.com 2>&1 | grep "Hi" | sed 's/^/   /'
    
    GITHUB_AUTH=true
else
    echo -e "   ${RED}❌ Could not authenticate with GitHub${NC}"
    
    # Check if GitHub is in known_hosts
    if ! grep -q "github.com" ~/.ssh/known_hosts 2>/dev/null; then
        echo -e "   ${YELLOW}⚠️  GitHub not in known_hosts${NC}"
        echo ""
        echo -e "   ${BLUE}Adding GitHub to known hosts...${NC}"
        ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts 2>/dev/null
        echo -e "   ${GREEN}✅ Added GitHub to known_hosts${NC}"
        echo ""
        echo "   Retrying authentication..."
        if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
            echo -e "   ${GREEN}✅ Now successfully authenticated!${NC}"
            GITHUB_AUTH=true
        else
            echo -e "   ${RED}❌ Still cannot authenticate${NC}"
            GITHUB_AUTH=false
        fi
    else
        GITHUB_AUTH=false
    fi
fi

# If not authenticated, provide guidance
if [ "$GITHUB_AUTH" = false ]; then
    echo ""
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}To fix GitHub authentication:${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    if [ "$KEY_FOUND" = false ]; then
        echo -e "${BLUE}1. Generate an SSH key:${NC}"
        echo "   ssh-keygen -t ed25519 -C \"your_email@example.com\""
        echo ""
    fi
    
    if [ "$KEY_FOUND" = true ]; then
        echo -e "${BLUE}1. Copy your public key:${NC}"
        for key in $KEY_FILES; do
            if [ -f "${key}.pub" ]; then
                echo "   cat ${key}.pub"
                break
            fi
        done
        echo ""
    fi
    
    echo -e "${BLUE}2. Add the key to GitHub:${NC}"
    echo "   • Go to: https://github.com/settings/keys"
    echo "   • Click 'New SSH key'"
    echo "   • Paste your public key"
    echo "   • Click 'Add SSH key'"
    echo ""
    
    echo -e "${BLUE}3. Test again:${NC}"
    echo "   ssh -T git@github.com"
fi

# Test repository access (if configured)
CONFIG_FILE="$HOME/.mentat/config.json"
if [ -f "$CONFIG_FILE" ] && command_exists python3; then
    echo -e "\n${BLUE}6. Checking Mentat configuration...${NC}"
    
    REPO_URL=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE')).get('dotfiles_repo', ''))" 2>/dev/null || echo "")
    
    if [ -n "$REPO_URL" ]; then
        echo -e "   Repository: ${CYAN}$REPO_URL${NC}"
        
        if [[ "$REPO_URL" == git@* ]]; then
            echo -e "\n${BLUE}7. Testing repository access...${NC}"
            if git ls-remote "$REPO_URL" HEAD &>/dev/null; then
                echo -e "   ${GREEN}✅ Can access your dotfiles repository!${NC}"
            else
                echo -e "   ${RED}❌ Cannot access repository${NC}"
                echo "   Possible reasons:"
                echo "   • Repository doesn't exist yet"
                echo "   • Repository name is incorrect"
                echo "   • You don't have access to this repository"
            fi
        fi
    else
        echo -e "   ${YELLOW}⚠️  No repository configured${NC}"
        echo "   Run: mentat install"
        echo "   Or: /mentat:config"
    fi
else
    echo -e "\n${YELLOW}ℹ️  Mentat not configured yet${NC}"
fi

# Summary
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}Summary${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [ "$GITHUB_AUTH" = true ]; then
    echo -e "${GREEN}✅ SSH authentication is working correctly!${NC}"
    echo "You can use private GitHub repositories with Mentat."
else
    echo -e "${YELLOW}⚠️  SSH authentication needs to be configured${NC}"
    echo "Follow the steps above to set up SSH with GitHub."
fi

echo ""