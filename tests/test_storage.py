"""
tests/test_storage.py - tests for save/load persistence logic
"""

import os
import json
import pytest
import tempfile
from unittest.mock import patch
from models.user import User
from models.category import Category
from models.transaction import Transaction
import utils.storage as storage


@pytest.fixture
def temp_data_dir(tmp_path):
    """Redirect all data file paths to a temp directory for each test."""
    with patch.object(storage, "DATA_DIR", str(tmp_path)), \
         patch.object(storage, "USERS_FILE", str(tmp_path / "users.json")), \
         patch.object(storage, "CATEGORIES_FILE", str(tmp_path / "categories.json")), \
         patch.object(storage, "TRANSACTIONS_FILE", str(tmp_path / "transactions.json")):
        yield tmp_path


def test_save_and_load_users(temp_data_dir):
    users = {"Alex": User(name="Alex", email="alex@test.com")}
    storage.save_users(users)
    loaded = storage.load_users()
    assert "Alex" in loaded
    assert loaded["Alex"].email == "alex@test.com"


def test_load_users_empty(temp_data_dir):
    result = storage.load_users()
    assert result == {}


def test_save_and_load_categories(temp_data_dir):
    key = storage.category_key("Alex", "Food")
    cats = {key: Category(name="Food", user_name="Alex", budget_limit=3000.0)}
    storage.save_categories(cats)
    loaded = storage.load_categories()
    assert key in loaded
    assert loaded[key].budget_limit == 3000.0


def test_save_and_load_transactions(temp_data_dir):
    t = Transaction(title="Coffee", amount=150.0, category_name="Food", user_name="Alex")
    transactions = {t.id: t}
    storage.save_transactions(transactions)
    loaded = storage.load_transactions()
    assert t.id in loaded
    assert loaded[t.id].title == "Coffee"


def test_category_key_format():
    key = storage.category_key("Alex", "Transport")
    assert key == "Alex::Transport"
