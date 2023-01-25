from datetime import date
from typing import Any

from funml import let, enum, record, Option, Result, match, l, val


def main():
    """Main program"""
    # define some data types
    Date = (
        enum("Date")
        .opt("January", shape=date)
        .opt("February", shape=date)
        .opt("March", shape=date)
        .opt("April", shape=date)
        .opt("May", shape=date)
        .opt("June", shape=date)
        .opt("July", shape=date)
        .opt("August", shape=date)
        .opt("September", shape=date)
        .opt("October", shape=date)
        .opt("November", shape=date)
        .opt("December", shape=date)
    )
    Color = record({"r": int, "g": int, "b": int, "a": int})

    # defining a number of functions
    is_even = lambda v: v % 2 == 0
    is_not_number = lambda v: not isinstance(v, (int, float))
    multiply = lambda x, y: x * y
    superscript = lambda num, power: num**power
    accumulated_factorial = (
        lambda num, accum: accum
        if num <= 0
        else accumulated_factorial(num - 1, num * accum)
    )
    get_month = lambda value: value.month

    # Result
    get_type_str = lambda v: f"{type(v)}"
    make_type_err = lambda *args: Result.ERR(
        TypeError(f"expected numbers, got {', '.join(l(*args).map(get_type_str))}")
    )
    try_multiply = (
        lambda x, y: make_type_err(x, y)
        if any(l(x, y).map(is_not_number))
        else Result.OK(multiply(x, y))
    )

    # Option
    result_to_option = (
        match()
        .case(Result.ERR(Exception), do=lambda: Option.NONE)
        .case(Result.OK(Any), do=lambda v: Option.SOME(v))
    )

    # some pattern matching
    to_date_enum = lambda date_value: (
        match(date_value.month)
        .case(
            1,
            do=lambda: Date.January(date_value),
        )
        .case(
            2,
            do=lambda: Date.February(date_value),
        )
        .case(
            3,
            do=lambda: Date.March(date_value),
        )
        .case(
            4,
            do=lambda: Date.April(date_value),
        )
        .case(
            5,
            do=lambda: Date.May(date_value),
        )
        .case(
            6,
            do=lambda: Date.June(date_value),
        )
        .case(
            7,
            do=lambda: Date.July(date_value),
        )
        .case(
            8,
            do=lambda: Date.August(date_value),
        )
        .case(
            9,
            do=lambda: Date.September(date_value),
        )
        .case(
            10,
            do=lambda: Date.October(date_value),
        )
        .case(
            11,
            do=lambda: Date.November(date_value),
        )
        .case(
            12,
            do=lambda: Date.December(date_value),
        )
    )()

    # combine a number of functions into bigger ones
    cube = let(int, power=3) >> superscript
    factorial = let(int, accum=1) >> accumulated_factorial
    get_month_str = val(get_month) >> (
        match()
        .case(1, do=lambda: "JAN")
        .case(2, do=lambda: "FEB")
        .case(3, do=lambda: "MAR")
        .case(4, do=lambda: "APR")
        .case(5, do=lambda: "MAY")
        .case(6, do=lambda: "JUN")
        .case(7, do=lambda: "JUL")
        .case(8, do=lambda: "AUG")
        .case(9, do=lambda: "SEP")
        .case(10, do=lambda: "OCT")
        .case(11, do=lambda: "NOV")
        .case(12, do=lambda: "DEC")
    )

    dates = [
        date(200, 3, 4),
        date(2009, 1, 16),
        date(1993, 12, 29),
        date(2004, 10, 13),
        date(2020, 9, 5),
        date(2004, 5, 7),
        date(1228, 8, 18),
    ]

    nums = l(12, 3, 45, 7, 80, 6, 3)

    dates_as_enums = l(*dates).map(to_date_enum)
    print(f"\ndates as enums: {dates_as_enums}")

    print(f"\nfirst date enum: {dates_as_enums[0]}")

    months_as_str = l(*dates).map(get_month_str)
    print(f"\nmonths of dates as str:\n{months_as_str}")

    print(f"\ncube of 5: {cube(5)}")

    factorials_str = nums.filter(is_even).map(
        lambda v: f"factorial for {v}: {factorial(v)}"
    )
    print("\n".join(factorials_str))

    blue = Color(r=0, g=0, b=255, a=1)
    print(f"blue: {blue}")

    data = l((2, 3), ("hey", 7), (5, "y"), (8.1, 6)).map(lambda x: try_multiply(*x))
    print(f"\nafter multiplication:\n{data}")

    data_as_options = data.map(result_to_option)
    print(f"\ndata as options: {data_as_options}")


if __name__ == "__main__":
    main()