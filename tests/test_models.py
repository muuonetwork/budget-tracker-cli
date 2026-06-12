"""
tests/test_models.py - unit tests for User, Category, Transaction models
Run with: pytest tests/
"""

import pytest
from models.user import User
from models.category import Category
from models.transaction import Transaction


# ── User Tests ─────────────────────────────────────────────────────────────

def test_user_creation():
    user = User(name="Alex", email="alex@example.com")
    assert user.name == "Alex"
    assert user.email == "alex@example.com"
    assert user.categories == []


def test_user_add_category():
    user = User(name="Alex")
    user.add_category("Food")
    assert "Food" in user.categories


def test_user_add_category_no_duplicates():
    user = User(name="Alex")
    user.add_category("Food")
    user.add_category("Food")
    assert user.categories.count("Food") == 1


def test_user_remove_category():
    user = User(name="Alex")
    user.add_category("Food")
    user.remove_category("Food")
    assert "Food" not in user.categories


def test_user_serialization():
    user = User(name="Alex", email="alex@example.com")
    user.add_category("Food")
    d = user.to_dict()
    restored = User.from_dict(d)
    assert restored.name == user.name
    assert restored.email == user.email
    assert restored.categories == user.categories


# ── Category Tests ─────────────────────────────────────────────────────────

def test_category_creation():
    cat = Category(name="Food", user_name="Alex", budget_limit=5000.0)
    assert cat.name == "Food"
    assert cat.budget_limit == 5000.0
    assert cat.transaction_ids == []


def test_category_add_transaction():
    cat = Category(name="Food", user_name="Alex")
    cat.add_transaction("abc123")
    assert "abc123" in cat.transaction_ids


def test_category_serialization():
    cat = Category(name="Transport", user_name="Alex", budget_limit=2000.0)
    cat.add_transaction("tx001")
    d = cat.to_dict()
    restored = Category.from_dict(d)
    assert restored.name == cat.name
    assert restored.budget_limit == cat.budget_limit
    assert restored.transaction_ids == cat.transaction_ids


# ── Transaction Tests ──────────────────────────────────────────────────────

def test_transaction_creation():
    t = Transaction(title="Lunch", amount=350.0, category_name="Food", user_name="Alex")
    assert t.title == "Lunch"
    assert t.amount == 350.0
    assert t.transaction_type == "expense"
    assert t.completed is False
    assert len(t.id) == 8


def test_transaction_mark_complete():
    t = Transaction(title="Lunch", amount=350.0, category_name="Food", user_name="Alex")
    t.mark_complete()
    assert t.completed is True


def test_transaction_type_defaults_to_expense():
    t = Transaction(title="Misc", amount=100.0, category_name="Other",
                    user_name="Alex", transaction_type="invalid_type")
    assert t.transaction_type == "expense"


def test_transaction_serialization():
    t = Transaction(title="Salary", amount=50000.0, category_name="Income",
                    user_name="Alex", transaction_type="income", date="2025-01-15")
    d = t.to_dict()
    restored = Transaction.from_dict(d)
    assert restored.title == t.title
    assert restored.amount == t.amount
    assert restored.transaction_type == t.transaction_type
    assert restored.id == t.id
