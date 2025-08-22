# SuperClaude Framework Release Instructions

## 🚀 Complete Publishing Guide for PyPI and NPM

**Version**: 4.0.0 (PyPI) / 4.0.3 (NPM)  
**Date**: 2025-08-22  
**Status**: READY FOR RELEASE

---

## 📋 Pre-Flight Checklist

### Critical Fixes Applied ✅
- [x] Version consistency fixed (PyPI: 4.0.0)
- [x] License format updated to PEP 639 compliance
- [x] NPM package name corrected to `@superclaude-org/superclaude`
- [x] NPM version incremented to 4.0.3 (from existing 4.0.2)

### Required Accounts
- [ ] PyPI account with maintainer access
- [ ] TestPyPI account for testing
- [ ] NPM account with org access to @superclaude-org
- [ ] GitHub account with repo write access

---

## 🔐 Step 1: Setup Credentials

### PyPI Credentials

1. **Create PyPI API Token** (if not exists):
   ```bash
   # Go to https://pypi.org/manage/account/token/
   # Create token with scope: "Entire account" or "Project: SuperClaude"
   # Save token securely
   ```

2. **Create ~/.pypirc file**:
   ```ini
   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
   username = __token__
   password = pypi-YOUR_TOKEN_HERE

   [testpypi]
   username = __token__
   password = pypi-YOUR_TEST_TOKEN_HERE
   repository = https://test.pypi.org/legacy/
   ```

3. **Secure the file**:
   ```bash
   chmod 600 ~/.pypirc
   ```

### NPM Credentials

1. **Login to NPM**:
   ```bash
   npm login
   # Enter username, password, email
   # Enter OTP if 2FA enabled
   ```

2. **Verify login**:
   ```bash
   npm whoami
   # Should show your username
   
   npm org ls @superclaude-org
   # Should show you have access
   ```

---

## 🧪 Step 2: Test Deployments

### Test PyPI Deployment

1. **Clean previous builds**:
   ```bash
   rm -rf dist/ build/ *.egg-info
   ```

2. **Run validation**:
   ```bash
   python3 scripts/validate_pypi_ready.py
   # Must show 5/5 checks passed
   ```

3. **Build packages**:
   ```bash
   python3 setup.py sdist bdist_wheel
   ```

4. **Upload to TestPyPI**:
   ```bash
   ./scripts/publish.sh test
   # OR manually:
   python3 -m twine upload --repository testpypi dist/*
   ```

5. **Test installation from TestPyPI**:
   ```bash
   # Create virtual environment
   python3 -m venv test_env
   source test_env/bin/activate
   
   # Install from TestPyPI
   pip install --index-url https://test.pypi.org/simple/ \
               --extra-index-url https://pypi.org/simple/ \
               SuperClaude==4.0.0
   
   # Test the CLI
   SuperClaude --version
   SuperClaude install --dry-run
   
   # Cleanup
   deactivate
   rm -rf test_env
   ```

### Test NPM Deployment

1. **Verify package configuration**:
   ```bash
   npm publish --dry-run
   # Check output for:
   # - Correct package name: @superclaude-org/superclaude
   # - Version: 4.0.3
   # - Files included: bin/, README.md, LICENSE, package.json
   ```

2. **Local test**:
   ```bash
   # Pack the package
   npm pack
   
   # Test local installation
   npm install -g ./superclaude-org-superclaude-4.0.3.tgz
   
   # Verify it works
   superclaude --version
   
   # Uninstall test
   npm uninstall -g @superclaude-org/superclaude
   ```

---

## 🚀 Step 3: Production Release

### ⚠️ FINAL CHECKS BEFORE RELEASE

```bash
# Ensure on correct branch
git branch --show-current
# Should show: SuperClaude_V4_Beta or master

# Ensure working directory is clean
git status
# Should show: nothing to commit, working tree clean

# Tag the release
git tag -a v4.0.0 -m "Release v4.0.0 - Production ready"
git push origin v4.0.0
```

### PyPI Production Release

1. **Final validation**:
   ```bash
   python3 scripts/validate_pypi_ready.py
   # MUST show: "Project is ready for PyPI publication!"
   ```

2. **Clean and rebuild**:
   ```bash
   rm -rf dist/ build/ *.egg-info
   python3 setup.py sdist bdist_wheel
   ```

3. **Upload to PyPI**:
   ```bash
   ./scripts/publish.sh prod
   # OR manually:
   python3 -m twine upload dist/*
   ```

