"""Output: console table, CSV export, and Matplotlib pie chart."""
import csv
import os
from typing import Dict, List

from models import Expense


def print_table(expenses: List[Expense]) -> None:
    if not expenses:
        print("No expenses found.")
        return
    header = f"{'ID':<4} {'Date':<12} {'Category':<14} {'Amount (Rs)':>12}  Note"
    print(header)
    print("-" * len(header))
    for e in expenses:
        print(f"{e.id:<4} {e.date:<12} {e.category:<14} {e.amount:>12.2f}  {e.note}")
    print("-" * len(header))
    print(f"{'Total':<32}{sum(x.amount for x in expenses):>12.2f}")


def print_summary(totals: Dict[str, float]) -> None:
    if not totals:
        print("No expenses to summarise.")
        return
    grand = sum(totals.values())
    print(f"{'Category':<16}{'Total':>10}{'Share':>9}")
    print("-" * 35)
    for category, amount in totals.items():
        print(f"{category:<16}{amount:>10.2f}{amount / grand * 100:>8.1f}%")
    print("-" * 35)
    print(f"{'Grand total':<16}{grand:>10.2f}")


def export_csv(expenses: List[Expense], path: str) -> str:
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "date", "category", "amount", "note"])
        for e in expenses:
            writer.writerow([e.id, e.date, e.category, e.amount, e.note])
    return path


def plot_pie(totals: Dict[str, float], save_path: str = None) -> None:
    """Show a pie chart, or save it to a file if save_path is given."""
    import matplotlib
    if save_path:
        matplotlib.use("Agg")  # no GUI needed when only saving
    import matplotlib.pyplot as plt

    if not totals:
        print("No expenses to plot.")
        return
    plt.figure(figsize=(6, 6))
    plt.pie(list(totals.values()), labels=list(totals.keys()),
            autopct="%1.1f%%", startangle=140)
    plt.title("Expenses by Category")
    plt.tight_layout()
    if save_path:
        folder = os.path.dirname(save_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        plt.savefig(save_path, dpi=150)
        print(f"Chart saved to {save_path}")
    else:
        plt.show()
    plt.close()
