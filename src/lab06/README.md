# ЛР6 — CLI‑утилиты с argparse (cat/grep‑lite + конвертеры): Техническое задание

> **Цель:** Научиться создавать консольные инструменты с аргументами командной строки, подкомандами и флагами.  
> **Связь:** продолжение ЛР5 (работа с JSON/CSV/XLSX) и подготовка к ЛР7 (тестирование).  
> Основная задача — обернуть существующие функции конвертации и анализа текста в CLI‑оболочки с помощью **argparse**.

---

## Результат ЛР

- Модуль `src/lab06/cli_text.py` с подкомандами:
  - `stats --input <txt> [--top 5]` — анализ частот слов в тексте (использовать функции из `lab03`);
  - `cat --input <path> [-n]` — вывод содержимого файла построчно (с нумерацией при `-n`).

- Модуль `src/lab06/cli_convert.py` с подкомандами:
  - `json2csv --in data/samples/people.json --out data/out/people.csv`  
  - `csv2json --in data/samples/people.csv --out data/out/people.json`  
  - `csv2xlsx --in data/samples/people.csv --out data/out/people.xlsx`  
  (использовать функции из `lab05`)

- Примеры запуска и скриншоты терминала — в `images/lab06/`.  
- `README.md` с кратким описанием всех подкоманд и параметров (`--help` и реальные примеры).  
- **Только стандартная библиотека** (`argparse`, `os`, `pathlib`, `sys` и ранее написанные функции).  
- Python **3.хх+**.

---
```
python_labs/
├─ README.md                       #Общий отчет
├─ requirements.txt                # openpyxl или xlsxwriter, по выбору
├─ src/                            # здесь — все скрипты по заданиям
|  ├─ lib/                         # Переиспользуемые модули - хранить здесь
|  |  └── io_helpers.py            
|  ├─ lab01
|  ........
|  ├─ lab05  
|  ├─ lab06/                       # Реализация кода
│  |   ├─ cli_text.py              
│  |   ├─ cli_convert.py
│  |   └─ __init__.py
|  ........
|  └─ lab10
├─ data/
|   ├── samples
│   └── out
|
└─ images/                         # сюда — скриншоты работы программ
   ├─ lab01
   ........
   └─ lab10
```
---

## Теоретическая часть

### Что такое CLI‑утилита
**CLI (Command Line Interface)** — интерфейс взаимодействия через консоль.  
CLI‑программы позволяют вызывать функции программы через команды и флаги, например:
```bash
python -m src.lab06.cli_convert json2csv --in data/samples/people.json --out data/out/people.csv
```

### Что такое argparse
Модуль **argparse** — стандартный инструмент Python для парсинга аргументов командной строки.

**Основные понятия:**
- `ArgumentParser` — объект, описывающий интерфейс программы;
- `add_argument()` — добавление параметров (`--input`, `--output`, `-n`, и т.д.);
- `add_subparsers()` — создание подкоманд (`stats`, `cat`, `json2csv` и др.).

**Минимальный пример:**
```python
import argparse

parser = argparse.ArgumentParser(description="Пример CLI")
parser.add_argument("--name", required=True, help="Имя пользователя")
args = parser.parse_args()
print(f"Привет, {args.name}!")
```

**Результат запуска:**
```bash
$ python hello.py --name Alice
Привет, Alice!
```
---

## Примеры кода

### Пример 1. Подкоманды в одном CLI
```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="CLI‑утилиты лабораторной №6")
    subparsers = parser.add_subparsers(dest="command")

    # подкоманда cat
    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла")
    cat_parser.add_argument("--input", required=True)
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки")

    # подкоманда stats
    stats_parser = subparsers.add_parser("stats", help="Частоты слов")
    stats_parser.add_argument("--input", required=True)
    stats_parser.add_argument("--top", type=int, default=5)

    args = parser.parse_args()

    if args.command == "cat":
        """ Реализация команды cat """
    elif args.command == "stats":
        """ Реализация команды stats """
```

---

### Пример 2. CLI‑конвертер
```python
import argparse
from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx

def main():
    parser = argparse.ArgumentParser(description="Конвертеры данных")
    sub = parser.add_subparsers(dest="cmd")

    p1 = sub.add_parser("json2csv")
    p1.add_argument("--in", dest="input", required=True)
    p1.add_argument("--out", dest="output", required=True)

    p2 = sub.add_parser("csv2json")
    p2.add_argument("--in", dest="input", required=True)
    p2.add_argument("--out", dest="output", required=True)

    p3 = sub.add_parser("csv2xlsx")
    p3.add_argument("--in", dest="input", required=True)
    p3.add_argument("--out", dest="output", required=True)

    args = parser.parse_args()

    """
        Вызываем код в зависимости от аргументов.
    """
```

---

## Проверка и демонстрация

**Файлы для демонстрации:**
- Использовать данные из `data/samples/` из ЛР5.  
- Результаты сохраняются в `data/out/`.

**Сценарии проверки (описать в README):**
1. `cat --input data/samples/people.csv -n` → вывод строк с номерами.  
2. `stats --input data/samples/people.txt --top 5` → вывод топ‑слов.  
3. `json2csv`, `csv2json`, `csv2xlsx` — корректная конвертация без ошибок.  
4. Проверка `--help` для каждой подкоманды.

---

## Валидация и обработка ошибок
- Отсутствие входного файла → `FileNotFoundError`.  
- Неверные аргументы → вывод `parser.error(...)`.  
- Все сообщения — понятные, человекочитаемые.  
- Вывод справки (`--help`) должен работать без ошибок.  
- Код не должен зависеть от внешних библиотек.

---

## Что сдавать
1. Код в `src/lab06/*`  
2. Файлы демонстрации в `data/out/`  
3. `README.md` с командами запуска и примерами вывода (скриншоты) 
4. Скриншоты в `images/lab06/`

---

## Критерии допуска
- Лабораторная работа **выполнена на 100%**
- Оформлен отчет в README-файле по примеру **effective-broccoli**

## Критерии приёмки
- Корректность работы всех CLI‑команд — **20%**  
- Наличие справки (`--help`) и ошибок — **20%**  
- Ответы на вопросы по теории (argparse, CLI, структура) — **60%**  
