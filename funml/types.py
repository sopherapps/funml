"""All types used by funml"""
from __future__ import annotations

import functools
from collections.abc import Awaitable, Callable
from inspect import signature, Parameter, Signature
from typing import Any, Optional, List, Tuple, Union

from funml import errors
from funml.utils import is_equal_or_of_type


class MLType:
    """An ML-enabled type, that can easily be used in pattern matching, piping etc.

    Methods common to ML-enabled types are defined in this class.
    """

    def generate_case(
        self, do: "Operation"
    ) -> Tuple[Callable[[Any], bool], "Expression"]:
        """Generates a case statement for pattern matching.

        Args:
            do: The operation to do if the arg matches on this type

        Returns:
            A tuple (checker, expn) where checker is a function that checks if argument matches this case, and expn \
            is the expression that is called when the case is matched.
        """
        raise NotImplemented("generate_case not implemented")

    def _is_like(self, other: Any) -> bool:
        """Checks whether a value has the given pattern.

        Args:
            other: the value being checked against the pattern represented by type.

        Returns:
            A boolean showing true if `other` matches the pattern represented by current type.
        """
        raise NotImplemented("_is_like not implemented")


class Pipeline:
    """A series of logic blocks that operate on the same data in sequence.

    This has internal state so it is not be used in such stuff as recursion.
    However when compile is run on it, a reusable (pure) expression is created.
    """

    def __init__(self):
        self._queue: List[Expression] = []
        self._is_terminated = False

    def __rshift__(
        self,
        nxt: Union[
            "Expression",
            Callable,
            "Pipeline",
        ],
    ) -> Union["Pipeline", Any]:
        """Uses `>>` to append the nxt expression, callable, pipeline to this pipeline.

        Args:
            nxt: the next expression, pipeline, or callable to apply after the current one.

        Returns:
            the updated pipeline or the value when the pipeline is executed in case `nxt` is of \
            type `ExecutionExpression`

        Raises:
            ValueError: when the pipeline is already terminated with ml.execute() in its queue.
        """
        self.__update_queue(nxt)
        if self._is_terminated:
            return self()

        return self

    def __call__(
        self, *args: Any, **kwargs: Any
    ) -> Union["Expression", Awaitable["Expression"], Awaitable[Any], Any,]:
        """Computes the logic within the pipeline and returns the value.

        This method runs all those expressions in the queue sequentially,
        with the output of an expression being used as
        input for the next expression.

        Args:
            args: any arguments passed.
            kwargs: any key-word arguments passed

        Returns:
            the computed output of this pipeline or a partial expression if the args and kwargs provided are less than those expected.
        """
        output = None
        queue = self._queue[:-1] if self._is_terminated else self._queue
        is_async = False

        for expn in queue:
            if output is None:
                output = expn(*args, **kwargs)
            elif isinstance(output, Awaitable):
                is_async = True
                break
            else:
                # make sure piped expressions only consume previous outputs args, and kwargs
                output = expn(output, **kwargs)

        if is_async:
            return self.__as_async()(*args, **kwargs)

        return output

    def __copy__(self):
        """Helps call copy on a pipeline"""
        new_pipeline = Pipeline()
        new_pipeline._queue += self._queue
        new_pipeline._is_terminated = self._is_terminated
        return new_pipeline

    def __as_async(self) -> "AsyncPipeline":
        """Creates an async pipeline from this pipeline"""
        pipe = AsyncPipeline()
        pipe._queue = [*self._queue]
        pipe._is_terminated = self._is_terminated
        return pipe

    def __update_queue(
        self,
        nxt: Union[
            "Expression",
            Callable,
            "Pipeline",
        ],
    ):
        """Appends a pipeline or an expression to the queue."""
        if self._is_terminated:
            raise ValueError("a terminated pipeline cannot be extended.")

        if isinstance(nxt, Pipeline):
            self._queue += nxt._queue
            self._is_terminated = nxt._is_terminated
        else:
            nxt_expn = to_expn(nxt)
            self._queue.append(nxt_expn)
            self._is_terminated = isinstance(nxt, ExecutionExpression)


class AsyncPipeline(Pipeline):
    """A pipeline for handling async code.

    See more details in the [base class](funml.types.Pipeline)
    """

    async def __call__(self, *args: Any, **kwargs: Any) -> Union["Expression", Any]:
        """Computes the logic within the pipeline and returns the value.

        This method runs all those expressions in the queue sequentially,
        with the output of an expression being used as
        input for the next expression.

        Args:
            args: any arguments passed.
            kwargs: any key-word arguments passed

        Returns:
            the computed output of this pipeline or a partial expression if the args and kwargs provided \
            are less than expected.
        """
        output = None
        queue = self._queue[:-1] if self._is_terminated else self._queue

        for expn in queue:
            if output is None:
                output = expn(*args, **kwargs)
            elif isinstance(output, Awaitable):
                output = expn((await output), **kwargs)
            else:
                output = expn(output, **kwargs)

        return output


class Operation:
    """A computation.

    Args:
        func: the logic to run as part of the operation.
    """

    def __init__(self, func: Callable):
        self.__signature = _get_func_signature(func)
        self.__args_length = _get_non_variable_args_length(self.__signature)

        if len(self.__signature.parameters) == 0:
            # be more fault tolerant by using variable params
            self.__f = lambda *args, **kwargs: func()
        else:
            self.__f = func

    def __call__(self, *args: Any, **kwargs: Any) -> Union["Operation", Any]:
        """Applies the logic attached to this operation and returns output.

        Args:
            args: the args passed
            kwargs: the context in which the operation is being run.

        Returns:
            the final output of the operation's logic code or a partial operation if the args and kwargs \
            provided are less than those expected.
        """
        try:
            args_length = _get_num_of_relevant_args(self.__signature, *args, **kwargs)
            if args_length < self.__args_length:
                return Operation(func=functools.partial(self.__f, *args, **kwargs))
        except TypeError:
            # binding is impossible so just use the default implementation
            pass

        return self.__f(*args, **kwargs)


