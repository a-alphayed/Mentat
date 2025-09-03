# /mentat:packages

Package management command for tracking and synchronizing installed packages across machines.

## Usage
```
/mentat:packages [action]
```

## Actions

### update
Updates all package tracking files with currently installed packages
```
/mentat:packages update
```
- Updates Brewfile with current Homebrew packages
- Updates npm-global.txt with global npm packages
- Updates pipx-packages.txt with pipx packages
- Updates cursor-extensions.txt with Cursor extensions

### install
Installs all tracked packages on the current machine
```
/mentat:packages install
```
- Installs all Homebrew packages from Brewfile
- Installs all npm global packages
- Installs all pipx packages
- Installs all Cursor extensions

### status
Shows the difference between tracked and installed packages
```
/mentat:packages status
```
- Lists packages that are installed but not tracked
- Lists tracked packages that are not installed
- Shows sync status with remote repository

### sync
Updates package lists and syncs with dotfiles repository
```
/mentat:packages sync
```
- Updates all package lists
- Commits changes to dotfiles repository
- Pushes to GitHub for cross-machine sync

## Examples

```bash
# Update package tracking after installing new tools
/mentat:packages update

# Install all packages on a new machine
/mentat:packages install

# Check what packages need tracking or installation
/mentat:packages status

# Full sync - update lists and push to GitHub
/mentat:packages sync
```

## Package Files

All package tracking files are stored in `~/dotfiles/packages/`:
- `Brewfile` - Homebrew formulae and casks
- `npm-global.txt` - Global npm packages
- `pipx-packages.txt` - Python tools installed via pipx
- `cursor-extensions.txt` - Cursor/VSCode extensions

## Automation

The package lists are automatically updated during dotfiles sync if changes are detected. Manual updates can be triggered using this command when installing new packages.

## Implementation

```bash
# Update package lists
bash ~/dotfiles/scripts/update-package-lists.sh

# Install all packages
bash ~/dotfiles/scripts/install-packages.sh

# Check status
cd ~/dotfiles && git status packages/

# Sync with remote
cd ~/dotfiles && git add packages/ && git commit -m "Update package lists" && git push
```