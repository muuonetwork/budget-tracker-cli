"""
User model - represents a person using the budget tracker
"""
from models.person import Person


class User(Person):
    def __init__(self, name: str, email: str = ""):
        super().__init__(name, email)
        self.categories: list[str] = []  # list of category names owned by this user

    def add_category(self, category_name: str):
        if category_name not in self.categories:
            self.categories.append(category_name)

    def remove_category(self, category_name: str):
        if category_name in self.categories:
            self.categories.remove(category_name)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "email": self.email,
            "categories": self.categories,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls(name=data["name"], email=data.get("email", ""))
        user.categories = data.get("categories", [])
        return user

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"
