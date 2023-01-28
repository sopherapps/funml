"""Assigning variables and literals
"""
from typing import Type, Any

from funml.types import Assignment, to_expn, Expression


def let(t: Type, **kwargs: Any) -> Assignment:
    """Creates a variable local to any expressions that follow it after piping.

    It creates a variable, initializing it to a given value. That variable
    with its given name can then be accessed by any expressions after it in the
    given pipe.

    For a given expression to access the value of that variable, one of its argument
    must have the same name as that variable.

    Args:
        t: the type of the variable
        kwargs: *Only ONE* key-word argument whose key is variable name and value is the value of the variable.

    Returns:
        An [`Assignment`][funml.types.Assignment] that can be connected to another by piping, thus making the created
        variable accessible to the subsequent expression.

    Example:

        ```python
        import funml as ml

        expn = ml.let(int, x=9) >> (lambda x: x + 10) >> (lambda y: y * 20) >> str
        assert expn() == "380"
        ```
    """
    if len(kwargs) == 1:
        [(_var, _val)] = kwargs.items()
        return Assignment(var=_var, t=t, val=_val)

    raise ValueError(f"kwargs passed should be only 1, got {len(kwargs)}")


def val(v: Any) -> Expression:
    """Converts a generic value or lambda expression into a functional expression.

    This is useful when one needs to use piping on a non-ml function or
    value. It is like the connection that give non-ml values and functions
    capabilities to be used in the ml world.

    Args:
        v: the value e.g. 90 or function e.g. `min`

    Returns:
        an ml [`Expression`][funml.types.Expression] that can be piped to other ml-expressions or invoked to return its
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
