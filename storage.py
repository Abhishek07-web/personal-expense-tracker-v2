"""JSON persistence layer with safe (atomic) writes."""
import json
import os
import tempfile
from typing import List

from models import Expense


class StorageError(Exception):
    """Raised when the data file cannot be read or written."""


class JsonStorage:
    def __init__(self, path: str = "data/expenses.json"):
        self.path = path

    def load(self) -> List[Expense]:
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            return [Expense.from_dict(item) for item in raw]
        except (json.JSONDecodeError, KeyError, ValueError, TypeError) as exc:
            raise StorageError(
                f"Data file '{self.path}' is corrupted ({exc}). "
                "Fix or delete it to start fresh."
            ) from exc

    def save(self, expenses: List[Expense]) -> None:
        folder = os.path.dirname(self.path) or "."
        os.makedirs(folder, exist_ok=True)
        # Write to a temp file first, then replace: a crash mid-write
        # can never leave a half-written (corrupt) expenses.json.
        fd, tmp_path = tempfile.mkstemp(dir=folder, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump([e.to_dict() for e in expenses], f, indent=2)
            os.replace(tmp_path, self.path)
        except OSError as exc:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise StorageError(f"Could not save data: {exc}") from exc
