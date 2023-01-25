# funml

A collection of utilities to help write python as though it were an ML-kind of functional language like OCaml

## What is Functional Programming

### 1. All About Pure Functions

Pure functions are those with no side effects i.e. the output of the function is a function of the inputs only.
Unpredictable things such as accessing the file system, the network, etc. or mutating the inputs are strictly avoided.

This is what makes the code obvious to the reader of the code. There are no hidden modifications of function inputs or
some delay waiting for a network or file system connection or an unexpected error from an attempted network connection.
  
Of course, we need to access the file system or the network in useful programs.
Usually, functional programs wrap such impure operations in obvious wrappers showing that
they have side effect.

For instance [Ocaml](https://ocaml.org/docs/first-hour#imperative-ocaml) supports some imperative language constructs
specifically to handle this kind of real-life imperative operations.

### 2. Programs Compose Functions From Other Functions

Programs are generated from composing multiple functions together.
  
For instance:

```python
add = lambda x, y: x+y 
add70 = lambda x: add(x, 70)

basic_factorial = lambda x: 1 if x <= 0 else x * basic_factorial(x-1)
# tail recursive -- easier for compiler to optimise
accum_factorial = lambda x, ac: ac if x <= 0 else accum_factorial(x-1, x*ac)
factorial = lambda x: accum_factorial(x, 1)
```

### 3. Data is Immutable

In order to ensure functions do not mutate their inputs, the data used once initialized cannot be changed.

## Why Functional Programming

1. Writing programs in a functional-style is really, really intuitive.
2. The automated tests one writes for a functional-style program end up being small
3. Reading functional-style source code is easy because functions are obvious.
4. Due to data being immutable, it is easy to make concurrent programs. 
  [Erlang](https://www.erlang.org/) maximizes this advantage, together with a few other concepts to 
  make really huge concurrent programs.

## Notable Features of funml

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

### Installation
<div class="termy">

```console
$ pip install funml

---> 100%
```
</div>

### Example

#### Create a module

- Create a file `main.py` with:

```Python
{!../docs_src/index/main.py!}
```

#### Run it

Run the example with:

<div class="termy">

```console
$ python main.py

dates as enums: [<Date.March: (datetime.date(200, 3, 4),)>, <Date.January: (datetime.date(2009, 1, 16),)>, <Date.December: (datetime.date(1993, 12, 29),)>, <Date.October: (datetime.date(2004, 10, 13),)>, <Date.September: (datetime.date(2020, 9, 5),)>, <Date.May: (datetime.date(2004, 5, 7),)>, <Date.August: (datetime.date(1228, 8, 18),)>]

first date enum: <Date.March: (datetime.date(200, 3, 4),)>

months of dates as str:
[MAR, JAN, DEC, OCT, SEP, MAY, AUG]

cube of 5: 125
factorial for 12: 479001600
factorial for 8: 40320
factorial for 6: 720
blue: {'r': 0, 'g': 0, 'b': 255, 'a': 1}

after multiplication:
[<Result.OK: (6,)>, <Result.ERR: (TypeError("expected numbers, got <class 'str'>, <class 'int'>"),)>, <Result.ERR: (TypeError("expected numbers, got <class 'int'>, <class 'str'>"),)>, <Result.OK: (48.599999999999994,)>]

data as options: [<Option.SOME: (6,)>, <Option.NONE: ('NONE',)>, <Option.NONE: ('NONE',)>, <Option.SOME: (48.599999999999994,)>]
```
</div>
