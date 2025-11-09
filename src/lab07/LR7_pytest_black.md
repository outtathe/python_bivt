# ЛР7 — Тестирование: pytest + стиль (black)

> **Цель:** научиться писать модульные тесты на `pytest`, измерять покрытие и поддерживать единый стиль кода (`black`).  
> **Связь:** тестируем функции из `src/lib/text.py` (ЛР3) и `src/lab05/json_csv.py` (ЛР5).

---

## Результат ЛР
- Папка `tests/` с автотестами для:
  - `normalize`, `tokenize`, `count_freq`, `top_n` из `src/lib/text.py` (ЛР3);
  - `json_to_csv`, `csv_to_json` из `src/lab05/json_csv.py` (ЛР5).
- Конфиги: `pytest.ini`, `pyproject.toml` (для black).
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
|   ├── samples
│   └── out
├─ images
└─ pyproject.toml                  # Конфигурационный файл
```

---

## Теоретическая часть

## Что такое модуль в Python
**Модуль** — это обычный Python-файл (`.py`), который содержит функции, классы или переменные, и который можно **импортировать** в другие части программы.  
Он помогает разбивать код на **логические части** и **повторно использовать** уже написанные компоненты.

Например:
```python
# text_utils.py
def count_words(text):
    return len(text.split())
```

Теперь этот файл можно использовать как модуль:
```python
import text_utils

print(text_utils.count_words("Привет мир"))  # 2
```
Такой способ импорта отлично работает, если проект небольшой и состоит из пары файлов.
Но что, если у нас десятки модулей, сгруппированных по темам — например, обработка текста, файловые конвертеры и т.д.? (`../lab05/json_csv.py` и `../lib/text.py`)

Тогда логично объединить их в **пакеты**. Пакет — это не один файл, а целая папка с несколькими связанными модулями. Для этого был придуман...

## `__init__.py`. Что он делает и зачем он нужен?

Чтобы Python понял, что перед ним **пакет**, а не просто папка,  
в ней должен быть файл `__init__.py`.  
Он может быть пустым — достаточно просто его наличия.  
Этот файл говорит интерпретатору:  
> «Эта директория — часть Python-проекта, и из неё можно импортировать модули».

Пример структуры:
```
src/
└─ lib/
   ├─ __init__.py
   └─text.py
```

Теперь можно импортировать код сразу из пакета:

```python
from src.lib import text
from src.lib.text import normalize
```

Таким образом, `__init__.py` превращает набор отдельных модулей в **единую библиотеку**,  
из которой можно удобно импортировать нужные части.  
Если его убрать, Python не будет считать папку пакетом, и импорт из неё перестанет работать.

**Полезные ссылки:**
- [Официальная документация Python — Модули и пакеты](https://docs.python.org/3/tutorial/modules.html)
- [PEP 420 — Implicit Namespace Packages (об особенностях пакетов без `__init__.py`)](https://peps.python.org/pep-0420/)

---

## Задание

### A. Тесты к `src/lib/text.py`
Покрыть тестами все публичные функции модуля `text.py` (ЛР3): `normalize`, `tokenize`, `count_freq`, `top_n`.

### B. Тесты к `src/lab05/json_csv.py`
Написать тесты для `json_to_csv` и `csv_to_json` (ЛР5):
- позитивные сценарии: корректная конвертация, совпадение количества записей, ключей/заголовков;
- негативные сценарии: пустой JSON/CSV → `ValueError`, отсутствующий файл → `FileNotFoundError`.

### C. Стиль
- Прогон `black --check .` обязателен.  
- (Опционально) `ruff check .` — рекомендуется.

### ★ Дополнительно (со звёздочкой)
- Запустить `pytest --cov=src --cov-report=term-missing`.

---

## Пример кода

### 1) `pytest.ini`
```ini
[pytest]
addopts = -q
testpaths = tests
```

### 2) `pyproject.toml`
```toml
[tool.black]
line-length = 88
target-version = ["py311"]
exclude = ["venv", ".venv", "data", "images"]

