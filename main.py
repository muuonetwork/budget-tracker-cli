"""
Budget Tracker CLI - Main Entry Point (click version)
Run: python main.py <command> [options]
"""
import click

from cli.user_commands import add_user, list_users, delete_user
from cli.category_commands import add_category, list_categories, edit_category
from cli.transaction_commands import (
    add_transaction, list_transactions, complete_transaction, delete_transaction,
)
from cli.report_commands import summary, category_report


@click.group()
def cli():
    """Personal Budget Tracker - Manage users, categories, and transactions."""
    pass


cli.add_command(add_user)
cli.add_command(list_users)
cli.add_command(delete_user)

cli.add_command(add_category)
cli.add_command(list_categories)
cli.add_command(edit_category)

cli.add_command(add_transaction)
cli.add_command(list_transactions)
cli.add_command(complete_transaction)
cli.add_command(delete_transaction)

cli.add_command(summary)
cli.add_command(category_report)


if __name__ == "__main__":
    cli()