class Expression:
    """Logic that returns a value when applied.

    This is the basic building block of all functions and thus
    almost everything in FunML is converted into an expression at one point or another.

    Args:
        f: the operation or logic to run as part of this expression
    """

    def __init__(self, f: Optional["Operation"] = None):
        self._f = f if f is not None else Operation(lambda x, *args, **kwargs: x)

    def __call__(self, *args: Any, **kwargs: Any) -> Union["Expression", Any]:
        """Computes the logic within and returns the value.

        Args:
            args: any arguments passed.
            kwargs: any key-word arguments passed

        Returns:
            the computed output of this expression or another expression with a partial operation \
            in it if the args provided are less than expected.
        """
        value = self._f(*args, **kwargs)
        if isinstance(value, Operation):
            return Expression(f=value)
        return value

    def __rshift__(
        self,
        nxt: Union[
            "Expression",
            "Pipeline",
            Callable,
        ],
    ) -> Union["Pipeline", Any]:
        """This makes piping using the '>>' symbol possible.

        Combines with the given `nxt` expression or pipeline to produce a new pipeline
        where data flows from current to nxt.

        Args:
            nxt: the next expression, pipeline, or callable to apply after the current one.

        Returns:
            a new pipeline  where the first expression is the current expression followed by `nxt` \
            or returns the value when the pipeline is executed in case `nxt` is of type `ExecutionExpression`
        """
        new_pipeline = Pipeline()
        new_pipeline >> self >> nxt
        return new_pipeline


class ExecutionExpression(Expression):
    """Expression that executes all previous once it is found on a pipeline

    Raises:
        NotImplementedError: when `>>` is used after it.
    """

    def __rshift__(self, nxt: Any):
        """rshift is not supported for this.

        This is a terminal expression that expects no other expression
        after it on the pipeline.
        """
        raise NotImplementedError("terminal pipeline expression: `>>` not supported")


class MatchExpression(Expression):
    """A special expression used when pattern matching.

    Args:
        arg: the value to be pattern matched.
    """

    def __init__(self, arg: Optional[Any] = None):
        super().__init__()
        self._matches: List[Tuple[Callable[[Any], bool], Expression[T]]] = []
        self.__arg = arg

    def case(self, pattern: Union[MLType, Any], do: Callable) -> "MatchExpression":
        """Adds a case to a match statement.

        This is chainable, allowing multiple cases to be added to the same
        match pipeline.

        Args:
            pattern: the pattern to match against.
            do: the logic to run if pattern is matched.

        Returns:
            The current match expressions, after adding the case.
        """
        if isinstance(pattern, MLType):
            check, expn = pattern.generate_case(Operation(func=do))
        else:
            check = lambda arg: is_equal_or_of_type(arg, pattern)
            expn = Expression(Operation(func=do))

        self.__add_match(check=check, expn=expn)
        return self

    def __add_match(self, check: Callable[[Any], bool], expn: "Expression"):
        """Adds a match set to the list of match sets

        A match set comprises a checker function and an expression.
        The checker function checks if a given argument matches this case.
        The expression is called when the case is matched.

        Args:
            check: the checker function
            expn: the expression to run if a value matches.
        """
        if not callable(check):
            raise TypeError(f"the check is supposed to be a callable. Got {check}")

        if not isinstance(expn, Expression):
            raise TypeError(
                f"expected expression to be an Expression. Got {type(expn)}"
            )

        self._matches.append((check, expn))

    def __call__(self, arg: Optional[Any] = None) -> Union["Expression", Any]:
        """Applies the matched case and returns the output.

        The match cases are surveyed for any that matches the given argument
        until one that matches is found.
        Then the expression of that case is run and its output returned.

        Args:
            arg: the potential value to match against.

        Returns:
            The output of the expression of the matched case.

        Raises:
            MatchError: no case was matched for the given argument.
        """
        if arg is None:
            arg = self.__arg

        for check, expn in self._matches:
            if check(arg):
                return expn(arg)

        raise errors.MatchError(arg)


def _get_num_of_relevant_args(sig: Signature, *args, **kwargs) -> int:
    """Computes the number of args and kwargs relevant to the signature

    Raises:
        TypeError if the args and kwargs cannot be bound to the signature

    Returns:
        the number of args and kwargs passed that are relevant to the given signature
    """
    all_args = sig.bind_partial(*args, **kwargs)
    all_args.apply_defaults()
    return len(all_args.args) + len(all_args.kwargs)


def _get_non_variable_args_length(sig: Signature) -> int:
    """Retrieves the number of non variable args from the signature"""
    return len(
        list(
            filter(
                lambda v: v.kind
                not in (Parameter.VAR_KEYWORD, Parameter.VAR_POSITIONAL),
                sig.parameters.values(),
            )
        )
    )


def _get_func_signature(func: Callable):
    """Gets the function signature of the given callable"""
    try:
        return signature(func)
    except ValueError:
        return signature(func.__call__)


def to_expn(v: Union["Expression", Callable, Any]) -> "Expression":
    """Converts a Callable or Expression into an Expression"""
    if isinstance(v, Expression):
        return v
    elif isinstance(v, Callable):
        return Expression(Operation(v))
    # return a noop expression
    return Expression(Operation(func=lambda: v))
