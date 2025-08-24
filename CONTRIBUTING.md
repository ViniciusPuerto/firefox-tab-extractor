# Contributing to Firefox Tab Extractor

Thank you for your interest in contributing to Firefox Tab Extractor! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to see if the problem has already been reported.

**Bug Report Template:**
```
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment:**
- OS: [e.g. macOS, Windows, Linux]
- Python version: [e.g. 3.8, 3.9]
- Firefox version: [e.g. 100.0]
- firefox-tab-extractor version: [e.g. 1.0.0]

**Additional context**
Add any other context about the problem here.
```

### 💡 Feature Requests

We welcome feature requests! Please use the "enhancement" label when creating an issue.

**Feature Request Template:**
```
**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

## 🔧 Development Setup

### Prerequisites

- Python 3.7 or higher
- Git
- Firefox browser (for testing)

### Setup Steps

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/firefox-tab-extractor.git
   cd firefox-tab-extractor
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=firefox_tab_extractor

# Run specific test file
pytest tests/test_extractor.py

# Run tests with verbose output
pytest -v
```

### Code Quality Tools

```bash
# Format code with Black
black firefox_tab_extractor/

# Check code style with flake8
flake8 firefox_tab_extractor/

# Type checking with mypy
mypy firefox_tab_extractor/
```

## 📝 Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use Black for code formatting (line length: 88 characters)
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes

### Example Code Style

```python
from typing import List, Optional, Dict, Any
from datetime import datetime


def extract_tabs_from_session(session_data: Dict[str, Any]) -> List[Tab]:
    """
    Extract tab information from Firefox session data.
    
    Args:
        session_data: Parsed session data from Firefox
        
    Returns:
        List of Tab objects
        
    Raises:
        SessionDataError: If session data is invalid
    """
    tabs: List[Tab] = []
    
    if 'windows' not in session_data:
        raise SessionDataError("No windows found in session data")
    
    # ... implementation ...
    
    return tabs
```

### Commit Message Guidelines

Use conventional commit messages:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for code style changes
- `refactor:` for code refactoring
- `test:` for adding or updating tests
- `chore:` for maintenance tasks

Example:
```
feat: add support for Chrome browser tabs

- Add ChromeTabExtractor class
- Implement Chrome profile detection
- Add tests for Chrome functionality
- Update documentation with Chrome examples

Closes #123
```

## 🚀 Making Changes

### Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following the style guidelines
   - Add tests for new functionality
   - Update documentation if needed

3. **Run tests and quality checks**
   ```bash
   pytest
   black firefox_tab_extractor/
   flake8 firefox_tab_extractor/
   mypy firefox_tab_extractor/
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: your commit message"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Fill out the PR template
   - Request review from maintainers

### Pull Request Template

```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] All existing tests pass
- [ ] I have tested the changes manually

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

## 🧪 Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Use mocking for external dependencies
- Aim for good test coverage

### Example Test

```python
def test_extract_tabs_from_session_with_valid_data():
    """Test extracting tabs from valid session data."""
    session_data = {
        'windows': [
            {
                'tabs': [
                    {
                        'index': 1,
                        'entries': [
                            {
                                'title': 'Test Tab',
                                'url': 'https://example.com'
                            }
                        ],
                        'lastAccessed': 1705312200000,
                        'pinned': False,
                        'hidden': False
                    }
                ]
            }
        ]
    }
    
    extractor = FirefoxTabExtractor()
    tabs = extractor._extract_tabs_from_session(session_data)
    
    assert len(tabs) == 1
    assert tabs[0].title == 'Test Tab'
    assert tabs[0].url == 'https://example.com'
```

## 📚 Documentation

### Updating Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add examples for new features
- Update installation instructions if needed

### Documentation Standards

- Use clear, concise language
- Include code examples
- Add screenshots for UI changes
- Keep documentation up to date with code changes

## 🏷️ Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is up to date
- [ ] CHANGELOG.md is updated
- [ ] Version number is updated in setup.py and __init__.py
- [ ] Release notes are written
- [ ] PyPI package is built and uploaded

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the project's coding standards

### Getting Help

- Check existing issues and discussions
- Ask questions in GitHub Discussions
- Join our community chat (if available)
- Read the documentation thoroughly

## 🙏 Recognition

Contributors will be recognized in:

- The project's README.md
- Release notes
- GitHub contributors page
- Documentation acknowledgments

Thank you for contributing to Firefox Tab Extractor! 🎉
