"""
utils/storage.py - handles saving and loading all data to/from JSON files
"""

import json
import os
from models.user import User
from models.category import Category
from models.transaction import Transaction

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


# ── Users ──────────────────────────────────────────────────────────────────

def load_users() -> dict[str, User]:
    _ensure_data_dir()
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            raw = json.load(f)
        return {name: User.from_dict(data) for name, data in raw.items()}
    except (json.JSONDecodeError, KeyError) as e:
        print(f"[Warning] Could not load users file: {e}")
        return {}


def save_users(users: dict[str, User]):
    _ensure_data_dir()
    with open(USERS_FILE, "w") as f:
        json.dump({name: user.to_dict() for name, user in users.items()}, f, indent=2)


# ── Categories ─────────────────────────────────────────────────────────────

def load_categories() -> dict[str, Category]:
    _ensure_data_dir()
    if not os.path.exists(CATEGORIES_FILE):
        return {}
    try:
        with open(CATEGORIES_FILE, "r") as f:
            raw = json.load(f)
        return {key: Category.from_dict(data) for key, data in raw.items()}
    except (json.JSONDecodeError, KeyError) as e:
        print(f"[Warning] Could not load categories file: {e}")
        return {}


def save_categories(categories: dict[str, Category]):
    _ensure_data_dir()
    with open(CATEGORIES_FILE, "w") as f:
        json.dump({key: cat.to_dict() for key, cat in categories.items()}, f, indent=2)


def category_key(user_name: str, category_name: str) -> str:
    """Unique key combining user + category name."""
    return f"{user_name}::{category_name}"


# ── Transactions ───────────────────────────────────────────────────────────

def load_transactions() -> dict[str, Transaction]:
    _ensure_data_dir()
    if not os.path.exists(TRANSACTIONS_FILE):
        return {}
    try:
        with open(TRANSACTIONS_FILE, "r") as f:
            raw = json.load(f)
        return {tid: Transaction.from_dict(data) for tid, data in raw.items()}
    except (json.JSONDecodeError, KeyError) as e:
        print(f"[Warning] Could not load transactions file: {e}")
        return {}


def save_transactions(transactions: dict[str, Transaction]):
    _ensure_data_dir()
    with open(TRANSACTIONS_FILE, "w") as f:
        json.dump({tid: t.to_dict() for tid, t in transactions.items()}, f, indent=2)
