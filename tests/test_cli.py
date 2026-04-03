import pytest

from scraper_lib.cli import parse_args


def test_parses_single_query_with_defaults():
    args = parse_args(["python selenium tips"])
    assert args.query == "python selenium tips"
    assert args.queries_file is None
    assert args.pages == 1
    assert args.format == "xlsx"
    assert args.headless is False
    assert args.output is None


def test_parses_flags():
    args = parse_args(
        ["python selenium tips", "--pages", "3", "--format", "csv", "--headless", "-o", "out.csv"]
    )
    assert args.pages == 3
    assert args.format == "csv"
    assert args.headless is True
    assert args.output == "out.csv"


def test_parses_batch_mode():
    args = parse_args(["--queries-file", "queries.txt", "--headless"])
    assert args.queries_file == "queries.txt"
    assert args.query is None
    assert args.headless is True


def test_query_and_queries_file_are_mutually_exclusive():
    with pytest.raises(SystemExit):
        parse_args(["some query", "--queries-file", "queries.txt"])


def test_requires_query_or_queries_file():
    with pytest.raises(SystemExit):
        parse_args([])


def test_rejects_unsupported_format():
    with pytest.raises(SystemExit):
        parse_args(["query", "--format", "yaml"])


# FIXME: add integration test that invokes main() with a live query.
