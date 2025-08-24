"""
Command-line interface for Firefox Tab Extractor
"""

import argparse
import sys
from datetime import datetime


from .extractor import FirefoxTabExtractor
from .exceptions import (
    FirefoxProfileNotFoundError,
    SessionDataError,
    LZ4DecompressionError,
    NoTabsFoundError,
)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Extract Firefox browser tabs for organization and productivity",  # noqa: E501
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract tabs and save to default files
  firefox-tab-extractor

  # Save to specific files
  firefox-tab-extractor --json my_tabs.json --csv my_tabs.csv

  # Show statistics only
  firefox-tab-extractor --stats-only

  # Verbose output
  firefox-tab-extractor --verbose

  # Specify custom Firefox profile path
  firefox-tab-extractor --profile ~/.mozilla/firefox/abc123.default
        """,
    )

    parser.add_argument(
        "--json",
        "-j",
        help="Output JSON file path (default: firefox_tabs_YYYYMMDD_HHMMSS.json)",  # noqa: E501
    )

    parser.add_argument(
        "--csv",
        "-c",
        help="Output CSV file path (default: firefox_tabs_YYYYMMDD_HHMMSS.csv)",  # noqa: E501
    )

    parser.add_argument("--profile", "-p", help="Custom Firefox profile path")

    parser.add_argument(
        "--stats-only",
        "-s",
        action="store_true",
        help="Show statistics only, don't save files",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    parser.add_argument(
        "--preview",
        "-P",
        type=int,
        default=5,
        help="Number of tabs to preview (default: 5, use 0 to disable)",
    )

    args = parser.parse_args()

    # Setup logging level
    log_level = "DEBUG" if args.verbose else "INFO"

    try:
        # Initialize extractor
        extractor = FirefoxTabExtractor(
            profile_path=args.profile,
            log_level=getattr(sys.modules["logging"], log_level),
        )

        print("🔥 Firefox Tab Extractor")
        print("=" * 50)

        # Extract tabs
        tabs = extractor.extract_tabs()

        # Get statistics
        stats = extractor.get_statistics(tabs)

        # Display summary
        print("\n📊 Summary:")
        print("  • Total tabs: {stats['total_tabs']}")
        print("  • Windows: {stats['total_windows']}")
        print("  • Pinned tabs: {stats['pinned_tabs']}")
        print("  • Hidden tabs: {stats['hidden_tabs']}")
        print("  • Visible tabs: {stats['visible_tabs']}")

        # Show preview
        if args.preview > 0:
            print("\n🔍 Preview of first {min(args.preview, len(tabs))} tabs:")
            for i, tab in enumerate(tabs[: args.preview]):
                print(
                    "  {i+1}. {tab.title[:60]}{'...' if len(tab.title) > 60 else ''}"  # noqa: E501
                )
                print(
                    "     URL: {tab.url[:80]}{'...' if len(tab.url) > 80 else ''}"
                )  # noqa: E501
                print("     Window: {tab.window_index}, Tab: {tab.tab_index}")
                if tab.pinned:
                    print("     📌 Pinned")
                print()

        # Show domain statistics
        if stats["domains"]:
            print("🌐 Top domains:")
            domain_counts = {}
            for tab in tabs:
                if tab.domain:
                    domain_counts[tab.domain] = (
                        domain_counts.get(tab.domain, 0) + 1
                    )  # noqa: E501

            sorted_domains = sorted(
                domain_counts.items(), key=lambda x: x[1], reverse=True
            )
            for domain, count in sorted_domains[:5]:
                print("  • {domain}: {count} tabs")

        if args.stats_only:
            return

        # Generate default filenames if not provided
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # noqa: F841

        if not args.json:
            args.json = "firefox_tabs_{timestamp}.json"

        if not args.csv:
            args.csv = "firefox_tabs_{timestamp}.csv"

        # Save files
        print("\n💾 Saving files...")

        if args.json:
            extractor.save_to_json(tabs, args.json)
            print("  ✅ JSON: {args.json}")

        if args.csv:
            extractor.save_to_csv(tabs, args.csv)
            print("  ✅ CSV: {args.csv}")

        print("\n🎉 Extraction completed successfully!")
        print("📁 Files created:")
        if args.json:
            print("  • {args.json} (for programmatic use)")
        if args.csv:
            print("  • {args.csv} (for Notion import)")

    except FirefoxProfileNotFoundError:
        print("❌ Firefox profile not found!")
        print("Make sure Firefox is installed and has been run at least once.")
        print("\nCommon solutions:")
        print("  • Run Firefox at least once to create profile")
        print("  • Check if Firefox is installed via snap: snap list firefox")
        print("  • Use --profile to specify custom profile path")
        sys.exit(1)

    except SessionDataError as e:
        print("❌ Failed to read session data: {e}")
        print("Try closing and reopening Firefox to refresh session data.")
        sys.exit(1)

    except LZ4DecompressionError as e:
        print("❌ Failed to decompress session file: {e}")
        print("This might happen if Firefox is currently running.")
        print("Try closing Firefox and running the extractor again.")
        sys.exit(1)

    except NoTabsFoundError:
        print("❌ No tabs found in session data")
        print("Make sure Firefox has active tabs open.")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⏹️  Extraction cancelled by user")
        sys.exit(1)

    except Exception:  # noqa: F841
        print("❌ Unexpected error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
