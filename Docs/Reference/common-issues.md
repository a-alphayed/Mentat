# Common Issues Guide

> **Command Context**: This guide covers both **Terminal Commands** (for installation/setup issues) and **Claude Code Commands** (`/sc:` for development issues). Each section is clearly marked.

**Quick Resolution Focus**: Most common SuperClaude issues can be resolved in under 5 minutes with the right diagnostic approach. This guide provides systematic troubleshooting methods for installation, basic commands, and platform-specific problems.

**Problem Classification**: Issues are categorized by type for fast navigation - installation failures, command execution problems, and platform-specific compatibility issues.

## 🖥️ Installation Issues (Terminal Commands)

### Permission and Access Problems

#### Issue: Permission Denied During Installation
**Error Message**: `ERROR: Permission denied: '/home/user/.claude/CLAUDE.md'`

**Diagnosis**:
```bash
ls -la ~/.claude/
# Check file ownership and permissions
```

**Solution 1**: Fix permissions
```bash
sudo chown -R $USER ~/.claude
chmod 755 ~/.claude
```

**Solution 2**: Use --user installation
```bash
pip install --user SuperClaude
python3 -m SuperClaude install --install-dir ~/superclaude
```

**Verification**:
```bash
ls -la ~/.claude/
python3 -m SuperClaude --version
```

**Prevention**: Always install SuperClaude in user space, avoid sudo for installation

**Issue: Directory Creation Failures**
```bash
# Error message
ERROR: Cannot create directory ~/.claude

# Diagnosis
whoami
ls -la ~/
# Check home directory permissions

# Solution 1: Manual directory creation
mkdir -p ~/.claude
chmod 755 ~/.claude
python3 -m SuperClaude install

# Solution 2: Alternative installation directory
python3 -m SuperClaude install --install-dir ~/Documents/superclaude

# Verification
ls -la ~/.claude/
cat ~/.claude/CLAUDE.md | head -5
```

### Python Version and Compatibility

**Issue: Python Version Compatibility**
```bash
# Error message
ERROR: SuperClaude requires Python 3.8+ but found Python 3.7

# Diagnosis
python3 --version
which python3

# Solution 1: Update Python (Linux/Ubuntu)
sudo apt update
sudo apt install python3.8 python3.8-pip
python3.8 -m pip install SuperClaude

# Solution 2: Use pyenv for version management
curl https://pyenv.run | bash
pyenv install 3.9.0
pyenv global 3.9.0
pip install SuperClaude

# Solution 3: Virtual environment with specific Python
python3.9 -m venv superclaude-env
source superclaude-env/bin/activate
pip install SuperClaude

# Verification
python3 --version
python3 -m SuperClaude --version
```

**Issue: Package Installation Conflicts**
```bash
# Error message
ERROR: Package 'SuperClaude' conflicts with existing installation

# Diagnosis
pip list | grep -i claude
pip show SuperClaude

# Solution 1: Clean uninstall and reinstall
pip uninstall SuperClaude
pip install SuperClaude

# Solution 2: Force upgrade
pip install --upgrade --force-reinstall SuperClaude

# Solution 3: Virtual environment isolation
python3 -m venv fresh-superclaude
source fresh-superclaude/bin/activate
pip install SuperClaude

# Verification
pip show SuperClaude
python3 -m SuperClaude --version
```

### Component Installation Failures

**Issue: Component Installation Failures**
```bash
# Error message
ERROR: Component 'mcp' installation failed - dependency not met

# Diagnosis
python3 -m SuperClaude --version
ls ~/.claude/
# Check component installation status

# Solution 1: Install dependencies first
python3 -m SuperClaude install --components core  # Install core first
python3 -m SuperClaude install --components mcp   # Then install MCP

# Solution 2: Force reinstallation
python3 -m SuperClaude install --components mcp --force

# Solution 3: Clean installation
rm -rf ~/.claude/
python3 -m SuperClaude install --fresh

# Verification
cat ~/.claude/CLAUDE.md | grep -E "MCP|SuperClaude"
ls ~/.claude/

# Prevention
# Always install components in dependency order: core → agents → modes → mcp
```

