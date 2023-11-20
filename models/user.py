"""User"""

from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING, Deque, List
if TYPE_CHECKING:
    from models.company import Company

class User:
    """User"""

    def __init__(
        self,
        id: int,
        first_name: str,
        last_name: str,
        email: str,
        company_id: int,
        email_status: bool,
        active_status: bool,
        tokens: 19,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.company_id = company_id
        self.email_status = email_status
        self.active_status = active_status
        self.tokens = tokens
        self.company : Company = None
        self.token_log : Deque[int] = deque()
        self.token_log.appendleft(tokens)

    def add_tokens(self, amount: int):
        self.tokens += amount
        self.token_log.appendleft(amount)
    
    def top_up(self):
        top_up_amount = self.company.top_up
        self.add_tokens(top_up_amount)
        self.company.add_to_top_up_sum(top_up_amount)

    def set_company(self, company: Company):
        self.company = company

    def should_email(self) -> bool:
        return self.company.email_status and self.email_status
    
    def balance(self) -> int:
        return self.tokens
    
    def previous_balance(self) -> int:
        return self.token_log[-1]
