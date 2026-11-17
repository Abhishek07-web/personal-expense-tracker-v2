# Personal Expense Tracker (CLI)

A modular Python command-line app (interactive menu + direct commands) to record, filter, summarise, chart and export personal expenses. Data is stored in JSON with crash-safe writes; business logic is separated from storage and output, and covered by unit tests.

## Features
- Add / list / delete expenses with input validation (positive amount, `YYYY-MM-DD` dates)
- Filter by category or month (`YYYY-MM`)
- Category-wise summary with percentage share
- Matplotlib pie chart (show or save as PNG)
- CSV export
- Atomic JSON saves + clear error for corrupted data files
- 7 unit tests (`unittest`)

## Setup
```bash
pip install -r requirements.txt
python main.py add 250 food "Lunch with team"
```

## Usage
Interactive menu (add, view, total, summary, CSV export, chart, delete):
```bash
python main.py
```
Or direct commands:
```bash
python main.py add 1200 travel "Train tickets" --date 2026-11-05
python main.py list --month 2026-11
python main.py list --category food
python main.py summary
python main.py chart --save output/pie.png
python main.py export output/expenses.csv
python main.py delete 2
```

## Run tests
```bash
python -m unittest -v
```

## Project structure
| File | Responsibility |
|---|---|
| `main.py` | Entry point: no arguments -> menu; otherwise argparse commands; prints errors cleanly |
| `menu.py` | Interactive menu loop (input prompts, DD-MM-YYYY dates) |
| `models.py` | `Expense` dataclass + dict conversion |
| `storage.py` | JSON load/save, atomic write (temp file + `os.replace`), `StorageError` |
| `manager.py` | Validation, add/delete/filter, totals, category summary |
| `reports.py` | Console tables, CSV export, pie chart |
| `test_manager.py` | Unit tests for logic and storage |

## Design decisions
- **Layered design:** UI (`main.py`) -> logic (`manager.py`) -> storage (`storage.py`); each layer can change independently (e.g., swap JSON for SQLite).
- **Atomic writes:** data is written to a temp file and then renamed, so a crash cannot corrupt `expenses.json`.
- **IDs:** `max(id) + 1`, so IDs are never reused after deleting the latest record.
- **Money:** amounts rounded to 2 decimals; stored dates are ISO strings so month filtering is a simple prefix match.

## Troubleshooting
| Problem | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: matplotlib` | Dependencies not installed | `pip install -r requirements.txt` |
| `Error: Data file ... is corrupted` | JSON edited by hand or damaged | Fix the file, or delete `data/expenses.json` to start fresh |
| `Date must be in YYYY-MM-DD format` | Wrong date format | Use e.g. `--date 2026-11-05` |
| Chart window doesn't open (server/WSL) | No display available | Use `chart --save output/pie.png` |
| `ModuleNotFoundError: manager` | Running from another folder | `cd` into the project folder first |

## Improvements over the first version
- Single script split into modules (models / storage / logic / reports / menu)
- Fixed data-loss bug: the original saved to `expenses.json` but loaded from `expense.json`, so data vanished on restart
- Dates are validated and stored as ISO `YYYY-MM-DD` (the first version accepted any text, e.g. `02-20-26`)
- Amount validation, delete command, month/category filters, unit tests

## Future improvements
SQLite backend, monthly budget alerts, edit command, bar chart of monthly trends.
