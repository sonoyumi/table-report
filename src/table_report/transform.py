"""Merging, cleaning and summarising rows. Pure functions, no I/O."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from table_report.readers import Row, Table

SOURCE_COLUMN = "Файл"
EMPTY_GROUP = "(пусто)"
TOTAL_LABEL = "ИТОГО"

_NUMBER_CHARS = re.compile(r"[^\d,.\-]")


def parse_number(value: Any) -> float | None:
    """Turns '1 234,50 €', '1,234.50', '-12', 7 into floats; returns None for anything else."""
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int | float):
        return float(value)
    text = _NUMBER_CHARS.sub("", str(value).replace(" ", ""))
    if not text or text in {"-", ".", ","}:
        return None
    if "," in text and "." in text:
        # The separator that comes last is the decimal one.
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        whole, _, frac = text.rpartition(",")
        if text.count(",") == 1 and len(frac) != 3:
            text = f"{whole}.{frac}"  # decimal comma: "12,5", "12,50"
        else:
            text = text.replace(",", "")  # thousands: "1,234", "1,234,567"
    try:
        return float(text)
    except ValueError:
        return None


def merge(tables: Iterable[Table]) -> tuple[list[str], list[Row]]:
    """Combines tables whose headers may differ in case/spacing; adds the source file column."""
    display: dict[str, str] = {}  # casefolded name -> name as first seen
    rows: list[Row] = []
    for table in tables:
        mapping = {}
        for column in table.columns:
            key = column.casefold()
            display.setdefault(key, column)
            mapping[column] = display[key]
        for row in table.rows:
            merged = {mapping[k]: v for k, v in row.items()}
            merged[SOURCE_COLUMN] = table.source
            rows.append(merged)
    columns = list(display.values())
    if rows:
        columns.append(SOURCE_COLUMN)
    return columns, rows


def dedupe(rows: list[Row], ignore: Iterable[str] = (SOURCE_COLUMN,)) -> tuple[list[Row], int]:
    """Drops rows identical in every column except `ignore` (the same row exported twice)."""
    ignored = set(ignore)
    seen: set[tuple] = set()
    unique: list[Row] = []
    for row in rows:
        key = tuple(sorted((k, repr(v)) for k, v in row.items() if k not in ignored and v is not None))
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return unique, len(rows) - len(unique)


def find_column(columns: list[str], name: str) -> str:
    wanted = " ".join(name.split()).casefold()
    for column in columns:
        if column.casefold() == wanted:
            return column
    raise ValueError(f"Column {name!r} not found. Available: {', '.join(columns) or '(no columns)'}")


def _tidy(value: float) -> int | float:
    """2535.5 stays as is, 33.0 becomes 33: whole numbers look cleaner in the report."""
    value = round(value, 2)
    return int(value) if value.is_integer() else value


@dataclass
class Summary:
    header: list[str]
    rows: list[list[Any]]
    skipped: dict[str, int] = field(default_factory=dict)  # sum column -> values that were not numbers


def summarize(rows: list[Row], group_by: list[str], sums: list[str]) -> Summary:
    """Groups rows and returns count + sums per group, biggest first, with a total line."""
    groups: dict[tuple, list[float]] = {}
    counts: dict[tuple, int] = {}
    skipped = dict.fromkeys(sums, 0)
    for row in rows:
        key = tuple(EMPTY_GROUP if row.get(col) is None else str(row[col]) for col in group_by)
        totals = groups.setdefault(key, [0.0] * len(sums))
        counts[key] = counts.get(key, 0) + 1
        for i, col in enumerate(sums):
            number = parse_number(row.get(col))
            if number is None:
                if row.get(col) is not None:
                    skipped[col] += 1
                continue
            totals[i] += number

    def sort_key(item: tuple[tuple, list[float]]) -> tuple:
        key, totals = item
        return (-(totals[0] if totals else counts[key]), key)

    table = [[*key, counts[key], *(_tidy(t) for t in totals)] for key, totals in sorted(groups.items(), key=sort_key)]
    if group_by and table:
        total_sums = [_tidy(sum(t[i] for t in groups.values())) for i in range(len(sums))]
        table.append([TOTAL_LABEL, *[""] * (len(group_by) - 1), sum(counts.values()), *total_sums])
    header = [*group_by, "Строк", *sums]
    return Summary(header=header, rows=table, skipped={k: v for k, v in skipped.items() if v})
