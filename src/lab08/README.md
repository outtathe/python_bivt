# ЛР8 – Модель данных без классов: запись `Student` как словарь, валидация и сериализация

> **Цель:** научиться описывать модель данных без классов — как словарь с фиксированным
> набором ключей, — реализовывать функции-конструкторы и валидацию,
> сериализовывать/десериализовывать записи в JSON.\
> **Связь:** продолжаем работу с файлами и сериализацией из ЛР5, логику структуры
> и оформления наследуем из предыдущих ЛР. Инициалы для красивого вывода берём из ЛР1.
> Основная задача — реализовать полноценную модель студента, экспорт/импорт в JSON и корректные
> функции над записью. Во втором семестре ровно эта запись станет классом.
___
## Результат ЛР

После выполнения ЛР8 в репозитории должны присутствовать:

### `src/lab08/models.py`
Модель **`Student`** — запись-словарь, содержащая:

- константу `STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")` — перечень ключей записи
- поля (ключи словаря):
  - `fio`
  - `birthdate`
  - `group`
  - `gpa`
- функции:
  - `make_student(fio, birthdate, group, gpa) -> dict`
  - `validate_student(rec: dict) -> None`
  - `student_age(rec: dict, today=None) -> int`
  - `format_student(rec: dict) -> str`
  - `student_to_dict(rec: dict) -> dict`
  - `student_from_dict(d: dict) -> dict`
- валидацию:
  - набора ключей (ровно `STUDENT_FIELDS`, ничего лишнего и ничего пропущенного)
  - формата даты (`YYYY-MM-DD`) и её существования (`2003-02-30` — не дата)
  - диапазона среднего балла `0 ≤ gpa ≤ 5`

---

### `src/lab08/serialize.py`

Функции сериализации:

- `students_to_json(list[dict], path)`
- `students_from_json(path) -> list[dict]`

---

### `data/lab08/`

Должны находиться:

- пример входного JSON (`students_input.json`)
- пример выходного JSON (результат сериализации, `students_output.json`)
- пример JSON с **битой** записью (`students_bad.json`) — для демонстрации валидации

---

### `lab08/README.md`

Файл отчёта должен содержать:

- примеры запуска функций
- примеры JSON **до/после преобразования**
- описание структуры записи `Student` и логики каждой функции
- **политику обработки битых записей** (см. задание B) — падаем или пропускаем

---

## Структура репозитория (рекомендация)
```
python_labs/
├─ README.md                        # Общий отчет
├─ src/
│   ├─ lib
│   ├─ lab08/
|   |   ├─ models.py
|   |   ├─ serialize.py
│   │   ├─ _ _init_ _.py
|   └─  └─ README.md                # Отчет по ЛР8
├─ data/
│   └─ lab08/
│       ├─ students_input.json
│       ├─ students_output.json
│       └─ students_bad.json
├─ images /
    └── lab08
```

---

## Теоретическая часть: запись как словарь

### Запись (record)

Запись — это набор именованных полей фиксированной формы. В Python без классов запись
удобнее всего представлять словарём, у которого **всегда одни и те же ключи**:

``` python
student = {"fio": "Иванов Иван Иванович", "birthdate": "2007-05-14", "group": "БИВТ-26-6-1", "gpa": 4.3}
```

Чем это отличается от «просто словаря»: ключи не произвольны. Их перечень — константа
`STUDENT_FIELDS`, и любая функция может на неё положиться.

### Функция-конструктор

Раз ключи фиксированы, словарь не собирают руками в каждом месте — это делает одна функция,
которая заодно **проверяет данные**. Такую функцию называют конструктором:

``` python
def make_student(fio, birthdate, group, gpa):
    ...проверки...
    return {"fio": fio, "birthdate": birthdate, "group": group, "gpa": gpa}
```

Если данные плохие — `raise ValueError("...")` с сообщением, из которого понятно,
**какое поле** и **почему** не подошло. Никаких `print("warning")` — программа, которая
молча продолжает работать с неверными данными, хуже программы, которая упала.

### Валидация даты

Формат `YYYY-MM-DD` — это ISO 8601. Проверять регуляркой недостаточно: `2003-02-30`
проходит по формату, но такой даты нет. Правильный способ — попросить `datetime` разобрать строку:

``` python
from datetime import date
date.fromisoformat("2003-02-30")   # ValueError: day is out of range for month
```

### Сериализация

Запись-словарь → JSON — напрямую, `json` умеет словари. Обратно: JSON → словарь → **валидация** →
запись. Пропустить валидацию на входе — значит впустить в программу данные, которые она не умеет обрабатывать.

``` python
import json
json.dumps(student, ensure_ascii=False, indent=2)
```

### Почему не менять запись на месте

Функции, которые «изменяют» запись, возвращают **новую** запись, а старую не трогают
(см. ★). Вспомните Л3: два имени могут указывать на один словарь, и изменение через одно
имя видно через другое.

---

## Задание

### A. Реализовать модель `Student` (`models.py`)

### Поля:

| Поле       | Тип   | Описание                |
|------------|-------|--------------------------|
| `fio`      | `str` | ФИО студента, непустая строка |
| `birthdate`| `str` | Формат `YYYY-MM-DD`, дата существует |
| `group`    | `str` | Группа, напр. `БИВТ-26-6-1`, непустая |
| `gpa`      | `float` | Средний балл 0…5; `int` допустим и приводится к `float` |

