# ЛР9 — «База данных» на CSV: CRUD-функции над `students.csv` и CLI

> **Цель:** реализовать простейшее хранилище данных студентов на основе
> CSV-файла, отработать CRUD-операции (Create / Read / Update / Delete)
> и научиться работать с ними через набор функций с общим хранилищем и через консольную утилиту.
> **Связь:** ЛР9 использует запись `Student` и валидацию из ЛР8, утилиты работы с CSV из ЛР4–ЛР5
> и argparse из ЛР6.

---
## Результат ЛР

После выполнения ЛР9 в репозитории должны присутствовать:

### `src/lab09/group.py`

Модуль с **функциями CRUD** над студентами. Каждая функция получает **путь к CSV-файлу первым аргументом**
и работает по схеме «загрузить → изменить → сохранить»:

- служебные функции хранилища:
  - `ensure_storage(path)` — создать файл с заголовком, если его ещё нет
  - `load_students(path) -> list[dict]` — прочитать все записи из CSV
  - `save_students(path, students)` — перезаписать файл целиком
- CRUD:
  - `add_student(path, student: dict)` — добавление студента
  - `list_students(path, sort_by=None) -> list[dict]` — получить всех студентов
  - `find_students(path, substr: str) -> list[dict]` — поиск по подстроке в ФИО
  - `remove_student(path, fio: str) -> int` — удаление по ФИО
  - `update_student(path, fio: str, **fields) -> bool` — обновление полей существующей записи

---
### `src/lab09/cli_students.py`

Консольная утилита с подкомандами `add`, `list`, `find`, `remove`, `update` (см. задание B).

---
### `src/lab09/__init__.py`

- файл инициализации пакета `lab09`

---
### `data/lab09/students.csv`

CSV-файл — «база данных» студентов, содержащий:

- строку-заголовок:  
  `fio,birthdate,group,gpa`
- одну или несколько строк с данными студентов, например:  
  `Иванов Иван,2007-10-10,БИВТ-26-6-1,4.3`

---
### `images/lab09/`

Каталог со скриншотами, демонстрирующими работу ЛР9:

- добавление студента
- вывод списка (с сортировкой и без)
- поиск / обновление / удаление записей
- ошибка при попытке добавить запись с неверным `gpa`

---
### Формат CSV

Файл хранится по пути `data/lab09/students.csv`.

Структура:

```csv
fio,birthdate,group,gpa
Иванов Иван,2007-10-10,БИВТ-26-6-1,4.3
...
```
---

## Структура репозитория (рекомендации)
```text
python_labs/
├─ README.md
├─ src/
│   ├─ lab08
│   ├─ lab09/
│   │   ├─ group.py          # функции хранилища + CRUD
│   │   ├─ cli_students.py   # CLI на argparse
│   │   └─ __init__.py
│   └─ ...
├─ data/
│   ├─ lab08
│   └─ lab09/
│       └─ students.csv      # «база данных» студентов
└─ images/
    ├─ lab08
    └─ lab09
```

---
## Теоретическая часть: CRUD

CRUD — стандартный набор операций:

| Операция | Назначение                       |
|----------|----------------------------------|
| Create   | Добавление записи                |
| Read     | Получение списка / поиск         |
| Update   | Изменение существующей записи    |
| Delete   | Удаление                         |

В этой ЛР каждая операция будет реализована как функция с общим первым аргументом `path`.

### Состояние передаётся явно

Все функции работают с одним и тем же файлом. Вместо того чтобы «помнить» путь где-то
внутри, они принимают его первым аргументом:

``` python
add_student("data/lab09/students.csv", s)
find_students("data/lab09/students.csv", "Иван")
```

Это и есть общее состояние группы функций. Во втором семестре ровно этот аргумент
превратится в `self`, а набор функций — в класс.

### Загрузить → изменить → сохранить

CSV не умеет менять одну строку на месте. Поэтому каждая изменяющая операция
(`add`, `remove`, `update`) устроена одинаково:

1. `students = load_students(path)` — весь файл в список словарей
2. изменить список в памяти
3. `save_students(path, students)` — записать файл целиком заново

Читающие операции (`list`, `find`) файл не трогают.

### Валидация на входе и на выходе

- при чтении: каждая строка CSV → `student_from_dict` из ЛР8 (там же `gpa` из строки станет `float`)
- при записи: `add_student` и `update_student` не сохраняют запись, не прошедшую `validate_student`

Из CSV всё приходит строками. Это главная ловушка лабы: сравнение `"4.3" > "10.0"` работает
не так, как вы думаете.

---

## Задание

### A. Реализовать функции хранилища и CRUD (`group.py`)

- служебные:
  - `ensure_storage(path)` — если файла нет, создать его с одной строкой-заголовком `fio,birthdate,group,gpa`; создать недостающие каталоги
  - `load_students(path) -> list[dict]` — `csv.DictReader`, каждая строка через `student_from_dict`; отсутствие заголовка или лишние колонки — `ValueError`
  - `save_students(path, students)` — `csv.DictWriter` с `fieldnames=STUDENT_FIELDS`, `newline=""`, `encoding="utf-8"`

