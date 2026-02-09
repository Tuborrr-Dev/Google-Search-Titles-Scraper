# Google Search Titles Scraper

![CI](https://github.com/Tuborrr-Dev/Google-Search-Titles-Scraper/actions/workflows/ci.yml/badge.svg)

Uses Selenium to scrape the titles and URLs of Google search results for a
given query (or a batch of queries), and writes them out to xlsx, CSV, or
JSON.

## Description

- 🔍 Sends one search query, or a whole file of queries, to Google
- 📄 Collects the title and URL of each organic result, across as many
  result pages as you want
- 💾 Exports to `.xlsx`, `.csv`, or `.json`
- 🕵️ Basic anti-detection: rotating user-agents, randomized human-like
  delays, and a patched `navigator.webdriver` flag
- ✅ Unit-tested, linted, and checked on every push via GitHub Actions

## Setup

1. **Install Python 3.11+** and clone this repo.
2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Install Google Chrome.** ChromeDriver is managed automatically via
   [`webdriver-manager`](https://pypi.org/project/webdriver-manager/) — no
   manual download needed.

For running tests/lint locally, install the dev extras instead:

```bash
pip install -r requirements-dev.txt
pytest
ruff check .
```

## Usage

**Single query:**

```bash
python Selenium_scrapper.py "your search query"
```

**Batch mode** — scrape a whole list of queries from a file (one per line,
`#` for comments):

```bash
python Selenium_scrapper.py --queries-file sample_queries.txt -f json
```

Each query in batch mode is saved to its own file inside the output
directory (default `scraped_output/`), named after the query.

### Options

| Flag | Description |
|---|---|
| `query` | Search query (omit if using `--queries-file`) |
| `--queries-file FILE` | Batch mode: one query per line |
| `-p`, `--pages N` | Result pages per query (default: 1) |
| `-f`, `--format {xlsx,csv,json}` | Output format (default: xlsx) |
| `-o`, `--output PATH` | Output file (single mode) or directory (batch mode) |
| `--headless` | Run without a visible browser window |
| `--driver-path PATH` | Use a specific chromedriver instead of auto-managing one |
| `--wait SECONDS` | How long to wait for page elements (default: 20) |

Example — scrape 3 pages headlessly, save as CSV:

```bash
python Selenium_scrapper.py "python web scraping" --pages 3 --headless -f csv -o results.csv
```

## Project Structure

```
Selenium_scrapper.py     # thin CLI entrypoint
scraper_lib/
  cli.py                 # argument parsing, main()
  driver.py              # Chrome WebDriver setup + user-agent rotation
  stealth.py             # human-like delay/typing helpers
  captcha.py             # CAPTCHA / "unusual traffic" detection
  scrape.py              # core scraping logic
  exporters.py           # xlsx/csv/json export
  batch.py               # multi-query batch mode
tests/                    # pytest unit tests (no live browser required)
.github/workflows/ci.yml  # lint + test on every push
```

## Limitations

- Google actively detects and blocks automated browsers. The anti-detection
  measures here (user-agent rotation, randomized delays, patched
  `navigator.webdriver`) reduce how quickly you get flagged — they don't
  eliminate CAPTCHAs on repeated or high-volume runs. The scraper detects a
  CAPTCHA page and stops cleanly rather than crashing.
- Google's HTML/CSS class names (e.g. `MjjYud`, `LC20lb`) are undocumented
  and change periodically. If the scraper suddenly returns nothing, that's
  the first place to check.
- Scraping Google's search results pages is against Google's Terms of
  Service. This project is for educational purposes only — for anything
  production-grade, use a licensed SERP API instead.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit).