---

### Функции:

- `make_student(fio, birthdate, group, gpa) -> dict` — собрать запись, проверив каждое поле
- `validate_student(rec) -> None` — проверить готовый словарь: набор ключей и значения; при ошибке — `ValueError`
- `student_age(rec, today=None) -> int` — полных лет на дату `today` (по умолчанию `date.today()`);
  человек, родившийся `2007-09-20`, на `2026-09-19` ещё не отметил день рождения
- `format_student(rec) -> str` — красивый вывод: `Иванов И.И. (БИВТ-26-6-1), 19 лет, GPA 4.30`
- `student_to_dict(rec) -> dict` — **копия** записи (не та же самая!) для сериализации
- `student_from_dict(d) -> dict` — десериализация: взять из словаря ровно нужные ключи, привести `gpa` к `float`, провалидировать

---

### Валидация в `make_student` и `validate_student`:

- `fio` и `group` — строки, после `strip()` непустые
- `birthdate` — строка, `date.fromisoformat` её разбирает, дата не в будущем
- `gpa` — число (`int` или `float`, **не** `bool`), `0 <= gpa <= 5`
- в `validate_student` дополнительно: `set(rec) == set(STUDENT_FIELDS)`
---

### B. Реализовать модуль `serialize.py`

#### `students_to_json(students, path)`

Сохраняет список записей в JSON: массив объектов, `ensure_ascii=False`, `indent=2`.

#### `students_from_json(path) -> list[dict]`

-   читает JSON-массив
-   каждую запись прогоняет через `student_from_dict`
-   при битой записи — **одна из двух политик**, выбранную описать в README:
    - `strict`: первая же ошибка → `ValueError` с номером записи и причиной
    - `skip`: битые записи пропускаются, в конце в консоль — сколько пропущено и почему

---

### ★ Дополнительное задание (со звёздочкой)

#### `update_student(rec, **fields) -> dict`

Возвращает **новую** запись с изменёнными полями. Исходная запись не меняется.
Неизвестный ключ в `fields` — `KeyError`, неверное значение — `ValueError` (через `validate_student`).

``` python
s2 = update_student(s1, gpa=4.8)
s1["gpa"]   # прежнее значение
```

#### `students_from_csv(path) -> list[dict]`

Чтение записей из CSV через `csv.DictReader` (заголовок `fio,birthdate,group,gpa`).
Обратите внимание: из CSV `gpa` приходит **строкой** — где именно это лечится, опишите в README.

---

## Пример кода

### `models.py`

``` python
# imports

STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")


def make_student(fio, birthdate, group, gpa):
    # TODO: добавить нормальную валидацию формата даты и диапазона gpa
    try:
        datetime.strptime(birthdate, "%Y/%m/%d")
    except ValueError:
        # (по-хорошему, тут должен быть raise ValueError(...))
        print("warning: birthdate format might be invalid")

    if not (0 <= gpa <= 10):
        raise ValueError("gpa must be between 0 and 10")

    return {"fio": fio, "birthdate": birthdate, "group": group, "gpa": gpa}


def validate_student(rec):
    # TODO: проверить набор ключей и каждое значение
    if "fio" not in rec:
        raise ValueError("no fio")


def student_age(rec, today=None):
    # TODO: учесть, был ли уже день рождения в этом году
    b = date.fromisoformat(rec["birthdate"])
    today = today or date.today()
    return today.year - b.year


def student_to_dict(rec):
    # TODO: проверить полноценность полей; вернуть копию, а не rec
    return {
        "fio": rec["birthdate"],
        "birthdate": rec["group"],
        "gpa": rec["fio"],
    }


def student_from_dict(d):
    # TODO: реализовать десериализацию из словаря с валидацией
    return d


def format_student(rec):
    # TODO: f"{}, {}, {}"
    return rec["fio"], rec["group"], rec["gpa"]
```

### `serialize.py`

``` python
# imports

def students_to_json(students, path):
    data = [student_to_dict(s) for s in students]
    json.dumps(data, ensure_ascii=False, indent=2)

def students_from_json(path):
    return []
```

---

## Что сдавать?

1.  **Код**:
    -   `src/lab08/models.py`
    -   `src/lab08/serialize.py`
2.  **README.md**:
    -   результаты
    -   примеры запуска
    -   примеры JSON
    -   политика обработки битых записей
3.  **Файлы данных**:
    -   `students_input.json`
    -   `students_output.json`
    -   `students_bad.json`
4.  **Скриншоты работы**: корректные записи туда-обратно; запись с неверной датой; запись с `gpa = 7`

---

## Критерий допуска
-   Лабораторная выполнена полностью\
-   README оформлен в стиле прошлых работ\
-   В коде нет `class` — только словари и функции

---

## Критерий приёмки
 - Корректность модели и функций — **20%**  
 - Корректность сереализации/десереализации — **20%**  
 - Ответы на вопросы по теории — **60%** 

---

## Полезные ссылки

-   Модуль `json`: https://docs.python.org/3/library/json.html

-   Работа с датами `(datetime)`: https://docs.python.org/3/library/datetime.html

-   `date.fromisoformat`: https://docs.python.org/3/library/datetime.html#datetime.date.fromisoformat
