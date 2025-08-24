"""
Main Firefox Tab Extractor class
"""

import json
import csv
import os
import glob
import lz4.block
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any
import logging

from .models import Tab, Window
from .exceptions import (
    FirefoxProfileNotFoundError,
    SessionDataError,
    LZ4DecompressionError,
    NoTabsFoundError
)


class FirefoxTabExtractor:
    """
    Main class for extracting Firefox browser tabs
    
    This class provides methods to find Firefox profiles, extract tab data,
    and save the results in various formats (JSON, CSV).
    """
    
    def __init__(self, profile_path: Optional[str] = None, log_level: int = logging.INFO):
        """
        Initialize the Firefox Tab Extractor
        
        Args:
            profile_path: Optional path to Firefox profile directory
            log_level: Logging level for the extractor
        """
        self.profile_path = profile_path
        self.recovery_file = None
        self.logger = self._setup_logging(log_level)
        
        if not self.profile_path:
            self.profile_path, self.recovery_file = self._find_firefox_profile()
    
    def _setup_logging(self, log_level: int) -> logging.Logger:
        """Setup logging for the extractor"""
        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _find_firefox_profile(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Find the active Firefox profile directory and recovery file
        
        Returns:
            Tuple of (profile_path, recovery_file_path) or (None, None) if not found
        """
        possible_paths = [
            os.path.expanduser("~/.mozilla/firefox/"),
            os.path.expanduser("~/Library/Application Support/Firefox/Profiles/"),  # macOS
            os.path.expanduser("~/AppData/Roaming/Mozilla/Firefox/Profiles/"),  # Windows
            os.path.expanduser("~/snap/firefox/common/.mozilla/firefox/"),  # Snap Firefox
        ]
        
        for base_path in possible_paths:
            if os.path.exists(base_path):
                self.logger.debug(f"Checking base path: {base_path}")
                
                # Look for profile directories
                profiles = glob.glob(os.path.join(base_path, "*.default*"))
                if not profiles:
                    profiles = [d for d in os.listdir(base_path) 
                               if os.path.isdir(os.path.join(base_path, d)) and not d.startswith('.')]
                
                for profile in profiles:
                    profile_path = os.path.join(base_path, profile) if isinstance(profile, str) else profile
                    recovery_file = os.path.join(profile_path, "sessionstore-backups", "recovery.jsonlz4")
                    
                    if os.path.exists(recovery_file):
                        self.logger.info(f"Found Firefox profile: {profile_path}")
                        return profile_path, recovery_file
        
        self.logger.error("Firefox profile not found")
        return None, None
    
    def _decompress_lz4_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Decompress Firefox's LZ4-compressed session file
        
        Args:
            file_path: Path to the LZ4 compressed file
            
        Returns:
            Parsed JSON data or None if decompression fails
        """
        try:
            with open(file_path, 'rb') as f:
                # Skip the first 8 bytes (magic number)
                f.read(8)
                compressed_data = f.read()
                
            # Decompress the data
            decompressed = lz4.block.decompress(compressed_data)
            return json.loads(decompressed.decode('utf-8'))
            
        except Exception as e:
            self.logger.error(f"Error decompressing file: {e}")
            raise LZ4DecompressionError(f"Failed to decompress {file_path}: {e}")
    
    def _extract_tabs_from_session(self, session_data: Dict[str, Any]) -> List[Tab]:
        """
        Extract tab information from Firefox session data
        
        Args:
            session_data: Parsed session data from Firefox
            
        Returns:
            List of Tab objects
        """
        tabs = []
        
        if 'windows' not in session_data:
            self.logger.warning("No windows found in session data")
            return tabs
        
        for window_idx, window in enumerate(session_data['windows']):
            if 'tabs' not in window:
                continue
                
            for tab_idx, tab in enumerate(window['tabs']):
                if 'entries' not in tab or not tab['entries']:
                    continue
                
                # Get the current entry (active page in tab)
                current_entry_idx = tab.get('index', 1) - 1  # Firefox uses 1-based indexing
                if current_entry_idx >= len(tab['entries']):
                    current_entry_idx = len(tab['entries']) - 1
                
                entry = tab['entries'][current_entry_idx]
                
                tab_obj = Tab(
                    window_index=window_idx + 1,
                    tab_index=tab_idx + 1,
                    title=entry.get('title', 'Untitled'),
                    url=entry.get('url', ''),
                    last_accessed=tab.get('lastAccessed', 0),
                    last_accessed_readable=datetime.fromtimestamp(
                        tab.get('lastAccessed', 0) / 1000
                    ).strftime('%Y-%m-%d %H:%M:%S') if tab.get('lastAccessed') else 'Unknown',
                    pinned=tab.get('pinned', False),
                    hidden=tab.get('hidden', False)
                )
                
                tabs.append(tab_obj)
        
        return tabs
    
    def extract_tabs(self) -> List[Tab]:
        """
        Extract all tabs from Firefox session
        
        Returns:
            List of Tab objects
            
        Raises:
            FirefoxProfileNotFoundError: If Firefox profile cannot be found
            SessionDataError: If session data cannot be read
            NoTabsFoundError: If no tabs are found
        """
        if not self.profile_path or not self.recovery_file:
            raise FirefoxProfileNotFoundError("Firefox profile not found")
        
        self.logger.info("Reading Firefox session data...")
        session_data = self._decompress_lz4_file(self.recovery_file)
        
        if not session_data:
            raise SessionDataError("Failed to read session data")
        
        self.logger.info("Extracting tabs...")
        tabs = self._extract_tabs_from_session(session_data)
        
        if not tabs:
            raise NoTabsFoundError("No tabs found in session data")
        
        self.logger.info(f"Found {len(tabs)} tabs")
        return tabs
    
    def get_windows(self, tabs: List[Tab]) -> List[Window]:
        """
        Group tabs by window
        
        Args:
            tabs: List of Tab objects
            
        Returns:
            List of Window objects
        """
        windows_dict = {}
        
        for tab in tabs:
            if tab.window_index not in windows_dict:
                windows_dict[tab.window_index] = []
            windows_dict[tab.window_index].append(tab)
        
        windows = []
        for window_index, window_tabs in sorted(windows_dict.items()):
            windows.append(Window(window_index=window_index, tabs=window_tabs))
        
        return windows
    
    def save_to_json(self, tabs: List[Tab], output_path: str) -> None:
        """
        Save tabs to JSON file
        
        Args:
            tabs: List of Tab objects
            output_path: Path to output JSON file
        """
        data = {
            'extraction_time': datetime.now().isoformat(),
            'total_tabs': len(tabs),
            'windows': len(set(tab.window_index for tab in tabs)),
            'pinned_tabs': sum(1 for tab in tabs if tab.pinned),
            'hidden_tabs': sum(1 for tab in tabs if tab.hidden),
            'tabs': [tab.to_dict() for tab in tabs]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Saved {len(tabs)} tabs to {output_path}")
    
    def save_to_csv(self, tabs: List[Tab], output_path: str) -> None:
        """
        Save tabs to CSV file (Notion-ready format)
        
        Args:
            tabs: List of Tab objects
            output_path: Path to output CSV file
        """
        if not tabs:
            return
        
        fieldnames = [
            'window_index', 'tab_index', 'title', 'url', 
            'last_accessed_readable', 'pinned', 'hidden', 'domain'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for tab in tabs:
                csv_row = {field: tab.to_dict().get(field, '') for field in fieldnames}
                writer.writerow(csv_row)
        
        self.logger.info(f"Saved {len(tabs)} tabs to {output_path}")
    
    def get_statistics(self, tabs: List[Tab]) -> Dict[str, Any]:
        """
        Get statistics about the extracted tabs
        
        Args:
            tabs: List of Tab objects
            
        Returns:
            Dictionary with statistics
        """
        windows = self.get_windows(tabs)
        
        return {
            'total_tabs': len(tabs),
            'total_windows': len(windows),
            'pinned_tabs': sum(1 for tab in tabs if tab.pinned),
            'hidden_tabs': sum(1 for tab in tabs if tab.hidden),
            'visible_tabs': sum(1 for tab in tabs if not tab.hidden),
            'windows': [window.to_dict() for window in windows],
            'domains': list(set(tab.domain for tab in tabs if tab.domain)),
        }
