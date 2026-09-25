from pathlib import Path

import pytest
from openpyxl import Workbook

from table_report.readers import collect_files, read_table

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def test_utf8_comma_csv():
    table = read_table(EXAMPLES / "2026-01_sales.csv")
    assert table.columns[:3] == ["Дата", "Город", "Менеджер"]
    assert len(table.rows) == 6
    assert table.rows[0]["Сумма"] == "1 240,00"


def test_cp1251_semicolon_csv_with_messy_headers():
    table = read_table(EXAMPLES / "2026-02_sales.csv")
    assert table.columns[0] == "город"  # spaces trimmed
    assert "СУММА" in table.columns
    assert len(table.rows) == 5  # the empty ";;;;;" line is skipped
    assert table.rows[0]["город"] == "Рим"


def test_xlsx_and_header_fixes(tmp_path):
    wb = Workbook()
    ws = wb.active
    ws.append(["Name", "Name", None, "  Total  "])
    ws.append(["  Ann ", "x", 1, 10.5])
    ws.append([None, None, None, None])  # empty row is skipped
    ws.append(["Bob"])  # short row is padded
    path = tmp_path / "data.xlsx"
    wb.save(path)

    table = read_table(path)
    assert table.columns == ["Name", "Name (2)", "column_3", "Total"]
    assert table.rows[0] == {"Name": "Ann", "Name (2)": "x", "column_3": 1, "Total": 10.5}
    assert table.rows[1]["Total"] is None
    assert len(table.rows) == 2


def test_unsupported_format(tmp_path):
    path = tmp_path / "notes.txt"
    path.write_text("x")
    with pytest.raises(ValueError, match="unsupported"):
        read_table(path)


def test_collect_files_expands_folders_and_skips_excel_lock_files(tmp_path):
    (tmp_path / "a.csv").write_text("x\n1\n")
    (tmp_path / "b.xlsx").write_bytes(b"")
    (tmp_path / "~$b.xlsx").write_bytes(b"")
    (tmp_path / "readme.txt").write_text("")
    files = collect_files([tmp_path, tmp_path / "a.csv"])
    assert [p.name for p in files] == ["a.csv", "b.xlsx"]


def test_collect_files_missing_path(tmp_path):
    with pytest.raises(FileNotFoundError):
        collect_files([tmp_path / "nope.csv"])
