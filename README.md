# funml

[![PyPI version](https://badge.fury.io/py/funml.svg)](https://badge.fury.io/py/funml) ![CI](https://github.com/sopherapps/funml/actions/workflows/CI.yml/badge.svg)

A collection of utilities to help write python as though it were an ML-kind of functional language like OCaml

**This is still a toy I am playing with. The API is very unstable. Use at your own risk.**

## Why

- Functional language expressiveness make writing, testing and reading code fun

## Features

- pattern matching
- destructing assignments (let {a, _} = door)
- [x] simpler function composition with function being defined as one would define a variable
- [x] piping 
- immutable compound and simple data types
- [x] enums 
- records
- [x] monads of Option, Result to express probably nothing or probably an error
- conditional expressions (e.g. if constructs that evaluate to values and can be used in assignments)
- implicit returns of the last expression 

## Dependencies

- [python 3.7+](https://docs.python.org/)

## Contributing

Contributions are welcome. The docs have to maintained, the code has to be made cleaner, more idiomatic and faster,
and there might be need for someone else to take over this repo in case I move on to other things. It happens!

Please look at the [CONTRIBUTIONS GUIDELINES](./CONTRIBUTING.md)

### How to Test

- Make sure you have [poetry](https://python-poetry.org/) installed.
- Clone the repo and enter its root folder

```shell
git clone https://github.com/sopherapps/funml.git && cd funml
```

- Install the dependencies

```shell
poetry install
```

- Run the tests command

```shell
pytest
```

## Benchmarks

TBD

## License

Licensed under both the [MIT License](./LICENSE-MIT)

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