"""
cli/transaction_commands.py - add-transaction, list-transactions, complete-transaction, delete-transaction (click version)
"""
import click

from models.transaction import Transaction
from utils.storage import (
    load_users,
    load_categories, save_categories,
    load_transactions, save_transactions,
    category_key,
)
from utils.display import print_success, print_error, print_transactions_table


@click.command("add-transaction")
@click.option("--user", required=True, help="User name")
@click.option("--category", required=True, help="Category name")
@click.option("--title", required=True, help="Transaction description")
@click.option("--amount", type=float, required=True, help="Amount in KES")
@click.option("--type", "transaction_type", type=click.Choice(["expense", "income"]),
              default="expense", help="Transaction type (default: expense)")
@click.option("--date", default="", help="Date in YYYY-MM-DD format (default: today)")
def add_transaction(user, category, title, amount, transaction_type, date):
    """Record an income or expense."""
    users = load_users()
    if user not in users:
        print_error(f"User '{user}' not found.")
        return

    categories = load_categories()
    key = category_key(user, category)
    if key not in categories:
        print_error(f"Category '{category}' not found for user '{user}'. Create it first.")
        return

    transactions = load_transactions()
    t = Transaction(
        title=title,
        amount=amount,
        category_name=category,
        user_name=user,
        transaction_type=transaction_type,
        date=date,
    )
    transactions[t.id] = t

    categories[key].add_transaction(t.id)

    save_transactions(transactions)
    save_categories(categories)
    print_success(f"Transaction '{title}' (ID: {t.id}) recorded under '{category}'.")


@click.command("list-transactions")
@click.option("--user", required=True, help="User name")
@click.option("--category", default="", help="Filter by category name")
def list_transactions(user, category):
    """List transactions for a user/category."""
    transactions = load_transactions()
    filtered = [
        t for t in transactions.values()
        if t.user_name == user
        and (not category or t.category_name == category)
    ]
    title = f"Transactions for {user}"
    if category:
        title += f" -> {category}"
    print_transactions_table(filtered, title=title)


@click.command("complete-transaction")
@click.option("--id", "transaction_id", required=True, help="Transaction ID")
def complete_transaction(transaction_id):
    """Mark a transaction as completed/reconciled."""
    transactions = load_transactions()
    if transaction_id not in transactions:
        print_error(f"Transaction ID '{transaction_id}' not found.")
        return
    transactions[transaction_id].mark_complete()
    save_transactions(transactions)
    print_success(f"Transaction '{transaction_id}' marked as completed.")


@click.command("delete-transaction")
@click.option("--id", "transaction_id", required=True, help="Transaction ID")
def delete_transaction(transaction_id):
    """Delete a transaction by ID."""
    transactions = load_transactions()
    if transaction_id not in transactions:
        print_error(f"Transaction ID '{transaction_id}' not found.")
        return
    del transactions[transaction_id]
    save_transactions(transactions)
    print_success(f"Transaction '{transaction_id}' deleted.")
