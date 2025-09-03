# Package Management System

## Overview

Mentat's package management system ensures consistent development environments across all your machines by tracking and synchronizing installed packages from multiple package managers.

## Supported Package Managers

### Homebrew (macOS/Linux)
- **File**: `packages/Brewfile`
- **Tracks**: Formulae, casks, taps
- **Update**: `brew bundle dump --file=~/dotfiles/packages/Brewfile --force`
- **Install**: `brew bundle install --file=~/dotfiles/packages/Brewfile`

### npm (Node.js)
- **File**: `packages/npm-global.txt`
- **Tracks**: Global npm packages
- **Update**: Automatic via update script
- **Install**: Loop through file with `npm install -g`

### pipx (Python)
- **File**: `packages/pipx-packages.txt`
- **Tracks**: Python applications
- **Update**: `pipx list --short | cut -d' ' -f1`
- **Install**: Loop through file with `pipx install`

### Cursor/VSCode Extensions
- **File**: `packages/cursor-extensions.txt`
- **Tracks**: Editor extensions
- **Update**: `cursor --list-extensions`
- **Install**: Loop through with `cursor --install-extension`

## Command Usage

### Update Package Lists

After installing new packages, capture them:

```bash
# Using Mentat command
/mentat:packages update

# Or directly with script
bash ~/dotfiles/scripts/update-package-lists.sh
```

This will:
1. Scan all package managers
2. Update tracking files
3. Show what changed
4. Ready for commit/sync

### Install Packages

On a new machine or after pulling updates:

```bash
# Using Mentat command
/mentat:packages install

# Or directly with script
bash ~/dotfiles/scripts/install-packages.sh
```

This will:
1. Read all tracking files
2. Install missing packages
3. Skip already installed
4. Report any failures

### Check Status

See differences between tracked and installed:

```bash
/mentat:packages status
```

Shows:
- Installed but not tracked
- Tracked but not installed
- Version mismatches
- Sync status

### Sync Package Lists

Update and push to GitHub:

```bash
/mentat:packages sync
```

Performs:
1. Update all lists
2. Commit changes
3. Push to remote
4. Trigger sync

## Tracking Files

### Brewfile Format

```ruby
tap "nikitabobko/tap"
brew "git"
brew "node"
brew "pipx"
brew "powerlevel10k"
cask "wezterm"
cask "font-meslo-lg-nerd-font"
vscode "ms-python.python"
```

**Categories**:
- `tap`: Third-party repositories
- `brew`: Command-line tools
- `cask`: GUI applications
- `vscode`: Extensions (Cursor/VSCode)

### npm-global.txt Format

```
typescript
eslint
prettier
npm-check-updates
```

One package per line, without version numbers.

### pipx-packages.txt Format

```
black
flake8
mypy
poetry
```

Python applications, one per line.

### cursor-extensions.txt Format

```
ms-python.python
ms-python.debugpy
esbenp.prettier-vscode
dbaeumer.vscode-eslint
```

Extension IDs in `publisher.name` format.

## Scripts

### update-package-lists.sh

Located at `~/dotfiles/scripts/update-package-lists.sh`

**What it does**:
1. Checks for each package manager
2. Exports current state to tracking files
3. Handles missing managers gracefully
4. Provides colored output

**Key Functions**:
- Brewfile generation with `brew bundle dump`
- npm global list parsing
- pipx package extraction
- Cursor extension listing

### install-packages.sh

Located at `~/dotfiles/scripts/install-packages.sh`

**What it does**:
1. Reads all tracking files
2. Installs packages per manager
3. Skips existing packages
4. Reports failures

**Error Handling**:
- Missing package managers warning
- Individual package failure recovery
- Continues despite errors
- Summary at completion

## Workflow Examples

### Daily Development

```bash
# Morning - pull latest
cd ~/dotfiles && git pull

# Install any new packages from team
/mentat:packages install

# Work day - install new tool
brew install jq
npm install -g @angular/cli

# Evening - update tracking
/mentat:packages update

# Push changes
/mentat:sync
```

### New Project Setup

```bash
# Project needs specific tools
brew install postgresql
npm install -g yarn
pipx install cookiecutter

# Capture immediately
/mentat:packages update

# Commit with context
cd ~/dotfiles
git add -A
git commit -m "Add tools for new Python project"
git push
```

