"""Write scraped results to disk in xlsx, csv, or json."""

import sys
from pathlib import Path

import pandas as pd

SUPPORTED_FORMATS = ("xlsx", "csv", "json")


def save_results(
    titles: list[str],
    urls: list[str | None],
    output_path,
    fmt: str = "xlsx",
    query: str | None = None,
) -> pd.DataFrame:
    """Save titles/urls to `output_path` in the given format.

    If `query` is provided, a leading 'Query' column is added -- used by
    batch mode so each row records which search produced it.
    """
    fmt = fmt.lower()
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format '{fmt}'. Choose one of {SUPPORTED_FORMATS}.")

    rows = {"Page Titles": titles, "URL": urls}
    if query is not None:
        rows = {"Query": [query] * len(titles), **rows}
    df = pd.DataFrame(rows)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if fmt == "xlsx":
            with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name="Search_results", index=False)
        elif fmt == "csv":
            df.to_csv(output_path, index=False)
        elif fmt == "json":
            df.to_json(output_path, orient="records", indent=2)
    except Exception as e:
        print(f"An error occurred while writing '{output_path}': {e}")
        sys.exit(1)

    print(f"Saved {len(df)} result(s) to '{output_path}'.")
    return df


# NOTE: xlsxwriter is used instead of openpyxl for better formatting control.