- CRUD:
  - `add_student(path, student)` — валидирует запись, дописывает в конец; вернуть ничего не нужно
  - `list_students(path, sort_by=None)` — `sort_by` ∈ `{None, "fio", "gpa"}`; сортировать через `sorted(..., key=...)`; неизвестное значение — `ValueError`
  - `find_students(path, substr)` — все записи, у которых `substr` входит в `fio` **без учёта регистра**
  - `remove_student(path, fio)` — удалить **все** записи с таким `fio`, вернуть количество удалённых
  - `update_student(path, fio, **fields)` — обновить поля **первой** записи с таким `fio`; неизвестный ключ — `KeyError`; результат валидируется; вернуть `True`, если запись найдена, иначе `False`

- валидация:
  - наличие строки-заголовка в CSV (`fio,birthdate,group,gpa`)
  - соответствие каждой строки корректной записи `Student` из ЛР8

### B. Реализовать CLI (`cli_students.py`)

Подкоманды argparse (см. ЛР6), общий параметр `--db` с путём к хранилищу
(по умолчанию `data/lab09/students.csv`):

- `add --fio ... --birthdate ... --group ... --gpa ...`
- `list [--sort fio|gpa]`
- `find --q <подстрока>`
- `remove --fio ...` — печатает, сколько удалено
- `update --fio ... [--gpa ...] [--group ...] [--birthdate ...]`

Вывод списка — по одной записи на строку через `format_student` из ЛР8.
Ошибки валидации — понятным текстом в stderr и код возврата `1`.

Запуск: `python -m src.lab09.cli_students list --sort gpa`

### ★ Дополнительное задание (со звёздочкой)
#### Расширенная аналитика по группе

Добавить в `group.py` **аналитическую функцию**, собирающую статистику по студентам,
и подкоманду `stats` в CLI.

#### Функция `stats(path) -> dict`

Функция должна возвращать словарь следующей структуры:

```python
{
    "count": <общее количество студентов>,
    "min_gpa": <минимальный gpa>,
    "max_gpa": <максимальный gpa>,
    "avg_gpa": <средний gpa>,
    "groups": {
        "БИВТ-26-6-1": <число студентов>,
        "БИВТ-26-6-2": <число студентов>,
        ...
    },
    "top_5_students": [
        {"fio": "...", "gpa": ...},
        ...
    ]
}
```

#### Запрет дубликатов

`add_student` отказывается добавлять запись, если студент с таким `fio` уже есть — `ValueError`.




## Пример кода 

``` python
import csv
from pathlib import Path
from src.lab08.models import STUDENT_FIELDS, student_from_dict, validate_student

HEADER = STUDENT_FIELDS


def ensure_storage(path):
    path = Path(path)
    if not path.exists():
        path.write_text("", encoding="utf-8")   # TODO: здесь должен появиться заголовок


def load_students(path):
    # TODO: реализовать чтение строк из csv через DictReader + student_from_dict
    rows = []
    return rows


def save_students(path, students):
    # TODO: реализовать запись через DictWriter (newline="", encoding="utf-8")
    pass


def list_students(path, sort_by=None):
    # TODO: реализовать сортировку по sort_by
    return load_students(path)


def add_student(path, student):
    # TODO: validate_student, затем load → append → save
    pass


def find_students(path, substr):
    rows = load_students(path)
    # TODO: без учёта регистра
    return [r for r in rows if substr in r["fio"]]


def remove_student(path, fio):
    rows = load_students(path)
    # TODO: удалить ВСЕ вхождения и вернуть их количество
    for i, r in enumerate(rows):
        if r["fio"] == fio:
            rows.pop(i)
            break


def update_student(path, fio, **fields):
    # TODO: реализовать обновление с валидацией результата
    pass
```

## Что сдавать

1.  **Код**:
    -   `src/lab09/group.py`
    -   `src/lab09/cli_students.py`
2.  **README.md**:
    -   результаты
    -   сценарий из 5–6 команд подряд с выводом
    -   итоговый `students.csv`
3.  **Файлы данных**:
    -   `students.csv`
4.  **Скриншоты работы**

---

## Критерий допуска
-   Лабораторная выполнена полностью\
-   README оформлен в стиле прошлых работ\
-   В коде нет `class` — только функции с явным `path`

---

## Критерий приёмки
 - Корректность функций `crud` — **20%**  
 - Корректность `csv` — **20%**  
 - Ответы на вопросы по теории — **60%** 

---

## Полезные ссылки
 - Модуль `csv`: https://docs.python.org/3/library/csv.html
 - `argparse`, подкоманды: https://docs.python.org/3/library/argparse.html#sub-commands
 - [Интересно про то, зачем всё-таки классы](https://letmegooglethat.com)
