"""Data model for a single expense."""
from dataclasses import dataclass, asdict


@dataclass
class Expense:
    id: int
    amount: float
    category: str
    note: str
    date: str  # stored as YYYY-MM-DD

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        return cls(
            id=int(data["id"]),
            amount=float(data["amount"]),
            category=str(data["category"]),
            note=str(data.get("note", "")),
            date=str(data["date"]),
        )
