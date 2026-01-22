"""Command-line entrypoint for the Google Search Titles Scraper."""

import argparse
import sys

from selenium.common.exceptions import WebDriverException

from .batch import load_queries, run_batch
from .driver import build_driver
from .exporters import save_results
from .scrape import scrape


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape titles + URLs from Google search results."
    )
    query_group = parser.add_mutually_exclusive_group(required=True)
    query_group.add_argument("query", nargs="?", help="Search query to run on Google")
    query_group.add_argument(
        "--queries-file",
        help="Path to a text file with one query per line (batch mode)",
    )
    parser.add_argument(
        "-p", "--pages", type=int, default=1,
        help="Max result pages per query (default: 1)",
    )
    parser.add_argument(
        "-o", "--output", default=None,
        help="Output file in single-query mode (default: Google_titles_Url_Scraped.<format>), "
             "or output directory in batch mode (default: scraped_output/)",
    )
    parser.add_argument(
        "-f", "--format", choices=["xlsx", "csv", "json"], default="xlsx",
        help="Output format (default: xlsx)",
    )
    parser.add_argument(
        "--driver-path", default=None,
        help="Explicit path to a chromedriver binary. If omitted, webdriver-manager "
             "will download/manage one automatically (if installed).",
    )
    parser.add_argument(
        "--headless", action="store_true",
        help="Run Chrome without opening a visible browser window",
    )
    parser.add_argument(
        "--wait", type=float, default=20,
        help="Seconds to wait for page elements before giving up (default: 20)",
    )
    return parser.parse_args(argv)


def main(argv=None) -> None:
    args = parse_args(argv)

    if args.queries_file:
        queries = load_queries(args.queries_file)
        if not queries:
            print(f"No queries found in '{args.queries_file}'.")
            sys.exit(1)
        run_batch(queries, args, args.output or "scraped_output")
        return

    try:
        driver = build_driver(args.driver_path, args.headless)
    except WebDriverException as e:
        print(
            "Failed to start Chrome/ChromeDriver. Make sure Google Chrome is "
            "installed, and either install 'webdriver-manager' "
            "(pip install webdriver-manager) or pass --driver-path explicitly.\n"
            f"Original error: {e}"
        )
        sys.exit(1)

    try:
        titles, urls = scrape(driver, args.query, args.pages, args.wait)
    finally:
        driver.quit()

    if not titles:
        print("No results were scraped.")
        sys.exit(1)

    output_path = args.output or f"Google_titles_Url_Scraped.{args.format}"
    save_results(titles, urls, output_path, args.format)


if __name__ == "__main__":
    main()
