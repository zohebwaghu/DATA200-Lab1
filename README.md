## CheckMyGrade (DATA 200 - Lab 1)

Strict, testable, object-oriented Python implementation with CSV persistence,
reversible demo-grade password encryption, search/sort timings, statistics, and CLI.

Important: The included password encryption is for demonstration only and is NOT secure.
Do not reuse for real credentials.

### Setup
- Python 3.10+
- No external dependencies required

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Run
```bash
python main.py
```

CSV files are created under `data/` on first run.

### Tests
```bash
python -m unittest -v
```

### Structure
- `checkmygrade/models.py`: Data classes
- `checkmygrade/storage.py`: CSV repositories
- `checkmygrade/services.py`: Domain logic (CRUD, search, sort, stats, reports)
- `checkmygrade/crypto.py`: Reversible demo-grade encryption
- `checkmygrade/cli.py`: Console UI
- `main.py`: Entry point
- `tests/test_app.py`: Unit tests (incl. 1000-record scenarios)

### Academic Integrity
- This code is original and written for this assignment specification.
- If you reuse any part, cite appropriately; plagiarism tolerance is 0%.
