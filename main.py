"""Personal Expense Tracker - entry point.

Interactive menu:
    python main.py

Or direct commands:
    python main.py add 250 food "Lunch with team"
    python main.py list --month 2026-11
    python main.py summary
    python main.py chart --save output/pie.png
    python main.py export output/expenses.csv
    python main.py delete 3
"""
import argparse
import sys

from manager import ExpenseManager, ValidationError
from storage import JsonStorage, StorageError
import reports
from menu import run_menu


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Personal Expense Tracker")
    parser.add_argument("--data", default="data/expenses.json",
                        help="path to JSON data file")
    sub = parser.add_subparsers(dest="command")  # no command -> interactive menu

    add = sub.add_parser("add", help="add an expense")
    add.add_argument("amount", type=float)
    add.add_argument("category")
    add.add_argument("note", nargs="?", default="")
    add.add_argument("--date", help="YYYY-MM-DD (default: today)")

    lst = sub.add_parser("list", help="list expenses")
    lst.add_argument("--category")
    lst.add_argument("--month", help="YYYY-MM")

    dele = sub.add_parser("delete", help="delete an expense by id")
    dele.add_argument("id", type=int)

    summ = sub.add_parser("summary", help="category-wise totals")
    summ.add_argument("--month", help="YYYY-MM")

    chart = sub.add_parser("chart", help="pie chart of spending")
    chart.add_argument("--month", help="YYYY-MM")
    chart.add_argument("--save", help="save chart to this file instead of showing")

    exp = sub.add_parser("export", help="export to CSV")
    exp.add_argument("path", nargs="?", default="output/expenses.csv")
    return parser


def run(args: argparse.Namespace) -> None:
    manager = ExpenseManager(JsonStorage(args.data))

    if args.command is None:
        run_menu(manager)
    elif args.command == "add":
        e = manager.add(args.amount, args.category, args.note, args.date)
        print(f"Added #{e.id}: {e.amount:.2f} on {e.category} ({e.date})")
    elif args.command == "list":
        reports.print_table(manager.filter(args.category, args.month))
    elif args.command == "delete":
        e = manager.delete(args.id)
        print(f"Deleted #{e.id}: {e.amount:.2f} {e.category}")
    elif args.command == "summary":
        reports.print_summary(manager.by_category(manager.filter(month=args.month)))
    elif args.command == "chart":
        reports.plot_pie(manager.by_category(manager.filter(month=args.month)),
                         args.save)
    elif args.command == "export":
        path = reports.export_csv(manager.filter(), args.path)
        print(f"Exported to {path}")


def main() -> int:
    args = build_parser().parse_args()
    try:
        run(args)
    except (ValidationError, StorageError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
