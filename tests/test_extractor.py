"""
Tests for Firefox Tab Extractor
"""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from datetime import datetime
import json

from firefox_tab_extractor import FirefoxTabExtractor
from firefox_tab_extractor.models import Tab, Window
from firefox_tab_extractor.exceptions import (
    FirefoxProfileNotFoundError,
    SessionDataError,
    LZ4DecompressionError,
    NoTabsFoundError
)


class TestTab:
    """Test Tab model"""
    
    def test_tab_creation(self):
        """Test creating a Tab object"""
        tab = Tab(
            window_index=1,
            tab_index=1,
            title="Test Tab",
            url="https://example.com",
            last_accessed=1705312200000,
            last_accessed_readable="2024-01-15 10:30:00",
            pinned=False,
            hidden=False
        )
        
        assert tab.window_index == 1
        assert tab.tab_index == 1
        assert tab.title == "Test Tab"
        assert tab.url == "https://example.com"
        assert tab.domain == "example.com"
        assert not tab.pinned
        assert not tab.hidden
    
    def test_tab_domain_extraction(self):
        """Test domain extraction from URL"""
        tab = Tab(
            window_index=1,
            tab_index=1,
            title="Test",
            url="https://github.com/user/repo",
            last_accessed=0,
            last_accessed_readable="",
            pinned=False,
            hidden=False
        )
        
        assert tab.domain == "github.com"
    
    def test_tab_to_dict(self):
        """Test converting tab to dictionary"""
        tab = Tab(
            window_index=1,
            tab_index=1,
            title="Test Tab",
            url="https://example.com",
            last_accessed=1705312200000,
            last_accessed_readable="2024-01-15 10:30:00",
            pinned=True,
            hidden=False
        )
        
        tab_dict = tab.to_dict()
        
        assert tab_dict['window_index'] == 1
        assert tab_dict['title'] == "Test Tab"
        assert tab_dict['pinned'] is True
        assert tab_dict['domain'] == "example.com"


class TestWindow:
    """Test Window model"""
    
    def test_window_creation(self):
        """Test creating a Window object"""
        tabs = [
            Tab(1, 1, "Tab 1", "https://example1.com", 0, "", False, False),
            Tab(1, 2, "Tab 2", "https://example2.com", 0, "", True, False),
        ]
        
        window = Window(window_index=1, tabs=tabs)
        
        assert window.window_index == 1
        assert window.tab_count == 2
        assert len(window.pinned_tabs) == 1
        assert len(window.visible_tabs) == 2
    
    def test_window_to_dict(self):
        """Test converting window to dictionary"""
        tabs = [
            Tab(1, 1, "Tab 1", "https://example1.com", 0, "", False, False),
            Tab(1, 2, "Tab 2", "https://example2.com", 0, "", True, False),
        ]
        
        window = Window(window_index=1, tabs=tabs)
        window_dict = window.to_dict()
        
        assert window_dict['window_index'] == 1
        assert window_dict['tab_count'] == 2
        assert window_dict['pinned_tab_count'] == 1
        assert window_dict['visible_tab_count'] == 2


class TestFirefoxTabExtractor:
    """Test FirefoxTabExtractor class"""
    
    def test_extractor_initialization(self):
        """Test extractor initialization"""
        extractor = FirefoxTabExtractor()
        assert extractor.profile_path is None
        assert extractor.recovery_file is None
    
    @patch('firefox_tab_extractor.extractor.os.path.exists')
    @patch('firefox_tab_extractor.extractor.glob.glob')
    def test_find_firefox_profile_success(self, mock_glob, mock_exists):
        """Test successful Firefox profile detection"""
        mock_exists.return_value = True
        mock_glob.return_value = ["/path/to/profile.default"]
        
        with patch('os.path.join') as mock_join:
            mock_join.return_value = "/path/to/profile.default/sessionstore-backups/recovery.jsonlz4"
            
            extractor = FirefoxTabExtractor()
            profile_path, recovery_file = extractor._find_firefox_profile()
            
            assert profile_path == "/path/to/profile.default"
            assert recovery_file == "/path/to/profile.default/sessionstore-backups/recovery.jsonlz4"
    
    @patch('firefox_tab_extractor.extractor.os.path.exists')
    def test_find_firefox_profile_not_found(self, mock_exists):
        """Test Firefox profile not found"""
        mock_exists.return_value = False
        
        extractor = FirefoxTabExtractor()
        profile_path, recovery_file = extractor._find_firefox_profile()
        
        assert profile_path is None
        assert recovery_file is None
    
    def test_extract_tabs_from_session(self):
        """Test extracting tabs from session data"""
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
    
    def test_get_windows(self):
        """Test grouping tabs by windows"""
        tabs = [
            Tab(1, 1, "Tab 1", "https://example1.com", 0, "", False, False),
            Tab(1, 2, "Tab 2", "https://example2.com", 0, "", False, False),
            Tab(2, 1, "Tab 3", "https://example3.com", 0, "", False, False),
        ]
        
        extractor = FirefoxTabExtractor()
        windows = extractor.get_windows(tabs)
        
        assert len(windows) == 2
        assert windows[0].window_index == 1
        assert windows[0].tab_count == 2
        assert windows[1].window_index == 2
        assert windows[1].tab_count == 1
    
    def test_get_statistics(self):
        """Test getting statistics from tabs"""
        tabs = [
            Tab(1, 1, "Tab 1", "https://example1.com", 0, "", False, False),
            Tab(1, 2, "Tab 2", "https://example2.com", 0, "", True, False),
            Tab(2, 1, "Tab 3", "https://example3.com", 0, "", False, True),
        ]
        
        extractor = FirefoxTabExtractor()
        stats = extractor.get_statistics(tabs)
        
        assert stats['total_tabs'] == 3
        assert stats['total_windows'] == 2
        assert stats['pinned_tabs'] == 1
        assert stats['hidden_tabs'] == 1
        assert stats['visible_tabs'] == 2
    
    def test_save_to_json(self):
        """Test saving tabs to JSON file"""
        tabs = [
            Tab(1, 1, "Test Tab", "https://example.com", 0, "", False, False),
        ]
        
        extractor = FirefoxTabExtractor()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            extractor.save_to_json(tabs, temp_file)
            
            # Verify file was created and contains expected data
            assert os.path.exists(temp_file)
            
            with open(temp_file, 'r') as f:
                data = json.loads(f.read())
            
            assert data['total_tabs'] == 1
            assert len(data['tabs']) == 1
            assert data['tabs'][0]['title'] == 'Test Tab'
            
        finally:
            os.unlink(temp_file)
    
    def test_save_to_csv(self):
        """Test saving tabs to CSV file"""
        tabs = [
            Tab(1, 1, "Test Tab", "https://example.com", 0, "", False, False),
        ]
        
        extractor = FirefoxTabExtractor()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            extractor.save_to_csv(tabs, temp_file)
            
            # Verify file was created
            assert os.path.exists(temp_file)
            
            with open(temp_file, 'r') as f:
                content = f.read()
            
            assert 'window_index,tab_index,title,url' in content
            assert 'Test Tab' in content
            
        finally:
            os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__])
