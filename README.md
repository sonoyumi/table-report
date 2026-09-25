# 📊 Table Report

<p>
  <a href="https://github.com/sonoyumi/table-report/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/sonoyumi/table-report/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white">
  <img alt="openpyxl" src="https://img.shields.io/badge/Excel-openpyxl-217346?logo=microsoftexcel&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
</p>

**🇬🇧 [English](#en)** · **🇷🇺 [Русский](#ru)**

---

<a name="en"></a>

## 🇬🇧 English

A command-line tool that turns a pile of messy CSV and Excel exports into one clean,
formatted Excel report with totals, and can send it straight to Telegram.
Typical use: monthly sales from several branches, exports from different systems,
anything that is usually merged by hand every week.

### What it handles

- **Different formats:** `.csv` and `.xlsx` in one run; pass files or whole folders.
- **Different CSV flavours:** `,` `;` `\t` `|` delimiters are detected automatically; UTF-8 and Windows-1251 encodings.
- **Messy headers:** `Сумма`, ` СУММА ` and `сумма` are treated as the same column; duplicate and empty headers are fixed.
- **Messy numbers:** `1 240,00 €`, `1,234.50`, `1.234,50`, `12,5` are all parsed correctly;
  values that are not numbers (`on request`) are skipped and reported, never silently counted as 0.
- **Duplicates:** `--dedupe` removes rows exported twice.
- **Report:** sheet **"Итоги"** (totals by group, biggest first, with a grand total) and sheet **"Данные"**
  (all merged rows + source file column); bold headers, frozen header row, filters, column widths.
- **Safe output:** cell values like `=HYPERLINK(...)` from input files are stored as text, not live formulas.
- **Telegram:** `--telegram` sends the finished report to a chat (the token never appears in error messages).

### Example

```bash
table-report examples/ -g "Город" -s "Сумма" -s "Кол-во" --dedupe
```

```
Файлов: 2, строк: 10, удалено дублей: 1
Внимание: в «Сумма» 1 значени(й) не похожи на числа и не вошли в сумму

Город    Строк  Сумма   Кол-во
-------  -----  ------  ------
Рим      3      2535.5  33
Милан    4      2370.2  45
Турин    1      620     1
Неаполь  2      480     61
ИТОГО    10     6005.7  140

Отчёт сохранён: report.xlsx
```

The two files in [`examples/`](examples) are deliberately inconsistent: comma vs semicolon, UTF-8 vs Windows-1251,
different header case and column order, a duplicated row, an empty line and a non-numeric amount.

> Tip: name exports by date (`2026-01_sales.csv`, `2026-02_sales.csv`). Files in a folder are read in
> alphabetical order, and column titles in the report are taken from the first file.

### Quick start

```bash
git clone https://github.com/sonoyumi/table-report.git
cd table-report
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
table-report --help
```

For `--telegram`: `cp .env.example .env` and set `BOT_TOKEN` (from @BotFather) and `CHAT_ID`.

Tests: `pytest` (34 tests, including an end-to-end run on the example files and a mocked Telegram API).

### Project structure

```
src/table_report/
├── readers.py    # CSV/XLSX reading, encoding and delimiter detection, header cleanup
├── transform.py  # merge, number parsing, dedupe, grouping and totals (pure functions)
├── writer.py     # formatted Excel report
├── telegram.py   # sendDocument via httpx
└── cli.py        # command-line interface
```

### Author

**Vladyslav Shokun** ([@sonoyumi](https://github.com/sonoyumi)), Python developer: Telegram bots, web scraping, automation.

[![Telegram](https://img.shields.io/badge/Telegram-write%20me-2CA5E0?logo=telegram&logoColor=white)](https://t.me/sonoyumiii)
[![Email](https://img.shields.io/badge/Email-contact-EA4335?logo=gmail&logoColor=white)](mailto:sonoyumiii@gmail.com)

> 💼 Tired of merging spreadsheets by hand? Get in touch, I'll automate it.

### License

MIT, see [LICENSE](LICENSE).

---

<a name="ru"></a>

## 🇷🇺 Русский

**[🇬🇧 English](#en)** · **🇷🇺 Русский**

Утилита командной строки, которая превращает кучу разрозненных CSV- и Excel-выгрузок в один
чистый оформленный Excel-отчёт с итогами и может сразу отправить его в Telegram.
Типичные задачи: продажи за месяц из нескольких филиалов, выгрузки из разных систем —
всё, что обычно каждую неделю сводят вручную.

### С чем справляется

- **Разные форматы:** `.csv` и `.xlsx` за один запуск; можно передать файлы или целые папки.
- **Разные CSV:** разделители `,` `;` `\t` `|` определяются автоматически; кодировки UTF-8 и Windows-1251.
- **Кривые заголовки:** `Сумма`, ` СУММА ` и `сумма` считаются одной колонкой; дубли и пустые заголовки исправляются.
- **Кривые числа:** `1 240,00 €`, `1,234.50`, `1.234,50`, `12,5` разбираются правильно; нечисловые значения
  (`по запросу`) пропускаются с предупреждением, а не превращаются молча в 0.
- **Дубли:** `--dedupe` удаляет строки, выгруженные дважды.
- **Отчёт:** лист **«Итоги»** (суммы по группам, от большего к меньшему, со строкой ИТОГО) и лист **«Данные»**
  (все объединённые строки + колонка с именем исходного файла); жирные заголовки, закреплённая шапка,
  фильтры, ширина колонок.
- **Безопасность:** значения вроде `=HYPERLINK(...)` из входных файлов сохраняются как текст, а не как живые формулы.
- **Telegram:** `--telegram` отправляет готовый отчёт в чат (токен никогда не попадает в сообщения об ошибках).

### Пример

```bash
table-report examples/ -g "Город" -s "Сумма" -s "Кол-во" --dedupe
```

Вывод — как в английском разделе выше. Два файла в [`examples/`](examples) специально разные:
запятая и точка с запятой, UTF-8 и Windows-1251, другой регистр и порядок колонок, дубль строки,
пустая строка и нечисловая сумма.

> Совет: называйте выгрузки по дате (`2026-01_sales.csv`, `2026-02_sales.csv`). Файлы из папки читаются
> по алфавиту, а названия колонок в отчёте берутся из первого файла.

### Быстрый старт

```bash
git clone https://github.com/sonoyumi/table-report.git
cd table-report
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
table-report --help
```

Для `--telegram`: `cp .env.example .env` и вписать `BOT_TOKEN` (от @BotFather) и `CHAT_ID`.

Тесты: `pytest` (34 теста, включая сквозной запуск на примерах и Telegram API через заглушку).

### Структура проекта

```
src/table_report/
├── readers.py    # чтение CSV/XLSX, определение кодировки и разделителя, чистка заголовков
├── transform.py  # объединение, разбор чисел, дубли, группировка и итоги (чистые функции)
├── writer.py     # оформленный Excel-отчёт
├── telegram.py   # sendDocument через httpx
└── cli.py        # интерфейс командной строки
```

### Автор

**Vladyslav Shokun** ([@sonoyumi](https://github.com/sonoyumi)) — Python-разработчик: Telegram-боты, парсинг, автоматизация.

[![Telegram](https://img.shields.io/badge/Telegram-write%20me-2CA5E0?logo=telegram&logoColor=white)](https://t.me/sonoyumiii)
[![Email](https://img.shields.io/badge/Email-contact-EA4335?logo=gmail&logoColor=white)](mailto:sonoyumiii@gmail.com)

> 💼 Надоело сводить таблицы вручную? Напишите мне, автоматизирую.

### Лицензия

MIT — см. [LICENSE](LICENSE).
