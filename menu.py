"""Interactive menu mode (run `python main.py` with no arguments)."""
from datetime import datetime

from manager import ExpenseManager, ValidationError
from storage import StorageError
import reports

MENU = """
---- Personal Expense Tracker ----
1. Add Expense
2. View Expenses
3. Total Expense
4. Category Summary
5. Export to CSV
6. Show Expense Chart
7. Delete Expense
8. Exit"""


def _ask_date() -> str:
    """Ask for DD-MM-YYYY; blank means today. Returns ISO date or ''."""
    raw = input("Date (DD-MM-YYYY, blank = today): ").strip()
    if not raw:
        return ""
    try:
        return datetime.strptime(raw, "%d-%m-%Y").date().isoformat()
    except ValueError:
        raise ValidationError("Date must be in DD-MM-YYYY format.")


def _add(manager: ExpenseManager) -> None:
    date = _ask_date()
    category = input("Category (Food, Travel, etc.): ")
    try:
        amount = float(input("Amount: "))
    except ValueError:
        raise ValidationError("Please enter a valid number for amount.")
    note = input("Note (optional): ")
    e = manager.add(amount, category, note, date)
    print(f"Added #{e.id}: Rs {e.amount:.2f} on {e.category} ({e.date})")


def _delete(manager: ExpenseManager) -> None:
    try:
        expense_id = int(input("ID to delete: "))
    except ValueError:
        raise ValidationError("ID must be a number.")
    e = manager.delete(expense_id)
    print(f"Deleted #{e.id}: Rs {e.amount:.2f} {e.category}")


def run_menu(manager: ExpenseManager) -> None:
    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()
        try:
            if choice == "1":
                _add(manager)
            elif choice == "2":
                reports.print_table(manager.filter())
            elif choice == "3":
                print(f"Total expenses: Rs {manager.total(manager.expenses):.2f}")
            elif choice == "4":
                reports.print_summary(manager.by_category(manager.expenses))
            elif choice == "5":
                print(f"Exported to {reports.export_csv(manager.filter(), 'output/expenses.csv')}")
            elif choice == "6":
                reports.plot_pie(manager.by_category(manager.expenses))
            elif choice == "7":
                _delete(manager)
            elif choice == "8":
                print("Goodbye, have a nice day!")
                break
            else:
                print("Invalid choice, try again.")
        except (ValidationError, StorageError) as exc:
            print(f"Error: {exc}")
