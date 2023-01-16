"""The context available to each expression"""
from typing import Any


class _Context(dict):
    """The _context map containing variables in scope"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__last_computed_val: Any = None

    def set_last_computed_val(self, val: Any):
        self.__last_computed_val = val

    @property
    def last_computed_val(self) -> Any:
        """The last computed value in the chain"""
        return self.__last_computed_val
