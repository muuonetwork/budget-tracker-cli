"""
cli/transaction_commands.py - add-transaction, list-transactions, complete-transaction
"""

from models.transaction import Transaction
from utils.storage import (
    load_users,
    load_categories, save_categories,
    load_transactions, save_transactions,
    category_key,
)
from utils.display import print_success, print_error, print_transactions_table


def register_transaction_commands(subparsers):
    # add-transaction
    p = subparsers.add_parser("add-transaction", help="Record an income or expense")
    p.add_argument("--user", required=True, help="User name")
    p.add_argument("--category", required=True, help="Category name")
    p.add_argument("--title", required=True, help="Transaction description")
    p.add_argument("--amount", type=float, required=True, help="Amount in KES")
    p.add_argument("--type", dest="transaction_type", choices=["expense", "income"],
                   default="expense", help="Transaction type (default: expense)")
    p.add_argument("--date", default="", help="Date in YYYY-MM-DD format (default: today)")
    p.set_defaults(func=cmd_add_transaction)

    # list-transactions
    p2 = subparsers.add_parser("list-transactions", help="List transactions for a user/category")
    p2.add_argument("--user", required=True, help="User name")
    p2.add_argument("--category", default="", help="Filter by category name")
    p2.set_defaults(func=cmd_list_transactions)

    # complete-transaction
    p3 = subparsers.add_parser("complete-transaction", help="Mark a transaction as completed/reconciled")
    p3.add_argument("--id", required=True, help="Transaction ID")
    p3.set_defaults(func=cmd_complete_transaction)

    # delete-transaction
    p4 = subparsers.add_parser("delete-transaction", help="Delete a transaction by ID")
    p4.add_argument("--id", required=True, help="Transaction ID")
    p4.set_defaults(func=cmd_delete_transaction)


def cmd_add_transaction(args):
    users = load_users()
    if args.user not in users:
        print_error(f"User '{args.user}' not found.")
        return

    categories = load_categories()
    key = category_key(args.user, args.category)
    if key not in categories:
        print_error(f"Category '{args.category}' not found for user '{args.user}'. Create it first.")
        return

    transactions = load_transactions()
    t = Transaction(
        title=args.title,
        amount=args.amount,
        category_name=args.category,
        user_name=args.user,
        transaction_type=args.transaction_type,
        date=args.date,
    )
    transactions[t.id] = t

    # Link transaction to category
    categories[key].add_transaction(t.id)

    save_transactions(transactions)
    save_categories(categories)
    print_success(f"Transaction '{args.title}' (ID: {t.id}) recorded under '{args.category}'.")


def cmd_list_transactions(args):
    transactions = load_transactions()
    filtered = [
        t for t in transactions.values()
        if t.user_name == args.user
        and (not args.category or t.category_name == args.category)
    ]
    title = f"Transactions for {args.user}"
    if args.category:
        title += f" → {args.category}"
    print_transactions_table(filtered, title=title)


def cmd_complete_transaction(args):
    transactions = load_transactions()
    if args.id not in transactions:
        print_error(f"Transaction ID '{args.id}' not found.")
        return
    transactions[args.id].mark_complete()
    save_transactions(transactions)
    print_success(f"Transaction '{args.id}' marked as completed.")


def cmd_delete_transaction(args):
    transactions = load_transactions()
    if args.id not in transactions:
        print_error(f"Transaction ID '{args.id}' not found.")
        return
    del transactions[args.id]
    save_transactions(transactions)
    print_success(f"Transaction '{args.id}' deleted.")
