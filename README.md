# Auto Apply AI

A Python 3.13 project using UV for dependency management.

## Setup

This project uses Python 3.13.0rc2 and UV for package management.

### Prerequisites

- Python 3.13.0rc2 (installed via pyenv)
- UV package manager

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Install development dependencies:
   ```bash
   uv sync --extra dev
   ```
4. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

### Dependencies

**Main Dependencies:**
- FastAPI - Web framework
- Pydantic Settings - Settings management
- SQLAlchemy - Database ORM
- HTTPX - HTTP client
- BeautifulSoup4 - HTML parsing
- AnyIO - Async I/O utilities
- AIOSQLite - Async SQLite

**Development Dependencies:**
- Pytest - Testing framework
- Pytest-asyncio - Async testing support
- Ruff - Fast Python linter
- MyPy - Static type checker

## Development Tools

This project includes several development tools:

### Testing with pytest

Run tests:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

### Code Quality with Ruff

Check code quality:
```bash
ruff check .
```

Auto-fix issues:
```bash
ruff check --fix .
```

### Type Checking with MyPy

Note: MyPy has known compatibility issues with Python 3.13. The module can be imported but the CLI may not work correctly.

## Project Structure

```
auto-apply-ai/
├── .venv/              # Virtual environment
├── src/                # Source code
│   └── auto_apply_ai/  # Main package
│       ├── __init__.py
│       └── main.py
├── tests/              # Test files
│   └── test_hello.py
├── main.py             # Entry point script
├── pyproject.toml      # Project configuration
└── README.md           # This file
```

## Running the Application

```bash
python main.py
```

Or run the module directly:
```bash
python -m auto_apply_ai.main
```

IDEA for decisions

I am using SQL DB as of now I will have to test it how it is doing to work. My idea is that i dont want to just give the LLM whole resume and job description and do the matching and changing based on the Similarly, I felt that taking data in structures and matching it in section by section will make more precise and efficient.