"""Batch mode: run the scraper across a list of queries loaded from a file."""

from pathlib import Path

from .driver import build_driver
from .exporters import save_results
from .scrape import scrape


def load_queries(path: str) -> list[str]:
    """One query per line. Blank lines and '#'-prefixed comment lines are ignored."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]


def _safe_filename(query: str) -> str:
    cleaned = "".join(c if c.isalnum() or c in " -_" else "_" for c in query)
    return cleaned.strip().replace(" ", "_") or "query"


def run_batch(queries: list[str], args, output_dir) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for i, query in enumerate(queries, start=1):
        print(f"[{i}/{len(queries)}] Scraping: {query!r}")
        driver = build_driver(args.driver_path, args.headless)
        try:
            titles, urls = scrape(driver, query, args.pages, args.wait)
        finally:
            driver.quit()

        if not titles:
            print(f"  -> no results for {query!r}, skipping save.")
            continue

        out_path = output_dir / f"{_safe_filename(query)}.{args.format}"
        save_results(titles, urls, out_path, args.format, query=query)


# TODO: add progress bar (tqdm) for long batch runs.
