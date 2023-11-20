"""Company"""


from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from models.user import User

class Company:
    """Company"""
    def __init__(self, id: int, name: str, top_up: int, email_status: bool):
        self.id = id
        self.name = name
        self.top_up = top_up
        self.email_status = email_status
        self.users : List[User] = []
        self.top_up_sum : int = 0
    
    def add_user(self, user: User):
        self.users.append(user)

    def add_to_top_up_sum(self, amount):
        self.top_up_sum += amount
