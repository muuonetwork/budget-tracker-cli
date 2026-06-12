"""
cli/category_commands.py - add-category, list-categories, edit-category commands (click version)
"""
import click

from models.category import Category
from utils.storage import (
    load_users, save_users,
    load_categories, save_categories,
    category_key,
)
from utils.display import print_success, print_error, print_categories_table


@click.command("add-category")
@click.option("--user", required=True, help="User name")
@click.option("--name", required=True, help="Category name (e.g. Food)")
@click.option("--limit", type=float, default=0.0, help="Optional monthly budget limit")
def add_category(user, name, limit):
    """Add a budget category for a user."""
    users = load_users()
    if user not in users:
        print_error(f"User '{user}' not found. Create them first with 'add-user'.")
        return

    categories = load_categories()
    key = category_key(user, name)
    if key in categories:
        print_error(f"Category '{name}' already exists for user '{user}'.")
        return

    try:
        cat = Category(name=name, user_name=user, budget_limit=limit)
    except ValueError as e:
        print_error(str(e))
        return

    categories[key] = cat
    users[user].add_category(name)

    save_categories(categories)
    save_users(users)
    print_success(f"Category '{name}' added for user '{user}'.")


@click.command("list-categories")
@click.option("--user", default="", help="Filter by user name")
def list_categories(user):
    """List categories (optionally filtered by user)."""
    categories = load_categories()
    print_categories_table(categories, user_name=user)


@click.command("edit-category")
@click.option("--user", required=True, help="User name")
@click.option("--name", required=True, help="Category name")
@click.option("--limit", type=float, required=True, help="New budget limit")
def edit_category(user, name, limit):
    """Update a category's budget limit."""
    categories = load_categories()
    key = category_key(user, name)
    if key not in categories:
        print_error(f"Category '{name}' not found for user '{user}'.")
        return

    try:
        categories[key].budget_limit = limit
    except ValueError as e:
        print_error(str(e))
        return

    save_categories(categories)
    print_success(f"Budget limit for '{name}' updated to KES {limit:,.2f}.")
