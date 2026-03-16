"""
Google Search Titles Scraper — entrypoint.

Implementation lives in scraper_lib/. This file exists so the original
`python Selenium_scrapper.py "query"` usage keeps working.

Usage:
    python Selenium_scrapper.py "your search query"
    python Selenium_scrapper.py "your search query" --pages 3 --headless -f csv
    python Selenium_scrapper.py --queries-file queries.txt -f json

Run `python Selenium_scrapper.py --help` for all options.
"""

from scraper_lib.cli import main

if __name__ == "__main__":
    main()


# NOTE: thin wrapper around scraper_lib.cli for backward-compatible invocation.
