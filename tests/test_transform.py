import pytest

from table_report.readers import Table
from table_report.transform import (
    EMPTY_GROUP,
    SOURCE_COLUMN,
    TOTAL_LABEL,
    dedupe,
    find_column,
    merge,
    parse_number,
    summarize,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (7, 7.0),
        (2.5, 2.5),
        ("1 240,00", 1240.0),
        ("1 240,50 €", 1240.5),
        ("1,234.50", 1234.5),
        ("1.234,50", 1234.5),
        ("12,5", 12.5),
        ("1,234", 1234.0),
        ("1,234,567", 1234567.0),
        ("-42", -42.0),
        ("$ 99", 99.0),
        ("по запросу", None),
        ("", None),
        (None, None),
        (True, None),
    ],
)
def test_parse_number(raw, expected):
    assert parse_number(raw) == expected


def test_merge_matches_headers_ignoring_case_and_adds_source():
    a = Table("a.csv", ["Город", "Сумма"], [{"Город": "Рим", "Сумма": "10"}])
    b = Table("b.csv", ["город", "СУММА", "Менеджер"], [{"город": "Милан", "СУММА": "5", "Менеджер": "Анна"}])
    columns, rows = merge([a, b])
    assert columns == ["Город", "Сумма", "Менеджер", SOURCE_COLUMN]
    assert rows[1] == {"Город": "Милан", "Сумма": "5", "Менеджер": "Анна", SOURCE_COLUMN: "b.csv"}


def test_dedupe_ignores_source_file():
    rows = [
        {"x": 1, SOURCE_COLUMN: "a.csv"},
        {"x": 1, SOURCE_COLUMN: "b.csv"},
        {"x": 2, SOURCE_COLUMN: "a.csv"},
    ]
    unique, removed = dedupe(rows)
    assert removed == 1
    assert [r["x"] for r in unique] == [1, 2]


def test_find_column_is_case_insensitive_and_helpful():
    assert find_column(["Город", "Сумма"], "  сумма ") == "Сумма"
    with pytest.raises(ValueError, match="Available: Город, Сумма"):
        find_column(["Город", "Сумма"], "Цена")


def test_summarize_groups_sorts_and_totals():
    rows = [
        {"city": "Rome", "sum": "10"},
        {"city": "Milan", "sum": "30"},
        {"city": "Rome", "sum": "5,5"},
        {"city": None, "sum": "1"},
        {"city": "Milan", "sum": "n/a"},
    ]
    summary = summarize(rows, ["city"], ["sum"])
    assert summary.header == ["city", "Строк", "sum"]
    assert summary.rows == [
        ["Milan", 2, 30.0],
        ["Rome", 2, 15.5],
        [EMPTY_GROUP, 1, 1.0],
        [TOTAL_LABEL, 5, 46.5],
    ]
    assert summary.skipped == {"sum": 1}


def test_summarize_without_grouping_counts_everything():
    summary = summarize([{"a": 1}, {"a": 2}], [], ["a"])
    assert summary.rows == [[2, 3.0]]
