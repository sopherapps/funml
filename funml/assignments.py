"""A way of assigning variables"""
from typing import Type, Any


def let(
    t: Type,
    *args,
    **kwargs,
) -> "_Assignment":
    """Creates an assignment in a user-friendly way"""
    if len(args) == 1:
        return _Assignment(var=args[0], t=t)
    elif len(kwargs) == 1:
        [(var, val)] = kwargs.items()
        return _Assignment(var=var, t=t) <= val

    raise ValueError(f"kwargs passed should be only 1, got {len(kwargs)}")


class _Assignment:
    """Class for making assignments"""

    def __init__(self, var: Any, t: Type = type(None)):
        self.__var = var
        self.__t = t
        self.__val = None

    def __le__(self, val: Any) -> "_Assignment":
        """'<=' is the match operator. Here it is being used to assign a value."""
        if not isinstance(val, self.__t):
            raise TypeError(f"expected type {self.__t}, got {type(val)}")
        self.__val = val
        return self

    def __iter__(self):
        """Generates an iterator that can be used to create a dict using dict()"""
        yield self.__var, self.__val

    def __call__(self) -> Any:
        """Returns the value associated with this assignment"""
        return self.__val