### Team Onboarding

```bash
# New team member setup
git clone https://github.com/team/dotfiles.git ~/dotfiles
cd ~/dotfiles
./setup.sh

# Install all team tools
bash scripts/install-packages.sh

# They're ready to work!
```

## Advanced Features

### Machine-Specific Packages

For packages only needed on certain machines:

```bash
# Create local Brewfile
~/dotfiles/packages/Brewfile.local

# Won't be tracked in git
echo "Brewfile.local" >> ~/dotfiles/.gitignore
```

### Conditional Installation

Modify install script for conditions:

```bash
# Only on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew install mac-specific-tool
fi

# Only on work machine
if [[ "$HOSTNAME" == "work-laptop" ]]; then
    brew install work-tools
fi
```

### Version Pinning

For specific versions in Brewfile:

```ruby
brew "node@18"
brew "postgresql@14"
cask "docker", args: { version: "4.15.0" }
```

### Backup Before Updates

Create safety snapshot:

```bash
# Backup current state
cp ~/dotfiles/packages/Brewfile ~/dotfiles/packages/Brewfile.backup

# Update
/mentat:packages update

# Compare if needed
diff ~/dotfiles/packages/Brewfile ~/dotfiles/packages/Brewfile.backup
```

## Troubleshooting

### Common Issues

**Brewfile syntax error**:
```bash
# Validate Brewfile
brew bundle check --file=~/dotfiles/packages/Brewfile

# Fix syntax and retry
```

**npm permission denied**:
```bash
# Fix npm permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
```

**pipx not found**:
```bash
# Install pipx first
brew install pipx
pipx ensurepath
```

**Cursor command not found**:
```bash
# Add to PATH
export PATH="/Applications/Cursor.app/Contents/Resources/app/bin:$PATH"
```

### Recovery Procedures

**Corrupted package file**:
```bash
# Restore from git
cd ~/dotfiles
git checkout packages/Brewfile

# Or regenerate
brew bundle dump --file=~/dotfiles/packages/Brewfile --force
```

**Partial installation failure**:
```bash
# Check what's installed
brew list
npm list -g --depth=0
pipx list

# Manually install missing
brew install missing-package
```

**Sync conflicts**:
```bash
# Pull and merge
cd ~/dotfiles
git pull --rebase
git mergetool  # Resolve conflicts

# Regenerate if needed
/mentat:packages update
```

## Best Practices

1. **Update Regularly**: Run update after any installation
2. **Commit Context**: Add meaningful commit messages
3. **Test First**: Try packages before adding to tracking
4. **Clean Periodically**: Remove unused packages
5. **Document Custom**: Note why unusual packages needed

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Validate Packages
on: [push, pull_request]

jobs:
  validate:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate Brewfile
        run: brew bundle check --file=packages/Brewfile
      - name: Check npm packages
        run: cat packages/npm-global.txt | xargs -I {} npm view {} > /dev/null
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Update package lists before commit
bash scripts/update-package-lists.sh

# Add updated files
git add packages/*
```

## Package Categories

### Essential Developer Tools
```
git, node, python, docker
vim, tmux, curl, wget, jq
```

### Productivity Enhancers
```
eza, zoxide, fzf, ripgrep
bat, fd, htop, ncdu
```

### Shell Enhancements
```
powerlevel10k, zsh-syntax-highlighting
zsh-autosuggestions, zsh-completions
```

### Development Utilities
```
postgresql, redis, nginx
awscli, gh, hub, lazygit
```

## Maintenance

### Regular Cleanup

```bash
# Remove unused Homebrew packages
brew bundle cleanup --file=~/dotfiles/packages/Brewfile

# Check for outdated
brew outdated
npm outdated -g
```

### Update Everything

```bash
# Update all packages
brew upgrade
npm update -g
pipx upgrade-all

# Capture new versions
/mentat:packages update
```

### Audit Security

```bash
# Check for vulnerabilities
brew audit
npm audit -g
```

## Future Enhancements

Planned improvements:
- apt/dnf support for Linux
- Version locking capabilities
- Dependency resolution
- Package groups/profiles
- Automated cleanup
- Cloud backup integration