**Issue: Incomplete Installation**
```bash
# Symptoms: Missing files or configuration elements

# Diagnosis
ls ~/.claude/
cat ~/.claude/CLAUDE.md | wc -l
# Should have substantial content (>100 lines)

# Solution 1: Complete installation
python3 -m SuperClaude install --components core agents modes mcp

# Solution 2: Fresh installation
rm -rf ~/.claude/
python3 -m SuperClaude install --fresh

# Solution 3: Component-by-component installation
python3 -m SuperClaude install --components core
python3 -m SuperClaude install --components agents
python3 -m SuperClaude install --components modes

# Verification
cat ~/.claude/CLAUDE.md | grep "@"
# Should show multiple @imports for components
```

## Platform-Specific Issues

### Windows Platform Issues

**Windows Path and Environment Problems:**
```cmd
# Issue: Path separator problems
ERROR: Cannot find file 'C:\Users\name\.claude\CLAUDE.md'

# Solution: Use proper Windows paths
set CLAUDE_CONFIG_DIR=C:\Users\%USERNAME%\.claude
python -m SuperClaude install --install-dir "%CLAUDE_CONFIG_DIR%"

# Issue: PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Issue: Node.js not found for MCP servers
# Solution: Install Node.js from official source
winget install OpenJS.NodeJS
# or download from https://nodejs.org/

# Verification
python -m SuperClaude --version
dir "%USERPROFILE%\.claude"
```

**Windows Subsystem for Linux (WSL) Issues:**
```bash
# Issue: WSL path conflicts
ERROR: Cannot access Windows user directory

# Solution 1: Use WSL-native paths
python3 -m SuperClaude install --install-dir ~/.claude

# Solution 2: Configure WSL-Windows path mapping
export CLAUDE_CONFIG_DIR=/mnt/c/Users/$USER/.claude
python3 -m SuperClaude install --install-dir "$CLAUDE_CONFIG_DIR"

# Verification
ls ~/.claude/
python3 -m SuperClaude --version
```

### macOS Platform Issues

**macOS Python and Homebrew Conflicts:**
```bash
# Issue: Homebrew Python conflicts
# Solution: Use pyenv for Python management
brew install pyenv
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
source ~/.zshrc
pyenv install 3.9.0
pyenv global 3.9.0

# Issue: Rosetta compatibility on Apple Silicon
# Solution: Install native Python and Node.js
arch -arm64 brew install python@3.9
arch -arm64 brew install node

# Issue: System Integrity Protection conflicts
# Solution: User-space installation only
pip install --user SuperClaude
python3 -m SuperClaude install --install-dir ~/.claude

# Verification
python3 --version
which python3
python3 -m SuperClaude --version
```

**macOS Permission Issues:**
```bash
# Issue: Gatekeeper blocking installation
# Solution: Allow unsigned packages (carefully)
sudo spctl --master-disable  # Temporarily
pip install SuperClaude
sudo spctl --master-enable   # Re-enable after installation

# Issue: Keychain access problems
# Solution: Use system keychain for Node.js packages
security unlock-keychain ~/Library/Keychains/login.keychain

# Verification
python3 -m SuperClaude --version
ls -la ~/.claude/
```

### Linux Distribution Issues

**Ubuntu/Debian Issues:**
```bash
# Issue: Missing system dependencies
sudo apt update
sudo apt install python3-dev python3-pip build-essential

# Issue: Python 3.8+ not available on older versions
# Solution: Add deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9 python3.9-pip
python3.9 -m pip install SuperClaude

# Verification
python3 --version
python3 -m SuperClaude --version
```

