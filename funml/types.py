"""All types used by funml"""
from inspect import signature
from typing import Any, Type, Union, Callable, Optional, List, Tuple

from funml import errors
from funml.utils import is_equal_or_of_type


class Assignment:
    """A variable assignment

    Assigns a given value a variable name and type. It will check that
    the data type passed is as expected. It can thus be used to
    validate third party data before passing it through the ml-program.

    Args:
        var: the variable name
        t: the variable type
        val: the value stored in the variable

    Raises:
        TypeError: `val` passed is not of type `t`
    """

    def __init__(self, var: Any, t: Type = type(None), val: Any = None):
        self.__var = var
        self.__t = t

        if not isinstance(val, t):
            raise TypeError(f"expected type {t}, got {type(val)}")

        self.__val = val

    def __rshift__(self, nxt: Union["Expression", "Assignment", Callable]):
        """This makes piping using the '>>' symbol possible

        Combines with the given expression, assignments, Callables to produce a new expression
        where data flows from current to nxt
        """
        return _append_expn(self, nxt)

    def __iter__(self):
        """Generates an iterator that can be used to create a dict using dict()"""
        yield self.__var, self.__val

    def __call__(self) -> Any:
        """Returns the value associated with this assignment"""
        return self.__val


class Context(dict):
    """The context map containing variables in scope."""

    pass


class MLType:
    """An ML-enabled type, that can easily be used in pattern matching, piping etc.

    Methods common to ML-enabled types are defined in this class.
    """

    def generate_case(self, do: "Operation") -> Tuple[Callable, "Expression"]:
        """Generates a case statement for pattern matching.

        Args:
            do: The operation to do if the arg matches on this type

        Returns:
            A tuple (checker, expn) where checker is a function that checks if argument matches this case, and expn
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


class Expression:
    """Logic that returns a value when applied.

    This is the basic building block of all functions and thus
    almost everything in FunML is converted into an expression at one point or another.

    Args:
        f: the operation or logic to run as part of this expression
    """

    # FIXME: Expressions are not working right when undergoing recursion
    #       It seems as if the operation f is frozen and never changes
    #       or something like that. Try:     accum_factorial = ml.val(lambda num, accum: (
    #         ml.match(num <= 0).case(True, do=lambda: accum).case(False, accum_factorial(num - 1, num * accum))()
    #     ))
    #     factorial = ml.val(lambda x: accum_factorial(x, 1))
    def __init__(self, f: Optional["Operation"] = None):
        self._f = f if f is not None else Operation(lambda x, *args, **kwargs: x)
        self._context: "Context" = Context()
        self._queue: List[Expression] = []

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Computes the logic within and returns the value.

        Args:
            args: any arguments passed.
            kwargs: any key-word arguments passed

        Returns:
            the computed output of this expression.
        """
        prev_output = self._run_prev_expns(*args, **kwargs)

        if isinstance(prev_output, Context):
            self._context.update(prev_output)
        elif prev_output is not None:
            # make sure piped expressions only consume previous outputs args, and kwargs
            return self._f(prev_output, **self._context, **kwargs)

        return self._f(*args, **self._context, **kwargs)

    def __rshift__(self, nxt: Union["Expression", "Assignment", Callable]):
        """This makes piping using the '>>' symbol possible.

        Combines with the given `nxt` expression to produce a new expression
        where data flows from current to nxt.

        Args:
            nxt: the next expression, assignment or callable to apply after the current one.
        """
        merged_expn = _append_expn(self, nxt)

        if isinstance(nxt, ExecutionExpression):
            # stop pipeline, execute and return values
            return merged_expn()

        return merged_expn

    def _run_prev_expns(self, *args: Any, **kwargs: Any) -> Union["Context", Any]:
        """Runs all the previous expressions, returning the final output.

        In order to have expressions piped, all expressions are queued in the
        expression at the end of the pipe. This method runs all those expressions sequentially,
        with the output of the previous expression being used as input of the current expression.

        Args:
            args: Any args passed
            kwargs: Any key-word arguments passed.

         Returns:
             The output of the most previous expression, after running all expressions before it and piping their output
             sequentially to the next.
        """
        output = None

        for expn in self._queue:
            if output is None:
                output = expn(*args, **expn._context, **kwargs)
            elif isinstance(output, Context):
                output = expn(*args, **expn._context, **output, **kwargs)
            else:
                # make sure piped expressions only consume previous outputs args, and kwargs
                output = expn(output, **expn._context, **kwargs)

        return output

    def append_prev_expns(self, *expns: "Expression"):
        """Appends expressions that should be computed before this one.

        Args:
            expns: the previous expressions to add to the queue
        """
        self._queue += expns

    def clear_prev_expns(self):
        """Clears all previous expressions in queue."""
        self._queue.clear()


