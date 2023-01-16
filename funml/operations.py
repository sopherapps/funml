"""Operations i.e. the actual business logic"""
from typing import Callable, Any


class _Operation:
    """A computation"""

    def __init__(self, f: Callable):
        self.__f = f

    def __call__(self, *args: Any, **kwargs: "_Context") -> Any:
        """Handles the actual computation"""
        return self.__f(*args, **kwargs)
