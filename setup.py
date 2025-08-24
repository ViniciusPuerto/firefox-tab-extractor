from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="firefox-tab-extractor",
    version="1.0.0",
    author="Vinicius Porto",
    author_email="your.email@example.com",
    description="A Python library to extract and organize Firefox browser tabs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/firefox-tab-extractor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "lz4>=3.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "firefox-tab-extractor=firefox_tab_extractor.cli:main",
        ],
    },
    keywords="firefox, browser, tabs, extraction, organization, productivity",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/firefox-tab-extractor/issues",
        "Source": "https://github.com/yourusername/firefox-tab-extractor",
        "Documentation": "https://github.com/yourusername/firefox-tab-extractor#readme",
    },
)