4. **Verify on PyPI**:
   ```bash
   # Wait 1-2 minutes for CDN propagation
   pip install SuperClaude==4.0.0 --no-cache-dir
   SuperClaude --version
   ```

### NPM Production Release

1. **Ensure logged in**:
   ```bash
   npm whoami
   # Must show your username
   ```

2. **Publish with 2FA** (if enabled):
   ```bash
   npm publish --otp=YOUR_2FA_CODE
   # Without 2FA:
   npm publish
   ```

3. **Verify on NPM**:
   ```bash
   # Wait 1-2 minutes
   npm view @superclaude-org/superclaude@4.0.3
   
   # Test installation
   npm install -g @superclaude-org/superclaude@4.0.3
   superclaude --version
   ```

---

## 🔄 Step 4: Post-Release Verification

### Verification Checklist

1. **PyPI Verification**:
   ```bash
   # Check PyPI page
   open https://pypi.org/project/SuperClaude/4.0.0/
   
   # Fresh install test
   pip install SuperClaude==4.0.0 --no-cache-dir
   SuperClaude install --list-components
   ```

2. **NPM Verification**:
   ```bash
   # Check NPM page
   open https://www.npmjs.com/package/@superclaude-org/superclaude
   
   # Fresh install test
   npm install -g @superclaude-org/superclaude@4.0.3
   superclaude install --list-components
   ```

3. **Cross-platform test**:
   ```bash
   # Test NPM → PyPI flow
   npm install -g @superclaude-org/superclaude
   superclaude install --dry-run
   # Should successfully detect/install Python package
   ```

---

## 🔙 Rollback Procedures

### If PyPI Release Fails

1. **Yank the release** (makes it non-installable):
   ```bash
   # Via web interface:
   # https://pypi.org/manage/project/SuperClaude/release/4.0.0/
   # Click "Options" → "Yank"
   
   # Users can still install if they specify exact version
   ```

2. **Fix issues and release patch**:
   ```bash
   # Update version to 4.0.1
   # Fix issues
   # Re-release following steps above
   ```

### If NPM Release Fails

1. **Unpublish** (within 72 hours):
   ```bash
   npm unpublish @superclaude-org/superclaude@4.0.3
   ```

2. **Deprecate** (after 72 hours):
   ```bash
   npm deprecate @superclaude-org/superclaude@4.0.3 "Critical bug - use 4.0.4"
   ```

---

## 📢 Step 5: Announcement

### GitHub Release

1. Create release at: https://github.com/SuperClaude-Org/SuperClaude_Framework/releases/new
2. Tag: v4.0.0
3. Title: "SuperClaude v4.0.0 - Production Release"
4. Description: Include changelog and installation instructions

### Update Documentation

```bash
# Update README badges
# Update installation docs
# Update website if applicable
```

### Community Announcement Template

```markdown
🎉 SuperClaude v4.0.0 Released!

Install via:
- PyPI: `pip install SuperClaude`
- NPM: `npm install -g @superclaude-org/superclaude`

What's New:
- 14 specialized AI agents
- 6 integrated MCP servers
- 30-50% token usage reduction
- [Full changelog](link)

Docs: https://github.com/SuperClaude-Org/SuperClaude_Framework
```

---

## ⚠️ Common Issues & Solutions

### PyPI Issues

**"Invalid credentials"**
- Regenerate API token
- Ensure token starts with `pypi-`
- Check ~/.pypirc formatting

**"Version already exists"**
- Can't overwrite - increment version
- Update all version references

### NPM Issues

**"402 Payment Required"**
- Package name might be private
- Check org settings

**"403 Forbidden"**
- No publish access to org
- Contact org admin

**"E409 Conflict"**
- Version already exists
- Increment version number

---

## 📊 Success Metrics

After 24 hours, check:
- PyPI download stats: https://pypistats.org/packages/superclaude
- NPM download stats: https://www.npmjs.com/package/@superclaude-org/superclaude
- GitHub stars/issues
- Community feedback

---

## 🎯 Quick Command Summary

```bash
# PyPI Test & Release
./scripts/publish.sh test          # Test on TestPyPI
./scripts/publish.sh prod          # Release to PyPI

# NPM Test & Release  
npm publish --dry-run              # Test locally
npm publish --otp=123456           # Release to NPM

# Verification
pip install SuperClaude==4.0.0
npm install -g @superclaude-org/superclaude@4.0.3
```

---

**Remember**: Once published to PyPI, versions cannot be reused. Plan carefully!

Good luck with the release! 🚀