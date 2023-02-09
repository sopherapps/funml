"""A collection of utilities to do with piping or pipeline.
"""
from typing import Any

from funml.types import ExecutionExpression


def execute(*args: Any, **kwargs: Any) -> ExecutionExpression:
    """Executes a pipeline returning its output.

    A pipeline will be executed the moment this expression is
    reached.

    Don't use `>>` after a call to execute as the pipeline
    would have already terminated.

    Args:
        args: any arguments to run on the pipeline
        kwargs: any key-word arguments to run on the pipeline.

    Example:
        ```python
        import funml as ml

        to_power_of = ml.val(lambda power, v: v**power)
        divided_by = ml.val(lambda divisor, v: v / divisor)

        output = ml.val(90) >> to_power_of(3) >> divided_by(90) >> divided_by(3) >> ml.execute()
        # prints 2700
        ```
    """
    return ExecutionExpression(*args, **kwargs)
