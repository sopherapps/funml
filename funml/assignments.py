"""Assigning variables and literals
"""
from typing import Type, Any

from funml.types import Assignment, _to_expn


def let(t: Type, **kwargs) -> Assignment:
    """Creates an assignment in a user-friendly way"""
    if len(kwargs) == 1:
        [(_var, _val)] = kwargs.items()
        return Assignment(var=_var, t=t, val=_val)

    raise ValueError(f"kwargs passed should be only 1, got {len(kwargs)}")


def val(v: Any):
    """val meaning value. Converts a generic value into a functional expression"""
    return _to_expn(v)
