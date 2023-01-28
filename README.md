# FunML

[![PyPI version](https://badge.fury.io/py/funml.svg)](https://badge.fury.io/py/funml) ![CI](https://github.com/sopherapps/funml/actions/workflows/CI.yml/badge.svg)

A collection of utilities to help write python as though it were an ML-kind of functional language like OCaml

**The API is still unstable. Use at your own risk.**

---

**Documentation:** [https://sopherapps.github.io/funml](https://sopherapps.github.io/funml)

**Source Code:** [https://github.com/sopherapps/funml](https://github.com/sopherapps/funml)

--- 

Most Notable Features are:

1. Immutable data structures like enums, records, lists
2. Piping outputs of one function to another as inputs. That's how bigger functions are created from smaller ones.
3. Pattern matching for declarative conditional control of flow instead of using 'if's
4. Error handling using the `Result` monad, courtesy of [rust](https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html).
   Instead of using `try-except` all over the place, functions return 
   a `Result` which has the right data when successful and an exception if unsuccessful. 
   The result is then pattern-matched to retrieve the data or react to the exception.
5. No `None`. Instead, we use the `Option` monad, courtesy of [rust](https://doc.rust-lang.org/book/ch06-01-defining-an-enum.html?highlight=option#the-option-enum-and-its-advantages-over-null-values).
   When an Option has data, it is `Option.SOME`, or else it is `Option.NONE`. 
   Pattern matching helps handle both scenarios.

## Dependencies

- [python 3.7+](https://docs.python.org/)

## Getting Started

- Ensure you have python 3.7 and above installed.
- Install `FunML`

```shell
pip install funml
```

- Add the following code in `main.py`

```python
from datetime import date

import funml as ml


def main():
    """Main program"""

    """
    Data Types:
    ===
    
    Using the `Enum` base class and the 
    `@record` decorator, one can create custom
    data types in form of Enums and records respectively.
    """

    class Date(ml.Enum):
        January = date
        February = date
        March = date
        April = date
        May = date
        June = date
        July = date
        August = date
        September = date
        October = date
        November = date
        December = date

    @ml.record
    class Color:
        r: int
        g: int
        b: int
        a: int

    """
    Expressions
    ===
    
    The main construct in funml is the expression.
    As long as anything is an expression, it can be piped 
    i.e. added to a pipeline.
    
    Anything can be turned into an expression using
    `funml.val`.
    functions, static values, variables, name it.
    
    Expressions are the building blocks for more expressions.
    Combining multiple expressions creates new expressions
    
    It may have:
    
    - `ml.Result`, `ml.Option` and their helpers like `ml.is_ok`, `ml.if_ok`
    - `IList` and its helpers `ireduce`, `imap`, `ifilter` etc.
    - `Enum`'s, `Record`'s
    - pattern matching with `ml.match().case(...)`
    - lambda functions wrapped in `ml.val` to make them expressions
    - Even piping with the `>>` to move data from LEFT to RIGHT through a number of expressions
    etc.
    """

    """
    Primitive Expressions
    ---
    
    We can start with a few primitive expressions.
    These we will use later to build more complex expressions.
    
    A typical primitive expression is `ml.val(<lambda function>)`
    But one can also wrap functions/classes from external modules
    
    e.g. 
    MlDbConnection = ml.val(DbConnection)
    # then later, use it as though it was a funml expression.
    conn = (
            ml.val(config) 
            >> MlDbConnection
            >> ml.execute())
            
    We have some builtin primitive expressions like
    - ml.val
    - ml.match
    - ml.execute
    - ml.ireduce
    - ml.ifilter
    - ml.imap
    - ml.if_ok
    - ml.is_ok
    - ml.if_err
    - ml.is_err
    - ml.if_some
    - ml.is_some
    - ml.if_none
    - ml.is_none
    """
    unit = ml.val(lambda v: v)
    is_even = ml.val(lambda v: v % 2 == 0)
    mul = ml.val(lambda x, y: x * y)
    superscript = ml.val(lambda num, power: num**power)
    get_month = ml.val(lambda value: value.month)
    is_num = ml.val(lambda v: isinstance(v, (int, float)))
    is_exp = ml.val(lambda v: isinstance(v, BaseException))

    """
    Higher-level Expressions
    ---
    
    Here we combine the primitive expressions into more
    complex ones using:
    
    - normal function calls 
      e.g. `if_else(some_stuff)` where `if_else` is a primitive expression
    - pipes `>>`
      pipes let one start with data then define the steps that operate on the
      data.
      e.g. `output = records >> remove_nulls >> parse_json >> ml.execute()`
    - chaining primitives that have methods on their outputs that return expressions.
      e.g. `output = ml.match(data).case(1, do=...).case(2, do=...).case(3, ...)`
      
    We can combine these complex expressions into even more complex ones
    to infinite complexity.
    
    That is the main thing about functional programming i.e.
    composing simpler functions into more complex functions 
    to an indefinite level of complexity BUT while keeping the
    complex functions readable and predictable (pure)
    
    NOTE:
    ---
    Avoid calling expressions recursively. Each expression has state
    and unexpected things happen when hidden state is maintained during
    recursion.
    """
    accum_factorial = ml.val(lambda num, accum: (
        accum if num <= 0 else accum_factorial(num - 1, num * accum)
    ))
    cube = ml.val(lambda v: superscript(v, 3))
    factorial = ml.val(lambda x: accum_factorial(x, 1))
    get_item_types = ml.ireduce(lambda x, y: f"{type(x)}, {type(y)}")
    num_type_err = ml.val(
        lambda *args: TypeError(f"expected numbers, got {get_item_types(args)}")
    )
    is_seq_of_nums = ml.ireduce(lambda x, y: x and is_num(y), True)
    to_result = ml.val(lambda v: ml.Result.ERR(v) if is_exp(v) else ml.Result.OK(v))

    try_multiply = ml.val(
        lambda x, y: num_type_err(x, y) if is_seq_of_nums([x, y]) else mul(x, y)
    ) >> to_result

    result_to_option = ml.if_ok(ml.Option.SOME, strict=False) >> ml.if_err(
        lambda *args: ml.Option.NONE, strict=False
    )
    to_date_enum = ml.val(
        lambda v: (
            ml.match(v.month)
            .case(1, do=ml.val(Date.January(v)))
            .case(2, do=ml.val(Date.February(v)))
            .case(3, do=ml.val(Date.March(v)))
            .case(4, do=ml.val(Date.April(v)))
            .case(5, do=ml.val(Date.May(v)))
            .case(6, do=ml.val(Date.June(v)))
            .case(7, do=ml.val(Date.July(v)))
            .case(8, do=ml.val(Date.August(v)))
            .case(9, do=ml.val(Date.September(v)))
            .case(10, do=ml.val(Date.October(v)))
            .case(11, do=ml.val(Date.November(v)))
            .case(12, do=ml.val(Date.December(v)))
        )()
    )
    get_month_str = get_month >> (
        ml.match()
        .case(1, do=ml.val("JAN"))
        .case(2, do=ml.val("FEB"))
        .case(3, do=ml.val("MAR"))
        .case(4, do=ml.val("APR"))
        .case(5, do=ml.val("MAY"))
        .case(6, do=ml.val("JUN"))
        .case(7, do=ml.val("JUL"))
        .case(8, do=ml.val("AUG"))
        .case(9, do=ml.val("SEP"))
        .case(10, do=ml.val("OCT"))
        .case(11, do=ml.val("NOV"))
        .case(12, do=ml.val("DEC"))
    )

    """
    Data
    ===
    
    We have a number of data types that are work well with ml
    
        - IList: an immutable list, with pattern matching enabled
        - Enum: an enumerable data type, with pattern matching enabled
        - Record: a record-like data type, with pattern matching enabled
        
    Using our Higher level expressions (and lower level ones if they can),
    we operate on the data.
    
    In order to add data variables to pipelines, we turn them into expressions
    using `ml.val`
    
    e.g. `ml.val(90)` becomes an expression that evaluates to `lambda: 90`
    """
    dates = [
        date(200, 3, 4),
        date(2009, 1, 16),
        date(1993, 12, 29),
        date(2004, 10, 13),
        date(2020, 9, 5),
        date(2004, 5, 7),
        date(1228, 8, 18),
    ]
    dates = ml.val(dates)
    nums = ml.val(ml.l(12, 3, 45, 7, 8, 6, 3))
    data = ml.l((2, 3), ("hey", 7), (5, "y"), (8.1, 6))
    blue = Color(r=0, g=0, b=255, a=1)

    """
    Execution
    ===
    
    To mimic pipelines, we use
    `>>` as pipe to move data from left to right
    and `ml.execute()` to execute the pipeline and return 
    the results
    
    Don't forget to call `ml.execute()` at the end of the
    pipeline or else you will get just a callable object.
    
    It is more like not calling `await` on a function that
    returns an `Awaitable`.
    """
    dates_as_enums = dates >> ml.imap(to_date_enum) >> ml.execute()
    print(f"\ndates as enums: {dates_as_enums}")

    print(f"\nfirst date enum: {dates_as_enums[0]}")

    months_as_str = dates >> ml.imap(get_month_str) >> ml.execute()
    print(f"\nmonths of dates as str:\n{months_as_str}")

    print(f"\ncube of 5: {cube(5)}")

    factorials_str = (
        nums
        >> ml.ifilter(is_even)
        >> ml.imap(lambda v: f"factorial for {v}: {factorial(v)}")
        >> ml.ireduce(lambda x, y: f"{x}\n{y}")
        >> ml.execute()
    )
    print(factorials_str)

    print(f"blue: {blue}")

    data = ml.val(data) >> ml.imap(lambda x: try_multiply(*x)) >> ml.execute()
    print(f"\nafter multiplication:\n{data}")

    data_as_options = ml.val(data) >> ml.imap(result_to_option) >> ml.execute()
    print(f"\ndata as options: {data_as_options}")

    data_as_actual_values = (
        ml.val(data) >> ml.ifilter(ml.is_ok) >> ml.imap(ml.if_ok(unit)) >> ml.execute()
    )
    print(f"\ndata as actual values: {data_as_actual_values}")


if __name__ == "__main__":
    main()
```

- Run the script

```shell
python main.py
```

## Contributing

Contributions are welcome. The docs have to maintained, the code has to be made cleaner, more idiomatic and faster,
and there might be need for someone else to take over this repo in case I move on to other things. It happens!

Please look at the [CONTRIBUTIONS GUIDELINES](./CONTRIBUTING.md)

## Benchmarks

TBD

## License

Licensed under both the [MIT License](./LICENSE)

Copyright (c) 2023 [Martin Ahindura](https://github.com/tinitto)

## Gratitude

> "...and His (the Father's) incomparably great power for us who believe. That power is the same as the mighty strength
> He exerted when He raised Christ from the dead and seated Him at His right hand in the heavenly realms, 
> far above all rule and authority, power and dominion, and every name that is invoked, not only in the present age but 
> also in the one to come."
>
> -- Ephesians 1: 19-21

All glory be to God.

<a href="https://www.buymeacoffee.com/martinahinJ" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>