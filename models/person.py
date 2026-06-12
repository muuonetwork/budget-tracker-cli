"""
Person model - base class for anyone using the system
"""
class Person:
    def __init__(self, name: str, email: str = ""):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, email={self.email})"
