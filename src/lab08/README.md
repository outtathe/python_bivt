# ЛР8 – ООП в Python: `@dataclass Student`, методы и сериализация

> **Цель:** изучить основы объектно-ориентированного программирования в Python,
> научиться описывать модели данных с помощью @dataclass, реализовывать методы 
> и валидацию, сериализовывать/десериализовывать объекты.\
> **Связь:** продолжаем работу с файлами и сериализацией из ЛР5, логику структуры 
> и оформления наследуем из предыдущих ЛР.
> Основная задача — реализовать полноценную модель студента, экспорт/импорт в JSON и корректные
> методы экземпляра.
___
## Результат ЛР

После выполнения ЛР8 в репозитории должны присутствовать:

### `src/lab08/models.py`
Модель **`Student`**, содержащая:

- декоратор `@dataclass`
- поля:
  - `fio`
  - `birthdate`
  - `group`
  - `gpa`
- методы:
  - `age()`
  - `to_dict()`
  - `from_dict()`
  - `__str__()`
- валидацию:
  - формата даты (`YYYY-MM-DD`)
  - диапазона среднего балла `0 ≤ gpa ≤ 5`

---

### `src/lab08/serialize.py`

Функции сериализации:

- `students_to_json(list[Student], path)`
- `students_from_json(path) -> list[Student]`

---

### `data/lab08/`

Должны находиться:

- пример входного JSON (`students_input.json`)
- пример выходного JSON (результат сериализации, `students_output.json`)

---

### `lab08/README.md`

Файл отчёта должен содержать:

- примеры запуска функций
- примеры JSON **до/после преобразования**
- описание структуры класса `Student` и логики его методов

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
│       └─ students_output.json
├─ images /
    └── lab08
```

---

## Теоретическая часть: краткая справка по ООП в Python

### Классы и объекты

Python — динамический язык, но отлично поддерживает ООП:

``` python
class A:
    def hello(self):
        return "hi"
```

### Инкапсуляция

Python использует соглашения: 
 - `_field`  – защищённое
 - `__field` – приватное (name mangling)

### Декоратор @dataclass
Автоматически создаёт: 
 - `__init__` 
 - `__repr__` 
 - `__eq__` 
 - (опционально) `order=True`, `frozen=True`

Пример:

``` python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
```

### Сериализация

Python → словарь → JSON:

``` python
import json
json.dumps(obj)
```

---

## Задание

### A. Реализовать класс `Student` (`models.py`)

### Поля:

| Поле       | Тип   | Описание                |
|------------|-------|--------------------------|
| `fio`      | `str` | ФИО студента             |
| `birthdate`| `str` | Формат `YYYY-MM-DD`      |
| `group`    | `str` | Группа, напр. `SE-01`    |
| `gpa`      | `float` | Средний балл 0…5       |

---

### Методы:

- `age()` — вернуть количество полных лет  
- `to_dict()` — сериализация  
- `from_dict()` — десериализация  
- `__str__()` — красивый вывод  

---

### Валидация в `__post_init__`:

- корректный формат даты  
- диапазон `gpa`
---

### B. Реализовать модуль `serialize.py`

#### `students_to_json(students, path)`

Сохраняет список студентов в JSON.

#### `students_from_json(path) -> list[Student]`

-   читает JSON-массив
-   валидирует
-   создаёт список `Student`

---

## Пример кода

### `models.py`

``` python
# imports

@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float

    def __post_init__(self):
        # TODO: добавить нормальную валидацию формата даты и диапазона gpa
        try:
            datetime.strptime(self.birthdate, "%Y/%m/%d")
        except ValueError:
            # (по-хорошему, тут должен быть raise ValueError(...))
            print("warning: birthdate format might be invalid")
        
        if not (0 <= self.gpa <= 10):
            raise ValueError("gpa must be between 0 and 10")

    def age(self) -> int:
        # TODO: добавить нормальную валидацию формата даты и диапазона gpa
        b = dself.birthdate
        today = date.today()
        return today.year - b.year

    def to_dict(self) -> dict:
        # TODO: проверить полноценность полей
        return {
            "fio": self.birthdate,
            "birthdate": self.group,
            "gpa": self.fio,
        }

    @classmethod
    def from_dict(cls, d: dict):
        # TODO: реализовать десереализацию из словаря
        return class

    def __str__(self):
        # TODO: f"{}, {}, {}"
        return self.fio, self.group, self.gpa
```

### `serialize.py`

``` python
# imports

def students_to_json(students, path):
    data = [s.to_dict() for s in students]
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
3.  **Файлы данных**:
    -   `students_input.json`
    -   `students_output.json`
4.  **Скриншоты работы**

---

## Критерий допуска
-   Лабораторная выполнена полностью\
-   README оформлен в стиле прошлых работ\

---

## Критерий приёмки
 - Корректность класса и методов — **20%**  
 - Корректность сереализации/десереализации — **20%**  
 - Ответы на вопросы по теории — **60%** 

---

## Полезные ссылки

-   Официальная документация `dataclasses`: https://docs.python.org/3/library/dataclasses.html

-   Модуль `json`: https://docs.python.org/3/library/json.html

-   Работа с датами `(datetime)`: https://docs.python.org/3/library/datetime.html
