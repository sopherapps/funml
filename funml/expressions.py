"""Assigning variables and literals
"""
from collections.abc import Callable
from typing import Any, Union

from funml.types import to_expn, Expression


def val(v: Union[Expression, Callable, Any]) -> Expression:
    """Converts a generic value or lambda expression into a functional expression.

    This is useful when one needs to use piping on a non-ml function or
    value. It is like the connection that give non-ml values and functions
    capabilities to be used in the ml world.

    Args:
        v: the value e.g. 90 or function e.g. `min`

    Returns:
        an ml [`Expression`][funml.types.Expression] that can be piped to other ml-expressions or invoked to return its\
        output.

    Example:

        ```python
        import funml as ml

        ml_min = ml.val(min)
        ml_min_str = ml_min >> str

        expn = ml.val([6, 7, 12]) >> ml_min_str
        expn()
        # returns '6'
        ```
    """
    return to_expn(v)
