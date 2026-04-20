import json
from pathlib import Path
from threading import Lock
from typing import Any

from backend.app.core.config import DATA_FILE


DEFAULT_DATA: dict[str, list[dict[str, Any]]] = {
    "transactions": [],
    "budgets": [],
    "goals": [],
    "recurring_items": [],
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
            json.dump(DEFAULT_DATA, file, indent=2)


store = JsonStore()
