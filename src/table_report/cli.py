"""Command line interface: table-report FILES... --group-by COL --sum COL."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from table_report import __version__
from table_report.readers import collect_files, read_table
from table_report.telegram import TelegramError, send_document
from table_report.transform import Summary, dedupe, find_column, merge, summarize
from table_report.writer import write_report

EXIT_USER_ERROR = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="table-report",
        description="Merge CSV/Excel files, clean them and build an Excel report with totals.",
        epilog='Example: table-report examples/ --group-by "Город" --sum "Сумма" --dedupe',
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="CSV/XLSX files or folders with them")
    parser.add_argument("-o", "--output", type=Path, default=Path("report.xlsx"), help="report file (report.xlsx)")
    parser.add_argument("-g", "--group-by", action="append", default=[], metavar="COLUMN", help="group by column")
    parser.add_argument("-s", "--sum", action="append", default=[], metavar="COLUMN", help="sum a numeric column")
    parser.add_argument("--dedupe", action="store_true", help="drop duplicate rows")
    parser.add_argument(
        "--telegram", action="store_true", help="send the report to Telegram (BOT_TOKEN, CHAT_ID in env/.env)"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def format_summary(summary: Summary, limit: int = 15) -> str:
    rows = [summary.header, *[[str(v) for v in row] for row in summary.rows]]
    shown = rows[: limit + 1] + ([rows[-1]] if len(rows) > limit + 1 else [])
    widths = [max(len(str(r[i])) for r in shown) for i in range(len(summary.header))]
    lines = ["  ".join(str(v).ljust(w) for v, w in zip(r, widths, strict=True)) for r in shown]
    lines.insert(1, "  ".join("-" * w for w in widths))
    if len(rows) > limit + 1:
        lines.insert(-1, f"... ещё {len(rows) - limit - 2} строк(и) в отчёте")
    return "\n".join(lines)


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        files = collect_files(args.inputs)
        if not files:
            raise ValueError("No .csv or .xlsx files found")
        tables = [read_table(path) for path in files]
        columns, rows = merge(tables)
        removed = 0
        if args.dedupe:
            rows, removed = dedupe(rows)
        group_by = [find_column(columns, name) for name in args.group_by]
        sums = [find_column(columns, name) for name in args.sum]
    except (OSError, ValueError) as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return EXIT_USER_ERROR

    summary = summarize(rows, group_by, sums)
    output = write_report(args.output, columns, rows, summary)

    print(f"Файлов: {len(files)}, строк: {len(rows)}" + (f", удалено дублей: {removed}" if args.dedupe else ""))
    for column, count in summary.skipped.items():
        print(f"Внимание: в «{column}» {count} значени(й) не похожи на числа и не вошли в сумму")
    print()
    print(format_summary(summary))
    print(f"\nОтчёт сохранён: {output}")

    if args.telegram:
        load_dotenv()
        token, chat_id = os.getenv("BOT_TOKEN", "").strip(), os.getenv("CHAT_ID", "").strip()
        if not token or not chat_id:
            print("Ошибка: для --telegram задайте BOT_TOKEN и CHAT_ID (в .env или окружении)", file=sys.stderr)
            return EXIT_USER_ERROR
        caption = f"📊 {output.name}: {len(files)} файл(ов), {len(rows)} строк"
        try:
            send_document(token, chat_id, output, caption)
        except TelegramError as exc:
            print(f"Ошибка: {exc}", file=sys.stderr)
            return 1
        print("Отчёт отправлен в Telegram ✅")
    return 0


def main() -> None:
    sys.exit(run())
