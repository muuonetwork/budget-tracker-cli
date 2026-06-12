"""
Transaction model - a single income or expense entry
"""
import uuid
from datetime import datetime


class Transaction:
    TYPES = ("expense", "income")

    def __init__(
        self,
        title: str,
        amount: float,
        category_name: str,
        user_name: str,
        transaction_type: str = "expense",
        date: str = "",
        completed: bool = False,
    ):
        self.id = str(uuid.uuid4())[:8]  # short unique ID
        self.title = title
        self.amount = amount
        self.category_name = category_name
        self.user_name = user_name
        self.transaction_type = transaction_type if transaction_type in self.TYPES else "expense"
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.completed = completed  # mirrors "task completed" from the rubric

    def mark_complete(self):
        self.completed = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "amount": self.amount,
            "category_name": self.category_name,
            "user_name": self.user_name,
            "transaction_type": self.transaction_type,
            "date": self.date,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        t = cls(
            title=data["title"],
            amount=data["amount"],
            category_name=data["category_name"],
            user_name=data["user_name"],
            transaction_type=data.get("transaction_type", "expense"),
            date=data.get("date", ""),
            completed=data.get("completed", False),
        )
        t.id = data["id"]
        return t

    def __repr__(self):
        return f"Transaction(id={self.id}, title={self.title}, amount={self.amount})"
