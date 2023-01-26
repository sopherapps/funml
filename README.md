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

## Contributing

Contributions are welcome. The docs have to maintained, the code has to be made cleaner, more idiomatic and faster,
and there might be need for someone else to take over this repo in case I move on to other things. It happens!

Please look at the [CONTRIBUTIONS GUIDELINES](./CONTRIBUTING.md)

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