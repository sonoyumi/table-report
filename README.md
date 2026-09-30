# 📊 Table Report

<p>
  <a href="https://github.com/sonoyumi/table-report/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/sonoyumi/table-report/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white">
  <img alt="openpyxl" src="https://img.shields.io/badge/Excel-openpyxl-217346?logo=microsoftexcel&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
</p>

**🇬🇧 [English](#en)** · **🇮🇹 [Italiano](#it)** · **🇺🇦 [Українська](#uk)** · **🇷🇺 [Русский](#ru)**

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
[![LinkedIn](https://img.shields.io/badge/LinkedIn-profile-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vladyslav-shokun/)

> 💼 Tired of merging spreadsheets by hand? Get in touch, I'll automate it.

### License

MIT, see [LICENSE](LICENSE).

---

<a name="it"></a>

## 🇮🇹 Italiano

**[🇬🇧 English](#en)** · **🇮🇹 Italiano** · **[🇺🇦 Українська](#uk)** · **[🇷🇺 Русский](#ru)**

Uno strumento da riga di comando che trasforma un mucchio di esportazioni CSV ed Excel disordinate in un unico
report Excel pulito e formattato con i totali, e può inviarlo direttamente su Telegram.
Uso tipico: vendite mensili di più filiali, esportazioni da sistemi diversi,
tutto ciò che di solito si unisce a mano ogni settimana.

### Cosa gestisce

- **Formati diversi:** `.csv` e `.xlsx` in un'unica esecuzione; si possono passare file o intere cartelle.
- **CSV di ogni tipo:** i separatori `,` `;` `\t` `|` vengono rilevati automaticamente; codifiche UTF-8 e Windows-1251.
- **Intestazioni disordinate:** `Сумма`, ` СУММА ` e `сумма` sono considerate la stessa colonna; intestazioni duplicate e vuote vengono sistemate.
- **Numeri disordinati:** `1 240,00 €`, `1,234.50`, `1.234,50`, `12,5` vengono tutti interpretati correttamente;
  i valori che non sono numeri (`su richiesta`) vengono saltati e segnalati, mai contati in silenzio come 0.
- **Duplicati:** `--dedupe` rimuove le righe esportate due volte.
- **Report:** foglio **"Итоги"** ("Totali": totali per gruppo, dal più grande, con il totale generale) e foglio **"Данные"**
  ("Dati": tutte le righe unite + colonna con il file di origine); intestazioni in grassetto, riga di intestazione bloccata,
  filtri, larghezza delle colonne.
- **Output sicuro:** i valori delle celle come `=HYPERLINK(...)` provenienti dai file di input vengono salvati come testo, non come formule attive.
- **Telegram:** `--telegram` invia il report finito in una chat (il token non compare mai nei messaggi di errore).

### Esempio

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

> I file di esempio e l'output del programma sono in russo: colonne Città / Righe / Importo / Quantità
> (Roma, Milano, Torino, Napoli), riga TOTALE; in cima: "File: 2, righe: 10, duplicati rimossi: 1" e l'avviso
> che 1 valore in «Importo» non sembra un numero e non è entrato nella somma; in fondo: "Report salvato: report.xlsx".

I due file in [`examples/`](examples) sono volutamente incoerenti: virgola contro punto e virgola, UTF-8 contro Windows-1251,
maiuscole/minuscole e ordine delle colonne diversi, una riga duplicata, una riga vuota e un importo non numerico.

> Consiglio: dai alle esportazioni un nome con la data (`2026-01_sales.csv`, `2026-02_sales.csv`). I file di una cartella vengono letti
> in ordine alfabetico e i titoli delle colonne nel report vengono presi dal primo file.

### Avvio rapido

```bash
git clone https://github.com/sonoyumi/table-report.git
cd table-report
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
table-report --help
```

Per `--telegram`: `cp .env.example .env` e impostare `BOT_TOKEN` (da @BotFather) e `CHAT_ID`.

Test: `pytest` (34 test, inclusa un'esecuzione end-to-end sui file di esempio e un'API Telegram simulata).

### Struttura del progetto

```
src/table_report/
├── readers.py    # lettura CSV/XLSX, rilevamento di codifica e separatore, pulizia delle intestazioni
├── transform.py  # unione, parsing dei numeri, rimozione duplicati, raggruppamento e totali (funzioni pure)
├── writer.py     # report Excel formattato
├── telegram.py   # sendDocument tramite httpx
└── cli.py        # interfaccia a riga di comando
```

### Autore

**Vladyslav Shokun** ([@sonoyumi](https://github.com/sonoyumi)), sviluppatore Python: bot Telegram, web scraping, automazione.

[![Telegram](https://img.shields.io/badge/Telegram-write%20me-2CA5E0?logo=telegram&logoColor=white)](https://t.me/sonoyumiii)
[![Email](https://img.shields.io/badge/Email-contact-EA4335?logo=gmail&logoColor=white)](mailto:sonoyumiii@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-profile-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vladyslav-shokun/)

> 💼 Stanco di unire i fogli di calcolo a mano? Scrivimi, lo automatizzo io.

### Licenza

MIT, vedi [LICENSE](LICENSE).

---

<a name="uk"></a>

## 🇺🇦 Українська

**[🇬🇧 English](#en)** · **[🇮🇹 Italiano](#it)** · **🇺🇦 Українська** · **[🇷🇺 Русский](#ru)**

Утиліта командного рядка, яка перетворює купу розрізнених CSV- та Excel-вивантажень на один
чистий оформлений Excel-звіт із підсумками й може одразу надіслати його в Telegram.
Типові задачі: продажі за місяць із кількох філій, вивантаження з різних систем —
усе, що зазвичай щотижня зводять вручну.

### З чим справляється

- **Різні формати:** `.csv` і `.xlsx` за один запуск; можна передати файли або цілі папки.
- **Різні CSV:** роздільники `,` `;` `\t` `|` визначаються автоматично; кодування UTF-8 і Windows-1251.
- **Криві заголовки:** `Сумма`, ` СУММА ` і `сумма` вважаються однією колонкою; дублікати й порожні заголовки виправляються.
- **Криві числа:** `1 240,00 €`, `1,234.50`, `1.234,50`, `12,5` розбираються правильно; нечислові значення
  (`за запитом`) пропускаються з попередженням, а не перетворюються мовчки на 0.
- **Дублікати:** `--dedupe` видаляє рядки, вивантажені двічі.
- **Звіт:** аркуш **«Итоги»** («Підсумки»: суми за групами, від більшого до меншого, з рядком ИТОГО) і аркуш **«Данные»**
  («Дані»: усі об'єднані рядки + колонка з назвою вихідного файлу); жирні заголовки, закріплена шапка,
  фільтри, ширина колонок.
- **Безпека:** значення на кшталт `=HYPERLINK(...)` із вхідних файлів зберігаються як текст, а не як живі формули.
- **Telegram:** `--telegram` надсилає готовий звіт у чат (токен ніколи не потрапляє в повідомлення про помилки).

### Приклад

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

> Файли-приклади та вивід програми — російською: колонки Місто / Рядків / Сума / Кількість
> (Рим, Мілан, Турин, Неаполь), рядок РАЗОМ; угорі — «Файлів: 2, рядків: 10, видалено дублікатів: 1» і попередження,
> що 1 значення в «Сума» не схоже на число й не ввійшло в суму; унизу — «Звіт збережено: report.xlsx».

Два файли в [`examples/`](examples) навмисно різні: кома й крапка з комою, UTF-8 і Windows-1251,
інший регістр і порядок колонок, дубль рядка, порожній рядок і нечислова сума.

> Порада: називайте вивантаження за датою (`2026-01_sales.csv`, `2026-02_sales.csv`). Файли з папки читаються
> за абеткою, а назви колонок у звіті беруться з першого файлу.

### Швидкий старт

```bash
git clone https://github.com/sonoyumi/table-report.git
cd table-report
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
table-report --help
```

Для `--telegram`: `cp .env.example .env` і вписати `BOT_TOKEN` (від @BotFather) та `CHAT_ID`.

Тести: `pytest` (34 тести, зокрема наскрізний запуск на прикладах і Telegram API через заглушку).

### Структура проєкту

```
src/table_report/
├── readers.py    # читання CSV/XLSX, визначення кодування й роздільника, чищення заголовків
├── transform.py  # об'єднання, розбір чисел, дублікати, групування й підсумки (чисті функції)
├── writer.py     # оформлений Excel-звіт
├── telegram.py   # sendDocument через httpx
└── cli.py        # інтерфейс командного рядка
```

### Автор

**Vladyslav Shokun** ([@sonoyumi](https://github.com/sonoyumi)) — Python-розробник: Telegram-боти, парсинг, автоматизація.

[![Telegram](https://img.shields.io/badge/Telegram-write%20me-2CA5E0?logo=telegram&logoColor=white)](https://t.me/sonoyumiii)
[![Email](https://img.shields.io/badge/Email-contact-EA4335?logo=gmail&logoColor=white)](mailto:sonoyumiii@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-profile-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vladyslav-shokun/)

> 💼 Набридло зводити таблиці вручну? Напишіть мені, автоматизую.

### Ліцензія

MIT — див. [LICENSE](LICENSE).

---

<a name="ru"></a>

## 🇷🇺 Русский

**[🇬🇧 English](#en)** · **[🇮🇹 Italiano](#it)** · **[🇺🇦 Українська](#uk)** · **🇷🇺 Русский**

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
[![LinkedIn](https://img.shields.io/badge/LinkedIn-profile-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vladyslav-shokun/)

> 💼 Надоело сводить таблицы вручную? Напишите мне, автоматизирую.

### Лицензия

MIT — см. [LICENSE](LICENSE).
