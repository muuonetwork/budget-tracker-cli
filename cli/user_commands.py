"""
cli/user_commands.py - add-user, list-users, delete-user commands (click version)
"""
import click

from models.user import User
from utils.storage import load_users, save_users
from utils.display import print_success, print_error, print_users_table


@click.command("add-user")
@click.option("--name", required=True, help="User's name")
@click.option("--email", default="", help="User's email (optional)")
def add_user(name, email):
    """Create a new user."""
    users = load_users()
    if name in users:
        print_error(f"User '{name}' already exists.")
        return
    users[name] = User(name=name, email=email)
    save_users(users)
    print_success(f"User '{name}' created successfully!")


@click.command("list-users")
def list_users():
    """Show all users."""
    users = load_users()
    print_users_table(users)


@click.command("delete-user")
@click.option("--name", required=True, help="Name of user to delete")
def delete_user(name):
    """Delete a user by name."""
    users = load_users()
    if name not in users:
        print_error(f"User '{name}' not found.")
        return
    del users[name]
    save_users(users)
    print_success(f"User '{name}' deleted.")
