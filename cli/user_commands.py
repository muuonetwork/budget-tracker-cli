"""
cli/user_commands.py - add-user, list-users commands
"""

from models.user import User
from utils.storage import load_users, save_users
from utils.display import print_success, print_error, print_users_table


def register_user_commands(subparsers):
    # add-user
    p = subparsers.add_parser("add-user", help="Create a new user")
    p.add_argument("--name", required=True, help="User's name")
    p.add_argument("--email", default="", help="User's email (optional)")
    p.set_defaults(func=cmd_add_user)

    # list-users
    p2 = subparsers.add_parser("list-users", help="Show all users")
    p2.set_defaults(func=cmd_list_users)

    # delete-user
    p3 = subparsers.add_parser("delete-user", help="Delete a user by name")
    p3.add_argument("--name", required=True, help="Name of user to delete")
    p3.set_defaults(func=cmd_delete_user)


def cmd_add_user(args):
    users = load_users()
    if args.name in users:
        print_error(f"User '{args.name}' already exists.")
        return
    users[args.name] = User(name=args.name, email=args.email)
    save_users(users)
    print_success(f"User '{args.name}' created successfully!")


def cmd_list_users(args):
    users = load_users()
    print_users_table(users)


def cmd_delete_user(args):
    users = load_users()
    if args.name not in users:
        print_error(f"User '{args.name}' not found.")
        return
    del users[args.name]
    save_users(users)
    print_success(f"User '{args.name}' deleted.")