**CentOS/RHEL Issues:**
```bash
# Issue: Python 3.8+ not available
sudo yum install python39 python39-pip
python3.9 -m pip install SuperClaude

# Issue: Node.js repository setup for MCP servers
curl -fsSL https://rpm.nodesource.com/setup_lts.x | sudo bash -
sudo yum install -y nodejs

# Verification
python3.9 --version
python3.9 -m SuperClaude --version
```

**Arch Linux Issues:**
```bash
# Issue: Package conflicts
sudo pacman -S python python-pip
pip install --user SuperClaude

# Issue: Node.js version conflicts for MCP
sudo pacman -S nodejs npm
# or use nvm for version management
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node

# Verification
python --version
python -m SuperClaude --version
```

## Basic Command Issues

### Command Recognition Problems

**Issue: Command Not Found**
```bash
# Error message
ERROR: Command '/sc:analyze' not recognized

# Diagnosis
# Check if SuperClaude is properly installed
python3 -m SuperClaude --version
ls ~/.claude/

# Check Claude Code session
claude --version

# Solution 1: Restart Claude Code session
# Exit and restart Claude Code completely

# Solution 2: Verify installation
cat ~/.claude/CLAUDE.md
python3 -m SuperClaude install --components core --force

# Solution 3: Manual verification
cat ~/.claude/CLAUDE.md
# Should contain SuperClaude instructions and imports

# Verification
grep "SuperClaude" ~/.claude/CLAUDE.md
# Should show framework content

# Prevention
# Always restart Claude Code after SuperClaude installation
```

**Issue: Partial Command Recognition**
```bash
# Symptoms: Some commands work, others don't

# Diagnosis
cat ~/.claude/CLAUDE.md | grep -E "@|SuperClaude"
# Check for missing components

# Solution 1: Complete component installation
python3 -m SuperClaude install --components core agents modes mcp

# Solution 2: Reset configuration
cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.backup
python3 -m SuperClaude install --reset-config

# Solution 3: Fresh installation
rm -rf ~/.claude/
python3 -m SuperClaude install --fresh

# Verification
cat ~/.claude/CLAUDE.md | wc -l
# Should have substantial content (>100 lines)
```

### Command Execution Problems

**Issue: Command Timeout or Hanging**
```bash
# Symptoms: Command runs but never completes

# Diagnosis
# Check system resources
top
df -h
ps aux | grep claude

# Solution 1: Reduce scope
python3 -m SuperClaude analyze src/ --scope file    # Instead of entire project

# Solution 2: Use scope limiting
python3 -m SuperClaude analyze ./specific-folder/ --scope module

# Solution 3: Clear session data and restart
# Remove old session files if they exist
rm -rf ~/.claude/sessions/old-*
# Restart Claude Code session

# Verification
time python3 -m SuperClaude --version
# Should complete quickly

# Prevention
# Use appropriate scope for large projects
# Monitor system resources before large operations
```

**Issue: Command Returns Unexpected Results**
```bash
# Symptoms: Command executes but produces wrong output

# Diagnosis
# Check current directory and context
pwd
ls -la

# Solution 1: Use explicit paths
python3 -m SuperClaude analyze ./specific-folder/

# Solution 2: Verify configuration
cat ~/.claude/CLAUDE.md | head -20
grep "SuperClaude" ~/.claude/CLAUDE.md

# Solution 3: Reset session context
# Restart Claude Code and reload if needed

# Verification
python3 -m SuperClaude --version
ls ~/.claude/

# Prevention
# Use explicit paths and clear task descriptions
```

## Configuration Validation

### Quick Health Checks

**Basic Configuration Validation:**
```bash
# Essential health check
python3 -m SuperClaude --version        # Version verification
ls ~/.claude/                           # Check installation
cat ~/.claude/CLAUDE.md | grep "@"      # Check imports

# Component verification
cat ~/.claude/CLAUDE.md | grep -E "FLAGS|RULES|PRINCIPLES"  # Core components
cat ~/.claude/CLAUDE.md | grep -E "MODE_|MCP_"              # Modes and MCP

# File integrity check
wc -l ~/.claude/CLAUDE.md
# Should have substantial content (>100 lines)
```

