"""
Category model - a budget category (e.g. Food, Transport, Rent)
Each category belongs to a user and contains transactions.
"""


class Category:
    def __init__(self, name: str, user_name: str, budget_limit: float = 0.0):
        self.name = name
        self.user_name = user_name
        self.budget_limit = budget_limit  # 0 means no limit set
        self.transaction_ids: list[str] = []

    def add_transaction(self, transaction_id: str):
        if transaction_id not in self.transaction_ids:
            self.transaction_ids.append(transaction_id)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "user_name": self.user_name,
            "budget_limit": self.budget_limit,
            "transaction_ids": self.transaction_ids,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        cat = cls(
            name=data["name"],
            user_name=data["user_name"],
            budget_limit=data.get("budget_limit", 0.0),
        )
        cat.transaction_ids = data.get("transaction_ids", [])
        return cat

    def __repr__(self):
        return f"Category(name={self.name}, user={self.user_name}, limit={self.budget_limit})"
