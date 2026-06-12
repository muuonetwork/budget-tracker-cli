"""
utils/display.py - pretty printing helpers using the `rich` library
"""

from rich.console import Console
from rich.table import Table
from rich import box
from models.user import User
from models.category import Category
from models.transaction import Transaction

console = Console()


def print_success(message: str):
    console.print(f"[bold green]✔ {message}[/bold green]")


def print_error(message: str):
    console.print(f"[bold red]✘ {message}[/bold red]")


def print_info(message: str):
    console.print(f"[bold cyan]ℹ {message}[/bold cyan]")


def print_users_table(users: dict[str, User]):
    if not users:
        print_info("No users found. Use 'add-user' to create one.")
        return
    table = Table(title="👤 Users", box=box.ROUNDED)
    table.add_column("Name", style="bold yellow")
    table.add_column("Email", style="cyan")
    table.add_column("Categories", style="green")
    for user in users.values():
        table.add_row(user.name, user.email or "-", str(len(user.categories)))
    console.print(table)


def print_categories_table(categories: dict[str, Category], user_name: str = ""):
    filtered = {k: v for k, v in categories.items() if not user_name or v.user_name == user_name}
    if not filtered:
        print_info("No categories found.")
        return
    table = Table(title=f"📂 Categories{' for ' + user_name if user_name else ''}", box=box.ROUNDED)
    table.add_column("Name", style="bold yellow")
    table.add_column("User", style="cyan")
    table.add_column("Budget Limit", style="magenta")
    table.add_column("Transactions", style="green")
    for cat in filtered.values():
        limit = f"KES {cat.budget_limit:,.2f}" if cat.budget_limit > 0 else "No limit"
        table.add_row(cat.name, cat.user_name, limit, str(len(cat.transaction_ids)))
    console.print(table)


def print_transactions_table(transactions: list[Transaction], title: str = "Transactions"):
    if not transactions:
        print_info("No transactions found.")
        return
    table = Table(title=f"💳 {title}", box=box.ROUNDED)
    table.add_column("ID", style="dim")
    table.add_column("Title", style="bold white")
    table.add_column("Type", style="cyan")
    table.add_column("Amount (KES)", style="green")
    table.add_column("Category", style="yellow")
    table.add_column("Date", style="blue")
    table.add_column("Done", style="magenta")
    for t in transactions:
        amount_color = "green" if t.transaction_type == "income" else "red"
        table.add_row(
            t.id,
            t.title,
            t.transaction_type,
            f"[{amount_color}]{t.amount:,.2f}[/{amount_color}]",
            t.category_name,
            t.date,
            "✔" if t.completed else "–",
        )
    console.print(table)


def print_summary(income: float, expenses: float):
    balance = income - expenses
    balance_color = "green" if balance >= 0 else "red"
    table = Table(title="📊 Budget Summary", box=box.HEAVY_HEAD)
    table.add_column("Metric", style="bold")
    table.add_column("Amount (KES)", style="bold")
    table.add_row("Total Income", f"[green]{income:,.2f}[/green]")
    table.add_row("Total Expenses", f"[red]{expenses:,.2f}[/red]")
    table.add_row("Balance", f"[{balance_color}]{balance:,.2f}[/{balance_color}]")
    console.print(table)
