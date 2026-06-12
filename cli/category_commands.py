"""
cli/category_commands.py - add-category, list-categories commands
"""

from models.category import Category
from utils.storage import (
    load_users, save_users,
    load_categories, save_categories,
    category_key,
)
from utils.display import print_success, print_error, print_categories_table


def register_category_commands(subparsers):
    # add-category
    p = subparsers.add_parser("add-category", help="Add a budget category for a user")
    p.add_argument("--user", required=True, help="User name")
    p.add_argument("--name", required=True, help="Category name (e.g. Food)")
    p.add_argument("--limit", type=float, default=0.0, help="Optional monthly budget limit")
    p.set_defaults(func=cmd_add_category)

    # list-categories
    p2 = subparsers.add_parser("list-categories", help="List categories (optionally filtered by user)")
    p2.add_argument("--user", default="", help="Filter by user name")
    p2.set_defaults(func=cmd_list_categories)

    # edit-category
    p3 = subparsers.add_parser("edit-category", help="Update a category's budget limit")
    p3.add_argument("--user", required=True, help="User name")
    p3.add_argument("--name", required=True, help="Category name")
    p3.add_argument("--limit", type=float, required=True, help="New budget limit")
    p3.set_defaults(func=cmd_edit_category)


def cmd_add_category(args):
    users = load_users()
    if args.user not in users:
        print_error(f"User '{args.user}' not found. Create them first with 'add-user'.")
        return

    categories = load_categories()
    key = category_key(args.user, args.name)
    if key in categories:
        print_error(f"Category '{args.name}' already exists for user '{args.user}'.")
        return

    cat = Category(name=args.name, user_name=args.user, budget_limit=args.limit)
    categories[key] = cat

    # Link category to user
    users[args.user].add_category(args.name)

    save_categories(categories)
    save_users(users)
    print_success(f"Category '{args.name}' added for user '{args.user}'.")


def cmd_list_categories(args):
    categories = load_categories()
    print_categories_table(categories, user_name=args.user)


def cmd_edit_category(args):
    categories = load_categories()
    key = category_key(args.user, args.name)
    if key not in categories:
        print_error(f"Category '{args.name}' not found for user '{args.user}'.")
        return
    categories[key].budget_limit = args.limit
    save_categories(categories)
    print_success(f"Budget limit for '{args.name}' updated to KES {args.limit:,.2f}.")
