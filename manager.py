"""Business logic: validation, add/delete/filter, and summaries."""
from collections import defaultdict
from datetime import datetime, date as date_cls
from typing import Dict, List, Optional

from models import Expense
from storage import JsonStorage


class ValidationError(ValueError):
    """Raised for invalid user input."""


class ExpenseManager:
    def __init__(self, storage: JsonStorage):
        self.storage = storage
        self.expenses: List[Expense] = storage.load()

    # ---------- helpers ----------
    @staticmethod
    def _parse_date(value: Optional[str]) -> str:
        if not value:
            return date_cls.today().isoformat()
        try:
            return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
        except ValueError:
            raise ValidationError("Date must be in YYYY-MM-DD format.")

    def _next_id(self) -> int:
        return max((e.id for e in self.expenses), default=0) + 1

    # ---------- operations ----------
    def add(self, amount: float, category: str, note: str = "",
            date: Optional[str] = None) -> Expense:
        if amount <= 0:
            raise ValidationError("Amount must be greater than 0.")
        category = category.strip().title()
        if not category:
            raise ValidationError("Category cannot be empty.")
        expense = Expense(self._next_id(), round(amount, 2), category,
                          note.strip(), self._parse_date(date))
        self.expenses.append(expense)
        self.storage.save(self.expenses)
        return expense

    def delete(self, expense_id: int) -> Expense:
        for expense in self.expenses:
            if expense.id == expense_id:
                self.expenses.remove(expense)
                self.storage.save(self.expenses)
                return expense
        raise ValidationError(f"No expense found with id {expense_id}.")

    def filter(self, category: Optional[str] = None,
               month: Optional[str] = None) -> List[Expense]:
        """month format: YYYY-MM"""
        result = self.expenses
        if category:
            result = [e for e in result if e.category.lower() == category.lower()]
        if month:
            result = [e for e in result if e.date.startswith(month)]
        return sorted(result, key=lambda e: (e.date, e.id))

    @staticmethod
    def total(expenses: List[Expense]) -> float:
        return round(sum(e.amount for e in expenses), 2)

    @staticmethod
    def by_category(expenses: List[Expense]) -> Dict[str, float]:
        totals: Dict[str, float] = defaultdict(float)
        for e in expenses:
            totals[e.category] += e.amount
        return {k: round(v, 2) for k, v in
                sorted(totals.items(), key=lambda kv: kv[1], reverse=True)}
