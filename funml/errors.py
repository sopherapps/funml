"""Errors for this domain"""
from typing import Optional


class MatchError(BaseException):
    def __init__(self, arg: Optional[str] = None):
        self.arg = arg

    def __repr__(self):
        return f"MatchError: No match found for {self.arg}"
