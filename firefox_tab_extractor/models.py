"""
Data models for Firefox Tab Extractor
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Tab:
    """Represents a Firefox tab with all its metadata"""

    window_index: int
    tab_index: int
    title: str
    url: str
    last_accessed: int  # Unix timestamp in milliseconds
    last_accessed_readable: str
    pinned: bool
    hidden: bool

    @property
    def last_accessed_datetime(self) -> datetime:
        """Convert last_accessed timestamp to datetime object"""
        return datetime.fromtimestamp(self.last_accessed / 1000)

    @property
    def domain(self) -> str:
        """Extract domain from URL"""
        from urllib.parse import urlparse

        try:
            parsed = urlparse(self.url)
            return parsed.netloc
        except Exception:
            return ""

    def to_dict(self) -> dict:
        """Convert tab to dictionary"""
        return {
            "window_index": self.window_index,
            "tab_index": self.tab_index,
            "title": self.title,
            "url": self.url,
            "last_accessed": self.last_accessed,
            "last_accessed_readable": self.last_accessed_readable,
            "pinned": self.pinned,
            "hidden": self.hidden,
            "domain": self.domain,
        }


@dataclass
class Window:
    """Represents a Firefox window with its tabs"""

    window_index: int
    tabs: List[Tab]

    @property
    def tab_count(self) -> int:
        """Number of tabs in this window"""
        return len(self.tabs)

    @property
    def pinned_tabs(self) -> List[Tab]:
        """Get all pinned tabs in this window"""
        return [tab for tab in self.tabs if tab.pinned]

    @property
    def visible_tabs(self) -> List[Tab]:
        """Get all visible (non-hidden) tabs in this window"""
        return [tab for tab in self.tabs if not tab.hidden]

    def to_dict(self) -> dict:
        """Convert window to dictionary"""
        return {
            "window_index": self.window_index,
            "tab_count": self.tab_count,
            "pinned_tab_count": len(self.pinned_tabs),
            "visible_tab_count": len(self.visible_tabs),
            "tabs": [tab.to_dict() for tab in self.tabs],
        }
