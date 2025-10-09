# ЛР5 — JSON и конвертации (JSON↔CSV, CSV→XLSX): Техническое задание

> **Цель:** Разобраться с форматом JSON, сериализацией/десериализацией и табличными конвертациями.  
> **Связь:** продолжение ЛР4 (работа с файлами) и подготовка базы для ЛР6 (CLI-конвертеры) и ЛР7 (тестирование).

---

## Результат ЛР
- Модуль `src/lab05/json_csv.py` с чистыми функциями:  
  - `json_to_csv(json_path, csv_path)`  
  - `csv_to_json(csv_path, json_path)`  
  (без вывода в stdout, только работа с файлами; валидация ошибок).

- Модуль `src/lab05/cvs_xlsx.py` с функцией  
  - `csv_to_xlsx(csv_path, xlsx_path)`  
  (через **openpyxl** или **xlsxwriter**, авто-ширина колонок).

- Примеры данных в `data/samples/` и артефакты конвертаций в `data/out/`:
  - `people.json` ⇄ `people_from_json.csv`
  - `people.csv` ⇄ `people_from_csv.json`
  - `people.xlsx` (из любого CSV)

- `README.md` с командами запуска, описанием форматов, допущений и скриншотами проверки XLSX.

- `requirements.txt` с одной зависимостью (**openpyxl** или **xlsxwriter**).  
  Всё остальное — стандартная библиотека (`json`, `csv`, `pathlib`).  
  Python **3.хх+**.

---

## Теоретическая часть

### Что такое JSON
**JSON (JavaScript Object Notation)** — текстовый формат для обмена структурированными данными.  
Хранит объекты и списки, используется для сериализации и API.  

**Пример:**
```json
[
  {"name": "Alice", "age": 22},
  {"name": "Bob", "age": 25}
]
```

Python-модуль `json`:
- `json.load(f)` — загрузить из файла;
- `json.dump(obj, f, ensure_ascii=False, indent=2)` — записать в файл;
- `json.loads(s)` / `json.dumps(obj)` — работа со строками.

---

### Что такое CSV
**CSV (Comma-Separated Values)** — табличный текстовый формат, где значения разделены запятыми или `;`.

**Пример:**
```csv
name,age,city
Alice,22,SPB
Bob,25,Moscow
```

Python-модуль `csv`:
- `csv.DictReader(f)` — читает CSV как список словарей;
- `csv.DictWriter(f, fieldnames=...)` — записывает список словарей;
- `csv.Sniffer()` — автоопределение разделителя.

---

### JSON ↔ CSV ↔ XLSX
- JSON хранит **объекты** и **списки**.  
- CSV — **таблицы** (строки и колонки).  
- XLSX — **формат Excel**.  

Конвертация:
- JSON → CSV: объединение ключей → столбцы.  
- CSV → JSON: каждая строка → словарь.  
- CSV → XLSX: перенос строк в лист Excel, установка ширины колонок.

---

## Примеры кода

### Пример 1. JSON чтение и запись
```python
import json
from pathlib import Path

data = [{"name": "Alice", "age": 22}, {"name": "Bob", "age": 25}]
path = Path("data/out/people.json")

with path.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with path.open(encoding="utf-8") as f:
    print(json.load(f))
```

### Пример 2. Работа с CSV
```python
import csv

rows = [
    {"name": "Alice", "age": "22", "city": "SPB"},
    {"name": "Bob", "age": "25", "city": "Moscow"}
]

with open("data/out/people.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
    writer.writeheader()
    writer.writerows(rows)

with open("data/out/people.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
```

### Пример 3. CSV → XLSX через openpyxl
```python
from openpyxl import Workbook
import csv

wb = Workbook()
ws = wb.active
ws.title = "Sheet1"

with open("data/samples/people.csv", encoding="utf-8") as f:
    for row in csv.reader(f):
        ws.append(row)

for col in ws.columns:
    max_len = max(len(str(cell.value)) if cell.value else 0 for cell in col)
    ws.column_dimensions[col[0].column_letter].width = max(max_len + 2, 8)

wb.save("data/out/people.xlsx")
```

### Пример 4. JSON → CSV
```python
import json, csv

with open("data/samples/people.json", encoding="utf-8") as jf:
    data = json.load(jf)

fieldnames = sorted(set().union(*[d.keys() for d in data]))

with open("data/out/people_from_json.csv", "w", newline="", encoding="utf-8") as cf:
    writer = csv.DictWriter(cf, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
```

---

## Проверка и валидация
- Пустой JSON → `ValueError("Пустой JSON или неподдерживаемая структура")`  
- Список с не-словарами → `ValueError`  
- CSV без заголовка или пустой → `ValueError`  
- CSV отсутствует → ошибка при открытии.  
- Проверка: количество записей совпадает до и после конвертации.

---

## Набор данных и примеры
Для вашго удобства подготовлены мини-наборы:
- `data/samples/people.json` — список объектов одинаковой формы 
- `data/samples/people.csv` — CSV с теми же данными (для проверки обратимого преобразования).
- `data/samples/cities.csv` — CSV с 2–3 колонками для демонстрации CSV→XLSX.

От вас также требуется подготовить по 1 примеру файлов для каждого сценария.

**Сценарии демонстрации (описываются в README):**
1. JSON→CSV → проверка заголовка и количества строк.
2. CSV→JSON → сравнение ключей и количества объектов.
3. CSV→XLSX → открываем файл в Excel/LibreOffice, проверяем лист и ширины колонок.


## Что сдавать
1. Код в `src/lab05/*`.
2. Файлы для демонстрации работы  в `data/out/*` и `data/samples/*`.  
3. `README.md` с командами запуска сценариев, пояснениями, скриншотами результатов.  

## Критерии допуска
- Лабораторная работа **выполнена на 100%**
- Оформлен отчет в README-файле по примеру **effective-broccoli**

## Критерии приемки
- Корректность функций и формат ввода/вывода — **20%**  
- Корректность тест-кейсов, покрытие всех случаев — **20%%**  
- Качество ответов на вопросы по лабе — **60%**  