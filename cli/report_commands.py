"""
cli/report_commands.py - summary and spending report for a user (click version)
"""
import click

from utils.storage import load_transactions, load_categories
from utils.display import print_summary, print_error, console
from rich.table import Table
from rich import box


@click.command("summary")
@click.option("--user", required=True, help="User name")
def summary(user):
    """Show income/expense summary for a user."""
    transactions = load_transactions()
    user_transactions = [t for t in transactions.values() if t.user_name == user]

    if not user_transactions:
        print_error(f"No transactions found for user '{user}'.")
        return

    income = sum(t.amount for t in user_transactions if t.transaction_type == "income")
    expenses = sum(t.amount for t in user_transactions if t.transaction_type == "expense")
    print_summary(income, expenses)


@click.command("category-report")
@click.option("--user", required=True, help="User name")
def category_report(user):
    """Show spending per category for a user."""
    transactions = load_transactions()
    categories = load_categories()

    user_cats = {k: v for k, v in categories.items() if v.user_name == user}
    if not user_cats:
        print_error(f"No categories found for user '{user}'.")
        return

    table = Table(title=f"Category Report for {user}", box=box.ROUNDED)
    table.add_column("Category", style="bold yellow")
    table.add_column("Budget Limit", style="magenta")
    table.add_column("Total Spent", style="red")
    table.add_column("Total Income", style="green")
    table.add_column("Status", style="bold")

    for cat in user_cats.values():
        cat_transactions = [t for t in transactions.values()
                            if t.user_name == user and t.category_name == cat.name]
        spent = sum(t.amount for t in cat_transactions if t.transaction_type == "expense")
        earned = sum(t.amount for t in cat_transactions if t.transaction_type == "income")
        limit = cat.budget_limit

        if limit > 0:
            status = "[green]Under budget[/green]" if spent <= limit else "[red]Over budget![/red]"
            limit_str = f"KES {limit:,.2f}"
        else:
            status = "[dim]No limit set[/dim]"
            limit_str = "-"

        table.add_row(cat.name, limit_str, f"KES {spent:,.2f}", f"KES {earned:,.2f}", status)

    console.print(table)
