"""
Firefox Tab Extractor

A Python library to extract and organize Firefox browser tabs for productivity and study organization.  # noqa: E501
"""

__version__ = "1.0.0"
__author__ = "Vinicius Porto"
__email__ = "vinicius.alves.porto@gmail.com"

from .extractor import FirefoxTabExtractor
from .models import Tab, Window
from .exceptions import FirefoxProfileNotFoundError, SessionDataError

__all__ = [
    "FirefoxTabExtractor",
    "Tab",
    "Window",
    "FirefoxProfileNotFoundError",
    "SessionDataError",
]
