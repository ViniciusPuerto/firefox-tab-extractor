# Firefox Tab Extractor 🔥

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/firefox-tab-extractor.svg)](https://badge.fury.io/py/firefox-tab-extractor)

A powerful Python library to extract and organize Firefox browser tabs for productivity, study organization, and workflow management.

## 🎯 Why Firefox Tab Extractor?

**Tired of losing track of important tabs?** This library helps you:

- 📚 **Organize study materials** - Extract all your research tabs into structured formats
- 📊 **Productivity tracking** - See which sites you visit most and optimize your workflow
- 🔄 **Session backup** - Save your browsing sessions before major cleanup
- 📋 **Notion integration** - Export tabs directly to Notion for task management
- 🎓 **Learning management** - Create structured study schedules from your open tabs

## ✨ Features

- 🔍 **Smart profile detection** - Automatically finds Firefox profiles across different OS
- 📁 **Multiple output formats** - JSON for developers, CSV for Notion/Excel
- 🏷️ **Rich metadata** - Tab titles, URLs, access times, pinned status, domains
- 📊 **Statistics & analytics** - Get insights about your browsing patterns
- 🛠️ **Developer-friendly** - Clean API, type hints, comprehensive error handling
- 🚀 **CLI & Library** - Use as command-line tool or import in your Python code

## 🚀 Quick Start

### Installation

```bash
pip install firefox-tab-extractor
```

### Command Line Usage

```bash
# Extract all tabs to default files
firefox-tab-extractor

# Save to specific files
firefox-tab-extractor --json my_tabs.json --csv my_tabs.csv

# Show statistics only
firefox-tab-extractor --stats-only

# Verbose output with preview
firefox-tab-extractor --verbose --preview 10
```

### Python Library Usage

```python
from firefox_tab_extractor import FirefoxTabExtractor

# Initialize extractor
extractor = FirefoxTabExtractor()

# Extract tabs
tabs = extractor.extract_tabs()

# Get statistics
stats = extractor.get_statistics(tabs)
print(f"Found {stats['total_tabs']} tabs across {stats['total_windows']} windows")

# Save to files
extractor.save_to_json(tabs, "my_tabs.json")
extractor.save_to_csv(tabs, "my_tabs.csv")

# Group by windows
windows = extractor.get_windows(tabs)
for window in windows:
    print(f"Window {window.window_index}: {window.tab_count} tabs")
```

## 📊 Output Formats

### JSON Output
```json
{
  "extraction_time": "2024-01-15T10:30:00",
  "total_tabs": 25,
  "windows": 3,
  "pinned_tabs": 5,
  "hidden_tabs": 2,
  "tabs": [
    {
      "window_index": 1,
      "tab_index": 1,
      "title": "GitHub - Your Repository",
      "url": "https://github.com/username/repo",
      "last_accessed": 1705312200000,
      "last_accessed_readable": "2024-01-15 10:30:00",
      "pinned": true,
      "hidden": false,
      "domain": "github.com"
    }
  ]
}
```

### CSV Output (Notion-ready)
```csv
window_index,tab_index,title,url,last_accessed_readable,pinned,hidden,domain
1,1,GitHub - Your Repository,https://github.com/username/repo,2024-01-15 10:30:00,true,false,github.com
```

## 🎓 Study Organization Workflow

### 1. Extract Your Tabs
```bash
firefox-tab-extractor --csv study_materials.csv
```

### 2. Import to Notion
1. Create a new Notion database
2. Import the CSV file
3. Add custom properties:
   - **Category** (JavaScript, Python, System Design, etc.)
   - **Priority** (High, Medium, Low)
   - **Estimated Reading Time** (15min, 30min, 1hr)
   - **Status** (Not Started, In Progress, Completed)
   - **Study Day** (Monday, Wednesday, Friday, Weekend)

### 3. Create Study Schedule
```
Monday (1 hour):
- 1 book chapter (30 min)
- 2-3 short articles (30 min)

Wednesday (1 hour):
- 1 book chapter (30 min)
- 1 long technical article (30 min)

Friday (1 hour):
- 1 book chapter (30 min)
- Practice problems/coding (30 min)

Weekend (2 hours):
- 1 book chapter (30 min)
- 2-3 comprehensive tutorials (90 min)
```

## 🛠️ Advanced Usage

### Custom Firefox Profile
```python
extractor = FirefoxTabExtractor(profile_path="~/.mozilla/firefox/custom.profile")
```

### Filtering and Analysis
```python
# Get only pinned tabs
pinned_tabs = [tab for tab in tabs if tab.pinned]

# Get tabs by domain
github_tabs = [tab for tab in tabs if tab.domain == "github.com"]

# Get recently accessed tabs
from datetime import datetime, timedelta
recent_tabs = [
    tab for tab in tabs 
    if tab.last_accessed_datetime > datetime.now() - timedelta(days=7)
]
```

### Error Handling
```python
from firefox_tab_extractor import FirefoxTabExtractor
from firefox_tab_extractor.exceptions import FirefoxProfileNotFoundError

try:
    extractor = FirefoxTabExtractor()
    tabs = extractor.extract_tabs()
except FirefoxProfileNotFoundError:
    print("Firefox profile not found. Make sure Firefox is installed.")
```

## 🔧 Troubleshooting

### Firefox Profile Not Found
- Make sure Firefox has been run at least once
- Check if Firefox is installed via snap: `snap list firefox`
- Use `--profile` to specify custom profile path

### Permission Issues
- Ensure you have read access to Firefox profile directory
- On some systems, you might need to close Firefox first

### No Tabs Found
- Ensure Firefox has active tabs open
- Try closing and reopening Firefox to refresh session data
- Check if Firefox is in private browsing mode (private tabs aren't saved)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 Reporting Bugs
- Use the [GitHub issue tracker](https://github.com/ViniciusPuerto/firefox-tab-extractor/issues)
- Include your OS, Firefox version, and Python version
- Provide error messages and steps to reproduce

### 💡 Feature Requests
- Open an issue with the "enhancement" label
- Describe the feature and its use case
- Consider contributing the implementation

### 🔧 Development Setup
```bash
# Clone the repository
git clone https://github.com/ViniciusPuerto/firefox-tab-extractor.git
cd firefox-tab-extractor

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black firefox_tab_extractor/

# Type checking
mypy firefox_tab_extractor/
```

### 📝 Code Style
- Follow PEP 8 style guidelines
- Use type hints for all functions
- Add docstrings for all public methods
- Write tests for new features

## 🚀 Roadmap

### Planned Features
- [ ] **Chrome/Edge support** - Extract tabs from other browsers
- [ ] **Tab categorization** - AI-powered content classification
- [ ] **Reading time estimation** - Based on content analysis
- [ ] **Duplicate detection** - Find and merge similar tabs
- [ ] **Scheduled extraction** - Automatically extract tabs at intervals
- [ ] **Web interface** - Browser-based tab management
- [ ] **Cloud sync** - Backup and sync across devices
- [ ] **Tab analytics** - Detailed browsing pattern analysis

### Integration Ideas
- [ ] **Notion API** - Direct integration with Notion
- [ ] **Obsidian** - Export to Obsidian vault
- [ ] **Roam Research** - Integration with Roam
- [ ] **Todoist** - Create tasks from tabs
- [ ] **Slack** - Share tab collections with teams

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Firefox** - For providing an accessible session storage format
- **LZ4** - For the compression library used by Firefox
- **Python community** - For the excellent ecosystem of tools and libraries

## 📞 Support

- 📧 **Email**: vinicius.alves.porto@gmail.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/ViniciusPuerto/firefox-tab-extractor/issues)
- 📖 **Documentation**: [GitHub Wiki](https://github.com/ViniciusPuerto/firefox-tab-extractor/wiki)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/ViniciusPuerto/firefox-tab-extractor/discussions)

---

**Made with ❤️ for the productivity community**

If this project helps you organize your digital life, consider giving it a ⭐ on GitHub!
