#!/usr/bin/env python3
"""
Notion Integration Example for Firefox Tab Extractor

This example shows how to prepare tab data for import into Notion
with additional categorization and study planning features.
"""

import csv
from datetime import datetime, timedelta
from firefox_tab_extractor import FirefoxTabExtractor


def categorize_tab(tab):
    """
    Categorize tabs based on domain and title
    This is a simple example - you can make this more sophisticated
    """
    domain = tab.domain.lower()
    title = tab.title.lower()
    
    # Programming and development
    if any(keyword in domain for keyword in ['github.com', 'gitlab.com', 'stackoverflow.com']):
        return 'Development'
    if any(keyword in title for keyword in ['python', 'javascript', 'react', 'vue', 'node']):
        return 'Programming'
    
    # Documentation and learning
    if any(keyword in domain for keyword in ['docs.', 'developer.', 'learn.', 'tutorial']):
        return 'Documentation'
    if any(keyword in title for keyword in ['tutorial', 'guide', 'documentation', 'learn']):
        return 'Learning'
    
    # News and articles
    if any(keyword in domain for keyword in ['medium.com', 'dev.to', 'hashnode.dev']):
        return 'Articles'
    if any(keyword in title for keyword in ['news', 'article', 'blog']):
        return 'Articles'
    
    # Social media
    if any(keyword in domain for keyword in ['twitter.com', 'linkedin.com', 'reddit.com']):
        return 'Social Media'
    
    # Default category
    return 'Other'


def estimate_reading_time(tab):
    """
    Estimate reading time based on domain and content type
    This is a simple heuristic - you can make this more sophisticated
    """
    domain = tab.domain.lower()
    title = tab.title.lower()
    
    # Documentation and guides (longer reads)
    if any(keyword in domain for keyword in ['docs.', 'developer.']):
        return 30
    if any(keyword in title for keyword in ['tutorial', 'guide', 'complete guide']):
        return 45
    
    # Articles and blog posts
    if any(keyword in domain for keyword in ['medium.com', 'dev.to']):
        return 15
    
    # GitHub repositories (quick browse)
    if 'github.com' in domain:
        return 10
    
    # Default reading time
    return 5


def get_priority(tab):
    """
    Determine priority based on various factors
    """
    # Pinned tabs are high priority
    if tab.pinned:
        return 'High'
    
    # Recently accessed tabs are medium priority
    week_ago = datetime.now() - timedelta(days=7)
    if tab.last_accessed_datetime > week_ago:
        return 'Medium'
    
    # Older tabs are low priority
    return 'Low'


def suggest_study_day(tab):
    """
    Suggest which day to study this content
    """
    category = categorize_tab(tab)
    
    # Programming and development on weekdays
    if category in ['Programming', 'Development']:
        return 'Weekday'
    
    # Documentation and learning on weekends
    if category in ['Documentation', 'Learning']:
        return 'Weekend'
    
    # Articles can be read anytime
    if category == 'Articles':
        return 'Any Day'
    
    # Default
    return 'Weekday'


def create_notion_ready_csv(tabs, output_file):
    """
    Create a CSV file optimized for Notion import with additional columns
    """
    fieldnames = [
        'Title',  # Notion will use this as the main title
        'URL',
        'Category',
        'Priority',
        'Reading Time (minutes)',
        'Study Day',
        'Status',
        'Window',
        'Tab Position',
        'Last Accessed',
        'Pinned',
        'Domain',
        'Notes'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for tab in tabs:
            row = {
                'Title': tab.title,
                'URL': tab.url,
                'Category': categorize_tab(tab),
                'Priority': get_priority(tab),
                'Reading Time (minutes)': estimate_reading_time(tab),
                'Study Day': suggest_study_day(tab),
                'Status': 'Not Started',
                'Window': tab.window_index,
                'Tab Position': tab.tab_index,
                'Last Accessed': tab.last_accessed_readable,
                'Pinned': 'Yes' if tab.pinned else 'No',
                'Domain': tab.domain,
                'Notes': ''  # User can fill this in Notion
            }
            writer.writerow(row)


def main():
    """Notion integration example"""
    print("📋 Firefox Tab Extractor - Notion Integration Example")
    print("=" * 60)
    
    # Initialize the extractor
    extractor = FirefoxTabExtractor()
    
    try:
        # Extract tabs
        print("📖 Extracting tabs from Firefox...")
        tabs = extractor.extract_tabs()
        
        print(f"✅ Found {len(tabs)} tabs")
        
        # Create Notion-ready CSV
        output_file = "notion_study_materials.csv"
        print(f"📝 Creating Notion-ready CSV: {output_file}")
        create_notion_ready_csv(tabs, output_file)
        
        # Show categorization summary
        print(f"\n📊 Categorization Summary:")
        categories = {}
        for tab in tabs:
            category = categorize_tab(tab)
            categories[category] = categories.get(category, 0) + 1
        
        for category, count in sorted(categories.items()):
            print(f"   • {category}: {count} tabs")
        
        # Show priority distribution
        print(f"\n🎯 Priority Distribution:")
        priorities = {}
        for tab in tabs:
            priority = get_priority(tab)
            priorities[priority] = priorities.get(priority, 0) + 1
        
        for priority, count in sorted(priorities.items()):
            print(f"   • {priority}: {count} tabs")
        
        # Show study day suggestions
        print(f"\n📅 Study Day Suggestions:")
        study_days = {}
        for tab in tabs:
            study_day = suggest_study_day(tab)
            study_days[study_day] = study_days.get(study_day, 0) + 1
        
        for day, count in sorted(study_days.items()):
            print(f"   • {day}: {count} tabs")
        
        # Calculate total reading time
        total_time = sum(estimate_reading_time(tab) for tab in tabs)
        print(f"\n⏱️  Total estimated reading time: {total_time} minutes ({total_time/60:.1f} hours)")
        
        print(f"\n✅ Notion-ready CSV created: {output_file}")
        print("\n📋 Next steps:")
        print("1. Open Notion and create a new database")
        print("2. Import the CSV file")
        print("3. Customize the properties as needed")
        print("4. Start organizing your study materials!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure Firefox is installed and has been run at least once.")


if __name__ == "__main__":
    main()
