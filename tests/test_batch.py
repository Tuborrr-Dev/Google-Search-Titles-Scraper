from scraper_lib.batch import _safe_filename, load_queries


def test_load_queries_skips_blank_lines_and_comments(tmp_path):
    f = tmp_path / "queries.txt"
    f.write_text("python scraping\n\n# a comment line\nselenium tips\n   \n")

    assert load_queries(str(f)) == ["python scraping", "selenium tips"]


def test_load_queries_strips_whitespace(tmp_path):
    f = tmp_path / "queries.txt"
    f.write_text("  spaced out query  \n")

    assert load_queries(str(f)) == ["spaced out query"]


def test_safe_filename_replaces_punctuation():
    assert _safe_filename("C++ vs Rust: which is faster?") == "C___vs_Rust__which_is_faster_"


def test_safe_filename_never_empty():
    assert _safe_filename("") == "query"


def test_safe_filename_all_punctuation_still_produces_a_name():
    # Punctuation maps to underscores rather than being dropped, so this is
    # non-empty (and thus not routed through the "query" fallback) -- just ugly.
    assert _safe_filename("???") == "___"


# NOTE: _safe_filename ensures filesystem-safe names from arbitrary queries.