**System Requirements Validation:**
```bash
# System requirements validation
python3 --version  # Should be 3.8+
which claude       # Should return path to Claude Code
df -h ~            # Check disk space (50MB+ available)
touch ~/.claude/test && rm ~/.claude/test  # Test write permissions

# Expected validations:
# ✅ Python 3.8+ detected
# ✅ Claude Code installation verified  
# ✅ Sufficient disk space (50MB minimum)
# ✅ Write permissions to ~/.claude directory
# ⚠️  Node.js 16+ recommended for MCP servers
```

### Emergency Recovery

**Complete Configuration Reset:**
```bash
# Emergency Recovery Procedure
# Step 1: Backup current state
cp -r ~/.claude ~/.claude.backup.$(date +%Y%m%d)

# Step 2: Complete reset
rm -rf ~/.claude/
python3 -m SuperClaude install --fresh

# Step 3: Verification
python3 -m SuperClaude --version
cat ~/.claude/CLAUDE.md | grep SuperClaude

# Step 4: Gradual reconfiguration
python3 -m SuperClaude install --components core agents modes
# Test after each component

# Prevention
# Regular configuration backups
# Test configuration changes in non-production environment
```

## Quick Diagnostic Commands

### Rapid Problem Identification

**One-Minute Health Check:**
```bash
# Rapid diagnostic sequence
echo "=== SuperClaude Health Check ==="
python3 -m SuperClaude --version
echo "=== Installation Check ==="
ls ~/.claude/
echo "=== Configuration Check ==="
cat ~/.claude/CLAUDE.md | head -5
echo "=== Component Check ==="
grep -c "@" ~/.claude/CLAUDE.md
echo "=== System Resources ==="
df -h ~ | grep -E "Avail|Available"
```

**Problem Classification:**
```bash
# Quick problem identification
if ! python3 -m SuperClaude --version; then
    echo "❌ Installation Problem - Check Python and package installation"
elif ! ls ~/.claude/CLAUDE.md; then
    echo "❌ Configuration Problem - Run fresh installation"
elif [ $(cat ~/.claude/CLAUDE.md | wc -l) -lt 50 ]; then
    echo "⚠️ Incomplete Installation - Reinstall components"
else
    echo "✅ Basic Configuration OK - Check specific component issues"
fi
```

## Related Resources

### Essential References
- **Installation Guide**: [../Getting-Started/installation.md](../Getting-Started/installation.md) - Complete installation procedures
- **MCP Server Guide**: [mcp-server-guide.md](mcp-server-guide.md) - MCP-specific troubleshooting
- **Diagnostic Reference**: [diagnostic-reference.md](diagnostic-reference.md) - Advanced diagnostic procedures
- **System Requirements**: [../Getting-Started/installation.md#prerequisites-setup-🛠️](../Getting-Started/installation.md#prerequisites-setup-🛠️) - Hardware and software requirements

### Support Channels
- **GitHub Issues**: [Technical problems and bug reports](https://github.com/SuperClaude-Org/SuperClaude_Framework/issues)
- **GitHub Discussions**: [General help and community support](https://github.com/SuperClaude-Org/SuperClaude_Framework/discussions)

---

**Emergency Contact**: If all solutions fail, backup your configuration (`cp -r ~/.claude ~/.claude.backup`) and perform a fresh installation (`rm -rf ~/.claude && python3 -m SuperClaude install --fresh`). Report persistent issues to GitHub with diagnostic information.

**Verification Pattern**: After every solution, verify with:
- ✅ `python3 -m SuperClaude --version` - Should return version number
- ✅ `cat ~/.claude/CLAUDE.md | grep SuperClaude` - Should show framework content
- ✅ Try basic commands in Claude Code - Should work without errors