[tool.ruff]
line-length = 88
target-version = "py311"
extend-exclude = ["venv", ".venv", "data", "images"]
select = ["E", "F", "I"]
ignore = ["E501"]
```

### 3) `tests/test_text.py`
```python
import pytest
from src.lib.text import normalize, tokenize, count_freq, top_n

@pytest.mark.parametrize(
    "src,expected",
    [
        ("ПрИвЕт\nМИр\t", "привет мир"),
        ("ёжик, Ёлка", "ежик, елка"),
        ("Hello\r\nWorld", "hello world"),
        ("  двойные   пробелы  ", "двойные пробелы"),
    ],
)
def test_normalize(src, expected):
    assert normalize(src) == expected

@pytest.mark.parametrize(
    "src,expected",
    [
        ("привет мир", ["привет", "мир"]),
        ("hello,world!!!", ["hello", "world"]),
        ("по-настоящему круто", ["по-настоящему", "круто"]),
        ("2025 год", ["2025", "год"]),
        ("emoji 😀 не слово", ["emoji", "не", "слово"]),
    ],
)
def test_tokenize(src, expected):
    assert tokenize(src) == expected

def test_count_and_top():
    tokens = ["a","b","a","c","b","a"]
    freq = count_freq(tokens)
    assert freq == {"a":3, "b":2, "c":1}
    assert top_n(freq, 2) == [("a",3), ("b",2)]

def test_top_tie_breaker():
    freq = count_freq(["bb","aa","bb","aa","cc"])
    assert top_n(freq, 2) == [("aa",2), ("bb",2)]
```

### 4) `tests/test_json_csv.py`
```python
import json, csv
from pathlib import Path
import pytest
from src.lab05.json_csv import json_to_csv, csv_to_json

def write_json(path: Path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")

def read_csv_rows(path: Path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))

def test_json_to_csv_roundtrip(tmp_path: Path):
    src = tmp_path / "people.json"
    dst = tmp_path / "people.csv"
    data = [{"name": "Alice", "age": 22}, {"name": "Bob", "age": 25}]
    write_json(src, data)

    json_to_csv(str(src), str(dst))
    rows = read_csv_rows(dst)
    assert len(rows) == 2
    assert set(rows[0]) >= {"name", "age"}

def test_csv_to_json_roundtrip(tmp_path: Path):
    src = tmp_path / "people.csv"
    dst = tmp_path / "people.json"
    src.write_text("name,age\nAlice,22\nBob,25\n", encoding="utf-8")

    csv_to_json(str(src), str(dst))
    obj = json.loads(dst.read_text(encoding="utf-8"))
    assert isinstance(obj, list) and len(obj) == 2
    assert set(obj[0]) == {"name", "age"}

def test_json_to_csv_empty_raises(tmp_path: Path):
    src = tmp_path / "empty.json"
    src.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError):
        json_to_csv(str(src), str(tmp_path / "out.csv"))

def test_csv_to_json_no_header_raises(tmp_path: Path):
    src = tmp_path / "bad.csv"
    src.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        csv_to_json(str(src), str(tmp_path / "out.json"))

def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        csv_to_json("nope.csv", "out.json")
```

---

## Сценарий демонстрации
1. `pytest -q`
2. `black --check .`
3. `pytest --cov=src --cov-report=term-missing -q`

---

## Что сдавать
1. Код: `tests/`, `pytest.ini`, `pyproject.toml`.
2. Исходники `src/lib/text.py`, `src/lab05/json_csv.py`.
3. Скриншоты/логи прогонов.
4. `README.md` для ЛР7 с командами запуска и примерами вывода.

---

## Критерий допуска
- Есть тесты ко всем функциям.
- Проверка стиля проходит.
- Скриншоты/логи приложены.

## Критерий приёмки
- **Корректность тестов** — 40%
- **Корректность функций** — 40%
- **Качество проекта** — 20%
- **(★)** Покрытие `--cov` приложено.