class MatchExpression(Expression):
    """A special expression used when pattern matching.

    Args:
        arg: the value to be pattern matched.
    """

    def __init__(self, arg: Optional[Any] = None):
        super().__init__(f=Operation(self))
        self._matches: List[Tuple[Callable, Expression]] = []
        self.__arg = arg

    def case(self, pattern: Union[MLType, Any], do: Callable) -> "MatchExpression":
        """Adds a case to a match statement.

        This is chainable, allowing multiple cases to be added to the same
        match expression.

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

    def __add_match(self, check: Callable, expn: Expression):
        """Adds a match set to the list of matches.

        A match set comprises a checker function and an expression.
        The checker function checks if a given argument matches this case.
        The expression that is called when the case is matched.

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

    def __call__(self, arg: Optional[Any] = None) -> Any:
        """Applies the matched case and returns the output.

        The match cases are surveyed for any that matches the given argument until one that matches is found.
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

        args = [] if arg is None else [arg]
        prev_output = self._run_prev_expns(*args)
        if prev_output is not None:
            arg = prev_output

        for check, expn in self._matches:
            if check(arg):
                return expn(arg)

        raise errors.MatchError(arg)


class ExecutionExpression(Expression):
    """Expression that executes all previous once it is found on a pipeline

    Args:
        args: any arguments to run on the pipeline
        kwargs: any key-word arguments to run on the pipeline.

    Raises:
        NotImplementedError: when `>>` is used after it.
    """

    def __init__(self, *args, **kwargs):
        op = Operation(lambda *a, **kwd: a[0] if len(a) > 0 else None)
        super().__init__(f=op)
        self.__args = args
        self.__kwargs = kwargs

    def __call__(self, *args, **kwargs):
        """Computes value of most recent expression, using args on object plus any new ones"""
        return self._run_prev_expns(*self.__args, *args, **self.__kwargs, **kwargs)

    def __rshift__(self, nxt: Any):
        """rshift is not supported for this.

        This is a terminal expression that expects no other expression
        after it on the pipeline.
        """
        raise NotImplementedError("terminal pipeline expression: `>>` not supported")


class Operation:
    """A computation.

    Args:
        func: the logic to run as part of the operation.
    """

    def __init__(self, func: Callable):
        sig = _get_func_signature(func)
        if len(sig.parameters) == 0:
            # be more fault tolerant by using variable params
            self.__f = lambda *args, **kwargs: func()
        else:
            self.__f = func

    def __call__(self, *args: Any, **kwargs: "Context") -> Any:
        """Applies the logic attached to this operation and returns output.

        Args:
            args: the args passed
            kwargs: the context in which the operation is being run.

        Returns:
            the final output of the operation's logic code.
        """
        return self.__f(*args, **kwargs)


def _get_func_signature(func: Callable):
    """Gets the function signature of the given callable"""
    try:
        return signature(func)
    except ValueError:
        return signature(func.__call__)


def to_expn(v: Union["Expression", "Assignment", Callable, Any]) -> "Expression":
    """Converts a Callable or Expression into an Expression"""
    if isinstance(v, Expression):
        return v
    elif isinstance(v, Assignment):
        # update the context
        return Expression(
            Operation(lambda *args, **kwargs: Context(**kwargs, **dict(v)))
        )
    elif isinstance(v, Callable):
        return Expression(Operation(v))
    # return a noop expression
    return Expression(Operation(func=lambda: v))


def _append_expn(
    first: Union["Expression", "Assignment", Callable, Any],
    other: Union["Expression", "Assignment", Callable, Any],
):
    """Returns a new combined Expression where the current expression runs before the passed expression"""
    other = to_expn(other)
    first = to_expn(first)

    other.append_prev_expns(*first._queue, first)
    first.clear_prev_expns()
    return other
