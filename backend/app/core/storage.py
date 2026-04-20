import json
from copy import deepcopy
from pathlib import Path
from threading import Lock
from typing import Any

from backend.app.core.config import DATA_FILE


DEFAULT_DATA: dict[str, list[dict[str, Any]]] = {
    "transactions": [
        {
            "id": "seed-paycheck",
            "date": "2026-04-01",
            "description": "Paycheck",
            "category": "Income",
            "amount": 3200.00,
            "kind": "income",
        },
        {
            "id": "seed-rent",
            "date": "2026-04-03",
            "description": "Rent",
            "category": "Housing",
            "amount": 1200.00,
            "kind": "expense",
        },
        {
            "id": "seed-groceries",
            "date": "2026-04-07",
            "description": "Groceries",
            "category": "Food",
            "amount": 168.45,
            "kind": "expense",
        },
    ],
    "budgets": [
        {"id": "seed-food-budget", "category": "Food", "monthly_limit": 500.00},
        {"id": "seed-housing-budget", "category": "Housing", "monthly_limit": 1300.00},
        {"id": "seed-transport-budget", "category": "Transport", "monthly_limit": 250.00},
    ],
    "goals": [
        {
            "id": "seed-emergency-goal",
            "name": "Emergency fund",
            "target_amount": 5000.00,
            "saved_amount": 850.00,
        }
    ],
    "recurring_items": [
        {
            "id": "seed-rent-recurring",
            "description": "Rent",
            "category": "Housing",
            "amount": 1200.00,
            "kind": "expense",
            "day_of_month": 3,
        }
    ],
}


class JsonStore:
    def __init__(self, path: Path = DATA_FILE) -> None:
        self.path = path
        self._lock = Lock()

    def read(self) -> dict[str, list[dict[str, Any]]]:
        with self._lock:
            self._ensure_file()
            with self.path.open("r", encoding="utf-8") as file:
                return json.load(file)

    def write(self, data: dict[str, list[dict[str, Any]]]) -> None:
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=2)

    def _ensure_file(self) -> None:
        if self.path.exists():
            return

        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(deepcopy(DEFAULT_DATA), file, indent=2)


store = JsonStore()
