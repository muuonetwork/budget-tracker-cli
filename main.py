"""
Budget Tracker CLI - Main Entry Point
Run: python main.py <command> [options]
"""

import argparse
from cli.user_commands import register_user_commands
from cli.category_commands import register_category_commands
from cli.transaction_commands import register_transaction_commands
from cli.report_commands import register_report_commands


def build_parser():
    parser = argparse.ArgumentParser(
        prog="budget-tracker",
        description="💰 Personal Budget Tracker - Manage users, categories, and transactions",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    register_user_commands(subparsers)
    register_category_commands(subparsers)
    register_transaction_commands(subparsers)
    register_report_commands(subparsers)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        # Each command module sets args.func
        args.func(args)


if __name__ == "__main__":
    main()
