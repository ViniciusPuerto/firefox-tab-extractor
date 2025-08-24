# PyPI Publishing Guide for Firefox Tab Extractor

This guide walks you through the process of publishing the Firefox Tab Extractor package to PyPI (Python Package Index).

## 🚀 Quick Start

### Automated Publishing (Recommended)

1. **Set up GitHub Secrets** (see section below)
2. **Create a GitHub Release** with a version tag (e.g., `v1.0.0`)
3. **The GitHub Action will automatically publish to PyPI**

### Manual Publishing

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to Test PyPI first
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ firefox-tab-extractor

# If everything works, upload to PyPI
twine upload dist/*
```

## 🔧 Setup Instructions

### 1. PyPI Account Setup

#### Create PyPI Account
1. Go to [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. Create an account with a unique username
3. Verify your email address

#### Create Test PyPI Account
1. Go to [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/)
2. Create an account (can be same username as PyPI)
3. Verify your email address

### 2. API Token Setup

#### PyPI API Token
1. Go to [https://pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)
2. Click "Add API token"
3. Give it a name (e.g., "Firefox Tab Extractor")
4. Select "Entire account (all projects)"
5. Copy the token (starts with `pypi-`)

#### Test PyPI API Token
1. Go to [https://test.pypi.org/manage/account/token/](https://test.pypi.org/manage/account/token/)
2. Click "Add API token"
3. Give it a name (e.g., "Firefox Tab Extractor Test")
4. Select "Entire account (all projects)"
5. Copy the token (starts with `pypi-`)

### 3. GitHub Secrets Setup

For automated publishing, add these secrets to your GitHub repository:

1. Go to your GitHub repository
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Add these secrets:

```
PYPI_API_TOKEN = pypi-your_actual_token_here
TEST_PYPI_API_TOKEN = pypi-your_test_token_here
```

### 4. Local Environment Setup

For manual publishing, set environment variables:

```bash
# For macOS/Linux
export PYPI_TOKEN="pypi-your_actual_token_here"
export TEST_PYPI_TOKEN="pypi-your_test_token_here"

# For Windows (PowerShell)
$env:PYPI_TOKEN="pypi-your_actual_token_here"
$env:TEST_PYPI_TOKEN="pypi-your_test_token_here"
```

## 📦 Publishing Workflows

### Option 1: GitHub Actions (Automated)

#### Trigger by Release
1. Update version in `pyproject.toml` and `firefox_tab_extractor/__init__.py`
2. Commit and push changes
3. Create a new GitHub release with version tag (e.g., `v1.0.0`)
4. The workflow will automatically:
   - Run tests on multiple Python versions
   - Build the package
   - Publish to PyPI
   - Publish to Test PyPI

#### Manual Trigger
1. Go to GitHub repository → Actions
2. Select "Publish to PyPI" workflow
3. Click "Run workflow"
4. Enter version number
5. Click "Run workflow"

### Option 2: Local Script (Manual)

Use the provided build script:

```bash
# Make script executable (if not already)
chmod +x scripts/build_and_publish.sh

# Build package only
./scripts/build_and_publish.sh build

# Publish to Test PyPI
./scripts/build_and_publish.sh test-pypi

# Publish to PyPI
./scripts/build_and_publish.sh pypi

# Full release (build + publish to PyPI)
./scripts/build_and_publish.sh release
```

### Option 3: Manual Commands

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Run tests
pytest tests/ -v

# Run linting
black --check firefox_tab_extractor/ tests/ examples/
flake8 firefox_tab_extractor/ tests/ examples/
mypy firefox_tab_extractor/

# Build package
python -m build

# Check package
twine check dist/*

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ firefox-tab-extractor

# Upload to PyPI
twine upload dist/*
```

## 🔄 Release Process

### 1. Version Update

Before each release, update the version in these files:

```bash
# Update pyproject.toml
# Update firefox_tab_extractor/__init__.py
# Update CHANGELOG.md
```

### 2. Pre-release Checklist

- [ ] All tests pass
- [ ] Code is linted and formatted
- [ ] Documentation is up to date
- [ ] Version numbers are updated
- [ ] CHANGELOG.md is updated
- [ ] README.md is current

### 3. Release Steps

#### For GitHub Actions:
1. Commit all changes
2. Push to main branch
3. Create GitHub release with version tag
4. Monitor Actions tab for completion

#### For Manual Release:
1. Run pre-release checks
2. Build and test locally
3. Publish to Test PyPI
4. Test installation from Test PyPI
5. Publish to PyPI
6. Create GitHub release

### 4. Post-release

- [ ] Verify package is available on PyPI
- [ ] Test installation: `pip install firefox-tab-extractor`
- [ ] Update documentation if needed
- [ ] Announce release on social media/GitHub

## 🧪 Testing Before Publishing

### Test Package Locally

```bash
# Build package
python -m build

# Install in development mode
pip install -e .

# Test CLI
firefox-tab-extractor --help

# Test library import
python -c "from firefox_tab_extractor import FirefoxTabExtractor; print('Success!')"
```

### Test from Test PyPI

```bash
# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ firefox-tab-extractor

# Test functionality
firefox-tab-extractor --stats-only
```

## 🚨 Troubleshooting

### Common Issues

#### 1. "Package already exists" Error
- Check if version already exists on PyPI
- Increment version number
- Update version in all files

#### 2. "Invalid distribution" Error
- Check `MANIFEST.in` includes all necessary files
- Verify `pyproject.toml` is properly formatted
- Run `twine check dist/*` to validate

#### 3. "Authentication failed" Error
- Verify API token is correct
- Check token has proper permissions
- Ensure token is not expired

#### 4. "Build failed" Error
- Check all dependencies are installed
- Verify Python version compatibility
- Check for syntax errors in code

### Debug Commands

```bash
# Check package contents
tar -tzf dist/firefox_tab_extractor-*.tar.gz

# Validate package
twine check dist/*

# Test upload (dry run)
twine upload --repository testpypi --dry-run dist/*

# Check PyPI package info
pip show firefox-tab-extractor
```

## 📋 Version Management

### Semantic Versioning

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

### Version Update Locations

1. `pyproject.toml` - `version = "1.0.0"`
2. `firefox_tab_extractor/__init__.py` - `__version__ = "1.0.0"`
3. `CHANGELOG.md` - Add new version entry

### Example Version Update

```bash
# Update version in pyproject.toml
sed -i 's/version = "1.0.0"/version = "1.0.1"/' pyproject.toml

# Update version in __init__.py
sed -i 's/__version__ = "1.0.0"/__version__ = "1.0.1"/' firefox_tab_extractor/__init__.py

# Update CHANGELOG.md (manually)
# Add new version entry with changes
```

## 🔐 Security Best Practices

### Token Security

- Never commit tokens to version control
- Use environment variables or GitHub secrets
- Rotate tokens regularly
- Use least-privilege access

### Package Security

- Sign packages with GPG (optional but recommended)
- Use HTTPS for all uploads
- Verify package integrity after upload
- Monitor for security vulnerabilities

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review PyPI documentation: [https://packaging.python.org/](https://packaging.python.org/)
3. Check GitHub Actions logs for automated publishing
4. Create an issue in the repository

## 🎉 Success Checklist

After publishing, verify:

- [ ] Package appears on PyPI: [https://pypi.org/project/firefox-tab-extractor/](https://pypi.org/project/firefox-tab-extractor/)
- [ ] Installation works: `pip install firefox-tab-extractor`
- [ ] CLI works: `firefox-tab-extractor --help`
- [ ] Library import works: `from firefox_tab_extractor import FirefoxTabExtractor`
- [ ] GitHub release is created with proper notes
- [ ] Documentation is updated if needed

---

**Happy Publishing! 🚀**
