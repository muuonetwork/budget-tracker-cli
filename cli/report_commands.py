"""
cli/report_commands.py - summary and spending report for a user
"""

from utils.storage import load_transactions, load_categories, category_key
from utils.display import print_summary, print_error, print_info, console
from rich.table import Table
from rich import box


def register_report_commands(subparsers):
    p = subparsers.add_parser("summary", help="Show income/expense summary for a user")
    p.add_argument("--user", required=True, help="User name")
    p.set_defaults(func=cmd_summary)

    p2 = subparsers.add_parser("category-report", help="Show spending per category for a user")
    p2.add_argument("--user", required=True, help="User name")
    p2.set_defaults(func=cmd_category_report)


def cmd_summary(args):
    transactions = load_transactions()
    user_transactions = [t for t in transactions.values() if t.user_name == args.user]

    if not user_transactions:
        print_error(f"No transactions found for user '{args.user}'.")
        return

    income = sum(t.amount for t in user_transactions if t.transaction_type == "income")
    expenses = sum(t.amount for t in user_transactions if t.transaction_type == "expense")
    print_summary(income, expenses)


def cmd_category_report(args):
    transactions = load_transactions()
    categories = load_categories()

    user_cats = {k: v for k, v in categories.items() if v.user_name == args.user}
    if not user_cats:
        print_error(f"No categories found for user '{args.user}'.")
        return

    table = Table(title=f"📈 Category Report for {args.user}", box=box.ROUNDED)
    table.add_column("Category", style="bold yellow")
    table.add_column("Budget Limit", style="magenta")
    table.add_column("Total Spent", style="red")
    table.add_column("Total Income", style="green")
    table.add_column("Status", style="bold")

    for cat in user_cats.values():
        cat_transactions = [t for t in transactions.values()
                            if t.user_name == args.user and t.category_name == cat.name]
        spent = sum(t.amount for t in cat_transactions if t.transaction_type == "expense")
        earned = sum(t.amount for t in cat_transactions if t.transaction_type == "income")
        limit = cat.budget_limit

        if limit > 0:
            status = "[green]Under budget[/green]" if spent <= limit else "[red]Over budget![/red]"
            limit_str = f"KES {limit:,.2f}"
        else:
            status = "[dim]No limit set[/dim]"
            limit_str = "–"

        table.add_row(cat.name, limit_str, f"KES {spent:,.2f}", f"KES {earned:,.2f}", status)

    console.print(table)
