# Getting Started

In this tutorial, we will build a simple script that showcases most of the features of FunML.

## Create the Script File

Create a file `main.py`.

<div class="termy">

```console
$ touch main.py
```
</div>

## Add Some Custom Data Types

FunML allows us to create two types of custom data types:

- Enums: by subclassing the `ml.Enum` class
- Records: by wrapping [dataclass](https://docs.python.org/3/library/dataclasses.html)-like classes with the `@record` decorator

!!! note
    We have shortened `funml` to `ml` so wherever you see `ml` take it as `funml`

Add the following code to `main.py`.

```python
from copy import copy
from datetime import date

import funml as ml


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
```

## Expressions

The main construct in FunML is the expression.
As long as anything is an expression, it can initialize a pipeline
i.e. added to the beginning of a pipeline.

Anything can be turned into an expression using `ml.val`.
Functions, static values, variables, name it.

Expressions are the building blocks for more expressions.
Combining multiple expressions creates new expressions

An expression can contain:

- `ml.Result`, `ml.Option` and their helpers like `ml.is_ok`, `ml.if_ok`
- `IList` and its helpers `ireduce`, `imap`, `ifilter` etc.
- `Enum`'s, `Record`'s
- pattern matching with `ml.match().case(...)`
- lambda functions wrapped in `ml.val` to make them expressions
- Even piping with the `>>` to move data from LEFT to RIGHT through a number of expressions etc.

### Add Some Primitive Expressions
    
We can start with a few primitive expressions.
These we will use later to build more complex expressions.

A typical primitive expression is `ml.val(<lambda function>)`
But one can also wrap functions/classes from external modules

e.g. 
 
```python
MlDbConnection = ml.val(DbConnection)
# then later, use it as though it was a funml expression.
conn = (
            ml.val(config) 
            >> MlDbConnection
            >> ml.execute())
```   

We have some builtin primitive expressions like
    
- `ml.val`
- `ml.match`
- `ml.execute`
- `ml.ireduce`
- `ml.ifilter`
- `ml.imap`
- `ml.if_ok`
- `ml.is_ok`
- `ml.if_err`
- `ml.is_err`
- `ml.if_some`
- `ml.is_some`
- `ml.if_none`
- `ml.is_none`

So in our script, let's add a `main` function and in it, add the primitive expressions:

```python
def main():
    """Main program"""

    """
    Primitive Expressions
    """
    unit = ml.val(lambda v: v)
    is_even = ml.val(lambda v: v % 2 == 0)
    mul = ml.val(lambda args: args[0] * args[1])
    superscript = ml.val(lambda num, power: num**power)
    get_month = ml.val(lambda value: value.month)
    is_num = ml.val(lambda v: isinstance(v, (int, float)))
    is_exp = ml.val(lambda v: isinstance(v, BaseException))
    is_zero_or_less = ml.val(lambda v, *args: v <= 0)
    if_else = lambda check=unit, do=unit, else_do=unit: ml.val(
        lambda *args, **kwargs: (
            ml.match(check(*args, **kwargs))
            .case(True, do=lambda: do(*args, **kwargs))
            .case(False, do=lambda: else_do(*args, **kwargs))
        )()
    )
```

### Compose Some High Order Expressions

Here we combine the primitive expressions into more complex ones using:

- normal function calls e.g. `if_else(some_stuff)` where `if_else` is a primitive expression
- pipelines using the pipeline operator (`>>`).
  Pipelines let one start with data followed by the steps that operate on that
  data e.g. `output = records >> remove_nulls >> parse_json >> ml.execute()`
- chaining primitives that have methods on their outputs that return expressions.
  e.g. `output = ml.match(data).case(1, do=...).case(2, do=...).case(3, ...)`

We can combine these complex expressions into even more complex ones to infinite complexity.

!!! info
    That is the main thing about functional programming i.e. composing simpler functions into more complex functions 
    to an indefinite level of complexity BUT while keeping the complex functions readable and predictable (pure).

In our `main` function in our script `main.py`, let's add the following high order expressions.

```python
    """
    High Order Expressions
    """
    accum_factorial = if_else(
        check=is_zero_or_less,
        do=lambda v, ac: ac,
        else_do=lambda v, ac: accum_factorial(v - 1, v * ac),
    )
    cube = ml.val(lambda v: superscript(v, 3))
    factorial = ml.val(lambda x: accum_factorial(x, 1))
    get_item_types = ml.ireduce(lambda x, y: f"{type(x)}, {type(y)}")
    nums_type_err = ml.val(
        lambda args: TypeError(f"expected numbers, got {get_item_types(args)}")
    )
    is_seq_of_nums = ml.ireduce(lambda x, y: x and is_num(y), True)
    to_result = ml.val(lambda v: ml.Result.ERR(v) if is_exp(v) else ml.Result.OK(v))

    try_multiply = (
        if_else(check=is_seq_of_nums, do=mul, else_do=nums_type_err) >> to_result
    )

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
```

## Add the Data to Work On

We have a number of data types that are work well with FunML

- IList: an immutable list, with pattern matching enabled 
- Enum: an enumerable data type, with pattern matching enabled
- Record: a record-like data type, with pattern matching enabled

Using our High order expressions (and primitive ones, your choice), we operate on the data.

In order to add data variables to pipelines, we turn them into expressions using `ml.val`
e.g. `ml.val(90)` becomes an expression that evaluates to `lambda: 90`.

Remember, when evaluating pipelines, we start with the data, then the steps of transformation
it has to go through.

Let's add some data to the `main` function in our script `main.py`.

```python
    """
    Data
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
```

## Create Some Pipelines and Execute Them

To construct pipelines, we use `>>` starting with an expression or data wrapped in `ml.val`.

!!! note
    If we don't add data before the pipeline, we will have to add it in another step later.

!!! info
    We prefer putting data before transformations in pipelines because it is more readable (_usually_).

    However, you might discover that it is also possible to save a pipeline and invoke it on the data like a normal function.

    Try not to do that.

Pipelines move data from left to right, transforming it from one step to the next.

Pipelines are lazily evaluated. To evaluate/execute a pipeline, we add `ml.execute()` as the last step of the pipeline.
This transforms the inputs into some output and returns the output.

Otherwise, we can keep adding steps to such a pipeline across different sections of the code.

Alright, let's create and evaluate some pipelines.

```python
    dates_as_enums = dates >> ml.imap(to_date_enum) >> ml.execute()
    print(f"\ndates as enums: {dates_as_enums}")

    print(f"\nfirst date enum: {dates_as_enums[0]}")

    months_as_str = dates >> ml.imap(get_month_str) >> ml.execute()
    print(f"\nmonths of dates as str:\n{months_as_str}")

    print(f"\ncube of 5: {cube(5)}")

    even_nums_pipeline = nums >> ml.ifilter(is_even)
    # here `even_nums_pipeline` is a `Pipeline` instance
    print(even_nums_pipeline)

    factorials_list = (
        copy(even_nums_pipeline)
        >> ml.imap(lambda v: f"factorial for {v}: {factorial(v)}")
        >> ml.execute()
    )
    # we created a new pipeline by coping the previous one
    # otherwise we would be mutating the old pipeline.
    # Calling ml.execute(), we get an actual iterable of strings
    print(factorials_list)

    factorials_str = (
        even_nums_pipeline
        >> ml.imap(lambda v: f"factorial for {v}: {factorial(v)}")
        >> ml.ireduce(lambda x, y: f"{x}\n{y}")
        >> ml.execute()
    )
    # here after calling ml.execute(), we get one string as output
    print(factorials_str)

    print(f"blue: {blue}")

    data = ml.val(data) >> ml.imap(try_multiply) >> ml.execute()
    print(f"\nafter multiplication:\n{data}")

    data_as_options = ml.val(data) >> ml.imap(result_to_option) >> ml.execute()
    print(f"\ndata as options: {data_as_options}")

    data_as_actual_values = (
        ml.val(data) >> ml.ifilter(ml.is_ok) >> ml.imap(ml.if_ok(unit)) >> ml.execute()
    )
    print(f"\ndata as actual values: {data_as_actual_values}")
```

## Run the Script

To run the `main` function, we need to add the following code at the end of the `main.py` script.

```python
if __name__ == "__main__":
    main()
```

The final script should look like:

```Python
{!../docs_src/tutorial/main.py!}
```

And then run the script  in the terminal with:

<div class="termy">

```console
$ python main.py

dates as enums: [&lt;Date.March: (datetime.date(200, 3, 4),)&gt;, &lt;Date.January: (datetime.date(2009, 1, 16),)&gt;, &lt;Date.December: (datetime.date(1993, 12, 29),)&gt;, &lt;Date.October: (datetime.date(2004, 10, 13),)&gt;, &lt;Date.September: (datetime.date(2020, 9, 5),)&gt;, &lt;Date.May: (datetime.date(2004, 5, 7),)&gt;, &lt;Date.August: (datetime.date(1228, 8, 18),)&gt;]

first date enum: &lt;Date.March: (datetime.date(200, 3, 4),)&gt;

months of dates as str:
[MAR, JAN, DEC, OCT, SEP, MAY, AUG]

cube of 5: 125
&lt;funml.types.Pipeline object at 0x1039ce690&gt;
[factorial for 12: 479001600, factorial for 8: 40320, factorial for 6: 720]
factorial for 12: 479001600
factorial for 8: 40320
factorial for 6: 720
blue: {'r': 0, 'g': 0, 'b': 255, 'a': 1}

after multiplication:
[&lt;Result.OK: (6,)&gt;, &lt;Result.ERR: (TypeError("expected numbers, got &lt;class 'str'&gt;, &lt;class 'int'&gt;"),)&gt;, &lt;Result.ERR: (TypeError("expected numbers, got &lt;class 'int'&gt;, &lt;class 'str'&gt;"),)&gt;, &lt;Result.OK: (48.599999999999994,)&gt;]

data as options: [&lt;Option.SOME: (6,)&gt;, &lt;Option.NONE: ('NONE',)&gt;, &lt;Option.NONE: ('NONE',)&gt;, &lt;Option.SOME: (48.599999999999994,)&gt;]

data as actual values: [6, 48.599999999999994]
```
</div>
