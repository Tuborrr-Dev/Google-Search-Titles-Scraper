import json

import pandas as pd
import pytest

from scraper_lib.exporters import save_results


def test_save_results_csv(tmp_path):
    out = tmp_path / "out.csv"
    df = save_results(["Title A", "Title B"], ["http://a", "http://b"], out, fmt="csv")

    assert out.exists()
    assert len(df) == 2
    loaded = pd.read_csv(out)
    assert list(loaded["Page Titles"]) == ["Title A", "Title B"]


def test_save_results_json(tmp_path):
    out = tmp_path / "out.json"
    save_results(["Only Title"], ["http://only"], out, fmt="json")

    data = json.loads(out.read_text())
    assert data[0]["Page Titles"] == "Only Title"
    assert data[0]["URL"] == "http://only"


def test_save_results_xlsx(tmp_path):
    out = tmp_path / "out.xlsx"
    save_results(["T1", "T2"], ["http://1", "http://2"], out, fmt="xlsx")

    assert out.exists()
    loaded = pd.read_excel(out, sheet_name="Search_results")
    assert list(loaded["Page Titles"]) == ["T1", "T2"]


def test_save_results_adds_query_column_when_given(tmp_path):
    out = tmp_path / "out.csv"
    save_results(["T"], ["http://x"], out, fmt="csv", query="my search")

    loaded = pd.read_csv(out)
    assert loaded["Query"].iloc[0] == "my search"
    assert list(loaded.columns) == ["Query", "Page Titles", "URL"]


def test_save_results_rejects_unsupported_format(tmp_path):
    with pytest.raises(ValueError):
        save_results(["T"], ["http://x"], tmp_path / "out.txt", fmt="txt")


def test_save_results_creates_missing_parent_dirs(tmp_path):
    out = tmp_path / "nested" / "dir" / "out.csv"
    save_results(["T"], ["http://x"], out, fmt="csv")
    assert out.exists()
