# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure and documentation
- Basic Firefox tab extraction functionality
- CLI interface with multiple options
- JSON and CSV output formats
- Comprehensive error handling
- Type hints and documentation
- Test suite with pytest
- Examples for basic usage and Notion integration

### Changed
- Refactored original script into well-structured Python library
- Improved error messages and user feedback
- Enhanced logging and debugging capabilities

### Fixed
- Better handling of Firefox profile detection across different OS
- Improved LZ4 decompression error handling
- Fixed tab indexing issues

## [1.0.0] - 2024-01-15

### Added
- Initial release of Firefox Tab Extractor
- Core extraction functionality
- Command-line interface
- Python library API
- Support for multiple output formats (JSON, CSV)
- Automatic Firefox profile detection
- Tab metadata extraction (title, URL, access time, pinned status)
- Statistics and analytics features
- Comprehensive documentation and examples
- MIT license

### Features
- Extract tabs from Firefox session data
- Support for multiple Firefox windows
- Domain extraction from URLs
- Timestamp conversion and formatting
- Pinned and hidden tab detection
- Window and tab organization
- Notion-ready CSV export
- Developer-friendly JSON export
- Cross-platform compatibility (macOS, Windows, Linux)
- Snap Firefox support

### Technical
- Type hints throughout the codebase
- Comprehensive error handling with custom exceptions
- Logging system for debugging
- Modular architecture with separate models and extractors
- Test coverage for core functionality
- Modern Python packaging with pyproject.toml
- Development tools configuration (Black, flake8, mypy, pytest)

---

## Version History

### Version 1.0.0
- **Release Date**: January 15, 2024
- **Status**: Initial release
- **Key Features**: Core extraction, CLI, library API, multiple formats
- **Compatibility**: Python 3.7+, Firefox 60+

---

## Migration Guide

### From Original Script to Library

If you were using the original `extract_firefox_tabs.py` script:

**Old way:**
```bash
python3 extract_firefox_tabs.py
```

**New way:**
```bash
# Install the library
pip install firefox-tab-extractor

# Use the CLI
firefox-tab-extractor

# Or use as a library
python -c "
from firefox_tab_extractor import FirefoxTabExtractor
extractor = FirefoxTabExtractor()
tabs = extractor.extract_tabs()
print(f'Found {len(tabs)} tabs')
"
```

---

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

---

## Support

- 📧 **Email**: your.email@example.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/firefox-tab-extractor/issues)
- 📖 **Documentation**: [GitHub Wiki](https://github.com/yourusername/firefox-tab-extractor/wiki)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/firefox-tab-extractor/discussions)
