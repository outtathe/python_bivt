# ЛР7 — Тестирование: pytest + стиль (black)

> **Цель:** научиться писать модульные тесты на `pytest`, измерять покрытие и поддерживать единый стиль кода (`black`).  
> **Связь:** тестируем функции из `src/lib/text.py` (ЛР3) и `src/lab05/json_csv.py` (ЛР5).

---

## Результат ЛР
- Папка `tests/` с автотестами для:
  - `normalize`, `tokenize`, `count_freq`, `top_n` из `src/lib/text.py` (ЛР3);
  - `json_to_csv`, `csv_to_json` из `src/lab05/json_csv.py` (ЛР5).
- Конфиг: `pyproject.toml`.
- Скриншоты/вывод успешного прогона тестов и проверок стиля.
- (★) Отчёт покрытия `pytest --cov` (вывод в терминал).

---

## Структура репозитория (рекомендация)
```
python_labs/
├─ README.md                        # Общий отчет
├─ src/
│   ├─ lib/
│   │   └─ text.py
│   ├─ lab05/
│   │   └─ json_csv.py
│   └─ lab07/
│       └─ README.md                # Отчет по ЛР7            
├─ tests/
│   ├─ test_text.py                 # Автотесты для text.py
│   └─ test_json_csv.py             # Автотесты для json_csv.py
├─ data/
│   ├── samples
│   └── out
├─ images
└─ pyproject.toml                  # Конфигурационный файл
```

---

## Теоретическая часть

Данный блок был вынесен в отдельный файлик -> [клииик](./THEORY.md)

---

## Задание

### 0. Модули или нет?

Для удобства тестирования наших функций как модулей **рекомендуется** перевод проекта на модульную структуру. Но **в вашем праве** использовать старые способы запуска/импорта проектов. 

### A. Тесты для `src/lib/text.py`

Написать автотесты для всех публичных функций модуля:

- `normalize(text: str) -> str`
- `tokenize(text: str) -> list[str]`
- `count_freq(tokens: list[str]) -> dict[str, int]`
- `top_n(freq: dict[str, int], n: int) -> list[tuple[str, int]]`

**Требования:**

- покрыть как минимум:
  - базовые случаи (обычный текст),
  - граничные случаи (пустые строки, повторы, спецсимволы),
  - сценарий с одинаковой частотой слов (проверка сортировки по алфавиту при равных значениях);
- использовать `pytest`, допускается параметризация (`@pytest.mark.parametrize`). [Что это такое?](./THEORY.md#параметризация)

---

### B. Тесты для `src/lab05/json_csv.py`

Написать автотесты для функций:

- `json_to_csv(src_path: str, dst_path: str)`
- `csv_to_json(src_path: str, dst_path: str)`

**Позитивные сценарии:**

- корректная конвертация JSON → CSV и CSV → JSON;
- совпадает количество записей;
- совпадает набор ключей/заголовков (например, `name`, `age`).

**Негативные сценарии (минимум):**

- пустой или некорректный входной файл → ожидаем `ValueError`;
- несуществующий путь к файлу → ожидаем `FileNotFoundError`.

Рекомендуется использовать встроенную фикстуру `tmp_path` для работы с временными файлами. [Что это такое?](./THEORY.md#фикстура-для-файловой-системы)

---

### C. Стиль кода (`black`)

- перед сдачей ЛР:
    - отформатировать проект:
        ```bash
            black .
        ```
    - для самопроверки:
        ```bash
            black --check .
        ```
[Что такое стиль?](./THEORY.md#стиль)


### ★ Дополнительное задание: покрытие кода 

 - установить плагин `pytest-cov`;
 - запустить тесты с покрытием:
    ```python
        pytest --cov=src --cov-report=term-missing
    ```
 - проанализировать, какие строки/функции не покрыты тестами.

---

## Пример кода

Пример тестов для `normalize.py`
`tests/test_text.py`

```python
import pytest
from src.lib.text import normalize


@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\\nМИр\\t", "привет мир"),
        ("ёжик, Ёлка", "ежик, елка"),
        ("Hello\\r\\nWorld", "hello world"),
        ("  двойные   пробелы  ", "двойные пробелы"),
    ],
)
def test_normalize_basic(source, expected):
    assert normalize(source) == expected

def test_tokenize_basic(source, expected):
    # TODO: Реализовать тесты токенизации
    pass

def test_count_freq_and_top_n():
    # TODO: Реализовать тесты частоты
    pass

def test_top_n_tie_breaker():
    # TODO: Реализовать тесты для топ_н
    pass

```

Пример тестов для `json_csv.py`

`tests/test_json_csv.py`
``` python
import pytest
from src.lab05.json_csv import json_to_csv, csv_to_json


def test_json_to_csv_roundtrip(tmp_path: Path):
    src = tmp_path / "people.json"
    dst = tmp_path / "people.csv"
    data = [
        {"name": "Alice", "age": 22},
        {"name": "Bob", "age": 25},
    ]
    src.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    json_to_csv(str(src), str(dst))

    with dst.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert {"name", "age"} <= set(rows[0].keys())


def test_csv_to_json_roundtrip(tmp_path: Path):
    # TODO: Реализовать тесты для конвертации в другую сторону
    pass

#   Бро придумывай кейсы сам
#   и тд....

```

## Что сдавать?

1. Общий README
2. README для ЛР7
3. Тесты:
В директории `tests/` должны находиться:
 - `tests/test_text.py` – Тесты для всех функций из `src/lib/text.py`.
- `tests/test_json_csv.py` – Тесты для функций в `src/lab05/json_csv.py`.

4. Скриншоты выполнения команд/прогона тестов

## Критерии допуска
- Лабораторная работа **выполнена на 100%**
- Код сооветствует стилю `black`
- Оформлен отчет в README-файле по примеру **effective-broccoli**

## Критерии приёмки
- Тесты приустствуют для всех функций — **20%**  
- 100% результат на тестах — **20%**  
- Ответы на вопросы по теории — **60%** 
---

**Полезные ссылки:**
- [Официальная документация Python — Модули и пакеты](https://docs.python.org/3/tutorial/modules.html)
- [PEP 420 — Implicit Namespace Packages (об особенностях пакетов без `__init__.py`)](https://peps.python.org/pep-0420/)
- [PEP 518 — pyproject.toml](https://peps.python.org/pep-0518/)
- [Pytest: Configuration via pyproject.toml](https://docs.pytest.org/en/latest/reference/customize.html#configuration-file-formats)
 - [Pytest documentation](https://docs.pytest.org/en/stable/)
 - [Pytest: parametrize](https://docs.pytest.org/en/stable/example/parametrize.html)
 - [Pytest: fixture](https://docs.pytest.org/en/stable/explanation/fixtures.html)
---

