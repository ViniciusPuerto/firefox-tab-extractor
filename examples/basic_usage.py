#!/usr/bin/env python3
"""
Basic usage example for Firefox Tab Extractor

This example demonstrates how to use the library to extract tabs
and perform basic analysis.
"""

from firefox_tab_extractor import FirefoxTabExtractor
from datetime import datetime, timedelta


def main():
    """Basic usage example"""
    print("🔥 Firefox Tab Extractor - Basic Usage Example")
    print("=" * 50)
    
    # Initialize the extractor
    extractor = FirefoxTabExtractor()
    
    try:
        # Extract all tabs
        print("📖 Extracting tabs from Firefox...")
        tabs = extractor.extract_tabs()
        
        # Get statistics
        stats = extractor.get_statistics(tabs)
        
        print(f"\n📊 Found {stats['total_tabs']} tabs across {stats['total_windows']} windows")
        print(f"   • Pinned tabs: {stats['pinned_tabs']}")
        print(f"   • Hidden tabs: {stats['hidden_tabs']}")
        print(f"   • Visible tabs: {stats['visible_tabs']}")
        
        # Show tabs by window
        windows = extractor.get_windows(tabs)
        print(f"\n🪟 Windows breakdown:")
        for window in windows:
            print(f"   Window {window.window_index}: {window.tab_count} tabs")
            if window.pinned_tabs:
                print(f"     📌 Pinned: {len(window.pinned_tabs)}")
        
        # Show domain statistics
        if stats['domains']:
            print(f"\n🌐 Top domains:")
            domain_counts = {}
            for tab in tabs:
                if tab.domain:
                    domain_counts[tab.domain] = domain_counts.get(tab.domain, 0) + 1
            
            sorted_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)
            for domain, count in sorted_domains[:5]:
                print(f"   • {domain}: {count} tabs")
        
        # Show recent tabs (accessed in last 7 days)
        print(f"\n🕒 Recently accessed tabs (last 7 days):")
        week_ago = datetime.now() - timedelta(days=7)
        recent_tabs = [
            tab for tab in tabs 
            if tab.last_accessed_datetime > week_ago
        ]
        
        for i, tab in enumerate(recent_tabs[:5]):
            print(f"   {i+1}. {tab.title[:50]}{'...' if len(tab.title) > 50 else ''}")
            print(f"      {tab.url[:60]}{'...' if len(tab.url) > 60 else ''}")
        
        # Show pinned tabs
        pinned_tabs = [tab for tab in tabs if tab.pinned]
        if pinned_tabs:
            print(f"\n📌 Pinned tabs:")
            for i, tab in enumerate(pinned_tabs):
                print(f"   {i+1}. {tab.title[:50]}{'...' if len(tab.title) > 50 else ''}")
        
        # Save to files
        print(f"\n💾 Saving to files...")
        extractor.save_to_json(tabs, "example_tabs.json")
        extractor.save_to_csv(tabs, "example_tabs.csv")
        print("   ✅ example_tabs.json (for programmatic use)")
        print("   ✅ example_tabs.csv (for Notion import)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure Firefox is installed and has been run at least once.")


if __name__ == "__main__":
    main()
