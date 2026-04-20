# Budgeting App

A small modular budgeting app with a Python FastAPI backend and a static frontend.

## Features

- Dashboard with income, expenses, remaining monthly budget, and savings progress
- Transaction tracking with categories and income/expense types
- Monthly category budgets
- Savings goals
- Recurring bills and income reminders
- JSON file persistence for simple local development

## Project Structure

```text
backend/
  app/
    api/          API route modules
    core/         App settings and storage helpers
    services/     Budget calculations and data operations
    main.py       FastAPI app entrypoint
frontend/
  static/
    css/
    js/
    index.html
tests/
```

## Run Locally

Create a virtual environment, install dependencies, and start the backend:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

The app stores local data in `data/budget_data.json`.

## Run Tests

```powershell
pytest
```
